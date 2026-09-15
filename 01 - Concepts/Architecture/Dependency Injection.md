---
type: concept
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - architecture
---

# Dependency Injection

## O que é?

Dependency Injection (DI) é uma **técnica/mecanismo** pelo qual um objeto recebe suas dependências de fora (via construtor, método ou campo) em vez de criá-las internamente. É uma forma específica de implementar Inversion of Control.

## Por que existe?

Para que uma classe possa depender apenas de uma abstração (ver [[Dependency Inversion]]) sem precisar saber *qual* implementação concreta usar ou *como* construí-la — essa responsabilidade é delegada a quem monta o objeto (um container de DI, uma factory, ou código de composição manual).

## Qual problema resolve?

Sem DI, uma classe que depende de uma abstração ainda precisaria instanciar uma implementação concreta em algum lugar (`new JdbcOrderRepository()`), reintroduzindo acoplamento com o detalhe concreto. DI resolve isso externalizando a decisão de "qual implementação usar" para fora da classe consumidora.

## Como funciona?

```java
interface OrderRepository { void save(Order order); }

class CreateOrder {
    private final OrderRepository repository;

    // Constructor Injection — a dependência é recebida, não criada
    CreateOrder(OrderRepository repository) {
        this.repository = repository;
    }
}

// Em algum ponto de composição (main, factory, container DI):
OrderRepository repo = new JdbcOrderRepository();
CreateOrder useCase = new CreateOrder(repo);
```

## Formas de injeção

```java
// Constructor Injection (preferida por padrão)
class CreateOrder {
    private final OrderRepository repository;
    CreateOrder(OrderRepository repository) { this.repository = repository; }
}

// Setter Injection
class CreateOrder {
    private OrderRepository repository;
    void setRepository(OrderRepository repository) { this.repository = repository; }
}

// Field Injection (ex.: @Autowired em um campo, no Spring)
class CreateOrder {
    @Autowired
    private OrderRepository repository;
}
```

| | Constructor Injection | Setter Injection | Field Injection |
|---|---|---|---|
| Imutabilidade | Permite `final` — dependência obrigatória e imutável | Dependência mutável após construção | Dependência mutável, geralmente sem `final` |
| Testabilidade | Alta — basta chamar o construtor com um fake, sem precisar de um container | Média — exige chamar o setter manualmente | Baixa — objeto não pode ser instanciado com a dependência sem reflection ou um container |
| Dependência obrigatória vs. opcional | Boa para dependências obrigatórias (não compila sem elas) | Adequada para dependências opcionais/reconfiguráveis | Não deixa explícito se a dependência é obrigatória |
| Visibilidade das dependências | Alta — todas aparecem na assinatura do construtor | Média | Baixa — dependências ficam "escondidas" dentro da classe |

Esta base dá **preferência conceitual a Constructor Injection** por tornar as dependências explícitas, permitir imutabilidade e facilitar testes sem precisar de um container. Isso não é uma regra dogmática: Setter Injection pode ser apropriado para dependências verdadeiramente opcionais; Field Injection é desencorajado principalmente por dificultar testes e esconder dependências (ver anti-pattern "Overuse of @Autowired" em [[Spring Boot Anti-Patterns]]), mas não é tecnicamente proibido.

## Dependency Inversion vs. Dependency Injection

**Não são sinônimos.** Dependency Inversion é um **princípio de design** (depender de abstrações, não de concretizações). Dependency Injection é uma **técnica de composição** que ajuda a satisfazer esse princípio na prática, fornecendo a implementação concreta de fora. É possível aplicar DIP sem um framework de DI (montagem manual, como no exemplo acima); frameworks de DI (como o container do Spring) apenas automatizam essa montagem.

## Quando usar?

Sempre que uma classe dependa de uma abstração cuja implementação pode variar (produção vs. teste, ou entre ambientes).

## Quando evitar?

Para objetos de valor simples e sem estado externo, instanciar diretamente (`new`) é mais simples e não precisa de injeção.

## Relações

- [[Dependency Inversion]]
- [[Hexagonal Architecture]] — a "montagem" (composition root) de uma aplicação hexagonal é onde adapters concretos são injetados nos casos de uso.
- [[Inversion of Control]] — IoC é o princípio mais amplo do qual DI é uma técnica; ver a distinção completa nessa nota.
- [[Spring Bean]], [[Spring Boot Anti-Patterns]] — mecanismo de DI aplicado concretamente pelo Spring.

## Referências

- Fowler, Martin. "Inversion of Control Containers and the Dependency Injection pattern", martinfowler.com, 2004.
