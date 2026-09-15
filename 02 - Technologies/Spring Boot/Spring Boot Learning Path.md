---
type: study
status: learning
confidence: 30
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
---

# Spring Boot Learning Path

## O que quero entender?

Sequência lógica de pré-requisitos para compreender Spring Boot com profundidade suficiente para usá-lo sem deixar o framework definir a arquitetura da aplicação.

## Resumo

1. [[Java 21]]
2. [[Spring Framework vs Spring Boot]]
3. [[Inversion of Control]]
4. [[Dependency Injection]] *(nota em `01 - Concepts/Architecture`)*
5. [[ApplicationContext]]
6. [[Spring Bean]]
7. [[Spring Configuration]] (+ [[Component Scanning]])
8. [[Spring Boot Application]]
9. [[Spring Boot Auto-Configuration]] (+ [[Spring Boot Starters]])
10. [[Spring REST]] (Web/REST)
11. [[Spring Validation]]
12. [[Spring Data]] (persistência)
13. [[Spring Transactions]]
14. [[Spring Testing]]
15. [[Spring Boot Actuator]]
16. [[Spring Boot Logging]]
17. [[Java 21 with Spring Boot]] (Virtual Threads)
18. [[Spring Boot + Hexagonal Architecture]]

## Conceitos importantes

A ordem importa: IoC/DI precisam ser entendidos antes de ApplicationContext/Bean fazerem sentido; Auto-Configuration só é compreensível depois de entender Configuration explícita e Component Scanning; a integração com Hexagonal Architecture só faz sentido depois de entender Ports/Adapters (etapa anterior) e os mecanismos web/data do Spring.

## Exemplo prático

Usar o exemplo "Order API" documentado em [[Spring Boot + Hexagonal Architecture]] como estudo de caso para percorrer toda a sequência acima.

## O que aprendi?

*(a preencher conforme o estudo avança)*

## Dúvidas

*(a preencher conforme o estudo avança)*

## Próximos passos

Avaliar necessidade de aprofundar Spring Security/OAuth apenas quando houver um caso real de autenticação/autorização a resolver. Preparar terreno para a etapa futura de observabilidade (Azure Monitor, Application Insights, Log Analytics, KQL), já conectada conceitualmente via [[Spring Boot Actuator]] e [[Spring Boot Logging]].

## Relações

- [[Spring Boot]]
- [[Hexagonal Architecture Learning Path]]
- [[Java 18-21 Learning Path]]

## Referências

- Ver referências detalhadas nas notas individuais de cada conceito.
