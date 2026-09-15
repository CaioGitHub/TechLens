---
type: troubleshooting
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - application-insights
  - troubleshooting
---

# Application Insights Troubleshooting

## Modelo geral de investigação

```
Problema
   ↓
Impacto
   ↓
Requests / Metrics
   ↓
Exceptions / Logs
   ↓
Traces / Dependencies
   ↓
Hipótese
   ↓
Validação
   ↓
Correção
```

## Cenário 1 — HTTP 500

Usuários relatam erro 500.

```
Request
   ↓
Error Rate
   ↓
Failed Requests
   ↓
Exception
   ↓
Trace
   ↓
Dependency
   ↓
Root Cause
```

Começa-se pela taxa de falha das [[Request Telemetry|requests]], filtra-se as que falharam, examina-se a [[Exception Telemetry|exceção]] associada e seu contexto ([[Trace Telemetry|traces]] próximos), e verifica-se se há uma [[Dependency Telemetry|dependência]] envolvida na operação que falhou.

## Cenário 2 — API lenta, CPU normal

```
Latency
   ↓
Requests
   ↓
Dependencies
   ↓
Database
   ↓
External API
   ↓
Trace
```

CPU normal não elimina problemas de performance: o tempo pode estar sendo gasto esperando uma dependência externa (banco, API) responder, não processando na própria aplicação. Por isso a investigação segue para [[Dependency Telemetry|dependências]] e sua duração, não para métricas de infraestrutura.

## Cenário 3 — Banco de dados lento

```
API normal
   ↓
Database dependency lenta
   ↓
Request duration elevada
```

Aqui a correlação (ver [[Correlation]]) é o que permite relacionar o sintoma percebido (requisição lenta) à causa específica (uma dependência de banco especificamente lenta), em vez de tratar a lentidão como um problema genérico e indiferenciado da aplicação.

## Cenário 4 — Erro intermitente

99% das requisições funcionam; 1% falha.

Investigar:

- **requests** — isolar apenas as que falharam;
- **exceções** associadas a essas falhas específicas;
- **dependências** envolvidas nessas operações;
- **correlação** — todos os sinais da mesma operação falha;
- **contexto** — o que era diferente nessas requisições (parâmetros, horário, carga);
- **[[Sampling]]** — se a taxa de amostragem estiver descartando justamente os eventos raros de falha, a investigação fica prejudicada; pode ser necessário revisar a configuração de sampling para capturar mais desses eventos intermitentes.

## Relações

- [[Application Insights]]
- [[Azure Monitor Troubleshooting]]
- [[Correlation]]
- [[Sampling]]

## Referências

- Microsoft Learn — "Application Insights overview": https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview
