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

# Spring Boot Logging

## O que é?

Suporte do Spring Boot para logging, com configuração sensata por padrão (usa Logback como implementação padrão via SLF4J como fachada) e customização via `application.properties`/`application.yml`.

## Log levels

`TRACE < DEBUG < INFO < WARN < ERROR` — cada nível mais alto inclui os níveis de severidade acima dele quando configurado como limiar mínimo (ex.: configurar `INFO` também exibe `WARN` e `ERROR`).

## Structured logging (menção conceitual)

Logging estruturado (ex.: formato JSON, com campos nomeados) facilita processamento automatizado de logs por ferramentas externas — mencionado aqui apenas como preparação conceitual; a integração com uma ferramenta específica de observabilidade não é aprofundada nesta etapa.

## Correlation (menção conceitual)

Em uma requisição que passa por múltiplos componentes, um identificador de correlação (correlation ID / trace ID) permite juntar logs relacionados à mesma requisição — mecanismo relevante para observabilidade distribuída, não aprofundado aqui.

## Boas práticas de logging de exceções

- Logar exceções de domínio com contexto suficiente para diagnóstico, sem expor detalhes sensíveis.
- Evitar logar e relançar a mesma exceção em múltiplas camadas (duplicação de log).

## Ponte para observabilidade

```
Java (java.util.logging / SLF4J)
        ↓
Spring Boot (Logback + configuração)
        ↓
Observability (conceito — não aprofundado aqui)
        ↓
Application Insights (etapa futura)
```

## Relações

- [[Spring Boot Actuator]]
- [[Spring Boot]]

## Referências

- Spring Boot Reference Documentation — "Logging": https://docs.spring.io/spring-boot/reference/features/logging.html
