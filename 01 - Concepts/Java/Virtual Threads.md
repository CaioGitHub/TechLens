---
type: concept
status: learning
confidence: 60
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
  - concurrency
---

# Virtual Threads

## O que são?

Virtual Threads (**Final no Java 21**, JEP 444) são threads leves implementadas e escalonadas pela própria JVM, e não pelo sistema operacional. Usam a mesma API `java.lang.Thread` já conhecida — a diferença é interna, não de programação.

## Qual problema resolvem?

O estilo "thread-per-request" (uma thread dedicada por requisição) é simples de escrever, depurar e dar profile, mas não escala com Platform Threads porque cada uma delas consome uma thread do sistema operacional — um recurso caro e limitado (tipicamente milhares, não milhões). Virtual Threads permitem manter esse estilo simples enquanto escalam para números muito maiores de tarefas concorrentes.

## Platform Threads vs. Virtual Threads

- **Platform Thread**: wrapper 1:1 sobre uma thread do SO. Cara para criar, stack de tamanho fixo reservado antecipadamente.
- **Virtual Thread**: objeto leve gerenciado pela JVM; muitas virtual threads compartilham um pool pequeno de *carrier threads* (platform threads) sob demanda.

## Relação com OS Threads

Uma virtual thread só ocupa uma carrier thread (e, portanto, uma thread do SO) enquanto está efetivamente executando código Java. Quando bloqueia em uma operação de I/O suportada pela JVM, a carrier thread é liberada para executar outra virtual thread — o bloqueio "lógico" da virtual thread não bloqueia o recurso do SO.

## JVM

A JVM implementa o escalonamento das virtual threads em modo cooperativo sobre um `ForkJoinPool` de carrier threads. A partir do Java 21, virtual threads sempre suportam variáveis thread-local (mudança em relação às previews anteriores) e podem ser observadas via thread dumps específicos, facilitando debugging e profiling.

## Concurrency vs Parallelism

- **Concorrência**: múltiplas tarefas progridem em um período sobreposto de tempo (podem ou não executar no mesmo instante).
- **Paralelismo**: múltiplas tarefas executam literalmente ao mesmo tempo, em núcleos de CPU distintos.

Virtual Threads endereçam principalmente concorrência (muitas tarefas aguardando I/O), não paralelismo de CPU.

## I/O-bound vs CPU-bound

Virtual Threads são especialmente vantajosas para workloads **I/O-bound** (chamadas a banco de dados, APIs externas, filesystem): a maior parte do tempo de vida da tarefa é gasto esperando, não computando. Como esse tempo de espera libera a carrier thread, é possível ter centenas de milhares de virtual threads ativas com um número pequeno de threads de SO. Para workloads **CPU-bound**, virtual threads não trazem vantagem — o gargalo é a CPU, não a quantidade de threads disponíveis.

## Blocking

Chamadas bloqueantes tradicionais (`InputStream.read()`, JDBC síncrono, `Thread.sleep()`) dentro de uma virtual thread **não bloqueiam a carrier thread** quando a operação é uma das reconhecidas pela JVM como "yield point". O código continua com aparência síncrona/bloqueante, mas se comporta de forma assíncrona por baixo dos panos.

## Escalabilidade

Aplicações que hoje limitam o número de threads (e portanto de requisições concorrentes) por causa do custo de Platform Threads podem, com Virtual Threads, aproximar o número de tarefas concorrentes do número real de requisições em andamento, sem precisar reescrever para um modelo reativo/assíncrono explícito.

## Executor

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> {
        // tarefa I/O-bound
        return chamarServicoExterno();
    });
} // fecha o executor e aguarda as tarefas
```

Também é possível criar uma virtual thread diretamente:

```java
Thread.ofVirtual().start(() -> processar());
```

## Exemplo

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<String>> resultados = requisicoes.stream()
        .map(req -> executor.submit(() -> chamarApiExterna(req)))
        .toList();

    for (var f : resultados) {
        System.out.println(f.get());
    }
}
```

## Quando utilizar?

- Servidores que atendem grande volume de requisições concorrentes com trabalho predominantemente I/O-bound.
- Substituir pools de threads dimensionados artificialmente por medo do custo de criação de threads.

## Quando evitar?

- Tarefas CPU-bound intensas (não há ganho; considerar paralelismo real com Platform Threads/`ForkJoinPool`).
- Código que depende fortemente de `ThreadLocal` com grande quantidade de dados por thread (considerar [[Scoped Values]] no futuro).

## Limitações

- **Pinning**: uma virtual thread pode ficar "presa" (pinned) à sua carrier thread durante blocos `synchronized` ou chamadas nativas (JNI), no Java 21 anulando parte do ganho de escalabilidade nesses trechos específicos. Recomenda-se evitar `synchronized` em seções longas ou trocá-lo por `java.util.concurrent.locks.ReentrantLock` em código crítico para virtual threads.
- Uso excessivo de `synchronized` em código de alta concorrência pode limitar os benefícios.
- Tarefas CPU-bound não se beneficiam do modelo.
- Recursos externos com pool limitado (ex.: conexões de banco) continuam sendo o gargalo real, independentemente do número de virtual threads disponíveis.

## Relações

- [[Java 21]]
- [[Concurrency]]
- [[JVM]]
- [[Structured Concurrency]]
- [[Scoped Values]]

## Referências

- JEP 444 — Virtual Threads (Final, Java 21): https://openjdk.org/jeps/444
- JEP 425 — Virtual Threads (Preview, Java 19): https://openjdk.org/jeps/425
