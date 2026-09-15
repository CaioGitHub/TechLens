---
type: concept
status: learning
confidence: 50
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Resource Manager

## O que é?

Azure Resource Manager (ARM) é o **control plane** do Azure: o serviço responsável por receber pedidos (via portal, CLI, SDK, templates) e criar, atualizar, remover e organizar [[Azure Resource|Resources]] de forma consistente, aplicando autenticação, autorização e políticas antes de qualquer operação.

## Responsabilidades

- Gerenciar o ciclo de vida de recursos dentro de [[Resource Group|Resource Groups]].
- Processar *deployments* (criação/atualização declarativa de recursos via templates — ver [[Infrastructure as Code]]).
- Aplicar [[Azure RBAC]] (quem pode fazer o quê).
- Aplicar Azure Policies (regras organizacionais, ex.: "só permitir recursos em determinadas regiões") — mencionado aqui apenas como contexto, sem aprofundar.

## Control Plane vs. Data Plane

Esta distinção é importante e será usada em etapas futuras (ex.: segurança, identidade):

- **Control Plane**: operações sobre a **existência/configuração** do recurso em si — criar, atualizar, deletar, listar um Storage Account, mudar seu tier. Passa sempre pelo ARM.
- **Data Plane**: operações sobre os **dados dentro** do recurso já existente — ler/escrever um blob dentro do Storage Account, inserir uma linha em um banco de dados. Não necessariamente passa pelo ARM; geralmente usa outro endpoint/API específico do serviço.

```
Control Plane (ARM): "criar esta Storage Account"
Data Plane:          "fazer upload deste arquivo dentro da Storage Account"
```

## Relações

- [[Azure Resource]]
- [[Resource Group]]
- [[Azure RBAC]]
- [[Infrastructure as Code]]

## Referências

- Microsoft Learn — "Azure Resource Manager overview": https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview
