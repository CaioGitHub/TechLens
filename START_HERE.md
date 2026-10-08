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
NEXT STAGE (Root Cause Analysis & Semantic Relation Nexus Remediation)
```

O Stage 31.7.9 realizou a validação cega independente da arquitetura **Open-Domain Proposition & Semantic Relation** sobre o runtime 100% congelado (SHA-256: `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`), avaliando 242 casos independentes contra oráculo humano independente. O resultado demonstrou superação total da barreira lexical (100% de acerto na Categoria P de False Negative Traps e 92.86% em Invariância de Representação), mas revelou uma nova vulnerabilidade estrutural: **Permissividade Proposicional (Bias de Falsos Positivos)**, onde 88 dos 101 erros foram falsos `DIRECT` causados por heurísticas de ação operativa excessivamente permissivas que ignoravam o nexo funcional entre a demanda e a resposta. Com 58.26% de concordância exata e falhas recorrentes nas categorias O (0%) e G (18.75%), o gate foi emitido como `POST_OPEN_DOMAIN_BLIND_REVALIDATION_BLOCKED`. A regressão histórica permaneceu integralmente intacta (1005/1005 testes, 8/8 suites do Harness).

## Regra fundamental

Não modificar o projeto apenas para fazer testes passarem.

Não criar regras específicas para casos individuais.

Não apagar histórico.

Não utilizar avaliação humana como alvo de score.

Não pular stages.

Não interpretar `BLOCKED` como aprovação.

## Princípio

> Não estamos construindo um sistema que parece inteligente. Estamos construindo um sistema cuja avaliação pode ser investigada, reproduzida, contestada e corrigida.
