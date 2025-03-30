"""
Gemini model integration for the CLI tool.
Targeting Gemini 2.5 Pro Experimental.
AGENTIC LOOP w/ FORCED ORIENTATION & TASK COMPLETE TOOL.
Includes SummarizeCodeTool, Quality tools. Prompt v13. Syntax FIXED.
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
# Import tool getter AND the specific class for special instantiation
from ..tools import get_tool, AVAILABLE_TOOLS
from ..tools.summarizer_tool import SummarizeCodeTool # Import class directly

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

TOOL_CALL_PATTERN = re.compile(r"cli_tools\.(\w+)\s*\((.*?)\)", re.DOTALL | re.MULTILINE)
TASK_COMPLETE_PATTERN = re.compile(r"#\s*Task Complete", re.IGNORECASE)
MAX_AGENT_ITERATIONS = 15

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
    """Interface for Gemini models implementing an agentic loop with TaskCompleteTool."""

    def __init__(self, api_key: str, console: Console, model_name: str ="gemini-2.5-pro-exp-03-25"):
        """Initialize the Gemini model interface for agentic code generation."""
        self.api_key = api_key
        self.model_name = model_name
        self.console = console
        genai.configure(api_key=api_key)

        self.generation_config = genai.types.GenerationConfig( temperature=0.4, top_p=0.95, top_k=40 )
        self.safety_settings = { "HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE", "HATE": "BLOCK_MEDIUM_AND_ABOVE", "SEXUAL": "BLOCK_MEDIUM_AND_ABOVE", "DANGEROUS": "BLOCK_MEDIUM_AND_ABOVE" }
        _ = self._create_tool_definitions() # Syntax check only
        # Use the V13 prompt explaining summarize_code tool
        self.system_instruction = self._create_system_prompt()

        try:
            logging.info(f"Creating model: {self.model_name} for Agentic Loop w/ Summarizer.")
            # Initialize self.model using helper BEFORE passing it to tools if needed
            # However, we instantiate SummarizeCodeTool inside the execute call now
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                system_instruction=self.system_instruction
            )
            logging.info("GeminiModel initialized successfully (TaskComplete Agent Loop w/ Summarizer).")
        except Exception as e:
             logging.error(f"Fatal error initializing Gemini model '{self.model_name}': {str(e)}", exc_info=True); raise Exception(f"Could not initialize Gemini model: {e}") from e

    def get_available_models(self):
        return list_available_models(self.api_key)

    # --- generate function for Agentic Loop with TaskCompleteTool ---
    def generate(self, prompt: str, conversation=None) -> str | None:
        # ... (generate function logic remains the same as previous TaskComplete version) ...
        logging.info(f"Agent Loop w/ Summarizer - Starting task: '{prompt[:100]}...'")
        original_user_prompt = prompt
        if prompt.startswith('/'):
             command = prompt.split()[0].lower()
             if command in ['/exit', '/help', '/compact']: logging.info(f"Handled command: {command}"); return None

        orientation_context = ""; ls_result = "(ls tool not found or failed)"
        try:
            logging.info("Performing mandatory orientation (ls)...")
            ls_tool = get_tool("ls") # Simple instantiation ok for ls
            if ls_tool: ls_result = ls_tool.execute()
            else: logging.warning("Could not find 'ls' tool for mandatory orientation.")
            self.console.print(f"[dim]Directory context acquired.[/dim]")
            orientation_context = f"Current directory contents (from `ls .`):\n```\n{ls_result}\n```\n"
            logging.info("Orientation successful.")
        except Exception as orient_error:
            logging.error(f"Error during mandatory orientation: {orient_error}", exc_info=True)
            orientation_context = f"Error during initial directory scan: {orient_error}\n"
            self.console.print(f"[red]Error getting directory listing: {orient_error}[/red]")

        current_task_history = [
            {'role': 'user', 'parts': [self.system_instruction]},
            {'role': 'user', 'parts': [f"{orientation_context}\nUser request: {original_user_prompt}\n\nBased on the directory contents and the request, generate the Python code for the first necessary action(s) using `cli_tools.X(...)`. If the task is already complete or requires no action, call `cli_tools.task_complete(summary='...')`."]}
        ]
        iteration_count = 0; task_completed = False; final_summary = None

        try:
            while iteration_count < MAX_AGENT_ITERATIONS:
                iteration_count += 1
                logging.info(f"Agent Loop Iteration {iteration_count}/{MAX_AGENT_ITERATIONS}")

                generated_text = ""; llm_response = None
                try:
                    logging.info(f"Asking LLM ({self.model_name}) for next action(s)...")
                    llm_response = self.model.generate_content( current_task_history, generation_config=self.generation_config )
                    logging.debug(f"RAW Gemini Response Object (Iter {iteration_count}): {llm_response}")
                    generated_text = self._extract_text_from_response(llm_response)
                except Exception as generation_error:
                     logging.error(f"Error during LLM generation: {generation_error}", exc_info=True)
                     error_text = self._extract_text_from_response(llm_response) if llm_response else f"Generation Error: {generation_error}"
                     if "(Response blocked" in error_text or "(Prompt blocked" in error_text or "(Response generation incomplete" in error_text: self.console.print(f"[bold red]{error_text}[/bold red]"); return f"LLM Error: {error_text}"
                     return f"Error during LLM generation step: {generation_error}"

                logging.info(f"LLM suggested action/code (Iter {iteration_count}):\n---\n{generated_text}\n---")
                current_task_history.append({'role': 'model', 'parts': [generated_text]})

                # === Parse and Execute Tool Calls (Handles Summarizer Instantiation) ===
                executed_tool_info = self._parse_and_execute_tool_calls(generated_text)

                if not executed_tool_info:
                    logging.warning(f"No tool calls found/executed in LLM response (Iter {iteration_count}). Task might be stuck.")
                    clarification_request = "You did not provide any tool calls or a completion signal. Please either provide the next `cli_tools.X(...)` call or signal completion with `cli_tools.task_complete(summary='...')`."
                    current_task_history.append({'role': 'user', 'parts': [clarification_request]})
                    continue

                # === Check for Task Completion Signal ===
                for tool_name, result_data in executed_tool_info:
                    if tool_name == "task_complete":
                        logging.info("Task completion signaled by task_complete tool call.")
                        task_completed = True
                        final_summary = result_data.get("result", "Task completed, but summary extraction failed.")
                        break
                if task_completed: break

                # === Prepare Results Feedback ===
                results_feedback = "Executed tool calls. Results:\n\n"; any_errors = False
                for tool_name, result_data in executed_tool_info:
                     call_str = result_data.get('call_str', f'cli_tools.{tool_name}(...)')
                     result = result_data.get('result', '(No result captured)')
                     results_feedback += f"Call: `{call_str}`\n"; results_feedback += f"Result: ```\n{result}\n```\n---\n"
                     if "Error" in str(result): any_errors = True
                results_feedback += "\nBased on these results, what is the next `cli_tools.X(...)` action needed, or call `cli_tools.task_complete(summary='...')` if finished?"
                current_task_history.append({'role': 'user', 'parts': [results_feedback]})

                if any_errors: logging.warning("Errors occurred during tool execution. Loop will continue.")

            # === End Agent Loop ===

            # === Handle Output ===
            if task_completed and final_summary:
                 logging.info("Task completed successfully via task_complete tool.")
                 cleaned_summary = self._cleanup_internal_tags(final_summary)
                 return cleaned_summary.strip()
            elif iteration_count >= MAX_AGENT_ITERATIONS:
                 logging.warning(f"Agent loop terminated after reaching max iterations ({MAX_AGENT_ITERATIONS}).")
                 timeout_summary_request = f"Reached max iterations ({MAX_AGENT_ITERATIONS}). Please provide a concise final summary based on the history."
                 final_response = self.model.generate_content(current_task_history + [{'role':'user', 'parts':[timeout_summary_request]}])
                 final_summary = f"(Task exceeded max iterations)\n{self._extract_text_from_response(final_response).strip()}"
                 return self._cleanup_internal_tags(final_summary).strip()
            else:
                 logging.error("Agent loop exited without task_complete signal or reaching max iterations.")
                 return "Error: Agent loop finished unexpectedly."

        except Exception as e:
             logging.error(f"Error during Agent Loop: {str(e)}", exc_info=True); return f"An unexpected error occurred during the agent process: {str(e)}"


    # --- UPDATED _parse_and_execute_tool_calls for Summarizer ---
    def _parse_and_execute_tool_calls(self, text: str) -> list[tuple[str, dict]]:
        """Finds, parses, executes ALL `cli_tools.X(...)` calls, returning name and results.
           Handles special instantiation for SummarizeCodeTool."""
        executed_call_results = []
        matches = TOOL_CALL_PATTERN.finditer(text)
        any_matches = False

        for match in matches:
            any_matches = True
            call_str = match.group(0); func_name = match.group(1); args_str = match.group(2).strip()
            logging.info(f"Found potential tool call: cli_tools.{func_name}({args_str[:100]}...)")
            args = {}
            result_data = {"call_str": call_str}

            try:
                # --- Argument Parsing (same robust version) ---
                kw_arg_pattern = re.compile( r"(\w+)\s*=\s*(" r"'''(.*?)'''|" r'"""(.*?)"""|' r"'(.*?)'(?!')|" r'"(.*?)"(?!")|' r"([^,=\s(][^,]*?)" r")\s*(?:,|$)", re.DOTALL)
                last_pos = 0
                for kw_match in kw_arg_pattern.finditer(args_str):
                    arg_name = kw_match.group(1); matched_value_part = kw_match.group(2)
                    if kw_match.group(3) is not None: args[arg_name] = kw_match.group(3); logging.debug(f"Parsed arg '{arg_name}' as triple-single-quoted string")
                    elif kw_match.group(4) is not None: args[arg_name] = kw_match.group(4); logging.debug(f"Parsed arg '{arg_name}' as triple-double-quoted string")
                    elif kw_match.group(5) is not None: try: args[arg_name] = bytes(kw_match.group(5), "utf-8").decode("unicode_escape"); logging.debug(f"Parsed arg '{arg_name}' as single-quoted string") except Exception: args[arg_name] = kw_match.group(5)
                    elif kw_match.group(6) is not None: try: args[arg_name] = bytes(kw_match.group(6), "utf-8").decode("unicode_escape"); logging.debug(f"Parsed arg '{arg_name}' as double-quoted string") except Exception: args[arg_name] = kw_match.group(6)
                    elif kw_match.group(7) is not None:
                        literal_str = kw_match.group(7).strip()
                        try: args[arg_name] = ast.literal_eval(literal_str); logging.debug(f"Parsed arg '{arg_name}' as literal using ast")
                        except (ValueError, SyntaxError): logging.warning(f"Could not parse '{literal_str}' as literal for arg '{arg_name}'. Treating as string."); args[arg_name] = literal_str
                    else: logging.warning(f"Could not determine value type for arg '{arg_name}' in {call_str}. Skipping."); continue
                    last_pos = kw_match.end()
                if last_pos < len(args_str.rstrip(')')): logging.warning(f"Potential unparsed arguments remaining in '{args_str[last_pos:]}' for call {call_str}")
            except Exception as parse_error:
                logging.error(f"Arg parse failed for '{call_str}': {parse_error}", exc_info=True); result_data["result"] = f"Error: Failed to parse arguments - {parse_error}"; executed_call_results.append((func_name, result_data)); continue

            # --- Execute the parsed call ---
            try:
                result_str = "(Execution failed)"
                logging.info(f"Executing parsed call: func='{func_name}', args={ {k: (v[:50] + '...' if isinstance(v, str) and len(v)>50 else v) for k,v in args.items()} })")
                self.console.print(f"[dim] -> Executing {func_name}...[/dim]")

                # --- Special Instantiation for Summarizer ---
                tool_instance = None
                if func_name == "summarize_code":
                     # Check if SummarizeCodeTool is available before trying to instantiate
                     if "summarize_code" in AVAILABLE_TOOLS:
                          tool_instance = SummarizeCodeTool(model_instance=self.model)
                     else:
                          raise ValueError("Tool 'summarize_code' is not available/imported correctly.")
                else:
                    # Use generic getter for other tools
                    tool_instance = get_tool(func_name)
                # --- End Special Instantiation ---

                if not tool_instance: raise ValueError(f"Tool '{func_name}' could not be instantiated or is not available.")

                result = tool_instance.execute(**args)
                result_str = str(result) if result is not None else "(No output)"

                result_data["result"] = result_str
                executed_call_results.append((func_name, result_data))
                logging.info(f"Execution successful for '{call_str}'. Result length: {len(result_str)}")

            except Exception as exec_error:
                logging.error(f"Exception during execution of '{call_str}': {exec_error}", exc_info=True)
                result_data["result"] = f"Error during execution: {exec_error}"
                executed_call_results.append((func_name, result_data))

        if not any_matches: logging.info("No parsable cli_tools calls found in the generated text.")
        return executed_call_results # Return list of tuples


    # ... (_extract_text_from_response remains the same) ...
    def _extract_text_from_response(self, response):
        # ... (Same robust version) ...
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
        # ... (Same cleanup) ...
        text = re.sub(r"<thinking>.*?</thinking>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"<plan>.*?</plan>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"# Thinking:.*?\n", "", text)
        text = re.sub(r"# Plan:.*?\n", "", text)
        return text.strip()

    # --- V13 Prompt: Agentic Loop + Summarizer Tool ---
    def _create_system_prompt(self) -> str:
        """Creates the system instruction prompt for the agentic loop w/ SummarizerTool."""
        tools_description = []
        if AVAILABLE_TOOLS:
            for name, tool_class in AVAILABLE_TOOLS.items():
                try:
                    tool_instance = tool_class(); desc = getattr(tool_instance, 'description', f'Tool {name}')
                    # Generate param hints including summarize_code
                    param_hints = []
                    if name == 'summarize_code': param_hints = ["file_path='path/to/large_file.ext'"]
                    elif name == 'view': param_hints = ["file_path='path'", "offset=Optional[int]", "limit=Optional[int]"]
                    # ...(rest of hints)...
                    elif name == 'task_complete': param_hints = ["summary='User-facing summary.'"]
                    elif name == 'edit': param_hints = ["file_path='path'", "content='...' (OR)", "old_string='...', new_string='...'"]
                    elif name == 'ls': param_hints = ["path='.'", "ignore='Optional[str]'"]
                    elif name == 'grep': param_hints = ["pattern='regex'", "path='.'", "include='*.ext'"]
                    elif name == 'glob': param_hints = ["pattern='glob_pat'", "path='.'"]
                    elif name == 'bash': param_hints = ["command='cmd string'"]
                    elif name == 'test_runner': param_hints = ["test_path='Optional[str]'", "options='Optional[str]'", "runner_command='pytest'"]
                    elif name == 'create_directory': param_hints = ["dir_path='path/to/new_dir'"]
                    elif name == 'linter_checker': param_hints = ["path='.'", "linter_command='ruff check'"]
                    elif name == 'formatter': param_hints = ["path='.'", "formatter_command='black'"]
                    else: param_hints = ["..."]
                    tools_description.append(f"`cli_tools.{name}({', '.join(param_hints)})`: {desc}")
                except Exception as e: logging.warning(f"Could not get description/params for tool '{name}': {e}"); tools_description.append(f"`cli_tools.{name}(...)`: Tool to {name} files/system.")
        else: logging.warning("AVAILABLE_TOOLS dictionary not found or empty.")

        system_prompt = f"""You are 'Gemini Code', an AI coding assistant in a CLI. **Your ONLY way to interact is by generating Python code calling `cli_tools` functions.**

**Your Goal:** Achieve the user's request via a sequence of `cli_tools` calls.

**Workflow:**

1.  **Receive Context:** User request & directory listing.
2.  **Plan & Generate Initial Actions:** Analyze context. Generate code for initial actions using `cli_tools`. **INFO GATHERING STRATEGY:**
    *   Use `cli_tools.summarize_code(file_path='...')` for large files or when you only need an overview (purpose, key functions/classes).
    *   Use `cli_tools.view(file_path='...')` ONLY for small files or when you need the *exact* full content.
    *   Use `cli_tools.view(file_path='...', offset=..., limit=...)` for specific small sections, ideally after using `grep` to find line numbers.
    *   Use `cli_tools.grep(...)` to find specific lines or patterns first.
    *   Generate necessary info-gathering calls first (can be multiple `summarize_code`/`view`/`grep`/`ls`/`glob`). If ready for action, generate the first `edit`/`bash`/etc. call. Use comments (`# Thinking:`).
3.  **Receive Results:** CLI executes code, gives results back.
4.  **Reflect & Generate Next Action OR Finish:** Analyze results. If more steps needed, generate code for the *next single action*. If task complete, **you MUST call `cli_tools.task_complete(summary='...')`**, providing a concise user-facing summary. Handle errors.
5.  **Repeat:** Loop continues until `task_complete` is called.
6.  **(Final Step Handled by CLI):** Summary from `task_complete` shown.

**CRITICAL INSTRUCTIONS:**
*   **OUTPUT ONLY PYTHON CODE or `task_complete` call:** Your response MUST be *either* Python code calling `cli_tools` functions *or* `cli_tools.task_complete(summary='...')`. No conversational text unless in comments.
*   **USE SUMMARIZER FOR LARGE FILES:** Prefer `summarize_code` over `view` for large files.
*   **FINAL STEP IS `task_complete`:** End tasks with `cli_tools.task_complete(summary='...')`.
*   **USE `cli_tools`:** Prefix all calls with `cli_tools.`.
*   **ONE ACTION AT A TIME (after info gathering):** Focus on one `edit`/`bash`/`test_runner` action per turn.
*   **STRINGS MUST BE QUOTED:** Use quotes correctly (triple for multiline). Use keyword arguments.
*   **`edit` Tool:** Use `content='...'` (create/overwrite) OR `old_string`/`new_string` (replace).
*   **HANDLE RESULTS:** Decide next action based on results.

**Available `cli_tools` Functions:**
{chr(10).join(tools_description) if tools_description else "No `cli_tools` functions available."}

You will now receive the initial context. Generate the Python code for the first action(s), using `summarize_code` or `view` appropriately for information gathering.
"""
        return system_prompt


        # --- CORRECTED _create_tool_definitions Method (Syntax DOUBLE-CHECKED) ---
    def _create_tool_definitions(self) -> list[Tool]:
        """Native tool definitions - NOT CURRENTLY USED but needs correct syntax for import."""
        tool_declarations = [] # Holds FunctionDeclaration objects

        # --- Define the view tool ---
        if "view" in AVAILABLE_TOOLS:
            try: # Indented
                tool_declarations.append(FunctionDeclaration(
                    name="view",
                    description="View specific sections or small files. For large files, use summarize_code.",
                    parameters={ "type": "object", "properties": {
                            "file_path": {"type": "string", "description": "Path to the file to view."},
                            "offset": {"type": "integer", "description": "Line number to start reading from (1-based index, optional)."},
                            "limit": {"type": "integer", "description": "Maximum number of lines to read (optional)."}
                        }, "required": ["file_path"] }
                ))
            except Exception as e: # Aligned with try
                logging.error(f"Failed to define 'view' tool: {e}")

        # --- Define the edit tool ---
        if "edit" in AVAILABLE_TOOLS:
            try: # Indented
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
            except Exception as e: # Aligned with try
                logging.error(f"Failed to define 'edit' tool: {e}")

        # --- Define the ls tool ---
        if "ls" in AVAILABLE_TOOLS:
            try: # Indented
                tool_declarations.append(FunctionDeclaration(
                    name="ls",
                    description="List files and directories in a given path.",
                    parameters={ "type": "object", "properties": {
                            "path": {"type": "string", "description": "Directory path to list (default: current directory '.')."},
                            "ignore": {"type": "string", "description": "Comma-separated glob patterns to ignore (e.g., '*.pyc,__pycache__'). Optional."}
                        }}
                ))
            except Exception as e: # Aligned with try
                logging.error(f"Failed to define 'ls' tool: {e}")

        # --- Define the grep tool ---
        if "grep" in AVAILABLE_TOOLS:
            try: # Indented
                tool_declarations.append(FunctionDeclaration(
                    name="grep",
                    description="Search for a pattern (regex) in files within a directory.",
                    parameters={ "type": "object", "properties": {
                            "pattern": {"type": "string", "description": "Regular expression pattern to search for."},
                            "path": {"type": "string", "description": "Directory path to search within (default: '.'). Optional."},
                            "include": {"type": "string", "description": "Glob pattern for files to include (e.g., '*.py', '*.txt'). Searches all files if omitted. Optional."}
                        }, "required": ["pattern"] }
                ))
            except Exception as e: # Aligned with try
                logging.error(f"Failed to define 'grep' tool: {e}")

        # --- Define the glob tool ---
        if "glob" in AVAILABLE_TOOLS:
            try: # Indented
                tool_declarations.append(FunctionDeclaration(
                    name="glob",
                    description="Find files matching specific glob patterns recursively.",
                    parameters={ "type": "object", "properties": {
                            "pattern": {"type": "string", "description": "Glob pattern to match (e.g., '**/*.py', 'docs/**/*.md')."},
                            "path": {"type": "string", "description": "Base directory path to search within (default: '.'). Optional."}
                        }, "required": ["pattern"] }
                ))
            except Exception as e: # Aligned with try
                logging.error(f"Failed to define 'glob' tool: {e}")

        # --- Define the bash tool ---
        if "bash" in AVAILABLE_TOOLS:
            try: # Indented
                tool_declarations.append(FunctionDeclaration(
                    name="bash",
                    description="Execute a shell command using the system's default shell.",
                    parameters={ "type": "object", "properties": {
                            "command": {"type": "string", "description": "The shell command string to execute."},
                            "timeout": {"type": "integer", "description": "Maximum execution time in seconds (optional)."}
                        }, "required": ["command"] }
                ))
            except Exception as e: # Aligned with try
                logging.error(f"Failed to define 'bash' tool: {e}")

        # --- Define the test_runner tool ---
        if "test_runner" in AVAILABLE_TOOLS:
            try: # Indented
                tool_declarations.append(FunctionDeclaration(
                    name="test_runner",
                    description="Runs automated tests using the project's test runner (e.g., pytest).",
                    parameters={ "type": "object", "properties": {
                            "test_path": {"type": "string", "description": "Specific file or directory path to test (optional, runs discovered tests if omitted)."},
                            "options": {"type": "string", "description": "Additional command-line options for the test runner (e.g., '-k my_test', '-v', '--cov'). Optional."},
                            "runner_command": {"type": "string", "description": "The command for the test runner (default: 'pytest'). Optional."}
                        }}
                ))
            except Exception as e: # Aligned with try
                logging.error(f"Failed to define 'test_runner' tool: {e}")

        # --- Define the task_complete tool ---
        if "task_complete" in AVAILABLE_TOOLS:
             try: # Indented
                 tool_declarations.append(FunctionDeclaration(
                     name="task_complete",
                     description="Signals task completion. MUST be called as the final step, providing a user-friendly summary.",
                     parameters={ "type": "object", "properties": {
                             "summary": {"type": "string", "description": "Concise, user-friendly summary of actions taken and final outcome."}
                         }, "required": ["summary"] }
                 ))
             except Exception as e: # Aligned with try
                 logging.error(f"Failed to define 'task_complete' tool: {e}")

        # --- Define create_directory tool ---
        if "create_directory" in AVAILABLE_TOOLS:
             try: # Indented
                 tool_declarations.append(FunctionDeclaration(
                     name="create_directory",
                     description="Creates a new directory, including any necessary parent directories.",
                     parameters={ "type": "object", "properties": {
                             "dir_path": {"type": "string", "description": "The path of the directory to create."}
                         }, "required": ["dir_path"] }
                 ))
             except Exception as e: # Aligned with try
                 logging.error(f"Failed to define 'create_directory' tool: {e}")

        # --- Define linter_checker tool ---
        if "linter_checker" in AVAILABLE_TOOLS:
             try: # Indented
                 tool_declarations.append(FunctionDeclaration(
                     name="linter_checker",
                     description="Runs a code linter (default: 'ruff check') on a specified path to find potential issues.",
                     parameters={ "type": "object", "properties": {
                             "path": {"type": "string", "description": "File or directory path to lint (default: '.')."},
                             "linter_command": {"type": "string", "description": "Base command for the linter (default: 'ruff check')."}
                         }}
                 ))
             except Exception as e: # Aligned with try
                 logging.error(f"Failed to define 'linter_checker' tool: {e}")

        # --- Define formatter tool ---
        if "formatter" in AVAILABLE_TOOLS:
             try: # Indented
                 tool_declarations.append(FunctionDeclaration(
                     name="formatter",
                     description="Runs a code formatter (default: 'black') on a specified path to automatically fix styling.",
                     parameters={ "type": "object", "properties": {
                             "path": {"type": "string", "description": "File or directory path to format (default: '.')."},
                             "formatter_command": {"type": "string", "description": "Base command for the formatter (default: 'black')."}
                         }}
                 ))
             except Exception as e: # Aligned with try
                 logging.error(f"Failed to define 'formatter' tool: {e}")

        # --- Define summarize_code tool ---
        if "summarize_code" in AVAILABLE_TOOLS:
             try: # Indented
                 tool_declarations.append(FunctionDeclaration(
                     name="summarize_code",
                     description="Provides a summary of a code file's purpose, key functions/classes, and structure. Use for large files.",
                     parameters={ "type": "object", "properties": {
                             "file_path": {"type": "string", "description": "Path to the file to summarize."}
                         }, "required": ["file_path"] }
                 ))
             except Exception as e: # Aligned with try
                 logging.error(f"Failed to define 'summarize_code' tool: {e}")

        logging.debug("Native tool definitions parsed (syntax check only in Code Gen mode).")
        # Return empty list as we are not using native tools in Code Gen mode
        return []
    # --- End CORRECTED Method ---