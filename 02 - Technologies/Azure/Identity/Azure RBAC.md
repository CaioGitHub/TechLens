---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
  - security
---

# Azure RBAC

## O que é?

Azure RBAC (Role-Based Access Control) é o sistema de autorização do Azure: define **o que** uma identidade já autenticada (ver [[Authentication vs Authorization]]) tem permissão de fazer, e **sobre qual escopo**.

## Modelo

```
Identity (usuário, grupo, Service Principal ou Managed Identity)
   ↓
Role (conjunto de permissões, ex.: "Reader", "Contributor", ou uma role customizada)
   ↓
Scope (onde a role se aplica: Management Group, Subscription, Resource Group ou Resource individual)
   ↓
Permission (a ação efetivamente permitida ou negada)
```

## Componentes

- **Role**: um conjunto nomeado de permissões (ex.: "pode ler dados de um Storage Account", "pode gerenciar Virtual Machines").
- **Principal**: quem está recebendo a role — pode ser um usuário, um grupo, um Service Principal ou uma [[Managed Identity]] (uma Managed Identity é, por baixo, um tipo de Service Principal com credencial gerenciada automaticamente — ver distinção completa em [[Managed Identity]]).
- **Scope**: o nível hierárquico onde a atribuição se aplica — de um recurso individual até um Management Group inteiro (ver [[Azure Subscription]]).

## Authentication vs. Authorization vs. RBAC

- **Authentication**: confirma quem é a identidade (ver [[Microsoft Entra ID]]).
- **Authorization**: decisão geral de "o que pode ser feito".
- **RBAC**: o **mecanismo específico** do Azure para implementar Authorization no control plane (ver [[Azure Resource Manager]]) — atribuindo roles a principals em determinados scopes.

## Relações

- [[Authentication vs Authorization]]
- [[Managed Identity]]
- [[Azure Resource Manager]]
- [[Azure Subscription]]

## Referências

- Microsoft Learn — "What is Azure role-based access control (Azure RBAC)?": https://learn.microsoft.com/en-us/azure/role-based-access-control/overview
