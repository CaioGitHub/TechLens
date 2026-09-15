---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
  - spring-boot
---

# Spring Configuration Properties

## O que é?

Mecanismo do Spring Boot para trazer valores de configuração externos (arquivos `.properties`/`.yml`, variáveis de ambiente, argumentos de linha de comando) para dentro da aplicação de forma **tipada**, em vez de espalhar `System.getenv(...)` ou strings soltas pelo código.

## Hardcoded vs. Externalized Configuration

```java
// Hardcoded — muda apenas recompilando o código
class OrderService {
    private final int timeoutSeconds = 30;
}

// Externalized + tipado — muda sem recompilar
@ConfigurationProperties(prefix = "order")
record OrderProperties(int timeoutSeconds) {}
```

```yaml
order:
  timeout-seconds: 30
```

## Por que existe?

Separar código de configuração permite mudar comportamento entre ambientes (ver [[Spring Profiles]]) sem recompilar, e agrupa propriedades relacionadas em um único objeto tipado e validável, em vez de várias chamadas dispersas a `@Value("${...}")`.

## Binding

O Spring Boot faz o *binding* automático entre as chaves do arquivo de propriedades e os campos da classe/record anotada, incluindo conversão de tipos (String → int, Duration, List, etc.).

## Relações

- [[Spring Profiles]]
- [[Spring Configuration]]
- [[Records]] — um bom ajuste para classes de propriedades imutáveis.

## Referências

- Spring Boot Reference Documentation — "Typesafe Configuration Properties": https://docs.spring.io/spring-boot/reference/features/external-config.html#features.external-config.typesafe-configuration-properties
