---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# Spring Bean

## O que é?

Um Bean é um objeto cuja instanciação, configuração e ciclo de vida são gerenciados pelo container [[Inversion of Control|IoC]] do Spring (a [[ApplicationContext]]), em vez de serem criados diretamente pelo código da aplicação com `new`.

## Ciclo de vida (visão conceitual, não exaustiva)

```
Definição do Bean (via anotação, XML ou código Java)
        ↓
Container instancia o Bean
        ↓
Container injeta as dependências (Dependency Injection)
        ↓
Callbacks de inicialização (ex.: @PostConstruct) — quando existirem
        ↓
Bean pronto para uso
        ↓
Callbacks de destruição (ex.: @PreDestroy) — no encerramento do contexto
```

## Criação

Um Bean pode ser registrado de duas formas principais:

- **Component Scanning**: anotando a classe (`@Component` e especializações — ver [[Component Scanning]]).
- **Declaração explícita**: um método anotado com `@Bean` dentro de uma classe `@Configuration` (ver [[Spring Configuration]]).

## Escopos (scopes) principais

- **singleton** (padrão): uma única instância por container, compartilhada por toda a aplicação.
- **prototype**: uma nova instância a cada solicitação ao container.
- **request**: uma instância por requisição HTTP (aplicações web).
- **session**: uma instância por sessão HTTP (aplicações web).

A escolha do escopo afeta diretamente questões de estado compartilhado e concorrência — beans singleton normalmente devem ser *stateless* (sem estado mutável de instância) quando compartilhados entre múltiplas threads.

## Relação com ApplicationContext

A [[ApplicationContext]] é o container que efetivamente mantém, cria e resolve as dependências entre Beans — o Bean é o objeto gerenciado; a ApplicationContext é quem gerencia.

## Relação com Dependency Injection

O mecanismo pelo qual um Bean recebe suas dependências (outros Beans) é [[Dependency Injection]].

## Relações

- [[ApplicationContext]]
- [[Dependency Injection]]
- [[Component Scanning]]
- [[Spring Configuration]]
- [[Inversion of Control]]

## Referências

- Spring Framework Reference — "Bean Overview": https://docs.spring.io/spring-framework/reference/core/beans/definition.html
