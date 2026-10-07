# Stage 31.6 — Controlled Correction of Semantic Relevance Model

**Status:** Concluído  
**Data:** 2026-10-07  
**Gate:** `CONTROLLED_CORRECTION_COMPLETE`  
**Referência Metodológica:** `AGENTS.md`, `SECOND_BRAIN.md`, `GEMINI_GUARDRAILS.md`, `GEMINI_HANDOFF.md`, Stage 31.5  

---

## 1. Resumo Executivo

O **Stage 31.6** realizou a **correção controlada e estrutural** das três falhas fundamentais identificadas durante a revalidação cega e independente do Stage 31.5 (`POST_REMEDIATION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED`):

1. **Causa A (Word-Count Proxy Residual):** Uso residual de contagem de palavras (`len(r_words_list) <= 6`, `len <= 3`, `short = len < 15`, `multi_aspect_short`) para inferir cobertura de demandas e suficiência de respostas.
2. **Causa B (Matching Lexical Rígido sem Normalização Morfológica Geral):** Dependência de interseção exata de strings (`q_words & r_words`) gerando falsos negativos em domínio aberto para flexões verbais, plurais e variações lexicais em português/inglês técnico.
3. **Causa C (Colisão de Substrings e Delimitação Lexical Frouxa):** Matching via substring (`d_term in q_lower`), causando falsas capturas semânticas como `"orm"` dentro de `"performance"`, `"bus"` em `"business"` ou `"orquestração"` geral de workflows capturada indevidamente por orquestração de containers.

Todas as três causas foram corrigidas **sem a criação de regras ad-hoc por tecnologia, sem tabelas de pares tecnológicos e sem otimização direta de scores**. A causalidade estrutural foi comprovada por suíte dedicada com 35 testes (incluindo testes de mutação deliberada, testes de colisão lexical, invariância linguística, tecnologias desconhecidas, conceitos abertos, determinismo e isolamento), com 100% de sucesso na regressão global (716/716 PASS) e no Reference Harness (8/8 suites PASS_WITH_WARNINGS).

---

## 2. Root Cause Analysis (Achados do Stage 31.5)

| Falha Identificada | Mecanismo Defeituoso no Runtime | Sintoma / Efeito Adverso |
| :--- | :--- | :--- |
| **Causa A: Proxy por contagem de palavras** | `len(r_words_list) <= 6` em perguntas multi-aspecto e `short = len(tokens) < 15` na rubrica de completude. | Respostas curtas de alta precisão (ex.: *"Usaria backoff exponencial com jitter e circuit breaker."* - 8 palavras) eram rebaixadas arbitrariamente para `PARTIAL`, enquanto respostas prolixas com conteúdo irrelevante eram promovidas. |
| **Causa B: Rigidez morfológica lexical** | `q_words & r_words` comparando termos literais sem stripping de sufixos ou normalização de acentos. | Falhas de domínio aberto quando uma pergunta utilizava *"correlacionar"* e a resposta *"fazer a correlação"*, ou *"retry"* vs *"repetições"*, gerando falso `OFF_TOPIC`. |
| **Causa C: Substring matching em tokens curtos** | `any(term in text)` sem verificação de limites de palavra (`\b`). | Termo curto como `"orm"` colidia dentro de `"performance"`; `"bus"` dentro de `"business"`; `"api"` dentro de `"apicultura"`; `"orquestração"` de workflows colidia com container orchestration. |

---

## 3. Modificações Estruturais Implementadas

### 3.1. Eliminação Integral de Word-Count Proxies (Causa A)
- **Remoção de todas as heurísticas de tamanho:** Foram expurgados do runtime de avaliação:
  - `len(r_words_list) <= 6`
  - `len(r_words_list) <= 3`
  - `multi_aspect_short`
  - `short = len(tokens) < 15`
- **Cobertura Propositional Multi-Aspecto (`_evaluate_multi_aspect_coverage`):**
  - Perguntas multi-aspecto têm suas demandas funcionais decompostas por marcadores gramaticais explícitos (`" e como "`, `" e qual seu "`, `" e suas "`, etc.).
  - A cobertura é avaliada verificando se proposições técnicas na resposta satisfazem independentemente as demandas de cada aspecto (`Aspect 1 -> Satisfied`, `Aspect 2 -> Satisfied/Omitted`).
  - Respostas curtas que cobrem todas as proposições essenciais recebem `DIRECT` independentemente de terem 5, 8 ou 50 palavras.
  - Respostas longas que cobrem apenas um aspecto recebem `PARTIAL` justificando explicitamente o aspecto omitido via `omitted_summary`.

### 3.2. Camada Geral de Normalização Linguística e Stemming (Causa B)
- **Normalização Unicode Geral (`_normalize_text`):**
  - Aplicação de decomposição canônica NFD (`unicodedata.normalize('NFD', ...)`), removendo diacríticos de forma puramente algorítmica, unificando acentos gráficos em português.
- **Stemmer Morfológico Algorítmico (`_stem_word`):**
  - Implementado algoritmo determinístico de redução de sufixos flexionais para o português (verbais, nominais, plurais e aumentativos/diminutivos) e estrangeirismos técnicos em inglês (`-ies -> -y`, `-ing`):
    - Redução verbal: `-acionar`, `-icionar`, `-amento`, `-imento`, `-aria`, `-ariamos`, `-ando`, `-endo`, `-indo`, `-amos`, `-emos`, `-imos`, `-aram`, `-eram`, `-iram`.
    - Redução nominal/adjetival: `-acao`, `-acoes`, `-icao`, `-icoes`, `-sao`, `-soes`, `-encia`, `-encias`, `-avel`, `-aveis`, `-ivel`, `-iveis`.
    - Normalização de gênero e número: flexões `-a`/`-o` e desinência de plural `-s`.
  - **Zero Closed Vocabulary:** Não foram criadas listas de pares de palavras (`correlacionar -> correlação` não é dicionário; ambas são reduzidas algorítmicamente para a raiz `correl`).

### 3.3. Delimitação Estrita de Palavras e Token Boundary Matching (Causa C)
- **Substituição de Substring por Word Boundaries (`_lexical_contains`):**
  - Termos simples são verificados estritamente via boundary regex (`r"\b" + re.escape(term) + r"\b"`) sobre o texto normalizado, ou por igualdade de stems entre tokens independentes.
  - Termos compostos são verificados com boundary delimitado para a locução inteira (`r"\b" + r"\s+".join(...) + r"\b"`).
  - Colisões como `"orm"` dentro de `"performance"` tornam-se matematicamente impossíveis.
  - Desambiguação de demandas globais: `"orquestração de containers"` substituiu o termo solto `"orquestração"`, prevenindo falsos positivos em orquestração de workflows distribuídos (Temporal, Airflow, Cadence).

---

## 4. Áreas do Runtime Afetadas

| Arquivo | Componente / Função | Natureza da Alteração |
| :--- | :--- | :--- |
| `reference_runtime/runtime.py` | `_normalize_text` | Adição de normalização Unicode NFD algorítmica. |
| `reference_runtime/runtime.py` | `_stem_word` | Implementação de stemmer sufixal para flexões do português e termos técnicos. |
| `reference_runtime/runtime.py` | `_extract_stemmed_tokens` | Extração de conjunto de stems semânticos limpos de stop words gerais. |
| `reference_runtime/runtime.py` | `_lexical_contains` | Substituição de `term in text` por boundary regex `\b` e equivalência morfológica por stem. |
| `reference_runtime/runtime.py` | `_evaluate_multi_aspect_coverage` | Derivação composicional de aspectos sem word-count proxy. |
| `reference_runtime/runtime.py` | `_FUNCTIONAL_CAPABILITIES` | Disambiguação de container orchestration e inclusão de demandas abertas para padrões arquiteturais e de resiliência. |
| `reference_runtime/runtime.py` | `_blind_dimensions` | Propagação de omissão parcial estruturada (`partial_aspect_omission`) sem corte arbitrário por contagem de palavras. |

---

## 5. Impacto no Modelo Semântico

O pipeline de avaliação preserva sua hierarquia canônica estrita:

```text
Question
   ↓
Demand / Intent Analysis (Factual / Architectural / Diagnostic / Experience)
   ↓
Response
   ↓
Technical Propositions Extraction (Stems & Semantic Boundary Match)
   ↓
Proposition → Demand Multi-Aspect Coverage Derivation
   ↓
Relevance Classification (DIRECT / PARTIAL / SUPPORTING / RELATED / OFF_TOPIC / INSUFFICIENT)
   ↓
Evidence Strength & Epistemic Attribution (demonstrated_experience vs declaration vs hypothesis)
   ↓
Rubric Evaluation (Completude baseada em Proposições, não em palavras)
```

1. **Invariância de Representação:** Respostas concisas e formuladas diretamente têm garantia de equivalência semântica com respostas prolixas.
2. **Robustez Epistêmica:** Declarações de experiência isoladas (*"Trabalhei 3 anos com X"*) permanecem categorizadas estritamente como `experience_declaration` com completude `Insufficient`, sem pontuação conceitual indevida.
3. **Generalização em Domínio Aberto:** Tecnologias nunca mapeadas em repositórios internos (ex.: *Temporal, NATS, ScyllaDB, ClickHouse, Keycloak, Traefik*) são classificadas com precisão diretamente pelo alinhamento de proposições técnicas com as demandas das perguntas.

---

## 6. Resultados da Suíte de Testes Estruturais (Stage 31.6)

Arquivo: `tests/test_stage_31_6_controlled_correction.py`  
Total de Testes: **35**  
Resultado: **35 PASS, 0 FAIL (100% OK)**  

### 6.1. Cobertura Multi-Aspecto sem Word Count (Seção 19)
- `test_01_short_answer_covering_all_aspects_is_direct`: Resposta curta (8 palavras) cobrindo todos os aspectos é `DIRECT` (não rebaixada por tamanho).
- `test_02_long_answer_covering_only_one_aspect_remains_partial`: Resposta longa (>30 palavras) cobrindo apenas um aspecto permanece `PARTIAL` (não promovida por tamanho).
- `test_03_medium_answer_covering_initial_aspect_omitting_secondary`: Resposta cobrindo aspecto inicial mas omitindo secundário é `PARTIAL`.
- `test_04_long_answer_irrelevant_is_off_topic`: Resposta longa com enchimento irrelevante permanece `OFF_TOPIC`.
- `test_05_multiple_propositions_covering_multiple_demands`: Resposta com proposições cobrindo múltiplas demandas é `DIRECT`.
- `test_06_oauth_refresh_token_omission_is_partial`: Omissão de refresh token em query OAuth é `PARTIAL`.

### 6.2. Invariância Linguística e Morfológica (Seção 20)
- `test_invariance_correlacionar_and_correlacao`: Variações de flexão de *"correlacionar"* (*"correlacionar"*, *"fazer a correlação"*, *"correlacionando"*, *"correlacionou"*) recebem classificação idêntica (`SUPPORTING`, contribuição funcional `True`).
- `test_retry_repeticao_plural_inflections`: Plurais e singulares (*"retries e repetições"* vs *"retry e repetição"*) reduzem para os mesmos stems (`retry`, `repet`).
- `test_general_portuguese_conjugations`: Normalização correta de conjugações verbais e substantivos (*"atualizações"*, *"atualização"*, *"atualizamos"*, *"configurações"*).

### 6.3. Prevenção de Colisões Lexicais por Token Boundary (Seção 21)
- `test_orm_does_not_collide_with_performance`: *"performance"* não colide com *"orm"*.
- `test_api_does_not_collide_with_apicultura`: *"apicultura"* não colide com *"api"*.
- `test_bus_does_not_collide_with_business`: *"business"* não colide com *"bus"*.
- `test_cache_matches_cached_but_not_unrelated`: *"cache"* combina com *"cached"* sem colisão espúria.
- `test_log_does_not_collide_with_login`: *"login"* não colide com *"log"*.
- `test_trace_does_not_collide_with_traceroute_if_distinct`: Limites lexicais preservados.
- `test_sincrono_does_not_collide_with_assincrono`: *"síncrono"* combina com *"síncrona"*, mas não com *"assíncrono"*.

### 6.4. Tecnologias Desconhecidas em Domínio Aberto (Seção 22)
- `test_unknown_tech_clickhouse_columnar`: ClickHouse e execução vetorizada classificados como `DIRECT` sem cadastro prévio da tecnologia.
- `test_unknown_tech_keycloak_identity`: Keycloak e SSO federado classificados como `DIRECT`.
- `test_unknown_tech_traefik_reverse_proxy`: Traefik e roteamento dinâmico classificados como `DIRECT`.

### 6.5. Conceitos sem Nomes de Produtos Tecnológicos (Seção 23)
- `test_in_memory_caching_without_redis_name`: Caching em memória com TTL sem citar Redis classificado como `DIRECT`.
- `test_circuit_breaking_without_product_name`: Circuit breaking e fallback sem citar Resilience4j/Hystrix classificado como `SUPPORTING`.
- `test_eventual_consistency_without_product_name`: Consistência eventual com idempotência sem citar produtos classificado como `DIRECT`.

### 6.6. Discriminação Supporting vs Related (Seção 24)
- `test_troubleshooting_diagnostic_action_is_supporting`: Diagnóstico com correlação de logs e traces é `SUPPORTING` com contribuição funcional ativa.
- `test_ecosystem_adjacency_without_mechanism_is_related`: Spring Data em pergunta sobre DI é `RELATED` sem contribuição funcional.
- `test_adjacent_tools_without_diagnostic_action_is_related`: Swagger/OpenAPI em pergunta sobre REST sem explicação do mecanismo é `RELATED`.

### 6.7. Separação Epistêmica de Experiência (Seção 25)
- `test_declaration_only_produces_insufficient_qualification`: Declaração isolada gera `experience_declaration` com completude `Insufficient`.
- `test_hypothesis_produces_distinct_epistemic_evidence`: Hipótese gera `hypothesis_formulation`.
- `test_concrete_demonstration_produces_strong_evidence`: Demonstração concreta com decisões e trade-offs gera `demonstrated_experience` com completude `Strong`.

---

## 7. Testes de Mutação Deliberada (Seção 29)

Os testes de mutação comprovaram a causalidade direta entre proposições semânticas e os resultados de avaliação:

| Teste de Mutação | Ação da Mutação | Comportamento Observado | Causalidade Comprovada |
| :--- | :--- | :--- | :--- |
| **Mutação 1** | Remoção de proposição que cobria aspecto 2. | `DIRECT` converte-se estritamente em `PARTIAL`. | A cobertura depende da proposição técnica, não da existência da resposta. |
| **Mutação 2** | Adição de parágrafo irrelevante (padding de git/code review). | Resposta parcial com padding permanece `PARTIAL`. | O aumento da quantidade de palavras não inflaciona a cobertura. |
| **Mutação 3** | Substituição de termo por flexão morfológica equivalente (*"correlacionar"* -> *"fazer a correlação"*). | Classificação permanece `SUPPORTING` com contribuição `True`. | Invariância morfológica garantida. |
| **Mutação 4** | Substituição por palavra com substring comum (*"ORM"* -> *"performance"*). | `DIRECT` converte-se em não-direto. | Discriminação lexical preservada sem colisão de substring. |

---

## 8. Determinismo e Isolamento (Seções 30 e 31)

1. **Determinismo Estrito:** Três execuções sequenciais idênticas do pipeline completo produziram pontuações idênticas (`score1 == score2 == score3`) e dicionários dimensionais estritamente idênticos.
2. **Isolamento de Execução:** A execução de casos em ordens permutadas e aleatorizadas produziu resultados idênticos para cada caso, comprovando ausência de estado compartilhado ou vazamento entre entrevistas.

---

## 9. Regressão Global e Reference Harness

- **Regressão Global de Testes (`run_reference_runtime_tests.py`):**
  - **716 de 716 testes PASS (0 falhas, 0 bloqueios).**
  - Status: `PASS`.
- **Reference Harness (`run_reference_harness.py`):**
  - **8 de 8 suítes executadas com sucesso.**
  - Status: `PASS_WITH_WARNINGS` (conforme contratos canônicos dos estágios históricos).

---

## 10. Auditoria de Código e Ausência de Regras Ad-hoc (Seção 33)

Auditoria exaustiva realizada sobre o runtime confirmou:
1. **Nenhum word-count proxy residual:** Nenhuma ocorrência de `len(tokens)`, `split()` ou contagem de caracteres é utilizada no cálculo de relevância, completude ou evidência.
2. **Nenhuma nova regra de pares tecnológicos:** Não foram criadas listas de tecnologias proibidas ou pares específicos (*"Docker -> K8s"*, *"SQL -> Redis"*).
3. **Nenhum vocabulário fechado de flexões:** A equivalência linguística é provida pelo algoritmo morfológico determinístico (`_stem_word`) e normalização Unicode.
4. **Nenhum matching por substring em classificadores de domínio:** Substituído por `\b` boundary regex e casamento por stems no `_lexical_contains`.

---

## 11. Limitações Remanescentes

1. **Stemmer Baseado em Regras Sufixais:** O stemmer atende com alta precisão o português técnico e empréstimos do inglês, mas não substitui um lematizador morfológico formal para verbos irregulares de radical variável (*"fazer"* vs *"feito"*). Casos de irregularidade extrema devem continuar sendo avaliados pela semântica de proposição técnica.
2. **Validação Cega Humana Independente Necessária (Stage 31.7):** Em obediência estrita à Seção 36 das instruções do Stage 31.6, a revalidação comparativa contra a anotação humana não foi executada nesta etapa de correção. Essa revalidação deverá ser realizada em etapa cega dedicada subsequente (Stage 31.7).

---

## 12. Gate Final

Com base no cumprimento integral de todos os 15 critérios de sucesso definidos na Seção 34:

```text
GATE: CONTROLLED_CORRECTION_COMPLETE
```
