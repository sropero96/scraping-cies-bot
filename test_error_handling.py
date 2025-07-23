#!/usr/bin/env python3
"""
Script para probar el manejo de páginas de error
"""

import logging
from scraper import CiesScraper
from datetime import datetime
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_error_handling():
    """Probar el manejo de páginas de error"""
    print("🧪 Probando manejo de páginas de error...")
    
    scraper = CiesScraper()
    
    try:
        # Configurar driver
        if not scraper.setup_driver():
            print("❌ Error al configurar WebDriver")
            return
        
        # Navegar al sitio
        if not scraper.navigate_to_site():
            print("❌ Error al navegar al sitio")
            return
        
        print("✅ Navegación exitosa")
        
        # Verificar URL actual
        current_url = scraper.driver.current_url
        print(f"📍 URL actual: {current_url}")
        
        # Hacer clic en Visitantes
        if not scraper.click_visitantes_cies():
            print("❌ Error al hacer clic en Visitantes")
            return
        
        # Verificar URL después del clic
        time.sleep(3)
        current_url = scraper.driver.current_url
        print(f"📍 URL después del clic: {current_url}")
        
        # Verificar si estamos en página de error
        if "aceptacion" in current_url:
            print("⚠️ Detectada página de error, probando manejo...")
            
            # Probar manejo de página de error
            if scraper.handle_error_page():
                print("✅ Manejo de página de error exitoso")
                
                # Verificar URL después del manejo
                current_url = scraper.driver.current_url
                print(f"📍 URL después del manejo: {current_url}")
                
                if "inicio" in current_url:
                    print("✅ Regresado correctamente a la página de inicio")
                else:
                    print("⚠️ No se regresó a la página de inicio")
            else:
                print("❌ Error en el manejo de página de error")
        else:
            print("✅ No se detectó página de error")
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
    finally:
        if scraper.driver:
            scraper.driver.quit()
            print("🧹 WebDriver cerrado")

if __name__ == "__main__":
    test_error_handling() 