---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# ApplicationContext

## O que é?

`ApplicationContext` é a implementação central do container [[Inversion of Control|IoC]] do Spring: é ela quem instancia, configura e gerencia os [[Spring Bean|Beans]] de uma aplicação, resolvendo as dependências entre eles.

## Relação com BeanFactory

`ApplicationContext` estende a interface mais básica `BeanFactory`, adicionando recursos usados por praticamente toda aplicação moderna: inicialização antecipada (eager) dos beans singleton por padrão, propagação de eventos, integração com AOP, suporte a internacionalização, e resolução de recursos (arquivos, mensagens, propriedades). Na prática, `BeanFactory` isolada raramente é usada diretamente hoje — `ApplicationContext` é o container padrão.

## Fluxo conceitual

```
Spring Application (main())
       ↓
ApplicationContext é criado
       ↓
Beans são registrados e instanciados
       ↓
Dependências entre Beans são resolvidas e injetadas
       ↓
Aplicação pronta (contexto "up")
```

## Responsabilidades

- Ler as definições de Bean (via anotações, classes `@Configuration`, ou XML legado).
- Instanciar os Beans na ordem correta, resolvendo o grafo de dependências.
- Aplicar o escopo correto de cada Bean (ver [[Spring Bean]]).
- Publicar e propagar eventos da aplicação.
- Fechar/destruir os Beans ao encerrar o contexto.

## Relação com Spring Boot

Em uma aplicação Spring Boot, `SpringApplication.run(...)` cria e inicializa a `ApplicationContext` automaticamente, aplicando [[Spring Boot Auto-Configuration]] durante esse processo — ver [[Spring Boot Application]].

## Relações

- [[Spring Bean]]
- [[Inversion of Control]]
- [[Component Scanning]]
- [[Spring Boot Application]]

## Referências

- Spring Framework Reference — "The IoC Container": https://docs.spring.io/spring-framework/reference/core/beans/context.html
