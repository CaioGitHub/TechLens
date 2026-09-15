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

# Golden Signals

## O que são?

Os "quatro sinais de ouro" (Golden Signals) são um conjunto de quatro categorias de sinais frequentemente citadas (originadas do livro "Site Reliability Engineering" do Google) como um bom ponto de partida para monitorar qualquer sistema orientado a usuário.

## Os quatro sinais

- **Latency**: tempo que uma requisição leva para ser processada.
- **Traffic**: volume de demanda sobre o sistema (ex.: requests por segundo).
- **Errors**: taxa de requisições que falham.
- **Saturation**: o quão "cheio" o sistema está em relação à sua capacidade (ex.: uso de CPU/memória/conexões próximo do limite).

## Conexão com Azure Monitor

```
Golden Signals
      ↓
Metrics / Logs / Traces
      ↓
Azure Monitor
```

Os Golden Signals não são um recurso específico do Azure — são um modelo conceitual para decidir **o que** vale a pena medir; Metrics, Logs e Traces são os mecanismos usados para efetivamente coletar esses sinais no Azure.

## Escopo desta nota

Introdução conceitual apenas — não aprofunda a disciplina mais ampla de Site Reliability Engineering (SRE).

## Relações

- [[Performance Monitoring]]
- [[SLI SLO SLA]]
- [[Metrics Logs Traces]]

## Referências

- Google SRE Book — "Monitoring Distributed Systems": https://sre.google/sre-book/monitoring-distributed-systems/
