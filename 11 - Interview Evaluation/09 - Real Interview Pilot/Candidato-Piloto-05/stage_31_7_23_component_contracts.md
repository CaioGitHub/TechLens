---
type: architecture
status: study
confidence: 95
created: 2026-10-14
updated: 2026-10-14
tags:
  - stage-31-7-23
  - component-contracts
  - semantic-pipeline
  - cycle-4
---

# Stage 31.7.23 — Especificação Formal dos Contratos de Componentes (Cycle 4)

## 1. Princípios de Arquitetura e Separação de Responsabilidades

Para assegurar auditabilidade causal e eliminar o acoplamento procedural monolítico identificado no Stage 31.7.22, a arquitetura do motor semântico é decomposta em 5 componentes com **responsabilidade estrita e única**:

```text
Entrada da Avaliação: (question_text: str, response_text: str)
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│ 1. SemanticIntentAndDemandExtractor                          │
│    Interpreta intenção e extrai demandas e aspectos          │
│    (NÃO avalia respostas nem presume satisfação)              │
└──────────────────────────────────────────────────────────────┘
                         │ QuestionAnalysis
                         ▼
┌──────────────────────────────────────────────────────────────┐
│ 2. PropositionDiscourseFilter                                │
│    Classifica o gênero discursivo e extrai proposições       │
│    (NÃO decide classe final nem descarta relatos a priori)   │
└──────────────────────────────────────────────────────────────┘
                         │ tuple[FilteredProposition, ...]
                         ▼
┌──────────────────────────────────────────────────────────────┐
│ 3. MorphologicalCircularityAnalyzer                          │
│    Avalia ganho informacional e detecta tautologias          │
│    (NÃO usa sobreposição léxica como autoridade final)       │
└──────────────────────────────────────────────────────────────┘
                         │ CircularityEvaluation
                         ▼
┌──────────────────────────────────────────────────────────────┐
│ 4. DemandPropositionNexusBipartiteMatcher                    │
│    Mapeia 1-para-1 ou M-para-N nexos entre demandas e props │
│    (NÃO aceita palavras isoladas como prova de nexo)         │
└──────────────────────────────────────────────────────────────┘
                         │ tuple[DemandNexusResult, ...]
                         ▼
┌──────────────────────────────────────────────────────────────┐
│ 5. StrictOntologyRelevanceAggregator                         │
│    ÚNICO responsável pela classificação final canônica       │
│    (NÃO inventa evidências nem ignora demandas não cobertas) │
└──────────────────────────────────────────────────────────────┘
                         │
                         ▼
Saída Canônica: EvaluationResult (JSON estruturado e auditável)
```

---

## 2. Contrato 1: `SemanticIntentAndDemandExtractor`

### 2.1 Responsabilidade Única
Interpretar a intenção semântica da pergunta e extrair todas as demandas operacionais primárias, aspectos obrigatórios, restrições e relações de dependência, preservando o escopo semântico mesmo em orações simples sem conjunções explícitas.

### 2.2 Assinatura e Tipos de Dados
```python
def extract_demands(question_text: str) -> QuestionAnalysis:
    ...

@dataclass(frozen=True)
class SemanticDemand:
    demand_id: str                      # Identificador único ('demand_1', 'demand_2', ...)
    demand_type: str                    # 'PRIMARY_MECHANISM' | 'FAILURE_HANDLER' | 'STATE_TRANSITION' | 'COMPARISON'
    target_concept: str                 # Conceito nuclear (ex: 'circuit_breaker', 'two_phase_commit')
    required_aspects: tuple[str, ...]   # Aspectos funcionais obrigatórios (ex: ('fechado', 'aberto', 'meio-aberto'))
    is_mandatory: bool                  # True para aspectos essenciais; False para extensões opcionais
    dependency_on: Optional[str]        # ID da demanda da qual esta depende (ex: 'demand_1')
    raw_clause: str                     # Trecho textual correspondente na pergunta

@dataclass(frozen=True)
class QuestionAnalysis:
    intent_type: str                    # 'MECHANISM' | 'DIAGNOSIS' | 'DEFINITION' | 'COMPARISON' | 'EXPERIENCE'
    central_entities: tuple[str, ...]   # Tecnologias mencionadas (ex: ('Redis', 'Kafka'))
    demands: tuple[SemanticDemand, ...] # Lista imutável de demandas
    decomposition_confidence: str       # 'HIGH' | 'MEDIUM' | 'LOW'
    ambiguities: tuple[str, ...]        # Ambiguidades ou elipses detectadas
```

### 2.3 Invariantes Obrigatórios
1. **Preservação de Aspectos de Estado:** Perguntas que mencionam múltiplos estados funcionais (ex: "fechado, aberto e meio-aberto") DEVEM conter todos os estados em `required_aspects`, gerando subdemandas atômicas ou uma demanda de transição composta com 3 aspectos obrigatórios.
2. **Decomposição de Ação e Compensação:** Perguntas com coordenação de ações distintas (ex: "coordena transações locais e executa compensações") DEVEM gerar 2 demandas distintas (`demand_1` para coordenação, `demand_2` para compensações).
3. **Isolamento de Julgamento:** Este componente NÃO pode avaliar o texto da resposta, NÃO pode classificar e NÃO pode presumir se uma demanda foi atendida.

---

## 3. Contrato 2: `PropositionDiscourseFilter`

### 3.1 Responsabilidade Única
Segmentar a resposta em proposições técnicas e classificar o **gênero discursivo** e a postura pragmática de cada segmento. Não descarta relatos pessoais ou dados biográficos de forma cega, mas contextualiza seu papel discursivo ANTES que qualquer regra atribua operatividade técnica.

### 3.2 Assinatura e Tipos de Dados
```python
def filter_propositions(
    response_text: str, 
    analysis: QuestionAnalysis
) -> tuple[FilteredProposition, ...]:
    ...

@dataclass(frozen=True)
class FilteredProposition:
    proposition_id: str
    raw_text: str
    discourse_genre: str       # 'OPERATIVE_SOLUTION' | 'PERSONAL_DECLARATION' | 'HISTORICAL_TRIVIA' |
                               # 'MONITORING_AUXILIARY' | 'DESTRUCTIVE_ANTITHESIS' | 'EVASIVE_FILLER' | 
                               # 'EXPLICIT_IGNORANCE' | 'CONCEPTUAL_DEFINITION'
    is_operative: bool         # True SOMENTE se fornecer mecanismo técnico executável
    action_verb: str           # Lema normalizado do verbo (ex: 'indexar', 'particionar')
    mechanism_payload: str     # Núcleo explicativo
    preventative_context: bool # True se explicar por que evitar uma ação destrutiva
    confidence: str            # 'HIGH' | 'MEDIUM' | 'LOW'
    traceable_tokens: tuple[str, ...]
```

### 3.3 Invariantes Obrigatórios
1. **Desqualificação de Relato Autobiográfico como Mecanismo Interno:** Frases declarando tempo de uso ou familiaridade (ex: "já usei o Redis em diversos projetos", "nossa equipe sobe pods diariamente") recebem `discourse_genre = 'PERSONAL_DECLARATION'` e `is_operative = False`, a menos que a intenção da pergunta seja explicitamente de experiência (`intent_type == 'EXPERIENCE'`).
2. **Desqualificação de Fatos Biográficos / Institucionais:** Informações sobre fundadores, datas ou empresas criadoras (ex: "NGINX foi escrito por Igor Sysoev", "modelo relacional formalizado por Codd") recebem `discourse_genre = 'HISTORICAL_TRIVIA'` e `is_operative = False`.
3. **Imunidade de Verbos em Discursos Não-Operativos:** Verbos técnicos de ação ("fazer cache", "subir pods", "escrever código") contidos em proposições biográficas ou autobiográficas NÃO podem ativar `is_operative = True`.
4. **Isolamento:** O componente NÃO pode decidir a classe final da resposta.

---

## 4. Contrato 3: `MorphologicalCircularityAnalyzer`

### 4.1 Responsabilidade Única
Avaliar o ganho informacional substantivo da resposta em relação à pergunta através de um grafo léxico-morfológico unificado (lematização e famílias de cognatas), detectando tautologias, raciocínios circulares e repetições vazias, imune a variações entre classes gramaticais (ex: substantivo vs. verbo).

### 4.2 Assinatura e Tipos de Dados
```python
def analyze_circularity(
    question_text: str, 
    demands: tuple[SemanticDemand, ...], 
    propositions: tuple[FilteredProposition, ...]
) -> CircularityEvaluation:
    ...

@dataclass(frozen=True)
class CircularityEvaluation:
    is_circular_tautology: bool         # True se o predicado apenas reformular a pergunta
    informational_gain_score: float     # Grau de conteúdo novo (0.0 a 1.0)
    shared_cognate_families: tuple[str, ...] # Famílias morfológicas repetidas
    external_mechanisms_found: tuple[str, ...] # Mecanismos técnicos concretos não presentes na pergunta
    uncertainty: str                    # 'CONFIDENT' | 'BORDERLINE' | 'INDETERMINATE'
    rationale: str
```

### 4.3 Invariantes Obrigatórios
1. **Unificação de Raízes Cognatas:** O analisador trata substantivos e verbos da mesma família como equivalentes léxicos de base:
   - `replicação` ↔ `replicar` ↔ `réplicas` (raiz unificada: `replic-`)
   - `compressão` ↔ `comprimir` ↔ `comprimido` (raiz unificada: `comprim-` / `compress-`)
   - `travamento` ↔ `travar` ↔ `travas` (raiz unificada: `trav-`)
   - `índice` ↔ `indexar` ↔ `indexação` (raiz unificada: `indic-` / `index-`)
2. **Incompetência de Conectivos para Gerar Ganho Informacional:** A mera presença de conectivos causais ("porque", "para que", "de forma que", "mantém") ou termos genéricos de computação ("servidores", "dados") NÃO é suficiente para configurar ganho informacional positivo.
3. **Preservação de Incerteza:** Casos limítrofes onde há dúvida se a explicação é uma simplificação didática ou uma tautologia pura devem receber `uncertainty = 'BORDERLINE'` e não forçar `is_circular_tautology = True`.
4. **Isolamento:** Não utiliza sobreposição léxica como autoridade final para determinar `OFF_TOPIC` ou `DIRECT`.

---

## 5. Contrato 4: `DemandPropositionNexusBipartiteMatcher`

### 5.1 Responsabilidade Única
Emparelhar as demandas essenciais da pergunta com as proposições operativas da resposta através de validação bipartida (1-para-1 ou M-para-N explícito), determinando com precisão quais aspectos foram integralmente resolvidos, parcialmente resolvidos, sustentados como telemetria auxiliar ou não atendidos.

### 5.2 Assinatura e Tipos de Dados
```python
def match_demand_nexus(
    demands: tuple[SemanticDemand, ...],
    propositions: tuple[FilteredProposition, ...],
    circularity: CircularityEvaluation
) -> tuple[DemandNexusResult, ...]:
    ...

@dataclass(frozen=True)
class DemandNexusResult:
    demand_id: str
    satisfaction_degree: str  # 'FULL' | 'PARTIAL' | 'AUXILIARY_ONLY' | 'UNMET'
    matched_proposition_ids: tuple[str, ...] # IDs das proposições que sustentam a decisão
    nexus_relation: str       # 'FUNCTIONALLY_SOLVES' | 'PARTIALLY_SOLVES' | 'CONTRIBUTES_TO' |
                              # 'THEMATICALLY_ADJACENT' | 'DOMAIN_DISJUNCT' | 'ANTITHESIS_OPPOSED'
    aspects_covered: tuple[str, ...]    # Aspectos da demanda comprovadamente satisfeitos
    aspects_missing: tuple[str, ...]    # Aspectos da demanda que foram omitidos
    rationale: str
```

### 5.3 Invariantes Obrigatórios
1. **Proibição de Satisfação Difusa por Palavra Isolada:** A presença de um termo coincidente (ex: a palavra "coordenador") no texto de uma proposição voltada para a demanda $D_1$ NÃO pode satisfazer automaticamente uma demanda independente $D_2$ ("o que ocorre se o coordenador falhar?"). A demanda $D_2$ exige evidência de mecanismo específico de falha/recuperação.
2. **Justificativa Explícita para Múltipla Satisfação:** Uma mesma proposição operativa $P_1$ só pode satisfazer mais de uma demanda ($D_1$ e $D_2$) se $P_1$ contiver explicitamente a unificação causal demonstrada no texto (ex: "o algoritmo CRUSH elimina a necessidade de metadados centralizados calculando a localização diretamente via hash").
3. **Detecção de Omissão Parcial:** Se uma demanda $D_1$ contiver 3 aspectos obrigatórios (ex: fechado, aberto, meio-aberto) e a resposta cobrir apenas 2, `satisfaction_degree` DEVE ser `PARTIAL` e `aspects_missing` DEVE conter o estado faltante.

---

## 6. Contrato 5: `StrictOntologyRelevanceAggregator`

### 6.1 Responsabilidade Única
Atuar como a **única fonte de verdade** para a emissão da classificação final entre as 7 classes canônicas, integrando a matriz de nexo, o gênero discursivo e a avaliação de circularidade, gerando uma trilha de decisão explicável e determinística.

### 6.2 Assinatura e Tipos de Dados
```python
def aggregate_relevance(
    analysis: QuestionAnalysis,
    propositions: tuple[FilteredProposition, ...],
    circularity: CircularityEvaluation,
    nexus_results: tuple[DemandNexusResult, ...]
) -> EvaluationResult:
    ...

@dataclass(frozen=True)
class EvaluationResult:
    classification: str                 # 'DIRECT' | 'PARTIAL' | 'SUPPORTING' | 'RELATED' | 
                                        # 'OFF_TOPIC' | 'INSUFFICIENT' | 'UNKNOWN'
    functional_contribution: bool       # True se contribui substantivamente para a solução
    demand_coverage_status: str         # 'FULL' | 'PARTIAL' | 'SUPPORTING_ONLY' | 'RELATED_ONLY' | 'NONE' | 'UNKNOWN'
    demand_coverage_ratio: float        # Cobertura numérica (0.0 a 1.0)
    determinant_evidence: tuple[str, ...] # Principais evidências que determinaram a classe
    demands_solved: tuple[str, ...]
    demands_unmet: tuple[str, ...]
    residual_uncertainty: str           # 'LOW' | 'MEDIUM' | 'HIGH'
    decision_trail: tuple[str, ...]     # Sequência reproduzível de regras disparadas
```

### 6.3 Regras de Decisão Ontológica e Resolução de Conflitos
1. **Regra de Evasão (Resolução de CR-04):** Respostas evasivas ou preenchimentos genéricos ("depende do caso", "cada caso é um caso") são mapeadas estritamente para **`INSUFFICIENT`**, nunca para `UNKNOWN`.
2. **Regra de Tautologia (Resolução de CR-03):** Se `circularity.is_circular_tautology == True`, a classificação DEVE ser **`UNKNOWN`** (raciocínio circular sem ganho informacional).
3. **Regra de Antítese Destrutiva:** Se qualquer proposição for classificada como `DESTRUCTIVE_ANTITHESIS` (sem contexto preventivo), a classificação DEVE ser **`OFF_TOPIC`**.
4. **Regra de `DIRECT` Estrito:** `DIRECT` exige cumulativamente:
   - 100% das demandas primárias com `satisfaction_degree == 'FULL'`;
   - Zero aspectos obrigatórios em `aspects_missing`;
   - `discourse_genre == 'OPERATIVE_SOLUTION'`.
5. **Regra de `PARTIAL`:** Se $\ge 1$ aspecto obrigatório for satisfeito, mas $< 100\%$ das demandas/aspectos obrigatórios forem atendidos, a classificação DEVE ser **`PARTIAL`**.
6. **Regra de `SUPPORTING`:** Respostas focadas exclusivamente em telemetria, instrumentação ou métricas auxiliares que não solucionam a demanda principal recebem **`SUPPORTING`**.
7. **Regra de `RELATED`:** Respostas contendo metadados históricos, biografias ou declarações de experiência sem mecanismo operativo recebem **`RELATED`**.

---

## 7. Propagação de Incerteza e Resolução de Conflitos

| Cenário de Conflito | Componente com Autoridade | Decisão Arquitetural | Justificativa |
|---|---|---|---|
| Proposição contém verbo técnico, mas está em relato autobiográfico | `PropositionDiscourseFilter` | `is_operative = False` | Gênero discursivo prevalece sobre presença isolada de verbos. |
| Pergunta tem aspectos múltiplos, mas resposta parece completa | `SemanticIntentAndDemandExtractor` | Exigir todos os aspectos | Intenção da pergunta define a régua de completude. |
| Resposta parece circular, mas menciona um termo técnico novo | `MorphologicalCircularityAnalyzer` | `uncertainty = 'BORDERLINE'` | Preserva incerteza; não força falso positivo de tautologia. |
| Resposta evasiva vs. incerteza epistêmica | `StrictOntologyRelevanceAggregator` | Evasão -> `INSUFFICIENT`; Desconhecimento -> `INSUFFICIENT`; Tautologia -> `UNKNOWN` | Diferenciação formal da ontologia canônica. |
