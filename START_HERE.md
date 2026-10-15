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
RCA_COMPLETE_ARCHITECTURE_PENDING_REVIEW

Stage 31.7.23
    ↓
CORRECTION_PLAN_READY_FOR_CONTROLLED_IMPLEMENTATION

Stage 31.7.24
    ↓
IMPLEMENTATION_COMPLETE_PENDING_INDEPENDENT_BLIND_VALIDATION

Stage 31.7.25
    ↓
BLIND_SEMANTIC_REVALIDATION_BLOCKED

Stage 31.7.26
    ↓
RCA_COMPLETE_ARCHITECTURE_APPROVED_FOR_IMPLEMENTATION

Stage 31.7.27
    ↓
IMPLEMENTATION_COMPLETE_PENDING_INDEPENDENT_BLIND_VALIDATION

Stage 31.7.28
    ↓
NEXT STAGE (Independent Blind Semantic Revalidation — Cycle 5)
```

O Stage 31.7.27 concluiu a implementação controlada dos 5 incrementos da arquitetura do Ciclo 5 em `reference_runtime/runtime.py`: `SemanticDomainDisjunctionEngine`, `DemandPropositionNexusBipartiteMatcher`, `PropositionDiscourseFilter`, `StrictOntologyRelevanceAggregator` e `OpenDomainPropositionEngine`. O hash criptográfico final do runtime é `3FD3F80D9BB8A13CCC3A2791759D08F2EED25271913B56F064710DB94B2BC229`. Todos os 20 testes de contrato obrigatórios foram aprovados com 100% de sucesso (`tests/test_stage_31_7_27_contract_tests.py`). A suíte canônica de 1.047 testes passou integralmente com zero regressões (1.046 OK, 1 skipped, 0 falhas, 0 erros), assim como o Reference Harness do Stage 26 (15/15 OK). Na verificação puramente diagnóstica dos 250 casos históricos, a acurácia subiu de 60.80% para 89.20% (+71 casos) e os falsos DIRECTs despencaram de 70 para 6 (redução de 91.43%). O gate emitido é `IMPLEMENTATION_COMPLETE_PENDING_INDEPENDENT_BLIND_VALIDATION`. A próxima etapa autorizada é exclusivamente o **Stage 31.7.28 — Independent Blind Semantic Revalidation (Cycle 5)**.

## Regra fundamental

Não modificar o projeto apenas para fazer testes passarem.

Não criar regras específicas para casos individuais.

Não apagar histórico.

Não utilizar avaliação humana como alvo de score.

Não pular stages.

Não interpretar `BLOCKED` como aprovação.

## Princípio

> Não estamos construindo um sistema que parece inteligente. Estamos construindo um sistema cuja avaliação pode ser investigada, reproduzida, contestada e corrigida.
