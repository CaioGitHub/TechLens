---
type: reference
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# Spring Boot vs Alternatives

## Objetivo

Contexto conceitual breve — não é um estudo aprofundado de cada framework.

| Aspecto | Spring Boot | Jakarta EE | Micronaut | Quarkus |
|---|---|---|---|---|
| Modelo de DI | Container Spring (reflection-heavy, tradicionalmente) | CDI (Contexts and Dependency Injection) | DI resolvido em tempo de compilação (menos reflection) | DI resolvido em tempo de build (menos reflection) |
| Startup | Mais lento tradicionalmente (JVM) | Depende do servidor/implementação | Rápido, pensado para serverless/cloud desde o início | Rápido, pensado para containers/cloud desde o início |
| Ecossistema | Muito grande, maduro, maior comunidade | Padrão especificado (múltiplos vendors) | Menor, mas crescente | Menor, mas crescente, forte em GraalVM |
| Compilação nativa (GraalVM) | Suportada (Spring Native/AOT), mas não é o caso de uso original | Depende da implementação | Projetado com isso em mente desde o início | Projetado com isso em mente desde o início |
| Cloud-native | Suportado, mas não nasceu "cloud-first" | Depende da implementação | Cloud-native desde a concepção | Cloud-native desde a concepção ("Supersonic Subatomic Java") |

## Por que essa comparação importa (brevemente)

Todos resolvem, em essência, o mesmo problema central: gerenciar dependências e configurar uma aplicação Java de forma produtiva. As diferenças relevantes concentram-se em **tempo de inicialização, consumo de memória e adequação a ambientes serverless/containers de curta duração** — Spring Boot prioriza maturidade de ecossistema e compatibilidade retroativa; Micronaut e Quarkus priorizam startup rápido e baixo consumo de memória.

## O que esta nota não faz

Não avalia qual framework é "melhor" nem aprofunda detalhes de implementação de cada um — isso pertence a uma eventual etapa futura, se necessário.

## Relações

- [[Spring Boot]]
- [[Spring Framework vs Spring Boot]]

## Referências

- Spring Boot: https://docs.spring.io/spring-boot/
- Jakarta EE: https://jakarta.ee/
- Micronaut: https://micronaut.io/
- Quarkus: https://quarkus.io/
