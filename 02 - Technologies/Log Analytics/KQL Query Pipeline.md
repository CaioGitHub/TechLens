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

# KQL Query Pipeline

## Anatomia de uma query

```
Table
| operator
| operator
| operator
```

Exemplo:

```kql
AppRequests
| where Success == false
| project TimeGenerated, Name, ResultCode, DurationMs
| order by TimeGenerated desc
```

## Leitura como pipeline

```
AppRequests
   ↓
where
   ↓
project
   ↓
order by
```

Cada linha recebe o resultado tabular da linha anterior e o transforma — filtra, seleciona colunas, ordena, agrega. O resultado final é o que sobra depois de toda a cadeia de transformações.

## O operador pipe `|`

```
Tabela
  ↓
Filtro
  ↓
Transformação
  ↓
Agregação
  ↓
Resultado
```

`|` compõe operações: o resultado de cada operador se torna a entrada do próximo. Não existe uma ordem obrigatória única para todos os casos, mas há uma ordem que tende a ser mais eficiente — filtrar (`where`) o quanto antes, antes de projetar ou agregar, reduz o volume de dados processado nas etapas seguintes (ver [[KQL Query Performance]]).

## Nota sobre nomenclatura de colunas

Os exemplos desta base usam nomes de coluna **PascalCase das tabelas workspace-based** do Application Insights (ex.: `AppRequests`) — como `TimeGenerated` (não `Timestamp`), `Success`, `ResultCode`, `DurationMs` (não `Duration`) e `OperationId`. Recursos clássicos (não baseados em workspace) usam nomes em camelCase em tabelas como `requests`, com colunas como `timestamp`, `success`, `resultCode` e `duration`. Ver [[Application Insights Tables]] para a distinção completa — a nomenclatura exata das colunas muda entre os dois modelos, não apenas o estilo de capitalização.

## Relações

- [[Kusto Query Language]]
- [[KQL Filtering]]
- [[KQL Projection]]
- [[KQL Aggregation]]
- [[Application Insights Tables]]

## Referências

- Microsoft Learn — "KQL tutorial": https://learn.microsoft.com/en-us/kusto/query/tutorials/learn-common-operators?view=microsoft-fabric
