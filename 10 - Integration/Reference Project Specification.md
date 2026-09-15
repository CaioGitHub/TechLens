---
type: project
status: inbox
confidence: 30
created: 2026-09-09
updated: 2026-09-09
tags:
  - project
  - integration
  - specification
---

# Reference Project Specification

Especificação conceitual de um projeto de referência para praticar toda a stack integrada. **Não implementado nesta etapa** — este documento é a especificação para estudo/prática futura.

## Proposta

Uma **API de pedidos** (Orders API) construída em Java 21 + Spring Boot, usando [[Hexagonal Architecture|Arquitetura Hexagonal]], executada no [[Azure]] e observada via [[Application Insights]]/[[Azure Monitor]]/[[Log Analytics]]/[[Kusto Query Language|KQL]].

## Estrutura conceitual (aplicação)

```
REST API
   ↓
Use Cases (criar pedido, consultar pedido, cancelar pedido)
   ↓
Ports (OrderRepositoryPort, PaymentPort)
   ↓
Adapters (JPA/Azure SQL adapter, HTTP client para serviço de pagamento externo)
   ↓
Database (Azure SQL)
```

## Estrutura conceitual (observabilidade)

```
Application
   ↓
Application Insights (SDK/agente)
   ↓
Azure Monitor
   ↓
Log Analytics
   ↓
KQL
```

## Cenários a simular

O projeto deve permitir provocar deliberadamente, para praticar o [[End-to-End Troubleshooting Playbook]]:

| Cenário | Como simular (conceitual) |
|---|---|
| HTTP 500 | Forçar exceção não tratada em um caminho específico do Use Case |
| Lentidão | Introduzir `sleep`/processamento artificial no Adapter de banco |
| Timeout | Configurar timeout curto no client HTTP do serviço de pagamento e simular resposta lenta |
| Falha de dependency | Derrubar/simular indisponibilidade do serviço de pagamento externo |
| Indisponibilidade | Bloquear a porta/endpoint via configuração de rede (NSG) |
| Erro de configuração | Omitir/errar uma variável de configuração (connection string, endpoint) |
| Problema de infraestrutura | Reduzir artificialmente o SKU/capacidade do recurso Azure para gerar throttling |

## Escopo desta especificação

- Definir os Ports e Use Cases necessários (não o código).
- Definir onde a instrumentação de telemetria entra (Adapters, nunca Use Cases/Domain — ver [[Hexagonal Architecture + Observability]]).
- Definir os recursos Azure mínimos: compute (ver [[Choosing Azure Compute]]), banco (ver [[Azure Databases]]), Application Insights, Log Analytics Workspace.
- Servir de base para exercícios práticos que conectem [[KQL Exercises]] a uma aplicação real, quando o projeto for efetivamente implementado.

## Fora de escopo (nesta etapa)

Implementação de código, pipeline de CI/CD, Infrastructure as Code, containers/Kubernetes — ver [[Integration Gaps]] para esses itens classificados como "Future Topics".

## Relações

- [[Integration]]
- [[Reference Architecture - Java Spring Azure]]
- [[End-to-End Troubleshooting Playbook]]
