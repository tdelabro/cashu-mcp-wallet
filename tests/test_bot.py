#!/usr/bin/env python3
"""
Test script for Cashu MCP Wallet Telegram Bot

This script tests various message lengths and scenarios to ensure
the bot handles long messages correctly.
"""

import asyncio
import os
import random
import string
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("TEST_CHAT_ID")  # Optional: for automated testing

def generate_test_message(length: int, char_type: str = "mixed") -> str:
    """Generate test messages of specified length."""
    if char_type == "hex":
        # Generate hex-like string (like Cashu tokens)
        chars = "0123456789abcdef"
    elif char_type == "ascii":
        chars = string.ascii_letters + string.digits + " "
    else:
        # Mixed characters including emojis and special chars
        chars = string.ascii_letters + string.digits + " " + "🚀💰💎🔥⚡🎯"
    
    return ''.join(random.choice(chars) for _ in range(length))

async def test_message_lengths():
    """Test different message lengths."""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found in environment variables")
        return
    
    bot = Bot(token=BOT_TOKEN)
    
    # Test scenarios
    test_cases = [
        (100, "Short message"),
        (1000, "Medium message"),
        (5000, "Long message (>4k)"),
        (15000, "Very long message (>15k)"),
        (25000, "Extremely long message (>25k)"),
    ]
    
    print("🧪 Starting message length tests...")
    
    for length, description in test_cases:
        print(f"\n📝 Testing: {description} ({length} characters)")
        
        # Generate test message
        test_message = generate_test_message(length, "hex")
        
        try:
            # Send test message
            await bot.send_message(
                chat_id=CHAT_ID or "me",  # Send to self if no chat_id specified
                text=f"🧪 Test: {description}\n\n{test_message}"
            )
            print(f"✅ Sent {length} character message successfully")
            
            # Wait a bit between tests
            await asyncio.sleep(2)
            
        except Exception as e:
            print(f"❌ Error sending {length} character message: {e}")

async def test_special_characters():
    """Test messages with special characters and emojis."""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found in environment variables")
        return
    
    bot = Bot(token=BOT_TOKEN)
    
    special_messages = [
        "🚀 Cashu MCP Wallet Bot Test 🚀",
        "💰 Testing with emojis: 💎🔥⚡🎯",
        "Test with accented characters: áéíóú ñ ç",
        "Test with unicode: 🌍🌎🌏 🏦💳",
        "Mixed content: Hello 123 🚀 Cashu token: abc123def456",
    ]
    
    print("\n🎨 Testing special characters and emojis...")
    
    for message in special_messages:
        try:
            await bot.send_message(
                chat_id=CHAT_ID or "me",
                text=f"🎨 Special chars test:\n{message}"
            )
            print(f"✅ Sent special message: {message[:30]}...")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"❌ Error sending special message: {e}")

async def test_cashu_like_tokens():
    """Test with Cashu-like token strings."""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found in environment variables")
        return
    
    bot = Bot(token=BOT_TOKEN)
    
    # Generate Cashu-like tokens (long hex strings)
    cashu_tokens = [
        generate_test_message(1000, "hex"),
        generate_test_message(5000, "hex"),
        generate_test_message(15000, "hex"),
    ]
    
    print("\n💎 Testing Cashu-like tokens...")
    
    for i, token in enumerate(cashu_tokens, 1):
        try:
            await bot.send_message(
                chat_id=CHAT_ID or "me",
                text=f"💎 Cashu Token Test #{i} ({len(token)} chars):\n\n{token}"
            )
            print(f"✅ Sent Cashu-like token #{i} ({len(token)} characters)")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error sending Cashu token #{i}: {e}")

async def main():
    """Run all tests."""
    print("🤖 Cashu MCP Wallet Bot - Test Suite")
    print("=" * 50)
    
    if not BOT_TOKEN:
        print("❌ Please set BOT_TOKEN in your .env file")
        print("💡 Copy env.example to .env and add your bot token")
        return
    
    print(f"✅ Bot token found: {BOT_TOKEN[:10]}...")
    
    if CHAT_ID:
        print(f"✅ Test chat ID: {CHAT_ID}")
    else:
        print("ℹ️  No TEST_CHAT_ID set - tests will be sent to yourself")
    
    try:
        # Run tests
        await test_message_lengths()
        await test_special_characters()
        await test_cashu_like_tokens()
        
        print("\n🎉 All tests completed!")
        print("\n📋 Next steps:")
        print("1. Check your Telegram for the test messages")
        print("2. Verify that long messages are properly chunked")
        print("3. Test the /test_long command in the bot")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
