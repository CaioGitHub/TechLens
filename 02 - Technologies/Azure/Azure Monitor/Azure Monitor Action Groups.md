---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Azure Monitor Action Groups

## O que é?

Um Action Group é uma coleção reutilizável de ações de notificação/automação, que pode ser associada a um ou mais Alert Rules.

## Modelo

```
Alert
  ↓
Action Group
  ├── Email
  ├── SMS
  ├── Webhook
  └── Automation
```

## Por que reutilizável

Em vez de configurar "enviar e-mail para o time X" separadamente em cada Alert Rule, um Action Group é definido uma vez (ex.: "Time de Plataforma") e referenciado por múltiplas regras — mudar o destinatário em um único lugar atualiza todos os alertas associados.

## Escopo desta nota

Não é uma lista exaustiva de integrações possíveis (existem várias: ITSM, Logic Apps, Azure Functions, runbooks) — o conceito central é "conjunto reutilizável de ações", independentemente de quantas integrações específicas existam.

## Relações

- [[Azure Monitor Alerts]]
- [[Azure Monitoring Alerting Strategy]]

## Referências

- Microsoft Learn — "Action groups": https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/action-groups
