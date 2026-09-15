---
type: technology
status: learning
confidence: 45
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
  - security
---

# Microsoft Entra ID

## O que é?

Microsoft Entra ID (anteriormente conhecido como Azure Active Directory) é o identity provider do Azure: o serviço responsável por autenticar usuários e identidades de aplicações/serviços.

## O que ele gerencia

- **Users**: identidades humanas (funcionários, colaboradores).
- **Applications**: identidades registradas que representam uma aplicação (para que ela possa se autenticar e ser autorizada a chamar APIs ou acessar recursos).
- **Service identities**: identidades usadas por serviços/processos em vez de pessoas — ver [[Managed Identity]].

## Papel na autenticação

Quando uma aplicação ou usuário precisa provar "quem é" (ver [[Authentication vs Authorization]]), o Microsoft Entra ID é o serviço que emite e valida essa prova (tipicamente tokens).

## Escopo desta nota

Esta base não é um curso completo de Microsoft Entra ID — cobre apenas o suficiente para entender seu papel como identity provider central do Azure, base para [[Managed Identity]] e [[Azure RBAC]].

## Relações

- [[Authentication vs Authorization]]
- [[Managed Identity]]
- [[Azure RBAC]]

## Referências

- Microsoft Learn — "What is Microsoft Entra ID?": https://learn.microsoft.com/en-us/entra/fundamentals/whatis
