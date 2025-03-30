"""
Gemini model integration for the CLI tool.
Targeting Gemini 2.5 Pro Experimental.
AGENTIC LOOP (CODE GENERATION) with FORCED ORIENTATION.
Includes Test Runner tool & INTERMEDIATE STATUS UPDATES.
Prompt v11.1. Syntax FIXED.
"""

import google.generativeai as genai
# Native function calling types NOT used
from google.generativeai.types import FunctionDeclaration, Tool # FunctionDeclaration needed for the unused method
import re
import json
import logging
import ast
import shlex
import time # For potential delays
from rich.console import Console # <--- Added for status updates

from ..utils import count_tokens
from ..tools import get_tool, AVAILABLE_TOOLS # Still need these to EXECUTE tools

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

# Regex to find potential tool calls in the generated code block
TOOL_CALL_PATTERN = re.compile(r"cli_tools\.(\w+)\s*\((.*?)\)", re.DOTALL | re.MULTILINE)
# Regex to detect completion signal
TASK_COMPLETE_PATTERN = re.compile(r"#\s*Task Complete", re.IGNORECASE)

MAX_AGENT_ITERATIONS = 10 # Safety limit for the loop

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

    # --- MODIFIED __init__ to accept console ---
    def __init__(self, api_key: str, console: Console, model_name: str ="gemini-2.5-pro-exp-03-25"):
        """Initialize the Gemini model interface for agentic code generation."""
        self.api_key = api_key
        self.model_name = model_name
        self.console = console # Store console object
        genai.configure(api_key=api_key)

        self.generation_config = genai.types.GenerationConfig( temperature=0.4, top_p=0.95, top_k=40 )
        self.safety_settings = { "HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE", "HATE": "BLOCK_MEDIUM_AND_ABOVE", "SEXUAL": "BLOCK_MEDIUM_AND_ABOVE", "DANGEROUS": "BLOCK_MEDIUM_AND_ABOVE" }
        _ = self._create_tool_definitions() # Syntax check only
        self.system_instruction = self._create_system_prompt() # Using v11.1 prompt

        try:
            logging.info(f"Creating model: {self.model_name} for Agentic Loop w/ Orientation.")
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                system_instruction=self.system_instruction
            )
            # Connectivity test is less critical now, can be simplified/removed if needed
            # logging.info("Testing model connectivity...")
            # try:
            #     test_response = self.model.generate_content("Say 'Test OK'.", request_options={'timeout': 15})
            #     text_content = self._extract_text_from_response(test_response)
            #     logging.info(f"Model connectivity test successful. Response: {text_content[:50]}...")
            #     if 'Test OK' not in text_content: logging.warning("Connectivity test response unexpected.")
            # except Exception as test_error: logging.warning(f"Initial model connectivity test failed: {test_error}")

            logging.info("GeminiModel initialized successfully (Forced Orientation Agent Loop).")

        except Exception as e:
            # ... (Error handling remains the same) ...
            logging.error(f"Fatal error initializing Gemini model '{self.model_name}': {str(e)}", exc_info=True); raise Exception(f"Could not initialize Gemini model: {e}") from e

    # ... (get_available_models remains the same) ...
    def get_available_models(self): return list_available_models(self.api_key)

    # --- generate function (Agentic Loop logic remains the same) ---
    def generate(self, prompt: str, conversation=None) -> str | None:
        logging.info(f"Agent Loop w/ Orientation - Starting task for prompt: '{prompt[:100]}...'")
        original_user_prompt = prompt
        if prompt.startswith('/'):
             command = prompt.split()[0].lower()
             if command in ['/exit', '/help', '/compact']: logging.info(f"Handled command: {command}"); return None

        # === Step 1: Mandatory Orientation ===
        orientation_context = ""
        ls_result = "(ls tool not found or failed)" # Default message
        try:
            with self.console.status("🧭 Getting directory listing...", spinner="earth"): # Status for orientation
                 logging.info("Performing mandatory orientation (ls)...")
                 ls_tool = get_tool("ls")
                 if ls_tool: ls_result = ls_tool.execute() # Execute with default path '.'
                 else: logging.warning("Could not find 'ls' tool for mandatory orientation.")
            # Display result briefly *after* status disappears
            self.console.print(f"[dim]Directory listing obtained.[/dim]")
            orientation_context = f"Current directory contents (from `ls .`):\n```\n{ls_result}\n```\n"
            logging.info("Orientation successful.")
            logging.debug(f"Orientation Context:\n{orientation_context}")
            time.sleep(0.5) # Small pause so user sees the confirmation
        except Exception as orient_error:
            logging.error(f"Error during mandatory orientation: {orient_error}", exc_info=True)
            orientation_context = f"Error during initial directory scan: {orient_error}\n"
            self.console.print(f"[red]Error getting directory listing: {orient_error}[/red]")
            # Continue anyway for now, model might still work or ask

        # === Step 2: Initialize History and Start Agent Loop ===
        current_task_history = [
            {'role': 'user', 'parts': [self.system_instruction]},
            {'role': 'user', 'parts': [f"{orientation_context}\nUser request: {original_user_prompt}\n\nBased on the directory contents and the request, what is the first code action (`cli_tools.X(...)`) needed? If no action is needed, respond with '# Task Complete'."]}
        ]
        full_log = [f"System (Orientation):\n{orientation_context}", f"User: {original_user_prompt}"]
        iteration_count = 0; task_completed = False; last_llm_response_text = ""

        try:
            while iteration_count < MAX_AGENT_ITERATIONS:
                iteration_count += 1
                logging.info(f"Agent Loop Iteration {iteration_count}/{MAX_AGENT_ITERATIONS}")

                # === Get Next Action Code ===
                generated_text = "" # Define before status block
                with self.console.status(f"[yellow]Iteration {iteration_count}: Assistant planning next step...", spinner="dots"):
                    logging.info("Asking LLM for next action(s)...")
                    llm_response = self.model.generate_content( current_task_history, generation_config=self.generation_config )
                    logging.debug(f"RAW Gemini Response Object (Iter {iteration_count}): {llm_response}")
                    generated_text = self._extract_text_from_response(llm_response)
                # No need to print "Received..." here, execution status will show next
                last_llm_response_text = generated_text
                logging.info(f"LLM suggested action/code (Iter {iteration_count}):\n---\n{generated_text}\n---")

                current_task_history.append({'role': 'model', 'parts': [generated_text]})
                full_log.append(f"Assistant (Code Gen - Iter {iteration_count}):\n{generated_text}")

                if TASK_COMPLETE_PATTERN.search(generated_text): logging.info("Task completion signal detected."); task_completed = True; break

                # === Parse and Execute Tool Calls (This function now shows status) ===
                tool_calls_executed = self._parse_and_execute_tool_calls(generated_text)

                if not tool_calls_executed:
                    logging.warning(f"No tool calls found in LLM response (Iter {iteration_count}), and no completion signal. Assuming task finished implicitly or is stuck.")
                    if iteration_count > 0: task_completed = True; break
                    task_completed = True; break

                # === Prepare Results Feedback ===
                results_feedback = "Executed tool calls. Results:\n\n"; any_errors = False
                for call_info in tool_calls_executed:
                     results_feedback += f"Call: {call_info['call_str']}\n"; results_feedback += f"Result: ```\n{call_info['result']}\n```\n---\n"
                     if "Error" in call_info['result']: any_errors = True
                results_feedback += "\nBased on these results, what is the next `cli_tools.X(...)` action needed, or is the task complete (respond with '# Task Complete')?"

                current_task_history.append({'role': 'user', 'parts': [results_feedback]})
                full_log.append(f"System (Tool Results - Iter {iteration_count}):\n{results_feedback.splitlines()[0]}...")

                if any_errors: logging.warning("Errors occurred during tool execution. Loop will continue for potential correction.")

            # === End Agent Loop ===

            # === Final Summary Generation ===
            final_summary = ""
            if task_completed:
                # ... (Summary logic remains the same) ...
                completion_text_only = TASK_COMPLETE_PATTERN.sub('', last_llm_response_text).strip()
                if completion_text_only and len(completion_text_only) > 10:
                     logging.info("Using text before completion signal as final summary.")
                     final_summary = completion_text_only
                else:
                     with self.console.status("[yellow]Assistant preparing final summary...", spinner="dots"):
                         logging.info("Task loop finished. Requesting final summary...")
                         summary_request = "The task is marked complete. Please provide a concise final summary for the user based on the conversation history, describing the actions taken and the overall outcome."
                         # Use a slightly different history for summary? Maybe just the log? Or full chat history?
                         # Using full chat history for now.
                         final_response = self.model.generate_content(current_task_history + [{'role':'user', 'parts':[summary_request]}])
                         logging.debug(f"RAW Gemini Response Object (Summary): {final_response}")
                         final_summary = self._extract_text_from_response(final_response)
                         logging.info("Received final summary.")
            else:
                 # ... (Max iterations logic remains the same) ...
                 logging.warning(f"Agent loop terminated after reaching max iterations ({MAX_AGENT_ITERATIONS}). Requesting summary of progress.")
                 timeout_summary_request = f"Reached max iterations ({MAX_AGENT_ITERATIONS}). Please summarize progress and any issues based on the history."
                 final_response = self.model.generate_content(current_task_history + [{'role':'user', 'parts':[timeout_summary_request]}])
                 final_summary = f"(Task exceeded max iterations)\n{self._extract_text_from_response(final_response).strip()}"

            cleaned_summary = self._cleanup_internal_tags(final_summary)
            return cleaned_summary.strip()

        except Exception as e:
            # ... (Error handling remains the same) ...
            logging.error(f"Error during Agent Loop: {str(e)}", exc_info=True); return f"An unexpected error occurred during the agent process: {str(e)}"


    # --- MODIFIED _parse_and_execute_tool_calls to use self.console.status ---
    def _parse_and_execute_tool_calls(self, text: str) -> list[dict]:
        """Finds, parses, and executes `cli_tools.X(...)` calls in text, showing status."""
        executed_calls = []
        matches = TOOL_CALL_PATTERN.finditer(text)
        any_matches = False # Flag to check if we found any parsable calls

        for match in matches:
            any_matches = True
            call_str = match.group(0); func_name = match.group(1); args_str = match.group(2).strip()
            logging.info(f"Found potential tool call: cli_tools.{func_name}({args_str[:100]}...)")
            args = {}
            status_message = f"⚙️ Executing: {func_name}" # Default status

            try:
                # --- Argument Parsing (same as before) ---
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
                                      except Exception: logging.error(f"Failed literal_eval on reconstructed '{arg_name}'. Skipping."); continue
                                 else: logging.error(f"Reconstructed value for '{arg_name}' not safe literal. Skipping."); continue
                            except ImportError: logging.error(f"ast.unparse required (Py3.9+). Skipping complex arg '{arg_name}'."); continue
                            except Exception as unparse_err: logging.error(f"Error reconstructing source for arg '{arg_name}': {unparse_err}. Skipping."); continue
                # --- End Argument Parsing ---

                # --- Set Specific Status Message ---
                if func_name == 'view' and 'file_path' in args: status_message = f"👀 Reading file [cyan]{args['file_path']}[/cyan]..."
                elif func_name == 'edit' and 'file_path' in args: status_message = f"📝 Writing to file [cyan]{args['file_path']}[/cyan]..."
                elif func_name == 'ls' and 'path' in args: status_message = f" Ls Listing directory [cyan]{args['path']}[/cyan]..."
                elif func_name == 'grep' and 'pattern' in args: status_message = f"🔍 Searching for pattern '{args['pattern'][:20]}...'..."
                elif func_name == 'glob' and 'pattern' in args: status_message = f" F Finding files matching [cyan]{args['pattern']}[/cyan]..."
                elif func_name == 'bash' and 'command' in args: status_message = f"⚙️ Running command: [yellow]{args['command'][:40]}...[/yellow]"
                elif func_name == 'test_runner': status_message = "🧪 Running tests..."
                # --- End Status Message ---

                # --- Execute within Status Context ---
                result_str = "(Execution failed before completion)" # Default if error happens right away
                with self.console.status(status_message, spinner="dots"):
                    logging.info(f"Executing parsed call: func='{func_name}', args={ {k: (v[:50] + '...' if isinstance(v, str) and len(v)>50 else v) for k,v in args.items()} })")
                    tool_instance = get_tool(func_name)
                    if not tool_instance: raise ValueError(f"Tool '{func_name}' is not available.")
                    result = tool_instance.execute(**args)
                    result_str = str(result) if result is not None else "(No output)"
                # --- End Status Context ---

                # Execution finished (successfully or with tool error captured in result_str)
                executed_calls.append({ "call_str": call_str, "result": result_str })
                logging.info(f"Execution logged for '{call_str}'. Result length: {len(result_str)}")
                time.sleep(0.1) # Tiny pause to ensure status clears visually

            except Exception as exec_error:
                # Catch errors during parsing or getting tool instance before status block
                logging.error(f"Exception during setup or execution of '{call_str}': {exec_error}", exc_info=True)
                executed_calls.append({ "call_str": call_str, "result": f"Error during execution setup: {exec_error}" })
                # Ensure status is cleared if it was started and error occurred
                # The `with` statement handles this automatically

        if not any_matches:
             logging.info("No parsable cli_tools calls found in the generated text.")

        return executed_calls

    # ... (_extract_text_from_response remains the same) ...
    def _extract_text_from_response(self, response):
        try:
            all_text = []
            if response.candidates:
                 if response.candidates[0].finish_reason.name != "STOP":
                     logging.warning(f"Response generation stopped due to: {response.candidates[0].finish_reason.name}")
                     if response.candidates[0].safety_ratings:
                         ratings = {r.category.name: r.probability.name for r in response.candidates[0].safety_ratings}
                         return f"(Response blocked due to safety settings: {ratings})"
                     return f"(Response generation incomplete: {response.candidates[0].finish_reason.name})"
                 for part in response.candidates[0].content.parts:
                     if hasattr(part, 'text'): all_text.append(part.text)
                 return "".join(all_text)
            elif hasattr(response, 'text'): return response.text
            elif response.prompt_feedback and response.prompt_feedback.block_reason:
                 logging.warning(f"Prompt blocked due to: {response.prompt_feedback.block_reason.name}")
                 return f"(Prompt blocked due to: {response.prompt_feedback.block_reason.name})"
            else: logging.warning("Could not extract text from response structure."); return ""
        except Exception as e: logging.error(f"Error extracting text: {e}", exc_info=True); return f"Error extracting response text: {e}"

    # ... (_cleanup_internal_tags remains the same) ...
    def _cleanup_internal_tags(self, text: str) -> str:
        text = re.sub(r"<thinking>.*?</thinking>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"<plan>.*?</plan>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"# Thinking:.*?\n", "", text)
        text = re.sub(r"# Plan:.*?\n", "", text)
        return text.strip()

    # --- V11.1 Prompt: Agentic Loop + Updated Edit Tool Description ---
    def _create_system_prompt(self) -> str:
        """Creates the system instruction prompt for the agentic loop w/ forced orientation."""
        # ... (V11.1 prompt remains the same as previous step) ...
        tools_description = []
        if AVAILABLE_TOOLS:
            for name, tool_class in AVAILABLE_TOOLS.items():
                try:
                    tool_instance = tool_class(); desc = getattr(tool_instance, 'description', f'Tool {name}')
                    param_hints = []
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
2.  **Plan & Generate First Action:** Analyze the request and context. Generate Python code for the *single next logical action* using `cli_tools`. Use comments (`# Thinking:`) for reasoning. If the request requires reading a file first, generate the `cli_tools.view(...)` call. If the request can be fulfilled immediately (e.g. creating a simple file), generate the `cli_tools.edit(...)` call.
3.  **Receive Results:** The CLI will execute your code and provide the results back to you.
4.  **Reflect & Generate Next Action (or Finish):** Analyze the results of the previous action.
    *   If the task requires more steps, generate the Python code for the *next single action* using `cli_tools`.
    *   If the task is complete based on the results, output **ONLY** the comment `# Task Complete`.
    *   If an error occurred, analyze the error message and generate code for a corrective action or output `# Task Complete` if unrecoverable.
5.  **Repeat:** The CLI will continue executing your generated code and providing results until you output `# Task Complete`.
6.  **Summarize (Final Step):** After you signal completion, you will be asked one last time to provide a concise summary for the user based on the entire interaction history.

**CRITICAL INSTRUCTIONS:**
*   **OUTPUT ONLY PYTHON CODE (or # Task Complete):** In each step (except the final summary), your output MUST be *either* valid Python code calling one or more `cli_tools` functions *or* the exact line `# Task Complete`. Do not include conversational text unless it's within a Python comment (`#`).
*   **USE `cli_tools`:** All tool calls MUST start with `cli_tools.`.
*   **ONE STEP AT A TIME:** Focus on generating the code for the immediate next logical step based on the history and results.
*   **STRINGS MUST BE QUOTED:** Ensure all string arguments in your generated code (`file_path`, `content`, `command`, `pattern`, etc.) are correctly enclosed in quotes (single or triple). Use triple quotes for multi-line content.
*   **`edit` Tool Usage:** Use the `content='...'` argument to create/overwrite files. Use `old_string='...'` and `new_string='...'` arguments to replace specific text. Do not use `content` and `old_string`/`new_string` in the same call.
*   **HANDLE RESULTS:** Use the results provided back to you to decide your next action.

**Available `cli_tools` Functions (Examples - Parameters might vary):**
{chr(10).join(tools_description) if tools_description else "No `cli_tools` functions available."}

You will now receive the initial context (directory listing and user request). Generate the Python code for the first action.
"""
        return system_prompt


    # --- CORRECTED _create_tool_definitions Method (Syntax TRULY FIXED AGAIN) ---
    def _create_tool_definitions(self) -> list[Tool]:
        """Native tool definitions - NOT CURRENTLY USED but needs correct syntax for import."""
        tool_declarations = [] # Holds FunctionDeclaration objects
        
        if "view" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="view",
                    description="View the contents of a specific file.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Path to the file to view."},
                            "offset": {"type": "integer", "description": "Line number to start reading from (1-based index, optional)."},
                            "limit": {"type": "integer", "description": "Maximum number of lines to read (optional)."}
                        },
                        "required": ["file_path"]
                    }
                ))
            except Exception as e:
                logging.error(f"Failed to define 'view' tool: {e}")
        
        if "edit" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="edit",
                    description="Edit a file: create it, replace its content, replace a specific string, or delete a string.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "file_path": {"type": "string", "description": "Path to the file to edit or create."},
                            "content": {"type": "string", "description": "Full content for a new file or to completely overwrite an existing file. Use if `old_string` is omitted."},
                            "old_string": {"type": "string", "description": "The exact text to find and replace. If omitted, `content` overwrites the file."},
                            "new_string": {"type": "string", "description": "Text to replace `old_string` with. If replacing, this is required. Use an empty string ('') to delete `old_string`."}
                        },
                        "required": ["file_path"]
                    }
                ))
            except Exception as e:
                logging.error(f"Failed to define 'edit' tool: {e}")
        
        if "ls" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="ls",
                    description="List files and directories in a given path.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "Directory path to list (default: current directory '.')."},
                            "ignore": {"type": "string", "description": "Comma-separated glob patterns to ignore (e.g., '*.pyc,__pycache__'). Optional."}
                        }
                    }
                ))
            except Exception as e:
                logging.error(f"Failed to define 'ls' tool: {e}")
        
        if "grep" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="grep",
                    description="Search for a pattern (regex) in files within a directory.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "pattern": {"type": "string", "description": "Regular expression pattern to search for."},
                            "path": {"type": "string", "description": "Directory path to search within (default: '.'). Optional."},
                            "include": {"type": "string", "description": "Glob pattern for files to include (e.g., '*.py', '*.txt'). Searches all files if omitted. Optional."}
                        },
                        "required": ["pattern"]
                    }
                ))
            except Exception as e:
                logging.error(f"Failed to define 'grep' tool: {e}")
        
        if "glob" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="glob",
                    description="Find files matching specific glob patterns recursively.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "pattern": {"type": "string", "description": "Glob pattern to match (e.g., '**/*.py', 'docs/**/*.md')."},
                            "path": {"type": "string", "description": "Base directory path to search within (default: '.'). Optional."}
                        },
                        "required": ["pattern"]
                    }
                ))
            except Exception as e:
                logging.error(f"Failed to define 'glob' tool: {e}")
        
        if "bash" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="bash",
                    description="Execute a shell command using the system's default shell.",
                    parameters={
                        "type": "object",
                        "properties": {
                            "command": {"type": "string", "description": "The shell command string to execute."},
                            "timeout": {"type": "integer", "description": "Maximum execution time in seconds (optional)."}
                        },
                        "required": ["command"]
                    }
                ))
            except Exception as e:
                logging.error(f"Failed to define 'bash' tool: {e}")
        
        if "test_runner" in AVAILABLE_TOOLS:
            try:
                test_runner_declaration = FunctionDeclaration(
                    name="test_runner",
                    description="Runs automated tests using the project's test runner (e.g., pytest).",
                    parameters={
                        "type": "object",
                        "properties": {
                            "test_path": {"type": "string", "description": "Specific file or directory path to test (optional, runs discovered tests if omitted)."},
                            "options": {"type": "string", "description": "Additional command-line options for the test runner (e.g., '-k my_test', '-v', '--cov'). Optional."},
                            "runner_command": {"type": "string", "description": "The command for the test runner (default: 'pytest'). Optional."}
                        }
                    }
                )
                tool_declarations.append(test_runner_declaration)
            except Exception as e:
                logging.error(f"Failed to define 'test_runner' tool: {e}")
        
        logging.debug("Native tool definitions parsed (syntax check only in Code Gen mode).")
        return []
    # --- End CORRECTED Method ---