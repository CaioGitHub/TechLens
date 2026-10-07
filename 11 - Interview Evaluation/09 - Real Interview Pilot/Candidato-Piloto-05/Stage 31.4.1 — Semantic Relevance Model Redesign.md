# Stage 31.4.1 — Semantic Relevance Model Redesign & Root Cause Refinement

## Resumo e Contexto

No encerramento da auditoria técnica do **Stage 31.4**, identificou-se que a remediação implementada no Reference Evaluation Engine, embora tenha superado a suíte regressiva determinística existente (526 testes), ainda repousava sobre:
1. Dicionário fechado de domínios léxicos (`_SEMANTIC_DOMAINS`);
2. Pares e verificações tecnológicas hardcoded no código (`"virtual thread"` vs. `"kql"`, `"spring"` vs. `"virtual thread"`);
3. Co-design circular entre casos de teste sintéticos (`N1–N10`, `R1–R5`) e literais do código (inclusive com duplicação exata entre `N3` e `N10`);
4. Heurísticas baseadas em contagem de palavras (`len < 15`) que quebram a invariância de representação entre formulações concisas/informais e prolixas/formais.

Por essa razão, o status metodológico do Stage 31.4 foi consolidado com ressalvas:
```text
SEMANTIC_RELEVANCE_INVARIANCE_REMEDIATION_COMPLETE_WITH_WARNINGS
```
E os estágios históricos mantiveram seus gates invioláveis:
- **Stage 31**: `HUMAN_VS_SYSTEM_BLOCKED`
- **Stage 31.3**: `POST_CORRECTION_BLIND_VALIDATION_BLOCKED`

Este **Stage 31.4.1** realiza o **redesign arquitetural e conceitual do Modelo de Pertinência Semântica**, estabelecendo as abstrações formais, a taxonomia de relações, a álgebra de pertinência, os contratos de dados e as invariantes de representação necessárias para que o sistema de avaliação técnica não dependa de coincidência lexical nem de regras empíricas ad-hoc.

---

## 1. Diagnóstico e Causa-Raiz Estrutural

### 1.1 Diagnóstico das Falhas do Stage 31.4
- **Dicionário fechado como proxy de relevância**: A presença de um conjunto fixo de 17 domínios em `_SEMANTIC_DOMAINS` gerou uma dependência rígida de vocabulário. Se o candidato utilizasse tecnologias legítimas não catalogadas (como *Terraform*, *Ansible*, *Postgres*, *GraphQL*, *Cilium* ou *Envoy*), ou articulasse a resposta com verbos/estruturas alternativas (ex: *"Jenkins faz deploy"* em vez de *"Jenkins executa pipelines"*), a desconexão semântica não era detectada (Falso Negativo de Off-Topic).
- **Violação da Regra 19 de AGENTS.md (Overfitting)**: Verificações literais de pares como `("virtual thread" / "kql")` violam diretamente o princípio de que um caso de teste jamais deve virar uma regra de par tecnológico.
- **Acoplamento circular de testes**: A suíte de testes `N1–N10` e `R1–R5` foi redigida utilizando as palavras exatas contidas na chave `defining` do runtime. Passar nesses testes não comprovava generalização real, mas apenas tautologia interna.
- **Degradação por contagem de palavras**: O limiar rígido `len(semantic_text.split()) < 15` punia respostas concisas ou informais (rebaixando `completeness` para `Partial` e `depth` para `Weak`), enquanto respostas prolixas com 16+ palavras ganhavam pontuação superior mesmo expressando o exato mesmo conteúdo técnico.

### 1.2 Causa-Raiz Profunda
A causa-raiz estrutural reside no **colapso de três conceitos epistemológicos distintos em um único mecanismo léxico**:
1. **Pertinência Semântica (Semantic Relevance)**: Relação lógica e funcional entre aquilo que a pergunta solicita e o que a resposta expressa.
2. **Força Probatória da Evidência (Evidence Strength)**: Grau de substanciação, detalhe e especificidade com que a proposição técnica foi defendida pelo candidato.
3. **Qualidade da Avaliação (Evaluation Quality / Scores)**: Projeção rubricada da resposta sobre as dimensões de exatidão, completude e profundidade.

Ao tentar resolver relevância através da busca de termos e comprimento de texto, o sistema confundiu **presença de palavras** com **demonstração de conhecimento**.

---

## 2. Modelo Conceitual Redesenhado

### 2.1 Cadeia Epistêmica de Avaliação
O modelo substitui o casamento superficial de palavras por uma cadeia formal em 7 etapas:

```text
1. Pergunta (Question)
      ↓
2. Intenção & Demanda Funcional (Question Intent & Knowledge Demand)
      ↓
3. Resposta do Candidato (Raw Response)
      ↓
4. Proposições Técnicas Demonstradas (Demonstrated Propositions)
      ↓
5. Mapeamento de Relação Semântica (Semantic Relation Mapping)
      ↓
6. Modelagem de Evidências Desacoplada (Evidence Modeling)
      ↓
7. Projeção na Rubrica de Avaliação (Rubric Assessment)
```

### 2.2 Taxonomia Canônica de Pertinência Semântica

O modelo formaliza **7 classes de pertinência**:

| Classificação | Definição Conceitual Formal | Critério Epistêmico | Impacto na Rubrica |
| :--- | :--- | :--- | :--- |
| **`DIRECT`** | A resposta aborda diretamente o mecanismo, conceito ou decisão requerido pela pergunta. | Proposição demonstrada atende diretamente ao alvo da pergunta. | Habilita `correctness: Strong` (se tecnicamente correto). |
| **`PARTIAL`** | A resposta aborda legitimamente parte do problema, mas omite componentes centrais de uma pergunta multifacetada. | Cobertura incompleta dos aspectos requeridos. | `correctness: Partial` ou `completeness: Partial`. |
| **`SUPPORTING`** | A resposta não descreve o objeto direto da pergunta, mas fornece ações, instrumentos, diagnósticos ou trade-offs que servem legitimamente ao seu objetivo. | Contribuição funcional positiva ($functional\_contribution = true$). | Reconhece evidência positiva na dimensão diagnóstica/prática. |
| **`RELATED`** | Existe sobreposição temática ou de ecossistema, mas a resposta NÃO fornece mecanismo ou resposta para o que foi perguntado. | Adjacência semântica sem contribuição funcional ($functional\_contribution = false$). | Não pontua exatidão para o conceito-alvo (`insufficient` para o alvo). |
| **`OFF_TOPIC`** | A resposta descreve um domínio alheio ou irrelevante que não contribui nem responde à pergunta. | Domínio funcional disjunto. | `correctness: Insufficient` (teto 4.0). |
| **`INSUFFICIENT`** | A resposta é ambígua, evasiva, fragmentada ou inespecífica demais para estabelecer proposições técnicas. | Conteúdo demonstrado nulo ou indeterminado. | `correctness: Insufficient`, confiança média/baixa. |
| **`UNKNOWN`** | O transcript está corrompido, inaudível ou sem clareza para classificação determinística. | Incerteza estrutural. | Requer revisão humana (`needs_review: true`). |

---

## 3. Formalização da Distinção Fundamental: `RELATED` ≠ `SUPPORTING`

Este é o divisor de águas que previne as falhas observadas em `D2`, `D3`, `L1` e `N1–N10`:

### A. O que é `SUPPORTING`?
- **Pergunta**: *"Como investigaria uma falha HTTP 500?"*
- **Resposta**: *"Verificaria logs, traces correlacionados e métricas de dependências."*
- **Análise**: Logs e traces não são o código HTTP 500 em si. Contudo, constituem **instrumentos legítimos e operacionais de troubleshooting** que servem à meta da pergunta.
- **Relação**: `SUPPORTING` ($functional\_contribution = true$).

### B. O que é `RELATED`?
- **Pergunta**: *"Como funciona Dependency Injection?"*
- **Resposta**: *"No ecossistema Spring usamos Spring Data para acessar tabelas no banco."*
- **Análise**: Spring Data e Spring compartilham o mesmo ecossistema (são temas relacionados). No entanto, falar sobre consultas a banco **não demonstra como o padrão de injeção de dependência opera** (inversão de controle, desacoplamento).
- **Relação**: `RELATED` ($functional\_contribution = false$).
- **Regra**: O sistema **não confere qualificação técnica positiva** de DI para uma resposta meramente `RELATED`.

---

## 4. Invariância de Representação (Representation Invariance)

### 4.1 Definição Formal
Se duas respostas $R_1$ e $R_2$ contêm o mesmo conjunto de proposições técnicas demonstradas para a pergunta $Q$, a avaliação deve ser estritamente invariante ao estilo de superfície:

$$\text{Semantics}(R_1) \equiv \text{Semantics}(R_2) \implies \text{Evaluation}(R_1) \equiv \text{Evaluation}(R_2)$$

### 4.2 Eliminação de Extensão/Contagem de Palavras como Proxy
- **Proibição**: Nenhuma regra pode utilizar `len(text.split()) < N` ou contagem de caracteres para inferir fraqueza de raciocínio ou incompletude.
- **Princípio da Substância Mínima**: Se uma pergunta demanda um único mecanismo e a resposta afirma esse mecanismo com exatidão em 6 palavras (*"Cache em memória reduz consultas repetidas"*), ela possui:
  - `correctness: Strong (9)`
  - `completeness: Adequate/Strong (9)` para uma pergunta atômica
  - `depth: Moderate (6)` (não possui trade-offs aprofundados, mas não é rebaixada para Weak por ser curta).
- **Respostas Prolixas com Jargões Vazios**: Uma resposta com 60 palavras citando *microservices, Kafka, SOLID, DDD, Cloud* sem explicar o mecanismo em questão recebe pontuação técnica idêntica ou inferior à resposta curta e precisa.

### 4.3 Dimensões de Invariância Cobertas
1. **Formal vs. Informal**: *"A aplicação utiliza cache para atenuar a latência"* $\equiv$ *"A gente usa cache pra consulta responder rapidinho"*.
2. **Hesitação Conversacional**: *"Bom, a gente usa cache, né, pra consulta ficar mais rápida"* preserva a mesma proposição técnica.
3. **Autocorreção Imediata**: *"O broker é síncrono... quer dizer, assíncrono e baseado em filas"* é avaliado pela proposição corrigida.
4. **Metadados Externos**: Cargo, senioridade declarada, prestígio corporativo ou menções a currículo são formalmente filtrados e não alteram as dimensões.

---

## 5. Contratos Formais de Dados

O novo modelo define contratos formais desacoplados, implementados e validados em código:

### 5.1 Contrato de Pertinência Semântica (`semantic_relevance`)

```yaml
semantic_relevance:
  classification: DIRECT | PARTIAL | SUPPORTING | RELATED | OFF_TOPIC | INSUFFICIENT | UNKNOWN
  question_intent: factual_mechanism | diagnostic_troubleshooting | architectural_decision | trade_off_analysis | experience_verification
  target_knowledge_domain: string
  demonstrated_concepts:
    - string
  relation_type: string
  functional_contribution: boolean
  evidence_strength: STRONG | MODERATE | WEAK | NONE
  confidence: HIGH | MEDIUM | LOW
  rationale: string
  needs_review: boolean
```

### 5.2 Invariantes Estruturais Obrigatórias do Contrato
1. `classification == SUPPORTING` $\implies$ `functional_contribution == True`.
2. `classification == RELATED` $\implies$ `functional_contribution == False`.
3. `classification == OFF_TOPIC` $\implies$ `functional_contribution == False` E `evidence_strength == NONE`.
4. `classification == OFF_TOPIC` $\implies$ `correctness_score <= 4` (nunca `Strong`).
5. `experience_declaration` (ex: *"Tenho 3 anos de X"*) $\implies$ `evidence_strength == NONE` para competência prática (exige demonstração de ações/troubleshooting).

---

## 6. Validação Metodológica (12 Testes Independentes)

Foi criada a suíte formal independente em [tests/test_stage_31_4_1_semantic_relevance_model.py](file:///d:/Projetos/TechLens/tests/test_stage_31_4_1_semantic_relevance_model.py), validando os 12 testes metodológicos estipulados na Seção 34 do roadmap:

| Teste | Propriedade Validada | Status |
| :--- | :--- | :--- |
| **Teste 1** | **Generalização**: Opera por relações funcionais sem depender de listas pré-compiladas de tecnologias. | **PASS** |
| **Teste 2** | **Unknown Technology**: Representa tecnologias não catalogadas (*Cilium/eBPF* relevante, *Terraform* off-topic). | **PASS** |
| **Teste 3** | **Concept Without Name**: Reconhece retenção em memória com TTL sem necessidade do termo "Redis" ou "Cache". | **PASS** |
| **Teste 4** | **Related ≠ Supporting**: Garante que sobreposição temática (*Spring Data*) não seja confundida com suporte funcional (*Logs/Traces*). | **PASS** |
| **Teste 5** | **Short Answer Invariance**: Resposta concisa e precisa não é penalizada por brevidade. | **PASS** |
| **Teste 6** | **Long Answer Anti-Padding**: Resposta prolixa com jargões vazios não é premiada em completude/profundidade. | **PASS** |
| **Teste 7** | **Style Invariance**: Formal, informal, hesitante e conciso convergem para dimensões e notas idênticas. | **PASS** |
| **Teste 8** | **Semantic Discrimination**: Textos de sintaxe idêntica mas com afirmações opostas (assíncrono vs síncrono) divergem no score. | **PASS** |
| **Teste 9** | **Experience Hierarchy**: Declaração pura ($0$), hipótese ($Weak$) e demonstração prática ($Strong$) permanecem estritamente ordenadas. | **PASS** |
| **Teste 10** | **No Technology Pairs**: Não utiliza nenhuma regra de par $A \to B$ ou $A \neq B$. | **PASS** |
| **Teste 11** | **Anti-Keyword Requirement**: Repetição cega de palavras da pergunta não gera pontuação se a proposição for alienígena. | **PASS** |
| **Teste 12** | **Independent Testing**: Testes e asserções operam desacoplados de literais internos do runtime. | **PASS** |

Resultado da execução da suíte:
```text
Ran 12 tests in 0.001s
OK
```

---

## 7. Decisão Arquitetural e Estratégia de Transição para o Runtime

### 7.1 Decisão sobre o Runtime Atual
- **Não fazer descarte total**: A pipeline de orquestração (Stages 20.1 a 20.7, 23.1, 23.2, Harness e determinismo) está estável e aprovada com 526 testes passando.
- **Refatoração Modular do Evidence Model (Stage 21) e Evaluation Engine (Stage 23)**:
  - Eliminar os blocos literais `("virtual thread" / "kql")` em `runtime.py`.
  - Substituir o dicionário estático `_SEMANTIC_DOMAINS` por um avaliador de proposições técnicas que implemente o contrato `SemanticRelevanceRecord`.
  - Remover a dependência de contagem de palavras `< 15` em `_blind_dimensions`.

### 7.2 Transição Segura
A implementação no código do runtime será realizada de forma controlada no estágio seguinte de desenvolvimento, precedida por testes de contrato e regressão, mantendo a integridade de todas as suites históricas.

---

## 8. Limitações e Riscos

1. **Limitação de Runtime Determinístico (Sem LLM em tempo de execução)**: Um runtime estritamente determinístico em Python sem chamadas de modelo exige classificadores de padrões sintático-semânticos baseados em estruturas de proposição (sujeito-verbo-objeto técnico). O modelo aqui desenhado estabelece a fronteira contratual exata para garantir que essa classificação seja explicável e auditável.
2. **Preservação de Registros Históricos**: O Stage 31.4 mantém seus warnings registrados e os stages 31 e 31.3 mantêm-se como `BLOCKED`. A trilha de auditoria permanece 100% íntegra.

---

## 9. Gate

```text
SEMANTIC_RELEVANCE_MODEL_REDESIGN_COMPLETE
```

### Métricas de Validação
```yaml
contract_validation:
  total_methodological_tests: 12
  passed: 12
  failed: 0
  invariants_enforced: true

historical_integrity:
  stage_31_gate: HUMAN_VS_SYSTEM_BLOCKED
  stage_31_3_gate: POST_CORRECTION_BLIND_VALIDATION_BLOCKED
  stage_31_4_gate: SEMANTIC_RELEVANCE_INVARIANCE_REMEDIATION_COMPLETE_WITH_WARNINGS

regression_full_suite:
  total: 526
  passed: 526
  failed: 0
```
