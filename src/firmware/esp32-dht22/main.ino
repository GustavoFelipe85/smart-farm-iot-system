#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT22
const char* ssid = "SEU_WIFI_SSID";
const char* password = "SUA_WIFI_SENHA";
const char* mqtt_server = "192.168.1.100"; // IP do broker MQTT

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando em ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
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
    if (client.connect("ESP32Client")) {
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
  client.setServer(mqtt_server, 1883);
  dht.begin();
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Falha na leitura do DHT22!");
    delay(2000);
    return;
  }

  String payload = "{\"device\":\"esp32-node-1\",\"temp\":" + String(temperature) + ",\"umid\":" + String(humidity) + "}";
  
  boolean published = client.publish("smartfarm/sensors", payload.c_str(), true);
  if (published) {
    Serial.println("Mensagem publicada: " + payload);
  } else {
    Serial.println("Falha ao publicar mensagem");
  }

  delay(5000); // Aguarda 5 segundos entre leituras
}
