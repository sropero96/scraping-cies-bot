import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del sitio web
TARGET_URL = "https://autorizacionillasatlanticas.xunta.gal/illasr/inicio"
TARGET_DATE = "02/08/2025"  # Formato DD/MM/YYYY
CHECK_INTERVAL = 30  # segundos

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
HEADLESS = True  # Activado con configuraciones avanzadas
BROWSER_TIMEOUT = 10  # segundos