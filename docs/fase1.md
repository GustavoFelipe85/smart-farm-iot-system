# Relatório Técnico — Fase 1  

## Smart Farm IoT System


1. Objetivo da Fase 1
A Fase 1 teve como objetivo estabelecer a infraestrutura básica do sistema IoT, validando a
comunicação entre dispositivos de borda e o backend por meio do protocolo MQTT. Esta fase é
essencial para garantir conectividade, segurança e confiabilidade na troca de dados.

2. Infraestrutura IoT Implementada
A infraestrutura da Fase 1 é composta por um microcontrolador ESP32 configurado como nó
IoT, um broker MQTT seguro (Mosquitto) e uma arquitetura preparada para escalabilidade. O
ESP32 é responsável pela publicação periódica de mensagens simuladas representando
sensores.

3. Metodologia
O ESP32 foi configurado para conectar-se ao broker MQTT utilizando autenticação. Mensagens
em formato JSON são publicadas em tópicos específicos, permitindo a validação da
comunicação e da integridade dos dados transmitidos.

4. Ambiente Experimental
O ambiente utiliza um broker MQTT configurado em container Docker, com controle de acesso
por usuário e senha. Essa configuração permite testes reprodutíveis e isolamento do ambiente.
5. Resultados Obtidos
Os testes demonstraram comunicação estável entre o ESP32 e o broker MQTT, com publicação
contínua de mensagens e ausência de perdas significativas. A autenticação garantiu controle
adequado de acesso ao sistema.

6. Limitações Conhecidas
Nesta fase, os dados são simulados e não há integração com sensores físicos reais. O foco foi
exclusivamente na validação da infraestrutura de comunicação.

7. Conclusão
A Fase 1 encontra-se concluída, estabelecendo uma base sólida de comunicação IoT que
sustenta as fases subsequentes do projeto, especialmente a ingestão e processamento de
dados na Fase 2.

---

Esta fase estabelece uma base reprodutível e validada de comunicação IoT, essencial para experimentação controlada nas fases subsequentes.

---

🔙 Voltar ao [README principal](../README.md)

---
