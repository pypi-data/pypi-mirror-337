"""
Tools module initialization.

This module defines the available tools and provides a way to access them.
"""

import logging
from .base import BaseTool
from .file_tools import ViewTool, EditTool, ListTool, GrepTool, GlobTool

# --- Assumptions ---
# Make sure you actually have these files and classes defined!
# If not, comment out the relevant lines here and in AVAILABLE_TOOLS.

# Commenting out BashTool assuming system_tools.py might not be ready
# from .system_tools import BashTool

# Commenting out WebTool because the import failed
# from .web_tools import WebTool
# --- End Assumptions ---

# AVAILABLE_TOOLS maps tool names (strings) to the tool classes
# This is used by GeminiModel to generate system prompts and tool definitions.
AVAILABLE_TOOLS = {
    "view": ViewTool,
    "edit": EditTool,
    "ls": ListTool,
    "grep": GrepTool,
    "glob": GlobTool,
    # "bash": BashTool,  # <<< COMMENTED OUT
    # "web": WebTool,    # <<< COMMENTED OUT
    # Add any other tool classes here AFTER you create the files and classes
}

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
            logging.error(f"Error instantiating tool '{name}': {e}", exc_info=True)
            return None
    else:
        logging.warning(f"Tool '{name}' not found in AVAILABLE_TOOLS.")
        return None

# You might also want a function to get all tool instances if needed elsewhere
def get_all_tool_instances() -> list[BaseTool]:
    """Returns a list of instances of all available tools."""
    instances = []
    for name in AVAILABLE_TOOLS.keys():
        instance = get_tool(name)
        if instance:
            instances.append(instance)
    return instances

logging.info(f"Tools initialized. Available tools: {list(AVAILABLE_TOOLS.keys())}")