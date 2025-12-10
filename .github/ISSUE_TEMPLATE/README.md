# 📂 **Issue Templates do Projeto Smart Farm IoT System**

Este diretório contém todos os **modelos oficiais de Issues** utilizados no projeto *Smart Farm IoT System*.
Eles padronizam o fluxo de trabalho, garantindo organização, rastreabilidade e coerência técnica — essenciais para um projeto acadêmico (PPGComp) e de engenharia IoT.

Cada template representa uma área específica do projeto:

---

## 🧩 **Visão Geral dos Templates**

### 🔧 **1. Hardware – Protótipo / CELUS / Eletrônica**

Arquivo: `hardware_issue.md`
Use para registrar atividades relacionadas a:

* ESP32, sensores ambientais e de solo
* Design eletrônico no CELUS
* Pinout, esquemáticos e revisões
* Testes de bancada, fonte AC/DC, atuadores
* Preparação para PCB v2

> Associado à **Fase 3** (hardware real) e **Fase 4** (irrigação automatizada).

---

### 💻 **2. Software – Python / API / ML**

Arquivo: `software_issue.md`
Use para:

* Python Consumer (ingestão de dados)
* API FastAPI (Fase 3 e Fase 4)
* Algoritmos de decisão
* Modelos de ML (previsão de umidade)
* Testes automatizados

> Ligado à **Fase 2** (backend), **Fase 3** e **Fase 4**.

---

### 🌱 **3. Experimentos – Irrigação / Solo / Bancada**

Arquivo: `experimento_issue.md`
Use quando for registrar experimentos como:

* Testes de sensores em diferentes tipos de solo
* Curvas de umidade vs. tempo
* Ensaios de irrigação controlada
* Monitoramento via InfluxDB + Grafana

> Parte central da **Fase 4** (automação).

---

### 📚 **4. Documentação Acadêmica – PPGComp**

Arquivo: `documentacao_issue.md`
Use para:

* Revisão bibliográfica
* Requisitos
* Arquitetura
* Evolução da pesquisa
* Materiais para a dissertação

> Mantém o componente acadêmico correto e organizado.

---

### 🛠 **5. Manutenção / Infraestrutura / Docker**

Arquivo: `infra_issue.md`
Use quando houver:

* Atualização nos containers
* Ajustes no `.env` / segurança
* Reorganização de pastas do repo
* Scripts de automação

> Associado às fases 1–4, pois a infraestrutura é contínua.

---

## 📝 **Como Usar os Templates**

Ao abrir uma Issue no GitHub:

1. Clique em **Issues → New Issue**
2. Selecione o template mais adequado
3. Preencha todos os campos obrigatórios
4. Adicione labels (ex.: `hardware`, `fase-3`, `documentacao`)
5. (Opcional) Associe a Milestones ou ao Kanban de Fase 3/4

Os templates foram criados para:

✔ padronizar a comunicação
✔ facilitar auditoria
✔ documentar histórico acadêmico
✔ garantir qualidade na engenharia do projeto

---

## 🏗 **Filosofia de Organização**

* **Cada Issue = 1 tarefa clara, objetiva e verificável**
* **Todos os resultados devem ser anexados no corpo da issue**
* **Nada deve ser deixado fora do rastreamento** — importante em ambientes científicos

Exemplo:

> Uma alteração no hardware deve ter Issue própria, com prints do CELUS, pinout, validações e critérios de aceite.

---

## 🎯 **Contribuição**

Para contribuir:

1. Abra uma Issue usando o template adequado
2. Aguarde triagem e atribuição
3. Submeta PRs sempre vinculando a Issue (`Closes #ID`)

---

## 📌 **Status**

Os templates estão alinhados às fases atuais:

* ✔ Fase 1 – Concluída
* ✔ Fase 2 – Concluída
* 🟨 Fase 3 – Em andamento (Hardware + API)
* 🔮 Fase 4 – Planejada (Automação da Irrigação)

---


