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

# Structured Concurrency

## O que é?

**Preview no Java 21** (JEP 453). Structured Concurrency propõe uma API (`StructuredTaskScope`, em `java.util.concurrent`) que trata um grupo de subtarefas relacionadas, executando em threads diferentes, como **uma única unidade de trabalho**.

## Problema que tenta resolver

Com `ExecutorService` "não estruturado", cada subtarefa (`Future`) tem ciclo de vida independente: se uma falha, nada cancela automaticamente as demais; se a thread "pai" é interrompida, as subtarefas podem continuar rodando (thread leak). Isso dificulta reasoning sobre erro, cancelamento e observabilidade.

## Modelo tradicional de concorrência

```java
// Não estruturado — cada Future vive por conta própria
Future<String> user  = executor.submit(() -> findUser());
Future<Integer> order = executor.submit(() -> fetchOrder());
String u = user.get();
int o = order.get();
```

Se `findUser()` falhar, `fetchOrder()` continua executando sem necessidade — desperdício de recursos e comportamento pouco previsível.

## Conceito de estrutura

Structured Concurrency amarra o ciclo de vida das subtarefas ao escopo léxico do bloco que as criou: nenhuma subtarefa "escapa" além do bloco, de forma análoga a como blocos aninhados funcionam em código sequencial.

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<String> user  = scope.fork(() -> findUser());
    Subtask<Integer> order = scope.fork(() -> fetchOrder());

    scope.join();           // aguarda ambas ou falha na primeira
    scope.throwIfFailed();  // propaga exceção se alguma subtarefa falhou

    return new Response(user.get(), order.get());
}
```

## Relação entre tarefas

Todas as subtarefas de um `StructuredTaskScope` compartilham o mesmo "pai" lógico; políticas como `ShutdownOnFailure` (cancela as demais se uma falhar) ou `ShutdownOnSuccess` (retorna assim que a primeira tiver sucesso) definem a relação entre elas.

## Cancelamento

Quando a política de shutdown é acionada (ex.: uma subtarefa falha em `ShutdownOnFailure`), o scope cancela automaticamente as subtarefas restantes — algo que não acontecia de forma automática com `ExecutorService` puro.

## Tratamento de erros

Erros de subtarefas ficam disponíveis via o objeto `Subtask` e podem ser propagados de forma centralizada com `scope.throwIfFailed()`, evitando exceções perdidas silenciosamente.

## Lifecycle

O `try-with-resources` garante que o scope só é fechado depois que todas as subtarefas realmente terminaram (com sucesso, erro ou cancelamento) — não há vazamento de threads além do bloco.

## Relação com Virtual Threads

Structured Concurrency é especialmente útil combinada com [[Virtual Threads]]: como criar uma virtual thread por subtarefa é barato, é comum despachar uma subtarefa por chamada de I/O dentro de um `StructuredTaskScope`.

## Status no Java 21

**Preview** (JEP 453). Já havia incubado no Java 19 (JEP 428) e Java 20 (JEP 437). A mudança mais notável na preview do Java 21 é que `fork()` passa a retornar um `Subtask`, não um `Future`.

## Evolução futura

Continuou evoluindo em versões posteriores ao Java 21 (fora do escopo desta base). Não deve ser tratada como API definitiva enquanto estiver em preview — assinatura de métodos pode mudar.

## Relações

- [[Java 21]]
- [[Virtual Threads]]
- [[Concurrency]]
- [[Scoped Values]]

## Referências

- JEP 453 — Structured Concurrency (Preview, Java 21): https://openjdk.org/jeps/453
- JEP 428 — Structured Concurrency (Incubator, Java 19): https://openjdk.org/jeps/428
