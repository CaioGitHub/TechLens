---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - spring
---

# Health Check

## O que é?

Um Health Check é um mecanismo (tipicamente um endpoint HTTP) através do qual uma aplicação ou componente reporta seu próprio estado de saúde, para que outro sistema (a plataforma, um load balancer) decida se deve considerá-lo apto a receber tráfego.

## Modelo

```
Application
    ↓
Health Endpoint  (ex.: /actuator/health do Spring Boot Actuator)
    ↓
Platform / Monitor
    ↓
Availability / Alerting
```

Um Spring Boot expõe naturalmente esse endpoint via [[Spring Boot Actuator]]; plataformas como [[Azure App Service]] e o [[Application Gateway and Load Balancing|Application Gateway]] podem consultá-lo periodicamente para decidir se uma instância deve continuar recebendo requisições.

## Ressalva importante

Um Health Check bem-sucedido **não implica automaticamente** que o sistema completo está saudável — um endpoint de health pode responder "ok" verificando apenas que o processo está ativo e a conexão com o banco existe, sem detectar, por exemplo, que uma dependência externa crítica está degradada, ou que uma funcionalidade específica está quebrada. Ver [[Availability Monitoring]] para a distinção entre "processo rodando" e disponibilidade real percebida pelo usuário.

## Relações

- [[Availability Monitoring]]
- [[Spring Boot Actuator]]
- [[Application Gateway and Load Balancing]]

## Referências

- Microsoft Learn — "Monitor App Service instances using Health check": https://learn.microsoft.com/en-us/azure/app-service/monitor-instances-health-check
