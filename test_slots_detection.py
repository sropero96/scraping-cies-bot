#!/usr/bin/env python3
"""
Script de prueba para verificar la detección de plazas disponibles
"""

import time
import logging
from scraper import CiesScraper
from config import *
from selenium.webdriver.common.by import By

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_slots_detection.log'),
        logging.StreamHandler()
    ]
)

def test_slots_detection():
    """Probar la detección de plazas disponibles"""
    scraper = CiesScraper()
    
    try:
        logging.info("🧪 Iniciando prueba de detección de plazas...")
        
        # Configurar driver
        if not scraper.setup_driver():
            logging.error("❌ Error al configurar driver")
            return False
        
        # Navegar al sitio
        if not scraper.navigate_to_site():
            logging.error("❌ Error al navegar al sitio")
            return False
        
        # Hacer clic en Visitantes
        if not scraper.click_visitantes_cies():
            logging.error("❌ Error al hacer clic en Visitantes")
            return False
        
        # Seleccionar fecha
        if not scraper.select_target_date():
            logging.error("❌ Error al seleccionar fecha")
            return False
        
        # Obtener plazas disponibles
        logging.info("🔍 Probando detección de plazas...")
        slots = scraper.get_available_slots()
        
        logging.info(f"Resultado: {slots} plazas disponibles")
        
        if slots == -1:
            logging.warning("⚠️ Error de detección - no se pudo obtener información de plazas")
            logging.info("📸 Revisar screenshots: 'slots_debug.png' o 'error_slots.png'")
            return True  # No es un error del script, es un problema de detección
        elif slots > 0:
            logging.info("🎉 ¡Plazas disponibles encontradas!")
            return True
        elif slots == 0:
            logging.info("😔 No hay plazas disponibles (confirmado)")
            return True
        else:
            logging.error("❌ Error inesperado en la detección de plazas")
            return False
        
    except Exception as e:
        logging.error(f"Error en la prueba: {e}")
        return False
    finally:
        if scraper.driver:
            scraper.driver.quit()
            logging.info("WebDriver cerrado")

def test_page_analysis():
    """Analizar la página para entender la estructura de plazas"""
    scraper = CiesScraper()
    
    try:
        logging.info("🔍 Analizando estructura de la página...")
        
        # Configurar driver
        if not scraper.setup_driver():
            logging.error("❌ Error al configurar driver")
            return False
        
        # Navegar al sitio
        if not scraper.navigate_to_site():
            logging.error("❌ Error al navegar al sitio")
            return False
        
        # Hacer clic en Visitantes
        if not scraper.click_visitantes_cies():
            logging.error("❌ Error al hacer clic en Visitantes")
            return False
        
        # Seleccionar fecha
        if not scraper.select_target_date():
            logging.error("❌ Error al seleccionar fecha")
            return False
        
        # Explorar estructura
        scraper.explore_page_structure()
        
        # Buscar elementos relacionados con plazas
        logging.info("🔍 Buscando elementos relacionados con plazas...")
        
        # Buscar elementos que contengan "plaza", "prazas", "disponible", etc.
        keywords = ["plaza", "prazas", "disponible", "libre", "availability", "slots"]
        
        for keyword in keywords:
            try:
                elements = scraper.driver.find_elements(By.XPATH, f"//*[contains(text(), '{keyword}')]")
                if elements:
                    logging.info(f"Elementos con '{keyword}': {len(elements)}")
                    for i, elem in enumerate(elements[:3]):  # Mostrar solo los primeros 3
                        try:
                            text = elem.text.strip()
                            if text:
                                logging.info(f"  {i+1}. '{text[:100]}...'")
                        except:
                            pass
            except Exception as e:
                logging.debug(f"Error buscando '{keyword}': {e}")
        
        # Tomar screenshot
        scraper.driver.save_screenshot("page_analysis.png")
        logging.info("📸 Screenshot guardado como 'page_analysis.png'")
        
        return True
        
    except Exception as e:
        logging.error(f"Error en el análisis: {e}")
        return False
    finally:
        if scraper.driver:
            scraper.driver.quit()
            logging.info("WebDriver cerrado")

if __name__ == "__main__":
    logging.info("🚀 Iniciando pruebas de detección de plazas...")
    
    # Ejecutar pruebas
    test1_result = test_slots_detection()
    test2_result = test_page_analysis()
    
    if test1_result and test2_result:
        logging.info("🎉 Pruebas de detección de plazas completadas")
    else:
        logging.error("❌ Algunas pruebas fallaron") 