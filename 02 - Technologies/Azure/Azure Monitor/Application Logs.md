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

# Application Logs

## O que é?

Application Logs são registros gerados pelo próprio código da aplicação (ex.: `logger.info(...)`, `logger.error(...)` em um Spring Boot) — diferentes de logs gerados pela plataforma Azure sobre um recurso.

## Diferenciação

```
Spring Boot
   ↓
Application Log        (gerado pelo código: "pedido 123 processado com sucesso")

versus:

Azure Resource
   ↓
Platform / Resource Log   (gerado pela plataforma: "conexão negada por NSG", "blob lido")
```

Application Logs conhecem o **contexto de negócio** da aplicação (qual pedido, qual usuário, qual regra de negócio falhou); Resource Logs conhecem apenas o comportamento do recurso de infraestrutura em si, sem saber nada sobre a lógica de negócio rodando dentro dele.

## Por que essa distinção importa

Um sistema pode ter Resource Logs perfeitamente saudáveis (o App Service está respondendo, sem erros de infraestrutura) e ainda assim ter Application Logs cheios de exceções de negócio — os dois tipos de log respondem perguntas complementares, e nenhum substitui o outro. Essa distinção é a base para entender o papel do Application Insights (Etapa 8), que se concentra justamente em capturar telemetria rica do lado da aplicação.

## Relações

- [[Resource Logs]]
- [[Azure Activity Log]]
- [[Application Monitoring]]
- [[Java Spring Boot Azure Monitor]]

## Referências

- Microsoft Learn — "Application monitoring for Java": https://learn.microsoft.com/en-us/azure/azure-monitor/app/opentelemetry-enable
