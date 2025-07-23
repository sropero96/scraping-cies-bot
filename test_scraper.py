#!/usr/bin/env python3
"""
Script de prueba para verificar que el scraper funciona correctamente
"""

from scraper import CiesScraper
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)

def test_scraper():
    """Probar el scraper"""
    print("🧪 Iniciando prueba del scraper...")
    
    scraper = CiesScraper()
    
    try:
        # Verificar disponibilidad
        result = scraper.check_availability()
        
        if result:
            print(f"✅ Prueba exitosa!")
            print(f"📅 Fecha: {result['date']}")
            print(f"🎫 Plazas disponibles: {result['available_slots']}")
            print(f"⏰ Timestamp: {result['timestamp']}")
            print(f"🔍 Hay disponibilidad: {result['has_availability']}")
        else:
            print("❌ La prueba falló - no se pudo obtener datos")
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")

if __name__ == "__main__":
    test_scraper()