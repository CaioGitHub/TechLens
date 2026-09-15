---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Resource Monitoring

## O que é?

Monitoramento de recursos é a coleta de sinais (principalmente métricas de plataforma, ver [[Azure Monitor Metrics]]) sobre a saúde e desempenho de recursos Azure — coletados automaticamente pelo Azure Monitor, sem exigir instrumentação do código da aplicação.

## Exemplos de recursos e sinais

| Recurso | Sinais típicos |
|---|---|
| [[Azure App Service]] | CPU, Memory, Requests, Response Time, HTTP errors |
| [[Virtual Machines]] | CPU, Disk I/O, Network In/Out |
| [[Azure Databases\|Database]] | Connections, DTU/CPU usage, Storage usage, Query duration |
| [[Azure Storage]] | Availability, Latency, Transactions |
| [[Azure Networking\|Network]] | Throughput, Latency, Connection count |
| [[Azure Container Apps]] | CPU, Memory, Replica count, Requests |

## Não generalizar

As métricas específicas disponíveis dependem inteiramente do recurso (e às vezes do SKU/tier escolhido) — é preciso consultar a documentação de cada serviço para saber exatamente o que pode ser observado.

## Limitação importante

Monitorar apenas recursos de infraestrutura não é suficiente para compreender completamente uma aplicação — ver [[Application Monitoring]] para o que falta.

## Relações

- [[Azure Monitor Metrics]]
- [[Resource Logs]]
- [[Application Monitoring]]

## Referências

- Microsoft Learn — "Monitoring Azure resources with Azure Monitor": https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/monitor-azure-resource
