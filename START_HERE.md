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
ROOT_CAUSE_ANALYSIS_COMPLETE

Stage 31.7.2
    ↓
SEMANTIC_RELEVANCE_ARCHITECTURE_IMPLEMENTED

Stage 31.7.3
    ↓
POST_DECOUPLING_BLIND_REVALIDATION_BLOCKED

Stage 31.7.4
    ↓
ROOT_CAUSE_ANALYSIS_COMPLETE

Stage 31.7.5
    ↓
SEMANTIC_INTENT_GENERALIZATION_IMPLEMENTATION_COMPLETE_WITH_WARNINGS

Stage 31.7.6
    ↓
POST_GENERALIZATION_BLIND_REVALIDATION_BLOCKED

Stage 31.7.7
    ↓
ROOT_CAUSE_ANALYSIS_AND_ARCHITECTURE_REDESIGN_COMPLETE

Stage 31.7.8
    ↓
CONTROLLED_IMPLEMENTATION_COMPLETE_WITH_WARNINGS

Stage 31.7.9
    ↓
POST_OPEN_DOMAIN_BLIND_REVALIDATION_BLOCKED

Stage 31.7.10
    ↓
ROOT_CAUSE_ANALYSIS_AND_DEMAND_SATISFACTION_REDESIGN_COMPLETE

Stage 31.7.11
    ↓
CONTROLLED_DEMAND_PROPOSITION_IMPLEMENTATION_COMPLETE

Stage 31.7.12
    ↓
INDEPENDENT_CONTRACT_AUDIT_AND_BLIND_VALIDATION_DESIGN_COMPLETE

Stage 31.7.13
    ↓
BLIND_SEMANTIC_REVALIDATION_BLOCKED

Stage 31.7.14
    ↓
INDEPENDENT_BLIND_VALIDATION_RCA_COMPLETE

Stage 31.7.15
    ↓
CONTROLLED_CORRECTION_PLAN_COMPLETE

Stage 31.7.16
    ↓
CONTROLLED_IMPLEMENTATION_COMPLETE_PENDING_BLIND_VALIDATION

Stage 31.7.17
    ↓
BLIND_SEMANTIC_REVALIDATION_BLOCKED

Stage 31.7.18
    ↓
RCA_COMPLETE_CORRECTION_PLAN_READY

Stage 31.7.19
    ↓
CORRECTION_PLAN_READY_FOR_CONTROLLED_IMPLEMENTATION

Stage 31.7.20
    ↓
IMPLEMENTATION_COMPLETE_PENDING_INDEPENDENT_BLIND_VALIDATION

Stage 31.7.21
    ↓
BLIND_SEMANTIC_REVALIDATION_BLOCKED

Stage 31.7.22
    ↓
NEXT STAGE (Root Cause Analysis & Semantic Precision Remediation Architecture — Cycle 4)
```

O Stage 31.7.21 concluiu a revalidação semântica cega e independente do runtime corrigido no Stage 31.7.20 (`reference_runtime/runtime.py`, SHA-256 congelado verificado: `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`). A validação foi conduzida sobre 250 casos de teste inéditos com zero sobreposição com benchmarks históricos, sem alterações de código no runtime e sem relaxamento de testes. A regressão canônica obteve 100% de conformidade (1.038 testes unitários e 15 testes do Reference Harness aprovados). Contudo, 6 dos 7 critérios quantitativos de aceite falharam: Concordância Exata de 68,00% (alvo $\ge 75\%$), Recall de DIRECT de 81,54% (alvo $\ge 85\%$), Precisão de DIRECT de 53,00% (alvo $\ge 70\%$), Falsos DIRECT entre divergências de 58,75% (alvo $\le 10\%$), Recall de PARTIAL de 37,78% (alvo $\ge 60\%$) e Invariância de Representação de 68,75% (alvo $\ge 80\%$). A salvaguarda de evitação e polaridade (Grupo I) obteve 92,86% de acurácia, confirmando o avanço na mitigação de antítese, mas a promoção indevida de respostas parciais (`PARTIAL` -> `DIRECT`: 25 casos) e afirmações históricas/declarações de experiência (`RELATED` -> `DIRECT`: 8 casos) revelou limites das regras heurísticas em orações simples multi-aspecto. Em respeito estrito às regras metodológicas, o gate emitido é `BLIND_SEMANTIC_REVALIDATION_BLOCKED`. A próxima etapa é o **Stage 31.7.22 — Root Cause Analysis & Semantic Precision Remediation Architecture (Cycle 4)**.

## Regra fundamental

Não modificar o projeto apenas para fazer testes passarem.

Não criar regras específicas para casos individuais.

Não apagar histórico.

Não utilizar avaliação humana como alvo de score.

Não pular stages.

Não interpretar `BLOCKED` como aprovação.

## Princípio

> Não estamos construindo um sistema que parece inteligente. Estamos construindo um sistema cuja avaliação pode ser investigada, reproduzida, contestada e corrigida.
