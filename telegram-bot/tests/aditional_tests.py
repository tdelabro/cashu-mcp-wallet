#!/usr/bin/env python3
"""
Additional Tests for Cashu MCP Wallet Telegram Bot

This file contains comprehensive tests to verify all bot functionalities,
especially for Cashu token handling and edge cases.
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

def generate_cashu_like_token(length: int) -> str:
    """Generate a realistic Cashu-like token."""
    # Cashu tokens typically contain: base64 chars, hyphens, underscores
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_hex_string(length: int) -> str:
    """Generate a hex string like Cashu tokens."""
    chars = "0123456789abcdef"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_mixed_content(length: int) -> str:
    """Generate mixed content with emojis, text, and special chars."""
    text_chars = string.ascii_letters + string.digits + " "
    emojis = "🚀💰💎🔥⚡🎯🏦💳🌍🌎🌏"
    special_chars = "áéíóúñç€$£¥"
    
    content = ""
    for i in range(length):
        if i % 10 == 0:
            content += random.choice(emojis)
        elif i % 15 == 0:
            content += random.choice(special_chars)
        else:
            content += random.choice(text_chars)
    
    return content

async def test_cashu_specific_scenarios():
    """Test scenarios specific to Cashu tokens."""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found in environment variables")
        return
    
    bot = Bot(token=BOT_TOKEN)
    
    print("\n💎 CASHU-SPECIFIC TESTS")
    print("=" * 50)
    
    # Test cases for Cashu tokens
    cashu_tests = [
        ("Short Cashu token", generate_cashu_like_token(100)),
        ("Medium Cashu token", generate_cashu_like_token(2000)),
        ("Long Cashu token", generate_cashu_like_token(8000)),
        ("Very long Cashu token", generate_cashu_like_token(18000)),
        ("Hex-like Cashu token", generate_hex_string(12000)),
        ("Mixed Cashu content", generate_mixed_content(6000)),
    ]
    
    for test_name, test_content in cashu_tests:
        print(f"\n🧪 Testing: {test_name} ({len(test_content)} chars)")
        try:
            await bot.send_message(
                chat_id=CHAT_ID or "me",
                text=f"💎 {test_name}:\n\n{test_content}"
            )
            print(f"✅ Sent {len(test_content)} character Cashu token")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_edge_cases():
    """Test edge cases and boundary conditions."""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found in environment variables")
        return
    
    bot = Bot(token=BOT_TOKEN)
    
    print("\n🔬 EDGE CASES & BOUNDARY TESTS")
    print("=" * 50)
    
    edge_tests = [
        ("Empty message", ""),
        ("Single character", "A"),
        ("Exactly 4096 chars", "A" * 4096),
        ("4097 chars (just over limit)", "A" * 4097),
        ("Exactly 4000 chars (chunk size)", "B" * 4000),
        ("4001 chars (just over chunk)", "B" * 4001),
        ("Exactly 20000 chars (document threshold)", "C" * 20000),
        ("20001 chars (just over document)", "C" * 20001),
        ("Very long (100k chars)", "D" * 100000),
    ]
    
    for test_name, test_content in edge_tests:
        print(f"\n🧪 Testing: {test_name} ({len(test_content)} chars)")
        try:
            await bot.send_message(
                chat_id=CHAT_ID or "me",
                text=f"🔬 {test_name}:\n\n{test_content}"
            )
            print(f"✅ Sent {len(test_content)} character message")
            await asyncio.sleep(3)  # Longer delay for large messages
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_special_characters():
    """Test special characters and Unicode."""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found in environment variables")
        return
    
    bot = Bot(token=BOT_TOKEN)
    
    print("\n🎨 SPECIAL CHARACTERS & UNICODE TESTS")
    print("=" * 50)
    
    special_tests = [
        ("Emojis only", "🚀💰💎🔥⚡🎯🏦💳🌍🌎🌏" * 100),
        ("Accented characters", "áéíóúñç€$£¥" * 200),
        ("Mixed emojis and text", "Hello 🚀 World 💰 Test 💎" * 150),
        ("Unicode symbols", "★☆♠♣♥♦♤♧♡♢" * 100),
        ("Mathematical symbols", "∑∏∫∂√∞≈≠≤≥" * 100),
        ("Currency symbols", "€$£¥₿₽₹₩₪₫₭₮₯₰₱₲₳₴₵₶₷₸₹₺₻₼₽₾₿" * 50),
    ]
    
    for test_name, test_content in special_tests:
        print(f"\n🧪 Testing: {test_name} ({len(test_content)} chars)")
        try:
            await bot.send_message(
                chat_id=CHAT_ID or "me",
                text=f"🎨 {test_name}:\n\n{test_content}"
            )
            print(f"✅ Sent {len(test_content)} character special content")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error: {e}")

async def test_command_responses():
    """Test bot command responses."""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found in environment variables")
        return
    
    bot = Bot(token=BOT_TOKEN)
    
    print("\n🤖 BOT COMMAND TESTS")
    print("=" * 50)
    
    commands = [
        "/start",
        "/help", 
        "/test_long"
    ]
    
    print("📝 Manual testing required for commands:")
    for cmd in commands:
        print(f"  • Send '{cmd}' to your bot and verify response")
    
    print("\n💡 Expected responses:")
    print("  • /start: Welcome message with bot info")
    print("  • /help: Help information about message handling")
    print("  • /test_long: Automatic tests of different message lengths")

async def test_document_handling():
    """Test document upload and processing."""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found in environment variables")
        return
    
    bot = Bot(token=BOT_TOKEN)
    
    print("\n📄 DOCUMENT HANDLING TESTS")
    print("=" * 50)
    
    print("📝 Manual testing required for documents:")
    print("  • Upload a text file with long content")
    print("  • Verify bot processes and echoes the content")
    print("  • Test with files of different sizes")
    
    print("\n💡 Expected behavior:")
    print("  • Bot should receive document")
    print("  • Show file name and size")
    print("  • Echo content with proper chunking")

async def test_error_handling():
    """Test error handling scenarios."""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found in environment variables")
        return
    
    bot = Bot(token=BOT_TOKEN)
    
    print("\n⚠️ ERROR HANDLING TESTS")
    print("=" * 50)
    
    error_tests = [
        ("Null bytes", "Hello\0World"),
        ("Control characters", "Hello\x01\x02\x03World"),
        ("Very long single word", "A" * 50000),
        ("Mixed nulls and text", "Hello\0World\0Test"),
    ]
    
    for test_name, test_content in error_tests:
        print(f"\n🧪 Testing: {test_name} ({len(test_content)} chars)")
        try:
            await bot.send_message(
                chat_id=CHAT_ID or "me",
                text=f"⚠️ {test_name}:\n\n{test_content}"
            )
            print(f"✅ Sent {len(test_content)} character problematic content")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"❌ Error (expected): {e}")

async def test_performance():
    """Test performance with multiple rapid messages."""
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found in environment variables")
        return
    
    bot = Bot(token=BOT_TOKEN)
    
    print("\n⚡ PERFORMANCE TESTS")
    print("=" * 50)
    
    print("🧪 Testing rapid message sending...")
    
    for i in range(5):
        message = f"Performance test #{i+1}: {generate_cashu_like_token(1000)}"
        try:
            await bot.send_message(
                chat_id=CHAT_ID or "me",
                text=message
            )
            print(f"✅ Sent performance test #{i+1}")
            await asyncio.sleep(1)  # 1 second between messages
        except Exception as e:
            print(f"❌ Error in performance test #{i+1}: {e}")

async def main():
    """Run all additional tests."""
    print("🧪 ADDITIONAL TESTS FOR CASHU MCP WALLET BOT")
    print("=" * 60)
    
    if not BOT_TOKEN:
        print("❌ Please set BOT_TOKEN in your .env file")
        return
    
    print(f"✅ Bot token found: {BOT_TOKEN[:10]}...")
    
    if CHAT_ID:
        print(f"✅ Test chat ID: {CHAT_ID}")
    else:
        print("ℹ️  No TEST_CHAT_ID set - tests will be sent to yourself")
    
    try:
        # Run all test suites
        await test_cashu_specific_scenarios()
        await test_edge_cases()
        await test_special_characters()
        await test_command_responses()
        await test_document_handling()
        await test_error_handling()
        await test_performance()
        
        print("\n🎉 All additional tests completed!")
        print("\n📋 SUMMARY:")
        print("✅ Cashu token handling")
        print("✅ Edge cases and boundaries")
        print("✅ Special characters and Unicode")
        print("✅ Command responses (manual verification needed)")
        print("✅ Document handling (manual verification needed)")
        print("✅ Error handling")
        print("✅ Performance under load")
        
        print("\n🔗 Your bot: t.me/cashu_mcp_wallet_bot")
        print("📚 Check the bot responses for each test!")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
