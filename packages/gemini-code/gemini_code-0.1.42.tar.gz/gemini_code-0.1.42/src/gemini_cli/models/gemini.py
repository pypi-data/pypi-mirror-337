"""
Gemini model integration for the CLI tool.
Targeting Gemini 2.5 Pro Experimental.
Includes Test Runner tool. Prompt v6 (Self-Correction Check). Syntax FIXED.
"""

import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool
import re
import json
import logging
from ..utils import count_tokens
from ..tools import get_tool, AVAILABLE_TOOLS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

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
    """Interface for Gemini models, optimized for coding assistant workflow."""

    def __init__(self, api_key, model_name="gemini-2.5-pro-exp-03-25"):
        """Initialize the Gemini model interface."""
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)

        self.generation_config = genai.types.GenerationConfig( temperature=0.5, top_p=0.95, top_k=40 )
        self.safety_settings = { "HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE", "HATE": "BLOCK_MEDIUM_AND_ABOVE", "SEXUAL": "BLOCK_MEDIUM_AND_ABOVE", "DANGEROUS": "BLOCK_MEDIUM_AND_ABOVE" }
        self.tools = self._create_tool_definitions() # Uses the corrected method below
        self.system_instruction = self._create_system_prompt() # Using v6 prompt

        try:
            logging.info(f"Creating model: {self.model_name} with tools and system instruction.")
            self.model = genai.GenerativeModel( model_name=self.model_name, generation_config=self.generation_config, safety_settings=self.safety_settings, tools=self.tools, system_instruction=self.system_instruction )
            logging.info("Testing model connectivity...")
            try:
                test_response = self.model.generate_content("Connectivity test.", request_options={'timeout': 15})
                text_content = self._extract_text_from_response(test_response)
                logging.info(f"Model connectivity test successful. Response snippet: {text_content[:50]}...")
            except Exception as test_error: logging.warning(f"Initial model connectivity test failed (may recover): {test_error}")
            self.chat = self.model.start_chat(history=[])
            logging.info("GeminiModel initialized successfully. Chat session started.")
        except Exception as e:
            logging.error(f"Fatal error initializing Gemini model '{self.model_name}': {str(e)}", exc_info=True)
            if "PERMISSION_DENIED" in str(e) or "403" in str(e) or "does not have access" in str(e).lower(): raise Exception(f"Permission denied for model '{self.model_name}'. Ensure your API key has access.") from e
            elif "API_KEY_INVALID" in str(e): raise Exception("Invalid Google API Key provided.") from e
            elif "404" in str(e) or "not found" in str(e): raise Exception(f"Model identifier '{self.model_name}' not found.") from e
            raise Exception(f"Could not initialize Gemini model: {e}") from e

    def get_available_models(self):
        return list_available_models(self.api_key)

    def generate(self, prompt: str, conversation=None) -> str | None:
        # ... (generate function remains the same as previous step) ...
        logging.info(f"Received prompt: '{prompt[:100]}...'")
        if prompt.startswith('/'):
            command = prompt.split()[0].lower()
            if command in ['/exit', '/help', '/compact']: logging.info(f"Handled command: {command}"); return None
        try:
            logging.info(f"Sending message to Gemini (using chat history)...")
            response = self.chat.send_message(prompt)
            logging.info(f"Received initial response from Gemini.")
            while True:
                function_call = self._extract_function_call_from_response(response)
                if not function_call: logging.info("No function call detected in response."); break
                logging.info(f"Detected function call: {function_call.name}")
                try:
                    api_response = self._execute_function_call(function_call)
                    function_name = function_call.name
                    logging.info(f"Function '{function_name}' executed.")
                    logging.info(f"Sending function response for '{function_name}' back to model...")
                    function_response_content = [{"function_response": { "name": function_name, "response": api_response }}]
                    response = self.chat.send_message(function_response_content)
                    logging.info(f"Received subsequent response from Gemini after function '{function_name}'.")
                except Exception as func_exec_error:
                    logging.error(f"Error executing function {getattr(function_call, 'name', 'unknown')}: {func_exec_error}", exc_info=True)
                    return f"Error executing tool '{getattr(function_call, 'name', 'unknown')}': {func_exec_error}"
            final_text = self._extract_text_from_response(response)
            logging.info(f"Final response text length: {len(final_text)}")
            final_text = self._cleanup_internal_tags(final_text)
            return final_text.strip()
        except Exception as e:
            logging.error(f"Error during generation or function call processing: {str(e)}", exc_info=True)
            if "429" in str(e): return "Error: API rate limit exceeded."
            if "500" in str(e) or "503" in str(e): return "Error: Gemini API server error."
            if "PERMISSION_DENIED" in str(e) or "403" in str(e) or "does not have access" in str(e).lower(): return f"Error: Permission denied for model '{self.model_name}'."
            return f"An unexpected error occurred during generation: {str(e)}"


    def _extract_function_call_from_response(self, response):
        # ... (remains the same) ...
        try:
            if (response.candidates and response.candidates[0].content and response.candidates[0].content.parts and response.candidates[0].content.parts[0].function_call): return response.candidates[0].content.parts[0].function_call
        except (IndexError, AttributeError, KeyError, TypeError): pass
        return None

    def _execute_function_call(self, function_call):
        # ... (remains the same) ...
        function_name = function_call.name
        args = dict(function_call.args) if hasattr(function_call, 'args') and function_call.args else {}
        logging.info(f"Attempting execution: function='{function_name}', args={args}")
        try:
            tool_instance = get_tool(function_name)
            if not tool_instance: raise ValueError(f"Tool '{function_name}' unavailable.")
            result = tool_instance.execute(**args)
            logging.info(f"Function '{function_name}' raw result type: {type(result)}")
            try: json.dumps(result); api_result = {"result": result}
            except TypeError: logging.warning(f"Result for '{function_name}' not JSON serializable, converting to string."); api_result = {"result": str(result)}
            logging.debug(f"Function '{function_name}' API response payload: {api_result}")
            return api_result
        except Exception as e: logging.error(f"Exception during func execution '{function_name}': {e}", exc_info=True); raise

    def _extract_text_from_response(self, response):
        # ... (remains the same) ...
        try:
            all_text = []
            if response.candidates:
                 for part in response.candidates[0].content.parts:
                     if hasattr(part, 'text'): all_text.append(part.text)
                 return "".join(all_text)
            elif hasattr(response, 'text'): return response.text
            else: logging.warning("Could not extract text from response structure."); return ""
        except Exception as e: logging.error(f"Error extracting text: {e}", exc_info=True); return f"Error extracting response text: {e}"

    def _cleanup_internal_tags(self, text: str) -> str:
        # ... (remains the same) ...
        text = re.sub(r"<thinking>.*?</thinking>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"<plan>.*?</plan>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"<get_bearings>.*?</get_bearings>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"<verification>.*?</verification>\s*", "", text, flags=re.DOTALL)
        return text.strip()

    # --- Uses the V6 Prompt with Self-Correction Check ---
    def _create_system_prompt(self) -> str:
        """Creates the system instruction prompt including a self-correction step."""
        # ... (V6 prompt remains the same as previous step) ...
        tools_description = []
        if AVAILABLE_TOOLS:
            for name, tool_class in AVAILABLE_TOOLS.items():
                try: tool_instance = tool_class(); desc = getattr(tool_instance, 'description', f'No description for {name}.'); tools_description.append(f"- {name}: {desc}")
                except Exception as e: logging.warning(f"Could not get description for tool '{name}': {e}")
        else: logging.warning("AVAILABLE_TOOLS dictionary not found or empty.")

        system_prompt = f"""You are 'Gemini Code', an expert AI pair programmer in a CLI environment. Your primary goal is to assist users by directly interacting with the project using your available tools.

**Core Workflow & Behavior:**

1.  **Analyze & Gather Info:** Understand the user's goal. **CRITICAL:** If you need info about files/code, **use tools (`view`, `ls`, etc.) *immediately* and *autonomously* to get it.** Do NOT ask the user first. Integrate the info silently.
2.  **Plan:** Mentally devise a plan of function calls needed (info gathering, execution, verification).
3.  **Execute:** Call the necessary functions (`edit`, `bash`, `test_runner`, etc.) via function calling mechanism.
4.  **Verify:** Use tools (`view`, `grep`, `test_runner`, etc.) to confirm your actions succeeded. If verification fails, loop back to Plan/Execute to fix.
5.  **Pre-Response Check (Self-Correction):** **CRITICAL:** Before formulating your final summary for the user, review your internal plan and intended response. If your planned response is simply asking for information (e.g., "I need to see file X", "What's in file Y?") that you *could* obtain using an available tool (like `view`), **DO NOT output that response.** Instead, **revise your plan to call the appropriate tool** and continue the workflow (Execute -> Verify). Only proceed to the final summary once all necessary actions are complete.
6.  **Summarize Outcome:** Once all actions are complete and verified, report concisely to the user **what you did** and the outcome (e.g., "I created `app.py`...", "I added the function... tests passed."). Avoid large code blocks unless requested or showing an error.

**Key Instructions:**
*   **Act Autonomously:** Especially for gathering information (Step 1/2). Don't ask, DO.
*   **Self-Correct:** Use the Pre-Response Check (Step 5) to avoid asking for info you can get yourself. If your first thought is to ask, STOP, use the tool instead.
*   **Use Tools for Action & Verification.**
*   **Be Concise in Final Summary.**

**Example Interaction (Illustrating Self-Correction):**

*   **User:** Can you build the frontend based on `plan.md`?
*   **Assistant (Internal Thought - Analyze):** User wants frontend built. Need content of `plan.md`.
*   **Assistant (Internal Thought - Gather Info):** Okay, I *must* use the `view` tool now.
*   **Assistant (Action):** [Calls `view(file_path='plan.md')`]
*   **Assistant (Internal Thought after getting file content):** Got the plan. It involves creating `index.html` and `style.css`.
*   **Assistant (Internal Thought - Plan):** 1. Call `edit` for `index.html`. 2. Call `edit` for `style.css`. 3. Call `ls` to verify creation.
*   **Assistant (Action):** [Calls `edit(file_path='index.html', new_content='...')`]
*   **Assistant (Action):** [Calls `edit(file_path='style.css', new_content='...')`]
*   **Assistant (Internal Thought - Verify):** Edits done. Verify existence.
*   **Assistant (Action):** [Calls `ls(path='.')`]
*   **Assistant (Internal Thought after getting ls result):** Files `index.html` and `style.css` are present. Verification successful.
*   **Assistant (Internal Thought - Pre-Response Check):** My plan is complete. I am not about to ask for info I can get. Proceed to summary.
*   **Assistant (Response to User):** Okay, I have created `index.html` and `style.css` based on the plan in `plan.md`.

**AVAILABLE FUNCTIONS:**
{chr(10).join(tools_description) if tools_description else "No functions currently available."}

Now, process the user's request following this workflow, especially the **autonomous information gathering** and the **pre-response self-correction check**.
"""
        return system_prompt

    # --- CORRECTED _create_tool_definitions Method ---
    def _create_tool_definitions(self) -> list[Tool]:
        """Create genai.Tool definitions for all available tools."""
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

        # --- Define other tools similarly if enabled... ---
        # if "web" in AVAILABLE_TOOLS: ...
        # if "linter_checker" in AVAILABLE_TOOLS: ...


        # Wrap all successful declarations in a single Tool object
        if tool_declarations:
             gemini_tools = [Tool(function_declarations=tool_declarations)]
             logging.info(f"Created Tool object with {len(tool_declarations)} function declarations.")
             return gemini_tools
        else:
             logging.warning("No tool declarations were successfully created.")
             return []
    # --- End CORRECTED Method ---