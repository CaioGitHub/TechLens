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

# Metric Dimensions

## O que é?

Uma dimensão é um atributo adicional de uma métrica que permite segmentá-la em fatias mais específicas, em vez de olhar apenas para um valor agregado único.

## Exemplo conceitual

```
Request Count
      ↓
pode ser segmentado por:
- Endpoint
- Status Code
- Instance
- Region
```

Sem dimensões, "Request Count = 10.000" é um número isolado. Com a dimensão "Status Code", é possível perguntar "quantas dessas 10.000 requisições foram 500?" sem precisar de uma métrica separada para cada status code.

## Não generalizar

As dimensões disponíveis para uma métrica dependem inteiramente do recurso e da própria métrica — nem toda métrica tem as mesmas dimensões, e nem todo recurso expõe as mesmas métricas. É preciso consultar a documentação específica do recurso.

## Relações

- [[Azure Monitor Metrics]]
- [[Metric Aggregation]]

## Referências

- Microsoft Learn — "Multi-dimensional metrics": https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/data-platform-metrics#multi-dimensional-metrics
