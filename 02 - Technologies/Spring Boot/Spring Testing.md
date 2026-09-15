---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# Spring Testing

## O que é?

Suporte do Spring (módulo Spring Test, trazido por `spring-boot-starter-test`) para testar aplicações Spring em diferentes níveis, do isolamento total à integração completa.

## Três níveis principais

```
Unit Test                    → mais rápido, sem Spring Context
        ↓
Spring Integration Test       → sobe (parte d)o ApplicationContext real
        ↓
End-to-End Test               → aplicação completa, incluindo infraestrutura real
```

### Unit Test

Testa uma classe isoladamente (ex.: um Use Case), sem subir a `ApplicationContext`, substituindo dependências por mocks/fakes manuais (ver a seção "Testabilidade" em [[Hexagonal Architecture]]). Não usa nada do Spring — é um teste Java comum (JUnit + Mockito, por exemplo).

### Spring Integration Test

Sobe (total ou parcialmente) a `ApplicationContext` real para validar que os Beans se integram corretamente (ex.: `@SpringBootTest`, ou um "test slice" mais específico como `@WebMvcTest` para testar apenas a camada web, ou `@DataJpaTest` para testar apenas a camada de persistência). Mais lento que um unit test, mas mais rápido que subir a aplicação inteira com infraestrutura real.

### End-to-End Test

Sobe a aplicação completa, incluindo infraestrutura real ou próxima da real (ex.: um banco de dados real via Testcontainers). Valida o comportamento do sistema como um todo, mas é o nível mais lento e caro de manter.

## Test slices

"Test slices" (`@WebMvcTest`, `@DataJpaTest`, etc.) carregam apenas a parte da `ApplicationContext` relevante para a camada testada, em vez do contexto inteiro — um meio-termo entre unit test puro e `@SpringBootTest` completo.

## Testcontainers (menção breve)

Quando um teste de integração precisa de um banco de dados real (não um em memória), Testcontainers permite subir esse banco em um container Docker durante o teste — mencionado aqui apenas como referência; não aprofundado nesta etapa.

## Relação com Hexagonal Architecture

A separação em Ports/Adapters (ver [[Ports]], [[Adapters]]) é o que torna possível testar o [[Application Core]] com um unit test puro (substituindo um Port por um fake), sem precisar de `ApplicationContext` nem de infraestrutura real.

## Relações

- [[Hexagonal Architecture]]
- [[Ports]]
- [[Application Core]]

## Referências

- Spring Framework Reference — "Testing": https://docs.spring.io/spring-framework/reference/testing.html
- Spring Boot Reference Documentation — "Testing": https://docs.spring.io/spring-boot/reference/testing/
