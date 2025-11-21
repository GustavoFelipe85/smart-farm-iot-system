
# Arquitetura do Sistema – Smart Farm IoT System (Fase 2)

Este documento descreve a arquitetura atual do projeto Smart Farm IoT System, correspondente à Fase 2 (pipeline IoT completo). A arquitetura inclui o nó IoT, o broker MQTT, o consumer em Python, o banco de dados InfluxDB e os dashboards Grafana.

---

## 1. Visão Geral da Arquitetura

A arquitetura do sistema segue o fluxo:

**Nó IoT → Broker MQTT → Consumer Python → InfluxDB → Grafana**

Todos os serviços (exceto o dispositivo IoT) são executados via Docker Compose.

---

## 2. Componentes da Arquitetura

### **2.1. Nó IoT (ESP32 ou simulador)**
- Realiza leitura de sensores (simulados na Fase 2)
- Formata dados em JSON
- Publica métricas no broker MQTT

### **2.2. Broker MQTT (Mosquitto)**
- Gerencia tópicos de publicação
- Aplica autenticação
- Entrega mensagens ao consumer Python

### **2.3. Consumer Python**
- Assina tópicos MQTT
- Valida JSON (estrutura, tipos e campos)
- Insere dados válidos no InfluxDB
- Gera logs de inconsistências

### **2.4. Banco InfluxDB 2.x**
- Armazena métricas time-series
- Buckets configurados via variáveis de ambiente
- API para consultas via Grafana

### **2.5. Grafana**
- Painéis dinâmicos para monitoramento
- Integração nativa com InfluxDB
- Visualização histórica e quase em tempo real

---

## 3. Fluxo de Dados Ponta-a-Ponta

```mermaid
flowchart LR
    subgraph Device["No IoT (ESP32 / Simulador)"]
        sensor["Leitura sensores temperatura e umidade"]
    end

    subgraph Broker["Mosquitto MQTT"]
        mqtt[(Broker MQTT)]
    end

    subgraph Backend["Backend e Storage"]
        consumer["Consumer Python - validacao e ingestao"]
        influx[(InfluxDB 2.x)]
    end

    subgraph Visualization["Visualizacao"]
        grafana["Grafana Dashboards"]
    end

    sensor -->|JSON MQTT| mqtt
    mqtt -->|Subscribe| consumer
    consumer -->|Write| influx
    grafana -->|Query| influx

````
## 4. Arquitetura Física (Containers)

Todos os serviços estão definidos no arquivo `docker-compose.yml`:

* **mqtt-broker** → Porta 1883
* **consumer** → Python 3.11
* **influxdb** → Porta 8086
* **grafana** → Porta 3000

Os serviços utilizam network Docker interna.

---

## 5. Evolução da Arquitetura

### **Fase 3 (Laboratório):**

* Sensores físicos reais
* Buffer local no ESP32
* Validação no edge
* Firmwares mais avançados

### **Fase 4 (Campo):**

* Coleta real em ambiente agrícola
* Análise científica
* Algoritmos de ML
* Comparações edge vs backend

---

**Documento atualizado para uso acadêmico e técnico na Fase 2 do projeto.**

````

---

# ✅ **2. Caminho correto da seção: “5. Taxa de Envio e Operação”**

Ela deve ficar dentro do arquivo:

📁 **`docs/requisitos.md`**

E exatamente **na seção 5** do documento (já existe e está correta).

Aqui está o trecho exato para colar dentro do arquivo:

```markdown
## 5. Taxa de Envio e Operação

### Frequência padrão de envio
O nó IoT (ESP32 ou simulador) deve enviar leituras em intervalos fixos de:

**→ 30 segundos (padrão da Fase 2)**

Isso garante:
- carga estável para o broker MQTT
- granularidade adequada para séries temporais
- consumo energético reduzido

### Estrutura do tópico MQTT
Todas as métricas devem ser enviadas seguindo um padrão hierárquico:

````

smartfarm/field1/device1/metrics

```

Regras:
- `smartfarm/` → namespace geral do projeto  
- `field1/` → campo ou área monitorada  
- `device1/` → identificador lógico do nó  
- `metrics` → tópico de publicação de dados ambientais  
```

