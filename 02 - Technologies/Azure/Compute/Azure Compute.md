---
type: technology
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - moc
  - azure
---

# Azure Compute

MOC para os principais modelos de execução de aplicações no Azure.

## Modelos de execução

```
Virtual Machine    → mais controle (IaaS)
       ↓
App Service        → PaaS / aplicação web
       ↓
Container Apps     → containers + abstração de infraestrutura
       ↓
AKS                → Kubernetes gerenciado
       ↓
Functions          → serverless / event-driven
```

Do topo para a base: cada modelo entrega **mais abstração e menos controle/responsabilidade operacional** do que o anterior — mas isso não é uma escala linear de "melhor para pior"; é uma escolha conforme necessidade (ver [[Choosing Azure Compute]]).

| Modelo | Controle | Abstração | Responsabilidade operacional | Escalabilidade | Complexidade |
|---|---|---|---|---|---|
| [[Virtual Machines]] | Alto (SO completo) | Baixa | Alta (você cuida do SO, patches) | Manual ou configurada por você | Média-alta |
| [[Azure App Service]] | Médio | Alta | Baixa (PaaS gerencia SO/runtime) | Configurável, simples | Baixa |
| [[Azure Container Apps]] | Médio | Alta | Baixa (ambiente gerenciado) | Automática (baseada em requisições/eventos) | Baixa-média |
| [[Azure Kubernetes Service]] | Alto (dentro do cluster) | Média | Alta (você opera o cluster) | Altamente configurável | Alta |
| [[Azure Functions]] | Baixo | Muito alta | Muito baixa | Automática (por evento) | Baixa (para o caso de uso certo) |

## Notas

- [[Virtual Machines]]
- [[Azure App Service]]
- [[Deployment Slots]]
- [[Azure Container Apps]]
- [[Azure Kubernetes Service]]
- [[Azure Functions]]
- [[Choosing Azure Compute]]

## Relações

- [[Azure]]
- [[Spring Boot on Azure]]

## Referências

- Microsoft Learn — "Choose an Azure compute service": https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree
