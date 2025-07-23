#!/usr/bin/env python3
"""
Script simple para obtener Chat ID de Telegram
"""

import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_chat_id():
    """Obtener Chat ID del usuario"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ Token del bot no encontrado en .env")
        return
    
    print("🤖 Obteniendo información del bot...")
    
    # Verificar bot
    try:
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getMe")
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info['ok']:
                bot_name = bot_info['result']['first_name']
                bot_username = bot_info['result']['username']
                print(f"✅ Bot: {bot_name} (@{bot_username})")
            else:
                print("❌ Token inválido")
                return
        else:
            print("❌ Error al verificar bot")
            return
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return
    
    print(f"\n📱 Pasos para obtener tu Chat ID:")
    print(f"1. Busca tu bot @{bot_username} en Telegram")
    print(f"2. Envíale el mensaje '/start'")
    print(f"3. Luego envía cualquier mensaje (ej: 'hola')")
    print(f"4. Presiona Enter cuando hayas enviado el mensaje...")
    input()
    
    # Obtener updates
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
                    
                    # Actualizar .env
                    update_env_file(chat_id)
                    
                    # Enviar mensaje de prueba
                    send_test_message(bot_token, chat_id)
                    
                else:
                    print("❌ No se encontró mensaje. Asegúrate de haber enviado un mensaje al bot.")
            else:
                print("❌ No se encontraron mensajes. Asegúrate de haber enviado un mensaje al bot.")
        else:
            print("❌ Error al obtener mensajes")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def update_env_file(chat_id):
    """Actualizar archivo .env con el Chat ID"""
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Reemplazar la línea del Chat ID
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('TELEGRAM_CHAT_ID='):
                lines[i] = f'TELEGRAM_CHAT_ID={chat_id}'
                break
        
        with open('.env', 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ Archivo .env actualizado con Chat ID")
    except Exception as e:
        print(f"❌ Error al actualizar .env: {e}")

def send_test_message(bot_token, chat_id):
    """Enviar mensaje de prueba"""
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

if __name__ == "__main__":
    get_chat_id() 