---
type: concept
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
---

# Sequenced Collections

## O que é?

**Final no Java 21** (JEP 431). Um conjunto de novas interfaces (`SequencedCollection`, `SequencedSet`, `SequencedMap`) que representam coleções com **ordem de encontro definida** (encounter order): primeiro elemento, segundo elemento, ..., último elemento — e operações uniformes sobre essa ordem.

## Problema

Antes do Java 21, o framework de coleções não tinha um tipo comum para representar "coleção com ordem definida". `List` e `Deque` têm ordem, mas seu supertipo comum é `Collection`, que não garante ordem. Operações básicas como "pegar o primeiro elemento" ou "iterar em ordem reversa" eram implementadas de forma inconsistente em cada tipo (`list.get(0)`, `deque.getFirst()`, `sortedSet.first()`, e para `LinkedHashSet` nem havia forma direta de pegar o último elemento).

## Conceito

As novas interfaces adicionam métodos default uniformes:

```java
interface SequencedCollection<E> extends Collection<E> {
    SequencedCollection<E> reversed();
    void addFirst(E e);
    void addLast(E e);
    E getFirst();
    E getLast();
    E removeFirst();
    E removeLast();
}
```

## Relação com List, Set e Map

- `List` agora implementa `SequencedCollection` (já tinha ordem, ganha os métodos uniformes).
- `Deque` também implementa `SequencedCollection`.
- `LinkedHashSet` passa a implementar `SequencedSet` — agora é possível obter o último elemento ou iterar em ordem reversa sem copiar a coleção inteira.
- `SortedSet`/`SortedMap` (e implementações como `TreeMap`) passam a implementar `SequencedSet`/`SequencedMap`.
- `HashSet`/`HashMap` **não** implementam essas interfaces, pois não têm ordem de encontro definida.

## Ordenação

`reversed()` retorna uma **view** da coleção original em ordem reversa (não uma cópia), refletindo mudanças futuras na coleção original.

## Casos de uso

- Obter o primeiro/último elemento de um `LinkedHashSet` ou `LinkedHashMap` sem código auxiliar.
- Iterar em ordem reversa de forma uniforme, independente do tipo concreto de coleção.

## Status no Java 21

**Final** — recurso novo, sem histórico de preview/incubação.

## Relações

- [[Java 21]]
- [[Concurrency]] *(não diretamente relacionado, mas parte do mesmo período de evolução das APIs)*

## Referências

- JEP 431 — Sequenced Collections (Final, Java 21): https://openjdk.org/jeps/431
