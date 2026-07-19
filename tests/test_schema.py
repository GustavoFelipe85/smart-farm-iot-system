import json
import os

import pytest
from jsonschema import validate
from jsonschema.exceptions import ValidationError


SCHEMA_PATH = os.path.join(
    "src",
    "backend",
    "schemas",
    "sensor_payload.json",
)


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        return json.load(schema_file)


def test_payload_schema_ok():
    schema = load_schema()

    sample = {
        "schema_version": "1.0.0",
        "device": "esp32-node-1",
        "timestamp": "2025-11-11T12:00:00Z",
        "metrics": {
            "temperature": 25.1,
            "humidity": 60.2,
            "soil_moisture": 42.0,
            "soil_raw": 1800,
        },
    }

    validate(instance=sample, schema=schema)


def test_payload_schema_invalid():
    schema = load_schema()

    invalid_sample = {
        "device": "esp32-node-1",
    }

    with pytest.raises(ValidationError):
        validate(instance=invalid_sample, schema=schema)
