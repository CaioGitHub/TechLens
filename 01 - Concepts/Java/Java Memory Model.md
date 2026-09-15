---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
  - concurrency
---

# Java Memory Model

## O que é?

O Java Memory Model (JMM) é a especificação formal (definida na Java Language Specification, capítulo 17) que define **quando** uma escrita feita por uma thread se torna visível para outra thread, e quais reordenações de operações de memória o compilador/JIT/CPU têm permissão de fazer.

## Memória e threads

Cada thread pode manter valores em registradores/caches de CPU antes de "publicá-los" na memória principal. Sem regras explícitas, uma thread B pode nunca enxergar uma escrita feita por uma thread A, ou enxergá-la fora de ordem.

## Visibilidade

Visibilidade é a garantia de que uma escrita em uma variável, feita por uma thread, seja observável por outra thread. Não é automática em Java — requer mecanismos como `volatile`, `synchronized` ou classes de `java.util.concurrent`.

## Atomicidade

Uma operação é atômica quando é executada por completo, sem intercalação parcial visível a outras threads. Operações compostas (`i++`) não são atômicas mesmo que pareçam uma única instrução.

## Ordenação

O compilador, o JIT e a CPU podem reordenar instruções para otimizar performance, desde que o comportamento observado por uma única thread não mude. Essa reordenação pode, porém, ser observável por outras threads na ausência de sincronização.

## Happens-before

O conceito central do JMM: se uma ação A "happens-before" uma ação B, então os efeitos de A são garantidamente visíveis para B. Relações de happens-before são estabelecidas, por exemplo, por: liberar um lock antes de outra thread adquiri-lo; escrever em uma variável `volatile` antes de outra thread lê-la; o término de uma thread antes de outra fazer `join()` nela.

## volatile

Declarar um campo como `volatile` garante visibilidade (toda leitura vê a escrita mais recente) e impede certas reordenações — mas **não** garante atomicidade de operações compostas.

## synchronized

Um bloco/método `synchronized` garante exclusão mútua (apenas uma thread por vez) e também estabelece uma relação happens-before entre a liberação e a aquisição do mesmo lock.

## Locks

Implementações explícitas de `java.util.concurrent.locks` (ex.: `ReentrantLock`) oferecem garantias semelhantes a `synchronized`, com mais flexibilidade (tentativa com timeout, interruptibilidade).

## Race conditions

Uma race condition ocorre quando o resultado de um programa depende da ordem não controlada de execução de operações concorrentes sobre dados compartilhados, geralmente por ausência de sincronização adequada.

## Relação com Virtual Threads

[[Virtual Threads]] não alteram o Java Memory Model — as mesmas regras de visibilidade, atomicidade e happens-before se aplicam integralmente. O que muda é apenas *como* as threads são escalonadas pela JVM, não o modelo de memória que rege a comunicação entre elas.

## Relações

- [[Concurrency]]
- [[Virtual Threads]]
- [[JVM]]

## Referências

- Java Language Specification, Chapter 17 (Threads and Locks): https://docs.oracle.com/javase/specs/jls/se21/html/jls-17.html
