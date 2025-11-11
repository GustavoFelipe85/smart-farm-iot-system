import requests

def test_api_current():
    r = requests.get("http://localhost:8000/api/v1/sensors/current", timeout=5)
    assert r.status_code == 200
