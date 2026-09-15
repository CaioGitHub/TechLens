---
type: concept
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - observability
---

# SLI SLO SLA

## Os três conceitos

```
SLI (Service Level Indicator)
↓
o que estou medindo? (ex.: latência P95, taxa de erro)

SLO (Service Level Objective)
↓
qual objetivo quero atingir? (ex.: "P95 < 300ms em 99% do tempo")

SLA (Service Level Agreement)
↓
qual compromisso contratual existe? (ex.: cláusula com o cliente, geralmente com penalidade financeira se violada)
```

## A relação entre eles

Um SLI é a métrica bruta observada; um SLO é a meta interna que a equipe define para esse SLI; um SLA é um compromisso externo/contratual, geralmente mais frouxo que o SLO interno (para dar margem de segurança). Nem todo SLO vira um SLA — muitas equipes têm SLOs internos sem nenhum compromisso contratual formal com clientes.

## Escopo desta nota

Introdução conceitual — a disciplina completa de Site Reliability Engineering (error budgets, burn rate, políticas de resposta) não é aprofundada nesta etapa.

## Relações

- [[Golden Signals]]
- [[Azure Availability]]
- [[Availability Monitoring]]

## Referências

- Google SRE Book — "Service Level Objectives": https://sre.google/sre-book/service-level-objectives/
