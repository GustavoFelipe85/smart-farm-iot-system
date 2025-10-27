# 🐳 Infraestrutura Docker

## 🚀 Inicialização Rápida

```bash
# 1. Copie o arquivo de ambiente
cp .env.example .env

# 2. Execute os serviços
docker-compose up -d

# 3. Verifique os serviços
docker-compose ps

🌐 Serviços Disponíveis
Serviço	URL	Credenciais
Grafana	http://localhost:3000	admin / ${GRAFANA_PASSWORD}
InfluxDB	http://localhost:8086	admin / ${INFLUXDB_PASSWORD}
MQTT Broker	mqtt://localhost:1883	-
