#!/usr/bin/env python3
"""
Setup script for Cashu MCP Wallet Telegram Bot

This script helps with initial setup and configuration.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Set up environment file."""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("ℹ️  .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ env.example file not found")
        return False
    
    try:
        # Copy example file
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        print("✅ Created .env file from template")
        print("📝 Please edit .env and add your bot token")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def get_bot_token():
    """Get bot token from user."""
    print("\n🤖 Bot Token Setup")
    print("=" * 30)
    print("1. Open Telegram and search for @BotFather")
    print("2. Send /newbot command")
    print("3. Choose a name for your bot")
    print("4. Choose a username ending in 'bot'")
    print("5. Copy the token provided")
    print()
    
    token = input("Enter your bot token: ").strip()
    
    if not token:
        print("❌ No token provided")
        return False
    
    if not token.count(':') == 1:
        print("❌ Invalid token format. Should be like: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
        return False
    
    # Update .env file
    try:
        with open(".env", "r") as f:
            content = f.read()
        
        content = content.replace("your_telegram_bot_token_here", token)
        
        with open(".env", "w") as f:
            f.write(content)
        
        print("✅ Bot token saved to .env file")
        return True
    except Exception as e:
        print(f"❌ Failed to save token: {e}")
        return False

def test_bot_connection():
    """Test if the bot can connect to Telegram."""
    print("\n🔗 Testing bot connection...")
    
    try:
        from dotenv import load_dotenv
        from telegram import Bot
        
        load_dotenv()
        token = os.getenv("BOT_TOKEN")
        
        if not token:
            print("❌ No bot token found in .env file")
            return False
        
        bot = Bot(token=token)
        me = bot.get_me()
        print(f"✅ Bot connected successfully!")
        print(f"🤖 Bot name: {me.first_name}")
        print(f"👤 Username: @{me.username}")
        print(f"🆔 Bot ID: {me.id}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to bot: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Cashu MCP Wallet Telegram Bot Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Get bot token if .env is empty
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if "your_telegram_bot_token_here" in content:
                if not get_bot_token():
                    sys.exit(1)
    
    # Test connection
    if not test_bot_connection():
        print("\n❌ Setup incomplete. Please check your bot token.")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the bot: python telegram_bot.py")
    print("2. Test with: python test_bot.py")
    print("3. Send /start to your bot in Telegram")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()
