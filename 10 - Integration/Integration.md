---
type: reference
status: learning
confidence: 45
created: 2026-09-09
updated: 2026-09-09
tags:
  - moc
  - integration
---

# Integration

MOC (Map of Content) — porta de entrada para a **visão end-to-end** do Second Brain: como Java 21, Spring Boot, Arquitetura Hexagonal, Azure e Observabilidade se conectam em um único sistema de conhecimento, do código à investigação de um incidente em produção.

Esta camada **não duplica** o conteúdo já construído em [[Java 21]], [[Spring Boot]], [[Hexagonal Architecture]], [[Azure]], [[Azure Monitor]], [[Application Insights]] e [[Log Analytics]] — ela **conecta** esse conhecimento e explica como as partes se relacionam, quando cada parte entra em ação, e como uma decisão em uma camada impacta outra.

## Visão Geral

```
Java 21 → Spring Boot → Hexagonal Architecture → Application
   → Azure → Azure Monitor → Application Insights
   → Azure Monitor Logs → Log Analytics → KQL
   → Observability → Troubleshooting
```

A pergunta que esta camada responde: **como uma aplicação Java 21 com Spring Boot, estruturada segundo Arquitetura Hexagonal, pode ser executada no Azure, observada através do Azure Monitor/Application Insights e investigada utilizando Log Analytics e KQL?**

Ver o modelo mental completo em [[End-to-End Mental Model]].

## Stack Integrada

| Camada | Papel | Nota principal |
|---|---|---|
| Linguagem/Runtime | Java 21 (Virtual Threads, JVM) | [[Java 21]] |
| Framework | Spring Boot (REST, Actuator) | [[Spring Boot]] |
| Arquitetura | Hexagonal (Domain, Ports, Adapters) | [[Hexagonal Architecture]] |
| Infraestrutura | Azure (Compute, Networking, Database, Identity) | [[Azure]] |
| Observabilidade — plataforma | Azure Monitor (Metrics, Logs, Alerts) | [[Azure Monitor]] |
| Observabilidade — aplicação | Application Insights (Requests, Dependencies, Exceptions, Traces) | [[Application Insights]] |
| Análise | Log Analytics + KQL | [[Log Analytics]] |
| Investigação | Troubleshooting sistemático | [[End-to-End Troubleshooting Playbook]] |

## Arquitetura

- [[Reference Architecture - Java Spring Azure]] — arquitetura de referência completa.
- [[Hexagonal Architecture + Azure]], [[Hexagonal Architecture + Observability]], [[Hexagonal Architecture + Application Insights]] — fronteiras entre Domain, Application, Infrastructure e Observability.

## Fluxo da Aplicação

```
HTTP Request
      ↓
Controller (Adapter)
      ↓
Use Case (Application Core)
      ↓
Port
      ↓
Adapter (Database / External API)
```

Ver o detalhamento completo com observabilidade acoplada em [[Reference Architecture - Java Spring Azure]].

## Azure

Azure não é apenas "onde o servidor fica" — é a combinação de compute, networking, identity, database e observabilidade que sustenta a aplicação. Ver [[Azure]] e a seção "Infraestrutura" em [[Reference Architecture - Java Spring Azure]].

## Observabilidade

Três conceitos que não são sinônimos:

- **[[Application Insights]] ≠ [[Azure Monitor]]** — Application Insights é a especialização em telemetria de aplicação; Azure Monitor é a plataforma completa.
- **[[Azure Monitor]] ≠ [[Log Analytics]]** — Azure Monitor coleta e correlaciona; Log Analytics é a capacidade de consulta sobre os dados armazenados.
- **[[Log Analytics]] ≠ [[Kusto Query Language|KQL]]** — Log Analytics é o ambiente; KQL é a linguagem usada nele.

E, dentro da telemetria: **[[Azure Monitor Metrics|Metrics]] ≠ [[Azure Monitor Logs|Logs]] ≠ [[Azure Monitor Traces|Traces]]** — ver [[Metrics Logs Traces]].

**Telemetry ≠ Root Cause**: dados de telemetria são evidência, não conclusão — ver [[End-to-End Troubleshooting Playbook]].

## Troubleshooting

- [[End-to-End Troubleshooting Playbook]] — processo sistemático + 7 cenários end-to-end + matriz de investigação + árvore de decisão.

## Cenários End-to-End

Ver [[End-to-End Troubleshooting Playbook]]: HTTP 500, latência, dependência lenta, banco de dados, disponibilidade, problema de infraestrutura, incidente distribuído.

## Decisões Arquiteturais

- Observabilidade é transversal — nunca uma dependência do [[Domain]] (ver [[Hexagonal Architecture + Observability]]).
- KQL e ferramentas de consulta operam **fora** da aplicação, sobre dados já exportados — não são dependências arquiteturais (ver [[Java Spring Boot Log Analytics]]).
- Mais telemetria não é sempre melhor — existe trade-off entre volume, custo e valor de investigação (ver [[Sampling]], [[Azure Monitor Cost Awareness]]).

## Segurança (visão integrada)

```
Application
   ↓
Identity (Managed Identity)
   ↓
Secrets (Key Vault)
   ↓
Permissions (RBAC)
   ↓
Azure Resources
   ↓
Telemetry
```

A aplicação autentica-se via [[Managed Identity]] (não credenciais fixas), acessa segredos via [[Azure Key Vault]], e o acesso a recursos — incluindo dados de telemetria em um [[Log Analytics Workspace]] — é controlado por [[Azure RBAC]] seguindo o princípio de menor privilégio. Telemetria pode carregar dados sensíveis sem intenção — ver [[Application Telemetry#Dados sensíveis|dados sensíveis em telemetria]].

## Custo (visão integrada)

```
Application
   ↓
Telemetry Volume
   ↓
Logs
   ↓
Retention
   ↓
Queries
   ↓
Cost
```

Mais telemetria não significa necessariamente melhor observabilidade — volume, retenção e frequência de consulta têm custo (ver [[Azure Monitor Cost Awareness]] e [[Sampling]]).

## Dashboards, Alerts e Troubleshooting

| Ferramenta | Papel |
|---|---|
| [[Dashboards and Workbooks\|Dashboard]] | visualizar |
| [[Azure Monitor Alerts\|Alert]] | detectar / notificar |
| [[Azure Monitor Logs\|Logs]] | investigar |
| [[Azure Monitor Traces\|Traces]] | correlacionar |
| [[Kusto Query Language\|KQL]] | analisar |
| [[End-to-End Troubleshooting Playbook\|Troubleshooting]] | encontrar causa raiz |

Um dashboard não substitui um alerta, e um alerta não substitui uma investigação.

## Relações

- [[Java 21]]
- [[Spring Boot]]
- [[Hexagonal Architecture]]
- [[Azure]]
- [[Azure Monitor]]
- [[Application Insights]]
- [[Log Analytics]]
- [[Observability]]
- [[Reference Architecture - Java Spring Azure]]
- [[End-to-End Troubleshooting Playbook]]

## Learning Path

- [[Integration Learning Path]]

## Outras notas desta camada

- [[End-to-End Mental Model]]
- [[Reference Project Specification]]
- [[Competency Matrix]]
- [[Integration Gaps]]
