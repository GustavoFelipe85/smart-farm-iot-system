// 🚿 src/esp32/actuators/irrigation_control.h
class IrrigationSystem {
private:
    int relayPin;
    bool autoMode;
    
public:
    void startWatering(int duration);
    void stopWatering();
    bool shouldWater(float soilMoisture, float temperature);
    
    // Lógica inteligente baseada em:
    // - Umidade do solo < 30%
    // - Temperatura < 35°C (evitar evaporação)
    // - Horário do dia (manhã/tarde)
};
