---
type: architecture
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
  - hexagonal-architecture
---

# Hexagonal Architecture + Azure

## O ponto central

> Azure é infraestrutura externa. A arquitetura da aplicação não deve depender da existência do Azure para fazer sentido.

Uma aplicação desenhada com [[Hexagonal Architecture]] deveria, em princípio, continuar fazendo sentido conceitual mesmo se toda a infraestrutura Azure fosse substituída por outra (on-premises, outro provedor de nuvem) — porque o [[Application Core]] nunca depende diretamente de nenhum serviço específico do Azure.

## Diagrama

```
                  APPLICATION CORE
                         │
              ┌──────────┴──────────┐
              │                     │
        Output Port            Output Port
              │                     │
              ▼                     ▼
      Database Adapter       Storage Adapter
              │                     │
              ▼                     ▼
        Azure SQL            Blob Storage
```

E do lado de entrada:

```
Input Adapter
     ↓
App Service / Container Apps
     ↓
Spring Boot
     ↓
Input Port
```

## O que isso significa na prática

- O [[Domain]] e os [[Use Case|Use Cases]] não importam nenhum SDK do Azure (`azure-storage-blob`, `azure-identity`, etc.) — essas dependências ficam isoladas nos Adapters.
- Um [[Ports|Repository Port]] definido pelo Core (ex.: `OrderRepository`) é implementado por um Adapter que, por baixo, usa Azure SQL — mas o Core só conhece a interface (ver [[Spring Data Repository vs Repository Port]] e [[Azure SQL]]).
- Um Output Port para armazenar arquivos (ex.: `FileStoragePort`) pode ser implementado por um Adapter que usa [[Blob Storage]] — o Core não sabe que existe um "Azure" por trás dessa Port.
- [[Managed Identity]] e [[Azure Key Vault]] são detalhes de **como** um Adapter se autentica com um serviço Azure — não afetam a assinatura da Port nem o Core.

## Por que isso importa concretamente

Se, no futuro, a organização migrar de Azure SQL para outro banco, ou de Blob Storage para outro serviço de objetos (inclusive de outro provedor de nuvem), apenas os Adapters precisam mudar — o Domain e os Use Cases permanecem intactos, desde que o contrato da Port continue sendo satisfeito.

## Relações

- [[Hexagonal Architecture]]
- [[Application Core]]
- [[Ports]]
- [[Adapters]]
- [[Azure SQL]]
- [[Blob Storage]]
- [[Java Spring Boot Application on Azure]]

## Referências

- Cockburn, Alistair. "Hexagonal Architecture", 2005.
- Microsoft Learn — "Azure Architecture Center": https://learn.microsoft.com/en-us/azure/architecture/
