---
type: concept
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure-monitor
---

# Resource Logs

## O que é?

Resource Logs (também chamados de "diagnostic logs") são logs gerados pela **operação interna** de um recurso específico durante seu funcionamento — diferente do [[Azure Activity Log]], que registra apenas operações de gerenciamento sobre o recurso.

## Modelo

```
Resource
   ↓
Resource Logs
```

## Exemplos conceituais

- **Application Gateway**: logs de requisições roteadas, decisões de regra.
- **Storage**: logs de operações de leitura/escrita em blobs.
- **Database**: logs de queries, eventos de conexão.
- **Key Vault**: logs de acesso a secrets/chaves.

## Não generalizar

Os tipos específicos de Resource Logs disponíveis (categorias) dependem inteiramente do recurso — cada serviço Azure define suas próprias categorias de log, e nem todo recurso oferece o mesmo nível de detalhe.

## Coleta não é automática

Diferente do Activity Log, Resource Logs geralmente **não** são coletados automaticamente — é necessário habilitá-los explicitamente através de [[Azure Diagnostic Settings]], escolhendo quais categorias enviar e para onde.

## Relações

- [[Azure Activity Log]]
- [[Application Logs]]
- [[Azure Diagnostic Settings]]

## Referências

- Microsoft Learn — "Resource logs": https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/resource-logs
