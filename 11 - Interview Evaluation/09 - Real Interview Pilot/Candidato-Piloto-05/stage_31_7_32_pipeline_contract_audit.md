# Stage 31.7.32 — Auditoria de Contratos e Responsabilidades dos Sete Estágios do Pipeline

## 1. Visão Geral do Fluxo Arquitetural Proposto

A especificação do Stage 31.7.31 decompôs o motor de relevância semântica em sete estágios sequenciais. Esta auditoria examina a integridade das interfaces de entrada/saída, a causalidade das dependências, as sobreposições de responsabilidade, a propagação de falhas e a presença de possíveis circularidades ou fallbacks implícitos.

```text
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                        DIAGRAMA DE FLUXO DO PIPELINE DO CICLO 6                        │
 └────────────────────────────────────────────────────────────────────────────────────────┘
                                            │
  [raw_question]                            ▼
  ────────────────►  1. QuestionProfileExtractor
                        ├─► Output: QuestionProfile (intent_mode, Dp, Ds, Eq, context)
                        │
  [raw_response]                            ▼
  ────────────────►  2. DiscourseSegmentationEngine
                        ├─► Output: DiscourseProfile (propositions, isolated_preambles, modifiers)
                        │
                                            ▼
                     3. ThematicAffinityEngine
                        ├─► Input: QuestionProfile, DiscourseProfile
                        ├─► Test: (Er ∩ Eq ≠ ∅) + Predicate Disjunction Test
                        ├─► Output: ThematicEvaluation (presumption_status, rebuttal_reason, is_alien)
                        │
                                            ▼
                     4. ConceptualEquivalenceEngine
                        ├─► Input: QuestionProfile, DiscourseProfile, ThematicEvaluation
                        ├─► Test: Invariant Properties Matching (Hypernyms, Paraphrases, CS Invariants)
                        ├─► Output: EquivalenceEvaluation (established_equivalences, property_clash)
                        │
                                            ▼
                     5. AnalogyResolutionEngine
                        ├─► Input: DiscourseProfile (Analogy Clauses), QuestionProfile
                        ├─► Test: Decouple Dv from Dt; Verify Grounding in Dt
                        ├─► Output: AnalogyEvaluation (is_grounded, target_mechanisms_resolved)
                        │
                                            ▼
                     6. SufficiencyAssessmentEngine
                        ├─► Input: QuestionProfile, DiscourseProfile, EquivalenceEvaluation, AnalogyEval
                        ├─► Test: Bipartite Demand Matching (Dp, Ds) + Intent Matrix Rules
                        ├─► Output: DemandNexusMatrix, CoverageEvaluation (coverage_ratio, gaps)
                        │
                                            ▼
                     7. StrictRelevanceAggregator
                        ├─► Input: All Stage Evaluations
                        ├─► Test: Reconciled Canonical Decision Table (Vetoes -> Multi -> Single Demand)
                        ├─► Explicit Routing: THEMATICALLY_ADJACENT ──► RELATED
                        └─► Output: Final Classification + EvidenceTraceabilityRecord JSON
```

---

## 2. Auditoria Individual dos Sete Estágios

### Estágio 1: `QuestionProfileExtractor`
- **Objetivo:** Identificar a intenção epistemológica da pergunta (entre 10 modos) e decompor suas demandas ($D_P, D_S$) e entidades centrais ($E_Q$).
- **Entrada:** `raw_question: str`
- **Saída:** `QuestionProfile`
- **Pré-condições:** Texto da pergunta não vazio e semanticamente formado.
- **Pós-condições:** Exatamente 1 modo de intenção selecionado, exatamente 1 demanda primária ($D_P$) definida, zero ou mais demandas secundárias ($D_S$), lista de entidades $E_Q$.
- **Dependências:** Nenhuma (estágio de entrada).
- **Tratamento de Incerteza:** Se a intenção for ambígua, adota o modo mais abrangente e registra incerteza no perfil.
- **Modos de Falha:** Erro na identificação de demandas compostas implícitas (quando a segunda pergunta não vem precedida de "e como").
- **Propagação de Erro:** Se falhar na extração de $D_S$, uma resposta completa pode ser avaliada apenas contra $D_P$, gerando falso `DIRECT` por simplificação de demanda.

### Estágio 2: `DiscourseSegmentationEngine`
- **Objetivo:** Decompor a resposta em proposições atômicas, isolando preâmbulos de ruído fático e anotando modificadores sintáticos (negações, condicionais, analogias, autocorreções).
- **Entrada:** `raw_response: str`
- **Saída:** `DiscourseProfile`
- **Pré-condições:** Texto da resposta normalizado.
- **Pós-condições:** Todas as sentenças catalogadas com papéis discursivos (`TECHNICAL_CORE`, `PREAMBLE`, etc.), escopos de negação e condicionais vinculados.
- **Dependências:** Nenhuma (opera diretamente sobre o texto).
- **Tratamento de Incerteza:** Sentenças ambíguas são mantidas como `TECHNICAL_CORE` por padrão conservador, para não descartar conteúdo técnico legítimo por engano.
- **Modos de Falha:** Fragmentação excessiva de sentenças ou corte indevido de orações subordinadas condicionais.
- **Propagação de Erro:** A perda de um operador de negação pode inverter a polaridade da afirmação no Estágio 6.

### Estágio 3: `ThematicAffinityEngine`
- **Objetivo:** Estabelecer a presunção de pertinência temática ($H_{tema}$) por compartilhamento de entidades e aplicar testes de refutação por predicados alienígenas ou disjunção radical aberta.
- **Entrada:** `QuestionProfile`, `DiscourseProfile`
- **Saída:** `ThematicEvaluation`
- **Pré-condições:** Entidades $E_Q$ extraídas e proposições disponíveis.
- **Pós-condições:** Presunção rotulada como `CONFIRMED`, `REBUTTED`, `EQUIVALENCE_ESTABLISHED` ou `NOT_ESTABLISHED`.
- **Dependências:** Estágios 1 e 2.
- **Tratamento de Incerteza:** Se o domínio de um predicado não puder ser determinado com segurança, **NÃO** dispara refutação; mantém a presunção sob observação para o Estágio 4/6.
- **Modos de Falha:** Erro na desambiguação de homônimos técnicos sutis (e.g. "pool de conexões" vs "piscina de natação").
- **Propagação de Erro:** Se refutar indevidamente, o Estágio 7 gerará falso `OFF_TOPIC`. Se não refutar, o Estágio 6 terá que discernir a suficiência.

### Estágio 4: `ConceptualEquivalenceEngine`
- **Objetivo:** Reconhecer equivalências funcionais, hiperônimos técnicos e tecnologias inéditas/fictícias que atendam aos invariantes da pergunta sem repetir o nome literal.
- **Entrada:** `QuestionProfile`, `DiscourseProfile`, `ThematicEvaluation`
- **Saída:** `EquivalenceEvaluation`
- **Pré-condições:** Perfil de intenção da pergunta e proposições discursivas estruturadas.
- **Pós-condições:** Registro de equivalências estabelecidas e flag de conflito conceitual (propriedades incompatíveis).
- **Dependências:** Estágios 1, 2 e 3.
- **Tratamento de Incerteza:** Descrições muito vagas de categorias amplas recebem status de equivalência atenuada (recomenda `PARTIAL` ou `RELATED`, vetando `DIRECT`).
- **Modos de Falha:** Não reconhecer uma paráfrase complexa em linguagem coloquial.
- **Propagação de Erro:** Se não reconhecer a equivalência, uma resposta excelente (Caso D: B-tree explicada como árvore balanceada) corre risco de ser tratada como irrelevante.

### Estágio 5: `AnalogyResolutionEngine`
- **Objetivo:** Desacoplar orações analógicas do mundo físico ($D_V$) e verificar se houve aterrissagem substantiva no sistema computacional ($D_T$).
- **Entrada:** `DiscourseProfile` (proposições com papel `ANALOGY_VEHICLE`), `QuestionProfile`
- **Saída:** `AnalogyEvaluation`
- **Pré-condições:** Existência de proposições analógicas identificadas no Estágio 2.
- **Pós-condições:** Veredito de analogia ancorada (`GROUNDED`) ou desancorada (`UNGROUNDED`).
- **Dependências:** Estágios 1 e 2.
- **Tratamento de Incerteza:** Se a aterrissagem for curta ou ambígua, veta `DIRECT` e permite avaliação como `SUPPORTING` ou `INSUFFICIENT`.
- **Modos de Falha:** Dependência excessiva de termos-chave literais de transposição ("no software", "na aplicação").
- **Propagação de Erro:** Se aprovar uma metáfora vazia, gera falso `DIRECT`; se rejeitar uma analogia ancorada, gera falso `INSUFFICIENT`.

### Estágio 6: `SufficiencyAssessmentEngine`
- **Objetivo:** Mapear o grafo bipartite entre cada demanda da pergunta e as proposições da resposta, aplicando a matriz de critérios dos 10 modos de intenção e calculando a cobertura ($D_P, D_S$).
- **Entrada:** Saídas dos Estágios 1, 2, 3, 4 e 5.
- **Saída:** `DemandNexusMatrix`, `CoverageEvaluation`
- **Pré-condições:** Demandas decompostas, equivalências mapeadas e discurso segmentado.
- **Pós-condições:** Cada demanda associada a uma relação formal (`FUNCTIONALLY_SOLVES`, `PARTIALLY_SOLVES`, `CONTRIBUTES_TO`, `THEMATICALLY_ADJACENT`, `NON_OPERATIVE`, `EVASIVE`, `IGNORANCE`, etc.) e índice de cobertura calculado ($0.0$ a $1.0$).
- **Dependências:** Todos os estágios anteriores.
- **Tratamento de Incerteza:** Se as evidências forem insuficientes para comprovar o mecanismo, emite nexo com grau de confiança reduzido.
- **Modos de Falha:** Avaliar uma resposta de definição com critérios exigentes de código de implementação.
- **Propagação de Erro:** Alimenta diretamente a tabela de decisão final no Estágio 7.

### Estágio 7: `StrictRelevanceAggregator`
- **Objetivo:** Consolidar todas as evidências na tabela de decisão determinística fechada das 7 classes canônicas, emitindo a classificação final e o schema JSON `EvidenceTraceabilityRecord`.
- **Entrada:** Todas as estruturas emitidas pelos Estágios 1 a 6.
- **Saída:** Classificação canônica final (`DIRECT`, `PARTIAL`, `SUPPORTING`, `RELATED`, `OFF_TOPIC`, `INSUFFICIENT`, `UNKNOWN`) + Registro JSON de rastreabilidade.
- **Pré-condições:** Todos os estágios 1 a 6 executados.
- **Pós-condições:** Classificação final única gerada estritamente por regras determinísticas auditáveis.
- **Dependências:** Todos os estágios.
- **Tratamento de Incerteza:** Quando há contradição irresolúvel ou tautologia, emite `UNKNOWN`. Quando há ausência de dados avaliáveis, emite `INSUFFICIENT`.
- **Modos de Falha:** Não há falhas lógicas no agregador desde que os estágios a montante forneçam as relações corretas.
- **Propagação de Erro:** Fim do pipeline.

---

## 3. Análise Crítica de Dependências, Circularidades e Fallbacks

1. **Ausência de Circularidade:** A ordem linear $1 \to 2 \to 3 \to 4 \to 5 \to 6 \to 7$ é causalmente estrita. Nenhum estágio depende da saída de um estágio posterior.
2. **Eliminação do Fallback Implícito:** O Stage 31.7.31 eliminou o histórico sumidouro `else: OFF_TOPIC`. Agora, nexos não-operativos de mesmo ecossistema são explicitamente roteados para `RELATED`, e asserções sem substância para `INSUFFICIENT`.
3. **Ponto de Atenção Identificado (Severidade: MAJOR):**
   - Os Estágios 3 (Afinidade Temática) e 4 (Equivalência Conceitual) possuem fronteiras interdependentes quando a pergunta cita uma tecnologia $A$ e a resposta descreve a estrutura funcional $B$ sem citar $A$. O Estágio 3 não pode emitir veto prematuro de disjunção antes que o Estágio 4 avalie a equivalência funcional.
   - *Recomendação Obrigatória para a Implementação:* O Estágio 3 deve marcar o status como `EQUIVALENCE_PENDING` em vez de `NOT_ESTABLISHED`, permitindo que o Estágio 4 confirme a equivalência funcional antes de qualquer conclusão sobre afinidade temática.
