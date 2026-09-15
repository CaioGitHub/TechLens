---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Monitoring vs Alerting

## A distinção

```
Monitoring
   ↓
observar e analisar

Alerting
   ↓
detectar condição relevante e notificar/agir
```

Monitoring é a atividade contínua de coletar e acompanhar sinais (ver [[Monitoring vs Observability]]); Alerting é o mecanismo específico que detecta quando um desses sinais cruza uma condição relevante e notifica/aciona alguém (ver [[Azure Monitor Alerts]]).

## Uma aplicação pode ser monitorada sem alertas adequados

É perfeitamente possível ter dashboards ricos, métricas e logs completos (boa capacidade de monitoring) e ainda assim não ter uma estratégia de alertas adequada — ninguém é avisado proativamente quando algo dá errado, dependendo de alguém observar um painel manualmente. Monitoring é necessário mas não suficiente para detecção proativa de problemas.

## Relações

- [[Azure Monitor Alerts]]
- [[Monitoring vs Observability]]
- [[Dashboards and Workbooks]]

## Referências

- Microsoft Learn — "Overview of Azure Monitor alerts": https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview
