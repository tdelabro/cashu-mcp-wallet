#!/usr/bin/env python3
"""
Command Patterns and Response Templates for Cashu Telegram Bot

This module contains natural language command patterns and response templates
for the Cashu MCP Wallet Telegram Bot.
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import random

class CommandPatterns:
    """Natural language command patterns for the Cashu bot."""
    
    # Balance commands
    BALANCE_PATTERNS = [
        r"show\s+my\s+balance",
        r"check\s+my\s+wallet",
        r"how\s+much\s+do\s+i\s+have",
        r"what('s|\s+is)\s+in\s+my\s+wallet",
        r"balance",
        r"wallet",
        r"funds"
    ]
    
    # Send money commands
    SEND_PATTERNS = [
        r"send\s+(\d+(?:\.\d+)?)\s*(usd|dollars?|sats?|gwei|micro\s*usdc?|micro\s*usdt?)\s+to\s+@(\w+)",
        r"pay\s+@(\w+)\s+(\d+(?:\.\d+)?)\s*(usd|dollars?|sats?|gwei|micro\s*usdc?|micro\s*usdt?)",
        r"transfer\s+(\d+(?:\.\d+)?)\s*(usd|dollars?|sats?|gwei|micro\s*usdc?|micro\s*usdt?)\s+to\s+@(\w+)",
        r"give\s+@(\w+)\s+(\d+(?:\.\d+)?)\s*(usd|dollars?|sats?|gwei|micro\s*usdc?|micro\s*usdt?)"
    ]
    
    # Create/mint tokens
    CREATE_PATTERNS = [
        r"create\s+(\d+(?:\.\d+)?)\s*(usd|dollars?|sats?|gwei|micro\s*usdc?|micro\s*usdt?)",
        r"mint\s+(\d+(?:\.\d+)?)\s*(usd|dollars?|sats?|gwei|micro\s*usdc?|micro\s*usdt?)",
        r"generate\s+(\d+(?:\.\d+)?)\s*(usd|dollars?|sats?|gwei|micro\s*usdc?|micro\s*usdt?)",
        r"make\s+(\d+(?:\.\d+)?)\s*(usd|dollars?|sats?|gwei|micro\s*usdc?|micro\s*usdt?)"
    ]
    
    # Help commands
    HELP_PATTERNS = [
        r"help",
        r"what\s+can\s+you\s+do",
        r"how\s+to\s+use",
        r"commands",
        r"guide"
    ]
    
    # Security commands
    SECURITY_PATTERNS = [
        r"help\s+security",
        r"security\s+help",
        r"how\s+to\s+stay\s+safe",
        r"safety\s+guide"
    ]

class ResponseTemplates:
    """Response templates for different bot interactions."""
    
    @staticmethod
    def welcome_message() -> str:
        """Welcome message for new users."""
        return (
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
    
    @staticmethod
    def balance_display(balances: Dict[str, float]) -> str:
        """Display user's wallet balance."""
        total_usd = 0
        balance_text = "💰 Your Cashu Wallet Balance:\n\n"
        
        for currency, amount in balances.items():
            if currency == "sats":
                usd_value = amount * 0.00025  # Approximate BTC price
                balance_text += f"🪙 Bitcoin: {amount:,.0f} sats (${usd_value:.2f})\n"
            elif currency == "gwei":
                usd_value = amount * 0.0000000005  # Approximate ETH price
                balance_text += f"⚡ Ethereum: {amount:,.0f} gwei (${usd_value:.2f})\n"
            elif currency == "micro_usdc":
                usd_value = amount * 0.000001
                balance_text += f"💵 USDC: {amount:,.0f} micro USDC (${usd_value:.2f})\n"
            elif currency == "micro_usdt":
                usd_value = amount * 0.000001
                balance_text += f"💵 USDT: {amount:,.0f} micro USDT (${usd_value:.2f})\n"
            
            total_usd += usd_value
        
        balance_text += f"\n💵 Total Value: ~${total_usd:.2f} USD"
        return balance_text
    
    @staticmethod
    def send_confirmation(amount: float, currency: str, recipient: str) -> str:
        """Confirmation message for sending money."""
        currency_symbols = {
            "usd": "USD",
            "dollars": "USD",
            "sats": "sats",
            "gwei": "gwei",
            "micro_usdc": "micro USDC",
            "micro_usdt": "micro USDT"
        }
        
        return (
            f"🔒 Security Check:\n\n"
            f"Amount: {amount:,.0f} {currency_symbols.get(currency, currency)}\n"
            f"Recipient: @{recipient}\n"
            f"Network: {currency.upper()}\n\n"
            f"⚠️ Please confirm:\n"
            f"• Amount is correct\n"
            f"• Recipient is correct\n"
            f"• You understand this is irreversible\n\n"
            f"Reply \"YES\" to confirm or \"NO\" to cancel"
        )
    
    @staticmethod
    def send_success(amount: float, currency: str, recipient: str, tx_id: str) -> str:
        """Success message for completed transaction."""
        return (
            f"✅ Payment sent successfully!\n\n"
            f"💰 Amount: {amount:,.0f} {currency}\n"
            f"👤 To: @{recipient}\n"
            f"🔗 Transaction ID: `{tx_id}`\n"
            f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n\n"
            f"🎉 Your payment is on its way!"
        )
    
    @staticmethod
    def insufficient_funds(requested: float, available: float, currency: str) -> str:
        """Error message for insufficient funds."""
        shortage = requested - available
        return (
            f"❌ Insufficient Funds\n\n"
            f"Your balance: ${available:.2f} USD\n"
            f"Requested: ${requested:.2f} USD\n"
            f"Shortage: ${shortage:.2f} USD\n\n"
            f"💡 Options:\n"
            f"• Send a smaller amount\n"
            f"• Add funds to your wallet\n"
            f"• Check your balance: \"Show my balance\""
        )
    
    @staticmethod
    def invalid_amount() -> str:
        """Error message for invalid amount."""
        return (
            f"❌ Invalid Amount\n\n"
            f"Amount must be positive and valid.\n\n"
            f"💡 Examples:\n"
            f"• \"Send 100 sats to @bob\"\n"
            f"• \"Pay 50 micro USDC to @alice\"\n"
            f"• \"Transfer 1000 gwei to @charlie\""
        )
    
    @staticmethod
    def recipient_not_found(username: str) -> str:
        """Error message for invalid recipient."""
        return (
            f"❌ Recipient Not Found\n\n"
            f"Could not find user: @{username}\n\n"
            f"💡 Make sure:\n"
            f"• Username is correct (including @ symbol)\n"
            f"• User has a Telegram account\n"
            f"• User has interacted with this bot before"
        )
    
    @staticmethod
    def network_error() -> str:
        """Error message for network issues."""
        return (
            f"⚠️ Network Connection Issue\n\n"
            f"Unable to process transaction at this time.\n\n"
            f"🔧 What happened:\n"
            f"• Lightning Network temporarily unavailable\n"
            f"• Please try again in a few minutes\n\n"
            f"💡 Alternative:\n"
            f"• Check network status: \"status\"\n"
            f"• Try smaller amount\n"
            f"• Contact support if problem persists"
        )
    
    @staticmethod
    def rate_limit() -> str:
        """Error message for rate limiting."""
        return (
            f"⏳ Too Many Requests\n\n"
            f"Please wait 30 seconds before making another transaction.\n\n"
            f"💡 This helps prevent:\n"
            f"• Accidental double-spending\n"
            f"• Network congestion\n"
            f"• Security issues"
        )
    
    @staticmethod
    def help_message() -> str:
        """Help message with available commands."""
        return (
            f"📚 Cashu Bot Help\n\n"
            f"💬 Natural Language Commands:\n\n"
            f"💰 Check Balance:\n"
            f"• \"Show my balance\"\n"
            f"• \"Check my wallet\"\n"
            f"• \"How much do I have?\"\n\n"
            f"💸 Send Money:\n"
            f"• \"Send 10 USD to @username\"\n"
            f"• \"Pay @alice 5000 sats\"\n"
            f"• \"Transfer 100 gwei to @bob\"\n\n"
            f"🪙 Create Tokens:\n"
            f"• \"Create 1000 sats\"\n"
            f"• \"Mint 500 gwei\"\n"
            f"• \"Generate 50 micro USDC\"\n\n"
            f"🔒 Security:\n"
            f"• \"Help security\" for safety tips\n\n"
            f"💡 Tip: You can use natural language - just tell me what you want to do!"
        )
    
    @staticmethod
    def security_help() -> str:
        """Security help message."""
        return (
            f"🔐 Security Guide\n\n"
            f"💡 Best Practices:\n\n"
            f"1. **Store Safely**: These tokens are like digital cash\n"
            f"2. **Private Keys**: Never share your private keys\n"
            f"3. **Backup**: Keep a backup of your wallet\n"
            f"4. **Verify**: Always verify amounts before spending\n"
            f"5. **Network**: These work on Lightning Network\n\n"
            f"⚠️ Important:\n"
            f"• Transactions are irreversible\n"
            f"• Double-check recipient usernames\n"
            f"• Keep your device secure\n\n"
            f"🆘 If you lose access:\n"
            f"• Contact support immediately\n"
            f"• Have backup information ready\n\n"
            f"💬 Need more help? Just ask!"
        )
    
    @staticmethod
    def received_tokens(amount: float, currency: str, sender: str, tx_id: str) -> str:
        """Message for received tokens."""
        return (
            f"🎁 You received Cashu tokens!\n\n"
            f"💰 Amount: {amount:,.0f} {currency}\n"
            f"👤 From: @{sender}\n"
            f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n"
            f"🔗 Transaction: `{tx_id}`\n\n"
            f"💡 What are Cashu tokens?\n"
            f"• Digital cash that's private and fast\n"
            f"• Can be spent instantly without banks\n"
            f"• Works with Bitcoin, Ethereum, and stablecoins\n\n"
            f"⚠️ Security Tips:\n"
            f"• Keep your tokens safe like cash\n"
            f"• Don't share private keys\n"
            f"• Verify amounts before spending\n\n"
            f"🚀 Ready to spend? Use these tokens to pay others or convert to other currencies!"
        )

class CommandParser:
    """Parse natural language commands."""
    
    @staticmethod
    def parse_balance_command(text: str) -> bool:
        """Check if text is a balance command."""
        text_lower = text.lower().strip()
        for pattern in CommandPatterns.BALANCE_PATTERNS:
            if re.match(pattern, text_lower):
                return True
        return False
    
    @staticmethod
    def parse_send_command(text: str) -> Optional[Tuple[float, str, str]]:
        """Parse send command and return (amount, currency, recipient)."""
        text_lower = text.lower().strip()
        
        for pattern in CommandPatterns.SEND_PATTERNS:
            match = re.match(pattern, text_lower)
            if match:
                if len(match.groups()) == 3:
                    amount = float(match.group(1))
                    currency = match.group(2)
                    recipient = match.group(3)
                else:
                    recipient = match.group(1)
                    amount = float(match.group(2))
                    currency = match.group(3)
                
                # Normalize currency
                currency = currency.replace(" ", "_")
                if currency in ["usd", "dollars", "dollar"]:
                    currency = "usd"
                elif currency in ["micro_usdc", "micro_usdc"]:
                    currency = "micro_usdc"
                elif currency in ["micro_usdt", "micro_usdt"]:
                    currency = "micro_usdt"
                
                return (amount, currency, recipient)
        
        return None
    
    @staticmethod
    def parse_create_command(text: str) -> Optional[Tuple[float, str]]:
        """Parse create/mint command and return (amount, currency)."""
        text_lower = text.lower().strip()
        
        for pattern in CommandPatterns.CREATE_PATTERNS:
            match = re.match(pattern, text_lower)
            if match:
                amount = float(match.group(1))
                currency = match.group(2)
                
                # Normalize currency
                currency = currency.replace(" ", "_")
                if currency in ["usd", "dollars", "dollar"]:
                    currency = "usd"
                elif currency in ["micro_usdc", "micro_usdc"]:
                    currency = "micro_usdc"
                elif currency in ["micro_usdt", "micro_usdt"]:
                    currency = "micro_usdt"
                
                return (amount, currency)
        
        return None
    
    @staticmethod
    def parse_help_command(text: str) -> str:
        """Parse help command and return appropriate help type."""
        text_lower = text.lower().strip()
        
        for pattern in CommandPatterns.SECURITY_PATTERNS:
            if re.match(pattern, text_lower):
                return "security"
        
        for pattern in CommandPatterns.HELP_PATTERNS:
            if re.match(pattern, text_lower):
                return "general"
        
        return "general"

def generate_transaction_id() -> str:
    """Generate a random transaction ID."""
    import uuid
    return f"cashu_{str(uuid.uuid4())[:8]}"

def format_currency_amount(amount: float, currency: str) -> str:
    """Format currency amount for display."""
    if currency == "usd":
        return f"${amount:.2f} USD"
    elif currency == "sats":
        return f"{amount:,.0f} sats"
    elif currency == "gwei":
        return f"{amount:,.0f} gwei"
    elif currency == "micro_usdc":
        return f"{amount:,.0f} micro USDC"
    elif currency == "micro_usdt":
        return f"{amount:,.0f} micro USDT"
    else:
        return f"{amount:,.0f} {currency}"

