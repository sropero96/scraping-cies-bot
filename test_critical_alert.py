#!/usr/bin/env python3
"""
Script para probar las alertas de error crítico
"""

import logging
from notifier import Notifier
from stats import BotStats
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_critical_alert():
    """Probar alerta de error crítico"""
    print("🧪 Probando alerta de error crítico...")
    
    # Crear instancias
    notifier = Notifier()
    stats = BotStats()
    
    # Simular mensaje de error crítico
    error_message = f"""
🚨 **BOT DETENIDO POR ERRORES CRÍTICOS** 🚨

🤖 El bot de monitoreo de Islas Cíes se ha detenido automáticamente debido a errores consecutivos.

⚠️ **Detalles:**
- Errores consecutivos: 5/5
- Última verificación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔄 **Acción requerida:**
Reinicia el bot manualmente para continuar el monitoreo.

📊 **Estadísticas de la sesión:**
{stats.get_session_summary()}

🔗 Repositorio: https://github.com/sropero96/scraping-cies-bot
    """
    
    print("📱 Enviando alerta de error crítico...")
    
    # Enviar alerta
    if notifier.send_telegram_critical_alert(error_message):
        print("✅ Alerta de error crítico enviada exitosamente!")
    else:
        print("❌ Error al enviar alerta de error crítico")
    
    # Cerrar recursos
    notifier.close()

if __name__ == "__main__":
    test_critical_alert() 