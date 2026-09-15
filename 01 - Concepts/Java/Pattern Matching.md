---
type: concept
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
---

# Pattern Matching

## O que é?

"Pattern Matching" no Java é uma família de recursos que permite testar uma expressão contra uma forma/padrão (não apenas um tipo) e extrair dados dessa forma se o teste passar. Engloba, nesta base, dois recursos relacionados que evoluíram juntos: **Pattern Matching for `instanceof`** (Final desde o Java 16, JEP 394) e **Pattern Matching for `switch`** (Final apenas no Java 21, JEP 441). A desestruturação de records dentro de patterns é tratada na nota separada [[Record Patterns]].

## Por que existe?

Para eliminar o idioma repetitivo "testar tipo + fazer cast" e para permitir que `switch` deixe de ser limitado a comparações de igualdade contra constantes, suportando lógica de "múltiplas formas possíveis" de maneira concisa e seguindo verificação de exaustividade pelo compilador.

## Como funciona?

**`instanceof` com pattern (Java 16, Final):**

```java
if (obj instanceof String s) {
    System.out.println(s.length());
}
```

**`switch` com patterns (Java 21, Final — JEP 441):**

```java
static String describe(Object obj) {
    return switch (obj) {
        case Integer i -> "int " + i;
        case String s  -> "String " + s;
        case null      -> "é nulo";
        default        -> "desconhecido";
    };
}
```

O recurso evoluiu ao longo de várias versões:

- JEP 406 (Java 17) — primeira preview.
- JEP 420 (Java 18) — segunda preview. Ver [[Java 18]].
- JEP 427 (Java 19) e JEP 433 (Java 20) — terceira e quarta preview.
- JEP 441 (Java 21) — **Final**. Ver [[Java 21]].

## Exemplo

Combinado com [[Sealed Classes]], o `switch` pode ser exaustivo sem precisar de `default`:

```java
sealed interface Result permits Success, Failure {}
record Success(String value) implements Result {}
record Failure(String error) implements Result {}

static String handle(Result r) {
    return switch (r) {
        case Success s -> "ok: " + s.value();
        case Failure f -> "erro: " + f.error();
    }; // sem default — compilador garante exaustividade
}
```

## Quando usar?

- Sempre que uma cadeia de `if (x instanceof Y) ... else if (x instanceof Z)` estiver sendo usada.
- Ao modelar lógica sobre hierarquias `sealed`, aproveitando a checagem de exaustividade.

## Quando evitar?

- Quando o `switch` tradicional sobre constantes já é suficiente e mais simples.

## Relações

- [[Record Patterns]]
- [[Sealed Classes]]
- [[Records]]
- [[Java 18]] — segunda preview do switch pattern matching.
- [[Java 21]] — finalização do switch pattern matching.

## Referências

- JEP 394 — Pattern Matching for instanceof (Final, Java 16): https://openjdk.org/jeps/394
- JEP 406 — Pattern Matching for switch (Preview, Java 17): https://openjdk.org/jeps/406
- JEP 420 — Pattern Matching for switch (2nd Preview, Java 18): https://openjdk.org/jeps/420
- JEP 441 — Pattern Matching for switch (Final, Java 21): https://openjdk.org/jeps/441
