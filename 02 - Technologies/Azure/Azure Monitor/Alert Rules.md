---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Alert Rules

## A distinção central

- **Alert Rule**: a definição de **quando** uma condição deve gerar um alerta (a "regra" — configurada uma vez, avaliada continuamente).
- **Alert**: a **ocorrência** concreta de uma condição detectada (o "evento" — criado toda vez que a regra é satisfeita).

## Analogia

Uma Alert Rule é como uma regra "se a temperatura passar de 38°C, avise-me" — configurada uma única vez. Cada vez que a temperatura de fato ultrapassa 38°C, um Alert específico é gerado, representando aquela ocorrência.

## Por que a distinção importa

Uma única Alert Rule pode gerar múltiplos Alerts ao longo do tempo (toda vez que a condição volta a ser satisfeita) — entender essa diferença evita confundir "eu configurei um alerta" (a regra) com "eu recebi um alerta" (a ocorrência).

## Relações

- [[Azure Monitor Alerts]]
- [[Metric Alerts]]
- [[Log Alerts]]

## Referências

- Microsoft Learn — "Types of Azure Monitor alerts": https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-types
