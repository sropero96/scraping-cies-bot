#!/usr/bin/env python3
"""
Script de prueba para verificar las configuraciones anti-detección
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
        logging.FileHandler('test_anti_detection.log'),
        logging.StreamHandler()
    ]
)

def test_anti_detection_config():
    """Probar las configuraciones anti-detección"""
    scraper = CiesScraper()
    
    try:
        logging.info("🧪 Iniciando prueba de configuraciones anti-detección...")
        
        # Configurar driver con configuraciones anti-detección
        if not scraper.setup_driver():
            logging.error("❌ Error al configurar driver")
            return False
        
        logging.info("✅ Driver configurado con configuraciones anti-detección")
        
        # Navegar al sitio con comportamiento humano
        if not scraper.navigate_to_site():
            logging.error("❌ Error al navegar al sitio")
            return False
        
        logging.info("✅ Navegación exitosa con comportamiento humano")
        
        # Verificar que no estamos en página de error
        if scraper.is_error_page():
            logging.error("❌ Detectada página de error después de la navegación inicial")
            return False
        
        # Probar clic humano en Visitantes
        if scraper.click_visitantes_cies():
            logging.info("✅ Clic humano exitoso")
            
            # Verificar que no estamos en página de error
            if not scraper.is_error_page():
                logging.info("✅ No se detectó página de error después del clic")
                return True
            else:
                logging.warning("⚠️ Página de error detectada después del clic")
                return False
        else:
            logging.error("❌ Error en clic humano")
            return False
        
    except Exception as e:
        logging.error(f"Error en la prueba: {e}")
        return False
    finally:
        if scraper.driver:
            scraper.driver.quit()
            logging.info("WebDriver cerrado")

def test_user_agent_rotation():
    """Probar la rotación de user-agents"""
    scraper = CiesScraper()
    
    try:
        logging.info("🧪 Probando rotación de user-agents...")
        
        user_agents_used = set()
        
        for i in range(3):
            logging.info(f"Prueba {i+1}/3")
            
            # Configurar driver (cada vez usa un user-agent diferente)
            if not scraper.setup_driver():
                logging.error("❌ Error al configurar driver")
                return False
            
            # Obtener el user-agent actual
            current_ua = scraper.driver.execute_script("return navigator.userAgent;")
            user_agents_used.add(current_ua)
            
            logging.info(f"User-Agent {i+1}: {current_ua[:50]}...")
            
            # Navegar al sitio
            scraper.navigate_to_site()
            
            # Cerrar driver
            scraper.driver.quit()
            scraper.driver = None
            
            # Delay entre pruebas
            time.sleep(2)
        
        logging.info(f"✅ Se usaron {len(user_agents_used)} user-agents diferentes")
        return len(user_agents_used) > 1
        
    except Exception as e:
        logging.error(f"Error en la prueba: {e}")
        return False

def test_human_behavior():
    """Probar comportamientos humanos"""
    scraper = CiesScraper()
    
    try:
        logging.info("🧪 Probando comportamientos humanos...")
        
        # Configurar driver
        if not scraper.setup_driver():
            logging.error("❌ Error al configurar driver")
            return False
        
        # Navegar al sitio
        if not scraper.navigate_to_site():
            logging.error("❌ Error al navegar al sitio")
            return False
        
        # Probar delays aleatorios
        logging.info("Probando delays aleatorios...")
        for i in range(3):
            delay = scraper.random_delay(0.5, 1.5)
            logging.info(f"Delay {i+1}: {delay:.2f} segundos")
        
        # Probar scroll aleatorio
        logging.info("Probando scroll aleatorio...")
        scraper.driver.execute_script("""
            window.scrollTo(0, Math.random() * 500);
        """)
        
        logging.info("✅ Comportamientos humanos probados exitosamente")
        return True
        
    except Exception as e:
        logging.error(f"Error en la prueba: {e}")
        return False
    finally:
        if scraper.driver:
            scraper.driver.quit()
            logging.info("WebDriver cerrado")

if __name__ == "__main__":
    logging.info("🚀 Iniciando pruebas de anti-detección...")
    
    # Ejecutar pruebas
    test1_result = test_anti_detection_config()
    test2_result = test_user_agent_rotation()
    test3_result = test_human_behavior()
    
    if test1_result and test2_result and test3_result:
        logging.info("🎉 Todas las pruebas de anti-detección pasaron exitosamente")
    else:
        logging.error("❌ Algunas pruebas de anti-detección fallaron") 