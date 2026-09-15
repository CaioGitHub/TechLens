---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - observability
---

# Metric Aggregation

## O que é?

Quando múltiplos valores de uma métrica existem dentro de um período de tempo, uma agregação resume esses valores em um único número representativo, segundo uma função escolhida.

## Funções comuns

- **Average**: média dos valores no período — boa visão geral, mas pode esconder picos.
- **Sum**: soma total no período (útil para contagens, ex.: total de requests).
- **Minimum / Maximum**: menor/maior valor observado no período.
- **Count**: quantidade de amostras coletadas.
- **Percentis (ex.: P95, P99)**: valor abaixo do qual X% das amostras estão — útil para entender a "cauda" da distribuição, não só a média.

## Exemplo

```
Latency
  ↓
Average → visão geral (pode esconder que 5% dos usuários têm experiência ruim)

P95
  ↓
visão da cauda da distribuição (o que os "piores" 5% dos casos enfrentam)
```

## Por que isso importa

Uma média baixa de latência não garante que todos os usuários tenham boa experiência — poucos requests muito lentos podem não mover a média significativamente, mas afetam usuários reais. Percentis altos (P95, P99) revelam esse tipo de problema que a média esconde.

## Relações

- [[Azure Monitor Metrics]]
- [[Metric Dimensions]]
- [[Performance Monitoring]]

## Referências

- Microsoft Learn — "Metrics aggregation and display": https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/metrics-supported
