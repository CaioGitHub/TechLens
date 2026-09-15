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

# Instrumentation

## O que é

Instrumentação é o processo de fazer uma aplicação emitir telemetria — sem instrumentação, não existe [[Application Telemetry]] para o [[Application Insights]] coletar.

## Automatic Instrumentation

A aplicação recebe instrumentação sem que o código precise ser manualmente alterado — tipicamente via um agente Java (ver [[Azure Monitor OpenTelemetry]]) anexado no start da JVM, que intercepta bibliotecas conhecidas (servlets, clientes HTTP, JDBC) e gera telemetria automaticamente.

**Vantagens**: adoção rápida, sem alterar código-fonte, cobertura ampla de bibliotecas comuns.
**Desvantagens**: menos controle sobre o que é capturado; telemetria de lógica de negócio específica (ver [[Application Telemetry#Custom Telemetry|Custom Telemetry]]) ainda exige código manual.

## Manual Instrumentation

O desenvolvedor adiciona instrumentação explicitamente no código — por exemplo, emitindo um evento customizado ao concluir um processo de negócio, ou criando um span manual em torno de uma operação específica.

**Vantagens**: controle total, telemetria com significado de negócio explícito.
**Desvantagens**: exige esforço, manutenção contínua, e risco de instrumentação inconsistente entre partes do código.

## Nenhuma abordagem é universalmente superior

Automatic e manual instrumentation não são mutuamente exclusivas — a prática comum é usar automatic instrumentation como base (cobertura ampla e imediata) e complementar com manual instrumentation apenas onde há necessidade real de contexto de negócio adicional.

## Relações

- [[Azure Monitor OpenTelemetry]]
- [[Application Telemetry]]
- [[Java Spring Boot Application Insights]]

## Referências

- Microsoft Learn — "Configure Azure Monitor Application Insights for Java": https://learn.microsoft.com/en-us/azure/azure-monitor/app/java-standalone-config
