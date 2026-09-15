---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - spring
  - java
---

# Java 21 with Spring Boot

## O que é?

Análise da integração entre recursos de [[Java 21]] e o ecossistema Spring Boot, com foco especial em [[Virtual Threads]].

## Compatibilidade

Versões recentes do Spring Framework/Spring Boot suportam Java 21 como baseline, incluindo suporte a Virtual Threads (habilitável via propriedade de configuração, sem exigir reescrever a aplicação).

## Virtual Threads no ecossistema Spring

```
Java 21
   ↓
Virtual Threads (JEP 444 — Final)
   ↓
Spring Boot (pode executar requisições web em Virtual Threads)
```

Quando habilitado, o Spring Boot pode processar cada requisição HTTP (e outros pontos de execução configuráveis) em uma Virtual Thread em vez de uma thread de plataforma do pool tradicional (ex.: pool de threads do Tomcat).

## Quando Virtual Threads ajudam (e quando não)

- **I/O-bound**: código que passa a maior parte do tempo bloqueado esperando I/O (chamadas a banco de dados, APIs externas, sistema de arquivos) é o cenário onde Virtual Threads trazem o maior benefício — permitem escalar para um número muito maior de requisições concorrentes sem esgotar um pool de threads de plataforma.
- **CPU-bound**: código que gasta a maior parte do tempo em computação (não bloqueando em I/O) não se beneficia significativamente de Virtual Threads — o gargalo continua sendo CPU disponível, não o modelo de threads.
- Virtual Threads **não são automaticamente "mais rápidas"**: elas resolvem um problema de **escalabilidade de concorrência** (quantas operações bloqueantes simultâneas o sistema aguenta), não de velocidade de uma única operação.

## Limites e considerações práticas

- Bibliotecas ou trechos de código com `synchronized` intensivo podem não se beneficiar completamente do modelo de Virtual Threads (pinning de thread de plataforma) — ponto a validar conforme a versão do JDK utilizada.
- Pools de conexão de banco de dados (ex.: HikariCP) continuam sendo um limite real de concorrência independente do modelo de thread usado — Virtual Threads não removem a necessidade de dimensionar corretamente recursos externos.
- A adoção de Virtual Threads é uma decisão de configuração/infraestrutura de execução — não deveria alterar o desenho arquitetural do [[Application Core]], que permanece agnóstico a como suas Ports são acionadas.

## Relações

- [[Virtual Threads]]
- [[Concurrency]]
- [[Java 21]]
- [[Spring Boot]]

## Referências

- Spring Boot Reference Documentation — "Embedded Web Servers" / Virtual Threads: https://docs.spring.io/spring-boot/reference/web/servlet.html
- OpenJDK JEP 444 — Virtual Threads: https://openjdk.org/jeps/444
