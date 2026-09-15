---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
  - hexagonal-architecture
---

# Spring Data Repository vs Repository Port

## O ponto central desta nota

> Um `Spring Data Repository` (ex.: uma interface que estende `JpaRepository`) **não precisa ser automaticamente o mesmo conceito** que um Repository/Output Port da Arquitetura Hexagonal. São dois conceitos que podem se relacionar, mas pertencem a camadas diferentes.

## Diagrama

```
Application Core
      ↓
Repository Port (interface definida pelo Core — ex.: OrderRepository)
      ↑ (implementada por)
Spring Data Adapter (Driven Adapter, usa Spring Data JPA internamente)
      ↓
Database
```

## Duas formas comuns de organizar isso

**1. Port própria + Adapter que usa Spring Data internamente (preserva o isolamento):**

```java
// Port definida pelo Core, sem qualquer import do Spring
interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(OrderId id);
}

// Interface técnica do Spring Data (detalhe de infraestrutura)
interface SpringDataOrderRepository extends JpaRepository<OrderEntity, UUID> {}

// Adapter: implementa a Port do Core, usando o Spring Data por baixo
class JpaOrderRepositoryAdapter implements OrderRepository {
    private final SpringDataOrderRepository springDataRepository;
    // traduz entre OrderEntity (JPA) e Order (Domain)
}
```

**2. Usar a interface do Spring Data diretamente como se fosse a Port (atalho comum na prática):**

```java
interface OrderRepository extends JpaRepository<Order, UUID> {}
```

Esta segunda forma é mais simples e comum em projetos pequenos, mas faz o [[Application Core]] (ou algo próximo dele) importar diretamente um tipo do Spring (`JpaRepository`) — uma escolha consciente de trade-off entre pureza arquitetural e simplicidade, não um erro automático.

## Quando a distinção importa mais

Quando há real necessidade de trocar a tecnologia de persistência sem tocar o Core, ou quando o modelo de domínio (`Order`) precisa ser diferente do modelo de persistência (`OrderEntity`, com anotações JPA). Para aplicações pequenas ou protótipos, a segunda forma costuma ser um trade-off aceitável.

## Relações

- [[Ports]]
- [[Adapters]]
- [[Spring Data]]
- [[Spring Boot + Hexagonal Architecture]]
- [[Dependency Rule]]

## Referências

- Spring Data Reference Documentation: https://docs.spring.io/spring-data/jpa/reference/
- Cockburn, Alistair. "Hexagonal Architecture", 2005.
