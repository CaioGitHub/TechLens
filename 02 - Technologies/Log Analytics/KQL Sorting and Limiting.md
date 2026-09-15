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

# KQL Sorting and Limiting

## `order by`

```kql
AppRequests
| order by TimeGenerated desc
```

Ordena o resultado — `desc` (mais recente primeiro) é comum ao investigar eventos recentes; `asc` é útil ao construir uma série temporal (ver [[KQL Aggregation]]). `order by` normalmente faz mais sentido **depois** de filtrar e agregar — ordenar um volume grande de dados brutos antes de reduzi-lo é desperdício de processamento.

## `take`

```kql
AppRequests
| take 20
```

`take` (equivalente a `limit`) retorna um número fixo de linhas, sem garantia de ordem específica. É a ferramenta certa para uma **exploração inicial**: entender rapidamente que colunas uma tabela tem e como os dados se parecem, antes de construir uma query mais elaborada com filtros e agregações. Não deve ser confundido com uma amostra estatisticamente representativa — ver o anti-pattern "concluir com poucos dados" em [[KQL Anti-Patterns]].

## `distinct`

```kql
AppRequests
| distinct Name
```

Responde perguntas como "quais endpoints apareceram nos dados?" ou "quais valores de ResultCode existem?" — útil para entender a variedade de valores de uma coluna antes de decidir como filtrar ou agrupar por ela.

```kql
AppRequests
| distinct ResultCode
```

## Ordem recomendada de uso

```
take (exploração)
   ↓
distinct (entender valores possíveis)
   ↓
where (filtrar)
   ↓
summarize (agregar)
   ↓
order by (apresentar)
```

## Relações

- [[Kusto Query Language]]
- [[KQL Filtering]]
- [[KQL Aggregation]]

## Referências

- Microsoft Learn — "take operator": https://learn.microsoft.com/en-us/kusto/query/take-operator?view=microsoft-fabric
- Microsoft Learn — "distinct operator": https://learn.microsoft.com/en-us/kusto/query/distinct-operator?view=microsoft-fabric
- Microsoft Learn — "sort/order operator": https://learn.microsoft.com/en-us/kusto/query/order-operator?view=microsoft-fabric
