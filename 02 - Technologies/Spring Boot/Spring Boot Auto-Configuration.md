---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
  - spring-boot
---

# Spring Boot Auto-Configuration

## O que é?

Auto-Configuration é o mecanismo pelo qual o Spring Boot tenta configurar automaticamente [[Spring Bean|Beans]] comuns com base no que está presente no classpath da aplicação, evitando configuração manual repetitiva.

## Qual problema resolve?

Antes do Spring Boot, configurar uma aplicação Spring web com acesso a banco de dados exigia declarar manualmente dezenas de Beans (DispatcherServlet, conversores JSON, DataSource, TransactionManager...). Auto-Configuration elimina essa repetição para casos comuns, aplicando convenções sensatas por padrão.

## Como funciona (comportamento documentado, sem tratar como "mágica")

1. `@SpringBootApplication` inclui `@EnableAutoConfiguration`.
2. No startup, o Spring Boot carrega uma lista de classes de auto-configuração (declaradas em um arquivo de metadados dentro dos JARs de dependência).
3. Cada classe de auto-configuração é **condicional**: só é aplicada se certas condições forem satisfeitas — tipicamente anotadas com `@ConditionalOnClass` (uma classe específica está no classpath), `@ConditionalOnMissingBean` (você ainda não declarou seu próprio Bean equivalente), `@ConditionalOnProperty` (uma propriedade de configuração está definida).
4. Se você declarar seu próprio Bean explicitamente (ver [[Spring Configuration]]), ele tem precedência — a auto-configuração correspondente recua.

## Exemplo conceitual

```
spring-boot-starter-web no classpath
        ↓
Spring MVC detectado (@ConditionalOnClass)
        ↓
Auto-Configuration registra DispatcherServlet, conversores JSON, etc.
        ↓
Aplicação web funcional sem configuração manual
```

## Relação com Starters

Auto-Configuration reage ao que está no classpath; [[Spring Boot Starters]] são justamente o mecanismo que coloca dependências relacionadas no classpath de uma vez. Os dois mecanismos trabalham juntos: o starter traz a dependência, a auto-configuration reage a ela.

## Possibilidade de override

Qualquer Bean auto-configurado pode ser substituído declarando seu próprio Bean com o mesmo tipo/nome — a auto-configuration foi desenhada para recuar nesse caso (`@ConditionalOnMissingBean`). Também é possível excluir uma auto-configuração explicitamente (`@SpringBootApplication(exclude = ...)`).

## Comportamento documentado vs. implementação interna

- **Documentado**: o comportamento condicional (`@ConditionalOnClass`, `@ConditionalOnMissingBean`, possibilidade de override) é contrato público, estável entre versões.
- **Implementação interna**: a lista exata de classes de auto-configuração e o mecanismo interno de carregamento pode variar entre versões do Spring Boot — não deve ser tratado como API pública estável.

## Trade-offs

- Reduz drasticamente boilerplate de configuração.
- Pode dificultar entender "de onde veio" um Bean específico sem ferramentas de diagnóstico (ex.: endpoint `/actuator/conditions` — ver [[Spring Boot Actuator]]).

## Relações

- [[Spring Boot Starters]]
- [[Spring Configuration]]
- [[Spring Boot Application]]
- [[Spring Framework vs Spring Boot]]

## Referências

- Spring Boot Reference Documentation — "Auto-configuration": https://docs.spring.io/spring-boot/reference/using/auto-configuration.html
