---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
  - security
---

# Authentication vs Authorization

## A distinção central

```
Authentication
    ↓
Who are you? (você é quem diz ser?)

Authorization
    ↓
What can you do? (o que você tem permissão de fazer?)
```

Estas são etapas sequenciais e distintas: primeiro o sistema confirma a identidade (Authentication); só depois decide o que essa identidade pode fazer (Authorization). É possível estar autenticado e ainda assim não autorizado a realizar uma ação específica.

## No contexto Azure

- **Authentication**: tipicamente resolvida por um identity provider — [[Microsoft Entra ID]].
- **Authorization**: tipicamente resolvida por [[Azure RBAC]] (para o control plane do Azure) ou por lógica de autorização própria da aplicação (para o data plane/regras de negócio).

## Relações

- [[Microsoft Entra ID]]
- [[Azure RBAC]]
- [[Managed Identity]]

## Referências

- Microsoft Learn — "Authentication vs. authorization": https://learn.microsoft.com/en-us/entra/identity-platform/authentication-vs-authorization
