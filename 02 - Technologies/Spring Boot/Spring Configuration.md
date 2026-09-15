---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# Spring Configuration

## O que é?

Configuração, no Spring, é o mecanismo de declarar explicitamente como um [[Spring Bean]] deve ser criado — em contraste com deixar o Spring descobri-lo automaticamente via [[Component Scanning]].

## @Configuration + @Bean

```java
@Configuration
class AppConfig {
    @Bean
    OrderRepository orderRepository(DataSource dataSource) {
        return new JdbcOrderRepository(dataSource);
    }
}
```

Uma classe `@Configuration` é, ela mesma, registrada como Bean; cada método `@Bean` dentro dela declara explicitamente um Bean gerenciado pelo container, com controle total sobre como ele é construído.

## Quando declarar um Bean explicitamente (em vez de Component Scanning)?

- A classe vem de uma biblioteca externa (não pode ser anotada com `@Component`).
- A construção depende de lógica condicional ou de parâmetros externos.
- Você quer manter classes de domínio/infraestrutura **livres de anotações do Spring** (relevante para proteger o [[Application Core]] — ver [[Spring Boot + Hexagonal Architecture]]).

## Configuração automática vs. explícita

```
Configuração explícita:  eu decido, no código de configuração, qual implementação usar.
Configuração automática: o Spring Boot decide por convenção, com base no classpath (ver Spring Boot Auto-Configuration).
```

Ambas coexistem: uma configuração explícita sempre pode sobrescrever (override) uma auto-configuração equivalente.

## Propriedades e Profiles

Valores de configuração (strings, números, flags) tipicamente não ficam hardcoded na classe `@Configuration` — são externalizados via `application.properties`/`application.yml` e podem variar por ambiente (ver [[Spring Profiles]] e [[Spring Configuration Properties]]).

## Relações

- [[Spring Bean]]
- [[Component Scanning]]
- [[Spring Boot Auto-Configuration]]
- [[Spring Profiles]]
- [[Spring Configuration Properties]]
- [[Application Core]]

## Referências

- Spring Framework Reference — "Java-based Container Configuration": https://docs.spring.io/spring-framework/reference/core/beans/java.html
