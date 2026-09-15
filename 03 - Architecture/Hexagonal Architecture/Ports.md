---
type: concept
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - hexagonal-architecture
---

# Ports

## O que é?

Uma Port é uma **abstração/contrato** definida pelo [[Application Core]] para se comunicar com o mundo externo, sem conhecer detalhes de como essa comunicação é implementada. Na prática em Java, tipicamente uma `interface`.

## Por que existe?

Para que o Core dependa apenas de um contrato que ele mesmo define, e não de uma implementação concreta de infraestrutura — aplicação direta de [[Dependency Inversion]].

## Quem define a Port?

**O Core**, não a infraestrutura. Isso é essencial: a Port existe para servir às necessidades do Core, então sua assinatura é desenhada pensando na linguagem do domínio/aplicação, não nos detalhes da tecnologia que a implementará.

## Qual problema resolve?

Sem Ports, o Core precisaria conhecer diretamente APIs de bibliotecas externas (driver JDBC, cliente HTTP, SDK de nuvem), o que o acopla à tecnologia escolhida e dificulta testes e substituição.

## Como reduz acoplamento

O Core conhece apenas a assinatura da Port (ex.: `save(Order)`), nunca a implementação. Trocar a tecnologia por trás da Port (Postgres → MongoDB, REST → gRPC) não exige mudança no Core, desde que o contrato seja respeitado.

## Driving Ports (Primary Ports / Input Ports)

Representam como o mundo externo **aciona** a aplicação. É a "entrada" — o contrato que um [[Adapters|Driving Adapter]] (ex.: um REST Controller) usa para invocar um [[Use Case]].

```java
interface CreateOrderPort {
    void execute(CreateOrderCommand command);
}
```

## Driven Ports (Secondary Ports / Output Ports)

Representam o que a aplicação **precisa** do mundo externo para completar seu trabalho. É a "saída" — o contrato que o Core define e que um [[Adapters|Driven Adapter]] (ex.: um repositório JDBC) implementa.

```java
interface OrderRepository {
    void save(Order order);
}
```

## Nomenclaturas equivalentes

"Driving Port" = "Primary Port" = "Input Port" (mesmo conceito, nomes diferentes conforme o autor). "Driven Port" = "Secondary Port" = "Output Port" (idem). Não são arquiteturas diferentes — apenas vocabulário diferente para o mesmo papel.

## Relações

- [[Adapters]] — implementam ou consomem as Ports.
- [[Dependency Inversion]]
- [[Use Case]]
- [[Application Core]]
- [[Hexagonal Architecture]]

## Referências

- Cockburn, Alistair. "Hexagonal Architecture", 2005: https://alistair.cockburn.us/hexagonal-architecture/
