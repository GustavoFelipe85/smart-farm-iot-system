<p align="center">
  <img src="https://img.shields.io/badge/Projeto_Acadêmico-IoT%20%7C%20UNIOESTE-brightgreen?style=for-the-badge&logo=github" alt="Projeto Acadêmico IoT">
</p>

# 🚜 Smart Farm IoT System
### *Arquitetura IoT Segura para Monitoramento Ambiental em Agricultura de Precisão*

<div align="center">

![Docker](https://img.shields.io/badge/Docker-OK-2496ED?style=for-the-badge&logo=docker)
![MQTT](https://img.shields.io/badge/MQTT-Secure-660066?style=for-the-badge&logo=eclipse)
![InfluxDB](https://img.shields.io/badge/InfluxDB-2.7-22ADF6?style=for-the-badge&logo=influxdb)
![Grafana](https://img.shields.io/badge/Grafana-10.4-FF9800?style=for-the-badge&logo=grafana)
![Python](https://img.shields.io/badge/Python-Consumer-3776AB?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

---

# 📘 Resumo Executivo

O Smart Farm IoT System é uma plataforma modular de monitoramento ambiental agrícola, baseada em uma arquitetura IoT segura e containerizada.

O sistema implementa:

- Captura via ESP32 + sensores  
- Comunicação MQTT autenticada (Mosquitto)  
- Ingestão e validação em Python  
- Armazenamento time-series em InfluxDB  
- Dashboards analíticos no Grafana  

Funcionalidades como API, automação, ML e atuadores serão implementadas nas Fases 3 e 4.

---

> 📝 **Projeto integrante do processo seletivo do Programa de Pós-Graduação em Ciência da Computação (PPGComp) – UNIOESTE.**  
> Desenvolvimento conduzido com rigor metodológico e reprodutibilidade, alinhado à linha *Sistemas de Computação*, conforme Edital 11/2025.

Este repositório documenta integralmente a **Fase 2**, incluindo:

- arquitetura distribuída  
- pipeline IoT completo  
- validação de dados  
- persistência estruturada  
- dashboards analíticos  
- documentação técnica formal  

As **Fases 3 e 4** (sensores reais, laboratório, campo, automação e ML) serão executadas durante o Mestrado.

---

# 🎯 Objetivos do Projeto

- Criar uma arquitetura IoT segura, replicável e modular  
- Monitorar temperatura, umidade do ar e umidade do solo  
- Registrar medições em banco time-series  
- Disponibilizar dashboards analíticos  
- Construir base técnica para automação, controle e ML  

---

# 🧩 Fases do Projeto

| Fase | Descrição | Status | Entregas |
|------|------------|--------|-----------|
| **1️⃣ Fase 1 — Infraestrutura IoT** | Sensores, firmware e MQTT Broker | ✅ Concluída | ESP32 + MQTT Secure |
| **2️⃣ Fase 2 — Processamento e Visualização** | Ingestão, persistência e dashboards | ✅ Concluída | Python Consumer + InfluxDB + Grafana |
| **3️⃣ Fase 3 — Expansão Inteligente** | API, automação e ML | 🔜 Planejada | FastAPI + Controle + ML |

> 💡 **Status Atual:** Repositório corresponde à **Fase 2 concluída**.

---

## 🔧 Integração com CELUS (Fase 3 — Hardware Assistido por IA)

Na Fase 3 o projeto passa da simulação para o hardware real.  
O design eletrônico é desenvolvido dentro do **CELUS Design Studio**, permitindo:

- geração automatizada de esquemas eletrônicos (ESP32 + sensores)
- criação assistida de PCB
- documentação eletrônica padronizada
- lista de materiais (BOM)
- pinout detalhado por cubo (MCU + sensores)
- infraestrutura reprodutível para laboratório e testes

📎 **Arquivos exportados da Fase 3 (Hardware v1) estão em:**  
`/hardware/celus-v1/`

🔗 **Link do projeto no CELUS:**  
https://app.celus.io/design-studio/692de65654a678ec656686fe/design-canvas

---

# 🏗️ Arquitetura Implementada

```mermaid
flowchart LR
  subgraph EDGE[🌱 Edge - Sensores IoT]
    ESP[ESP32<br/>DHT22 + Solo]
  end

  subgraph COMM[📡 Comunicação Segura]
    MQ[MQTT Broker<br/>Mosquitto Secure]
  end

  subgraph PROC[⚙️ Processamento]
    PY[Python Consumer<br/>JSON Validation]
  end

  subgraph DB[💾 Armazenamento]
    INF[InfluxDB 2.7]
  end

  subgraph VIS[📊 Visualização]
    GF[Grafana 10.4<br/>Dashboards Básicos]
  end

  ESP -->|MQTT Secure| MQ
  MQ -->|Mensagem Validada| PY
  PY -->|Write Data| INF
  INF -->|Consulta| GF
```
# 🔧 **Componentes Implementados (Fase 2 – Concluída)**

| Camada       | Tecnologia       | Status | Função               |
| ------------ | ---------------- | ------ | -------------------- |
| IoT Device   | ESP32 + Sensores | ✅      | Captura ambiental    |
| Broker       | Mosquitto + Auth | ✅      | Comunicação segura   |
| Consumer     | Python 3.11      | ✅      | Validação + ingestão |
| Banco        | InfluxDB 2.7     | ✅      | Time-series          |
| Visualização | Grafana 10.4     | ✅      | Dashboards           |
| Infra        | Docker Compose   | ✅      | Orquestração         |

---

# ❌ **O que NÃO existe (rigor acadêmico)**

| Funcionalidade        | Status            |
| --------------------- | ----------------- |
| API FastAPI           | ❌                 |
| Automação (atuadores) | ❌                 |
| Machine Learning      | ❌                 |
| Dashboards avançados  | ⚠️ Apenas básicos |
| Alertas/Notificações  | ❌                 |
| Controle de irrigação | ❌                 |

---

# ⚙️ **Fluxo Operacional**

### 1️⃣ Captura — ESP32

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

### 2️⃣ Transporte — MQTT Seguro (Auth)

### 3️⃣ Ingestão — Python Consumer

* valida JSON
* trata erros
* rejeita payload inválido
* grava no InfluxDB

### 4️⃣ Armazenamento — InfluxDB 2.7

### 5️⃣ Visualização — Grafana

---

# 🧪 **Metodologia Operacional**

* Frequência de amostragem: **30s**
* MQTT QoS: **1**
* Sanitização completa do payload
* Persistência com política de retenção
* Dashboards exploratórios

---

# 📈 **Resultados Obtidos (Fase 2)**

| Indicador                | Valor              |
| ------------------------ | ------------------ |
| Latência MQTT → Consumer | **< 120 ms**       |
| Taxa de ingestão         | **10.000+ msgs/h** |
| Uptime (Docker)          | **99.9%**          |
| Retenção                 | configurável       |

---

# 🔐 **Segurança Implementada**

* MQTT com `allow_anonymous false`
* Autenticação por arquivo `passwords`
* Variáveis sensíveis no `.env`
* `.env.example` fornecido
* Rede Docker isolada
* Senha do Grafana via env

---

# 📘 **.env.example (versão final)**

```bash
# MQTT
MQTT_BROKER=mosquitto
MQTT_PORT=1883
MQTT_USERNAME=iot_user
MQTT_PASSWORD=SUA_SENHA_AQUI

# INFLUXDB
INFLUX_URL=http://influxdb:8086
INFLUX_ORG=smartfarm
INFLUX_BUCKET=sensors
INFLUX_TOKEN=SUA_CHAVE_INFLUX

# GRAFANA
GRAFANA_PASSWORD=SUA_SENHA_GRAFANA
```

---

# 🚀 **Quick Start (5 minutos)**

```bash
git clone https://github.com/GustavoFelipe85/smart-farm-iot-system
cd smart-farm-iot-system

copy .env.example .env  # Windows
cp .env.example .env    # Linux / macOS

cd docker
docker-compose up -d
```

Acessos:

* 📊 Grafana → [http://localhost:3000](http://localhost:3000)
* 💾 InfluxDB → [http://localhost:8086](http://localhost:8086)
* 📡 MQTT Broker → mqtt://localhost:1883

---

# 🎓 **Contribuições Acadêmicas**

* Arquitetura IoT modular e segura
* Pipeline completo de ingestão
* Documentação científica reprodutível
* Validação robusta de dados
* Base para ML e automação

---

# 📚 **Referências**

* Wolfert, S. et al. *Big Data in Smart Farming.* Agricultural Systems, 2017.
* Zhang, Y. *IoT Applications in Smart Agriculture.* JAI, 2022.
* ConectarAGRO. *Agricultura 4.0.*
* Este trabalho evolui do TCC: 
[📘 TCC – “Fatores e Aplicações Limitantes da IoT na Agricultura” (UNISA)](https://dspace.unisa.br/items/ab0577db-a4a9-4fc7-af72-d1b23e7345ed)

---

# 👨‍💻 **Autor**

**Gustavo Felipe Paluch Figueiredo**

Bacharelado em Engenharia da Computação 

Universidade Santo Amaro (Unisa)

🔗 LinkedIn: [https://www.linkedin.com/in/gustavofpaluch](https://www.linkedin.com/in/gustavofpaluch)

📧 Email: [gustavo.f.p.f@outlook.com.br](mailto:gustavo.f.p.f@outlook.com.br)

---

<div align="center">

### ✨ “Tecnologia e ciência transformando a agricultura brasileira.”

📌 Documento técnico elaborado para o processo seletivo do **PPGComp – UNIOESTE (Edital 11/2025)**

Este repositório documenta integralmente a **Fase 2**, concluída com foco em rigor metodológico, reprodutibilidade e aderência às diretrizes de pesquisa em Sistemas de Computação.

---

# 📚 Documentação Oficial (Fase 2)

Este repositório inclui toda a documentação técnica referente à Fase 2 do projeto, contendo requisitos, arquitetura, diagramas e histórico de versões.

- [Requisitos do Sistema (Fase 2)](docs/requisitos.md)
- [Especificação Técnica da Arquitetura](docs/especificacao_arquitetura.md)
- [Diagrama da Arquitetura (Mermaid)](docs/architecture.md)
- [Histórico de Versões e Roadmap](docs/versoes.md)

---

## 🧩 Hardware (Fase 3)

O hardware do projeto Smart Farm IoT System — incluindo o protótipo baseado em ESP32-S3, sensores ambientais e sensor capacitivo de solo — está documentado na pasta:

➡️ **[/hardware](hardware/)**

Lá você encontra:

- Estrutura completa do hardware
- Versão celus-v1 do design (prototipagem assistida por IA)
- Esquemáticos, BOM e canvas (ao serem exportados)
- Datasheets oficiais
- Planejamento para a PCB v2 (laboratório / mestrado)


---


