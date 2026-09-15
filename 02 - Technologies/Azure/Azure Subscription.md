---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Subscription

## O que é?

Uma Subscription é a **fronteira de faturamento (billing boundary)** e de gerenciamento de acesso no Azure: define quotas de recursos, agrega custos, e serve como container para [[Resource Group|Resource Groups]].

## Modelo hierárquico

```
Management Group
       ↓
Subscription
       ↓
Resource Group
       ↓
Resources
```

## Responsabilidades de uma Subscription

- **Billing boundary**: todos os custos dos recursos dentro dela são agregados nesta subscription.
- **Quotas**: limites de quantidade/capacidade de recursos são aplicados por subscription (ex.: número de VMs de um determinado tipo).
- **Acesso**: permissões podem ser concedidas no nível da subscription (herdadas por todos os Resource Groups e recursos abaixo).

## Management Groups (visão conceitual, sem aprofundar governança empresarial)

```
Management Group
       ↓
Subscriptions (uma ou mais)
       ↓
Resource Groups
       ↓
Resources
```

Management Groups existem para organizar **múltiplas subscriptions** sob uma mesma estrutura de políticas e permissões — relevante principalmente em organizações com muitas subscriptions (ex.: uma por departamento/projeto). Esta base não aprofunda governança empresarial em detalhe — apenas registra a existência do nível hierárquico.

## Relações

- [[Resource Group]]
- [[Azure Resource Manager]]
- [[Azure RBAC]]

## Referências

- Microsoft Learn — "Organize your resources with Azure management groups": https://learn.microsoft.com/en-us/azure/governance/management-groups/overview
- Microsoft Learn — "What is an Azure subscription?": https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/created-account
