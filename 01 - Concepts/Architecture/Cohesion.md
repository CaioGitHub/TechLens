---
type: concept
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - architecture
---

# Cohesion

## O que é?

Cohesion (coesão) é o grau em que os elementos internos de um módulo (métodos, atributos, responsabilidades) estão relacionados entre si e trabalham juntos para um único propósito bem definido.

## Por que existe?

Um módulo com alta coesão é mais fácil de entender, nomear e testar, porque tudo o que ele contém serve a um mesmo propósito. Um módulo com baixa coesão mistura responsabilidades não relacionadas, dificultando manutenção e reuso.

## Qual problema resolve (ou ajuda a identificar)?

Módulos de baixa coesão tendem a crescer descontroladamente ("classes deus"), pois qualquer coisa "parece caber ali". Isso aumenta o custo de mudança, já que alterar uma responsabilidade arrisca afetar outras não relacionadas dentro do mesmo módulo.

## Como funciona?

Pergunta prática: "todos os métodos e atributos desta classe existem para servir ao mesmo propósito?" Se a resposta for não, é provável que existam duas ou mais responsabilidades misturadas que deveriam ser separadas (ver Single Responsibility Principle em [[SOLID]]).

## Exemplo

```java
// Baixa coesão: mistura persistência, validação e envio de e-mail
class OrderManager {
    void save(Order order) { /* ... */ }
    boolean validate(Order order) { /* ... */ }
    void sendConfirmationEmail(Order order) { /* ... */ }
}

// Alta coesão: cada classe tem um único propósito
class OrderRepository { void save(Order order) { /* ... */ } }
class OrderValidator { boolean validate(Order order) { /* ... */ } }
class OrderNotifier { void sendConfirmationEmail(Order order) { /* ... */ } }
```

## Relações

- [[Coupling]] — o par clássico "baixo acoplamento, alta coesão".
- [[SOLID]] — Single Responsibility Principle é essencialmente uma regra de coesão.
- [[Use Case]] — um bom caso de uso tende a ter alta coesão (uma única intenção do usuário).

## Referências

- Larman, Craig. *Applying UML and Patterns* — princípios GRASP (Low Coupling / High Cohesion).
