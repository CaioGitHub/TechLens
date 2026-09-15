---
type: technology
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Container Apps

## O que é?

Azure Container Apps é uma plataforma gerenciada para executar containers, sem exigir que o desenvolvedor administre um cluster Kubernetes diretamente — uma camada de abstração entre "só o container" e "Kubernetes completo".

## Conceitos principais

- **Managed Environment**: o agrupamento lógico onde uma ou mais Container Apps rodam, compartilhando rede e configuração.
- **Scaling**: escala automaticamente com base em HTTP, eventos, filas ou métricas customizadas — inclusive escalando a zero (nenhuma instância ativa quando não há tráfego).
- **Revisions**: cada atualização de uma Container App gera uma revisão; é possível manter múltiplas revisões ativas simultaneamente (ex.: para testes A/B ou rollout gradual).
- **Ingress**: exposição HTTP/HTTPS da aplicação, com opção de tráfego interno (privado) ou externo.
- **Jobs**: execução de containers sob demanda ou agendada, para tarefas que não são serviços de longa duração.

## Cenários típicos

Microsserviços, APIs orientadas a eventos, background processing — cenários que se beneficiam de containers e escala orientada a eventos sem a complexidade operacional de administrar Kubernetes.

## Comparação conceitual com App Service

| | App Service | Container Apps |
|---|---|---|
| Unidade de deployment | Artefato de aplicação (ex.: `.jar`) ou container único | Container(s), com suporte nativo a múltiplos containers/revisions |
| Escala a zero | Não (nos tiers tradicionais) | Sim |
| Orientado a eventos | Limitado | Nativo (KEDA por baixo) |
| Uso típico | Aplicação web/API tradicional | Microsserviços, event-driven, jobs |

## Fora de escopo aqui

Esta nota não é um curso de Docker — assume-se que o leitor já sabe o que é um container; o foco é como o Azure executa e escala esses containers.

## Relações

- [[Azure Compute]]
- [[Azure Kubernetes Service]]
- [[Choosing Azure Compute]]

## Referências

- Microsoft Learn — "Azure Container Apps overview": https://learn.microsoft.com/en-us/azure/container-apps/overview
