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
