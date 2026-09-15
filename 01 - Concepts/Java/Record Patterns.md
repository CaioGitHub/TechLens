---
type: concept
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
---

# Record Patterns

## O que é?

Record Patterns (Final no Java 21, JEP 440) estendem o pattern matching para **desestruturar** um `record`, extraindo seus componentes diretamente no próprio pattern, inclusive de forma aninhada. É um recurso distinto de [[Pattern Matching]] for switch, mas os dois co-evoluíram e são usados em conjunto.

## Por que existe?

Sem record patterns, extrair os componentes de um record via `instanceof`/`switch` ainda exigia chamar cada accessor manualmente após o teste de tipo. Record patterns eliminam essa etapa intermediária.

## Como funciona?

```java
record Point(int x, int y) {}

// Antes (Java 16+): apenas type pattern
if (obj instanceof Point p) {
    int x = p.x();
    int y = p.y();
}

// Com Record Pattern (Java 21, Final):
if (obj instanceof Point(int x, int y)) {
    System.out.println(x + y);
}
```

Patterns aninhados permitem decompor object graphs inteiros:

```java
record Point(int x, int y) {}
enum Color { RED, GREEN, BLUE }
record ColoredPoint(Point p, Color c) {}
record Rectangle(ColoredPoint upperLeft, ColoredPoint lowerRight) {}

static void printUpperLeftColor(Rectangle r) {
    if (r instanceof Rectangle(ColoredPoint(Point p, Color c), var lowerRight)) {
        System.out.println(c);
    }
}
```

## Quando usar?

- Ao processar estruturas de dados imutáveis compostas por vários `record`s aninhados (árvores, eventos compostos, mensagens estruturadas).
- Em conjunto com `switch` sobre hierarquias `sealed` de records.

## Quando evitar?

- Para objetos simples com poucos componentes, onde o ganho de legibilidade é marginal.

## Limitações conhecidas

A versão final (Java 21) removeu, em relação à segunda preview, o suporte a record patterns no cabeçalho de um `for` aprimorado (`for (Point(var x, var y) : points)`) — esse uso pode ser reproposto em versão futura.

## Relações

- [[Pattern Matching]]
- [[Records]]
- [[Sealed Classes]]
- [[Java 21]] — finalização (era preview no Java 19 e 20).

## Referências

- JEP 405 — Record Patterns (Preview, Java 19): https://openjdk.org/jeps/405
- JEP 432 — Record Patterns (2nd Preview, Java 20): https://openjdk.org/jeps/432
- JEP 440 — Record Patterns (Final, Java 21): https://openjdk.org/jeps/440
