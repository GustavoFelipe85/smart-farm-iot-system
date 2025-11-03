#ifndef CONFIG_H
#define CONFIG_H

// Configurações WiFi - EDITAR COM SUAS CREDENCIAIS
const char* WIFI_SSID = "SEU_WIFI_SSID";
const char* WIFI_PASSWORD = "SUA_WIFI_SENHA";

// Configurações MQTT
const char* MQTT_SERVER = "192.168.1.100";  // IP do seu broker MQTT
const int MQTT_PORT = 1883;
const char* MQTT_TOPIC = "smartfarm/sensors";

// Configurações Hardware
const int DHT_PIN = 4;
const int DHT_TYPE = DHT22;

#endif
