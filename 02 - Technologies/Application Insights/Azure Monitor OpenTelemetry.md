---
type: concept
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - application-insights
  - observability
---

# Azure Monitor OpenTelemetry

## O que é OpenTelemetry

OpenTelemetry (OTel) é um padrão aberto e vendor-neutral para instrumentação, coleta e exportação de telemetria (traces, metrics, logs) — mantido pela CNCF, com implementações em múltiplas linguagens, incluindo Java.

## Por que ele existe

Antes do OpenTelemetry, cada fornecedor de observabilidade (incluindo o Application Insights) tinha seu próprio SDK proprietário de instrumentação. Isso significava reescrever instrumentação ao trocar de fornecedor. OpenTelemetry padroniza como a telemetria é gerada e propagada, permitindo trocar o destino (exporter) sem reescrever a instrumentação da aplicação.

## Relação atual entre Application Insights, Azure Monitor e OpenTelemetry

O Azure Monitor migrou sua estratégia de instrumentação para se basear em OpenTelemetry. O componente recomendado atualmente para Java é o **Azure Monitor OpenTelemetry Distro** — um agente Java que:

- instrumenta automaticamente bibliotecas comuns (servlets, clientes HTTP, JDBC) usando os instrumentadores do ecossistema OpenTelemetry;
- exporta a telemetria coletada para o Application Insights, adaptando os conceitos do OTel (traces, spans, metrics, logs) ao modelo de dados do Application Insights (requests, dependencies, exceptions, traces).

```
Aplicação Java
      ↓
OpenTelemetry (instrumentation + SDK)
      ↓
Azure Monitor OpenTelemetry Distro (exporter)
      ↓
Application Insights
```

O SDK clássico do Application Insights (pré-OpenTelemetry) ainda existe, mas o caminho recomendado para novas aplicações é a distro baseada em OpenTelemetry — não se deve misturar os dois mecanismos na mesma aplicação.

## Escopo desta nota

Esta é uma introdução conceitual ao papel do OpenTelemetry no ecossistema Azure Monitor/Application Insights. Aprofundamento em OTel SDK, Collector, exporters customizados e propagação de contexto avançada não pertence a esta etapa.

## Relações

- [[Instrumentation]]
- [[Distributed Tracing]]
- [[Java Spring Boot Application Insights]]

## Referências

- Microsoft Learn — "Azure Monitor OpenTelemetry overview": https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-overview
- Microsoft Learn — "Migrate to OpenTelemetry": https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-migration
