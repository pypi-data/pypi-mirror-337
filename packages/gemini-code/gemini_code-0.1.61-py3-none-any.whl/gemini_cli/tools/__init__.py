"""
Tools module initialization. Registers all available tools.
"""

import logging
from .base import BaseTool
from .file_tools import ViewTool, EditTool, ListTool, GrepTool, GlobTool

# --- Tool Imports ---
try: from .system_tools import BashTool; bash_tool_available = True
except ImportError: logging.warning("system_tools.BashTool not found. Disabled."); bash_tool_available = False

# Add new tools
try: from .task_complete_tool import TaskCompleteTool; task_complete_available = True
except ImportError: logging.warning("task_complete_tool.TaskCompleteTool not found. Disabled."); task_complete_available = False

try: from .directory_tools import CreateDirectoryTool; create_dir_available = True
except ImportError: logging.warning("directory_tools.CreateDirectoryTool not found. Disabled."); create_dir_available = False

try: from .quality_tools import LinterCheckerTool, FormatterTool; quality_tools_available = True
except ImportError: logging.warning("quality_tools not found or missing classes. Disabled."); quality_tools_available = False

# Commented out placeholders
# try: from .test_runner import TestRunnerTool; test_runner_available = True
# except ImportError: logging.warning("test_runner.TestRunnerTool not found. Disabled."); test_runner_available = False
test_runner_available = True # Assuming test_runner.py exists from previous steps
if test_runner_available:
    try: from .test_runner import TestRunnerTool
    except ImportError: logging.warning("test_runner.py exists but failed import?"); test_runner_available=False

# --- End Tool Imports ---


# AVAILABLE_TOOLS maps tool names (strings) to the actual tool classes.
AVAILABLE_TOOLS = {
    "view": ViewTool,
    "edit": EditTool,
    "ls": ListTool,
    "grep": GrepTool,
    "glob": GlobTool,
}

# Conditionally add tools based on successful imports
if bash_tool_available: AVAILABLE_TOOLS["bash"] = BashTool
if task_complete_available: AVAILABLE_TOOLS["task_complete"] = TaskCompleteTool
if create_dir_available: AVAILABLE_TOOLS["create_directory"] = CreateDirectoryTool
if quality_tools_available:
    AVAILABLE_TOOLS["linter_checker"] = LinterCheckerTool
    AVAILABLE_TOOLS["formatter"] = FormatterTool
if test_runner_available: AVAILABLE_TOOLS["test_runner"] = TestRunnerTool

def get_tool(name: str) -> BaseTool | None:
    """Retrieves an *instance* of the tool class based on its name."""
    tool_class = AVAILABLE_TOOLS.get(name)
    if tool_class:
        try: return tool_class()
        except Exception as e: logging.error(f"Error instantiating tool '{name}': {e}", exc_info=True); return None
    else: logging.warning(f"Tool '{name}' not found in AVAILABLE_TOOLS."); return None

logging.info(f"Tools initialized. Available: {list(AVAILABLE_TOOLS.keys())}")