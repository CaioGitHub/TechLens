---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
---

# Foreign Function and Memory API

## O que é?

API (conhecida como FFM API) que permite programas Java interagirem com código nativo (fora da JVM) e memória fora da heap gerenciada pelo garbage collector. No Java 21, está em sua **terceira preview** (JEP 442).

## Problema

Bibliotecas de alta performance (ex.: bancos vetoriais, engines de dados) precisam de memória off-heap para evitar custo e imprevisibilidade do garbage collector, e frequentemente precisam chamar bibliotecas nativas (C/C++). A solução histórica, JNI, é frágil, verbosa e propensa a erros de segurança de memória; `sun.misc.Unsafe` é rápida mas não suportada oficialmente.

## Interação Java ↔ código nativo

A API permite invocar funções nativas (via `Linker`/`MethodHandle`) e acessar/alocar memória nativa (via `MemorySegment`/`Arena`) diretamente do Java, sem escrever código C intermediário (diferente de JNI, que exige stubs nativos).

## Memória fora da heap

`MemorySegment` representa uma região de memória (nativa ou não), com `Arena` controlando o ciclo de vida (quando a memória é liberada) de forma explícita — diferente de `ByteBuffer` direto, cuja liberação depende do garbage collector.

## Objetivo da API

Substituir JNI e `sun.misc.Unsafe` por um modelo de desenvolvimento seguro, em Java puro, com performance comparável.

## Relação com JNI

FFM API não reimplementa nem estende o JNI — é uma alternativa completa, com o objetivo de eventualmente reduzir a necessidade de JNI para a maioria dos casos de uso.

## Segurança

Operações nativas são inerentemente inseguras (podem corromper memória do processo), mas a API sinaliza isso explicitamente e por padrão avisa/exige opt-in para operações potencialmente perigosas, em vez de permiti-las silenciosamente como o `Unsafe`.

## Casos de uso

- Chamar bibliotecas nativas existentes (ex.: bibliotecas de sistema, drivers) sem escrever código C.
- Processar grandes volumes de dados fora da heap (evitando pressão sobre o GC) para cargas de trabalho performance-críticas.

## Status no Java 21

**Preview** (terceira preview, JEP 442). Histórico: incubou no Java 17/18 (como duas APIs separadas, depois unificadas), previu no Java 19 e 20, terceira preview no Java 21. **Finalizada apenas no Java 22** — fora do escopo desta base.

## Relações

- [[Java 18]] — incubava como JEP 419 (2ª incubação).
- [[Java 21]]
- [[JVM]]

## Referências

- JEP 442 — Foreign Function & Memory API (3ª Preview, Java 21): https://openjdk.org/jeps/442
- JEP 419 — Foreign Function & Memory API (2ª Incubação, Java 18): https://openjdk.org/jeps/419
