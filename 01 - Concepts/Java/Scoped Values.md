---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
  - concurrency
---

# Scoped Values

## O que é?

**Preview no Java 21** (JEP 446). Scoped Values permitem compartilhar um valor imutável com métodos chamados adiante na pilha de execução (e com threads filhas), sem precisar passá-lo explicitamente como parâmetro por toda a cadeia de chamadas.

## Problema

Frameworks frequentemente precisam propagar contexto (usuário autenticado, ID de transação, trace ID) por uma cadeia de chamadas onde código intermediário não usa esse dado diretamente, mas ainda assim seria forçado a declará-lo como parâmetro. A alternativa histórica é `ThreadLocal`, que tem limitações (mutabilidade, custo por thread, propagação manual para threads filhas).

## Conceito

Um scoped value funciona como um **parâmetro implícito**: apenas o código que tem acesso ao objeto `ScopedValue` consegue ler seu valor, e esse valor só é válido dentro do escopo (bloco) em que foi vinculado (`ScopedValue.where(...).run(...)`).

```java
static final ScopedValue<String> USER_ID = ScopedValue.newInstance();

void handle(Request req) {
    ScopedValue.where(USER_ID, req.userId())
               .run(() -> processar());
}

void processar() {
    // em qualquer ponto da pilha de chamadas dentro do run():
    String userId = USER_ID.get();
}
```

## Relação com ThreadLocal

Diferente de `ThreadLocal`, um scoped value é **imutável** durante seu escopo, tem lifecycle bem definido (vinculado apenas durante a execução do `run()`) e é liberado automaticamente ao final do escopo — sem risco de "vazar" valor entre reaproveitamentos de thread em um pool.

## Herança de contexto (concorrência)

Scoped values podem ser propagados automaticamente para subtarefas — especialmente relevante ao usar [[Structured Concurrency]], onde subtarefas criadas dentro de um scope herdam os scoped values do escopo pai.

## Virtual Threads

Scoped Values foram desenhados pensando em cenários com grande número de [[Virtual Threads]], onde `ThreadLocal` tradicional tem custo de memória por thread que se torna proibitivo em escala de milhões de threads.

## Status no Java 21

**Preview** (JEP 446). Anteriormente incubou no Java 20 (JEP 429). Ainda sujeito a mudanças de API.

## Limitações

- Não substitui `ThreadLocal` em todos os casos (ex.: quando mutabilidade real é necessária).
- Sendo Preview, requer flag de compilação/execução (`--enable-preview`) e não deve ser considerado estável para produção.

## Relações

- [[Java 21]]
- [[Structured Concurrency]]
- [[Virtual Threads]]
- [[Concurrency]]

## Referências

- JEP 446 — Scoped Values (Preview, Java 21): https://openjdk.org/jeps/446
- JEP 429 — Scoped Values (Incubator, Java 20): https://openjdk.org/jeps/429
