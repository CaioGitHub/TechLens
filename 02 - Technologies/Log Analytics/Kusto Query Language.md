---
type: concept
status: learning
confidence: 45
created: 2026-09-09
updated: 2026-09-09
tags:
  - log-analytics
  - kql
---

# Kusto Query Language

## O que é

Kusto Query Language (KQL) é a linguagem de consulta usada para explorar e analisar dados armazenados em um [[Log Analytics Workspace]] — incluindo [[Azure Monitor Logs]] e a telemetria coletada pelo [[Application Insights]].

## KQL não é "SQL do Azure"

```
SQL
    ↓
Relational queries

KQL
    ↓
Data exploration / analytics / telemetry
```

SQL foi desenhado para manipular dados relacionais (inserir, atualizar, relacionar tabelas normalizadas). KQL foi desenhado para **explorar** grandes volumes de dados semi-estruturados de telemetria — logs, eventos, métricas — de forma rápida e legível, priorizando análise e agregação sobre transações. A comparação com SQL ajuda apenas como ponto de partida mental (ambos usam algo parecido com tabelas e produzem resultados tabulares); tratá-las como equivalentes leva a erros — ver o anti-pattern "usar KQL como SQL" em [[KQL Anti-Patterns]].

## Onde o KQL se encaixa

```
Application / Azure Resource
          ↓
       Telemetry
          ↓
      Azure Monitor
          ↓
   Azure Monitor Logs
          ↓
   Log Analytics Workspace
          ↓
          KQL
          ↓
      Analysis
          ↓
   Troubleshooting
```

KQL é a ferramenta de consulta; o Log Analytics Workspace é onde os dados residem. KQL não é o armazenamento, e o Workspace não é a linguagem — ver a distinção completa em [[Log Analytics]].

## Como uma query é estruturada

Uma query KQL é um **pipeline**: começa por uma tabela e encadeia operações através do operador `|` (pipe) — ver [[KQL Query Pipeline]].

## Relações

- [[Log Analytics]]
- [[Log Analytics Workspace]]
- [[KQL Query Pipeline]]
- [[Azure Monitor Logs]]

## Referências

- Microsoft Learn — "Kusto Query Language overview": https://learn.microsoft.com/en-us/kusto/query/?view=microsoft-fabric
- Microsoft Learn — "KQL quick reference": https://learn.microsoft.com/en-us/azure/data-explorer/kql-quick-reference
