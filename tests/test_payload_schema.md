# Teste de Schema do Payload MQTT

## 🎯 Objetivo
Definir e validar o formato correto das mensagens trocadas entre ESP32 e o sistema.

---

## 📋 Especificação do Schema

### Schema JSON Esperado
```json
{
  "device": "string",
  "temp": "float",
  "umid": "float"
}
Exemplos Válidos
json
{"device":"esp32-node-1","temp":24.3,"umid":60.1}
{"device":"esp32-node-2","temp":-5.2,"umid":85.7}
{"device":"sensor-001","temp":30.0,"umid":45.5}
{"device":"estufa-01","temp":22.5,"umid":70.8}

Exemplos Inválidos
json
{"device":"","temp":24.3,"umid":60.1}                    // device vazio
{"temp":24.3,"umid":60.1}                               // device faltando
{"device":"sensor-1","umid":60.1}                       // temp faltando
{"device":"sensor-1","temp":"24.3","umid":60.1}         // temp como string
{"device":"sensor-1","temp":null,"umid":60.1}           // temp null
{"device":"sensor-1","temp":150.0,"umid":60.1}          // temp fora do range
{"device":"sensor-1","temp":24.3,"umid":-10.0}          // umid negativo

🔍 Regras de Validação
Campo device
Tipo: String

Obrigatório: Sim

Formato: Não vazio, identificador único

Exemplos válidos: "esp32-node-1", "sensor-001", "estufa-A"

Campo temp (Temperatura)
Tipo: Float

Obrigatório: Sim

Range: -20.0 à 80.0 (°C)

Precisão: 1 casa decimal

Unidade: Graus Celsius

Campo umid (Umidade)
Tipo: Float

Obrigatório: Sim

Range: 0.0 à 100.0 (%)

Precisão: 1 casa decimal

Unidade: Percentual

Regras Gerais
✅ Todos os campos são obrigatórios

✅ Formato JSON estrito (double quotes)

✅ Sem campos extras

✅ Encoding UTF-8

🧪 Testes Manuais
1. Teste via Mosquitto
bash
# Publicar mensagem válida
mosquitto_pub -h localhost -t "smartfarm/sensors" \
  -m '{"device":"test-01","temp":25.5,"umid":65.5}'

# Publicar mensagem inválida (deve ser rejeitada)
mosquitto_pub -h localhost -t "smartfarm/sensors" \
  -m '{"device":"test-01","temp":"25.5","umid":65.5}'
2. Verificar no Consumer
python
# O consumer deve logar:
# ✅ "Dados gravados - Temp: 25.5°C, Umidade: 65.5%"
# ❌ "Erro ao decodificar JSON" ou "Campo faltando"
3. Verificar no InfluxDB
bash
# Consultar dados gravados
curl -G http://localhost:8086/api/v2/query?org=smartfarm \
  -H "Authorization: Token smartfarm-token-12345" \
  --data-urlencode 'q=from(bucket:"sensors") |> range(start: -5m) |> filter(fn: (r) => r.device == "test-01")'
🔄 Validação Automatizada (Futuro)
Script Python de Validação
python
# tests/validate_payload.py
import json

def validate_payload(payload_str):
    """
    Valida se o payload MQTT está no formato correto
    Retorna (is_valid, errors)
    """
    errors = []
    
    try:
        data = json.loads(payload_str)
    except json.JSONDecodeError as e:
        return False, [f"JSON inválido: {e}"]
    
    # Campos obrigatórios
    required_fields = ['device', 'temp', 'umid']
    for field in required_fields:
        if field not in data:
            errors.append(f"Campo obrigatório faltando: {field}")
    
    # Validações específicas
    if 'device' in data:
        if not data['device'] or not isinstance(data['device'], str):
            errors.append("Device deve ser string não vazia")
    
    if 'temp' in data:
        if not isinstance(data['temp'], (int, float)):
            errors.append("Temp deve ser número")
        elif data['temp'] < -20 or data['temp'] > 80:
            errors.append("Temp fora do range (-20 a 80°C)")
    
    if 'umid' in data:
        if not isinstance(data['umid'], (int, float)):
            errors.append("Umid deve ser número")
        elif data['umid'] < 0 or data['umid'] > 100:
            errors.append("Umid fora do range (0 a 100%)")
    
    return len(errors) == 0, errors

# Exemplo de uso
if __name__ == "__main__":
    test_payloads = [
        '{"device":"sensor-1","temp":25.5,"umid":65.5}',
        '{"device":"","temp":25.5,"umid":65.5}',
        '{"temp":25.5,"umid":65.5}',
        '{"device":"sensor-1","temp":"25.5","umid":65.5}'
    ]
    
    for payload in test_payloads:
        is_valid, errors = validate_payload(payload)
        status = "✅ VÁLIDO" if is_valid else "❌ INVÁLIDO"
        print(f"{status}: {payload}")
        if errors:
            for error in errors:
                print(f"   → {error}")
Testes Unitários
python
# tests/test_payload_validation.py
import unittest
from validate_payload import validate_payload

class TestPayloadValidation(unittest.TestCase):
    
    def test_valid_payload(self):
        payload = '{"device":"esp32-node-1","temp":24.3,"umid":60.1}'
        is_valid, errors = validate_payload(payload)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_missing_device(self):
        payload = '{"temp":24.3,"umid":60.1}'
        is_valid, errors = validate_payload(payload)
        self.assertFalse(is_valid)
        self.assertIn("Campo obrigatório faltando: device", errors)
    
    def test_invalid_temperature(self):
        payload = '{"device":"sensor-1","temp":150.0,"umid":60.1}'
        is_valid, errors = validate_payload(payload)
        self.assertFalse(is_valid)
        self.assertIn("Temp fora do range (-20 a 80°C)", errors)

if __name__ == '__main__':
    unittest.main()
🐛 Troubleshooting de Payload
Problemas Comuns:
❌ "Erro ao decodificar JSON"

Verificar aspas duplas (não simples)

Verificar vírgulas e chaves

Usar jsonlint.com para validar

❌ "Campo faltando"

Verificar se todos os 3 campos estão presentes

Verificar spelling (device, temp, umid)

❌ Dados não aparecem no Grafana

Verificar se consumer está processando

Verificar se dados chegam no InfluxDB

Verificar tags/fields no InfluxDB

Ferramentas de Debug:
bash
# Monitorar tópico MQTT
mosquitto_sub -h localhost -t "smartfarm/sensors" -v

# Validar JSON online
echo '{"device":"test","temp":25.5,"umid":65.5}' | python -m json.tool

# Testar payload específico
python tests/validate_payload.py
📊 Estatísticas de Payload
Métricas Recomendadas:
Total de mensagens recebidas

Mensagens válidas vs inválidas

Taxa de erro por campo

Distribuição de valores (temp/umid)

Exemplo de Monitoring:
python
# No consumer, adicionar métricas
valid_messages = 0
invalid_messages = 0

def on_message(client, userdata, msg):
    global valid_messages, invalid_messages
    try:
        data = json.loads(msg.payload.decode())
        # ... processamento
        valid_messages += 1
    except Exception as e:
        invalid_messages += 1
        print(f"❌ Mensagem inválida: {e}")
    
    # Log estatísticas a cada 100 mensagens
    if (valid_messages + invalid_messages) % 100 == 0:
        total = valid_messages + invalid_messages
        valid_percent = (valid_messages / total) * 100
        print(f"📊 Estatísticas: {valid_messages}/{total} válidas ({valid_percent:.1f}%)")
🔄 Versionamento do Schema
Versão	Data	Mudanças
1.0	2024-01-15	Schema inicial: device, temp, umid
1.1	Futuro	Adicionar campo battery
1.2	Futuro	Adicionar campo rssi (sinal WiFi)
Última atualização: {{DATA_ATUAL}}
Próxima revisão: {{DATA_FUTURA}}
Responsável: GustavoFelipe85

text

## 🎯 **PARA IMPLEMENTAR AGORA:**

```bash
# Criar estrutura de testes
mkdir -p tests

# Salvar o arquivo acima como: tests/test_payload_schema.md

# (Opcional) Criar também o script de validação
touch tests/validate_payload.py
touch tests/test_payload_validation.py

git add tests/
git commit -m "tests: adiciona schema de validação de payload MQTT"
git push origin main
