[`smart-farm-iot-system`](https://github.com/GustavoFelipe85/smart-farm-iot-system), estruturado em **português técnico e acadêmico**, de acordo com boas práticas DevOps e documentação científica do projeto IoT descrito no seu pré-projeto:

---

````markdown
# 🌾 Smart Farm IoT System  
**Plataforma Inteligente de Monitoramento e Automação para Agricultura de Precisão**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/GustavoFelipe85/smart-farm-iot-system)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🧠 Visão Geral do Projeto
O **Smart Farm IoT System** é uma plataforma baseada em **Internet das Coisas (IoT)** aplicada à agricultura de precisão.  
O sistema integra sensores ambientais, automação de irrigação e análise de dados em tempo real para aumentar a eficiência hídrica e produtiva.

A arquitetura é modular, de código aberto, e utiliza tecnologias amplamente adotadas na indústria, como **MQTT (Mosquitto)**, **InfluxDB**, e **Grafana**, orquestradas via **Docker Compose**.

> **Base teórica:** Projeto derivado do TCC “Fatores e Aplicações Limitantes da IoT na Agricultura” (UNISA, 2025).  
> **Repositório:** [TCC no DSpace UNISA](https://dspace.unisa.br/items/ab0577db-a4a9-4fc7-af72-d1b23e7345ed)

---

## 🏗️ Arquitetura da Solução

A plataforma é composta por três serviços principais executados em containers Docker:

| Serviço     | Descrição                                                                 |
|--------------|---------------------------------------------------------------------------|
| **Mosquitto** | Broker MQTT responsável pela comunicação entre os sensores e o backend. |
| **InfluxDB**  | Banco de dados time-series para armazenar medições ambientais.          |
| **Grafana**   | Interface para visualização e análise dos dados coletados.              |

```mermaid
graph TD
    A[Sensores IoT - ESP32] -->|MQTT| B[Broker Mosquitto]
    B --> C[InfluxDB - Banco de Dados]
    C --> D[Grafana - Dashboards e Alertas]
````

---

## ⚙️ Infraestrutura (Docker Compose)

Arquivo: `docker/docker-compose.yml`

```yaml
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
```

---

## 📦 Estrutura do Projeto

```
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
├── backend/          # Scripts de ingestão e APIs (Python/Node.js)
├── dashboards/       # Painéis Grafana e templates
└── docs/             # Documentação técnica e relatórios
```

---

## 🚀 Instruções de Execução

### 1️⃣ Criar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
INFLUXDB_PASSWORD=StrongPass_2025!
GRAFANA_PASSWORD=StrongPass_2025!
```

### 2️⃣ Subir os containers

```bash
cd docker
docker compose --env-file ../.env up -d
```

### 3️⃣ Verificar os serviços

* Mosquitto: `localhost:1883`
* InfluxDB UI: [http://localhost:8086](http://localhost:8086)
* Grafana UI: [http://localhost:3000](http://localhost:3000)

---

## 🧩 Próximas Etapas de Desenvolvimento

* [ ] Adicionar sensores físicos (DHT22, YL-69, BMP280)
* [ ] Implementar API REST de coleta de dados
* [ ] Criar dashboards de irrigação e produtividade
* [ ] Integração com aprendizado de máquina (MLflow / Scikit-Learn)
* [ ] Publicação de artigo científico (IEEE ou SBC)

---

## 📚 Referências

* **WOLFERT, S. et al.** *Big Data in Smart Farming – A review.* Agricultural Systems, 153, p.69–80, 2017.
* **ZHANG, Y. et al.** *IoT Applications in Smart Agriculture: A Review.* Journal of Agricultural Informatics, 13(1), p.45–60, 2022.
* **ConectarAGRO.** Agricultura 4.0: Conectividade no campo. Disponível em: [https://conectaragro.com.br](https://conectaragro.com.br)

---

## 👨‍💻 Autor

**Gustavo Felipe Paluch Figueiredo**
Graduado em Engenharia da Computação – UNISA (2025)
[LinkedIn](https://www.linkedin.com/in/gustavofpaluch) | [Lattes](https://wwws.cnpq.br/cvlattesweb/PKG_MENU.menu?f_cod=6B7200F84D28E12A9BE8186ED261D2D4)

---

> © 2025 – Projeto acadêmico e experimental desenvolvido com fins de pesquisa e inovação tecnológica.

```


