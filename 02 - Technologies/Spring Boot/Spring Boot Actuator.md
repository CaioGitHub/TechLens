---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
  - spring-boot
  - observability
---

# Spring Boot Actuator

## O que é?

Módulo do Spring Boot (`spring-boot-starter-actuator`) que expõe endpoints operacionais prontos para monitorar e gerenciar uma aplicação em execução — sem precisar implementá-los manualmente.

## Endpoints comuns

- `/actuator/health` — indica se a aplicação está saudável (e, com detalhes, quais componentes — banco, disco — contribuem para esse status).
- `/actuator/metrics` — métricas da aplicação e da JVM (memória, threads, contadores customizados).
- `/actuator/info` — informações estáticas sobre a build/aplicação.

## Readiness vs. Liveness

Distinção relevante em ambientes com orquestração (ex.: Kubernetes, mencionado apenas como contexto, sem aprofundar):

- **Liveness**: "a aplicação está travada e precisa ser reiniciada?"
- **Readiness**: "a aplicação está pronta para receber tráfego agora?" (pode estar viva, mas temporariamente não pronta, ex.: aguardando conexão com banco).

## Ponte para observabilidade (preparação para etapa futura)

```
Spring Boot Actuator
        ↓
Application Observability (conceito — não aprofundado aqui)
        ↓
Azure Monitor
        ↓
Application Insights
        ↓
Log Analytics
```

Esta nota registra apenas a existência dessa ponte. Azure Monitor, Application Insights e Log Analytics **não são documentados nesta etapa** — serão tratados em uma etapa futura dedicada a observabilidade.

## Relações

- [[Spring Boot]]
- [[Spring Boot Logging]]

## Referências

- Spring Boot Reference Documentation — "Actuator": https://docs.spring.io/spring-boot/reference/actuator/
