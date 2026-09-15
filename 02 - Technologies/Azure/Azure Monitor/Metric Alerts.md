---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Metric Alerts

## Modelo

```
Metric
   ↓
Condition
   ↓
Alert
```

## Exemplos conceituais

- `CPU > 80%` por um determinado período.
- `Error rate > 5%` nos últimos 5 minutos.

## Característica

Metric Alerts avaliam valores numéricos de série temporal (ver [[Azure Monitor Metrics]]) contra um threshold — tipicamente avaliados com maior frequência e menor latência de detecção do que Log Alerts, por operarem sobre dados já agregados e otimizados para esse fim.

## Não generalizar o exemplo

O threshold exato (ex.: "80%", "5%") depende do recurso, da métrica disponível e do contexto do sistema — não existe um valor universal correto (ver [[Azure Monitoring Alerting Strategy]]).

## Relações

- [[Azure Monitor Alerts]]
- [[Alert Rules]]
- [[Azure Monitor Metrics]]

## Referências

- Microsoft Learn — "Metric alerts overview": https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-types#metric-alerts
