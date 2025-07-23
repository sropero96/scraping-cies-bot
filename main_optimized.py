#!/usr/bin/env python3
"""
Bot optimizado de monitoreo de Islas Cíes
Usa scraper híbrido (Selenium + API directa)
"""

import logging
import time
import sys
import os
from datetime import datetime
from scraper_hybrid import HybridCiesScraper
from notifier import Notifier
from stats import BotStats
from config import TARGET_DATE, TARGET_URL

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot_optimized.log')
    ]
)

class OptimizedCiesMonitor:
    def __init__(self):
        self.scraper = HybridCiesScraper()
        self.notifier = Notifier()
        self.stats = BotStats()
        self.consecutive_errors = 0
        self.max_errors = 5
        self.last_check = None
        
    def check_availability(self):
        """Verificar disponibilidad usando scraper híbrido"""
        try:
            logging.info("=" * 50)
            logging.info("Iniciando verificación optimizada...")
            
            # Verificar disponibilidad
            result = self.scraper.check_availability_hybrid()
            
            if result is None:
                self.consecutive_errors += 1
                self.stats.record_attempt(0, had_error=True)
                logging.error(f"Error en verificación (intento {self.consecutive_errors}/{self.max_errors})")
                
                if self.consecutive_errors >= self.max_errors:
                    logging.critical("Demasiados errores consecutivos, deteniendo bot")
                    self.send_critical_error_notification()
                    return False
                
                return True
            
            # Resetear contador de errores si la verificación fue exitosa
            if self.consecutive_errors > 0:
                logging.info(f"✅ Verificación exitosa después de {self.consecutive_errors} errores")
                self.consecutive_errors = 0
            
            # Procesar resultado
            slots = result['available_slots']
            status = result['status']
            method = result['method']
            
            # Registrar estadísticas
            self.stats.record_attempt(slots, had_error=(slots == -1))
            
            # Manejar diferentes estados
            if slots == -1:
                # Error de detección
                logging.warning("⚠️ Error de detección de plazas")
                self.send_detection_error_notification(result)
            elif slots > 0:
                # ¡PLAZAS DISPONIBLES!
                logging.info(f"🎉 ¡PLAZAS DISPONIBLES ENCONTRADAS! ({slots} plazas)")
                self.send_availability_alert(slots, result)
            else:
                # No hay plazas disponibles
                logging.info(f"😔 No hay plazas disponibles (confirmado via {method})")
            
            # Enviar resumen horario si es necesario
            self.check_hourly_summary()
            
            return True
            
        except Exception as e:
            logging.error(f"Error en check_availability: {e}")
            self.consecutive_errors += 1
            return True
    
    def send_availability_alert(self, slots, result):
        """Enviar alerta de disponibilidad"""
        try:
            message = f"""
🚨 ¡PLAZAS DISPONIBLES ENCONTRADAS! 🚨

📅 Fecha: {result['date']}
🎫 Plazas disponibles: {slots}
⏰ Timestamp: {result['timestamp']}
🔧 Método: {result['method']}

🌐 Enlace directo: https://autorizacionillasatlanticas.xunta.gal/illasr/iniciarReserva

¡Actúa rápido antes de que se agoten!
            """.strip()
            
            # Usar el notificador existente
            alert_result = {
                'available_slots': slots,
                'date': result['date'],
                'timestamp': result['timestamp'],
                'method': result['method']
            }
            
            if self.notifier.send_alert(alert_result):
                logging.info("✅ Alertas de disponibilidad enviadas")
            else:
                logging.error("❌ Error enviando alertas de disponibilidad")
            
        except Exception as e:
            logging.error(f"Error enviando alertas de disponibilidad: {e}")
    
    def send_detection_error_notification(self, result):
        """Enviar notificación de error de detección"""
        try:
            message = f"""
⚠️ Error de Detección Técnica

📅 Fecha objetivo: {result['date']}
⏰ Timestamp: {result['timestamp']}
🔧 Método: {result['method']}

El bot no pudo obtener información de plazas debido a un problema técnico.
Esto puede ser temporal. El bot continuará monitoreando automáticamente.

🔄 Acciones automáticas:
- El bot se reiniciará automáticamente
- Continuará monitoreando cada segundo
- Se enviará otra notificación si el problema persiste

No es necesario que hagas nada manualmente.
            """.strip()
            
            # Enviar solo por Telegram para errores técnicos
            self.notifier.send_telegram_critical_alert(message)
            
            logging.info("✅ Notificación de error de detección enviada")
            
        except Exception as e:
            logging.error(f"Error enviando notificación de error: {e}")
    
    def send_critical_error_notification(self):
        """Enviar notificación de error crítico"""
        try:
            stats_summary = self.stats.get_summary()
            
            message = f"""
🚨 ERROR CRÍTICO - BOT DETENIDO

❌ El bot se ha detenido debido a demasiados errores consecutivos.

📊 Estadísticas de la sesión:
{stats_summary}

🔄 Para reiniciar el bot:
1. Ve a la terminal donde está corriendo
2. Presiona Ctrl+C para detenerlo
3. Ejecuta: python3 main_optimized.py

⚠️ El bot NO se reiniciará automáticamente.
            """.strip()
            
            self.notifier.send_telegram_critical_alert(message)
            self.notifier.send_email_alert({
                'date': TARGET_DATE,
                'available_slots': 0,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            logging.info("✅ Notificación de error crítico enviada")
            
        except Exception as e:
            logging.error(f"Error enviando notificación crítica: {e}")
    
    def check_hourly_summary(self):
        """Verificar si es hora de enviar resumen horario"""
        current_time = datetime.now()
        
        # Enviar resumen cada hora (minuto 0)
        if current_time.minute == 0 and self.last_check != current_time.hour:
            self.send_hourly_summary()
            self.last_check = current_time.hour
    
    def send_hourly_summary(self):
        """Enviar resumen horario"""
        try:
            stats_summary = self.stats.get_summary()
            
            message = f"""
📊 Resumen Horario - Bot Islas Cíes

⏰ Hora: {datetime.now().strftime('%H:%M')}
📅 Fecha objetivo: {TARGET_DATE}

{stats_summary}

🤖 El bot continúa monitoreando automáticamente.
            """.strip()
            
            self.notifier.send_telegram_summary(message)
            
            logging.info("✅ Resumen horario enviado")
            
        except Exception as e:
            logging.error(f"Error enviando resumen horario: {e}")
    
    def run(self):
        """Ejecutar el bot optimizado"""
        logging.info("🚀 Iniciando bot optimizado de Islas Cíes...")
        logging.info(f"📅 Fecha objetivo: {TARGET_DATE}")
        logging.info(f"⏱️ Intervalo de verificación: 1 segundo")
        logging.info(f"🛑 Máximo errores consecutivos: {self.max_errors}")
        
        # Enviar notificación de inicio
        try:
            start_message = f"""
🤖 Bot Optimizado Iniciado

📅 Fecha objetivo: {TARGET_DATE}
⏱️ Intervalo: 1 segundo
🔧 Método: Híbrido (Selenium + API)

El bot comenzará a monitorear automáticamente.
            """.strip()
            
            self.notifier.send_telegram_summary(start_message)
            
        except Exception as e:
            logging.error(f"Error enviando notificación de inicio: {e}")
        
        try:
            while True:
                if not self.check_availability():
                    break
                
                # Esperar antes de la siguiente verificación
                time.sleep(1)
                
        except KeyboardInterrupt:
            logging.info("🛑 Bot detenido por el usuario")
            
            # Enviar notificación de parada
            try:
                stop_message = f"""
🛑 Bot Detenido Manualmente

⏰ Hora de parada: {datetime.now().strftime('%H:%M:%S')}
📊 Estadísticas finales:
{self.stats.get_summary()}
                """.strip()
                
                self.notifier.send_telegram_summary(stop_message)
                
            except Exception as e:
                logging.error(f"Error enviando notificación de parada: {e}")
        
        except Exception as e:
            logging.error(f"Error inesperado en el bot: {e}")
            self.send_critical_error_notification()

def main():
    """Función principal"""
    monitor = OptimizedCiesMonitor()
    monitor.run()

if __name__ == "__main__":
    main() 