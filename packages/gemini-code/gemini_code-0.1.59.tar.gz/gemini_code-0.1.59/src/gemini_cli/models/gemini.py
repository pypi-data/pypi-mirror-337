"""
Gemini model integration for the CLI tool.
Targeting Gemini 2.5 Pro Experimental.
AGENTIC LOOP (CODE GENERATION) with FORCED ORIENTATION.
ALLOWING MULTIPLE TOOL CALLS PER TURN. Status removed for clarity.
Prompt v11.2 (Batch Info). Syntax FIXED.
"""

import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool
import re
import json
import logging
import ast
import shlex
import time
from rich.console import Console

from ..utils import count_tokens
from ..tools import get_tool, AVAILABLE_TOOLS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

TOOL_CALL_PATTERN = re.compile(r"cli_tools\.(\w+)\s*\((.*?)\)", re.DOTALL | re.MULTILINE)
TASK_COMPLETE_PATTERN = re.compile(r"#\s*Task Complete", re.IGNORECASE)
MAX_AGENT_ITERATIONS = 10

def list_available_models(api_key):
    # ... (Remains the same) ...
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models(); gemini_models = []
        for model in models:
            model_info = { "name": model.name, "display_name": model.display_name, "description": model.description, "supported_generation_methods": model.supported_generation_methods }
            gemini_models.append(model_info)
        return gemini_models
    except Exception as e: logging.error(f"Error listing models: {str(e)}"); return [{"error": str(e)}]


class GeminiModel:
    """Interface for Gemini models implementing an agentic loop with forced orientation."""

    def __init__(self, api_key: str, console: Console, model_name: str ="gemini-2.5-pro-exp-03-25"):
        """Initialize the Gemini model interface for agentic code generation."""
        self.api_key = api_key
        self.model_name = model_name
        self.console = console
        genai.configure(api_key=api_key)

        self.generation_config = genai.types.GenerationConfig( temperature=0.4, top_p=0.95, top_k=40 )
        self.safety_settings = { "HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE", "HATE": "BLOCK_MEDIUM_AND_ABOVE", "SEXUAL": "BLOCK_MEDIUM_AND_ABOVE", "DANGEROUS": "BLOCK_MEDIUM_AND_ABOVE" }
        _ = self._create_tool_definitions() # Syntax check only
        # Use the v11.2 prompt encouraging batch info gathering
        self.system_instruction = self._create_system_prompt()

        try:
            logging.info(f"Creating model: {self.model_name} for Agentic Loop w/ Orientation.")
            self.model = genai.GenerativeModel( model_name=self.model_name, generation_config=self.generation_config, safety_settings=self.safety_settings, system_instruction=self.system_instruction )
            logging.info("GeminiModel initialized successfully (Forced Orientation Agent Loop).")
        except Exception as e:
             logging.error(f"Fatal error initializing Gemini model '{self.model_name}': {str(e)}", exc_info=True); raise Exception(f"Could not initialize Gemini model: {e}") from e

    # ... (get_available_models remains the same) ...
    def get_available_models(self): return list_available_models(self.api_key)

    # --- generate function for Forced Orientation Agentic Loop (Multiple Calls Allowed) ---
    def generate(self, prompt: str, conversation=None) -> str | None:
        logging.info(f"Agent Loop w/ Orientation - Starting task for prompt: '{prompt[:100]}...'")
        original_user_prompt = prompt
        if prompt.startswith('/'):
             command = prompt.split()[0].lower()
             if command in ['/exit', '/help', '/compact']: logging.info(f"Handled command: {command}"); return None

        # === Step 1: Mandatory Orientation ===
        orientation_context = ""; ls_result = "(ls tool not found or failed)"
        try:
            logging.info("Performing mandatory orientation (ls)...")
            ls_tool = get_tool("ls")
            if ls_tool: ls_result = ls_tool.execute()
            else: logging.warning("Could not find 'ls' tool for mandatory orientation.")
            self.console.print(f"[dim]Directory context acquired.[/dim]") # Simplified confirmation
            orientation_context = f"Current directory contents (from `ls .`):\n```\n{ls_result}\n```\n"
            logging.info("Orientation successful.")
        except Exception as orient_error:
            logging.error(f"Error during mandatory orientation: {orient_error}", exc_info=True)
            orientation_context = f"Error during initial directory scan: {orient_error}\n"
            self.console.print(f"[red]Error getting directory listing: {orient_error}[/red]")

        # === Step 2: Initialize History and Start Agent Loop ===
        current_task_history = [
            {'role': 'user', 'parts': [self.system_instruction]},
            {'role': 'user', 'parts': [f"{orientation_context}\nUser request: {original_user_prompt}\n\nBased on the directory contents and the request, generate the Python code for the initial necessary action(s) using `cli_tools.X(...)`. If info gathering is needed (`view`, `ls`, `glob`), generate *all* such calls first. If ready for action, generate the first `edit`/`bash` call. If no action needed, respond with '# Task Complete'."]}
        ]
        full_log = [f"System (Orientation):\n{orientation_context}", f"User: {original_user_prompt}"]
        iteration_count = 0; task_completed = False; last_llm_response_text = ""

        try:
            while iteration_count < MAX_AGENT_ITERATIONS:
                iteration_count += 1
                logging.info(f"Agent Loop Iteration {iteration_count}/{MAX_AGENT_ITERATIONS}")

                generated_text = ""; llm_response = None
                try:
                    # REMOVED internal status block
                    logging.info(f"Asking LLM ({self.model_name}) for next action(s)...")
                    llm_response = self.model.generate_content( current_task_history, generation_config=self.generation_config )
                    logging.debug(f"RAW Gemini Response Object (Iter {iteration_count}): {llm_response}")
                    generated_text = self._extract_text_from_response(llm_response)
                except Exception as generation_error:
                     logging.error(f"Error during LLM generation: {generation_error}", exc_info=True)
                     error_text = self._extract_text_from_response(llm_response) if llm_response else f"Generation Error: {generation_error}"
                     if "(Response blocked" in error_text or "(Prompt blocked" in error_text or "(Response generation incomplete" in error_text: self.console.print(f"[bold red]{error_text}[/bold red]"); return f"LLM Error: {error_text}"
                     return f"Error during LLM generation step: {generation_error}"

                last_llm_response_text = generated_text
                logging.info(f"LLM suggested action/code (Iter {iteration_count}):\n---\n{generated_text}\n---")
                current_task_history.append({'role': 'model', 'parts': [generated_text]})
                full_log.append(f"Assistant (Code Gen - Iter {iteration_count}):\n{generated_text}")

                if TASK_COMPLETE_PATTERN.search(generated_text): logging.info("Task completion signal detected."); task_completed = True; break

                # === Parse and Execute Tool Calls (EXECUTES ALL FOUND CALLS) ===
                tool_calls_executed = self._parse_and_execute_tool_calls(generated_text) # Reverted name

                if not tool_calls_executed:
                    logging.warning(f"No tool calls found/executed in LLM response (Iter {iteration_count}), and no completion signal. Assuming finished/stuck.")
                    if iteration_count > 0: task_completed = True; break
                    task_completed = True; break

                # === Prepare Results Feedback (Handles multiple results) ===
                results_feedback = "Executed tool calls. Results:\n\n"; any_errors = False
                for call_info in tool_calls_executed:
                     results_feedback += f"Call: {call_info['call_str']}\n"; results_feedback += f"Result: ```\n{call_info['result']}\n```\n---\n"
                     if "Error" in call_info['result']: any_errors = True
                # Adjusted feedback prompt slightly
                results_feedback += "\nBased on these results, what is the next `cli_tools.X(...)` action needed (usually only ONE action now, like edit or bash), or is the task complete (respond with '# Task Complete')?"

                current_task_history.append({'role': 'user', 'parts': [results_feedback]})
                full_log.append(f"System (Tool Results - Iter {iteration_count}):\n{results_feedback.splitlines()[0]}...")

                if any_errors: logging.warning("Errors occurred during tool execution. Loop will continue.")

            # === End Agent Loop ===

            # === Final Summary Generation ===
            final_summary = ""
            # REMOVED internal status block
            if task_completed:
                completion_text_only = TASK_COMPLETE_PATTERN.sub('', last_llm_response_text).strip()
                if completion_text_only and len(completion_text_only) > 10: final_summary = completion_text_only; logging.info("Using text before completion signal as final summary.")
                else:
                     logging.info("Task loop finished. Requesting final summary...")
                     summary_request = "The task is marked complete. Please provide a concise final summary for the user based on the conversation history, describing the actions taken and the overall outcome."
                     final_response = self.model.generate_content(current_task_history + [{'role':'user', 'parts':[summary_request]}])
                     logging.debug(f"RAW Gemini Response Object (Summary): {final_response}")
                     final_summary = self._extract_text_from_response(final_response); logging.info("Received final summary.")
            else:
                 logging.warning(f"Agent loop terminated after reaching max iterations ({MAX_AGENT_ITERATIONS}). Requesting summary of progress.")
                 timeout_summary_request = f"Reached max iterations ({MAX_AGENT_ITERATIONS}). Please summarize progress and any issues based on the history."
                 final_response = self.model.generate_content(current_task_history + [{'role':'user', 'parts':[timeout_summary_request]}])
                 final_summary = f"(Task exceeded max iterations)\n{self._extract_text_from_response(final_response).strip()}"

            cleaned_summary = self._cleanup_internal_tags(final_summary)
            return cleaned_summary.strip()

        except Exception as e:
             logging.error(f"Error during Agent Loop: {str(e)}", exc_info=True); return f"An unexpected error occurred during the agent process: {str(e)}"


    # --- RENAMED BACK and MODIFIED to execute ALL found calls ---
    def _parse_and_execute_tool_calls(self, text: str) -> list[dict]:
        """Finds, parses, and executes ALL valid `cli_tools.X(...)` calls in text."""
        executed_calls = []
        matches = TOOL_CALL_PATTERN.finditer(text)
        any_matches = False

        for match in matches: # Loop through ALL matches found
            any_matches = True
            call_str = match.group(0); func_name = match.group(1); args_str = match.group(2).strip()
            logging.info(f"Found potential tool call: cli_tools.{func_name}({args_str[:100]}...)")
            args = {}

            # --- Argument Parsing ---
            try:
                full_call_for_ast = f"f({args_str})"
                logging.debug(f"Attempting to parse AST for: {full_call_for_ast[:200]}...")
                node = ast.parse(full_call_for_ast, mode='eval'); call_node = node.body
                if not isinstance(call_node, ast.Call): raise SyntaxError("Parsed args string not a call structure")
                for kw in call_node.keywords:
                    arg_name = kw.arg; value_node = kw.value
                    try: args[arg_name] = ast.literal_eval(value_node); logging.debug(f"Parsed arg '{arg_name}' using literal_eval")
                    except ValueError:
                        # ... (Robust parsing logic remains same) ...
                        if isinstance(value_node, ast.Constant) and isinstance(value_node.value, str): args[arg_name] = value_node.value; logging.debug(f"Parsed arg '{arg_name}' as Constant string")
                        elif hasattr(value_node, 's'): args[arg_name] = value_node.s; logging.debug(f"Parsed arg '{arg_name}' using fallback .s attribute")
                        else:
                            try:
                                 import io; from ast import unparse; f = io.StringIO(); unparse(value_node, f); reconstructed_value = f.getvalue().strip()
                                 logging.warning(f"Could not literal_eval arg '{arg_name}'. Reconstructed: {reconstructed_value[:100]}...")
                                 if reconstructed_value.startswith(('"', "'")):
                                      try: args[arg_name] = ast.literal_eval(reconstructed_value)
                                      except Exception: logging.error(f"Failed literal_eval on reconstructed '{arg_name}'. Skipping arg."); continue # Skip only this arg
                                 else: logging.error(f"Reconstructed value for '{arg_name}' not safe literal. Skipping arg."); continue
                            except ImportError: logging.error(f"ast.unparse required (Py3.9+). Skipping complex arg '{arg_name}'."); continue
                            except Exception as unparse_err: logging.error(f"Error reconstructing source for arg '{arg_name}': {unparse_err}. Skipping arg."); continue

            except Exception as parse_error:
                logging.error(f"Arg parse failed for '{call_str}': {parse_error}", exc_info=True)
                executed_calls.append({ "call_str": call_str, "result": f"Error: Failed to parse arguments - {parse_error}" })
                continue # Process next match even if this one failed parsing

            # --- Execute current successfully parsed call ---
            try:
                result_str = "(Execution failed)"
                # REMOVED status block here
                logging.info(f"Executing parsed call: func='{func_name}', args={ {k: (v[:50] + '...' if isinstance(v, str) and len(v)>50 else v) for k,v in args.items()} })")
                # Optional: Print simple confirmation
                self.console.print(f"[dim] -> Executing {func_name} ({args.get('file_path', args.get('command', '...'))[:30]}...)[/dim]")
                tool_instance = get_tool(func_name)
                if not tool_instance: raise ValueError(f"Tool '{func_name}' is not available.")
                result = tool_instance.execute(**args)
                result_str = str(result) if result is not None else "(No output)"
                # Append success result
                executed_calls.append({ "call_str": call_str, "result": result_str })
                logging.info(f"Execution successful for '{call_str}'. Result length: {len(result_str)}")
                # NO BREAK HERE - ALLOW LOOP TO CONTINUE TO NEXT MATCH

            except Exception as exec_error:
                logging.error(f"Exception during execution of '{call_str}': {exec_error}", exc_info=True)
                # Append execution error result
                executed_calls.append({ "call_str": call_str, "result": f"Error during execution: {exec_error}" })
                # NO BREAK HERE - ALLOW LOOP TO CONTINUE TO NEXT MATCH (maybe next tool call is independent?)

        if not any_matches: logging.info("No parsable cli_tools calls found in the generated text.")
        return executed_calls # Return list containing results for ALL calls attempted


    # ... (_extract_text_from_response remains the same) ...
    def _extract_text_from_response(self, response):
        try:
            all_text = []
            if response.candidates:
                 if response.candidates[0].finish_reason.name != "STOP":
                     logging.warning(f"Response generation stopped due to: {response.candidates[0].finish_reason.name}")
                     if response.candidates[0].safety_ratings: ratings = {r.category.name: r.probability.name for r in response.candidates[0].safety_ratings}; return f"(Response blocked due to safety settings: {ratings})"
                     return f"(Response generation incomplete: {response.candidates[0].finish_reason.name})"
                 for part in response.candidates[0].content.parts:
                     if hasattr(part, 'text'): all_text.append(part.text)
                 return "".join(all_text)
            elif hasattr(response, 'text'): return response.text
            elif response.prompt_feedback and response.prompt_feedback.block_reason: logging.warning(f"Prompt blocked due to: {response.prompt_feedback.block_reason.name}"); return f"(Prompt blocked due to: {response.prompt_feedback.block_reason.name})"
            else: logging.warning("Could not extract text from response structure."); return ""
        except Exception as e: logging.error(f"Error extracting text: {e}", exc_info=True); return f"Error extracting response text: {e}"

    # ... (_cleanup_internal_tags remains the same) ...
    def _cleanup_internal_tags(self, text: str) -> str:
        text = re.sub(r"<thinking>.*?</thinking>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"<plan>.*?</plan>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"# Thinking:.*?\n", "", text)
        text = re.sub(r"# Plan:.*?\n", "", text)
        return text.strip()

    # --- V11.2 Prompt: Agentic Loop + Batch Info Gathering ---
    def _create_system_prompt(self) -> str:
        """Creates the system instruction prompt for the agentic loop, encouraging initial info batching."""
        tools_description = []
        if AVAILABLE_TOOLS:
            for name, tool_class in AVAILABLE_TOOLS.items():
                try:
                    tool_instance = tool_class(); desc = getattr(tool_instance, 'description', f'Tool {name}')
                    param_hints = []
                    # ...(same param hint logic as before)...
                    if name == 'edit': param_hints = ["file_path='path/to/file.ext'", "content='FULL FILE CONTENT' (for create/overwrite)", "old_string='text_to_find', new_string='replacement_text' (for replacing)"]
                    elif name == 'view': param_hints = ["file_path='path/to/file.ext'", "offset=Optional[int]", "limit=Optional[int]"]
                    elif name == 'ls': param_hints = ["path='.'", "ignore='Optional[str]'"]
                    elif name == 'grep': param_hints = ["pattern='regex_pattern'", "path='.'", "include='*.py'"]
                    elif name == 'glob': param_hints = ["pattern='**/*.py'", "path='.'"]
                    elif name == 'bash': param_hints = ["command='shell command string'"]
                    elif name == 'test_runner': param_hints = ["test_path='Optional[str]'", "options='Optional[str]'", "runner_command='pytest'"]
                    else: param_hints = ["..."]
                    tools_description.append(f"`cli_tools.{name}({', '.join(param_hints)})`: {desc}")
                except Exception as e: logging.warning(f"Could not get description/params for tool '{name}': {e}"); tools_description.append(f"`cli_tools.{name}(...)`: Tool to {name} files/system.")
        else: logging.warning("AVAILABLE_TOOLS dictionary not found or empty.")

        system_prompt = f"""You are 'Gemini Code', an AI coding assistant operating in a CLI within the user's project directory. **Your ONLY way to interact with the environment is by generating Python code snippets that call functions from the `cli_tools` module.**

**Your Goal:** Achieve the user's request by generating a sequence of `cli_tools` calls.

**Workflow:**

1.  **Receive Context:** You will receive the user's request and the current directory listing.
2.  **Plan & Generate Initial Actions:** Analyze request and context. **Generate Python code for ALL INITIAL information gathering (`cli_tools.view`, `cli_tools.ls`, `cli_tools.glob`) you anticipate needing in ONE code block.** If no info gathering is needed, generate the first *action* (`cli_tools.edit`, `cli_tools.bash`, etc.) instead. Use comments (`# Thinking:`) for reasoning.
3.  **Receive Results:** The CLI will execute your code (potentially multiple calls from the first block) and provide results.
4.  **Reflect & Generate Next Action (or Finish):** Analyze results. If more steps needed, generate code for the *next single action* (usually `edit`, `bash`, or `test_runner`). If task complete, output **ONLY** `# Task Complete`. Handle errors.
5.  **Repeat:** Continue executing single actions until completion.
6.  **Summarize (Final Step):** After completion signal, provide a concise summary.

**CRITICAL INSTRUCTIONS:**
*   **OUTPUT ONLY PYTHON CODE (or # Task Complete):** Your output MUST be *either* valid Python code calling `cli_tools` functions *or* the exact line `# Task Complete`. No conversational text unless in comments.
*   **USE `cli_tools`:** Prefix all calls with `cli_tools.`.
*   **BATCH INITIAL INFO GATHERING:** Generate all needed `view`/`ls`/`glob` calls together in your first response if possible. Subsequent responses should focus on ONE action (`edit`, `bash`, etc.).
*   **STRINGS MUST BE QUOTED:** Use quotes correctly, triple quotes for multiline. Use keyword arguments.
*   **`edit` Tool Usage:** Use `content='...'` for create/overwrite OR `old_string`/`new_string` for replace. Not both.
*   **HANDLE RESULTS:** Use provided results for next step.

**Available `cli_tools` Functions (Examples - Parameters might vary):**
{chr(10).join(tools_description) if tools_description else "No `cli_tools` functions available."}

You will now receive the initial context (directory listing and user request). Generate the Python code for the initial information gathering or the first action.
"""
        return system_prompt


        # --- CORRECTED _create_tool_definitions Method (Syntax ABSOLUTELY, POSITIVELY FIXED) ---
    def _create_tool_definitions(self) -> list[Tool]:
        """Native tool definitions - NOT CURRENTLY USED but needs correct syntax for import."""
        tool_declarations = [] # Holds FunctionDeclaration objects

        # --- Define the view tool ---
        if "view" in AVAILABLE_TOOLS:
            # CORRECT: try is on a new line, indented
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="view",
                    description="View the contents of a specific file.",
                    parameters={ "type": "object", "properties": {
                            "file_path": {"type": "string", "description": "Path to the file to view."},
                            "offset": {"type": "integer", "description": "Line number to start reading from (1-based index, optional)."},
                            "limit": {"type": "integer", "description": "Maximum number of lines to read (optional)."}
                        }, "required": ["file_path"] }
                ))
            # CORRECT: except is aligned with try
            except Exception as e:
                logging.error(f"Failed to define 'view' tool: {e}")

        # --- Define the edit tool ---
        if "edit" in AVAILABLE_TOOLS:
            # CORRECT: try is on a new line, indented
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="edit",
                    description="Edit a file: create it, replace its content, replace a specific string, or delete a string.",
                    parameters={ "type": "object", "properties": {
                            "file_path": {"type": "string", "description": "Path to the file to edit or create."},
                            "new_content": {"type": "string", "description": "Full content for a new file or to completely overwrite an existing file. Use if `old_string` is omitted."},
                            "old_string": {"type": "string", "description": "The exact text to find and replace. If omitted, `new_content` overwrites the file."},
                            "new_string": {"type": "string", "description": "Text to replace `old_string` with. If replacing, this is required. Use an empty string ('') to delete `old_string`."}
                        }, "required": ["file_path"] }
                ))
            # CORRECT: except is aligned with try
            except Exception as e:
                logging.error(f"Failed to define 'edit' tool: {e}")

        # --- Define the ls tool ---
        if "ls" in AVAILABLE_TOOLS:
            # CORRECT: try is on a new line, indented
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="ls",
                    description="List files and directories in a given path.",
                    parameters={ "type": "object", "properties": {
                            "path": {"type": "string", "description": "Directory path to list (default: current directory '.')."},
                            "ignore": {"type": "string", "description": "Comma-separated glob patterns to ignore (e.g., '*.pyc,__pycache__'). Optional."}
                        }}
                ))
            # CORRECT: except is aligned with try
            except Exception as e:
                logging.error(f"Failed to define 'ls' tool: {e}")

        # --- Define the grep tool ---
        if "grep" in AVAILABLE_TOOLS:
            # CORRECT: try is on a new line, indented
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="grep",
                    description="Search for a pattern (regex) in files within a directory.",
                    parameters={ "type": "object", "properties": {
                            "pattern": {"type": "string", "description": "Regular expression pattern to search for."},
                            "path": {"type": "string", "description": "Directory path to search within (default: '.'). Optional."},
                            "include": {"type": "string", "description": "Glob pattern for files to include (e.g., '*.py', '*.txt'). Searches all files if omitted. Optional."}
                        }, "required": ["pattern"] }
                ))
            # CORRECT: except is aligned with try
            except Exception as e:
                logging.error(f"Failed to define 'grep' tool: {e}")

        # --- Define the glob tool ---
        if "glob" in AVAILABLE_TOOLS:
            # CORRECT: try is on a new line, indented
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="glob",
                    description="Find files matching specific glob patterns recursively.",
                    parameters={ "type": "object", "properties": {
                            "pattern": {"type": "string", "description": "Glob pattern to match (e.g., '**/*.py', 'docs/**/*.md')."},
                            "path": {"type": "string", "description": "Base directory path to search within (default: '.'). Optional."}
                        }, "required": ["pattern"] }
                ))
            # CORRECT: except is aligned with try
            except Exception as e:
                logging.error(f"Failed to define 'glob' tool: {e}")

        # --- Define the bash tool ---
        if "bash" in AVAILABLE_TOOLS:
            # CORRECT: try is on a new line, indented
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="bash",
                    description="Execute a shell command using the system's default shell.",
                    parameters={ "type": "object", "properties": {
                            "command": {"type": "string", "description": "The shell command string to execute."},
                            "timeout": {"type": "integer", "description": "Maximum execution time in seconds (optional)."}
                        }, "required": ["command"] }
                ))
            # CORRECT: except is aligned with try
            except Exception as e:
                logging.error(f"Failed to define 'bash' tool: {e}")

        # --- Define the test_runner tool ---
        if "test_runner" in AVAILABLE_TOOLS:
            # CORRECT: try is on a new line, indented
            try:
                test_runner_declaration = FunctionDeclaration(
                    name="test_runner",
                    description="Runs automated tests using the project's test runner (e.g., pytest).",
                    parameters={ "type": "object", "properties": {
                            "test_path": {"type": "string", "description": "Specific file or directory path to test (optional, runs discovered tests if omitted)."},
                            "options": {"type": "string", "description": "Additional command-line options for the test runner (e.g., '-k my_test', '-v', '--cov'). Optional."},
                            "runner_command": {"type": "string", "description": "The command for the test runner (default: 'pytest'). Optional."}
                        }}
                )
                tool_declarations.append(test_runner_declaration)
            # CORRECT: except is aligned with try
            except Exception as e:
                logging.error(f"Failed to define 'test_runner' tool: {e}")

        logging.debug("Native tool definitions parsed (syntax check only in Code Gen mode).")
        # Return empty list as we are not using native tools in Code Gen mode
        return []
    # --- End CORRECTED Method ---