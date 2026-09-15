---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# Inversion of Control

## O que é?

Inversion of Control (IoC) é um princípio de design em que o **controle sobre a criação e o ciclo de vida de objetos** deixa de pertencer ao próprio código que os usa e passa a pertencer a um agente externo — no caso do Spring, o **container IoC**.

## Comparação central

```
Sem IoC: "Aplicação cria a dependência"
class CreateOrder {
    private final OrderRepository repository = new JdbcOrderRepository(); // controle interno
}

Com IoC: "Container fornece a dependência"
class CreateOrder {
    private final OrderRepository repository;
    CreateOrder(OrderRepository repository) { this.repository = repository; } // controle externo
}
```

No segundo caso, `CreateOrder` não decide *qual* implementação usar nem *quando* criá-la — essa responsabilidade foi invertida para fora da classe.

## Papel do container

No Spring, o container IoC (representado pela [[ApplicationContext]]) é responsável por: instanciar objetos ([[Spring Bean|Beans]]), resolver e injetar as dependências entre eles, e gerenciar o ciclo de vida completo desses objetos.

## IoC vs Dependency Injection — não são sinônimos perfeitos

- **IoC** é o princípio mais amplo: "quem controla a criação/ciclo de vida de um objeto?". Pode ser implementado de várias formas (Service Locator, Template Method, Factory, eventos).
- **[[Dependency Injection]]** é **uma técnica específica** de se aplicar IoC — a mais usada no Spring — em que dependências são fornecidas de fora (via construtor, setter ou campo).

```
Inversion of Control (princípio)
        ↓
Dependency Injection (uma técnica que aplica IoC)
        ↓
Spring Container (implementação concreta)
        ↓
Bean (objeto gerenciado pelo container)
```

## Relação com Dependency Inversion

IoC (mecanismo de controle) e [[Dependency Inversion]] (princípio de design sobre depender de abstrações) são conceitos complementares, mas distintos: DIP diz *do que* depender (abstrações); IoC/DI dizem *quem* fornece essa dependência em tempo de execução. O Spring aplica ambos: você depende de uma interface (DIP) e o container a injeta (IoC/DI).

## Trade-offs

- Reduz acoplamento e facilita testes (é possível injetar um *fake*/*mock* no lugar da dependência real).
- Introduz indireção: entender "quem criou este objeto e com quais dependências" exige olhar a configuração do container, não apenas o código da classe.

## Relações

- [[Dependency Injection]]
- [[Dependency Inversion]]
- [[ApplicationContext]]
- [[Spring Bean]]
- [[Spring Framework vs Spring Boot]]

## Referências

- Spring Framework Reference — "The IoC Container": https://docs.spring.io/spring-framework/reference/core/beans.html
- Fowler, Martin. "Inversion of Control Containers and the Dependency Injection pattern", martinfowler.com, 2004.
