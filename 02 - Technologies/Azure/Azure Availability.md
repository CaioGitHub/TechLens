---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Availability

## O que é?

Disponibilidade (availability) é a proporção de tempo em que uma aplicação/serviço está funcionando corretamente e acessível — normalmente aumentada através de redundância e detecção rápida de falhas.

## Mecanismos que aumentam disponibilidade

- **Redundancy**: múltiplas instâncias/réplicas, de forma que a falha de uma não derrube o sistema — combinado com [[Azure Availability Zones]] para isolar falhas físicas.
- **Health checks**: monitoramento contínuo para detectar instâncias não saudáveis rapidamente (ver [[Application Gateway and Load Balancing]]).
- **Zones**: distribuir réplicas entre zonas fisicamente isoladas.
- **Scaling**: capacidade extra para absorver picos sem degradar (ver [[Azure Scalability]]).
- **Failover**: capacidade de redirecionar tráfego para uma réplica/região saudável quando a principal falha.

## SLA não é garantia absoluta

Um SLA (Service Level Agreement) é um compromisso contratual sobre disponibilidade esperada (ex.: "99,9% no mês") — **não é uma garantia técnica absoluta de que o serviço nunca ficará indisponível**. SLAs tipicamente definem créditos financeiros em caso de violação, não eliminam a possibilidade de falha. A arquitetura da aplicação ainda precisa ser desenhada considerando que falhas acontecem.

## Relações

- [[Azure Availability Zones]]
- [[Azure Scalability]]
- [[RPO and RTO]]
- [[Azure Well-Architected Framework]]

## Referências

- Microsoft Learn — "Design for high availability": https://learn.microsoft.com/en-us/azure/well-architected/reliability/
