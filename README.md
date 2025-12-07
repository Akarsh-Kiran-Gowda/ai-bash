# AI Bash — Natural Language to Linux Command Engine

## ✅ PROJECT STATUS: FULLY IMPLEMENTED & TESTED

**🎉 All development phases complete! Ready for installation and testing.**

📂 **Implementation Location:** `ai-bash/` directory  
📊 **Test Results:** ALL TESTS PASSING ✓  
📝 **Documentation:** 6 comprehensive guides included  
🔒 **Safety:** Multi-layer validation implemented  

### Quick Start

```bash
cd ai-bash
./setup.sh
nano .env  # Add your Gemini API key
ai         # Launch AI Bash
```

### Project Files (17 total)

**Core Application (6 files)**
- ✅ `cli.py` - Main terminal interface
- ✅ `llm_gemini.py` - Gemini API integration  
- ✅ `system_detect.py` - OS/kernel detection
- ✅ `safety.py` - Safety validation
- ✅ `executor.py` - Command execution
- ✅ `prompts.py` - LLM prompts

**Testing & Setup (4 files)**
- ✅ `test_suite.py` - Automated tests (ALL PASSING)
- ✅ `setup.sh` - Installation script
- ✅ `requirements.txt` - Dependencies
- ✅ `.env.example` - API key template

**Documentation (6 files)**
- ✅ `PROJECT_README.md` - Complete overview
- ✅ `ARCHITECTURE.md` - Technical design
- ✅ `INSTALLATION.md` - Setup guide
- ✅ `IMPLEMENTATION_SUMMARY.md` - Completion report
- ✅ `PROJECT_STRUCTURE.md` - Visual diagrams
- ✅ `QUICK_REFERENCE.md` - Command reference
- ✅ `CHECKLIST.md` - Development checklist

**See below for original requirements specification.**

---

## Original Project Goal

Build a Linux terminal application that starts with:

```bash
sudo ai
```

and launches an AI-powered Bash interface that:

Accepts natural language commands

Translates them into safe, distro-aware shell commands

Shows the command for user confirmation

Executes only after approval

Initial version will use Gemini API for rapid prototyping.
Later, the LLM backend will be replaced with a local LLM (Ollama).

This project must behave like a shell tool, not a chatbot.

Core Requirements
Convert natural language → single-line Bash command

Detect Linux distribution and kernel

Generate commands compatible with:

Ubuntu / Debian

CentOS / RHEL / Rocky / Alma

Enforce strict safety rules

Never auto-execute without user verification

System Environment Detection (Python)
The application must detect kernel and distro at startup and pass it to the LLM.

python
Copy code
import platform
import subprocess

def get_system_context():
    kernel = platform.release()
    distro = "unknown"

    try:
        distro = subprocess.check_output(
            ["bash", "-c", "source /etc/os-release && echo $ID"],
            text=True
        ).strip()
    except:
        pass

    pkg_manager = "unknown"
    if distro in ["ubuntu", "debian"]:
        pkg_manager = "apt"
    elif distro in ["centos", "rhel", "rocky", "almalinux"]:
        pkg_manager = "yum/dnf"

    return {
        "kernel": kernel,
        "distro": distro,
        "pkg_manager": pkg_manager
    }
This context must be dynamically injected into the LLM system prompt.

GEMINI SYSTEM PROMPT (CRITICAL)
This is the core intelligence of the project.

Use this prompt exactly as written as the Gemini system instruction.

csharp
Copy code
You are an AI-powered Linux shell command generator.

You do NOT chat.
You do NOT explain.
You ONLY output shell commands or a refusal message.

Your task:
Convert natural language requests into SAFE, SINGLE-LINE Linux shell commands
that are valid for the given system environment.

================ SYSTEM ENVIRONMENT ================
OS Distribution : {distro}
Kernel Version  : {kernel}
Package Manager : {pkg_manager}
Shell           : bash
====================================================

MANDATORY RULES (STRICT):
1. Output ONLY the command — no markdown, no explanation, no commentary.
2. Generate ONLY ONE command per request.
3. Command MUST be compatible with the detected distribution.
4. NEVER use commands not supported by the distro.
   - Ubuntu/Debian → apt
   - CentOS/RHEL   → yum or dnf
5. NEVER invent binaries or flags.

SAFETY RULES (CRITICAL):
- NEVER generate destructive commands without confirmation.
  Forbidden examples include:
  rm -rf /
  mkfs.*
  dd if=/dev/*
  shutdown now
- NEVER delete system directories.
- NEVER modify bootloader, kernel, or disk partitions.
- If the request is dangerous or unclear, respond with:
  ERROR: Unsafe or ambiguous request

EXECUTION RULES:
- Prefer non-recursive, least-privilege commands.
- Use absolute paths where applicable.
- Avoid sudo unless explicitly required.
- Assume the command will be shown to the user for approval before execution.

SPECIAL CASES:
- If the intent is to "change directory", output:
  cd <path>
- If the action cannot persist in a child shell, still generate the command.

OUTPUT FORMAT:
- Plain text only
- One line
- No trailing punctuation
User Prompt Format (Gemini Call)
The user message passed to Gemini must be minimal:

sql
Copy code
Convert the following request into a Linux shell command:

<USER_REQUEST>
Example:

sql
Copy code
Convert the following request into a Linux shell command:
list all open ports and listening services
Expected Behavioral Examples
Input
install nginx

Ubuntu

nginx
Copy code
apt install -y nginx
CentOS

nginx
Copy code
dnf install -y nginx
Input
clear all system cache and free RAM

makefile
Copy code
ERROR: Unsafe or ambiguous request
Input
find files larger than 500MB in home directory

arduino
Copy code
find /home -type f -size +500M
Input
move into /var/log directory

bash
Copy code
cd /var/log
Gemini API Usage (Python)
python
Copy code
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel(
    model_name="models/gemini-1.5-pro",
    system_instruction=SYSTEM_PROMPT.format(**system_context)
)

response = model.generate_content(user_input)
command = response.text.strip()
Execution Model
User enters natural language

AI outputs a suggested command

Command is displayed to the user

User explicitly confirms

Command is executed via subprocess.run()

⚠️ Never auto-execute
⚠️ Never suppress visibility

Project Structure
bash
Copy code
ai-bash/
├── cli.py               # terminal loop
├── llm_gemini.py        # Gemini integration
├── system_detect.py     # OS & kernel detection
├── safety.py            # blocklists & validation
├── executor.py          # command execution
├── prompts.py           # system prompt
└── README.md
Design Philosophy
This is not a chatbot

This is a command-generation engine

Refusal is better than unsafe execution

Explicit > implicit

Visible > automated