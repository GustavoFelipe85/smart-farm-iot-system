import os, json, time
from datetime import datetime
from jsonschema import validate, ValidationError
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "schemas", "sensor_payload.json")
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    PAYLOAD_SCHEMA = json.load(f)

INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG", "smartfarm")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "sensors")

MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_TOPIC = "smartfarm/sensors/#"

client_influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client_influx.write_api(write_options=SYNCHRONOUS)

def write_influx(payload: dict):
    p = Point("sensors") \
        .tag("device", payload["device"]) \
        .field("temp", float(payload["metrics"].get("temp", 0.0))) \
        .field("umid", float(payload["metrics"].get("umid", 0.0))) \
        .field("soil", float(payload["metrics"].get("soil", 0.0))) \
        .time(datetime.fromisoformat(payload["ts"].replace("Z","")), WritePrecision.NS)
    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=p)

def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected rc={rc}")
    client.subscribe(MQTT_TOPIC, qos=1)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode("utf-8"))
        validate(instance=data, schema=PAYLOAD_SCHEMA)
        write_influx(data)
        print(f"[OK] {data['device']} -> influx")
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"[SCHEMA ERROR] {e}")
    except Exception as e:
        print(f"[WRITE ERROR] {e}")

def main():
    mqttc = mqtt.Client()
    if MQTT_USERNAME and MQTT_PASSWORD:
        mqttc.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqttc.loop_forever()

if __name__ == "__main__":
    main()
