import paho.mqtt.client as mqtt
import requests
import json
import time
import random
import threading
import os
from datetime import datetime, timezone

# Variáveis de Ambiente Injetadas pelo Docker
MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USER = os.getenv("MQTT_USERNAME", "admin")
MQTT_PASS = os.getenv("MQTT_PASSWORD", "admin")
MQTT_TOPIC = "farm/telemetry"

INMET_API_CASCAVEL = "https://apitempo.inmet.gov.br/estacao/dados/A715"

# Estado Global de Referência
current_macro_temp = 24.0 
current_macro_hum = 60.0

def sync_inmet_weather():
    """Worker em background: Consome macroclima a cada 1 hora."""
    global current_macro_temp, current_macro_hum
    while True:
        try:
            # [Inferência] O contrato exato do payload do INMET pode variar; 
            # assumindo o padrão de array JSON com chaves TEM_INS e UMD_INS.
            response = requests.get(INMET_API_CASCAVEL, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list):
                    latest = data[-1] # Pega a leitura mais recente
                    current_macro_temp = float(latest.get('TEM_INS', current_macro_temp))
                    current_macro_hum = float(latest.get('UMD_INS', current_macro_hum))
                    print(f"[API] Macroclima sincronizado: {current_macro_temp}°C")
        except Exception as e:
            print(f"[!] Falha na API Externa. Operando em Fallback. Erro: {e}")
        
        time.sleep(3600)

def generate_sensor_data():
    """Gera telemetria mimetizando variância física do SHT31-DIS."""
    return {
        "device_id": "sht31_emulator_01",
        "temperature": round(random.gauss(current_macro_temp, 0.5), 2),
        "humidity": round(random.gauss(current_macro_hum, 2.0), 2),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[+] Emulador conectado ao Broker Mosquitto.")
    else:
        print(f"[-] Falha na conexão MQTT. Código: {rc}")

if __name__ == "__main__":
    threading.Thread(target=sync_inmet_weather, daemon=True).start()

    client = mqtt.Client(client_id="smartfarm_digital_twin")
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.on_connect = on_connect

    while True:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            break
        except Exception:
            print("[*] Aguardando broker MQTT...")
            time.sleep(5)

    client.loop_start()

    try:
        while True:
            payload = generate_sensor_data()
            client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
            time.sleep(10) # Ciclo de amostragem de 10 segundos
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
