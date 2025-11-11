import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from influxdb_client import InfluxDBClient

INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG", "smartfarm")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "sensors")

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()

app = FastAPI(title="Smart Farm IoT API", version="0.1.0")

class IrrigationCmd(BaseModel):
    duration: int

@app.get("/api/v1/sensors/current")
def current():
    try:
        flux = f'''
        from(bucket:"{INFLUX_BUCKET}")
          |> range(start: -5m)
          |> filter(fn: (r) => r._measurement == "sensors")
          |> last()
        '''
        tables = query_api.query(org=INFLUX_ORG, query=flux)
        out = {}
        for t in tables:
            for r in t.records:
                dev = r.values.get("device", "unknown")
                out.setdefault(dev, {})
                out[dev][r.get_field()] = r.get_value()
        return out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/control/irrigation")
def control(cmd: IrrigationCmd):
    # stub: integrar com atuador real via MQTT (tópico: smartfarm/control/irrigation)
    if cmd.duration <= 0 or cmd.duration > 900:
        raise HTTPException(status_code=400, detail="duration inválido")
    return {"status": "scheduled", "duration": cmd.duration}
