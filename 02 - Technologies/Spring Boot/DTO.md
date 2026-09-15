---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# DTO

## O que é?

DTO (Data Transfer Object) é um objeto simples usado para transportar dados **entre a borda da aplicação (ex.: HTTP) e o restante do sistema**, sem expor diretamente as classes de domínio.

## Por que existe?

O formato de entrada/saída de uma API (JSON de uma requisição HTTP) frequentemente não deve ser o mesmo formato do modelo de domínio: a API pode precisar de campos diferentes, validações estruturais próprias, ou versionamento independente do domínio.

## Diferença entre DTO e Domain Object

| | DTO | Domain Object |
|---|---|---|
| Propósito | Transporte de dados na borda | Representar regras/invariantes de negócio |
| Comportamento | Tipicamente anêmico (poucos ou nenhum método além de acesso a dados) | Pode conter comportamento (ex.: `Order.confirm()`) |
| Estabilidade | Pode mudar por motivo de API/contrato externo | Muda por motivo de regra de negócio |
| Local típico | Borda do Adapter (ex.: pacote `adapters/in/web`) | [[Domain]] |

## Fluxo conceitual

```
HTTP (JSON)
   ↓
DTO (CreateOrderRequest)
   ↓
Mapper (DTO → Command/objeto de domínio)
   ↓
Use Case
   ↓
Domain (Order)
```

## Exemplo (Java 21 — record como DTO)

```java
record CreateOrderRequest(List<OrderItemRequest> items) {
    CreateOrderCommand toCommand() {
        return new CreateOrderCommand(items.stream().map(OrderItemRequest::toItem).toList());
    }
}
```

[[Records]] são um bom ajuste para DTOs: imutáveis, sem boilerplate de getters/equals/hashCode.

## DTO é obrigatório?

Não. Para aplicações muito simples, onde não há necessidade real de desacoplar o contrato de API do modelo de domínio, usar o próprio objeto de domínio na borda pode ser uma escolha aceitável — introduzir DTOs sem necessidade real é um custo extra de mapeamento e classes.

## Relações

- [[Spring REST]]
- [[Domain]]
- [[Adapters]]
- [[Records]]
- [[Spring Validation]]

## Referências

- Fowler, Martin. *Patterns of Enterprise Application Architecture*, 2002 — "Data Transfer Object".
