---
type: reference
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Azure Monitoring Alerting Strategy

## Conceito principal

> Um bom sistema de alertas deve ajudar uma equipe a agir, não apenas produzir notificações.

## Princípios

- **Evitar alertas excessivos**: cada alerta configurado deve justificar sua existência — alertas demais treinam a equipe a ignorá-los ("alert fatigue").
- **Alertar sobre condições acionáveis**: se não há nenhuma ação possível quando o alerta dispara, ele provavelmente não deveria existir (ou deveria ser apenas informativo, sem notificação ativa).
- **Definir thresholds com contexto**: um threshold copiado de outro sistema sem considerar o comportamento real do recurso tende a gerar falsos positivos ou negativos.
- **Reduzir noise**: agrupar/correlacionar condições relacionadas em vez de gerar múltiplos alertas para sintomas do mesmo problema.
- **Priorizar impacto**: severidade deve refletir o impacto real no usuário/negócio, não a conveniência técnica de medir aquele sinal.
- **Associar ações apropriadas**: cada alerta relevante deveria ter um [[Azure Monitor Action Groups|Action Group]] claro — quem é notificado e o que se espera que essa pessoa/sistema faça.

## Relações

- [[Azure Monitor Alerts]]
- [[Azure Monitor Action Groups]]
- [[Severity]]
- [[Azure Monitor Anti-Patterns]]

## Referências

- Microsoft Learn — "Best practices for alerting": https://learn.microsoft.com/en-us/azure/azure-monitor/best-practices-alerts
