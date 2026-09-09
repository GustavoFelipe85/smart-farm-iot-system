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
