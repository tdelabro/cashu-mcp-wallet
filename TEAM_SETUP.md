# 👥 Team Setup

## 🔑 Bot Tokens

**❌ DO NOT share `.env` files between team members**

Each developer must create their own bot and token for security.

## 📋 Setup for Each Member

### 1. Create Personal Bot
```bash
# In Telegram:
# 1. Search @BotFather
# 2. Send /newbot
# 3. Choose name: "My Cashu Bot"
# 4. Choose username: "my_cashu_bot_123"
# 5. Save the 


token
```

### 2. Local Setup
```bash
git clone <repo-url>
cd cashu-mcp-wallet
./quick_start.sh
nano .env  # Add YOUR personal token
```

### 3. Test
```bash
source venv/bin/activate
python telegram_bot.py
```

## 🔒 Security

### ✅ Share:
- Source code
- `requirements.txt`
- `env.example`
- Documentation

### ❌ Don't Share:
- `.env` files
- Personal tokens
- Credentials

## 🧪 Individual Testing

Each member can test independently:

```bash
python tests/test_connection.py
python tests/test_bot.py
```

## 🚀 Production

For production, team can:
1. Use shared bot (with secure token)
2. Configure webhooks
3. See `DEPLOYMENT.md` for details
