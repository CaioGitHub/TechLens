---
type: reference
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Choosing Azure Compute

## Objetivo

Guia de decisão conceitual — não uma regra absoluta. Cada resposta deve ser ponderada com trade-offs reais do contexto (custo, equipe, prazo, requisitos).

## Perguntas

**Preciso de controle total do sistema operacional (drivers, software legado, compliance muito específico)?**
→ [[Virtual Machines]]

**Quero PaaS simples para uma aplicação web/API, sem gerenciar containers ou Kubernetes?**
→ [[Azure App Service]]

**Quero executar containers, com escala orientada a eventos, sem administrar um cluster Kubernetes?**
→ [[Azure Container Apps]]

**Preciso realmente de Kubernetes (orquestração complexa, requisitos avançados de scheduling/rede, já tenho maturidade operacional em K8s)?**
→ [[Azure Kubernetes Service]]

**Meu workload é orientado a eventos, de curta duração, sem necessidade de processo sempre ativo?**
→ [[Azure Functions]]

## Trade-offs a considerar em qualquer escolha

- **Complexidade operacional**: quanto a equipe precisa saber/operar (SO, containers, Kubernetes)?
- **Controle vs. abstração**: quanto controle sobre a infraestrutura é realmente necessário?
- **Custo**: capacidade reservada (App Service/AKS) vs. consumo (Functions/Container Apps com escala a zero).
- **Maturidade da equipe**: Kubernetes exige experiência operacional real para ser usado com segurança.
- **Padrão de tráfego**: constante (favorece App Service/AKS) vs. esporádico/orientado a evento (favorece Functions/Container Apps).

## Relações

- [[Azure Compute]]
- [[Spring Boot on Azure]]

## Referências

- Microsoft Learn — "Choose an Azure compute service": https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree
