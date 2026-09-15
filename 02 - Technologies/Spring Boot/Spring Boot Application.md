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

# Spring Boot Application

## O que é?

`@SpringBootApplication` é uma meta-anotação (combina outras três) usada na classe principal de uma aplicação Spring Boot, que dispara o processo completo de inicialização.

## O que ela combina

- `@Configuration` — marca a própria classe como fonte de definição de Beans (ver [[Spring Configuration]]).
- `@ComponentScan` — habilita a descoberta automática de componentes anotados (ver [[Component Scanning]]).
- `@EnableAutoConfiguration` — habilita a [[Spring Boot Auto-Configuration]].

## Fluxo de inicialização

```
main()
  ↓
SpringApplication.run(...)
  ↓
ApplicationContext é criado
  ↓
Bean Registration (Component Scanning + @Bean explícitos)
  ↓
Auto-Configuration é aplicada (conforme classpath e condições)
  ↓
Application Ready (contexto totalmente inicializado)
```

## Exemplo mínimo

```java
@SpringBootApplication
class OrderApiApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderApiApplication.class, args);
    }
}
```

## Relação com os conceitos que ela ativa

`@SpringBootApplication` não introduz um novo mecanismo — ela é um atalho para três mecanismos já existentes do Spring Framework/Boot ([[Spring Configuration]], [[Component Scanning]], [[Spring Boot Auto-Configuration]]), aplicados juntos por convenção.

## Relações

- [[ApplicationContext]]
- [[Component Scanning]]
- [[Spring Boot Auto-Configuration]]
- [[Spring Configuration]]

## Referências

- Spring Boot Reference Documentation — "Using the @SpringBootApplication Annotation": https://docs.spring.io/spring-boot/reference/using/using-the-springbootapplication-annotation.html
