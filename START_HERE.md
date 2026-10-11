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
NEXT STAGE (Independent Contract Validation and Blind Semantic Revalidation Design)
```

O Stage 31.7.11 implementou de forma controlada a arquitetura **Demand-Proposition Nexus Architecture** em `reference_runtime/runtime.py` (Exit SHA-256: `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E`). A implementação eliminou a heurística de proxy de tamanho de resposta (`len(r_words) >= 8`) e os atalhos permissivos para `DIRECT`, implementando a avaliação de nexus par-a-par (`FUNCTIONALLY_SOLVES`, `CONTRIBUTES_TO`, `THEMATICALLY_ADJACENT`, `ANTITHESIS_OPPOSED`, `DOMAIN_DISJUNCT`, `UNKNOWN`/`INSUFFICIENT`) e epistemologia desacoplada. O motor legado (`engine="legacy"`) foi mantido inalterado como padrão para garantir compatibilidade histórica total. Todos os 1013 testes da suíte canônica passaram (100% PASS), a suíte contratual cobriu 8 categorias (A a H) e o Reference Harness determinístico executou com status `PASS_WITH_WARNINGS` (8/8 suítes). O gate foi emitido como `CONTROLLED_DEMAND_PROPOSITION_IMPLEMENTATION_COMPLETE`.

## Regra fundamental

Não modificar o projeto apenas para fazer testes passarem.

Não criar regras específicas para casos individuais.

Não apagar histórico.

Não utilizar avaliação humana como alvo de score.

Não pular stages.

Não interpretar `BLOCKED` como aprovação.

## Princípio

> Não estamos construindo um sistema que parece inteligente. Estamos construindo um sistema cuja avaliação pode ser investigada, reproduzida, contestada e corrigida.
