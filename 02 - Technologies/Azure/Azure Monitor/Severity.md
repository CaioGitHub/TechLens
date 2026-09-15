---
type: concept
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Severity

## O que é?

Severidade é a classificação de importância atribuída a um alerta quando ele dispara — ajuda a equipe a priorizar qual alerta exige atenção imediata.

## Níveis comuns (conceitual)

- **Informational**: relevante para registro, sem necessidade de ação imediata.
- **Warning**: indica um problema potencial que merece atenção, mas não é crítico.
- **Critical**: indica um problema que exige ação imediata (ex.: indisponibilidade do serviço).

## Não generalizar

O significado exato e a escala de severidade (ex.: níveis numéricos como Sev 0–4 usados pelo Azure Monitor) variam conforme a configuração adotada pela organização — não existe um significado universal idêntico entre diferentes produtos, times ou sistemas de alerta.

## Relações

- [[Azure Monitor Alerts]]
- [[Azure Monitoring Alerting Strategy]]

## Referências

- Microsoft Learn — "Alert severity": https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-overview
