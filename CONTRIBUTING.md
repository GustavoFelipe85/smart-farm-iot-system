# 📋 **CÓDIGO COMPLETO DO CONTRIBUTING.md**

Aqui está o código completo para você colar no arquivo:

```markdown
# 🤝 Guia de Contribuição

Bem-vindo ao **Smart Farm IoT System**! Este é um projeto de pesquisa acadêmica desenvolvido para o Programa de Pós-Graduação em Ciência da Computação da UNIOESTE.

## 🎓 Contexto Acadêmico

Este projeto representa a evolução do trabalho de TCC para aplicações em pesquisa de mestrado, focando em:
- **IoT para Agricultura de Precisão**
- **Machine Learning aplicado a dados agrícolas** 
- **Sistemas Distribuídos e Edge Computing**
- **Otimização de Recursos em Agricultura Familiar**

## 🔬 Para Pesquisadores

### 📊 Como Replicar os Experimentos

#### 1. **Configuração do Ambiente de Pesquisa**
```bash
# Clone o repositório
git clone https://github.com/GustavoFelipe85/smart-farm-iot-system.git
cd smart-farm-iot-system

# Execute a infraestrutura completa
docker-compose up -d

# Aguarde os serviços inicializarem (1-2 minutos)
```

#### 2. **Execução dos Modelos de Machine Learning**
```bash
# Acesse a pasta de machine learning
cd src/ml

# Execute o Jupyter Notebook principal
jupyter notebook agriculture_analysis.ipynb
```

#### 3. **Estrutura de Dados para Experimentos**
```csv
timestamp,temperature,soil_moisture,humidity,light_intensity,productivity,crop_type
2024-01-01 08:00:00,25.3,65.2,72.1,8450,1250,lettuce
```

### 📈 Metodologia de Validação Científica

#### **Métricas de Avaliação:**
- **RMSE**: Root Mean Square Error
- **MAE**: Mean Absolute Error
- **R²**: Coeficiente de Determinação
- **Acurácia**: Para modelos de classificação

## 💻 Para Desenvolvedores

### ⌨️ Padrões de Código

#### **Python (Backend/ML)**
```python
def predict_productivity(temperature: float, soil_moisture: float) -> dict:
    """
    Predict agricultural productivity based on environmental factors.
    """
    return {"prediction": 1250.0, "confidence": "high"}
```

#### **C++ (Firmware ESP32)**
```cpp
class SensorReader {
private:
    const int sampleRate = 300000; // 5 minutes
    
public:
    void readSensorData() {
        // Implementation
    }
};
```

### 🧪 Processo de Testes

#### **1. Testes Unitários**
```bash
pytest tests/unit/ -v
```

#### **2. Validação de Dados**
```bash
python src/validation/validate_dataset.py
```

## 🚀 Processo de Contribuição

### 1. **Configuração do Ambiente**
```bash
git clone https://github.com/GustavoFelipe85/smart-farm-iot-system.git
cd smart-farm-iot-system

# Configure o ambiente virtual
python -m venv venv
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### 2. **Fluxo de Trabalho**
```bash
# Crie uma branch para sua feature
git checkout -b feature/nova-funcionalidade

# Desenvolva e teste
git add .
git commit -m "feat: adiciona nova funcionalidade"

# Push e abra Pull Request
git push origin feature/nova-funcionalidade
```

## 📝 Template de Pull Request

```markdown
## Descrição das Mudanças

**Tipo de Mudança:**
- [ ] 🎯 Nova funcionalidade
- [ ] 🐛 Correção de bug
- [ ] 📚 Melhoria de documentação
- [ ] 🔬 Experimentos/Análises

## Métodos de Teste
- [ ] Testes unitários passando
- [ ] Experimentos replicados
- [ ] Documentação atualizada

## Impacto na Pesquisa
Como esta mudança contribui para os objetivos de pesquisa?
```

## 🐛 Reportando Problemas

Use as [Issues do GitHub](https://github.com/GustavoFelipe85/smart-farm-iot-system/issues) e inclua:

- Descrição detalhada do problema
- Passos para reproduzir
- Ambiente (OS, versões, etc)

## 📧 Contato

**Gustavo Felipe** - Pesquisador Principal
- Email: gustavo.f.p.f@outlook.com.br
- LinkedIn: [linkedin.com/in/gustavofpaluch](https://linkedin.com/in/gustavofpaluch)

---

*Projeto de pesquisa do Programa de Pós-Graduação em Ciência da Computação - UNIOESTE*
```

## 🎯 **PARA COPIAR/COLAR:**

1. **Clique no editor** do CONTRIBUTING.md
2. **Selecione tudo** (Ctrl+A)  
3. **Cole este código** (Ctrl+V)
4. **Commit:** `feat: add contributing guidelines`
5. **Marque:** "Create a new branch for this commit and start a pull request"

## 🔄 **PRÓXIMOS PASSOS:**

Depois de salvar, vamos:
1. **Atualizar README.md** com link para o CONTRIBUTING
2. **Criar docker-compose.yml** 
3. **Criar requirements.txt**

