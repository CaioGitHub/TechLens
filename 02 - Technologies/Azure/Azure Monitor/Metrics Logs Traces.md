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

# Metrics Logs Traces

## Visão integrada

```
                    Application
                         │
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
       Metrics         Logs          Traces
          │              │              │
          └──────────────┼──────────────┘
                         ↓
                   Azure Monitor
```

## A pergunta que cada sinal ajuda a responder

- **Metrics** → *Está acontecendo?* (existe um problema em andamento, medido numericamente?)
- **Logs** → *O que aconteceu?* (qual foi o evento específico, com que contexto?)
- **Traces** → *Onde aconteceu e por onde passou?* (qual o caminho da operação através do sistema?)

Essas não são definições absolutas — cada sinal pode, em algum grau, responder as outras perguntas também. Mas essa é a força natural de cada um: métricas são rápidas de agregar e ideais para detecção; logs carregam contexto rico para investigação; traces revelam o caminho através de componentes distribuídos.

## Por que os três juntos

Nenhum sinal isolado costuma ser suficiente para diagnosticar um problema completo — uma métrica pode indicar *que* algo está errado, um log pode indicar *o quê*, e um trace pode indicar *onde*. Ver o raciocínio de investigação completo em [[Azure Monitor Troubleshooting]] e [[Correlation]].

## Relações

- [[Azure Monitor Metrics]]
- [[Azure Monitor Logs]]
- [[Azure Monitor Traces]]
- [[Azure Monitor]]

## Referências

- Microsoft Learn — "Azure Monitor data platform": https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/data-platform
