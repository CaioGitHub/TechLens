---
type: architecture
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - hexagonal-architecture
  - observability
---

# Hexagonal Architecture + Observability

## Modelo

```
                Application Core
                      │
             ┌────────┴────────┐
             │                 │
         Input Ports       Output Ports
             │                 │
             ▼                 ▼
        Controllers       Adapters
                               │
                               ▼
                         Infrastructure
                               │
                               ▼
                         Azure Monitor
```

## Observabilidade como preocupação transversal

Observabilidade não é uma dependência do [[Domain]] ou de um [[Use Case]] — é uma preocupação **transversal** (cross-cutting concern), assim como logging e configuração já discutidos em [[Spring Boot Logging]]. Ela aparece nas bordas da aplicação:

- Um [[Adapters|Driving Adapter]] (ex.: um `@RestController`) pode gerar telemetria de requisição HTTP (latência, status code) sem que o [[Use Case]] chamado precise saber disso.
- Um [[Adapters|Driven Adapter]] (ex.: um Persistence Adapter) pode gerar telemetria de dependência (tempo de consulta ao banco) sem que o [[Application Core]] precise instrumentar nada.

## Não force Azure Monitor para dentro do Domain

O [[Domain]] não deve importar SDKs de telemetria do Azure Monitor ou Application Insights — assim como não deve importar SDKs do [[Azure SQL|Azure]] em geral (ver [[Hexagonal Architecture + Azure]]). Instrumentação acontece nas bordas (Adapters, Controllers, configuração de infraestrutura), preservando o Core livre de dependências de infraestrutura.

## Relações

- [[Hexagonal Architecture]]
- [[Hexagonal Architecture + Azure]]
- [[Observability Signals vs Application Architecture]]
- [[Java Spring Boot Azure Monitor]]
- [[Hexagonal Architecture + Application Insights]]

## Referências

- Microsoft Learn — "Azure Monitor overview": https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview
