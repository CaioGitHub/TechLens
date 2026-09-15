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

# KQL Aggregation

## `summarize` — o operador mais importante para análise

```kql
AppRequests
| summarize count()
```

Conta o total de linhas. Fica mais interessante ao agrupar:

```kql
AppRequests
| summarize count() by ResultCode
```

Isso responde "quantas requisições existem para cada código de resultado?" — uma pergunta agregada, não um evento individual.

## Funções de agregação comuns

- `count()` — quantidade de linhas.
- `avg(coluna)` — média.
- `min(coluna)` / `max(coluna)` — valores extremos.
- `sum(coluna)` — soma.
- `percentile(coluna, N)` — valor abaixo do qual N% das observações caem (ex.: `percentile(DurationMs, 95)` é o P95).

### Por que percentis importam

Uma média (`avg`) pode esconder outliers: se 95 requisições levam 100ms e 5 levam 10 segundos, a média ainda parece razoável, mas uma parcela relevante dos usuários teve uma experiência muito pior. `percentile(DurationMs, 95)` ou `percentile(DurationMs, 99)` revela a "cauda" da distribuição — ver o anti-pattern "confundir média com realidade" em [[KQL Anti-Patterns]].

```kql
AppRequests
| summarize avg(DurationMs), percentile(DurationMs, 95), percentile(DurationMs, 99) by Name
```

## `bin` — agrupamento temporal

```kql
AppRequests
| summarize count() by bin(TimeGenerated, 5m)
```

```
Eventos
   ↓
Tempo
   ↓
Buckets
   ↓
Trend
```

`bin(TimeGenerated, 5m)` agrupa os timestamps em intervalos fixos de 5 minutos, permitindo enxergar uma série temporal — essencial para investigar taxa de erro ao longo do tempo, volume de requisições por período, ou latência por janela, em vez de um número único agregando todo o período consultado.

```kql
AppRequests
| where Success == false
| summarize FailedCount = count() by bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```

## Relações

- [[Kusto Query Language]]
- [[KQL Projection]]
- [[KQL Sorting and Limiting]]
- [[Log Analytics Troubleshooting with KQL]]

## Referências

- Microsoft Learn — "summarize operator": https://learn.microsoft.com/en-us/kusto/query/summarize-operator?view=microsoft-fabric
- Microsoft Learn — "bin() function": https://learn.microsoft.com/en-us/kusto/query/bin-function?view=microsoft-fabric
- Microsoft Learn — "percentile() function": https://learn.microsoft.com/en-us/kusto/query/percentiles-aggregate-function?view=microsoft-fabric
