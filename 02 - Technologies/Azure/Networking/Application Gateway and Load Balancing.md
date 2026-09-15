---
type: concept
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Application Gateway and Load Balancing

## O que é Load Balancing?

Distribuir tráfego de entrada entre múltiplas instâncias de uma aplicação, evitando sobrecarregar uma única instância e permitindo escalar horizontalmente (ver [[Azure Scalability]]).

## Application Gateway (Layer 7)

Um Application Gateway opera na camada de aplicação (HTTP/HTTPS — "Layer 7" do modelo OSI), permitindo decisões de roteamento baseadas em conteúdo da requisição (caminho da URL, cabeçalhos), além de:

- **TLS termination**: o Gateway decripta o tráfego TLS, permitindo que as instâncias internas recebam tráfego HTTP simples (dentro da rede privada), simplificando o gerenciamento de certificados.
- **Health probes**: verificações periódicas de saúde das instâncias (ex.: contra `/actuator/health` do [[Spring Boot Actuator]]) para retirar instâncias não saudáveis da rotação.

## Onde entra na arquitetura

```
Internet
   ↓
Application Gateway (Layer 7, TLS termination, routing)
   ↓
Instâncias da aplicação (ex.: App Service, Container Apps, VMs)
```

## Escopo desta nota

Esta base cobre apenas o suficiente para reconhecer o papel de um load balancer/gateway em uma arquitetura Azure — não aprofunda configurações avançadas de roteamento, WAF ou regras complexas.

## Relações

- [[Azure Networking]]
- [[Azure Scalability]]
- [[Azure App Service]]

## Referências

- Microsoft Learn — "What is Azure Application Gateway?": https://learn.microsoft.com/en-us/azure/application-gateway/overview
