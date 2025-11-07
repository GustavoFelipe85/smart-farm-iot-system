# 📱 alerts/telegram_manager.py
class AlertSystem:
    def __init__(self):
        self.telegram_bot = TelegramBot()
        self.thresholds = {
            'temperature': {'min': 15, 'max': 35},
            'soil_moisture': {'min': 30, 'max': 80},
            'humidity': {'min': 40, 'max': 80}
        }
    
    def check_thresholds(self, sensor_data):
        """Monitora limites e envia alertas"""
        for sensor, values in sensor_data.items():
            if values['current'] < self.thresholds[sensor]['min']:
                self.send_alert(f"⚠️ {sensor} BAIXO: {values['current']}")
import requests
import os

class TelegramAlerts:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    def send_alert(self, message):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": f"🚨 SMART FARM ALERT:\n{message}",
            "parse_mode": "HTML"
        }
        try:
            response = requests.post(url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Erro enviar alerta Telegram: {e}")
            return False
