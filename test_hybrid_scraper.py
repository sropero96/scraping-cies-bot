#!/usr/bin/env python3
"""
Script de prueba para el scraper híbrido
"""

import logging
import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper_hybrid import HybridCiesScraper

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('test_hybrid_scraper.log')
    ]
)

def test_hybrid_scraper():
    """Probar el scraper híbrido"""
    scraper = HybridCiesScraper()
    
    try:
        logging.info("🧪 Iniciando prueba del scraper híbrido...")
        
        # Probar verificación híbrida
        result = scraper.check_availability_hybrid()
        
        if result:
            logging.info("✅ Resultado obtenido:")
            logging.info(f"  - Fecha: {result['date']}")
            logging.info(f"  - Plazas: {result['available_slots']}")
            logging.info(f"  - Estado: {result['status']}")
            logging.info(f"  - Método: {result['method']}")
            logging.info(f"  - Timestamp: {result['timestamp']}")
            
            if result['available_slots'] == -1:
                logging.warning("⚠️ Error de detección - no se pudo obtener información")
            elif result['available_slots'] > 0:
                logging.info("🎉 ¡Plazas disponibles encontradas!")
            else:
                logging.info("😔 No hay plazas disponibles (confirmado)")
            
            return True
        else:
            logging.error("❌ No se obtuvo resultado del scraper híbrido")
            return False
        
    except Exception as e:
        logging.error(f"Error en la prueba: {e}")
        return False
    finally:
        if scraper.driver:
            scraper.driver.quit()
            logging.info("WebDriver cerrado")

def test_navigation_only():
    """Probar solo la navegación"""
    scraper = HybridCiesScraper()
    
    try:
        logging.info("🧪 Probando solo navegación...")
        
        # Configurar driver
        if not scraper.setup_driver():
            logging.error("❌ Error al configurar driver")
            return False
        
        # Navegar hasta la página de solicitud
        if scraper.navigate_to_solicitud_page():
            logging.info("✅ Navegación exitosa")
            
            # Obtener CSRF token
            if scraper.get_csrf_token_from_page():
                logging.info("✅ CSRF token obtenido")
            else:
                logging.warning("⚠️ No se pudo obtener CSRF token")
            
            # Mostrar URL actual
            current_url = scraper.driver.current_url
            logging.info(f"📍 URL actual: {current_url}")
            
            return True
        else:
            logging.error("❌ Error en navegación")
            return False
        
    except Exception as e:
        logging.error(f"Error en la prueba de navegación: {e}")
        return False
    finally:
        if scraper.driver:
            scraper.driver.quit()
            logging.info("WebDriver cerrado")

def main():
    """Función principal de pruebas"""
    logging.info("🚀 Iniciando pruebas del scraper híbrido...")
    
    # Prueba 1: Solo navegación
    logging.info("=" * 50)
    logging.info("PRUEBA 1: Solo navegación")
    if test_navigation_only():
        logging.info("✅ Prueba 1: Navegación - PASÓ")
    else:
        logging.error("❌ Prueba 1: Navegación - FALLÓ")
    
    # Prueba 2: Scraper híbrido completo
    logging.info("=" * 50)
    logging.info("PRUEBA 2: Scraper híbrido completo")
    if test_hybrid_scraper():
        logging.info("✅ Prueba 2: Scraper híbrido - PASÓ")
    else:
        logging.error("❌ Prueba 2: Scraper híbrido - FALLÓ")
    
    logging.info("🎉 Pruebas del scraper híbrido completadas")

if __name__ == "__main__":
    main() 