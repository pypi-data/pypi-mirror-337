"""
Gemini model integration for the CLI tool.
Targeting Gemini 2.5 Pro Experimental.
IMPLEMENTING CLAUDE CODE STYLE WORKFLOW (CODE GENERATION).
Includes Test Runner tool. Prompt v10.1 (Inline Content Hint). Syntax FIXED.
"""

import google.generativeai as genai
# Native function calling types are NO LONGER needed here (kept Tool for the method return type hint)
from google.generativeai.types import FunctionDeclaration, Tool # FunctionDeclaration needed for the unused method
import re
import json
import logging
import ast # Using AST for potentially safer parsing than pure regex
import shlex

from ..utils import count_tokens
from ..tools import get_tool, AVAILABLE_TOOLS # Still need these to EXECUTE tools

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

# Regex to find potential tool calls in the generated code block
# Updated regex to better handle multi-line content and various quoting/spacing
# Looks for cli_tools.func_name( keyword = value , ... )
TOOL_CALL_PATTERN = re.compile(r"cli_tools\.(\w+)\s*\((.*?)\)", re.DOTALL | re.MULTILINE)


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
    """Interface for Gemini models using Claude Code style interaction."""

    def __init__(self, api_key, model_name="gemini-2.5-pro-exp-03-25"):
        """Initialize the Gemini model interface for code generation."""
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)

        self.generation_config = genai.types.GenerationConfig( temperature=0.4, top_p=0.95, top_k=40 )
        self.safety_settings = { "HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE", "HATE": "BLOCK_MEDIUM_AND_ABOVE", "SEXUAL": "BLOCK_MEDIUM_AND_ABOVE", "DANGEROUS": "BLOCK_MEDIUM_AND_ABOVE" }
        _ = self._create_tool_definitions() # Syntax check only
        # Use the V10.1 prompt with inline content hint
        self.system_instruction = self._create_system_prompt()

        try:
            logging.info(f"Creating model: {self.model_name} for code generation workflow (NO NATIVE TOOLS).")
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                system_instruction=self.system_instruction
            )
            logging.info("Testing model connectivity...")
            try:
                test_response = self.model.generate_content("Say 'Test OK'.", request_options={'timeout': 15})
                text_content = self._extract_text_from_response(test_response)
                logging.info(f"Model connectivity test successful. Response: {text_content[:50]}...")
                if 'Test OK' not in text_content: logging.warning("Connectivity test response unexpected.")
            except Exception as test_error: logging.warning(f"Initial model connectivity test failed (may recover): {test_error}")
            self.chat = self.model.start_chat(history=[])
            logging.info("GeminiModel initialized successfully (Code Gen Mode). Chat session started.")
        except Exception as e:
            # ... (Error handling remains the same) ...
             logging.error(f"Fatal error initializing Gemini model '{self.model_name}': {str(e)}", exc_info=True); raise Exception(f"Could not initialize Gemini model: {e}") from e

    # ... (get_available_models remains the same) ...
    def get_available_models(self): return list_available_models(self.api_key)

    # --- generate function for Code Generation Workflow (same as before) ---
    def generate(self, prompt: str, conversation=None) -> str | None:
        # ... (generate function remains the same as previous Claude-style version) ...
        logging.info(f"Code Gen Workflow - Received prompt: '{prompt[:100]}...'")
        if prompt.startswith('/'):
             command = prompt.split()[0].lower()
             if command in ['/exit', '/help', '/compact']: logging.info(f"Handled command: {command}"); return None
        try:
            logging.info("Sending initial prompt to Gemini for code generation...")
            response = self.chat.send_message(prompt)
            logging.debug(f"RAW Gemini Response Object (Initial Code Gen): {response}")
            generated_text = self._extract_text_from_response(response)
            logging.info("Received generated text potentially containing tool code.")
            logging.debug(f"Generated Text:\n---\n{generated_text}\n---")

            tool_calls_found = self._parse_and_execute_tool_calls(generated_text)

            if not tool_calls_found:
                logging.info("No tool calls found in the response. Returning generated text directly.")
                cleaned_text = self._cleanup_internal_tags(generated_text)
                return cleaned_text.strip()

            results_feedback = "Okay, I executed the requested tool calls. Here are the results:\n\n"
            for call_info in tool_calls_found:
                 results_feedback += f"Function Call: {call_info['call_str']}\n"
                 results_feedback += f"Result:\n```\n{call_info['result']}\n```\n---\n"
            results_feedback += "\nPlease review these results and provide a final summary or response to the user based on the outcome."

            logging.info("Sending tool execution results back to Gemini for summary...")
            response = self.chat.send_message(results_feedback)
            logging.debug(f"RAW Gemini Response Object (After Results Feedback): {response}")
            final_summary = self._extract_text_from_response(response)
            logging.info("Received final summary from Gemini.")
            cleaned_summary = self._cleanup_internal_tags(final_summary)
            return cleaned_summary.strip()
        except Exception as e:
            # ... (Error handling remains the same) ...
            logging.error(f"Error during Code Gen generation/execution: {str(e)}", exc_info=True); return f"An unexpected error occurred during generation: {str(e)}"

    # ... (_parse_and_execute_tool_calls - slightly improved parsing robustness) ...
    def _parse_and_execute_tool_calls(self, text: str) -> list[dict]:
        """Finds, parses, and executes `cli_tools.X(...)` calls in text."""
        executed_calls = []
        # Regex needs DOTALL to match multiline args like content='''...'''
        matches = TOOL_CALL_PATTERN.finditer(text)
        for match in matches:
            call_str = match.group(0) # Full matched string
            func_name = match.group(1)
            args_str = match.group(2).strip() # The arguments part, stripped
            logging.info(f"Found potential tool call: cli_tools.{func_name}({args_str[:100]}...)") # Log truncated args

            args = {}
            try:
                # More robust parsing: try parsing as a dict if it looks like kwargs,
                # otherwise handle simpler cases. This is still heuristic.
                # Wrap in a dummy function call `f(...)` for AST parsing
                full_call_for_ast = f"f({args_str})"
                logging.debug(f"Attempting to parse AST for: {full_call_for_ast[:200]}...")
                node = ast.parse(full_call_for_ast, mode='eval')
                call_node = node.body

                if not isinstance(call_node, ast.Call):
                     raise SyntaxError("Parsed arguments string is not a function call structure")

                # Only process keyword arguments for simplicity and safety
                for kw in call_node.keywords:
                    arg_name = kw.arg
                    value_node = kw.value
                    try:
                        # Prioritize literal_eval for simple, safe types
                        args[arg_name] = ast.literal_eval(value_node)
                        logging.debug(f"Parsed arg '{arg_name}' using literal_eval")
                    except ValueError:
                        # Handle specific cases like multi-line strings if literal_eval fails
                        if isinstance(value_node, ast.Constant) and isinstance(value_node.value, str):
                             args[arg_name] = value_node.value
                             logging.debug(f"Parsed arg '{arg_name}' as Constant string")
                        elif hasattr(value_node, 's'): # Fallback for older AST Constant string nodes
                             args[arg_name] = value_node.s
                             logging.debug(f"Parsed arg '{arg_name}' using fallback .s attribute")
                        else:
                            # Attempt to reconstruct the source string - potentially less safe
                            # Requires Python 3.9+ for ast.unparse
                            try:
                                 import io
                                 from ast import unparse
                                 f = io.StringIO()
                                 unparse(value_node, f)
                                 reconstructed_value = f.getvalue().strip()
                                 logging.warning(f"Could not literal_eval arg '{arg_name}'. Reconstructed value: {reconstructed_value[:100]}...")
                                 # Be cautious here - maybe only allow if it looks like a quoted string?
                                 if reconstructed_value.startswith(('"', "'")):
                                      # Try literal_eval on the reconstructed string
                                      try:
                                           args[arg_name] = ast.literal_eval(reconstructed_value)
                                      except Exception:
                                           logging.error(f"Failed to literal_eval reconstructed value for '{arg_name}'. Skipping.")
                                           continue # Skip this problematic argument
                                 else:
                                      logging.error(f"Reconstructed value for '{arg_name}' doesn't look like a safe literal. Skipping.")
                                      continue # Skip potentially unsafe args
                            except ImportError:
                                 logging.error(f"Cannot use ast.unparse (Python 3.9+ required). Skipping complex arg '{arg_name}'.")
                                 continue
                            except Exception as unparse_err:
                                 logging.error(f"Error reconstructing source for arg '{arg_name}': {unparse_err}. Skipping.")
                                 continue


            except Exception as parse_error:
                logging.error(f"Failed to parse arguments for '{call_str}': {parse_error}", exc_info=True)
                executed_calls.append({ "call_str": call_str, "result": f"Error: Failed to parse arguments - {parse_error}" }); continue

            # Execute the actual tool
            try:
                logging.info(f"Executing parsed call: func='{func_name}', args={ {k: (v[:50] + '...' if isinstance(v, str) and len(v)>50 else v) for k,v in args.items()} })") # Log truncated args
                tool_instance = get_tool(func_name)
                if not tool_instance: raise ValueError(f"Tool '{func_name}' is not available.")
                result = tool_instance.execute(**args)
                result_str = str(result) if result is not None else "(No output)"
                executed_calls.append({ "call_str": call_str, "result": result_str })
                logging.info(f"Execution successful for '{call_str}'. Result length: {len(result_str)}")
            except Exception as exec_error:
                logging.error(f"Exception during execution of '{call_str}': {exec_error}", exc_info=True)
                executed_calls.append({ "call_str": call_str, "result": f"Error during execution: {exec_error}" })
        return executed_calls

    # ... (_extract_text_from_response remains the same) ...
    def _extract_text_from_response(self, response):
        try:
            all_text = []
            if response.candidates:
                 for part in response.candidates[0].content.parts:
                     if hasattr(part, 'text'): all_text.append(part.text)
                 return "".join(all_text)
            elif hasattr(response, 'text'): return response.text
            else: logging.warning("Could not extract text from response structure."); return ""
        except Exception as e: logging.error(f"Error extracting text: {e}", exc_info=True); return f"Error extracting response text: {e}"

    # ... (_cleanup_internal_tags remains the same) ...
    def _cleanup_internal_tags(self, text: str) -> str:
        text = re.sub(r"<thinking>.*?</thinking>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"<plan>.*?</plan>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"# Thinking:.*?\n", "", text) # Cleanup comments too
        text = re.sub(r"# Plan:.*?\n", "", text)
        return text.strip()

    # --- Uses the V10.1 Prompt: Code Gen + Inline Content Hint ---
    def _create_system_prompt(self) -> str:
        """Creates the system instruction prompt for code-generation, asking for inline content."""
        # ... (V10.1 prompt remains the same as previous step) ...
        tools_description = []
        if AVAILABLE_TOOLS:
            for name, tool_class in AVAILABLE_TOOLS.items():
                try: tool_instance = tool_class(); desc = getattr(tool_instance, 'description', f'Tool {name}'); params = "..."; tools_description.append(f"`cli_tools.{name}({params})`: {desc}")
                except Exception as e: logging.warning(f"Could not get description/params for tool '{name}': {e}"); tools_description.append(f"`cli_tools.{name}(...)`: Tool to {name} files/system.")
        else: logging.warning("AVAILABLE_TOOLS dictionary not found or empty.")

        system_prompt = f"""You are 'Gemini Code', an expert AI pair programmer operating in a CLI. **You interact with the user's project directory by GENERATING PYTHON CODE that calls predefined tools.**

**Your Goal:** Fulfill the user's request by generating Python code snippets using the `cli_tools` module.

**Workflow:**

1.  **Analyze Request & Plan:** Understand goal, determine tool calls needed. Use comments like `# Thinking:`.
2.  **Generate Tool Code:** Write Python code calling `cli_tools` functions (e.g., `cli_tools.view(...)`). **Generate ONLY the necessary `cli_tools` calls.**
3.  **Execution & Results:** The CLI will execute your code and provide results back.
4.  **Analyze Results & Summarize:** Review results, explain errors, or summarize success concisely.

**CRITICAL INSTRUCTIONS:**
*   **OUTPUT PYTHON CODE:** Your primary output must be Python code using `cli_tools`.
*   **USE `cli_tools`:** Prefix all tool calls with `cli_tools.`.
*   **CORRECT ARGUMENTS:** Use keyword arguments (e.g., `file_path='...'`). Ensure strings are quoted.
*   **INLINE CONTENT:** **When using `cli_tools.edit` to create/overwrite files, embed the *entire file content* directly within the call as a multi-line string if possible.** Example: `cli_tools.edit(file_path='app.py', content='''import flask\\n\\napp = flask.Flask(__name__)\\n\\n@app.route("/")\\ndef hello():\\n    return "Hello"''')`
*   **AUTONOMOUS INFO GATHERING:** If you need file content/structure, generate the `cli_tools.view(...)` or `cli_tools.ls(...)` calls *first*.
*   **HANDLE RESULTS:** Use the results provided in the next turn to formulate your final response.

**Available `cli_tools` Functions:**
{chr(10).join(tools_description) if tools_description else "No `cli_tools` functions available."}

Generate the Python code using `cli_tools` needed to process the user's request, embedding content directly in `edit` calls where appropriate.
"""
        return system_prompt


    # --- CORRECTED _create_tool_definitions Method (Not used in Code Gen, but needs correct syntax) ---
    def _create_tool_definitions(self) -> list[Tool]:
        """Native tool definitions - NOT CURRENTLY USED but needs correct syntax for import."""
        tool_declarations = [] # Holds FunctionDeclaration objects

        # --- Define the view tool ---
        if "view" in AVAILABLE_TOOLS:
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
            except Exception as e:
                logging.error(f"Failed to define 'view' tool: {e}")

        # --- Define the edit tool ---
        if "edit" in AVAILABLE_TOOLS:
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
            except Exception as e:
                logging.error(f"Failed to define 'edit' tool: {e}")

        # --- Define the ls tool ---
        if "ls" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="ls",
                    description="List files and directories in a given path.",
                    parameters={ "type": "object", "properties": {
                            "path": {"type": "string", "description": "Directory path to list (default: current directory '.')."},
                            "ignore": {"type": "string", "description": "Comma-separated glob patterns to ignore (e.g., '*.pyc,__pycache__'). Optional."}
                        }}
                ))
            except Exception as e:
                logging.error(f"Failed to define 'ls' tool: {e}")

        # --- Define the grep tool ---
        if "grep" in AVAILABLE_TOOLS:
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
            except Exception as e:
                logging.error(f"Failed to define 'grep' tool: {e}")

        # --- Define the glob tool ---
        if "glob" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="glob",
                    description="Find files matching specific glob patterns recursively.",
                    parameters={ "type": "object", "properties": {
                            "pattern": {"type": "string", "description": "Glob pattern to match (e.g., '**/*.py', 'docs/**/*.md')."},
                            "path": {"type": "string", "description": "Base directory path to search within (default: '.'). Optional."}
                        }, "required": ["pattern"] }
                ))
            except Exception as e:
                logging.error(f"Failed to define 'glob' tool: {e}")

        # --- Define the bash tool ---
        if "bash" in AVAILABLE_TOOLS:
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="bash",
                    description="Execute a shell command using the system's default shell.",
                    parameters={ "type": "object", "properties": {
                            "command": {"type": "string", "description": "The shell command string to execute."},
                            "timeout": {"type": "integer", "description": "Maximum execution time in seconds (optional)."}
                        }, "required": ["command"] }
                ))
            except Exception as e:
                logging.error(f"Failed to define 'bash' tool: {e}")

        # --- Define the test_runner tool ---
        if "test_runner" in AVAILABLE_TOOLS:
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
            except Exception as e:
                logging.error(f"Failed to define 'test_runner' tool: {e}")

        logging.debug("Native tool definitions parsed (syntax check only in Code Gen mode).")
        # Return empty list as we are not using native tools in Code Gen mode
        return []
    # --- End CORRECTED Method ---