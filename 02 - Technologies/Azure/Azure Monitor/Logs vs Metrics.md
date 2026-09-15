---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - observability
---

# Logs vs Metrics

## A pergunta que cada um responde

```
Metric
  ↓
"Quanto?"

Log
  ↓
"O que aconteceu?"
```

## Exemplo lado a lado

```
Metric:
HTTP 500 rate = 8%

Log:
Request /orders failed
status=500
exception=NullPointerException at OrderService.process(...)
```

A métrica diz que há um problema em andamento (8% das requisições falhando); o log diz exatamente o que falhou e por quê para uma requisição específica.

## Usados em conjunto

Na prática, os dois se complementam: a métrica costuma ser o primeiro sinal de que algo está errado (ex.: um alerta dispara porque o error rate subiu); o log é usado depois, para investigar a causa raiz daquele aumento. Ver o raciocínio completo em [[Azure Monitor Troubleshooting]].

## Relações

- [[Azure Monitor Metrics]]
- [[Azure Monitor Logs]]
- [[Metrics Logs Traces]]

## Referências

- Microsoft Learn — "Azure Monitor data platform": https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/data-platform
