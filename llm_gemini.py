"""
Gemini API integration for AI Bash.
Handles communication with Google's Gemini LLM.
"""

import os
import google.generativeai as genai
from prompts import get_system_prompt, get_user_prompt
from safety import sanitize_output


class GeminiCommandGenerator:
    """
    Wrapper for Gemini API to generate Linux shell commands.
    """
    
    def __init__(self, system_context, api_key=None):
        """
        Initialize Gemini command generator.
        
        Args:
            system_context (dict): System detection context
            api_key (str, optional): Gemini API key. If None, reads from env var.
        """
        self.system_context = system_context
        
        # Get API key from parameter or environment
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Create model with system instruction
        system_prompt = get_system_prompt(system_context)
        self.model = genai.GenerativeModel(
            model_name="gemini-pro",
            system_instruction=system_prompt
        )
    
    def generate_command(self, user_request):
        """
        Generate a shell command from natural language request.
        
        Args:
            user_request (str): Natural language command request
            
        Returns:
            str: Generated shell command (or ERROR message)
        """
        try:
            # Format user prompt
            user_prompt = get_user_prompt(user_request)
            
            # Generate command
            response = self.model.generate_content(user_prompt)
            command = response.text.strip()
            
            # Sanitize output (remove markdown, extra whitespace)
            command = sanitize_output(command)
            
            return command
            
        except Exception as e:
            return f"ERROR: Failed to generate command - {str(e)}"


if __name__ == "__main__":
    # Test the Gemini integration
    from system_detect import get_system_context
    
    print("Testing Gemini Command Generator")
    print("=" * 50)
    
    # Get system context
    context = get_system_context()
    print(f"System: {context['distro']} ({context['pkg_manager']})")
    print()
    
    # Initialize generator
    try:
        generator = GeminiCommandGenerator(context)
        
        # Test requests
        test_requests = [
            "list all files in current directory",
            "install nginx",
            "find files larger than 500MB in home directory",
        ]
        
        for request in test_requests:
            print(f"Request: {request}")
            command = generator.generate_command(request)
            print(f"Command: {command}")
            print()
            
    except ValueError as e:
        print(f"Error: {e}")
        print("Set GEMINI_API_KEY environment variable to test.")
