#!/bin/bash
# Setup script for LINE OneDrive AI system

echo "🚀 LINE BOT × OneDrive AI System Setup"
echo "====================================="

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual API keys and configuration"
fi

# Test basic functionality
echo "Testing basic functionality..."
python3 -c "
import sys
sys.path.insert(0, '.')
from config import config
from modules.utils.logger import setup_logging, StructuredLogger
from modules.line_bot.bot_handler import LineBotHandler
from modules.onedrive.client import OneDriveClient
from modules.ai.assistant import AIAssistant

print('✓ All modules imported successfully')
print('✓ System is ready!')
"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: python3 main.py"
echo ""
echo "For development:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run tests: python3 -m pytest tests/"
echo "3. Run linting: black . && flake8"