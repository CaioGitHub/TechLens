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
REFINED_ARCHITECTURE_READY_FOR_INDEPENDENT_REVIEW
RUNTIME_PROVENANCE_RECONCILED

Stage 31.7.32
    ↓
ARCHITECTURE_APPROVED_FOR_IMPLEMENTATION_PLANNING
RUNTIME_PROVENANCE_RECONCILED

Stage 31.7.33
    ↓
IMPLEMENTATION_PLAN_READY_FOR_GOVERNANCE_APPROVAL
RUNTIME_PROVENANCE_RECONCILED

Stage 31.7.34
    ↓
INC0_FOUNDATION_IMPLEMENTED_AND_VERIFIED
RUNTIME_PROVENANCE_RECONCILED

Stage 31.7.35
    ↓
NEXT STAGE (Controlled Implementation of Question Profile and Proposition Engine — Increment 1)
```

O Stage 31.7.34 concluiu a implementação controlada do Incremento 0 (INC-0: Fundação de Dados e Rastreabilidade) do Ciclo 6:
1. **Fundação Estrutural e Tipagem Forte:** Introdução de dataclasses tipadas no runtime (`reference_runtime/runtime.py`) para perfis de pergunta e resposta, proposições discursivas, avaliações temáticas, nexos causais, equivalências, analogias ancoradas e registros de incerteza epistêmica.
2. **Resolução Formal do FINDING-06:** Inclusão do campo opcional `applied_contract_ids` em `FinalDecisionRecord` e no schema JSON Draft-07 de rastreabilidade causal (`EvidenceTraceabilityRecord`), com validação determinística estrita e 100% de retrocompatibilidade.
3. **100% dos Testes Contratuais Aprovados:** Suíte dedicada `tests/test_stage_31_7_34_inc0_contracts.py` com 17 testes automatizados cobrindo todos os critérios de schema, identificadores, enums, limites, serialização e invariância semântica.
4. **Zero Regressões Confirmadas:** A suíte canônica completa foi expandida para **1.084 testes (1.083 OK, 1 skipped, 0 falhas, 0 erros)** e o Reference Harness atingiu aprovação total (**15/15 OK**). O runtime avançou para o hash `E047BA643A6E98975E42336C58339A12AB4D33D48082ED808FF26248478AB1B8`.
5. **Próximo Passo Autorizado:** **Stage 31.7.35 — Controlled Implementation of Question Profile and Proposition Engine (Increment 1)**.

## Regra fundamental

Não modificar o projeto apenas para fazer testes passarem.

Não criar regras específicas para casos individuais.

Não apagar histórico.

Não utilizar avaliação humana como alvo de score.

Não pular stages.

Não interpretar `BLOCKED` como aprovação.

## Princípio

> Não estamos construindo um sistema que parece inteligente. Estamos construindo um sistema cuja avaliação pode ser investigada, reproduzida, contestada e corrigida.


## Auditoria e correções locais — 2026-10-23

Stage 31.7.35 permanece em andamento. Três falhas de extração foram corrigidas e cobertas por 13 novos testes. Regressão atual: 1.097 testes (1.096 aprovados, 1 ignorado), sem falhas ou erros. Classificador fora das duas classes INC-1 permaneceu inalterado por comparação AST. Gate limitado: `AUDIT_FIXES_VERIFIED_INC1_FULL_ACCEPTANCE_PENDING`. Ver [[stage_31_7_35_audit_fixes_report]]. A proveniência histórica dos snapshots continua não comprovada; esta nota não substitui os registros históricos.


## Cobertura complementar do Stage 31.7.35 — 2026-10-23

22 novos testes complementares e correções em grupos sequenciais. Regressão: 1119 testes (1118 aprovados, 1 ignorado), sem falhas ou erros; harness 15/15. Gate limitado: `CONTRACT_SCENARIOS_VERIFIED_GOVERNANCE_RECONCILIATION_PENDING`. Ver [[stage_31_7_35_remaining_contracts_report]]. Etapa continua aberta para reconciliação de escopo entre os planos e limites semânticos documentados; não houve promoção automática ao próximo incremento.


## Reconciliação de referências e aceite — 2026-10-23

Ver [[stage_31_7_35_scope_reconciliation]]. IDs locais da rastreabilidade representacional não equivalem aos IDs homônimos da matriz semântica: novas referências usam arquivo + identificador. Dez famílias históricas de suficiência agrupam Definição/Conceito; onze modos representacionais os distinguem. 52 testes direcionados reexecutados e aprovados; runtime inalterado. Gate limitado: `REPRESENTATION_REFERENCES_RECONCILED_SEMANTIC_ACCEPTANCE_OPEN`. Stage 31.7.35 continua aberto para critérios funcionais próprios de suficiência e segmentação, sem dispensa dos contratos históricos ou homologação automática.


## Inventário de aceitação semântica — 2026-10-23

Ver [[stage_31_7_35_semantic_acceptance_inventory]]. 16 critérios semânticos e oito casos adversariais registrados com fonte, expectativa e evidência necessária. Próximo passo: fixar oracles/caminhos de rastreabilidade e executar diagnóstico funcional da API existente antes de novas correções. Estado limitado: `SEMANTIC_ACCEPTANCE_INVENTORIED_NOT_VALIDATED`; runtime inalterado. Módulos planejados ausentes não demonstram inexistência de capacidade equivalente. Sem novas previsões ou homologação semântica nesta etapa documental.
