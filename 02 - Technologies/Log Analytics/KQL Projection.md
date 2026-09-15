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

# KQL Projection

## `project` — selecionar colunas relevantes

```kql
AppRequests
| project TimeGenerated, Name, DurationMs, ResultCode, Success
```

`project` reduz o resultado às colunas que interessam para a investigação atual. Isso facilita a leitura do resultado e reduz o volume de dados transferido/processado nas etapas seguintes do pipeline.

## `project-away` — remover colunas específicas

```kql
AppRequests
| project-away ClientIP, Properties
```

Útil quando a maioria das colunas é relevante e apenas algumas poucas (por exemplo, contendo dados sensíveis ou irrelevantes) precisam ser excluídas — o inverso de `project`.

## `extend` — criar colunas derivadas

```kql
AppRequests
| extend DurationSeconds = DurationMs / 1000.0
```

`extend` adiciona uma nova coluna calculada a partir de colunas existentes, sem remover as originais. Comum para conversões de unidade (ms → s), extração de partes de uma string, ou cálculos simples usados em etapas seguintes do pipeline (ex.: em um `summarize`).

## Quando usar cada um

- **project**: já sei exatamente quais colunas quero ver.
- **project-away**: quero quase tudo, exceto algumas colunas.
- **extend**: preciso de uma coluna nova, calculada, mantendo as demais.

## Relações

- [[Kusto Query Language]]
- [[KQL Query Pipeline]]
- [[KQL Aggregation]]
- [[Application Insights Tables]]

## Referências

- Microsoft Learn — "project operator": https://learn.microsoft.com/en-us/kusto/query/project-operator?view=microsoft-fabric
- Microsoft Learn — "extend operator": https://learn.microsoft.com/en-us/kusto/query/extend-operator?view=microsoft-fabric
