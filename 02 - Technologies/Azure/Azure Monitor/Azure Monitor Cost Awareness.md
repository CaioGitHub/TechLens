---
type: reference
status: learning
confidence: 35
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Azure Monitor Cost Awareness

## Nota temporal

> Preços e limites específicos mudam com o tempo. Esta nota registra apenas os fatores conceituais que influenciam custo — não valores.

## Fluxo de custo

```
Telemetry
   ↓
Ingestion
   ↓
Storage
   ↓
Query
```

Observabilidade tem custo em cada etapa: gerar telemetria, ingerir esses dados no [[Log Analytics Workspace]], armazená-los, e consultá-los.

## Fatores que influenciam custo

- **Volume de dados**: quanto mais logs/métricas detalhados são coletados, maior o custo de ingestão.
- **Retenção**: por quanto tempo os dados ficam armazenados antes de serem descartados ou arquivados.
- **Ingestão**: cada categoria de log habilitada via [[Azure Diagnostic Settings]] tem custo proporcional ao volume enviado.
- **Consultas**: dependendo do modelo de cobrança, consultas sobre grandes volumes de dados também têm custo associado.
- **Quantidade de recursos monitorados**: mais recursos com diagnostic settings habilitados geram mais volume agregado.

## Relação com Well-Architected

Custo de observabilidade é parte do pilar Cost Optimization do [[Azure Well-Architected Framework]] — nem toda categoria de log precisa estar habilitada em todo recurso; a decisão deve equilibrar valor de diagnóstico contra custo de ingestão/retenção.

## Application Insights e Sampling

Na telemetria de aplicação, o [[Sampling]] é o principal mecanismo de controle de volume/custo — reter uma amostra representativa das operações em vez de 100% delas. A mesma lógica de trade-off entre custo e representatividade descrita aqui se aplica: sampling agressivo reduz custo mas pode comprometer a investigação de eventos raros.

## Relações

- [[Azure Pricing Fundamentals]]
- [[Log Analytics Workspace]]
- [[Azure Diagnostic Settings]]
- [[Sampling]]

## Referências

- Microsoft Azure Pricing Calculator (consultar na data da decisão): https://azure.microsoft.com/en-us/pricing/calculator/
