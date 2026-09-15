---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Deployment Slots

## O que é?

Um Deployment Slot é uma instância adicional de uma aplicação [[Azure App Service]], com sua própria URL, que permite validar uma nova versão do código antes de expô-la ao tráfego de produção.

## Modelo

```
App Service
├── Production (slot principal)
└── Staging (slot adicional)
```

## Swap

A operação central é o **swap**: trocar o conteúdo do slot de staging com o de produção (efetivamente promovendo a versão validada para produção) de forma que minimiza downtime — a plataforma reencaminha o tráfego para o novo conteúdo sem exigir um novo ciclo completo de deployment.

## Benefícios

- Validar a aplicação (incluindo "warm-up" e testes de fumaça) em um ambiente idêntico ao de produção antes do swap.
- Reduzir o tempo de indisponibilidade percebido durante um deployment.
- Possibilidade de reverter rapidamente (swap de volta) se um problema for detectado logo após a promoção.

## Limitações

- Slots adicionais podem não estar disponíveis em todos os tiers/SKUs de App Service.
- Configurações específicas de ambiente (connection strings, variáveis) precisam ser tratadas com cuidado durante o swap — algumas podem (ou devem) ser "sticky" a um slot específico, para não vazar configuração de staging para produção ou vice-versa.

## Relações

- [[Azure App Service]]
- [[Azure Deployment]]

## Referências

- Microsoft Learn — "Set up staging environments in Azure App Service": https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots
