---
type: concept
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Log Alerts

## Modelo

```
Logs
  ↓
Query
  ↓
Condition
  ↓
Alert
```

## O que é?

Um Log Alert dispara com base no resultado de uma consulta sobre dados armazenados em um [[Log Analytics Workspace]] — permite condições mais ricas e específicas do que um Metric Alert (ex.: "existe mais de X ocorrências de uma exceção específica nos últimos 15 minutos"), ao custo de avaliação tipicamente menos frequente/imediata.

## Escopo desta nota

Esta é apenas uma introdução conceitual. A construção efetiva de consultas para alimentar um Log Alert depende de KQL (Kusto Query Language), que será estudado na Etapa 9 — Log Analytics + KQL.

## Relações

- [[Azure Monitor Alerts]]
- [[Metric Alerts]]
- [[Log Analytics Workspace]]

## Referências

- Microsoft Learn — "Log alerts": https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-types#log-alerts
