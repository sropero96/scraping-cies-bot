#!/usr/bin/env python3
"""
Módulo para manejar estadísticas y resúmenes del bot
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import logging

class BotStats:
    def __init__(self, stats_file="bot_stats.json"):
        self.stats_file = stats_file
        self.stats = self.load_stats()
        self.current_hour = datetime.now().replace(minute=0, second=0, microsecond=0)
        self.hourly_stats = defaultdict(lambda: {
            'attempts': 0,
            'total_slots': 0,
            'max_slots': 0,
            'min_slots': float('inf'),
            'availability_found': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        })
    
    def load_stats(self):
        """Cargar estadísticas desde archivo"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            'total_attempts': 0,
            'total_slots_checked': 0,
            'max_slots_found': 0,
            'availability_found_count': 0,
            'total_errors': 0,
            'start_date': datetime.now().isoformat(),
            'hourly_data': {}
        }
    
    def save_stats(self):
        """Guardar estadísticas a archivo"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            logging.error(f"Error al guardar estadísticas: {e}")
    
    def record_attempt(self, available_slots, had_error=False):
        """Registrar un intento de verificación"""
        now = datetime.now()
        current_hour = now.replace(minute=0, second=0, microsecond=0)
        
        # Actualizar estadísticas globales
        self.stats['total_attempts'] += 1
        self.stats['total_slots_checked'] += available_slots
        
        if available_slots > self.stats['max_slots_found']:
            self.stats['max_slots_found'] = available_slots
        
        if available_slots > 0:
            self.stats['availability_found_count'] += 1
        
        if had_error:
            self.stats['total_errors'] += 1
        
        # Actualizar estadísticas por hora
        hour_key = current_hour.isoformat()
        if hour_key not in self.stats['hourly_data']:
            self.stats['hourly_data'][hour_key] = {
                'attempts': 0,
                'total_slots': 0,
                'max_slots': 0,
                'min_slots': float('inf'),
                'availability_found': 0,
                'errors': 0,
                'start_time': current_hour.isoformat(),
                'end_time': current_hour.isoformat()
            }
        
        hour_stats = self.stats['hourly_data'][hour_key]
        hour_stats['attempts'] += 1
        hour_stats['total_slots'] += available_slots
        hour_stats['max_slots'] = max(hour_stats['max_slots'], available_slots)
        hour_stats['min_slots'] = min(hour_stats['min_slots'], available_slots)
        hour_stats['end_time'] = now.isoformat()
        
        if available_slots > 0:
            hour_stats['availability_found'] += 1
        
        if had_error:
            hour_stats['errors'] += 1
        
        # Guardar estadísticas
        self.save_stats()
    
    def get_hourly_summary(self, hour=None):
        """Obtener resumen de una hora específica"""
        if hour is None:
            hour = datetime.now().replace(minute=0, second=0, microsecond=0)
        
        hour_key = hour.isoformat()
        if hour_key in self.stats['hourly_data']:
            return self.stats['hourly_data'][hour_key]
        return None
    
    def get_current_hour_summary(self):
        """Obtener resumen de la hora actual"""
        return self.get_hourly_summary()
    
    def get_previous_hour_summary(self):
        """Obtener resumen de la hora anterior"""
        previous_hour = datetime.now().replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
        return self.get_hourly_summary(previous_hour)
    
    def format_hourly_summary(self, summary, hour_label="Hora actual"):
        """Formatear resumen horario para envío"""
        if not summary:
            return f"📊 {hour_label}: No hay datos disponibles"
        
        avg_slots = summary['total_slots'] / summary['attempts'] if summary['attempts'] > 0 else 0
        
        return f"""📊 {hour_label} ({summary['start_time'][:16]} - {summary['end_time'][:16]})

🔍 Intentos realizados: {summary['attempts']}
🎫 Plazas totales verificadas: {summary['total_slots']}
📈 Promedio de plazas: {avg_slots:.1f}
🏆 Máximo de plazas: {summary['max_slots']}
📉 Mínimo de plazas: {summary['min_slots'] if summary['min_slots'] != float('inf') else 0}
✅ Veces con disponibilidad: {summary['availability_found']}
❌ Errores: {summary['errors']}"""
    
    def get_global_summary(self):
        """Obtener resumen global del bot"""
        total_attempts = self.stats['total_attempts']
        total_slots = self.stats['total_slots_checked']
        avg_slots = total_slots / total_attempts if total_attempts > 0 else 0
        
        return f"""🤖 Resumen Global del Bot

📅 Desde: {self.stats['start_date'][:16]}
🔍 Total de intentos: {total_attempts}
🎫 Total de plazas verificadas: {total_slots}
📈 Promedio de plazas: {avg_slots:.1f}
🏆 Máximo de plazas encontradas: {self.stats['max_slots_found']}
✅ Veces con disponibilidad: {self.stats['availability_found_count']}
❌ Total de errores: {self.stats['total_errors']}"""
    
    def cleanup_old_data(self, days_to_keep=7):
        """Limpiar datos antiguos (más de X días)"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cutoff_hour = cutoff_date.replace(minute=0, second=0, microsecond=0)
        
        old_keys = []
        for hour_key in self.stats['hourly_data']:
            try:
                hour_date = datetime.fromisoformat(hour_key)
                if hour_date < cutoff_hour:
                    old_keys.append(hour_key)
            except:
                old_keys.append(hour_key)
        
        for key in old_keys:
            del self.stats['hourly_data'][key]
        
        if old_keys:
            logging.info(f"Limpiados {len(old_keys)} registros antiguos")
            self.save_stats()
    
    def get_session_summary(self):
        """Obtener resumen de la sesión actual (últimas 24 horas)"""
        try:
            # Obtener datos de las últimas 24 horas
            cutoff_time = datetime.now() - timedelta(hours=24)
            cutoff_hour = cutoff_time.replace(minute=0, second=0, microsecond=0)
            
            recent_data = {}
            for hour_key, hour_data in self.stats['hourly_data'].items():
                try:
                    hour_date = datetime.fromisoformat(hour_key)
                    if hour_date >= cutoff_hour:
                        recent_data[hour_key] = hour_data
                except:
                    continue
            
            if not recent_data:
                return "No hay datos recientes"
            
            total_attempts = sum(data['attempts'] for data in recent_data.values())
            total_errors = sum(data['errors'] for data in recent_data.values())
            successful_attempts = total_attempts - total_errors
            max_availability = max((data['max_slots'] for data in recent_data.values()), default=0)
            availability_found = sum(data['availability_found'] for data in recent_data.values())
            
            # Obtener última verificación
            last_verification = "N/A"
            if recent_data:
                latest_hour = max(recent_data.keys())
                last_verification = latest_hour[:16]  # Formato: YYYY-MM-DD HH:MM
            
            summary = f"""• Intentos totales: {total_attempts}
• Intentos exitosos: {successful_attempts}
• Errores: {total_errors}
• Máxima disponibilidad encontrada: {max_availability} plazas
• Veces con disponibilidad: {availability_found}
• Última verificación: {last_verification}"""
            
            return summary
            
        except Exception as e:
            logging.error(f"Error al obtener resumen de sesión: {e}")
            return "Error al obtener estadísticas" 