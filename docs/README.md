# Smart Farm IoT System

## Arquitetura Distribuída Versionada para Ingestão, Validação e Persistência de Dados IoT

---

## 1. Identificação do Projeto

**Área:** Ciência da Computação
**Linha de Pesquisa:** Sistemas de Computação
**Domínio Aplicado:** IoT em Agricultura de Precisão
**Natureza:** Projeto de Pesquisa Aplicada

---

## 2. Contextualização

Sistemas IoT distribuídos aplicados à agricultura de precisão apresentam desafios estruturais relacionados a:

* heterogeneidade de dispositivos embarcados;
* inconsistência de contratos de dados;
* ausência de versionamento formal de payload;
* ingestão não validada;
* baixa reprodutibilidade experimental;
* ausência de mecanismos explícitos de integridade estrutural.

Grande parte das implementações industriais prioriza o aspecto funcional (monitoramento), mas negligencia formalização de contrato e controle de consistência na camada de ingestão.

Este projeto investiga mecanismos arquiteturais para garantir integridade estrutural e versionamento explícito de dados em pipelines IoT distribuídos.

---

## 3. Problema de Pesquisa

Como projetar uma arquitetura distribuída de ingestão IoT que:

1. mantenha retrocompatibilidade entre versões de payload;
2. implemente validação formal de contratos;
3. preserve integridade estrutural antes da persistência;
4. mantenha latência compatível com sistemas near real-time;
5. seja reproduzível em ambiente containerizado?

---

## 4. Hipótese

A adoção de:

* JSON Schema como contrato canônico versionado;
* normalização estruturada retrocompatível;
* validação formal antes da persistência;
* arquitetura modular containerizada;

aumenta robustez estrutural e rastreabilidade do pipeline sem impacto significativo na latência do sistema.

---

## 5. Objetivos

### 5.1 Objetivo Geral

Projetar e avaliar uma arquitetura IoT distribuída com contrato versionado e validação formal de dados.

### 5.2 Objetivos Específicos

* Definir contrato de dados versionado (SemVer);
* Implementar camada de normalização retrocompatível;
* Integrar validação estrutural via JSON Schema;
* Avaliar latência e throughput do pipeline;
* Garantir reprodutibilidade via Docker Compose.

---

## 6. Arquitetura Proposta

A arquitetura é composta por cinco camadas:

1. **Edge Layer:** ESP32 + sensores ambientais
2. **Communication Layer:** MQTT autenticado (QoS 1)
3. **Ingestion Layer:** Python Consumer com normalização
4. **Persistence Layer:** InfluxDB (time-series)
5. **Visualization Layer:** Grafana

Contrato formal definido em:

```
src/backend/schemas/sensor_payload.json
```

O arquivo acima constitui o *Single Source of Truth* do sistema.

---

## 7. Modelo de Dados (Contrato Canônico)

Exemplo de payload versionado:

```json
{
  "schema_version": "1.0.0",
  "device": "esp32-node-01",
  "timestamp": "2025-11-11T14:57:00Z",
  "metrics": {
    "temperature": 25.7,
    "humidity": 63.1,
    "soil_moisture": 41.2,
    "soil_raw": 1820
  }
}
```

Características:

* Versionamento explícito
* Campos obrigatórios definidos formalmente
* Controle de propriedades adicionais
* Normalização de formatos legados

---

## 8. Metodologia Experimental

Ambiente:

* Docker Compose isolado
* Variáveis parametrizadas via `.env`
* Integração Contínua automatizada

Métricas avaliadas:

* Latência MQTT → Ingestão
* Throughput máximo suportado
* Taxa de rejeição de payload inválido
* Uptime da arquitetura
* Integridade estrutural sob STRICT_SCHEMA

---

## 9. Resultados Preliminares

| Métrica                     | Resultado              |
| --------------------------- | ---------------------- |
| Latência média              | < 120 ms               |
| Ingestão                    | > 10.000 msgs/h        |
| Uptime                      | 99.9%                  |
| Payload inválido persistido | 0 (STRICT_SCHEMA=true) |

---

## 10. Limitações

* Não há ainda avaliação em campo real;
* Ausência de análise comparativa com pipelines não validados;
* Não implementa controle fechado (atuadores);
* Não inclui modelagem estatística longitudinal.

---

## 11. Trabalhos Futuros

* Avaliação sob carga escalável;
* Controle automatizado (atuadores);
* Implementação de microserviço de decisão;
* Avaliação quantitativa de economia hídrica;
* Modelos preditivos para umidade do solo.

---

## 12. Reprodutibilidade

Execução local:

```bash
git clone https://github.com/GustavoFelipe85/smart-farm-iot-system
cd smart-farm-iot-system/docker
docker-compose up -d
```

Componentes:

* Mosquitto
* Python Consumer
* InfluxDB 2.7
* Grafana 10.x

---

## 13. Contribuição para Sistemas de Computação

O projeto contribui ao investigar:

* integridade estrutural em sistemas IoT distribuídos;
* versionamento de contratos de dados;
* normalização retrocompatível;
* validação formal em pipelines near real-time;
* arquitetura containerizada reprodutível.

O foco está no domínio de:

> Sistemas Distribuídos + Engenharia de Dados IoT + Confiabilidade Estrutural.

---

## 14. Autor

Gustavo Felipe Paluch Figueiredo
Engenharia da Computação

---

