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

# Dependency Telemetry

## O que representa

Dependency Telemetry captura cada chamada que a aplicação faz para um componente externo — banco de dados, API externa, fila de mensagens, cache. Uma aplicação raramente trabalha isolada:

```
API
 ↓
Database
 ↓
External API
 ↓
Message Broker
```

## Para que serve

Dependency Telemetry ajuda a identificar:

- **dependências lentas** — qual chamada externa está consumindo mais tempo dentro de uma operação;
- **dependências que falham** — erros retornados por um serviço externo;
- **aumento de latência** — se o aumento vem da aplicação ou de uma dependência;
- **erros externos** — falhas que não são causadas pelo código da própria aplicação;
- **gargalos e problemas de integração** — pontos de contato entre sistemas que concentram lentidão.

## Request vs Dependency

- **Request** — o que a aplicação recebeu (entrada).
- **Dependency** — o que a aplicação chamou (saída).

Ambas podem compor a mesma operação: uma única Request pode conter múltiplas Dependencies (uma chamada ao banco, depois uma chamada a uma API de pagamento, por exemplo) — e é a correlação entre elas (ver [[Correlation]]) que permite responder "esta requisição lenta está lenta por causa de qual dependência?".

## Relação com Hexagonal Architecture

Uma chamada de [[Dependency Telemetry|Dependency]] tipicamente nasce em um **Driven Adapter** (ex.: um Persistence Adapter chamando o banco, ou um adapter chamando uma API externa) — ver [[Hexagonal Architecture + Application Insights]]. O [[Application Core]] não precisa saber que está sendo instrumentado; a telemetria de dependência é responsabilidade do adapter.

## Relações

- [[Application Telemetry]]
- [[Request Telemetry]]
- [[Application Map]]
- [[Performance Monitoring]]

## Referências

- Microsoft Learn — "Application Insights telemetry data model — Dependencies": https://learn.microsoft.com/en-us/azure/azure-monitor/app/data-model-dependency-telemetry
