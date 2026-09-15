---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - application-insights
  - observability
---

# Application Telemetry

## O que é

Application Telemetry é o conjunto de sinais que uma aplicação instrumentada emite sobre sua própria execução — as unidades básicas de dados que o [[Application Insights]] coleta, armazena e correlaciona.

## Tipos principais

```
Application Telemetry
        │
   ┌────┼────┬─────────┐
   ↓    ↓    ↓         ↓
Request Dependency Exception Trace
```

- **[[Request Telemetry]]** — uma requisição recebida pela aplicação (ex.: HTTP).
- **[[Dependency Telemetry]]** — uma chamada que a aplicação faz para fora (banco, API externa, fila).
- **[[Exception Telemetry]]** — uma exceção lançada durante o processamento.
- **[[Trace Telemetry]]** — uma mensagem de log/diagnóstico emitida pela aplicação, com contexto associado.

Cada item de telemetria carrega um **contexto** comum (operação, timestamp, propriedades) que permite relacioná-lo a outros itens da mesma operação — ver [[Correlation]].

## Custom Telemetry

Além dos tipos padrão, é possível emitir telemetria customizada com significado de negócio — por exemplo, marcar explicitamente eventos como "Order Processing" ou "Payment Attempt" concluídos, com propriedades relevantes ao domínio.

Isso tem valor quando o time precisa responder perguntas de negócio (quantos pedidos falharam por motivo X?), não apenas técnicas. Mas custom telemetry deve ser usada com critério: transformar Application Insights em um mecanismo de logging indiscriminado (registrar tudo "só porque pode") aumenta volume, custo (ver [[Sampling]] e [[Azure Monitor Cost Awareness]]) e ruído, sem necessariamente aumentar capacidade de investigação.

## Dados sensíveis

Telemetria de aplicação pode carregar, sem intenção, dados sensíveis: parâmetros de requisição, mensagens de exceção, identificadores, informações de negócio. É responsabilidade de quem instrumenta a aplicação evitar que senhas, tokens, secrets, credenciais e dados pessoais desnecessários acabem em propriedades de telemetria — esses dados, uma vez armazenados em um [[Log Analytics Workspace]], ficam sujeitos às mesmas políticas de acesso e retenção de qualquer outro log. Esta nota não aprofunda compliance, apenas registra a consciência do risco.

## Relações

- [[Application Insights]]
- [[Request Telemetry]]
- [[Dependency Telemetry]]
- [[Exception Telemetry]]
- [[Trace Telemetry]]
- [[Correlation]]
- [[Azure Monitor Logs]]

## Referências

- Microsoft Learn — "Application Insights telemetry data model": https://learn.microsoft.com/en-us/azure/azure-monitor/app/data-model-complete
