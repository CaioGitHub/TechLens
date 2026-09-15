---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - hexagonal-architecture
---

# Use Case

## O que é?

Um Use Case (caso de uso) — também chamado de Application Service em algumas nomenclaturas — representa uma operação completa e significativa que a aplicação oferece, orquestrando o [[Domain]] para realizá-la (ex.: "criar pedido", "cancelar assinatura").

## Qual responsabilidade possui?

Coordenar: receber a intenção (via um [[Ports|Input Port]]), acionar as regras do Domain, e usar [[Ports|Output Ports]] quando precisar de algo externo (persistir, notificar, consultar outro serviço). O Use Case **não** deve conter regra de negócio complexa — essa fica no Domain; ele orquestra.

## Relação com Application Service

Em muitas implementações, "Use Case" e "Application Service" são tratados como sinônimos ou como o mesmo papel arquitetural com nomes diferentes conforme o autor/framework. Não trate como duas camadas distintas a menos que a implementação específica realmente as separe.

## Relação com Domain

O Use Case não substitui o Domain — ele o invoca. Regras invariantes de negócio (ex.: "pedido não pode ser confirmado sem itens") pertencem ao Domain; a sequência de passos para realizar a operação (buscar, validar, persistir, notificar) pertence ao Use Case.

## Relação com Ports e Adapters

```
Driving Adapter
      ↓
Input Port
      ↓
Use Case / Application Service
      ↓
Domain
      ↓
Output Port
      ↓
Driven Adapter
```

Esta representação é conceitual — implementações reais podem combinar ou renomear essas etapas.

## Exemplo

```java
interface CreateOrderPort { // Input Port
    void execute(CreateOrderCommand command);
}

class CreateOrderUseCase implements CreateOrderPort {
    private final OrderRepository repository; // Output Port

    CreateOrderUseCase(OrderRepository repository) {
        this.repository = repository;
    }

    public void execute(CreateOrderCommand command) {
        Order order = new Order(command.items(), OrderStatus.PENDING);
        Order confirmed = order.confirm(); // regra de negócio no Domain
        repository.save(confirmed);
    }
}
```

## Relações

- [[Domain]]
- [[Ports]]
- [[Application Core]]
- [[Hexagonal Architecture]]

## Referências

- Cockburn, Alistair. "Hexagonal Architecture", 2005: https://alistair.cockburn.us/hexagonal-architecture/
