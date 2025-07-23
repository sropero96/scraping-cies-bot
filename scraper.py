import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time
import logging
from config import *

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cies_monitor.log'),
        logging.StreamHandler()
    ]
)

class CiesScraper:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0'
        ]
        
    def random_delay(self, min_seconds=1, max_seconds=3):
        """Delay aleatorio para simular comportamiento humano"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        return delay
        
    def human_like_click(self, element):
        """Simular clic humano con delay aleatorio"""
        try:
            # Scroll suave hacia el elemento
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            self.random_delay(0.5, 1.5)
            
            # Mover el mouse de forma natural (simulado)
            self.driver.execute_script("""
                var element = arguments[0];
                var rect = element.getBoundingClientRect();
                var centerX = rect.left + rect.width / 2;
                var centerY = rect.top + rect.height / 2;
                
                // Simular movimiento del mouse
                var event = new MouseEvent('mouseover', {
                    'view': window,
                    'bubbles': true,
                    'cancelable': true,
                    'clientX': centerX,
                    'clientY': centerY
                });
                element.dispatchEvent(event);
            """, element)
            
            self.random_delay(0.3, 0.8)
            
            # Hacer clic
            element.click()
            logging.info(f"✅ Clic humano realizado en elemento")
            return True
            
        except Exception as e:
            logging.error(f"Error en clic humano: {e}")
            # Fallback a clic normal
            try:
                element.click()
                return True
            except:
                return False
        
    def setup_driver(self):
        """Configurar el WebDriver de Chrome con configuraciones anti-detección avanzadas"""
        try:
            chrome_options = Options()
            
            # Seleccionar user-agent aleatorio
            user_agent = random.choice(self.user_agents)
            
            # Configuraciones básicas
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--no-first-run')
            chrome_options.add_argument('--no-default-browser-check')
            chrome_options.add_argument('--disable-default-apps')
            chrome_options.add_argument('--disable-popup-blocking')
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_argument('--disable-background-timer-throttling')
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')
            chrome_options.add_argument('--disable-renderer-backgrounding')
            chrome_options.add_argument('--disable-field-trial-config')
            chrome_options.add_argument('--disable-ipc-flooding-protection')
            
            # Configuraciones anti-detección
            chrome_options.add_argument(f'--user-agent={user_agent}')
            
            # Configuración de headless
            if HEADLESS:
                chrome_options.add_argument('--headless=new')
                chrome_options.add_argument('--disable-images')
                chrome_options.add_argument('--window-size=1920,1080')
            else:
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_argument('--start-maximized')
            
            # Headers adicionales
            chrome_options.add_argument('--accept-lang=es-ES,es;q=0.9,en;q=0.8')
            chrome_options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
            
            # Configuraciones experimentales
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option("prefs", {
                "profile.default_content_setting_values.notifications": 2,
                "profile.default_content_settings.popups": 0,
                "profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values.media_stream": 2,
            })
            
            # Configurar Chrome para macOS
            chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            
            # Crear driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, BROWSER_TIMEOUT)
            
            # Configuraciones adicionales post-inicialización
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['es-ES', 'es', 'en-US', 'en']})")
            self.driver.execute_script("window.chrome = {runtime: {}}")
            
            # Agregar propiedades adicionales para evitar detección
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'permissions', {
                    get: () => ({
                        query: () => Promise.resolve({ state: 'granted' })
                    })
                });
                
                Object.defineProperty(navigator, 'connection', {
                    get: () => ({
                        effectiveType: '4g',
                        rtt: 50,
                        downlink: 10
                    })
                });
                
                // Simular que no es un bot
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """)
            
            mode = "headless" if HEADLESS else "visible"
            logging.info(f"WebDriver configurado correctamente en modo {mode} con User-Agent: {user_agent[:50]}...")
            return True
            
        except Exception as e:
            logging.error(f"Error al configurar WebDriver: {e}")
            return False
    
    def navigate_to_site(self):
        """Navegar al sitio web objetivo con comportamiento humano"""
        try:
            # Delay aleatorio antes de navegar
            self.random_delay(2, 5)
            
            self.driver.get(TARGET_URL)
            logging.info(f"Navegando a: {TARGET_URL}")
            
            # Esperar a que la página cargue
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            # Simular comportamiento humano: scroll aleatorio
            self.driver.execute_script("""
                // Scroll aleatorio para simular comportamiento humano
                setTimeout(() => {
                    window.scrollTo(0, Math.random() * 100);
                }, 500);
                
                setTimeout(() => {
                    window.scrollTo(0, 0);
                }, 1500);
            """)
            
            # Delay aleatorio después de cargar
            self.random_delay(2, 4)
            
            return True
            
        except Exception as e:
            logging.error(f"Error al navegar al sitio: {e}")
            return False
    
    def explore_home_page(self):
        """Explorar la página de inicio para entender su estructura"""
        try:
            logging.info("🔍 Explorando página de inicio...")
            
            # Esperar a que la página cargue completamente
            time.sleep(1)  # Reducido de 3 a 1 segundo
            
            # Buscar elementos que contengan "Cíes" o "Cies"
            cies_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Cíes') or contains(text(), 'Cies')]")
            logging.info(f"Encontrados {len(cies_elements)} elementos que contienen 'Cíes'")
            
            for i, elem in enumerate(cies_elements):
                try:
                    text = elem.text
                    if text.strip():
                        logging.info(f"Elemento Cíes {i+1}: '{text}'")
                except:
                    pass
            
            # Buscar elementos que contengan "Visitantes"
            visitantes_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Visitantes')]")
            logging.info(f"Encontrados {len(visitantes_elements)} elementos que contienen 'Visitantes'")
            
            for i, elem in enumerate(visitantes_elements):
                try:
                    text = elem.text
                    if text.strip():
                        logging.info(f"Elemento Visitantes {i+1}: '{text}'")
                        # Verificar si es clickeable
                        tag_name = elem.tag_name
                        logging.info(f"  - Tag: {tag_name}")
                except:
                    pass
            
            # Buscar elementos clickeables (botones, enlaces, etc.)
            clickable_elements = self.driver.find_elements(By.XPATH, "//a | //button | //div[@onclick] | //span[@onclick]")
            logging.info(f"Encontrados {len(clickable_elements)} elementos potencialmente clickeables")
            
            # Tomar screenshot de la página de inicio
            self.driver.save_screenshot("home_page.png")
            logging.info("📸 Screenshot de la página de inicio guardado como 'home_page.png'")
            
            return True
            
        except Exception as e:
            logging.error(f"Error explorando página de inicio: {e}")
            return False
    
    def click_visitantes_cies(self):
        """Hacer clic en el icono de Visitantes para Islas Cíes con comportamiento humano"""
        try:
            logging.info("🔍 Buscando icono de Visitantes para Islas Cíes...")
            
            # Delay aleatorio antes de buscar
            self.random_delay(1, 3)
            
            # Primero explorar la página de inicio
            self.explore_home_page()
            
            # Delay aleatorio después de explorar
            self.random_delay(1, 2)
            
            # Buscar elementos que contengan "Visitantes" con diferentes estrategias
            # Ser más específicos para encontrar el elemento correcto
            visitantes_selectors = [
                "//div[contains(text(), 'Visitantes') and contains(text(), 'Cíes')]",
                "//span[contains(text(), 'Visitantes') and contains(text(), 'Cíes')]",
                "//a[contains(text(), 'Visitantes') and contains(text(), 'Cíes')]",
                "//div[contains(@class, 'cies')]//*[contains(text(), 'Visitantes')]",
                "//div[contains(@class, 'islas')]//*[contains(text(), 'Visitantes')]",
                "//div[contains(text(), 'Visitantes')]",
                "//span[contains(text(), 'Visitantes')]",
                "//a[contains(text(), 'Visitantes')]",
                "//button[contains(text(), 'Visitantes')]",
                "//*[contains(text(), 'Visitantes')]"
            ]
            
            visitantes_element = None
            for selector in visitantes_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    logging.info(f"Selector '{selector}' encontró {len(elements)} elementos")
                    
                    for elem in elements:
                        try:
                            # Verificar que esté en la sección de Cíes
                            parent = elem.find_element(By.XPATH, "./ancestor::*[contains(text(), 'Cíes') or contains(text(), 'Cies')]")
                            if parent:
                                visitantes_element = elem
                                logging.info(f"Elemento Visitantes encontrado con selector: {selector}")
                                break
                        except:
                            # Si no encuentra ancestro con Cíes, verificar si está en la mitad izquierda de la página
                            location = elem.location
                            page_width = self.driver.execute_script("return window.innerWidth;")
                            if location['x'] < page_width / 2:  # Asumiendo que Cíes está a la izquierda
                                visitantes_element = elem
                                logging.info(f"Elemento Visitantes encontrado por posición (izquierda) con selector: {selector}")
                                break
                    
                    if visitantes_element:
                        break
                except Exception as e:
                    logging.warning(f"Error con selector '{selector}': {e}")
                    continue
            
            if not visitantes_element:
                # Intentar buscar por JavaScript
                try:
                    visitantes_element = self.driver.execute_script("""
                        var elements = document.querySelectorAll('*');
                        for (var i = 0; i < elements.length; i++) {
                            if (elements[i].textContent.includes('Visitantes')) {
                                // Verificar si está cerca de Cíes
                                var parent = elements[i].closest('*');
                                if (parent && parent.textContent.includes('Cíes')) {
                                    return elements[i];
                                }
                            }
                        }
                        return null;
                    """)
                    if visitantes_element:
                        logging.info("Elemento Visitantes encontrado por JavaScript")
                except:
                    pass
            
            if visitantes_element:
                # Delay aleatorio antes del clic
                self.random_delay(1, 3)
                
                # Usar clic humano en lugar de clic normal
                if self.human_like_click(visitantes_element):
                    logging.info("✅ Clic humano en Visitantes para Islas Cíes realizado")
                    
                    # Delay aleatorio después del clic
                    self.random_delay(2, 4)
                    
                    # Verificar que navegamos a la página correcta
                    current_url = self.driver.current_url
                    if "iniciarReserva" in current_url:
                        logging.info("✅ Navegación exitosa a página de solicitud")
                        return True
                    elif "aceptacion" in current_url:
                        logging.warning("⚠️ Detectada página de error después del clic en Visitantes")
                        # Manejar la página de error
                        if self.handle_error_page():
                            logging.info("✅ Página de error manejada exitosamente")
                            # Intentar el clic nuevamente después de volver al inicio
                            self.random_delay(2, 4)
                            return self.click_visitantes_cies()  # Llamada recursiva
                        else:
                            logging.error("❌ No se pudo manejar la página de error")
                            return False
                    else:
                        logging.warning(f"⚠️ Navegó a URL inesperada: {current_url}")
                        # Intentar navegar directamente a la página de solicitud
                        self.driver.get("https://autorizacionillasatlanticas.xunta.gal/illasr/iniciarReserva")
                        self.random_delay(2, 3)
                        return True
                else:
                    logging.error("❌ Error en clic humano")
                    return False
            else:
                logging.error("❌ No se pudo encontrar el elemento Visitantes para Islas Cíes")
                return False
                
        except Exception as e:
            logging.error(f"Error al hacer clic en Visitantes: {e}")
            return False
    
    def explore_page_structure(self):
        """Explorar la estructura de la página para entender los elementos"""
        try:
            logging.info("🔍 Explorando estructura de la página de solicitud...")
            
            # Esperar a que la página cargue completamente
            time.sleep(5)
            
            # Verificar que estamos en la página correcta
            current_url = self.driver.current_url
            logging.info(f"URL actual: {current_url}")
            
            # Buscar elementos de fecha con diferentes selectores
            date_selectors = [
                "//input[@type='text']",
                "//input[@type='date']",
                "//input[contains(@placeholder, 'data')]",
                "//input[contains(@placeholder, 'Data')]",
                "//input[contains(@class, 'date')]"
            ]
            
            for selector in date_selectors:
                date_inputs = self.driver.find_elements(By.XPATH, selector)
                if date_inputs:
                    logging.info(f"Encontrados {len(date_inputs)} campos con selector: {selector}")
                    for i, input_elem in enumerate(date_inputs):
                        try:
                            placeholder = input_elem.get_attribute('placeholder') or 'Sin placeholder'
                            value = input_elem.get_attribute('value') or 'Sin valor'
                            id_attr = input_elem.get_attribute('id') or 'Sin ID'
                            logging.info(f"Campo {i+1}: id='{id_attr}', placeholder='{placeholder}', value='{value}'")
                        except:
                            pass
            
            # Buscar elementos de calendario
            calendar_elements = self.driver.find_elements(By.XPATH, "//*[contains(@class, 'calendar') or contains(@class, 'date') or contains(@class, 'picker') or contains(@class, 'ui-datepicker')]")
            logging.info(f"Encontrados {len(calendar_elements)} elementos de calendario")
            
            # Buscar elementos que contengan "plaza" o "prazas"
            plaza_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'plaza') or contains(text(), 'prazas') or contains(text(), 'disponible') or contains(text(), 'libre')]")
            logging.info(f"Encontrados {len(plaza_elements)} elementos relacionados con plazas")
            
            for elem in plaza_elements:
                try:
                    text = elem.text
                    if text.strip():
                        logging.info(f"Elemento plaza: '{text}'")
                except:
                    pass
            
            # Buscar elementos de selección de año y mes
            year_elements = self.driver.find_elements(By.XPATH, "//select[contains(@class, 'year') or contains(@class, 'ui-datepicker-year')]")
            month_elements = self.driver.find_elements(By.XPATH, "//select[contains(@class, 'month') or contains(@class, 'ui-datepicker-month')]")
            logging.info(f"Encontrados {len(year_elements)} selectores de año y {len(month_elements)} selectores de mes")
            
            # Tomar screenshot para análisis
            self.driver.save_screenshot("page_structure.png")
            logging.info("📸 Screenshot guardado como 'page_structure.png'")
            
            return True
            
        except Exception as e:
            logging.error(f"Error explorando página: {e}")
            return False
    
    def select_target_date(self):
        """Seleccionar la fecha objetivo (2 de agosto de 2025)"""
        try:
            # Primero explorar la estructura
            self.explore_page_structure()
            
            # Verificar si estamos en página de error después de explorar
            if not self.check_and_handle_error_page():
                return False
            
            # Buscar el campo de fecha usando los IDs específicos encontrados
            date_selectors = [
                "//input[@id='fecha']",
                "//input[@id='fechaEntrada']",
                "//input[@placeholder='Data da visita']",
                "//input[contains(@placeholder, 'data')]",
                "//input[contains(@placeholder, 'Data')]",
                "//input[@type='text']",
                "//input[contains(@class, 'date')]"
            ]
            
            date_input = None
            for selector in date_selectors:
                try:
                    date_input = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    logging.info(f"Campo de fecha encontrado con selector: {selector}")
                    break
                except:
                    continue
            
            if not date_input:
                logging.error("No se pudo encontrar el campo de fecha")
                return False
            
            # Hacer clic en el campo de fecha para abrir el calendario
            date_input.click()
            logging.info("Campo de fecha clickeado - esperando calendario...")
            
            # Verificar si estamos en página de error después del clic
            if not self.check_and_handle_error_page():
                return False
            
            # Esperar a que aparezca el calendario
            time.sleep(3)
            
            # Buscar el calendario con diferentes selectores
            calendar_selectors = [
                "//div[contains(@class, 'ui-datepicker')]",
                "//div[contains(@class, 'calendar')]",
                "//div[contains(@class, 'datepicker')]",
                "//table[contains(@class, 'calendar')]"
            ]
            
            calendar = None
            for selector in calendar_selectors:
                try:
                    calendar = self.driver.find_element(By.XPATH, selector)
                    if calendar.is_displayed():
                        logging.info(f"Calendario encontrado con selector: {selector}")
                        break
                except:
                    continue
            
            if not calendar:
                logging.error("No se pudo encontrar el calendario")
                return False
            
            # Navegar hasta agosto 2025 usando las flechas del calendario
            logging.info("Navegando hasta agosto 2025...")
            
            # Buscar flechas de navegación
            next_arrow_selectors = [
                "//a[contains(@class, 'ui-datepicker-next')]",
                "//a[contains(@class, 'next')]",
                "//button[contains(@class, 'next')]",
                "//span[contains(@class, 'next')]",
                "//i[contains(@class, 'next')]"
            ]
            
            next_arrow = None
            for selector in next_arrow_selectors:
                try:
                    next_arrow = self.driver.find_element(By.XPATH, selector)
                    if next_arrow.is_displayed():
                        logging.info(f"Flecha siguiente encontrada con selector: {selector}")
                        break
                except:
                    continue
            
            if not next_arrow:
                logging.error("No se pudo encontrar la flecha de navegación")
                return False
            
            # Navegar hasta agosto 2025
            # Primero necesitamos llegar al año 2025, luego al mes de agosto
            current_month_year = self.get_current_month_year()
            logging.info(f"Mes y año actual: {current_month_year}")
            
            # Navegar hasta agosto 2025
            target_reached = self.navigate_to_august_2025(next_arrow)
            
            # Verificar si estamos en página de error después de navegar en el calendario
            if not self.check_and_handle_error_page():
                return False
            
            if target_reached:
                # Seleccionar el día 2
                day_2_selectors = [
                    "//table[contains(@class, 'ui-datepicker-calendar')]//td/a[text()='2']",
                    "//td/a[text()='2']",
                    "//a[text()='2']",
                    "//td[contains(@class, 'ui-datepicker-day')]/a[text()='2']"
                ]
                
                day_2_element = None
                for selector in day_2_selectors:
                    try:
                        day_2_element = self.driver.find_element(By.XPATH, selector)
                        if day_2_element.is_displayed():
                            logging.info(f"Día 2 encontrado con selector: {selector}")
                            break
                    except:
                        continue
                
                if day_2_element:
                    day_2_element.click()
                    logging.info("✅ Día 2 seleccionado")
                    time.sleep(2)  # Esperar a que se aplique la selección
                    
                    # Verificar si estamos en página de error después de seleccionar el día
                    if not self.check_and_handle_error_page():
                        return False
                    
                    return True
                else:
                    logging.error("No se pudo encontrar el día 2")
                    return False
            else:
                logging.error("No se pudo navegar hasta agosto 2025")
                return False
            
        except Exception as e:
            logging.error(f"Error al seleccionar fecha: {e}")
            return False
    
    def get_current_month_year(self):
        """Obtener el mes y año actual del calendario"""
        try:
            # Buscar elementos que muestren el mes y año actual
            month_year_selectors = [
                "//div[contains(@class, 'ui-datepicker-title')]",
                "//div[contains(@class, 'datepicker-title')]",
                "//span[contains(@class, 'ui-datepicker-month')]",
                "//span[contains(@class, 'ui-datepicker-year')]",
                "//div[contains(@class, 'calendar')]//div[contains(@class, 'header')]",
                "//table[contains(@class, 'calendar')]//caption",
                "//div[contains(@class, 'calendar')]//div[contains(@class, 'title')]"
            ]
            
            for selector in month_year_selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element.is_displayed():
                        text = element.text
                        if text.strip():
                            logging.info(f"Mes/año actual: {text}")
                            return text
                except:
                    continue
            
            # Si no encontramos el título, buscar elementos que contengan meses
            month_texts = [
                "xaneiro", "febreiro", "marzo", "abril", "maio", "xuño",
                "xullo", "agosto", "setembro", "outubro", "novembro", "decembro",
                "january", "february", "march", "april", "may", "june",
                "july", "august", "september", "october", "november", "december"
            ]
            
            for month in month_texts:
                try:
                    element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{month}')]")
                    if element.is_displayed():
                        text = element.text
                        logging.info(f"Mes encontrado: {text}")
                        return text
                except:
                    continue
            
            return "Unknown"
            
        except Exception as e:
            logging.error(f"Error obteniendo mes/año actual: {e}")
            return "Unknown"
    
    def navigate_to_august_2025(self, next_arrow):
        """Navegar hasta agosto 2025 usando las flechas del calendario"""
        try:
            # Basándome en tu observación, solo necesitamos un clic para llegar a agosto 2025
            # desde julio 2025 (que es donde estamos actualmente)
            logging.info("Haciendo un clic en la flecha para navegar a agosto 2025...")
            
            # Buscar la flecha siguiente
            next_arrow_selectors = [
                "//a[contains(@class, 'ui-datepicker-next')]",
                "//a[contains(@class, 'next')]",
                "//button[contains(@class, 'next')]",
                "//span[contains(@class, 'next')]",
                "//i[contains(@class, 'next')]"
            ]
            
            next_arrow = None
            for selector in next_arrow_selectors:
                try:
                    next_arrow = self.driver.find_element(By.XPATH, selector)
                    if next_arrow.is_displayed():
                        logging.info(f"Flecha encontrada con selector: {selector}")
                        break
                except:
                    continue
            
            if not next_arrow:
                logging.error("No se pudo encontrar la flecha de navegación")
                return False
            
            # Hacer un solo clic en la flecha para ir a agosto 2025
            try:
                # Usar JavaScript directamente para evitar problemas de interceptación
                self.driver.execute_script("arguments[0].click();", next_arrow)
                logging.info("✅ Clic realizado en la flecha - navegando a agosto 2025")
                time.sleep(1)  # Reducido de 2 a 1 segundo
                return True
            except Exception as js_error:
                logging.error(f"Error al hacer clic con JavaScript: {js_error}")
                return False
            
        except Exception as e:
            logging.error(f"Error navegando a agosto 2025: {e}")
            return False
    
    def get_available_slots(self):
        """Obtener el número de plazas disponibles"""
        try:
            # Verificar si estamos en página de error antes de obtener slots
            if not self.check_and_handle_error_page():
                return 0
            
            # Buscar el elemento que muestra las plazas libres
            # Basándome en la imagen, parece estar en un panel derecho
            slots_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Prazas libres:')]"))
            )
            
            # Extraer el número de plazas
            slots_text = slots_element.text
            slots_number = int(slots_text.split(':')[1].strip())
            
            logging.info(f"Plazas disponibles: {slots_number}")
            return slots_number
            
        except NoSuchElementException:
            logging.warning("No se encontró información de plazas disponibles")
            return 0
        except Exception as e:
            logging.error(f"Error al obtener plazas disponibles: {e}")
            return 0
    
    def is_error_page(self):
        """Verificar si estamos en la página de error"""
        try:
            current_url = self.driver.current_url
            return "aceptacion" in current_url
        except:
            return False

    def check_and_handle_error_page(self):
        """Verificar si estamos en página de error y manejarla si es necesario"""
        if self.is_error_page():
            logging.warning("⚠️ Detectada página de error durante el flujo")
            if not self.handle_error_page():
                logging.error("❌ No se pudo manejar la página de error")
                return False
            return True
        return True

    def clear_browser_data(self):
        """Limpiar cache, cookies y datos del navegador"""
        try:
            logging.info("🧹 Limpiando cache, cookies y datos del navegador...")
            
            # Limpiar cache
            self.driver.execute_script("window.localStorage.clear();")
            self.driver.execute_script("window.sessionStorage.clear();")
            
            # Limpiar cookies
            self.driver.delete_all_cookies()
            
            # Limpiar cache del navegador
            self.driver.execute_script("""
                if ('caches' in window) {
                    caches.keys().then(function(names) {
                        for (let name of names) {
                            caches.delete(name);
                        }
                    });
                }
            """)
            
            logging.info("✅ Datos del navegador limpiados exitosamente")
            return True
            
        except Exception as e:
            logging.error(f"Error al limpiar datos del navegador: {e}")
            return False

    def reset_browser(self):
        """Resetear completamente el navegador"""
        try:
            logging.info("🔄 Reseteando navegador...")
            
            # Cerrar el driver actual
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.wait = None
                logging.info("✅ Driver anterior cerrado")
            
            # Pequeña pausa para asegurar que se cierre completamente
            time.sleep(2)
            
            # Configurar un nuevo driver
            if not self.setup_driver():
                logging.error("❌ Error al configurar nuevo driver")
                return False
            
            logging.info("✅ Navegador reseteado exitosamente")
            return True
            
        except Exception as e:
            logging.error(f"Error al resetear navegador: {e}")
            return False

    def handle_error_page(self):
        """Manejar página de error reseteando el navegador completamente"""
        try:
            # Verificar si estamos en la página de error
            current_url = self.driver.current_url
            if "aceptacion" not in current_url:
                return True  # No estamos en página de error
            
            logging.info("🔄 Detectada página de error inesperada")
            logging.info("🔄 Iniciando reset completo del navegador...")
            
            # Limpiar datos del navegador antes de resetear
            self.clear_browser_data()
            
            # Resetear completamente el navegador
            if not self.reset_browser():
                logging.error("❌ Error al resetear navegador")
                return False
            
            # Navegar nuevamente al sitio desde cero
            if not self.navigate_to_site():
                logging.error("❌ Error al navegar al sitio después del reset")
                return False
            
            logging.info("✅ Navegación reiniciada exitosamente después del reset")
            return True
                
        except Exception as e:
            logging.error(f"Error manejando página de error: {e}")
            return False
    
    def check_availability(self):
        """Verificar disponibilidad para la fecha objetivo"""
        try:
            if not self.setup_driver():
                return None
                
            if not self.navigate_to_site():
                return None
            
            # Hacer clic en Visitantes para Islas Cíes
            if not self.click_visitantes_cies():
                return None
            
            # Verificar si estamos en página de error después del clic
            current_url = self.driver.current_url
            if "aceptacion" in current_url:
                logging.warning("⚠️ Detectada página de error después del clic en Visitantes")
                if not self.handle_error_page():
                    logging.error("❌ No se pudo manejar la página de error")
                    return None
                
                # Después del reset, reiniciar completamente el flujo
                logging.info("🔄 Reiniciando flujo completo después del reset...")
                
                # Hacer clic en Visitantes para Islas Cíes nuevamente
                if not self.click_visitantes_cies():
                    logging.error("❌ Error al hacer clic en Visitantes después del reset")
                    return None
                
                # Verificar nuevamente si estamos en página de error
                current_url = self.driver.current_url
                if "aceptacion" in current_url:
                    logging.error("❌ Seguimos en página de error después del reset")
                    return None
                
            if not self.select_target_date():
                return None
                
            slots = self.get_available_slots()
            
            return {
                'date': TARGET_DATE,
                'available_slots': slots,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'has_availability': slots > 0
            }
            
        except Exception as e:
            logging.error(f"Error en verificación de disponibilidad: {e}")
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