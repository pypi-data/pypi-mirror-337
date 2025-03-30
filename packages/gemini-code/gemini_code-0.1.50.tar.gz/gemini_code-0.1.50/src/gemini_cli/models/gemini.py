"""
Gemini model integration for the CLI tool.
Targeting Gemini 2.5 Pro Experimental.
IMPLEMENTING AGENTIC LOOP (CODE GENERATION) with FORCED ORIENTATION.
Includes Test Runner tool. Prompt v11. Syntax FIXED AGAIN.
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

    def __init__(self, api_key, model_name="gemini-2.5-pro-exp-03-25"):
        """Initialize the Gemini model interface for agentic code generation."""
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)

        self.generation_config = genai.types.GenerationConfig( temperature=0.4, top_p=0.95, top_k=40 )
        self.safety_settings = { "HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE", "HATE": "BLOCK_MEDIUM_AND_ABOVE", "SEXUAL": "BLOCK_MEDIUM_AND_ABOVE", "DANGEROUS": "BLOCK_MEDIUM_AND_ABOVE" }
        # Call the SYNTAX FIXED method just for import validation
        _ = self._create_tool_definitions()
        # Use the V11 prompt for agentic loop
        self.system_instruction = self._create_system_prompt()

        try:
            logging.info(f"Creating model: {self.model_name} for Agentic Loop w/ Orientation.")
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                system_instruction=self.system_instruction
                # NO tools parameter here for Code Gen approach
            )
            logging.info("Testing model connectivity...")
            try:
                test_response = self.model.generate_content("Say 'Test OK'.", request_options={'timeout': 15})
                text_content = self._extract_text_from_response(test_response)
                logging.info(f"Model connectivity test successful. Response: {text_content[:50]}...")
                if 'Test OK' not in text_content: logging.warning("Connectivity test response unexpected.")
            except Exception as test_error: logging.warning(f"Initial model connectivity test failed: {test_error}")

            # History managed manually in generate()
            logging.info("GeminiModel initialized successfully (Forced Orientation Agent Loop).")

        except Exception as e:
            # ... (Error handling remains the same) ...
            logging.error(f"Fatal error initializing Gemini model '{self.model_name}': {str(e)}", exc_info=True); raise Exception(f"Could not initialize Gemini model: {e}") from e

    # ... (get_available_models remains the same) ...
    def get_available_models(self): return list_available_models(self.api_key)

    # --- Rewritten generate function for Forced Orientation Agentic Loop ---
    def generate(self, prompt: str, conversation=None) -> str | None:
        # ... (generate function logic remains the same as previous - Agent Loop w/ Orientation) ...
        logging.info(f"Agent Loop w/ Orientation - Starting task for prompt: '{prompt[:100]}...'")
        original_user_prompt = prompt
        if prompt.startswith('/'):
             command = prompt.split()[0].lower()
             if command in ['/exit', '/help', '/compact']: logging.info(f"Handled command: {command}"); return None

        orientation_context = ""
        try:
            logging.info("Performing mandatory orientation (ls)...")
            ls_tool = get_tool("ls")
            if ls_tool: ls_result = ls_tool.execute(); orientation_context = f"Current directory contents (from `ls .`):\n```\n{ls_result}\n```\n"; logging.info("Orientation successful."); logging.debug(f"Orientation Context:\n{orientation_context}")
            else: logging.warning("Could not find 'ls' tool for mandatory orientation."); orientation_context = "Note: Could not retrieve directory listing.\n"
        except Exception as orient_error: logging.error(f"Error during mandatory orientation: {orient_error}", exc_info=True); orientation_context = f"Error during initial directory scan: {orient_error}\n"

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

                logging.info("Asking LLM for next action(s)...")
                llm_response = self.model.generate_content( current_task_history, generation_config=self.generation_config )
                logging.debug(f"RAW Gemini Response Object (Iter {iteration_count}): {llm_response}")
                generated_text = self._extract_text_from_response(llm_response)
                last_llm_response_text = generated_text
                logging.info(f"LLM suggested action/code (Iter {iteration_count}):\n---\n{generated_text}\n---")

                current_task_history.append({'role': 'model', 'parts': [generated_text]})
                full_log.append(f"Assistant (Code Gen - Iter {iteration_count}):\n{generated_text}")

                if TASK_COMPLETE_PATTERN.search(generated_text): logging.info("Task completion signal detected."); task_completed = True; break

                tool_calls_executed = self._parse_and_execute_tool_calls(generated_text)

                if not tool_calls_executed:
                    logging.warning(f"No tool calls found in LLM response (Iter {iteration_count}), and no completion signal. Assuming task finished implicitly or is stuck.")
                    if iteration_count > 0: task_completed = True; break # Allow finishing after first turn if no tools needed
                    # If first turn and no tools, let loop try again? Or assume text answer? Let's break.
                    task_completed = True; break

                results_feedback = "Executed tool calls. Results:\n\n"; any_errors = False
                for call_info in tool_calls_executed:
                     results_feedback += f"Call: {call_info['call_str']}\n"; results_feedback += f"Result: ```\n{call_info['result']}\n```\n---\n"
                     if "Error" in call_info['result']: any_errors = True
                results_feedback += "\nBased on these results, what is the next `cli_tools.X(...)` action needed, or is the task complete (respond with '# Task Complete')?"

                current_task_history.append({'role': 'user', 'parts': [results_feedback]})
                full_log.append(f"System (Tool Results - Iter {iteration_count}):\n{results_feedback.splitlines()[0]}...")

                if any_errors: logging.warning("Errors occurred during tool execution. Loop will continue for potential correction.")

            final_summary = ""
            if task_completed:
                completion_text_only = TASK_COMPLETE_PATTERN.sub('', last_llm_response_text).strip()
                if completion_text_only and len(completion_text_only) > 10:
                     logging.info("Using text before completion signal as final summary.")
                     final_summary = completion_text_only
                else:
                     logging.info("Task loop finished. Requesting final summary...")
                     summary_request = "The task is marked complete. Please provide a concise final summary for the user based on the conversation history, describing the actions taken and the overall outcome."
                     final_response = self.model.generate_content(current_task_history + [{'role':'user', 'parts':[summary_request]}])
                     logging.debug(f"RAW Gemini Response Object (Summary): {final_response}")
                     final_summary = self._extract_text_from_response(final_response)
                     logging.info("Received final summary.")
            else:
                 logging.warning(f"Agent loop terminated after reaching max iterations ({MAX_AGENT_ITERATIONS}). Requesting summary of progress.")
                 timeout_summary_request = f"Reached max iterations ({MAX_AGENT_ITERATIONS}). Please summarize progress and any issues based on the history."
                 final_response = self.model.generate_content(current_task_history + [{'role':'user', 'parts':[timeout_summary_request]}])
                 final_summary = f"(Task exceeded max iterations)\n{self._extract_text_from_response(final_response).strip()}"

            cleaned_summary = self._cleanup_internal_tags(final_summary)
            return cleaned_summary.strip()

        except Exception as e:
            # ... (Error handling remains the same) ...
            logging.error(f"Error during Agent Loop: {str(e)}", exc_info=True); return f"An unexpected error occurred during the agent process: {str(e)}"

    # ... (_parse_and_execute_tool_calls remains the same robust version) ...
    def _parse_and_execute_tool_calls(self, text: str) -> list[dict]:
        """Finds, parses, and executes `cli_tools.X(...)` calls in text."""
        executed_calls = []
        matches = TOOL_CALL_PATTERN.finditer(text)
        for match in matches:
            call_str = match.group(0); func_name = match.group(1); args_str = match.group(2).strip()
            logging.info(f"Found potential tool call: cli_tools.{func_name}({args_str[:100]}...)")
            args = {}
            try:
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
            except Exception as parse_error: logging.error(f"Arg parse failed for '{call_str}': {parse_error}", exc_info=True); executed_calls.append({ "call_str": call_str, "result": f"Error: Failed to parse arguments - {parse_error}" }); continue
            try:
                logging.info(f"Executing parsed call: func='{func_name}', args={ {k: (v[:50] + '...' if isinstance(v, str) and len(v)>50 else v) for k,v in args.items()} })")
                tool_instance = get_tool(func_name)
                if not tool_instance: raise ValueError(f"Tool '{func_name}' is not available.")
                result = tool_instance.execute(**args)
                result_str = str(result) if result is not None else "(No output)"
                executed_calls.append({ "call_str": call_str, "result": result_str })
                logging.info(f"Execution successful for '{call_str}'. Result length: {len(result_str)}")
            except Exception as exec_error: logging.error(f"Exception during execution of '{call_str}': {exec_error}", exc_info=True); executed_calls.append({ "call_str": call_str, "result": f"Error during execution: {exec_error}" })
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
        text = re.sub(r"# Thinking:.*?\n", "", text) # Cleanup comments too
        text = re.sub(r"# Plan:.*?\n", "", text)
        return text.strip()

    # --- V11 Prompt for Forced Orientation Agentic Loop ---
    def _create_system_prompt(self) -> str:
        """Creates the system instruction prompt for the agentic loop w/ forced orientation."""
        # ... (V11 prompt remains the same as previous step) ...
        tools_description = []
        if AVAILABLE_TOOLS:
            for name, tool_class in AVAILABLE_TOOLS.items():
                try: tool_instance = tool_class(); desc = getattr(tool_instance, 'description', f'Tool {name}'); params = "..."; tools_description.append(f"`cli_tools.{name}({params})`: {desc}")
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
*   **STRINGS MUST BE QUOTED:** Ensure all string arguments in your generated code (`file_path`, `content`, `command`, `pattern`, etc.) are correctly enclosed in quotes (single or triple).
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