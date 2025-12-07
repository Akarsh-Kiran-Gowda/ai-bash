"""
Command execution module for AI Bash.
Handles safe execution of validated shell commands.
"""

import subprocess
import shlex


def execute_command(command, shell="bash"):
    """
    Execute a shell command after user confirmation.
    
    Args:
        command (str): The validated shell command to execute
        shell (str): The shell to use (default: bash)
        
    Returns:
        tuple: (success, output, error) where:
            - success (bool): Whether command executed successfully
            - output (str): Standard output from command
            - error (str): Standard error from command
    """
    try:
        # Execute command using bash
        result = subprocess.run(
            [shell, "-c", command],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        success = result.returncode == 0
        output = result.stdout
        error = result.stderr
        
        return success, output, error
        
    except subprocess.TimeoutExpired:
        return False, "", "ERROR: Command timed out after 30 seconds"
    
    except Exception as e:
        return False, "", f"ERROR: Execution failed - {str(e)}"


def get_user_confirmation(command):
    """
    Display command and get user confirmation before execution.
    
    Args:
        command (str): The command to display
        
    Returns:
        bool: True if user confirms, False otherwise
    """
    print(f"\n→ Suggested command:")
    print(f"  {command}")
    print()
    
    while True:
        response = input("Execute this command? [y/N]: ").strip().lower()
        
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no', '']:
            return False
        else:
            print("Please enter 'y' or 'n'")


def display_result(success, output, error):
    """
    Display the execution result to the user.
    
    Args:
        success (bool): Whether command succeeded
        output (str): Standard output
        error (str): Standard error
    """
    if success:
        if output:
            print(output)
        else:
            print("Command executed successfully (no output)")
    else:
        print(f"✗ Command failed")
        if error:
            print(f"Error: {error}")


if __name__ == "__main__":
    # Test execution with a safe command
    test_command = "echo 'Hello from AI Bash'"
    
    print("Testing Command Executor")
    print("=" * 50)
    
    if get_user_confirmation(test_command):
        print("\nExecuting...")
        success, output, error = execute_command(test_command)
        display_result(success, output, error)
    else:
        print("Execution cancelled by user")
