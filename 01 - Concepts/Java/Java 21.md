---
type: concept
status: understood
confidence: 75
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
---

# Java 21

## Overview

Java 21 é uma release **LTS (Long-Term Support)**, lançada em 19/09/2023 sob a JSR 396. É considerada uma das versões LTS mais importantes desde o Java 17: finaliza recursos que vinham em preview há várias versões (Virtual Threads, Pattern Matching for switch, Record Patterns) e introduz a primeira preview de um novo modelo de concorrência estruturada (Structured Concurrency, Scoped Values). Para times backend, representa o primeiro LTS onde vale a pena avaliar seriamente a adoção de Virtual Threads em produção.

## Principais novidades

Recursos com atenção especial e seu status **exato** no Java 21 (não presuma "Final" apenas por estar no release):

| Recurso | Status no Java 21 | Nota |
|---|---|---|
| [[Virtual Threads]] | **Final** (JEP 444) | Preview no 19 e 20 |
| [[Record Patterns]] | **Final** (JEP 440) | Preview no 19 e 20 |
| [[Pattern Matching]] for switch | **Final** (JEP 441) | Preview desde o 17 |
| [[Sequenced Collections]] | **Final** (JEP 431) | Novo no 21 |
| [[Structured Concurrency]] | **Preview** (JEP 453) | Incubando no 19 e 20 |
| [[Scoped Values]] | **Preview** (JEP 446) | Incubando no 20 |
| [[String Templates]] | **Preview** (JEP 430) | Posteriormente **retirado** no Java 23 |
| [[Foreign Function and Memory API]] | **Preview** (JEP 442, 3ª preview) | Finalizada só no Java 22 |
| Vector API | **Incubator** (JEP 448, 6ª incubação) | Ainda incubando |
| Unnamed Patterns and Variables | Preview (JEP 443) | Não aprofundado nesta base |
| Unnamed Classes and Instance Main Methods | Preview (JEP 445) | Não aprofundado nesta base |
| Generational ZGC | Final (JEP 439) | Coletor de lixo, não default |

## JVM

- **JEP 439 — Generational ZGC**: o coletor ZGC passa a suportar gerações (objetos jovens vs. antigos), reduzindo overhead de coleta e melhorando throughput/latência em relação ao ZGC não-geracional. Não é o coletor padrão do JDK 21.
- Virtual Threads exigiram mudanças internas na JVM para suportar milhões de threads leves (ver [[JVM]] e [[Virtual Threads]]).

## Concorrência

Java 21 é o marco mais importante em concorrência desde `java.util.concurrent` (Java 5):

- [[Virtual Threads]] — finalizadas, base para o modelo thread-per-request escalável.
- [[Structured Concurrency]] — preview; trata grupos de tarefas relacionadas como uma unidade só, simplificando cancelamento e propagação de erros.
- [[Scoped Values]] — preview; alternativa a `ThreadLocal` pensada para funcionar bem com grande número de virtual threads.

## APIs

- [[Sequenced Collections]] — finalizada; preenche uma lacuna histórica no framework de coleções (acesso uniforme a primeiro/último elemento e iteração reversa).
- [[String Templates]] — preview; interpolação de strings segura. **Atenção**: teve sua preview retirada no Java 23 por reprojeto, então não deve ser tratada como caminho estável.
- [[Foreign Function and Memory API]] — terceira preview; substituta moderna do JNI.

## Preview

- **Structured Concurrency (JEP 453)** — preview. Motivo: API ainda em consolidação (mudança de `fork()` retornando `Subtask` em vez de `Future`). Evoluiu em versões posteriores ao 21.
- **Scoped Values (JEP 446)** — preview. Motivo: saiu de incubação (JDK 20) para preview, ainda sujeita a mudanças de API.
- **String Templates (JEP 430)** — preview. Foi reprevisada no JDK 22 (JEP 459) e **retirada** no JDK 23 por problemas de design (modelo baseado em "template processors" considerado confuso).
- **Foreign Function and Memory API (JEP 442)** — terceira preview; finalizada apenas no Java 22.

## Incubator

- **Vector API (JEP 448, sexta incubação)** — API para operações vetoriais explorando SIMD; segue incubando além do Java 21.

## JEPs relevantes

| JEP | Nome | Área | Status no 21 |
|---|---|---|---|
| 430 | String Templates | Linguagem | Preview (depois retirada) |
| 431 | Sequenced Collections | APIs | Final |
| 439 | Generational ZGC | JVM/GC | Final |
| 440 | Record Patterns | Linguagem | Final |
| 441 | Pattern Matching for switch | Linguagem | Final |
| 442 | Foreign Function & Memory API (3ª preview) | APIs | Preview |
| 444 | Virtual Threads | Concorrência | Final |
| 446 | Scoped Values | Concorrência | Preview |
| 448 | Vector API (6ª incubação) | APIs/Performance | Incubator |
| 453 | Structured Concurrency | Concorrência | Preview |

## Relações

- [[Java 18]]
- [[Java 18 vs Java 21]]
- [[Virtual Threads]]
- [[Structured Concurrency]]
- [[Scoped Values]]
- [[Record Patterns]]
- [[Pattern Matching]]
- [[Sequenced Collections]]
- [[Integration]] — visão end-to-end conectando Java 21 a Spring Boot, Azure e Observabilidade
- [[JVM]]
- [[Concurrency]]

## Referências

- JEP 430: https://openjdk.org/jeps/430
- JEP 431: https://openjdk.org/jeps/431
- JEP 439: https://openjdk.org/jeps/439
- JEP 440: https://openjdk.org/jeps/440
- JEP 441: https://openjdk.org/jeps/441
- JEP 442: https://openjdk.org/jeps/442
- JEP 444: https://openjdk.org/jeps/444
- JEP 446: https://openjdk.org/jeps/446
- JEP 448: https://openjdk.org/jeps/448
- JEP 453: https://openjdk.org/jeps/453
- OpenJDK — JDK 21 project page: https://openjdk.org/projects/jdk/21/
