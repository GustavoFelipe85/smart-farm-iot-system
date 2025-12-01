# CELUS Project Information — Smart Farm IoT Hardware v1

**MCU:** ESP32-S3-WROOM  
**Sensores utilizados:**
- SHT31 (Sensirion)
- BME280 (Bosch)
- Sensor capacitivo de solo (DFRobot)

**Alimentação:**
- Entrada 5V USB
- Regulador RECOM R-78E3.3-1.0 (3.3V)

**Conectividade:**
- Wi-Fi (MQTT)
- GPIOs configurados para sensores analógicos e I2C

**Objetivo do protótipo:**
- Testes laboratoriais controlados
- Medição ambiental + solo
- Pipeline real: Sensor → ESP32-S3 → MQTT → InfluxDB/Grafana
