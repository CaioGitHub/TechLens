---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - observability
---

# Monitoring vs Observability

## Monitoring

Monitoring é o ato de coletar e acompanhar sinais previamente definidos (métricas, logs conhecidos) para saber **se** um sistema está se comportando dentro do esperado — geralmente responde perguntas que já foram antecipadas ("a CPU está alta?", "o serviço está no ar?").

## Observability

Observability é a **capacidade** de um sistema de ter seu comportamento interno compreendido a partir de seus sinais externos (métricas, logs, traces) — incluindo perguntas que **não** foram antecipadas quando o sistema foi instrumentado ("por que este usuário específico recebeu um erro 500 às 14:32?").

## A diferença central

Monitoring pressupõe que você já sabe o que observar. Observability é sobre ter sinais ricos o suficiente para investigar problemas desconhecidos — um sistema pode ser monitorado (ter dashboards de CPU/memória) e ainda assim ser pouco observável (não ter logs/traces suficientes para explicar um comportamento inesperado).

## Relação com este Second Brain

Esta base não aprofunda a teoria de observabilidade (ex.: OpenTelemetry, os "três pilares" academicamente) — usa a distinção apenas como modelo mental para entender por que [[Azure Monitor]] combina Metrics, Logs e Traces em vez de apenas um deles.

## Relações

- [[Azure Monitor]]
- [[Metrics Logs Traces]]
- [[Monitoring vs Alerting]]

## Referências

- Microsoft Learn — "Azure Monitor overview": https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview
