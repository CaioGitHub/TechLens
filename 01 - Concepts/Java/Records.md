---
type: concept
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
---

# Records

## O que é?

Um `record` é um tipo de classe imutável e transparente para carregar dados, introduzido como Final no Java 16 (JEP 395). O compilador gera automaticamente construtor canônico, accessors, `equals`, `hashCode` e `toString` a partir dos componentes declarados.

## Por que existe?

Para eliminar o boilerplate clássico de classes "carregadoras de dados" (getters, `equals`/`hashCode`/`toString` manuais) e deixar explícita a intenção: um record é apenas dados, sem identidade mutável.

## Como funciona?

```java
record Point(int x, int y) {}
```

Isso gera automaticamente:
- construtor canônico `Point(int x, int y)`;
- accessors `x()` e `y()` (não `getX()`);
- `equals`/`hashCode` baseados em todos os componentes;
- `toString()` no formato `Point[x=1, y=2]`.

Os componentes são implicitamente `final` (imutáveis após construção). É possível customizar validação via **compact constructor**:

```java
record Point(int x, int y) {
    Point { // compact constructor — sem parênteses
        if (x < 0 || y < 0) throw new IllegalArgumentException("coordenadas negativas");
    }
}
```

## Exemplo

```java
record UserCreated(String userId, Instant occurredAt) {}
```

## Quando usar?

- DTOs, eventos, respostas de API, chaves compostas, valores imutáveis em geral.
- Sempre que a identidade do objeto for definida inteiramente por seus dados (value object).

## Quando evitar?

- Quando é necessária mutabilidade.
- Quando o tipo precisa de herança de implementação (records não podem estender outras classes, apenas implementar interfaces).
- Quando a "transparência" dos dados (accessors públicos) não é desejável para encapsulamento.

## Relações

- [[Java 18]] — já disponível (records finalizados desde o Java 16, portanto anteriores ao escopo desta base).
- [[Record Patterns]] — permitem desestruturar records diretamente em `instanceof` e `switch`.
- [[Sealed Classes]] — combinação comum: hierarquias `sealed` de `record`s para modelar estados finitos.
- DTO (conceito de arquitetura — nota futura).

## Referências

- JEP 395 — Records (Final, Java 16): https://openjdk.org/jeps/395
