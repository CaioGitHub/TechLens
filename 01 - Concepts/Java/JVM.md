---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
---

# JVM

## O que é?

Visão conceitual da Java Virtual Machine (JVM): a máquina que executa bytecode Java, independente da linguagem que o gerou e da plataforma física subjacente.

## Por que existe?

Permite que código Java compilado ("write once, run anywhere") execute sobre qualquer sistema operacional/hardware que tenha uma implementação de JVM, além de fornecer serviços de gerenciamento automático de memória, segurança e otimização em tempo de execução.

## Como funciona? (mapa de conceitos)

- **Class Loader** — carrega classes (bytecode `.class`) em memória sob demanda, seguindo uma hierarquia de carregadores.
- **Bytecode / Interpreter** — o código compilado é bytecode, inicialmente executado por um interpretador.
- **JIT (Just-In-Time compiler)** — compila trechos de bytecode executados com frequência ("hot spots") para código de máquina nativo, otimizando o desempenho em tempo de execução.
- **Heap** — região de memória onde objetos são alocados; gerenciada pelo Garbage Collector.
- **Stack** — cada thread tem sua própria stack, armazenando frames de chamadas de método e variáveis locais.
- **Metaspace** — região de memória nativa (fora da heap, desde o Java 8) onde metadados de classes são armazenados.
- **Garbage Collection** — processo automático de identificar e liberar memória de objetos não mais referenciados. Diversos coletores disponíveis (G1, ZGC, Generational ZGC desde o Java 21 — ver [[Java 21]]).
- **Threads** — unidade de execução concorrente; ver [[Concurrency]] e [[Virtual Threads]] para o modelo moderno introduzido no Java 21.
- **[[Java Memory Model]]** — regras formais sobre visibilidade e ordenação de operações de memória entre threads.

## Quando aprofundar?

Esta nota é intencionalmente um mapa de alto nível. Aprofundamentos específicos (tuning de GC, análise de JIT, heap dumps) devem virar notas próprias em `02 - Technologies` ou `07 - Troubleshooting` quando houver experiência prática concreta para documentar.

## Relações

- [[Concurrency]]
- [[Virtual Threads]]
- [[Java Memory Model]]
- Performance *(nota futura)*

## Referências

- The Java Virtual Machine Specification: https://docs.oracle.com/javase/specs/jvms/se21/html/index.html
