#!/usr/bin/env python3
"""
Script de prueba rápida para verificar el modo headless con configuraciones anti-detección
"""

import time
import logging
from scraper import CiesScraper
from config import *

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_headless.log'),
        logging.StreamHandler()
    ]
)

def test_headless_mode():
    """Probar el modo headless con configuraciones anti-detección"""
    scraper = CiesScraper()
    
    try:
        logging.info("🧪 Iniciando prueba de modo headless...")
        logging.info(f"Configuración HEADLESS: {HEADLESS}")
        
        # Configurar driver
        if not scraper.setup_driver():
            logging.error("❌ Error al configurar driver")
            return False
        
        logging.info("✅ Driver configurado en modo headless")
        
        # Navegar al sitio
        if not scraper.navigate_to_site():
            logging.error("❌ Error al navegar al sitio")
            return False
        
        logging.info("✅ Navegación exitosa en modo headless")
        
        # Verificar que no estamos en página de error
        if scraper.is_error_page():
            logging.error("❌ Detectada página de error")
            return False
        
        # Probar clic en Visitantes
        if scraper.click_visitantes_cies():
            logging.info("✅ Clic exitoso en modo headless")
            
            # Verificar que no estamos en página de error
            if not scraper.is_error_page():
                logging.info("✅ No se detectó página de error después del clic")
                return True
            else:
                logging.warning("⚠️ Página de error detectada después del clic")
                return False
        else:
            logging.error("❌ Error en clic")
            return False
        
    except Exception as e:
        logging.error(f"Error en la prueba: {e}")
        return False
    finally:
        if scraper.driver:
            scraper.driver.quit()
            logging.info("WebDriver cerrado")

if __name__ == "__main__":
    logging.info("🚀 Iniciando prueba de modo headless...")
    
    result = test_headless_mode()
    
    if result:
        logging.info("🎉 Prueba de modo headless exitosa")
    else:
        logging.error("❌ Prueba de modo headless falló") 