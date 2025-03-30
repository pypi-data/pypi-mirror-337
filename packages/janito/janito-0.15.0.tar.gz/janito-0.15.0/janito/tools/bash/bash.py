from typing import Optional
from typing import Tuple
import threading
import platform
import re
import queue
import signal
import time
from janito.config import get_config
from janito.tools.usage_tracker import get_tracker
from janito.tools.rich_console import console, print_info

# Import the appropriate implementation based on the platform
if platform.system() == "Windows":
    from janito.tools.bash.win_persistent_bash import PersistentBash
else:
    from janito.tools.bash.unix_persistent_bash import PersistentBash

# Global instance of PersistentBash to maintain state between calls
_bash_session = None
_session_lock = threading.RLock()  # Use RLock to allow reentrant locking
_current_bash_thread = None
_command_interrupted = False

def _execute_bash_command(command, result_queue):
    """
    Execute a bash command in a separate thread.
    
    Args:
        command: The bash command to execute
        result_queue: Queue to store the result
    """
    global _bash_session, _command_interrupted
    
    try:
        # Execute the command - output will be printed to console in real-time
        output = _bash_session.execute(command)
        
        # Put the result in the queue if the command wasn't interrupted
        if not _command_interrupted:
            result_queue.put((output, False))
    except Exception as e:
        # Handle any exceptions that might occur
        error_message = f"Error executing bash command: {str(e)}"
        console.print(error_message, style="red bold")
        result_queue.put((error_message, True))

def _keyboard_interrupt_handler(signum, frame):
    """
    Handle keyboard interrupt (Ctrl+C) by setting the interrupt flag.
    """
    global _command_interrupted
    _command_interrupted = True
    console.print("\n[bold red]Command interrupted by user (Ctrl+C)[/bold red]")
    
    # Restore the default signal handler
    signal.signal(signal.SIGINT, original_sigint_handler)

def bash_tool(command: str, restart: Optional[bool] = False) -> Tuple[str, bool]:
    """
    Execute a bash command using a persistent Bash session.
    The appropriate implementation (Windows or Unix) is selected based on the detected platform.
    When in ask mode, only read-only commands are allowed.
    Output is printed to the console in real-time as it's received.
    Command runs in a background thread, allowing Ctrl+C to interrupt just the command.
    
    Args:
        command: The bash command to execute
        restart: Whether to restart the bash session
        
    Returns:
        A tuple containing (output message, is_error flag)
    """
    # Import console for printing output in real-time
    from janito.tools.rich_console import console, print_info
    
    # Only print command if not in trust mode
    if not get_config().trust_mode:
        print_info(f"{command}", "Bash Run")
    
    global _bash_session, _current_bash_thread, _command_interrupted, original_sigint_handler
    _command_interrupted = False
    
    # Check if in ask mode and if the command might modify files
    if get_config().ask_mode:
        # List of potentially modifying commands
        modifying_patterns = [
            r'\brm\b', r'\bmkdir\b', r'\btouch\b', r'\becho\b.*[>\|]', r'\bmv\b', r'\bcp\b',
            r'\bchmod\b', r'\bchown\b', r'\bsed\b.*-i', r'\bawk\b.*[>\|]', r'\bcat\b.*[>\|]',
            r'\bwrite\b', r'\binstall\b', r'\bapt\b', r'\byum\b', r'\bpip\b.*install',
            r'\bnpm\b.*install', r'\bdocker\b', r'\bkubectl\b.*apply', r'\bgit\b.*commit',
            r'\bgit\b.*push', r'\bgit\b.*merge', r'\bdd\b'
        ]
        
        # Check if command matches any modifying pattern
        for pattern in modifying_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return ("Cannot execute potentially modifying commands in ask mode. Use --ask option to disable modifications.", True)
    
    with _session_lock:
        # Initialize or restart the session if needed
        if _bash_session is None or restart:
            if _bash_session is not None:
                _bash_session.close()
            # Get GitBash path from config (None means auto-detect)
            gitbash_path = get_config().gitbash_path
            _bash_session = PersistentBash(bash_path=gitbash_path)
        
        try:
            # Create a queue to get the result from the thread
            result_queue = queue.Queue()
            
            # Save the original SIGINT handler
            original_sigint_handler = signal.getsignal(signal.SIGINT)
            
            # Set our custom SIGINT handler
            signal.signal(signal.SIGINT, _keyboard_interrupt_handler)
            
            # Create and start the thread
            _current_bash_thread = threading.Thread(
                target=_execute_bash_command,
                args=(command, result_queue)
            )
            _current_bash_thread.daemon = True
            _current_bash_thread.start()
            
            # Wait for the thread to complete or for an interrupt
            while _current_bash_thread.is_alive() and not _command_interrupted:
                _current_bash_thread.join(0.1)  # Check every 100ms
            
            # If the command was interrupted, return a message
            if _command_interrupted:
                # Restore the original signal handler
                signal.signal(signal.SIGINT, original_sigint_handler)
                return ("Command was interrupted by Ctrl+C", True)
            
            # Get the result from the queue
            output, is_error = result_queue.get(timeout=1)
            
            # Restore the original signal handler
            signal.signal(signal.SIGINT, original_sigint_handler)
            
            # Track bash command execution
            get_tracker().increment('bash_commands')
            
            # Return the output
            return output, is_error
            
        except Exception as e:
            # Handle any exceptions that might occur
            error_message = f"Error executing bash command: {str(e)}"
            console.print(error_message, style="red bold")
            
            # Restore the original signal handler
            signal.signal(signal.SIGINT, original_sigint_handler)
            
            return error_message, True
