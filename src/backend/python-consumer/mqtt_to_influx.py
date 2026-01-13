diff --git a/src/backend/schemas/sensor_payload.json b/src/backend/schemas/sensor_payload.json
index 1111111..2222222 100644
--- a/src/backend/schemas/sensor_payload.json
+++ b/src/backend/schemas/sensor_payload.json
@@ -1,15 +1,22 @@
 {
   "$schema": "http://json-schema.org/draft-07/schema#",
   "title": "Smart Farm Sensor Payload",
   "type": "object",
-  "required": ["device", "timestamp", "metrics"],
+  "required": ["schema_version", "device", "timestamp", "metrics"],
   "properties": {
+    "schema_version": {
+      "type": "string",
+      "const": "1.0.0",
+      "description": "Payload contract version (SemVer)"
+    },
     "device": { "type": "string" },
     "timestamp": { "type": "string", "format": "date-time" },
     "metrics": {
       "type": "object",
       "required": ["temperature", "humidity"],
       "properties": {
         "temperature": { "type": "number" },
         "humidity": { "type": "number" },
         "soil_moisture": { "type": ["number", "null"] },
         "soil_raw": { "type": ["integer", "null"] }
       },
       "additionalProperties": false
     }
   },
   "additionalProperties": false
 }
diff --git a/src/backend/python-consumer/main.py b/src/backend/python-consumer/main.py
index 7a81dea..9c0fabc 100644
--- a/src/backend/python-consumer/main.py
+++ b/src/backend/python-consumer/main.py
@@ -1,60 +1,156 @@
-import os, json, time
-from datetime import datetime
-from jsonschema import validate, ValidationError
+import os, json
+from datetime import datetime, timezone
+from jsonschema import validate, ValidationError
 from influxdb_client import InfluxDBClient, Point, WritePrecision
 from influxdb_client.client.write_api import SYNCHRONOUS
 import paho.mqtt.client as mqtt
 
-SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "schemas", "sensor_payload.json")
+SCHEMA_VERSION = "1.0.0"
+STRICT_SCHEMA = os.getenv("STRICT_SCHEMA", "true").lower() in ("1", "true", "yes")
+
+SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "schemas", "sensor_payload.json")
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
 
+def _now_utc_iso_z() -> str:
+    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
+
+def normalize_payload(raw: dict) -> dict:
+    """
+    Normalize legacy payloads to canonical schema:
+      - canonical: {schema_version, device, timestamp, metrics{temperature,humidity,soil_*}}
+      - legacy supported: ts + metrics{temp,umid,soil} OR flat temp/umid/soil
+    IMPORTANT: missing soil fields stay None (null ≠ 0).
+    """
+    if not isinstance(raw, dict):
+        raise ValueError("payload must be a JSON object")
+
+    # Already canonical-shaped
+    if "device" in raw and "timestamp" in raw and "metrics" in raw:
+        out = dict(raw)
+        out.setdefault("schema_version", SCHEMA_VERSION)
+        if isinstance(out.get("metrics"), dict):
+            out["metrics"].setdefault("soil_moisture", None)
+            out["metrics"].setdefault("soil_raw", None)
+        return out
+
+    device = raw.get("device") or raw.get("dev") or "unknown"
+    timestamp = raw.get("timestamp") or raw.get("ts") or raw.get("time") or _now_utc_iso_z()
+
+    metrics_in = raw.get("metrics") if isinstance(raw.get("metrics"), dict) else raw
+
+    temperature = metrics_in.get("temperature", metrics_in.get("temp"))
+    humidity = metrics_in.get("humidity", metrics_in.get("umid", metrics_in.get("hum")))
+
+    soil_moisture = metrics_in.get("soil_moisture")
+    soil_raw = metrics_in.get("soil_raw")
+
+    # Legacy "soil" often used as % (keep conservative)
+    if soil_moisture is None and "soil" in metrics_in:
+        try:
+            soil_moisture = float(metrics_in["soil"])
+        except Exception:
+            soil_moisture = None
+
+    return {
+        "schema_version": SCHEMA_VERSION,
+        "device": str(device),
+        "timestamp": str(timestamp),
+        "metrics": {
+            "temperature": float(temperature),
+            "humidity": float(humidity),
+            "soil_moisture": None if soil_moisture is None else float(soil_moisture),
+            "soil_raw": None if soil_raw is None else int(soil_raw),
+        },
+    }
+
 def write_influx(payload: dict):
-    p = Point("sensors") \
-        .tag("device", payload["device"]) \
-        .field("temp", float(payload["metrics"].get("temp", 0.0))) \
-        .field("umid", float(payload["metrics"].get("umid", 0.0))) \
-        .field("soil", float(payload["metrics"].get("soil", 0.0))) \
-        .time(datetime.fromisoformat(payload["ts"].replace("Z", "")), WritePrecision.NS)
-    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=p)
+    # robust timestamp parsing: convert Z -> +00:00 for fromisoformat
+    ts = payload["timestamp"].replace("Z", "+00:00")
+    dt = datetime.fromisoformat(ts)
+
+    m = payload["metrics"]
+
+    # Preserve existing measurement & field names (avoid breaking Grafana/historical queries)
+    p = Point("sensors") \
+        .tag("device", payload["device"]) \
+        .field("temp", float(m["temperature"])) \
+        .field("umid", float(m["humidity"])) \
+        .time(dt, WritePrecision.NS)
+
+    # Only write soil if present (None ≠ 0)
+    if m.get("soil_moisture") is not None:
+        p = p.field("soil", float(m["soil_moisture"]))
+
+    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=p)
 
 def on_connect(client, userdata, flags, rc):
     print(f"[MQTT] Connected rc={rc}")
     client.subscribe(MQTT_TOPIC, qos=1)
 
 def on_message(client, userdata, msg):
     try:
-        data = json.loads(msg.payload.decode("utf-8"))
-        validate(instance=data, schema=PAYLOAD_SCHEMA)
-        write_influx(data)
-        print(f"[OK] {data['device']} -> influx")
-    except (json.JSONDecodeError, ValidationError) as e:
-        print(f"[SCHEMA ERROR] {e}")
-    except Exception as e:
-        print(f"[WRITE ERROR] {e}")
+        raw = json.loads(msg.payload.decode("utf-8"))
+        payload = normalize_payload(raw)
+
+        # Validate against canonical schema
+        validate(instance=payload, schema=PAYLOAD_SCHEMA)
+
+        write_influx(payload)
+        print(f"[OK] {payload['device']} -> influx")
+
+    except ValidationError as e:
+        if STRICT_SCHEMA:
+            print(f"[DROP][SCHEMA] {e.message}")
+            return
+        print(f"[WARN][SCHEMA] {e.message}")
+
+    except (json.JSONDecodeError, ValueError) as e:
+        print(f"[DROP] invalid payload: {e}")
+
+    except Exception as e:
+        print(f"[ERROR] {e}")
 
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
