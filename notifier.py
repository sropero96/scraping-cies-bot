import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import logging
from config import *

class Notifier:
    def __init__(self):
        self.setup_email()
        self.setup_telegram()
        self.setup_whatsapp()
    
    def setup_email(self):
        """Configurar cliente de email"""
        try:
            self.smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.smtp_server.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
            logging.info("Cliente de email configurado correctamente")
        except Exception as e:
            logging.error(f"Error al configurar email: {e}")
            self.smtp_server = None
    
    def setup_telegram(self):
        """Configurar cliente de Telegram"""
        try:
            if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
                self.telegram_bot_token = TELEGRAM_BOT_TOKEN
                self.telegram_chat_ids = [TELEGRAM_CHAT_ID]
                
                # Agregar segundo usuario si está configurado
                if TELEGRAM_CHAT_ID_2:
                    self.telegram_chat_ids.append(TELEGRAM_CHAT_ID_2)
                
                logging.info(f"Cliente de Telegram configurado correctamente para {len(self.telegram_chat_ids)} usuario(s)")
            else:
                self.telegram_bot_token = None
                self.telegram_chat_ids = []
                logging.warning("Credenciales de Telegram no configuradas")
        except Exception as e:
            logging.error(f"Error al configurar Telegram: {e}")
            self.telegram_bot_token = None
            self.telegram_chat_ids = []
    
    def setup_whatsapp(self):
        """Configurar cliente de WhatsApp (Twilio)"""
        try:
            if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
                self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
                logging.info("Cliente de WhatsApp configurado correctamente")
            else:
                self.twilio_client = None
                logging.warning("Credenciales de Twilio no configuradas")
        except Exception as e:
            logging.error(f"Error al configurar WhatsApp: {e}")
            self.twilio_client = None
    
    def send_email_alert(self, availability_data):
        """Enviar alerta por email"""
        if not self.smtp_server or not RECIPIENT_EMAIL:
            logging.warning("Email no configurado o destinatario no especificado")
            return False
        
        try:
            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = GMAIL_ADDRESS
            msg['To'] = RECIPIENT_EMAIL
            msg['Subject'] = f"🎉 PLAZAS DISPONIBLES - Islas Cíes {availability_data['date']}"
            
            # Contenido del mensaje
            body = f"""
            🏝️ ¡PLAZAS DISPONIBLES EN ISLAS CÍES! 🏝️
            
            📅 Fecha: {availability_data['date']}
            🎫 Plazas disponibles: {availability_data['available_slots']}
            ⏰ Verificado: {availability_data['timestamp']}
            
            🔗 Enlace directo: {TARGET_URL}
            
            ¡Reserva ahora antes de que se agoten!
            
            ---
            Bot de monitoreo Cíes
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Enviar email
            self.smtp_server.send_message(msg)
            logging.info(f"Alerta por email enviada a {RECIPIENT_EMAIL}")
            return True
            
        except Exception as e:
            logging.error(f"Error al enviar email: {e}")
            return False
    
    def send_telegram_alert(self, availability_data):
        """Enviar alerta por Telegram a todos los usuarios"""
        if not self.telegram_bot_token or not self.telegram_chat_ids:
            logging.warning("Telegram no configurado")
            return False
        
        try:
            # Crear mensaje
            message_body = f"""
🏝️ ¡PLAZAS DISPONIBLES EN ISLAS CÍES! 🏝️

📅 Fecha: {availability_data['date']}
🎫 Plazas: {availability_data['available_slots']}
⏰ Verificado: {availability_data['timestamp']}

🔗 {TARGET_URL}

¡Reserva ahora antes de que se agoten!
            """
            
            success_count = 0
            # Enviar mensaje a todos los usuarios
            for chat_id in self.telegram_chat_ids:
                try:
                    response = requests.post(
                        f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage",
                        data={
                            'chat_id': chat_id,
                            'text': message_body,
                            'parse_mode': 'HTML'
                        }
                    )
                    
                    if response.status_code == 200:
                        success_count += 1
                        logging.info(f"Alerta por Telegram enviada a usuario {chat_id}")
                    else:
                        logging.error(f"Error al enviar Telegram a {chat_id}: {response.text}")
                except Exception as e:
                    logging.error(f"Error al enviar Telegram a {chat_id}: {e}")
            
            if success_count > 0:
                logging.info(f"Alertas enviadas a {success_count}/{len(self.telegram_chat_ids)} usuarios")
                return True
            else:
                logging.error("No se pudo enviar a ningún usuario")
                return False
            
        except Exception as e:
            logging.error(f"Error al enviar Telegram: {e}")
            return False
    
    def send_telegram_summary(self, summary_text):
        """Enviar resumen horario por Telegram a todos los usuarios"""
        if not self.telegram_bot_token or not self.telegram_chat_ids:
            logging.warning("Telegram no configurado")
            return False
        
        try:
            message_body = f"""
📊 Resumen Horario - Bot Islas Cíes

{summary_text}

🤖 Bot funcionando correctamente
            """
            
            success_count = 0
            # Enviar mensaje a todos los usuarios
            for chat_id in self.telegram_chat_ids:
                try:
                    response = requests.post(
                        f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage",
                        data={
                            'chat_id': chat_id,
                            'text': message_body,
                            'parse_mode': 'HTML'
                        }
                    )
                    
                    if response.status_code == 200:
                        success_count += 1
                        logging.info(f"Resumen horario enviado a usuario {chat_id}")
                    else:
                        logging.error(f"Error al enviar resumen a {chat_id}: {response.text}")
                except Exception as e:
                    logging.error(f"Error al enviar resumen a {chat_id}: {e}")
            
            if success_count > 0:
                logging.info(f"Resúmenes enviados a {success_count}/{len(self.telegram_chat_ids)} usuarios")
                return True
            else:
                logging.error("No se pudo enviar resumen a ningún usuario")
                return False
            
        except Exception as e:
            logging.error(f"Error al enviar resumen Telegram: {e}")
            return False
    
    def send_whatsapp_alert(self, availability_data):
        """Enviar alerta por WhatsApp"""
        if not self.twilio_client or not RECIPIENT_WHATSAPP:
            logging.warning("WhatsApp no configurado o destinatario no especificado")
            return False
        
        try:
            # Crear mensaje
            message_body = f"""
🏝️ ¡PLAZAS DISPONIBLES EN ISLAS CÍES! 🏝️

📅 Fecha: {availability_data['date']}
🎫 Plazas: {availability_data['available_slots']}
⏰ Verificado: {availability_data['timestamp']}

🔗 {TARGET_URL}

¡Reserva ahora!
            """
            
            # Enviar mensaje WhatsApp
            message = self.twilio_client.messages.create(
                body=message_body,
                from_=f'whatsapp:{TWILIO_PHONE_NUMBER}',
                to=f'whatsapp:{RECIPIENT_WHATSAPP}'
            )
            
            logging.info(f"Alerta por WhatsApp enviada a {RECIPIENT_WHATSAPP}")
            return True
            
        except Exception as e:
            logging.error(f"Error al enviar WhatsApp: {e}")
            return False
    
    def send_alert(self, availability_data):
        """Enviar alertas por todos los medios configurados"""
        success_count = 0
        
        # Enviar Telegram (prioridad alta)
        if self.send_telegram_alert(availability_data):
            success_count += 1
        
        # Enviar email
        if self.send_email_alert(availability_data):
            success_count += 1
        
        # Enviar WhatsApp
        if self.send_whatsapp_alert(availability_data):
            success_count += 1
        
        if success_count > 0:
            logging.info(f"Alertas enviadas exitosamente por {success_count} medio(s)")
            return True
        else:
            logging.error("No se pudo enviar ninguna alerta")
            return False
    
    def close(self):
        """Cerrar conexiones"""
        if self.smtp_server:
            self.smtp_server.quit()
            logging.info("Conexión de email cerrada")