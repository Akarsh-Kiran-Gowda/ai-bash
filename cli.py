#!/usr/bin/env python3
"""
AI Bash - Natural Language to Linux Command Engine
Main CLI interface.

Usage:
    sudo ai
"""

import sys
import os
from system_detect import get_system_context
from llm_gemini import GeminiCommandGenerator
from safety import validate_command
from executor import get_user_confirmation, execute_command, display_result


def print_banner():
    """Display the AI Bash banner."""
    banner = """
╔═══════════════════════════════════════════╗
║          AI Bash - Command Engine         ║
║    Natural Language → Shell Commands      ║
╚═══════════════════════════════════════════╝
"""
    print(banner)


def print_system_info(context):
    """Display detected system information."""
    print(f"System: {context['distro']} | Kernel: {context['kernel']} | PM: {context['pkg_manager']}")
    print("Type 'exit' or 'quit' to exit\n")


def main():
    """Main CLI loop for AI Bash."""
    try:
        # Display banner
        print_banner()
        
        # Detect system context
        print("Detecting system environment...")
        system_context = get_system_context()
        print_system_info(system_context)
        
        # Initialize Gemini command generator
        try:
            generator = GeminiCommandGenerator(system_context)
        except ValueError as e:
            print(f"✗ Error: {e}")
            print("\nPlease set your Gemini API key:")
            print("  export GEMINI_API_KEY='your-api-key-here'")
            sys.exit(1)
        
        # Main command loop
        while True:
            try:
                # Get user input
                user_input = input("\nai> ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("Goodbye!")
                    break
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Generate command from natural language
                print("Generating command...")
                command = generator.generate_command(user_input)
                
                # Validate command safety
                is_safe, message = validate_command(command)
                
                if not is_safe:
                    print(f"\n✗ {message}")
                    continue
                
                # Get user confirmation
                if get_user_confirmation(command):
                    print("Executing...")
                    success, output, error = execute_command(command)
                    display_result(success, output, error)
                else:
                    print("Execution cancelled")
                    
            except KeyboardInterrupt:
                print("\n\nUse 'exit' to quit")
                continue
            except EOFError:
                print("\nGoodbye!")
                break
                
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
