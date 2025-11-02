# Arquitetura do Sistema Smart Farm IoT

## Visão Geral
Sistema de monitoramento de temperatura e umidade para agricultura de precisão usando ESP32, MQTT, InfluxDB e Grafana.

## Diagrama de Arquitetura

## Componentes

### 1. Firmware ESP32
- **Microcontrolador**: ESP32 com sensor DHT22
- **Função**: Coleta temperatura e umidade a cada 5 segundos
- **Comunicação**: WiFi + MQTT
- **Payload**: JSON `{"device":"esp32-node-1","temp":24.3,"umid":60.1}`

### 2. Broker MQTT (Mosquitto)
- **Porta**: 1883
- **Tópico**: `smartfarm/sensors`
- **Persistência**: Ativada

### 3. Consumer Python
- **Função**: Consome mensagens MQTT e grava no InfluxDB
- **Bibliotecas**: paho-mqtt, influxdb-client
- **Estrutura de dados**: Measurement `environment` com fields `temperature` e `humidity`

### 4. Banco de Dados (InfluxDB)
- **Porta**: 8086
- **Bucket**: `sensors`
- **Org**: `smartfarm`
- **Medição**: `environment`

### 5. Dashboard (Grafana)
- **Porta**: 3000
- **Dashboard**: `smart-farm-overview`
- **Fontes de dados**: InfluxDB (Flux queries)

## Fluxo de Dados
1. ESP32 lê sensor e publica no MQTT
2. Python consumer escuta tópico e processa mensagens
3. Dados são escritos no InfluxDB com timestamp
4. Grafana consulta InfluxDB e atualiza dashboard

## Segurança
- Token de autenticação no InfluxDB
- Senhas em variáveis de ambiente
- Rede local isolada para dispositivos IoT
