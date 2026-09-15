---
type: architecture
status: learning
confidence: 45
created: 2026-09-09
updated: 2026-09-09
tags:
  - architecture
  - integration
  - azure
  - java
---

# Reference Architecture - Java Spring Azure

Arquitetura de referência conceitual para: **Java 21 + Spring Boot + Arquitetura Hexagonal + Azure + Observabilidade**. Não é uma implementação — é a especificação que conecta o conhecimento já existente no Second Brain. Use como mapa antes de projetar um sistema real; ver a especificação de um projeto concreto em [[Reference Project Specification]].

## Application

- **Java 21** — runtime, [[Virtual Threads]] quando concorrência de I/O é relevante (ver caveat de observabilidade em [[Java Spring Boot Application Insights#Virtual Threads]]).
- **Spring Boot** — [[Spring Boot]], expõe REST via Controllers (Adapter — Driving).
- **REST** — camada HTTP, converte requisição em chamada ao Use Case.
- **Application Core**
  - **Use Cases** — orquestram a regra de negócio (ver [[Use Case]]).
  - **Ports** — contratos entre o Core e o mundo externo (ver [[Ports]]).
- **Adapters** — implementam Ports: REST controllers (driving), repositórios/clientes HTTP (driven) (ver [[Adapters]]).

Ver [[Spring Boot + Hexagonal Architecture]] para a conexão entre framework e arquitetura.

## Infrastructure / Azure

| Preocupação | Componente Azure | Nota |
|---|---|---|
| Compute | App Service / Container Apps / AKS | [[Azure Compute]], [[Choosing Azure Compute]] |
| Networking | Virtual Network, NSG, DNS | [[Azure Networking]] |
| Database | Azure SQL, Cosmos DB, banco gerenciado | [[Azure Databases]] |
| Identity | Managed Identity, Microsoft Entra ID | [[Managed Identity]], [[Microsoft Entra ID]] |
| Configuration | App Configuration / variáveis de ambiente do compute escolhido | [[Azure App Service]] |
| Secrets | Key Vault | [[Azure Key Vault]] |
| Scaling | Autoscale, deployment slots | [[Azure Scalability]], [[Deployment Slots]] |

Ver a conexão completa em [[Java Spring Boot Application on Azure]] e [[Hexagonal Architecture + Azure]].

## Observability

| Preocupação | Ferramenta | Nota |
|---|---|---|
| Plataforma | Azure Monitor | [[Azure Monitor]] |
| Aplicação | Application Insights | [[Application Insights]] |
| Metrics | Azure Monitor Metrics | [[Azure Monitor Metrics]] |
| Logs | Azure Monitor Logs | [[Azure Monitor Logs]] |
| Traces | Application Insights Traces / Distributed Tracing | [[Azure Monitor Traces]], [[Distributed Tracing]] |
| Dependencies | Dependency Telemetry | [[Dependency Telemetry]] |
| Exceptions | Exception Telemetry | [[Exception Telemetry]] |
| Availability | Availability Tests | [[Availability Monitoring]] |
| Alerts | Alert Rules / Action Groups | [[Alert Rules]], [[Azure Monitor Action Groups]] |

## Investigation

| Preocupação | Ferramenta | Nota |
|---|---|---|
| Armazenamento consultável | Azure Monitor Logs | [[Azure Monitor Logs]] |
| Workspace | Log Analytics Workspace | [[Log Analytics Workspace]] |
| Linguagem | KQL | [[Kusto Query Language]] |
| Correlação | OperationId/Correlation | [[Correlation]] |
| Distributed Tracing | Application Map | [[Application Map]] |

## Camadas e fronteiras

```
Domain        → regra de negócio pura, não conhece Azure/Spring/telemetria
Application   → orquestra Use Cases via Ports, não conhece implementações concretas
Infrastructure→ implementa Ports (Adapters): REST, banco, mensageria, cloud
Azure         → hospeda a Infrastructure (compute, rede, dados, identidade)
Observability → transversal, instrumenta Adapters/Infrastructure, nunca o Domain
Operations    → opera o sistema: dashboards, alertas, troubleshooting, deploy
```

### Domain

Responsabilidade pelo negócio. **Não deve conhecer**: Azure Monitor, Application Insights, Log Analytics, KQL, Azure SDK, detalhes de infraestrutura. Ver [[Domain]].

### Application

Coordena casos de uso, depende de [[Ports]], não depende diretamente de implementações de infraestrutura.

### Adapters

Conectam o Core ao mundo externo: REST, Database, Messaging, External APIs, Cloud services. É aqui que a instrumentação de telemetria tipicamente acontece. Ver [[Adapters]].

### Infrastructure

Implementa os recursos técnicos necessários (SDKs de banco, HTTP clients, configuração de cloud).

### Observability

Preocupação transversal — nunca inserida artificialmente dentro do Domain apenas para "ter logs". Ver [[Hexagonal Architecture + Observability]].

## Segurança (integrada)

```
Application → Identity → Secrets → Permissions → Azure Resources → Telemetry
```

[[Managed Identity]] elimina credenciais fixas; [[Azure Key Vault]] guarda segredos; [[Azure RBAC]] aplica menor privilégio, inclusive sobre o [[Log Analytics Workspace]] onde a telemetria fica armazenada. Detalhamento aprofundado de segurança é [[Azure Security Fundamentals]] — fora do escopo desta etapa (ver [[Integration Gaps]]).

## Custo (integrado)

```
Application → Telemetry Volume → Logs → Retention → Queries → Cost
```

Ver [[Azure Monitor Cost Awareness]] e [[Sampling]] — mais telemetria não é sinônimo de melhor observabilidade.

## Relações

- [[Integration]]
- [[End-to-End Mental Model]]
- [[Hexagonal Architecture]]
- [[Azure]]
- [[Azure Monitor]]
- [[Application Insights]]
- [[Log Analytics]]
