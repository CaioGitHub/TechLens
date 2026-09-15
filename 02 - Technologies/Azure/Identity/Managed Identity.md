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

# Managed Identity

## O que é?

Managed Identity é uma identidade gerenciada automaticamente pelo Azure e atribuída a um recurso (ex.: [[Azure App Service]], uma VM), que permite a esse recurso se autenticar em outros serviços Azure ([[Azure Key Vault]], [[Azure SQL]], [[Blob Storage]]) **sem que nenhuma credencial precise ser armazenada no código ou configuração da aplicação**.

## Modelo

```
Application
    ↓
Managed Identity
    ↓
Azure Resource
```

A aplicação solicita um token à Managed Identity (via um endpoint local gerenciado pela plataforma); o Azure emite esse token automaticamente, sem que a aplicação precise conhecer ou manusear nenhum segredo.

## Comparação com abordagens tradicionais

| | Hardcoded Secret | Connection String com senha | Managed Identity |
|---|---|---|---|
| Segredo armazenado em algum lugar (código/config) | Sim, no código (pior caso) | Sim, em configuração | Não |
| Risco de vazamento por commit acidental | Alto | Médio | Nenhum (não há segredo para vazar) |
| Rotação de credencial | Manual | Manual (ou via Key Vault) | Gerenciada automaticamente pelo Azure |
| Necessidade de gerenciar expiração | Sim | Sim | Não (o Azure renova os tokens) |

## Por que isso importa

Credenciais estáticas (senhas, connection strings, chaves de API) armazenadas em configuração ou código são um dos vetores de vazamento mais comuns em incidentes de segurança. Managed Identity elimina a necessidade de armazenar, rotacionar e proteger esse segredo — a autorização passa a ser controlada via [[Azure RBAC]] (conceder à identidade gerenciada permissão sobre o recurso alvo), em vez de "quem tem a senha".

## Dois tipos (visão conceitual)

- **System-assigned**: vinculada ao ciclo de vida de um único recurso (criada e destruída junto com ele).
- **User-assigned**: criada como um recurso independente, podendo ser associada a múltiplos recursos.

## Managed Identity vs. Service Principal

Um **Service Principal** é a identidade que representa uma aplicação/serviço dentro do [[Microsoft Entra ID]] — todo Service Principal precisa de alguma forma de credencial para se autenticar (uma senha/secret, ou um certificado). Uma **Managed Identity** é, na prática, um tipo especial de Service Principal cuja credencial é criada, gerenciada e rotacionada automaticamente pelo Azure — o desenvolvedor nunca vê nem manuseia esse segredo.

| | Service Principal "tradicional" | Managed Identity |
|---|---|---|
| Credencial | Client secret ou certificado — gerenciado manualmente pelo time | Gerenciada e rotacionada automaticamente pelo Azure |
| Uso típico | Aplicações que rodam fora do Azure, ou cenários que exigem uma identidade reutilizável entre ambientes/nuvens | Recursos que já rodam dentro do Azure (App Service, VM, Container App) |
| Risco de vazamento de segredo | Existe (a credencial precisa ser armazenada em algum lugar) | Não há segredo para vazar |

Ou seja: toda Managed Identity é, por baixo, um Service Principal — mas nem todo Service Principal é uma Managed Identity. Quando o recurso já roda no Azure, Managed Identity é preferível por eliminar o gerenciamento manual da credencial.

## Relações

- [[Azure Key Vault]]
- [[Azure RBAC]]
- [[Azure Security Fundamentals]]
- [[Authentication vs Authorization]]

## Referências

- Microsoft Learn — "What are managed identities for Azure resources?": https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview
