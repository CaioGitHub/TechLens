# Plano de Implementação — INC-0: Fundação de Dados e Rastreabilidade (Ciclo 6)

## 1. Contexto e Objetivos

O **Stage 31.7.34** executa a implementação controlada do **Incremento 0 (INC-0)** da arquitetura aprovada no Ciclo 6 (Stages 31.7.31 a 31.7.33).

O objetivo principal do INC-0 é fornecer a fundação estrutural estritamente tipada e o contrato formal de rastreabilidade causal (`EvidenceTraceabilityRecord`) para todos os incrementos subsequentes (INC-1 a INC-5), sem alterar nenhuma lógica de classificação semântica, branch de decisão ou resultado preditivo existente.

### Metas Específicas
1. **Definição de Tipos e Contratos Formais**: Introduzir estruturas tipadas em Python (`dataclasses`) representando o perfil da pergunta (`QuestionProfile`), perfil discursivo da resposta (`DiscourseProfile`), avaliação de afinidade temática (`ThematicAffinityEvaluation`), equivalência conceitual (`EquivalenceEvaluation`), analogia (`AnalogyEvaluation`), nexo proposição-demanda (`DemandNexusEvaluation`), cobertura (`CoverageEvaluation`), incerteza epistêmica (`EpistemicUncertaintyRecord`) e decisão final (`FinalDecisionRecord`).
2. **Resolução Formal do FINDING-06**: Integrar o campo `applied_contract_ids` ao `FinalDecisionRecord` e ao schema JSON Draft-07 de rastreabilidade de evidências, com semântica de lista de identificadores contratuais aplicados, cardinalidade $\ge 0$, tipos string, opcionalidade retrocompatível e imutabilidade estrutural.
3. **Validação Estrutural e Semântica de Schema**: Implementar validador determinístico `validate_evidence_traceability_record` em estrita conformidade com o schema Draft-07 de rastreabilidade.
4. **Isolamento de Impacto e Zero Regressão**: Garantir que as classificações semânticas anteriores permaneçam 100% inalteradas (1.084 testes canônicos OK, 15/15 no Reference Harness).

---

## 2. Escopo Estrito e Limites Autorizados

### Autorizado para o INC-0
- Contratos e estruturas de dados indispensáveis ao INC-0 em `reference_runtime/runtime.py`.
- Implementação de `EvidenceTraceabilityRecord` e subestruturas tipadas associadas.
- Inclusão do campo `applied_contract_ids` em `FinalDecisionRecord` e no schema JSON.
- Função validadora de schema `validate_evidence_traceability_record`.
- Criação da suíte de testes unitários e contratuais (`tests/test_stage_31_7_34_inc0_contracts.py`).
- Documentação formal do plano, testes, regressões, diff, rollback e relatório de gate.

### Proibido no INC-0
- Alterar pesos, thresholds ou heurísticas de classificação semântica.
- Implementar a extração funcional de proposições discursivas (reservado ao INC-1).
- Implementar regras de suficiência, nexo ou agregação de classes (reservado ao INC-2/3/4).
- Alterar o comportamento dos entry points existentes (`_decoupled_evaluate_semantic_relevance`, `_evaluate_semantic_relevance`, `run_interview_pipeline`, `run_real_pilot`).

---

## 3. Mapeamento das Estruturas aos Contratos do Ciclo 6

| Estrutura de Dados | Contrato Canônico | Responsabilidade / Invariante |
|---|---|---|
| `DemandSpecification` | `stage_31_7_31_demand_sufficiency_contract.md` | Especifica uma demanda atômica da pergunta com flag de obrigatoriedade. |
| `QuestionProfile` | `stage_31_7_31_refined_architecture.md` (Camada 1) | Modela intenção (`intent_mode`), demanda primária, demandas secundárias e entidades alvo. |
| `DiscourseProposition` | `stage_31_7_31_proposition_composition_contract.md` | Proposição atômica isolada com papel discursivo (`discourse_role`), negação e condicionalidade. |
| `DiscourseProfile` | `stage_31_7_31_refined_architecture.md` (Camada 2) | Proposições extraídas da resposta e preâmbulos isolados da análise técnica. |
| `ThematicAffinityEvaluation` | `stage_31_7_31_thematic_connection_contract.md` | Presunção temática com suporte a refutação explícita (`rebuttal_detected`) e disjunção alienígena. |
| `EquivalenceEvaluation` | `stage_31_7_31_conceptual_equivalence_contract.md` | Avalia equivalência entre terminologias e conceitos sem choque de propriedades. |
| `AnalogyEvaluation` | `stage_31_7_31_analogy_handling_contract.md` | Avalia mapeamento de domínio veículo para mecanismos técnicos alvo. |
| `DemandNexusEvaluation` | `stage_31_7_31_content_substance_contract.md` | Relaciona proposição à demanda (`FUNCTIONALLY_SOLVES`, `CONTRIBUTES_TO`, etc.) com rationale. |
| `CoverageEvaluation` | `stage_31_7_31_demand_sufficiency_contract.md` | Relação de cobertura de demandas obrigatórias atendidas. |
| `EpistemicUncertaintyRecord` | `stage_31_7_31_refined_architecture.md` (Camada 5) | Nível de confiança e registro explícito de ambiguidades não resolvidas. |
| `FinalDecisionRecord` | `stage_31_7_31_seven_class_decision_contract.md` | Classificação (7 classes), regra formal, justificativa e contratos aplicados (`applied_contract_ids`). |
| `EvidenceTraceabilityRecord` | `stage_31_7_31_evidence_traceability_schema.json` | Contêiner raiz de rastreabilidade auditável fim a fim. |

---

## 4. Decisão de Design e Retrocompatibilidade (FINDING-06)

O achado adversarial `FINDING-06` do Stage 31.7.32 identificou que o schema JSON original não possuía uma lista explícita dos identificadores de contratos semânticos exercitados para chegar à decisão.

**Resolução Adotada**:
1. O campo `applied_contract_ids` foi adicionado como opcional na propriedade `final_decision` do schema Draft-07:
   ```json
   "applied_contract_ids": {
       "type": "array",
       "description": "Lista de identificadores de contratos semânticos aplicados (ex.: SC-01, TRACE-01). Resolução do FINDING-06.",
       "items": { "type": "string" },
       "uniqueItems": true
   }
   ```
2. No `FinalDecisionRecord`, o campo possui `default_factory=list`. Na serialização `to_dict()`, o campo é emitido se houver identificadores, ou omitido caso a lista esteja vazia, garantindo 100% de compatibilidade reversa com consumidores legados e esquemas anteriores.
3. A função de validação `validate_evidence_traceability_record` verifica se `applied_contract_ids` (se presente) é uma lista contendo exclusivamente strings válidas.

---

## 5. Estratégia de Testes e Critérios de Aceitação

A verificação do INC-0 é composta por 3 níveis rigorosos de validação:
1. **Nível 1 — Suíte de Testes Contratuais do INC-0 (`test_stage_31_7_34_inc0_contracts.py`)**:
   - 17 testes automatizados cobrindo os 8 requisitos da Seção 7 do mandato:
     - Validação estrutural do schema (positivo completo e mínimo válido).
     - Validação de identificadores obrigatórios (`evaluation_id`, `runtime_version_hash`, etc.).
     - Testes negativos (propriedades ausentes, enums inválidos, tipos incorretos, valores fora de escala).
     - Testes específicos do FINDING-06 (preenchido, vazio, omitido, tipo inválido).
     - Serialização JSON roundtrip sem perda de dados.
     - Robustez com proposições vazias e nós não vinculados.
     - Invariância semântica em relação aos comportamentos do runtime.
   - **Critério**: 100% de aprovação (17/17).
2. **Nível 2 — Suíte de Testes Canônica**:
   - Execução integral de `tests/test_*.py`.
   - **Critério**: Zero falhas, zero erros (1.084 testes executados, 1.083 OK, 1 skipped).
3. **Nível 3 — Reference Harness**:
   - Execução de `tests.test_stage_26_reference_harness`.
   - **Critério**: 100% de aprovação (15/15 OK).
