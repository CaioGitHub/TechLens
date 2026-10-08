# Stage 31.7.9 — Blind Revalidation of Open-Domain Proposition Architecture

---

## 1. Objetivo
Executar a **primeira validação cega independente** da arquitetura Open-Domain Proposition & Semantic Relation implementada no Stage 31.7.8 sobre o runtime congelado, respondendo à pergunta fundamental:

> A nova arquitetura Open-Domain Proposition & Semantic Relation generaliza para casos novos, não utilizados durante sua implementação, sem depender de catálogo fechado, vocabulário conhecido, padrões lexicais ou conhecimento dos casos históricos?

Esta etapa é de **validação científica e auditoria de generalização**, não de desenvolvimento ou correção.

---

## 2. Gate de Entrada
- **Stage Anterior:** Stage 31.7.8 — Controlled Implementation of Open-Domain Proposition & Semantic Relation Architecture
- **Gate de Entrada:** `CONTROLLED_IMPLEMENTATION_COMPLETE_WITH_WARNINGS`
- **Condição Metodológica:** Runtime implementado de forma desacoplada, preservando baseline histórico e pronto para submissão a benchmark cego independente.

---

## 3. Runtime Hash & Congelamento Estrito
- **Arquivo Avaliado:** [reference_runtime/runtime.py](file:///d:/Projetos/TechLens/reference_runtime/runtime.py)
- **SHA-256 de Entrada (Stage 31.7.8):**
  `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
- **SHA-256 Verificado durante o Benchmark:**
  `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
- **SHA-256 Final (Conclusão do Stage 31.7.9):**
  `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
- **Status de Integridade:** `RUNTIME FROZEN (100% Inalterado)`. Nenhuma linha, heurística, peso, limiar ou lista de termos foi alterada no runtime durante a validação.

---

## 4. Metodologia Cega
Seguindo o protocolo estrito de blind validation (Seção 23 do `AGENTS.md` e Seção 5 do Stage 31.7.9):
1. O benchmark foi construído e anotado pelo oráculo humano independente **sem conhecimento prévio da classificação do sistema**.
2. A ordem de execução foi estritamente:
   $$Caso \to Pergunta \to Resposta \to Oráculo\ Humano \to Classificação\ do\ Sistema \to Comparação$$
3. O oráculo humano não foi ajustado retrospectivamente para convergir com o sistema.
4. O sistema não recebeu labels esperados durante a inferência.

---

## 5. Independência do Benchmark
Foi realizada auditoria de independência do conjunto de testes:
- **Zero overlapping** com os testes unitários de desenvolvimento ([tests/test_stage_31_7_8_open_domain_proposition_engine.py](file:///d:/Projetos/TechLens/tests/test_stage_31_7_8_open_domain_proposition_engine.py)).
- **Zero reutilização** dos casos de falha do Stage 31.7.6 ou Stage 31.7.7.
- Casos formulados de forma inédita, cobrindo novas tecnologias (reais e fictícias), cenários de concorrência, observabilidade, sistemas distribuídos, resiliência e traps linguísticas.

---

## 6. Composição dos Casos
O benchmark é composto por **242 casos independentes**, distribuídos em 16 categorias obrigatórias:

| Código | Categoria | Quantidade | Foco da Avaliação |
| :--- | :--- | :--- | :--- |
| **A** | `A_open_domain` | 18 | Tecnologias inéditas reais (Temporal, Meilisearch, ScyllaDB, Qdrant, Vitess, Turso, Neon) e fictícias (AstroMesh, HyperKV, CloudShaper, OmniSync, FluxStore). |
| **B** | `B_zero_lexical_overlap` | 18 | Relações funcionais problema $\to$ mecanismo sem nenhuma palavra ou stem compartilhado. |
| **C** | `C_jargon_vs_natural` | 16 | Jargão formal acadêmico em inglês vs descrições funcionais coloquiais equivalentes em português; traps de jargão vazio. |
| **D** | `D_entity_anchor` | 16 | Papéis de entidade: Target central vs Contexto de execução vs Declaração pessoal vs Contexto alienígena. |
| **E** | `E_different_intents` | 16 | Diversidade de intenção: definition, comparison, diagnosis, implementation, architecture, tradeoff. |
| **F** | `F_multi_aspect` | 16 | Perguntas multiaspecto: cobertura total vs omissão de uma ou mais demandas atômicas. |
| **G** | `G_supporting_vs_related` | 16 | Discriminação entre contribuição funcional auxiliar (SUPPORTING) e proximidade temática (RELATED). |
| **H** | `H_epistemology` | 16 | Separação entre DEMONSTRATED_EXPERIENCE, CONCEPTUAL, DECLARATION, HYPOTHESIS e UNCERTAINTY. |
| **I** | `I_short_answers` | 14 | Respostas ultracurtas (5 a 10 palavras), porém precisas e tecnicamente suficientes. |
| **J** | `J_long_answers` | 14 | Respostas prolixas e verbosas com sopa de jargões que não respondem à pergunta. |
| **K** | `K_semantic_mutations` | 14 | Mutações semânticas onde inversão de mecanismos ou desativação de travas inverte a validade da resposta. |
| **L** | `L_unknown_insufficient` | 12 | Respostas genuinamente vagas, ambíguas, vazias ou admissões explícitas de ignorância. |
| **M** | `M_representation_invariance` | 14 | Invariância de representação: inglês, português, bullets, gírias, erros ortográficos preservando significado. |
| **N** | `N_causal_framing` | 14 | Encadeamento causal explícito: Problema $\to$ Ação $\to$ Mecanismo $\to$ Efeito esperado. |
| **O** | `O_false_positive_traps` | 14 | Repetição das palavras da pergunta, tautologias circulares e vocabulário correto sem satisfazer a demanda. |
| **P** | `P_false_negative_traps` | 14 | Respostas em linguagem simples de chão de fábrica, sem nomes de ferramentas e sem jargão formal. |
| **Total** | | **242** | |

---

## 7. Oráculo Humano
Distribuição das classificações do oráculo humano independente no benchmark:
- **DIRECT:** 132 casos (54.5%)
- **RELATED:** 40 casos (16.5%)
- **OFF_TOPIC:** 27 casos (11.2%)
- **INSUFFICIENT:** 15 casos (6.2%)
- **SUPPORTING:** 13 casos (5.4%)
- **PARTIAL:** 10 casos (4.1%)
- **UNKNOWN:** 5 casos (2.1%)

---

## 8. Resultados Globais

```text
================================================================================
STAGE 31.7.9 BLIND REVALIDATION RESULTS
================================================================================
Total de Casos Avaliados:     242
Concordâncias Exatas:          141
Divergências:                  101
Taxa Global de Concordância:   58.26%
================================================================================
```

---

## 9. Confusion Matrix (Human \ System)

```text
Human \ System   | DIRECT      | PARTIAL     | SUPPORTING  | RELATED     | OFF_TOPIC   | INSUFFICIENT | UNKNOWN    
-------------------------------------------------------------------------------------------------------------------
DIRECT           | 127         | 1           | 0           | 0           | 4           | 0           | 0          
PARTIAL          | 9           | 1           | 0           | 0           | 0           | 0           | 0          
SUPPORTING       | 13          | 0           | 0           | 0           | 0           | 0           | 0          
RELATED          | 33          | 1           | 0           | 4           | 2           | 0           | 0          
OFF_TOPIC        | 25          | 0           | 0           | 0           | 2           | 0           | 0          
INSUFFICIENT     | 5           | 0           | 0           | 0           | 5           | 5           | 0          
UNKNOWN          | 3           | 0           | 0           | 0           | 0           | 0           | 2          
```

---

## 10. Resultados por Categoria

| Categoria | Total | Concordância Exata | Divergências | Taxa de Acordo (%) |
| :--- | :--- | :--- | :--- | :--- |
| **P — False Negative Traps** | 14 | 14 | 0 | **100.00%** |
| **M — Representation Invariance** | 14 | 13 | 1 | **92.86%** |
| **A — Open Domain** | 18 | 15 | 3 | **83.33%** |
| **C — Jargon vs Natural** | 16 | 13 | 3 | **81.25%** |
| **N — Causal Framing** | 14 | 11 | 3 | **78.57%** |
| **B — Zero Lexical Overlap** | 18 | 13 | 5 | **72.22%** |
| **I — Short Answers** | 14 | 10 | 4 | **71.43%** |
| **D — Entity Anchor** | 16 | 11 | 5 | **68.75%** |
| **E — Different Intents** | 16 | 11 | 5 | **68.75%** |
| **H — Epistemology** | 16 | 8 | 8 | **50.00%** |
| **K — Semantic Mutations** | 14 | 7 | 7 | **50.00%** |
| **L — Unknown / Insufficient** | 12 | 5 | 7 | **41.67%** |
| **F — Multi-Aspect** | 16 | 4 | 12 | **25.00%** |
| **J — Long Answers (Verbose)** | 14 | 3 | 11 | **21.43%** |
| **G — Supporting vs Related** | 16 | 3 | 13 | **18.75%** |
| **O — False Positive Traps** | 14 | 0 | 14 | **0.00%** |

---

## 11. Divergências & Padrão de Falhas

Das 101 divergências observadas, a distribuição por tipo de erro foi:
- **Semantic False Positive (Human $\ne$ DIRECT, System == DIRECT):** **88 casos (87.1%)**
- **Semantic False Negative (Human == DIRECT, System $\ne$ DIRECT):** **5 casos (5.0%)**
- **Insufficient Overcrediting (Human == INSUFFICIENT, System == OFF_TOPIC / DIRECT):** **5 casos (5.0%)**
- **Boundary RELATED vs OFF_TOPIC:** **2 casos (2.0%)**
- **Other:** **1 caso (1.0%)**

---

## 12. Análise Estrutural dos Failures (Root Cause Analysis)

A comparação entre o Stage 31.7.6 e o Stage 31.7.9 revela uma inversão fundamental e crucial do comportamento do sistema:

### No Stage 31.7.6 (Motor Legado com Fallback de Radical no Step 11):
- O problema dominante era o **Gargalo da Co-ocorrência Léxica**:
- O sistema exigia que a resposta contivesse os mesmos radicais da pergunta (`shared_stems`).
- Como consequência, respostas corretas sem overlap lexical eram massivamente jogadas em `OFF_TOPIC` (**79 Falsos Negativos**).

### No Stage 31.7.9 (Novo Motor de Proposições do Stage 31.7.8):
- O gargalo da co-ocorrência léxica foi **100% resolvido**:
  - Na Categoria P (False Negative Traps), o acerto foi de **100.00%** (14/14).
  - Na Categoria M (Representation Invariance), o acerto foi de **92.86%**.
  - O recall em casos verdadeiramente `DIRECT` saltou para **96.2%** (127 de 132 casos).
- **Porém**, ao remover o filtro de radicais, a heurística de proposição operativa implementada no Stage 31.7.8 tornou-se **excessivamente permissiva**:
  $$\text{is\_operative} = (\text{len}(r\_words) \ge 5) \land (\text{has\_operative\_mechanism} \lor \text{len}(r\_words) \ge 8)$$
  Qualquer resposta com 8 ou mais palavras que contivesse termos técnicos gerais (ou não fosse alienígena pura) foi considerada operativa.
  No passo 6 de `evaluate_relevance`:
  ```python
  if prop.is_operative:
      return {"classification": "DIRECT", ...}
  ```
- **Consequência:** Respostas prolixas sobre Jira e Confluence (J01), tautologias circulares (O01–O14), ações que apoiavam mas não resolviam diretamente (G01–G16) e mutações opostas com mais de 8 palavras (K02, K04) foram indistintamente promovidas a `DIRECT`.
- **A falha migrou de Falso Negativo estrutural para Falso Positivo estrutural (88 falsos DIRECTs).**

---

## 13. Falsos Positivos
Os 88 falsos positivos concentraram-se em 4 padrões claros:
1. **Tautologias e Repetições Circulares (Categoria O — 14 casos):**
   Exemplo: *"O Kubernetes é um orquestrador de pods muito robusto que gerencia containers em clusters grandes com muita facilidade."* (O01) $\to$ Não explica conflitos de IP, mas tem mais de 8 palavras $\to$ Sistema: `DIRECT` (Humano: `RELATED`).
2. **Sopa de Letrinhas e Desvios Prolixos (Categoria J — 11 casos):**
   Exemplo: Responder sobre sprints ágeis, Selenium e GitLab CI para uma pergunta de tuning de SQL (J01) $\to$ Sistema: `DIRECT` (Humano: `OFF_TOPIC`).
3. **Mecanismos Auxiliares não Discriminados (Categoria G — 13 casos):**
   Exemplo: Adicionar métricas no Prometheus para investigar lentidão (G01) $\to$ Sistema: `DIRECT` (Humano: `SUPPORTING`). O sistema não tem regra para rebaixar proposições operativas parciais a `SUPPORTING`.
4. **Respostas Multiaspecto Parciais (Categoria F — 9 casos):**
   Exemplo: Pergunta pede retries com backoff E idempotência; candidato responde apenas retries com backoff (F02) $\to$ Sistema falha na divisão da conjunção e classifica como `DIRECT` (Humano: `PARTIAL`).

---

## 14. Falsos Negativos
Ocorrência residual mínima (apenas 5 casos em 242, taxa de falso negativo de 3.8%):
- Casos em que a resposta técnica era extremamente suscinta e caiu em filtros de ambiguidade ou parsing, mas o núcleo de compreensão de linguagem coloquial e zero-lexical funcionou em 96.2% dos casos verdadeiramente diretos.

---

## 15. Zero Lexical Overlap
- **Resultado:** **72.22%** de exatidão na Categoria B (13/18).
- As únicas divergências nesta categoria ocorreram quando a resposta era um falso positivo (G01/B12 - métricas no Prometheus classificado como DIRECT em vez de SUPPORTING, ou B11 - CSS grid classificado como DIRECT por ter $\ge 8$ palavras).
- Em todos os casos em que a resposta resolvia o problema causal sem palavras compartilhadas (concorrência, quórum de split-brain, backpressure, ring buffers, relógios lógicos causais), o sistema classificou corretamente como `DIRECT`.

---

## 16. Entity Anchors
- **Taxa de Acordo:** **68.75%** na Categoria D.
- O sistema distinguiu com sucesso o Kubernetes/Kafka como alvo central (`DIRECT`) de contextos incidentais (`DIRECT` por causa da concorrência).
- **Falha residual:** Declarações de uso corporativo sem mecanismo (D03, D07, D11) que continham mais de 8 palavras e não caíram no padrão exato de verbos de declaração foram promovidas a `DIRECT`.

---

## 17. Epistemologia
- **Taxa de Acordo:** **50.00%** na Categoria H.
- O campo `epistemic_status` capturou adequadamente `DEMONSTRATED_EXPERIENCE` e `CONCEPTUAL`.
- Porém, como a relevância semântica (`classification`) dependia apenas de `prop.is_operative`, respostas hipotéticas ou autodeclarações de experiência com vocabulário técnico acabaram recebendo score `DIRECT` em relevância semântica, confirmando que o acoplamento entre proposição e relevância ainda precisa de refinamento.

---

## 18. Multi-Aspect Coverage
- **Taxa de Acordo:** **25.00%** na Categoria F.
- A decomposição de perguntas em múltiplas demandas (`demands`) foi limitada aos separadores conjuntivos exatos `" e como "`, `" e quais "`.
- Quando a pergunta utilizava outras construções sintáticas conjuntivas, ela foi tratada como demanda única, impedindo o cálculo fracionário de `AspectCoverage` e gerando 9 falsos `DIRECT` em casos que eram genuinamente `PARTIAL`.

---

## 19. Representation Invariance
- **Taxa de Acordo:** **92.86%** na Categoria M.
- Excelente robustez contra variações estilísticas, gírias, estruturas em lista, inglês formal e português coloquial.
- A única divergência ocorreu na mutação M06 (resposta confiante propondo desativar transações ACID, promovida a `DIRECT` por verbosidade).

---

## 20. Determinismo
- **Amostra:** 25 casos executados 10 vezes consecutivas de forma independente.
- **Resultado:** **100% Determinístico**. Zero variações de classificação ou scores entre execuções.

---

## 21. Catalog Independence
- **Resultado:** **PASS**. O motor executou de forma 100% independente do catálogo de tecnologias, sem autoridade semântica externa e sem divergências em tecnologias uncatalogued.

---

## 22. Explicabilidade
O motor gerou decision records estruturados para todas as inferências:
- A cadeia `QuestionIntent` $\to$ `QuestionDemand` $\to$ `TechnicalProposition` $\to$ `AspectCoverage` $\to$ `EpistemicStatus` permitiu rastrear com precisão cirúrgica o exato ponto onde cada um dos 101 erros foi produzido (a permissividade da condição `is_operative`).

---

## 23. Limitações Conhecidas
1. **Permissividade Proposicional:** Falta de um validador de nexo funcional entre o problema da demanda e a ação da proposição.
2. **Discriminação de SUPPORTING:** Ausência de regras dedicadas para classificar ações auxiliares/observabilidade como `SUPPORTING`.
3. **Polaridade Semântica:** Incapacidade de detectar quando uma proposição propõe a desativação ou destruição do mecanismo de segurança (K02, K04, K06).
4. **Parsing Multiaspecto:** Decomposição de demandas dependente de conectivos estritos.

---

## 24. Conclusão Metodológica
O Stage 31.7.9 cumpriu plenamente seu papel como instrumento de validação científica independente.

Ele provou conclusivamente que:
1. **A barreira lexical foi superada com sucesso:** O novo motor não depende mais de palavras compartilhadas, radicais ou catálogo fechado (100% de acerto em traps de falsos negativos).
2. **Uma nova vulnerabilidade estrutural foi descoberta:** O motor sofre de **Permissividade Proposicional (False Positive Bias)**, promovendo enunciados verbosos ou tautológicos a `DIRECT`.

Como essa falha é de natureza **estrutural e recorrente** (88 falsos positivos, categorias O e G com menos de 20% de exatidão), os critérios de bloqueio da Seção 35 foram atingidos.

---

## 25. Gate Final

```text
GATE:
POST_OPEN_DOMAIN_BLIND_REVALIDATION_BLOCKED
```

### Próximo Estágio:
**Stage 31.7.10 — Root Cause Analysis & Semantic Relation Nexus Remediation:**
Investigar formalmente a ausência do nexo de pertinência demanda-proposição e projetar o validador de relação causal/funcional sem recorrer a listas fechadas de palavras-chave.
