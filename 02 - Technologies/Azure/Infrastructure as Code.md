---
type: concept
status: learning
confidence: 40
created: 2026-09-08
updated: 2026-09-08
tags:
  - azure
---

# Infrastructure as Code

## O que é?

Definir e provisionar infraestrutura (Resource Groups, App Service, VNets, bancos de dados) através de arquivos declarativos versionados, em vez de criar recursos manualmente pelo portal.

## Manual Infrastructure vs. Infrastructure as Code (IaC)

| | Manual | IaC |
|---|---|---|
| Repetibilidade | Baixa (depende de quem clicou onde) | Alta (o mesmo arquivo gera o mesmo resultado) |
| Auditabilidade | Difícil (histórico de cliques não é rastreado) | Alta (versionado em Git, com histórico de mudanças) |
| Consistência entre ambientes | Difícil de garantir | O mesmo template pode gerar dev/staging/prod consistentes |
| Velocidade inicial | Mais rápida para algo pontual | Exige investimento inicial de escrever o template |

## Ferramentas (visão breve)

- **ARM Templates**: formato declarativo nativo do Azure (JSON) processado diretamente pelo [[Azure Resource Manager]].
- **Bicep**: linguagem declarativa mais legível que compila para ARM Templates — feita pela própria Microsoft como uma camada de abstração sobre ARM.
- **Terraform**: ferramenta de IaC multi-cloud (não exclusiva da Microsoft), com seu próprio provider para Azure.

## Escopo desta nota

Esta base não transforma nenhuma dessas ferramentas em uma disciplina própria — apenas registra a existência do conceito e das opções mais comuns, para que a decisão de aprofundar uma delas seja tomada com contexto, quando necessário.

## Relações

- [[Azure Resource Manager]]
- [[Azure Deployment]]

## Referências

- Microsoft Learn — "What is infrastructure as code (IaC)?": https://learn.microsoft.com/en-us/devops/deliver/what-is-infrastructure-as-code
