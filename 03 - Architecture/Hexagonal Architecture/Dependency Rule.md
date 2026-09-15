---
type: concept
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - hexagonal-architecture
---

# Dependency Rule

## O que é?

A Dependency Rule (regra de dependência) define que **dependências de código** devem sempre apontar de fora para dentro — de [[Adapters]] para [[Ports]], e de Ports para o [[Application Core]] — nunca o contrário.

## Por que existe?

Para garantir que o Core não conheça, em tempo de compilação, nenhuma classe concreta de infraestrutura. Isso é o que efetivamente isola o Core e permite substituir tecnologia sem alterá-lo.

## Como funciona?

```
External World
      ↓
   Adapters
      ↓
    Ports
      ↓
Application Core
```

Esse diagrama representa a direção das **dependências de código** (imports, referências de classe) — não necessariamente a direção da interação lógica em tempo de execução.

## Ponto central: direção lógica ≠ direção de código

Este é o ponto mais frequentemente confundido na arquitetura. Considere um Driving Adapter (ex.: REST Controller) que aciona o Core:

- **Interação lógica em runtime**: `Adapter → Core` (o adapter chama o método do caso de uso).
- **Dependência de código**: o Adapter importa/referencia a interface do Input Port (que pertence ao Core); o **Core nunca importa o Adapter**.

Já para um Driven Adapter (ex.: repositório de banco):

- **Interação lógica em runtime**: `Core → Adapter` (o caso de uso chama `repository.save(...)`).
- **Dependência de código**: mesmo assim, o Adapter é quem importa/implementa a interface (Output Port) definida pelo Core — a dependência de código continua apontando do Adapter para o Core, mesmo que a chamada em runtime vá na direção oposta.

Isso é possível graças a [[Dependency Inversion]]: o Core define a abstração (Port); quem depende dela em código é sempre quem está "fora".

## Exemplo

```java
// Core define a Port (não depende de nada externo)
interface OrderRepository {
    void save(Order order);
}

// Adapter depende do Core (implementa a interface do Core), nunca o contrário
class JdbcOrderRepository implements OrderRepository {
    public void save(Order order) { /* ... */ }
}
```

Mesmo que, em runtime, seja o `CreateOrderUseCase` (Core) quem *chama* `repository.save(order)` (ou seja, aciona o Adapter), a dependência de **código** (`implements OrderRepository`) aponta do Adapter para o Core.

## Relações

- [[Dependency Inversion]]
- [[Ports]]
- [[Adapters]]
- [[Application Core]]
- [[Hexagonal Architecture]]

## Referências

- Cockburn, Alistair. "Hexagonal Architecture", 2005: https://alistair.cockburn.us/hexagonal-architecture/
- Martin, Robert C. *Clean Architecture*, 2017 — capítulo sobre "The Dependency Rule".
