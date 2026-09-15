---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Resource Group

## O que é?

Um Resource Group é um **agrupamento lógico** de [[Azure Resource|Resources]] do Azure que compartilham o mesmo ciclo de vida, permissões ou finalidade — não é "uma pasta" no sentido de armazenamento físico; é uma fronteira de gerenciamento.

## Modelo

```
Subscription
    ↓
Resource Group
    ├── App Service
    ├── Database
    ├── Key Vault
    └── Storage
```

## Finalidade

- **Ciclo de vida**: recursos de um mesmo Resource Group tipicamente nascem e morrem juntos (ex.: remover o Resource Group remove todos os recursos dentro dele).
- **Gerenciamento**: aplicar permissões ([[Azure RBAC]]) e políticas em um único lugar, herdadas por todos os recursos contidos.
- **Custos**: visualizar e filtrar custos agregados por Resource Group.
- **Organização lógica**: agrupar por ambiente (dev/staging/prod), por aplicação, ou por time — a convenção varia por organização (ver [[Azure Naming and Organization]]).

## Não é sinônimo de

- **Resource** (ver [[Azure Resource]]) — o Resource Group não executa nada, ele organiza.
- **Region** — um Resource Group tem uma região associada aos seus metadados, mas os recursos dentro dele podem estar em regiões diferentes.

## Relações

- [[Azure Subscription]]
- [[Azure Resource]]
- [[Azure Resource Manager]]
- [[Azure Naming and Organization]]

## Referências

- Microsoft Learn — "Manage Azure resources by using the Azure portal": https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/manage-resource-groups-portal
