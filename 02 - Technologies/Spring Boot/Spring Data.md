---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# Spring Data

## O que é?

Spring Data é um módulo do Spring Framework que fornece abstrações comuns para acesso a dados — o objetivo é reduzir o boilerplate de implementar repositórios manualmente, para diferentes tecnologias de persistência (relacional, documento, chave-valor).

## Diferenciando tecnologias que costumam ser confundidas

| Tecnologia | O que é |
|---|---|
| **JDBC** | API padrão do Java (`java.sql`) para executar SQL diretamente contra um banco relacional. |
| **Hibernate** | Implementação concreta de ORM (Object-Relational Mapping) — mapeia objetos Java para tabelas relacionais. |
| **JPA** (Jakarta Persistence API) | Especificação/contrato de ORM em Java — Hibernate é **uma** implementação de JPA (não a única). |
| **Spring Data JPA** | Módulo do Spring que gera implementações de repositórios automaticamente **sobre** JPA (que por sua vez usa uma implementação como Hibernate). |

```
Spring Data JPA
      ↓ (usa)
JPA (especificação)
      ↓ (implementada por)
Hibernate
      ↓ (executa)
JDBC → Banco de dados
```

Estas quatro camadas não são a mesma coisa — cada uma resolve um problema em um nível diferente de abstração.

## O que Spring Data oferece

- Interfaces base (ex.: `CrudRepository`, `JpaRepository`) com operações comuns já implementadas (salvar, buscar por id, deletar).
- Geração automática de implementação de métodos de consulta a partir do **nome do método** (ex.: `findByStatus(OrderStatus status)`), sem escrever SQL/JPQL manualmente para casos simples.
- Suporte a consultas customizadas (`@Query`) quando a convenção de nomes não é suficiente.

## Relações

- [[Spring Data Repository vs Repository Port]]
- [[Spring Transactions]]
- [[Adapters]]

## Referências

- Spring Data Reference Documentation: https://docs.spring.io/spring-data/jpa/reference/
- Jakarta Persistence Specification: https://jakarta.ee/specifications/persistence/
