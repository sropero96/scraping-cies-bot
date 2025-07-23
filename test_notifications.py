#!/usr/bin/env python3
"""
Script de prueba para verificar las notificaciones
"""

import logging
from datetime import datetime
from notifier import Notifier
from config import *

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_notifications():
    """Probar las notificaciones"""
    print("🧪 Probando sistema de notificaciones...")
    
    # Crear datos de prueba
    test_data = {
        'date': TARGET_DATE,
        'available_slots': 5,  # Simular que hay 5 plazas disponibles
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Inicializar notificador
    notifier = Notifier()
    
    print(f"🤖 Telegram configurado: {'✅' if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID else '❌'}")
    print(f"📧 Email configurado: {'✅' if GMAIL_ADDRESS and GMAIL_PASSWORD else '❌'}")
    print(f"📱 WhatsApp configurado: {'✅' if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN else '❌'}")
    print(f"🤖 Chat ID Telegram: {TELEGRAM_CHAT_ID or 'No configurado'}")
    print(f"📧 Destinatario email: {RECIPIENT_EMAIL or 'No configurado'}")
    print(f"📱 Destinatario WhatsApp: {RECIPIENT_WHATSAPP or 'No configurado'}")
    
    # Probar envío
    print("\n🚀 Enviando notificaciones de prueba...")
    success = notifier.send_alert(test_data)
    
    if success:
        print("✅ Notificaciones enviadas exitosamente!")
    else:
        print("❌ Error al enviar notificaciones")
    
    # Cerrar conexiones
    notifier.close()
    
    print("\n📋 Resumen de la prueba:")
    print(f"   - Fecha: {test_data['date']}")
    print(f"   - Plazas simuladas: {test_data['available_slots']}")
    print(f"   - Timestamp: {test_data['timestamp']}")

if __name__ == "__main__":
    test_notifications() 