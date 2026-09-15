---
type: concept
status: learning
confidence: 65
created: 2026-09-08
updated: 2026-09-08
tags:
  - architecture
---

# Dependency Inversion

## O que é?

O Dependency Inversion Principle (DIP) — o "D" de [[SOLID]] — afirma que módulos de alto nível (política, regras de negócio) não devem depender de módulos de baixo nível (detalhes de implementação); ambos devem depender de **abstrações**. Além disso, abstrações não devem depender de detalhes — detalhes é que devem depender de abstrações.

## Por que existe?

Sem inversão de dependência, regras de negócio (alto nível) acabam importando diretamente bibliotecas, drivers e frameworks (baixo nível), tornando o núcleo do sistema refém de decisões de infraestrutura.

## Qual problema resolve?

Permite trocar uma implementação concreta (ex.: trocar PostgreSQL por outro banco, ou um provedor de nuvem por outro) sem alterar as regras de negócio, desde que a nova implementação obedeça à mesma abstração.

## Como funciona?

A **abstração é definida pelo lado que a consome** (o alto nível), não pelo lado que a implementa. Isso inverte a direção natural de dependência: em vez do alto nível depender do baixo nível, o baixo nível passa a depender da abstração definida pelo alto nível.

```java
// Alto nível define a abstração que precisa
interface OrderRepository {
    void save(Order order);
}

// Alto nível depende apenas da abstração
class CreateOrder {
    private final OrderRepository repository;
    CreateOrder(OrderRepository repository) { this.repository = repository; }
}

// Baixo nível implementa a abstração definida pelo alto nível
class JdbcOrderRepository implements OrderRepository {
    public void save(Order order) { /* detalhes JDBC */ }
}
```

## Quem define a interface, quem implementa

Em Arquitetura Hexagonal, essa distinção corresponde diretamente a [[Ports]] (definidos pelo Core, no lado de dentro) e [[Adapters]] (implementações concretas, no lado de fora).

## Exemplo

Ver bloco de código acima — `OrderRepository` é a abstração; `JdbcOrderRepository` é o detalhe que depende dela, não o contrário.

## Quando usar?

Sempre que o alto nível (regras de negócio) precisar de um recurso externo (banco, API, fila) cuja implementação concreta pode mudar ou precisar ser substituída em testes.

## Quando evitar?

Para dependências estáveis, internas ao próprio domínio, que nunca serão trocadas (inverter tudo indiscriminadamente gera abstrações desnecessárias — ver seção de trade-offs em [[Hexagonal Architecture]]).

## Relações

- [[SOLID]]
- [[Dependency Injection]] — mecanismo comum para *fornecer* a implementação concreta a quem depende da abstração.
- [[Ports]]
- [[Adapters]]
- [[Hexagonal Architecture]] — DIP é o princípio que fundamenta toda a arquitetura.

## Referências

- Martin, Robert C. — "The Dependency Inversion Principle", *Engineering Notebook*, 1996.
