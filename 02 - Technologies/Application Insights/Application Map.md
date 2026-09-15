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

# Application Map

## O que é

Application Map é uma visualização topológica que o Application Insights constrói a partir da [[Correlation]] entre [[Request Telemetry|requests]] e [[Dependency Telemetry|dependencies]] — mostrando os componentes de uma aplicação distribuída e como eles se conectam.

## Modelo

```
                ┌──────────────┐
                │    Client    │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │ Spring Boot  │
                └──────┬───────┘
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
       ┌──────────┐        ┌────────────┐
       │ Database │        │ Payment API│
       └──────────┘        └────────────┘
```

## Para que serve

- **visualizar dependências** — quais componentes externos a aplicação utiliza;
- **identificar componentes problemáticos** — nós do mapa com taxa de erro ou latência elevada tipicamente aparecem destacados;
- **entender a arquitetura real** em produção, não apenas a arquitetura documentada;
- **acelerar troubleshooting** — ponto de partida visual antes de mergulhar em requests, exceptions ou traces específicos.

## O que o Application Map não é

Application Map é uma ferramenta de **visualização** derivada da telemetria já coletada — não substitui [[Request Telemetry|requests]], [[Azure Monitor Logs|logs]] ou [[Azure Monitor Traces|traces]] como fonte de investigação detalhada. Ele ajuda a decidir **onde olhar**, mas a causa raiz de um problema específico ainda é encontrada examinando os sinais individuais (exceções, dependências lentas, traces).

## Relações

- [[Dependency Telemetry]]
- [[Correlation]]
- [[Distributed Tracing]]
- [[Azure Observability Architecture]]

## Referências

- Microsoft Learn — "Application Map": https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-map
