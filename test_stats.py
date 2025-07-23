#!/usr/bin/env python3
"""
Script para probar las estadísticas y resúmenes horarios
"""

import logging
from datetime import datetime, timedelta
from stats import BotStats
from notifier import Notifier

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_stats():
    """Probar el sistema de estadísticas"""
    print("🧪 Probando sistema de estadísticas...")
    
    # Crear instancia de estadísticas
    stats = BotStats("test_stats.json")
    
    # Simular algunos intentos
    print("\n📊 Simulando intentos de verificación...")
    
    # Simular 10 intentos con diferentes resultados
    test_data = [
        (0, False),   # Sin plazas, sin error
        (0, False),   # Sin plazas, sin error
        (2, False),   # 2 plazas disponibles
        (0, False),   # Sin plazas, sin error
        (0, True),    # Error
        (5, False),   # 5 plazas disponibles
        (0, False),   # Sin plazas, sin error
        (0, False),   # Sin plazas, sin error
        (1, False),   # 1 plaza disponible
        (0, False),   # Sin plazas, sin error
    ]
    
    for i, (slots, error) in enumerate(test_data, 1):
        stats.record_attempt(slots, had_error=error)
        print(f"  Intento {i}: {slots} plazas, error: {error}")
    
    # Mostrar resumen global
    print("\n📈 Resumen Global:")
    print(stats.get_global_summary())
    
    # Mostrar resumen de la hora actual
    print("\n⏰ Resumen de la hora actual:")
    current_summary = stats.get_current_hour_summary()
    if current_summary:
        print(stats.format_hourly_summary(current_summary, "Hora actual"))
    else:
        print("No hay datos para la hora actual")
    
    # Probar notificaciones
    print("\n🤖 Probando envío de resumen por Telegram...")
    notifier = Notifier()
    
    if current_summary:
        summary_text = stats.format_hourly_summary(current_summary, "Prueba de resumen")
        success = notifier.send_telegram_summary(summary_text)
        if success:
            print("✅ Resumen enviado exitosamente por Telegram")
        else:
            print("❌ Error al enviar resumen")
    else:
        print("❌ No hay datos para enviar resumen")
    
    notifier.close()
    
    print("\n✅ Prueba de estadísticas completada!")

if __name__ == "__main__":
    test_stats() 