---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Availability Zones

## O que são?

Availability Zones (AZs) são localizações físicas fisicamente separadas dentro de uma mesma [[Azure Regions|Region]] — cada zona é composta por um ou mais datacenters com energia, resfriamento e rede independentes.

## Modelo

```
Azure Region
├── Availability Zone 1
├── Availability Zone 2
└── Availability Zone 3
```

## Por que existem

Isolar falhas: um problema de energia, resfriamento ou rede em uma zona não deve derrubar as outras zonas da mesma região. Distribuir uma aplicação entre zonas aumenta a disponibilidade sem exigir uma região geograficamente distante (evitando a latência extra de replicar entre regiões).

## Fault domains

Cada Availability Zone representa, na prática, um fault domain independente — falhas de infraestrutura física tendem a ficar contidas dentro de uma única zona.

## Suporte variável por serviço — não generalizar

Nem todo serviço Azure suporta Availability Zones da mesma forma. Existem variações: alguns serviços são **zone-redundant** automaticamente (o próprio serviço replica entre zonas sem configuração extra), outros são **zonal** (você escolhe explicitamente uma zona específica para uma instância), e outros ainda podem não ter suporte a zonas em determinadas regiões. É necessário verificar a documentação específica de cada serviço antes de assumir suporte a zonas.

## Relações

- [[Azure Regions]]
- [[Azure Scalability]]
- [[RPO and RTO]]

## Referências

- Microsoft Learn — "Azure regions and Availability Zones": https://learn.microsoft.com/en-us/azure/reliability/regions-overview
