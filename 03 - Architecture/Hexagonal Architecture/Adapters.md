---
type: concept
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - hexagonal-architecture
---

# Adapters

## O que é?

Um Adapter é uma implementação concreta que conecta uma [[Ports|Port]] do [[Application Core]] a uma tecnologia específica do mundo externo (um framework web, um banco de dados, uma fila de mensagens).

## Por que existe?

Para que o conhecimento sobre "como" se comunicar com uma tecnologia específica (protocolo HTTP, SQL, formato de mensagem) fique isolado fora do Core, que só conhece o contrato abstrato (a Port).

## Como implementa uma Port

Um Adapter implementa (ou consome) a assinatura definida por uma Port, traduzindo entre o "mundo externo" e a linguagem do Core.

## Como protege o Core contra detalhes externos

O Core nunca importa uma classe de Adapter. A dependência de código sempre aponta do Adapter para a Port (ver [[Dependency Rule]]), nunca o contrário — mesmo quando o Adapter é quem *aciona* o Core (caso dos Driving Adapters).

## Driving Adapters (lado que aciona a aplicação)

Traduzem um estímulo externo (uma requisição HTTP, um comando de CLI, uma mensagem recebida) para uma chamada ao Input Port. Exemplos conceituais: REST Controller, CLI, messaging consumer, UI, event listener.

```java
class OrderRestController { // Driving Adapter
    private final CreateOrderPort createOrder; // Input Port

    void handlePost(HttpRequest req) {
        var command = toCommand(req);
        createOrder.execute(command);
    }
}
```

## Driven Adapters (lado que a aplicação aciona)

Implementam um Output Port definido pelo Core para acessar um recurso externo. Exemplos conceituais: Database Repository, HTTP Client, Message Broker, File System, External API.

```java
class JdbcOrderRepository implements OrderRepository { // Driven Adapter
    public void save(Order order) {
        // detalhes de SQL/JDBC aqui, isolados do Core
    }
}
```

## Nomenclaturas equivalentes

Driving Adapter costuma ser referido também como Primary Adapter; Driven Adapter como Secondary Adapter. Mesmo conceito, vocabulário diferente.

## Relações

- [[Ports]]
- [[Application Core]]
- [[Dependency Rule]]
- [[Hexagonal Architecture]]

## Referências

- Cockburn, Alistair. "Hexagonal Architecture", 2005: https://alistair.cockburn.us/hexagonal-architecture/
