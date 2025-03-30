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
    
    def __init__(self, api_key, model_name="models/gemini-2.5-pro-exp-03-25"):
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
            
            # Process the response to check for tool usage
            response_text = response.text
            processed_response = self._process_response_for_tools(response_text)
            
            return processed_response
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _create_system_prompt_with_tools(self):
        """Create a system prompt that includes tool descriptions."""
        tools_description = []
        
        for name, tool_class in AVAILABLE_TOOLS.items():
            tool = tool_class()
            tools_description.append(f"- Tool: {name}\n  Description: {tool.description}")
        
        system_prompt = f"""You are an expert software engineer and AI coding assistant powered by Gemini 2.5 Pro with access to various tools in this CLI environment. Your goal is to help users of all skill levels write production-quality code and accomplish their programming tasks effectively by ACTIVELY USING TOOLS to create, modify, and run code.

ESSENTIAL WORKFLOW - ALWAYS FOLLOW THIS APPROACH:
1. <thinking>
   - First, carefully analyze what the user is trying to accomplish
   - Break down complex requests into actionable steps
   - Consider edge cases and potential obstacles
   - Plan how to use tools to implement the solution
   - DO NOT display this thinking to the user
</thinking>

2. <implementation>
   - Use appropriate tools to ACTUALLY IMPLEMENT solutions, rather than just describing them
   - Create real files, modify existing code, and execute commands when needed
   - Verify your work by checking the results of your tool operations
   - Use 'edit' and 'bash' tools actively rather than just showing code in the terminal
</implementation>

EXPERT TOOL USAGE - TAKE ACTION RATHER THAN JUST DESCRIBING:
- IMPORTANT: When users ask for code to be created, USE THE EDIT TOOL to actually create files
- CRUCIAL: Do not just print code in the terminal - use appropriate tools to implement solutions
- ALWAYS use tools to verify your work (check if files exist, test your code, etc.)
- Chain multiple tools together to accomplish complex tasks

TOOL USAGE PHILOSOPHY:
- You are a CODING PARTNER, not just an advisor. Take concrete actions with tools.
- Assume the user wants you to make actual changes when they ask for implementation
- For significant changes, first explain your plan, then execute it with tools
- When exploring codebases, use a structured approach (ls→glob→grep→view→edit)

Available tools:
{chr(10).join(tools_description)}

WHEN TO USE SPECIFIC TOOLS:
- 'edit': CREATE or MODIFY actual files - use this when users ask for code to be written
- 'view': Examine existing code, understand implementations, check configurations
- 'ls': Explore directory structure, find files, understand project organization
- 'grep': Search for patterns, locate function definitions, find usages of variables/classes
- 'glob': Find files by pattern (e.g., all Python files, all test files, all config files)
- 'bash': Run commands, install dependencies, execute tests, build projects
- 'web': Retrieve documentation, check APIs, find examples, research solutions

CODE QUALITY PRINCIPLES:
- Write DRY (Don't Repeat Yourself) code
- Follow language-specific conventions and style guides
- Include appropriate error handling
- Write defensive code that validates inputs
- Add meaningful comments explaining "why" not just "what"
- Ensure proper indentation and consistent formatting
- Use descriptive variable and function names
- Break complex operations into readable functions
- Write testable code with single responsibilities

RECOMMENDED RESPONSE FORMAT:
1. <thinking>
   [Your analysis of the problem and plan for implementation - NOT displayed to user]
</thinking>

2. Brief explanation of what you understand the user wants to do
3. Outline of your approach (1-3 bullet points or sentences)
4. Concrete implementation using tools - ACTUALLY CREATE/MODIFY FILES
5. Verification of your implementation 
6. Brief explanation of what you did (if needed)

EXAMPLE INTERACTIONS:
User: "Create a simple Flask app that shows 'Hello World'"
Assistant: <thinking>
The user wants a simple Flask web app. I'll need to:
1. Check if Flask is installed
2. Create an app.py file with a basic Flask application
3. Show the user how to run it
</thinking>

I'll create a simple Flask web app for you that displays "Hello World".

First, let's check if Flask is installed:
```tool
bash: python -c "try: import flask; print(f'Flask is installed'); except ImportError: print('Flask is not installed')"
```

Now I'll create a basic Flask application file:
```tool
edit: app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
```

Let's verify the file was created:
```tool
view: app.py
```

You can run the app with this command:
```tool
bash: python app.py
```

Your Flask app is ready! It will be available at http://127.0.0.1:5000/ when you run it.

```python
# I would recommend creating a function like read_json_file that:
# 1. Takes a file path as input
# 2. Opens the file with proper UTF-8 encoding
# 3. Uses json.load to parse the content
# 4. Has appropriate error handling for:
#    - FileNotFoundError
#    - JSONDecodeError 
#    - Other unexpected exceptions
# 5. Returns the parsed JSON data or None on failure
# 6. Uses logging to record errors
```

This implementation includes proper error handling for common issues and uses the context manager pattern for file handling. The encoding parameter ensures consistent UTF-8 handling across different platforms.

Would you like me to explain any specific part in more detail or adapt this for a particular use case?"

To use a tool, include it in your response using the following format:
```tool
tool_name: arguments
```

Remember to balance depth of explanations with brevity based on the user's skill level. Always aim for production-quality code that demonstrates best practices.
"""
        return system_prompt
    
    def _process_response_for_tools(self, response_text):
        """Process the response to execute any tools the model wants to use."""
        # First, remove any <thinking> blocks as they're not meant for the user
        thinking_pattern = r"<thinking>.*?</thinking>"
        processed_response = re.sub(thinking_pattern, "", response_text, flags=re.DOTALL)
        
        # Regular expression to find tool usage blocks (handle multiple formats)
        tool_patterns = [
            r"```tool\n(.*?)\n```",  # Format: ```tool\ntool_name: args\n```
            r"Tool: (.*?)\nArgs: (.*?)(?:\nResult:|$)",  # Format: Tool: tool_name\nArgs: args
            r"Tool: ([a-zA-Z0-9_]+) Args: (.*?)(?:\nResult:|$)",  # Format: Tool: tool_name Args: args
            r"Tool: ([a-zA-Z0-9_]+)(?:\s+Args:)?\s+(.*?)(?:\nResult:|$)"  # Very flexible pattern
        ]
        
        # Additional patterns that don't follow standard formats but are commonly generated by Gemini
        custom_edit_patterns = [
            # Pattern for "edit filename with content" in free text
            r'edit\s+([a-zA-Z0-9_./-]+)(?:\s+with)?\s+content[:\s]+(.*?)(?:\n\n|\Z)',
            # Pattern for just edit filename
            r'edit\s+([a-zA-Z0-9_./-]+)\s+'
        ]
        
        # Process standard tool patterns
        for pattern_idx, pattern in enumerate(tool_patterns):
            tool_matches = re.findall(pattern, processed_response, re.DOTALL)
            
            if not tool_matches:
                continue
                
            # Process based on pattern type
            if pattern_idx == 0:  # ```tool\ntool_name: args\n```
                for tool_text in tool_matches:
                    try:
                        # Parse the tool name and arguments
                        tool_parts = tool_text.split(':', 1)
                        if len(tool_parts) != 2:
                            replacement = f"Error: Invalid tool format: {tool_text}"
                        else:
                            tool_name = tool_parts[0].strip()
                            tool_args = tool_parts[1].strip()
                            
                            # Execute the tool
                            tool = get_tool(tool_name)
                            result = tool(tool_args)
                            
                            # Format the tool result
                            replacement = f"Tool: {tool_name}\nArgs: {tool_args}\nResult:\n\n{result}\n"
                    
                    except Exception as e:
                        replacement = f"Error executing tool '{tool_text}': {str(e)}"
                    
                    # Replace this specific tool block with its result
                    pattern_to_replace = f"```tool\n{re.escape(tool_text)}\n```"
                    processed_response = re.sub(pattern_to_replace, replacement, processed_response, flags=re.DOTALL)
            
            elif pattern_idx in [1, 2, 3]:  # Tool: name\nArgs: args or variants
                # Handle tuples differently based on the pattern
                for match in tool_matches:
                    try:
                        if isinstance(match, tuple):
                            if len(match) == 2:
                                tool_name, tool_args = match
                            else:
                                continue
                        else:
                            # This shouldn't happen with the patterns we're using
                            continue
                        
                        # Skip if already processed (has Result:)
                        if pattern_idx == 1:
                            pattern_check = f"Tool: {re.escape(tool_name)}\nArgs: {re.escape(tool_args)}\nResult:"
                        elif pattern_idx == 2:
                            pattern_check = f"Tool: {re.escape(tool_name)} Args: {re.escape(tool_args)}\nResult:"
                        else:
                            pattern_check = f"Tool: {re.escape(tool_name)} {re.escape(tool_args)}\nResult:"
                            
                        if pattern_check in processed_response:
                            continue
                        
                        tool_name = tool_name.strip()
                        tool_args = tool_args.strip()
                        
                        # Execute the tool
                        tool = get_tool(tool_name)
                        result = tool(tool_args)
                        
                        # Format the replacement (keep the original tool invocation and add result)
                        if pattern_idx == 1:
                            pattern_to_replace = f"Tool: {re.escape(tool_name)}\nArgs: {re.escape(tool_args)}"
                            replacement = f"Tool: {tool_name}\nArgs: {tool_args}\nResult:\n\n{result}\n"
                        elif pattern_idx == 2:
                            pattern_to_replace = f"Tool: {re.escape(tool_name)} Args: {re.escape(tool_args)}"
                            replacement = f"Tool: {tool_name} Args: {tool_args}\nResult:\n\n{result}\n"
                        else:
                            pattern_to_replace = f"Tool: {re.escape(tool_name)} {re.escape(tool_args)}"
                            replacement = f"Tool: {tool_name} {tool_args}\nResult:\n\n{result}\n"
                        
                        # Replace this specific tool invocation with result
                        processed_response = re.sub(pattern_to_replace, replacement, processed_response, count=1)
                    
                    except Exception as e:
                        # Create appropriate replacement based on pattern
                        if pattern_idx == 1:
                            pattern_to_replace = f"Tool: {re.escape(tool_name)}\nArgs: {re.escape(tool_args)}"
                            replacement = f"Tool: {tool_name}\nArgs: {tool_args}\nError: {str(e)}"
                        elif pattern_idx == 2:
                            pattern_to_replace = f"Tool: {re.escape(tool_name)} Args: {re.escape(tool_args)}"
                            replacement = f"Tool: {tool_name} Args: {tool_args}\nError: {str(e)}"
                        else:
                            pattern_to_replace = f"Tool: {re.escape(tool_name)} {re.escape(tool_args)}"
                            replacement = f"Tool: {tool_name} {tool_args}\nError: {str(e)}"
                            
                        processed_response = re.sub(pattern_to_replace, replacement, processed_response, count=1)
        
        # Now process custom edit patterns
        for pattern in custom_edit_patterns:
            matches = re.findall(pattern, processed_response, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                try:
                    if isinstance(match, tuple) and len(match) == 2:
                        file_path, content = match
                        file_path = file_path.strip()
                        content = content.strip()
                        
                        # Skip if already processed
                        if f"Successfully created {file_path}" in processed_response:
                            continue
                            
                        # Execute edit tool
                        tool = get_tool("edit")
                        result = tool.execute(file_path=file_path, new_string=content)
                        
                        # Create replacement text
                        original_text = f"edit {file_path} with content: {content}"
                        replacement = f"Tool: edit\nArgs: {file_path}\nResult:\n\n{result}\n"
                        
                        # Replace in response
                        processed_response = processed_response.replace(original_text, replacement)
                    
                    elif isinstance(match, str):
                        file_path = match.strip()
                        
                        # Skip if already processed
                        if f"Successfully created {file_path}" in processed_response:
                            continue
                            
                        # Execute edit tool to create empty file
                        tool = get_tool("edit")
                        result = tool.execute(file_path=file_path)
                        
                        # Create replacement text
                        original_text = f"edit {file_path}"
                        replacement = f"Tool: edit\nArgs: {file_path}\nResult:\n\n{result}\n"
                        
                        # Replace in response
                        processed_response = processed_response.replace(original_text, replacement)
                        
                except Exception as e:
                    # Just log the error but don't modify text for these custom patterns
                    print(f"Error processing custom edit pattern: {str(e)}")
        
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