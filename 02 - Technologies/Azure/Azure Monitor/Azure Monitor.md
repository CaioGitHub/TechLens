---
type: technology
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - moc
  - azure
  - azure-monitor
  - observability
---

# Azure Monitor

MOC (Map of Content) — visão geral do Azure Monitor: a plataforma de observabilidade e monitoramento do Azure. Coleta, armazena, analisa e permite agir sobre sinais de telemetria de recursos e aplicações.

## O que é Azure Monitor

Azure Monitor é a plataforma central do Azure para coletar, armazenar, analisar e agir sobre telemetria — não é "um lugar onde ficam os logs", mas sim o conjunto de serviços que cobre coleta de sinais, análise, visualização e alertas.

## Modelo mental

```
Azure Resources
      +
Applications
      ↓
Telemetry
      ↓
Azure Monitor
      ↓
┌─────────────┬─────────────┬─────────────┐
│   Metrics   │    Logs     │   Traces    │
└─────────────┴─────────────┴─────────────┘
      ↓
Analysis
      ↓
Alerts
      ↓
Actions
```

## O que ele monitora

- **Recursos Azure**: App Service, VM, Database, Storage, Network, Container Apps — ver [[Resource Monitoring]].
- **Aplicações**: Spring Boot, incluindo requests, dependências, exceções — ver [[Application Monitoring]] (aprofundado via Application Insights na Etapa 8).
- **Infraestrutura**: rede, conectividade, saúde de componentes.

## Fundamentals

- [[Monitoring vs Observability]]
- [[Azure Monitor Metrics]]
- [[Metric Dimensions]]
- [[Metric Aggregation]]
- [[Azure Monitor Logs]]
- [[Logs vs Metrics]]
- [[Azure Monitor Traces]]
- [[Metrics Logs Traces]]

## Azure Resources

- [[Resource Monitoring]]
- [[Azure Activity Log]]
- [[Resource Logs]]
- [[Application Logs]]
- [[Azure Diagnostic Settings]]
- [[Log Analytics Workspace]]

## Application

- [[Application Monitoring]]
- [[Availability Monitoring]]
- [[Performance Monitoring]]
- [[Health Check]]
- [[Golden Signals]]
- [[SLI SLO SLA]]

## Alerts

- [[Azure Monitor Alerts]]
- [[Alert Rules]]
- [[Metric Alerts]]
- [[Log Alerts]]
- [[Severity]]
- [[Azure Monitor Action Groups]]
- [[Azure Monitoring Alerting Strategy]]

## Visualization

- [[Dashboards and Workbooks]]

## Architecture

- [[Azure Observability Architecture]]
- [[Monitoring vs Alerting]]
- [[Monitoring vs Observability vs Alerting]]
- [[Correlation]]
- [[Observability Signals vs Application Architecture]]

## Application Integration

- [[Java Spring Boot Azure Monitor]]
- [[Hexagonal Architecture + Observability]]

## Troubleshooting

- [[Azure Monitor Troubleshooting]]
- [[Azure Monitor Anti-Patterns]]

## Cost

- [[Azure Monitor Cost Awareness]]

## Learning Path

- [[Azure Monitor Learning Path]]

## Future (não aprofundado nesta etapa)

- Application Insights — capacidade de APM integrada ao Azure Monitor (Etapa 8 — concluída, ver [[Application Insights]]).
- Log Analytics + KQL — consulta avançada de logs (Etapa 9 — concluída, ver [[Log Analytics]]).

## Relações

- [[Azure]]
- [[Observability]]
- [[Java Spring Boot Application on Azure]]
- [[Application Insights]]
- [[Integration]]

## Referências

- Microsoft Learn — "Azure Monitor overview": https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview
- Microsoft Learn — "Azure Monitor data platform": https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/data-platform
