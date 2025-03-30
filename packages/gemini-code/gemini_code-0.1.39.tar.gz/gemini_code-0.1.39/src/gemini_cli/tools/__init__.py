"""
Tools module initialization.

This module defines the available tools for the Gemini coding assistant
and provides a standardized way to access instances of these tools.
"""

import logging
from .base import BaseTool
from .file_tools import ViewTool, EditTool, ListTool, GrepTool, GlobTool

# --- Tool Imports ---
# Import tools that are confirmed to exist and be implemented.
# Comment out any imports for tools that are not yet ready.

# Assuming system_tools.py exists with a BashTool class:
try:
    from .system_tools import BashTool
    bash_tool_available = True
except ImportError:
    logging.warning("system_tools.py or BashTool class not found. Bash tool disabled.")
    bash_tool_available = False

# Assuming web_tools.py/WebTool is NOT ready:
# from .web_tools import WebTool
web_tool_available = False

# --- ADDED: Import the new TestRunnerTool ---
try:
    from .test_runner import TestRunnerTool
    test_runner_available = True
except ImportError:
    logging.warning("test_runner.py or TestRunnerTool class not found. Test runner tool disabled.")
    test_runner_available = False
# --- End Add ---

# Assuming linter_checker.py/LinterCheckerTool is NOT ready:
# from .linter_checker import LinterCheckerTool # Example placeholder
linter_checker_available = False
# --- End Tool Imports ---


# AVAILABLE_TOOLS maps tool names (strings) used in prompts/definitions
# to the actual tool classes. Only include implemented and imported tools.
AVAILABLE_TOOLS = {
    "view": ViewTool,
    "edit": EditTool,
    "ls": ListTool,
    "grep": GrepTool,
    "glob": GlobTool,
}

# Conditionally add tools based on successful imports
if bash_tool_available:
    AVAILABLE_TOOLS["bash"] = BashTool
# if web_tool_available:
#     AVAILABLE_TOOLS["web"] = WebTool

# --- ADDED: Register TestRunnerTool if available ---
if test_runner_available:
    AVAILABLE_TOOLS["test_runner"] = TestRunnerTool
# --- End Add ---

# if linter_checker_available:
#     AVAILABLE_TOOLS["linter_checker"] = LinterCheckerTool # Example placeholder

def get_tool(name: str) -> BaseTool | None:
    """
    Retrieves an *instance* of the tool class based on its name.

    Args:
        name: The name of the tool (e.g., "edit", "view").

    Returns:
        An instance of the corresponding BaseTool subclass, or None if not found
        or if instantiation fails.
    """
    tool_class = AVAILABLE_TOOLS.get(name)
    if tool_class:
        try:
            # Return a new instance of the tool class
            instance = tool_class()
            logging.debug(f"Successfully instantiated tool: {name}")
            return instance
        except Exception as e:
            # Log the error with traceback for easier debugging
            logging.error(f"Error instantiating tool '{name}': {e}", exc_info=True)
            return None
    else:
        logging.warning(f"Tool '{name}' not found in AVAILABLE_TOOLS.")
        return None

# Optional helper (might not be used directly by GeminiModel now)
def get_all_tool_instances() -> list[BaseTool]:
    """Returns a list of instances of all available tools."""
    instances = []
    for name in AVAILABLE_TOOLS.keys():
        instance = get_tool(name)
        if instance:
            instances.append(instance)
    return instances

logging.info(f"Tools initialized. Available tools: {list(AVAILABLE_TOOLS.keys())}")