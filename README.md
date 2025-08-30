# 🤖 Cashu MCP Wallet - Telegram Bot

Telegram bot designed to handle Cashu tokens with long message support.

## 🚀 Quick Start (For Dummies)

### Step 1: Create Your Bot
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Choose a name (e.g., "My Cashu Bot")
5. Choose a username ending in `bot` (e.g., "my_cashu_bot")
6. **Save the token** that BotFather gives you

### Step 2: Setup Project
```bash
# Clone and setup
git clone <repo-url>
cd cashu-mcp-wallet
./quick_start.sh

# Add your bot token
nano .env
# Replace: BOT_TOKEN=your_token_here
```

### Step 3: Run Bot
```bash
source venv/bin/activate
python telegram_bot.py
```

### Step 4: Test
1. Go to your bot in Telegram
2. Send `/start`
3. Send any long message

## 🎯 Features

- ✅ **Long messages**: Handles Cashu tokens of any length
- ✅ **Auto-chunking**: Splits messages >4k characters
- ✅ **Documents**: Sends very long content as files
- ✅ **Unicode support**: Emojis and special characters

## 📱 Commands

- `/start` - Initialize bot
- `/help` - Show help
- `/test_long` - Test long messages
- **Any text** - Echo with long message support

## 🧪 Testing

```bash
# Test connection
python tests/test_connection.py

# Run automated tests
python tests/test_bot.py
```

## 🔒 Security

- ❌ **Never** commit `.env` file
- ✅ Each developer creates their own bot
- ✅ Use webhooks in production

## 📚 Documentation

- `DEPLOYMENT.md` - Production setup
- `TEAM_SETUP.md` - Team configuration
- `tests/README.md` - Test documentation