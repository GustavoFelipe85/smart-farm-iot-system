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
