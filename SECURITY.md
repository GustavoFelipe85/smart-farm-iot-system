# Política de Segurança (Security Policy)

A infraestrutura do **Smart Farm IoT System** é concebida sob o princípio de *Secure by Design*, empregando contêineres imutáveis, execução *rootless* e descarte total de capacidades do kernel (`cap_drop: ALL`).

## Versões Suportadas

Apenas a ramificação principal (`main`) e as *releases* a partir da versão 2.0.0 (onde a esteira DevSecOps foi consolidada) recebem patches de segurança ativos.

| Versão | Suporte a Correções de Segurança |
| :--- | :--- |
| >= 2.0.x | :white_check_mark: Ativo |
| < 2.0.x | :x: Depreciado |

## Relato de Vulnerabilidades (Vulnerability Reporting)

Para proteger a integridade do sistema, vulnerabilidades não devem ser divulgadas publicamente através de *Issues* no GitHub. Siga o protocolo de divulgação coordenada:

1. **Contato Direto:** Envie um e-mail detalhado diretamente para o mantenedor do projeto com a tag `[SECURITY]` no assunto.
2. **Artefatos Necessários:** O relatório deve conter obrigatoriamente:
   * Vetor de ataque detalhado.
   * Prova de Conceito (PoC) reprodutível no ambiente Docker local.
   * Pontuação CVSS v3.1 estimada.
3. **Acordo de Nível de Serviço (SLA):** 
   * Confirmação de recebimento: 48 horas.
   * Validação técnica da PoC: 5 dias úteis.
   * Lançamento de *patch* e comunicação: A depender da complexidade, mitigado na *branch* `main` prioritariamente.

## Threat Model & Mitigações Existentes

Antes de relatar *exploits*, considere as barreiras arquiteturais já validadas na implantação:
* **Escalonamento de Privilégios:** Mitigado via `security_opt: no-new-privileges:true`.
* **Injeção de Malware/Persistência:** Mitigado via sistemas de arquivos restritos (`read_only: true`) e injeção de estados temporários em RAM (`tmpfs`).
* **Segregação de Rede:** Banco de dados de séries temporais (InfluxDB) e *broker* de telemetria (Mosquitto) rodam em rede *bridge* isolada (`iot-network`), inacessíveis de forma externa exceto através das rotas validadas pela API.
