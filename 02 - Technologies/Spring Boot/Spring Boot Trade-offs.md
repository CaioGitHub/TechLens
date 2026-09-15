---
type: reference
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# Spring Boot Trade-offs

## Objetivo

Registrar os custos reais do ecossistema Spring Boot — não deve ser tratado como solução universal.

## Abstrações e "magic"

[[Spring Boot Auto-Configuration]] e Component Scanning reduzem boilerplate, mas tornam menos óbvio "de onde veio" um determinado comportamento ou Bean sem ferramentas de diagnóstico (ex.: endpoint `/actuator/conditions`).

## Reflection

Boa parte do funcionamento do Spring depende de reflection (para escanear anotações, injetar dependências, proxies dinâmicos). Isso tem custo de performance em relação a código estaticamente ligado, embora normalmente aceitável para a maioria das aplicações.

## Startup time e memory consumption

Uma aplicação Spring Boot tradicional carrega e processa uma quantidade significativa de metadados de configuração no startup, o que aumenta tempo de inicialização e consumo de memória em comparação com frameworks mais minimalistas ou compilação nativa (ver [[Spring Boot vs Alternatives]]).

## Debugging

Erros relacionados a configuração automática, proxies do Spring AOP, ou ciclo de vida de Beans podem gerar stack traces difíceis de interpretar para quem não conhece o funcionamento interno do container.

## Framework coupling

Quanto mais anotações e classes do Spring se espalham pelo código (inclusive dentro do que deveria ser o [[Application Core]]), mais difícil se torna substituir o framework no futuro — o oposto do que a [[Hexagonal Architecture]] busca proteger.

## Dependency management

Embora [[Spring Boot Starters]] resolvam boa parte do problema, projetos grandes ainda podem acumular conflitos de versão entre dependências transitivas.

## Learning curve

Entender por completo o funcionamento do container IoC, do ciclo de vida de Beans, de proxies AOP e de auto-configuration exige tempo — a "produtividade imediata" do Spring Boot pode mascarar uma curva de aprendizado real para diagnosticar problemas não triviais.

## Relações

- [[Spring Boot]]
- [[Hexagonal Architecture]]

## Referências

- Spring Boot Reference Documentation: https://docs.spring.io/spring-boot/reference/
