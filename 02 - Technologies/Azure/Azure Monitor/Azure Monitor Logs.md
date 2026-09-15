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

# Azure Monitor Logs

## O que é?

Logs são registros estruturados de eventos que aconteceram em um sistema — cada entrada tipicamente carrega contexto rico (timestamp, origem, mensagem, propriedades adicionais) sobre um evento específico, em vez de apenas um número.

## Modelo

```
Application
     ↓
Logs
     ↓
Log Storage
     ↓
Query
     ↓
Analysis
```

Logs são armazenados de forma que possam ser buscados e analisados posteriormente — no ecossistema Azure Monitor, esse armazenamento e análise acontece tipicamente através de um [[Log Analytics Workspace]].

## Características

- **Eventos**: cada log representa algo que aconteceu em um momento específico (uma requisição, uma exceção, uma mudança de configuração).
- **Contexto**: logs carregam mais informação por entrada do que uma métrica (mensagens, stack traces, identificadores).
- **Busca e correlação**: logs são projetados para serem consultados (ex.: "todas as requisições que falharam com erro X na última hora") e correlacionados entre si (ver [[Correlation]]).

## Escopo desta nota

A linguagem de consulta usada para analisar logs no Azure (KQL — Kusto Query Language) está aprofundada em [[Kusto Query Language]] e nas notas relacionadas em [[Log Analytics]].

## Relações

- [[Logs vs Metrics]]
- [[Log Analytics Workspace]]
- [[Resource Logs]]
- [[Azure Activity Log]]
- [[Log Analytics]]

## Referências

- Microsoft Learn — "Logs in Azure Monitor": https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-platform-logs
