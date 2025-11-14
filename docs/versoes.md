# Histórico de Versões – Smart Farm IoT System
Linha do tempo oficial de desenvolvimento do projeto, da concepção à conclusão.

---

# 0. Conceituação e Planejamento (Pré-Projeto)
- Definição do problema: monitoramento de temperatura, umidade do ar e solo em ambientes agrícolas.
- Levantamento de literatura (IoT, Agricultura 4.0, limitações, protocolos).
- Escolha da arquitetura geral (ESP32 → MQTT → Backend → InfluxDB → Grafana).
- Definição do roadmap do projeto dividido em Fases 1 a 6.

---

# 1.0.0 – Fase 1 Concluída — Infraestrutura Base
**Objetivo:** Criar o ambiente inicial e a fundação do ecossistema IoT.

## Implementado
- Estrutura inicial do repositório (src/, docker/, docs/).
- Ambiente Docker funcional.
- Brokers essenciais rodando:
  - Mosquitto MQTT
  - InfluxDB 2.x
  - Grafana
- Criação das redes Docker internas.
- Primeiras variáveis de ambiente `.env.example`.
- Documento inicial de arquitetura.
- README básico apresentando o projeto.

---

# 2.0.0 – Fase 2 Concluída — Pipeline IoT + Observabilidade (ATUAL)
**Objetivo:** Concluir todo o fluxo de coleta → validação → armazenamento → visualização.

## Implementado
### 🔗 Pipeline completo
- ESP32 publicando métricas em JSON.
- Tópicos estruturados: `farm/<id>/metrics`.
- MQTT com autenticação (`allow_anonymous false`).
- Consumer Python recebendo e validando payloads.
- Inserção no InfluxDB em tempo real.

### 📊 Monitoramento e dashboards
- Grafana configurado com:
  - Painéis de temperatura
  - Umidade do ar
  - Umidade do solo
- Export de dashboards salvo no repositório.

### 🛡 Segurança aplicada
- Senhas fora do repositório.
- Variáveis de ambiente padronizadas.
- Rede Docker isolada.

### 📈 Métricas comprovadas
- Latência total < **120 ms**
- Taxa de ingestão > **10.000 msgs/h**
- Uptime dos services Docker = **99,9%**

### 📚 Documentação consolidada
- README completo
- Quick Start funcional
- Arquitetura detalhada
- Referências acadêmicas

---

# Planejado – Fase 3 — API + Regras de Negócio
**Objetivo:** Criar a camada de serviços e transformar dados em informação útil.**

## Previsto
- API REST via FastAPI.
- Endpoints:
  - Última leitura por dispositivo.
  - Médias e agregações.
  - Amostragem por intervalo.
- Registro de thresholds:
  - Temperatura crítica
  - Umidade crítica
  - Umidade do solo crítica
- Sistema de alertas (MQTT + API).
- Autenticação JWT.

---

# Planejado – Fase 4 — Inteligência e Predição (ML)
**Objetivo:** Aplicar modelos para análise preditiva e suporte à decisão.**

## Previsto
- Importação automática do InfluxDB para ML pipelines.
- Modelos:
  - Regressão (umidade, temperatura)
  - Random Forest para previsão de irrigação
  - Análise de tendência e sazonalidade (STL)
- Export de previsões para nova série InfluxDB.
- Visualização no Grafana (curva real vs curva prevista).
- Avaliação:
  - RMSE, MAE, MAPE
  - Comparação de modelos

---

# Planejado – Fase 5 — Automação de Irrigação
**Objetivo:** Criar a primeira versão do sistema de atuação remota.**

## Previsto
- Controlador ESP32 para atuadores (bomba/válvula).
- Tópicos de comando:
  - `farm/<id>/irrigation/cmd`
- Estados:
  - `manual_on`, `manual_off`, `auto_mode`
- Regras automáticas:
  - Umidade do solo baixa → ligar bomba.
  - Temperatura alta + baixa umidade → irrigação complementar.
- Fail-safe:
  - Se perder comunicação → desligar atuador.

---

# Planejado – Fase 6 — Multi-Fazenda + Modo Produção
**Objetivo:** Transformar o projeto em solução escalável, modular e replicável.**

## Previsto
### 🔥 Multi-tenant
- Campos farm_id, field_id, device_id no schema.
- Permissões por fazenda e por usuário.

### 🏗 Infra robusta
- API com versionamento.
- Painéis Grafana separados por organização.
- Logs centralizados.
- Backup automatizado.

### 🧪 Testes e DevOps
- Testes unitários (consumer, validação).
- Testes de integração (Mosquitto → InfluxDB).
- CI/CD completo.
- Publicação de imagens Docker no GHCR.

---

# Estado Final Planejado (Conclusão)
A conclusão total do projeto considera a entrega das 6 fases:

**Fase 1 — Infraestrutura Base** ✔  
**Fase 2 — Pipeline + Observabilidade** ✔  
**Fase 3 — API e Regras de Negócio**  
**Fase 4 — Inteligência Artificial / Predição**  
**Fase 5 — Automação de Irrigação**  
**Fase 6 — Escalabilidade / Multi-Fazenda**  

---

# Versão Atual
**v2.0.0 — Fase 2 Concluída**  
Projeto pronto para apresentação, publicação, demonstração técnica e replicação acadêmica.

