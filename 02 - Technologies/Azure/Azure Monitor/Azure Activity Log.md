---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Azure Activity Log

## O que é?

O Activity Log registra operações de **gerenciamento** realizadas sobre recursos Azure — eventos do control plane (ver [[Azure Resource Manager]]), coletados automaticamente para toda a subscription.

## Exemplos conceituais

- Create Resource
- Delete Resource
- Update Resource
- Configuration Change (ex.: alterar uma regra de RBAC)

## Diferenciação importante

- **Activity Log**: "o que foi feito **sobre** o recurso" (quem criou, alterou ou removeu um recurso) — nível de subscription, sempre coletado.
- **Resource Logs**: "o que aconteceu **dentro** do recurso durante sua operação" (ver [[Resource Logs]]) — específico de cada recurso, requer configuração.
- **Application Logs**: "o que aconteceu dentro do código da aplicação" (ver [[Application Logs]]) — gerado pelo próprio código, não pelo Azure.

## Relações

- [[Resource Logs]]
- [[Application Logs]]
- [[Azure Resource Manager]]
- [[Azure Diagnostic Settings]]

## Referências

- Microsoft Learn — "Azure Activity log": https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/activity-log
