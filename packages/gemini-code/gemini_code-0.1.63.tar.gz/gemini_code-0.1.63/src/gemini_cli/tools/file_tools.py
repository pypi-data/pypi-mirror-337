class ViewTool(BaseTool):
    """Tool to view specific sections or small files. For large files, use summarize_code."""
    name = "view"
    description = "View specific sections of a file using offset/limit, or view small files entirely. Use summarize_code for large files."

    def execute(self, file_path: str, offset: int | None = None, limit: int | None = None) -> str:
        """
        View specific parts or small files. Suggests summarize_code for large files if no offset/limit.

        Args:
            file_path: Path to the file to view.
            offset: Line number to start reading from (1-based index, optional).
            limit: Maximum number of lines to read (optional).
        Returns:
            The requested content or an error/suggestion message.
        """
        try:
            # Basic path safety
            if ".." in file_path.split(os.path.sep):
                 log.warning(f"Attempted to access parent directory in path: {file_path}")
                 return f"Error: Invalid file path '{file_path}'. Cannot access parent directories."

            path = os.path.abspath(os.path.expanduser(file_path))
            log.info(f"Viewing file: {path} (Offset: {offset}, Limit: {limit})")

            if not os.path.exists(path):
                log.warning(f"File not found for view: {file_path}")
                return f"Error: File not found: {file_path}"
            if not os.path.isfile(path):
                 log.warning(f"Attempted to view a directory: {file_path}")
                 return f"Error: Cannot view a directory: {file_path}"

            # Check size if offset/limit are NOT provided
            if offset is None and limit is None:
                 file_size = os.path.getsize(path)
                 if file_size > MAX_CHARS_FOR_FULL_CONTENT: # Use same threshold as summarizer
                      log.warning(f"File '{file_path}' is large ({file_size} bytes) and no offset/limit provided for view.")
                      return f"Error: File '{file_path}' is large. Use the 'summarize_code' tool for an overview, or 'view' with offset/limit for specific sections."

            # Proceed with reading (potentially whole file if small, or slice if offset/limit)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            start_index = 0
            if offset is not None:
                start_index = max(0, int(offset) - 1)

            end_index = len(lines)
            if limit is not None:
                end_index = start_index + max(0, int(limit))

            content_slice = lines[start_index:end_index]

            result = []
            for i, line in enumerate(content_slice):
                original_line_num = start_index + i + 1
                result.append(f"{original_line_num:6d} {line}")

            # Add prefix for clarity
            prefix = f"--- Content of {file_path} (Lines {start_index+1}-{start_index+len(content_slice)}) ---" if offset is not None or limit is not None else f"--- Full Content of {file_path} ---"
            return prefix + "\n" + "".join(result) if result else f"{prefix}\n(File is empty or slice resulted in no lines)"

        except Exception as e:
            log.error(f"Error viewing file '{file_path}': {e}", exc_info=True)
            return f"Error viewing file: {str(e)}"