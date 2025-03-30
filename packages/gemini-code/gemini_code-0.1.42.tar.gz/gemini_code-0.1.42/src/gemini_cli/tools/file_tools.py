"""
File operation tools.
"""

import os
import glob
import re
from pathlib import Path

from .base import BaseTool

class ViewTool(BaseTool):
    """Tool to view file contents."""
    
    name = "view"
    description = "View the contents of a file"
    
    def execute(self, file_path, offset=None, limit=None):
        """
        View the contents of a file.
        
        Args:
            file_path: Path to the file to view
            offset: Line number to start reading from (optional)
            limit: Maximum number of lines to read (optional)
        """
        try:
            path = os.path.expanduser(file_path)
            with open(path, 'r') as f:
                content = f.readlines()
            
            # Apply offset and limit if provided
            if offset:
                offset = int(offset)
                content = content[offset:]
            
            if limit:
                limit = int(limit)
                content = content[:limit]
            
            # Format with line numbers
            result = []
            for i, line in enumerate(content):
                line_num = i + 1
                if offset:
                    line_num += int(offset)
                result.append(f"{line_num:6d} {line}")
            
            return "".join(result)
        
        except FileNotFoundError:
            return f"Error: File not found: {file_path}"
        except Exception as e:
            return f"Error viewing file: {str(e)}"

class EditTool(BaseTool):
    """Tool to edit file contents."""
    
    name = "edit"
    description = "Edit a file by replacing text or create a new file with content"
    
    def execute(self, file_path, old_string=None, new_string=None):
        """
        Edit a file by replacing text or create a new file with content.
        
        Args:
            file_path: Path to the file to edit or create
            old_string: Text to replace (optional when creating new file)
            new_string: Text to replace it with or full content for new file
        """
        try:
            path = os.path.expanduser(file_path)
            
            # Determine if this is a file creation or edit operation
            is_file_creation = not os.path.exists(path) or old_string is None
            
            # Handle file creation
            if is_file_creation:
                try:
                    # Create directory if it doesn't exist
                    directory = os.path.dirname(path)
                    if directory and not os.path.exists(directory):
                        os.makedirs(directory)
                    
                    # Create empty file or file with content
                    with open(path, 'w') as f:
                        if new_string is not None:
                            f.write(new_string)
                    
                    if new_string is None:
                        return f"Successfully created empty file {file_path}"
                    else:
                        return f"Successfully created {file_path} with content"
                except Exception as e:
                    return f"Error creating file: {str(e)}"
            
            # Handle normal editing case (file exists and old_string is provided)
            try:
                # Read the file
                with open(path, 'r') as f:
                    content = f.read()
                
                # If old_string is empty or None, overwrite the entire file
                if old_string == "" or old_string is None:
                    with open(path, 'w') as f:
                        if new_string is not None:
                            f.write(new_string)
                    return f"Successfully overwrote {file_path}"
                
                # Check if old_string exists in the file
                if old_string not in content:
                    return f"Error: The specified text was not found in the file."
                
                # Replace the text
                new_content = content.replace(old_string, new_string, 1)
                
                # Write the file
                with open(path, 'w') as f:
                    f.write(new_content)
                
                return f"Successfully edited {file_path}"
            except Exception as e:
                return f"Error editing file: {str(e)}"
        
        except Exception as e:
            return f"Error: {str(e)}"

class ListTool(BaseTool):
    """Tool to list files in a directory."""
    
    name = "ls"
    description = "List files in a directory"
    
    def execute(self, path='.', ignore=None):
        """
        List files in a directory.
        
        Args:
            path: Directory path to list
            ignore: Glob patterns to ignore (comma-separated)
        """
        try:
            path = os.path.expanduser(path)
            entries = os.listdir(path)
            
            # Sort entries: directories first, then files
            dirs = []
            files = []
            
            for entry in entries:
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    dirs.append(entry + '/')
                else:
                    files.append(entry)
            
            # Sort alphabetically
            dirs.sort()
            files.sort()
            
            # Apply ignore patterns if specified
            if ignore:
                ignore_patterns = ignore.split(',')
                
                for pattern in ignore_patterns:
                    pattern = pattern.strip()
                    dirs = [d for d in dirs if not glob.fnmatch.fnmatch(d, pattern)]
                    files = [f for f in files if not glob.fnmatch.fnmatch(f, pattern)]
            
            # Format the output
            result = []
            if dirs:
                result.append("Directories:")
                for d in dirs:
                    result.append(f"  {d}")
                    
            if files:
                if dirs:
                    result.append("")
                result.append("Files:")
                for f in files:
                    result.append(f"  {f}")
            
            if not dirs and not files:
                result.append("(empty directory)")
            
            return "\n".join(result)
        
        except FileNotFoundError:
            return f"Error: Directory not found: {path}"
        except Exception as e:
            return f"Error listing directory: {str(e)}"

class GrepTool(BaseTool):
    """Tool to search for patterns in files."""
    
    name = "grep"
    description = "Search for patterns in files"
    
    def execute(self, pattern, path='.', include=None):
        """
        Search for patterns in files.
        
        Args:
            pattern: Regex pattern to search for
            path: Directory to search in
            include: File patterns to include (e.g., "*.py")
        """
        try:
            path = os.path.expanduser(path)
            
            # Build the file list
            if include:
                file_pattern = os.path.join(path, include)
                files = glob.glob(file_pattern, recursive=True)
            else:
                files = []
                for root, _, filenames in os.walk(path):
                    for filename in filenames:
                        files.append(os.path.join(root, filename))
            
            # Compile the regex pattern
            regex = re.compile(pattern)
            
            # Search for matches
            results = []
            
            for file_path in sorted(files):
                try:
                    with open(file_path, 'r') as f:
                        for i, line in enumerate(f, 1):
                            if regex.search(line):
                                # Format: file:line_num: line_content
                                rel_path = os.path.relpath(file_path, path)
                                results.append(f"{rel_path}:{i}: {line.rstrip()}")
                except UnicodeDecodeError:
                    # Skip binary files
                    continue
                except Exception:
                    # Skip files with read errors
                    continue
            
            if results:
                return "\n".join(results)
            else:
                return f"No matches found for pattern: {pattern}"
        
        except Exception as e:
            return f"Error searching files: {str(e)}"

class GlobTool(BaseTool):
    """Tool to find files using glob patterns."""
    
    name = "glob"
    description = "Find files using glob patterns"
    
    def execute(self, pattern, path='.'):
        """
        Find files matching a glob pattern.
        
        Args:
            pattern: Glob pattern to match
            path: Directory to search in
        """
        try:
            path = os.path.expanduser(path)
            
            # Find files matching the pattern
            search_pattern = os.path.join(path, pattern)
            matches = glob.glob(search_pattern, recursive=True)
            
            # Sort by modification time (newest first)
            matches.sort(key=os.path.getmtime, reverse=True)
            
            if matches:
                # Format the output
                result = []
                for file_path in matches:
                    rel_path = os.path.relpath(file_path, path)
                    result.append(rel_path)
                
                return "\n".join(result)
            else:
                return f"No files found matching pattern: {pattern}"
        
        except Exception as e:
            return f"Error finding files: {str(e)}"