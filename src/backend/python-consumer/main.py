"""
Smart Farm IoT System — Python MQTT Consumer

Responsibilities:
- Subscribe to MQTT topic(s).
- Decode MQTT messages encoded as UTF-8 JSON.
- Normalize legacy payloads into the canonical data contract.
- Validate normalized payloads against JSON Schema.
- Write valid sensor data to InfluxDB.
- Preserve historical InfluxDB field names for Grafana compatibility.

Environment variables:
- INFLUX_URL
- INFLUX_TOKEN
- INFLUX_ORG
- INFLUX_BUCKET
- MQTT_BROKER
- MQTT_PORT
- MQTT_USERNAME
- MQTT_PASSWORD
- MQTT_TOPIC
- STRICT_SCHEMA: true/false (default: true)

Data integrity policy:
- Structurally invalid payloads are never written to the "sensors"
  measurement.
- STRICT_SCHEMA controls the log severity applied to schema violations.
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


# ---------------------------------------------------------------------------
# Data contract and JSON Schema
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "1.0.0"

STRICT_SCHEMA = (
    os.getenv("STRICT_SCHEMA", "true")
    .strip()
    .lower()
    in ("1", "true", "yes", "y", "on")
)

SCHEMA_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "schemas",
        "sensor_payload.json",
    )
)

with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
    PAYLOAD_SCHEMA = json.load(schema_file)

FORMAT_CHECKER = FormatChecker()


# ---------------------------------------------------------------------------
# InfluxDB configuration
# ---------------------------------------------------------------------------

INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG", "smartfarm")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "sensors")


# ---------------------------------------------------------------------------
# MQTT configuration
# ---------------------------------------------------------------------------

MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

MQTT_USERNAME = os.getenv("MQTT_USERNAME", "").strip()
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "").strip()

MQTT_TOPIC = os.getenv(
    "MQTT_TOPIC",
    "smartfarm/sensors/#",
)


# ---------------------------------------------------------------------------
# External clients
# ---------------------------------------------------------------------------

client_influx = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG,
)

write_api = client_influx.write_api(
    write_options=SYNCHRONOUS,
)


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _now_utc_iso_z() -> str:
    """
    Return the current UTC time using ISO 8601 format and the Z suffix.

    Example:
        2026-07-21T23:15:00.000000Z
    """
    return (
        datetime.now(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _require_number(value: Any, name: str) -> float:
    """
    Convert a required metric to float.

    Raises:
        ValueError: if the metric is missing or cannot be converted.
    """
    if value is None:
        raise ValueError(
            f"missing required metric: {name}"
        )

    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"invalid metric '{name}': "
            f"expected number, got {value!r}"
        ) from exc


def _optional_float(value: Any, name: str) -> float | None:
    """
    Convert an optional metric to float.

    Returns:
        None when the metric is absent.

    Raises:
        ValueError: if the value exists but cannot be converted.
    """
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"invalid metric '{name}': "
            f"expected number, got {value!r}"
        ) from exc


def _optional_int(value: Any, name: str) -> int | None:
    """
    Convert an optional metric to integer.

    Returns:
        None when the metric is absent.

    Raises:
        ValueError: if the value exists but cannot be converted.
    """
    if value is None:
        return None

    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"invalid metric '{name}': "
            f"expected integer, got {value!r}"
        ) from exc


# ---------------------------------------------------------------------------
# Payload normalization
# ---------------------------------------------------------------------------

def normalize_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize supported payload formats into the canonical contract.

    Canonical format:

        {
            "schema_version": "1.0.0",
            "device": "esp32-01",
            "timestamp": "2026-07-21T23:15:00Z",
            "metrics": {
                "temperature": 25.4,
                "humidity": 61.2,
                "soil_moisture": 48.5,
                "soil_raw": 2108
            }
        }

    Supported legacy formats:
    - ts + metrics{temp, umid, soil}
    - flat temp/umid/soil fields
    - dev as an alias for device
    - time or ts as aliases for timestamp

    The returned dictionary contains only fields defined by the canonical
    contract. Legacy aliases are not copied to the normalized payload.
    """
    if not isinstance(raw, dict):
        raise ValueError(
            "payload must be a JSON object"
        )

    nested_metrics = raw.get("metrics")

    if isinstance(nested_metrics, dict):
        metrics_source = nested_metrics
    else:
        metrics_source = raw

    device = (
        raw.get("device")
        or raw.get("dev")
        or "unknown"
    )

    timestamp = (
        raw.get("timestamp")
        or raw.get("ts")
        or raw.get("time")
        or _now_utc_iso_z()
    )

    schema_version = raw.get(
        "schema_version",
        SCHEMA_VERSION,
    )

    temperature = metrics_source.get(
        "temperature",
        metrics_source.get("temp"),
    )

    humidity = metrics_source.get(
        "humidity",
        metrics_source.get(
            "umid",
            metrics_source.get("hum"),
        ),
    )

    soil_moisture = metrics_source.get(
        "soil_moisture"
    )

    soil_raw = metrics_source.get(
        "soil_raw"
    )

    # Legacy "soil" is interpreted as soil moisture percentage.
    # It is not assumed to be a raw ADC value.
    if (
        soil_moisture is None
        and "soil" in metrics_source
    ):
        soil_moisture = metrics_source.get("soil")

    canonical_payload = {
        "schema_version": str(schema_version),
        "device": str(device),
        "timestamp": str(timestamp),
        "metrics": {
            "temperature": _require_number(
                temperature,
                "temperature",
            ),
            "humidity": _require_number(
                humidity,
                "humidity",
            ),
            "soil_moisture": _optional_float(
                soil_moisture,
                "soil_moisture",
            ),
            "soil_raw": _optional_int(
                soil_raw,
                "soil_raw",
            ),
        },
    }

    return canonical_payload


# ---------------------------------------------------------------------------
# JSON Schema validation
# ---------------------------------------------------------------------------

def validate_payload(payload: Dict[str, Any]) -> None:
    """
    Validate a canonical payload against the project JSON Schema.

    Raises:
        ValidationError: when the payload violates the schema.
    """
    validate(
        instance=payload,
        schema=PAYLOAD_SCHEMA,
        format_checker=FORMAT_CHECKER,
    )


# ---------------------------------------------------------------------------
# InfluxDB persistence
# ---------------------------------------------------------------------------

def write_influx(payload: Dict[str, Any]) -> None:
    """
    Write a validated canonical payload to InfluxDB.

    Historical field names are preserved for Grafana compatibility:

    - temp: temperature
    - umid: humidity
    - soil: soil_moisture
    - soil_raw: raw ADC soil sensor reading
    """
    timestamp = payload["timestamp"].replace(
        "Z",
        "+00:00",
    )

    timestamp_datetime = datetime.fromisoformat(
        timestamp
    )

    metrics = payload["metrics"]

    point = (
        Point("sensors")
        .tag(
            "device",
            payload["device"],
        )
        .field(
            "temp",
            float(metrics["temperature"]),
        )
        .field(
            "umid",
            float(metrics["humidity"]),
        )
        .time(
            timestamp_datetime,
            WritePrecision.NS,
        )
    )

    if metrics.get("soil_moisture") is not None:
        point = point.field(
            "soil",
            float(metrics["soil_moisture"]),
        )

    if metrics.get("soil_raw") is not None:
        point = point.field(
            "soil_raw",
            int(metrics["soil_raw"]),
        )

    write_api.write(
        bucket=INFLUX_BUCKET,
        org=INFLUX_ORG,
        record=point,
    )


# ---------------------------------------------------------------------------
# MQTT callbacks
# ---------------------------------------------------------------------------

def on_connect(
    client: mqtt.Client,
    userdata: Any,
    flags: Dict[str, Any],
    rc: int,
) -> None:
    """
    Subscribe to the configured topic after connecting to MQTT.
    """
    if rc == 0:
        print(
            f"[MQTT] Connected successfully "
            f"to {MQTT_BROKER}:{MQTT_PORT}"
        )

        client.subscribe(
            MQTT_TOPIC,
            qos=1,
        )

        print(
            f"[MQTT] Subscribed to {MQTT_TOPIC} "
            f"with QoS 1"
        )
        return

    print(
        f"[MQTT][ERROR] Connection failed with rc={rc}"
    )


def on_message(
    client: mqtt.Client,
    userdata: Any,
    msg: mqtt.MQTTMessage,
) -> None:
    """
    Process an MQTT message through the ingestion pipeline.

    Pipeline:
        MQTT bytes
        -> UTF-8 decoding
        -> JSON parsing
        -> normalization
        -> JSON Schema validation
        -> InfluxDB persistence
    """
    try:
        decoded_message = msg.payload.decode(
            "utf-8"
        )

        raw_payload = json.loads(
            decoded_message
        )

        normalized_payload = normalize_payload(
            raw_payload
        )

        validate_payload(
            normalized_payload
        )

        write_influx(
            normalized_payload
        )

        print(
            f"[OK] "
            f"device={normalized_payload['device']} "
            f"topic={msg.topic} "
            f"-> influx"
        )

    except UnicodeDecodeError as exc:
        print(
            f"[DROP][ENCODING] "
            f"payload is not valid UTF-8: {exc}"
        )

    except json.JSONDecodeError as exc:
        print(
            f"[DROP][JSON] "
            f"invalid JSON: {exc}"
        )

    except ValidationError as exc:
        if STRICT_SCHEMA:
            print(
                f"[DROP][SCHEMA] "
                f"{exc.message}"
            )
        else:
            print(
                f"[WARN][SCHEMA] "
                f"payload not persisted: {exc.message}"
            )

    except (ValueError, TypeError) as exc:
        print(
            f"[DROP][PAYLOAD] "
            f"{exc}"
        )

    except Exception as exc:
        print(
            f"[ERROR] "
            f"unexpected consumer failure: {exc}"
        )


# ---------------------------------------------------------------------------
# Application lifecycle
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Configure the MQTT client and start the blocking consumer loop.
    """
    mqtt_client = mqtt.Client()

    if MQTT_USERNAME and MQTT_PASSWORD:
        mqtt_client.username_pw_set(
            username=MQTT_USERNAME,
            password=MQTT_PASSWORD,
        )

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    print(
        f"[START] MQTT consumer connecting to "
        f"{MQTT_BROKER}:{MQTT_PORT}"
    )

    try:
        mqtt_client.connect(
            MQTT_BROKER,
            MQTT_PORT,
            keepalive=60,
        )

        mqtt_client.loop_forever()

    except KeyboardInterrupt:
        print(
            "[STOP] Consumer interrupted by user"
        )

    finally:
        mqtt_client.disconnect()
        client_influx.close()

        print(
            "[STOP] MQTT and InfluxDB clients closed"
        )


if __name__ == "__main__":
    main()
