---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Managed Database

## O que é?

"Managed Service" (aplicado a bancos de dados) significa que o provedor de nuvem assume a responsabilidade operacional de manter o banco funcionando — em contraste com um banco self-managed, onde o próprio time instala, corrige e opera o motor de banco de dados (ex.: em uma VM).

## Self-managed vs. Managed

| Responsabilidade | Self-managed (ex.: PostgreSQL em uma VM) | Managed (ex.: [[Azure SQL]]) |
|---|---|---|
| Patching do motor de banco | Seu time | Provedor |
| Backups | Configurar e testar manualmente | Automatizados pela plataforma (com opções de configuração) |
| Alta disponibilidade | Configurar réplicas manualmente | Oferecida como opção/configuração do serviço |
| Scaling | Redimensionar a VM/discos manualmente | Ajustar tier/SKU pela plataforma |
| Responsabilidade operacional | Alta | Baixa (mas não zero — configuração, monitoramento e uso continuam sendo do time) |

## Por que isso importa

Um banco gerenciado reduz significativamente o esforço operacional (patching, backup, failover), ao custo de menos controle sobre a configuração de baixo nível do motor de banco — um trade-off típico de PaaS (ver [[Cloud Computing]]).

## Relações

- [[Azure Databases]]
- [[Azure SQL]]
- [[Cloud Computing]]

## Referências

- Microsoft Learn — "Databases on Azure": https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/data-store-overview
