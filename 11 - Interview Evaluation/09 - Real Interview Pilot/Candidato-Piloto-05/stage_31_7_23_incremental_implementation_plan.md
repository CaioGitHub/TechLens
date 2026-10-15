---
type: architecture
status: study
confidence: 95
created: 2026-10-14
updated: 2026-10-14
tags:
  - stage-31-7-23
  - implementation-plan
  - incremental-plan
  - cycle-4
---

# Stage 31.7.23 — Plano de Implementação Incremental (Cycle 4)

## 1. Diretrizes de Execução Controlada

A implementação da arquitetura aprovada no Stage 31.7.22 será executada no **Stage 31.7.24** de forma estritamente modular, dividida em 5 incrementos sequenciais com dependências explícitas.

**Regras Mandatórias de Execução:**
1. Nenhum incremento pode ser iniciado sem que o anterior tenha sido auditado e aprovado com 100% de conformidade nos testes canônicos.
2. Cada incremento deve criar um checkpoint intermediário do runtime antes de iniciar qualquer edição.
3. Se qualquer teste existente falhar ou surgir comportamento inexplicado, o rollback imediato para o checkpoint do incremento anterior é obrigatório.
4. **Nenhum código será implementado no Stage 31.7.23.** Este documento constitui o plano aprovado que autorizará o Stage 31.7.24.

---

## 2. Mapa de Dependências dos Incrementos

```text
[Baseline: runtime.py congelado (SHA-256: 75C6841D...)]
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│ Incremento A: Intenção e Demandas                      │
│ Componente: SemanticIntentAndDemandExtractor           │
│ Resolve: CR-01 (subdecomposição em orações simples)    │
└────────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│ Incremento B: Nexo Funcional e Cobertura Bipartida     │
│ Componente: DemandPropositionNexusBipartiteMatcher     │
│ Resolve: CR-06 (acoplamento difuso em multi-demandas)  │
└────────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│ Incremento C: Gênero Discursivo e Circularidade        │
│ Componentes: PropositionDiscourseFilter &              │
│              MorphologicalCircularityAnalyzer          │
│ Resolve: CR-02, CR-03, CR-05 (trivia/declaração/tauto) │
└────────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│ Incremento D: Polaridade, Evasão e Incerteza           │
│ Componentes: Filtros de Antítese e Mapeamento Evasivo  │
│ Resolve: CR-04, CR-07, CR-08 (EVASIVE -> INSUFFICIENT) │
└────────────────────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────┐
│ Incremento E: Agregação Canônica e Integração Final    │
│ Componente: StrictOntologyRelevanceAggregator          │
│ Validação: Regressão Canônica Completa + Harness       │
└────────────────────────────────────────────────────────┘
                         │
                         ▼
[Novo Runtime Congelado para Validação Cega no Stage 31.7.25]
```

---

## 3. Especificação Detalhada por Incremento

### Incremento A — Intenção Semântica e Decomposição de Demandas
- **Componente Foco:** `SemanticIntentAndDemandExtractor` (refatoração de `decompose_question`).
- **Arquivos a Modificar no Stage 31.7.24:** `reference_runtime/runtime.py`.
- **Causas-Raiz Abordadas:** CR-01 (Demanda composta tratada como simples em orações sem conjunção explícita).
- **Responsabilidades Alteradas:**
  - Extrair aspectos obrigatórios de estados em máquinas de estado (ex: fechado, aberto e meio-aberto).
  - Decompor perguntas com pares de ação/compensação (ex: coordenação e transações compensatórias em Saga).
  - Preservar o isolamento de escopo sem fragmentação artificial.
- **Pré-condições:** Baseline congelado com SHA-256 `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`.
- **Pós-condições:** `decompose_question` retorna `QuestionAnalysis` contendo a lista completa de aspectos obrigatórios para perguntas compostas.
- **Testes de Contrato:**
  - `TC-01`: Pergunta sobre Circuit Breaker gera 3 aspectos obrigatórios (`fechado`, `aberto`, `meio-aberto`).
  - `TC-02`: Pergunta sobre Saga gera 2 demandas obrigatórias (`coordenação`, `compensação`).
- **Testes de Regressão:** Suíte canônica (`py -m unittest discover tests`) com 1038 testes sem falhas.
- **Critério de Rollback:** Falha em testes existentes de decomposição de perguntas.

---

### Incremento B — Relação Funcional e Cobertura Bipartida
- **Componente Foco:** `DemandPropositionNexusBipartiteMatcher` (refatoração de `assess_demand_nexus`).
- **Arquivos a Modificar no Stage 31.7.24:** `reference_runtime/runtime.py`.
- **Causas-Raiz Abordadas:** CR-06 (Acoplamento difuso em multi-demandas via correspondência de palavras isoladas) e CR-01.
- **Responsabilidades Alteradas:**
  - Eliminar a escada de `if/elif` com palavras isoladas (`coordenador`, `revogacao`, `vazao de escrita`).
  - Implementar verificação de correspondência 1-para-1 ou M-para-N explícita.
  - Exigir mecanismo comprobatório substantivo para cada demanda primária independente.
- **Pré-condições:** Incremento A concluído e testado.
- **Pós-condições:** Uma proposição só satisfaz a demanda se demonstrar o mecanismo operacional exigido por ela.
- **Testes de Contrato:**
  - `TC-02B`: Em pergunta sobre 2PC com queda do coordenador, resposta que apenas explica o fluxo normal recebe `satisfaction_degree = 'UNMET'` para a demanda 2.
- **Testes de Regressão:** Suíte canônica (1038 testes) + Reference Harness (15 testes).
- **Critério de Rollback:** Atribuição indevida de `FUNCTIONALLY_SOLVES` a demandas secundárias não explicadas.

---

### Incremento C — Gênero Discursivo e Circularidade Morfológica
- **Componentes Foco:** `PropositionDiscourseFilter` e `MorphologicalCircularityAnalyzer` (refatoração de `extract_response_propositions` e `_detect_structural_circularity`).
- **Arquivos a Modificar no Stage 31.7.24:** `reference_runtime/runtime.py`.
- **Causas-Raiz Abordadas:** CR-02 (Relatos autobiográficos), CR-03 (Circularidade morfológica), CR-05 (Fatos históricos).
- **Responsabilidades Alteradas:**
  - Classificar gênero discursivo em 7 categorias. Fatos históricos (Sysoev, Codd) e relatos pessoais ("já usei em produção") recebem `is_operative = False`.
  - Unificar lemas e famílias cognatas entre substantivos e verbos (`compressão` ↔ `comprimir`, `replicação` ↔ `replicar`, `travamento` ↔ `travar`), identificando tautologias independentemente da flexão.
- **Pré-condições:** Incremento B concluído e testado.
- **Pós-condições:** Relatos autobiográficos e anedotas históricas recebem `HISTORICAL_TRIVIA` ou `PERSONAL_DECLARATION`. Tautologias puras recebem `is_circular_tautology = True`.
- **Testes de Contrato:**
  - `TC-03`: Fatos sobre criadores com verbos ativos recebem `HISTORICAL_TRIVIA` e `is_operative = False`.
  - `TC-04`: Relatos autobiográficos sem mecanismo recebem `PERSONAL_DECLARATION` e `is_operative = False`.
  - `TC-05`: Tautologias nominais/verbais recebem `is_circular_tautology = True`.
- **Testes de Regressão:** Suíte canônica (1038 testes) sem regressões.
- **Critério de Rollback:** Falha na identificação de proposições operativas genuínas em respostas concisas.

---

### Incremento D — Polaridade, Evasão e Incerteza
- **Componentes Foco:** Filtros de Antítese em `_detect_antithesis` e Mapeamento Evasivo em `evaluate_relevance`.
- **Arquivos a Modificar no Stage 31.7.24:** `reference_runtime/runtime.py`.
- **Causas-Raiz Abordadas:** CR-04 (Mapeamento errôneo EVASIVE -> UNKNOWN), CR-07 (Invariância em antíteses coloquiais/passivas), CR-08 (Escopo de polaridade).
- **Responsabilidades Alteradas:**
  - Corrigir a linha 3633: respostas com `is_evasive == True` passam a ser mapeadas para `INSUFFICIENT`.
  - Expandir padrões de antítese destrutiva para capturar formas coloquiais ("tirar a trava") e voz passiva ("quando as travas forem retiradas").
  - Preservar a guarda preventiva de evitação do Grupo I (92,86% de eficácia).
- **Pré-condições:** Incremento C concluído e testado.
- **Pós-condições:** Evasões recebem `INSUFFICIENT`; antíteses coloquiais/passivas recebem `OFF_TOPIC`.
- **Testes de Contrato:**
  - `TC-06`: Respostas evasivas ("depende do caso") recebem deterministicamente `INSUFFICIENT`.
  - `TC-07`: Remoção coloquial de travas/ACID recebe terminantemente `OFF_TOPIC`.
- **Testes de Regressão:** Suíte canônica (1038 testes) + Reference Harness (15 testes).
- **Critério de Rollback:** Falsos positivos de antítese em respostas que explicam prevenção.

---

### Incremento E — Agregação Canônica e Integração Final
- **Componente Foco:** `StrictOntologyRelevanceAggregator` (unificação final em `evaluate_open_domain_semantic_relevance`).
- **Arquivos a Modificar no Stage 31.7.24:** `reference_runtime/runtime.py`.
- **Causas-Raiz Abordadas:** CR-01 a CR-08 (Consolidação da trilha de decisão e da ontologia das 7 classes).
- **Responsabilidades Alteradas:**
  - Centralizar toda a lógica de atribuição de classe em regras formais imutáveis.
  - Gerar trilha de decisão auditável (`decision_trail`).
  - Assegurar determinismo estrito e compatibilidade reversa total com contratos do Reference Harness.
- **Pré-condições:** Incrementos A, B, C e D concluídos e validados individualmente.
- **Pós-condições:** Runtime totalmente funcional, integrado e congelado sob novo digest SHA-256.
- **Testes de Contrato:** Execução completa dos 7 testes de contrato integrados (TC-01 a TC-07).
- **Testes de Regressão:**
  - Execução da suíte canônica de 1.038 testes com 100% de aprovação.
  - Execução do Reference Harness (15/15 testes com 100% de aprovação).
- **Critério de Rollback:** Qualquer regressão observada na suíte canônica ou no Reference Harness.

---

## 4. Matriz de Rastreabilidade: Causas-Raiz vs. Incrementos

| Causa-Raiz | Descrição Sucinta | Incremento Responsável | Teste de Contrato |
|---|---|:---:|:---:|
| **CR-01** | Subdecomposição de demandas multi-aspecto em orações simples | **Incremento A & B** | `TC-01`, `TC-02` |
| **CR-02** | Verbos técnicos em relatos autobiográficos e históricos | **Incremento C** | `TC-03`, `TC-04` |
| **CR-03** | Tautologia circular burlada por divergência morfológica | **Incremento C** | `TC-05` |
| **CR-04** | Disjunção terminológica hardcoded (EVASIVE -> UNKNOWN) | **Incremento D** | `TC-06` |
| **CR-05** | Proximidade temática e metadados promovidos a DIRECT | **Incremento C** | `TC-03` |
| **CR-06** | Cross-satisfaction de demandas por token isolado coincidente | **Incremento B** | `TC-02B` |
| **CR-07** | Invariância assimétrica em formulações coloquiais/passivas | **Incremento D** | `TC-07` |
| **CR-08** | Preservação da salvaguarda preventiva de polaridade | **Incremento D** | `TC-07B` |
