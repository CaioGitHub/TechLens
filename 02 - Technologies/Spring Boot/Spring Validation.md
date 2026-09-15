---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# Spring Validation

## O que é?

Suporte do Spring (via Bean Validation / Jakarta Validation, habilitado com `spring-boot-starter-validation`) para validar automaticamente a estrutura de um objeto de entrada, usando anotações de restrição (constraints).

## Exemplo

```java
record CreateOrderRequest(
    @NotEmpty List<OrderItemRequest> items
) {}

@PostMapping
ResponseEntity<Void> create(@RequestBody @Valid CreateOrderRequest request) { ... }
```

`@Valid` dispara a validação das constraints (`@NotNull`, `@NotEmpty`, `@Size`, `@Min`, etc.) declaradas no DTO antes do método do controller ser executado.

## Validação estrutural vs. regra de domínio

Este é o ponto conceitual mais importante desta nota:

```
HTTP Validation (estrutural — "o campo veio no formato esperado?")
      ↓
Input Boundary (o DTO chegou íntegro ao Use Case)
      ↓
Domain Rules (regra de negócio — "este pedido pode ser confirmado?")
```

- **Validação de entrada (Bean Validation)**: verifica **forma** — campo obrigatório, tamanho, formato. É uma preocupação da borda (Adapter/DTO).
- **Regra de domínio**: verifica **significado de negócio** — ex.: "um pedido não pode ser confirmado sem itens" (ver exemplo em [[Domain]]). Essa regra deve existir no Domain independentemente de como a requisição chegou até ali (HTTP, CLI, mensageria).

## Por que essa distinção importa

Validação de request **não substitui** regras de domínio: um DTO estruturalmente válido (todos os campos presentes) ainda pode representar uma operação inválida do ponto de vista de negócio. Se a regra de negócio só existir na validação HTTP, ela desaparece quando a mesma operação é acionada por outro Driving Adapter (ex.: um consumidor de mensageria, um CLI).

## Relações

- [[DTO]]
- [[Domain]]
- [[Spring REST]]
- [[Spring Exception Handling]]

## Referências

- Spring Framework Reference — "Validation": https://docs.spring.io/spring-framework/reference/core/validation.html
- Jakarta Bean Validation Specification: https://jakarta.ee/specifications/bean-validation/
