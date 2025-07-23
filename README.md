# 🤖 Bot de Monitoreo de Islas Cíes

Bot automatizado para monitorear la disponibilidad de autorizaciones para visitar las Islas Cíes en la web oficial de la Xunta de Galicia.

## 🎯 Características

- **Monitoreo continuo** sin intervalos de espera
- **Detección robusta** de plazas disponibles con múltiples estrategias
- **Manejo inteligente de errores** con distinción entre "0 plazas reales" vs "error de detección"
- **Notificaciones automáticas** por Telegram y Gmail
- **Anti-detección avanzado** con rotación de User-Agents y comportamiento humano
- **Recuperación automática** de páginas de error
- **Estadísticas detalladas** y reportes horarios
- **Screenshots automáticos** para debugging

## 🚀 Instalación

### Prerrequisitos
- Python 3.8+
- Chrome/Chromium browser
- Cuenta de Telegram (opcional)
- Cuenta de Gmail (opcional)

### Configuración

1. **Clonar el repositorio:**
```bash
git clone https://github.com/sropero96/scraping-cies-bot.git
cd scraping-cies-bot
```

2. **Crear entorno virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

## ⚙️ Configuración

### Variables de Entorno (.env)

```env
# Telegram (opcional)
TELEGRAM_BOT_TOKEN=tu_token_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui

# Gmail (opcional)
GMAIL_USER=tu_email@gmail.com
GMAIL_PASSWORD=tu_password_de_aplicacion

# Configuración del bot
TARGET_DATE=02/08/2025
TARGET_URL=https://autorizacionillasatlanticas.xunta.gal/illasr/inicio
```

### Agregar Usuarios de Telegram

```bash
# Agregar un usuario
python3 add_telegram_user.py

# Ver usuarios registrados
python3 list_telegram_users.py
```

## 🏃‍♂️ Uso

### Ejecutar el Bot

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar bot en modo continuo
python3 main.py
```

### Scripts de Prueba

```bash
# Probar detección de plazas
python3 test_slots_detection.py

# Probar notificaciones de error
python3 test_error_notifications.py

# Probar anti-detección
python3 test_anti_detection.py
```

### Detener el Bot

```bash
# En la terminal donde corre el bot: Ctrl+C
# O buscar el proceso:
ps aux | grep python3
kill <PID>
```

## 🔧 Características Técnicas

### Manejo de Errores Inteligente

El bot distingue entre diferentes tipos de resultados:

- **`slots > 0`**: Plazas disponibles encontradas
- **`slots == 0`**: No hay plazas disponibles (confirmado)
- **`slots == -1`**: Error de detección (problema técnico)

### Notificaciones Automáticas

- **Plazas disponibles**: Alerta inmediata a todos los usuarios
- **Error de detección**: Notificación técnica con detalles del problema
- **Errores críticos**: Alerta cuando el bot se detiene por demasiados errores
- **Reportes horarios**: Resumen de actividad cada hora

### Anti-Detección

- Rotación automática de User-Agents
- Delays aleatorios entre acciones
- Simulación de movimientos de mouse humanos
- Headers adicionales para parecer navegador real
- Limpieza automática de cache y cookies

### Recuperación Automática

- Detección de páginas de error (`/aceptacion`)
- Reset completo del navegador cuando es necesario
- Limpieza de cache y cookies automática
- Reintentos automáticos sin interrupción

## 📊 Monitoreo y Logs

### Logs en Tiempo Real

```bash
# Ver logs en tiempo real
tail -f bot.log

# Ver solo errores
grep "ERROR" bot.log

# Ver solo alertas
grep "ALERT" bot.log
```

### Screenshots Automáticos

El bot toma screenshots automáticamente para debugging:
- `home_page.png`: Página de inicio
- `page_structure.png`: Estructura de la página de solicitud
- `slots_debug.png`: Debugging de detección de plazas
- `error_slots.png`: Error en detección de plazas

### Estadísticas

```bash
# Ver estadísticas del bot
python3 stats.py
```

## 🛠️ Solución de Problemas

### Error de Detección de Plazas

Si el bot reporta errores de detección frecuentes:

1. **Verificar screenshots**: Revisar `slots_debug.png` y `error_slots.png`
2. **Probar detección manual**: Ejecutar `python3 test_slots_detection.py`
3. **Verificar cambios en el sitio**: El sitio puede haber cambiado su estructura

### Problemas de Conexión

```bash
# Verificar conectividad
curl -I https://autorizacionillasatlanticas.xunta.gal/illasr/inicio

# Probar con diferentes User-Agents
python3 test_anti_detection.py
```

### Errores de Credenciales

```bash
# Verificar configuración de Telegram
python3 test_telegram.py

# Verificar configuración de Gmail
python3 test_gmail.py
```

## 📈 Estado del Proyecto

- ✅ **Monitoreo básico**: Funcionando
- ✅ **Detección de plazas**: Funcionando con múltiples estrategias
- ✅ **Notificaciones Telegram**: Funcionando
- ✅ **Notificaciones Gmail**: Funcionando (requiere configuración)
- ✅ **Anti-detección**: Funcionando
- ✅ **Manejo de errores**: Funcionando
- ✅ **Recuperación automática**: Funcionando
- ✅ **Estadísticas**: Funcionando
- ✅ **Reportes horarios**: Funcionando

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ⚠️ Disclaimer

Este bot es para uso educativo y personal. Respeta los términos de servicio del sitio web objetivo y no sobrecargues sus servidores.

## 🔗 Enlaces Útiles

- [Sitio oficial de autorizaciones](https://autorizacionillasatlanticas.xunta.gal/illasr/inicio)
- [Documentación de Telegram Bot API](https://core.telegram.org/bots/api)
- [Documentación de Selenium](https://selenium-python.readthedocs.io/)