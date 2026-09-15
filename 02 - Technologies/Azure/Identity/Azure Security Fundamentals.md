---
type: architecture
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
  - security
---

# Azure Security Fundamentals

## Objetivo

Conectar os conceitos de segurança já apresentados em um modelo mental único.

## O modelo

```
Identity ([[Microsoft Entra ID]])
   +
RBAC ([[Azure RBAC]])
   +
Network Security ([[Network Security Group]], [[Public vs Private Networking]])
   +
Key Vault ([[Azure Key Vault]])
   +
Managed Identity ([[Managed Identity]])
```

Nenhum desses mecanismos, isoladamente, resolve segurança por completo — eles se complementam: identidade confirma quem é; RBAC decide o que essa identidade pode fazer; rede controla por onde o tráfego pode passar; Key Vault protege segredos; Managed Identity elimina a necessidade de armazenar credenciais para que os outros mecanismos funcionem entre serviços.

## Responsabilidade compartilhada

Assim como em [[Cloud Computing]], segurança no Azure segue um modelo de responsabilidade compartilhada: a Microsoft protege a infraestrutura física e a plataforma; o cliente continua responsável por configurar identidade, rede, segredos e código da aplicação corretamente. Um serviço PaaS não torna a aplicação automaticamente segura.

## Relações

- [[Microsoft Entra ID]]
- [[Azure RBAC]]
- [[Managed Identity]]
- [[Azure Key Vault]]
- [[Network Security Group]]
- [[Azure Anti-Patterns]]

## Referências

- Microsoft Learn — "Azure security fundamentals": https://learn.microsoft.com/en-us/azure/security/fundamentals/overview
