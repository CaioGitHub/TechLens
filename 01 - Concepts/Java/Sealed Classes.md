---
type: concept
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
---

# Sealed Classes

## O que é?

Classes e interfaces `sealed` (finalizadas como Final no Java 17, JEP 409) restringem explicitamente quais outras classes/interfaces podem estendê-las ou implementá-las. Isso permite modelar hierarquias fechadas e finitas de tipos.

## Por que existe?

Antes de `sealed`, uma hierarquia era ou totalmente aberta (`public`/`abstract`, qualquer um pode estender) ou totalmente fechada (`final`, ninguém pode estender). Faltava um meio-termo: "apenas estes tipos específicos podem estender esta classe". Isso é essencial para permitir que o compilador verifique **exaustividade** em `switch` com pattern matching.

## Como funciona?

```java
sealed interface Shape permits Circle, Square, Rectangle {}

record Circle(double radius) implements Shape {}
record Square(double side) implements Shape {}
record Rectangle(double width, double height) implements Shape {}
```

Cada subtipo permitido deve ser declarado como `final`, `sealed` (permitindo nova restrição) ou `non-sealed` (reabrindo a hierarquia para extensão livre a partir daquele ponto).

## Exemplo

```java
final class Circle implements Shape { /* ... */ }
non-sealed class Square implements Shape { /* qualquer um pode estender Square */ }
```

## Quando usar?

- Modelar um conjunto finito e conhecido de variantes (estados de uma máquina de estados, tipos de eventos de domínio, resultado de uma operação — sucesso/erro).
- Sempre que a exaustividade em `switch` (ver [[Pattern Matching]]) for desejável: o compilador acusa erro se um novo subtipo não for tratado.

## Quando evitar?

- Quando a hierarquia realmente precisa ser aberta para extensão por código de terceiros (bibliotecas públicas de extensão).

## Relações

- [[Pattern Matching]] — sealed hierarchies habilitam exaustividade em `switch`.
- [[Records]] — combinação comum: `sealed interface` com implementações `record`.
- [[Java 18]] — Pattern Matching for switch no Java 18 já considerava exaustividade com sealed hierarchies (JEP 420).

## Referências

- JEP 409 — Sealed Classes (Final, Java 17): https://openjdk.org/jeps/409
