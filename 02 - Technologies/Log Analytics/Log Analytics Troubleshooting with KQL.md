---
type: troubleshooting
status: learning
confidence: 45
created: 2026-09-09
updated: 2026-09-09
tags:
  - log-analytics
  - kql
  - troubleshooting
---

# Log Analytics Troubleshooting with KQL

## Modelo geral

```
Problema
   ↓
Pergunta
   ↓
Tabela
   ↓
KQL
   ↓
Evidência
   ↓
Correlação
   ↓
Hipótese
   ↓
Validação
   ↓
Conclusão
```

A meta não é decorar queries prontas, mas construir a investigação progressivamente: começar simples, validar, adicionar complexidade.

## Cenário 1 — HTTP 500

**Pergunta**: Quais requests estão retornando HTTP 500?

```kql
AppRequests
| where ResultCode == "500"
```

Refinar:

```kql
AppRequests
| where ResultCode == "500"
| project TimeGenerated, Name, DurationMs, ResultCode
| order by TimeGenerated desc
```

Depois, seguir a cadeia (ver [[Application Insights Troubleshooting]]):

```
Request
↓
Exception
↓
Trace
↓
Dependency
```

```kql
AppRequests
| where ResultCode == "500"
| join kind=inner (AppExceptions) on OperationId
| project TimeGenerated, Name, ExceptionType, ExceptionMessage = OuterMessage
```

## Cenário 2 — Error Rate aumentou?

**Pergunta**: A taxa de erros aumentou?

Raciocínio:

```
Total Requests
        ↓
Failed Requests
        ↓
Error Rate
        ↓
Time Series
```

```kql
AppRequests
| summarize Total = count(), Failed = countif(Success == false) by bin(TimeGenerated, 5m)
| extend ErrorRate = todouble(Failed) / Total
| order by TimeGenerated asc
```

Ver a série temporal (em vez de um único número agregado) é o que permite identificar **quando** o problema começou, não apenas que ele existe.

## Cenário 3 — A API ficou lenta?

**Pergunta**: A API ficou lenta?

```
Requests
   ↓
DurationMs
   ↓
Percentiles
   ↓
Time
```

```kql
AppRequests
| summarize avg(DurationMs), percentile(DurationMs, 95), percentile(DurationMs, 99) by bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```

`avg` sozinho pode esconder outliers (ver [[KQL Aggregation]]) — por isso p95/p99 são incluídos: eles revelam se uma parcela relevante dos usuários teve experiência muito pior que a média sugere.

## Cenário 4 — Qual endpoint está mais lento?

**Pergunta**: Qual endpoint está apresentando maior latência?

```
Endpoint
   ↓
Request Count
   ↓
Average DurationMs
   ↓
Percentile
```

```kql
AppRequests
| summarize RequestCount = count(), AvgDuration = avg(DurationMs), P95Duration = percentile(DurationMs, 95) by Name
| order by P95Duration desc
```

Cuidado: um endpoint com poucas requisições pode aparecer com p95 alto apenas por baixa amostragem — validar `RequestCount` antes de tirar conclusões (ver [[KQL Anti-Patterns]]).

## Cenário 5 — Qual dependência está causando lentidão?

**Pergunta**: Qual dependência está causando lentidão?

```
Request
   ↓
Dependency
   ↓
DurationMs
   ↓
Target
```

```kql
AppDependencies
| summarize AvgDuration = avg(DurationMs), P95Duration = percentile(DurationMs, 95) by Target, DependencyType
| order by P95Duration desc
```

Investigar se o alvo (`Target`) é um banco de dados, uma API externa, um cache ou um message broker ajuda a direcionar a investigação para o componente correto.

## Cenário 6 — Quais exceções ocorreram?

**Pergunta**: Quais exceções ocorreram durante o incidente?

```
Exceptions
   ↓
Type
   ↓
Message
   ↓
TimeGenerated
   ↓
Operation
```

```kql
AppExceptions
| where TimeGenerated > ago(1h)
| summarize count() by ExceptionType, OuterMessage
| order by count_ desc
```

Depois, correlacionar com requests da mesma operação usando `OperationId` (ver [[KQL Join and Union]]).

## Cenário 7 — Correlação: o que aconteceu nesta operação específica?

```
Request
   ↓
Trace / Operation
   ↓
Dependency
   ↓
Exception
```

```kql
let opId = "abc123";
union AppRequests, AppDependencies, AppExceptions, AppTraces
| where OperationId == opId
| order by TimeGenerated asc
```

Usar `union` sobre as quatro tabelas, filtrando por um único `OperationId`, reconstrói a linha do tempo completa de uma operação específica — a essência da correlação aplicada na prática.

## Cenário 8 — Incidente completo

**Situação**: a API começou a retornar erros e ficou lenta às 14:32.

Processo de investigação (sem pular etapas):

```
14:32
↓
Requests (volume e status ao redor do horário)
↓
Error Rate (aumentou exatamente nesse período?)
↓
Latency (p95/p99 também subiram?)
↓
Exceptions (quais tipos apareceram a partir desse horário?)
↓
Dependencies (alguma dependência específica degradou junto?)
↓
Trace / Correlation (seguir uma operação afetada específica)
↓
Root Cause (hipótese apoiada em evidência, não suposição)
```

Passo a passo conceitual:

1. Limitar o período ao redor de 14:32 (`where TimeGenerated between (...)`).
2. Verificar volume e taxa de erro (`summarize ... by bin(TimeGenerated, 1m)`).
3. Verificar se a latência (p95/p99) também subiu no mesmo período.
4. Listar exceções que começaram a partir daquele horário.
5. Verificar dependências correlacionadas às requisições afetadas.
6. Escolher uma operação específica (`OperationId`) e reconstruir sua linha do tempo completa.
7. Só então formular e validar uma hipótese de causa raiz.

## Relações

- [[Kusto Query Language]]
- [[Application Insights Tables]]
- [[Application Insights Troubleshooting]]
- [[Azure Monitor Troubleshooting]]
- [[Correlation]]

## Referências

- Microsoft Learn — "Log queries in Azure Monitor": https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-query-overview
