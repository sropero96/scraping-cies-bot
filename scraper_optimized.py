#!/usr/bin/env python3
"""
Scraper optimizado para Islas Cíes usando API directa
Basado en análisis del tráfico HAR
"""

import requests
import json
import logging
import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import TARGET_DATE, TARGET_URL

class OptimizedCiesScraper:
    def __init__(self):
        self.session = requests.Session()
        self.driver = None
        self.wait = None
        self.csrf_token = None
        self.setup_session()
        
    def setup_session(self):
        """Configurar sesión HTTP con headers apropiados"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
        })
    
    def setup_driver(self):
        """Configurar WebDriver solo para obtener CSRF token"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36')
            
            # Anti-detección
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 10)
            
            logging.info("✅ WebDriver configurado correctamente")
            return True
            
        except Exception as e:
            logging.error(f"Error al configurar WebDriver: {e}")
            return False
    
    def get_csrf_token(self):
        """Obtener CSRF token de la página de inicio"""
        try:
            logging.info("🔍 Obteniendo CSRF token...")
            
            # Navegar a la página de inicio
            self.driver.get(TARGET_URL)
            time.sleep(2)
            
            # Buscar el token CSRF en el HTML
            csrf_token = self.driver.execute_script("""
                var token = document.querySelector('meta[name="csrf-token"]');
                if (token) return token.getAttribute('content');
                
                // Buscar en inputs hidden
                var input = document.querySelector('input[name="_token"]');
                if (input) return input.value;
                
                // Buscar en cualquier elemento con data-csrf
                var element = document.querySelector('[data-csrf]');
                if (element) return element.getAttribute('data-csrf');
                
                return null;
            """)
            
            if csrf_token:
                self.csrf_token = csrf_token
                logging.info(f"✅ CSRF token obtenido: {csrf_token[:20]}...")
                return True
            else:
                logging.warning("⚠️ No se encontró CSRF token, intentando sin él")
                return True
                
        except Exception as e:
            logging.error(f"Error al obtener CSRF token: {e}")
            return False
    
    def call_plazas_api(self, fecha=None):
        """Llamar directamente a la API de plazas"""
        try:
            if not fecha:
                fecha = TARGET_DATE
            
            # URL de la API
            api_url = "https://autorizacionillasatlanticas.xunta.gal/illasr/recuperarPlazasTotales"
            
            # Datos del formulario
            data = {
                'fecha': fecha,
                'numPlazas': '1',
                'idIsla': '1',  # Islas Cíes
                'idTipoCupo': ''
            }
            
            # Headers específicos para la API
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://autorizacionillasatlanticas.xunta.gal',
                'Referer': 'https://autorizacionillasatlanticas.xunta.gal/illasr/iniciarReserva'
            }
            
            # Agregar CSRF token si está disponible
            if self.csrf_token:
                headers['X-CSRF-TOKEN'] = self.csrf_token
            
            logging.info(f"📡 Llamando a API de plazas para fecha: {fecha}")
            
            # Hacer la llamada POST
            response = self.session.post(api_url, data=data, headers=headers)
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    logging.info(f"✅ Respuesta API recibida: {result}")
                    return result
                except json.JSONDecodeError:
                    logging.error(f"Error al decodificar JSON: {response.text}")
                    return None
            else:
                logging.error(f"Error en API: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logging.error(f"Error al llamar API de plazas: {e}")
            return None
    
    def get_available_slots_api(self):
        """Obtener plazas disponibles usando la API directa"""
        try:
            # Obtener CSRF token si no lo tenemos
            if not self.csrf_token:
                if not self.get_csrf_token():
                    return -1
            
            # Llamar a la API
            api_result = self.call_plazas_api()
            
            if not api_result:
                return -1
            
            # Extraer información de plazas
            if api_result.get('existenDatos'):
                plazas_ocupadas = api_result.get('plazasOcupadas', '0')
                try:
                    slots = int(plazas_ocupadas)
                    logging.info(f"✅ Plazas disponibles obtenidas via API: {slots}")
                    return slots
                except ValueError:
                    logging.error(f"Error al convertir plazas: {plazas_ocupadas}")
                    return -1
            else:
                logging.warning("API indica que no existen datos")
                return -1
                
        except Exception as e:
            logging.error(f"Error en get_available_slots_api: {e}")
            return -1
    
    def check_availability_optimized(self):
        """Verificar disponibilidad usando API optimizada"""
        try:
            logging.info("🚀 Iniciando verificación optimizada...")
            
            # Configurar driver solo para obtener CSRF token
            if not self.setup_driver():
                return None
            
            # Obtener plazas via API
            slots = self.get_available_slots_api()
            
            # Determinar estado
            if slots == -1:
                has_availability = None
                status = "error_detection"
                logging.warning("⚠️ Error en la detección de plazas via API")
            elif slots > 0:
                has_availability = True
                status = "available"
                logging.info(f"🎉 ¡PLAZAS DISPONIBLES ENCONTRADAS! ({slots} plazas)")
            else:
                has_availability = False
                status = "unavailable"
                logging.info("😔 No hay plazas disponibles")
            
            return {
                'date': TARGET_DATE,
                'available_slots': slots,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'has_availability': has_availability,
                'status': status,
                'detection_error': slots == -1,
                'method': 'api_optimized'
            }
            
        except Exception as e:
            logging.error(f"Error en verificación optimizada: {e}")
            return None
        finally:
            if self.driver:
                self.driver.quit()
                logging.info("WebDriver cerrado")
    
    def close_driver(self):
        """Cerrar el WebDriver"""
        if self.driver:
            self.driver.quit()
            logging.info("WebDriver cerrado")

def test_optimized_scraper():
    """Probar el scraper optimizado"""
    scraper = OptimizedCiesScraper()
    
    try:
        logging.info("🧪 Probando scraper optimizado...")
        result = scraper.check_availability_optimized()
        
        if result:
            logging.info(f"✅ Resultado: {result}")
            return True
        else:
            logging.error("❌ Error en scraper optimizado")
            return False
            
    except Exception as e:
        logging.error(f"Error en prueba: {e}")
        return False

if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    test_optimized_scraper() 