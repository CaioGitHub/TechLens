---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
  - hexagonal-architecture
---

# Spring Boot Anti-Patterns

## Objetivo

Registrar problemas comuns quando Spring Boot é usado sem atenção às fronteiras arquiteturais — cada um explicado pelo **porquê** é um problema, não apenas listado.

## Anemic Architecture

Classes de domínio sem nenhum comportamento (apenas getters/setters), com toda a lógica de negócio "vazada" para services ou controllers. Problema: perde-se o benefício de encapsular invariantes no próprio [[Domain]] — regras de negócio ficam espalhadas e duplicáveis.

## Fat Controllers

`@RestController` com lógica de negócio, validação de domínio e acesso a dados diretamente dentro do método do controller. Problema: mistura a responsabilidade de tradução HTTP (Driving Adapter) com orquestração de aplicação e regra de negócio — dificulta testar e reutilizar a lógica por outro tipo de Driving Adapter.

## Fat Services / God Service

Uma única classe `@Service` acumulando responsabilidades de múltiplos casos de uso não relacionados. Problema: baixa [[Cohesion]] — mudanças em uma responsabilidade arriscam quebrar outra não relacionada.

## Repository Leakage

Expor diretamente um `Spring Data Repository` (ou seu tipo de entidade JPA) para camadas externas ao invés de passar por uma Port/DTO. Problema: acopla consumidores externos a detalhes de persistência (ver [[Spring Data Repository vs Repository Port]]).

## Framework Coupling

Classes de [[Domain]] ou [[Use Case]] anotadas extensivamente com anotações do Spring, JPA, ou outras bibliotecas de infraestrutura, misturando regra de negócio com metadados técnicos. Problema: dificulta testar sem subir o framework e acopla o Core a decisões de infraestrutura que podem mudar.

## Domain depending directly on infrastructure

O Domain importa diretamente classes de banco de dados, HTTP, ou SDKs de nuvem. Problema: viola a [[Dependency Rule]] — qualquer troca de infraestrutura passa a exigir mudança em regra de negócio que não mudou.

## Excessive interfaces

Criar uma Port/interface para toda e qualquer classe, inclusive dependências estáveis que nunca serão substituídas ou mockadas. Problema: overengineering — mais indireção sem benefício real de desacoplamento (ver trade-offs em [[Hexagonal Architecture]]).

## Overuse of @Autowired (field injection)

Injeção de dependência via campo (`@Autowired private X x;`) espalhada por muitas classes. Problema: dificulta identificar dependências obrigatórias, dificulta testes unitários sem o container Spring, e permite estados parcialmente inicializados. Ver preferência por constructor injection em [[Dependency Injection]] (nota de `01 - Concepts/Architecture`).

## Business logic inside Controllers / Persistence Adapters

Regra de negócio (ex.: "pedido não pode ser confirmado sem itens") implementada dentro de um `@RestController` ou dentro de um adapter de persistência. Problema: a regra fica presa a um único ponto de entrada/saída específico, em vez de valer para qualquer forma de acionar a aplicação.

## DTO leaking into Domain

Um DTO da camada web (ex.: `CreateOrderRequest`) sendo usado diretamente como parâmetro de um método do [[Domain]]. Problema: acopla o Domain ao formato de uma API específica — mudanças no contrato HTTP forçam mudança em classes de domínio.

## Relações

- [[Spring Boot + Hexagonal Architecture]]
- [[Dependency Rule]]
- [[Domain]]
- [[Use Case]]

## Referências

- Martin, Robert C. *Clean Architecture*, 2017.
- Cockburn, Alistair. "Hexagonal Architecture", 2005.
