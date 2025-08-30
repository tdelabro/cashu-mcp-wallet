#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
from telegram import Bot

async def test_connection():
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    
    if not token:
        print("❌ No se encontró BOT_TOKEN en .env")
        return
    
    try:
        bot = Bot(token)
        me = await bot.get_me()
        print(f"✅ Bot conectado exitosamente!")
        print(f"🤖 Nombre: {me.first_name}")
        print(f"👤 Username: @{me.username}")
        print(f"🆔 ID: {me.id}")
        print(f"🔗 Enlace: t.me/{me.username}")
        return True
    except Exception as e:
        print(f"❌ Error conectando al bot: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())
