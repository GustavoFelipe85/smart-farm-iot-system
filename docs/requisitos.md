# Requisitos do Sistema – Smart Farm IoT System (Fase 2)

## 1. Visão Geral

O Smart Farm IoT System é uma plataforma distribuída para monitoramento ambiental aplicada à agricultura de precisão.  
A Fase 2 tem como foco a consolidação do pipeline de dados IoT:

> Dispositivo (ESP32/simulador) → Broker MQTT → Consumer Python → InfluxDB → Grafana

Esta fase não trata ainda de sensores avançados nem automação de irrigação; esses elementos serão desenvolvidos nas Fases 3 e 4, em ambiente de laboratório.

---

## 2. Requisitos Funcionais

**RF01 – Coleta de dados ambientais**  
O sistema deve coletar periodicamente leituras de temperatura, umidade do ar e umidade do solo a partir de um nó IoT (ESP32 ou simulador).

**RF02 – Publicação via MQTT**  
O nó IoT deve publicar as leituras em um tópico MQTT configurado, em formato JSON.

**RF03 – Validação de payload**  
O serviço consumer em Python deve validar o payload recebido (estrutura JSON, campos obrigatórios e tipos) e descartar mensagens inválidas ou incompletas.

**RF04 – Armazenamento em banco time-series**  
As mensagens válidas devem ser persistidas em um bucket do InfluxDB 2.x, com timestamp e tags adequadas (ex.: `device_id`, `sensor_type`).

**RF05 – Dashboard de monitoramento**  
O sistema deve disponibilizar dashboards no Grafana para visualização de séries históricas e dados em tempo quase real.

**RF06 – Configuração via variáveis de ambiente**  
Parâmetros sensíveis (usuários, senhas, URLs) devem ser configuráveis via variáveis de ambiente, sem exposição direta em código.

**RF07 – Execução via Docker Compose**  
Todos os serviços da Fase 2 (MQTT, consumer, InfluxDB, Grafana) devem ser executáveis através de um `docker-compose up`.

---

## 3. Requisitos Não Funcionais

**RNF01 – Desempenho**  
O sistema deve ser capaz de processar, no mínimo, 10.000 mensagens/hora sem perda significativa de desempenho, em ambiente de laboratório.

**RNF02 – Latência**  
O tempo médio entre a publicação MQTT e a persistência no InfluxDB deve ser inferior a 200 ms em condições normais de rede local.

**RNF03 – Confiabilidade**  
Falhas em um dos serviços não devem corromper os dados já armazenados. Após reinício, o sistema deve retornar ao estado operacional normal.

**RNF04 – Segurança básica**  
O broker MQTT não deve permitir conexões anônimas. Usuários e senhas devem ser exigidos para publicação e assinatura.

**RNF05 – Reprodutibilidade**  
Um usuário com Docker instalado deve ser capaz de replicar o ambiente executando apenas os comandos e instruções descritos no README.

**RNF06 – Extensibilidade**  
A arquitetura deve permitir a adição futura de novos sensores, tópicos MQTT, atuadores e módulos de análise sem grandes mudanças estruturais.

---

## 4. Formato do Payload MQTT (Fase 2)

```json
{
  "device_id": "esp32-01",
  "timestamp": "2025-01-01T12:00:00Z",
  "temperature": 25.3,
  "humidity_air": 60.5,

Campos obrigatórios:

device_id (string)

timestamp (ISO 8601)

temperature (float)

humidity_air (float)

humidity_soil (float)
  "humidity_soil": 45.2
}
