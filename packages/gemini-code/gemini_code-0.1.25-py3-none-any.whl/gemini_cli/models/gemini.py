"""
Gemini model integration for the CLI tool.
"""

import google.generativeai as genai
import re
import json
import logging
from ..utils import count_tokens
from ..tools import get_tool, AVAILABLE_TOOLS

def list_available_models(api_key):
    """List all available models from Google's Generative AI API."""
    try:
        # Configure the API with the provided key
        genai.configure(api_key=api_key)
        
        # Get all available models
        models = genai.list_models()
        
        # Filter for Gemini models and format the response
        gemini_models = []
        for model in models:
            if "gemini" in model.name.lower():
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
    
    def __init__(self, api_key, model_name="gemini-2.5-pro"):
        """Initialize the Gemini model interface."""
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=api_key)
        
        # Configure model with function calling capability
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
        }
        
        try:
            # Create the model with safety settings but without tools first
            self.model = genai.GenerativeModel(
                model_name,
                generation_config=self.generation_config
            )
            
            # Only add tools if the initial model creation succeeds
            # Get tool definitions
            self.tool_definitions = self._create_tool_definitions()
            
            # Recreate the model with tool definitions if needed
            if self.tool_definitions:
                self.model = genai.GenerativeModel(
                    model_name,
                    generation_config=self.generation_config,
                    tools=self.tool_definitions
                )
                
        except Exception as e:
            import logging
            logging.error(f"Error creating model: {str(e)}")
            # Create a basic model without tools as fallback
            self.model = genai.GenerativeModel(
                model_name,
                generation_config=self.generation_config
            )
        
    def get_available_models(self):
        """Get a list of available Gemini models."""
        return list_available_models(self.api_key)
    
    def generate(self, prompt, conversation=None):
        """Generate a response to the prompt."""
        if not conversation:
            conversation = []
            
        # Special case for built-in commands
        if prompt.startswith('/'):
            command = prompt.split()[0].lower()
            if command in ['/exit', '/help', '/compact']:
                # These are handled by the main CLI loop
                return None
        
        # Convert our conversation format to Gemini format
        gemini_messages = self._format_conversation_for_gemini(conversation)
        
        # Add system prompt with tool information
        system_prompt = self._create_system_prompt_with_tools()
        gemini_messages.insert(0, {"role": "model", "parts": [system_prompt]})
        
        try:
            # Create Gemini chat session
            chat = self.model.start_chat(history=gemini_messages)
            
            # Generate response
            response = chat.send_message(prompt)
            
            # Process response for function calls
            try:
                response_text = self._process_function_calls(response)
            except Exception as e:
                import logging
                logging.error(f"Error processing function calls: {str(e)}")
                # Fallback to basic text extraction
                response_text = str(response.text) if hasattr(response, "text") else str(response)
            
            return response_text
        
        except Exception as e:
            import logging
            logging.error(f"Error generating response: {str(e)}")
            return f"Error generating response: {str(e)}"
            
    def _process_function_calls(self, response):
        """Process any function calls from the response."""
        try:
            # First, try to get the text directly if it's a simple response
            if hasattr(response, "text"):
                response_text = response.text
            else:
                # If response has candidates structure
                if hasattr(response, "candidates") and response.candidates:
                    candidate = response.candidates[0]
                    
                    # Navigate the response structure to find content
                    if hasattr(candidate, "content") and candidate.content:
                        content = candidate.content
                        
                        # Extract the main text response from parts if available
                        if hasattr(content, "parts") and content.parts:
                            response_text = content.parts[0].text if hasattr(content.parts[0], "text") else str(content.parts[0])
                        else:
                            # If no parts, try to convert content to string
                            response_text = str(content)
                    else:
                        # If no content, try to get text from candidate
                        response_text = candidate.text if hasattr(candidate, "text") else str(candidate)
                else:
                    # Last resort: convert the entire response to string
                    response_text = str(response)
            
            # Initialize to track function calls
            function_responses = []
            functions_called = False
            
            # Check for function calls if we have a structured response
            if hasattr(response, "candidates") and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, "content") and candidate.content:
                    content = candidate.content
                    
                    # Look for function calls in parts
                    if hasattr(content, "parts"):
                        for part in content.parts:
                            if hasattr(part, "function_call"):
                                functions_called = True
                                function_call = part.function_call
                                
                                try:
                                    # Get the tool and execute it
                                    tool = get_tool(function_call.name)
                                    
                                    # Parse arguments from function_call.args
                                    args = json.loads(function_call.args) if function_call.args else {}
                                    
                                    # Execute the tool
                                    result = tool(**args)
                                    
                                    # Format the function response
                                    function_response = (
                                        f"Function: {function_call.name}\n"
                                        f"Arguments: {json.dumps(args)}\n"
                                        f"Result:\n{result}\n"
                                    )
                                    
                                    function_responses.append(function_response)
                                    
                                except Exception as e:
                                    error_message = f"Error executing function {function_call.name}: {str(e)}"
                                    function_responses.append(error_message)
            
            # If no functions were called, just return the response text
            if not functions_called:
                return response_text
                
            # Combine the response text with function results
            if function_responses:
                combined_response = response_text + "\n\n" + "\n\n".join(function_responses)
                return combined_response
            
            return response_text
            
        except Exception as e:
            # If any error occurs in processing, log it and return a useful message
            logging.error(f"Error processing function calls: {str(e)}")
            return f"Error processing model response: {str(e)}"
    
    def _create_system_prompt_with_tools(self):
        """Create a system prompt that includes tool descriptions."""
        tools_description = []
        
        for name, tool_class in AVAILABLE_TOOLS.items():
            tool = tool_class()
            tools_description.append(f"- Function: {name}\n  Description: {tool.description}")
        
        system_prompt = f"""You are an expert software engineer and AI coding assistant powered by Gemini with access to various functions in this CLI environment. Your goal is to help users write production-quality code by ACTIVELY CALLING FUNCTIONS to create, modify, and run code.

## CRITICAL WORKFLOW - YOU MUST FOLLOW THIS APPROACH:

1. THINK: <thinking>
   - First, carefully analyze what the user is trying to accomplish
   - Break down complex requests into actionable steps  
   - Plan how you will use functions to implement the solution
   - Do not display this thinking to the user
</thinking>

2. PLAN: <plan>
   - Create a step-by-step plan of function calls needed
   - Design a verification strategy for each step
   - This is still your internal process, not displayed to user
</plan>

3. EXECUTE:
   - ACTUALLY CALL FUNCTIONS to make real changes (don't just talk about them)
   - Do not describe what functions would do - CALL THEM
   - Use 'edit' to create/modify files (not just show code in your response)
   - Use 'bash' to run commands (not just suggest commands)
   - DO NOT print lengthy code listings in your response

4. VERIFY:
   - After each function call, verify the result
   - If a function call fails, troubleshoot and try a different approach
   - Chain function calls together to accomplish complex tasks

## FUNCTION CALLING RULES:

- NEVER JUST PRINT CODE in your response when a user asks for implementation
- ALWAYS use the 'edit' function to actually create or update files
- ALWAYS use functions to verify your work actually succeeded
- Assume the user wants you to make actual changes when they ask for implementation
- Think of yourself as a hands-on developer who actively modifies files

## YOUR AVAILABLE FUNCTIONS:
{chr(10).join(tools_description)}

## WHEN TO USE SPECIFIC FUNCTIONS:
- 'edit': CREATE or MODIFY actual files - use this whenever users ask for code
- 'view': Examine existing code, understand implementations, check configurations
- 'ls': Explore directory structure, find files, understand project organization
- 'grep': Search for patterns, locate function definitions, find usages of variables/classes
- 'glob': Find files by pattern (e.g., all Python files, all test files, all config files)
- 'bash': Run commands, install dependencies, execute tests, build projects
- 'web': Retrieve documentation, check APIs, find examples, research solutions

## CODE QUALITY PRINCIPLES:
- Write DRY (Don't Repeat Yourself) code
- Follow language-specific conventions and style guides
- Include appropriate error handling
- Write defensive code that validates inputs
- Ensure proper indentation and consistent formatting
- Use descriptive variable and function names
- Break complex operations into readable functions
- Write testable code with single responsibilities

## RESPONSE FORMAT REQUIREMENTS:
1. <thinking>
   [Your analysis and plan - NOT displayed to user]
</thinking>

2. Brief explanation of what you understand the user wants (1-2 sentences)
3. CALL FUNCTIONS to implement the solution (use actual function calls, not explanations)
4. If needed, show a brief explanation of what you did after completion

CRITICAL: When a user asks you to create or modify code:
- DO NOT show the code in your response
- INSTEAD use the 'edit' function to actually create or modify the file
- Then use other functions to verify your changes worked

Remember: You are a coding partner who makes actual changes through function calls, not just talks about code.

IMPORTANT: When using function calling, I expect you to use Gemini's function calling format, where your calls will be recognized and executed. Focus on creating actual solutions, not just describing them."""
        return system_prompt
    
    def _create_tool_definitions(self):
        """Create function definitions for all available tools."""
        tool_definitions = []
        
        # Define the view tool
        view_tool = {
            "name": "view",
            "description": "View the contents of a file",
            "parameters": {
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
        }
        
        # Define the edit tool
        edit_tool = {
            "name": "edit",
            "description": "Edit a file by replacing text or create a new file with content",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to edit or create"
                    },
                    "old_string": {
                        "type": "string",
                        "description": "Text to replace (optional when creating new file)"
                    },
                    "new_string": {
                        "type": "string",
                        "description": "Text to replace it with or full content for new file"
                    }
                },
                "required": ["file_path"]
            }
        }
        
        # Define the ls tool
        ls_tool = {
            "name": "ls",
            "description": "List files in a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory path to list"
                    },
                    "ignore": {
                        "type": "string",
                        "description": "Glob patterns to ignore (comma-separated)"
                    }
                },
                "required": ["path"]
            }
        }
        
        # Define the grep tool
        grep_tool = {
            "name": "grep",
            "description": "Search for patterns in files",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Regex pattern to search for"
                    },
                    "path": {
                        "type": "string",
                        "description": "Directory to search in"
                    },
                    "include": {
                        "type": "string",
                        "description": "File patterns to include (e.g., \"*.py\")"
                    }
                },
                "required": ["pattern"]
            }
        }
        
        # Define the glob tool
        glob_tool = {
            "name": "glob",
            "description": "Find files using glob patterns",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Glob pattern to match"
                    },
                    "path": {
                        "type": "string",
                        "description": "Directory to search in"
                    }
                },
                "required": ["pattern"]
            }
        }
        
        # Define the bash tool
        bash_tool = {
            "name": "bash",
            "description": "Execute a bash command",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute"
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in milliseconds (optional)"
                    }
                },
                "required": ["command"]
            }
        }
        
        # Define the web tool
        web_tool = {
            "name": "web",
            "description": "Fetch content from a website",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Optional prompt to process the content"
                    }
                },
                "required": ["url"]
            }
        }
        
        # Add all tool definitions to the list
        tool_definitions.extend([
            view_tool,
            edit_tool,
            ls_tool,
            grep_tool,
            glob_tool,
            bash_tool,
            web_tool
        ])
        
        return tool_definitions
        
    def _process_response_for_tools(self, response_text):
        """
        Legacy method for processing tool usage in text.
        This is kept for backward compatibility but not used with function calling.
        """
        # First, remove any <thinking> blocks as they're not meant for the user
        thinking_pattern = r"<thinking>.*?</thinking>"
        processed_response = re.sub(thinking_pattern, "", response_text, flags=re.DOTALL)
        
        # Return the processed response without any tool processing
        return processed_response
    
    def _format_conversation_for_gemini(self, conversation):
        """Convert our conversation format to Gemini format."""
        gemini_messages = []
        
        for message in conversation:
            role = message["role"]
            content = message["content"]
            
            # Map our roles to Gemini roles (system becomes model)
            if role == "system":
                gemini_role = "model"
            else:
                gemini_role = role
                
            gemini_messages.append({"role": gemini_role, "parts": [content]})
        
        return gemini_messages