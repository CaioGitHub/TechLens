---
type: technology
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
  - spring
---

# Spring Boot on Azure

## Objetivo

Comparar as opções de hospedagem de uma aplicação Spring Boot no Azure, sem declarar nenhuma como universalmente superior.

## Opções

```
Spring Boot
   ├── App Service
   ├── Container Apps
   ├── AKS
   └── Functions
```

## Comparação

| | [[Azure App Service]] | [[Azure Container Apps]] | [[Azure Kubernetes Service]] | [[Azure Functions]] |
|---|---|---|---|---|
| Complexidade operacional | Baixa | Baixa-média | Alta | Baixa (para o caso de uso certo) |
| Controle | Médio | Médio | Alto | Baixo |
| Escalabilidade | Boa (manual/automática) | Automática, inclusive a zero | Altamente configurável | Automática, orientada a evento |
| Custo (workload constante) | Previsível (capacidade reservada) | Pode ser menor com tráfego variável | Pode ser eficiente em grande escala, mas com overhead operacional | Pode ser muito baixo se o tráfego for esporádico |
| Deployment | `.jar`/WAR direto ou container | Container (imagem) | Container (imagem), manifests Kubernetes | Função individual (não a aplicação inteira tipicamente) |
| Workload ideal | API/aplicação web tradicional, longa duração | Microsserviços, event-driven, containers | Orquestração complexa, múltiplos serviços, times com maturidade K8s | Processamento pontual/orientado a evento — raramente a aplicação Spring Boot inteira |

## Recomendação conceitual (não universal)

Para uma aplicação Spring Boot típica (API monolítica ou poucos serviços, tráfego relativamente constante), [[Azure App Service]] costuma ser o ponto de partida com menor complexidade operacional. [[Azure Container Apps]] é uma alternativa quando já existe uma estratégia de containers e se deseja escala orientada a eventos sem o overhead do Kubernetes. [[Azure Kubernetes Service]] só se justifica com necessidade real de orquestração complexa. Uma aplicação Spring Boot inteira raramente é reescrita como [[Azure Functions]] — Functions se encaixa melhor em processamento pontual complementar.

## Relações

- [[Choosing Azure Compute]]
- [[Java Spring Boot Application on Azure]]
- [[Hexagonal Architecture + Azure]]

## Referências

- Microsoft Learn — "Deploy a Spring Boot application to Azure App Service": https://learn.microsoft.com/en-us/azure/developer/java/spring-framework/deploy-spring-boot-java-app-with-maven-plugin
