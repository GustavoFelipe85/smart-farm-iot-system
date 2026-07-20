"""
Smart Farm IoT System — Python MQTT Consumer

Responsibilities:
- Subscribe to MQTT topic(s)
- Normalize legacy payloads into the canonical contract (schema_version=1.0.0)
- Validate payloads against JSON Schema (with format checking)
- Write normalized data to InfluxDB (keeping historical field names for Grafana compatibility)

Env vars:
- INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET
- MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, MQTT_TOPIC
- STRICT_SCHEMA: true/false (default true)
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from jsonschema import FormatChecker, validate
from jsonschema.exceptions import ValidationError

# -----------------------------
# Contract / schema
# -----------------------------
SCHEMA_VERSION = "1.0.0"
STRICT_SCHEMA = os.getenv("STRICT_SCHEMA", "true").strip().lower() in ("1", "true", "yes", "y", "on")

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "schemas", "sensor_payload.json")
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    PAYLOAD_SCHEMA = json.load(f)

FORMAT_CHECKER = FormatChecker()

# -----------------------------
# InfluxDB config
# -----------------------------
INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG", "smartfarm")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "sensors")

# -----------------------------
# MQTT config
# -----------------------------
MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "").strip()
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "").strip()
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "smartfarm/sensors/#")

# -----------------------------
# Clients
# -----------------------------
client_influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client_influx.write_api(write_options=SYNCHRONOUS)


def _now_utc_iso_z() -> str:
    """UTC timestamp with 'Z' suffix."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _require_number(value: Any, name: str) -> float:
    """Convert value to float or raise a clear error."""
    if value is None:
        raise ValueError(f"missing required metric: {name}")
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"invalid metric '{name}': expected number, got {value!r}")


def normalize_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize legacy payloads to canonical schema:
      canonical:
        {schema_version, device, timestamp, metrics{temperature, humidity, soil_moisture?, soil_raw?}}

      legacy supported:
        - ts + metrics{temp, umid, soil}
        - flat temp/umid/soil on root
        - optional dev/time synonyms (dev, time)
    """
    if not isinstance(raw, dict):
        raise ValueError("payload must be a JSON object")

    # If it's already in canonical shape, just ensure schema_version and optional soil fields exist.
    if "device" in raw and "timestamp" in raw and isinstance(raw.get("metrics"), dict):
        out = dict(raw)
        out.setdefault("schema_version", SCHEMA_VERSION)

        metrics = out["metrics"]
        # Allow either canonical keys or legacy keys inside metrics (normalize if needed)
        if "temperature" not in metrics and "temp" in metrics:
            metrics["temperature"] = metrics["temp"]
        if "humidity" not in metrics and "umid" in metrics:
            metrics["humidity"] = metrics["umid"]
        if "soil_moisture" not in metrics and "soil" in metrics:
            metrics["soil_moisture"] = metrics["soil"]

        metrics.setdefault("soil_moisture", None)
        metrics.setdefault("soil_raw", None)

        # Enforce required numeric conversions at normalization time (clearer errors)
        metrics["temperature"] = _require_number(metrics.get("temperature"), "temperature")
        metrics["humidity"] = _require_number(metrics.get("humidity"), "humidity")

        if metrics.get("soil_moisture") is not None:
            metrics["soil_moisture"] = float(metrics["soil_moisture"])
        if metrics.get("soil_raw") is not None:
            metrics["soil_raw"] = int(metrics["soil_raw"])

        return out

    # Legacy or mixed shapes
    device = raw.get("device") or raw.get("dev") or "unknown"
    timestamp = raw.get("timestamp") or raw.get("ts") or raw.get("time") or _now_utc_iso_z()

    metrics_in = raw.get("metrics") if isinstance(raw.get("metrics"), dict) else raw

    temperature = metrics_in.get("temperature", metrics_in.get("temp"))
    humidity = metrics_in.get("humidity", metrics_in.get("umid", metrics_in.get("hum")))

    soil_moisture = metrics_in.get("soil_moisture")
    soil_raw = metrics_in.get("soil_raw")

    # Legacy "soil" often used as % (do not assume raw ADC)
    if soil_moisture is None and "soil" in metrics_in:
        soil_moisture = metrics_in.get("soil")

    canonical = {
        "schema_version": SCHEMA_VERSION,
        "device": str(device),
        "timestamp": str(timestamp),
        "metrics": {
            "temperature": _require_number(temperature, "temperature"),
            "humidity": _require_number(humidity, "humidity"),
            "soil_moisture": None if soil_moisture is None else float(soil_moisture),
            "soil_raw": None if soil_raw is None else int(soil_raw),
        },
    }
    return canonical


def write_influx(payload: Dict[str, Any]) -> None:
    """
    Write to InfluxDB.

    Keeps historical field names:
      - temp (temperature)
      - umid (humidity)
      - soil (soil_moisture)
    """
    ts = payload["timestamp"].replace("Z", "+00:00")  # fromisoformat expects offset form
    dt = datetime.fromisoformat(ts)

    m = payload["metrics"]

    p = (
        Point("sensors")
        .tag("device", payload["device"])
        .field("temp", float(m["temperature"]))
        .field("umid", float(m["humidity"]))
        .time(dt, WritePrecision.NS)
    )

  if m.get("soil_moisture") is not None:
    p = p.field("soil", float(m["soil_moisture"]))

if m.get("soil_raw") is not None:
    p = p.field("soil_raw", int(m["soil_raw"]))

write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=p)


def on_connect(client: mqtt.Client, userdata, flags, rc):
    print(f"[MQTT] Connected rc={rc}")
    client.subscribe(MQTT_TOPIC, qos=1)


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    try:
        raw = json.loads(msg.payload.decode("utf-8"))
        payload = normalize_payload(raw)

        # Validate canonical payload
        validate(instance=payload, schema=PAYLOAD_SCHEMA, format_checker=FORMAT_CHECKER)

        write_influx(payload)
        print(f"[OK] {payload['device']} -> influx")

    except ValidationError as e:
        # Schema violations: drop or warn based on STRICT_SCHEMA
        if STRICT_SCHEMA:
            print(f"[DROP][SCHEMA] {e.message}")
            return
        print(f"[WARN][SCHEMA] {e.message}")

    except (json.JSONDecodeError, ValueError, TypeError) as e:
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
