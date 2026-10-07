# START HERE

Este projeto possui histórico e metodologia já estabelecidos.

## Antes de fazer qualquer alteração

Leia obrigatoriamente:

1. `AGENTS.md`
2. `SECOND_BRAIN.md`
3. `GEMINI_GUARDRAILS.md`
4. `GEMINI_HANDOFF.md`

Depois identifique:

```text
Qual é o stage atual?
Qual foi o último gate?
Existe algum BLOCKED?
Quais warnings estão abertos?
Quais artefatos são históricos?
Quais testes devem continuar passando?
```

## Estado atual

O projeto está na sequência:

```text
Stage 31
    ↓
HUMAN_VS_SYSTEM_BLOCKED

Stage 31.1
    ↓
ROOT CAUSE IDENTIFIED

Stage 31.2
    ↓
CONTROLLED CORRECTION COMPLETE_WITH_WARNINGS

Stage 31.3
    ↓
POST_CORRECTION_BLIND_VALIDATION_BLOCKED

Stage 31.4
    ↓
SEMANTIC_RELEVANCE_INVARIANCE_REMEDIATION_COMPLETE_WITH_WARNINGS

Stage 31.4.1
    ↓
SEMANTIC_RELEVANCE_MODEL_REDESIGN_COMPLETE

Stage 31.4.2
    ↓
SEMANTIC_RELEVANCE_MODEL_IMPLEMENTATION_COMPLETE

Stage 31.5
    ↓
POST_REMEDIATION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED

Stage 31.6
    ↓
CONTROLLED_CORRECTION_COMPLETE

Stage 31.7
    ↓
POST_CORRECTION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED

Stage 31.7.1
    ↓
NEXT STAGE (Root Cause Analysis & Architectural Decoupling of Functional Catalog)
```

O Stage 31.7 executou a revalidação cega e independente pós-Stage 31.6. A calibração contra a referência humana do Candidato-Piloto-05 manteve-se estável com MAE 0.64 (0.6364), 4 concordâncias exatas e 716/716 testes de regressão global aprovados. Entretanto, a auditoria estrutural profunda da suíte adversarial de 65 testes (51 PASS, 14 FAIL) revelou que `_FUNCTIONAL_CAPABILITIES` atua como um catálogo obrigatório que intercepta e rejeita indevidamente tecnologias desconhecidas e conceitos em domínio aberto (via `alien_defines` e colisões de monopalavras polissêmicas como `"transação"` e `"telemetria"`). O gate foi corretamente declarado `POST_CORRECTION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED`. O próximo passo é o Stage 31.7.1.

## Regra fundamental

Não modificar o projeto apenas para fazer testes passarem.

Não criar regras específicas para casos individuais.

Não apagar histórico.

Não utilizar avaliação humana como alvo de score.

Não pular stages.

Não interpretar `BLOCKED` como aprovação.

## Princípio

> Não estamos construindo um sistema que parece inteligente. Estamos construindo um sistema cuja avaliação pode ser investigada, reproduzida, contestada e corrigida.
