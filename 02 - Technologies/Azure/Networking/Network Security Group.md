---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
  - security
---

# Network Security Group

## O que é?

Um Network Security Group (NSG) é um conjunto de regras de permitir/negar tráfego de rede, aplicado a uma [[Virtual Network|Subnet]] ou a uma interface de rede específica de um recurso.

## Regras

- **Inbound**: controla tráfego entrando no recurso/subnet (ex.: permitir porta 443 de qualquer origem, negar todo o resto).
- **Outbound**: controla tráfego saindo do recurso/subnet.
- Cada regra tem prioridade, protocolo, porta, origem e destino.

## Onde se aplica

NSGs podem ser associados a uma subnet inteira (afetando todos os recursos dentro dela) ou a uma interface de rede individual — regras aplicadas em ambos os níveis são combinadas.

## NSG não é um firewall de aplicação completo

Este é o ponto de atenção mais importante: NSG opera nas camadas de rede/transporte (endereço IP, porta, protocolo) — ele **não** inspeciona o conteúdo da aplicação (ex.: não filtra por padrões de payload HTTP, não é um Web Application Firewall). Para proteção na camada de aplicação, é necessário um serviço dedicado (ex.: Application Gateway com WAF, mencionado aqui apenas como referência).

## Relações

- [[Virtual Network]]
- [[Public vs Private Networking]]
- [[Azure Security Fundamentals]]

## Referências

- Microsoft Learn — "Network security groups": https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview
