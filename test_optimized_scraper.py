#!/usr/bin/env python3
"""
Script de prueba para el scraper optimizado
"""

import logging
import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper_optimized import OptimizedCiesScraper

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('test_optimized_scraper.log')
    ]
)

def test_optimized_scraper():
    """Probar el scraper optimizado"""
    scraper = OptimizedCiesScraper()
    
    try:
        logging.info("🧪 Iniciando prueba del scraper optimizado...")
        
        # Probar verificación optimizada
        result = scraper.check_availability_optimized()
        
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
            logging.error("❌ No se obtuvo resultado del scraper optimizado")
            return False
        
    except Exception as e:
        logging.error(f"Error en la prueba: {e}")
        return False
    finally:
        if scraper.driver:
            scraper.driver.quit()
            logging.info("WebDriver cerrado")

def test_api_direct():
    """Probar llamada directa a la API"""
    scraper = OptimizedCiesScraper()
    
    try:
        logging.info("🧪 Probando llamada directa a la API...")
        
        # Configurar driver para obtener CSRF token
        if not scraper.setup_driver():
            logging.error("❌ Error al configurar driver")
            return False
        
        # Obtener CSRF token
        if not scraper.get_csrf_token():
            logging.error("❌ Error al obtener CSRF token")
            return False
        
        # Llamar a la API
        api_result = scraper.call_plazas_api()
        
        if api_result:
            logging.info("✅ Respuesta de la API:")
            logging.info(f"  - existenDatos: {api_result.get('existenDatos')}")
            logging.info(f"  - plazasOcupadas: {api_result.get('plazasOcupadas')}")
            logging.info(f"  - diaLibre: {api_result.get('diaLibre')}")
            logging.info(f"  - fecha: {api_result.get('fecha')}")
            
            # Extraer plazas
            if api_result.get('existenDatos'):
                plazas = int(api_result.get('plazasOcupadas', '0'))
                logging.info(f"✅ Plazas disponibles: {plazas}")
            else:
                logging.warning("⚠️ No existen datos para la fecha")
            
            return True
        else:
            logging.error("❌ Error al llamar a la API")
            return False
        
    except Exception as e:
        logging.error(f"Error en la prueba de API: {e}")
        return False
    finally:
        if scraper.driver:
            scraper.driver.quit()
            logging.info("WebDriver cerrado")

def main():
    """Función principal de pruebas"""
    logging.info("🚀 Iniciando pruebas del scraper optimizado...")
    
    # Prueba 1: Scraper optimizado completo
    logging.info("=" * 50)
    logging.info("PRUEBA 1: Scraper optimizado completo")
    if test_optimized_scraper():
        logging.info("✅ Prueba 1: Scraper optimizado - PASÓ")
    else:
        logging.error("❌ Prueba 1: Scraper optimizado - FALLÓ")
    
    # Prueba 2: Llamada directa a API
    logging.info("=" * 50)
    logging.info("PRUEBA 2: Llamada directa a API")
    if test_api_direct():
        logging.info("✅ Prueba 2: Llamada directa a API - PASÓ")
    else:
        logging.error("❌ Prueba 2: Llamada directa a API - FALLÓ")
    
    logging.info("🎉 Pruebas del scraper optimizado completadas")

if __name__ == "__main__":
    main() 