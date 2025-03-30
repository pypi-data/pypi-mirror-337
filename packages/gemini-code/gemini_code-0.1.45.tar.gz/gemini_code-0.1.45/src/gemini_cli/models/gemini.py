"""
Gemini model integration for the CLI tool.
Targeting Gemini 2.5 Pro Experimental.
IMPLEMENTING CLAUDE CODE STYLE WORKFLOW (CODE GENERATION).
Includes Test Runner tool. Prompt v10.
"""

import google.generativeai as genai
# Native function calling types are NO LONGER needed here
# from google.generativeai.types import FunctionDeclaration, Tool, FunctionCall
import re
import json
import logging
import ast # Using AST for potentially safer parsing than pure regex
import shlex # For parsing bash commands safely if needed later

from ..utils import count_tokens
from ..tools import get_tool, AVAILABLE_TOOLS # Still need these to EXECUTE tools

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

# Regex to find potential tool calls in the generated code block
# Looks for cli_tools.func_name(arg1="value1", arg2=...)
# It's basic and might need refinement based on model output variations
TOOL_CALL_PATTERN = re.compile(r"cli_tools\.(\w+)\((.*?)\)")

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

        self.generation_config = genai.types.GenerationConfig(
            temperature=0.4, # Slightly lower temp might yield more predictable code
            top_p=0.95,
            top_k=40,
            # Stop sequences might be useful if model adds extra conversational text
            # stop_sequences=["\nHuman:", "\nUser:"]
        )
        self.safety_settings = { "HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE", "HATE": "BLOCK_MEDIUM_AND_ABOVE", "SEXUAL": "BLOCK_MEDIUM_AND_ABOVE", "DANGEROUS": "BLOCK_MEDIUM_AND_ABOVE" }

        # CRITICAL: NO NATIVE TOOLS CONFIGURED
        # self.tools = self._create_tool_definitions() # REMOVED

        # Use the V10 prompt instructing code generation
        self.system_instruction = self._create_system_prompt()

        try:
            logging.info(f"Creating model: {self.model_name} for code generation workflow.")
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                # tools=self.tools, # REMOVED
                system_instruction=self.system_instruction
            )
            logging.info("Testing model connectivity...")
            try:
                # Test basic generation, not function calling
                test_response = self.model.generate_content("Say 'Test OK'.", request_options={'timeout': 15})
                text_content = self._extract_text_from_response(test_response)
                logging.info(f"Model connectivity test successful. Response: {text_content[:50]}...")
                if 'Test OK' not in text_content:
                     logging.warning("Connectivity test response unexpected.")
            except Exception as test_error: logging.warning(f"Initial model connectivity test failed (may recover): {test_error}")

            # Start chat session - history management is still useful
            self.chat = self.model.start_chat(history=[])
            logging.info("GeminiModel initialized successfully (Code Gen Mode). Chat session started.")
        except Exception as e:
            # ... (Error handling remains the same) ...
            logging.error(f"Fatal error initializing Gemini model '{self.model_name}': {str(e)}", exc_info=True)
            if "PERMISSION_DENIED" in str(e) or "403" in str(e) or "does not have access" in str(e).lower(): raise Exception(f"Permission denied for model '{self.model_name}'. Ensure API key has access.") from e
            elif "API_KEY_INVALID" in str(e): raise Exception("Invalid Google API Key provided.") from e
            elif "404" in str(e) or "not found" in str(e): raise Exception(f"Model identifier '{self.model_name}' not found.") from e
            raise Exception(f"Could not initialize Gemini model: {e}") from e

    # ... (get_available_models remains the same) ...
    def get_available_models(self): return list_available_models(self.api_key)

    # --- Rewritten generate function for Code Generation Workflow ---
    def generate(self, prompt: str, conversation=None) -> str | None:
        logging.info(f"Code Gen Workflow - Received prompt: '{prompt[:100]}...'")

        if prompt.startswith('/'):
             command = prompt.split()[0].lower()
             if command in ['/exit', '/help', '/compact']: logging.info(f"Handled command: {command}"); return None

        try:
            # === Turn 1: Get Model's Planned Code ===
            logging.info("Sending initial prompt to Gemini for code generation...")
            response = self.chat.send_message(prompt)
            # --- ADDING RAW RESPONSE LOGGING ---
            logging.debug(f"RAW Gemini Response Object (Initial Code Gen): {response}")
            # --- ---
            generated_text = self._extract_text_from_response(response)
            logging.info("Received generated text potentially containing tool code.")
            logging.debug(f"Generated Text:\n---\n{generated_text}\n---")

            # === Parse and Execute Tool Calls ===
            tool_calls_found = self._parse_and_execute_tool_calls(generated_text)

            if not tool_calls_found:
                logging.info("No tool calls found in the response. Returning generated text directly.")
                # If no tools called, assume the text is the final answer.
                # Could potentially add a reflection step here if desired.
                return generated_text.strip()

            # === Turn 2: Send Results Back to Model for Summary ===
            # Format the results clearly
            results_feedback = "Okay, I executed the requested tool calls. Here are the results:\n\n"
            for call_info in tool_calls_found:
                 results_feedback += f"Function Call: {call_info['call_str']}\n"
                 results_feedback += f"Result:\n```\n{call_info['result']}\n```\n---\n"

            results_feedback += "\nPlease review these results and provide a final summary or response to the user based on the outcome."

            logging.info("Sending tool execution results back to Gemini for summary...")
            response = self.chat.send_message(results_feedback)
            # --- ADDING RAW RESPONSE LOGGING ---
            logging.debug(f"RAW Gemini Response Object (After Results Feedback): {response}")
            # --- ---
            final_summary = self._extract_text_from_response(response)
            logging.info("Received final summary from Gemini.")

            return final_summary.strip()

        except Exception as e:
            # ... (Error handling remains the same) ...
            logging.error(f"Error during Code Gen generation/execution: {str(e)}", exc_info=True)
            if "429" in str(e): return "Error: API rate limit exceeded."
            if "500" in str(e) or "503" in str(e): return "Error: Gemini API server error."
            if "PERMISSION_DENIED" in str(e) or "403" in str(e) or "does not have access" in str(e).lower(): return f"Error: Permission denied for model '{self.model_name}'."
            return f"An unexpected error occurred during generation: {str(e)}"

    def _parse_and_execute_tool_calls(self, text: str) -> list[dict]:
        """Finds, parses, and executes `cli_tools.X(...)` calls in text."""
        executed_calls = []
        # Find all matches using regex
        matches = TOOL_CALL_PATTERN.finditer(text)

        for match in matches:
            call_str = match.group(0) # The full matched string like cli_tools.view(...)
            func_name = match.group(1)
            args_str = match.group(2)
            logging.info(f"Found potential tool call: {call_str}")

            args = {}
            try:
                # Attempt to parse args string as Python keyword args
                # We wrap it in a dummy function call `f(...)` to make it valid Python code
                # Note: This is safer than eval() but still has risks if model generates malicious args_str.
                # It relies on ast only evaluating literals.
                node = ast.parse(f"f({args_str})")
                call_node = node.body[0].value
                for kw in call_node.keywords:
                    # Use ast.literal_eval to safely evaluate the argument value
                    # Handles strings, numbers, booleans, lists, dicts, tuples, None
                    try:
                        args[kw.arg] = ast.literal_eval(kw.value)
                    except ValueError:
                         logging.warning(f"Could not literal_eval value for arg '{kw.arg}' in '{call_str}'. Treating as raw string.")
                         # Fallback for complex/unsupported literals: try to get source segment (less safe)
                         if hasattr(kw.value, 's'): # String literal
                            args[kw.arg] = kw.value.s
                         else: # If it's not a simple literal, maybe just use its string representation? Risky.
                            # Or skip this argument / raise error
                            logging.error(f"Unsupported argument type for arg '{kw.arg}' in '{call_str}'. Skipping argument.")
                            # Decide how to handle - skip, error, etc. For now, skip.
                            # args[kw.arg] = "ERROR_UNPARSABLE_ARG"


            except Exception as parse_error:
                logging.error(f"Failed to parse arguments for '{call_str}': {parse_error}", exc_info=True)
                executed_calls.append({
                    "call_str": call_str,
                    "result": f"Error: Failed to parse arguments - {parse_error}"
                })
                continue # Skip execution if args parsing failed

            # Execute the actual tool
            try:
                logging.info(f"Executing parsed call: func='{func_name}', args={args}")
                tool_instance = get_tool(func_name)
                if not tool_instance:
                    raise ValueError(f"Tool '{func_name}' is not available.")

                result = tool_instance.execute(**args)
                # Ensure result is string for feedback
                result_str = str(result) if result is not None else "(No output)"

                executed_calls.append({
                    "call_str": call_str,
                    "result": result_str
                })
                logging.info(f"Execution successful for '{call_str}'. Result length: {len(result_str)}")

            except Exception as exec_error:
                logging.error(f"Exception during execution of '{call_str}': {exec_error}", exc_info=True)
                executed_calls.append({
                    "call_str": call_str,
                    "result": f"Error during execution: {exec_error}"
                })

        return executed_calls


    def _extract_text_from_response(self, response):
        # ... (remains the same) ...
        try:
            all_text = []
            if response.candidates:
                 for part in response.candidates[0].content.parts:
                     # Ensure part is text, not other potential future part types
                     if hasattr(part, 'text'): all_text.append(part.text)
                 return "".join(all_text)
            elif hasattr(response, 'text'): return response.text # Should be less common now
            else: logging.warning("Could not extract text from response structure."); return ""
        except Exception as e: logging.error(f"Error extracting text: {e}", exc_info=True); return f"Error extracting response text: {e}"

    def _cleanup_internal_tags(self, text: str) -> str:
        # Might still be useful if model adds thinking blocks
        text = re.sub(r"<thinking>.*?</thinking>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"<plan>.*?</plan>\s*", "", text, flags=re.DOTALL)
        # Add cleanup for potential Python code comments if desired
        # text = re.sub(r"# Thinking:.*?\n", "", text)
        # text = re.sub(r"# Plan:.*?\n", "", text)
        return text.strip()

    # --- Uses the V10 Prompt for Code Generation ---
    def _create_system_prompt(self) -> str:
        """Creates the system instruction prompt for code-generation workflow."""
        tools_description = []
        if AVAILABLE_TOOLS:
            # Format description for code generation context
            for name, tool_class in AVAILABLE_TOOLS.items():
                try:
                    tool_instance = tool_class()
                    desc = getattr(tool_instance, 'description', f'Tool {name}')
                    # Try to get parameter info (this is complex, basic version here)
                    # In a real scenario, tools might need explicit param definitions
                    params = "..." # Placeholder - Ideally inspect signature or have metadata
                    tools_description.append(f"`cli_tools.{name}({params})`: {desc}")
                except Exception as e:
                     logging.warning(f"Could not get description/params for tool '{name}': {e}")
                     tools_description.append(f"`cli_tools.{name}(...)`: Tool to {name} files/system.")

        else:
             logging.warning("AVAILABLE_TOOLS dictionary not found or empty.")

        system_prompt = f"""You are 'Gemini Code', an expert AI pair programmer operating in a CLI. **You interact with the user's project directory by GENERATING PYTHON CODE that calls predefined tools.**

**Your Goal:** Fulfill the user's request by generating Python code snippets using the `cli_tools` module.

**Workflow:**

1.  **Analyze Request & Plan:** Understand the user's goal. Determine the sequence of tool calls needed. Think step-by-step. Use comments like `# Thinking:` or `# Plan:` for your internal reasoning.
2.  **Generate Tool Code:** Write Python code that calls functions from the `cli_tools` module (e.g., `cli_tools.view(file_path='...')`, `cli_tools.edit(...)`). Ensure arguments are correct Python syntax (e.g., strings are quoted). **Generate ONLY the necessary `cli_tools` calls.**
3.  **Execution & Results:** The CLI environment will execute the code you generate and provide the results back to you in the next turn.
4.  **Analyze Results & Summarize:** Review the execution results. If errors occurred, explain them. If successful, provide a concise summary to the user about what actions were taken based on the results. Avoid showing raw tool output unless necessary to explain an error or result.

**CRITICAL INSTRUCTIONS:**
*   **OUTPUT PYTHON CODE:** Your primary output when action is needed should be Python code using the `cli_tools` functions.
*   **USE `cli_tools`:** All tool interactions MUST go through the `cli_tools` module (e.g., `cli_tools.view(...)`, NOT `view(...)` or `api.view(...)`).
*   **CORRECT ARGUMENTS:** Ensure arguments in your generated code are valid Python (quoted strings, correct types if possible). Use keyword arguments (e.g., `file_path='...'`).
*   **AUTONOMOUS INFO GATHERING:** If you need file content or directory structure, your *first* generated code block should include the necessary `cli_tools.view(...)` or `cli_tools.ls(...)` calls.
*   **COMPLETE ACTIONS:** Generate all necessary code calls to fulfill the request in one block if possible.
*   **HANDLE RESULTS:** In the turn *after* your code is executed, use the provided results to formulate your final response to the user.

**Available `cli_tools` Functions:**
{chr(10).join(tools_description) if tools_description else "No `cli_tools` functions available."}

Generate the Python code using `cli_tools` needed to process the user's request.
"""
        return system_prompt


    # --- _create_tool_definitions is NO LONGER USED for native function calling ---
    # You can remove this method or keep it commented out for reference.
    # def _create_tool_definitions(self) -> list[Tool]:
    #     """Native tool definitions - NOT USED in Code Gen Workflow."""
    #     pass # Or return []
    # Keep the corrected version just in case we switch back
    def _create_tool_definitions(self) -> list[Tool]:
        """Native tool definitions - NOT CURRENTLY USED but kept for reference."""
        tool_declarations = []
        # ... (Same corrected code for definitions as previous step) ...
        if "view" in AVAILABLE_TOOLS: try: tool_declarations.append(FunctionDeclaration( name="view", description="View the contents of a specific file.", parameters={ "type": "object", "properties": { "file_path": {"type": "string", "description": "Path to the file to view."}, "offset": {"type": "integer", "description": "Line number to start reading from (1-based index, optional)."}, "limit": {"type": "integer", "description": "Maximum number of lines to read (optional)."} }, "required": ["file_path"] } )) except Exception as e: logging.error(f"Failed to define 'view' tool: {e}")
        if "edit" in AVAILABLE_TOOLS: try: tool_declarations.append(FunctionDeclaration( name="edit", description="Edit a file: create it, replace its content, replace a specific string, or delete a string.", parameters={ "type": "object", "properties": { "file_path": {"type": "string", "description": "Path to the file to edit or create."}, "new_content": {"type": "string", "description": "Full content for a new file or to completely overwrite an existing file. Use if `old_string` is omitted."}, "old_string": {"type": "string", "description": "The exact text to find and replace. If omitted, `new_content` overwrites the file."}, "new_string": {"type": "string", "description": "Text to replace `old_string` with. If replacing, this is required. Use an empty string ('') to delete `old_string`."} }, "required": ["file_path"] } )) except Exception as e: logging.error(f"Failed to define 'edit' tool: {e}")
        if "ls" in AVAILABLE_TOOLS: try: tool_declarations.append(FunctionDeclaration( name="ls", description="List files and directories in a given path.", parameters={ "type": "object", "properties": { "path": {"type": "string", "description": "Directory path to list (default: current directory '.')."}, "ignore": {"type": "string", "description": "Comma-separated glob patterns to ignore (e.g., '*.pyc,__pycache__'). Optional."} }} )) except Exception as e: logging.error(f"Failed to define 'ls' tool: {e}")
        if "grep" in AVAILABLE_TOOLS: try: tool_declarations.append(FunctionDeclaration( name="grep", description="Search for a pattern (regex) in files within a directory.", parameters={ "type": "object", "properties": { "pattern": {"type": "string", "description": "Regular expression pattern to search for."}, "path": {"type": "string", "description": "Directory path to search within (default: '.'). Optional."}, "include": {"type": "string", "description": "Glob pattern for files to include (e.g., '*.py', '*.txt'). Searches all files if omitted. Optional."}}, "required": ["pattern"] } )) except Exception as e: logging.error(f"Failed to define 'grep' tool: {e}")
        if "glob" in AVAILABLE_TOOLS: try: tool_declarations.append(FunctionDeclaration( name="glob", description="Find files matching specific glob patterns recursively.", parameters={ "type": "object", "properties": { "pattern": {"type": "string", "description": "Glob pattern to match (e.g., '**/*.py', 'docs/**/*.md')."}, "path": {"type": "string", "description": "Base directory path to search within (default: '.'). Optional."}}, "required": ["pattern"] } )) except Exception as e: logging.error(f"Failed to define 'glob' tool: {e}")
        if "bash" in AVAILABLE_TOOLS: try: tool_declarations.append(FunctionDeclaration( name="bash", description="Execute a shell command using the system's default shell.", parameters={ "type": "object", "properties": { "command": {"type": "string", "description": "The shell command string to execute."}, "timeout": {"type": "integer", "description": "Maximum execution time in seconds (optional)."} }, "required": ["command"] } )) except Exception as e: logging.error(f"Failed to define 'bash' tool: {e}")
        if "test_runner" in AVAILABLE_TOOLS: try: test_runner_declaration = FunctionDeclaration( name="test_runner", description="Runs automated tests using the project's test runner (e.g., pytest).", parameters={ "type": "object", "properties": { "test_path": {"type": "string", "description": "Specific file or directory path to test (optional, runs discovered tests if omitted)."}, "options": {"type": "string", "description": "Additional command-line options for the test runner (e.g., '-k my_test', '-v', '--cov'). Optional."}, "runner_command": {"type": "string", "description": "The command for the test runner (default: 'pytest'). Optional."} }}); tool_declarations.append(test_runner_declaration) except Exception as e: logging.error(f"Failed to define 'test_runner' tool: {e}")
        # Return empty list as we are not using native tools
        return []