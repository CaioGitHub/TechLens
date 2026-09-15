---
type: architecture
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - observability
---

# Azure Observability Architecture

## Modelo completo

```
                         SYSTEM
                           │
            ┌──────────────┼──────────────┐
            ↓              ↓              ↓
        Application     Azure Resource   Network
            │              │              │
            └──────────────┼──────────────┘
                           ↓
                       Telemetry
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
           Metrics        Logs        Traces
              │            │            │
              └────────────┼────────────┘
                           ↓
                    Azure Monitor
                           │
              ┌────────────┴────────────┐
              ↓                         ↓
          Analysis                    Alerts
              │                         │
              ↓                         ↓
         Visualization              Actions
```

## Leitura do diagrama

Três fontes geram telemetria (aplicação, recursos Azure, rede) — todas convergem para os três tipos de sinal ([[Azure Monitor Metrics|Metrics]], [[Azure Monitor Logs|Logs]], [[Azure Monitor Traces|Traces]]), que são processados pelo [[Azure Monitor]]. A partir daí, dois caminhos paralelos: análise (que alimenta [[Dashboards and Workbooks|visualização]]) e avaliação de condições (que alimenta [[Azure Monitor Alerts|alertas]], que disparam ações via [[Azure Monitor Action Groups|Action Groups]]).

## Relações

- [[Azure Monitor]]
- [[Metrics Logs Traces]]
- [[Azure Monitor Alerts]]

## Referências

- Microsoft Learn — "Azure Monitor overview": https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview
