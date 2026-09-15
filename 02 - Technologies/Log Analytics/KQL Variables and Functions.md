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

# KQL Variables and Functions

## `let` — variáveis de query

```kql
let timeRange = 1h;
AppRequests
| where TimeGenerated > ago(timeRange)
```

`let` declara um valor (ou até uma sub-query reutilizável) nomeado, usado no restante da query. Benefícios:

- **legibilidade** — `ago(timeRange)` comunica intenção melhor do que um valor mágico repetido;
- **reutilização** — o mesmo valor pode ser usado em múltiplos pontos da query sem repetição;
- **manutenção** — alterar a janela de tempo (ou outro parâmetro) em um único lugar.

```kql
let threshold = 1000;
AppRequests
| where DurationMs > threshold
| summarize count() by Name
```

## Funções

- **Funções embutidas** — parte da linguagem, sempre disponíveis (`ago()`, `count()`, `avg()`, `tostring()`, `bin()` etc.) — a grande maioria do uso prático de KQL se apoia nelas.
- **Funções definidas pelo usuário** — é possível declarar uma função reutilizável com `let nome = (parametros) { ... };`, similar a uma sub-rotina, para lógica repetida entre queries.

Esta base não aprofunda a criação de funções definidas pelo usuário — na prática, a maior parte do troubleshooting do dia a dia é resolvida com funções embutidas combinadas a `let` para parâmetros simples.

## Relações

- [[Kusto Query Language]]
- [[KQL Filtering]]
- [[KQL Query Performance]]

## Referências

- Microsoft Learn — "let statement": https://learn.microsoft.com/en-us/kusto/query/let-statement?view=microsoft-fabric
- Microsoft Learn — "User-defined functions": https://learn.microsoft.com/en-us/kusto/query/functions/user-defined-functions?view=microsoft-fabric
