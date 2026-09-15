---
type: reference
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Well-Architected Framework

## O que é?

Um conjunto de cinco "pilares" (lentes de avaliação) que a Microsoft recomenda usar para avaliar e guiar decisões arquiteturais na nuvem — não é uma checklist mecânica a ser marcada, e sim um conjunto de perguntas a fazer sobre qualquer decisão de arquitetura.

## Os cinco pilares

- **Reliability**: a aplicação se recupera de falhas e continua operando conforme esperado? (relacionado a [[Azure Availability]], [[RPO and RTO]]).
- **Security**: a aplicação e os dados estão protegidos contra acesso não autorizado e ameaças? (ver [[Azure Security Fundamentals]]).
- **Cost Optimization**: os recursos escolhidos entregam valor proporcional ao que custam? (ver [[Azure Pricing Fundamentals]]).
- **Operational Excellence**: a aplicação pode ser operada, monitorada e atualizada de forma sustentável? (conecta-se com deployment e, futuramente, observabilidade).
- **Performance Efficiency**: a aplicação escala e responde adequadamente à carga esperada? (ver [[Azure Scalability]]).

## Como usar (lentes, não checklist)

Para qualquer decisão (ex.: "usar AKS ou App Service?"), a pergunta não é "isso passa em todos os pilares?", mas sim: "quais trade-offs esta escolha faz entre os cinco pilares, e isso é aceitável para este contexto?". Otimizar um pilar frequentemente tem custo em outro (ex.: mais réplicas para Reliability custam mais em Cost Optimization).

## Relações

- [[Azure Scalability]]
- [[Azure Availability]]
- [[Azure Security Fundamentals]]
- [[Azure Pricing Fundamentals]]

## Referências

- Microsoft Learn — "Azure Well-Architected Framework": https://learn.microsoft.com/en-us/azure/well-architected/pillars
