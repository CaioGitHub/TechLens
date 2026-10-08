# Stage 31.7.4 — Root Cause Analysis & Semantic Intent Generalization

**Status:** Concluído  
**Data:** 2026-10-08  
**Gate:** `ROOT_CAUSE_ANALYSIS_COMPLETE`  
**Referência Metodológica:** `AGENTS.md`, `SECOND_BRAIN.md`, `GEMINI_GUARDRAILS.md`, `GEMINI_HANDOFF.md`, Stage 31.7, Stage 31.7.1, Stage 31.7.2, Stage 31.7.3  

---

## Status

```text
GATE: ROOT_CAUSE_ANALYSIS_COMPLETE
```

A análise formal de causa-raiz (RCA) das **38 falhas estruturais** identificadas na revalidação cega do Stage 31.7.3 foi integralmente concluída. O runtime canônico (`reference_runtime/runtime.py`) permaneceu rigorosamente **congelado** durante toda a investigação, preservando os princípios metodológicos do projeto.

O diagnóstico revelou por que a tentativa de desacoplamento do Stage 31.7.2 manteve comportamento lexicalmente fechado: a implementação removeu a autoridade explícita de `_FUNCTIONAL_CAPABILITIES`, mas dispersou essa autoridade em uma cadeia de **blocos procedurais rígidos (mini-whitelists locais com cláusulas `else: return OFF_TOPIC`)**, manteve o catálogo residual como atalho eliminatório no Step 9 (gerando falsos positivos onde a entidade atuava como passe-livre para `DIRECT`), e delegou o fallback a um casador estrito de radicais léxicos (`shared_stems`).

Foi formulada a arquitetura de **Semantic Intent Generalization**, modelando a relação causal entre a Demanda Funcional da pergunta (`QuestionDemand`) e a Proposição Técnica da resposta (`TechnicalProposition`), eliminando qualquer dependência de listas fechadas, sinônimos ad-hoc ou proxies lexicais.

---

## Gate

```text
GATE: ROOT_CAUSE_ANALYSIS_COMPLETE
```

---

## Runtime Integrity

Em cumprimento estrito à Seção 2 do mandato (`NÃO MODIFICAR O RUNTIME`):

| Ponto de Verificação | Algoritmo | Hash SHA-256 Registrado | Integridade |
| :--- | :---: | :--- | :---: |
| **Entrada do Stage 31.7.4** | SHA-256 | `9B466EB010CD586E0BA8699CCE5529C52A3C28540969B7F8C17BD3CF0D4E0A44` | Base Congelada |
| **Saída do Stage 31.7.4** | SHA-256 | `9B466EB010CD586E0BA8699CCE5529C52A3C28540969B7F8C17BD3CF0D4E0A44` | **100% Inalterado** |

Zero bytes foram alterados no runtime de referência durante esta etapa investigativa.

---

## Summary of Stage 31.7.3

O Stage 31.7.3 executou uma validação cega independente composta por 92 casos de teste projetados para verificar generalização, independência de catálogo, robustez a gaps lexicais e separação epistêmica. O resultado foi:
- **Total de Casos**: 92
- **Aprovados (PASS)**: 54 (58.7%)
- **Falhas (FAIL)**: 38 (41.3%)
- **Gate Final**: `POST_DECOUPLING_BLIND_REVALIDATION_BLOCKED`

Embora tecnologias inéditas (10/10 PASS) e estabilidade métrica do candidato piloto (MAE = 0.64) tenham sido alcançadas, o sistema exibiu falhas categóricas quando submetido a formulações interrogativas alternativas, variações de extensão e conceitos técnicos livres expressos em português.

---

## 38 Failure Matrix

A tabela a seguir cataloga exaustivamente todas as 38 falhas registradas em [`tests/test_stage_31_7_3_post_decoupling_blind_revalidation.py`](file:///d:/Projetos/TechLens/tests/test_stage_31_7_3_post_decoupling_blind_revalidation.py):

| ID | Teste Específico | Classe | Sintoma Observado | Causa Imediata no Código | Causa Estrutural Sistêmica | Camada Afetada |
|---|---|:---:|---|---|---|:---:|
| **F01** | `test_contradictory_01_circuit_breaker` | Invariância | Resposta válida classificada como `OFF_TOPIC` | Pergunta usou "serviço externo" em vez de "dependência externa" | Padrão interrogativo literal rígido no Step 4 | Intent Extraction |
| **F02** | `test_entity_anchor_02_kubernetes` | Classe A | Menção factual "temos cluster..." vira `DIRECT` | Step 9 encontra `"cluster"` em `cap["valid"]` | Entidade atuando como passe-livre para `DIRECT` | Semantic Relation |
| **F03** | `test_entity_anchor_03_kafka` | Classe A | Menção a "plataforma adotada" vira `DIRECT` | Step 9 / Step 11 consideram entidade como asserção | Ausência de validação de mecanismo na resposta | Semantic Relation |
| **F04** | `test_entity_anchor_04_redis` | Classe A | "Instalei instância de Redis" vira `DIRECT` | Termo `"instância"` casa com whitelist do Step 9 | Palavras de infraestrutura tratadas como mecanismo | Semantic Relation |
| **F05** | `test_entity_anchor_05_spring` | Classe A | "Spring Boot é o framework padrão" vira `DIRECT` | Step 11 casa `"spring"` como asserção técnica aberta | Falta de filtro de adjacência passiva factual | Semantic Relation |
| **F06** | `test_entity_anchor_06_postgres` | Classe A | "Postgres é banco relacional padrão" vira `DIRECT` | Step 11 casa `"postgres"` sem checar se explicou MVCC | Atribuição de acerto por mera menção à ferramenta | Semantic Relation |
| **F07** | `test_entity_anchor_07_docker` | Classe A | "Gosto de rodar imagens Docker" vira `DIRECT` | Step 11 casa `"docker"` ignorando demanda de namespaces | Falso positivo por sobreposição do nome da ferramenta | Semantic Relation |
| **F08** | `test_entity_anchor_08_istio` | Classe A | "Instalou Istio recentemente" vira `DIRECT` | Step 11 casa `"istio"` sem checar roteamento de tráfego | Incapacidade de exigir proposição funcional ativa | Semantic Relation |
| **F09** | `test_entity_anchor_09_surrealdb` | Classe A | "SurrealDB foi desenvolvido em Rust" vira `DIRECT` | Step 8 casa `"surrealdb"` sem checar dados multi-modelo | Atributo factual de implementação tratado como resposta | Semantic Relation |
| **F10** | `test_entity_anchor_10_clickhouse` | Classe A | "Criado por engenheiros na Europa" vira `DIRECT` | Step 8 casa `"clickhouse"` sem checar ordenação esparsa | Fato biográfico tratado como proposição técnica | Semantic Relation |
| **F11** | `test_epistemic_04_experience_plus_demonstration` | Classe E | Perde qualificação `demonstrated_experience` | Linha 686 só adiciona se houver verbos da lista estrita | Separação incompleta entre semântica e epistemologia | Evidence Model |
| **F12** | `test_fn_02_indirect_causal_tracing` | Classe B | "IDs de correlação nos envelopes HTTP" vira `OFF_TOPIC` | Pergunta ("acompanhar caminho...") não casou padrão de tracing | Descontinuidade léxica entre pergunta informal e mecanismo | Intent Extraction |
| **F13** | `test_fn_03_concise_deadlock` | Classe B | "Travas em ordem hierárquica estrita" vira `OFF_TOPIC` | Pergunta ("impasses mútuos...") não usou palavra "deadlock" | Dependência de termo formal na pergunta interrogativa | Intent Extraction |
| **F14** | `test_fn_04_casual_concurrency` | Classe B | "Boto coluna de versão lá e vejo se ninguém mudou" vira `OFF_TOPIC` | Resposta informal não continha "timestamp" ou "contador" | Exigência de terminologia técnica padronizada | Proposition Matching |
| **F15** | `test_f04_multi_aspect_rest_and_pagination` | Classe D | Cobriu só REST e ganhou `DIRECT` | Segmentador de multi-aspecto falhou na conjunção natural | Quebra da pergunta dependente de conectivos fixos | Demand Modeling |
| **F16** | `test_f05_eventual_consistency_and_idempotency` | Classe D | Consistência eventual com mensageria rebaixada para `PARTIAL` | Mensageria tratada como alienígena ou aspecto incompleto | Penalização indevida de sinergia entre tópicos | Semantic Relation |
| **F17** | `test_lexical_gap_01_concurrency_lock_free` | Classe B | "Duas requisições sobrescrevendo alterações" vira `OFF_TOPIC` | Não casou `"sem travar a linha no banco"` do Contexto 4 | Padrão interrogativo literal rígido impediu ativação | Intent Extraction |
| **F18** | `test_lexical_gap_03_flow_correlation` | Classe B | "Acompanhar pedido por dezenas de instâncias" vira `OFF_TOPIC` | Não casou `"rastrear uma transação"` do Contexto 1 | Sequestro frasal de demanda interrogativa | Intent Extraction |
| **F19** | `test_lexical_gap_04_burst_throttling` | Classe B | "Conter disparos massivos de requisições" vira `OFF_TOPIC` | Não casou `"rajadas abusivas"` do Contexto 2 | Incapacidade de generalizar sinônimos funcionais | Intent Extraction |
| **F20** | `test_lexical_gap_05_latency_degradation` | Classe B | "Diagnosticar lentidão após atualizar versão" vira `OFF_TOPIC` | Não casou `"degradação de latência pós deploy"` | Regex de troubleshooting não disparou e caiu em OFF_TOPIC | Intent Extraction |
| **F21** | `test_lexical_gap_06_producer_consumer_imbalance` | Classe B | "Entrada de mensagens superando fila" vira `OFF_TOPIC` | Não casou `"produtor rápido consumidor sobrecarregado"` | Literalismo interrogativo em fluxo de controle | Intent Extraction |
| **F22** | `test_lexical_gap_08_thread_freeze` | Classe B | "Travamento com CPU em zero por cento" vira `OFF_TOPIC` | Não casou palavras de diagnóstico de threads | Ausência de mapeamento sintoma $\to$ diagnóstico | Intent Extraction |
| **F23** | `test_lexical_gap_09_resource_compartmentalization` | Classe B | "Esgotamento de conexões de um parceiro afetando outros" vira `OFF_TOPIC` | Não casou frase exata de isolamento por bulkhead | Ausência de generalização de problema de contenção | Intent Extraction |
| **F24** | `test_lexical_gap_10_cache_invalidation` | Classe B | "Evitar exibir dados desatualizados após atualização" vira `OFF_TOPIC` | Não casou termos de consistência eventual | Falha em mapear problema de staleness para invalidação | Intent Extraction |
| **F25** | `test_rest_and_pagination_aspect_1_only` | Classe D | Resposta cobriu só REST e ganhou `DIRECT` | `_decoupled_evaluate_multi_aspect_coverage` não detectou omissão | Regex de aspectos ignora demanda secundária | Demand Modeling |
| **F26** | `test_rest_and_pagination_aspect_2_only` | Classe D | Resposta cobriu só paginação e ganhou `DIRECT` | Sistema tratou paginação isolada como asserção direta | Falta de rastreamento de aspectos não cobertos | Demand Modeling |
| **F27** | `test_retry_and_rate_limiting_aspect_1_only` | Classe D | Resposta cobriu só retry e ganhou `DIRECT` | Sistema premiou menção isolada de backoff como resposta completa | Ausência de checagem estrita de conjunções de demanda | Demand Modeling |
| **F28** | `test_invariance_02_short_vs_long_occ` | Classe E | Explicação longa de OCC de 4 linhas ejetada para `OFF_TOPIC` | Não continha palavras literais `"timestamp"` ou `"contador"` | **Mini-whitelist eliminatória no bloco Contexto 4** | Proposition Matching |
| **F29** | `test_pair_01_http500_investigation` | Classe G | Resposta cita ecossistema e é ejetada para `OFF_TOPIC` em vez de `RELATED` | Fallback de troubleshooting marca como alienígena absoluto | Falta de taxonomia de adjacência de ecossistema | Semantic Relation |
| **F30** | `test_pair_02_resilience_fallback` | Classe G | Ação de fallback com cache e degradação vira `OFF_TOPIC` | Pergunta não usou palavras típicas de troubleshooting | Roteamento rígido de intenção impediu reconhecimento | Intent Extraction |
| **F31** | `test_pair_03_latency_investigation` | Classe G | Monitorar GC e pausas de JVM vira `OFF_TOPIC` | Ação de suporte não casou com palavras de métricas do catálogo | Falta de reconhecimento de ações de apoio diagnóstico | Semantic Relation |
| **F32** | `test_pair_04_thread_blocking_diagnosis` | Classe G | Citar servidor com 16 cores vira `OFF_TOPIC` em vez de `RELATED` | Ejeção prematura por ausência de ações de dump | Classificação de ecossistema não discriminada | Semantic Relation |
| **F33** | `test_pair_05_slow_query_optimization` | Classe G | Ação válida com EXPLAIN ANALYZE vira `OFF_TOPIC` | Pergunta ("otimizar consultas lentas") não ativou rota | Desconexão entre meta de performance e análise de plano | Intent Extraction |
| **F34** | `test_01_optimistic_concurrency` | Classe C | "Versionamento com checagem no commit" vira `OFF_TOPIC` | Pergunta ("sem bloqueio de linha") divergiu de "sem travar linha" | Fragilidade léxica em sinônimos de restrição | Intent Extraction |
| **F35** | `test_03_circuit_breaking` | Classe C | "Disjuntor que aciona resposta degradada" vira `OFF_TOPIC` | Termo em português "disjuntor" não constava na whitelist | Rejeição de português técnico conceitual | Proposition Matching |
| **F36** | `test_04_rate_limiting` | Classe C | "Algoritmo de balde de fichas" vira `OFF_TOPIC` | Termo em português "balde de fichas" ausente da whitelist | Rejeição de metáfora funcional legítima | Proposition Matching |
| **F37** | `test_05_graceful_degradation` | Classe C | "Desativar módulos e servir dados em cache" vira `OFF_TOPIC` | Proposição de degradação suave não mapeada | Ausência de modelo abstrato de resiliência | Proposition Matching |
| **F38** | `test_09_idempotency` | Classe C | "Chave exclusiva enviada na requisição" vira `OFF_TOPIC` | Expressão "chave exclusiva" divergiu de "idempotência" | Dependência de jargão comercial em vez da mecânica | Proposition Matching |

---

## Failure Clustering

O agrupamento analítico consolidou as 38 falhas em **6 clusters estruturais**:

```text
                       [38 Falhas Estruturais]
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
     Cluster 1                Cluster 2                Cluster 3
   Entidade como             Problema →               Vocabulário
    Passe-Livre              Mecanismo                  Fechado
    (9 falhas)              (11 falhas)               (5 falhas)
   [F02-F10]               [F12-F14, F17-F24]         [F34-F38]
         │                        │                        │
         ├────────────────────────┼────────────────────────┤
         ▼                        ▼                        ▼
     Cluster 4                Cluster 5                Cluster 6
   Supporting vs            Multi-Aspect              Invariância
      Related               Segmentation              & Epistêmica
    (5 falhas)               (5 falhas)               (3 falhas)
   [F29-F33]               [F15, F16, F25-F27]       [F01, F11, F28]
```

### Síntese dos Clusters:
1. **Cluster 1 — Entidade como Passe-Livre (9 falhas / 23.7%)**: O sistema premia qualquer frase factual sobre a ferramenta ("temos cluster", "instalamos", "escrito em Rust") como `DIRECT`.
2. **Cluster 2 — Fragilidade Léxica em Problema $\to$ Mecanismo (11 falhas / 28.9%)**: O casamento de intenção depende de strings literais na pergunta. Pequenas variações de fraseado ejetam a resposta para `OFF_TOPIC`.
3. **Cluster 3 — Vocabulário Fechado em Conceitos Sem Tecnologia (5 falhas / 13.2%)**: Conceitos em português técnico ("balde de fichas", "disjuntor", "chave exclusiva") são ejetados por falta dos termos equivalentes em inglês.
4. **Cluster 4 — Discriminação Falha de Supporting vs Related (5 falhas / 13.2%)**: Ações funcionais de suporte e menções a ecossistema adjacente são indistintamente tratadas como `OFF_TOPIC`.
5. **Cluster 5 — Fragmentação e Cobertura Multi-Aspecto (5 falhas / 13.2%)**: Conectivos naturais não são reconhecidos como delimitadores de demanda, gerando falso `DIRECT` para respostas que cobrem apenas metade da pergunta.
6. **Cluster 6 — Invariância de Extensão e Detecção Epistêmica (3 falhas / 7.8%)**: Respostas longas conceituais são penalizadas por não repetirem keywords específicas, e respostas mistas perdem anotações de experiência.

---

## Root Cause

A resposta à pergunta central da RCA (Seção 4) é inequívoca:

> **O Stage 31.7.2 não substituiu o modelo lexical fechado por um modelo de proposições semânticas; ele apenas descentralizou o catálogo fechado, fragmentando-o em mini-whitelists procedurais embutidas em blocos condicionais (`Context 1`, `Context 2`, etc.), cada qual com seu próprio `else: return OFF_TOPIC`.**

### Por que a semântica foi perdida?
Na cadeia:
```text
Question ──► Intent ──► Demand ──► Technical Proposition ──► Semantic Relation
```
A quebra ocorre em dois pontos fundamentais:

1. **Ruptura na Demanda (`Demand Extraction`)**:
   A demanda não é extraída gramatical ou funcionalmente da frase. O código faz `if "frase exata" in q_lower`. Se o entrevistador disser *"duas requisições sobrescrevendo alterações"* em vez de *"conflitos de escrita concorrente"*, a demanda **deixa de existir** para o sistema.
2. **Ruptura na Proposição (`Proposition Matching`)**:
   Em vez de analisar se o candidato descreveu uma *ação mecânica* (ex.: adicionar versionamento e abortar caso haja divergência), o código exige palavras isoladas obrigatórias (`"timestamp"`, `"contador"`). A explicação longa (F28) foi rejeitada exatamente porque articulou a mecânica perfeita em português formal sem usar as palavras pré-selecionadas.
3. **Bypass Não-Eliminatório Residual (Step 9)**:
   O catálogo `_FUNCTIONAL_CAPABILITIES` continuou executando um bypass positivo no Step 9: se a tecnologia constasse no catálogo e qualquer palavra de `cap["valid"]` (como `"cluster"`, `"instância"`, `"servidor"`) estivesse na resposta, o sistema emitia `DIRECT` imediatamente, sem validar se a resposta continha qualquer mecanismo funcional.

---

## Entity Anchor Analysis

A presença de uma entidade na pergunta e na resposta gera um forte viés cognitivo e computacional. A RCA estabelece formalmente a especificação do papel da entidade:

```yaml
entity_anchor:
  can:
    - identify_context
    - reduce_ambiguity
    - anchor_interpretation
    - establish_thematic_proximity

  cannot:
    - imply_direct_relevance
    - imply_correctness
    - imply_demonstrated_knowledge
    - imply_functional_mechanism
```

### Regra Operacional da Entidade:
```text
entity_match == True
     AND
mechanism_demonstrated == False
     ──► RELATED (thematic_adjacency_without_mechanism)
```
Nunca `DIRECT`. Se o candidato diz *"Temos Kubernetes na nuvem"*, a entidade identifica o contexto, mas a ausência de mecanismo relativo à pergunta (*readiness probe*) obriga a classificação `RELATED`.

---

## Problem → Mechanism Analysis

A relação entre um problema de engenharia de software e sua solução deve ser modelada como uma cadeia causal abstrata:

```text
[Functional Problem]
        │  (Ex.: duas escritas concorrentes sobre o mesmo recurso)
        ▼
[Desired Outcome]
        │  (Ex.: preservar consistência e integridade sem locks bloqueantes)
        ▼
[Causal Mechanism]
        │  (Ex.: validação de versão/estado pré-commit com aborto em divergência)
        ▼
[Functional Effect]
           (Ex.: prevenção atômica de lost update)
```

### Princípio de Independência Lexical:
A validação dessa cadeia não requer que o candidato e o entrevistador compartilhem radicais léxicos:
- Problema formulado como: *"duas pessoas alterando o mesmo dado ao mesmo tempo"*
- Mecanismo articulado como: *"coloco um campo que incrementa e checo antes de gravar"*
- **Relação Semântica**: `DIRECT`. O mecanismo resolve diretamente o problema causal sem nenhuma palavra em comum com a pergunta.

---

## Closed Vocabulary Analysis

O erro de classificar termos em português como `OFF_TOPIC` ("balde de fichas", "disjuntor", "chave exclusiva") decorre da crença implícita de que termos técnicos só existem sob seus equivalentes canônicos em inglês (*token bucket*, *circuit breaker*, *idempotency key*).

A RCA proíbe a resolução disso via lista de sinônimos ("dicionário de termos equivalentes"). A solução arquitetural correta é:
1. **Reconhecimento de Papel Funcional**: A expressão *"chave exclusiva enviada para rejeitar execuções redundantes já processadas"* descreve uma **proposição técnica de desduplicação idempotente**.
2. **Avaliação pelo Efeito Declarado**: Se a proposição declara um mecanismo (*chave única*) e um efeito (*rejeitar redundâncias*), ela cumpre a demanda de idempotência, independentemente do jargão comercial utilizado.

---

## Multi-Aspect Analysis

Perguntas multi-aspecto demandam a extração explícita de uma lista de demandas atômicas:

```yaml
demand:
  id: "DEMAND-01"
  functional_goal: "Expor recursos via protocolo semântico"
  required_aspect: "api_design_principles"
  constraints: ["HTTP", "verbos semânticos"]
  expected_relation: "DIRECT"
  provenance: "Como projetar uma API REST"

demand:
  id: "DEMAND-02"
  functional_goal: "Controlar volume de dados transferidos por página"
  required_aspect: "pagination_strategy"
  constraints: ["limit/offset", "cursor-based"]
  expected_relation: "DIRECT"
  provenance: "estruturar a paginação de recursos"
```

A cobertura deve ser calculada por:
```text
AspectCoverage = { d in Demands | exists p in Propositions : p satisfies d }
```
- Se `len(AspectCoverage) == len(Demands)` $\to$ `DIRECT`.
- Se `0 < len(AspectCoverage) < len(Demands)` $\to$ `PARTIAL`.
- Se `len(AspectCoverage) == 0` $\to$ `OFF_TOPIC` / `RELATED`.

Isso elimina qualquer dependência de conectivos literais (`" e como "`, `" e estruturar "`) ou contagem de palavras.

---

## Epistemic Separation

Semantic Relevance e Epistemic Status são dimensões ortogonais:

```text
Response Analysis
 ├── Semantic Relevance (O que foi abordado em relação à pergunta?)
 │    ├── DIRECT
 │    ├── PARTIAL
 │    ├── SUPPORTING
 │    ├── RELATED
 │    └── OFF_TOPIC
 │
 └── Epistemic Status (Qual a natureza e solidez da evidência?)
      ├── experience_declaration ("Trabalhei 3 anos com X")
      ├── demonstrated_experience ("Em produção, quando X caiu, reconfiguramos Y")
      ├── conceptual_assertion ("X opera dividindo o estado em shards")
      ├── hypothesis ("Eu começaria suspeitando que o pool saturou")
      └── conditional_reasoning ("Se a latência for alta, então aplicaria cache")
```

Uma resposta pode ter `semantic_relevance: DIRECT` e `epistemic_status: experience_declaration` quando o candidato responde à pergunta diretamente, mas sua evidência consiste apenas em declarar experiência pregressa sem demonstrar o mecanismo em detalhes.

---

## Lexical Gap Analysis

A similaridade léxica (`shared_words`, `shared_stems`) deve ser tratada como um **sinal de suporte contextual de baixa prioridade**, nunca como autoridade eliminatória:
- Se `lexical_overlap == 0`, mas a proposição técnica atende à demanda funcional $\to$ `DIRECT`.
- Se `lexical_overlap > 0`, mas a resposta é apenas repetição de palavras sem mecanismo $\to$ `RELATED` ou `OFF_TOPIC`.

O gap lexical é a norma em entrevistas de alto nível, onde candidatos explicam causas raízes e princípios sem repetir os termos formulados pelo entrevistador.

---

## Polysemy Analysis

Termos técnicos polissêmicos não podem determinar o domínio funcional isoladamente:

```text
Termo Polissêmico: "Transação"
 ├── Contexto A: "rastrear uma transação entre microsserviços"
 │    └── Domínio: Distributed Tracing / Context Propagation
 │
 ├── Contexto B: "garantir rollback de transação no banco"
 │    └── Domínio: Database ACID / Concurrency
 │
 └── Contexto C: "transação financeira com chave idempotente"
      └── Domínio: Idempotency & Business Workflow
```

A desambiguação deve ocorrer pela análise dos modificadores adjacentes e dos predicados verbais da frase (*rastrear entre serviços* vs *rollback no banco*).

---

## Technical Proposition Model

Especificação formal da estrutura de proposição técnica a ser extraída da fala do candidato:

```yaml
technical_proposition:
  proposition_text: str       # Trecho textual original
  subject: str                # Objeto ou componente técnico em discussão
  action: str                 # Verbo funcional ou operação realizada
  mechanism: str              # Mecanismo, algoritmo ou técnica empregada
  constraint: str             # Condição ou restrição operacional atendida
  effect: str                 # Resultado causal gerado pela operação
  causal_role: str            # primary_mechanism | diagnostic_action | supporting_pattern
  evidence_span: tuple[int, int]
  provenance: str
```

Essa modelagem transforma a resposta de um "bloco de texto com palavras" em uma "asserção de engenharia com causa e efeito".

---

## Question Demand Model

Especificação formal da estrutura de demanda a ser extraída da pergunta:

```yaml
question_demand:
  demand_id: str
  target_problem: str         # O problema concreto a ser resolvido
  expected_mechanism_type: str # concurrency | telemetry | resilience | api_design
  operational_constraints: list[str] # ["sem bloquear linha", "sem perder contexto"]
  is_composite: bool          # Indica se há múltiplos aspectos interdependentes
  aspect_goals: list[str]     # Lista de metas funcionais atômicas
```

---

## Semantic Relation Model

Definições formais das 7 relações semânticas do motor:

1. **`DIRECT`**: A resposta contém proposições técnicas que respondem de forma causal e suficiente à demanda funcional central da pergunta, demonstrando o mecanismo requerido.
2. **`PARTIAL`**: A resposta atende causalmente a uma ou mais demandas de uma pergunta multi-aspecto, mas omite outras demandas requeridas; ou mistura o mecanismo correto com conceitos disjuntos.
3. **`SUPPORTING`**: A proposição não constitui o mecanismo primário solicitado, mas descreve uma ação ou técnica que contribui funcional e comprovadamente para alcançar o objetivo (ex.: logs e tracing para apoiar investigação de 500).
4. **`RELATED`**: Existe adjacência temática ou menção a ferramentas do mesmo ecossistema, mas a resposta não articula mecanismos nem contribui funcionalmente para a demanda.
5. **`OFF_TOPIC`**: A resposta não possui relação funcional, causal ou temática defensável com o problema apresentado.
6. **`INSUFFICIENT`**: O candidato expressa falta de conhecimento ("não sei", "não lembro") ou a resposta é evasiva demais para inferir qualquer proposição técnica.
7. **`UNKNOWN`**: A estrutura da transcrição é fragmentada, ausente ou ambígua ao ponto de impedir uma classificação defensável, exigindo revisão humana (`needs_review: True`).

---

## Open Domain Requirements

O sistema deve operar em regime de **Domínio Aberto por Construção**:
1. A chegada de uma nova tecnologia (ex.: TiFlash, Redpanda, Nomad) não pode exigir novas linhas de código em listas de whitelists ou dicionários.
2. Se uma resposta articula sujeito, mecanismo e efeito coerentes com o objetivo da pergunta, ela deve ser reconhecida como `DIRECT` ou `SUPPORTING` pelo motor geral de proposições.
3. A taxonomia interna deve ser enriquecida a posteriori, nunca atuando como filtro eliminatório prévio.

---

## Representation Invariance

Para garantir que respostas com a mesma mecânica recebam a mesma classificação independente de estilo:
- **Respostas Curtas vs Longas**: A completude é dada pelo fechamento causal da proposição (sujeito + mecanismo + efeito), nunca pelo tamanho de tokens ou contagem de palavras.
- **Linguagem Formal vs Informal**: O motor deve buscar os papéis causais da ação e do efeito, ignorando a ausência de substantivos anglófonos eruditos.
- **Autocorreção e Hesitação**: Discursos que contêm hesitações ou correções ("eu usaria lock... quer dizer, versionamento") devem ter suas proposições finais avaliadas pela asserção consolidada.

---

## Proposed Architecture

O desenho arquitetural para a futura implementação (Stage 31.7.5) decompõe o processo de avaliação semântica em 5 estágios desacoplados:

```text
[Question Input]                                    [Response Input]
       │                                                   │
       ▼                                                   ▼
┌─────────────────────────┐                         ┌─────────────────────────┐
│ Stage 1: Demand Parser  │                         │ Stage 2: Proposition    │
│  - Target Problem       │                         │          Extractor      │
│  - Operational Bounds   │                         │  - Action & Mechanism   │
│  - Sub-Demands (Aspects)│                         │  - Declared Effects     │
└───────────┬─────────────┘                         └───────────┬─────────────┘
            │                                                   │
            └─────────────────────────┬─────────────────────────┘
                                      ▼
                        ┌───────────────────────────┐
                        │ Stage 3: Causal Relation  │
                        │          Matcher          │
                        │  - Does Mechanism resolve │
                        │    the Target Problem?    │
                        │  - Aspect Coverage Check  │
                        │  - Entity Anchor Weight   │
                        └─────────────┬─────────────┘
                                      ▼
                        ┌───────────────────────────┐
                        │ Stage 4: Semantic Status  │
                        │  - DIRECT / PARTIAL /     │
                        │    SUPPORTING / RELATED / │
                        │    OFF_TOPIC / UNKNOWN    │
                        └─────────────┬─────────────┘
                                      ▼
                        ┌───────────────────────────┐
                        │ Stage 5: Epistemic Split  │
                        │  - Experience Declaration │
                        │  - Demonstrated Mechanics │
                        │  - Hypothesis Formulation │
                        └───────────────────────────┘
```

---

## Architectural Invariants

As 10 invariantes obrigatórias para a futura implementação:

1. **Invariante 1 (Catálogo Proibido como Filtro)**: `_FUNCTIONAL_CAPABILITIES` não pode ter cláusulas de rejeição ou aprovação automática em decisões semânticas.
2. **Invariante 2 (Entidade sem Passe-Livre)**: `entity_match == True` nunca produz `DIRECT` sem proposição de mecanismo comprovada.
3. **Invariante 3 (Problema $\to$ Mecanismo Causal)**: Problemas funcionais e mecanismos devem ser casados pelo alinhamento causal do efeito pretendido, nunca por overlap lexical estrito.
4. **Invariante 4 (Independência de Vocabulário)**: Expressões funcionais legítimas em língua portuguesa têm a mesma validade de termos técnicos anglófonos.
5. **Invariante 5 (Multi-Aspect Independente de Conectivos)**: Demandas multi-aspecto são particionadas pela estrutura conceitual da pergunta, e a cobertura exige satisfação proposicional de cada sub-demanda.
6. **Invariante 6 (Separação Epistêmica Estrita)**: Relevância semântica e tipo de evidência epistêmica são campos independentes.
7. **Invariante 7 (Invariância de Extensão)**: Nenhuma decisão pode utilizar contagem de palavras, número de caracteres ou densidade de tokens como limiar de corte.
8. **Invariante 8 (Domínio Aberto Nativo)**: Novas tecnologias e conceitos devem ser avaliados com sucesso sem requerer cadastro prévio no runtime.
9. **Invariante 9 (Desambiguação Contextual de Polissemia)**: Tokens altamente polissêmicos (`transação`, `endpoint`, `telemetria`) têm seu domínio determinado pelos modificadores e predicados da frase.
10. **Invariante 10 (Determinismo e Rastreabilidade)**: A classificação deve ser 100% determinística e fornecer uma justificativa (`rationale`) causalmente verificável.

---

## Rejected Alternatives

1. **Expansão do Catálogo `_FUNCTIONAL_CAPABILITIES`**: Rejeitada porque manteria o sistema como um vocabulário fechado frágil e incapaz de generalizar.
2. **Criação de Dicionário Global de Sinônimos**: Rejeitada porque apenas trocaria um catálogo de tecnologias por um catálogo de termos, reproduzindo a mesma classe de falhas.
3. **Ajuste Fino de Thresholds Numéricos ou Word Counts**: Rejeitada porque contagem de palavras é um proxy superficial que pune respostas concisas e premia enrolação (*padding*).
4. **Uso de LLM Online no Runtime de Referência**: Rejeitada porque violaria os requisitos de determinismo, independência local, reprodutibilidade exata e custo zero do harness local.

---

## Required Future Tests

Para validar a implementação do Stage 31.7.5, a suíte de testes deverá conter:
- 10+ casos de tecnologias inéditas em domínios diversos.
- 10+ casos de conceitos sem nomes comerciais em português técnico legítimo.
- 10+ casos de problemas funcionais formulados sem jargões com respostas de zero overlap lexical.
- 10+ casos de entidades presentes em declarações factuais sem mecanismo (`RELATED`).
- 10+ pares de discriminação entre contribuição funcional (`SUPPORTING`) e ecossistema passivo (`RELATED`).
- 10+ perguntas multi-aspecto com variações de conjunção natural.
- Casos de invariância representacional (respostas curtas de 5 palavras vs longas de 50 palavras).
- Casos com significados opostos e contradições proposicionais.

---

## Risks

1. **Complexidade de Parsing Semântico Local**: Construir um extrator causal em Python puro sem dependências pesadas de NLP exige desenho cuidadoso para não reimplementar regexes frágeis.
2. **Risco de Regressão no Candidato Piloto**: Qualquer modificação no motor deve manter estritamente o alinhamento comprovado com a referência humana (MAE $\le 0.64$).

---

## Limitations

1. O motor de referência permanece operando sobre a língua portuguesa técnica; termos em outros idiomas além do inglês/português demandariam extensão gramatical.
2. Respostas truncadas ou com menos de 3 palavras sem verbo continuarão sendo conservadoramente marcadas como `UNKNOWN` ou `INSUFFICIENT`.

---

## Conclusion

A Root Cause Analysis do Stage 31.7.4 identificou formalmente por que o Stage 31.7.2 falhou: **o desacoplamento foi superficial, substituindo um catálogo estático por mini-whitelists procedurais embutidas**.

O desenho de Semantic Intent Generalization formulado nesta RCA estabelece as fundações para que o sistema reconheça relações funcionais e causais legítimas sem depender de vocabulário fechado, overlap de radicais ou nomes de produtos comerciais.

---

## Next Gate

```text
GATE: ROOT_CAUSE_ANALYSIS_COMPLETE
```

O próximo estágio canônico é o:
```text
Stage 31.7.5 — Controlled Implementation of Semantic Intent Generalization
```
onde a arquitetura proposta será implementada no runtime congelado, seguida de nova validação cega.
