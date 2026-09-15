---
type: study
status: learning
confidence: 30
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
---

# Java 18-21 Learning Path

## O que quero entender?

Uma sequência de estudo lógica para dominar o intervalo Java 18 → Java 21, dos fundamentos até os recursos mais modernos de concorrência e JVM.

## Resumo

Roteiro organizado em 5 níveis, do mais fundamental ao mais avançado. Cada item aponta para a nota correspondente (quando existente nesta base).

### Nível 1 — Fundamentos

- Classes
- Interfaces
- Collections
- Exceptions
- Generics

*(notas fundamentais ainda não criadas nesta base — candidatas a Inbox/futura criação)*

### Nível 2 — Java moderno

- [[Records]]
- [[Sealed Classes]]
- [[Pattern Matching]]
- [[Record Patterns]]
- Streams *(nota ainda não criada)*

### Nível 3 — Concorrência

- [[Concurrency]]
- [[Java Memory Model]]
- CompletableFuture *(a aprofundar dentro de [[Concurrency]])*

### Nível 4 — Java 21

- [[Virtual Threads]]
- [[Structured Concurrency]]
- [[Scoped Values]]
- [[Sequenced Collections]]

### Nível 5 — JVM

- [[JVM]]
- Java Memory Model (ver [[Java Memory Model]])
- Garbage Collection e JIT *(aprofundar dentro de [[JVM]] quando houver conteúdo suficiente para notas próprias)*

## Conceitos importantes

A ordem importa: Pattern Matching e Record Patterns dependem de entender Records e Sealed Classes primeiro; Virtual Threads e Structured Concurrency dependem de entender o modelo de concorrência tradicional (threads, executors) e o Java Memory Model.

## Exemplo prático

Sequência sugerida de exercícios: modelar um domínio simples com `record` + `sealed interface` + `switch` com pattern matching; depois reescrever um fluxo de chamadas HTTP concorrentes usando Virtual Threads + Structured Concurrency.

## O que aprendi?

*(a preencher conforme o estudo avança)*

## Dúvidas

*(a preencher conforme o estudo avança)*

## Próximos passos

Avaliar a criação de notas de Nível 1 (Fundamentos) caso a base identifique lacunas relevantes durante o uso prático.

## Relações

- [[Java 18]]
- [[Java 21]]
- [[Java 18 vs Java 21]]

## Referências

- Ver referências detalhadas nas notas individuais de cada conceito.
