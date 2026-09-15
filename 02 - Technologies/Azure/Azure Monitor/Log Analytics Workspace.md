---
type: concept
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Log Analytics Workspace

## O que é?

Um Log Analytics Workspace é o ambiente onde dados de log coletados pelo Azure Monitor ficam armazenados e disponíveis para consulta e análise.

## Modelo

```
Azure Resources
      ↓
Diagnostic / Telemetry Data
      ↓
Log Analytics Workspace
      ↓
Queries
```

## Finalidade

Recursos Azure (e aplicações, via Application Insights) enviam seus dados de log/telemetria para um Workspace — que funciona como o repositório central onde essas informações podem ser consultadas, correlacionadas e analisadas, tipicamente através de KQL (Kusto Query Language).

## Relação com Azure Monitor

```
Azure Monitor
      ↓
Azure Monitor Logs
      ↓
Log Analytics Workspace
```

O Log Analytics Workspace é o destino de armazenamento para [[Azure Monitor Logs|logs]] coletados pelo Azure Monitor — não é um serviço separado e desconectado, mas parte da mesma plataforma de observabilidade.

## Escopo desta nota

Esta nota cobre o conceito e a operação de um Workspace. A linguagem de consulta (KQL) é aprofundada em [[Kusto Query Language]].

## Organização dos dados

Dentro de um Workspace, os dados são organizados em **tabelas** (ver [[Application Insights Tables]] para o caso específico de telemetria de aplicação) — cada tabela tem seu próprio schema de colunas, mas todas compartilham o mesmo ambiente de consulta via KQL.

## Retenção

Dados em um Workspace são mantidos por um período de retenção configurável — após esse período, os dados deixam de estar disponíveis para consulta padrão (podendo, dependendo da configuração, ser arquivados para acesso menos frequente e mais barato). Retenção mais longa permite investigar incidentes antigos, mas aumenta custo de armazenamento — parte do trade-off já discutido em [[Azure Monitor Cost Awareness]].

## Permissões e acesso

O acesso a um Workspace (quem pode consultar quais dados) é controlado através de mecanismos de controle de acesso do Azure (ver [[Azure RBAC]]) — nem todo usuário com acesso à assinatura necessariamente tem acesso de leitura aos logs de um Workspace específico. Isso é relevante porque logs podem conter dados sensíveis (ver [[Application Telemetry#Dados sensíveis|dados sensíveis em telemetria]]).

## Custo

O custo de um Workspace é influenciado por volume de ingestão, retenção configurada e, dependendo do modelo de cobrança, volume de consultas — ver o detalhamento em [[Azure Monitor Cost Awareness]].

## Relações

- [[Azure Monitor Logs]]
- [[Azure Diagnostic Settings]]
- [[Azure Monitor]]
- [[Application Insights Tables]]
- [[Kusto Query Language]]
- [[Azure Monitor Cost Awareness]]

## Referências

- Microsoft Learn — "Log Analytics workspace overview": https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-workspace-overview
