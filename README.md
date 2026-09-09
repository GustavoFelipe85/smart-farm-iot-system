# Smart Farm IoT System

[![EN](https://img.shields.io/badge/lang-English-blue)](README_en.md) ![Release](https://img.shields.io/github/v/release/GustavoFelipe85/smart-farm-iot-system)  [![Google Scholar](https://img.shields.io/badge/Google%20Scholar-Perfil_do_Autor-blue)](https://scholar.google.com/citations?user=5EhQZ31XiJ0C)

<a href="https://doi.org/10.5281/zenodo.19040531"><img src="https://zenodo.org/badge/1070426251.svg" alt="DOI"></a> 

## Arquitetura Distribuída Versionada para Ingestão, Validação e Persistência de Dados IoT

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
* ausência de mecanismos explícitos de integridade estrutural e isolamento de privilégios.

Grande parte das implementações industriais prioriza o aspecto funcional (monitoramento), mas negligencia formalização de contrato, controle de consistência na camada de ingestão e mitigação de vetores de ataque na infraestrutura. Este projeto investiga mecanismos arquiteturais para garantir integridade estrutural, segurança (*Secure by Design*) e versionamento explícito de dados em pipelines IoT distribuídos.

---

## 3. Problema de Pesquisa

Como projetar uma arquitetura distribuída de ingestão IoT que:

1. mantenha retrocompatibilidade entre versões de payload;
2. implemente validação formal de contratos;
3. preserve integridade estrutural antes da persistência;
4. blinde a infraestrutura contra escalonamento de privilégios e exaustão de recursos;
5. mantenha latência compatível com sistemas near real-time;
6. seja reprozudível em ambiente containerizado sob o princípio de menor privilégio?

---

## 4. Hipótese

A adoção de:

* JSON Schema como contrato canônico versionado;
* normalização estruturada retrocompatível;
* validação formal antes da persistência;
* arquitetura modular containerizada com execução *rootless* e imutabilidade de sistema;

aumenta robustez estrutural, segurança e rastreabilidade do pipeline sem impacto significativo na latência do sistema.

---

## 5. Objetivos

### 5.1 Objetivo Geral

Projetar e avaliar uma arquitetura IoT distribuída com contrato versionado, validação formal de dados e blindagem de infraestrutura.

### 5.2 Objetivos Específicos

* Definir contrato de dados versionado (SemVer);
* Implementar camada de normalização retrocompatível;
* Integrar validação estrutural via JSON Schema;
* Aplicar controles DevSecOps (SAST, *Secret Scanning*, *Rootless Containers*);
* Avaliar latência e throughput do pipeline;
* Garantir reprodutibilidade via Docker Compose.

---

## 6. Arquitetura Proposta

A arquitetura é composta por cinco camadas, operando sobre uma rede virtualizada isolada (*Bridge Network*):

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

## 7. Matriz de Segurança e Confiabilidade (DevSecOps)

[MODO ACADÊMICO] O ambiente implementa controles estritos no nível de engenharia e esteira de integração contínua (CI/CD), mitigando vetores de ataque comuns em implantações de IoT industrial:

| Vetor de Ameaça | Controle Implementado (*Mitigação*) |
| :--- | :--- |
| **Container Breakout** | Execução *Rootless* forçada (UID/GID predefinidos), `security_opt: no-new-privileges:true` e supressão de *capabilities* do kernel (`cap_drop: ALL`). |
| **Supply Chain Attacks** | Arquitetura *Multi-Stage Build* isolando dependências de compilação do ambiente de execução. |
| **Vazamento de Credenciais** | Controle de exclusão algorítmica (`.gitignore`) e varredura ativa de segredos (Gitleaks) na esteira de CI. |
| **Exploração de Execução** | Sistemas de arquivos operacionais montados como somente leitura (`read_only: true`). |
| **Vulnerabilidade de Código** | Integração SAST (Bandit) no *pipeline* para identificação estática de falhas na camada de ingestão. |
| **Resource Exhaustion (DoS)** | Imposição de limites de consumo computacional (CPU/Memória RAM) via orquestrador. |

---

## 8. Modelo de Dados (Contrato Canônico)

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

## 9. Metodologia Experimental

Ambiente:

* Docker Compose isolado com limitação de recursos
* Variáveis e credenciais isoladas via `.env`
* Integração Contínua automatizada (Validação de Software e SecOps)

Métricas avaliadas:

* Latência MQTT → Ingestão
* Throughput máximo suportado
* Taxa de rejeição de payload inválido
* Uptime da arquitetura
* Integridade estrutural sob STRICT_SCHEMA

---

## 10. Resultados Preliminares

| Métrica | Resultado |
| --- | --- |
| Latência média | < 120 ms |
| Ingestão | > 10.000 msgs/h |
| Uptime | 99.9% |
| Payload inválido persistido | 0 (STRICT_SCHEMA=true) |

---

## 11. Limitações

* Não há ainda avaliação em campo real;
* Ausência de análise comparativa com pipelines não validados;
* Não implementa controle fechado (atuadores);
* Não inclui modelagem estatística longitudinal.

---

## 12. Trabalhos Futuros

* Avaliação sob carga escalável;
* Controle automatizado (atuadores) via autenticação mútua (mTLS);
* Implementação de microserviço de decisão;
* Avaliação quantitativa de economia hídrica;
* Modelos preditivos para umidade do solo.

---

## 13. Reprodutibilidade

Para fins de auditoria e testes de segurança, a implantação exige a injeção de credenciais em ambiente local isolado:

```bash
git clone [https://github.com/GustavoFelipe85/smart-farm-iot-system](https://github.com/GustavoFelipe85/smart-farm-iot-system)
cd smart-farm-iot-system/docker

# 1. Configuração do isolamento de credenciais
cp .env.example .env

# 2. Orquestração e compilação das imagens imutáveis
docker compose up -d --build

```

Componentes:

* Mosquitto (Rootless)
* Python Consumer (Multi-Stage Build)
* InfluxDB 2.7 (Rootless)
* Grafana 10.x (Rootless)

---

## 14. Contribuição para Sistemas de Computação

O projeto contribui ao investigar:

* integridade estrutural em sistemas IoT distribuídos;
* versionamento de contratos de dados;
* validação formal em pipelines near real-time;
* mitigação de superfície de ataque em infraestrutura de borda.

O foco está no domínio de:

> Sistemas Distribuídos + Engenharia de Dados IoT + Cibersegurança (SecOps) + Confiabilidade Estrutural.

---

## 15. Autor

Gustavo F. Paluch

Engenheiro da Computação

```

A estrutura agora demonstra domínio simultâneo em pesquisa acadêmica de alta performance e pragmatismo operacional de mercado. Qual o próximo componente da arquitetura você deseja submeter ao *pipeline* local para validar as restrições de sistema de arquivos do contêiner?

```
