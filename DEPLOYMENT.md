# 🚀 Production Deployment

## 📋 Prerequisites

- Server with HTTPS support
- Domain name (for webhooks)
- Python 3.8+
- Systemd (for service management)

## 🔧 Deployment Options

### Option 1: VPS Deployment

```bash
# Server setup
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv -y
sudo mkdir -p /opt/cashu-bot
sudo chown $USER:$USER /opt/cashu-bot
cd /opt/cashu-bot

# Application setup
git clone <repo-url> .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env
nano .env  # Add bot token
```

### Option 2: Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "telegram_bot.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  cashu-bot:
    build: .
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
    restart: unless-stopped
```

### Option 3: Webhook Deployment (Recommended)

```python
# In telegram_bot.py, replace run_polling() with:
app.run_webhook(
    listen='0.0.0.0',
    port=8443,
    url_path='telegram/webhook',
    webhook_url='https://your-domain.com/telegram/webhook'
)
```

## 🔒 Security

- Never commit `.env` files
- Use secrets management in production
- Rotate bot tokens regularly
- Use HTTPS for webhooks
- Run as non-root user

## 📊 Monitoring

```bash
# View logs
sudo journalctl -u cashu-bot -f

# Check status
sudo systemctl status cashu-bot
```

## 🔄 Updates

```bash
# Rolling updates
sudo systemctl stop cashu-bot
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl start cashu-bot
```
