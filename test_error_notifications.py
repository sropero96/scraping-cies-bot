#!/usr/bin/env python3
"""
Script de prueba para verificar notificaciones de error de detección
"""

import logging
import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import CiesMonitor
from config import TARGET_DATE

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('test_error_notifications.log')
    ]
)

def test_error_notification():
    """Probar notificación de error de detección"""
    try:
        logging.info("🧪 Iniciando prueba de notificación de error de detección...")
        
        # Crear monitor
        monitor = CiesMonitor()
        
        # Simular resultado con error de detección
        mock_result = {
            'date': TARGET_DATE,
            'available_slots': -1,  # Error de detección
            'timestamp': '2025-07-23 20:52:00',
            'has_availability': None,
            'status': 'error_detection',
            'detection_error': True
        }
        
        logging.info("📋 Resultado simulado:")
        logging.info(f"  - Plazas: {mock_result['available_slots']}")
        logging.info(f"  - Estado: {mock_result['status']}")
        logging.info(f"  - Error de detección: {mock_result['detection_error']}")
        
        # Probar envío de notificación de error
        logging.info("📤 Enviando notificación de error de detección...")
        monitor.send_detection_error_alert(mock_result)
        
        logging.info("✅ Prueba de notificación completada")
        return True
        
    except Exception as e:
        logging.error(f"❌ Error en la prueba: {e}")
        return False

def test_main_flow_with_error():
    """Probar el flujo principal con error de detección simulado"""
    try:
        logging.info("🧪 Iniciando prueba del flujo principal con error simulado...")
        
        # Crear monitor
        monitor = CiesMonitor()
        
        # Simular resultado con error de detección
        mock_result = {
            'date': TARGET_DATE,
            'available_slots': -1,  # Error de detección
            'timestamp': '2025-07-23 20:52:00',
            'has_availability': None,
            'status': 'error_detection',
            'detection_error': True
        }
        
        # Simular el flujo de check_availability con error
        logging.info("📋 Procesando resultado con error de detección...")
        
        # Registrar estadísticas
        monitor.stats.record_attempt(mock_result['available_slots'], had_error=False)
        
        # Mostrar resultado
        logging.info(f"Resultado: {mock_result['available_slots']} plazas disponibles para {mock_result['date']}")
        
        # Manejar diferentes estados
        if mock_result['detection_error']:
            logging.warning("⚠️ Error de detección de plazas - notificando a usuarios")
            monitor.send_detection_error_alert(mock_result)
        elif mock_result['has_availability']:
            logging.info("🎉 ¡PLAZAS DISPONIBLES ENCONTRADAS!")
        else:
            logging.info("😔 No hay plazas disponibles aún...")
        
        logging.info("✅ Prueba del flujo principal completada")
        return True
        
    except Exception as e:
        logging.error(f"❌ Error en la prueba: {e}")
        return False

def main():
    """Función principal de pruebas"""
    logging.info("🚀 Iniciando pruebas de notificaciones de error...")
    
    # Prueba 1: Notificación de error
    if test_error_notification():
        logging.info("✅ Prueba 1: Notificación de error - PASÓ")
    else:
        logging.error("❌ Prueba 1: Notificación de error - FALLÓ")
    
    # Prueba 2: Flujo principal con error
    if test_main_flow_with_error():
        logging.info("✅ Prueba 2: Flujo principal con error - PASÓ")
    else:
        logging.error("❌ Prueba 2: Flujo principal con error - FALLÓ")
    
    logging.info("🎉 Pruebas de notificaciones de error completadas")

if __name__ == "__main__":
    main() 