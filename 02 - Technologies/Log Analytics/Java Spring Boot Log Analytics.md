---
type: architecture
status: learning
confidence: 45
created: 2026-09-09
updated: 2026-09-09
tags:
  - log-analytics
  - kql
  - spring
  - hexagonal-architecture
---

# Java Spring Boot Log Analytics

## Cadeia completa

```
Spring Boot
    ↓
Telemetry
    ↓
Application Insights
    ↓
Azure Monitor Logs
    ↓
Log Analytics
    ↓
KQL
    ↓
Troubleshooting
```

Uma aplicação Java 21 + Spring Boot instrumentada (ver [[Java Spring Boot Application Insights]]) gera [[Application Telemetry]] que acaba, em última instância, armazenada como linhas em tabelas de um [[Log Analytics Workspace]] — e é KQL que permite transformar esses dados brutos em respostas.

## Exemplo contextualizado

```
GET /orders/{id}
      ↓
Controller
      ↓
Use Case
      ↓
Repository Port
      ↓
Database Adapter
```

Cada camada dessa cadeia [[Hexagonal Architecture|hexagonal]] pode contribuir telemetria correlacionada pelo mesmo `OperationId`: o `Controller` gera a `AppRequests`, o `Database Adapter` gera a `AppDependencies` correspondente. Perguntas que essa telemetria permite responder via KQL:

- **Quais endpoints falharam?** → `AppRequests | where Success == false | summarize count() by Name`
- **Qual endpoint está lento?** → agrupar `AppRequests` por `Name`, comparar `percentile(DurationMs, 95)` (ver [[Log Analytics Troubleshooting with KQL]]).
- **Quais dependências estão lentas?** → `AppDependencies` agrupado por `Target`.
- **Quais exceções ocorreram?** → `AppExceptions` no período do incidente.
- **Quando o problema começou?** → `summarize ... by bin(TimeGenerated, 1m)` para localizar a mudança de comportamento.
- **Qual operação foi afetada?** → filtrar por `OperationId` específico e reconstruir a linha do tempo com `union`.

## Observabilidade continua transversal

KQL é uma ferramenta de **consulta** sobre dados já coletados — ela não introduz nenhuma dependência de código na aplicação, muito menos no [[Domain]]. A cadeia observada é:

```
Hexagonal Application
        ↓
Telemetry
        ↓
Application Insights
        ↓
KQL
        ↓
Investigation
```

KQL opera inteiramente fora da aplicação, sobre dados já exportados — não é, e não deve ser tratado como, uma dependência arquitetural da aplicação (ver [[Hexagonal Architecture + Application Insights]] e [[Hexagonal Architecture + Observability]]).

## Relações

- [[Java Spring Boot Application Insights]]
- [[Hexagonal Architecture + Application Insights]]
- [[Application Insights Tables]]
- [[Log Analytics Troubleshooting with KQL]]

## Referências

- Microsoft Learn — "Log queries in Azure Monitor": https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-query-overview
