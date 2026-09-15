---
type: study
status: learning
confidence: 40
created: 2026-09-09
updated: 2026-09-09
tags:
  - log-analytics
  - kql
  - exercises
---

# KQL Exercises

Exercícios progressivos para praticar KQL sobre dados de Application Insights (tabelas workspace-based — ver [[Application Insights Tables]]).

## Nível 1 — Exploração

```kql
AppRequests
| take 20
```

```kql
AppExceptions
| take 20
```

```kql
AppDependencies
| take 20
```

```kql
AppRequests
| order by TimeGenerated desc
| take 20
```

Objetivo: entender o schema e o formato dos dados antes de qualquer filtro — ver [[KQL Sorting and Limiting]].

## Nível 2 — Filtros

```kql
AppRequests
| where ResultCode == "500"
```

```kql
AppRequests
| where DurationMs > 1000
```

```kql
AppExceptions
| where TimeGenerated > ago(1h)
```

```kql
AppDependencies
| where Success == false
```

Objetivo: isolar eventos relevantes — ver [[KQL Filtering]].

## Nível 3 — Agregações

```kql
AppRequests
| summarize count()
```

```kql
AppRequests
| summarize FailedCount = countif(Success == false)
```

```kql
AppRequests
| summarize avg(DurationMs), percentile(DurationMs, 95)
```

```kql
AppRequests
| summarize count() by Name
```

```kql
AppRequests
| summarize count() by ResultCode
```

Objetivo: transformar eventos individuais em respostas agregadas — ver [[KQL Aggregation]].

## Nível 4 — Tempo

```kql
AppRequests
| where Success == false
| summarize FailedCount = count() by bin(TimeGenerated, 1m)
| order by TimeGenerated asc
```

```kql
AppRequests
| summarize percentile(DurationMs, 95) by bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```

Compare dois períodos (antes/depois de um deploy, por exemplo) filtrando cada um separadamente e comparando os agregados.

Objetivo: identificar quando um comportamento mudou, não apenas que ele mudou.

## Nível 5 — Correlação

```kql
AppRequests
| where Success == false
| join kind=inner (AppExceptions) on OperationId
```

```kql
AppRequests
| where OperationId == "<um OperationId específico>"
| join kind=leftouter (AppDependencies) on OperationId
```

```kql
let opId = "<um OperationId específico>";
union AppRequests, AppDependencies, AppExceptions, AppTraces
| where OperationId == opId
| order by TimeGenerated asc
```

Objetivo: seguir uma operação através de múltiplos sinais — ver [[KQL Join and Union]] e [[Correlation]].

## Nível 6 — Incidente

Sem receber a query pronta: investigue um cenário como "a API começou a retornar erros e ficou lenta às 14:32" seguindo o processo completo descrito em [[Log Analytics Troubleshooting with KQL]] (Cenário 8) — definir a pergunta, limitar o período, filtrar, explorar, agregar, correlacionar, formular e validar uma hipótese.

## Relações

- [[Kusto Query Language]]
- [[Log Analytics Troubleshooting with KQL]]
- [[Application Insights Tables]]
