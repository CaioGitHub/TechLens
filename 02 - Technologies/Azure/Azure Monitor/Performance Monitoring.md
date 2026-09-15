---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Performance Monitoring

## O que engloba

Performance não é apenas CPU — engloba múltiplas dimensões do comportamento de uma aplicação:

- **Latency**: tempo de resposta de uma operação.
- **Throughput**: volume de operações processadas por unidade de tempo.
- **CPU / Memory**: consumo de recursos computacionais.
- **Dependency Time**: tempo gasto esperando por dependências externas (banco de dados, APIs externas).
- **Error Rate**: proporção de operações que falham.

## Conexão

```
Application Performance
        ↓
Telemetry
        ↓
Analysis
```

Nenhuma dessas dimensões isolada conta a história completa: CPU baixa não significa boa performance percebida pelo usuário se a latência estiver alta por causa de uma dependência lenta (ver [[Metric Aggregation]] para o papel de percentis nessa análise).

## No Application Insights

O [[Application Insights]] observa performance a partir da telemetria de aplicação: duração de [[Request Telemetry|requests]], duração de [[Dependency Telemetry|dependencies]] e frequência de [[Exception Telemetry|exceptions]] — permitindo investigar se um problema de performance percebido pelo usuário se origina na própria aplicação ou em uma dependência externa (ver o modelo completo em [[Application Insights Troubleshooting]]).

## Relações

- [[Azure Monitor Metrics]]
- [[Metric Aggregation]]
- [[Golden Signals]]
- [[Azure Monitor Traces]]
- [[Application Insights]]

## Referências

- Microsoft Learn — "Application performance monitoring": https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview
