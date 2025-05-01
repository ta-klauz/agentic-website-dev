"""
Helper utilities for the agentic website development system.
"""
import subprocess
import time
import socket
from typing import Tuple, Optional

def wait_for_server(port: int, process: subprocess.Popen, timeout: float = 10.0) -> Tuple[bool, Optional[str]]:
    """
    Waits for a server to become available at localhost:port within 'timeout' seconds.
    Also checks if the process has exited with an error.
    
    Args:
        port: The port number to check
        process: The subprocess.Popen object representing the server process
        timeout: Maximum time to wait in seconds
        
    Returns:
        Tuple of (success, error_message)
    """
    endtime = time.time() + timeout
    error_output = None
    
    while time.time() < endtime:
        # Check if process has exited with an error
        if process.poll() is not None:
            # Process ended - get error output
            stdout, stderr = process.communicate()
            error_output = stderr.decode('utf-8') if stderr else (stdout.decode('utf-8') if stdout else "Unknown error")
            return False, error_output
            
        try:
            # Try to establish a connection to the server
            s = socket.create_connection(('localhost', port), timeout=1)
            s.close()
            return True, None
        except OSError:
            time.sleep(0.1)  # wait a bit before trying again
    
    # Timeout reached, check if process is still running
    if process.poll() is not None:
        stdout, stderr = process.communicate()
        error_output = stderr.decode('utf-8') if stderr else (stdout.decode('utf-8') if stdout else "Unknown error")
    
    return False, error_output or "Server did not respond within timeout period"

def terminate_process(process: subprocess.Popen, timeout: int = 3) -> None:
    """
    Safely terminates a process with timeout.
    
    Args:
        process: The subprocess.Popen object to terminate
        timeout: Time to wait for normal termination before killing
    """
    if process.poll() is None:  # Process is still running
        process.terminate()
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait() 