"""
Gemini model integration for the CLI tool.
Enhanced for a structured coding assistant workflow.
Includes Test Runner tool.
"""

import google.generativeai as genai
# Import the necessary types for function calling
from google.generativeai.types import FunctionDeclaration, Tool
import re
import json
import logging
from ..utils import count_tokens
# Assuming get_tool correctly retrieves your tool *instance* based on name
# And AVAILABLE_TOOLS maps names to tool *classes* (needed for system prompt)
from ..tools import get_tool, AVAILABLE_TOOLS # Ensure AVAILABLE_TOOLS includes your tools

# Configure logging more verbosely for debugging if needed
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

def list_available_models(api_key):
    """List all available models from Google's Generative AI API."""
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        gemini_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                model_info = {
                    "name": model.name,
                    "display_name": model.display_name,
                    "description": model.description,
                    "supported_generation_methods": model.supported_generation_methods
                }
                gemini_models.append(model_info)
        return gemini_models
    except Exception as e:
        logging.error(f"Error listing models: {str(e)}")
        return [{"error": str(e)}]

class GeminiModel:
    """Interface for Gemini models, optimized for coding assistant workflow."""

    def __init__(self, api_key, model_name="gemini-1.5-pro-latest"): # Using latest pro model
        """Initialize the Gemini model interface."""
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)

        self.generation_config = genai.types.GenerationConfig(
            temperature=0.6,
            top_p=0.95,
            top_k=40,
        )

        self.safety_settings = {
            "HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
            "HATE": "BLOCK_MEDIUM_AND_ABOVE",
            "SEXUAL": "BLOCK_MEDIUM_AND_ABOVE",
            "DANGEROUS": "BLOCK_MEDIUM_AND_ABOVE",
        }

        # Create Tool definitions (FunctionDeclarations wrapped in a Tool object)
        self.tools = self._create_tool_definitions() # Will be list[Tool]

        # Create the detailed System Instruction enforcing the workflow
        self.system_instruction = self._create_system_prompt()

        try:
            logging.info(f"Creating model: {model_name} with tools and system instruction.")
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                tools=self.tools,
                system_instruction=self.system_instruction
            )

            logging.info("Testing model connectivity...")
            try:
                test_response = self.model.generate_content("Test prompt", request_options={'timeout': 10}) # Add timeout
                text_content = self._extract_text_from_response(test_response)
                logging.info(f"Model connectivity test successful. Response snippet: {text_content[:50]}...")
            except Exception as test_error:
                 logging.warning(f"Initial model connectivity test failed (may recover): {test_error}")

            # Start a chat session to maintain conversation history
            self.chat = self.model.start_chat(history=[])
            logging.info("GeminiModel initialized successfully. Chat session started.")

        except Exception as e:
            logging.error(f"Fatal error initializing Gemini model '{self.model_name}': {str(e)}", exc_info=True)
            if "API_KEY_INVALID" in str(e):
                 raise Exception("Invalid Google API Key provided.") from e
            elif "PERMISSION_DENIED" in str(e) or "403" in str(e):
                 raise Exception(f"Permission denied for model '{self.model_name}'. Check API key permissions.") from e
            raise Exception(f"Could not initialize Gemini model: {e}") from e


    def get_available_models(self):
        """Get a list of available Gemini models."""
        return list_available_models(self.api_key)

    def generate(self, prompt: str, conversation=None) -> str | None:
        """
        Generate a response using the chat session, handling the function calling workflow.
        """
        logging.info(f"Received prompt: '{prompt[:100]}...'")

        if prompt.startswith('/'):
            command = prompt.split()[0].lower()
            if command in ['/exit', '/help', '/compact']:
                logging.info(f"Handled command: {command}")
                return None # Let main loop handle these

        try:
            logging.info(f"Sending message to Gemini (using chat history)...")
            response = self.chat.send_message(prompt)
            logging.info(f"Received initial response from Gemini.")

            # --- Function Calling Loop ---
            while True:
                function_call = self._extract_function_call_from_response(response)
                if not function_call:
                    logging.info("No function call detected in response.")
                    break # Exit loop if no function call

                logging.info(f"Detected function call: {function_call.name}")
                try:
                    api_response = self._execute_function_call(function_call)
                    function_name = function_call.name # Store name for logging/response
                    logging.info(f"Function '{function_name}' executed.")

                    logging.info(f"Sending function response for '{function_name}' back to model...")
                    function_response_content = [{"function_response": {
                        "name": function_name,
                        "response": api_response
                    }}]
                    response = self.chat.send_message(function_response_content)
                    logging.info(f"Received subsequent response from Gemini after function '{function_name}'.")

                except Exception as func_exec_error:
                    logging.error(f"Error executing function {getattr(function_call, 'name', 'unknown')}: {func_exec_error}", exc_info=True)
                    return f"Error executing tool '{getattr(function_call, 'name', 'unknown')}': {func_exec_error}"

            # --- End Function Calling Loop ---

            final_text = self._extract_text_from_response(response)
            logging.info(f"Final response text length: {len(final_text)}")
            final_text = self._cleanup_internal_tags(final_text)
            return final_text.strip()

        except Exception as e:
            logging.error(f"Error during generation or function call processing: {str(e)}", exc_info=True)
            if "429" in str(e): return "Error: API rate limit exceeded. Please wait and try again."
            if "500" in str(e) or "503" in str(e): return "Error: The Gemini API reported a server error. Please try again later."
            return f"An unexpected error occurred during generation: {str(e)}"

    def _extract_function_call_from_response(self, response):
        """Safely extracts the first FunctionCall object from the model's response."""
        try:
            if (response.candidates and
                response.candidates[0].content and
                response.candidates[0].content.parts and
                response.candidates[0].content.parts[0].function_call):
                return response.candidates[0].content.parts[0].function_call
        except (IndexError, AttributeError, KeyError, TypeError) as e:
            logging.debug(f"Did not find function call in response structure: {e}")
        return None

    def _execute_function_call(self, function_call):
        """Executes the requested function call and returns API-ready response."""
        function_name = function_call.name
        args = dict(function_call.args) if hasattr(function_call, 'args') and function_call.args else {}
        logging.info(f"Attempting execution: function='{function_name}', args={args}")

        try:
            tool_instance = get_tool(function_name)
            if not tool_instance:
                raise ValueError(f"Tool '{function_name}' is not available or failed to instantiate.")

            result = tool_instance.execute(**args)
            logging.info(f"Function '{function_name}' raw result type: {type(result)}")

            try:
                json.dumps(result)
                api_result = {"result": result}
            except TypeError:
                logging.warning(f"Result for function '{function_name}' is not JSON serializable, converting to string.")
                api_result = {"result": str(result)}

            logging.debug(f"Function '{function_name}' API response payload: {api_result}")
            return api_result

        except Exception as e:
            logging.error(f"Exception during function execution '{function_name}': {e}", exc_info=True)
            raise

    def _extract_text_from_response(self, response):
        """Extracts concatenated text parts from a model response, ignoring function calls/responses."""
        try:
            all_text = []
            if response.candidates:
                 for part in response.candidates[0].content.parts:
                     if hasattr(part, 'text'):
                         all_text.append(part.text)
                 return "".join(all_text)
            elif hasattr(response, 'text'): return response.text
            else: logging.warning("Could not extract text from response structure."); return ""
        except Exception as e:
            logging.error(f"Error extracting text from response: {e}", exc_info=True)
            return f"Error extracting response text: {e}"

    def _cleanup_internal_tags(self, text: str) -> str:
        """Removes internal <thinking>, <plan>, etc. tags from the final response."""
        text = re.sub(r"<thinking>.*?</thinking>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"<plan>.*?</plan>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"<get_bearings>.*?</get_bearings>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"<verification>.*?</verification>\s*", "", text, flags=re.DOTALL)
        return text.strip()


    def _create_system_prompt(self) -> str:
        """Creates the system instruction prompt enforcing the coding workflow."""
        tools_description = []
        if AVAILABLE_TOOLS:
            for name, tool_class in AVAILABLE_TOOLS.items():
                try:
                    tool_instance = tool_class()
                    desc = getattr(tool_instance, 'description', f'No description for {name}.')
                    tools_description.append(f"- {name}: {desc}")
                except Exception as e:
                     logging.warning(f"Could not get description for tool '{name}': {e}")
        else:
             logging.warning("AVAILABLE_TOOLS dictionary not found or empty.")

        # --- Updated System Prompt with mention of testing ---
        system_prompt = f"""You are 'Gemini Code', an expert AI pair programmer embedded in a CLI environment. Your primary goal is to assist users with software development tasks by directly interacting with the project using your available tools. You MUST follow this structured workflow for every request:

1.  **<thinking>**
    *   Analyze the user's request deeply. What is the *actual* goal? Identify ambiguities. Break down the request. Anticipate issues. Determine necessary tools for information gathering and execution.
    *   This section is for your internal reasoning ONLY and will be stripped from the final output.
    **</thinking>**

2.  **<get_bearings>**
    *   If information about the current project state (files, content) is needed, use tools (`ls`, `view`, `glob`, `grep`) *immediately and autonomously* to gather it. DO NOT ask the user for information you can retrieve yourself. Record key findings briefly.
    *   This section is for your internal reasoning ONLY and will be stripped from the final output.
    **</get_bearings>**

3.  **<plan>**
    *   Based on the request and bearings, create a concise, step-by-step plan detailing the *exact* function calls you will make. Include calls for creating files/directories, editing code, **running tests/linters (if appropriate and available)**, and final verification. Specify exact arguments.
    *   This section is for your internal reasoning ONLY and will be stripped from the final output.
    **</plan>**

4.  **EXECUTE FUNCTION CALLS:**
    *   Execute the planned function calls sequentially using the Gemini function calling mechanism. The results will be provided back to you.

5.  **<verification>**
    *   After function calls (especially `edit` or `bash`), use tools to verify the changes (e.g., `view`, `grep`).
    *   **Crucially, if tests exist and `test_runner` is available, use `test_runner` to confirm changes didn't break anything.**
    *   If verification fails, analyze the error and attempt to correct it by replanning and executing new function calls.
    *   This section is for your internal reasoning ONLY and will be stripped from the final output.
    **</verification>**

6.  **SUMMARIZE FOR USER:**
    *   Once the plan is complete and verified, provide a **concise summary** to the user. State clearly what you did (e.g., "I created `app.py`...", "I added the function to `utils.py` and verified it with `test_runner`. Tests passed."). Do NOT show large code blocks unless requested or needed to show an error state.

**CRITICAL INSTRUCTIONS:**
*   **AUTONOMOUS TOOL USE:** Prioritize using tools for information gathering *before* asking the user or executing changes.
*   **ACTION-ORIENTED:** Fulfill requests by *calling functions* (`edit`, `bash`, `test_runner`, etc.), not just by discussing code.
*   **VERIFY CHANGES:** Use available tools (`view`, `grep`, **`test_runner`**) to verify the success and correctness of your actions.
*   **CONCISE OUTPUT:** Keep your final summary to the user brief and focused on actions and outcome.
*   **INTERNAL TAGS:** Use the `<thinking>`, `<get_bearings>`, `<plan>`, `<verification>` tags internally.

**AVAILABLE FUNCTIONS:**
{chr(10).join(tools_description) if tools_description else "No functions currently available."}

Now, begin processing the user's request following this exact workflow.
"""
        return system_prompt


    def _create_tool_definitions(self) -> list[Tool]:
        """Create genai.Tool definitions for all available tools."""
        tool_declarations = [] # Holds FunctionDeclaration objects

        # Define tools based on AVAILABLE_TOOLS to ensure consistency
        # (Manual definitions kept here for now, but ensure they match __init__.py)

        # --- Define the view tool ---
        if "view" in AVAILABLE_TOOLS:
             try: tool_declarations.append(FunctionDeclaration(name="view",description="View the contents of a specific file.",parameters={ "type": "object", "properties": {"file_path": {"type": "string", "description": "Path to the file to view."},"offset": {"type": "integer", "description": "Line number to start reading from (1-based index, optional)."},"limit": {"type": "integer", "description": "Maximum number of lines to read (optional)."} }, "required": ["file_path"] }))
             except Exception as e: logging.error(f"Failed to define 'view' tool: {e}")

        # --- Define the edit tool ---
        if "edit" in AVAILABLE_TOOLS:
             try: tool_declarations.append(FunctionDeclaration(name="edit",description="Edit a file: create it, replace its content, replace a specific string, or delete a string.",parameters={ "type": "object", "properties": {"file_path": {"type": "string", "description": "Path to the file to edit or create."},"new_content": {"type": "string", "description": "Full content for a new file or to completely overwrite an existing file. Use if `old_string` is omitted."}, "old_string": {"type": "string", "description": "The exact text to find and replace. If omitted, `new_content` overwrites the file."}, "new_string": {"type": "string", "description": "Text to replace `old_string` with. If replacing, this is required. Use an empty string ('') to delete `old_string`."} }, "required": ["file_path"] }))
             except Exception as e: logging.error(f"Failed to define 'edit' tool: {e}")

        # --- Define the ls tool ---
        if "ls" in AVAILABLE_TOOLS:
             try: tool_declarations.append(FunctionDeclaration(name="ls",description="List files and directories in a given path.",parameters={ "type": "object", "properties": { "path": {"type": "string", "description": "Directory path to list (default: current directory '.')."}, "ignore": {"type": "string", "description": "Comma-separated glob patterns to ignore (e.g., '*.pyc,__pycache__'). Optional."} }}))
             except Exception as e: logging.error(f"Failed to define 'ls' tool: {e}")

        # --- Define the grep tool ---
        if "grep" in AVAILABLE_TOOLS:
             try: tool_declarations.append(FunctionDeclaration(name="grep",description="Search for a pattern (regex) in files within a directory.",parameters={ "type": "object", "properties": {"pattern": {"type": "string", "description": "Regular expression pattern to search for."}, "path": {"type": "string", "description": "Directory path to search within (default: '.'). Optional."}, "include": {"type": "string", "description": "Glob pattern for files to include (e.g., '*.py', '*.txt'). Searches all files if omitted. Optional."}}, "required": ["pattern"] }))
             except Exception as e: logging.error(f"Failed to define 'grep' tool: {e}")

        # --- Define the glob tool ---
        if "glob" in AVAILABLE_TOOLS:
             try: tool_declarations.append(FunctionDeclaration(name="glob",description="Find files matching specific glob patterns recursively.",parameters={ "type": "object", "properties": {"pattern": {"type": "string", "description": "Glob pattern to match (e.g., '**/*.py', 'docs/**/*.md')."}, "path": {"type": "string", "description": "Base directory path to search within (default: '.'). Optional."}}, "required": ["pattern"] }))
             except Exception as e: logging.error(f"Failed to define 'glob' tool: {e}")

        # --- Define the bash tool ---
        if "bash" in AVAILABLE_TOOLS:
             try: tool_declarations.append(FunctionDeclaration(name="bash",description="Execute a shell command using the system's default shell.",parameters={ "type": "object", "properties": {"command": {"type": "string", "description": "The shell command string to execute."}, "timeout": {"type": "integer", "description": "Maximum execution time in seconds (optional)."} }, "required": ["command"] }))
             except Exception as e: logging.error(f"Failed to define 'bash' tool: {e}")

        # --- Define the web tool (if enabled in __init__) ---
        # if "web" in AVAILABLE_TOOLS:
        #      try: tool_declarations.append(FunctionDeclaration(name="web", ... )) etc ...

        # --- Define the test_runner tool (if enabled in __init__) ---
        if "test_runner" in AVAILABLE_TOOLS:
            try:
                test_runner_declaration = FunctionDeclaration(
                    name="test_runner",
                    description="Runs automated tests using the project's test runner (e.g., pytest).",
                    parameters={ "type": "object", "properties": {
                            "test_path": {"type": "string", "description": "Specific file or directory path to test (optional, runs discovered tests if omitted)."},
                            "options": {"type": "string", "description": "Additional command-line options for the test runner (e.g., '-k my_test', '-v', '--cov'). Optional."},
                            "runner_command": {"type": "string", "description": "The command for the test runner (default: 'pytest'). Optional."}
                        }} # No required fields, defaults handled by tool
                )
                tool_declarations.append(test_runner_declaration)
            except Exception as e: logging.error(f"Failed to define 'test_runner' tool: {e}")

        # --- Define the linter_checker tool (if enabled in __init__) ---
        # if "linter_checker" in AVAILABLE_TOOLS:
        #      try: tool_declarations.append(FunctionDeclaration(name="linter_checker", ... )) etc ...


        # Wrap all successful declarations in a single Tool object
        if tool_declarations:
             gemini_tools = [Tool(function_declarations=tool_declarations)]
             logging.info(f"Created Tool object with {len(tool_declarations)} function declarations.")
             return gemini_tools
        else:
             logging.warning("No tool declarations were successfully created.")
             return [] # Return empty list if no tools defined