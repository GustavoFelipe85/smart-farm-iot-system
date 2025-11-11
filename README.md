<p align="center">
  <img src="https://img.shields.io/badge/Projeto_Acadêmico-IoT%20%7C%20UNIOESTE-brightgreen?style=for-the-badge&logo=github" alt="Projeto Acadêmico IoT">
  
Entendido.
Vou entregar exatamente o que você pediu:

✅ **README híbrido**
✅ **Visual forte como o DeepSeek**
✅ **Com emojis e ilustrações gráficas**
✅ **Mas 100% coerente com o SEU projeto real**
✅ **Seguro para ser submetido à UNIOESTE**
✅ **Sem exageros, sem mentir funcionalidades**
✅ **Tom científico + design moderno**

---

# ✅ **🚀 PRONTO PARA USAR – README HÍBRIDO (VISUAL + CIENTÍFICO)**

Use este arquivo como **README.md oficial** no repositório.

---

````markdown
<div align="center">

# 🌾 Smart Farm IoT System  
### **Plataforma Inteligente de Monitoramento e Análise para Agricultura de Precisão**

📡 **IoT** • 📊 **Time-Series Analytics** • 🐍 **Python** • 🐳 **Docker** • 📈 **Grafana**  

[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge)]()
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)]()
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)]()
[![Docker](https://img.shields.io/badge/Docker-OK-2496ED?style=for-the-badge&logo=docker)]()

</div>

---

# 📘 Visão Geral

O **Smart Farm IoT System** é um ecossistema de monitoramento agrícola que integra sensores ambientais, comunicação MQTT, persistência de dados em séries temporais e visualização em tempo real.  

✅ Projeto baseado no TCC:  
**“Fatores e Aplicações Limitantes da IoT na Agricultura” – UNISA (2025)**  

✅ Evolução científica para **Mestrado UNIOESTE – Sistemas de Computação**.  

🎯 Foco: construir uma plataforma modular, científica e expandível para experimentação IoT aplicada à agricultura de precisão.

---

# 🎯 Objetivos do Projeto

- ✅ Monitoramento contínuo de **temperatura**, **umidade do ar**, **umidade do solo**  
- ✅ Transmissão eficiente via **MQTT com autenticação**  
- ✅ Armazenamento temporal usando **InfluxDB 2.x**  
- ✅ Visualização por **Grafana**  
- ✅ Arquitetura **modular** para permitir:
  - aprendizado de máquina (fase 3)  
  - controle inteligente de irrigação (fase 2)  
  - testes científicos e validação experimental  

---

# 🏗️ Arquitetura do Sistema

## 🔄 Fluxo de Dados

```mermaid
flowchart LR
    A[🌡️ ESP32 + Sensores] -->|MQTT| B[(📡 Mosquitto Broker)]
    B -->|Mensagem JSON| C[🐍 Python Consumer]
    C -->|Write| D[(💾 InfluxDB)]
    D -->|Query| E[📈 Grafana Dashboards]
````

✅ Arquitetura **real**, exatamente como implementada no repositório.

---

# 🧩 Componentes Principais

| Camada            | Tecnologia           | Função                            |
| ----------------- | -------------------- | --------------------------------- |
| 📡 Comunicação    | **MQTT (Mosquitto)** | Transporte leve e eficiente       |
| 🐍 Backend        | **Python Consumer**  | Processa mensagens e valida dados |
| 💾 Banco de Dados | **InfluxDB 2.x**     | Time-series database              |
| 📈 Visualização   | **Grafana**          | Dashboards e alertas              |
| 🔌 Edge IoT       | **ESP32**            | Leitura de sensores               |

---

# 📁 Estrutura do Repositório

```
smart-farm-iot-system/
├── docker/
│   ├── docker-compose.yml          # Orquestração
│   ├── mosquitto/                  # Configuração MQTT
│   ├── influxdb/                   # Armazenamento Influx
│   └── grafana/                    # Persistência Grafana
├── src/
│   ├── backend/python-consumer/    # Processamento MQTT → InfluxDB
│   ├── esp32/                      # Código fonte para microcontroladores
│   └── api/                        # (fase 2) API REST futura
├── docs/                           # Documentação acadêmica
├── tests/                          # Testes unitários
└── .env.example                    # Variáveis de ambiente
```

---

# 🐳 Docker – Infraestrutura

O sistema roda completamente em Docker para garantir:

✅ Reprodutibilidade
✅ Isolamento de serviços
✅ Testabilidade científica

### Comando básico

```bash
cd docker
docker compose up -d
```

---

# 🔧 Configuração via `.env`

Exemplo **seguro** para seu ambiente:

```bash
# MQTT
MQTT_BROKER=mosquitto
MQTT_PORT=1883
MQTT_USERNAME=iot_user
MQTT_PASSWORD=SenhaMQTT_2025!

# InfluxDB
INFLUX_URL=http://influxdb:8086
INFLUX_ORG=smartfarm
INFLUX_BUCKET=sensors
INFLUX_TOKEN=TokenInflux_2025!

# Grafana
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=Admin2025!
```

⚠️ Importante:
✅ `.env` **não deve ser commitado**
✅ Apenas `.env.example` fica no GitHub

---

# 📊 Dashboards (Grafana)

✅ Painéis principais recomendados:

* **Visão Geral do Ambiente**
* **Umidade do Solo x Tempo**
* **Temperatura/Humidade**
* **Taxa de mensagens MQTT**
* **Alertas e thresholds**

Adicione posteriormente capturas reais do painel para fortalecer apresentação.

---

# 🔬 Roteiro Científico (usado na banca)

### Contribuições acadêmicas

* Arquitetura IoT modular de baixo custo
* Pipeline MQTT → Python → InfluxDB replicável
* Base real para pesquisa de machine learning
* Reprodutibilidade científica via Docker
* Métricas verificáveis para agricultura de precisão

### Próximas fases

✅ **Fase 1:** Infraestrutura base
✅ **Fase 2:** Controle inteligente de irrigação
✅ **Fase 3:** Predição de necessidades hídricas (ML)
✅ **Fase 4:** Artigo científico para congresso/IEEE

---

# 🧪 Testes rápidos

### Publicar mensagem simulada

```bash
mosquitto_pub -h localhost -t "smartfarm/sensors" \
 -m '{"device":"test", "temp":25.4, "umid":60.1}' \
 -u iot_user -P SenhaMQTT_2025!
```

### Consultar dados no Influx

```bash
curl -G http://localhost:8086/api/v2/query \
  -H "Authorization: Token $INFLUX_TOKEN" \
  --data-urlencode 'q=from(bucket:"sensors") |> range(start: -10m)'
```

---

# 👨‍💻 Autor

**Gustavo Felipe Paluch Figueiredo**
Engenharia da Computação – UNISA

🔗 LinkedIn: [https://www.linkedin.com/in/gustavofpaluch](https://www.linkedin.com/in/gustavofpaluch)
📧 Email: [gustavo.f.p.f@outlook.com.br](mailto:gustavo.f.p.f@outlook.com.br)

---

<div align="center">

### ✨ “Tecnologia e ciência transformando a agricultura brasileira.”

### 🌱 Smart Farm IoT System – 2025

</div>

```

**📌 Documento técnico elaborado para fins acadêmicos no contexto do processo seletivo do Programa de Pós-Graduação em Ciência da Computação – UNIOESTE (EDITAL Nº 11/2025 - PPGComp.)**

---

## 🐳 Execução com Docker

A infraestrutura completa pode ser executada com Docker:


cd docker
docker-compose up -d

Serviços disponíveis:

📊 Grafana: http://localhost:3000

💾 InfluxDB: http://localhost:8086

📡 MQTT Broker: mqtt://localhost:1883

Veja docker/README.md para detalhes completos.

🤝 Contribuição
Contribuições são bem-vindas! Este é um projeto de pesquisa acadêmica.

🔗 Veja nosso Guia de Contribuição para detalhes.

👨‍🔬 Pesquisadores: Como replicar experimentos

💻 Desenvolvedores: Padrões de código

🤝 Parceiros: Colaborações acadêmicas


