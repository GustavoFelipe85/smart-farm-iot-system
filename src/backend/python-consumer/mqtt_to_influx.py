import os
import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WriteOptions
from dotenv import load_dotenv

load_dotenv()

# Configurações
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "smartfarm/sensors")
INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "smartfarm-token-12345")
INFLUX_ORG = os.getenv("INFLUX_ORG", "smartfarm")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "sensors")

# Cliente InfluxDB
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10000))

def on_connect(client, userdata, flags, rc):
    print(f"✅ Conectado ao broker MQTT com código: {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"📡 Inscrito no tópico: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"📨 Mensagem recebida: {payload}")
        
        data = json.loads(payload)
        
        # Criar ponto para InfluxDB
        point = Point("environment") \
            .tag("device", data.get("device", "unknown")) \
            .field("temperature", float(data["temp"])) \
            .field("humidity", float(data["umid"]))
        
        # Escrever no InfluxDB
        write_api.write(bucket=INFLUX_BUCKET, record=point)
        print(f"✅ Dados gravados - Temp: {data['temp']}°C, Umidade: {data['umid']}%")
        
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao decodificar JSON: {e}")
    except KeyError as e:
        print(f"❌ Campo faltando no payload: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def main():
    print("🚀 Iniciando consumidor MQTT -> InfluxDB")
    print(f"Broker: {MQTT_BROKER}, Tópico: {MQTT_TOPIC}")
    print(f"InfluxDB: {INFLUX_URL}, Bucket: {INFLUX_BUCKET}")
    
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    
    try:
        mqtt_client.connect(MQTT_BROKER, 1883, 60)
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        print("🛑 Parando consumidor...")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    finally:
        client.close()
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()
