---
type: concept
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure DNS

## O que é?

Serviço do Azure para hospedar e resolver nomes de domínio (DNS — Domain Name System), traduzindo um hostname legível (ex.: `api.minhaempresa.com`) para o endereço IP do recurso correspondente.

## Fluxo conceitual

```
Client
  ↓
DNS (resolve hostname → IP)
  ↓
Application
```

## Custom Domain

Serviços como [[Azure App Service]] fornecem um domínio padrão (`*.azurewebsites.net`), mas é comum configurar um domínio próprio (custom domain) apontando para o recurso, geralmente combinado com um certificado TLS.

## Private DNS

Para recursos acessados via [[Public vs Private Networking|Private Endpoint]], é necessário DNS privado (zona DNS privada dentro da VNet) para que o hostname do serviço resolva para o endereço IP privado, em vez do público — detalhe frequentemente esquecido ao configurar Private Endpoints.

## Relações

- [[Azure Networking]]
- [[Public vs Private Networking]]

## Referências

- Microsoft Learn — "What is Azure DNS?": https://learn.microsoft.com/en-us/azure/dns/dns-overview
