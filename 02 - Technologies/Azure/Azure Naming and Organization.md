---
type: reference
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Azure Naming and Organization

## Objetivo

Boas práticas conceituais — não uma convenção rígida universal. Cada organização pode (e deve) adaptar às próprias necessidades.

## Naming

Um padrão de nomenclatura consistente (ex.: incluir tipo de recurso, aplicação, ambiente, região no nome) facilita identificar rapidamente o propósito de um recurso ao navegar pelo portal ou por logs, sem precisar abrir cada recurso individualmente.

## Tagging

Tags (metadados chave-valor associados a um recurso) permitem categorizar recursos para fins de custo, ambiente, responsável ou aplicação — úteis para relatórios de custo agregados por tag, independentemente de como os recursos estão organizados em Resource Groups.

## Resource Organization

Agrupar por [[Resource Group]] tipicamente por aplicação + ambiente (ex.: um Resource Group por combinação de app e ambiente) é uma convenção comum, mas não universal — outras organizações agrupam por time, por camada (compute/dados/rede), ou de outras formas conforme a necessidade de gerenciamento de ciclo de vida.

## Environments

Separar recursos de development, staging e production (tipicamente em Resource Groups ou até Subscriptions diferentes) evita que uma mudança em um ambiente afete outro acidentalmente, e permite aplicar permissões diferentes por ambiente.

## Relações

- [[Resource Group]]
- [[Azure Subscription]]

## Referências

- Microsoft Learn — "Recommended naming and tagging conventions": https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/naming-and-tagging
