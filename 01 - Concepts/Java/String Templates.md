---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - java
---

# String Templates

## O que é?

**Preview no Java 21** (JEP 430). String Templates propõem sintaxe para interpolação de strings — combinar texto literal com expressões embutidas — usando "template processors" que controlam como o resultado final é produzido (string, ou outro tipo de valor).

## Problema

Concatenação com `+` é difícil de ler; `StringBuilder` é verboso; `String.format`/`formatted` separam o texto dos parâmetros (risco de erro de aridade/tipo). Outras linguagens (Python, Kotlin, JavaScript, C#) já oferecem interpolação nativa de strings.

## Sintaxe / Interpolação

```java
String name = "Duke";
String info = STR."Olá, \{name}!"; // "Olá, Duke!"
```

`STR` é um template processor padrão que produz um `String` simples, interpolando as expressões dentro de `\{ }`.

## Segurança

Um diferencial em relação à interpolação de outras linguagens: o processor pode **validar e transformar** tanto o template quanto os valores antes de gerar o resultado — por exemplo, um processor `SQL` poderia gerar uma prepared statement corretamente parametrizada em vez de concatenar valores brutos, mitigando injection.

## Casos de uso (pretendidos)

- Construção de mensagens de log, textos formatados, JSON/XML de forma mais legível.
- Construção seguraa de queries (SQL) e outros DSLs, delegando validação ao processor.

## Limitações e status no Java 21

**Preview** (JEP 430) — primeira preview. **Importante**: não deve ser tratado como recurso estável.

## Evolução posterior (contextualização)

- Java 22 (JEP 459): segunda preview, com refinamentos.
- Java 23: a feature foi **retirada** (JEP 465 foi fechado/descartado) por problemas de design — o modelo baseado em "template processors" foi considerado confuso e pouco composicional. Não há consenso, até o momento desta nota, sobre se/quando retornará em novo formato.

Por isso, **String Templates não deve ser adotado em código de produção** a partir do que se sabe hoje — trata-se de um recurso experimental que já mudou de rumo uma vez.

## Relações

- [[Java 21]]
- [[Java 18 vs Java 21]]

## Referências

- JEP 430 — String Templates (Preview, Java 21): https://openjdk.org/jeps/430
- Retirada em Java 23 — confirmar status mais recente em https://openjdk.org/jeps/465 (JEP fechado) antes de qualquer uso.
