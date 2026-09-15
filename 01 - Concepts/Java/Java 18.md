---
type: concept
status: understood
confidence: 75
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
---

# Java 18

## Overview

Java 18 é uma versão de funcionalidades ("feature release") do Java SE, lançada em 22/03/2022 sob a JSR 393. **Não é uma versão LTS** — o suporte padrão é curto, e a maioria dos projetos de produção pula direto para a próxima LTS ([[Java 21]]). Sua importância histórica está em consolidar mudanças de base (como UTF-8 padrão) e amadurecer recursos que seriam finalizados em versões LTS futuras (Pattern Matching for switch, Foreign Function & Memory API).

## Principais novidades

- Padronização do UTF-8 como charset padrão da plataforma (impacto amplo, silencioso, relevante para portabilidade).
- Um servidor HTTP mínimo embutido no JDK, útil para testes e prototipagem.
- Continuação da evolução de Pattern Matching for switch e da Foreign Function & Memory API (ambos ainda não finalizados).

## Linguagem

- **JEP 420 — Pattern Matching for switch (Second Preview)**: refinamentos sobre a primeira preview do Java 17. Ver [[Pattern Matching]].

## JVM

- **JEP 416 — Reimplement Core Reflection with Method Handles**: mudança interna na implementação de `java.lang.reflect`, sem impacto direto na API pública, mas relevante para performance de reflection.

## APIs

- **JEP 400 — UTF-8 by Default**: UTF-8 passa a ser o charset padrão em todas as APIs que dependiam de um charset "default" dependente do sistema operacional/locale. Reduz um histórico problema de portabilidade (arquivos gerados em uma máquina sendo lidos incorretamente em outra).
- **JEP 408 — Simple Web Server**: uma ferramenta de linha de comando (`jwebserver`) e uma API mínima (`com.sun.net.httpserver`) para servir arquivos estáticos, útil para testes locais — não é destinada a produção.
- **JEP 418 — Internet-Address Resolution SPI**: permite customizar a resolução de nomes de host/IP via um SPI, reduzindo a dependência exclusiva das rotinas nativas do sistema operacional.
- **JEP 413 — Code Snippets in Java API Documentation**: nova tag `@snippet` para o Javadoc, melhorando a apresentação de exemplos de código na documentação.
- **JEP 421 — Deprecate Finalization for Removal**: o mecanismo de `Object.finalize()` é marcado para remoção futura (não removido ainda); recomenda-se `try-with-resources` e `Cleaner` como alternativas.

## Preview

- **Pattern Matching for switch (JEP 420)** — era Preview desde o Java 17. Motivo: a sintaxe e as regras de exaustividade/dominância ainda estavam sendo refinadas com base em feedback da comunidade. O que aconteceu depois: passou por mais duas rodadas de preview (JDK 19 e 20) e foi **finalizado no Java 21** (JEP 441). Ver [[Java 18 vs Java 21]].

## Incubator

- **Foreign Function & Memory API (JEP 419, Second Incubator)** — ainda incubando desde o Java 17 (como duas APIs separadas antes disso). Evoluiu para Preview no Java 19–21 (JEP 442) e foi finalizada apenas no Java 22. Ver [[Foreign Function and Memory API]].
- **Vector API (JEP 417, Third Incubator)** — API para computação vetorial explorando instruções SIMD; permanece incubando por várias versões (ainda incubando no Java 21, JEP 448). Não documentada em profundidade nesta base por não ser prioridade para desenvolvimento backend típico.

## JEPs relevantes

| JEP | Nome | Objetivo | Status posterior |
|---|---|---|---|
| 400 | UTF-8 by Default | Padronizar UTF-8 como charset padrão | Final, permanece |
| 408 | Simple Web Server | Servidor HTTP mínimo para testes | Final, permanece |
| 413 | Code Snippets in Java API Documentation | Tag `@snippet` no Javadoc | Final, permanece |
| 416 | Reimplement Core Reflection with Method Handles | Performance interna de reflection | Final (interno) |
| 417 | Vector API (3rd Incubator) | Computação vetorial SIMD | Ainda incubando no Java 21 |
| 418 | Internet-Address Resolution SPI | SPI para resolução de nomes/IP | Final, permanece |
| 419 | Foreign Function & Memory API (2nd Incubator) | Interoperar com código/memória nativos | Finalizada apenas no Java 22 |
| 420 | Pattern Matching for switch (2nd Preview) | `switch` com patterns | Finalizada no Java 21 (JEP 441) |
| 421 | Deprecate Finalization for Removal | Depreciar `finalize()` | Ainda depreciado, não removido |

## Relações

- [[Java 21]]
- [[Pattern Matching]]
- [[Foreign Function and Memory API]]
- [[Java 18 vs Java 21]]

## Referências

- JEP 400: https://openjdk.org/jeps/400
- JEP 408: https://openjdk.org/jeps/408
- JEP 413: https://openjdk.org/jeps/413
- JEP 416: https://openjdk.org/jeps/416
- JEP 417: https://openjdk.org/jeps/417
- JEP 418: https://openjdk.org/jeps/418
- JEP 419: https://openjdk.org/jeps/419
- JEP 420: https://openjdk.org/jeps/420
- JEP 421: https://openjdk.org/jeps/421
- OpenJDK — JDK 18 project page: https://openjdk.org/projects/jdk/18/
