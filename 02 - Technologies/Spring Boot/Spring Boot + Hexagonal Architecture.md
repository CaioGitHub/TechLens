---
type: architecture
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
  - hexagonal-architecture
---

# Spring Boot + Hexagonal Architecture

## Objetivo desta nota

Mostrar como usar os mecanismos do Spring Boot **sem deixar o framework definir sozinho a arquitetura da aplicação** — a pergunta central da Etapa 5.

## A ponte

```
                  Spring Boot
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
      Web/MVC          DI          Data
          │            │            │
          ↓            ↓            ↓
Driving Adapter   Composition   Driven Adapter
          │            │            │
          └────────────┼────────────┘
                       ↓
                 Application Core
                       │
                 ┌─────┴─────┐
                 ↓           ↓
               Domain     Use Cases
```

Spring Boot fornece a infraestrutura de execução (web, container de DI, acesso a dados); a Arquitetura Hexagonal decide **onde** essa infraestrutura tem permissão para tocar o sistema.

## Mapeamentos possíveis (exemplos, não regras obrigatórias)

| Mecanismo do Spring | Papel arquitetural possível |
|---|---|
| `@RestController` | [[Adapters\|Driving Adapter]] |
| Uma interface de Use Case | [[Ports\|Input Port]] |
| `@Service` | Application Service / [[Use Case]] |
| Interface de repositório definida pelo Core | [[Ports\|Driven/Output Port]] |
| `Spring Data Repository` (`JpaRepository`, etc.) | [[Adapters\|Driven Adapter]] (ver [[Spring Data Repository vs Repository Port]]) |

## IMPORTANTE — o que esta nota NÃO afirma

> "`@Service` significa Application Service."

Isso seria uma generalização incorreta. `@Service` é apenas um mecanismo do Spring para **registrar** um Bean no container (ver [[Component Scanning]]) — semanticamente uma dica de intenção, não uma garantia arquitetural. A classe anotada com `@Service` **pode** desempenhar o papel de Use Case se for desenhada para isso (orquestrar o Domain via Ports); ou pode, na prática, virar um "God Service" com lógica de infraestrutura misturada (ver [[Spring Boot Anti-Patterns]]). A responsabilidade arquitetural depende do desenho da aplicação, não do nome da anotação.

## Direção das dependências com Spring no jogo

```
Framework
    ↓
Adapters
    ↓
Ports
    ↓
Application Core
```

A dependência de **código** deve continuar apontando de fora para dentro (ver [[Dependency Rule]]), mesmo com Spring envolvido:

```
Core
├── Domain          → sem imports do Spring
├── Use Cases        → sem imports do Spring (idealmente)
└── Ports            → interfaces puras Java, sem imports do Spring
        ↑
        │ (implementam/consomem)
Adapters
├── REST (@RestController)         → depende do Spring MVC
├── Database (Spring Data Adapter)  → depende do Spring Data
└── Messaging                       → depende do broker escolhido
```

Manter o Core livre de anotações do Spring (`@Service`, `@Component`, `@Autowired`) é uma escolha de design — não uma exigência absoluta do Spring nem da Arquitetura Hexagonal. É perfeitamente possível usar `@Service` diretamente numa classe de Use Case sem imports de infraestrutura pesada (a anotação em si não força acoplamento a banco/HTTP); o risco real está em deixar lógica de acesso a dados ou de protocolo web vazar para dentro dessa classe.

## Exemplo completo — Order API

```
REST Controller (@RestController)
      ↓
CreateOrderUseCase (@Service, implementa CreateOrderPort)
      ↓
Domain (Order.confirm())
      ↓
OrderRepository (Port, interface pura)
      ↓
Persistence Adapter (implementa OrderRepository usando Spring Data)
      ↓
Database
```

```
Spring Boot participa via:
├── REST (Spring MVC — Driving Adapter)
├── Dependency Injection (container resolve CreateOrderUseCase → OrderRepository → Adapter)
├── Configuration (application.yml, @Configuration quando necessário)
├── Persistence (Spring Data — Driven Adapter)
└── Testing (Spring Test — testes de integração dos Adapters)
```

O `Application Core` (Domain + Use Case + Ports) permanece, neste desenho, sem depender diretamente de bibliotecas de infraestrutura pesada — apenas de interfaces que ele mesmo define.

## Relações

- [[Hexagonal Architecture]]
- [[Ports]]
- [[Adapters]]
- [[Dependency Rule]]
- [[Component Scanning]]
- [[Spring Data Repository vs Repository Port]]
- [[Spring Boot Anti-Patterns]]

## Referências

- Cockburn, Alistair. "Hexagonal Architecture", 2005.
- Spring Framework Reference Documentation: https://docs.spring.io/spring-framework/reference/
