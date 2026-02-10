#!/bin/bash
# Installation script for Client Conduct Auditor plugin

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║         CLIENT CONDUCT AUDITOR - Installation                ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Found Python $PYTHON_VERSION"

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Make auditor.py executable
echo ""
echo "🔧 Making auditor.py executable..."
chmod +x auditor.py

# Check for API key
echo ""
echo "🔑 Checking for Anthropic API key..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY environment variable not set"
    echo ""
    echo "To set your API key:"
    echo "  export ANTHROPIC_API_KEY='sk-ant-...'"
    echo ""
    echo "Or add to your shell profile (~/.bashrc or ~/.zshrc):"
    echo "  echo \"export ANTHROPIC_API_KEY='sk-ant-...'\" >> ~/.zshrc"
    echo ""
else
    echo "✅ API key found"
fi

# Check for SOP file
echo ""
echo "📄 Checking for SOP file..."
SOP_PATH="/Users/weipengzhuo/Downloads/special delinquent sop.md"
if [ -f "$SOP_PATH" ]; then
    echo "✅ SOP file found at: $SOP_PATH"
else
    echo "⚠️  SOP file not found at default location: $SOP_PATH"
    echo "You can specify a custom path using --sop flag"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║         ✅ Installation Complete!                            ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Usage:"
echo "  python3 auditor.py /path/to/pdf_folder"
echo ""
echo "For help:"
echo "  python3 auditor.py --help"
echo ""
