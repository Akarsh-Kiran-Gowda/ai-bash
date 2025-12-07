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
        
        # Store system prompt to prepend to user messages
        self.system_prompt = get_system_prompt(system_context)
        
        # Try to find an available model
        available_model = self._get_available_model()
        
        # Create model without system instruction (for compatibility)
        self.model = genai.GenerativeModel(model_name=available_model)
    
    def _get_available_model(self):
        """
        Find the best available Gemini model for the API key.
        
        Returns:
            str: Model name to use
        """
        try:
            # List all available models
            available = []
            for m in genai.list_models():
                if "generateContent" in m.supported_generation_methods:
                    available.append(m.name)
            
            # Preference order (newer models first)
            preferred = [
                "models/gemini-2.5-flash",
                "models/gemini-2.5-pro",
                "models/gemini-flash-latest",
                "models/gemini-pro-latest",
                "models/gemini-1.5-flash",
                "models/gemini-1.5-pro", 
                "models/gemini-pro"
            ]
            
            # Return first match (keep the full model name)
            for model in preferred:
                if model in available:
                    return model
            
            # Fallback to first available
            if available:
                return available[0]
                
        except Exception:
            pass
        
        # Ultimate fallback
        return "gemini-pro"
    
    def generate_command(self, user_request):
        """
        Generate a shell command from natural language request.
        
        Args:
            user_request (str): Natural language command request
            
        Returns:
            str: Generated shell command (or ERROR message)
        """
        try:
            # Format user prompt with system prompt prepended
            user_prompt = get_user_prompt(user_request)
            full_prompt = f"{self.system_prompt}\n\n{user_prompt}"
            
            # Generate command
            response = self.model.generate_content(full_prompt)
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
