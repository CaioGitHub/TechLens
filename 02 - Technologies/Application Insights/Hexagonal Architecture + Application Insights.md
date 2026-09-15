---
type: architecture
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - application-insights
  - hexagonal-architecture
---

# Hexagonal Architecture + Application Insights

## Modelo

```
                Application Insights
                       │
                       ↓
              Observability Layer
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Request        Trace        Dependency
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                  Application
                       ↓
                    Domain
```

## Observabilidade permanece transversal

Este modelo estende o que já foi estabelecido em [[Hexagonal Architecture + Observability]]: Application Insights não é uma dependência arquitetural do [[Domain]]. A telemetria de requisição nasce em um **Driving Adapter** (ex.: `@RestController`), a de dependência nasce em um **Driven Adapter** (ex.: Persistence Adapter chamando o banco), e ambas são correlacionadas pela camada de observabilidade — sem que o [[Use Case]] precise conhecer o Application Insights.

```
Application
   ↑
Observability / Instrumentation
```

A seta aponta para cima propositalmente: a instrumentação observa a aplicação a partir de fora/das bordas — ela não é algo que o Domain "chama" ou de que depende.

## O que evitar

```
Domain
   ↓
Application Insights
```

Se um caso de uso importar diretamente um SDK do Application Insights (ou anotações específicas do Java Agent) para emitir telemetria de negócio, isso acopla o Domain à infraestrutura de observabilidade — o mesmo problema já discutido para SDKs de Azure em geral (ver [[Hexagonal Architecture + Azure]]). Quando telemetria de negócio (Custom Telemetry) for necessária, o ideal é expô-la através de uma porta/abstração própria da aplicação, mantendo o Domain livre de dependências diretas de infraestrutura.

## Relações

- [[Hexagonal Architecture + Observability]]
- [[Hexagonal Architecture + Azure]]
- [[Java Spring Boot Application Insights]]
- [[Application Telemetry]]

## Referências

- Microsoft Learn — "Application Insights overview": https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview
