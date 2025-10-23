🌾 Smart Farm IoT System

Plataforma Inteligente de Monitoramento e Automação para Agricultura de Precisão




🧠 Visão Geral do Projeto

O Smart Farm IoT System é uma plataforma modular de Internet das Coisas (IoT) aplicada à agricultura de precisão, com foco em eficiência hídrica e energética.
O sistema coleta dados ambientais por meio de sensores de baixo custo, armazena-os em um banco de dados de séries temporais e os apresenta em dashboards interativos para análise e automação agrícola.

Baseado em princípios de computação ubíqua, análise de dados em tempo real e arquitetura escalável via contêineres, o projeto tem como objetivo apoiar pesquisas acadêmicas e o desenvolvimento sustentável no campo.

📘 Base teórica: Projeto derivado do TCC “Fatores e Aplicações Limitantes da IoT na Agricultura
” (UNISA, 2025).

🏗️ Arquitetura da Solução

A infraestrutura é composta por três serviços principais executados em containers Docker, conectados em rede local:

Serviço	Função
Mosquitto	Broker MQTT responsável pela comunicação entre sensores e backend.
InfluxDB	Banco de dados de séries temporais que armazena medições ambientais.
Grafana	Interface de visualização e análise de dados coletados em tempo real.
graph TD
    A[Sensores IoT - ESP32] -->|MQTT| B[Broker Mosquitto]
    B --> C[InfluxDB - Banco de Dados]
    C --> D[Grafana - Dashboards e Alertas]

⚙️ Infraestrutura (Docker Compose)

Arquivo: docker/docker-compose.yml

version: "3.8"

networks:
  iot-network:
    driver: bridge

services:
  mosquitto:
    image: eclipse-mosquitto:2
    container_name: mosquitto
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
    restart: unless-stopped
    networks:
      - iot-network

  influxdb:
    image: influxdb:2.7
    container_name: influxdb
    ports:
      - "8086:8086"
    volumes:
      - ./influxdb/data:/var/lib/influxdb2
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=${INFLUXDB_PASSWORD}
      - DOCKER_INFLUXDB_INIT_ORG=smartfarm
      - DOCKER_INFLUXDB_INIT_BUCKET=sensors
    restart: unless-stopped
    networks:
      - iot-network

  grafana:
    image: grafana/grafana:10.4.2
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    depends_on:
      - influxdb
    restart: unless-stopped
    networks:
      - iot-network

📦 Estrutura do Projeto
smart-farm-iot-system/
├── docker/
│   ├── docker-compose.yml
│   ├── mosquitto/
│   │   ├── config/
│   │   ├── data/
│   │   └── log/
│   └── influxdb/
│       └── data/
├── firmware/         # Códigos embarcados (ESP32)
├── backend/          # Scripts e APIs (Python/Node.js)
├── dashboards/       # Painéis Grafana
└── docs/             # Documentação técnica e relatórios

🚀 Instruções de Execução

1️⃣ Criar variáveis de ambiente
Crie um arquivo .env na raiz do projeto:

INFLUXDB_PASSWORD=StrongPass_2025!
GRAFANA_PASSWORD=StrongPass_2025!


2️⃣ Iniciar os containers

cd docker
docker compose --env-file ../.env up -d


3️⃣ Verificar os serviços

Mosquitto → localhost:1883

InfluxDB UI → http://localhost:8086

Grafana UI → http://localhost:3000

🧩 Próximas Etapas

Adicionar sensores físicos (DHT22, YL-69, BMP280)

Implementar API REST de coleta de dados

Criar dashboards de irrigação e produtividade

Integrar aprendizado de máquina (Scikit-Learn / MLflow)

Redigir artigo científico para congresso (IEEE / SBC)

📚 Referências

WOLFERT, S. et al. Big Data in Smart Farming – A review. Agricultural Systems, v.153, p.69–80, 2017.

ZHANG, Y. et al. IoT Applications in Smart Agriculture: A Review. Journal of Agricultural Informatics, v.13, n.1, p.45–60, 2022.

ConectarAGRO. Agricultura 4.0: Conectividade no campo. Disponível em: https://conectaragro.com.br

👨‍💻 Autor

Gustavo Felipe Paluch Figueiredo
Graduado em Engenharia da Computação – UNISA (2025)
📎 LinkedIn
 • Lattes

© 2025 – Projeto acadêmico e experimental desenvolvido com fins de pesquisa e inovação tecnológica.
