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
NEXT STAGE (Root Cause Analysis & Architecture Remediation for Propositional Precision, Tautology Detection and Demand Conjunctive Satisfaction)
```

O Stage 31.7.17 executou a revalidação semântica cega independente do runtime congelado no Stage 31.7.16 (`AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB`) sobre 200 casos técnicos inéditos (0% de sobreposição com os 250 casos do Stage 31.7.13). A validação seguiu protocolo estritamente cego e determinístico. O runtime demonstrou avanço expressivo em Recall de DIRECT (88,89%, superando a meta de $\ge 85\%$) e na classificação de SUPPORTING (96,0%), mantendo regressão canônica perfeita de 1.024 testes aprovados (`OK (skipped=1)`) e Reference Harness 8/8 aprovado. No entanto, o runtime falhou em 5 dos 7 critérios de aceitação: Concordância Exata atingiu 62,00% (meta $\ge 75\%$), Precisão de DIRECT foi de 47,62% (meta $\ge 70\%$), Falsos DIRECTs entre divergências foi de 57,89% (meta $\le 10\%$), Recall de PARTIAL foi de 45,71% (meta $\ge 60\%$) e Invariância de Representação foi de 61,54% (meta $\ge 80\%$). A auditoria semântica revelou 44 falsos DIRECTs gerados por falta de conjunção estrita em perguntas multi-demanda (14 casos PARTIAL), confusão entre descrição histórica/institucional e resolução mecânica (15 casos RELATED), tautologias circulares não detectadas (6 casos UNKNOWN) e vazamento léxico em antíteses/casos cotidianos (7 casos OFF_TOPIC). O gate formal emitido foi `GATE: BLIND_SEMANTIC_REVALIDATION_BLOCKED`. A próxima etapa é o **Stage 31.7.18 — Root Cause Analysis & Architecture Remediation for Propositional Precision, Tautology Detection and Demand Conjunctive Satisfaction**.

## Regra fundamental

Não modificar o projeto apenas para fazer testes passarem.

Não criar regras específicas para casos individuais.

Não apagar histórico.

Não utilizar avaliação humana como alvo de score.

Não pular stages.

Não interpretar `BLOCKED` como aprovação.

## Princípio

> Não estamos construindo um sistema que parece inteligente. Estamos construindo um sistema cuja avaliação pode ser investigada, reproduzida, contestada e corrigida.
