---
type: concept
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - observability
---

# Correlation

## O que é?

Correlação é a capacidade de relacionar múltiplos sinais de telemetria (métricas, logs, traces) que representam partes diferentes da **mesma** operação ou incidente.

## Exemplo

```
Request
   ↓
Trace
   ↓
Dependency
   ↓
Database
   ↓
Exception
   ↓
Log
```

Uma única requisição de um usuário pode gerar: um trace mostrando o caminho da operação, uma métrica indicando aumento de latência, um log de exceção no ponto exato da falha — todos representando o **mesmo** evento, sob perspectivas diferentes. Correlação é conseguir conectar esses pontos de vista em uma única narrativa coerente, em vez de olhar cada sinal isoladamente.

## Escopo desta nota

Introdução conceitual. Os mecanismos técnicos que viabilizam correlação na prática (Operation ID, propagação de contexto, spans) estão aprofundados em [[Distributed Tracing]] (Etapa 8 — Application Insights).

## Relações

- [[Metrics Logs Traces]]
- [[Azure Monitor Troubleshooting]]
- [[Azure Monitor Traces]]
- [[Distributed Tracing]]
- [[Application Insights]]

## Referências

- Microsoft Learn — "Distributed tracing": https://learn.microsoft.com/en-us/azure/azure-monitor/app/distributed-tracing-telemetry
