# Stage 31.7.9 — Blind Revalidation of Open-Domain Proposition Architecture

---

## 1. Objective

Executar a **primeira validação cega independente** da nova arquitetura **Open-Domain Proposition & Semantic Relation** implementada no Stage 31.7.8 sobre o runtime congelado, respondendo à pergunta fundamental:

> A nova arquitetura Open-Domain Proposition & Semantic Relation generaliza para casos novos, não utilizados durante sua implementação, sem depender de catálogo fechado, vocabulário conhecido, padrões lexicais ou conhecimento dos casos históricos?

Esta etapa é exclusivamente de **validação científica, auditoria metodológica e mensuração empírica de generalização**, não autorizando qualquer desenvolvimento, correção ou calibração no runtime.

---

## 2. Entry Gate

- **Stage Anterior:** Stage 31.7.8 — Controlled Implementation of Open-Domain Proposition & Semantic Relation Architecture
- **Gate de Entrada:** `CONTROLLED_IMPLEMENTATION_COMPLETE_WITH_WARNINGS`
- **Condição Metodológica:** A arquitetura de proposições abertas foi implementada em paralelo e de modo desacoplado em `reference_runtime/runtime.py`, preservando 100% dos testes históricos e pronta para submissão a um benchmark cego inédito.

---

## 3. Runtime Hash

- **Arquivo Avaliado:** [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py)
- **SHA-256 de Entrada (Stage 31.7.8):**
  `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
- **SHA-256 Verificado durante a Execução:**
  `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
- **SHA-256 de Saída (Auditoria Final do Stage 31.7.9):**
  `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
- **Status de Congelamento:** **100% CONGELADO / INVIOLADO**. Zero linhas, funções, heurísticas, constantes ou pesos foram alterados.

---

## 4. Benchmark Composition

O benchmark foi formulado com **242 casos independentes**, cobrindo exaustivamente todas as 16 categorias semânticas obrigatórias (A a P):

| Código | Categoria | Casos | Foco da Avaliação Semântica |
| :--- | :--- | :---: | :--- |
| **A** | `A_open_domain` | 18 | Tecnologias inéditas reais (Temporal, Meilisearch, ScyllaDB, Qdrant, Vitess, Turso, Neon) e fictícias (AstroMesh, HyperKV, CloudShaper, OmniSync, FluxStore). |
| **B** | `B_zero_lexical_overlap` | 18 | Relações funcionais problema $\to$ mecanismo sem palavras ou radicais compartilhados. |
| **C** | `C_jargon_vs_natural` | 16 | Jargão formal acadêmico em inglês vs descrições funcionais coloquiais equivalentes em português; armadilhas de jargão vazio. |
| **D** | `D_entity_anchor` | 16 | Papéis de entidade: Target central vs Contexto de execução vs Declaração biográfica vs Contexto alienígena. |
| **E** | `E_different_intents` | 16 | Diversidade de intenção: definition, comparison, diagnosis, implementation, architecture, tradeoff. |
| **F** | `F_multi_aspect` | 16 | Perguntas com múltiplas demandas atômicas: cobertura total vs omissão parcial de demandas. |
| **G** | `G_supporting_vs_related` | 16 | Discriminação entre contribuição funcional auxiliar (SUPPORTING) e proximidade temática (RELATED). |
| **H** | `H_epistemology` | 16 | Separação entre DEMONSTRATED_EXPERIENCE, CONCEPTUAL, DECLARATION, HYPOTHESIS e UNCERTAINTY. |
| **I** | `I_short_answers` | 14 | Respostas ultracurtas (5 a 10 palavras), precisas e tecnicamente suficientes. |
| **J** | `J_long_answers` | 14 | Respostas prolixas e verbosas com sopa de jargões que não respondem à pergunta. |
| **K** | `K_semantic_mutations` | 14 | Mutações semânticas onde inversão de mecanismos ou desativação de travas inverte a validade da resposta. |
| **L** | `L_unknown_insufficient` | 12 | Respostas genuinamente vagas, ambíguas, vazias ou admissões explícitas de ignorância. |
| **M** | `M_representation_invariance` | 14 | Invariância de representação: inglês, português, bullets, gírias, erros ortográficos preservando significado. |
| **N** | `N_causal_framing` | 14 | Encadeamento causal explícito: Problema $\to$ Ação $\to$ Mecanismo $\to$ Efeito esperado. |
| **O** | `O_false_positive_traps` | 14 | Repetição das palavras da pergunta, tautologias circulares e vocabulário correto sem satisfazer a demanda. |
| **P** | `P_false_negative_traps` | 14 | Respostas em linguagem simples de chão de fábrica, sem nomes de ferramentas e sem jargão formal. |
| **Total** | | **242** | |

---

## 5. Benchmark Independence Audit

- **Origem dos Casos:** Casos formulados de forma independente e armazenados em [`scratch/build_stage_31_7_9_blind_benchmark.py`](file:///d:/Projetos/TechLens/scratch/build_stage_31_7_9_blind_benchmark.py).
- **Sobreposição com Testes Unitários do Stage 31.7.8:** **ZERO**. Nenhum dos casos de teste de [`tests/test_stage_31_7_8_open_domain_proposition_engine.py`](file:///d:/Projetos/TechLens/tests/test_stage_31_7_8_open_domain_proposition_engine.py) foi reutilizado.
- **Sobreposição com Casos Históricos (Stages 31.7.6 / 31.7.7):** **ZERO**. Nenhuma das 107 falhas históricas foi adaptada como caso de teste deste benchmark.
- **Auditoria de Co-design:** Não houve derivação reversa a partir da implementação de `OpenDomainPropositionEngine`.
- **Classificação de Independência:** `INDEPENDENT`.

---

## 6. Human Oracle Methodology

1. **Protocolo Cego Estrito:** A anotação do oráculo humano foi realizada **antes** de qualquer execução do sistema. O executor cego não teve acesso aos rótulos humanos durante a inferência.
2. **Justificativa Explicada:** Cada anotação humana contém uma justificativa causal e funcional independente (`human_rationale`).
3. **Imutabilidade do Oráculo:** Nenhuma classificação humana foi ajustada retrospectivamente para aproximar o oráculo do comportamento do sistema.
4. **Distribuição das Classes no Oráculo Humano:**
   - `DIRECT`: 132 casos (54.55%)
   - `RELATED`: 40 casos (16.53%)
   - `OFF_TOPIC`: 27 casos (11.16%)
   - `INSUFFICIENT`: 15 casos (6.20%)
   - `SUPPORTING`: 13 casos (5.37%)
   - `PARTIAL`: 10 casos (4.13%)
   - `UNKNOWN`: 5 casos (2.07%)

---

## 7. Global Results

```text
================================================================================
STAGE 31.7.9 BLIND REVALIDATION AUDIT METRICS
================================================================================
Total de Casos no Benchmark:      242
Casos Avaliados:                  242 (100.0%)
Casos Não Avaliados:              0 (0.0%)
Concordâncias Exatas:             141
Divergências Globais:             101
Taxa Global de Concordância:      58.26%
--------------------------------------------------------------------------------
Falsos Positivos de Relevância:   88 casos (87.1% das divergências)
Falsos Negativos de Relevância:   5 casos (5.0% das divergências)
Outras Divergências:              8 casos (7.9% das divergências)
================================================================================
```

---

## 8. Confusion Matrix

Matriz completa cruzando a classificação do Oráculo Humano com a inferência do Sistema:

```text
Human \ System   | DIRECT      | PARTIAL     | SUPPORTING  | RELATED     | OFF_TOPIC   | INSUFFICIENT | UNKNOWN    | Total Humano
--------------------------------------------------------------------------------------------------------------------------------
DIRECT           | 127         | 1           | 0           | 0           | 4           | 0           | 0          | 132
PARTIAL          | 9           | 1           | 0           | 0           | 0           | 0           | 0          | 10
SUPPORTING       | 13          | 0           | 0           | 0           | 0           | 0           | 0          | 13
RELATED          | 33          | 1           | 0           | 4           | 2           | 0           | 0          | 40
OFF_TOPIC        | 25          | 0           | 0           | 0           | 2           | 0           | 0          | 27
INSUFFICIENT     | 5           | 0           | 0           | 0           | 5           | 5           | 0          | 15
UNKNOWN          | 3           | 0           | 0           | 0           | 0           | 0           | 2          | 5
--------------------------------------------------------------------------------------------------------------------------------
Total Sistema    | 215         | 3           | 0           | 4           | 13          | 5           | 2          | 242
```

---

## 9. Results by Category

| Categoria | Total | Concordância Exata | Divergências | Taxa de Acordo (%) | Principais Tipos de Falha |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **P — False Negative Traps** | 14 | 14 | 0 | **100.00%** | Nenhuma falha (superação total da barreira lexical) |
| **M — Representation Invariance** | 14 | 13 | 1 | **92.86%** | Falso DIRECT em mutação de polaridade (M06) |
| **A — Open Domain** | 18 | 15 | 3 | **83.33%** | Falsos DIRECTs em respostas verbosas de tech inédita |
| **C — Jargon vs Natural** | 16 | 13 | 3 | **81.25%** | Falsos DIRECTs em traps de jargão prolixo sem mecanismo |
| **N — Causal Framing** | 14 | 11 | 3 | **78.57%** | Falsos DIRECTs em ações desconectadas do efeito |
| **B — Zero Lexical Overlap** | 18 | 13 | 5 | **72.22%** | Falsos DIRECTs em ferramentas auxiliares (Prometheus) |
| **I — Short Answers** | 14 | 10 | 4 | **71.43%** | Falsos Negativos pontuais por parsing de brevidade extrema |
| **D — Entity Anchor** | 16 | 11 | 5 | **68.75%** | Falsos DIRECTs em declarações biográficas com $\ge 8$ palavras |
| **E — Different Intents** | 16 | 11 | 5 | **68.75%** | Falsos DIRECTs em descrições sem comparação ou diagnóstico |
| **H — Epistemology** | 16 | 8 | 8 | **50.00%** | Falsos DIRECTs em hipóteses formuladas com vocabulário técnico |
| **K — Semantic Mutations** | 14 | 7 | 7 | **50.00%** | Falsos DIRECTs quando ação desativa proteção ou causa dano |
| **L — Unknown / Insufficient** | 12 | 5 | 7 | **41.67%** | Falsos DIRECTs em respostas evasivas que citam termos |
| **F — Multi-Aspect** | 16 | 4 | 12 | **25.00%** | Falsos DIRECTs em respostas parciais (falha de conectivos) |
| **J — Long Answers (Verbose)** | 14 | 3 | 11 | **21.43%** | Falsos DIRECTs em parágrafos prolixos sem relação causal |
| **G — Supporting vs Related** | 16 | 3 | 13 | **18.75%** | Ausência de classe SUPPORTING; promoção massiva a DIRECT |
| **O — False Positive Traps** | 14 | 0 | 14 | **0.00%** | Falsos DIRECTs em tautologias que repetem o enunciado |

---

## 10. False Positives

Dos 101 casos divergentes, **88 casos (87.1%)** foram **Falsos DIRECTs** (onde o Oráculo Humano classificou como `RELATED`, `OFF_TOPIC`, `SUPPORTING`, `PARTIAL`, `INSUFFICIENT` ou `UNKNOWN`, e o sistema concedeu `DIRECT`).

Padrões recorrentes observados:
1. **Tautologias e Repetições Circulares (Categoria O — 14 casos, 0% acerto):** Respostas que apenas reformulam a pergunta em português formal sem apresentar ação operativa (ex.: *"O Kubernetes gerencia containers com alta robustez"* em pergunta sobre colisão de IPs) foram promovidas a `DIRECT`.
2. **Sopa de Letrinhas e Desvios Prolixos (Categoria J — 11 casos, 21.4% acerto):** Parágrafos longos citando termos de DevOps, Scrum e CI/CD para perguntas de banco de dados receberam `DIRECT` por ultrapassarem o threshold de comprimento substantivo.
3. **Mecanismos Auxiliares não Discriminados (Categoria G — 13 casos, 18.8% acerto):** Instrumentação de métricas no Prometheus ou alertas no Grafana foram promovidos a `DIRECT` para perguntas cuja demanda exigia mitigação causal direta (ex.: pool de conexões esgotado).
4. **Respostas Parciais em Perguntas Multiaspecto (Categoria F — 9 casos):** Perguntas exigindo 2 ou 3 ações combinadas tiveram respostas que cobriam apenas uma delas classificadas como `DIRECT`.
5. **Mutações Opostas e Antíteses (Categoria K — 7 casos):** Propostas que sugerem explicitamente desativar transações ACID ou desligar locks foram aceitas como solução direta por conterem termos operacionais válidos.

---

## 11. False Negatives

Ocorrência residual mínima: **apenas 5 casos em 242 (3.8% de taxa de falso negativo global)**.
- Recall de `DIRECT` legítimo: **96.2%** (127 de 132 casos verdadeiramente diretos identificados com sucesso).
- Comparação histórica: No Stage 31.7.6, o motor legado registrava **79 falsos negativos** causados pela dependência de radicais coincidentes. O novo motor de proposições abertas eliminou 93.7% dessa deficiência histórica.

---

## 12. Structural Failure Analysis

A auditoria científica revela uma **inversão de paradigma metodológico**:

### No Stage 31.7.6 (Gargalo da Co-ocorrência Léxica):
O sistema era hiper-conservador no domínio aberto: sem radicais coincidentes no `Step 11`, descartava sumariamente respostas legítimas como `disjunct_open_domain`.

### No Stage 31.7.9 (Permissividade Proposicional no Domínio Aberto):
Ao remover o filtro de radicais, a heurística de extração de proposições em `reference_runtime/runtime.py`:
$$\text{is\_operative} = (\text{len}(r\_words) \ge 5) \land (\text{has\_operative\_mechanism} \lor \text{len}(r\_words) \ge 8)$$
rotulou **qualquer frase substantiva com 8 ou mais palavras** como proposição operativa (`is_operative = True`).

Subsequentemente, no Step 6 da resolução semântica:
```python
if prop.is_operative:
    return {"classification": "DIRECT", ...}
```
O sistema concedeu `DIRECT` para qualquer resposta que contivesse uma proposição operativa, **sem validar o nexo de pertinência causal/funcional entre a demanda da pergunta e a ação descrita**. A falha migrou de Falso Negativo estrutural para **Falso Positivo estrutural (88 falsos DIRECTs)**.

---

## 13. Zero Lexical Overlap Analysis

- **Performance na Categoria B:** **72.22% de acerto exato (13/18)**.
- **Resultado Semântico:** Em todos os casos em que a resposta descrevia o mecanismo causal sem palavras compartilhadas (concorrência, quórum de split-brain, backpressure, ring buffers, relógios vetoriais), o sistema classificou corretamente como `DIRECT`.
- **Divergências:** As 5 divergências da Categoria B não foram falsos OFF_TOPIC (zero falsos descartes), mas falsos DIRECTs onde a resposta era auxiliar (SUPPORTING) ou genérica e foi promovida a DIRECT. A dependência lexical foi formalmente superada.

---

## 14. Entity Anchor Analysis

- **Performance na Categoria D:** **68.75% de acerto exato (11/16)**.
- O sistema distinguiu satisfatoriamente menções incidentais de entidades e contextos alienígenas.
- **Vulnerabilidade Residual:** Declarações de experiência pessoal ou citações biográficas de uso da tecnologia em ambientes corporativos (D03, D07, D11) que continham mais de 8 palavras e escaparam da lista restrita de marcadores declarativos foram indevidamente promovidas a `DIRECT`.

---

## 15. Epistemic Analysis

- **Performance na Categoria H:** **50.00% de acerto exato (8/16)**.
- O campo `epistemic_status` capturou adequadamente os marcadores de `DEMONSTRATED_EXPERIENCE` e `CONCEPTUAL`.
- **Desacoplamento Incompleto:** Como a relevância semântica dependia apenas de `prop.is_operative`, respostas formuladas como hipóteses ou declarações biográficas acabaram recebendo classificação `DIRECT` no plano da relevância semântica, revelando que a separação entre epistemologia e relevância ainda permite vazamento de score.

---

## 16. Multi-Aspect Analysis

- **Performance na Categoria F:** **25.00% de acerto exato (4/16)**.
- A decomposição de perguntas em múltiplas demandas (`demands`) foi limitada aos separadores sintáticos literais `" e como "` e `" e quais "`.
- Perguntas contendo conjunções alternativas, pontuação ou enumerações foram tratadas como demanda atômica única, impedindo o cálculo fracionário de `AspectCoverage` e gerando 9 falsos `DIRECT` em respostas que cobriam apenas parte dos requisitos.

---

## 17. Representation Invariance

- **Performance na Categoria M:** **92.86% de acerto exato (13/14)**.
- Excelente robustez contra variações estilísticas, gírias, estruturas em lista, inglês formal e português coloquial.
- A única divergência ocorreu em M06 (mutação onde o candidato sugeriu desativar transações ACID, promovido a `DIRECT` pela permissividade do tamanho da resposta).

---

## 18. Determinism

- **Amostra Auditada:** 25 casos executados em 10 iterações consecutivas independentes.
- **Resultado:** **100% Determinístico**. Zero variações de classificação semântica, proposições extraídas ou scores entre execuções.

---

## 19. Catalog Independence

- **Auditoria de Catálogo:** Execução do benchmark sob esvaziamento completo do dicionário de capacidades (`_FUNCTIONAL_CAPABILITIES.clear()`).
- **Resultado:** **100% Invariante**. Zero dependência de catálogo fechado ou de ontologia pré-codificada.

---

## 20. Explainability

Para 100% dos casos avaliados, o motor gerou registros de decisão auditáveis no formato:
```yaml
semantic_decision:
  question_intent: "troubleshooting"
  question_demands: ["reduzir contenção em regiões críticas"]
  response_propositions:
    - subject: "período de reserva de recurso compartilhado"
      action: "diminuir"
      mechanism: "reserva temporária mínima"
      is_operative: true
  aspect_coverage: 1.0
  relevance: "DIRECT"
  epistemic_status: "CONCEPTUAL"
```
A cadeia explicativa permitiu identificar exatamente a linha de raciocínio de cada classificação e rastrear com clareza matemática a causa-raiz dos 88 falsos positivos.

---

## 21. Historical Regression

Execução da suíte canônica de testes de regressão do repositório:
```text
Comando: py run_reference_runtime_tests.py
Total de testes:    1005
Testes aprovados:   1005 (100.0%)
Testes falhos:      0 (0.0%)
Testes pulados:     1 (quarentena histórica)
Status:             PASS
```
Todos os 1005 testes históricos continuam passando integralmente.

---

## 22. Reference Harness

Execução do harness de referência canônico:
```text
Comando: py run_reference_harness.py
Suítes executadas:  8 / 8
Suítes falhas:      0 / 8
Status Global:      PASS_WITH_WARNINGS
```
A integridade estrutural do pipeline completo permanece preservada.

---

## 23. Runtime Integrity

- **Verificação SHA-256 de [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py):**
  - Entrada: `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
  - Saída:   `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
- **Integridade:** **RUNTIME INALTERADO (100% Frozen)**.

---

## 24. Limitations

1. **Permissividade Proposicional (False Positive Bias):** O limiar `len(r_words) >= 8` promove qualquer frase com vocabulário substantivo a proposição operativa.
2. **Ausência de Validador de Nexo Demanda $\to$ Proposição:** Não há verificação se a ação descrita neutraliza o problema formulado na demanda.
3. **Ausência de Mecanismo de Classificação para SUPPORTING:** Proposições auxiliares ou de monitoramento são indiscriminadamente promovidas a `DIRECT`.
4. **Insensibilidade à Polaridade Semântica:** Ações que propõem desabilitar mecanismos de segurança não são distinguidas de ações corretivas.
5. **Rigidez Sintática no Parsing Multiaspecto:** Decomposição conjuntiva de demandas depende de conectivos estritos.

---

## 25. Conclusion

O Stage 31.7.9 cumpriu rigorosamente seu papel como instrumento de validação científica independente.

O resultado estabelece duas conclusões fundamentais:
1. **Sucesso Metodológico:** A barreira da co-ocorrência léxica e a dependência de catálogo fechado foram superadas com sucesso (100% de acerto na Categoria P e 96.2% de recall em casos diretos).
2. **Descoberta da Nova Falha Estrutural:** A remoção do filtro léxico sem a introdução de um validador de nexo funcional gerou um viés massivo de falsos positivos (88 falsos DIRECTs em 242 casos).

Em observância aos princípios da governança de que *"um bloqueio é um resultado válido da validação"* e de que *"não se deve tentar transformar BLOCKED em PASS por conveniência"*, a presença de falhas estruturais recorrentes nas categorias O (0%), G (18.75%) e J (21.43%) exige formalmente a interrupção da esteira antes de Production Readiness.

---

## 26. Gate

```text
GATE FINAL DO STAGE 31.7.9:
POST_OPEN_DOMAIN_BLIND_REVALIDATION_BLOCKED
```

### Próximo Estágio Recomendado:
**Stage 31.7.10 — Root Cause Analysis & Semantic Relation Nexus Remediation**
- Investigar a fundo a permissividade proposicional.
- Projetar o modelo formal do **Validador de Nexo Demanda $\to$ Proposição** (verificação de pertinência funcional sem listas fechadas de termos).
- Modelar o discriminador estrutural para a classe `SUPPORTING`.
- Modelar a detecção de polaridade semântica para antíteses e mutações destrutivas.
