#!/usr/bin/env python3
"""
Bot de monitoreo para autorizaciones de Islas Cíes
Monitorea la disponibilidad de plazas para una fecha específica
"""

import time
import schedule
import logging
from datetime import datetime, timedelta
from scraper import CiesScraper
from notifier import Notifier
from stats import BotStats
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

class CiesMonitor:
    def __init__(self):
        self.scraper = CiesScraper()
        self.notifier = Notifier()
        self.stats = BotStats()
        self.last_check = None
        self.consecutive_errors = 0
        self.max_errors = 5
        self.last_hourly_report = datetime.now().replace(minute=0, second=0, microsecond=0)
        
    def check_availability(self):
        """Verificar disponibilidad y enviar alertas si es necesario"""
        try:
            logging.info("=" * 50)
            logging.info("Iniciando verificación de disponibilidad...")
            
            # Verificar disponibilidad
            result = self.scraper.check_availability()
            
            if result is None:
                self.consecutive_errors += 1
                self.stats.record_attempt(0, had_error=True)
                logging.error(f"Error en verificación (intento {self.consecutive_errors}/{self.max_errors})")
                
                if self.consecutive_errors >= self.max_errors:
                    logging.critical("Demasiados errores consecutivos. Deteniendo el bot.")
                    return False
                return True
            
            # Resetear contador de errores si la verificación fue exitosa
            self.consecutive_errors = 0
            
            # Registrar estadísticas
            self.stats.record_attempt(result['available_slots'], had_error=False)
            
            # Mostrar resultado
            logging.info(f"Resultado: {result['available_slots']} plazas disponibles para {result['date']}")
            
            # Verificar si hay disponibilidad
            if result['has_availability']:
                logging.info("🎉 ¡PLAZAS DISPONIBLES ENCONTRADAS! Enviando alertas...")
                
                # Enviar alertas
                if self.notifier.send_alert(result):
                    logging.info("✅ Alertas enviadas exitosamente")
                else:
                    logging.error("❌ Error al enviar alertas")
            else:
                logging.info("😔 No hay plazas disponibles aún...")
            
            self.last_check = datetime.now()
            
            # Verificar si es hora de enviar resumen horario
            self.check_hourly_report()
            
            return True
            
        except Exception as e:
            logging.error(f"Error inesperado en check_availability: {e}")
            self.stats.record_attempt(0, had_error=True)
            return True
    
    def check_hourly_report(self):
        """Verificar si es hora de enviar resumen horario"""
        current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
        
        # Si ha pasado una hora desde el último reporte
        if current_hour > self.last_hourly_report:
            try:
                # Obtener resumen de la hora anterior
                previous_hour_summary = self.stats.get_previous_hour_summary()
                
                if previous_hour_summary:
                    summary_text = self.stats.format_hourly_summary(
                        previous_hour_summary, 
                        f"Hora {self.last_hourly_report.strftime('%H:00')}"
                    )
                    
                    # Enviar resumen por Telegram
                    if self.notifier.send_telegram_summary(summary_text):
                        logging.info("✅ Resumen horario enviado por Telegram")
                    else:
                        logging.error("❌ Error al enviar resumen horario")
                
                # Actualizar hora del último reporte
                self.last_hourly_report = current_hour
                
                # Limpiar datos antiguos (más de 7 días)
                self.stats.cleanup_old_data(days_to_keep=7)
                
            except Exception as e:
                logging.error(f"Error al enviar resumen horario: {e}")
    
    def run_continuous(self):
        """Ejecutar monitoreo continuo sin intervalos"""
        logging.info("🚀 Iniciando bot de monitoreo de Islas Cíes")
        logging.info(f"📅 Fecha objetivo: {TARGET_DATE}")
        logging.info(f"⚡ Modo: Verificación continua (sin intervalos)")
        logging.info(f"🌐 URL objetivo: {TARGET_URL}")
        
        # Ejecutar verificación inicial
        self.check_availability()
        
        # Loop principal - ejecutar continuamente sin esperar
        try:
            while True:
                # Ejecutar verificación inmediatamente
                if not self.check_availability():
                    logging.critical("🛑 Bot detenido debido a errores críticos")
                    break
                
                # Pequeña pausa para no saturar el servidor (1 segundo)
                time.sleep(1)
                
        except KeyboardInterrupt:
            logging.info("🛑 Bot detenido por el usuario")
        except Exception as e:
            logging.error(f"Error en el loop principal: {e}")
        finally:
            # Determinar si fue un error crítico o detención manual
            critical_error = self.consecutive_errors >= self.max_errors
            self.cleanup(critical_error=critical_error)
    
    def run_once(self):
        """Ejecutar una sola verificación"""
        logging.info("🔍 Ejecutando verificación única...")
        return self.check_availability()
    
    def cleanup(self, critical_error=False):
        """Limpiar recursos"""
        try:
            # Enviar alerta de error crítico si es necesario
            if critical_error:
                self.send_critical_error_alert()
            
            self.notifier.close()
            logging.info("🧹 Recursos limpiados")
        except Exception as e:
            logging.error(f"Error en cleanup: {e}")
    
    def send_critical_error_alert(self):
        """Enviar alerta de error crítico por Telegram"""
        try:
            error_message = f"""
🚨 **BOT DETENIDO POR ERRORES CRÍTICOS** 🚨

🤖 El bot de monitoreo de Islas Cíes se ha detenido automáticamente debido a errores consecutivos.

⚠️ **Detalles:**
- Errores consecutivos: {self.consecutive_errors}/{self.max_errors}
- Última verificación: {self.last_check.strftime('%Y-%m-%d %H:%M:%S') if self.last_check else 'N/A'}
- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🔄 **Acción requerida:**
Reinicia el bot manualmente para continuar el monitoreo.

📊 **Estadísticas de la sesión:**
{self.stats.get_session_summary()}

🔗 Repositorio: https://github.com/sropero96/scraping-cies-bot
            """
            
            if self.notifier.send_telegram_critical_alert(error_message):
                logging.info("✅ Alerta de error crítico enviada por Telegram")
            else:
                logging.error("❌ Error al enviar alerta de error crítico")
                
        except Exception as e:
            logging.error(f"Error al enviar alerta de error crítico: {e}")

def main():
    """Función principal"""
    monitor = CiesMonitor()
    
    # Verificar configuración
    if not GMAIL_ADDRESS or not GMAIL_PASSWORD:
        logging.warning("⚠️  Configuración de email incompleta")
    
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        logging.warning("⚠️  Configuración de WhatsApp incompleta")
    
    # Ejecutar monitoreo
    monitor.run_continuous()

if __name__ == "__main__":
    main()