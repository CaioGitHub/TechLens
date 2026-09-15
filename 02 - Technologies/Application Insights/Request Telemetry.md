---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - application-insights
  - observability
---

# Request Telemetry

## O que representa

Request Telemetry captura cada requisição recebida pela aplicação (tipicamente HTTP) — o ponto de entrada de uma operação.

## Exemplo

```
GET /orders/123

Request
├── URL
├── HTTP method
├── status code
├── duration
├── timestamp
├── success
└── correlation context
```

## Para que serve

Requests são a base para investigar:

- **aumento de latência** — duração das requisições ao longo do tempo;
- **aumento de HTTP 500** — taxa de falha por status code;
- **endpoints problemáticos** — quais rotas concentram erro ou lentidão;
- **throughput** — quantidade de requisições por período;
- **taxa de sucesso** — proporção de requisições bem-sucedidas;
- **disponibilidade** — a aplicação está respondendo (ver [[Availability Monitoring]]).

## Relação com Spring Boot

```
HTTP Request
      ↓
Spring MVC
      ↓
Controller
      ↓
Use Case
```

Em uma aplicação Spring Boot instrumentada, cada requisição que chega a um `@RestController` pode gerar automaticamente um item de Request Telemetry, capturando a borda de entrada — antes de qualquer lógica de negócio ser executada. Isso é coerente com [[Hexagonal Architecture + Application Insights]]: a telemetria de requisição nasce no adapter de entrada, não dentro do [[Use Case]].

## Request vs Dependency

Uma Request representa o que a aplicação **recebeu**; uma [[Dependency Telemetry|Dependency]] representa o que a aplicação **chamou**. Ambas podem fazer parte da mesma operação: uma Request pode conter, internamente, uma ou mais Dependencies — ver [[Correlation]].

## Relações

- [[Application Telemetry]]
- [[Dependency Telemetry]]
- [[Application Insights Troubleshooting]]
- [[Golden Signals]]

## Referências

- Microsoft Learn — "Application Insights telemetry data model — Requests": https://learn.microsoft.com/en-us/azure/azure-monitor/app/data-model-request-telemetry
