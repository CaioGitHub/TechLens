---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Virtual Machines

## O que é?

Um Virtual Machine (VM) no Azure é um servidor virtualizado completo (IaaS): você recebe controle total sobre o sistema operacional, mas também assume a responsabilidade operacional correspondente.

## Responsabilidades do operador de uma VM

- **OS**: escolher, atualizar e proteger o sistema operacional (patching).
- **Networking**: configurar rede, IPs, regras de firewall (ver [[Azure Networking]]).
- **Storage**: gerenciar discos anexados.
- **Patching**: aplicar atualizações de segurança do SO e runtime manualmente ou via automação própria.
- **Scaling**: configurar manualmente (ou via Scale Sets) o aumento/redução do número de instâncias.

## Onde uma aplicação Java roda em uma VM

```
Java Application
      ↓
JVM
      ↓
Operating System
      ↓
Virtual Machine
      ↓
Azure
```

A aplicação e a JVM não sabem que estão em uma VM na nuvem — do ponto de vista da aplicação, é apenas um sistema operacional com uma JVM instalada. A VM é a camada de infraestrutura sobre a qual tudo isso roda.

## Quando usar

- Necessidade real de controle total do SO (drivers específicos, software legado, requisitos de compliance muito específicos).
- Migração direta ("lift-and-shift") de uma aplicação já existente sem refatoração.

## Quando evitar

- Quando [[Azure App Service]] ou [[Azure Container Apps]] atendem ao caso de uso — evita o custo operacional de gerenciar o SO manualmente.

## Relações

- [[Azure Compute]]
- [[Choosing Azure Compute]]

## Referências

- Microsoft Learn — "Virtual machines in Azure": https://learn.microsoft.com/en-us/azure/virtual-machines/overview
