---
type: architecture
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - moc
  - hexagonal-architecture
---

# Hexagonal Architecture

## O que é

Hexagonal Architecture — também chamada de **Ports and Adapters** (nome original dado por Alistair Cockburn, 2005) — é um estilo arquitetural que isola o núcleo de uma aplicação (regras de negócio) de tudo que é externo a ela (UI, banco de dados, frameworks, serviços de terceiros), permitindo que a aplicação seja "igualmente acionada por usuários, programas, testes automatizados ou scripts em lote", nas palavras do próprio Cockburn.

O termo "hexágono" é uma **representação conceitual, não uma exigência literal** de seis lados ou seis componentes — o número de lados não tem significado técnico; serve apenas para visualizar múltiplos pontos de entrada/saída ao redor de um núcleo.

## Problema

A motivação original de Cockburn (2005) era um problema recorrente: lógica de negócio "vazando" para a camada de interface (UI) e para a camada de acesso a dados. Isso causa, entre outros sintomas:

- **Acoplamento**: o núcleo do sistema passa a depender de detalhes de tecnologia (framework web, driver de banco).
- **Dificuldade de testes**: testar a regra de negócio exige subir UI, banco de dados ou outra infraestrutura real.
- **Dificuldade de substituir tecnologias**: trocar o banco de dados, o framework web, ou o provedor de nuvem exige alterar regras de negócio que, em princípio, não mudaram.
- **Domínio dependente de frameworks**: classes de domínio "presas" a anotações e convenções de um framework específico.
- **Dificuldade de evolução**: mudanças pequenas em um lado do sistema propagam para outros lados não relacionados.

## Ideia central

```
Application Core
      ↕
    Ports
      ↕
   Adapters
```

O [[Application Core]] não conhece nada além de si mesmo e das [[Ports]] que ele mesmo define. Os [[Adapters]] ficam do lado de fora, conectando o Core a tecnologias concretas. A direção das dependências de código é regida pela [[Dependency Rule]] — e é importante entender que essa direção **não é necessariamente igual** à direção da interação lógica em runtime (ver detalhes em [[Dependency Rule]]).

## Fundamentals

- [[Coupling]]
- [[Cohesion]]
- [[Dependency Inversion]]
- [[Dependency Injection]]
- [[SOLID]]

## Core

- [[Application Core]]
- [[Domain]]
- [[Use Case]]

## Ports

- [[Ports]] (cobre Driving/Primary/Input e Driven/Secondary/Output em uma única nota — mesmo conceito, nomenclaturas diferentes)

## Adapters

- [[Adapters]] (cobre Driving e Driven Adapters)

## Dependency Direction

- [[Dependency Rule]]

## Comparisons

- [[Hexagonal vs Clean vs Onion]]

## Ecosystem

- [[Java 21]] — ver seção "Java" abaixo.
- Spring Boot — ver seção "Ponte para Spring Boot" abaixo (sem aprofundar).
- DDD — ver seção "Relação com DDD" abaixo (sem aprofundar).

## Exemplo prático — Create Order

Exemplo pequeno, apenas para tornar a arquitetura concreta (não é uma aplicação completa):

```
HTTP Request
     ↓
REST Adapter (Driving Adapter)
     ↓
CreateOrder Port (Input Port)
     ↓
CreateOrder Use Case
     ↓
Domain (Order.confirm())
     ↓
OrderRepository Port (Output Port)
     ↓
Database Adapter (Driven Adapter)
     ↓
Database
```

```java
// Port (definida pelo Core)
interface CreateOrderPort {
    void execute(CreateOrderCommand command);
}

// Use Case (Core)
class CreateOrderUseCase implements CreateOrderPort {
    private final OrderRepository repository; // Output Port

    CreateOrderUseCase(OrderRepository repository) {
        this.repository = repository;
    }

    public void execute(CreateOrderCommand command) {
        Order order = new Order(command.items(), OrderStatus.PENDING).confirm();
        repository.save(order);
    }
}

// Driving Adapter (fora do Core)
class OrderRestController {
    private final CreateOrderPort createOrder;
    void handlePost(HttpRequest req) { createOrder.execute(toCommand(req)); }
}

// Driven Adapter (fora do Core)
class JdbcOrderRepository implements OrderRepository {
    public void save(Order order) { /* SQL aqui */ }
}
```

## Estrutura de projeto (uma possibilidade, não uma exigência)

```
src/
├── domain/
├── application/
│   ├── ports/
│   │   ├── in/
│   │   └── out/
│   └── services/
└── adapters/
    ├── in/
    └── out/
```

Esta estrutura de pastas é apenas **uma** forma possível de organizar o código. Hexagonal Architecture não exige essa árvore de diretórios — o que importa é responsabilidade, fronteiras e direção das dependências, não a posição física dos arquivos.

## Testabilidade

O Application Core depende apenas de Ports (interfaces). Isso permite testar o Core com um **test double** no lugar do Adapter real:

```
Application Core → Mock/Fake Adapter   (unit test: rápido, sem infraestrutura real)
Application Core → Real Database        (integration test: mais lento, valida integração real)
```

- **Unit tests**: testam o Domain/Use Case isoladamente, substituindo Ports por *mocks*, *stubs* ou *fakes*.
- **Integration tests**: validam um Adapter real contra a infraestrutura real (ex.: repositório contra um banco de teste).
- **Test doubles**: termo genérico para qualquer substituto de uma dependência real em teste (mock, stub, fake, spy).

## Trade-offs

Hexagonal Architecture **não é uma solução universal**. Custos reais a considerar:

- Mais interfaces e mais classes do que uma implementação direta.
- Complexidade inicial e overhead cognitivo para quem não está familiarizado com o estilo.
- Risco de overengineering: criar Ports para tudo, mesmo dependências estáveis que nunca serão trocadas.
- Pode ser difícil de adotar com qualidade em equipes sem maturidade arquitetural — a disciplina de manter o Core isolado não é imposta automaticamente pela linguagem.
- Para aplicações pequenas ou de vida curta, o benefício de isolamento pode não compensar o custo extra de abstração.

## Quando usar

- Sistemas com regras de negócio não triviais que precisam sobreviver a mudanças de tecnologia.
- Aplicações que precisam ser acionadas por múltiplas formas (HTTP, CLI, mensageria, testes automatizados).
- Quando testar regras de negócio isoladamente é uma prioridade.

## Quando evitar

- Protótipos, scripts ou aplicações muito simples e de vida curta, onde o overhead de abstração não se paga.
- Equipes sem experiência arquitetural, onde a disciplina de isolar o Core pode não ser sustentada, tornando as abstrações apenas burocracia sem benefício real.

## Java

```
Java 21
   ↓
Interfaces / Abstractions
   ↓
Ports
   ↓
Adapters
   ↓
Hexagonal Architecture
```

Recursos de [[Java 21]] que ajudam a expressar esta arquitetura:

- **Interfaces** — mecanismo direto para expressar [[Ports]].
- **[[Records]]** — bom ajuste para Value Objects e comandos/DTOs de entrada/saída de um [[Use Case]] (ex.: `CreateOrderCommand`).
- **[[Sealed Classes]]** — úteis para modelar um conjunto finito de resultados de um Use Case (ex.: sucesso/erro) quando fizer sentido.
- Exceptions — para sinalizar violação de invariantes do [[Domain]].

Esta base não repete o conteúdo de Java aqui — ver [[Java 21]] para os conceitos de linguagem em si.

## Ponte para Spring Boot

```
Hexagonal Architecture
        ↓
Dependency Injection
        ↓
Spring
        ↓
Spring Boot
```

Esta ponte foi aprofundada na Etapa 5 — ver [[Spring Boot + Hexagonal Architecture]] para os mapeamentos completos (`@RestController` → Driving Adapter, `@Service` → possível Use Case, Repository Port → Driven Port, Spring Data Repository → Driven Adapter) e a explicação de por que essas anotações são mecanismos do framework, não definições arquiteturais.

## Ponte para Azure e Observabilidade

```
Driven Adapter → External Infrastructure → Azure
```

Esta ponte foi aprofundada na Etapa 6 — ver [[Hexagonal Architecture + Azure]] para o mapeamento completo (Repository Port → Database Adapter → Azure SQL; Output Port → Storage Adapter → Blob Storage) e a explicação de por que Azure é infraestrutura externa e não deve ser uma dependência do [[Application Core]]. A ponte com Observabilidade foi aprofundada na Etapa 7 — ver [[Hexagonal Architecture + Observability]]: observabilidade é tratada como preocupação transversal, instrumentada nas bordas (Controllers/Adapters), sem entrar no Domain. Application Insights, Log Analytics e KQL permanecem para etapas futuras (8 e 9).

## Relação com DDD (sem aprofundar)

Hexagonal Architecture não exige Domain-Driven Design, mas coexiste bem com seus conceitos: Entity, Value Object, Aggregate, Domain Service, Repository e Bounded Context podem viver dentro do [[Domain]] e ser acessados através de [[Ports]]. Estes conceitos de DDD ainda não têm notas próprias nesta base — registrados como gap (ver relatório da Etapa 4).

## Relações

- [[Architecture]] (conceitos)
- [[Java]] (tecnologia)
- [[Hexagonal Architecture Learning Path]]
- [[Reference Architecture - Java Spring Azure]]
- [[Integration]]

## Referências

- Cockburn, Alistair. "Hexagonal Architecture", HaT Technical Report 2005.02: https://alistair.cockburn.us/hexagonal-architecture/
- Martin, Robert C. "The Clean Architecture", blog.cleancoder.com, 2012.
- Palermo, Jeffrey. "The Onion Architecture", jeffreypalermo.com, 2008.
