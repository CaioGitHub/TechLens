---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - application-insights
  - observability
---

# Exception Telemetry

## O que representa

Exception Telemetry captura exceções lançadas durante o processamento de uma operação — tratadas ou não tratadas — junto com stack trace e o contexto da operação em que ocorreram.

## Um HTTP 500 é sintoma, não causa raiz

```
HTTP 500
   ↓
Exception
   ↓
Trace
   ↓
Dependency
   ↓
Root Cause
```

Um status HTTP 500 informa que algo falhou, mas não explica **por quê**. A Exception Telemetry é o próximo passo da investigação: qual exceção foi lançada, em qual ponto do código, com qual mensagem e stack trace. A partir daí, [[Trace Telemetry|traces]] de aplicação e [[Dependency Telemetry|dependências]] envolvidas ajudam a chegar à causa raiz — que pode estar na própria aplicação ou em uma dependência externa.

## Exceções tratadas vs não tratadas

- **Não tratadas**: propagam até o topo da pilha, tipicamente resultando em uma resposta de erro ao usuário (ex.: HTTP 500).
- **Tratadas**: capturadas e tratadas pelo código (ex.: convertidas em uma resposta de erro específica), mas ainda podem valer a pena registrar como telemetria — frequência de exceções tratadas pode indicar um problema recorrente mesmo que a aplicação "lide" com ele.

## Frequência de exceções

Acompanhar a **frequência** de um tipo de exceção ao longo do tempo (não apenas sua ocorrência isolada) ajuda a distinguir um evento raro de uma regressão real após um deploy, por exemplo.

## Relações

- [[Application Telemetry]]
- [[Request Telemetry]]
- [[Trace Telemetry]]
- [[Application Insights Troubleshooting]]

## Referências

- Microsoft Learn — "Application Insights telemetry data model — Exceptions": https://learn.microsoft.com/en-us/azure/azure-monitor/app/data-model-exception-telemetry
