---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - observability
---

# Azure Monitor Traces

## O que é um trace?

Um trace representa o caminho completo de uma única operação (ex.: uma requisição HTTP) conforme ela atravessa múltiplos componentes de um sistema — permitindo visualizar não apenas que algo aconteceu, mas **onde** e **por onde** essa operação passou.

## Span

Um trace é composto por um ou mais **spans** — cada span representa uma unidade de trabalho dentro da operação (ex.: uma chamada de método, uma consulta ao banco, uma chamada a uma API externa), com sua própria duração e contexto.

## Modelo

```
HTTP Request
      ↓
Controller
      ↓
Service
      ↓
Database
      ↓
External API
```

Cada etapa desse caminho pode ser representada como um span dentro do trace geral da requisição — permitindo ver quanto tempo cada etapa levou e onde, especificamente, uma operação lenta ou com erro se originou.

## Por que isso importa

Sem traces, uma requisição lenta é uma "caixa preta": sabe-se que ela demorou, mas não onde o tempo foi gasto. Com traces, é possível identificar se o gargalo está no banco de dados, em uma API externa, ou em processamento interno.

## Escopo desta nota

Esta é uma introdução conceitual — a implementação prática de tracing distribuído no ecossistema Azure (Application Insights, instrumentação automática/manual, correlação entre serviços) pertence à Etapa 8.

## Relações

- [[Metrics Logs Traces]]
- [[Correlation]]
- [[Performance Monitoring]]

## Referências

- Microsoft Learn — "Distributed tracing": https://learn.microsoft.com/en-us/azure/azure-monitor/app/distributed-tracing-telemetry
