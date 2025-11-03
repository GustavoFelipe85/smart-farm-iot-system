## 📁 **Arquivo: `docs/checklist_validacao.md`**

```markdown
# Checklist de Validação do Sistema Smart Farm IoT

## 🎯 Objetivo
Garantir que todos os componentes do sistema estão funcionando corretamente e integrados.

---

## 🔍 PRÉ-REQUISITOS

### ✅ Infraestrutura
- [ ] Docker e Docker Compose instalados
- [ ] Python 3.8+ instalado
- [ ] Git instalado e configurado
- [ ] 2GB+ de RAM disponível
- [ ] 5GB+ de espaço em disco

### ✅ Rede
- [ ] Portas 1883, 8086, 3000 livres
- [ ] Acesso à internet (para download de imagens Docker)
- [ ] WiFi disponível para ESP32

---

## 🐋 INFRAESTRUTURA DOCKER

### ✅ Serviços em Execução
```bash
# Executar e verificar
cd docker
docker-compose up -d
sleep 30
docker-compose ps
```
- [ ] Mosquitto: Status `Up`
- [ ] InfluxDB: Status `Up` 
- [ ] Grafana: Status `Up`

### ✅ Portas Acessíveis
```bash
# Testar conectividade
nc -z localhost 1883 && echo "✅ Mosquitto OK" || echo "❌ Mosquitto FALHOU"
nc -z localhost 8086 && echo "✅ InfluxDB OK" || echo "❌ InfluxDB FALHOU" 
nc -z localhost 3000 && echo "✅ Grafana OK" || echo "❌ Grafana FALHOU"
```
- [ ] Porta 1883 (Mosquitto) respondendo
- [ ] Porta 8086 (InfluxDB) respondendo
- [ ] Porta 3000 (Grafana) respondendo

### ✅ Logs sem Erros Críticos
```bash
docker-compose logs --tail=10 | grep -i error
```
- [ ] Nenhum erro crítico nos logs

---

## 🗄️ BANCO DE DADOS (INFLUXDB)

### ✅ Configuração Inicial
- [ ] Acessar http://localhost:8086
- [ ] Login: `admin` / `smartfarm123`
- [ ] Organization `smartfarm` criada
- [ ] Bucket `sensors` criado
- [ ] Token `smartfarm-token-12345` ativo

### ✅ Teste de Escrita
```bash
# Testar escrita via API
curl -X POST http://localhost:8086/api/v2/write?org=smartfarm&bucket=sensors \
  -H "Authorization: Token smartfarm-token-12345" \
  -H "Content-Type: text/plain" \
  -d 'environment,device=test temperature=25.0,humidity=60.1'
```
- [ ] Retorno HTTP 204 (sucesso)

### ✅ Teste de Leitura
```bash
# Testar leitura via API
curl -G http://localhost:8086/api/v2/query?org=smartfarm \
  -H "Authorization: Token smartfarm-token-12345" \
  --data-urlencode 'q=from(bucket:"sensors") |> range(start: -1h)'
```
- [ ] Retorno com dados no formato Flux

---

## 📡 BACKEND PYTHON

### ✅ Ambiente Python
```bash
cd src/backend/python-consumer
python --version  # Deve ser 3.8+
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
```
- [ ] Python 3.8+ disponível
- [ ] Ambiente virtual criado

### ✅ Dependências
```bash
pip install -r requirements.txt
pip list | grep -E "(paho-mqtt|influxdb-client|python-dotenv)"
```
- [ ] paho-mqtt==1.6.1 instalado
- [ ] influxdb-client==1.43.0 instalado
- [ ] python-dotenv==1.0.1 instalado

### ✅ Configuração
```bash
cp .env.example .env
# Verificar se .env existe e tem configurações
cat .env
```
- [ ] Arquivo .env criado
- [ ] MQTT_BROKER=localhost configurado
- [ ] INFLUX_TOKEN configurado

### ✅ Teste do Consumer
```bash
# Em um terminal: executar consumer
python mqtt_to_influx.py &
CONSUMER_PID=$!

# Em outro terminal: testar publicação
mosquitto_pub -h localhost -t "smartfarm/sensors" -m '{"device":"test","temp":25.5,"umid":65.5}'

sleep 5
kill $CONSUMER_PID
```
- [ ] Consumer inicia sem erro
- [ ] Mensagem MQTT processada
- [ ] Dados gravados no InfluxDB

---

## 🔌 FIRMWARE ESP32

### ✅ Compilação
- [ ] Arduino IDE ou PlatformIO instalado
- [ ] Bibliotecas: WiFi, PubSubClient, DHT sensor
- [ ] Código compila sem erros

### ✅ Configuração WiFi
```cpp
// Verificar no código
const char* ssid = "SEU_WIFI_SSID";        // ✅ Configurado
const char* password = "SUA_WIFI_SENHA";   // ✅ Configurado  
const char* mqtt_server = "IP_DO_BROKER";  // ✅ Configurado
```
- [ ] SSID WiFi configurado
- [ ] Senha WiFi configurada
- [ ] IP do broker MQTT configurado

### ✅ Hardware
- [ ] ESP32 conectado via USB
- [ ] Sensor DHT22 conectado no GPIO4
- [ ] Alimentação estável (3.3V)

### ✅ Teste de Publicação
```bash
# Monitorar serial do ESP32
# Deve mostrar:
# ✅ "WiFi conectado"
# ✅ "Mensagem publicada: {...}"
# ✅ Dados de temperatura/umidade válidos
```
- [ ] Conecta no WiFi
- [ ] Publica no tópico MQTT
- [ ] Payload JSON válido

---

## 📊 DASHBOARD GRAFANA

### ✅ Acesso
- [ ] http://localhost:3000 acessível
- [ ] Login: `admin` / `admin123` funciona

### ✅ Data Source
- [ ] InfluxDB data source configurado
- [ ] Conexão testada e funcionando
- [ ] Query básica retorna dados

### ✅ Dashboard
```bash
# Importar dashboard
# Via UI: + → Import → Upload JSON
```
- [ ] Dashboard `smart-farm-overview.json` importado
- [ ] Gráficos de temperatura visíveis
- [ ] Gráficos de umidade visíveis
- [ ] Dados atualizando em tempo real

---

## 🔄 FLUXO COMPLETO

### ✅ Integração End-to-End
```bash
# 1. ESP32 publica dados
# 2. Verificar se chega no MQTT
mosquitto_sub -h localhost -t "smartfarm/sensors" -v

# 3. Verificar se consumer processa
# 4. Verificar se dados estão no InfluxDB
curl -G http://localhost:8086/api/v2/query?org=smartfarm \
  -H "Authorization: Token smartfarm-token-12345" \
  --data-urlencode 'q=from(bucket:"sensors") |> range(start: -5m)'

# 5. Verificar se Grafana mostra dados
```
- [ ] ESP32 → MQTT: ✅ OK
- [ ] MQTT → Consumer: ✅ OK  
- [ ] Consumer → InfluxDB: ✅ OK
- [ ] InfluxDB → Grafana: ✅ OK

### ✅ Persistência
```bash
# Reiniciar serviços e verificar dados
docker-compose restart
sleep 30
# Dados históricos devem permanecer
```
- [ ] Dados persistem após restart
- [ ] Dashboard mantém histórico

---

## 🚨 VALIDAÇÃO DE SEGURANÇA

### ✅ Configurações Básicas
- [ ] Senhas diferentes das padrão em produção
- [ ] Token InfluxDB seguro em produção
- [ ] Rede isolada para IoT em produção

---

## 📝 REGISTRO DE VALIDAÇÃO

| Data | Versão | Responsável | Status |
|------|--------|-------------|---------|
| {{DATA}} | 1.0 | {{NOME}} | ✅ **APROVADO** |

### 🔍 Observações:
```
- Sistema integrado com sucesso
- Todos os componentes comunicando
- Dashboard funcionando em tempo real
- Pronto para uso em desenvolvimento
```

### ⚠️ Pendências (se houver):
```
- [ ] Item 1
- [ ] Item 2
```

---

## 🆘 TROUBLESHOOTING

### Problemas Comuns:

**❌ Mosquitto não sobe**
```bash
# Verificar se porta 1883 já está em uso
sudo lsof -i :1883
```

**❌ Consumer não conecta no InfluxDB**
```bash
# Verificar token e URL
echo $INFLUX_TOKEN
curl http://localhost:8086/health
```

**❌ ESP32 não publica**
```bash
# Verificar WiFi e IP do broker
# Testar broker com cliente desktop MQTT
```

**❌ Grafana sem dados**
```bash
# Verificar data source
# Testar query manual no InfluxDB
```

---

**Checklist versão**: 1.0  
**Última atualização**: {{DATA_ATUAL}}  
**Próxima revisão**: {{DATA_FUTURA}}
```

## 🎯 **PARA ADICIONAR AO SEU REPOSITÓRIO:**

```bash
# Salve o conteúdo acima no arquivo que você criou:
# docs/checklist_validacao.md

git add docs/checklist_validacao.md
git commit -m "docs: adiciona checklist completo de validação do sistema"
git push origin main
```

