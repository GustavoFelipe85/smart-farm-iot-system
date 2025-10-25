<p align="center">
  <img src="https://img.shields.io/badge/Projeto_Acadêmico-IoT%20%7C%20UNIOESTE-brightgreen?style=for-the-badge&logo=github" alt="Projeto Acadêmico IoT">
</p>

# 🌱 Smart Farm IoT System

## 🎓 Projeto para Seleção de Mestrado
**Universidade Pública - Universidade do Oeste do Paraná (Unioeste)** - Programa de Pós-Graduação Mestrado em Ciências da Computação/Sistemas

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![IoT](https://img.shields.io/badge/IoT-Agriculture-yellow.svg)](https://github.com/topics/iot-agriculture)
[![Docker](https://img.shields.io/badge/Docker-Container-blue)](https://docker.com)
[![ESP32](https://img.shields.io/badge/ESP32-IoT-green)](https://espressif.com)
[![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)](https://github.com/GustavoFelipe85/smart-farm-iot-system)
[![Fase](https://img.shields.io/badge/Fase-Proposta_de_Pesquisa-blue)](https://github.com/GustavoFelipe85/smart-farm-iot-system/projects)

## 🚀 Status do Projeto

**📅 Próximos Prazos:**
- [ ] Sistema de coleta de dados - 
- [ ] Integração MQTT - 
- [ ] API REST para telemetria - 
- [ ] Dashboard de monitoramento - 

**⚠️ Blocker Atual:** [Nenhum | Especificar se houver impedimentos]

**✅ Última Conquista:** Estrutura inicial do projeto e documentação finalizada

**📊 Progresso Geral:** 
- [x] Definição de arquitetura (90%)
- [x] Setup do repositório (100%)
- [x] Research de tecnologias (85%)
- [ ] Desenvolvimento do core (15%)
- [ ] Testes e validação (0%)
- [ ] Deploy (0%)

## 📋 Descrição do Projeto
Sistema IoT avançado para monitoramento e automação em agricultura de precisão, evoluindo do trabalho de TCC para aplicações em pesquisa acadêmica. O projeto integra sensores ambientais, análise de dados em tempo real e algoritmos de Machine Learning para otimização de recursos agrícolas.

## 🎯 Objetivos de Pesquisa
- [ ] **Machine Learning** para predição de safras e detecção de anomalias
- [ ] **Otimização inteligente** de recursos hídricos e energéticos
- [ ] **Integração avançada** com sensores multispectrais
- [ ] **Análise em tempo real** com dashboard interativo
- [ ] **Publicação científica** dos resultados obtidos

## 🛠 Tecnologias Utilizadas
| Área | Tecnologias |
|------|-------------|
| **Embedded** | Arduino, ESP32, Raspberry Pi |
| **Sensores** | DHT22, Soil Moisture, LDR, pH sensors |
| **Backend** | Python, Node.js, PostgreSQL |
| **ML/AI** | Scikit-learn, TensorFlow, Pandas |
| **Frontend** | React.js, Chart.js, WebSocket |
| **Cloud/Infra** | Docker, MQTT, InfluxDB, Grafana |

## 📁 Estrutura do Projeto
```
smart-farm-iot-system/
├── 📁 docker/              # Infraestrutura containerizada
├── 📁 documentacao/        # Documentação acadêmica
├── 📁 firmware/           # Código para microcontroladores
├── 📁 backend/           # API e processamento de dados
├── 📁 machine-learning/  # Modelos preditivos
├── 📁 dashboard/         # Interface web
└── 📁 hardware/         # Esquemas e PCB
```
## 🚀 Quick Start

### Pré-requisitos
- **Docker** e **Docker Compose** instalados
- **Git** para clonagem do repositório
- **4GB RAM** disponível (mínimo recomendado)

### Execução Rápida da Infraestrutura

```bash
# 1. Clone o repositório
git clone https://github.com/GustavoFelipe85/smart-farm-iot-system.git
cd smart-farm-iot-system

# 2. Execute a infraestrutura Docker
cd docker
docker-compose up -d

# 3. Aguarde os serviços inicializarem (≈ 1-2 minutos)

🎯 Serviços Disponíveis
Serviço	URL	Credenciais	Descrição
Grafana	http://localhost:3000	admin / admin	Dashboard de monitoramento
InfluxDB	http://localhost:8086	admin / SmartFarm2024!IoT@Unioeste	Banco de dados temporal
Mosquitto	mqtt://localhost:1883	-	Broker MQTT

📊 Verificação dos Serviços

# Verificar status dos containers
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f

# Parar a infraestrutura
docker-compose down

🤖 Testando o Machine Learning

# Execute o notebook de demonstração (requer Python/Jupyter)
cd src/ml
jupyter notebook demonstracao_ml.ipynb

🔧 Configuração de Desenvolvimento

# Instalar dependências Python (se desenvolvendo localmente)
pip install -r requirements.txt

# Ou usando ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install -r requirements.txt

⏱️ Tempo estimado para setup completo: 5-10 minutos


## 🔧 **VAMOS IMPLEMENTAR AGORA:**

### **PASSO A PASSO:**

1. **Edite o README.md**
2. **Adicione a seção acima** após "## 📁 Estrutura do Projeto"
3. **Commit:** `Add Quick Start section with Docker and ML instructions`

### **LOCALIZAÇÃO EXATA NO README:**
```markdown
## 📁 Estrutura do Projeto
[conteúdo atual...]

## 🚀 Quick Start  ← **ADICIONAR AQUI**
[novo conteúdo...]

## 🔬 Metodologia Científica
[conteúdo atual...]


## 🔬 Metodologia Científica
A metodologia está alinhada à linha de pesquisa **Sistemas de Computação**, integrando práticas de instrumentação IoT, análise de dados e automação inteligente:

1. **Revisão bibliográfica** do estado da arte em IoT agrícola
2. **Desenvolvimento iterativo** do sistema com testes de campo
3. **Coleta e análise** de dados em condições reais
4. **Validação estatística** dos resultados obtidos
5. **Comparação** com métodos tradicionais

## 📊 Resultados Esperados
- Redução de **≥20%** no consumo hídrico
- Aumento de **≥15%** na produtividade
- Sistema **autônomo** com mínima intervenção humana
- Publicação em **periódico científico**

## 🔗 Projeto Anterior
[TCC IoT Agribusiness](https://github.com/GustavoFelipe85/IoT-agribusiness-tcc) - Trabalho de graduação que originou esta pesquisa

## 📊 Gestão do Projeto & Roadmap

### 🎯 GitHub Projects
Acompanhe o progresso da pesquisa através do nosso quadro Kanban:

[**🔗 Acesse o Smart Farm IoT - Research Kanban**](https://github.com/GustavoFelipe85/smart-farm-iot-system/projects)

### 🗓️ Roadmap da Pesquisa

#### 🎓 Fase 1: Proposta de Pesquisa (Atual)
- [x] Definição do problema de pesquisa
- [x] Revisão bibliográfica sistemática
- [x] Metodologia científica
- [ ] Submissão para a universidade

#### 🔬 Fase 2: Desenvolvimento do Sistema
- [ ] Prototipagem hardware IoT
- [ ] Desenvolvimento do firmware
- [ ] API e backend
- [ ] Dashboard de monitoramento

#### 📊 Fase 3: Análise de Dados
- [ ] Coleta de dados em campo
- [ ] Análise estatística
- [ ] Modelos de machine learning
- [ ] Validação dos resultados

#### ✍️ Fase 4: Produção Científica
- [ ] Redação do artigo
- [ ] Submissão para periódico
- [ ] Preparação de apresentação

### 📋 Métricas de Progresso
| Fase | Progresso | Previsão |
|------|-----------|----------|
| Proposta | 🔵 90% | Out 2024 |
| Desenvolvimento | 🟡 15% | Dez 2024 |
| Análise | ⚪ 0% | Fev 2025 |
| Publicação | ⚪ 0% | Abr 2025 |

## 👨‍💻 Autor
**Gustavo Felipe Paluch Figueiredo**
- Graduado em Bacharelado em Engenharia da Computação pela Universidade de Santo Amaro (UNISA)
- Email: gustavo.f.p.f@outlook.com.br
- LinkedIn: [linkedin.com/in/gustavofpaluch](https://www.linkedin.com/in/gustavofpaluch)

## 🔗 Documentos Relacionados
- [📘 TCC - Fatores e Aplicações Limitantes da IoT na Agricultura (UNISA)](https://dspace.unisa.br/items/ab0577db-a4a9-4fc7-af72-d1b23e7345ed)
- [🌱 Repositório do Projeto - Smart Farm IoT System (GitHub)](https://github.com/GustavoFelipe85/smart-farm-iot-system)
- [📑 Projeto de Pesquisa - UNIOESTE](https://github.com/GustavoFelipe85/smart-farm-iot-system/tree/main/documentacao)

## 📚 Referências Complementares
> WOLFERT, S. et al. *Big Data in Smart Farming – A review.* Agricultural Systems, v.153, p.69–80, 2017.  
> ZHANG, Y. et al. *IoT Applications in Smart Agriculture: A Review.* Journal of Agricultural Informatics, v.13, n.1, p.45–60, 2022.  
> CONECTARAGRO. *Agricultura 4.0: Conectividade no campo.* Disponível em: <https://conectaragro.com.br>. Acesso em: 09 out. 2024.

## 📄 Licença
Este projeto está sob licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhos.

---

**📌 Documento técnico elaborado para fins acadêmicos no contexto do processo seletivo do Programa de Pós-Graduação em Ciência da Computação – UNIOESTE (2024).**

---
