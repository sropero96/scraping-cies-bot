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
from config import TARGET_DATE, TARGET_URL, USER_AGENTS, MIN_DELAY, MAX_DELAY, HEADLESS, BROWSER_TIMEOUT, MAX_RETRIES, RETRY_DELAY

class HybridCiesScraper:
    def __init__(self):
        self.session = requests.Session()
        self.driver = None
        self.wait = None
        self.csrf_token = None
        self.retry_count = 0
        self.setup_session()
        
    def setup_session(self):
        """Configurar sesión HTTP con headers apropiados"""
        user_agent = random.choice(USER_AGENTS)
        self.session.headers.update({
            'User-Agent': user_agent,
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
        """Configurar WebDriver con anti-detección mejorada"""
        try:
            chrome_options = Options()
            
            # Configuración de headless
            if HEADLESS:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # Rotación de User-Agent
            user_agent = random.choice(USER_AGENTS)
            chrome_options.add_argument(f'--user-agent={user_agent}')
            
            # Anti-detección mejorada
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            
            # Configuraciones adicionales para evitar detección
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--disable-ipc-flooding-protection')
            
            # Preferencias adicionales
            prefs = {
                "profile.default_content_setting_values": {
                    "notifications": 2,
                    "geolocation": 2,
                    "media_stream": 2
                },
                "profile.managed_default_content_settings": {
                    "images": 1  # Permitir imágenes para parecer más humano
                }
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Scripts para ocultar automatización
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            self.driver.execute_script("Object.defineProperty(navigator, 'permissions', {get: () => ({query: () => Promise.resolve({state: 'granted'})})})")
            
            self.wait = WebDriverWait(self.driver, BROWSER_TIMEOUT)
            
            logging.info("✅ WebDriver configurado correctamente")
            return True
            
        except Exception as e:
            logging.error(f"Error al configurar WebDriver: {e}")
            return False
    
    def random_delay(self, min_seconds=None, max_seconds=None):
        """Delay aleatorio mejorado para simular comportamiento humano"""
        if min_seconds is None:
            min_seconds = MIN_DELAY
        if max_seconds is None:
            max_seconds = MAX_DELAY
            
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def human_like_click(self, element):
        """Simular clic humano con movimiento de mouse"""
        try:
            # Scroll hasta el elemento
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.random_delay(1, 2)
            
            # Mover mouse al elemento
            webdriver.ActionChains(self.driver).move_to_element(element).perform()
            self.random_delay(0.5, 1.5)
            
            # Hacer clic
            element.click()
            logging.info("✅ Clic humano realizado en elemento")
            return True
            
        except Exception as e:
            logging.error(f"Error en clic humano: {e}")
            return False
    
    def navigate_direct_to_solicitud(self):
        """Navegar directamente a la página de solicitud"""
        try:
            direct_url = "https://autorizacionillasatlanticas.xunta.gal/illasr/iniciarReserva"
            logging.info(f"🌐 Navegando directamente a: {direct_url}")
            
            self.driver.get(direct_url)
            self.random_delay(3, 6)
            
            # Verificar si llegamos a la página correcta
            current_url = self.driver.current_url
            if "iniciarReserva" in current_url:
                logging.info("✅ Navegación directa exitosa")
                return True
            elif "aceptacion" in current_url:
                logging.warning("⚠️ Redirigido a página de error en navegación directa")
                return False
            else:
                logging.warning(f"⚠️ URL inesperada en navegación directa: {current_url}")
                return False
                
        except Exception as e:
            logging.error(f"Error en navegación directa: {e}")
            return False
    
    def navigate_to_solicitud_page(self):
        """Navegar hasta la página de solicitud usando estrategia híbrida"""
        try:
            # Primero intentar navegación directa
            if self.navigate_direct_to_solicitud():
                return True
            
            # Si falla, intentar navegación tradicional
            logging.info("🔄 Intentando navegación tradicional...")
            logging.info("🌐 Navegando a la página de inicio...")
            self.driver.get(TARGET_URL)
            self.random_delay(3, 6)
            
            # Verificar si estamos en página de error
            current_url = self.driver.current_url
            if "aceptacion" in current_url:
                logging.warning("⚠️ Detectada página de error, intentando reset...")
                return self.handle_error_page()
            
            logging.info("🔍 Buscando enlace de Visitantes para Islas Cíes...")
            self.random_delay(2, 4)
            
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
            
            # Delay antes del clic
            self.random_delay(2, 4)
            
            # Hacer clic en Visitantes
            if not self.human_like_click(target_element):
                return False
            
            self.random_delay(3, 6)
            
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
        """Verificar disponibilidad usando enfoque híbrido con reintentos"""
        for attempt in range(MAX_RETRIES):
            try:
                logging.info(f"🚀 Iniciando verificación híbrida (intento {attempt + 1}/{MAX_RETRIES})...")
                
                # Configurar driver
                if not self.setup_driver():
                    if attempt < MAX_RETRIES - 1:
                        logging.warning(f"⚠️ Reintentando en {RETRY_DELAY} segundos...")
                        time.sleep(RETRY_DELAY)
                        continue
                    else:
                        return None
                
                # Obtener plazas usando enfoque híbrido
                slots = self.get_available_slots_hybrid()
                
                # Si obtuvimos datos válidos, retornar resultado
                if slots != -1:
                    # Determinar estado
                    if slots > 0:
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
                        'detection_error': False,
                        'method': 'hybrid_api',
                        'attempt': attempt + 1
                    }
                
                # Si no obtuvimos datos y no es el último intento, reintentar
                if attempt < MAX_RETRIES - 1:
                    logging.warning(f"⚠️ Error en detección, reintentando en {RETRY_DELAY} segundos...")
                    time.sleep(RETRY_DELAY)
                    continue
                else:
                    # Último intento fallido
                    logging.error("❌ Todos los intentos fallaron")
                    return {
                        'date': TARGET_DATE,
                        'available_slots': -1,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'has_availability': None,
                        'status': 'error_detection',
                        'detection_error': True,
                        'method': 'hybrid_api',
                        'attempt': MAX_RETRIES
                    }
                
            except Exception as e:
                logging.error(f"Error en verificación híbrida (intento {attempt + 1}): {e}")
                if attempt < MAX_RETRIES - 1:
                    logging.warning(f"⚠️ Reintentando en {RETRY_DELAY} segundos...")
                    time.sleep(RETRY_DELAY)
                    continue
                else:
                    return None
            finally:
                if self.driver:
                    self.driver.quit()
                    logging.info("WebDriver cerrado")
        
        return None
    
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