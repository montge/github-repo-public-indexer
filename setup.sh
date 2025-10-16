#!/bin/bash
# Quick setup script for GitHub Organization Repository Indexer

set -e

echo "🚀 GitHub Organization Repository Indexer - Setup"
echo "=================================================="
echo

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✓ Dependencies installed"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo
    echo "⚠️  Please edit .env and add your GitHub token:"
    echo "   GITHUB_TOKEN=ghp_your_token_here"
    echo "   GITHUB_ORG=your-org-name"
    echo
else
    echo "✓ .env file already exists"
fi

# Make collect_repos.py executable
chmod +x collect_repos.py
echo "✓ Made collect_repos.py executable"

echo
echo "✅ Setup complete!"
echo
echo "Next steps:"
echo "1. Edit .env with your GitHub token and organization name"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python collect_repos.py --summary"
echo
echo "For help: python collect_repos.py --help"
echo "For usage guide: see USAGE.md"
