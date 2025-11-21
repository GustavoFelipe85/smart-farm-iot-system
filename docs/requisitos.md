# Requisitos do Sistema – Smart Farm IoT System (Fase 2)

## 1. Visão Geral

A Fase 2 do Smart Farm IoT System especifica os requisitos necessários para a consolidação do pipeline IoT:

> Nó IoT (ESP32 / Simulador) → Broker MQTT → Consumer Python → InfluxDB → Grafana

O objetivo desta fase é estabelecer a base técnica, garantir reprodutibilidade e documentar os requisitos funcionais e não funcionais antes da integração com sensores reais (Fase 3) e testes de campo (Fase 4).

---

## 2. Requisitos Funcionais (RF)

**RF01 – Coleta de dados ambientais**  
O sistema deve coletar periodicamente leituras de temperatura, umidade do ar e umidade do solo (simuladas nesta fase).

**RF02 – Publicação via MQTT**  
O nó IoT deve publicar um payload JSON em um tópico MQTT específico.

**RF03 – Validação do payload**  
O consumer Python deve validar se cada mensagem possui todos os campos obrigatórios e tipos corretos.

**RF04 – Armazenamento no InfluxDB**  
O consumer deve persistir as leituras válidas no InfluxDB, organizando por timestamps e tags.

**RF05 – Visualização via Grafana**  
O sistema deve possuir dashboards com gráficos históricos das medições.

**RF06 – Configuração via variáveis de ambiente**  
Credenciais, URLs e parâmetros sensíveis não devem estar hardcoded.

**RF07 – Execução via Docker Compose**  
Todo o pipeline (MQTT, Consumer, InfluxDB, Grafana) deve subir com o comando:

```

docker-compose up -d

````

---

## 3. Requisitos Não Funcionais (RNF)

**RNF01 – Desempenho**  
Processar pelo menos 10.000 mensagens/hora sem degradação significativa.

**RNF02 – Latência**  
Latência média MQTT → InfluxDB deve ser < 200 ms em rede local.

**RNF03 – Confiabilidade**  
O sistema deve se recuperar após falhas sem perda de dados já processados.

**RNF04 – Segurança**  
O broker MQTT deve operar com autenticação habilitada (`allow_anonymous false`).

**RNF05 – Reprodutibilidade**  
Qualquer usuário deve conseguir executar o ambiente apenas com Docker instalado.

**RNF06 – Extensibilidade**  
A arquitetura deve permitir novos sensores, tópicos e módulos sem grandes mudanças.

---

## 4. Formato do Payload MQTT

```json
{
  "device_id": "esp32-01",
  "timestamp": "2025-01-01T12:00:00Z",
  "temperature": 25.3,
  "humidity_air": 60.5,
  "humidity_soil": 45.2
}
````

### Campos obrigatórios

* `device_id`
* `timestamp` (ISO 8601)
* `temperature`
* `humidity_air`
* `humidity_soil`

---

## 5. Taxa de Envio e Operação

### Frequência padrão de envio

A taxa de envio das medições deve ser:

**→ 1 leitura a cada 30 segundos**

### Estrutura do tópico MQTT

O padrão hierárquico de publicação é:

```
smartfarm/<area>/<device>/metrics
```

**Exemplo real utilizado nesta fase:**

```
smartfarm/field1/device1/metrics
```

Esse padrão facilita:

* organização dos dispositivos
* segmentação por ambientes de coleta
* escalabilidade para Fase 3 e Fase 4

---

## 6. Escopo da Fase 2

### Incluído nesta fase:

* Pipeline completo MQTT → Consumer Python → InfluxDB → Grafana
* Validação de JSON
* Dashboards usuais
* Documentação inicial (requisitos, arquitetura, especificações)

### Fora do escopo desta fase (próximas etapas):

* Integração com sensores reais
* Firmware avançado (buffer, validação no edge)
* Automação de irrigação
* Testes de campo
* Algoritmos de ML
* Coleta com hardware real em ambiente agrícola

Esses itens pertencem às **Fase 3 e Fase 4**, a serem desenvolvidas com laboratório durante o mestrado.

---
