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
BLIND_SEMANTIC_REVALIDATION_BLOCKED

Stage 31.7.29
    ↓
RUNTIME_PROVENANCE_RECONCILED
RCA_COMPLETE_ARCHITECTURE_PENDING_REVIEW

Stage 31.7.30
    ↓
RUNTIME_PROVENANCE_RECONCILED
ARCHITECTURE_REQUIRES_REVISION

Stage 31.7.31
    ↓
NEXT STAGE (Architectural Remediation & Refined Specification — Cycle 6)
```

O Stage 31.7.30 concluiu a revisão adversarial e os testes de estresse contratual da arquitetura do Ciclo 6:
1. **Proveniência do Runtime Confirmada (`RUNTIME_PROVENANCE_RECONCILED`):** Todas as 9 alegações sobre o runtime `6C44B7A8...` foram 100% verificadas (`VERIFIED`), comprovando que ele é a versão legítima homologada com 0 regressões e autorizada pelo usuário.
2. **Revisão Adversarial da Regra de Entidades (`ARCHITECTURE_REQUIRES_REVISION`):** A regra de "veto absoluto" de `OFF_TOPIC` por compartilhamento de entidade foi refutada pelo Cenário E (homonímia/divagação geopolítica) e pelo Cenário C (respostas corretas sem menção literal da entidade, gerando risco de falso `OFF_TOPIC`).
3. **Prescrições Mandatórias para o Ciclo 6:** (1) Substituir o veto absoluto por presunção refutável de pertinência temática derrubada por predicados alienígenas; (2) Reconhecer equivalências conceituais e hiperônimos técnicos; (3) Instituir regra de isenção para analogias pedagógicas (e.g. disjuntor elétrico para circuit breaker); (4) Aplicar segmentação oracional para isolar preâmbulos conversacionais de ruído; (5) Filtrar elogios superficiais como `INSUFFICIENT`. O runtime permaneceu 100% congelado no hash `6C44B7A8...`.
4. **Próximo Passo:** **Stage 31.7.31 — Architectural Remediation & Refined Specification (Cycle 6)** para incorporar as prescrições mandatórias antes de qualquer autorização de implementação.

## Regra fundamental

Não modificar o projeto apenas para fazer testes passarem.

Não criar regras específicas para casos individuais.

Não apagar histórico.

Não utilizar avaliação humana como alvo de score.

Não pular stages.

Não interpretar `BLOCKED` como aprovação.

## Princípio

> Não estamos construindo um sistema que parece inteligente. Estamos construindo um sistema cuja avaliação pode ser investigada, reproduzida, contestada e corrigida.
