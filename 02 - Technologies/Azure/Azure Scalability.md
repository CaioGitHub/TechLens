---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Scalability

## Vertical vs. Horizontal Scaling

```
Vertical Scaling
Instance
   ↓
mais CPU/RAM (a mesma instância fica "maior")

Horizontal Scaling
Instance  Instance  Instance
   ↓
mais capacidade (mais instâncias idênticas em paralelo)
```

## Comparação

| | Vertical (scale up/down) | Horizontal (scale out/in) |
|---|---|---|
| Como escala | Aumenta recursos da mesma instância | Adiciona/remove instâncias |
| Limite | Limitado pelo maior SKU/tier disponível | Praticamente ilimitado (dentro de quotas) |
| Downtime | Frequentemente exige reinício da instância | Pode ser feito sem downtime (novas instâncias entram gradualmente) |
| Requisito da aplicação | Nenhum requisito especial | Aplicação idealmente stateless (sem estado preso a uma instância específica) |

## Onde aparece nos serviços já estudados

- [[Azure App Service]]: suporta tanto vertical (mudar o plano/SKU) quanto horizontal (mais instâncias).
- [[Azure Container Apps]]: escala horizontal automática, inclusive a zero.
- [[Azure Kubernetes Service]]: escala horizontal de pods e de nodes.

## Relação com a aplicação

Escalar horizontalmente com sucesso normalmente exige que a aplicação seja *stateless* entre instâncias (não guardar estado de sessão apenas em memória local) — um Use Case do [[Application Core]] bem desenhado, sem estado mutável compartilhado, favorece esse tipo de escala.

## Relações

- [[Azure Compute]]
- [[Application Gateway and Load Balancing]]
- [[Azure Well-Architected Framework]]

## Referências

- Microsoft Learn — "Scalability in Azure": https://learn.microsoft.com/en-us/azure/architecture/framework/scalability/overview
