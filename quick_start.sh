#!/bin/bash

# Cashu MCP Wallet Telegram Bot - Quick Start Script

set -e

echo "🚀 Cashu MCP Wallet Telegram Bot - Quick Start"
echo "=============================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Setup environment file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp env.example .env
    echo "⚠️  Please edit .env and add your bot token!"
    echo "💡 You can get a bot token from @BotFather on Telegram"
fi

# Check if bot token is set
if grep -q "your_telegram_bot_token_here" .env; then
    echo ""
    echo "⚠️  IMPORTANT: You need to set your bot token!"
    echo "1. Open Telegram and search for @BotFather"
    echo "2. Send /newbot command"
    echo "3. Follow the instructions to create your bot"
    echo "4. Copy the token and edit .env file"
    echo ""
    echo "After setting the token, run: python telegram_bot.py"
else
    echo "✅ Bot token is configured!"
    echo ""
    echo "🎉 Setup complete! You can now:"
    echo "1. Run the bot: python telegram_bot.py"
    echo "2. Test the bot: python tests/test_bot.py"
    echo "3. Send /start to your bot in Telegram"
fi

echo ""
echo "📚 For more information, see README.md"
