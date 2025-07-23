#!/usr/bin/env python3
"""
Script para configurar Telegram Bot paso a paso
"""

import os
import requests
import time

def setup_telegram():
    """Configurar Telegram Bot interactivamente"""
    print("🤖 Configuración de Telegram Bot")
    print("=" * 50)
    
    print("\n📋 Pasos para crear un bot de Telegram:")
    print("1. Abre Telegram y busca '@BotFather'")
    print("2. Envía '/newbot'")
    print("3. Sigue las instrucciones para crear tu bot")
    print("4. Guarda el token que te da BotFather")
    print("5. Busca tu bot y envíale '/start'")
    
    print("\n🔧 Configuración actual:")
    
    # Verificar si ya existe .env
    env_exists = os.path.exists('.env')
    if env_exists:
        print("✅ Archivo .env encontrado")
        with open('.env', 'r') as f:
            content = f.read()
            if 'TELEGRAM_BOT_TOKEN' in content:
                print("✅ Telegram ya configurado")
                return
    else:
        print("❌ Archivo .env no encontrado")
    
    print("\n📝 Ingresa la información de tu bot:")
    
    # Bot Token
    bot_token = input("Token del bot (ej: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz): ").strip()
    if not bot_token:
        print("❌ Token del bot es requerido")
        return
    
    # Verificar que el token es válido
    print("\n🔍 Verificando token del bot...")
    try:
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getMe")
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info['ok']:
                bot_name = bot_info['result']['first_name']
                bot_username = bot_info['result']['username']
                print(f"✅ Bot verificado: {bot_name} (@{bot_username})")
            else:
                print("❌ Token inválido")
                return
        else:
            print("❌ Error al verificar token")
            return
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return
    
    # Obtener Chat ID
    print(f"\n📱 Ahora necesito tu Chat ID:")
    print(f"1. Busca tu bot @{bot_username} en Telegram")
    print(f"2. Envíale el mensaje '/start'")
    print(f"3. Luego envía cualquier mensaje (ej: 'hola')")
    print(f"4. Presiona Enter cuando hayas enviado el mensaje...")
    input()
    
    # Obtener updates para encontrar el chat_id
    print("🔍 Buscando tu mensaje...")
    try:
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates")
        if response.status_code == 200:
            updates = response.json()
            if updates['ok'] and updates['result']:
                # Tomar el último mensaje
                last_update = updates['result'][-1]
                if 'message' in last_update:
                    chat_id = last_update['message']['chat']['id']
                    user_name = last_update['message']['from'].get('first_name', 'Usuario')
                    print(f"✅ Chat ID encontrado: {chat_id}")
                    print(f"✅ Usuario: {user_name}")
                else:
                    print("❌ No se encontró mensaje. Asegúrate de haber enviado un mensaje al bot.")
                    return
            else:
                print("❌ No se encontraron mensajes. Asegúrate de haber enviado un mensaje al bot.")
                return
        else:
            print("❌ Error al obtener mensajes")
            return
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return
    
    # Enviar mensaje de prueba
    print("\n🧪 Enviando mensaje de prueba...")
    try:
        test_message = "🎉 ¡Bot configurado correctamente! Recibirás alertas cuando haya plazas disponibles en Islas Cíes."
        response = requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={
                'chat_id': chat_id,
                'text': test_message
            }
        )
        if response.status_code == 200:
            print("✅ Mensaje de prueba enviado exitosamente!")
        else:
            print("❌ Error al enviar mensaje de prueba")
    except Exception as e:
        print(f"❌ Error al enviar mensaje: {e}")
    
    # Crear archivo .env
    env_content = f"""# Configuración de Telegram Bot
TELEGRAM_BOT_TOKEN={bot_token}
TELEGRAM_CHAT_ID={chat_id}

# Configuración de Gmail (opcional)
GMAIL_ADDRESS=
GMAIL_PASSWORD=
RECIPIENT_EMAIL=

# Configuración de Twilio (opcional)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
RECIPIENT_WHATSAPP=
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ Archivo .env creado exitosamente!")
    print(f"🤖 Bot: {bot_name} (@{bot_username})")
    print(f"👤 Chat ID: {chat_id}")
    
    print("\n🎯 Tu bot está listo para recibir alertas!")

if __name__ == "__main__":
    setup_telegram() 