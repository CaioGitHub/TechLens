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

# Application Insights Tables

## Tabelas atuais (workspace-based) vs clássicas

Recursos Application Insights atuais são **workspace-based** (armazenados em um [[Log Analytics Workspace]] — ver [[Application Insights]]). Nesse modelo, cada tipo de telemetria vive em uma tabela com prefixo `App`, em PascalCase. Recursos clássicos (em retirada) usam tabelas com nomes antigos, em camelCase.

| Telemetria | Tabela atual (workspace-based) | Tabela clássica (legado) |
|---|---|---|
| [[Request Telemetry\|Requests]] | `AppRequests` | `requests` |
| [[Dependency Telemetry\|Dependencies]] | `AppDependencies` | `dependencies` |
| [[Exception Telemetry\|Exceptions]] | `AppExceptions` | `exceptions` |
| [[Trace Telemetry\|Traces]] | `AppTraces` | `traces` |
| Availability | `AppAvailabilityResults` | `availabilityResults` |
| Custom Events | `AppEvents` | `customEvents` |
| Custom Metrics | `AppMetrics` | `customMetrics` |
| Page Views | `AppPageViews` | `pageViews` |
| Performance Counters | `AppPerformanceCounters` | `performanceCounters` |

Esta base usa os nomes de tabela e coluna **workspace-based** (atuais) em seus exemplos.

## Colunas comuns em `AppRequests`

```
AppRequests
├── TimeGenerated
├── Name
├── Url
├── ResultCode
├── Success
├── DurationMs
├── OperationId
└── Properties
```

- **TimeGenerated** — quando a requisição ocorreu.
- **Name** — nome da operação (ex.: rota/endpoint).
- **ResultCode** — código retornado (ex.: status HTTP).
- **Success** — booleano indicando sucesso/falha.
- **DurationMs** — duração em milissegundos.
- **OperationId** — identificador que permite correlacionar esta request com dependencies/exceptions/traces da mesma operação (ver [[Correlation]]).

`AppDependencies` e `AppExceptions` seguem uma estrutura semelhante, com colunas específicas (ex.: `Target`, `DependencyType` para dependencies; `ExceptionType`, `Message`, `OuterMessage` para exceptions). Note que ambas as tabelas também têm uma coluna genérica chamada `Type`, herdada de todas as tabelas do Azure Monitor Logs — ela contém apenas o nome da tabela (ex.: `"AppDependencies"`) e não deve ser confundida com `DependencyType` ou `ExceptionType`.

## O schema varia

O conjunto exato de colunas disponível depende do tipo de telemetria, da versão do agente/SDK de instrumentação, e de eventuais propriedades customizadas adicionadas via [[Application Telemetry#Custom Telemetry|Custom Telemetry]]. Antes de escrever uma query em um ambiente real, é recomendável explorar o schema com `| take 20` (ver [[KQL Sorting and Limiting]]) em vez de assumir colunas de memória.

## Relações

- [[Application Insights]]
- [[Application Telemetry]]
- [[Log Analytics Workspace]]
- [[KQL Query Pipeline]]

## Referências

- Microsoft Learn — "Azure Monitor Application Insights table reference": https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/apprequests
- Microsoft Learn — "Convert to workspace-based Application Insights": https://learn.microsoft.com/en-us/azure/azure-monitor/app/convert-classic-resource
