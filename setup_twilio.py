#!/usr/bin/env python3
"""
Script para configurar Twilio WhatsApp paso a paso
"""

import os
import re

def validate_phone_number(phone):
    """Validar formato de número de teléfono"""
    # Remover espacios y caracteres especiales
    phone = re.sub(r'[^\d+]', '', phone)
    
    # Verificar que empiece con + y tenga al menos 10 dígitos
    if not phone.startswith('+'):
        phone = '+' + phone
    
    if len(phone) < 10:
        return None
    
    return phone

def setup_twilio():
    """Configurar Twilio interactivamente"""
    print("🚀 Configuración de Twilio WhatsApp")
    print("=" * 50)
    
    print("\n📋 Pasos para obtener credenciales de Twilio:")
    print("1. Ve a https://www.twilio.com/ y crea una cuenta gratuita")
    print("2. Una vez registrado, ve a la consola de Twilio")
    print("3. Copia tu Account SID y Auth Token")
    print("4. Para WhatsApp, necesitas un número de Twilio")
    print("5. En modo trial, puedes usar el número de sandbox de Twilio")
    
    print("\n🔧 Configuración actual:")
    
    # Verificar si ya existe .env
    env_exists = os.path.exists('.env')
    if env_exists:
        print("✅ Archivo .env encontrado")
        with open('.env', 'r') as f:
            content = f.read()
            if 'TWILIO_ACCOUNT_SID' in content:
                print("✅ Twilio ya configurado")
                return
    else:
        print("❌ Archivo .env no encontrado")
    
    print("\n📝 Ingresa tus credenciales de Twilio:")
    
    # Account SID
    account_sid = input("Account SID: ").strip()
    if not account_sid:
        print("❌ Account SID es requerido")
        return
    
    # Auth Token
    auth_token = input("Auth Token: ").strip()
    if not auth_token:
        print("❌ Auth Token es requerido")
        return
    
    # Número de Twilio (para sandbox)
    twilio_phone = input("Número de Twilio (o 'sandbox' para modo trial): ").strip()
    if twilio_phone.lower() == 'sandbox':
        twilio_phone = '+14155238886'  # Número de sandbox de Twilio
        print("✅ Usando número de sandbox de Twilio")
    else:
        twilio_phone = validate_phone_number(twilio_phone)
        if not twilio_phone:
            print("❌ Formato de número inválido")
            return
    
    # Tu número de WhatsApp
    recipient_whatsapp = input("Tu número de WhatsApp (ej: +34612345678): ").strip()
    recipient_whatsapp = validate_phone_number(recipient_whatsapp)
    if not recipient_whatsapp:
        print("❌ Formato de número inválido")
        return
    
    # Crear archivo .env
    env_content = f"""# Configuración de Twilio WhatsApp
TWILIO_ACCOUNT_SID={account_sid}
TWILIO_AUTH_TOKEN={auth_token}
TWILIO_PHONE_NUMBER={twilio_phone}
RECIPIENT_WHATSAPP={recipient_whatsapp}

# Configuración de Gmail (opcional)
GMAIL_ADDRESS=
GMAIL_PASSWORD=
RECIPIENT_EMAIL=
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ Archivo .env creado exitosamente!")
    print(f"📱 Número de Twilio: {twilio_phone}")
    print(f"📱 Tu WhatsApp: {recipient_whatsapp}")
    
    if twilio_phone == '+14155238886':
        print("\n🔧 Para activar WhatsApp en modo trial:")
        print("1. Envía 'join <código>' al número +14155238886 en WhatsApp")
        print("2. El código aparecerá en tu consola de Twilio")
        print("3. Una vez unido, podrás recibir mensajes")
    
    print("\n🧪 ¿Quieres probar las notificaciones ahora? (s/n): ", end="")
    test = input().strip().lower()
    if test == 's':
        test_notifications()

def test_notifications():
    """Probar las notificaciones"""
    print("\n🧪 Probando notificaciones...")
    os.system('python3 test_notifications.py')

if __name__ == "__main__":
    setup_twilio() 