#!/bin/bash
# AI Bash Installation Script
# Sets up the ai command for global use

set -e

echo "╔═══════════════════════════════════════════╗"
echo "║       AI Bash Installation Script         ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "✗ Please do NOT run this script as root"
    echo "  Run: ./setup.sh"
    echo "  You will be prompted for sudo password when needed"
    exit 1
fi

# Check Python installation
echo "→ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed"
    echo "  Install Python 3.8 or higher and try again"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "  ✓ Found Python $PYTHON_VERSION"

# Check pip installation
echo "→ Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo "✗ pip3 is not installed"
    echo "  Install pip and try again"
    exit 1
fi
echo "  ✓ pip3 found"

# Get installation directory
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo ""
echo "→ Installation directory: $INSTALL_DIR"

# Create virtual environment
echo ""
echo "→ Creating Python virtual environment..."
cd "$INSTALL_DIR"
python3 -m venv venv
echo "  ✓ Virtual environment created"

# Activate virtual environment and install dependencies
echo "→ Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
deactivate
echo "  ✓ Dependencies installed"

# Create wrapper script
echo ""
echo "→ Creating ai command wrapper..."
WRAPPER_SCRIPT="/usr/local/bin/ai"

sudo tee "$WRAPPER_SCRIPT" > /dev/null << EOF
#!/bin/bash
# AI Bash Wrapper Script
# Activates venv and runs cli.py

cd "$INSTALL_DIR"
source venv/bin/activate
python3 cli.py "\$@"
deactivate
EOF

# Make wrapper executable
sudo chmod +x "$WRAPPER_SCRIPT"
echo "  ✓ Wrapper script created at $WRAPPER_SCRIPT"

# Check for API key
echo ""
echo "→ Checking for Gemini API key..."
if [ -f "$INSTALL_DIR/.env" ]; then
    if grep -q "GEMINI_API_KEY=your-api-key-here" "$INSTALL_DIR/.env" || \
       grep -q "GEMINI_API_KEY=$" "$INSTALL_DIR/.env"; then
        echo "  ⚠ API key not configured in .env file"
        API_KEY_SET=false
    else
        echo "  ✓ API key found in .env file"
        API_KEY_SET=true
    fi
else
    echo "  ⚠ No .env file found"
    cp "$INSTALL_DIR/.env.example" "$INSTALL_DIR/.env"
    echo "  ✓ Created .env file from template"
    API_KEY_SET=false
fi

# Check environment variable
if [ -z "$GEMINI_API_KEY" ]; then
    if [ "$API_KEY_SET" = false ]; then
        echo ""
        echo "╔═══════════════════════════════════════════╗"
        echo "║       API KEY CONFIGURATION NEEDED        ║"
        echo "╚═══════════════════════════════════════════╝"
        echo ""
        echo "You need to set your Gemini API key to use AI Bash."
        echo ""
        echo "Option 1 - Set in .env file (recommended):"
        echo "  1. Get your API key from: https://makersuite.google.com/app/apikey"
        echo "  2. Edit $INSTALL_DIR/.env"
        echo "  3. Replace 'your-api-key-here' with your actual API key"
        echo ""
        echo "Option 2 - Set as environment variable:"
        echo "  export GEMINI_API_KEY='your-api-key-here'"
        echo "  (Add to ~/.bashrc or ~/.zshrc for persistence)"
        echo ""
    fi
else
    echo "  ✓ GEMINI_API_KEY environment variable is set"
fi

# Final instructions
echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║       Installation Complete! ✓            ║"
echo "╚═══════════════════════════════════════════╝"
echo ""
echo "Usage:"
echo "  ai              # Start AI Bash (requires sudo on Linux)"
echo "  sudo ai         # Start with elevated privileges"
echo ""
echo "Example:"
echo "  ai> install nginx"
echo "  ai> find files larger than 500MB"
echo "  ai> list all running services"
echo ""
echo "To uninstall:"
echo "  sudo rm /usr/local/bin/ai"
echo "  rm -rf $INSTALL_DIR/venv"
echo ""
