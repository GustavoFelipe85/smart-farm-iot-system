#!/usr/bin/env python3
"""
Legacy-compatible MQTT -> InfluxDB consumer.
Keeps Influx measurement/fields stable ("sensors", temp/umid/soil),
but normalizes payloads to the canonical schema-first contract before validation.

Path: src/backend/python-consumer/mqtt_to_influx.py
"""

import os
import json
from datetime import datetime, timezone

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from jsonschema import validate, ValidationError
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Load .env if present
load_dotenv()

SCHEMA_VERSION = "1.0.0"
STRICT_SCHEMA = os.getenv("STRICT_SCHEMA", "true").lower() in ("1", "true", "yes")

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "schemas", "sensor_payload.json")
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    PAYLOAD_SCHEMA = json.load(f)

# Influx config
INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG", "smartfarm")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "sensors")

# MQTT config
MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "smartfarm/sensors/#")

client_influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client_influx.write_api(write_options=SYNCHRONOUS)


def _now_utc_iso_z() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_payload(raw: dict) -> dict:
    """
    Normalize payloads to canonical schema:
    {
      "schema_version": "1.0.0",
      "device": "...",
      "timestamp": "....Z",
      "metrics": {
        "temperature": number,
        "humidity": number,
        "soil_moisture": number|null,
        "soil_raw": integer|null
      }
    }

    Accept legacy variants:
    - {"device":..., "ts":..., "metrics":{"temp":..,"umid":..,"soil":..}}
    - {"device":..., "ts":..., "temp":..,"umid":..,"soil":..}
    """
    if not isinstance(raw, dict):
        raise ValueError("payload must be a JSON object")

    # Already canonical
    if "device" in raw and "timestamp" in raw and "metrics" in raw:
        out = dict(raw)
        out.setdefault("schema_version", SCHEMA_VERSION)
        if isinstance(out.get("metrics"), dict):
            out["metrics"].setdefault("soil_moisture", None)
            out["metrics"].setdefault("soil_raw", None)
        return out

    device = raw.get("device") or raw.get("dev") or "unknown"
    timestamp = raw.get("timestamp") or raw.get("ts") or raw.get("time") or _now_utc_iso_z()

    metrics_in = raw.get("metrics") if isinstance(raw.get("metrics"), dict) else raw

    temperature = metrics_in.get("temperature", metrics_in.get("temp"))
    humidity = metrics_in.get("humidity", metrics_in.get("umid", metrics_in.get("hum")))

    soil_moisture = metrics_in.get("soil_moisture")
    soil_raw = metrics_in.get("soil_raw")

    # Legacy "soil" (keep conservative: treat as % unless you document ADC calibration)
    if soil_moisture is None and "soil" in metrics_in:
        try:
            soil_moisture = float(metrics_in["soil"])
        except Exception:
            soil_moisture = None

    return {
        "schema_version": SCHEMA_VERSION,
        "device": str(device),
        "timestamp": str(timestamp),
        "metrics": {
            "temperature": float(temperature),
            "humidity": float(humidity),
            "soil_moisture": None if soil_moisture is None else float(soil_moisture),
            "soil_raw": None if soil_raw is None else int(soil_raw),
        },
    }


def write_influx(payload: dict):
    # Robust timestamp parsing: Z -> +00:00
    ts = payload["timestamp"].replace("Z", "+00:00")
    dt = datetime.fromisoformat(ts)

    m = payload["metrics"]

    # Preserve measurement/fields (avoid breaking Grafana/historical queries)
    p = (
        Point("sensors")
        .tag("device", payload["device"])
        .field("temp", float(m["temperature"]))
        .field("umid", float(m["humidity"]))
        .time(dt, WritePrecision.NS)
    )

    # Only write soil when available (None ≠ 0)
    if m.get("soil_moisture") is not None:
        p = p.field("soil", float(m["soil_moisture"]))

    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=p)


def on_connect(client, userdata, flags, rc):
    print(f"[MQTT] Connected rc={rc}")
    client.subscribe(MQTT_TOPIC, qos=1)
    print(f"[MQTT] Subscribed: {MQTT_TOPIC}")


def on_message(client, userdata, msg):
    try:
        raw = json.loads(msg.payload.decode("utf-8"))
        payload = normalize_payload(raw)

        validate(instance=payload, schema=PAYLOAD_SCHEMA)

        write_influx(payload)
        print(f"[OK] {payload['device']} -> influx")

    except ValidationError as e:
        if STRICT_SCHEMA:
            print(f"[DROP][SCHEMA] {e.message}")
            return
        print(f"[WARN][SCHEMA] {e.message}")

    except (json.JSONDecodeError, ValueError) as e:
        print(f"[DROP] invalid payload: {e}")

    except Exception as e:
        print(f"[ERROR] {e}")


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

