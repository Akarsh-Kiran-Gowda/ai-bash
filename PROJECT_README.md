# AI Bash - Natural Language to Linux Command Engine

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.8+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

Convert natural language requests into safe, distribution-aware Linux shell commands with AI assistance.

## 🎯 Project Overview

**AI Bash** is a Linux terminal application that translates natural language into executable shell commands. It's designed as a **command-generation engine**, not a chatbot—focused on safety, clarity, and distribution awareness.

```bash
ai> install nginx
→ Suggested command: apt install -y nginx
Execute this command? [y/N]: y
```

### Key Features

✅ **Natural Language Input** - Describe what you want in plain English  
✅ **Distribution-Aware** - Adapts to Ubuntu, Debian, CentOS, RHEL, Rocky, AlmaLinux  
✅ **Safety-First** - Blocks dangerous commands with comprehensive validation  
✅ **Explicit Approval** - Never executes without user confirmation  
✅ **Single-Line Output** - Clean, executable commands (no chatbot fluff)  
✅ **Gemini-Powered** - Uses Google Gemini API (swappable with local LLMs)

## 🚀 Quick Start

### Prerequisites

- Linux system (Ubuntu/Debian/CentOS/RHEL family)
- Python 3.8 or higher
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

```bash
# 1. Clone the repository
cd /path/to/ai-bash

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Configure API key
nano .env
# Replace 'your-api-key-here' with your actual Gemini API key

# 4. Start using AI Bash
ai
# or with sudo for system commands
sudo ai
```

## 📖 Usage Examples

### Safe Commands (Executed)

```bash
ai> install nginx
→ apt install -y nginx

ai> find files larger than 500MB in home directory
→ find /home -type f -size +500M

ai> list all running services
→ systemctl list-units --type=service --state=running

ai> show disk usage in human readable format
→ df -h
```

### Dangerous Commands (Blocked)

```bash
ai> delete everything in root directory
✗ ERROR: Unsafe or ambiguous request

ai> format the hard drive
✗ ERROR: Unsafe or ambiguous request

ai> shutdown the system
✗ ERROR: Unsafe or ambiguous request
```

## 🏗️ Architecture

```
User Input (Natural Language)
    ↓
System Detection (distro, kernel, pkg_manager)
    ↓
LLM Generation (Gemini API with system context)
    ↓
Safety Validation (blocklist, pattern matching)
    ↓
User Confirmation (display & approve)
    ↓
Command Execution (subprocess)
    ↓
Result Display
```

### Project Structure

```
ai-bash/
├── cli.py              # Main terminal loop
├── llm_gemini.py       # Gemini API integration
├── system_detect.py    # OS & kernel detection
├── safety.py           # Safety validation & blocklists
├── executor.py         # Command execution engine
├── prompts.py          # LLM system prompts
├── test_suite.py       # Automated tests
├── setup.sh            # Installation script
├── requirements.txt    # Python dependencies
├── .env.example        # API key template
├── README.md           # This file
├── ARCHITECTURE.md     # Technical documentation
└── INSTALLATION.md     # Detailed setup guide
```

## 🔒 Safety Features

AI Bash implements multiple layers of safety:

1. **LLM-Level Safety**: System prompt instructs Gemini to refuse dangerous requests
2. **Pattern Blocking**: Regex patterns block destructive commands
3. **Protected Paths**: System directories are protected from deletion/modification
4. **User Confirmation**: Every command requires explicit approval
5. **Timeout Protection**: Commands timeout after 30 seconds

### Blocked Command Patterns

- `rm -rf /` (and variations)
- `mkfs.*` (filesystem formatting)
- `dd if=/dev/*` (disk overwrite)
- `shutdown`, `reboot`, `halt`
- Fork bombs and malicious scripts
- Operations on protected system paths

## 🧪 Testing

Run the automated test suite:

```bash
cd ai-bash
python3 test_suite.py
```

Expected output:
```
✓ PASSED: System Detection
✓ PASSED: Safety Validation
✓ PASSED: Dangerous Patterns
✓ PASSED: README Examples
```

## 📋 Requirements

- **Python**: 3.8+
- **Dependencies**: `google-generativeai` (installed via setup.sh)
- **OS**: Linux (Ubuntu, Debian, CentOS, RHEL, Rocky, AlmaLinux)
- **Shell**: Bash
- **API**: Gemini API key (free tier available)

## 🔧 Configuration

### API Key Setup

**Option 1: .env file (Recommended)**
```bash
cp .env.example .env
nano .env
# Set: GEMINI_API_KEY=your-actual-key
```

**Option 2: Environment Variable**
```bash
export GEMINI_API_KEY='your-actual-key'
# Add to ~/.bashrc for persistence
```

### Advanced Configuration

See [INSTALLATION.md](INSTALLATION.md) for:
- Changing LLM models
- Adjusting command timeouts
- Adding custom safety rules
- Testing individual modules

## 🛣️ Roadmap

### Current Implementation (v1.0)
- [x] Gemini API integration
- [x] Distribution detection (Ubuntu, Debian, CentOS, RHEL)
- [x] Safety validation layer
- [x] Command execution with confirmation
- [x] Automated test suite

### Planned Features
- [ ] **Local LLM Support** (Ollama integration)
- [ ] Command history and favorites
- [ ] Multi-step command sequences
- [ ] Interactive mode with context
- [ ] Additional distributions (Arch, Fedora, openSUSE)
- [ ] Plugin system for extensions

## 📚 Documentation

- **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation and troubleshooting
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical design and LLM backend swap guide
- **[test_suite.py](test_suite.py)** - Test examples and validation

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

1. **LLM Backends**: Add support for Ollama, OpenAI, Claude, etc.
2. **Safety Rules**: Enhance pattern detection and validation
3. **Distribution Support**: Add more Linux distributions
4. **Testing**: Expand test coverage
5. **Documentation**: Improve guides and examples

## ⚖️ License

This project is released under the MIT License.

## 🙏 Acknowledgments

- **Google Gemini** - AI model powering command generation
- **Linux Community** - For the amazing ecosystem
- **Open Source Contributors** - For inspiration and tools

## ⚠️ Disclaimer

**AI Bash is an experimental tool. While safety measures are in place:**

- Always review commands before execution
- Use at your own risk
- Test in safe environments first
- Keep backups of important data
- Safety validation is not foolproof

The developers are not responsible for any damage caused by using this tool.

## 📞 Support

- **Issues**: File bugs or feature requests on GitHub
- **Documentation**: Check INSTALLATION.md and ARCHITECTURE.md
- **Testing**: Run test_suite.py to verify installation

---

**Made with ❤️ for the Linux community**

*Transform your terminal experience with natural language*
