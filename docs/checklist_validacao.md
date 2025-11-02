# Checklist de Validação do Sistema

## ✅ Infraestrutura
- [ ] Docker e Docker Compose instalados
- [ ] Serviços sobem sem erro: `docker-compose up -d`
- [ ] Mosquitto acessível na porta 1883
- [ ] InfluxDB acessível na porta 8086
- [ ] Grafana acessível na porta 3000

## ✅ Configuração InfluxDB
- [ ] Bucket `sensors` criado
- [ ] Org `smartfarm` configurada
- [ ] Token de API gerado e salvo no `.env`

## ✅ Firmware ESP32
- [ ] WiFi conecta na rede
- [ ] DHT22 lê temperatura/umidade corretamente
- [ ] Publica JSON válido no tópico MQTT
- [ ] Payload segue schema: `{"device":"id","temp":float,"umid":float}`

## ✅ Consumer Python
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas: `pip install -r requirements.txt`
- [ ] Arquivo `.env` configurado com token
- [ ] Conecta no broker MQTT
- [ ] Grava dados no InfluxDB sem erro

## ✅ Dashboard Grafana
- [ ] Fonte de dados InfluxDB configurada
- [ ] Dashboard importado do JSON
- [ ] Dados aparecem em tempo real
- [ ] Gráficos atualizam automaticamente

## ✅ Teste de Fluxo Completo
- [ ] ESP32 publica dados
- [ ] Consumer processa e grava
- [ ] Grafana mostra dados atualizados
- [ ] Dados persistem após restart

## Comandos de Verificação
```bash
# Verificar serviços
docker ps

# Testar MQTT
mosquitto_pub -h localhost -t "smartfarm/sensors" -m '{"device":"test","temp":25.0,"umid":65.0}'

# Verificar dados InfluxDB
curl -G http://localhost:8086/api/v2/query?org=smartfarm \
  -H "Authorization: Token smartfarm-token-12345" \
  --data-urlencode 'q=from(bucket:"sensors") |> range(start: -1h)'

  
### 10. `tests/test_payload_schema.md`
```markdown
# Teste de Schema do Payload MQTT

## Schema Esperado
```json
{
  "device": "string",
  "temp": "float",
  "umid": "float"
}
{"device":"esp32-node-1","temp":24.3,"umid":60.1}
{"device":"esp32-node-2","temp":-5.2,"umid":85.7}
{"device":"sensor-001","temp":30.0,"umid":45.5}

Testes Automatizados (Futuro)
python
def validate_payload(payload):
    required = ['device', 'temp', 'umid']
    return all(field in payload for field in required)

    
### 11. `src/frontend/README.md`
```markdown
# Frontend - Smart Farm Dashboard

## Status: Planejado para Fase 2

## Funcionalidades Previstas
- Dashboard web responsivo
- Controle de dispositivos IoT
- Alertas e notificações
- Relatórios personalizados

## Stack Tecnológica
- React.js ou Vue.js
- Chart.js para gráficos
- WebSocket para atualizações em tempo real
- API REST para histórico

## No momento:
Use o Grafana em http://localhost:3000 para visualização dos dados.
