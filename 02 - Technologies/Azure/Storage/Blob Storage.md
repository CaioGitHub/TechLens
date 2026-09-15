---
type: concept
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Blob Storage

## O que é?

Blob Storage é o serviço de armazenamento de objetos do Azure — projetado para grandes volumes de dados não estruturados (arquivos), acessíveis via HTTP/HTTPS.

## Modelo

```
Application
    ↓
Blob Storage
    ↓
Objects (blobs), organizados em containers
```

Um **container** (dentro da Storage Account) agrupa blobs, de forma análoga a uma pasta de topo — cada blob é identificado por um nome dentro do container.

## Access Tiers

- **Hot**: acesso frequente, custo de armazenamento mais alto, custo de acesso mais baixo.
- **Cool**: acesso pouco frequente, custo de armazenamento menor, custo de acesso maior.
- **Archive**: dados raramente acessados (ex.: retenção legal), custo de armazenamento mínimo, latência de acesso alta (requer "rehydration" antes de ler).

## Lifecycle Management

É possível configurar regras automáticas para mover blobs entre tiers (ou excluí-los) com base em idade/último acesso — reduzindo custo sem intervenção manual.

## Acesso

- **URLs**: cada blob possui uma URL própria.
- **Acesso privado vs. público**: por padrão, o acesso deve ser privado, controlado via chaves de acesso, SAS tokens ou [[Managed Identity]] com RBAC — evitar containers publicamente acessíveis sem necessidade explícita.

## Casos de uso típicos

Imagens, documentos, arquivos de upload de usuários, backups, logs exportados.

## Relações

- [[Azure Storage]]
- [[Managed Identity]]
- [[Public vs Private Networking]]

## Referências

- Microsoft Learn — "Introduction to Blob Storage": https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction
