"""
Utility module for rich console printing in tools.
"""
from rich.console import Console
from rich.text import Text
from typing import Optional
from janito.config import get_config

# Create a shared console instance
console = Console()

def print_info(message: str, title: Optional[str] = None):
    """
    Print an informational message with rich formatting.
    
    Args:
        message: The message to print
        title: Optional title for the panel
    """
    # Skip printing if trust mode is enabled
    if get_config().trust_mode:
        return
    # Map titles to specific icons
    icon_map = {
        # File operations
        "Delete Operation": "🗑️ ",
        "Move Operation": "📦",
        "File Operation": "📄",
        "Directory View": "📁",
        "File View": "📄",
        "File Creation": "📝",
        "Undo Operation": "↩️",
        
        # Search and find operations
        "Text Search": "🔍",
        "Search Results": "📊",
        
        # Web operations
        "Web Fetch": "🌐",
        "Content Extraction": "📰",
        "News Extraction": "📰",
        "Targeted Extraction": "🎯",
        "Content Chunking": "📊",
        "Content Ex": "📰",  # For truncated "Content Extraction" in search results
        
        # Command execution
        "Bash Run": "🔄",
        
        # User interaction
        "Input Instructions": "⌨️",
        
        # Default
        "Info": "ℹ️ ",
    }
    
    # Get the appropriate icon based on title and message content
    icon = "ℹ️ "  # Default icon
    
    # Check for exact matches in the icon map based on title
    if title and title in icon_map:
        icon = icon_map[title]
    else:
        # Check for matching strings in both title and message
        for key, value in icon_map.items():
            # Skip the default "Info" key to avoid too many matches
            if key == "Info":
                continue
                
            # Check if the key appears in both title and message (if title exists)
            if title and key in title and key in message:
                icon = value
                break
                
        # If no match found yet, check for partial matches for str_replace_editor operations
        if title:
            if "Replacing text in file" in title:
                icon = "✏️ "  # Edit icon
            elif "Inserting text in file" in title:
                icon = "➕"  # Plus icon
            elif "Viewing file" in title:
                icon = "📄"  # File icon
            elif "Viewing directory" in title:
                icon = "📁"  # Directory icon
            elif "Creating file" in title:
                icon = "📝"  # Create icon
            elif "Undoing last edit" in title:
                icon = "↩️"  # Undo icon
    
    # Add indentation to all tool messages
    indent = "    "
    text = Text(message)
    if title:
        # Special case for Bash Run commands
        if title == "Bash Run":
            console.print("\n" + "-"*50)
            console.print(f"{indent}{icon} {title}", style="bold white on blue")
            console.print("-"*50)
            console.print(f"{indent}$ {text}", style="white on dark_blue")
            # Make sure we're not returning anything
            return
        else:
            console.print(f"{indent}{icon} {message}", style="blue", end="")
    else:
        console.print(f"{indent}{icon} {text}", style="blue", end="")

def print_success(message: str, title: Optional[str] = None):
    """
    Print a success message with rich formatting.
    
    Args:
        message: The message to print
        title: Optional title for the panel
    """
    # Skip printing if trust mode is enabled
    if get_config().trust_mode:
        return
    text = Text(message)
    if title:
        console.print(f" ✅ {message}", style="green")
    else:
        console.print(f"✅ {text}", style="green")

def print_error(message: str, title: Optional[str] = None):
    """
    Print an error message with rich formatting.
    In trust mode, error messages are suppressed.
    
    Args:
        message: The message to print
        title: Optional title for the panel
    """
    # Skip printing if trust mode is enabled
    if get_config().trust_mode:
        return
        
    text = Text(message)
    
    # Check if message starts with question mark emoji (❓)
    # If it does, use warning styling (yellow) instead of error styling (red)
    starts_with_question_mark = message.startswith("❓")
    
    if starts_with_question_mark:
        # Use warning styling for question mark emoji errors
        # For question mark emoji errors, don't include the title (like "Error")
        # Just print the message with the emoji
        if title == "File View":
            console.print(f"\n {message}", style="yellow")
        else:
            console.print(f"{message}", style="yellow")
    else:
        # Regular error styling
        if title:
            # Special case for File View - print without header
            if title == "File View":
                console.print(f"\n ❌ {message}", style="red")
            # Special case for Search Error
            elif title == "Search Error":
                console.print(f"❌ {message}", style="red")
            else:
                console.print(f"❌ {title} {text}", style="red")
        else:
            console.print(f"\n❌ {text}", style="red")

def print_warning(message: str):
    """
    Print a warning message with rich formatting.
    In trust mode, warning messages are suppressed.
    
    Args:
        message: The message to print
    """
    # Skip printing if trust mode is enabled
    if get_config().trust_mode:
        return
        
    console.print(f"⚠️  {message}", style="yellow")