---
type: concept
status: learning
confidence: 45
created: 2026-09-09
updated: 2026-09-09
tags:
  - integration
  - architecture
  - observability
---

# End-to-End Mental Model

Modelo conceitual de como uma requisição atravessa uma aplicação Java 21 + Spring Boot construída em [[Hexagonal Architecture|Arquitetura Hexagonal]], executando no [[Azure]], e como essa mesma execução gera telemetria que percorre [[Application Insights]] → [[Azure Monitor]] → [[Log Analytics]] → [[Kusto Query Language|KQL]] até a investigação.

## O modelo

```
                    ┌─────────────────────┐
                    │      Usuário        │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │    Spring Boot      │
                    │      REST API       │   (Adapter — Driving)
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │     Use Case        │
                    │  Application Core   │   (não conhece Azure/telemetria)
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │      Port           │   (contrato/interface)
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │      Adapter        │
                    │    Database/API     │   (Adapter — Driven)
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │       Azure         │   (Compute + Database + Networking)
                    └──────────┬──────────┘
                               ↓
                  ┌─────────────────────────┐
                  │       Telemetria        │   (nasce nos adapters/instrumentação)
                  └───────────┬─────────────┘
                              ↓
              ┌────────────────────────────────┐
              │       Application Insights     │   (coleta específica de aplicação)
              └───────────────┬────────────────┘
                              ↓
                    ┌─────────────────────┐
                    │   Azure Monitor     │   (plataforma unificada)
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │   Log Analytics     │   (armazenamento + consulta)
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │        KQL          │   (linguagem de análise)
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │   Investigação      │   (root cause)
                    └─────────────────────┘
```

## O que é conceitual, não obrigatório

Este diagrama descreve um **fluxo possível**, não um requisito universal. Nem toda aplicação precisa de todos os componentes:

| Componente | Sempre obrigatório? | Depende de |
|---|---|---|
| Spring Boot REST | Não | Aplicação pode ser um worker, job batch, mensageria — sem API HTTP |
| Port/Adapter separados | Não | Aplicações muito pequenas podem não justificar Hexagonal (ver [[Hexagonal Architecture#Quando não usar]]) |
| Application Insights | Não | Pode-se usar apenas [[Azure Monitor Metrics|Metrics]]/[[Resource Logs]] de plataforma sem instrumentação de aplicação |
| Log Analytics/KQL | Não | Times pequenos podem depender só de dashboards/alertas prontos sem consultas ad-hoc |
| Distributed Tracing | Não | Só faz sentido com múltiplos serviços — ver [[Distributed Tracing]] |

A decisão de incluir cada camada depende de escala, criticidade do sistema, maturidade da equipe e orçamento (ver [[Azure Monitor Cost Awareness]]).

## Por que essa ordem importa

- **Domain nunca aparece no diagrama de infraestrutura/observabilidade** — ele fica "dentro" do Use Case/Application Core e é isolado de Azure e telemetria (ver [[Hexagonal Architecture + Observability]]).
- **A telemetria nasce onde a instrumentação acontece** — normalmente nos Adapters (HTTP entrando, banco/API saindo) e na infraestrutura da aplicação (agente/SDK), não no Domain.
- **Cada seta é uma fronteira de responsabilidade diferente**: Port→Adapter é uma fronteira arquitetural; Application Insights→Azure Monitor é uma fronteira de plataforma; Log Analytics→KQL é uma fronteira de linguagem/consulta.

## Relações

- [[Reference Architecture - Java Spring Azure]]
- [[Hexagonal Architecture]]
- [[Application Telemetry]]
- [[Integration]]
