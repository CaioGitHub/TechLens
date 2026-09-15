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

# Trace Telemetry

## O que representa

Trace Telemetry (no contexto do Application Insights) representa uma mensagem de diagnóstico/log emitida deliberadamente pelo código da aplicação — diferente de um [[Azure Monitor Traces|trace distribuído]], que é o caminho de uma operação através de componentes.

> Nota de nomenclatura: "trace" é usado com dois sentidos relacionados mas distintos no ecossistema Azure Monitor — (1) Trace Telemetry, um item de log de aplicação; (2) distributed trace, o caminho fim-a-fim de uma operação (ver [[Distributed Tracing]]). Um distributed trace é composto por vários spans, e cada span pode conter, entre outras coisas, itens de Trace Telemetry como contexto adicional.

## Diferenciando os tipos de telemetria

| Tipo | O que captura |
|---|---|
| [[Request Telemetry\|Request]] | uma requisição recebida |
| [[Dependency Telemetry\|Dependency]] | uma chamada feita para fora |
| [[Exception Telemetry\|Exception]] | uma falha lançada pelo código |
| [[Azure Monitor Metrics\|Metric]] | um valor numérico agregado no tempo |
| Trace | uma mensagem de diagnóstico com contexto |

## Para que serve

Um Trace Telemetry fornece contexto textual que complementa os demais sinais — por exemplo, uma mensagem de log logo antes de uma exceção, indicando o estado da aplicação naquele momento. Ele não substitui Request, Dependency ou Exception; adiciona narrativa entre eles.

## Escopo desta nota

Esta nota trata do conceito de Trace Telemetry como item de dado. A consulta desses dados via linguagem de consulta (KQL) é aprofundada na Etapa 9 — Log Analytics + KQL; aqui, o objetivo é entender **o que** é coletado, não **como consultar**.

## Relações

- [[Application Telemetry]]
- [[Azure Monitor Traces]]
- [[Distributed Tracing]]
- [[Exception Telemetry]]

## Referências

- Microsoft Learn — "Application Insights telemetry data model — Traces": https://learn.microsoft.com/en-us/azure/azure-monitor/app/data-model-trace-telemetry
