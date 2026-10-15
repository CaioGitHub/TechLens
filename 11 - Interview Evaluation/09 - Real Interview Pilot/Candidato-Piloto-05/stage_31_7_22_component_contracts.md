---
type: architecture
status: study
confidence: 95
created: 2026-10-14
updated: 2026-10-14
tags:
  - stage-31-7-22
  - component-contracts
  - semantic-pipeline
  - specification
---

# Stage 31.7.22 — Especificação dos Contratos de Componentes (Cycle 4)

## 1. Visão Geral do Pipeline Proposto

Para sanar as causas-raiz identificadas (CR-01 a CR-08) sem reintroduzir heurísticas lexicais ad hoc, a arquitetura do motor de relevância semântica é estruturada em um pipeline linear de 5 componentes especializados:

```text
Entrada: (question_text, response_text)
                  │
                  ▼
┌────────────────────────────────────────────────────────┐
│ 1. SemanticIntentAndDemandExtractor                    │  --> Resolve CR-01 & CR-06
│    Decomposição profunda de demandas multi-aspecto      │
└────────────────────────────────────────────────────────┘
                  │ tuple[SemanticDemand, ...]
                  ▼
┌────────────────────────────────────────────────────────┐
│ 2. PropositionDiscourseFilter                          │  --> Resolve CR-02 & CR-05 & CR-08
│    Classificação de discurso (biográfico, operante)    │
└────────────────────────────────────────────────────────┘
                  │ tuple[FilteredProposition, ...]
                  ▼
┌────────────────────────────────────────────────────────┐
│ 3. MorphologicalCircularityAnalyzer                    │  --> Resolve CR-03
│    Cálculo de ganho informacional e tautologia         │
└────────────────────────────────────────────────────────┘
                  │ CircularityEvaluation
                  ▼
┌────────────────────────────────────────────────────────┐
│ 4. DemandPropositionNexusBipartiteMatcher              │  --> Resolve CR-01, CR-06 & CR-07
│    Emparelhamento bipartido 1-para-1 demanda/proposição │
└────────────────────────────────────────────────────────┘
                  │ tuple[DemandNexusResult, ...]
                  ▼
┌────────────────────────────────────────────────────────┐
│ 5. StrictOntologyRelevanceAggregator                   │  --> Resolve CR-04 & Agregação
│    Mapeamento determinístico para as 7 classes         │
└────────────────────────────────────────────────────────┘
                  │
                  ▼
Saída: EvaluationResult (JSON compatível com runtime)
```

---

## 2. Contrato 1: `SemanticIntentAndDemandExtractor`

### Propósito
Interpretar a intenção da pergunta e extrair todas as demandas operacionais primárias e secundárias, independentemente de haver conjunções interrogativas explícitas ("e como", "e qual"), reconhecendo transições de múltiplos estados, pares de ação/compensação e requisitos de mecanismo/efeito.

### Contrato de Entrada
```python
question_text: str  # Enunciado integral da pergunta sem truncamento
```

### Contrato de Saída
```python
@dataclass(frozen=True)
class SemanticDemand:
    demand_id: str                      # Identificador único (ex: 'demand_1', 'demand_2')
    demand_type: str                    # 'PRIMARY_MECHANISM' | 'FAILURE_HANDLER' | 'STATE_TRANSITION' | 'COMPARISON'
    target_concept: str                 # Entidade ou conceito nuclear (ex: 'circuit_breaker', 'saga')
    required_aspects: tuple[str, ...]   # Aspectos mínimos (ex: ('fechado', 'aberto', 'meio-aberto'))
    raw_clause: str                     # Oração fonte na pergunta

@dataclass(frozen=True)
class QuestionAnalysis:
    intent_type: str                    # 'MECHANISM' | 'DIAGNOSIS' | 'DEFINITION' | 'COMPARISON'
    central_entities: tuple[str, ...]   # Tecnologias identificadas
    demands: tuple[SemanticDemand, ...] # Lista ordenada e imutável de demandas
```

### Invariantes
1. Se a pergunta mencionar 3 estados funcionais essenciais (ex: fechado, aberto, meio-aberto), `required_aspects` DEVE conter os 3 estados, gerando uma demanda de transição completa ou múltiplas sub-demandas atômicas.
2. Nenhuma demanda primária pode ser descartada ou fundida com outra sem preservar a lista completa de aspectos exigidos.
3. Se a pergunta consistir em uma única frase simples com verbos coordenados (ex: "coordena X e executa compensações"), o parser DEVE gerar 2 demandas funcionais distintas.

### Relação com Causas-Raiz
- **CR-01:** Elimina o colapso de perguntas compostas de oração simples em uma única demanda genérica.

---

## 3. Contrato 2: `PropositionDiscourseFilter`

### Propósito
Classificar o gênero discursivo e a postura pragmática de cada segmento da resposta ANTES de atribuir qualquer operatividade técnica. Fatos biográficos, anedotas históricas de criadores, especificações de hardware descontextualizadas e declarações puramente autobiográficas de uso de ferramentas são desqualificadas terminantemente de atuarem como "soluções funcionais".

### Contrato de Entrada
```python
response_text: str
question_entities: tuple[str, ...]
```

### Contrato de Saída
```python
@dataclass(frozen=True)
class FilteredProposition:
    proposition_id: str
    raw_text: str
    discourse_genre: str       # 'OPERATIVE_SOLUTION' | 'HISTORICAL_TRIVIA' | 'PERSONAL_DECLARATION' | 
                               # 'MONITORING_TELEMETRY' | 'DESTRUCTIVE_ANTITHESIS' | 'EVASIVE_FILLER' | 'IGNORANCE'
    is_operative: bool         # True SOMENTE se discourse_genre == 'OPERATIVE_SOLUTION'
    action_verb: str           # Lema normalizado do verbo principal (ex: 'indexar', 'particionar')
    mechanism_payload: str     # Núcleo explicativo substantivo
    preventative_context: bool # True se a proposição alerta/previne contra um risco
```

### Invariantes
1. Frases iniciadas ou dominadas por marcadores de relato pessoal sem explicação técnica detalhada (ex: "já usei", "na nossa empresa nós utilizamos", "nossa equipe sobe pods diariamente") DEVEM receber `discourse_genre = 'PERSONAL_DECLARATION'` e `is_operative = False`.
2. Frases biográficas sobre criadores ou história de produtos (ex: "foi escrito por Igor Sysoev no início dos anos 2000", "formalizado por Edgar Codd na IBM") DEVEM receber `discourse_genre = 'HISTORICAL_TRIVIA'` e `is_operative = False`.
3. Verbos de ação técnicos contidos em segmentos biográficos ou autobiográficos NÃO podem ativar `is_operative = True`.

### Relação com Causas-Raiz
- **CR-02 & CR-05:** Elimina os 11 falsos `DIRECT` gerados a partir de `RELATED` e `SUPPORTING`.

---

## 4. Contrato 3: `MorphologicalCircularityAnalyzer`

### Propósito
Calcular o ganho informacional real da resposta em relação à pergunta através de um grafo léxico-morfológico normalizado (lemas e raízes cognatas unificadas), identificando tautologias, raciocínios circulares e poliptotos vazios, imune a variações entre classes gramaticais (ex: verbo "comprimir" vs. substantivo "compressão").

### Contrato de Entrada
```python
question_text: str
propositions: tuple[FilteredProposition, ...]
```

### Contrato de Saída
```python
@dataclass(frozen=True)
class CircularityEvaluation:
    is_circular_tautology: bool     # True se o predicado apenas reformular a pergunta
    informational_gain_score: float # Grau de novidade explicativa (0.0 a 1.0)
    external_mechanisms_found: tuple[str, ...] # Mecanismos técnicos concretos não presentes na pergunta
    rationale: str
```

### Invariantes
1. Palavras cognatas entre classes gramaticais (ex: `replicação` ↔ `replicar`, `compressão` ↔ `comprimir`, `travamento` ↔ `travar`, `índice` ↔ `indexar`) são tratadas como tokens idênticos de base.
2. A presença de conectivos funcionais ("mantém", "para", "de forma que") ou plurais genéricos ("servidores", "vários lugares") NÃO constitui ganho informacional na ausência de mecanismos técnicos externos explícitos.
3. Se `external_mechanisms_found` for vazio e o predicado consistir em repetição de lemas da pergunta sob conectivos causais, `is_circular_tautology` DEVE ser `True`.

### Relação com Causas-Raiz
- **CR-03:** Elimina os 6 casos de `UNKNOWN` tautológico que foram promovidos a `DIRECT`.

---

## 5. Contrato 4: `DemandPropositionNexusBipartiteMatcher`

### Propósito
Realizar o casamento e a validação do nexo funcional entre as demandas essenciais da pergunta e as proposições operativas da resposta através de um modelo de emparelhamento bipartido. Garante que uma proposição simples não possa satisfazer simultaneamente duas demandas independentes (ex: explicar replicação de log no Raft não satisfaz a sincronização de seguidores com log divergente).

### Contrato de Entrada
```python
demands: tuple[SemanticDemand, ...]
propositions: tuple[FilteredProposition, ...]
circularity: CircularityEvaluation
```

### Contrato de Saída
```python
@dataclass(frozen=True)
class DemandNexusResult:
    demand_id: str
    satisfied: bool
    satisfaction_degree: str  # 'FULL' | 'PARTIAL' | 'AUXILIARY_ONLY' | 'UNMET'
    matched_proposition_id: Optional[str]
    nexus_relation: str       # 'FUNCTIONALLY_SOLVES' | 'PARTIALLY_SOLVES' | 'CONTRIBUTES_TO' | 
                              # 'THEMATICALLY_ADJACENT' | 'DOMAIN_DISJUNCT' | 'ANTITHESIS_OPPOSED'
    rationale: str
```

### Invariantes
1. Cada demanda primária independente DEVE ser respaldada por evidência substantiva específica. A correspondência de uma palavra isolada (ex: "coordenador") no texto não permite marcar uma segunda demanda ("o que ocorre se o coordenador falhar") como `FUNCTIONALLY_SOLVES`.
2. Se uma resposta contiver apenas uma proposição operativa que atende a uma demanda $D_1$, e uma demanda $D_2$ não possuir proposição comprobatória associada, $D_2$ DEVE receber `satisfaction_degree = 'UNMET'`.

### Relação com Causas-Raiz
- **CR-01 & CR-06:** Impede a sobre-promoção de respostas parciais para `DIRECT` em perguntas multi-aspecto.
- **CR-07:** Assegura que construções coloquiais ou na voz passiva de ações perigosas sejam emparelhadas com `ANTITHESIS_OPPOSED`.

---

## 6. Contrato 5: `StrictOntologyRelevanceAggregator`

### Propósito
Agregador final e determinístico, atuando como **única fonte de verdade** para atribuir a classificação final entre as 7 classes canônicas, calculando a cobertura consolidada e assegurando a consistência terminológica entre `INSUFFICIENT` e `UNKNOWN`.

### Contrato de Entrada
```python
analysis: QuestionAnalysis
propositions: tuple[FilteredProposition, ...]
circularity: CircularityEvaluation
nexus_results: tuple[DemandNexusResult, ...]
```

### Regras Formais de Agregação Ontológica

| Condição Lógica Estrita | Classe Canônica | Justificativa Operacional |
|---|:---:|---|
| `circularity.is_circular_tautology == True` | `UNKNOWN` | Raciocínio circular sem valor de verdade determinável |
| Proposição expressa ignorância / desconhecimento explícito | `INSUFFICIENT` | Candidato não ofereceu evidência técnica para avaliação |
| Proposição evasiva ("depende do caso", consultoria vaga) | `INSUFFICIENT` | Lógica formal: falta de substância técnica avaliável |
| Qualquer nexo == `DOMAIN_DISJUNCT` ou `ANTITHESIS_OPPOSED` | `OFF_TOPIC` | Resposta fora do domínio ou ação que viola proteções |
| 100% das demandas possuem `FULL` satisfaction | `DIRECT` | Satisfação integral comprovada de todos os aspectos |
| $\ge 1$ demanda `FULL` ou `PARTIAL`, mas $< 100\%$ das demandas | `PARTIAL` | Resposta satisfaz parte substantiva, mas omite outro aspecto primário |
| Nenhuma demanda resolvida, mas $\ge 1$ nexo `CONTRIBUTES_TO` | `SUPPORTING` | Contribuição auxiliar de monitoramento/telemetria |
| Nenhuma demanda resolvida, mas contexto temático presente | `RELATED` | Adjacência temática, metadados ou relato de experiência |
| Nenhuma evidência técnica, sem menção de entidade nem contexto | `OFF_TOPIC` | Disjunção completa de conteúdo |

### Invariantes
1. Nenhuma resposta com evasão genérica ("depende do caso") pode receber `UNKNOWN`. Seu destino canônico é estritamente `INSUFFICIENT`.
2. Uma resposta classificada como `DIRECT` DEVE ter `aspect_coverage.ratio == 1.0` e todas as demandas primárias com `FUNCTIONALLY_SOLVES`.
3. Fatos puramente biográficos ou históricos nunca podem gerar score $\ge 0.5$ nem classe `SUPPORTING`/`DIRECT`. Seu teto ontológico é `RELATED`.

### Relação com Causas-Raiz
- **CR-04:** Corrige os 11 falsos `UNKNOWN` do Grupo F, direcionando-os para `INSUFFICIENT`.
- **CR-01 & CR-06:** Garante que a conjunção de demandas exija 100% de cobertura funcional para conceder `DIRECT`.

---

## 7. Critérios Observáveis de Aceitação

A conformidade com estes contratos será verificada por testes de contrato unitários isolados para cada componente, validando casos positivos, negativos e de fronteira antes da homologação final do motor integrado.
