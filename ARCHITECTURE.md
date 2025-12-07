# AI Bash - Project Documentation

## Architecture Overview

AI Bash is designed with a modular architecture that separates concerns and allows for easy LLM backend replacement.

## Module Structure

### 1. **system_detect.py** - System Detection Layer
- **Purpose**: Detect Linux distribution, kernel version, and package manager
- **Key Function**: `get_system_context()`
- **Dependencies**: `platform`, `subprocess`
- **Output**: Dictionary with `kernel`, `distro`, `pkg_manager`

### 2. **prompts.py** - Prompt Management
- **Purpose**: Store and format LLM system prompts and user prompts
- **Key Components**:
  - `SYSTEM_PROMPT`: Core intelligence prompt (distro-aware, safety-focused)
  - `USER_PROMPT_TEMPLATE`: Wrapper for user requests
  - `get_system_prompt()`: Inject system context into prompt
  - `get_user_prompt()`: Format user request
- **Reusability**: Designed to work with any LLM backend

### 3. **llm_gemini.py** - LLM Interface (Gemini)
- **Purpose**: Interface with Google Gemini API
- **Key Class**: `GeminiCommandGenerator`
- **Methods**:
  - `__init__()`: Configure API and create model with system prompt
  - `generate_command()`: Convert natural language to shell command
- **Isolation**: Self-contained - can be swapped with `llm_ollama.py`

### 4. **safety.py** - Safety Validation
- **Purpose**: Validate commands before execution
- **Key Functions**:
  - `is_dangerous_command()`: Check against blocklist patterns
  - `validate_command()`: Full safety validation
  - `sanitize_output()`: Clean LLM output (remove markdown)
- **Blocklist Includes**:
  - Destructive commands: `rm -rf /`, `mkfs.*`, `dd if=/dev/*`
  - System control: `shutdown`, `reboot`, `halt`
  - Protected paths: `/bin`, `/boot`, `/etc`, `/usr`, etc.

### 5. **executor.py** - Command Execution
- **Purpose**: Execute validated commands with user confirmation
- **Key Functions**:
  - `get_user_confirmation()`: Display command and get y/n approval
  - `execute_command()`: Run command via subprocess
  - `display_result()`: Show output or errors
- **Safety**: Never auto-executes, always requires confirmation

### 6. **cli.py** - Main CLI Interface
- **Purpose**: Main application loop
- **Flow**:
  1. Detect system context
  2. Initialize LLM generator
  3. Accept natural language input
  4. Generate command
  5. Validate safety
  6. Request confirmation
  7. Execute if approved
- **User Experience**: Terminal-based, not chatbot-like

## Data Flow

```
User Input (Natural Language)
    ↓
System Detection (distro, kernel, pkg_manager)
    ↓
Prompt Formatting (system context injection)
    ↓
LLM Generation (Gemini API)
    ↓
Safety Validation (blocklist, patterns)
    ↓
User Confirmation (display & approve)
    ↓
Command Execution (subprocess)
    ↓
Result Display
```

## LLM Backend Abstraction

The architecture is designed to support multiple LLM backends:

### Current Implementation (Gemini)
- `llm_gemini.py` uses Google Gemini API
- Requires `GEMINI_API_KEY` environment variable
- Model: `gemini-1.5-pro`

### Future Implementation (Ollama)
To swap to Ollama (local LLM):

1. Create `llm_ollama.py` with same interface:
   ```python
   class OllamaCommandGenerator:
       def __init__(self, system_context, model="llama2"):
           # Initialize Ollama client
           pass
       
       def generate_command(self, user_request):
           # Generate command using Ollama
           pass
   ```

2. Update `cli.py` import:
   ```python
   # from llm_gemini import GeminiCommandGenerator
   from llm_ollama import OllamaCommandGenerator as CommandGenerator
   ```

### Shared Components (LLM-agnostic)
- `prompts.py`: System prompt works with any LLM
- `system_detect.py`: System detection is universal
- `safety.py`: Validation independent of LLM
- `executor.py`: Execution independent of LLM

## Security Principles

1. **Never Trust LLM Output**: Always validate through `safety.py`
2. **Explicit Approval**: Always show command and require confirmation
3. **Fail Secure**: Reject ambiguous or dangerous requests
4. **Least Privilege**: Avoid `sudo` unless explicitly requested
5. **Visibility**: Never hide what's being executed

## Installation & Configuration

### Dependencies
- Python 3.8+
- `google-generativeai` package (for Gemini)
- Bash shell (Linux)

### Setup Steps
1. Run `./setup.sh` to install
2. Configure API key in `.env` or environment variable
3. Use `ai` or `sudo ai` to launch

### Environment Variables
- `GEMINI_API_KEY`: Required for Gemini backend
- Future: `OLLAMA_HOST` for Ollama backend

## Extension Points

### Adding New LLM Backends
1. Create `llm_<provider>.py` with `CommandGenerator` class
2. Implement `__init__(system_context)` and `generate_command(user_request)`
3. Update `cli.py` to import new generator
4. Add dependencies to `requirements.txt`

### Enhancing Safety Rules
1. Add patterns to `DANGEROUS_PATTERNS` in `safety.py`
2. Add protected paths to `PROTECTED_PATHS`
3. Implement custom validation logic in `validate_command()`

### Supporting New Distributions
1. Add distro detection in `system_detect.py`
2. Map to package manager (apt, yum, dnf, pacman, etc.)
3. Update system prompt in `prompts.py` if needed

## Testing Strategy

### Manual Testing
- Use examples from README behavioral tests
- Verify distro-specific commands
- Confirm safety rejections

### Unit Testing (Future)
- `test_system_detect.py`: Mock OS detection
- `test_safety.py`: Validate blocklist patterns
- `test_prompts.py`: Check prompt formatting
- Mock LLM responses for integration testing

## Design Philosophy Alignment

✓ **Not a chatbot**: Single-line command output only  
✓ **Command-generation engine**: Focused on shell commands  
✓ **Refusal over risk**: Blocks dangerous operations  
✓ **Explicit approval**: Always requires user confirmation  
✓ **Distro-aware**: Adapts to Ubuntu, CentOS, etc.  
✓ **Visible execution**: Never hides what runs  
✓ **Modular design**: Easy LLM backend swap
