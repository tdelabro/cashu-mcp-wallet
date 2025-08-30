#!/usr/bin/env python3
import random
import string

def generate_test_message(length, char_type="mixed"):
    """Generate test messages of specified length."""
    if char_type == "hex":
        chars = "0123456789abcdef"
    elif char_type == "ascii":
        chars = string.ascii_letters + string.digits + " "
    else:
        chars = string.ascii_letters + string.digits + " " + "🚀💰💎🔥⚡🎯"
    
    return ''.join(random.choice(chars) for _ in range(length))

# Generate different test messages
print("🧪 MENSAJES DE PRUEBA PARA EL BOT")
print("=" * 50)

# Short message
short_msg = "Hola bot! Este es un mensaje corto de prueba. 🚀"
print(f"\n📝 Mensaje corto ({len(short_msg)} chars):")
print(short_msg)

# Medium message (5k chars)
medium_msg = generate_test_message(5000, "mixed")
print(f"\n📝 Mensaje medio ({len(medium_msg)} chars):")
print(medium_msg[:200] + "...")

# Long message (15k chars)
long_msg = generate_test_message(15000, "hex")
print(f"\n📝 Mensaje largo tipo Cashu ({len(long_msg)} chars):")
print(long_msg[:200] + "...")

# Very long message (25k chars)
very_long_msg = generate_test_message(25000, "hex")
print(f"\n📝 Mensaje muy largo ({len(very_long_msg)} chars):")
print(very_long_msg[:200] + "...")

print("\n💡 Copia estos mensajes y envíalos a tu bot para probar!")
print("🔗 Tu bot: t.me/cashu_mcp_wallet_bot")
