"""
File operation tools.
"""

import os
import glob
import re
import logging
from pathlib import Path
from .base import BaseTool

log = logging.getLogger(__name__)

class ViewTool(BaseTool):
    """Tool to view file contents."""
    name = "view"
    description = "View the contents of a specific file."

    def execute(self, file_path: str, offset: int | None = None, limit: int | None = None) -> str:
        """
        View the contents of a file.

        Args:
            file_path: Path to the file to view.
            offset: Line number to start reading from (1-based index, optional).
            limit: Maximum number of lines to read (optional).
        Returns:
            The content of the file with line numbers, or an error message.
        """
        try:
            # Basic path safety (prevent walking up directory tree significantly)
            # This is a simple check, more robust sandboxing might be needed for security
            if ".." in file_path.split(os.path.sep):
                 log.warning(f"Attempted to access parent directory in path: {file_path}")
                 return f"Error: Invalid file path '{file_path}'. Cannot access parent directories."

            path = os.path.abspath(os.path.expanduser(file_path))
            # Optional: Add further checks to ensure path stays within project root if needed

            log.info(f"Viewing file: {path} (Offset: {offset}, Limit: {limit})")
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            start_index = 0
            if offset is not None:
                # Convert 1-based offset to 0-based index
                start_index = max(0, int(offset) - 1)

            end_index = len(lines)
            if limit is not None:
                end_index = start_index + max(0, int(limit))

            content_slice = lines[start_index:end_index]

            # Format with line numbers (relative to original file)
            result = []
            for i, line in enumerate(content_slice):
                original_line_num = start_index + i + 1
                result.append(f"{original_line_num:6d} {line}")

            return "".join(result) if result else "(File is empty or slice resulted in no lines)"

        except FileNotFoundError:
            log.warning(f"File not found for view: {file_path}")
            return f"Error: File not found: {file_path}"
        except IsADirectoryError:
             log.warning(f"Attempted to view a directory: {file_path}")
             return f"Error: Cannot view a directory: {file_path}"
        except Exception as e:
            log.error(f"Error viewing file '{file_path}': {e}", exc_info=True)
            return f"Error viewing file: {str(e)}"

# --- Updated EditTool ---
class EditTool(BaseTool):
    """Tool to edit/create files. Can overwrite, replace strings, or create new."""
    name = "edit"
    description = "Edit a file: create it with content, replace its entire content, replace the first occurrence of a specific string, or delete the first occurrence of a specific string."

    def execute(self, file_path: str, content: str | None = None, old_string: str | None = None, new_string: str | None = None) -> str:
        """
        Edits or creates a file.

        Args:
            file_path: Path to the file to edit or create.
            content: The full content to write to the file. If provided, this overwrites the entire file or creates a new file. Mutually exclusive with old_string/new_string.
            old_string: The exact string to find for replacement. Required if replacing/deleting specific text.
            new_string: The string to replace old_string with. Use an empty string ('') to delete old_string. Required if old_string is provided.

        Returns:
            A success message or an error message.
        """
        try:
            # Basic path safety
            if ".." in file_path.split(os.path.sep):
                 log.warning(f"Attempted to access parent directory in path: {file_path}")
                 return f"Error: Invalid file path '{file_path}'. Cannot access parent directories."

            path = os.path.abspath(os.path.expanduser(file_path))
            log.info(f"Editing file: {path}")

            # Ensure directory exists
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                 log.info(f"Creating directory: {directory}")
                 os.makedirs(directory, exist_ok=True)

            # --- Mode 1: Create or Overwrite with 'content' ---
            if content is not None:
                if old_string is not None or new_string is not None:
                    log.warning("Both 'content' and 'old_string/new_string' provided. Prioritizing 'content'.")
                    # return "Error: Cannot use 'content' and 'old_string'/'new_string' arguments together." # Option: stricter error

                log.info(f"Writing content (length: {len(content)}) to {path}.")
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"Successfully wrote content to {file_path}."

            # --- Mode 2: Replace specific string ---
            elif old_string is not None and new_string is not None:
                log.info(f"Replacing '{old_string[:50]}...' with '{new_string[:50]}...' in {path}.")
                if not os.path.exists(path):
                    log.warning(f"File not found for replacement: {path}")
                    return f"Error: File not found to perform replacement: {file_path}"

                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        original_content = f.read()
                except Exception as read_err:
                     log.error(f"Error reading file for replacement '{path}': {read_err}", exc_info=True)
                     return f"Error reading file for replacement: {read_err}"

                if old_string not in original_content:
                    log.warning(f"old_string not found in {path}")
                    return f"Error: The specified text `old_string` was not found in the file {file_path}."

                # Replace only the first occurrence
                new_content = original_content.replace(old_string, new_string, 1)

                if new_content == original_content:
                    # This case might happen if old_string == new_string
                     log.warning(f"Replacement resulted in no change to the file content for {path}.")
                     # Still report success as the operation technically completed
                     # return f"Warning: Replacement of '{old_string}' with '{new_string}' did not change file content."


                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                if new_string == "":
                     return f"Successfully deleted first occurrence of specified text in {file_path}."
                else:
                     return f"Successfully replaced first occurrence of specified text in {file_path}."

            # --- Mode 3: Create empty file (if no content, no old/new) ---
            elif old_string is None and new_string is None and content is None:
                 log.info(f"Creating empty file: {path}")
                 # Check if it already exists - if so, do nothing? Or truncate? Let's truncate.
                 with open(path, 'w', encoding='utf-8') as f:
                      f.write("") # Ensure it's empty
                 return f"Successfully created or ensured empty file {file_path}."

            else:
                # Invalid combination of arguments
                log.error(f"Invalid argument combination for edit tool: content={content}, old={old_string}, new={new_string}")
                return "Error: Invalid argument combination for edit. Use 'content' OR ('old_string' and 'new_string')."


        except IsADirectoryError:
             log.warning(f"Attempted to edit a directory: {file_path}")
             return f"Error: Cannot edit a directory: {file_path}"
        except Exception as e:
            log.error(f"Error editing file '{file_path}': {e}", exc_info=True)
            return f"Error editing file: {str(e)}"
# --- End Updated EditTool ---


class ListTool(BaseTool):
    """Tool to list files in a directory."""
    name = "ls"
    description = "List files and directories in a given path."

    def execute(self, path: str = '.', ignore: str | None = None) -> str:
        """
        List files in a directory.

        Args:
            path: Directory path to list (default: '.').
            ignore: Glob patterns to ignore (comma-separated). Optional.
        Returns:
            Formatted list of files and directories or error message.
        """
        try:
            if ".." in path.split(os.path.sep):
                 log.warning(f"Attempted to access parent directory in ls path: {path}")
                 return f"Error: Invalid path '{path}'. Cannot access parent directories."

            target_path = os.path.abspath(os.path.expanduser(path))
            log.info(f"Listing directory: {target_path} (Ignore: {ignore})")

            if not os.path.isdir(target_path):
                 return f"Error: Path is not a directory: {path}"

            entries = os.listdir(target_path)
            dirs = sorted([entry + '/' for entry in entries if os.path.isdir(os.path.join(target_path, entry))])
            files = sorted([entry for entry in entries if not os.path.isdir(os.path.join(target_path, entry))])

            ignore_patterns = []
            if ignore:
                ignore_patterns = [p.strip() for p in ignore.split(',') if p.strip()]

            def should_ignore(entry_name, patterns):
                for pattern in patterns:
                    if glob.fnmatch.fnmatch(entry_name.rstrip('/'), pattern): # Match against name without trailing /
                        return True
                return False

            # Filter based on ignore patterns
            filtered_dirs = [d for d in dirs if not should_ignore(d, ignore_patterns)]
            filtered_files = [f for f in files if not should_ignore(f, ignore_patterns)]

            result = []
            if filtered_dirs:
                result.append("Directories:")
                result.extend([f"  {d}" for d in filtered_dirs])
            if filtered_files:
                if filtered_dirs: result.append("") # Add separator
                result.append("Files:")
                result.extend([f"  {f}" for f in filtered_files])

            if not filtered_dirs and not filtered_files:
                return "(Directory is empty or all entries ignored)"

            return "\n".join(result)

        except FileNotFoundError:
            log.warning(f"Directory not found for ls: {path}")
            return f"Error: Directory not found: {path}"
        except Exception as e:
            log.error(f"Error listing directory '{path}': {e}", exc_info=True)
            return f"Error listing directory: {str(e)}"


class GrepTool(BaseTool):
    """Tool to search for patterns in files."""
    name = "grep"
    description = "Search for a pattern (regex) in files within a directory."

    def execute(self, pattern: str, path: str = '.', include: str | None = None) -> str:
        """
        Search for patterns in files.

        Args:
            pattern: Regex pattern to search for.
            path: Directory path to search within (default: '.'). Optional.
            include: Glob pattern for files to include (e.g., '*.py', '*.txt'). Searches all files if omitted. Optional.
        Returns:
            Matching lines with file/line number, or a message if no matches found/error.
        """
        try:
            if ".." in path.split(os.path.sep):
                 log.warning(f"Attempted to access parent directory in grep path: {path}")
                 return f"Error: Invalid path '{path}'. Cannot access parent directories."

            target_path = os.path.abspath(os.path.expanduser(path))
            log.info(f"Grepping in {target_path} for pattern '{pattern}' (Include: {include})")

            if not os.path.isdir(target_path):
                 return f"Error: Path is not a directory: {path}"

            try:
                regex = re.compile(pattern)
            except re.error as re_err:
                log.warning(f"Invalid regex pattern provided: {pattern} - {re_err}")
                return f"Error: Invalid regex pattern: {pattern} ({re_err})"

            results = []
            files_to_search = []

            # Determine files to search
            if include:
                # Use glob with recursive=True if pattern suggests it (**)
                recursive = '**' in include
                glob_pattern = os.path.join(target_path, include)
                log.debug(f"Using glob pattern: {glob_pattern}, recursive={recursive}")
                try:
                     files_to_search = glob.glob(glob_pattern, recursive=recursive)
                except Exception as glob_err:
                     log.error(f"Error during glob operation '{glob_pattern}': {glob_err}", exc_info=True)
                     return f"Error finding files with include pattern: {glob_err}"
            else:
                # Walk the directory if no include pattern
                log.debug(f"Walking directory tree: {target_path}")
                for root, _, filenames in os.walk(target_path):
                    # Simple check to avoid descending into obviously irrelevant hidden dirs like .git, .venv, __pycache__
                    # This could be made more robust or configurable
                    basename = os.path.basename(root)
                    if basename.startswith('.') or basename == '__pycache__':
                         continue # Skip hidden dirs and pycache

                    for filename in filenames:
                        # Maybe skip certain file types by extension? For now, include all.
                        files_to_search.append(os.path.join(root, filename))

            log.info(f"Found {len(files_to_search)} files to search.")
            files_searched_count = 0
            matches_found_count = 0

            for file_path in files_to_search:
                # Ensure we are only dealing with files, not dirs returned by glob
                if not os.path.isfile(file_path):
                     continue

                files_searched_count += 1
                try:
                    # Try reading with utf-8, fallback or skip if fails
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for i, line in enumerate(f, 1):
                            if regex.search(line):
                                matches_found_count += 1
                                rel_path = os.path.relpath(file_path, target_path)
                                # Prepend ./ if it's in the immediate directory for clarity
                                if os.path.dirname(rel_path) == '':
                                    rel_path = f"./{rel_path}"
                                results.append(f"{rel_path}:{i}: {line.rstrip()}")
                                # Optional: Limit number of results per file or overall?
                                if matches_found_count > 500: # Safety break
                                     log.warning("Reached grep match limit (500). Stopping search.")
                                     results.append("--- Match limit reached ---")
                                     break # Stop searching this file
                except OSError as read_err:
                     log.debug(f"Could not read file during grep: {file_path} - {read_err}")
                     continue # Skip files that can't be read
                except Exception as e:
                     log.warning(f"Unexpected error grepping file {file_path}: {e}", exc_info=True)
                     continue # Skip problematic files

                if matches_found_count > 500: break # Stop searching other files

            log.info(f"Searched {files_searched_count} files, found {matches_found_count} matches.")

            if results:
                return "\n".join(results)
            else:
                return f"No matches found for pattern: {pattern}"

        except Exception as e:
            log.error(f"Error during grep operation: {e}", exc_info=True)
            return f"Error searching files: {str(e)}"


class GlobTool(BaseTool):
    """Tool to find files using glob patterns."""
    name = "glob"
    description = "Find files/directories matching specific glob patterns recursively."

    def execute(self, pattern: str, path: str = '.') -> str:
        """
        Find files/directories matching a glob pattern.

        Args:
            pattern: Glob pattern to match (e.g., '**/*.py', 'docs/**/*.md').
            path: Base directory path to search within (default: '.'). Optional.
        Returns:
            Newline-separated list of matching relative paths or error message.
        """
        try:
            if ".." in path.split(os.path.sep):
                 log.warning(f"Attempted to access parent directory in glob path: {path}")
                 return f"Error: Invalid path '{path}'. Cannot access parent directories."

            target_path = os.path.abspath(os.path.expanduser(path))
            log.info(f"Globbing in {target_path} for pattern '{pattern}'")

            if not os.path.isdir(target_path):
                 return f"Error: Path is not a directory: {path}"

            # Ensure the pattern is joined correctly with the target path
            search_pattern = os.path.join(target_path, pattern)
            # Use recursive=True always, let the pattern ('**') control recursion depth
            matches = glob.glob(search_pattern, recursive=True)

            if matches:
                # Make paths relative to the original target_path for cleaner output
                relative_matches = sorted([os.path.relpath(m, target_path) for m in matches])
                # Prepend ./ if needed
                formatted_matches = [f"./{m}" if os.path.dirname(m) == '' else m for m in relative_matches]
                return "\n".join(formatted_matches)
            else:
                return f"No files or directories found matching pattern: {pattern}"

        except Exception as e:
            log.error(f"Error finding files with glob: {e}", exc_info=True)
            return f"Error finding files: {str(e)}"

# Other tools like BashTool, TestRunnerTool would go in their respective files
# (system_tools.py, test_runner.py) and inherit from BaseTool