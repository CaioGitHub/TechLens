---
type: troubleshooting
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Azure Monitor Troubleshooting

## Processo conceitual

```
Problema percebido
       ↓
Identificar impacto
       ↓
Metrics
       ↓
Logs
       ↓
Traces
       ↓
Encontrar causa provável
       ↓
Validar hipótese
       ↓
Corrigir
       ↓
Monitorar novamente
```

## Cenário 1 — Erros aumentando, CPU e requests normais

Uma API Spring Boot no Azure começa a gerar HTTP 500 para usuários. CPU está normal, número de requests está normal, mas o error rate subiu.

```
Problem
  ↓
Metrics → Error Rate elevado (ex.: 8%)
  ↓
Logs → buscar exceções recentes (ex.: NullPointerException em OrderService)
  ↓
Trace → identificar em qual span/dependência a falha ocorre
  ↓
Dependency → ex.: chamada a uma API externa retornando payload inesperado
  ↓
Root Cause
```

Raciocínio: como CPU/requests estão normais, o problema não é de capacidade — é algo específico no comportamento do código ou de uma dependência, revelado pela combinação de métrica (detecção) + log (contexto da exceção) + trace (onde no fluxo ela ocorre).

## Cenário 2 — Aplicação lenta, mas funcionando

```
Latency
   ↓
Metrics → confirmar aumento de latência (ex.: P95 subiu)
   ↓
Trace → identificar qual span está consumindo mais tempo
   ↓
Dependency Duration → ex.: tempo de consulta ao banco aumentou
   ↓
Database / External API
   ↓
Root Cause
```

Raciocínio: latência alta sem erro explícito costuma apontar para uma dependência específica (banco, API externa) — o trace revela **onde**, no caminho da requisição, o tempo está sendo gasto.

## Cenário 3 — Aplicação "saudável", mas inacessível

```
Availability
   ↓
Endpoint → o endpoint está acessível externamente?
   ↓
Networking → DNS, NSG, Application Gateway estão roteando corretamente?
   ↓
Application → o processo está de fato respondendo?
   ↓
Health Check → o que o health check reporta?
   ↓
Logs / Metrics → confirmar hipótese
```

Raciocínio: "saudável" internamente (processo rodando, health check OK) não implica acessível externamente — o problema pode estar em uma camada de rede (ver [[Availability Monitoring]] e a ressalva sobre [[Health Check]]).

## Nota de escopo

Este processo é apenas o raciocínio conceitual — não um catálogo de erros específicos nem consultas KQL prontas (isso pertence à Etapa 9).

## Relações

- [[Metrics Logs Traces]]
- [[Correlation]]
- [[Availability Monitoring]]
- [[Performance Monitoring]]

## Referências

- Microsoft Learn — "Azure Monitor overview": https://learn.microsoft.com/en-us/azure/azure-monitor/fundamentals/overview
