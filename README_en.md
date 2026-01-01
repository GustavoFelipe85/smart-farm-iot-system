# 🚜 Smart Farm IoT System

🇧🇷 Versão em Português: [README.md](README.md)

### *Secure IoT Architecture for Environmental Monitoring in Precision Agriculture*

[![PT-BR](https://img.shields.io/badge/lang-PT--BR-green)](README.md)

![status](https://img.shields.io/badge/Phase%203-In%20Progress-blue)

---

## 📘 Executive Summary

The **Smart Farm IoT System** is a modular and secure IoT platform for environmental monitoring applied to precision agriculture.  
The solution integrates IoT sensors, authenticated MQTT communication, Python-based data processing, a time-series database (InfluxDB), and analytical dashboards in Grafana.

The entire architecture is containerized using Docker to ensure **portability, isolation, and experimental reproducibility**.

Currently, the repository corresponds to **Phase 2 (completed)**, while **Phases 3 and 4** focus on real hardware integration and agricultural automation and are planned to be developed during the graduate program.

---

> 📝 **This project is part of the selection process for the Graduate Program in Computer Science (PPGComp) – UNIOESTE.**  
> Development follows rigorous methodological principles and reproducibility guidelines, aligned with the *Computer Systems* research area (Call for Applications 11/2025).

---

## 🧪 CI Pipeline Status

⚠️ The CI pipeline is active and continuously validating the repository.

Current failures are related to **hardware-dependent integrations under development**, which are characteristic of **Phase 3 (Real Hardware / CELUS)**.

The pipeline is already prepared for full stabilization in later phases.

---

## 🎯 Project Objectives

- Design a **secure, modular, and replicable IoT architecture**
- Monitor air temperature, air humidity, and soil moisture
- Persist measurements in a **time-series database**
- Provide analytical dashboards for data exploration
- Establish a solid technical foundation for **automation, control, and ML**

---

## 📚 Official Documentation

All technical, academic, and planning documentation is available at:

➡️ [`/docs`](./docs)

---

## 📄 Technical Documents by Phase

| Phase | Document | Content | Status |
|-----|---------|--------|--------|
| Phase 1 | [`docs/fase1.md`](./docs/fase1.md) | IoT infrastructure, secure MQTT, communication baseline | ✅ Completed |
| Phase 2 | [`docs/fase2.md`](./docs/fase2.md) | Data ingestion, time-series persistence, dashboards | ✅ Completed |
| Phase 3 | [`docs/fase3.md`](./docs/fase3.md) | Real hardware, CELUS, laboratory testing | 🟡 In Progress |

---

## 🧩 Project Phases

The phases below represent the functional and architectural evolution of the system.

| Phase | Description | Status | Deliverables |
|-----|------------|--------|-------------|
| Phase 1 — IoT Infrastructure | Sensors, firmware, MQTT broker | ✅ Completed | ESP32 + Secure MQTT |
| Phase 2 — Processing & Visualization | Ingestion, persistence, dashboards | ✅ Completed | Python Consumer + InfluxDB + Grafana |
| **Phase 3 — Intelligent Expansion & Real Hardware** | API, automation, ML, **physical prototyping with CELUS** | 🟨 In Progress | Hardware v1 + FastAPI + ML |

📌 **Current status:** Phase 3 in progress (AI-assisted hardware design with CELUS).

---

## 🔧 CELUS Integration (Phase 3 — AI-assisted Hardware)

In **Phase 3**, the project transitions from simulation to **real hardware**.

Electronic design is developed using **CELUS Design Studio**, enabling:

- automated schematic generation (ESP32 + sensors)
- assisted PCB design
- standardized electronic documentation
- Bill of Materials (BOM)
- detailed pinout per module (MCU + sensors)
- reproducible laboratory and testing infrastructure

📎 **Phase 3 hardware exports (Hardware v1):**  
➡️ [`/hardware/celus-v1`](./hardware/celus-v1)

🔗 **CELUS Design Studio Project:**  
https://app.celus.io/design-studio/692de65654a678ec656686fe/design-canvas

---

## 🏗️ Implemented Architecture

```mermaid
flowchart LR
  subgraph EDGE[🌱 Edge - IoT Sensors]
    ESP[ESP32<br/>DHT22 + Soil]
  end

  subgraph COMM[📡 Secure Communication]
    MQ[MQTT Broker<br/>Mosquitto Secure]
  end

  subgraph PROC[⚙️ Processing]
    PY[Python Consumer<br/>JSON Validation]
  end

  subgraph DB[💾 Storage]
    INF[InfluxDB 2.7]
  end

  subgraph VIS[📊 Visualization]
    GF[Grafana 10.4<br/>Basic Dashboards]
  end

  ESP -->|MQTT Secure| MQ
  MQ -->|Validated Message| PY
  PY -->|Write Data| INF
  INF -->|Query| GF
````

---

## 🔧 Implemented Components (Phase 2 — Completed)

| Layer          | Technology       | Status | Function               |
| -------------- | ---------------- | ------ | ---------------------- |
| IoT Device     | ESP32 + Sensors  | ✅      | Environmental sensing  |
| Broker         | Mosquitto + Auth | ✅      | Secure communication   |
| Consumer       | Python 3.11      | ✅      | Validation + ingestion |
| Database       | InfluxDB 2.7     | ✅      | Time-series storage    |
| Visualization  | Grafana 10.4     | ✅      | Dashboards             |
| Infrastructure | Docker Compose   | ✅      | Orchestration          |

---

## ❌ What Is NOT Implemented (Academic Rigor)

| Feature                | Status        |
| ---------------------- | ------------- |
| FastAPI API            | ❌             |
| Automation (actuators) | ❌             |
| Machine Learning       | ❌             |
| Advanced dashboards    | ⚠️ Basic only |
| Alerts / Notifications | ❌             |
| Irrigation control     | ❌             |

---

## ⚙️ Operational Flow

### 1️⃣ Acquisition — ESP32

```json
{
  "device": "esp32-node-01",
  "timestamp": "2025-11-11T14:57:00Z",
  "metrics": {
    "temperature": 25.7,
    "humidity": 63.1,
    "soil_moisture": 41.2
  }
}
```

### 2️⃣ Transport — Secure MQTT

### 3️⃣ Ingestion — Python Consumer

### 4️⃣ Storage — InfluxDB

### 5️⃣ Visualization — Grafana

---

## 🧪 Experimental Methodology

* Sampling frequency: **30 s**
* MQTT QoS: **1**
* Full payload sanitization
* Retention policies applied
* Exploratory dashboards

---

## 📈 Results (Phase 2)

| Metric                  | Value              |
| ----------------------- | ------------------ |
| MQTT → Consumer latency | **< 120 ms**       |
| Ingestion rate          | **10,000+ msgs/h** |
| Docker uptime           | **99.9%**          |
| Retention               | configurable       |

---

## 🔐 Security Measures

* MQTT with `allow_anonymous false`
* File-based authentication
* Secrets handled via `.env`
* `.env.example` provided
* Isolated Docker network
* Grafana credentials via environment variables

---

## 🚀 Quick Start (5 minutes)

```bash
git clone https://github.com/GustavoFelipe85/smart-farm-iot-system
cd smart-farm-iot-system

cp .env.example .env

cd docker
docker-compose up -d
```

Access points:

* 📊 Grafana → [http://localhost:3000](http://localhost:3000)
* 💾 InfluxDB → [http://localhost:8086](http://localhost:8086)
* 📡 MQTT Broker → mqtt://localhost:1883

---

## 🎓 Academic Contributions

* Secure and modular IoT architecture
* Complete ingestion pipeline
* Reproducible scientific documentation
* Robust data validation
* Foundation for automation and ML research

---

## 📚 References

* Wolfert, S. et al. *Big Data in Smart Farming.* Agricultural Systems, 2017.
* Zhang, Y. *IoT Applications in Smart Agriculture.* JAI, 2022.
* ConectarAGRO. *Agriculture 4.0.*
* This work extends the undergraduate thesis:
  **“Limiting Factors and Applications of IoT in Agriculture” (UNISA)**
  [https://dspace.unisa.br/items/ab0577db-a4a9-4fc7-af72-d1b23e7345ed](https://dspace.unisa.br/items/ab0577db-a4a9-4fc7-af72-d1b23e7345ed)

---

## 👨‍💻 Author

**Gustavo Felipe Paluch Figueiredo**

B.Sc. in Computer Engineering
Universidade Santo Amaro (UNISA)

🔗 LinkedIn: [https://www.linkedin.com/in/gustavofpaluch](https://www.linkedin.com/in/gustavofpaluch)
📧 Email: [gustavo.f.p.f@outlook.com.br](mailto:gustavo.f.p.f@outlook.com.br)

---

📝 *This repository fully documents Phase 2 and establishes an experimental foundation for subsequent phases involving real hardware and agricultural automation.*

```

