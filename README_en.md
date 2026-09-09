```markdown
# Smart Farm IoT System

[![PT-BR](https://img.shields.io/badge/lang-PT--BR-green)](README.md) ![Release](https://img.shields.io/github/v/release/GustavoFelipe85/smart-farm-iot-system)  [![Google Scholar](https://img.shields.io/badge/Google%20Scholar-Author_Profile-blue)](https://scholar.google.com/citations?user=5EhQZ31XiJ0C)

<a href="https://doi.org/10.5281/zenodo.19040531"><img src="https://zenodo.org/badge/1070426251.svg" alt="DOI"></a> 

## Versioned Distributed Architecture for IoT Data Ingestion, Validation, and Persistence

## 1. Project Identification

**Area:** Computer Science
**Research Line:** Computing Systems
**Applied Domain:** Precision Agriculture IoT
**Nature:** Applied Research Project

---

## 2. Contextualization

Distributed IoT systems applied to precision agriculture present structural challenges related to:

* heterogeneity of embedded devices;
* inconsistency of data contracts;
* absence of formal payload versioning;
* unvalidated data ingestion;
* low experimental reproducibility;
* lack of explicit mechanisms for structural integrity and privilege isolation.

Most industrial implementations prioritize the functional aspect (monitoring) but neglect contract formalization, consistency control at the ingestion layer, and attack surface mitigation in the infrastructure. This project investigates architectural mechanisms to ensure structural integrity, security (*Secure by Design*), and explicit data versioning in distributed IoT pipelines.

---

## 3. Research Problem

How to design a distributed IoT ingestion architecture that:

1. maintains backward compatibility between payload versions;
2. implements formal contract validation;
3. preserves structural integrity prior to persistence;
4. shields the infrastructure against privilege escalation and resource exhaustion;
5. maintains latency compatible with near real-time systems;
6. is reproducible in a containerized environment under the principle of least privilege?

---

## 4. Hypothesis

The adoption of:

* JSON Schema as a versioned canonical contract;
* backward-compatible structured normalization;
* formal validation prior to persistence;
* containerized modular architecture with *rootless* execution and system immutability;

increases the structural robustness, security, and traceability of the pipeline without significant impact on system latency.

---

## 5. Objectives

### 5.1 General Objective

To design and evaluate a distributed IoT architecture with versioned contracts, formal data validation, and infrastructure hardening.

### 5.2 Specific Objectives

* Define a versioned data contract (SemVer);
* Implement a backward-compatible normalization layer;
* Integrate structural validation via JSON Schema;
* Apply DevSecOps controls (SAST, Secret Scanning, Rootless Containers);
* Evaluate pipeline latency and throughput;
* Ensure reproducibility via Docker Compose.

---

## 6. Proposed Architecture

The architecture consists of five layers operating over an isolated virtualized network (*Bridge Network*):

1. **Edge Layer:** ESP32 + environmental sensors
2. **Communication Layer:** Authenticated MQTT (QoS 1)
3. **Ingestion Layer:** Python Consumer with data normalization
4. **Persistence Layer:** InfluxDB (time-series)
5. **Visualization Layer:** Grafana

Formal contract defined in:


```

src/backend/schemas/sensor_payload.json

```

The file above constitutes the system's *Single Source of Truth* (SSOT).

---

## 7. Security and Reliability Matrix (DevSecOps)

[MODO ACADÊMICO] The environment implements strict controls at the engineering and Continuous Integration (CI/CD) pipeline levels, mitigating common attack vectors in industrial IoT deployments:

| Threat Vector | Implemented Control (*Mitigation*) |
| :--- | :--- |
| **Container Breakout** | Forced *Rootless* execution (predefined UID/GID), `security_opt: no-new-privileges:true` and host kernel capability suppression (`cap_drop: ALL`). |
| **Supply Chain Attacks** | *Multi-Stage Build* architecture isolating compilation dependencies from the runtime environment. |
| **Credential Leaks** | Algorithmic exclusion control (`.gitignore`) and active secret scanning (Gitleaks) within the CI pipeline. |
| **Execution Exploitation** | Operational container file systems mounted as read-only (`read_only: true`). |
| **Code Vulnerability** | SAST integration (Bandit) in the pipeline for static identification of flaws in the ingestion layer. |
| **Resource Exhaustion (DoS)** | Imposition of computational consumption limits (CPU/RAM) via the orchestrator. |

---

## 8. Data Model (Canonical Contract)

Versioned payload example:

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

Characteristics:

* Explicit versioning
* Formally defined mandatory fields
* Additional properties control
* Normalization of legacy formats

---

## 9. Experimental Methodology

Environment:

* Isolated Docker Compose with resource limitation
* Variables and credentials isolated via `.env`
* Automated Continuous Integration (Software Validation and SecOps)

Evaluated Metrics:

* MQTT → Ingestion Latency
* Maximum supported throughput
* Invalid payload rejection rate
* Architecture uptime
* Structural integrity under STRICT_SCHEMA

---

## 10. Preliminary Results

| Metric | Result |
| --- | --- |
| Average Latency | < 120 ms |
| Ingestion Throughput | > 10,000 msgs/h |
| Uptime | 99.9% |
| Invalid Payload Persisted | 0 (STRICT_SCHEMA=true) |

---

## 11. Limitations

* No real-world field evaluation yet;
* Absence of comparative analysis with unvalidated pipelines;
* Does not implement closed-loop control (actuators);
* Does not include longitudinal statistical modeling.

---

## 12. Future Work

* Evaluation under scalable load;
* Automated control (actuators) via mutual authentication (mTLS);
* Implementation of a decision microservice;
* Quantitative evaluation of water savings;
* Predictive models for soil moisture.

---

## 13. Reproducibility

For auditing and security testing purposes, deployment requires credential injection in an isolated local environment:

```bash
git clone [https://github.com/GustavoFelipe85/smart-farm-iot-system](https://github.com/GustavoFelipe85/smart-farm-iot-system)
cd smart-farm-iot-system/docker

# 1. Credential isolation setup
cp .env.example .env

# 2. Orchestration and compilation of immutable images
docker compose up -d --build

```

Components:

* Mosquitto (Rootless)
* Python Consumer (Multi-Stage Build)
* InfluxDB 2.7 (Rootless)
* Grafana 10.x (Rootless)

---

## 14. Contribution to Computing Systems

The project contributes by investigating:

* structural integrity in distributed IoT systems;
* data contract versioning;
* formal validation in near real-time pipelines;
* attack surface mitigation in edge infrastructure.

The focus lies within the domain of:

> Distributed Systems + IoT Data Engineering + Cybersecurity (SecOps) + Structural Reliability.

---

## 15. Author

Gustavo F. Paluch

Computer Engineer

```

```
