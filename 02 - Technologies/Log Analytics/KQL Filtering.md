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

# KQL Filtering

## `where`

`where` filtra linhas com base em uma condição — o operador mais usado em KQL.

```kql
AppRequests
| where Success == false
```

```kql
AppRequests
| where DurationMs > 1000
```

```kql
AppExceptions
| where TimeGenerated > ago(1h)
```

Suporta combinação lógica:

```kql
AppRequests
| where Success == false and DurationMs > 1000
```

- `and`, `or`, `not` combinam condições.
- comparações numéricas (`>`, `<`, `>=`, `<=`, `==`, `!=`) funcionam como esperado para `int`, `long`, `real`, `datetime`.
- strings têm operadores próprios — ver seção abaixo.

## Time filtering — a primeira coisa a decidir

```kql
| where TimeGenerated > ago(1h)
```

```kql
| where TimeGenerated between (datetime(2026-09-08T14:00:00Z) .. datetime(2026-09-08T15:00:00Z))
```

Consultas sem limite temporal podem: variar de custosas a lentas, processar muito mais dados do que o necessário, e produzir resultados difíceis de interpretar (uma mistura de eventos de dias diferentes). **Boa prática**: comece com uma janela temporal pequena (ex.: última hora) e amplie apenas se necessário — ver [[KQL Query Performance]].

## Strings

| Operador | Comportamento |
|---|---|
| `==` | igualdade exata (case-sensitive) |
| `has` | contém a palavra completa (indexado, mais eficiente) |
| `contains` | contém a substring em qualquer posição (não exige palavra completa) |
| `startswith` | começa com |
| `endswith` | termina com |

`has` é preferível a `contains` quando se busca uma palavra inteira, porque é otimizado internamente pelo motor de indexação do Kusto — `contains` faz uma busca de substring mais genérica e tende a ser mais custosa em tabelas grandes.

```kql
AppTraces
| where Message has "timeout"
```

## Booleanos e nulos

```kql
AppRequests
| where isnotnull(ResultCode)
```

- `true` / `false` — valores booleanos diretos (ex.: `Success == true`).
- `isnull(x)` / `isnotnull(x)` — testam explicitamente a ausência de valor; comparar diretamente com `== null` nem sempre se comporta como esperado, por isso as funções dedicadas são preferidas.

## Relações

- [[Kusto Query Language]]
- [[KQL Query Pipeline]]
- [[KQL Query Performance]]
- [[Application Insights Tables]]

## Referências

- Microsoft Learn — "where operator": https://learn.microsoft.com/en-us/kusto/query/where-operator?view=microsoft-fabric
- Microsoft Learn — "datetime/timespan arithmetic": https://learn.microsoft.com/en-us/kusto/query/scalar-data-types/datetime?view=microsoft-fabric
