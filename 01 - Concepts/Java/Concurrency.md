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

# Concurrency

## O que é?

Visão conceitual do modelo de concorrência em Java: mecanismos para executar múltiplas unidades de trabalho ao mesmo tempo (ou de forma intercalada), coordená-las e compartilhar dados entre elas com segurança.

## Por que existe?

Aplicações servidoras precisam atender muitas requisições simultâneas; sistemas modernos precisam aproveitar múltiplos núcleos de CPU. Java oferece um modelo de concorrência baseado em threads desde sua primeira versão, evoluído ao longo do tempo com abstrações de mais alto nível.

## Como funciona? (mapa de conceitos)

Esta nota funciona como MOC do domínio de concorrência. Não repete conteúdo já coberto pelas notas específicas:

- **Threads** — unidade de execução tradicional da JVM, mapeada 1:1 para uma thread do sistema operacional (Platform Thread). Ver [[Virtual Threads]] para a alternativa leve introduzida no Java 21.
- **Executor / ExecutorService** — abstração para submeter tarefas sem gerenciar threads diretamente (`java.util.concurrent`, desde o Java 5).
- **Future / CompletableFuture** — representam o resultado futuro de uma tarefa assíncrona; `CompletableFuture` (Java 8) adiciona composição funcional sobre `Future`.
- **synchronized / Locks** — mecanismos de exclusão mútua para proteger acesso concorrente a estado compartilhado.
- **Atomic Variables / Concurrent Collections** — estruturas de dados e variáveis thread-safe sem bloqueio explícito (`java.util.concurrent.atomic`, `ConcurrentHashMap`, etc.).
- **[[Java Memory Model]]** — regras que definem quando mudanças feitas por uma thread se tornam visíveis para outra.
- **Race Condition / Deadlock / Starvation** — problemas clássicos de concorrência decorrentes de acesso compartilhado mal coordenado.
- **[[Virtual Threads]]** — threads leves gerenciadas pela JVM (Java 21, Final).
- **[[Structured Concurrency]]** — trata grupos de tarefas relacionadas como uma unidade (Java 21, Preview).
- **[[Scoped Values]]** — alternativa a `ThreadLocal` para compartilhar dados imutáveis entre threads (Java 21, Preview).

## Quando usar cada abordagem?

- I/O-bound com alto grau de concorrência → [[Virtual Threads]].
- CPU-bound / paralelismo de dados → threads de plataforma com pool dimensionado para os núcleos disponíveis, ou Stream API paralelo.
- Coordenar múltiplas subtarefas relacionadas com cancelamento conjunto → [[Structured Concurrency]].
- Compartilhar contexto imutável entre uma tarefa e suas subtarefas → [[Scoped Values]].

## Relações

- [[Virtual Threads]]
- [[Structured Concurrency]]
- [[Scoped Values]]
- [[Java Memory Model]]
- [[JVM]]

## Referências

- `java.util.concurrent` (Java SE API): https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/package-summary.html
