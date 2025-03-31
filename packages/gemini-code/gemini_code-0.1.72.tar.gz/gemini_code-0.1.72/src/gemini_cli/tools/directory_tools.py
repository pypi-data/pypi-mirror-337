"""
Tools for directory operations.
"""
import os
import logging
from .base import BaseTool

log = logging.getLogger(__name__)

class CreateDirectoryTool(BaseTool):
    """Tool to create a new directory."""
    name = "create_directory"
    description = "Creates a new directory, including any necessary parent directories."

    def execute(self, dir_path: str) -> str:
        """
        Creates a directory.

        Args:
            dir_path: The path of the directory to create.

        Returns:
            A success or error message.
        """
        try:
            # Basic path safety
            if ".." in dir_path.split(os.path.sep):
                 log.warning(f"Attempted to access parent directory in create_directory path: {dir_path}")
                 return f"Error: Invalid path '{dir_path}'. Cannot access parent directories."

            target_path = os.path.abspath(os.path.expanduser(dir_path))
            log.info(f"Attempting to create directory: {target_path}")

            if os.path.exists(target_path):
                if os.path.isdir(target_path):
                    log.warning(f"Directory already exists: {target_path}")
                    return f"Directory already exists: {dir_path}"
                else:
                    log.error(f"Path exists but is not a directory: {target_path}")
                    return f"Error: Path exists but is not a directory: {dir_path}"

            os.makedirs(target_path, exist_ok=True) # exist_ok=True handles race conditions slightly better
            log.info(f"Successfully created directory: {target_path}")
            return f"Successfully created directory: {dir_path}"

        except OSError as e:
            log.error(f"Error creating directory '{dir_path}': {e}", exc_info=True)
            return f"Error creating directory: {str(e)}"
        except Exception as e:
            log.error(f"Unexpected error creating directory '{dir_path}': {e}", exc_info=True)
            return f"Error creating directory: {str(e)}"