---
type: reference
status: understood
confidence: 75
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
---

# Java 18 vs Java 21

Comparação de referência rápida entre [[Java 18]] (feature release) e [[Java 21]] (LTS).

| Área | Java 18 | Java 21 |
|---|---|---|
| LTS | Não | Sim |
| Linguagem | Pattern Matching for switch (2ª preview) | Pattern Matching for switch (**Final**), Record Patterns (**Final**) |
| Concorrência | Sem mudanças relevantes | [[Virtual Threads]] (**Final**), [[Structured Concurrency]] (Preview), [[Scoped Values]] (Preview) |
| JVM | Reimplementação interna de reflection | Generational ZGC (Final) |
| APIs | Simple Web Server, UTF-8 by Default, Internet-Address Resolution SPI | [[Sequenced Collections]] (Final), [[String Templates]] (Preview) |
| Preview | Pattern Matching for switch | Structured Concurrency, Scoped Values, String Templates, Unnamed Patterns/Classes |
| Incubator | Vector API (3ª), Foreign Function & Memory API (2ª) | Vector API (6ª); FFM API saiu de incubator e virou Preview (3ª) |
| Principais impactos | Portabilidade (UTF-8), base para recursos futuros | Escalabilidade de concorrência, modelagem de dados mais expressiva |

## O que realmente mudou?

Entre Java 18 e Java 21, o maior salto não está em uma única feature, mas na consolidação do modelo de concorrência (Virtual Threads finalizadas) e da modelagem de dados (Records + Sealed Classes + Pattern Matching + Record Patterns trabalhando juntos).

## O que amadureceu?

- **Pattern Matching for switch**: preview no 17/18/19/20 → **Final no 21** (JEP 441).
- **Record Patterns**: preview no 19/20 → **Final no 21** (JEP 440).
- **Virtual Threads**: preview no 19/20 → **Final no 21** (JEP 444).
- **Foreign Function & Memory API**: incubator no 17/18, preview no 19/20/21 → finalizada apenas no Java 22 (fora do escopo desta base).

## Recursos que surgiram no período (18 → 21)

- Structured Concurrency (incubator no 19/20 → preview no 21).
- Scoped Values (incubator no 20 → preview no 21).
- Sequenced Collections (novo, direto como Final no 21).
- String Templates (novo, preview no 21).
- Generational ZGC (novo, Final no 21).

## Recursos que chegaram ao Java 21 finalizados

[[Virtual Threads]], [[Record Patterns]], [[Pattern Matching]] for switch, [[Sequenced Collections]], Generational ZGC.

## Recursos que ainda eram Preview no Java 21

[[Structured Concurrency]], [[Scoped Values]], [[String Templates]] (posteriormente retirado no Java 23), Foreign Function & Memory API (3ª preview), Unnamed Patterns and Variables, Unnamed Classes and Instance Main Methods.

## Por que Java 21 é importante?

É a primeira LTS a oferecer, de forma estável, um modelo de concorrência (Virtual Threads) que reduz drasticamente o custo de escrever código thread-per-request escalável, além de consolidar um estilo de modelagem de dados mais declarativo (records + sealed + pattern matching).

## Para um projeto backend, o que importa?

- Adotar [[Virtual Threads]] para workloads I/O-bound (chamadas HTTP, banco de dados) pode simplificar código concorrente sem reescrever a aplicação para um modelo reativo.
- [[Record Patterns]] e [[Pattern Matching]] simplificam a manipulação de estruturas de dados imutáveis (DTOs, eventos).
- Recursos ainda em Preview (Structured Concurrency, Scoped Values, String Templates) não devem ser usados em produção sem avaliação de risco — APIs podem mudar ou, como no caso de String Templates, ser retiradas.

## Relações

- [[Java 18]]
- [[Java 21]]
- [[Java 18-21 Learning Path]]

## Referências

- Ver referências detalhadas em [[Java 18]] e [[Java 21]].
