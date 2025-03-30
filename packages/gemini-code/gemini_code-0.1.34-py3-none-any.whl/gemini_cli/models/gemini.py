"""
Gemini model integration for the CLI tool.
"""

import google.generativeai as genai
# Import the necessary types for function calling (REMOVED Part)
from google.generativeai.types import FunctionDeclaration, Tool
import re
import json
import logging
from ..utils import count_tokens
# Assuming get_tool correctly retrieves your tool *instance* based on name
# And AVAILABLE_TOOLS maps names to tool *classes* (needed for system prompt)
from ..tools import get_tool, AVAILABLE_TOOLS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def list_available_models(api_key):
    """List all available models from Google's Generative AI API."""
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        gemini_models = []
        for model in models:
            # Filter for models supporting generateContent to be safe
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
    """Interface for Gemini models."""

    def __init__(self, api_key, model_name="gemini-pro"): # Defaulting to gemini-pro as a stable base
        """Initialize the Gemini model interface."""
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)

        # Generation Config (can be adjusted later)
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.95,
            top_k=40,
        )

        # Safety Settings (adjust as needed)
        self.safety_settings = {
            "HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
            "HATE": "BLOCK_MEDIUM_AND_ABOVE",
            "SEXUAL": "BLOCK_MEDIUM_AND_ABOVE",
            "DANGEROUS": "BLOCK_MEDIUM_AND_ABOVE",
        }

        # System Instruction
        self.system_instruction = self._create_system_prompt_with_tools()

        # Create Tool definitions using the correct API types
        # self.tools will be list[Tool]
        self.tools = self._create_tool_definitions()

        try:
            logging.info(f"Creating model: {model_name} with tools and system instruction.")
            # Initialize the model ONCE with tools, safety, config, and system instruction
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                tools=self.tools,
                system_instruction=self.system_instruction
            )

            # Test the model with a simple generation (optional, but good for validation)
            logging.info("Testing model with simple generation...")
            # Use a try-except block for the test as it might fail for various reasons
            try:
                test_response = self.model.generate_content("Hello")
                # Accessing response parts safely
                text_content = "".join(part.text for part in test_response.candidates[0].content.parts if hasattr(part, 'text'))
                logging.info(f"Test successful, response length: {len(text_content)}")
            except Exception as test_error:
                 logging.warning(f"Initial model test failed (might be okay): {test_error}")
                 # Decide if you want to raise an error or just warn here

            # Start a chat session (important for conversation history)
            self.chat = self.model.start_chat(history=[])
            logging.info("Model initialized and chat session started.")

        except Exception as e:
            logging.error(f"Fatal error initializing Gemini model: {str(e)}", exc_info=True)
            # Consider falling back or re-raising depending on desired behavior
            # Fallback example (without tools/system prompt):
            # try:
            #     logging.warning(f"Falling back to basic 'gemini-pro' due to error: {e}")
            #     self.model_name = "gemini-pro"
            #     self.model = genai.GenerativeModel(self.model_name)
            #     self.chat = self.model.start_chat(history=[])
            #     logging.info("Fallback model initialized.")
            # except Exception as fallback_error:
            #     logging.error(f"Fallback model creation failed: {fallback_error}", exc_info=True)
            raise Exception(f"Could not initialize Gemini model: {e}") from e


    def get_available_models(self):
        """Get a list of available Gemini models."""
        return list_available_models(self.api_key)

    def generate(self, prompt, conversation=None):
        """
        Generate a response using the chat session, handling function calls.
        Note: The 'conversation' argument is less relevant now as history is managed by self.chat.
        """
        logging.info(f"Received prompt: {prompt[:100]}...") # Log truncated prompt

        # Basic command handling (can be expanded)
        if prompt.startswith('/'):
            command = prompt.split()[0].lower()
            if command in ['/exit', '/help', '/compact']:
                logging.info(f"Handled command: {command}")
                return None # Let main loop handle these

        try:
            # Send the user message to the chat session
            logging.info("Sending message to Gemini model...")
            # IMPORTANT: Use self.chat.send_message for conversation flow
            response = self.chat.send_message(prompt)
            logging.info("Received response from Gemini model.")

            # --- Standard Gemini Function Calling Flow ---
            # 1. Check if the response contains a function call
            function_call = self._extract_function_call_from_response(response)

            if function_call:
                logging.info(f"Detected function call: {function_call.name}")
                # 2. Execute the function
                try:
                    api_response = self._execute_function_call(function_call)
                    logging.info(f"Function '{function_call.name}' executed successfully.")

                    # --- MODIFIED SECTION ---
                    # 3. Send the function response back to the model
                    logging.info("Sending function response back to the model...")
                    # Construct the function response part manually as a list of dicts
                    # The chat session should understand this structure.
                    function_response_content = [
                        {"function_response": {
                            "name": function_call.name,
                            "response": api_response # api_response should be {"result": ...}
                           }
                        }
                    ]
                    response = self.chat.send_message(function_response_content)
                    # --- END MODIFIED SECTION ---

                    logging.info("Received final response after function execution.")
                    # The model will now generate a text response based on the function result

                except Exception as func_exec_error:
                    logging.error(f"Error executing function {function_call.name}: {func_exec_error}", exc_info=True)
                    # Optionally: Send an error message back to the model
                    # function_error_content = [
                    #     {"function_response": {
                    #         "name": function_call.name,
                    #         "response": {"error": str(func_exec_error)} # Ensure error is serializable
                    #        }
                    #     }
                    # ]
                    # response = self.chat.send_message(function_error_content)

                    # Or just return an error message directly to the user
                    return f"Error executing tool '{function_call.name}': {func_exec_error}"

            # 4. Extract and return the final text response
            final_text = self._extract_text_from_response(response)
            logging.info(f"Final response text length: {len(final_text)}")

             # Remove specific blocks if your system prompt still includes them (better handled by model)
            thinking_pattern = r"<thinking>.*?</thinking>"
            final_text = re.sub(thinking_pattern, "", final_text, flags=re.DOTALL)
            plan_pattern = r"<plan>.*?</plan>"
            final_text = re.sub(plan_pattern, "", final_text, flags=re.DOTALL)

            return final_text.strip()

        except Exception as e:
            logging.error(f"Error during generation or function call processing: {str(e)}", exc_info=True)
            # Provide specific error feedback if possible
            if "API key not valid" in str(e):
                 return "Error: Invalid Google API Key. Please check your configuration."
            # Add more specific error checks as needed
            return f"An unexpected error occurred: {str(e)}"

    def _extract_function_call_from_response(self, response):
        """Extracts the first FunctionCall object from the model's response."""
        try:
            # Safely navigate the response structure
            if (response.candidates and
                response.candidates[0].content and
                response.candidates[0].content.parts and
                response.candidates[0].content.parts[0].function_call):
                return response.candidates[0].content.parts[0].function_call
        except (IndexError, AttributeError, KeyError) as e:
            logging.debug(f"No function call found in response structure: {e}")
            # It's normal not to have a function call, so don't log as error
        return None

    def _execute_function_call(self, function_call):
        """Executes the requested function call using the mapped tool."""
        function_name = function_call.name
        # Ensure args is always a dictionary, even if function_call.args is None or empty
        args = dict(function_call.args) if hasattr(function_call, 'args') and function_call.args else {}


        logging.info(f"Executing function '{function_name}' with args: {args}")

        try:
            # Get the *instance* of the tool class
            # Assumes get_tool(name) returns an object with an execute(**args) method
            tool_instance = get_tool(function_name)
            if not tool_instance:
                raise ValueError(f"Tool '{function_name}' not found.")

            # Call the tool's execute method
            result = tool_instance.execute(**args) # Pass args using **kwargs

            # The API expects the response part to be JSON serializable.
            # Wrap result in a dict with a "result" key for the API.
            # Ensure the actual result is serializable (convert complex objects if needed).
            try:
                 # Attempt to serialize result to ensure it's valid JSON later
                 json.dumps(result)
                 # Now wrap it
                 return {"result": result}
            except TypeError as json_error:
                 logging.warning(f"Result for function {function_name} is not JSON serializable, converting to string: {json_error}")
                 return {"result": str(result)}


        except Exception as e:
            logging.error(f"Exception during function execution '{function_name}': {e}", exc_info=True)
            # Re-raise to be caught in the main generate loop
            raise

    def _extract_text_from_response(self, response):
        """Extracts the concatenated text parts from a model response."""
        try:
            # Check candidates and parts safely
            if (response.candidates and
                response.candidates[0].content and
                response.candidates[0].content.parts):
                 return "".join(part.text for part in response.candidates[0].content.parts if hasattr(part, 'text'))
            elif hasattr(response, 'text'): # Simpler direct text response (less common with function calling)
                 return response.text
            else:
                 logging.warning("Could not extract text from response structure.")
                 return "" # Return empty string if no text found
        except Exception as e:
            logging.error(f"Error extracting text from response: {e}", exc_info=True)
            return f"Error extracting response text: {e}" # Return error message


    def _create_system_prompt_with_tools(self):
        """Create a system prompt that includes tool descriptions.
           (This is now passed via system_instruction parameter)"""
        # Use AVAILABLE_TOOLS which should map names to classes
        tools_description = []
        if AVAILABLE_TOOLS: # Check if the import worked and is not empty
            for name, tool_class in AVAILABLE_TOOLS.items():
                try:
                    # Instantiate temporarily to get description (if needed)
                    # Alternatively, store description as a class variable
                    tool_instance = tool_class()
                    desc = getattr(tool_instance, 'description', 'No description available.')
                    tools_description.append(f"- Function: {name}\n  Description: {desc}")
                except Exception as e:
                     logging.warning(f"Could not get description for tool '{name}': {e}")
                     tools_description.append(f"- Function: {name}\n  Description: Error loading description.")
        else:
             logging.warning("AVAILABLE_TOOLS dictionary not found or empty. Cannot include tool descriptions in system prompt.")


        # Construct the system prompt (keep it concise and focused)
        system_prompt = f"""You are an expert AI pair programmer. Your goal is to help users write, debug, and manage code by directly interacting with the file system and executing commands when necessary and appropriate, using the available functions.

## Core Directives:
1.  **Analyze:** Understand the user's request.
2.  **Plan:** If complex, briefly outline the steps (mentally or explicitly if asked).
3.  **Execute:** Use the provided functions *directly* to fulfill the request (e.g., use 'edit' to write code to a file, don't just display it). Only show the code in your response if the user explicitly asks to *see* it without modification, or if a function call fails.
4.  **Verify:** Briefly confirm the outcome of function calls or explain any errors.
5.  **Respond:** Provide concise explanations and results. Avoid verbose narratives unless requested.

## Function Usage:
- You MUST call functions to perform actions like creating/editing files (`edit`), listing files (`ls`), searching (`grep`), running commands (`bash`), etc., when the user's request implies such an action.
- Do not just *describe* what a function would do. Call it.
- Inform the user after a function has been executed (e.g., "I have created the file `example.py`.")

## Available Functions:
{chr(10).join(tools_description) if tools_description else "No functions available."}

Think step-by-step. Fulfill the user's request by taking direct action using your tools.
"""
        return system_prompt


    # --- THIS METHOD NOW RETURNS list[Tool] ---
    def _create_tool_definitions(self) -> list[Tool]:
        """Create genai.Tool definitions for all available tools."""
        tool_declarations = [] # To hold FunctionDeclaration objects

        # --- Define the view tool ---
        try: # Add try/except around each tool definition for robustness
            view_declaration = FunctionDeclaration(
                name="view",
                description="View the contents of a file",
                parameters={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to view"
                        },
                        "offset": {
                            "type": "integer",
                            "description": "Line number to start reading from (optional)"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of lines to read (optional)"
                        }
                    },
                    "required": ["file_path"]
                }
            )
            tool_declarations.append(view_declaration)
        except Exception as e:
            logging.error(f"Failed to define 'view' tool: {e}")


        # --- Define the edit tool ---
        try:
            edit_declaration = FunctionDeclaration(
                name="edit",
                description="Edit a file by replacing text or create a new file with content",
                parameters={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to edit or create"
                        },
                        "old_string": {
                            "type": "string",
                            "description": "Text to replace (use null or omit if creating new file or overwriting). If replacing, this exact string must exist."
                        },
                        "new_string": {
                            "type": "string",
                            "description": "Text to replace with, or the full content for a new file. Use empty string to delete matched old_string."
                        }
                    },
                    # Ensure required fields match tool logic. new_string is needed unless deleting.
                    "required": ["file_path", "new_string"]
                }
            )
            tool_declarations.append(edit_declaration)
        except Exception as e:
            logging.error(f"Failed to define 'edit' tool: {e}")

        # --- Define the ls tool ---
        try:
            ls_declaration = FunctionDeclaration(
                name="ls",
                description="List files and directories in a given path",
                parameters={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Directory path to list (default: current directory '.')"
                        },
                        "ignore": {
                            "type": "string",
                            "description": "Comma-separated glob patterns to ignore (e.g., '*.pyc,__pycache__')"
                        }
                    },
                    # 'path' is often optional with a default, adjust if your tool requires it
                }
            )
            tool_declarations.append(ls_declaration)
        except Exception as e:
            logging.error(f"Failed to define 'ls' tool: {e}")

        # --- Define the grep tool ---
        try:
            grep_declaration = FunctionDeclaration(
                name="grep",
                description="Search for patterns (regex) in files within a directory",
                parameters={
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Regular expression pattern to search for"
                        },
                        "path": {
                            "type": "string",
                            "description": "Directory path to search within (default: '.')"
                        },
                        "include": {
                            "type": "string",
                            "description": "Glob pattern for files to include (e.g., '*.py', '*.txt'). Searches all files if omitted."
                        }
                    },
                    "required": ["pattern"]
                }
            )
            tool_declarations.append(grep_declaration)
        except Exception as e:
            logging.error(f"Failed to define 'grep' tool: {e}")

        # --- Define the glob tool ---
        try:
            glob_declaration = FunctionDeclaration(
                name="glob",
                description="Find files matching specific glob patterns recursively",
                parameters={
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Glob pattern to match (e.g., '**/*.py', 'docs/**/*.md')"
                        },
                        "path": {
                            "type": "string",
                            "description": "Base directory path to search within (default: '.')"
                        }
                    },
                    "required": ["pattern"]
                }
            )
            tool_declarations.append(glob_declaration)
        except Exception as e:
            logging.error(f"Failed to define 'glob' tool: {e}")

        # --- Define the bash tool ---
        try:
            bash_declaration = FunctionDeclaration(
                name="bash",
                description="Execute a shell command using the system's default shell",
                parameters={
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The shell command string to execute"
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Maximum execution time in seconds (optional)"
                        }
                    },
                    "required": ["command"]
                }
            )
            tool_declarations.append(bash_declaration)
        except Exception as e:
            logging.error(f"Failed to define 'bash' tool: {e}")

        # --- Define the web tool ---
        try:
            web_declaration = FunctionDeclaration(
                name="web",
                description="Fetch content from a web URL",
                parameters={
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "The URL to fetch content from (must include http:// or https://)"
                        },
                        "prompt": {
                            "type": "string",
                            "description": "Instruction for processing the web content (e.g., 'summarize', 'extract main points', optional)"
                        }
                    },
                    "required": ["url"]
                }
            )
            tool_declarations.append(web_declaration)
        except Exception as e:
            logging.error(f"Failed to define 'web' tool: {e}")

        # IMPORTANT: Wrap the FunctionDeclarations in a Tool object.
        # If tool_declarations is empty, pass None or an empty list to GenerativeModel.
        if tool_declarations:
             gemini_tools = [Tool(function_declarations=tool_declarations)]
             logging.info(f"Successfully created Tool object with {len(tool_declarations)} function declarations.")
             return gemini_tools
        else:
             logging.warning("No tool declarations were successfully created.")
             return [] # Return empty list if no tools could be defined