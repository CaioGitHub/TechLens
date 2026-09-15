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

# Distributed Tracing

## Por que observar eventos isolados é insuficiente

```
Client
  ↓
API
  ↓
Order Service
  ↓
Database
  ↓
Payment API
```

Uma única operação de usuário pode atravessar vários componentes. Olhar cada componente isoladamente (um log aqui, uma métrica ali) não permite responder "esta requisição lenta está lenta por causa de qual dependência?" — é necessário conectar os sinais de todos os componentes que participaram da **mesma** operação.

## Conceitos-chave

- **Operation** — a unidade lógica de trabalho de ponta a ponta (ex.: uma requisição do usuário).
- **Operation ID** — identificador único compartilhado por todos os itens de telemetria (requests, dependencies, exceptions, traces) que pertencem à mesma operação.
- **Trace** — o caminho completo de uma operação através dos componentes (ver [[Azure Monitor Traces]]).
- **Span** — uma unidade de trabalho dentro do trace (uma chamada de método, uma consulta ao banco), com sua própria duração.
- **Contexto de telemetria / propagação de contexto** — o mecanismo pelo qual o Operation ID (e outros identificadores) é transmitido entre componentes — por exemplo, via cabeçalhos HTTP quando uma requisição passa de um serviço para outro.

## Como a investigação funciona

```
Request
   ↓
Trace
   ↓
Dependency
   ↓
External Service
```

Com o contexto de correlação propagado corretamente, uma requisição lenta pode ser seguida: qual dependência ela chamou, quanto tempo cada uma levou, e onde exatamente o tempo foi gasto — em vez de examinar logs de cada serviço separadamente e tentar adivinhar a relação entre eles.

## Relação com Correlation

Distributed Tracing é o mecanismo técnico que viabiliza a [[Correlation]] entre sinais: sem um identificador de operação compartilhado e propagado entre componentes, não há como conectar um log em um serviço a uma exceção em outro como parte do mesmo evento.

## Escopo desta nota

O objetivo aqui é o modelo conceitual (operation, trace, span, propagação de contexto). Detalhes de implementação específicos de uma tecnologia de tracing (formatos de propagação de contexto, exporters) são abordados em [[Azure Monitor OpenTelemetry]].

## Relações

- [[Correlation]]
- [[Azure Monitor Traces]]
- [[Application Map]]
- [[Application Insights Troubleshooting]]

## Referências

- Microsoft Learn — "Distributed tracing": https://learn.microsoft.com/en-us/azure/azure-monitor/app/distributed-tracing-telemetry
