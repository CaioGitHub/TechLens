---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
  - hexagonal-architecture
  - observability
---

# Observability Signals vs Application Architecture

## A distinção central

- **Architecture** define **como** responsabilidades e dependências são organizadas dentro do código (ex.: [[Hexagonal Architecture]] separando Core de Adapters).
- **Observability** permite **compreender o comportamento** do sistema em execução (o que realmente aconteceu em produção, não como o código foi organizado).

## Por que não confundir

Uma aplicação pode ter uma arquitetura excelente (bem separada, testável) e ainda assim ser pouco observável (poucos logs úteis, nenhuma métrica de negócio exposta) — e o inverso também é possível: uma aplicação mal arquiteturada pode ter ótima instrumentação. Os dois são **complementares**, não a mesma coisa: arquitetura organiza o código; observabilidade revela o comportamento real desse código em produção.

## Relações

- [[Hexagonal Architecture + Observability]]
- [[Monitoring vs Observability]]

## Referências

- Microsoft Learn — "Azure Monitor overview": https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview
