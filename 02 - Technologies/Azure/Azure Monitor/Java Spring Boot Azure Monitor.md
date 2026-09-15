---
type: architecture
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - spring
---

# Java Spring Boot Azure Monitor

## A conexão

```
Java 21
   ↓
Spring Boot
   ↓
Application
   ↓
Telemetry
   ↓
Azure Monitor
```

## O que isso significa

Uma aplicação Spring Boot, ao rodar sobre a JVM (Java 21) e ser hospedada no Azure, naturalmente gera telemetria em diferentes níveis:

- **Nível de plataforma**: o recurso que hospeda a aplicação (ex.: [[Azure App Service]]) já expõe métricas de CPU, memória e requisições sem qualquer configuração do lado do código — ver [[Resource Monitoring]].
- **Nível de aplicação**: o próprio código Spring Boot pode gerar [[Application Logs]] (via logging) e expor um [[Health Check]] (via [[Spring Boot Actuator]]) — mas sinais mais ricos de aplicação (requests individuais, exceções, dependências) exigem instrumentação adicional.

## A aplicação gera sinais; a coleta é uma responsabilidade maior

A aplicação Spring Boot não precisa "saber" como o Azure Monitor funciona para gerar bons sinais (logs bem estruturados, métricas de negócio expostas via [[Spring Boot Actuator]]) — a coleta, o armazenamento e a análise desses sinais são responsabilidade da infraestrutura de observabilidade, configurada separadamente da lógica de negócio da aplicação.

## Duas afirmações que esta base evita

- **Spring Boot não fornece automaticamente toda a observabilidade necessária**: o [[Spring Boot Actuator]] expõe health checks e métricas básicas da JVM/framework, mas não gera automaticamente traces distribuídos, telemetria de dependências externas ou correlação entre serviços — isso exige instrumentação adicional (ver [[Application Monitoring]]).
- **Azure Monitor não instrumenta automaticamente uma aplicação Java**: sem configuração explícita (Diagnostic Settings para o recurso, e instrumentação de aplicação como Java Agent/SDK/OpenTelemetry), o Azure Monitor coleta apenas métricas de plataforma do recurso hospedeiro (ver [[Resource Monitoring]]) — não sinais de negócio de dentro do código Spring Boot.

## Escopo desta etapa

Esta nota estabelece apenas a conexão conceitual. A instrumentação prática (SDK, Java Agent, OpenTelemetry) pertence à Etapa 8 — Application Insights.

## Relações

- [[Application Monitoring]]
- [[Spring Boot Actuator]]
- [[Spring Boot Logging]]
- [[Hexagonal Architecture + Observability]]
- [[Java Spring Boot Application Insights]]

## Referências

- Microsoft Learn — "Monitor Java applications": https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable
