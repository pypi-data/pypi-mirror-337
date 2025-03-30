"""
Gemini model integration for the CLI tool.
Targeting Gemini 2.5 Pro Experimental.
AGENTIC LOOP (CODE GENERATION) w/ FORCED ORIENTATION & TASK COMPLETE TOOL.
Includes Quality tools. Prompt v12. Syntax FIXED.
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
# TASK_COMPLETE_PATTERN no longer needed, we check the function name

MAX_AGENT_ITERATIONS = 15 # Allow slightly more iterations

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
        # Use the V12 prompt for TaskCompleteTool workflow
        self.system_instruction = self._create_system_prompt()

        try:
            logging.info(f"Creating model: {self.model_name} for Agentic Loop w/ TaskCompleteTool.")
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                system_instruction=self.system_instruction
            )
            logging.info("GeminiModel initialized successfully (TaskComplete Agent Loop).")
        except Exception as e:
             logging.error(f"Fatal error initializing Gemini model '{self.model_name}': {str(e)}", exc_info=True); raise Exception(f"Could not initialize Gemini model: {e}") from e

    def get_available_models(self):
        return list_available_models(self.api_key)

    # --- generate function for Agentic Loop with TaskCompleteTool ---
    def generate(self, prompt: str, conversation=None) -> str | None:
        logging.info(f"Agent Loop w/ TaskComplete - Starting task: '{prompt[:100]}...'")
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
            self.console.print(f"[dim]Directory context acquired.[/dim]")
            orientation_context = f"Current directory contents (from `ls .`):\n```\n{ls_result}\n```\n"
            logging.info("Orientation successful.")
        except Exception as orient_error:
            logging.error(f"Error during mandatory orientation: {orient_error}", exc_info=True)
            orientation_context = f"Error during initial directory scan: {orient_error}\n"
            self.console.print(f"[red]Error getting directory listing: {orient_error}[/red]")

        # === Step 2: Initialize History and Start Agent Loop ===
        current_task_history = [
            {'role': 'user', 'parts': [self.system_instruction]},
            {'role': 'user', 'parts': [f"{orientation_context}\nUser request: {original_user_prompt}\n\nBased on the directory contents and the request, generate the Python code for the first necessary action(s) using `cli_tools.X(...)`. If the task is already complete or requires no action, call `cli_tools.task_complete(summary='...')`."]}
        ]
        iteration_count = 0; task_completed = False; final_summary = None

        try:
            while iteration_count < MAX_AGENT_ITERATIONS:
                iteration_count += 1
                logging.info(f"Agent Loop Iteration {iteration_count}/{MAX_AGENT_ITERATIONS}")

                # === Get Next Action Code ===
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

                # === Parse and Execute Tool Calls ===
                # Returns list of tuples: [(tool_name, result_dict), ...]
                executed_tool_info = self._parse_and_execute_tool_calls(generated_text)

                if not executed_tool_info:
                    logging.warning(f"No tool calls found/executed in LLM response (Iter {iteration_count}). Task might be stuck.")
                    # Ask LLM to clarify or finish if stuck
                    clarification_request = "You did not provide any tool calls or a completion signal. Please either provide the next `cli_tools.X(...)` call or signal completion with `cli_tools.task_complete(summary='...')`."
                    current_task_history.append({'role': 'user', 'parts': [clarification_request]})
                    continue # Ask again

                # === Check for Task Completion Signal ===
                for tool_name, result_data in executed_tool_info:
                    if tool_name == "task_complete":
                        logging.info("Task completion signaled by task_complete tool call.")
                        task_completed = True
                        final_summary = result_data.get("result", "Task completed, but summary extraction failed.")
                        break # Exit the execution loop

                if task_completed: break # Exit the while loop

                # === Prepare Results Feedback for Next Iteration ===
                results_feedback = "Executed tool calls. Results:\n\n"; any_errors = False
                for tool_name, result_data in executed_tool_info:
                     call_str = result_data.get('call_str', f'cli_tools.{tool_name}(...)') # Reconstruct approx call if needed
                     result = result_data.get('result', '(No result captured)')
                     results_feedback += f"Call: `{call_str}`\n"; results_feedback += f"Result: ```\n{result}\n```\n---\n"
                     if "Error" in str(result): any_errors = True # Check result string for errors

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
                 # Ask for a final summary attempt even on timeout
                 timeout_summary_request = f"Reached max iterations ({MAX_AGENT_ITERATIONS}). Please provide a concise final summary based on the history."
                 final_response = self.model.generate_content(current_task_history + [{'role':'user', 'parts':[timeout_summary_request]}])
                 final_summary = f"(Task exceeded max iterations)\n{self._extract_text_from_response(final_response).strip()}"
                 return self._cleanup_internal_tags(final_summary).strip()
            else:
                 # Should not be reached if loop terminates properly via task_complete
                 logging.error("Agent loop exited without task_complete signal or reaching max iterations.")
                 return "Error: Agent loop finished unexpectedly."

        except Exception as e:
             logging.error(f"Error during Agent Loop: {str(e)}", exc_info=True); return f"An unexpected error occurred during the agent process: {str(e)}"


    # --- Modified _parse_and_execute_tool_calls to return list of (name, result_dict) tuples ---
    def _parse_and_execute_tool_calls(self, text: str) -> list[tuple[str, dict]]:
        """Finds, parses, executes ALL `cli_tools.X(...)` calls, returning name and results."""
        executed_call_results = [] # List of tuples: (func_name, result_dict)
        matches = TOOL_CALL_PATTERN.finditer(text)
        any_matches = False

        for match in matches:
            any_matches = True
            call_str = match.group(0); func_name = match.group(1); args_str = match.group(2).strip()
            logging.info(f"Found potential tool call: cli_tools.{func_name}({args_str[:100]}...)")
            args = {}
            result_data = {"call_str": call_str} # Store info for feedback

            try:
                # --- Argument Parsing ---
                full_call_for_ast = f"f({args_str})"
                logging.debug(f"Attempting to parse AST for: {full_call_for_ast[:200]}...")
                node = ast.parse(full_call_for_ast, mode='eval'); call_node = node.body
                if not isinstance(call_node, ast.Call): raise SyntaxError("Parsed args string not a call structure")
                for kw in call_node.keywords:
                    arg_name = kw.arg; value_node = kw.value
                    try: args[arg_name] = ast.literal_eval(value_node); logging.debug(f"Parsed arg '{arg_name}' using literal_eval")
                    except ValueError:
                         if isinstance(value_node, ast.Constant) and isinstance(value_node.value, str): args[arg_name] = value_node.value; logging.debug(f"Parsed arg '{arg_name}' as Constant string")
                         elif hasattr(value_node, 's'): args[arg_name] = value_node.s; logging.debug(f"Parsed arg '{arg_name}' using fallback .s attribute")
                         else:
                             try:
                                  import io; from ast import unparse; f = io.StringIO(); unparse(value_node, f); reconstructed_value = f.getvalue().strip()
                                  logging.warning(f"Could not literal_eval arg '{arg_name}'. Reconstructed: {reconstructed_value[:100]}...")
                                  if reconstructed_value.startswith(('"', "'")):
                                       try: args[arg_name] = ast.literal_eval(reconstructed_value)
                                       except Exception: logging.error(f"Failed literal_eval on reconstructed '{arg_name}'. Skipping arg."); continue
                                  else: logging.error(f"Reconstructed value for '{arg_name}' not safe literal. Skipping arg."); continue
                             except ImportError: logging.error(f"ast.unparse required (Py3.9+). Skipping complex arg '{arg_name}'."); continue
                             except Exception as unparse_err: logging.error(f"Error reconstructing source for arg '{arg_name}': {unparse_err}. Skipping arg."); continue

            except Exception as parse_error:
                logging.error(f"Arg parse failed for '{call_str}': {parse_error}", exc_info=True)
                result_data["result"] = f"Error: Failed to parse arguments - {parse_error}"
                executed_call_results.append((func_name, result_data)) # Log failure
                continue # Process next match

            # --- Execute the parsed call ---
            try:
                result_str = "(Execution failed)"
                logging.info(f"Executing parsed call: func='{func_name}', args={ {k: (v[:50] + '...' if isinstance(v, str) and len(v)>50 else v) for k,v in args.items()} })")
                self.console.print(f"[dim] -> Executing {func_name}...[/dim]")
                tool_instance = get_tool(func_name)
                if not tool_instance: raise ValueError(f"Tool '{func_name}' is not available.")
                # Special handling for task_complete: pass args directly
                if func_name == "task_complete":
                     result = tool_instance.execute(**args)
                else:
                     # For other tools, execute normally
                     result = tool_instance.execute(**args)
                result_str = str(result) if result is not None else "(No output)"

                result_data["result"] = result_str # Add successful result
                executed_call_results.append((func_name, result_data)) # Add success tuple
                logging.info(f"Execution successful for '{call_str}'. Result length: {len(result_str)}")

            except Exception as exec_error:
                logging.error(f"Exception during execution of '{call_str}': {exec_error}", exc_info=True)
                result_data["result"] = f"Error during execution: {exec_error}"
                executed_call_results.append((func_name, result_data)) # Add failure tuple

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

    # --- V12 Prompt: Agentic Loop with TaskCompleteTool ---
    def _create_system_prompt(self) -> str:
        """Creates the system instruction prompt for the agentic loop w/ TaskCompleteTool."""
        tools_description = []
        if AVAILABLE_TOOLS:
            for name, tool_class in AVAILABLE_TOOLS.items():
                try:
                    tool_instance = tool_class(); desc = getattr(tool_instance, 'description', f'Tool {name}')
                    # --- Generate param hints including task_complete ---
                    param_hints = []
                    if name == 'task_complete': param_hints = ["summary='User-facing summary of actions and outcome.'"]
                    elif name == 'edit': param_hints = ["file_path='path'", "content='...' (OR)", "old_string='...', new_string='...'"]
                    elif name == 'view': param_hints = ["file_path='path'", "offset=Optional[int]", "limit=Optional[int]"]
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

1.  **Receive Context:** You get the user request & current directory listing.
2.  **Plan & Generate First Action(s):** Analyze context. Generate code for initial actions using `cli_tools`. **Prioritize necessary info gathering (`view`, `ls`, `glob`) first.** You can generate multiple info gathering calls together if needed. If ready for action, generate the first `edit`/`bash`/`create_directory` etc. call. Use comments (`# Thinking:`) for reasoning.
3.  **Receive Results:** The CLI executes your code and gives results back.
4.  **Reflect & Generate Next Action OR Finish:** Analyze results.
    *   If more steps needed, generate code for the *next single action* (`edit`, `bash`, `test_runner`, `formatter`, etc.).
    *   If the task is complete, **you MUST call `cli_tools.task_complete(summary='...')`**, providing a concise user-facing summary.
    *   Handle errors by generating corrective code or calling `task_complete` with an error summary.
5.  **Repeat:** The loop continues until `task_complete` is called.
6.  **(Final Step Handled by CLI):** The summary from your `task_complete` call will be shown to the user.

**CRITICAL INSTRUCTIONS:**
*   **OUTPUT ONLY PYTHON CODE or `task_complete` call:** Your response in each loop turn MUST be *only* Python code calling `cli_tools` functions.
*   **FINAL STEP IS `task_complete`:** You MUST end a successful task by generating a call to `cli_tools.task_complete(summary='...')`.
*   **USE `cli_tools`:** Prefix all calls with `cli_tools.`.
*   **STRINGS MUST BE QUOTED:** Use quotes correctly (triple for multiline). Use keyword arguments.
*   **`edit` Tool:** Use `content='...'` for create/overwrite OR `old_string`/`new_string` for replace.
*   **HANDLE RESULTS:** Decide your next action based on the results provided.

**Available `cli_tools` Functions:**
{chr(10).join(tools_description) if tools_description else "No `cli_tools` functions available."}

You will now receive the initial context. Generate the Python code for the first action(s) or call `task_complete`.
"""
        return system_prompt


    # --- CORRECTED _create_tool_definitions Method (Syntax ABSOLUTELY, POSITIVELY FIXED) ---
    def _create_tool_definitions(self) -> list[Tool]:
        """Native tool definitions - NOT CURRENTLY USED but needs correct syntax for import."""
        tool_declarations = [] # Holds FunctionDeclaration objects
        # --- Define the view tool ---
        if "view" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration( name="view", description="View the contents of a specific file.", parameters={ "type": "object", "properties": { "file_path": {"type": "string", "description": "Path to the file to view."}, "offset": {"type": "integer", "description": "Line number to start reading from (1-based index, optional)."}, "limit": {"type": "integer", "description": "Maximum number of lines to read (optional)."} }, "required": ["file_path"] } ))
            except Exception as e: logging.error(f"Failed to define 'view' tool: {e}")
        # --- Define the edit tool ---
        if "edit" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration( name="edit", description="Edit a file: create it, replace its content, replace a specific string, or delete a string.", parameters={ "type": "object", "properties": { "file_path": {"type": "string", "description": "Path to the file to edit or create."}, "new_content": {"type": "string", "description": "Full content for a new file or to completely overwrite an existing file. Use if `old_string` is omitted."}, "old_string": {"type": "string", "description": "The exact text to find and replace. If omitted, `new_content` overwrites the file."}, "new_string": {"type": "string", "description": "Text to replace `old_string` with. If replacing, this is required. Use an empty string ('') to delete `old_string`."} }, "required": ["file_path"] } ))
            except Exception as e: logging.error(f"Failed to define 'edit' tool: {e}")
        # --- Define the ls tool ---
        if "ls" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration( name="ls", description="List files and directories in a given path.", parameters={ "type": "object", "properties": { "path": {"type": "string", "description": "Directory path to list (default: current directory '.')."}, "ignore": {"type": "string", "description": "Comma-separated glob patterns to ignore (e.g., '*.pyc,__pycache__'). Optional."} }} ))
            except Exception as e: logging.error(f"Failed to define 'ls' tool: {e}")
        # --- Define the grep tool ---
        if "grep" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration( name="grep", description="Search for a pattern (regex) in files within a directory.", parameters={ "type": "object", "properties": { "pattern": {"type": "string", "description": "Regular expression pattern to search for."}, "path": {"type": "string", "description": "Directory path to search within (default: '.'). Optional."}, "include": {"type": "string", "description": "Glob pattern for files to include (e.g., '*.py', '*.txt'). Searches all files if omitted. Optional."}}, "required": ["pattern"] } ))
            except Exception as e: logging.error(f"Failed to define 'grep' tool: {e}")
        # --- Define the glob tool ---
        if "glob" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration( name="glob", description="Find files matching specific glob patterns recursively.", parameters={ "type": "object", "properties": { "pattern": {"type": "string", "description": "Glob pattern to match (e.g., '**/*.py', 'docs/**/*.md')."}, "path": {"type": "string", "description": "Base directory path to search within (default: '.'). Optional."}}, "required": ["pattern"] } ))
            except Exception as e: logging.error(f"Failed to define 'glob' tool: {e}")
        # --- Define the bash tool ---
        if "bash" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration( name="bash", description="Execute a shell command using the system's default shell.", parameters={ "type": "object", "properties": { "command": {"type": "string", "description": "The shell command string to execute."}, "timeout": {"type": "integer", "description": "Maximum execution time in seconds (optional)."} }, "required": ["command"] } ))
            except Exception as e: logging.error(f"Failed to define 'bash' tool: {e}")
        # --- Define the test_runner tool ---
        if "test_runner" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration( name="test_runner", description="Runs automated tests using the project's test runner (e.g., pytest).", parameters={ "type": "object", "properties": { "test_path": {"type": "string", "description": "Specific file or directory path to test (optional, runs discovered tests if omitted)."}, "options": {"type": "string", "description": "Additional command-line options for the test runner (e.g., '-k my_test', '-v', '--cov'). Optional."}, "runner_command": {"type": "string", "description": "The command for the test runner (default: 'pytest'). Optional."} }} ))
            except Exception as e: logging.error(f"Failed to define 'test_runner' tool: {e}")
        # --- Define the task_complete tool ---
        if "task_complete" in AVAILABLE_TOOLS:
             try:
                 tool_declarations.append(FunctionDeclaration( name="task_complete", description="Signals task completion. MUST be called as the final step, providing a user-friendly summary.", parameters={ "type": "object", "properties": { "summary": {"type": "string", "description": "Concise, user-friendly summary of actions taken and final outcome."} }, "required": ["summary"] } ))
             except Exception as e: logging.error(f"Failed to define 'task_complete' tool: {e}")
        # --- Define create_directory tool ---
        if "create_directory" in AVAILABLE_TOOLS:
             try:
                 tool_declarations.append(FunctionDeclaration( name="create_directory", description="Creates a new directory, including any necessary parent directories.", parameters={ "type": "object", "properties": { "dir_path": {"type": "string", "description": "The path of the directory to create."} }, "required": ["dir_path"] } ))
             except Exception as e: logging.error(f"Failed to define 'create_directory' tool: {e}")
        # --- Define linter_checker tool ---
        if "linter_checker" in AVAILABLE_TOOLS:
             try:
                 tool_declarations.append(FunctionDeclaration( name="linter_checker", description="Runs a code linter (default: 'ruff check') on a specified path to find potential issues.", parameters={ "type": "object", "properties": { "path": {"type": "string", "description": "File or directory path to lint (default: '.')."}, "linter_command": {"type": "string", "description": "Base command for the linter (default: 'ruff check')."} }} ))
             except Exception as e: logging.error(f"Failed to define 'linter_checker' tool: {e}")
        # --- Define formatter tool ---
        if "formatter" in AVAILABLE_TOOLS:
             try:
                 tool_declarations.append(FunctionDeclaration( name="formatter", description="Runs a code formatter (default: 'black') on a specified path to automatically fix styling.", parameters={ "type": "object", "properties": { "path": {"type": "string", "description": "File or directory path to format (default: '.')."}, "formatter_command": {"type": "string", "description": "Base command for the formatter (default: 'black')."} }} ))
             except Exception as e: logging.error(f"Failed to define 'formatter' tool: {e}")

        logging.debug("Native tool definitions parsed (syntax check only in Code Gen mode).")
        return [] # Return empty list as not used in code gen mode
    # --- End CORRECTED Method ---