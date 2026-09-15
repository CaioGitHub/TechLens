---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Azure Diagnostic Settings

## O que é?

Diagnostic Settings é a configuração, feita por recurso, que define **quais** categorias de logs/métricas devem ser coletadas e **para onde** esses dados devem ser enviados.

## Modelo

```
Azure Resource
      ↓
Diagnostic Settings
      ↓
Destination
┌────┼─────────────┐
↓    ↓             ↓
Log Analytics  Storage  Event Hub
```

## O que se configura

- **Categorias de logs/métricas**: selecionar quais [[Resource Logs]] (e quais métricas) do recurso devem ser exportados — variam por recurso.
- **Destino(s)**: um mesmo Diagnostic Setting pode enviar dados para múltiplos destinos simultaneamente:
  - **Log Analytics Workspace**: para consulta e análise (ver [[Log Analytics Workspace]]).
  - **Storage Account**: para retenção de longo prazo/arquivamento (ver [[Blob Storage]]).
  - **Event Hub**: para streaming em tempo real para sistemas externos (ex.: um SIEM de terceiros).

## Por recurso

Diagnostic Settings são configurados individualmente por recurso — não existe uma configuração global única que habilita logs para toda a subscription de uma vez.

## Relações

- [[Resource Logs]]
- [[Log Analytics Workspace]]
- [[Azure Monitor]]

## Referências

- Microsoft Learn — "Diagnostic settings in Azure Monitor": https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/diagnostic-settings
