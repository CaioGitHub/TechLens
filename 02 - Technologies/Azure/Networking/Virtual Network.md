---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Virtual Network

## O que é?

Uma Virtual Network (VNet) é o mecanismo fundamental de isolamento e segmentação de rede privada dentro do Azure — o espaço de endereçamento IP privado onde os recursos podem se comunicar entre si de forma controlada.

## Modelo

```
Azure
  ↓
Virtual Network
  ├── Subnet A
  ├── Subnet B
  └── Subnet C
```

Uma **Subnet** é uma subdivisão do espaço de endereços da VNet, usada tipicamente para segmentar recursos por função (ex.: uma subnet para a aplicação, outra para o banco de dados) e aplicar regras de rede diferentes a cada segmento (ver [[Network Security Group]]).

## Isolamento e comunicação

Recursos dentro da mesma VNet podem se comunicar por endereço IP privado, sem passar pela internet pública. Comunicação entre VNets diferentes (ou com redes on-premises) exige configuração explícita (peering, VPN, ExpressRoute — mencionados apenas como referência, sem aprofundar).

## Integração com serviços PaaS

Muitos serviços PaaS (ex.: [[Azure App Service]]) podem se integrar a uma VNet ("VNet Integration") para que o tráfego de saída da aplicação passe pela rede privada, permitindo acesso a recursos que não estão expostos publicamente (ex.: um banco de dados com [[Public vs Private Networking|endpoint privado]]).

## Relações

- [[Azure Networking]]
- [[Network Security Group]]
- [[Public vs Private Networking]]

## Referências

- Microsoft Learn — "What is Azure Virtual Network?": https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview
