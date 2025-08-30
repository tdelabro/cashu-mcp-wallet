#!/usr/bin/env python3
"""
Cashu MCP Wallet Telegram Bot

This bot handles Cashu token operations with support for long messages.
Cashu tokens can be lengthy hex strings that exceed Telegram's 4096 character limit.
"""

import os
import logging
import asyncio
from typing import Optional
from dotenv import load_dotenv
from telegram import Update, Document
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes
)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
TELEGRAM_MAX_MESSAGE_LENGTH = 4096
CHUNK_SIZE = 4000  # Safe chunk size for splitting messages
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required!")

class LongMessageHandler:
    """Handles message processing with support for long content."""
    
    @staticmethod
    async def send_long_message(update: Update, text: str, context: ContextTypes.DEFAULT_TYPE):
        """
        Sends a long message by splitting it into chunks.
        
        Args:
            update: Telegram update object
            text: The text to send
            context: Bot context
        """
        if len(text) <= TELEGRAM_MAX_MESSAGE_LENGTH:
            await update.message.reply_text(text)
            return
        
        # Split into chunks
        chunks = [text[i:i + CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
        
        for i, chunk in enumerate(chunks):
            if i == 0:
                # First chunk with header
                message = f"📄 Long message (part {i+1}/{len(chunks)}):\n\n{chunk}"
            else:
                # Subsequent chunks
                message = f"📄 Part {i+1}/{len(chunks)}:\n\n{chunk}"
            
            await update.message.reply_text(message)
    
    @staticmethod
    async def send_as_document(update: Update, text: str, filename: str, context: ContextTypes.DEFAULT_TYPE):
        """
        Sends long text as a document file.
        
        Args:
            update: Telegram update object
            text: The text content
            filename: Name for the document
            context: Bot context
        """
        # Create a temporary file-like object
        from io import BytesIO
        file_obj = BytesIO(text.encode('utf-8'))
        file_obj.name = filename
        
        await update.message.reply_document(
            document=file_obj,
            caption=f"📎 {filename} ({len(text)} characters)"
        )

# Bot command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    welcome_message = (
        "🎉 Welcome to Cashu MCP Wallet Bot!\n\n"
        "💡 I help you manage your Cashu tokens - digital cash that's private and fast.\n\n"
        "🪙 Supported currencies:\n"
        "• Bitcoin (sats)\n"
        "• Ethereum (gwei)\n"
        "• USDC & USDT\n"
        "• Starknet (STRK)\n\n"
        "💬 Try these commands:\n"
        "• \"Show my balance\"\n"
        "• \"Send 10 USD to @username\"\n"
        "• \"Create 1000 sats\"\n"
        "• \"Help\" for more info\n\n"
        "🔒 Your tokens are secure and private!"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = (
        "📚 Cashu Bot Help\n\n"
        "💬 Natural Language Commands:\n\n"
        "💰 Check Balance:\n"
        "• \"Show my balance\"\n"
        "• \"Check my wallet\"\n"
        "• \"How much do I have?\"\n\n"
        "💸 Send Money:\n"
        "• \"Send 10 USD to @username\"\n"
        "• \"Pay @alice 5000 sats\"\n"
        "• \"Transfer 100 gwei to @bob\"\n\n"
        "🪙 Create Tokens:\n"
        "• \"Create 1000 sats\"\n"
        "• \"Mint 500 gwei\"\n"
        "• \"Generate 50 micro USDC\"\n\n"
        "🔒 Security:\n"
        "• \"Help security\" for safety tips\n\n"
        "💡 Tip: You can use natural language - just tell me what you want to do!"
    )
    await update.message.reply_text(help_text)

async def test_long_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /test_long command - test different message lengths."""
    test_messages = [
        ("Short message test", "Short message (< 4k chars)"),
        ("Medium message test", "A" * 5000),  # 5k chars
        ("Long message test", "B" * 15000),   # 15k chars
        ("Very long message test", "C" * 25000)  # 25k chars
    ]
    
    for test_name, test_content in test_messages:
        await update.message.reply_text(f"🧪 Testing: {test_name}")
        await LongMessageHandler.send_long_message(update, test_content, context)
        await asyncio.sleep(1)  # Small delay between tests

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages - echo with long message support."""
    text = update.message.text or ""
    
    if not text.strip():
        await update.message.reply_text("Please send some text to echo!")
        return
    
    # Log message length for debugging
    logger.info(f"Received message: {len(text)} characters")
    
    # Check for natural language commands
    text_lower = text.lower().strip()
    
    # Balance commands
    if any(phrase in text_lower for phrase in ["show my balance", "check my wallet", "how much do i have", "what's in my wallet", "balance", "wallet", "funds"]):
        # Mock balance response for now
        balance_response = (
            "💰 Your Cashu Wallet Balance:\n\n"
            "🪙 Bitcoin: 50,000 sats ($12.50)\n"
            "⚡ Ethereum: 1,000,000 gwei ($0.50)\n"
            "💵 USDC: 100 micro USDC ($0.10)\n"
            "💵 USDT: 500 micro USDT ($0.50)\n\n"
            "💵 Total Value: ~$13.60 USD\n\n"
            "💡 What would you like to do next?"
        )
        await update.message.reply_text(balance_response)
        return
    
    # Help commands
    elif any(phrase in text_lower for phrase in ["help security", "security help", "how to stay safe", "safety guide"]):
        security_response = (
            "🔐 Security Guide\n\n"
            "💡 Best Practices:\n\n"
            "1. **Store Safely**: These tokens are like digital cash\n"
            "2. **Private Keys**: Never share your private keys\n"
            "3. **Backup**: Keep a backup of your wallet\n"
            "4. **Verify**: Always verify amounts before spending\n"
            "5. **Network**: These work on Lightning Network\n\n"
            "⚠️ Important:\n"
            "• Transactions are irreversible\n"
            "• Double-check recipient usernames\n"
            "• Keep your device secure\n\n"
            "🆘 If you lose access:\n"
            "• Contact support immediately\n"
            "• Have backup information ready\n\n"
            "💬 Need more help? Just ask!"
        )
        await update.message.reply_text(security_response)
        return
    
    # Send money commands (basic detection)
    elif any(word in text_lower for word in ["send", "pay", "transfer", "give"]) and "@" in text:
        await update.message.reply_text(
            "💸 Send Money Feature\n\n"
            "🔒 Security Check:\n\n"
            "⚠️ This feature is coming soon!\n\n"
            "For now, you can:\n"
            "• Check your balance\n"
            "• Get security help\n"
            "• Test long messages\n\n"
            "Stay tuned for full send functionality! 🚀"
        )
        return
    
    # Create/mint commands
    elif any(word in text_lower for word in ["create", "mint", "generate", "make"]) and any(word in text_lower for word in ["sats", "gwei", "usdc", "usdt"]):
        await update.message.reply_text(
            "🪙 Create Tokens Feature\n\n"
            "⚠️ This feature is coming soon!\n\n"
            "For now, you can:\n"
            "• Check your balance\n"
            "• Get security help\n"
            "• Test long messages\n\n"
            "Stay tuned for full token creation! 🚀"
        )
        return
    
    # Default: Handle as long message echo
    if len(text) <= TELEGRAM_MAX_MESSAGE_LENGTH:
        # Short message - send directly
        await update.message.reply_text(f"📤 Echo: {text}")
    elif len(text) <= 20000:
        # Medium-long message - split into chunks
        await LongMessageHandler.send_long_message(update, f"📤 Echo: {text}", context)
    else:
        # Very long message - send as document
        await LongMessageHandler.send_as_document(
            update, 
            text, 
            "long_message.txt", 
            context
        )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document uploads."""
    document: Document = update.message.document
    
    if document.file_size and document.file_size > 50 * 1024 * 1024:  # 50MB limit
        await update.message.reply_text("❌ File too large! Maximum 50MB allowed.")
        return
    
    try:
        file = await context.bot.get_file(document.file_id)
        file_content = await file.download_as_bytearray()
        text_content = file_content.decode('utf-8')
        
        await update.message.reply_text(f"📄 Document received: {document.file_name}")
        await update.message.reply_text(f"📊 File size: {len(text_content)} characters")
        
        # Echo the document content
        await echo_message(update, context)
        
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        await update.message.reply_text("❌ Error processing document. Please try again.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text("❌ An error occurred. Please try again.")

def main():
    """Initialize and run the bot."""
    logger.info("Starting Cashu MCP Wallet Telegram Bot...")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("test_long", test_long_command))
    
    # Add message handlers
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Bot started. Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
