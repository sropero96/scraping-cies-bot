#!/usr/bin/env python3
"""
Scraper híbrido para Islas Cíes
Combina navegación Selenium con llamadas API directas
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

class HybridCiesScraper:
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
        """Configurar WebDriver con anti-detección"""
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
    
    def random_delay(self, min_seconds=1, max_seconds=3):
        """Delay aleatorio para simular comportamiento humano"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def human_like_click(self, element):
        """Simular clic humano con movimiento de mouse"""
        try:
            # Scroll hasta el elemento
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.random_delay(0.5, 1)
            
            # Mover mouse al elemento
            webdriver.ActionChains(self.driver).move_to_element(element).perform()
            self.random_delay(0.3, 0.7)
            
            # Hacer clic
            element.click()
            logging.info("✅ Clic humano realizado en elemento")
            return True
            
        except Exception as e:
            logging.error(f"Error en clic humano: {e}")
            return False
    
    def navigate_to_solicitud_page(self):
        """Navegar hasta la página de solicitud usando Selenium"""
        try:
            logging.info("🌐 Navegando a la página de inicio...")
            self.driver.get(TARGET_URL)
            self.random_delay(2, 4)
            
            # Verificar si estamos en página de error
            current_url = self.driver.current_url
            if "aceptacion" in current_url:
                logging.warning("⚠️ Detectada página de error, intentando reset...")
                return self.handle_error_page()
            
            logging.info("🔍 Buscando enlace de Visitantes para Islas Cíes...")
            
            # Buscar elementos que contengan "Visitantes" y "Cíes"
            visitantes_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Visitantes')]")
            
            if not visitantes_elements:
                logging.error("❌ No se encontraron elementos de Visitantes")
                return False
            
            # Buscar el elemento correcto (generalmente el primero)
            target_element = None
            for element in visitantes_elements:
                if element.is_displayed() and element.is_enabled():
                    target_element = element
                    break
            
            if not target_element:
                logging.error("❌ No se encontró elemento clickeable de Visitantes")
                return False
            
            # Hacer clic en Visitantes
            if not self.human_like_click(target_element):
                return False
            
            self.random_delay(2, 4)
            
            # Verificar que llegamos a la página de solicitud
            current_url = self.driver.current_url
            if "iniciarReserva" in current_url:
                logging.info("✅ Navegación exitosa a página de solicitud")
                return True
            elif "aceptacion" in current_url:
                logging.warning("⚠️ Redirigido a página de error después del clic")
                return self.handle_error_page()
            else:
                logging.warning(f"⚠️ URL inesperada después del clic: {current_url}")
                return False
                
        except Exception as e:
            logging.error(f"Error en navegación: {e}")
            return False
    
    def handle_error_page(self):
        """Manejar página de error"""
        try:
            logging.info("🔄 Manejando página de error...")
            
            # Buscar botón "Ir ao inicio"
            try:
                inicio_button = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Ir ao inicio')]")
                if inicio_button:
                    logging.info("🔄 Haciendo clic en 'Ir ao inicio'")
                    self.human_like_click(inicio_button)
                    self.random_delay(2, 4)
                    
                    # Intentar navegación nuevamente
                    return self.navigate_to_solicitud_page()
            except:
                pass
            
            # Si no hay botón, intentar navegar directamente
            logging.info("🔄 Navegando directamente a la página de solicitud...")
            self.driver.get("https://autorizacionillasatlanticas.xunta.gal/illasr/iniciarReserva")
            self.random_delay(2, 4)
            
            current_url = self.driver.current_url
            if "iniciarReserva" in current_url:
                logging.info("✅ Navegación directa exitosa")
                return True
            else:
                logging.error("❌ No se pudo navegar a la página de solicitud")
                return False
                
        except Exception as e:
            logging.error(f"Error manejando página de error: {e}")
            return False
    
    def get_csrf_token_from_page(self):
        """Obtener CSRF token de la página actual"""
        try:
            logging.info("🔍 Obteniendo CSRF token de la página...")
            
            # Buscar el token CSRF en el HTML
            csrf_token = self.driver.execute_script("""
                var token = document.querySelector('meta[name="_csrf"]');
                if (token) return token.getAttribute('content');
                
                // Buscar en inputs hidden
                var input = document.querySelector('input[name="_csrf"]');
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
                logging.warning("⚠️ No se encontró CSRF token")
                return False
                
        except Exception as e:
            logging.error(f"Error al obtener CSRF token: {e}")
            return False
    
    def call_plazas_api(self, fecha=None):
        """Llamar a la API de plazas con la sesión establecida"""
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
            
            # Copiar cookies de Selenium a requests
            selenium_cookies = self.driver.get_cookies()
            for cookie in selenium_cookies:
                self.session.cookies.set(cookie['name'], cookie['value'])
            
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
    
    def get_available_slots_hybrid(self):
        """Obtener plazas usando enfoque híbrido"""
        try:
            # Navegar hasta la página de solicitud
            if not self.navigate_to_solicitud_page():
                return -1
            
            # Obtener CSRF token
            if not self.get_csrf_token_from_page():
                logging.warning("⚠️ Continuando sin CSRF token")
            
            # Llamar a la API
            api_result = self.call_plazas_api()
            
            if not api_result:
                return -1
            
            # Extraer información de plazas
            if api_result.get('existenDatos'):
                plazas_ocupadas = api_result.get('plazasOcupadas', '0')
                try:
                    slots = int(plazas_ocupadas)
                    logging.info(f"✅ Plazas disponibles obtenidas via API híbrida: {slots}")
                    return slots
                except ValueError:
                    logging.error(f"Error al convertir plazas: {plazas_ocupadas}")
                    return -1
            else:
                logging.warning("API indica que no existen datos")
                return -1
                
        except Exception as e:
            logging.error(f"Error en get_available_slots_hybrid: {e}")
            return -1
    
    def check_availability_hybrid(self):
        """Verificar disponibilidad usando enfoque híbrido"""
        try:
            logging.info("🚀 Iniciando verificación híbrida...")
            
            # Configurar driver
            if not self.setup_driver():
                return None
            
            # Obtener plazas usando enfoque híbrido
            slots = self.get_available_slots_hybrid()
            
            # Determinar estado
            if slots == -1:
                has_availability = None
                status = "error_detection"
                logging.warning("⚠️ Error en la detección de plazas via API híbrida")
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
                'method': 'hybrid_api'
            }
            
        except Exception as e:
            logging.error(f"Error en verificación híbrida: {e}")
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

def test_hybrid_scraper():
    """Probar el scraper híbrido"""
    scraper = HybridCiesScraper()
    
    try:
        logging.info("🧪 Probando scraper híbrido...")
        result = scraper.check_availability_hybrid()
        
        if result:
            logging.info(f"✅ Resultado: {result}")
            return True
        else:
            logging.error("❌ Error en scraper híbrido")
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
    
    test_hybrid_scraper() 