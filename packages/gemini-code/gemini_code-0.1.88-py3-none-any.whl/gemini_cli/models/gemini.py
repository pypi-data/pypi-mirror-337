"""
Gemini model integration for the CLI tool.
Using Native Function Calling, Planning Prompt, Persistent History.
Refactored agent loop based on native function calling API. Prompt v13.
"""

import google.generativeai as genai
from google.generativeai import protos
from google.generativeai.types import FunctionDeclaration, Tool
import logging
import time
from rich.console import Console

# Import exceptions for specific error handling if needed later
from google.api_core.exceptions import ResourceExhausted

from ..utils import count_tokens
from ..tools import get_tool, AVAILABLE_TOOLS
# Assuming SummarizeCodeTool might be used directly or indirectly later
# from ..tools.summarizer_tool import SummarizeCodeTool

# Setup logging (basic config, consider moving to main.py)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
log = logging.getLogger(__name__)

# REMOVED: TOOL_CALL_PATTERN, TASK_COMPLETE_PATTERN (no longer needed for parsing)
MAX_AGENT_ITERATIONS = 10
FALLBACK_MODEL = "gemini-1.5-pro-latest"
CONTEXT_TRUNCATION_THRESHOLD_TOKENS = 800000 # Example token limit

def list_available_models(api_key):
    # ... (Remains the same) ...
    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        gemini_models = []
        for model in models:
            # Filter for models supporting generateContent to avoid chat-only models if needed
            if 'generateContent' in model.supported_generation_methods:
                 model_info = { "name": model.name, "display_name": model.display_name, "description": model.description, "supported_generation_methods": model.supported_generation_methods }
                 gemini_models.append(model_info)
        return gemini_models
    except Exception as e:
        log.error(f"Error listing models: {str(e)}")
        return [{"error": str(e)}]


class GeminiModel:
    """Interface for Gemini models using native function calling agentic loop."""

    def __init__(self, api_key: str, console: Console, model_name: str ="gemini-2.5-pro-exp-03-25"):
        """Initialize the Gemini model interface."""
        self.api_key = api_key
        self.initial_model_name = model_name
        self.current_model_name = model_name
        self.console = console
        genai.configure(api_key=api_key)

        self.generation_config = genai.types.GenerationConfig(temperature=0.4, top_p=0.95, top_k=40)
        self.safety_settings = { "HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE", "HATE": "BLOCK_MEDIUM_AND_ABOVE", "SEXUAL": "BLOCK_MEDIUM_AND_ABOVE", "DANGEROUS": "BLOCK_MEDIUM_AND_ABOVE" }
        
        # --- Tool Definition ---
        self.function_declarations = self._create_tool_definitions()
        self.gemini_tools = Tool(function_declarations=self.function_declarations) if self.function_declarations else None
        # ---

        # --- System Prompt (v13 - Native Functions & Planning) ---
        self.system_instruction = self._create_system_prompt()
        # ---

        # --- Initialize Persistent History ---
        self.chat_history = [
            {'role': 'user', 'parts': [self.system_instruction]},
            {'role': 'model', 'parts': ["Okay, I'm ready. Provide the directory context and your request."]}
        ]
        log.info("Initialized persistent chat history.")
        # ---

        try:
            self._initialize_model_instance() # Creates self.model
            log.info("GeminiModel initialized successfully (Native Function Calling Agent Loop).")
        except Exception as e:
             log.error(f"Fatal error initializing Gemini model '{self.current_model_name}': {str(e)}", exc_info=True)
             raise Exception(f"Could not initialize Gemini model: {e}") from e

    def _initialize_model_instance(self):
        """Helper to create the GenerativeModel instance."""
        log.info(f"Initializing model instance: {self.current_model_name}")
        try:
            # Pass system instruction here, tools are passed during generate_content
            self.model = genai.GenerativeModel(
                model_name=self.current_model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                system_instruction=self.system_instruction
            )
            log.info(f"Model instance '{self.current_model_name}' created successfully.")
        except Exception as init_err:
            log.error(f"Failed to create model instance for '{self.current_model_name}': {init_err}", exc_info=True)
            raise init_err

    def get_available_models(self):
        return list_available_models(self.api_key)

    # --- Native Function Calling Agent Loop ---
    def generate(self, prompt: str) -> str | None:
        logging.info(f"Agent Loop - Processing prompt: '{prompt[:100]}...' using model '{self.current_model_name}'")
        original_user_prompt = prompt
        if prompt.startswith('/'):
             command = prompt.split()[0].lower()
             # Handle commands like /compact here eventually
             if command in ['/exit', '/help']:
                 logging.info(f"Handled command: {command}")
                 return None # Or return specific help text

        # === Step 1: Mandatory Orientation ===
        orientation_context = ""
        ls_result = None # Initialize to None
        try:
            logging.info("Performing mandatory orientation (ls).")
            ls_tool = get_tool("ls")
            if ls_tool:
                # Clear args just in case, assuming ls takes none for basic root listing
                ls_result = ls_tool.execute()
                # === START DEBUG LOGGING ===
                log.debug(f"LsTool raw result:\n---\n{ls_result}\n---")
                # === END DEBUG LOGGING ===
                log.info(f"Orientation ls result length: {len(ls_result) if ls_result else 0}") # Changed from logging full result
                self.console.print(f"[dim]Directory context acquired via 'ls'.[/dim]")
                orientation_context = f"Current directory contents (from initial `ls`):\n```\n{ls_result}\n```\n"
            else:
                log.error("CRITICAL: Could not find 'ls' tool for mandatory orientation.")
                # Stop execution if ls tool is missing - fundamental context is unavailable
                return "Error: The essential 'ls' tool is missing. Cannot proceed."

        except Exception as orient_error:
            log.error(f"Error during mandatory orientation (ls): {orient_error}", exc_info=True)
            error_message = f"Error during initial directory scan: {orient_error}"
            orientation_context = f"{error_message}\n"
            self.console.print(f"[bold red]Error getting initial directory listing: {orient_error}[/bold red]")
            # Stop execution if initial ls fails - context is unreliable
            return f"Error: Failed to get initial directory listing. Cannot reliably proceed. Details: {orient_error}"

        # === Step 2: Prepare Initial User Turn ===
        # Combine orientation with the actual user request
        turn_input_prompt = f"{orientation_context}\nUser request: {original_user_prompt}"
        
        # Add this combined input to the PERSISTENT history
        self.chat_history.append({'role': 'user', 'parts': [turn_input_prompt]})
        # === START DEBUG LOGGING ===
        log.debug(f"Prepared turn_input_prompt (sent to LLM):\n---\n{turn_input_prompt}\n---")
        # === END DEBUG LOGGING ===
        self._manage_context_window() # Truncate *before* sending the first request

        iteration_count = 0
        task_completed = False
        final_summary = None
        last_text_response = "No response generated." # Fallback text

        try:
            while iteration_count < MAX_AGENT_ITERATIONS:
                iteration_count += 1
                logging.info(f"Agent Loop Iteration {iteration_count}/{MAX_AGENT_ITERATIONS}")
                
                # === Call LLM with History and Tools ===
                llm_response = None
                try:
                    logging.info(f"Sending request to LLM ({self.current_model_name}). History length: {len(self.chat_history)} turns.")
                    # Pass the available tools to the generate_content call
                    llm_response = self.model.generate_content(
                        self.chat_history,
                        generation_config=self.generation_config,
                        tools=[self.gemini_tools] if self.gemini_tools else None
                    )
                    # === START DEBUG LOGGING ===
                    log.debug(f"RAW Gemini Response Object (Iter {iteration_count}): {llm_response}")
                    # === END DEBUG LOGGING ===
                    
                    # Extract the response part (candidate)
                    # Add checks for empty candidates or parts
                    if not llm_response.candidates:
                         log.error(f"LLM response had no candidates. Response: {llm_response}")
                         last_text_response = "(Agent received response with no candidates)"
                         task_completed = True; final_summary = last_text_response; break
                         
                    response_candidate = llm_response.candidates[0]
                    if not response_candidate.content or not response_candidate.content.parts:
                        log.error(f"LLM response candidate had no content or parts. Candidate: {response_candidate}")
                        last_text_response = "(Agent received response candidate with no content/parts)"
                        task_completed = True; final_summary = last_text_response; break

                    # --- REVISED LOOP LOGIC FOR MULTI-PART HANDLING ---
                    function_call_part_to_execute = None
                    text_response_buffer = ""
                    processed_function_call_in_turn = False # Flag to ensure only one function call is processed per turn

                    # Iterate through all parts in the response
                    for part in response_candidate.content.parts:
                        if hasattr(part, 'function_call') and part.function_call and not processed_function_call_in_turn:
                            function_call = part.function_call
                            tool_name = function_call.name
                            tool_args = dict(function_call.args) if function_call.args else {}
                            log.info(f"LLM requested Function Call: {tool_name} with args: {tool_args}")

                            # Add the function *call* part to history immediately
                            self.chat_history.append({'role': 'model', 'parts': [part]})
                            self._manage_context_window()
                            
                            # Store details for execution after processing all parts
                            function_call_part_to_execute = part 
                            processed_function_call_in_turn = True # Mark that we found and will process a function call
                            # Don't break here yet, process other parts (like text) first for history/logging

                        elif hasattr(part, 'text') and part.text:
                            llm_text = part.text
                            log.info(f"LLM returned text part (Iter {iteration_count}): {llm_text[:100]}...")
                            text_response_buffer += llm_text + "\n" # Append text parts
                            # Add the text response part to history
                            self.chat_history.append({'role': 'model', 'parts': [part]})
                            self._manage_context_window()
                            
                        else:
                            log.warning(f"LLM returned unexpected response part (Iter {iteration_count}): {part}")
                            # Add it to history anyway?
                            self.chat_history.append({'role': 'model', 'parts': [part]})
                            self._manage_context_window()

                    # --- Now, decide action based on processed parts ---
                    if function_call_part_to_execute:
                        # === Execute the Tool === (Using stored details)
                        function_call = function_call_part_to_execute.function_call # Get the stored call
                        tool_name = function_call.name
                        tool_args = dict(function_call.args) if function_call.args else {}
                        
                        tool_result = ""
                        tool_error = False
                        status_msg = f"Executing {tool_name}"
                        if tool_args: status_msg += f" ({', '.join([f'{k}={str(v)[:30]}...' if len(str(v))>30 else f'{k}={v}' for k,v in tool_args.items()])})"
                        
                        with self.console.status(f"[yellow]{status_msg}...", spinner="dots"):
                            try:
                                tool_instance = get_tool(tool_name)
                                if tool_instance:
                                    log.debug(f"Executing tool '{tool_name}' with arguments: {tool_args}")
                                    tool_result = tool_instance.execute(**tool_args)
                                    log.info(f"Tool '{tool_name}' executed. Result length: {len(str(tool_result)) if tool_result else 0}")
                                    log.debug(f"Tool '{tool_name}' result: {str(tool_result)[:500]}...")
                                else:
                                    log.error(f"Tool '{tool_name}' not found.")
                                    tool_result = f"Error: Tool '{tool_name}' is not available."
                                    tool_error = True
                            except Exception as tool_exec_error:
                                log.error(f"Error executing tool '{tool_name}' with args {tool_args}: {tool_exec_error}", exc_info=True)
                                tool_result = f"Error executing tool {tool_name}: {str(tool_exec_error)}"
                                tool_error = True
                        
                        if tool_error:
                            self.console.print(f"[red] -> Error executing {tool_name}: {str(tool_result)[:100]}...[/red]")
                        else:
                            self.console.print(f"[dim] -> Executed {tool_name}[/dim]")

                        # === Check for Task Completion Signal via Tool Call ===
                        if tool_name == "task_complete":
                            log.info("Task completion signaled by 'task_complete' function call.")
                            task_completed = True
                            final_summary = tool_result # The result of task_complete IS the summary
                            # We break *after* adding the function response below
                        
                        # === Add Function Response to History ===
                        # Create the FunctionResponse proto
                        function_response_proto = protos.FunctionResponse(
                            name=tool_name,
                            response={"result": tool_result} # API expects dict
                        )
                        # Wrap it in a Part proto
                        response_part_proto = protos.Part(function_response=function_response_proto)
                        
                        # Append to history
                        self.chat_history.append({'role': 'user', # Function response acts as a 'user' turn providing data
                                              'parts': [response_part_proto]})
                        self._manage_context_window()
                        
                        if task_completed: 
                            break # Exit loop NOW that task_complete result is in history
                        else:
                            continue # IMPORTANT: Continue loop to let LLM react to function result
                            
                    elif text_response_buffer: 
                        # === Only Text Returned ===
                        log.info("LLM returned only text response(s). Assuming task completion or explanation provided.")
                        last_text_response = text_response_buffer.strip()
                        task_completed = True # Treat text response as completion
                        final_summary = last_text_response # Use the text as the summary
                        break # Exit the loop
                    
                    else:
                        # === No actionable parts found ===
                        log.warning("LLM response contained no actionable parts (text or function call).")
                        last_text_response = "(Agent received response with no actionable parts)"
                        task_completed = True # Treat as completion to avoid loop errors
                        final_summary = last_text_response
                        break # Exit loop

                except ResourceExhausted as quota_error:
                    log.warning(f"Quota exceeded for model '{self.current_model_name}': {quota_error}")
                    # Implement model switching or error reporting as before
                    self.console.print(f"[bold red]API quota exceeded. Try again later.[/bold red]")
                    # Clean history before returning
                    if self.chat_history[-1]['role'] == 'user': self.chat_history.pop()
                    return f"Error: API quota exceeded."
                except Exception as generation_error:
                     log.error(f"Error during LLM generation: {generation_error}", exc_info=True)
                     # Clean history
                     if self.chat_history[-1]['role'] == 'user': self.chat_history.pop()
                     return f"Error during LLM generation step: {generation_error}"

            # === End Agent Loop ===

            # === Handle Final Output ===
            if task_completed and final_summary:
                 log.info("Agent loop finished. Returning final summary.")
                 # Cleanup internal tags if needed (using a hypothetical method)
                 # cleaned_summary = self._cleanup_internal_tags(final_summary) 
                 return final_summary.strip() # Return the summary from task_complete or final text
            elif iteration_count >= MAX_AGENT_ITERATIONS:
                 log.warning(f"Agent loop terminated after reaching max iterations ({MAX_AGENT_ITERATIONS}).")
                 # Try to get the last *text* response the model generated, even if it wanted to call a function after
                 last_model_response_text = self._find_last_model_text(self.chat_history)
                 timeout_message = f"(Task exceeded max iterations ({MAX_AGENT_ITERATIONS}). Last text from model was: {last_model_response_text})"
                 return timeout_message.strip()
            else:
                 # This case should be less likely now
                 log.error("Agent loop exited unexpectedly.")
                 last_model_response_text = self._find_last_model_text(self.chat_history)
                 return f"(Agent loop finished unexpectedly. Last model text: {last_model_response_text})"

        except Exception as e:
             log.error(f"Error during Agent Loop: {str(e)}", exc_info=True)
             return f"An unexpected error occurred during the agent process: {str(e)}"

    # --- Context Management (Consider Token Counting) ---
    def _manage_context_window(self):
        """Basic context window management based on turn count."""
        # Placeholder - Enhance with token counting
        MAX_HISTORY_TURNS = 20 # Keep ~N pairs of user/model turns + initial setup + tool calls/responses
        # Each full LLM round (request + function_call + function_response) adds 3 items
        if len(self.chat_history) > (MAX_HISTORY_TURNS * 3 + 2): 
             log.warning(f"Chat history length ({len(self.chat_history)}) exceeded threshold. Truncating.")
             # Keep system prompt (idx 0), initial model ack (idx 1)
             keep_count = MAX_HISTORY_TURNS * 3 # Keep N rounds
             keep_from_index = len(self.chat_history) - keep_count
             self.chat_history = self.chat_history[:2] + self.chat_history[keep_from_index:]
             log.info(f"History truncated to {len(self.chat_history)} items.")

    # --- Tool Definition Helper ---
    def _create_tool_definitions(self) -> list[FunctionDeclaration] | None:
        """Dynamically create FunctionDeclarations from AVAILABLE_TOOLS."""
        declarations = []
        for tool_name, tool_instance in AVAILABLE_TOOLS.items():
            if hasattr(tool_instance, 'get_function_declaration'):
                declaration = tool_instance.get_function_declaration()
                if declaration:
                    declarations.append(declaration)
                    log.debug(f"Generated FunctionDeclaration for tool: {tool_name}")
                else:
                    log.warning(f"Tool {tool_name} has 'get_function_declaration' but it returned None.")
            else:
                # Fallback or skip tools without the method? For now, log warning.
                log.warning(f"Tool {tool_name} does not have a 'get_function_declaration' method. Skipping.")
        
        log.info(f"Created {len(declarations)} function declarations for native tool use.")
        return declarations if declarations else None

    # --- System Prompt Helper ---
    def _create_system_prompt(self) -> str:
        """Creates the system prompt, emphasizing native functions and planning."""
        # Use docstrings from tools if possible for descriptions
        tool_descriptions = []
        if self.function_declarations:
            for func_decl in self.function_declarations:
                 # Simple representation: name(args) - description
                 # Ensure parameters exist before trying to access properties
                 args_str = ""
                 if func_decl.parameters and func_decl.parameters.properties:
                      args_list = []
                      required_args = func_decl.parameters.required or []
                      for prop, details in func_decl.parameters.properties.items():
                            # Access attributes directly from the Schema object
                            prop_type = details.type if hasattr(details, 'type') else 'UNKNOWN' 
                            prop_desc = details.description if hasattr(details, 'description') else ''
                            
                            suffix = "" if prop in required_args else "?" # Indicate optional args
                            
                            # Include parameter description in the string for clarity in the system prompt
                            args_list.append(f"{prop}: {prop_type}{suffix} # {prop_desc}") 
                            
                      args_str = ", ".join(args_list)
                 
                 desc = func_decl.description or "(No description provided)" # Overall func desc
                 tool_descriptions.append(f"- `{func_decl.name}({args_str})`: {desc}")
        else:
             tool_descriptions.append(" - (No tools available with function declarations)")

        tool_list_str = "\n".join(tool_descriptions)

        # Prompt v13.1 - Native Functions, Planning, Accurate Context
        return f"""You are Gemini Code, an AI coding assistant running in a CLI environment.
Your goal is to help the user with their coding tasks by understanding their request, planning the necessary steps, and using the available tools via **native function calls**.

Available Tools (Use ONLY these via function calls):
{tool_list_str}

Workflow:
1.  **Analyze & Plan:** Understand the user's request based on the provided directory context (`ls` output) and the request itself. For non-trivial tasks, **first outline a brief plan** of the steps and tools you will use in a text response.
2.  **Execute:** If a plan is not needed or after outlining the plan, make the **first necessary function call** to execute the next step (e.g., `view` a file, `edit` a file, `grep` for text, `tree` for structure).
3.  **Observe:** You will receive the result of the function call.
4.  **Repeat:** Based on the result, make the next function call required to achieve the user's goal. Continue calling functions sequentially until the task is complete.
5.  **Complete:** Once the *entire* task is finished, **you MUST call the `task_complete` function**, providing a concise summary of what was done in the `summary` argument. 
    *   The `summary` argument MUST accurately reflect the final outcome (success, partial success, error, or what was done).
    *   Format the summary using **Markdown** for readability (e.g., use backticks for filenames `like_this.py` or commands `like this`).
    *   If code was generated or modified, the summary SHOULD include concise instructions on how to run or test it (e.g., necessary commands in Markdown code blocks).

Important Rules:
*   **Use Native Functions:** ONLY interact with tools by making function calls as defined above. Do NOT output tool calls as text (e.g., `cli_tools.ls(...)`).
*   **Sequential Calls:** Call functions one at a time. You will get the result back before deciding the next step. Do not try to chain calls in one turn.
*   **Initial Context Handling:** When the user asks a general question about the codebase contents (e.g., "what's in this directory?", "show me the files", "whats in this codebase?"), your **first** response MUST be a summary or list of **ALL** files and directories provided in the initial context (`ls` or `tree` output). Do **NOT** filter this initial list or make assumptions (e.g., about virtual environments). Only after presenting the full initial context should you suggest further actions or use other tools if necessary.
*   **Accurate Context Reporting:** When asked about directory contents (like "whats in this codebase?"), accurately list or summarize **all** relevant files and directories shown in the `ls` or `tree` output, including common web files (`.html`, `.js`, `.css`), documentation (`.md`), configuration files, build artifacts, etc., not just specific source code types. Do not ignore files just because virtual environments are also present. Use `tree` for a hierarchical view if needed.
*   **Planning First:** For tasks requiring multiple steps (e.g., read file, modify content, write file), explain your plan briefly in text *before* the first function call.
*   **Precise Edits:** When editing files (`edit` tool), prefer viewing the relevant section first (`view` tool with offset/limit), then use exact `old_string`/`new_string` arguments if possible. Only use the `content` argument for creating new files or complete overwrites.
*   **Task Completion Signal:** ALWAYS finish by calling `task_complete(summary=...)`. 
    *   The `summary` argument MUST accurately reflect the final outcome (success, partial success, error, or what was done).
    *   Format the summary using **Markdown** for readability (e.g., use backticks for filenames `like_this.py` or commands `like this`).
    *   If code was generated or modified, the summary SHOULD include concise instructions on how to run or test it (e.g., necessary commands in Markdown code blocks).

The user's first message will contain initial directory context and their request."""

    # --- Text Extraction Helper (if needed for final output) ---
    def _extract_text_from_response(self, response) -> str | None:
         """Safely extracts text from a Gemini response object."""
         try:
             if response and response.candidates:
                 # Handle potential multi-part responses if ever needed, for now assume text is in the first part
                 if response.candidates[0].content and response.candidates[0].content.parts:
                     text_parts = [part.text for part in response.candidates[0].content.parts if hasattr(part, 'text')]
                     return "\n".join(text_parts).strip() if text_parts else None
             return None
         except (AttributeError, IndexError) as e:
             log.warning(f"Could not extract text from response: {e} - Response: {response}")
             return None
             
    # --- Find Last Text Helper ---
    def _find_last_model_text(self, history: list) -> str:
        """Finds the last text part sent by the model in the history."""
        for i in range(len(history) - 1, -1, -1):
            if history[i]['role'] == 'model':
                try:
                     # Check if parts exists and has content
                     if history[i]['parts'] and hasattr(history[i]['parts'][0], 'text'):
                           return history[i]['parts'][0].text.strip()
                except (AttributeError, IndexError):
                     continue # Ignore malformed history entries
        return "(No previous text response found)"

# --- ADD HELPER for Tool Definition Generation ---
# Moved into the class as _create_tool_definitions
# ---

# --- ADD get_function_declaration methods to BaseTool and concrete tools ---
# This needs to be done in the respective tool files (e.g., base.py, file_tools.py)
# Example for BaseTool (in base.py):
# from google.generativeai.types import FunctionDeclaration, Tool, HarmCategory, HarmBlockThreshold
# class BaseTool:
#     name: str = "base_tool"
#     description: str = "Base tool description"
#     # Define schema as a class variable or method
#     args_schema: dict = {} # Example: {"file_path": {"type": "string", "description": "Path to the file"}}
#     required_args: list[str] = [] # Example: ["file_path"]

#     @classmethod
#     def get_function_declaration(cls) -> FunctionDeclaration | None:
#         if not cls.args_schema:
#             # Handle tools with no arguments - still need a declaration
#             return FunctionDeclaration(
#                 name=cls.name,
#                 description=cls.description,
#                 parameters=None # Or an empty schema object if required by API
#             )
        
#         properties = {}
#         for arg_name, details in cls.args_schema.items():
#             # Basic mapping, might need adjustment for complex types/enums
#             properties[arg_name] = {
#                 "type": details.get("type", "string"), # Default to string if type missing
#                 "description": details.get("description", "")
#             }
            
#         # Ensure required list only contains args present in properties
#         valid_required = [req for req in cls.required_args if req in properties]
        
#         # Handle case where required is empty after validation
#         required_list = valid_required if valid_required else None

#         return FunctionDeclaration(
#             name=cls.name,
#             description=cls.description,
#             parameters={
#                 "type": "object",
#                 "properties": properties,
#                 "required": required_list
#             }
#         )
#     # ... rest of BaseTool ...