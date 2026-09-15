---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - application-insights
  - observability
---

# Application Performance Monitoring

## O que é

Application Performance Monitoring (APM) é a prática de observar o comportamento e o desempenho de uma aplicação em execução — não apenas se ela está "rodando", mas como ela está se comportando do ponto de vista de quem a utiliza e de suas dependências.

## Onde o APM se encaixa

```
Monitoring
    ↓
Observability
    ↓
Application Performance Monitoring
```

[[Monitoring vs Observability|Monitoring]] acompanha comportamento conhecido; [[Monitoring vs Observability|Observability]] permite entender comportamento interno a partir de sinais; APM é a aplicação prática desses dois conceitos especificamente à camada de aplicação — usando [[Application Telemetry]] (requests, dependências, exceções, traces) em vez de apenas métricas de infraestrutura.

## O que o APM observa

- **Disponibilidade** — a aplicação responde? (ver [[Availability Monitoring]])
- **Latência** — quanto tempo as operações levam?
- **Throughput** — quantas operações por período?
- **Erros** — quantas falham, e por quê?
- **Exceções** — falhas específicas de código (ver [[Exception Telemetry]])
- **Dependências** — como componentes externos afetam a aplicação (ver [[Dependency Telemetry]])
- **Performance geral** — ver [[Performance Monitoring]]

## APM não é apenas CPU e memória

Uma aplicação pode ter CPU e memória normais e ainda assim estar lenta ou falhando para o usuário — porque o gargalo está em uma dependência externa, em uma consulta de banco, ou em lógica de aplicação. APM foca no comportamento da aplicação sob a perspectiva de quem a consome, complementando (não substituindo) o monitoramento de infraestrutura já coberto por [[Resource Monitoring]].

## Relações

- [[Application Insights]]
- [[Application Telemetry]]
- [[Golden Signals]]
- [[Monitoring vs Observability]]

## Referências

- Microsoft Learn — "Application Insights overview": https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview
