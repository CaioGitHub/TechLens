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

# Public vs Private Networking

## O ponto central

```
Internet
   ↓
Public Endpoint          (acessível a partir da internet pública)

Private Network
   ↓
Private Endpoint         (acessível apenas dentro da rede privada / VNet)
```

## Public Endpoint

Um recurso com endpoint público possui um endereço acessível pela internet — conveniente, mas expande a superfície de ataque. Controles adicionais (autenticação, [[Network Security Group|regras de firewall/NSG]], TLS) tornam-se ainda mais importantes quando um endpoint é público.

## Private Endpoint

Um Private Endpoint conecta um serviço PaaS (ex.: [[Azure SQL]], [[Blob Storage]]) diretamente dentro de uma [[Virtual Network]], usando um endereço IP privado — o serviço deixa de ser acessível pela internet pública, reduzindo significativamente a superfície de ataque.

## Comparação

| | Public Endpoint | Private Endpoint |
|---|---|---|
| Acessibilidade | Internet pública (com controles de autenticação/firewall) | Somente dentro da VNet configurada |
| Superfície de ataque | Maior | Menor |
| Complexidade de rede | Baixa | Maior (exige VNet, DNS privado configurado) |
| Uso típico | Cenários simples, protótipos, APIs realmente públicas | Comunicação entre serviços internos, dados sensíveis |

## Conexão com segurança

Expor um serviço desnecessariamente à internet quando um endpoint privado seria suficiente é um anti-pattern comum (ver [[Azure Anti-Patterns]]) — reduz a superfície de ataque sem custo funcional real na maioria dos cenários internos.

## Relações

- [[Virtual Network]]
- [[Azure Security Fundamentals]]
- [[Azure Anti-Patterns]]

## Referências

- Microsoft Learn — "What is a private endpoint?": https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview
