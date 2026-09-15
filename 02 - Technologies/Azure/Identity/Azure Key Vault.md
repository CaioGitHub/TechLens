---
type: technology
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
  - security
---

# Azure Key Vault

## O que é?

Azure Key Vault é o serviço gerenciado do Azure para armazenar e proteger segredos, chaves de criptografia e certificados, evitando que essas informações sensíveis sejam armazenadas em código-fonte ou arquivos de configuração versionados.

## O que ele guarda

- **Secrets**: valores sensíveis genéricos (connection strings, senhas, chaves de API).
- **Keys**: chaves criptográficas gerenciadas (para operações de criptografia/assinatura).
- **Certificates**: certificados TLS/X.509 gerenciados, incluindo renovação.

## Modelo de acesso recomendado

```
Spring Boot
     ↓
Managed Identity
     ↓
Key Vault
     ↓
Secret
```

Em vez da aplicação armazenar uma senha ou connection string diretamente em `application.properties`, ela usa sua [[Managed Identity]] para se autenticar no Key Vault (autorizada via [[Azure RBAC]]) e buscar o segredo em tempo de execução — o segredo nunca fica no código, na imagem de container, nem em um arquivo de configuração versionado.

## Recomendação explícita

> Não armazenar secrets diretamente no código-fonte ou em arquivos de configuração versionados. Usar Key Vault (idealmente acessado via Managed Identity) é a prática recomendada para credenciais de produção.

## Relações

- [[Managed Identity]]
- [[Azure RBAC]]
- [[Spring Profiles]] — Profiles não substituem Key Vault para gerenciamento de segredos.
- [[Azure Security Fundamentals]]

## Referências

- Microsoft Learn — "About Azure Key Vault": https://learn.microsoft.com/en-us/azure/key-vault/general/overview
