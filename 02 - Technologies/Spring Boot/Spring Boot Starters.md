---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
  - spring-boot
---

# Spring Boot Starters

## O que é?

Um Starter é um descritor de dependências do Spring Boot: um único artefato Maven/Gradle que agrega um conjunto de bibliotecas relacionadas e compatíveis entre si para uma finalidade específica (ex.: `spring-boot-starter-web` para aplicações web).

## Por que existe?

Sem starters, adicionar suporte web exigiria escolher manualmente Spring MVC, um servidor embutido (Tomcat/Jetty/Undertow), uma biblioteca de serialização JSON (Jackson) e garantir que as versões de todas elas sejam compatíveis entre si. Starters resolvem o problema de **gerenciamento de versões compatíveis** (dependency management).

## Como funciona

```
spring-boot-starter-web
        ↓
Traz: Spring MVC, Tomcat embutido, Jackson (JSON), validação, etc.
        ↓
Essas dependências aparecem no classpath
        ↓
Spring Boot Auto-Configuration reage à presença delas
        ↓
Aplicação web funcional
```

## Exemplos conceituais

- `spring-boot-starter-web` — aplicações web/REST com Spring MVC.
- `spring-boot-starter-data-jpa` — persistência com Spring Data JPA.
- `spring-boot-starter-test` — dependências de teste (JUnit, Mockito, Spring Test).
- `spring-boot-starter-validation` — Bean Validation.
- `spring-boot-starter-actuator` — endpoints operacionais (ver [[Spring Boot Actuator]]).

## Relação com Auto-Configuration

Starter e Auto-Configuration são mecanismos complementares: o starter resolve **quais bibliotecas** entram no classpath com versões compatíveis; a Auto-Configuration decide **como configurá-las** automaticamente. Ver [[Spring Boot Auto-Configuration]].

## Relações

- [[Spring Boot Auto-Configuration]]
- [[Spring Framework vs Spring Boot]]

## Referências

- Spring Boot Reference Documentation — "Starters": https://docs.spring.io/spring-boot/reference/using/build-systems.html#using.build-systems.starters
