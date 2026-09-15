---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - observability
---

# Azure Monitor Metrics

## O que é uma métrica?

Uma métrica é um valor numérico, coletado em um determinado instante (timestamp), representando algum aspecto de um sistema em um ponto no tempo. Uma sequência de métricas ao longo do tempo forma uma **série temporal** (time series).

## Componentes

- **Valor numérico**: o número medido (ex.: 42% de CPU).
- **Timestamp**: o momento da coleta.
- **Dimensão**: um atributo adicional que permite segmentar a métrica (ver [[Metric Dimensions]]).
- **Intervalo de coleta**: com que frequência o valor é medido/registrado (ex.: a cada minuto).
- **Agregação**: como múltiplos valores dentro de um período são resumidos (ver [[Metric Aggregation]]).

## Métricas de plataforma vs. de aplicação

- **Métricas de plataforma**: geradas automaticamente pelo próprio recurso Azure (ex.: CPU do App Service, latência do Storage) — coletadas sem esforço de instrumentação.
- **Métricas de aplicação**: geradas pelo código da aplicação (ex.: número de pedidos processados) — exigem alguma forma de instrumentação (aprofundado na Etapa 8 com Application Insights).

## Exemplos conceituais

CPU, Memory, Requests, Latency, Error Rate.

## Metric vs. Log

Uma métrica é compacta e otimizada para series temporais e agregação rápida ("quanto?"); um log é um registro estruturado de um evento específico, com mais contexto, mas mais custoso para agregar em grande volume ("o que aconteceu?"). Ver [[Logs vs Metrics]].

## Relações

- [[Metric Dimensions]]
- [[Metric Aggregation]]
- [[Azure Monitor Logs]]
- [[Metrics Logs Traces]]

## Referências

- Microsoft Learn — "Metrics in Azure Monitor": https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/data-platform-metrics
