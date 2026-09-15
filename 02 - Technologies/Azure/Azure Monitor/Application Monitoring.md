---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - spring
---

# Application Monitoring

## O que é?

Monitoramento de aplicação é a observação do comportamento do próprio código em execução — não apenas do recurso de infraestrutura que o hospeda.

## Exemplo com Spring Boot

```
Spring Boot
    ↓
HTTP Requests
    ↓
Dependencies (chamadas a banco, APIs externas)
    ↓
Exceptions
    ↓
Performance (tempo de resposta, throughput)
```

## Por que monitorar só infraestrutura não é suficiente

[[Resource Monitoring]] mostra, por exemplo, que a CPU do App Service está normal e que o número de requisições está estável — mas não revela que 8% das requisições estão retornando erro 500 por uma exceção específica no código, ou que uma dependência externa está lenta. Esse tipo de sinal só existe quando a própria aplicação é instrumentada.

## Escopo desta etapa

Esta nota estabelece apenas o conceito — a instrumentação prática de uma aplicação Spring Boot (SDK, Java Agent, request/dependency/exception telemetry) é o foco da Etapa 8 — Application Insights.

## Relações

- [[Resource Monitoring]]
- [[Java Spring Boot Azure Monitor]]
- [[Performance Monitoring]]
- [[Availability Monitoring]]

## Referências

- Microsoft Learn — "Application monitoring for Java": https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable
