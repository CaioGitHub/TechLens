---
type: technology
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-09
tags:
  - moc
  - azure
  - azure-monitor
  - log-analytics
  - kql
---

# Log Analytics

MOC (Map of Content) — Log Analytics é a capacidade do Azure Monitor para armazenar, consultar e analisar dados de log, usando a Kusto Query Language (KQL).

## Modelo mental

```
Application / Azure Resource
          ↓
       Telemetry
          ↓
      Azure Monitor
          ↓
   Azure Monitor Logs
          ↓
   Log Analytics Workspace
          ↓
          KQL
          ↓
      Analysis
          ↓
   Troubleshooting
```

- Aplicações e recursos Azure **produzem** telemetria.
- O [[Azure Monitor]] **coleta** essa telemetria.
- [[Azure Monitor Logs]] é o tipo de dado (logs, em contraste com métricas/traces).
- O [[Log Analytics Workspace]] é **onde** esses logs ficam armazenados.
- **KQL** ([[Kusto Query Language]]) é **como** esses dados são consultados.
- "Log Analytics" é o nome dado a essa experiência de consulta/análise sobre o Workspace — não um produto separado do Azure Monitor.

## Três conceitos que não são sinônimos

- **Application Insights ≠ Log Analytics** — Application Insights é a fonte especializada de telemetria de aplicação (ver [[Application Insights]]); Log Analytics é a capacidade de consulta sobre os dados armazenados (que incluem, mas não se limitam a, dados do Application Insights).
- **KQL ≠ Log Analytics** — KQL é a linguagem; Log Analytics é o ambiente/workspace onde ela é usada.
- **Log Analytics ≠ "uma pasta de logs"** — é um ambiente de armazenamento, indexação e análise, com retenção, permissões e custo próprios (ver [[Log Analytics Workspace]]).

## Fundamentals

- [[Azure Monitor Logs]]
- [[Log Analytics Workspace]]
- [[Application Insights Tables]]

## KQL

- [[Kusto Query Language]]
- [[KQL Query Pipeline]]
- [[KQL Filtering]]
- [[KQL Projection]]
- [[KQL Aggregation]]
- [[KQL Sorting and Limiting]]
- [[KQL Data Types and Dynamic]]
- [[KQL Variables and Functions]]
- [[KQL Join and Union]]

## Query Performance

- [[KQL Query Performance]]
- [[KQL Anti-Patterns]]

## Integração

- [[Java Spring Boot Log Analytics]]

## Troubleshooting

- [[Log Analytics Troubleshooting with KQL]]
- [[KQL Exercises]]

## Learning Path

- [[Log Analytics Learning Path]]

## Relações

- [[Azure Monitor]]
- [[Application Insights]]
- [[Observability]]
- [[Metrics Logs Traces]]
- [[Integration]]

## Referências

- Microsoft Learn — "Log Analytics workspace overview": https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-workspace-overview
- Microsoft Learn — "Kusto Query Language overview": https://learn.microsoft.com/en-us/kusto/query/?view=microsoft-fabric
