---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - architecture
---

# SOLID

## O que é?

SOLID é um acrônimo para cinco princípios de design orientado a objetos, popularizados por Robert C. Martin, voltados a produzir código mais compreensível, flexível e sustentável.

## Por que existe?

Cada princípio ataca uma forma comum de acoplamento ou baixa coesão que surge naturalmente conforme um sistema cresce.

## Como funciona? (visão geral)

- **S — Single Responsibility Principle**: uma classe deve ter um único motivo para mudar. Relacionado a [[Cohesion]].
- **O — Open/Closed Principle**: entidades devem ser abertas para extensão, fechadas para modificação (estender comportamento sem alterar código existente, tipicamente via abstrações).
- **L — Liskov Substitution Principle**: uma subclasse deve poder substituir sua superclasse sem quebrar o comportamento esperado pelo código cliente.
- **I — Interface Segregation Principle**: interfaces específicas e coesas são preferíveis a uma interface única e genérica que força implementações a depender de métodos que não usam.
- **D — Dependency Inversion Principle**: módulos de alto nível não devem depender de módulos de baixo nível; ambos devem depender de abstrações. Ver nota dedicada [[Dependency Inversion]].

## Por que o "D" recebe atenção especial nesta base?

O Dependency Inversion Principle é o princípio que fundamenta diretamente a [[Hexagonal Architecture]]: a separação entre [[Ports]] (abstrações definidas pelo Core) e [[Adapters]] (implementações concretas) é uma aplicação direta do DIP.

## Quando usar?

Como heurísticas de design ao identificar sinais de baixa coesão, alto acoplamento ou dificuldade de estender o sistema sem quebrar código existente.

## Quando evitar (aplicação literal)?

Aplicar todos os princípios de forma dogmática e antecipada (antes de existir necessidade real de extensão ou substituição) pode gerar abstrações desnecessárias e overengineering.

## Relações

- [[Dependency Inversion]]
- [[Coupling]]
- [[Cohesion]]
- [[Hexagonal Architecture]]

## Referências

- Martin, Robert C. *Agile Software Development, Principles, Patterns, and Practices*, 2002.
- Martin, Robert C. "The Dependency Inversion Principle", *Engineering Notebook*, 1996.
