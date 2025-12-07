# AI Bash Installation & Usage Guide

## Prerequisites

- **Linux System**: Ubuntu, Debian, CentOS, RHEL, Rocky, or AlmaLinux
- **Python**: Version 3.8 or higher
- **Bash Shell**: Standard Linux shell
- **Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Installation

### 1. Clone or Download the Repository

```bash
cd /path/to/ai-bash
```

### 2. Run the Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Create a Python virtual environment
- Install required dependencies
- Create the `ai` command wrapper in `/usr/local/bin/ai`
- Set up configuration files

### 3. Configure Your API Key

**Option 1: Using .env file (Recommended)**

```bash
# Edit the .env file
nano .env

# Replace the placeholder with your actual API key
GEMINI_API_KEY=your-actual-api-key-here
```

**Option 2: Using Environment Variable**

```bash
# Add to ~/.bashrc or ~/.zshrc
export GEMINI_API_KEY='your-actual-api-key-here'

# Reload your shell configuration
source ~/.bashrc
```

### 4. Verify Installation

```bash
ai --help
```

## Usage

### Starting AI Bash

```bash
# Regular mode
ai

# With sudo privileges (for system commands)
sudo ai
```

### Example Session

```
╔═══════════════════════════════════════════╗
║          AI Bash - Command Engine         ║
║    Natural Language → Shell Commands      ║
╚═══════════════════════════════════════════╝

System: ubuntu | Kernel: 5.15.0-generic | PM: apt
Type 'exit' or 'quit' to exit

ai> install nginx
Generating command...

→ Suggested command:
  apt install -y nginx

Execute this command? [y/N]: y
Executing...
[nginx installation output]

ai> find all log files larger than 100MB
Generating command...

→ Suggested command:
  find /var/log -type f -size +100M

Execute this command? [y/N]: y
Executing...
/var/log/syslog.1
/var/log/kern.log.1

ai> delete everything in root directory
Generating command...

✗ ERROR: Unsafe or ambiguous request

ai> exit
Goodbye!
```

## Command Examples

### Safe Commands (Will Execute)

1. **Package Management**
   ```
   ai> install nginx
   ai> update all packages
   ai> remove apache2
   ```

2. **File Operations**
   ```
   ai> find files larger than 500MB in home directory
   ai> list all files modified today
   ai> create a backup of /etc/nginx
   ```

3. **System Information**
   ```
   ai> show disk usage
   ai> list all running services
   ai> check memory usage
   ```

4. **Directory Navigation**
   ```
   ai> move into /var/log directory
   ai> go to home directory
   ```

### Dangerous Commands (Will Be Blocked)

These requests will be rejected with an error:

```
ai> delete all files in root
✗ ERROR: Unsafe or ambiguous request

ai> format the hard drive
✗ ERROR: Unsafe or ambiguous request

ai> shutdown the system
✗ ERROR: Unsafe or ambiguous request
```

## Configuration

### Changing LLM Model

Edit `llm_gemini.py` and change the model name:

```python
self.model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",  # Faster, cheaper
    # or
    model_name="models/gemini-1.5-pro",    # More capable
    system_instruction=system_prompt
)
```

### Adjusting Command Timeout

Edit `executor.py`:

```python
result = subprocess.run(
    [shell, "-c", command],
    capture_output=True,
    text=True,
    timeout=60  # Change from 30 to 60 seconds
)
```

### Adding Custom Safety Rules

Edit `safety.py` and add patterns to `DANGEROUS_PATTERNS`:

```python
DANGEROUS_PATTERNS = [
    r'rm\s+-rf\s+/',
    r'your-custom-pattern',
    # ... more patterns
]
```

## Troubleshooting

### "GEMINI_API_KEY not found"

**Solution**: Set your API key in `.env` file or as an environment variable:

```bash
export GEMINI_API_KEY='your-key-here'
```

### "bash: ai: command not found"

**Solution**: Run the setup script again or manually add to PATH:

```bash
./setup.sh
# or
export PATH="/usr/local/bin:$PATH"
```

### "Permission denied" errors

**Solution**: Run with sudo for system-level commands:

```bash
sudo ai
```

### Command timeout errors

**Solution**: Increase timeout in `executor.py` or break request into smaller commands

### Wrong distribution detected

**Solution**: Check `/etc/os-release` file exists and contains proper `ID` field

## Uninstallation

To remove AI Bash:

```bash
# Remove the command wrapper
sudo rm /usr/local/bin/ai

# Remove the virtual environment (optional)
rm -rf /path/to/ai-bash/venv

# Remove the entire directory (optional)
rm -rf /path/to/ai-bash
```

## Advanced Usage

### Running Tests

```bash
cd /path/to/ai-bash
python3 test_suite.py
```

### Testing Individual Modules

```bash
# Test system detection
python3 system_detect.py

# Test safety validation
python3 safety.py

# Test command executor
python3 executor.py

# Test Gemini integration (requires API key)
python3 llm_gemini.py
```

### Using as a Python Module

```python
from system_detect import get_system_context
from llm_gemini import GeminiCommandGenerator
from safety import validate_command

# Get system info
context = get_system_context()

# Initialize generator
generator = GeminiCommandGenerator(context)

# Generate command
command = generator.generate_command("list all files")

# Validate
is_safe, message = validate_command(command)
```

## Security Best Practices

1. **Never Disable Safety Checks**: Always keep `safety.py` validation enabled
2. **Review Commands**: Always review suggested commands before approval
3. **Use Sudo Sparingly**: Only use `sudo ai` when necessary
4. **Keep API Key Secret**: Never commit `.env` file to version control
5. **Regular Updates**: Keep dependencies updated for security patches

## Getting Help

- Check the README.md for project overview
- Read ARCHITECTURE.md for technical details
- Review test_suite.py for usage examples
- File issues on the project repository

## Future Enhancements

- [ ] Local LLM support via Ollama
- [ ] Command history and favorites
- [ ] Multi-step command sequences
- [ ] Interactive tutorials
- [ ] Additional distribution support (Arch, Fedora, etc.)
