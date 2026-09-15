---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Resource

## O que é?

Um Resource é qualquer entidade gerenciável provisionada no Azure — a unidade fundamental que o [[Azure Resource Manager]] cria, atualiza, monitora e remove.

## Exemplos

- App Service (ver [[Azure App Service]])
- Storage Account (ver [[Azure Storage]])
- Key Vault (ver [[Azure Key Vault]])
- Database (ver [[Azure Databases]])
- Container Registry
- Virtual Network (ver [[Virtual Network]])

## Resource ≠ Resource Group

Um Resource é uma instância individual de um serviço (ex.: "esta Storage Account específica"). Um [[Resource Group]] é um **agrupamento lógico** de vários Resources relacionados — não são sinônimos: o Resource Group não é, ele mesmo, um recurso que executa algo; ele organiza recursos.

## Relações

- [[Resource Group]]
- [[Azure Resource Manager]]
- [[Azure Subscription]]

## Referências

- Microsoft Learn — "Azure Resource Manager overview": https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview
