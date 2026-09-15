---
type: technology
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure App Service

## O que é?

Azure App Service é uma plataforma PaaS totalmente gerenciada para hospedar aplicações web (incluindo APIs), sem exigir que o desenvolvedor gerencie o sistema operacional ou o runtime subjacente.

## Conceitos principais

- **Web App**: a unidade de aplicação hospedada — pode receber um artefato Java (`.jar`/`.war`) diretamente.
- **App Service Plan**: o recurso de computação subjacente (tamanho da VM/SKU, região, quantidade de instâncias) que efetivamente hospeda uma ou mais Web Apps. **Web App ≠ App Service Plan**: a Web App é a aplicação em si; o App Service Plan é a capacidade de computação que a sustenta. Várias Web Apps podem compartilhar o mesmo App Service Plan (dividindo a mesma capacidade), ou cada uma pode ter seu próprio plano — a escolha afeta isolamento de recursos e custo.
- **Deployment**: publicar código/artefato (via CI/CD, Git, container, ou upload direto).
- **Scaling**: escalar verticalmente (mudar o SKU do App Service Plan, mais CPU/RAM) ou horizontalmente (mais instâncias dentro do mesmo plano) — ver [[Azure Scalability]].
- **Configuration/Environment variables**: variáveis configuráveis fora do código (equivalente ao papel de [[Spring Configuration Properties]] no lado da aplicação).
- **TLS/Custom domains**: certificado TLS gerenciado e domínio customizado configuráveis na plataforma.
- **Health checks**: a plataforma pode monitorar um endpoint de saúde da aplicação (ex.: `/actuator/health` do [[Spring Boot Actuator]]) para decidir se uma instância deve receber tráfego.

## Conexão com Spring Boot

```
Spring Boot
    ↓
App Service
    ↓
Azure
```

Um `.jar` executável do Spring Boot pode ser publicado diretamente em um App Service configurado com o runtime Java apropriado — a plataforma cuida do SO, do runtime Java base e da infraestrutura de rede/TLS.

## Deployment Slots

Ver nota dedicada: [[Deployment Slots]].

## App Service não é a única forma de hospedar Spring Boot

Ver comparação completa em [[Spring Boot on Azure]] e [[Choosing Azure Compute]] — [[Azure Container Apps]] e [[Azure Kubernetes Service]] também são opções válidas dependendo do contexto.

## Relações

- [[Azure Compute]]
- [[Deployment Slots]]
- [[Spring Boot on Azure]]
- [[Choosing Azure Compute]]

## Referências

- Microsoft Learn — "Azure App Service overview": https://learn.microsoft.com/en-us/azure/app-service/overview
