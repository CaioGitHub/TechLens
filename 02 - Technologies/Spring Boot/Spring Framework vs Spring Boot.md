---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# Spring Framework vs Spring Boot

## O que é?

**Spring Framework** é a plataforma original (2003+): um conjunto de módulos (Core Container, MVC, Data, Security, Test, entre outros) construídos sobre um container de [[Inversion of Control]] (IoC). **Spring Boot** (2014+) é construído **sobre** o Spring Framework — ele não é um framework concorrente nem um substituto.

```
Spring Framework
       ↓
Core Container (IoC / DI)
       ↓
Spring MVC · Spring Data · Spring Security · Spring Test (módulos)
       ↓
Spring Boot
```

## Por que Spring Boot existe?

Aplicações Spring "puras" (pré-2014) exigiam bastante configuração manual: registrar beans explicitamente, configurar XML, escolher e alinhar versões compatíveis de dezenas de bibliotecas, configurar um servidor de aplicação externo. Spring Boot existe para resolver esse problema de **fricção de configuração**, sem mudar os conceitos fundamentais do Spring Framework (o container IoC continua sendo o mesmo).

## Qual problema resolve?

- Gerenciamento de versões compatíveis entre dezenas de dependências (resolvido via [[Spring Boot Starters]]).
- Configuração manual repetitiva de componentes comuns (resolvido via [[Spring Boot Auto-Configuration]]).
- Necessidade de um servidor de aplicação externo para rodar uma aplicação web (Spring Boot embute um servidor, ex.: Tomcat).
- Empacotamento e execução (um único JAR executável, `java -jar app.jar`, em vez de deploy manual em um servidor).

## O que Spring Boot adiciona (não substitui)

| Papel | Fornecido por |
|---|---|
| Container IoC, DI, AOP | Spring Framework (Core Container) |
| Camada web (Controllers, DispatcherServlet) | Spring MVC (módulo do Framework) |
| Acesso a dados | Spring Data (módulo do Framework) |
| Convenções + configuração automática | Spring Boot |
| Dependências pré-alinhadas ([[Spring Boot Starters]]) | Spring Boot |
| Servidor embutido, empacotamento (`.jar` executável) | Spring Boot |
| Endpoints operacionais ([[Spring Boot Actuator]]) | Spring Boot |

## Como funciona (visão geral)

Spring Boot não reimplementa o container IoC — ele apenas **configura o Spring Framework automaticamente**, com base no que está no classpath e em convenções, através de [[Spring Boot Auto-Configuration]]. Uma aplicação Spring Boot continua sendo, no fundo, uma aplicação Spring Framework.

## Quando usar Spring puro (sem Boot)?

Casos raros hoje em dia: bibliotecas que só usam o Core Container sem precisar de uma aplicação executável completa, ou ambientes legados com configuração já estabelecida. Para a grande maioria dos casos novos, Spring Boot é a forma padrão de usar o Spring Framework.

## Relações

- [[Inversion of Control]]
- [[Spring Bean]]
- [[ApplicationContext]]
- [[Spring Boot]]
- [[Spring Boot Auto-Configuration]]
- [[Spring Boot Starters]]

## Referências

- Spring Framework Reference Documentation: https://docs.spring.io/spring-framework/reference/
- Spring Boot Reference Documentation: https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/
