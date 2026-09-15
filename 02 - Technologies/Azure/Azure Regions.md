---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Regions

## O que é uma Region?

Uma Region é um conjunto de um ou mais datacenters, situados dentro de uma área geográfica com latência definida, conectados por uma rede de baixa latência dedicada da Microsoft. **Region não é sinônimo de datacenter**: uma região pode conter múltiplos datacenters (frequentemente organizados em [[Azure Availability Zones]]).

## Por que a escolha de região importa

- **Latência**: escolher uma região próxima dos usuários finais reduz latência de rede.
- **Residência de dados (data residency)**: alguns requisitos legais/regulatórios exigem que dados permaneçam dentro de fronteiras geográficas específicas.
- **Disponibilidade de serviços**: nem todo serviço Azure está disponível em toda região — é preciso verificar disponibilidade regional antes de planejar uma arquitetura.
- **Preço**: custos de alguns serviços podem variar por região.

## Region Pairs

Um Region Pair é um relacionamento definido pela Microsoft entre duas regiões dentro da mesma geografia, usado para:

- Sequenciar manutenções planejadas (as duas regiões de um par não recebem atualizações simultaneamente).
- Priorizar recuperação: em uma falha catastrófica que afete uma geografia inteira, a Microsoft prioriza restaurar pelo menos uma região de cada par.
- Servir de base para recursos de geo-replicação de alguns serviços (ex.: Geo-Redundant Storage).

### Region Pair NÃO é

> Um mecanismo automático de disaster recovery.

Usar uma região pareada **não** garante, por si só, alta disponibilidade ou recuperação de desastre para a sua aplicação — a organização ainda precisa desenhar sua própria estratégia de [[RPO and RTO|RPO/RTO]] e failover usando o par de regiões como um building block. Nem toda região possui um par (algumas dependem de [[Azure Availability Zones]] como mecanismo primário de redundância).

## Relações

- [[Azure Availability Zones]]
- [[RPO and RTO]]
- [[Azure Scalability]]

## Referências

- Microsoft Learn — "Azure regions and Availability Zones": https://learn.microsoft.com/en-us/azure/reliability/regions-overview
- Microsoft Learn — "Azure region pairs and nonpaired regions": https://learn.microsoft.com/en-us/azure/reliability/regions-paired
