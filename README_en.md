# Smart Farm IoT System

[![PT-BR](https://img.shields.io/badge/lang-Português-green)](README.md) ![Release](https://img.shields.io/github/v/release/GustavoFelipe85/smart-farm-iot-system)

<a href="https://doi.org/10.5281/zenodo.19040531"><img src="https://zenodo.org/badge/1070426251.svg" alt="DOI"></a> [![Google Scholar](https://img.shields.io/badge/Google%20Scholar-Perfil_do_Autor-blue)](https://scholar.google.com/citations?user=5EhQZ31XiJ0C)

## Versioned Distributed Architecture for IoT Data Ingestion, Validation, and Persistence

## 1. Project Identification

**Research Area:** Computer Science

**Research Line:** Computer Systems

**Application Domain:** Precision Agriculture IoT

**Project Type:** Applied Research Project

---

## 2. Background

Distributed IoT systems applied to precision agriculture present several structural challenges, including:

* heterogeneous embedded devices;
* inconsistent data contracts;
* lack of formal payload versioning;
* unvalidated data ingestion;
* limited experimental reproducibility;
* absence of explicit structural integrity mechanisms.

Most industrial implementations prioritize functional aspects (monitoring) while neglecting formal contract specification and consistency control during the ingestion stage.

This project investigates architectural mechanisms capable of ensuring structural integrity and explicit data versioning in distributed IoT pipelines.

---

## 3. Research Problem

How can a distributed IoT ingestion architecture be designed to:

1. maintain backward compatibility between payload versions;
2. implement formal contract validation;
3. preserve structural integrity before data persistence;
4. maintain latency compatible with near real-time systems;
5. remain fully reproducible in a containerized environment?

---

## 4. Hypothesis

The adoption of:

* JSON Schema as a versioned canonical contract;
* backward-compatible structured normalization;
* formal validation before persistence;
* modular containerized architecture;

increases structural robustness and pipeline traceability without significantly affecting system latency.

---

## 5. Objectives

### 5.1 General Objective

Design and evaluate a distributed IoT architecture based on versioned data contracts and formal validation.

### 5.2 Specific Objectives

* Define a versioned data contract (Semantic Versioning);
* Implement a backward-compatible normalization layer;
* Integrate structural validation through JSON Schema;
* Evaluate pipeline latency and throughput;
* Ensure experimental reproducibility using Docker Compose.

---

## 6. Proposed Architecture

The architecture consists of five layers:

1. **Edge Layer:** ESP32 + environmental sensors
2. **Communication Layer:** Authenticated MQTT (QoS 1)
3. **Ingestion Layer:** Python Consumer with normalization
4. **Persistence Layer:** InfluxDB (time-series database)
5. **Visualization Layer:** Grafana

The formal data contract is defined in:

```text
src/backend/schemas/sensor_payload.json
```

This file represents the system's **Single Source of Truth**.

---

## 7. Data Model (Canonical Contract)

Example of a versioned payload:

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
* Additional property control
* Legacy payload normalization

---

## 8. Experimental Methodology

Environment:

* Isolated Docker Compose infrastructure
* Environment variables managed through `.env`
* Automated Continuous Integration

Evaluated metrics:

* MQTT → Ingestion latency
* Maximum supported throughput
* Invalid payload rejection rate
* System uptime
* Structural integrity under STRICT_SCHEMA

---

## 9. Preliminary Results

| Metric | Result |
|----------|---------|
| Average latency | < 120 ms |
| Throughput | > 10,000 messages/hour |
| System uptime | 99.9% |
| Invalid persisted payloads | 0 (STRICT_SCHEMA=true) |

---

## 10. Limitations

* No real-field evaluation has been conducted yet;
* No comparative analysis with non-validated pipelines;
* Closed-loop control (actuators) has not yet been implemented;
* Longitudinal statistical modeling is not included.

---

## 11. Future Work

* Large-scale load evaluation;
* Automated irrigation control (actuators);
* Decision microservice implementation;
* Quantitative water-saving assessment;
* Predictive soil moisture models.

---

## 12. Reproducibility

Local execution:

```bash
git clone https://github.com/GustavoFelipe85/smart-farm-iot-system
cd smart-farm-iot-system/docker
docker compose up -d
```

Components:

* Mosquitto
* Python Consumer
* InfluxDB 2.7
* Grafana 10.x

---

## 13. Contribution to Computer Systems Research

This project contributes by investigating:

* structural integrity in distributed IoT systems;
* versioned data contracts;
* backward-compatible normalization;
* formal validation in near real-time pipelines;
* reproducible containerized architectures.

Research focus:

> Distributed Systems + IoT Data Engineering + Structural Reliability.

---

## 14. Author

**Gustavo F. Paluch**

Computer Engineering 

---
