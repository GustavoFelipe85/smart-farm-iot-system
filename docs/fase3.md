# 📡 Fase 3 — Sensores Reais, Laboratório e Hardware Assistido por IA

A Fase 3 marca o início da etapa **experimental** do projeto Smart Farm IoT System.  
Após a conclusão da Fase 2 (pipeline IoT completo em ambiente simulado), esta fase trata da **implementação física** do nó IoT utilizando sensores reais, testes em bancada, documentação eletrônica assistida por IA e validação do fluxo ponta a ponta com hardware.

---

# 🎯 1. Objetivos da Fase 3

- Integrar sensores ambientais reais ao ESP32  
- Realizar prototipagem e testes controlados em laboratório  
- Validar o fluxo de dados do hardware real até o backend (MQTT → Python → InfluxDB → Grafana)  
- Gerar documentação técnica e eletrônica via **CELUS Design Studio**  
- Preparar infraestrutura para testes de campo (Fase 4)  
- Avaliar ruído, estabilidade, confiabilidade e consistência das leituras  

---

# 🔧 2. Sensores Reais Utilizados

Os sensores planejados para esta etapa são:

| Sensor | Finalidade | Tipo |
|--------|------------|-------|
| **Sensor capacitivo de umidade do solo** | Medir teor de água no solo | analógico |
| **DHT22 / SHT31** | Temperatura e umidade do ar | digital |
| **BMP280** | Temperatura e pressão atmosférica | digital |
| **DS18B20** | Temperatura de precisão (opcional) | digital waterproof |

Todos os sensores serão conectados ao **ESP32 DevKit** com alimentação controlada.

---

# 🧪 3. Testes de Laboratório

Os testes serão realizados em bancada, incluindo:

- validação da leitura contínua dos sensores  
- análise de ruído elétrico  
- estabilidade térmica  
- interferências e oscilação das leituras  
- calibração inicial de sensores (solo + ar)  
- testes de ingestão MQTT em ambiente real  
- conexão com o pipeline existente  

**Objetivo:** garantir que tudo funcione com hardware real **antes** da fase de campo.

---

# 🤖 4. Prototipagem Assistida por CELUS

O **CELUS Design Studio** será usado nesta fase para automatizar parte da engenharia eletrônica:

### Artefatos gerados via CELUS:
- Esquemático eletrônico do nó IoT  
- Lista de materiais (BOM)  
- Regras de conexão e topologia  
- Pré-PCB para protótipo  
- Documentação eletrônica padronizada  

### Benefícios acadêmicos:
- Reprodutibilidade  
- Organização eletrônica  
- Padronização dos testes  
- Agilidade na prototipagem  
- Melhor preparação para experimentos científicos  

Os arquivos gerados deverão ser armazenados em:

```
/hardware/celus/
```

---

# 🔗 5. Pipeline com Hardware Real

O pipeline desta fase é:

```
ESP32 (sensores reais)
     ↓ MQTT Secure
Mosquitto Broker
     ↓ JSON validado
Python Consumer
     ↓ ingestão
InfluxDB 2.x
     ↓ visualização
Grafana 10.x
```

A meta é confirmar que o fluxo permanece estável em condições reais.

---

# 📄 6. Documentação Técnica da Fase 3

Será criado o documento:

```
/docs/hardware_fase3.md
```

Conteúdo esperado:

- lista de sensores  
- esquemático gerado no CELUS  
- instruções de montagem  
- pinagem do ESP32  
- firmware utilizado  
- fotos da bancada (opcional)  
- resultados preliminares dos testes  

---

# 📌 7. Critérios de Conclusão da Fase 3

A Fase 3 será considerada concluída quando:

- [ ] Sensores reais estiverem totalmente integrados  
- [ ] Pipeline com hardware real estiver funcional  
- [ ] Testes de bancada estiverem documentados  
- [ ] Esquemático e BOM forem gerados pelo CELUS  
- [ ] Documentação estiver completa em `/docs/hardware_fase3.md`  
- [ ] Preparação para testes de campo (Fase 4) estiver finalizada  

---

# 🚀 8. Transição para a Fase 4

Com a Fase 3 concluída, inicia-se a **Fase 4**, envolvendo:

- testes de campo  
- coleta de dados reais  
- análise de dados  
- automação  
- modelos de Machine Learning  
- experimentos científicos  

---

**Fase 3 = laboratório, hardware real, validação do nó IoT, documentação e preparação para campo.**  
É o coração da pesquisa experimental do mestrado.

---

🔙 Voltar ao README principal

---
