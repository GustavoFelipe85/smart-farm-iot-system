#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"
#include "config.h"  // Inclui as configurações

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHT_PIN, DHT_TYPE);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando em ");
  Serial.println(WIFI_SSID);
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println("IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Tentando conexão MQTT...");
    
    // Nome único para o cliente MQTT
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("conectado");
    } else {
      Serial.print("falha, rc=");
      Serial.print(client.state());
      Serial.println(" tentando novamente em 5s");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(MQTT_SERVER, MQTT_PORT);
  dht.begin();
  
  // Configurar timeout do MQTT
  client.setSocketTimeout(5);
  client.setKeepAlive(60);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Leitura do sensor com verificação de erro
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Verificar se a leitura é válida
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("❌ Falha na leitura do DHT22!");
    
    // Tentar reiniciar o sensor em caso de falha persistente
    static int readErrors = 0;
    readErrors++;
    if (readErrors > 10) {
      Serial.println("🔄 Reiniciando sensor DHT22...");
      dht.begin();
      readErrors = 0;
    }
    
    delay(2000);
    return;
  }

  // Resetar contador de erros se leitura for bem-sucedida
  static int readErrors = 0;
  readErrors = 0;

  // Criar payload JSON
  String payload = "{";
  payload += "\"device\":\"esp32-node-1\",";
  payload += "\"temp\":" + String(temperature, 1) + ",";
  payload += "\"umid\":" + String(humidity, 1);
  payload += "}";

  // Publicar no MQTT
  boolean published = client.publish(MQTT_TOPIC, payload.c_str(), true);
  
  if (published) {
    Serial.println("✅ Mensagem publicada: " + payload);
    Serial.println("📡 Temp: " + String(temperature, 1) + "°C | Umidade: " + String(humidity, 1) + "%");
  } else {
    Serial.println("❌ Falha ao publicar mensagem MQTT");
    Serial.println("📡 Estado do cliente: " + String(client.state()));
  }

  delay(5000); // Aguarda 5 segundos entre leituras
}
