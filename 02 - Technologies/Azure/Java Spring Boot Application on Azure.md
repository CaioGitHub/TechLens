---
type: architecture
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
  - spring
  - hexagonal-architecture
---

# Java Spring Boot Application on Azure

## Cenário integrado

```
                    INTERNET
                        │
                        ▼
                  Azure Network
                        │
                        ▼
                 Spring Boot API
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
        Azure Database        Azure Storage
             │
             │
        Key Vault
             │
             ▼
      Managed Identity
```

## Leitura do diagrama

- **Azure Network**: a aplicação recebe tráfego através de rede/gateway (ver [[Azure Networking]], [[Application Gateway and Load Balancing]]), antes de chegar ao processo Spring Boot.
- **Spring Boot API**: o processo em execução (hospedado em [[Azure App Service]], [[Azure Container Apps]] ou outra opção — ver [[Spring Boot on Azure]]).
- **Azure Database**: acessada através de um Adapter de persistência (ver [[Azure SQL]]).
- **Azure Storage**: acessada através de outro Adapter, para arquivos (ver [[Blob Storage]]).
- **Key Vault + Managed Identity**: a aplicação obtém segredos (connection strings, chaves) sem armazená-los — a [[Managed Identity]] do App Service/Container App é autorizada (via [[Azure RBAC]]) a ler do [[Azure Key Vault]].

## Conectando com a arquitetura da aplicação

```
Spring Boot
     ↓
Hexagonal Architecture
     ↓
Azure Adapters
     ↓
Azure Services
```

O Spring Boot fornece o runtime/framework de aplicação; a Hexagonal Architecture organiza onde cada dependência externa (banco, storage, segredos) entra através de uma Port/Adapter; os Azure Adapters são as implementações concretas que efetivamente chamam os SDKs/APIs do Azure. Ver detalhamento da fronteira em [[Hexagonal Architecture + Azure]].

## Relações

- [[Spring Boot on Azure]]
- [[Hexagonal Architecture + Azure]]
- [[Azure SQL]]
- [[Blob Storage]]
- [[Azure Key Vault]]
- [[Managed Identity]]

## Referências

- Microsoft Learn — "Azure Architecture Center — Web application architectures": https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree
