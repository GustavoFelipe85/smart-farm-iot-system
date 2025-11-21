# Especificação Técnica da Arquitetura – Smart Farm IoT System (Fase 2)

A Fase 2 do Smart Farm IoT System consolida a arquitetura de software responsável pelo fluxo completo de dados IoT: aquisição → transporte → validação → persistência → visualização.  
Este documento descreve todos os componentes, suas responsabilidades e o fluxo operacional do sistema.

---

## 1. Visão Geral da Arquitetura

A arquitetura da Fase 2 segue o seguinte pipeline:

> **Nó IoT (ESP32 ou simulador) → Broker MQTT → Consumer Python → InfluxDB → Grafana**

Todos os módulos, exceto o dispositivo IoT, são executados via **Docker Compose**, garantindo reprodutibilidade, isolamento e facilidade de implantação.

---

## 2. Arquitetura Lógica

### 2.1. Nó IoT (ESP32 / Simulador)
- Gera leituras de temperatura, umidade do ar e umidade do solo.  
- Formata os dados em JSON conforme requisito da Fase 2.  
- Publica os dados no tópico MQTT `smartfarm/field1/device1/metrics`.  
- Na Fase 3 será substituído por sensores reais.

### 2.2. Broker MQTT (Mosquitto)
- Recebe publicações do nó IoT.  
- Aplica autenticação (usuário e senha).  
- Entrega mensagens para o subscriber (Consumer Python).  
- Opera com `allow_anonymous false`.

### 2.3. Consumer Python
- Inscrito no tópico MQTT principal.  
- Valida estrutura JSON:
  - formato  
  - campos obrigatórios  
  - tipos numéricos  
- Registra mensagens inválidas via logs.  
- Converte dados válidos para InfluxDB Line Protocol.  
- Escreve no bucket configurado.

### 2.4. Banco InfluxDB 2.x
- Armazena séries temporais com precisão de milissegundos.  
- Buckets configurados via variáveis de ambiente:  
  - organização  
  - token  
  - política de retenção  
- Suporta consultas via Flux.

### 2.5. Grafana
- Conecta-se ao InfluxDB como data source.  
- Exibe:
  - temperatura  
  - umidade do ar  
  - umidade do solo  
  - séries temporais combinadas  
- Painéis configuráveis para experimentação durante o mestrado.

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

---

## 4. Arquitetura Física (Containers)

Todos os serviços estão definidos no arquivo `docker-compose.yml`.

### 4.1. Serviços do Docker Compose

| Serviço             | Porta   | Função                  |
| ------------------- | ------- | ----------------------- |
| **Mosquitto MQTT**  | 1883    | Transporte de mensagens |
| **Consumer Python** | interno | Validação + ingestão    |
| **InfluxDB 2.x**    | 8086    | Banco time-series       |
| **Grafana**         | 3000    | Dashboards              |

### 4.2 Rede interna

* Todos os contêineres utilizam a rede Docker:

  ```
  smartfarm_network
  ```
* Isso garante isolamento e comunicação eficiente.

### 4.3 Volumes persistentes

* `influxdb_data` — dados do banco
* `grafana_data` — dashboards e configurações
* `mosquitto_data`, `mosquitto_log` — configs e logs do broker

---

## 5. Descrição do Processo Operacional

1. O nó IoT gera uma leitura.
2. O payload é convertido para JSON.
3. O JSON é publicado via MQTT.
4. O broker entrega a mensagem ao subscriber.
5. O Consumer Python valida e transforma os dados.
6. Os dados são gravados no InfluxDB.
7. O Grafana consulta continuamente o Influx e atualiza a visualização.

---

## 6. Segurança e Boas Práticas

* Conexões MQTT exigem usuário e senha.
* Nenhum segredo deve ser incluído diretamente no código.
* Todos os tokens e senhas devem estar em `.env`.
* Docker Compose deve ser configurado de forma imutável e reprodutível.

---

## 7. Limitações da Fase 2 (para desenvolvimento futuro)

As seguintes funcionalidades são **intencionais e formalmente deixadas para as Fases 3 e 4**:

* Sensores físicos (solo, temperatura, clima).
* Buffer local no ESP32.
* Validação de dados diretamente no dispositivo (edge).
* Automação de irrigação.
* Testes de campo reais.
* Algoritmos de aprendizado de máquina.
* Comparações científicas (latência, perdas, robustez).

---

## 8. Evolução da Arquitetura — Fases Futuras

### **Fase 3 – Laboratório**

* Integração com sensores reais
* Testes de calibração
* Firmware avançado
* Buffer e reconexão

### **Fase 4 – Campo e Análise**

* Implantação em ambiente agrícola
* Análise estatística e ML
* Métricas de latência, perdas, robustez
* Produção de artigo científico

---

**Documento alinhado à estrutura formal da Fase 2 do projeto e ao pré-projeto do mestrado.**

```

