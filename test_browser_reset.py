#!/usr/bin/env python3
"""
Script de prueba para verificar las funciones de reset del navegador
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
        logging.FileHandler('test_browser_reset.log'),
        logging.StreamHandler()
    ]
)

def test_browser_reset():
    """Probar las funciones de reset del navegador"""
    scraper = CiesScraper()
    
    try:
        logging.info("🧪 Iniciando prueba de reset del navegador...")
        
        # Configurar driver
        if not scraper.setup_driver():
            logging.error("❌ Error al configurar driver")
            return False
        
        # Navegar al sitio
        if not scraper.navigate_to_site():
            logging.error("❌ Error al navegar al sitio")
            return False
        
        logging.info("✅ Navegación inicial exitosa")
        
        # Simular que estamos en página de error (cambiando la URL)
        scraper.driver.get("https://www.xunta.gal/aceptacion")
        logging.info("🔄 Simulando página de error...")
        
        # Verificar que detecta la página de error
        if scraper.is_error_page():
            logging.info("✅ Página de error detectada correctamente")
        else:
            logging.error("❌ No se detectó la página de error")
            return False
        
        # Probar el manejo de la página de error
        if scraper.handle_error_page():
            logging.info("✅ Manejo de página de error exitoso")
        else:
            logging.error("❌ Error en el manejo de página de error")
            return False
        
        # Verificar que estamos de vuelta en el sitio principal
        current_url = scraper.driver.current_url
        if TARGET_URL in current_url:
            logging.info("✅ Regresado exitosamente al sitio principal")
        else:
            logging.warning(f"⚠️ URL actual: {current_url}")
        
        logging.info("🎉 Prueba de reset del navegador completada exitosamente")
        return True
        
    except Exception as e:
        logging.error(f"Error en la prueba: {e}")
        return False
    finally:
        if scraper.driver:
            scraper.driver.quit()
            logging.info("WebDriver cerrado")

def test_clear_browser_data():
    """Probar la función de limpieza de datos del navegador"""
    scraper = CiesScraper()
    
    try:
        logging.info("🧪 Iniciando prueba de limpieza de datos...")
        
        # Configurar driver
        if not scraper.setup_driver():
            logging.error("❌ Error al configurar driver")
            return False
        
        # Navegar al sitio
        if not scraper.navigate_to_site():
            logging.error("❌ Error al navegar al sitio")
            return False
        
        # Agregar algunos datos de prueba
        scraper.driver.execute_script("localStorage.setItem('test', 'value');")
        scraper.driver.execute_script("sessionStorage.setItem('test', 'value');")
        scraper.driver.add_cookie({'name': 'test_cookie', 'value': 'test_value'})
        
        logging.info("✅ Datos de prueba agregados")
        
        # Probar la limpieza
        if scraper.clear_browser_data():
            logging.info("✅ Limpieza de datos exitosa")
        else:
            logging.error("❌ Error en la limpieza de datos")
            return False
        
        # Verificar que los datos se limpiaron
        local_storage = scraper.driver.execute_script("return localStorage.length;")
        session_storage = scraper.driver.execute_script("return sessionStorage.length;")
        cookies = len(scraper.driver.get_cookies())
        
        if local_storage == 0 and session_storage == 0 and cookies == 0:
            logging.info("✅ Verificación de limpieza exitosa")
        else:
            logging.warning(f"⚠️ Datos restantes - localStorage: {local_storage}, sessionStorage: {session_storage}, cookies: {cookies}")
        
        logging.info("🎉 Prueba de limpieza de datos completada")
        return True
        
    except Exception as e:
        logging.error(f"Error en la prueba: {e}")
        return False
    finally:
        if scraper.driver:
            scraper.driver.quit()
            logging.info("WebDriver cerrado")

if __name__ == "__main__":
    logging.info("🚀 Iniciando pruebas de reset del navegador...")
    
    # Ejecutar pruebas
    test1_result = test_browser_reset()
    test2_result = test_clear_browser_data()
    
    if test1_result and test2_result:
        logging.info("🎉 Todas las pruebas pasaron exitosamente")
    else:
        logging.error("❌ Algunas pruebas fallaron") 