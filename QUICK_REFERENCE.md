# AI Bash - Quick Reference Card

## 🚀 Installation (3 Steps)

```bash
# 1. Navigate to project
cd /path/to/ai-bash

# 2. Run setup
chmod +x setup.sh && ./setup.sh

# 3. Configure API key
nano .env  # Set GEMINI_API_KEY
```

---

## 💡 Basic Usage

```bash
# Start AI Bash
ai

# Start with sudo (for system commands)
sudo ai

# Exit
ai> exit
```

---

## 📝 Example Commands

### ✅ Safe Commands (Will Execute)

```
ai> install nginx
ai> find files larger than 500MB
ai> list all running services
ai> show disk usage
ai> create a backup of /etc/nginx
ai> list all files modified today
```

### ❌ Blocked Commands (Will Reject)

```
ai> delete everything
ai> format the hard drive
ai> shutdown the system
ai> remove all files in root
```

---

## 📂 Project Files

```
ai-bash/
├── cli.py              # Main program
├── llm_gemini.py       # AI interface
├── system_detect.py    # OS detection
├── safety.py           # Safety checks
├── executor.py         # Command execution
├── prompts.py          # AI prompts
├── test_suite.py       # Tests
├── setup.sh            # Installer
└── [docs]              # Documentation
```

---

## 🧪 Testing

```bash
# Run all tests
python3 test_suite.py

# Test individual modules
python3 system_detect.py
python3 safety.py
python3 executor.py
```

---

## ⚙️ Configuration

### API Key (Required)

```bash
# Option 1: .env file
echo "GEMINI_API_KEY=your-key" > .env

# Option 2: Environment variable
export GEMINI_API_KEY='your-key'
```

### Change LLM Model

Edit `llm_gemini.py`:
```python
model_name="models/gemini-1.5-flash"  # Faster
# or
model_name="models/gemini-1.5-pro"    # Smarter
```

---

## 🛠️ Troubleshooting

### "GEMINI_API_KEY not found"
```bash
export GEMINI_API_KEY='your-key-here'
# or edit .env file
```

### "command not found: ai"
```bash
./setup.sh  # Re-run installer
```

### Permission denied
```bash
sudo ai  # Run with sudo
```

---

## 🔒 Safety Features

1. **LLM Refusal** - AI trained to reject dangerous requests
2. **Pattern Blocking** - Regex blocks known dangerous commands
3. **Path Protection** - System directories protected
4. **User Confirmation** - Always asks before executing
5. **Timeout** - Commands killed after 30 seconds

---

## 📚 Documentation

- **PROJECT_README.md** - Full project overview
- **INSTALLATION.md** - Detailed setup guide
- **ARCHITECTURE.md** - Technical design
- **CHECKLIST.md** - Development phases
- **PROJECT_STRUCTURE.md** - Visual diagrams

---

## 🎯 Design Principles

✓ Command generator, NOT chatbot  
✓ Single-line output only  
✓ Always requires confirmation  
✓ Distribution-aware (Ubuntu, CentOS, etc.)  
✓ Safety over convenience  
✓ Visible execution  

---

## 🔄 Common Workflows

### Install Package
```
ai> install docker
→ apt install -y docker.io (Ubuntu)
→ dnf install -y docker (CentOS)
Execute? [y/N]: y
```

### Find Files
```
ai> find log files larger than 100MB
→ find /var/log -type f -size +100M
Execute? [y/N]: y
```

### Check System
```
ai> show memory usage
→ free -h
Execute? [y/N]: y
```

---

## 📞 Help & Support

- **Check docs**: Read INSTALLATION.md
- **Run tests**: `python3 test_suite.py`
- **View errors**: Check terminal output
- **Report bugs**: File GitHub issue

---

## ⚠️ Safety Reminders

- Always review commands before approving
- Test in safe environments first
- Keep backups of important data
- Use sudo only when necessary
- Safety validation is not foolproof

---

## 🚀 Quick Commands Reference

| Natural Language | Generated Command |
|-----------------|-------------------|
| install nginx | `apt install -y nginx` |
| update packages | `apt update` |
| find large files | `find / -type f -size +500M` |
| check disk space | `df -h` |
| list services | `systemctl list-units --type=service` |
| show processes | `ps aux` |
| check memory | `free -h` |
| network status | `ip addr show` |

---

## 🎓 Tips

1. **Be Specific** - "install nginx" vs "install web server"
2. **Check Output** - Always review suggested commands
3. **Start Simple** - Test with safe commands first
4. **Use Sudo** - Only when needed for system operations
5. **Read Errors** - Pay attention to blocked commands

---

*AI Bash - Natural Language to Linux Commands*  
*Safe • Fast • Distribution-Aware*
