# 🤖 Bot de Monitoreo - Islas Cíes

Bot automatizado para monitorear la disponibilidad de autorizaciones de visita a las Islas Cíes en Vigo, España.

## 🏝️ Descripción

Este bot monitorea continuamente el sitio web oficial de autorizaciones de las Islas Atlánticas para detectar cuando hay plazas disponibles para una fecha específica (por defecto: 2 de agosto de 2025).

### ✨ Características

- 🔍 **Monitoreo continuo** sin intervalos de espera
- 📱 **Alertas por Telegram** a múltiples usuarios
- 📊 **Estadísticas horarias** automáticas
- 🕵️ **Modo headless** (sin abrir ventana del navegador)
- 🛡️ **Anti-detección** con configuraciones avanzadas
- 📈 **Logs detallados** para debugging
- 🔄 **Reset automático del navegador** en caso de errores
- 🧹 **Limpieza de cache y cookies** para evitar problemas de sesión

### 🛠️ Mejoras de Robustez

- **Detección automática de páginas de error**: El bot detecta cuando es redirigido a páginas de error inesperadas
- **Reset completo del navegador**: En lugar de intentar navegar de vuelta, resetea completamente el navegador
- **Limpieza de datos**: Elimina cache, cookies y datos de sesión antes de reiniciar
- **Verificaciones múltiples**: Revisa la página de error en puntos críticos del flujo
- **Recuperación automática**: Reinicia la navegación desde cero después de un reset

### 🕵️ Configuraciones Anti-Detección

- **User-Agents rotativos**: Usa diferentes user-agents en cada sesión para evitar detección
- **Delays aleatorios**: Simula comportamiento humano con pausas aleatorias
- **Clics humanos**: Simula movimientos de mouse y clics naturales
- **Headers adicionales**: Incluye headers de idioma y aceptación apropiados
- **Scroll aleatorio**: Simula navegación humana con scrolls aleatorios
- **Ocultación de automatización**: Elimina indicadores de que es un bot
- **Configuraciones avanzadas**: Desactiva características que pueden delatar automatización

## �� Instalación

### Prerrequisitos

- Python 3.8+
- Chrome/Chromium instalado
- Cuenta de Telegram Bot

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/sropero96/scraping-cies-bot.git
cd scraping-cies-bot
```

2. **Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

## ⚙️ Configuración

### 1. Configurar Telegram Bot

1. Crear un bot con [@BotFather](https://t.me/botfather) en Telegram
2. Obtener el token del bot
3. Ejecutar el script de configuración:
```bash
python3 setup_telegram.py
```

### 2. Configurar segundo usuario (opcional)

```bash
python3 add_second_user.py
```

### 3. Variables de entorno (.env)

```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=tu_token_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui
TELEGRAM_CHAT_ID_2=segundo_chat_id_aqui

# Configuración del bot
TARGET_DATE=02/08/2025
CHECK_INTERVAL=30

# Email (opcional)
GMAIL_ADDRESS=tu_email@gmail.com
GMAIL_PASSWORD=tu_password_de_aplicacion

# Twilio WhatsApp (opcional)
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+14155238886
WHATSAPP_PHONE_NUMBER=whatsapp:+34600000000
```

## 🎯 Uso

### Ejecutar el bot

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar en primer plano
python3 main.py

# Ejecutar en segundo plano
nohup python3 main.py > bot_output.log 2>&1 &
```

### Scripts de utilidad

```bash
# Probar notificaciones
python3 test_notifications.py

# Probar scraper
python3 test_scraper.py

# Probar estadísticas
python3 test_stats.py

# Obtener Chat ID de Telegram
python3 get_chat_id.py
```

## 📁 Estructura del proyecto

```
scraping-cies-bot/
├── main.py              # Punto de entrada principal
├── scraper.py           # Lógica de scraping web
├── notifier.py          # Sistema de notificaciones
├── stats.py             # Gestión de estadísticas
├── config.py            # Configuración del bot
├── setup_telegram.py    # Configuración de Telegram
├── add_second_user.py   # Agregar usuarios adicionales
├── test_*.py           # Scripts de prueba
├── requirements.txt     # Dependencias
├── .env.example        # Template de variables de entorno
├── .gitignore          # Archivos a ignorar
└── README.md           # Este archivo
```

## 🔧 Configuración avanzada

### Modo headless

El bot funciona por defecto en modo headless. Para desactivarlo, edita `config.py`:

```python
HEADLESS_MODE = False
```

### Cambiar fecha objetivo

Edita `config.py` o la variable de entorno:

```python
TARGET_DATE = "15/08/2025"  # Cambiar fecha
```

### Personalizar intervalos

```python
CHECK_INTERVAL = 10  # Verificar cada 10 segundos
```

## 📊 Monitoreo

### Logs

Los logs se guardan en `cies_monitor.log`:

```bash
# Ver logs en tiempo real
tail -f cies_monitor.log

# Ver últimas líneas
tail -20 cies_monitor.log
```

### Estadísticas

El bot genera estadísticas automáticamente:
- Intentos de verificación
- Plazas disponibles encontradas
- Errores y excepciones
- Resúmenes horarios

### Procesos

```bash
# Verificar que el bot esté ejecutándose
ps aux | grep "python3 main.py" | grep -v grep

# Detener el bot
pkill -f "python3 main.py"
```

## 🚨 Alertas

### Telegram

- **Alertas inmediatas**: Cuando se encuentran plazas disponibles
- **Resúmenes horarios**: Cada hora en punto
- **Múltiples usuarios**: Soporte para varios destinatarios

### Formato de alertas

```
🏝️ ¡PLAZAS DISPONIBLES EN ISLAS CÍES! 🏝️

📅 Fecha: 02/08/2025
🎫 Plazas: 5
⏰ Verificado: 2025-07-23 17:30:15

🔗 https://autorizacionillasatlanticas.xunta.gal/illasr/inicio

¡Reserva ahora antes de que se agoten!
```

## 🧪 Pruebas

### Probar funciones de reset del navegador

Para verificar que las nuevas funciones de reset y limpieza funcionan correctamente:

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar pruebas de reset del navegador
python3 test_browser_reset.py
```

Este script prueba:
- Detección de páginas de error
- Reset completo del navegador
- Limpieza de cache y cookies
- Recuperación automática

### Probar configuraciones anti-detección

Para verificar que las configuraciones anti-detección funcionan:

```bash
# Ejecutar pruebas de anti-detección
python3 test_anti_detection.py
```

Este script prueba:
- Configuraciones anti-detección del WebDriver
- Rotación de user-agents
- Comportamientos humanos (delays, scrolls)
- Clics humanos
- Ocultación de indicadores de automatización

### Otras pruebas disponibles

```bash
# Probar notificaciones
python3 test_notifications.py

# Probar estadísticas
python3 test_stats.py

# Probar manejo de errores
python3 test_error_handling.py
```

## 🛠️ Troubleshooting

### Problemas comunes

1. **Error de ChromeDriver**
   ```bash
   pip install webdriver-manager
   ```

2. **Error de credenciales de Telegram**
   - Verificar token del bot
   - Ejecutar `python3 setup_telegram.py`

3. **Bot no encuentra elementos**
   - Verificar que el sitio web no haya cambiado
   - Revisar logs para errores específicos

4. **Modo headless no funciona**
   - Desactivar temporalmente: `HEADLESS_MODE = False`
   - Verificar configuración de Chrome

### Debugging

```bash
# Ejecutar en modo debug
python3 test_scraper.py

# Ver screenshots generados
ls -la *.png
```

## 📝 Licencia

Este proyecto es de uso personal. No se garantiza su funcionamiento continuo.

## 🤝 Contribuciones

Este es un proyecto personal, pero las sugerencias son bienvenidas.

## ⚠️ Disclaimer

Este bot es para uso personal y educativo. Respeta los términos de servicio del sitio web objetivo y no lo uses para actividades maliciosas.

---

**Desarrollado con ❤️ para monitorear las Islas Cíes**