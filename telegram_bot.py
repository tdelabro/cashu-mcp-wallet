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
        "🤖 Cashu MCP Wallet Bot\n\n"
        "✅ Bot ready!\n\n"
        "Commands:\n"
        "/start - Show this message\n"
        "/help - Show help information\n"
        "/test_long - Test long message handling\n\n"
        "Features:\n"
        "• Handles long Cashu tokens\n"
        "• Automatic message chunking\n"
        "• Document upload for very long content\n\n"
        "Send me any text and I'll echo it back!"
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = (
        "📚 Help - Cashu MCP Wallet Bot\n\n"
        "Message Length Handling:\n"
        "• Short messages (< 4k chars): Sent as regular text\n"
        "• Long messages (4k-20k chars): Split into chunks\n"
        "• Very long messages (> 20k chars): Sent as document\n\n"
        "Testing:\n"
        "Use /test_long to test different message lengths\n\n"
        "Cashu Tokens:\n"
        "This bot is designed to handle Cashu token strings which can be very long hex strings."
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
    
    # Handle different message lengths
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
