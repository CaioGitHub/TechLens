---
type: concept
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Dashboards and Workbooks

## Dashboard

Um Dashboard é uma visualização configurável de métricas/logs — gráficos, contadores, mapas — usado para acompanhamento visual e operacional contínuo (ex.: um painel exibido na sala de operações mostrando CPU, requests e erros em tempo real).

## Workbook

Um Workbook é uma ferramenta de análise e visualização mais flexível que um Dashboard simples — combina texto, consultas, parâmetros interativos e visualizações em um documento único, voltado para investigação e análise mais aprofundada, não apenas acompanhamento passivo.

## Dashboard vs. Workbook

| | Dashboard | Workbook |
|---|---|---|
| Uso típico | Acompanhamento operacional contínuo | Investigação e análise pontual |
| Interatividade | Baixa (visualização fixa) | Alta (parâmetros, narrativa, múltiplas fontes de dado) |
| Público típico | Equipe de operações, monitoramento passivo | Quem está investigando um problema específico |

## Dashboard vs. Alert

```
Dashboard
   ↓
ajuda a visualizar

Alert
   ↓
ajuda a detectar e notificar
```

Um Dashboard não notifica ninguém proativamente — alguém precisa estar olhando para ele. Um Alert existe justamente para não depender de alguém observando um painel o tempo todo (ver [[Monitoring vs Alerting]]).

## Escopo desta nota

Não aprofunda customização avançada de Workbooks (parâmetros complexos, múltiplas fontes combinadas) — apenas o suficiente para diferenciar os dois conceitos.

## Relações

- [[Azure Monitor Alerts]]
- [[Monitoring vs Alerting]]

## Referências

- Microsoft Learn — "Azure Workbooks": https://learn.microsoft.com/en-us/azure/azure-monitor/visualize/workbooks-overview
