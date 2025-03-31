"""
Gemini model integration for the CLI tool.
Targeting Gemini 2.5 Pro Experimental.
AGENTIC LOOP (CODE GENERATION) w/ FORCED ORIENTATION & TASK COMPLETE TOOL.
PERSISTENT HISTORY ACROSS TURNS. Includes Quality tools. Prompt v12. Syntax FIXED.
"""

import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool
import re
import json
import logging
import ast
import shlex
import time
from rich.console import Console

# Import exceptions for specific error handling if needed later
# from google.api_core.exceptions import ResourceExhausted, InvalidArgument

from ..utils import count_tokens
from ..tools import get_tool, AVAILABLE_TOOLS
from ..tools.summarizer_tool import SummarizeCodeTool # Import class directly

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

TOOL_CALL_PATTERN = re.compile(r"cli_tools\.(\w+)\s*\((.*?)\)", re.DOTALL | re.MULTILINE)
MAX_AGENT_ITERATIONS = 10 # Reduced slightly as context grows
CONTEXT_TRUNCATION_THRESHOLD = 800000 # Example: ~80% of 1M tokens, adjust based on model

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
    """Interface for Gemini models implementing agentic loop with persistent history."""

    def __init__(self, api_key: str, console: Console, model_name: str ="gemini-2.5-pro-exp-03-25"):
        """Initialize the Gemini model interface for agentic code generation."""
        self.api_key = api_key
        self.model_name = model_name
        self.console = console
        genai.configure(api_key=api_key)

        self.generation_config = genai.types.GenerationConfig( temperature=0.4, top_p=0.95, top_k=40 )
        self.safety_settings = { "HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE", "HATE": "BLOCK_MEDIUM_AND_ABOVE", "SEXUAL": "BLOCK_MEDIUM_AND_ABOVE", "DANGEROUS": "BLOCK_MEDIUM_AND_ABOVE" }
        _ = self._create_tool_definitions() # Syntax check only
        self.system_instruction = self._create_system_prompt() # Using v12 prompt

        try:
            logging.info(f"Creating model: {self.model_name} for Agentic Loop w/ TaskCompleteTool.")
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings,
                system_instruction=self.system_instruction
            )
            # --- Initialize Persistent History ---
            # Start history with just the system prompt (acting as initial user turn for setup)
            self.chat_history = [{'role': 'user', 'parts': [self.system_instruction]}]
            # Model's initial (empty) response after system prompt
            self.chat_history.append({'role': 'model', 'parts': ["Okay, I am ready and understand the workflow."]})
            # ---
            logging.info("GeminiModel initialized successfully (TaskComplete Agent Loop).")
        except Exception as e:
             logging.error(f"Fatal error initializing Gemini model '{self.model_name}': {str(e)}", exc_info=True); raise Exception(f"Could not initialize Gemini model: {e}") from e

    # ... (get_available_models remains the same) ...
    def get_available_models(self): return list_available_models(self.api_key)

    # --- generate function MODIFIED for Persistent History ---
    def generate(self, prompt: str, conversation=None) -> str | None:
        logging.info(f"Agent Loop - Processing prompt: '{prompt[:100]}...'")
        original_user_prompt = prompt
        if prompt.startswith('/'):
             command = prompt.split()[0].lower()
             if command in ['/exit', '/help', '/compact']: logging.info(f"Handled command: {command}"); return None

        # === Step 1: Mandatory Orientation ===
        orientation_context = ""; ls_result = "(ls tool not found or failed)"
        try:
            # We still perform orientation on every turn for freshest context
            logging.info("Performing mandatory orientation (ls)...")
            ls_tool = get_tool("ls")
            if ls_tool: ls_result = ls_tool.execute()
            else: logging.warning("Could not find 'ls' tool for mandatory orientation.")
            # Don't print this every time maybe? Or make it very subtle.
            # self.console.print(f"[dim]Directory context refreshed.[/dim]")
            orientation_context = f"Current directory contents (from `ls .`):\n```\n{ls_result}\n```\n"
            logging.info("Orientation successful.")
        except Exception as orient_error:
            logging.error(f"Error during mandatory orientation: {orient_error}", exc_info=True)
            orientation_context = f"Error during initial directory scan: {orient_error}\n"
            self.console.print(f"[red]Error getting directory listing: {orient_error}[/red]")

        # === Step 2: Prepare Input for First LLM Call of this Turn ===
        # Construct the message combining orientation and user prompt for THIS turn
        turn_input_prompt = f"{orientation_context}\nUser request: {original_user_prompt}\n\nBased on the directory contents and the request, generate the Python code for the first necessary action(s) using `cli_tools.X(...)`. If the task is already complete or requires no action, call `cli_tools.task_complete(summary='...')`."

        # Add this combined input to the PERSISTENT history
        self.chat_history.append({'role': 'user', 'parts': [turn_input_prompt]})
        # Truncate history if it gets too long BEFORE the API call
        self._manage_context_window()

        iteration_count = 0; task_completed = False; final_summary = None

        try:
            while iteration_count < MAX_AGENT_ITERATIONS:
                iteration_count += 1
                logging.info(f"Agent Loop Iteration {iteration_count}/{MAX_AGENT_ITERATIONS}")

                # === Get Next Action Code ===
                generated_text = ""; llm_response = None
                try:
                    logging.info(f"Asking LLM ({self.model_name}) for next action(s)...")
                    # Use the full persistent history
                    llm_response = self.model.generate_content( self.chat_history, generation_config=self.generation_config )
                    logging.debug(f"RAW Gemini Response Object (Iter {iteration_count}): {llm_response}")
                    generated_text = self._extract_text_from_response(llm_response)
                except Exception as generation_error:
                     # ...(error handling)...
                     logging.error(f"Error during LLM generation: {generation_error}", exc_info=True)
                     error_text = self._extract_text_from_response(llm_response) if llm_response else f"Generation Error: {generation_error}"
                     # Add error to history? Maybe not, could confuse it. Just return.
                     return f"Error during LLM generation step: {generation_error}"

                logging.info(f"LLM suggested action/code (Iter {iteration_count}):\n---\n{generated_text}\n---")
                # Add LLM response to PERSISTENT history
                self.chat_history.append({'role': 'model', 'parts': [generated_text]})
                self._manage_context_window() # Truncate after adding

                # === Parse and Execute Tool Calls ===
                executed_tool_info = self._parse_and_execute_tool_calls(generated_text) # List of (name, result_dict)

                # === Check for Task Completion Signal ===
                task_complete_found = False
                for tool_name, result_data in executed_tool_info:
                    if tool_name == "task_complete":
                        logging.info("Task completion signaled by task_complete tool call.")
                        task_completed = True
                        final_summary = result_data.get("result", "Task completed, but summary extraction failed.")
                        # Add the execution result of task_complete to history? Maybe just the fact it was called.
                        # Let's not add the result, just break. The summary is extracted.
                        break # Exit inner loop (tool execution results)

                if task_completed: break # Exit the outer while loop

                # === Handle case where NO tool calls were returned (or only task_complete was called but loop didn't break?) ===
                # Filter out task_complete before checking if the list is empty
                actionable_calls = [info for info in executed_tool_info if info[0] != 'task_complete']

                if not actionable_calls:
                    logging.warning(f"No actionable tool calls found/executed (Iter {iteration_count}). Asking LLM to clarify or finish.")
                    # Ask LLM to clarify or finish if stuck
                    clarification_request = "You did not provide any actionable tool calls (`edit`, `view`, `bash`, etc.). Please either provide the next `cli_tools.X(...)` call or signal completion with `cli_tools.task_complete(summary='...')`."
                    self.chat_history.append({'role': 'user', 'parts': [clarification_request]})
                    self._manage_context_window()
                    continue # Ask again in the next loop iteration

                # === Prepare Results Feedback for Next Iteration ===
                results_feedback = "Executed tool calls. Results:\n\n"; any_errors = False
                for tool_name, result_data in executed_tool_info: # Use the full list here for feedback
                     call_str = result_data.get('call_str', f'cli_tools.{tool_name}(...)')
                     result = result_data.get('result', '(No result captured)')
                     results_feedback += f"Call: `{call_str}`\n"; results_feedback += f"Result: ```\n{result}\n```\n---\n"
                     if "Error" in str(result): any_errors = True

                results_feedback += "\nBased on these results, what is the next `cli_tools.X(...)` action needed, or call `cli_tools.task_complete(summary='...')` if finished?"
                # Add results feedback to PERSISTENT history
                self.chat_history.append({'role': 'user', 'parts': [results_feedback]})
                self._manage_context_window()

                if any_errors: logging.warning("Errors occurred during tool execution. Loop will continue.")

            # === End Agent Loop ===

            # === Handle Output ===
            if task_completed and final_summary:
                 logging.info("Task completed successfully via task_complete tool.")
                 cleaned_summary = self._cleanup_internal_tags(final_summary)
                 return cleaned_summary.strip()
            elif iteration_count >= MAX_AGENT_ITERATIONS:
                 logging.warning(f"Agent loop terminated after reaching max iterations ({MAX_AGENT_ITERATIONS}).")
                 # Don't ask for summary on timeout, just return error/last state?
                 # Or maybe return the last *model* response?
                 last_model_response = self._find_last_model_message(self.chat_history)
                 timeout_message = f"(Task exceeded max iterations ({MAX_AGENT_ITERATIONS}). Last model output below)\n{last_model_response}"
                 return self._cleanup_internal_tags(timeout_message).strip()
            else:
                 logging.error("Agent loop exited without task_complete signal or reaching max iterations.")
                 # Return last model response if loop exited unexpectedly
                 last_model_response = self._find_last_model_message(self.chat_history)
                 return f"(Agent loop finished unexpectedly. Last model output below)\n{self._cleanup_internal_tags(last_model_response).strip()}"

        except Exception as e:
             logging.error(f"Error during Agent Loop: {str(e)}", exc_info=True); return f"An unexpected error occurred during the agent process: {str(e)}"


    # --- NEW HELPER for Context Management ---
    def _manage_context_window(self):
        """Basic context window management: remove oldest turns if history is too long."""
        # This is a very basic strategy. More sophisticated methods exist (summarization, etc.)
        # Calculate current token count (approximate)
        current_tokens = count_tokens(str(self.chat_history)) # Uses your existing count_tokens util

        if current_tokens > CONTEXT_TRUNCATION_THRESHOLD:
             logging.warning(f"Context approaching limit ({current_tokens} tokens). Truncating oldest non-system messages.")
             # Keep system prompt (index 0) and the model's initial ack (index 1)
             # Remove the oldest user/model pairs after that until below threshold
             history_to_prune = self.chat_history[2:]
             tokens_to_remove = current_tokens - CONTEXT_TRUNCATION_THRESHOLD

             removed_count = 0
             while tokens_to_remove > 0 and len(history_to_prune) >= 2:
                  # Remove one user/model pair from the beginning of the prunable section
                  removed_user = history_to_prune.pop(0)
                  removed_model = history_to_prune.pop(0)
                  removed_count += 2
                  # Recalculate tokens (less efficient but safer)
                  tokens_to_remove = count_tokens(str([self.chat_history[0], self.chat_history[1]] + history_to_prune)) - CONTEXT_TRUNCATION_THRESHOLD
                  # Or estimate removed tokens: tokens_to_remove -= (count_tokens(str(removed_user)) + count_tokens(str(removed_model)))

             # Reassemble history
             self.chat_history = [self.chat_history[0], self.chat_history[1]] + history_to_prune
             logging.info(f"Removed {removed_count} oldest messages from history. New approx token count: {count_tokens(str(self.chat_history))}")

    # --- NEW HELPER to find last model message ---
    def _find_last_model_message(self, history: list) -> str:
         """Extracts the text from the last message with role 'model' in the history."""
         for i in range(len(history) - 1, -1, -1):
              if history[i].get('role') == 'model':
                   try:
                        # Assuming 'parts' is a list containing text
                        return "".join(part for part in history[i].get('parts', []) if isinstance(part, str))
                   except Exception:
                        return "(Could not extract last model message)"
         return "(No model messages found in history)"


        # --- CORRECTED _parse_and_execute_tool_calls with robust string parsing syntax fix ---
    def _parse_and_execute_tool_calls(self, text: str) -> list[tuple[str, dict]]:
        """Finds, parses, executes ALL `cli_tools.X(...)` calls, robustly handling strings."""
        executed_call_results = [] # List of tuples: (func_name, result_dict)
        matches = TOOL_CALL_PATTERN.finditer(text)
        any_matches = False

        for match in matches:
            any_matches = True
            call_str = match.group(0); func_name = match.group(1); args_str = match.group(2).strip()
            logging.info(f"Found potential tool call: cli_tools.{func_name}({args_str[:100]}...)")
            args = {}
            result_data = {"call_str": call_str} # Store info for feedback

            # --- Improved Argument Parsing ---
            try:
                # Use regex to find keyword arguments: kw=\s*(value)
                kw_arg_pattern = re.compile(
                    r"(\w+)\s*=\s*("                           # Capture keyword name (group 1) and value (group 2)
                    r"'''(.*?)'''|"                          # Triple single quotes (non-greedy content group 3)
                    r'"""(.*?)"""|'                          # Triple double quotes (non-greedy content group 4)
                    r"'(.*?)'(?!')|"                         # Single quotes (non-greedy content group 5, not followed by another ')
                    r'"(.*?)"(?!")|'                         # Double quotes (non-greedy content group 6, not followed by another ")
                    r"([^,=\s(][^,]*?)"                        # Other literals (non-greedy, group 7) - needs refinement maybe?
                    r")\s*(?:,|$)"                            # Comma or end of string/args
                    , re.DOTALL
                )

                last_pos = 0
                for kw_match in kw_arg_pattern.finditer(args_str):
                    arg_name = kw_match.group(1)
                    matched_value_part = kw_match.group(2) # Full value part

                    # Extract and unescape string content carefully
                    if kw_match.group(3) is not None: # '''
                        args[arg_name] = kw_match.group(3); logging.debug(f"Parsed arg '{arg_name}' as triple-single-quoted string")
                    elif kw_match.group(4) is not None: # """
                        args[arg_name] = kw_match.group(4); logging.debug(f"Parsed arg '{arg_name}' as triple-double-quoted string")
                    elif kw_match.group(5) is not None: # '
                        # CORRECTED: try/except block indented
                        try:
                            args[arg_name] = bytes(kw_match.group(5), "utf-8").decode("unicode_escape")
                        except Exception:
                            args[arg_name] = kw_match.group(5) # Fallback
                        logging.debug(f"Parsed arg '{arg_name}' as single-quoted string")
                    elif kw_match.group(6) is not None: # "
                        # CORRECTED: try/except block indented
                        try:
                            args[arg_name] = bytes(kw_match.group(6), "utf-8").decode("unicode_escape")
                        except Exception:
                            args[arg_name] = kw_match.group(6) # Fallback
                        logging.debug(f"Parsed arg '{arg_name}' as double-quoted string")
                    elif kw_match.group(7) is not None: # Other literal
                        literal_str = kw_match.group(7).strip()
                        # CORRECTED: try/except block indented
                        try:
                            args[arg_name] = ast.literal_eval(literal_str)
                            logging.debug(f"Parsed arg '{arg_name}' as literal using ast")
                        except (ValueError, SyntaxError):
                            logging.warning(f"Could not parse '{literal_str}' as literal for arg '{arg_name}'. Treating as string.")
                            args[arg_name] = literal_str # Fallback to string
                    else:
                         logging.warning(f"Could not determine value type for arg '{arg_name}' in {call_str}. Skipping.")
                         continue # Skip this argument

                    last_pos = kw_match.end()

                # Check if there's unparsed content
                if last_pos < len(args_str.rstrip(')')):
                     logging.warning(f"Potential unparsed arguments remaining in '{args_str[last_pos:]}' for call {call_str}")

            except Exception as parse_error:
                logging.error(f"Complex arg parsing failed for '{call_str}': {parse_error}", exc_info=True)
                result_data["result"] = f"Error: Failed to parse arguments - {parse_error}"
                executed_call_results.append((func_name, result_data))
                continue # Process next match

            # --- Execute the parsed call ---
            try:
                result_str = "(Execution failed)"
                logging.info(f"Executing parsed call: func='{func_name}', args={ {k: (v[:50] + '...' if isinstance(v, str) and len(v)>50 else v) for k,v in args.items()} })")
                self.console.print(f"[dim] -> Executing {func_name}...[/dim]")

                tool_instance = None
                if func_name == "summarize_code":
                     if "summarize_code" in AVAILABLE_TOOLS: tool_instance = SummarizeCodeTool(model_instance=self.model)
                     else: raise ValueError("Tool 'summarize_code' unavailable.")
                else: tool_instance = get_tool(func_name)

                if not tool_instance: raise ValueError(f"Tool '{func_name}' could not be instantiated or is not available.")

                result = tool_instance.execute(**args)
                result_str = str(result) if result is not None else "(No output)"

                result_data["result"] = result_str
                executed_call_results.append((func_name, result_data))
                logging.info(f"Execution successful for '{call_str}'. Result length: {len(result_str)}")

            except Exception as exec_error:
                logging.error(f"Exception during execution of '{call_str}': {exec_error}", exc_info=True)
                result_data["result"] = f"Error during execution: {exec_error}"
                executed_call_results.append((func_name, result_data))

        if not any_matches: logging.info("No parsable cli_tools calls found in the generated text.")
        return executed_call_results # Return list of tuples
    # --- End CORRECTED Method ---


    # ... (_extract_text_from_response remains the same) ...
    def _extract_text_from_response(self, response):
        # ... (Same robust version) ...
        try:
            all_text = []
            if response.candidates:
                 if response.candidates[0].finish_reason.name != "STOP":
                     logging.warning(f"Response generation stopped due to: {response.candidates[0].finish_reason.name}")
                     if response.candidates[0].safety_ratings: ratings = {r.category.name: r.probability.name for r in response.candidates[0].safety_ratings}; return f"(Response blocked due to safety settings: {ratings})"
                     return f"(Response generation incomplete: {response.candidates[0].finish_reason.name})"
                 for part in response.candidates[0].content.parts:
                     if hasattr(part, 'text'): all_text.append(part.text)
                 return "".join(all_text)
            elif hasattr(response, 'text'): return response.text
            elif response.prompt_feedback and response.prompt_feedback.block_reason: logging.warning(f"Prompt blocked due to: {response.prompt_feedback.block_reason.name}"); return f"(Prompt blocked due to: {response.prompt_feedback.block_reason.name})"
            else: logging.warning("Could not extract text from response structure."); return ""
        except Exception as e: logging.error(f"Error extracting text: {e}", exc_info=True); return f"Error extracting response text: {e}"


    # ... (_cleanup_internal_tags remains the same) ...
    def _cleanup_internal_tags(self, text: str) -> str:
        # ... (Same cleanup) ...
        text = re.sub(r"<thinking>.*?</thinking>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"<plan>.*?</plan>\s*", "", text, flags=re.DOTALL)
        text = re.sub(r"# Thinking:.*?\n", "", text)
        text = re.sub(r"# Plan:.*?\n", "", text)
        return text.strip()

    # --- V12 Prompt: Agentic Loop with TaskCompleteTool & Summarizer ---
    def _create_system_prompt(self) -> str:
        """Creates the system instruction prompt for the agentic loop w/ TaskCompleteTool & Summarizer."""
        # ... (V12 prompt - same as previous response) ...
        tools_description = []
        if AVAILABLE_TOOLS:
            for name, tool_class in AVAILABLE_TOOLS.items():
                try:
                    tool_instance = tool_class(); desc = getattr(tool_instance, 'description', f'Tool {name}')
                    param_hints = []
                    # ...(param hints including summarize_code)...
                    if name == 'task_complete': param_hints = ["summary='User-facing summary.'"]
                    elif name == 'summarize_code': param_hints = ["file_path='path/to/large_file.ext'"]
                    elif name == 'edit': param_hints = ["file_path='path'", "content='...' (OR)", "old_string='...', new_string='...'"]
                    elif name == 'view': param_hints = ["file_path='path'", "offset=Optional[int]", "limit=Optional[int]"]
                    elif name == 'ls': param_hints = ["path='.'", "ignore='Optional[str]'"]
                    elif name == 'grep': param_hints = ["pattern='regex'", "path='.'", "include='*.ext'"]
                    elif name == 'glob': param_hints = ["pattern='glob_pat'", "path='.'"]
                    elif name == 'bash': param_hints = ["command='cmd string'"]
                    elif name == 'test_runner': param_hints = ["test_path='Optional[str]'", "options='Optional[str]'", "runner_command='pytest'"]
                    elif name == 'create_directory': param_hints = ["dir_path='path/to/new_dir'"]
                    elif name == 'linter_checker': param_hints = ["path='.'", "linter_command='ruff check'"]
                    elif name == 'formatter': param_hints = ["path='.'", "formatter_command='black'"]
                    else: param_hints = ["..."]
                    tools_description.append(f"`cli_tools.{name}({', '.join(param_hints)})`: {desc}")
                except Exception as e: logging.warning(f"Could not get description/params for tool '{name}': {e}"); tools_description.append(f"`cli_tools.{name}(...)`: Tool to {name} files/system.")
        else: logging.warning("AVAILABLE_TOOLS dictionary not found or empty.")

        system_prompt = f"""You are 'Gemini Code', an AI coding assistant in a CLI. **Your ONLY way to interact is by generating Python code calling `cli_tools` functions.**

**Your Goal:** Achieve the user's request via a sequence of `cli_tools` calls.

**Workflow:**

1.  **Receive Context:** User request & directory listing.
2.  **Plan & Generate Initial Actions:** Analyze context. Generate code for initial actions using `cli_tools`. **INFO GATHERING STRATEGY:**
    *   Use `cli_tools.summarize_code(file_path='...')` for large files or overviews.
    *   Use `cli_tools.view(...)` ONLY for small files or specific sections (ideally with offset/limit after using `grep`).
    *   Use `cli_tools.grep(...)` to find specific lines first.
    *   Generate necessary info-gathering calls first (can be multiple). If ready for action, generate the first `edit`/`bash`/etc. call. Use comments (`# Thinking:`).
3.  **Receive Results:** CLI executes code, gives results back.
4.  **Reflect & Generate Next Action OR Finish:** Analyze results. If more steps needed, generate code for the *next single action*. If task complete, **you MUST call `cli_tools.task_complete(summary='...')`**, providing a concise user-facing summary. Handle errors.
5.  **Repeat:** Loop continues until `task_complete` is called.
6.  **(Final Step Handled by CLI):** Summary from `task_complete` shown.

**CRITICAL INSTRUCTIONS:**
*   **OUTPUT ONLY PYTHON CODE or `task_complete` call:** Your response MUST be *only* Python code calling `cli_tools` functions OR `cli_tools.task_complete(summary='...')`. No conversational text unless in comments.
*   **USE SUMMARIZER/VIEW WISELY:** Prefer `summarize_code` for large files.
*   **FINAL STEP IS `task_complete`:** End tasks with `cli_tools.task_complete(summary='...')`.
*   **USE `cli_tools`:** Prefix calls with `cli_tools.`.
*   **ONE ACTION AT A TIME (after info gathering):** Focus on one `edit`/`bash`/`test_runner` action per turn.
*   **STRINGS MUST BE QUOTED:** Use quotes correctly (triple for multiline). Use keyword arguments.
*   **`edit` Tool:** Use `content='...'` (create/overwrite) OR `old_string`/`new_string` (replace).
*   **HANDLE RESULTS:** Decide next action based on results.

**Available `cli_tools` Functions:**
{chr(10).join(tools_description) if tools_description else "No `cli_tools` functions available."}

You will now receive the initial context. Generate the Python code for the first action(s), using `summarize_code` or `view` appropriately.
"""
        return system_prompt


        # --- CORRECTED _create_tool_definitions Method (Syntax GUARANTEED FIXED) ---
    def _create_tool_definitions(self) -> list[Tool]:
        """Native tool definitions - NOT CURRENTLY USED but needs correct syntax for import."""
        tool_declarations = [] # Holds FunctionDeclaration objects

        # --- Define the view tool ---
        if "view" in AVAILABLE_TOOLS:
            # CORRECT: try is on a new line, indented
            try:
                tool_declarations.append(FunctionDeclaration(
                    name="view",
                    description="View specific sections or small files. For large files, use summarize_code.",
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
                tool_declarations.append(FunctionDeclaration(
                    name="test_runner",
                    description="Runs automated tests using the project's test runner (e.g., pytest).",
                    parameters={ "type": "object", "properties": {
                            "test_path": {"type": "string", "description": "Specific file or directory path to test (optional, runs discovered tests if omitted)."},
                            "options": {"type": "string", "description": "Additional command-line options for the test runner (e.g., '-k my_test', '-v', '--cov'). Optional."},
                            "runner_command": {"type": "string", "description": "The command for the test runner (default: 'pytest'). Optional."}
                        }}
                ))
            # CORRECT: except is aligned with try
            except Exception as e:
                logging.error(f"Failed to define 'test_runner' tool: {e}")

        # --- Define the task_complete tool ---
        if "task_complete" in AVAILABLE_TOOLS:
             # CORRECT: try is on a new line, indented
             try:
                 tool_declarations.append(FunctionDeclaration(
                     name="task_complete",
                     description="Signals task completion. MUST be called as the final step, providing a user-friendly summary.",
                     parameters={ "type": "object", "properties": {
                             "summary": {"type": "string", "description": "Concise, user-friendly summary of actions taken and final outcome."}
                         }, "required": ["summary"] }
                 ))
             # CORRECT: except is aligned with try
             except Exception as e:
                 logging.error(f"Failed to define 'task_complete' tool: {e}")

        # --- Define create_directory tool ---
        if "create_directory" in AVAILABLE_TOOLS:
             # CORRECT: try is on a new line, indented
             try:
                 tool_declarations.append(FunctionDeclaration(
                     name="create_directory",
                     description="Creates a new directory, including any necessary parent directories.",
                     parameters={ "type": "object", "properties": {
                             "dir_path": {"type": "string", "description": "The path of the directory to create."}
                         }, "required": ["dir_path"] }
                 ))
             # CORRECT: except is aligned with try
             except Exception as e:
                 logging.error(f"Failed to define 'create_directory' tool: {e}")

        # --- Define linter_checker tool ---
        if "linter_checker" in AVAILABLE_TOOLS:
             # CORRECT: try is on a new line, indented
             try:
                 tool_declarations.append(FunctionDeclaration(
                     name="linter_checker",
                     description="Runs a code linter (default: 'ruff check') on a specified path to find potential issues.",
                     parameters={ "type": "object", "properties": {
                             "path": {"type": "string", "description": "File or directory path to lint (default: '.')."},
                             "linter_command": {"type": "string", "description": "Base command for the linter (default: 'ruff check')."}
                         }}
                 ))
             # CORRECT: except is aligned with try
             except Exception as e:
                 logging.error(f"Failed to define 'linter_checker' tool: {e}")

        # --- Define formatter tool ---
        if "formatter" in AVAILABLE_TOOLS:
             # CORRECT: try is on a new line, indented
             try:
                 tool_declarations.append(FunctionDeclaration(
                     name="formatter",
                     description="Runs a code formatter (default: 'black') on a specified path to automatically fix styling.",
                     parameters={ "type": "object", "properties": {
                             "path": {"type": "string", "description": "File or directory path to format (default: '.')."},
                             "formatter_command": {"type": "string", "description": "Base command for the formatter (default: 'black')."}
                         }}
                 ))
             # CORRECT: except is aligned with try
             except Exception as e:
                 logging.error(f"Failed to define 'formatter' tool: {e}")

        # --- Define summarize_code tool ---
        if "summarize_code" in AVAILABLE_TOOLS:
             # CORRECT: try is on a new line, indented
             try:
                 tool_declarations.append(FunctionDeclaration(
                     name="summarize_code",
                     description="Provides a summary of a code file's purpose, key functions/classes, and structure. Use for large files.",
                     parameters={ "type": "object", "properties": {
                             "file_path": {"type": "string", "description": "Path to the file to summarize."}
                         }, "required": ["file_path"] }
                 ))
             # CORRECT: except is aligned with try
             except Exception as e:
                 logging.error(f"Failed to define 'summarize_code' tool: {e}")

        logging.debug("Native tool definitions parsed (syntax check only in Code Gen mode).")
        # Return empty list as we are not using native tools in Code Gen mode
        return []
    # --- End CORRECTED Method ---