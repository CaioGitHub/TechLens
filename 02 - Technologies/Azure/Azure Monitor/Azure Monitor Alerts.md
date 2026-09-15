---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Azure Monitor Alerts

## O que é um Alert?

Um Alert é a notificação de que uma condição relevante, previamente definida, foi detectada em algum sinal de telemetria.

## Modelo

```
Telemetry
    ↓
Condition
    ↓
Alert Rule
    ↓
Alert
    ↓
Action
```

## Componentes principais

- **Condition**: a regra que define o que conta como "relevante" (ex.: "CPU > 80% por 5 minutos").
- **Threshold**: o valor limite usado na condição.
- **Evaluation**: o processo periódico que verifica se a condição foi atingida.
- **Severity**: a importância atribuída ao alerta quando disparado (ver [[Severity]]).
- **State**: o estado atual do alerta (ex.: ativo, reconhecido, fechado).
- **Action**: o que acontece quando o alerta dispara (ver [[Azure Monitor Action Groups]]).

## Ver também

- [[Alert Rules]] — diferença entre a regra e a ocorrência.
- [[Metric Alerts]]
- [[Log Alerts]]

## Relações

- [[Alert Rules]]
- [[Azure Monitor Action Groups]]
- [[Azure Monitoring Alerting Strategy]]
- [[Severity]]

## Referências

- Microsoft Learn — "Overview of Azure Monitor alerts": https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview
