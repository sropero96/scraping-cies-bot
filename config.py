import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del sitio web
TARGET_URL = "https://autorizacionillasatlanticas.xunta.gal/illasr/inicio"
TARGET_DATE = "02/08/2025"  # Formato DD/MM/YYYY
CHECK_INTERVAL = 10  # segundos (aumentado para reducir detección)

# Configuración de alertas críticas
CRITICAL_ERROR_THRESHOLD = 600  # intentos sin éxito (10 minutos a 1s)
CRITICAL_ERROR_TIME_THRESHOLD = 600  # segundos sin éxito (10 minutos)

# Configuración de Gmail
GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS', '')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD', '')  # App password de Gmail
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', '')

# Configuración de Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
TELEGRAM_CHAT_ID_2 = os.getenv('TELEGRAM_CHAT_ID_2', '')  # Segundo usuario

# Configuración de Twilio (WhatsApp)
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER', '')  # Número de Twilio
RECIPIENT_WHATSAPP = os.getenv('RECIPIENT_WHATSAPP', '')  # Tu número de WhatsApp

# Configuración del navegador
HEADLESS = False  # Cambiado a False para evitar detección
BROWSER_TIMEOUT = 20  # segundos (aumentado para más estabilidad)

# Configuración anti-detección mejorada
USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'
]

# Delays aleatorios mejorados
MIN_DELAY = 3  # segundos mínimo entre acciones
MAX_DELAY = 12  # segundos máximo entre acciones

# Configuración de reintentos
MAX_RETRIES = 3  # máximo reintentos por sesión
RETRY_DELAY = 30  # segundos entre reintentos