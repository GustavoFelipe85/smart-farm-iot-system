// 🌈 Novos sensores para implementar
class SensorSuite {
public:
    // Já implementado:
    float readDHT22();      // Temperatura & Umidade
    float readSoilMoisture(); // Umidade solo
    
    // Para implementar Fase 3:
    float readLuminosity();   // Sensor LDR
    float readPHLevel();      // pH do solo (simulado)
    float readWaterLevel();   // Nível reservatório
};
