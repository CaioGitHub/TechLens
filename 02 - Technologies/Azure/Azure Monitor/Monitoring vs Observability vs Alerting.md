---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - observability
---

# Monitoring vs Observability vs Alerting

## Visão integrada

```
Monitoring
     ↓
coleta e acompanhamento

Observability
     ↓
entendimento do comportamento

Alerting
     ↓
resposta a condições relevantes
```

## Não são sinônimos

- **Monitoring** é a atividade de coletar e acompanhar sinais já conhecidos (ver [[Monitoring vs Observability]]).
- **Observability** é a capacidade mais ampla de compreender comportamentos não antecipados a partir dos sinais disponíveis.
- **Alerting** é o mecanismo de resposta ativa quando uma condição relevante é detectada (ver [[Monitoring vs Alerting]]).

Um sistema pode ter os três em graus diferentes: bem monitorado, mas pouco observável (dashboards de CPU, mas sem logs ricos para investigar um bug específico); ou observável, mas sem alertas (dados ricos disponíveis, mas ninguém é avisado proativamente quando algo falha).

## Relações

- [[Monitoring vs Observability]]
- [[Monitoring vs Alerting]]
- [[Azure Observability Architecture]]

## Referências

- Microsoft Learn — "Azure Monitor overview": https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview
