# 🤖 Bot de Monitoreo de Islas Cíes - Versión Optimizada

Bot automatizado para monitorear la disponibilidad de autorizaciones para visitar las Islas Cíes en la web oficial de la Xunta de Galicia.

## 🎯 Características

- **Monitoreo continuo** sin intervalos de espera
- **Enfoque híbrido optimizado** (Selenium + API directa)
- **Detección robusta** de plazas disponibles con múltiples estrategias
- **Manejo inteligente de errores** con distinción entre "0 plazas reales" vs "error de detección"
- **Notificaciones automáticas** por Telegram y Gmail
- **Anti-detección avanzado** con rotación de User-Agents y comportamiento humano
- **Recuperación automática** de páginas de error
- **Estadísticas detalladas** y reportes horarios
- **Screenshots automáticos** para debugging

## 🚀 Optimizaciones Implementadas

### **Análisis de Tráfico HAR**
- ✅ **API directa identificada**: `recuperarPlazasTotales`
- ✅ **Parámetros exactos** extraídos del tráfico real
- ✅ **Headers necesarios** (CSRF token, Referer, Origin)
- ✅ **Respuesta JSON estructurada** con información completa

### **Scraper Híbrido**
- ✅ **Navegación Selenium** para establecer sesión
- ✅ **Llamadas API directas** para obtener datos
- ✅ **Transferencia de cookies** entre Selenium y Requests
- ✅ **CSRF token automático** desde la página
- ✅ **Respuesta JSON completa** con plazas y mareas

### **Ventajas del Enfoque Híbrido**
- **Más rápido**: API directa vs scraping HTML
- **Más confiable**: Respuesta JSON estructurada
- **Más información**: Datos de mareas y estado del día
- **Menos detección**: Menos interacción con la UI
- **Mejor rendimiento**: Menos carga en el servidor

## 🚀 Instalación

### Prerrequisitos
- Python 3.8+
- Chrome/Chromium browser
- Cuenta de Telegram (opcional)
- Cuenta de Gmail (opcional)

### Configuración

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd SCRAPING-CIES
```

2. **Crear entorno virtual**:
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

## 📋 Configuración

### Archivo `.env`
```env
# Configuración del bot
TARGET_DATE=02/08/2025
CHECK_INTERVAL=1
MAX_CONSECUTIVE_ERRORS=5

# Telegram (opcional)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Gmail (opcional)
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
```

## 🚀 Uso

### Bot Original (Scraping HTML)
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar bot original
python3 main.py
```

### Bot Optimizado (Híbrido)
```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar bot optimizado
python3 main_optimized.py
```

### Scripts de Prueba

```bash
# Probar detección de plazas
python3 test_slots_detection.py

# Probar scraper optimizado
python3 test_optimized_scraper.py

# Probar scraper híbrido
python3 test_hybrid_scraper.py

# Probar notificaciones de error
python3 test_error_notifications.py
```

## 📊 Monitoreo

### Ver logs en tiempo real
```bash
tail -f bot.log
tail -f bot_optimized.log
```

### Verificar que está corriendo
```bash
ps aux | grep python3
```

### Detener el bot
```bash
# En la terminal donde corre el bot
Ctrl+C
```

## 🔧 Arquitectura

### **Scrapers Disponibles**

1. **`scraper.py`** - Scraper original (HTML)
   - Navegación completa con Selenium
   - Scraping de elementos HTML
   - Manejo de páginas de error

2. **`scraper_optimized.py`** - Scraper optimizado (API directa)
   - Llamadas directas a la API
   - Requiere CSRF token
   - Más rápido pero menos confiable

3. **`scraper_hybrid.py`** - Scraper híbrido (Recomendado)
   - Combina lo mejor de ambos enfoques
   - Navegación Selenium + API directa
   - Transferencia automática de cookies

### **Flujo del Bot Híbrido**

1. **Navegación inicial** → Página de inicio
2. **Clic en Visitantes** → Página de solicitud
3. **Obtención CSRF token** → Desde meta tags
4. **Transferencia de cookies** → Selenium → Requests
5. **Llamada API directa** → `recuperarPlazasTotales`
6. **Procesamiento JSON** → Extracción de plazas
7. **Notificaciones** → Telegram/Gmail según resultado

## 📈 Estadísticas

El bot registra automáticamente:
- ✅ Intentos exitosos
- ❌ Errores de detección
- 📊 Tiempo promedio de respuesta
- 🎯 Tasa de éxito
- 📅 Resúmenes horarios

## 🔔 Notificaciones

### **Tipos de Notificaciones**

1. **Alerta de Disponibilidad** 🚨
   - Cuando se encuentran plazas disponibles
   - Incluye enlace directo
   - Envío inmediato

2. **Error de Detección** ⚠️
   - Problemas técnicos temporales
   - El bot continúa automáticamente
   - Información para debugging

3. **Error Crítico** 🚨
   - Demasiados errores consecutivos
   - El bot se detiene
   - Instrucciones para reiniciar

4. **Resumen Horario** 📊
   - Estadísticas cada hora
   - Estado del monitoreo
   - Confirmación de funcionamiento

## 🛠️ Troubleshooting

### **Problemas Comunes**

1. **Error de ChromeDriver**
   ```bash
   # Actualizar ChromeDriver
   brew install chromedriver  # macOS
   ```

2. **Error de dependencias**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Error de notificaciones**
   - Verificar credenciales en `.env`
   - Comprobar conexión a internet

4. **Bot detectado como bot**
   - El bot incluye anti-detección avanzado
   - Si persiste, aumentar delays

### **Logs de Debug**

```bash
# Ver logs detallados
tail -f bot_optimized.log

# Buscar errores específicos
grep "ERROR" bot_optimized.log
grep "WARNING" bot_optimized.log
```

## 📝 Changelog

### **v2.0 - Optimización HAR**
- ✅ Análisis completo del tráfico HAR
- ✅ Identificación de API directa
- ✅ Scraper híbrido implementado
- ✅ Transferencia automática de cookies
- ✅ Respuesta JSON estructurada
- ✅ Información adicional de mareas

### **v1.5 - Mejoras de Detección**
- ✅ Distinción entre "0 plazas" vs "error de detección"
- ✅ Notificaciones automáticas de errores técnicos
- ✅ Screenshots automáticos para debugging
- ✅ Múltiples estrategias de detección

### **v1.0 - Versión Inicial**
- ✅ Monitoreo básico con Selenium
- ✅ Notificaciones por Telegram y Gmail
- ✅ Anti-detección básico
- ✅ Manejo de páginas de error

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## ⚠️ Disclaimer

Este bot es para uso educativo y personal. Respeta los términos de servicio del sitio web y no sobrecargues sus servidores.

---

**¡Que tengas suerte consiguiendo tus plazas para las Islas Cíes!** 🏝️