---
type: concept
status: learning
confidence: 55
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
  - cloud
---

# Cloud Computing

## O que é?

Cloud Computing é o modelo de entrega de recursos de computação (servidores, armazenamento, banco de dados, rede, software) como um serviço sob demanda, pela internet, com cobrança baseada em consumo, em vez de comprar e operar hardware próprio.

## Características centrais

- **Consumo sob demanda (on-demand self-service)**: provisionar recursos sem intervenção humana do provedor.
- **Elasticidade**: capacidade de aumentar ou reduzir recursos automaticamente conforme a demanda.
- **Escalabilidade**: capacidade de crescer (ou reduzir) a capacidade do sistema — ver [[Azure Scalability]].
- **Disponibilidade**: recursos replicados/distribuídos para reduzir indisponibilidade.
- **Responsabilidade compartilhada**: o provedor de nuvem é responsável por parte da pilha (ex.: datacenter, hardware, virtualização); o cliente é responsável pelo restante (ex.: configuração, dados, identidade), variando conforme o modelo de serviço.

## On-Premises vs. Cloud

| | On-Premises | Cloud |
|---|---|---|
| Investimento | Capital upfront (hardware) | Consumo contínuo (OpEx) |
| Escalar | Lento (comprar/instalar hardware) | Rápido (provisionar via API/portal) |
| Operação | Equipe própria cuida de tudo | Provedor cuida de parte da pilha |
| Elasticidade | Limitada à capacidade instalada | Alta |

## IaaS, PaaS, SaaS — responsabilidade compartilhada

```
IaaS (Infrastructure as Service)   → você gerencia SO, runtime, aplicação (ex.: Virtual Machines)
PaaS (Platform as Service)          → provedor gerencia SO/runtime; você gerencia aplicação (ex.: App Service)
SaaS (Software as Service)          → provedor gerencia tudo; você apenas usa o software (ex.: Microsoft 365)
```

Quanto mais alto no modelo (IaaS → PaaS → SaaS), menos responsabilidade operacional para o cliente, e menos controle sobre a infraestrutura subjacente.

## Conexão com o contexto deste Second Brain

```
Spring Boot Application
        ↓
Cloud Platform
        ↓
Azure
```

Uma aplicação [[Spring Boot]] pode ser hospedada em qualquer um dos modelos (ex.: uma VM = IaaS, [[Azure App Service]] = PaaS) — a escolha do modelo afeta quanto de responsabilidade operacional cabe ao time, não a arquitetura da aplicação em si.

## Relações

- [[Azure]]
- [[Azure Resource]]
- [[Azure Scalability]]

## Referências

- Microsoft Learn — "What is cloud computing?": https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/getting-started/what-is-azure
