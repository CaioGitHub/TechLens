---
type: architecture
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - application-insights
  - spring
---

# Java Spring Boot Application Insights

## Cadeia completa

```
Java 21
   ↓
Spring Boot
   ↓
Application
   ↓
Instrumentation
   ↓
Requests / Dependencies / Exceptions / Traces
   ↓
Application Insights
   ↓
Azure Monitor
```

## Como instrumentar (visão atual)

O caminho recomendado atualmente para Java é o **Azure Monitor OpenTelemetry Distro** (Java Agent) — anexado à JVM no momento da inicialização, sem exigir alteração de código para cobertura básica (Spring MVC, JDBC, clientes HTTP comuns). Isso é **automatic instrumentation** (ver [[Instrumentation]]).

- Alternativa: usar o **SDK OpenTelemetry manualmente**, útil quando é necessário instrumentar algo que a automatic instrumentation não cobre, ou customizar profundamente o comportamento.
- Não se recomenda misturar o SDK clássico do Application Insights com a distro baseada em OpenTelemetry na mesma aplicação.
- A configuração de conexão usa uma **connection string** (o mecanismo atual, substituindo a antiga *instrumentation key* isolada).

## O que Spring Boot já expõe vs. o que exige instrumentação adicional

- [[Spring Boot Actuator]] expõe health checks e métricas básicas da JVM/framework — mas não gera automaticamente requests correlacionados, dependency tracking ou distributed tracing.
- A instrumentação do Application Insights (via Java Agent) é o que gera [[Request Telemetry]], [[Dependency Telemetry]] e [[Distributed Tracing]] a partir de uma aplicação Spring Boot real.

Essas duas camadas são complementares, não substitutas uma da outra.

## Java 21 e Virtual Threads — ponto de atenção

Java 21 populariza o uso de [[Virtual Threads]] para concorrência. A instrumentação automática de telemetria (via agente/OpenTelemetry) depende de propagar contexto de correlação entre threads — um mecanismo historicamente construído em torno de `ThreadLocal` e threads de plataforma tradicionais. Como virtual threads têm um modelo de execução diferente, a comunidade OpenTelemetry documenta publicamente (fora da documentação oficial da Microsoft) casos de comportamento ainda em maturação nessa combinação.

Esta base **não afirma** que a combinação Java 21 Virtual Threads + Application Insights é totalmente livre de particularidades, nem que é problemática — não há, no momento, uma fonte oficial Microsoft Learn suficientemente conclusiva sobre o tema. Trata-se de um gap reconhecido: antes de adotar virtual threads em produção com instrumentação automática, vale validar empiricamente com a versão do agente em uso.

## Relações

- [[Java Spring Boot Azure Monitor]]
- [[Instrumentation]]
- [[Azure Monitor OpenTelemetry]]
- [[Hexagonal Architecture + Application Insights]]
- [[Spring Boot Actuator]]

## Referências

- Microsoft Learn — "Configure Azure Monitor Application Insights for Java": https://learn.microsoft.com/en-us/azure/azure-monitor/app/java-standalone-config
- Microsoft Learn — "Monitor Java applications": https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable
