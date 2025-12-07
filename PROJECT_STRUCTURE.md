# AI Bash - Visual Project Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          AI BASH ARCHITECTURE                            │
└─────────────────────────────────────────────────────────────────────────┘

┌───────────────┐
│  User Input   │  "install nginx"
│ (Natural Lang)│
└───────┬───────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────────────┐
│                        CLI.PY - Main Interface                        │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │  • Print banner                                                 │ │
│  │  • Accept natural language input                               │ │
│  │  • Orchestrate all modules                                     │ │
│  │  • Handle exit commands (exit, quit, q)                        │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└───────────────────────────┬───────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│SYSTEM_DETECT │   │  PROMPTS.PY  │   │  SAFETY.PY   │
│    .PY       │   │              │   │              │
├──────────────┤   ├──────────────┤   ├──────────────┤
│• Get kernel  │   │• System      │   │• Dangerous   │
│• Get distro  │   │  prompt      │   │  patterns    │
│• Map pkg mgr │   │• User prompt │   │• Protected   │
│• Return ctx  │   │• Format with │   │  paths       │
│              │   │  context     │   │• Validate    │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       │                  │                  │
       └──────────┬───────┴──────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  LLM_GEMINI.PY  │
         ├─────────────────┤
         │• Init with ctx  │
         │• Call Gemini API│
         │• Get command    │
         │• Sanitize output│
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │   Generated     │  "apt install -y nginx"
         │    Command      │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │   SAFETY.PY     │
         │   Validation    │
         ├─────────────────┤
         │ is_safe = True  │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────────────────┐
         │      EXECUTOR.PY            │
         ├─────────────────────────────┤
         │ → Show command to user      │
         │ → Get confirmation (y/n)    │
         │ → Execute if approved       │
         │ → Display result            │
         └─────────────────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  Command Output │
         └─────────────────┘
```

---

## Module Interactions

```
┌──────────────────────────────────────────────────────────────┐
│                      MODULE DEPENDENCIES                      │
└──────────────────────────────────────────────────────────────┘

cli.py
  ├─→ system_detect.py  (get_system_context)
  ├─→ llm_gemini.py     (GeminiCommandGenerator)
  ├─→ safety.py         (validate_command)
  └─→ executor.py       (get_user_confirmation, execute_command)

llm_gemini.py
  ├─→ prompts.py        (get_system_prompt, get_user_prompt)
  └─→ safety.py         (sanitize_output)

system_detect.py
  └─→ [platform, subprocess]  (no internal dependencies)

safety.py
  └─→ [re]  (no internal dependencies)

executor.py
  └─→ [subprocess]  (no internal dependencies)

prompts.py
  └─→ [none]  (pure string templates)
```

---

## Data Flow Example

```
USER INPUT: "install nginx"
    │
    ▼
SYSTEM DETECTION
    │ {kernel: "5.15.0", distro: "ubuntu", pkg_manager: "apt"}
    ▼
PROMPT FORMATTING
    │ System Prompt + "Convert the following request into a Linux shell command: install nginx"
    ▼
GEMINI API CALL
    │ API Request → Gemini 1.5 Pro
    ▼
RAW OUTPUT
    │ "apt install -y nginx" (or with markdown)
    ▼
SANITIZATION
    │ Remove markdown, strip whitespace → "apt install -y nginx"
    ▼
SAFETY VALIDATION
    │ Check dangerous patterns ✓ SAFE
    │ Check protected paths ✓ SAFE
    ▼
USER CONFIRMATION
    │ Display: "→ Suggested command: apt install -y nginx"
    │ Prompt: "Execute this command? [y/N]:"
    │ User: "y"
    ▼
EXECUTION
    │ subprocess.run(["bash", "-c", "apt install -y nginx"])
    ▼
OUTPUT DISPLAY
    │ [nginx installation logs]
    └─→ Return to prompt
```

---

## Safety Layer Visualization

```
┌──────────────────────────────────────────────────────────────┐
│                    MULTI-LAYER SAFETY                         │
└──────────────────────────────────────────────────────────────┘

Layer 1: LLM System Prompt
┌─────────────────────────────────────────────────────────────┐
│ "NEVER generate destructive commands"                       │
│ "If dangerous or unclear, respond: ERROR: Unsafe request"   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
Layer 2: Regex Pattern Matching
┌─────────────────────────────────────────────────────────────┐
│ • Block: rm -rf /                                           │
│ • Block: mkfs.*, dd if=/dev/*, shutdown, reboot             │
│ • Block: Operations on /bin, /boot, /etc, /usr, etc.       │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
Layer 3: Protected Path Validation
┌─────────────────────────────────────────────────────────────┐
│ Ensure no deletions/modifications to system directories     │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
Layer 4: User Confirmation
┌─────────────────────────────────────────────────────────────┐
│ Display command → Get y/n approval → Execute only if "yes"  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
Layer 5: Timeout Protection
┌─────────────────────────────────────────────────────────────┐
│ Kill execution after 30 seconds                             │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure Tree

```
ai-bash/
├── Core Application
│   ├── cli.py                  # Main entry point
│   ├── llm_gemini.py           # Gemini API interface
│   ├── system_detect.py        # OS detection
│   ├── safety.py               # Safety validation
│   ├── executor.py             # Command execution
│   └── prompts.py              # LLM prompts
│
├── Testing & Validation
│   └── test_suite.py           # Automated tests
│
├── Installation
│   ├── setup.sh                # Installation script
│   ├── requirements.txt        # Python dependencies
│   └── .env.example            # API key template
│
├── Documentation
│   ├── PROJECT_README.md       # Main project docs
│   ├── ARCHITECTURE.md         # Technical design
│   ├── INSTALLATION.md         # Setup guide
│   ├── IMPLEMENTATION_SUMMARY.md  # Completion summary
│   └── PROJECT_STRUCTURE.md    # This file
│
└── Configuration
    ├── .gitignore              # Git exclusions
    └── .env                    # API key (created by user)
```

---

## Component Responsibilities

```
┌─────────────────────────────────────────────────────────────┐
│                  COMPONENT BREAKDOWN                         │
└─────────────────────────────────────────────────────────────┘

CLI.PY (Main Orchestrator)
├─ Display banner and system info
├─ Main terminal loop
├─ Handle user input/output
├─ Coordinate all modules
└─ Error handling & graceful shutdown

SYSTEM_DETECT.PY (Environment Detection)
├─ Detect Linux kernel version
├─ Identify distribution (Ubuntu, CentOS, etc.)
├─ Map to package manager (apt, yum, dnf)
└─ Return context dictionary

PROMPTS.PY (Prompt Management)
├─ Store system prompt template
├─ Store user prompt template
├─ Inject system context
└─ Format prompts for LLM

LLM_GEMINI.PY (AI Interface)
├─ Initialize Gemini API client
├─ Create model with system prompt
├─ Generate commands from natural language
├─ Handle API errors
└─ Return sanitized output

SAFETY.PY (Validation & Protection)
├─ Define dangerous command patterns
├─ Define protected system paths
├─ Validate command safety
├─ Sanitize LLM output (remove markdown)
└─ Return safety status

EXECUTOR.PY (Command Execution)
├─ Display suggested command
├─ Get user confirmation (y/n)
├─ Execute via subprocess if approved
├─ Handle timeouts (30s)
├─ Display results or errors
└─ Never auto-execute

TEST_SUITE.PY (Quality Assurance)
├─ Test system detection
├─ Test safety validation (13 cases)
├─ Test dangerous pattern blocking (11 cases)
├─ Verify README examples
└─ Report pass/fail results
```

---

## LLM Backend Abstraction

```
┌─────────────────────────────────────────────────────────────┐
│              LLM BACKEND SWAP ARCHITECTURE                   │
└─────────────────────────────────────────────────────────────┘

Current Implementation (Gemini)
┌─────────────────────────────────────────┐
│ llm_gemini.py                           │
│ ├─ GeminiCommandGenerator               │
│ │  ├─ __init__(system_context)         │
│ │  └─ generate_command(user_request)   │
│ └─ Uses: google-generativeai library   │
└─────────────────────────────────────────┘

Future Implementation (Ollama)
┌─────────────────────────────────────────┐
│ llm_ollama.py                           │
│ ├─ OllamaCommandGenerator               │
│ │  ├─ __init__(system_context, model)  │
│ │  └─ generate_command(user_request)   │
│ └─ Uses: ollama library                 │
└─────────────────────────────────────────┘

Shared Components (No changes needed)
┌─────────────────────────────────────────┐
│ • prompts.py (system prompt reusable)   │
│ • system_detect.py (universal)          │
│ • safety.py (LLM-independent)           │
│ • executor.py (LLM-independent)         │
│ • cli.py (just change import)           │
└─────────────────────────────────────────┘
```

---

## Execution Flow Timeline

```
t=0ms    User types: "install nginx"
         │
t=10ms   System detection runs
         │ → Kernel: 5.15.0
         │ → Distro: ubuntu
         │ → Package Manager: apt
         │
t=50ms   Prompts formatted with context
         │
t=100ms  Gemini API call initiated
         │
t=1500ms Gemini response received
         │ → "apt install -y nginx"
         │
t=1510ms Output sanitization
         │ → Remove markdown, strip whitespace
         │
t=1520ms Safety validation
         │ → Check dangerous patterns: PASS
         │ → Check protected paths: PASS
         │
t=1530ms Display to user
         │ → "Suggested command: apt install -y nginx"
         │ → "Execute this command? [y/N]:"
         │
t=????   Waiting for user input...
         │
t=5000ms User types "y" and presses Enter
         │
t=5010ms Command execution begins
         │ → subprocess.run(["bash", "-c", "apt install -y nginx"])
         │
t=8000ms Command completes
         │ → nginx installed successfully
         │
t=8010ms Display results
         │ → [installation logs]
         │
t=8020ms Return to prompt
         │ → "ai> "
```

---

## Design Philosophy Visualization

```
┌──────────────────────────────────────────────────────────────┐
│                   DESIGN PRINCIPLES                           │
└──────────────────────────────────────────────────────────────┘

NOT A CHATBOT                    ✓ Single-line command output
    ╳ "Sure! I'd be happy..."    ✓ "apt install -y nginx"
    ╳ "Let me explain..."        ✓ "find /home -type f"
    ╳ Multi-paragraph responses  ✓ Plain executable commands

COMMAND GENERATOR                ✓ Focused on shell commands
    ✓ Natural language → Bash    ✗ General conversation
    ✓ Distribution-aware         ✗ Chat/discussion
    ✓ Single-purpose tool        ✗ Multi-purpose assistant

REFUSAL OVER RISK                ✓ Block dangerous requests
    ✓ "ERROR: Unsafe request"    ✗ Auto-execute anything
    ✓ Conservative validation    ✗ "Trust me" approach
    ✓ Fail secure                ✗ Fail permissive

EXPLICIT APPROVAL                ✓ Always confirm
    ✓ Show command first         ✗ Hidden execution
    ✓ Require y/n                ✗ Assume approval
    ✓ User in control            ✗ AI in control

VISIBLE EXECUTION                ✓ Transparent
    ✓ Display command            ✗ Black box
    ✓ Show output                ✗ Silent operation
    ✓ Report errors              ✗ Suppress failures
```

---

*AI Bash - Transforming natural language into safe, executable Linux commands*
