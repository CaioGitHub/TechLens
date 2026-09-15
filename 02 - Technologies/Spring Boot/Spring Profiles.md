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

# Spring Profiles

## O que é?

Profiles são um mecanismo do Spring para ativar conjuntos diferentes de configuração (Beans e/ou propriedades) dependendo do ambiente em que a aplicação está rodando (development, test, production, etc.).

## Como funciona

```
application.properties (ou application.yml)   — configuração padrão/comum
application-dev.properties                     — sobrepõe/completa para o profile "dev"
application-prod.properties                    — sobrepõe/completa para o profile "prod"
```

O profile ativo é escolhido tipicamente por uma propriedade (`spring.profiles.active`) definida via variável de ambiente, argumento de linha de comando, ou arquivo de configuração.

## Uso comum

- Trocar a `DataSource` entre um banco em memória (testes) e um banco real (produção).
- Ativar/desativar Beans específicos de um ambiente com `@Profile("dev")`.
- Ajustar níveis de log, URLs de serviços externos, timeouts.

## O que Profiles NÃO resolvem sozinhos

Profiles não são um mecanismo de gerenciamento seguro de segredos (senhas, chaves de API). Colocar credenciais diretamente em `application-prod.properties` versionado é uma prática arriscada — esse tópico (cofres de segredos, variáveis de ambiente seguras, integração com provedores de nuvem) fica fora do escopo desta etapa.

## Relações

- [[Spring Configuration]]
- [[Spring Configuration Properties]]

## Referências

- Spring Boot Reference Documentation — "Profiles": https://docs.spring.io/spring-boot/reference/features/profiles.html
