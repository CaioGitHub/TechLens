---
type: technology
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Kubernetes Service

## O que é?

Azure Kubernetes Service (AKS) é a oferta de Kubernetes gerenciado do Azure: a Microsoft opera o *control plane* do Kubernetes (o componente que decide onde e como rodar as cargas de trabalho); você continua responsável por operar os *nodes* de trabalho e as aplicações rodando neles.

## Vocabulário mínimo do Kubernetes (o suficiente para entender onde AKS entra)

- **Cluster**: conjunto de máquinas (nodes) que executam containers de forma coordenada.
- **Node**: uma máquina (VM) que faz parte do cluster e efetivamente roda os containers.
- **Pod**: a menor unidade executável do Kubernetes — um ou mais containers que compartilham rede/armazenamento.
- **Deployment**: descreve declarativamente quantas réplicas de um Pod devem existir e como atualizá-las.
- **Service**: expõe um conjunto de Pods sob um endereço de rede estável, mesmo que os Pods individuais mudem.

## Modelo

```
Azure
  ↓
AKS
  ↓
Kubernetes Cluster
  ↓
Nodes
  ↓
Pods
  ↓
Application
```

## O que "managed" significa aqui

A Microsoft opera e atualiza o control plane do Kubernetes (sem custo direto de gerenciamento do control plane em si, na maioria dos casos); o cliente continua responsável por dimensionar e corrigir os nodes (embora existam recursos gerenciados adicionais, como node pools automáticos, que reduzem esse esforço).

## Quando realmente faz sentido usar AKS

- Já existe uma necessidade real e madura de orquestração Kubernetes (múltiplos serviços, deployments complexos, requisitos específicos de scheduling/rede que só o Kubernetes resolve).
- A equipe já possui ou está disposta a desenvolver expertise operacional em Kubernetes.

Para a maioria das aplicações Spring Boot single-service, [[Azure App Service]] ou [[Azure Container Apps]] entregam o necessário com muito menos complexidade operacional — ver [[Choosing Azure Compute]].

## Escopo desta nota

Esta base não é um curso de Kubernetes — apenas o vocabulário mínimo para reconhecer quando AKS aparece no desenho de uma arquitetura Azure.

## Relações

- [[Azure Compute]]
- [[Azure Container Apps]]
- [[Choosing Azure Compute]]

## Referências

- Microsoft Learn — "Azure Kubernetes Service (AKS)": https://learn.microsoft.com/en-us/azure/aks/what-is-aks
