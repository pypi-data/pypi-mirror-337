"""
Replace file tool that overwrites a file with new content.
"""
import os
from typing import Tuple

from janito.tools.decorators import tool
from janito.tools.rich_console import print_info, print_success, print_error
from janito.tools.usage_tracker import track_usage, get_tracker


@tool
@track_usage('files_modified')
def replace_file(file_path: str, new_content: str) -> Tuple[str, bool]:
    """
    Replace an existing file with new content.
    
    Args:
        file_path: Path to the file to replace, relative to the workspace directory
        new_content: New content to write to the file
        
    Returns:
        A tuple containing (message, is_error)
    """
    try:
        print_info(f"Replacing file '{file_path}'", "File Operation")
        
        # Convert relative path to absolute path
        abs_path = os.path.abspath(file_path)
        
        # Check if file exists
        if not os.path.isfile(abs_path):
            error_msg = f"Error: File '{file_path}' does not exist"
            print_error(error_msg, "File Error")
            return error_msg, True
        
        # Read the original content to calculate line delta
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                old_content = f.read()
            
            # Calculate line delta
            old_lines_count = len(old_content.splitlines()) if old_content else 0
            new_lines_count = len(new_content.splitlines()) if new_content else 0
            line_delta = new_lines_count - old_lines_count
            
            # Track line delta
            get_tracker().increment('lines_delta', line_delta)
        except Exception:
            # If we can't read the file, we can't calculate line delta
            pass
            
        # Write new content to the file
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        success_msg = f"Successfully replaced file '{file_path}'"
        print_success(success_msg, "Success")
        return success_msg, False
    except Exception as e:
        error_msg = f"Error replacing file '{file_path}': {str(e)}"
        print_error(error_msg, "Error")
        return error_msg, True