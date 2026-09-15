---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Deployment

## O que é?

O processo de levar código-fonte até um recurso Azure em execução.

## Fluxo conceitual

```
Code
  ↓
Build (compilar, empacotar — ex.: gerar o .jar do Spring Boot)
  ↓
Artifact (o .jar, ou uma imagem de container)
  ↓
Deployment (publicar o artifact no recurso Azure)
  ↓
Azure Resource (ex.: App Service, Container Apps)
  ↓
Running Application
```

## Formas de deployment

- **Manual deployment**: publicar o artefato diretamente (ex.: via portal, CLI) — simples, mas não repetível/auditável facilmente.
- **CI/CD**: pipeline automatizado que builda, testa e publica a cada mudança de código — mencionado aqui apenas como contexto; pipelines não são aprofundados nesta etapa.
- **Deployment Slots**: ver [[Deployment Slots]] — permite validar antes de promover para produção.
- **Containers**: publicar uma imagem de container em vez de um artefato de linguagem específica — mesma ideia de fluxo, unidade de deployment diferente.
- **Infrastructure as Code**: ver [[Infrastructure as Code]] — a própria infraestrutura (não só o código da aplicação) é versionada e implantada de forma declarativa.

## Relações

- [[Deployment Slots]]
- [[Infrastructure as Code]]
- [[Azure App Service]]

## Referências

- Microsoft Learn — "Deploy your app to Azure App Service": https://learn.microsoft.com/en-us/azure/app-service/deploy-best-practices
