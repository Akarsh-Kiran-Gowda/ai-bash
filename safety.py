"""
Safety validation module for AI Bash.
Implements blocklist and validation for dangerous commands.
"""

import re


# Dangerous command patterns that should never be executed
DANGEROUS_PATTERNS = [
    r'rm\s+-rf\s+/(?:\s|$)',  # rm -rf / (exact)
    r'rm\s+-fr\s+/(?:\s|$)',  # rm -fr / (exact)
    r'rm\s+-rf\s+/\*',        # rm -rf /*
    r'rm\s+-fr\s+/\*',        # rm -fr /*
    r'mkfs\.',                # mkfs.* (filesystem formatting)
    r'dd\s+if=/dev/',         # dd with device files
    r'shutdown',              # shutdown commands
    r'reboot',                # reboot commands
    r'halt',                  # halt commands
    r'poweroff',              # poweroff commands
    r'init\s+[06]',           # init 0 or init 6
    r':\(\)\s*\{',            # fork bomb pattern
    r'chmod\s+.*777\s+/',     # chmod 777 on root (any order)
    r'chown\s+-R.*\s+/(?:\s|$)',  # chown on root
]

# System directories that should never be deleted or formatted
PROTECTED_PATHS = [
    '/bin', '/boot', '/dev', '/etc', '/lib', '/lib64',
    '/proc', '/root', '/sbin', '/sys', '/usr', '/var'
]


def is_dangerous_command(command):
    """
    Check if a command matches dangerous patterns.
    
    Args:
        command (str): The shell command to validate
        
    Returns:
        bool: True if command is dangerous, False otherwise
    """
    command = command.strip().lower()
    
    # Check against dangerous patterns
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    
    # Check for operations on protected paths
    for path in PROTECTED_PATHS:
        # Check for deletion of protected paths
        if re.search(rf'rm\s+.*{re.escape(path)}(?:\s|$)', command):
            return True
        # Check for formatting protected paths
        if re.search(rf'mkfs.*{re.escape(path)}', command):
            return True
    
    return False


def validate_command(command):
    """
    Validate a command for safety.
    
    Args:
        command (str): The shell command to validate
        
    Returns:
        tuple: (is_safe, message) where is_safe is bool and message is explanation
    """
    if not command or not command.strip():
        return False, "Empty command received"
    
    # Check if command starts with ERROR (from LLM)
    if command.strip().startswith("ERROR:"):
        return False, command.strip()
    
    # Check against dangerous patterns
    if is_dangerous_command(command):
        return False, "ERROR: Unsafe or ambiguous request"
    
    return True, "Command validated successfully"


def sanitize_output(output):
    """
    Remove markdown formatting and extra whitespace from LLM output.
    
    Args:
        output (str): Raw output from LLM
        
    Returns:
        str: Cleaned command
    """
    # Remove markdown code blocks
    output = re.sub(r'```(?:bash|sh|shell)?\n?', '', output)
    output = re.sub(r'```', '', output)
    
    # Remove backticks
    output = output.replace('`', '')
    
    # Strip whitespace
    output = output.strip()
    
    return output


if __name__ == "__main__":
    # Test cases
    test_commands = [
        "apt install -y nginx",
        "rm -rf /",
        "find /home -type f -size +500M",
        "shutdown now",
        "cd /var/log",
        "mkfs.ext4 /dev/sda1",
        "ERROR: Unsafe or ambiguous request"
    ]
    
    print("Safety Validation Tests:")
    print("-" * 50)
    for cmd in test_commands:
        is_safe, msg = validate_command(cmd)
        status = "✓ SAFE" if is_safe else "✗ BLOCKED"
        print(f"{status}: {cmd}")
        if not is_safe:
            print(f"  Reason: {msg}")
        print()
