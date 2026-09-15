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
  - application-insights
  - observability
---

# Application Insights

MOC (Map of Content) — Application Insights é a solução de **Application Performance Monitoring (APM)** do Azure, voltada à observabilidade de aplicações. Não é uma plataforma separada do [[Azure Monitor]]: é a parte do Azure Monitor especializada em telemetria de aplicação.

## Application Insights dentro do Azure Monitor

```
                    Azure Monitor
                         │
        ┌────────────────┼────────────────┐
        │                │                │
      Metrics          Logs          Application
   (plataforma)    (plataforma)       Insights
                                          │
                                 Application Telemetry
                          (Requests, Dependencies,
                           Exceptions, Traces)
```

Application Insights **usa** a infraestrutura de dados do Azure Monitor (armazenamento em um [[Log Analytics Workspace]], mesmo mecanismo de [[Azure Monitor Alerts]], mesmas ferramentas de consulta) e a especializa para telemetria de aplicação. Não existe "Application Insights ≠ Azure Monitor" como se fossem plataformas independentes — hoje, todo recurso Application Insights é **workspace-based** (armazenado em um Log Analytics Workspace), o que torna essa integração explícita. O modo clássico (standalone, sem workspace) está em retirada.

## Modelo mental completo desta etapa

```
Spring Boot
      ↓
Application
      ↓
Instrumentation
      ↓
Requests / Dependencies / Exceptions / Traces
      ↓
Application Insights
      ↓
Azure Monitor
      ↓
Analysis
      ↓
Alerts
```

## Fundamentals

- [[Application Performance Monitoring]]
- [[Application Telemetry]]
- [[Request Telemetry]]
- [[Dependency Telemetry]]
- [[Exception Telemetry]]
- [[Trace Telemetry]]

## Correlation e Distributed Tracing

- [[Correlation]] (aprofundada nesta etapa com mecanismos técnicos)
- [[Distributed Tracing]]
- [[Application Map]]

## Application Health

- [[Availability Monitoring]]
- [[Performance Monitoring]]

## Coleta e custo

- [[Sampling]]
- [[Instrumentation]]
- [[Azure Monitor OpenTelemetry]]

## Integração

- [[Java Spring Boot Application Insights]]
- [[Hexagonal Architecture + Application Insights]]

## Troubleshooting

- [[Application Insights Troubleshooting]]

## Learning Path

- [[Application Insights Learning Path]]

## Future (não aprofundado nesta etapa)

- Log Analytics + KQL — consulta avançada de logs sobre esses mesmos dados (Etapa 9 — concluída, ver [[Log Analytics]]).

## Relações

- [[Azure Monitor]]
- [[Log Analytics]]
- [[Observability]]
- [[Java Spring Boot Azure Monitor]]
- [[Golden Signals]]
- [[SLI SLO SLA]]
- [[Integration]]

## Referências

- Microsoft Learn — "Application Insights overview": https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview
- Microsoft Learn — "Application Insights workspace-based resources": https://learn.microsoft.com/en-us/azure/azure-monitor/app/create-workspace-resource
