#!/usr/bin/env python3
"""
Script para agregar un segundo usuario de Telegram
"""

import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def add_second_user():
    """Agregar un segundo usuario de Telegram"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not bot_token:
        print("❌ Token del bot no encontrado en .env")
        return
    
    print("🤖 Agregando segundo usuario de Telegram")
    print("=" * 50)
    
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
    
    print(f"\n📱 Pasos para agregar el segundo usuario:")
    print(f"1. El segundo usuario debe buscar el bot @{bot_username} en Telegram")
    print(f"2. Enviarle el mensaje '/start'")
    print(f"3. Luego enviar cualquier mensaje (ej: 'hola')")
    print(f"4. Presiona Enter cuando el segundo usuario haya enviado el mensaje...")
    input()
    
    # Obtener updates para encontrar el nuevo chat_id
    print("🔍 Buscando mensaje del segundo usuario...")
    try:
        response = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates")
        if response.status_code == 200:
            updates = response.json()
            if updates['ok'] and updates['result']:
                # Buscar el mensaje más reciente que no sea del primer usuario
                first_user_id = os.getenv('TELEGRAM_CHAT_ID')
                
                for update in reversed(updates['result']):
                    if 'message' in update:
                        chat_id = update['message']['chat']['id']
                        user_name = update['message']['from'].get('first_name', 'Usuario')
                        user_id = update['message']['from'].get('id', '')
                        
                        # Si es un usuario diferente al primero
                        if str(chat_id) != str(first_user_id):
                            print(f"✅ Segundo usuario encontrado:")
                            print(f"   - Nombre: {user_name}")
                            print(f"   - Chat ID: {chat_id}")
                            print(f"   - User ID: {user_id}")
                            
                            # Enviar mensaje de prueba
                            test_message = "🎉 ¡Segundo usuario agregado correctamente! Recibirás alertas cuando haya plazas disponibles en Islas Cíes."
                            response = requests.post(
                                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                                data={
                                    'chat_id': chat_id,
                                    'text': test_message
                                }
                            )
                            
                            if response.status_code == 200:
                                print("✅ Mensaje de prueba enviado al segundo usuario")
                                
                                # Actualizar .env
                                update_env_file(chat_id)
                                return
                            else:
                                print("❌ Error al enviar mensaje de prueba")
                                return
                
                print("❌ No se encontró un segundo usuario. Asegúrate de que haya enviado un mensaje al bot.")
            else:
                print("❌ No se encontraron mensajes")
        else:
            print("❌ Error al obtener mensajes")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def update_env_file(second_chat_id):
    """Actualizar archivo .env con el segundo Chat ID"""
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Agregar la línea del segundo Chat ID
        lines = content.split('\n')
        
        # Buscar si ya existe la línea del segundo usuario
        second_user_line_index = -1
        for i, line in enumerate(lines):
            if line.startswith('TELEGRAM_CHAT_ID_2='):
                second_user_line_index = i
                break
        
        if second_user_line_index >= 0:
            # Actualizar línea existente
            lines[second_user_line_index] = f'TELEGRAM_CHAT_ID_2={second_chat_id}'
        else:
            # Agregar nueva línea después de TELEGRAM_CHAT_ID
            for i, line in enumerate(lines):
                if line.startswith('TELEGRAM_CHAT_ID='):
                    lines.insert(i + 1, f'TELEGRAM_CHAT_ID_2={second_chat_id}')
                    break
        
        with open('.env', 'w') as f:
            f.write('\n'.join(lines))
        
        print("✅ Archivo .env actualizado con segundo Chat ID")
        print(f"📱 Segundo usuario: {second_chat_id}")
        
    except Exception as e:
        print(f"❌ Error al actualizar .env: {e}")

if __name__ == "__main__":
    add_second_user() 