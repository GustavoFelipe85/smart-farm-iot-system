import json, os
from jsonschema import validate

def test_payload_schema_ok():
    schema_path = os.path.join("src","backend","schemas","sensor_payload.json")
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    sample = {
        "device":"esp32-node-1",
        "ts":"2025-11-11T12:00:00",
        "metrics":{"temp":25.1,"umid":60.2,"soil":42.0}
    }
    validate(instance=sample, schema=schema)
