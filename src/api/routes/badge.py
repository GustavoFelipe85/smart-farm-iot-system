from fastapi import APIRouter, Response
from influxdb_client import InfluxDBClient
import os

router = APIRouter()

# Instanciação via variáveis injetadas pelo Docker Compose
INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "")
INFLUX_ORG = os.getenv("INFLUX_ORG", "smartfarm")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "smartfarm_bucket")

@router.get("/metrics/badge.svg", response_class=Response)
async def get_telemetry_badge():
    """Gera o selo SVG dinâmico com a última leitura do InfluxDB."""
    
    # Consulta Flux otimizada (Busca apenas a última hora e extrai o último registro)
    query = f"""
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "environment")
      |> filter(fn: (r) => r._field == "temperature" or r._field == "humidity")
      |> last()
    """
    
    temp, hum = "--", "--"
    
    try:
        with InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG) as client:
            tables = client.query_api().query(query, org=INFLUX_ORG)
            for table in tables:
                for record in table.records:
                    if record.get_field() == "temperature":
                        temp = f"{record.get_value():.1f}"
                    elif record.get_field() == "humidity":
                        hum = f"{record.get_value():.1f}"
    except Exception:
        # Falha segura: omite o erro do frontend e exibe o selo neutro
        pass

    # Template SVG paramétrico
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="220" height="20">
      <linearGradient id="b" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
      </linearGradient>
      <mask id="a">
        <rect width="220" height="20" rx="3" fill="#fff"/>
      </mask>
      <g mask="url(#a)">
        <path fill="#555" d="M0 0h75v20H0z"/>
        <path fill="#4c1" d="M75 0h145v20H75z"/>
        <path fill="url(#b)" d="M0 0h220v20H0z"/>
      </g>
      <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,sans-serif" font-size="11">
        <text x="37.5" y="15" fill="#010101" fill-opacity=".3">A715</text>
        <text x="37.5" y="14">A715</text>
        <text x="147.5" y="15" fill="#010101" fill-opacity=".3">{temp}°C | {hum}% HR</text>
        <text x="147.5" y="14">{temp}°C | {hum}% HR</text>
      </g>
    </svg>"""

    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }

    return Response(content=svg, media_type="image/svg+xml", headers=headers)
