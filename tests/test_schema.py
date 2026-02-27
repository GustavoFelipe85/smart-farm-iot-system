import pytest
from jsonschema.exceptions import ValidationError

def test_payload_schema_invalid():
    schema_path = os.path.join("src", "backend", "schemas", "sensor_payload.json")

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    invalid_sample = {
        "device": "esp32-node-1"
    }

    with pytest.raises(ValidationError):
        validate(instance=invalid_sample, schema=schema)
