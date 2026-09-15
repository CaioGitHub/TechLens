---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - hexagonal-architecture
---

# Domain

## O que é?

O Domain (domínio) representa as regras de negócio e conceitos centrais de um sistema — o conhecimento que existiria independentemente de qual tecnologia é usada para implementá-lo. É a parte mais interna do [[Application Core]].

## Por que existe?

Regras de negócio mudam por motivos de negócio, não por motivos técnicos. Isolar essas regras de detalhes técnicos permite que elas evoluam e sejam testadas sem depender de infraestrutura.

## Domain Logic vs. Business Logic vs. Application Logic vs. Infrastructure Logic

- **Domain / Business Logic**: as regras e invariantes essenciais do negócio (ex.: "um pedido não pode ser confirmado sem itens").
- **Application Logic**: a orquestração necessária para realizar uma operação completa (ex.: "buscar o pedido, validar, salvar, notificar") — normalmente vive nos [[Use Case]]s, não no Domain puro.
- **Infrastructure Logic**: detalhes técnicos de como algo é feito (SQL específico, formato de mensagem HTTP, protocolo de fila) — não deve influenciar o Domain.

## Por que regras de negócio não deveriam depender de infraestrutura?

Se o Domain depende diretamente de banco de dados, HTTP, frameworks, cloud providers ou message brokers, qualquer mudança nessas tecnologias força mudança nas regras de negócio, mesmo que a regra em si não tenha mudado. Isso também impede testar a regra de negócio sem subir essa infraestrutura.

## Quando alguma dependência pode ser aceitável?

Esta não é uma regra dogmática: bibliotecas puramente utilitárias e estáveis (ex.: uma biblioteca de manipulação de datas sem efeitos colaterais, ou tipos da própria linguagem como `java.time`) geralmente são aceitáveis dentro do Domain, pois não amarram o domínio a uma infraestrutura substituível. O critério prático é: "essa dependência me impede de testar ou trocar infraestrutura?".

## Exemplo

```java
// Domain: regra de negócio pura, sem infraestrutura
record Order(List<OrderItem> items, OrderStatus status) {
    Order confirm() {
        if (items.isEmpty()) {
            throw new IllegalStateException("Pedido sem itens não pode ser confirmado");
        }
        return new Order(items, OrderStatus.CONFIRMED);
    }
}
```

## Relações

- [[Application Core]]
- [[Use Case]]
- Entity, Value Object, Aggregate *(conceitos de DDD — ver gap registrado em [[Hexagonal Architecture]])*

## Referências

- Cockburn, Alistair. "Hexagonal Architecture", 2005: https://alistair.cockburn.us/hexagonal-architecture/
