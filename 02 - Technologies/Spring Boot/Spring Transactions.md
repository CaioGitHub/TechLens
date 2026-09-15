---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# Spring Transactions

## O que é?

Suporte do Spring para demarcar limites transacionais (transaction boundaries) declarativamente, tipicamente com a anotação `@Transactional`, em vez de gerenciar `commit`/`rollback` manualmente.

## Conceitos de transação (ACID, visão conceitual)

- **Atomicidade**: a transação ocorre por completo ou não ocorre (rollback em caso de erro).
- **Consistência**: a transação leva o sistema de um estado válido para outro estado válido.
- **Isolamento**: transações concorrentes não interferem umas nas outras (nível configurável).
- **Durabilidade**: uma vez confirmada (commit), a mudança persiste mesmo após falhas.

## @Transactional

```java
@Transactional
class CreateOrderUseCase {
    void execute(CreateOrderCommand command) {
        // se qualquer exceção não-checked ocorrer aqui, a transação sofre rollback
    }
}
```

## Boundaries (limites transacionais)

O limite de uma transação normalmente corresponde à execução completa de um Use Case (uma operação de negócio completa) — não a uma única chamada de repositório isoladamente. Isso é relevante para onde a anotação `@Transactional` é aplicada arquiteturalmente.

## Propagation e Rollback (visão conceitual, sem aprofundar)

- **Propagation**: define o que acontece quando um método transacional chama outro método transacional (ex.: participar da transação existente, ou iniciar uma nova).
- **Rollback**: por padrão, o Spring reverte a transação em exceções não verificadas (`RuntimeException`); esse comportamento pode ser customizado.

Detalhes avançados de propagation (`REQUIRES_NEW`, `NESTED`, etc.) ficam fora do escopo desta etapa — relevantes apenas quando a aplicação realmente precisar deles.

## Relações

- [[Spring Data]]
- [[Use Case]]

## Referências

- Spring Framework Reference — "Transaction Management": https://docs.spring.io/spring-framework/reference/data-access/transaction.html
