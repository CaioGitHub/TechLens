# Stage 31.7.12 — Independent Contract Audit and Blind Semantic Revalidation Design

---

## 1. Integridade e Hashes

- **Objetivo da Auditoria:** Realizar uma inspeção crítica, factual e independente sobre a implementação da arquitetura `Demand-Proposition Nexus` entregue no Stage 31.7.11, avaliando aderência aos contratos arquiteturais e desenhando um protocolo estrito para a revalidação semântica cega independente (Stage 31.7.13).
- **Runtime File:** [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py)
- **Hash de Referência Anterior (Stage 31.7.10 Entry):**
  `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
- **Hash de Saída Documentado do Stage 31.7.11:**
  `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E`
- **Hash Atual Recalculado (SHA-256):**
  `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E`
- **Integridade do Congelamento:** **100% CONFIRMADA**. O arquivo não sofreu nenhuma alteração, mutação ou edição posterior à conclusão do Stage 31.7.11. O status de trabalho do repositório (`git status --short`) está completamente limpo.

```yaml
stage: "31.7.12"

audit_status:
  runtime_frozen: true
  baseline_hash: "5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E"
  hash_verified: true
  working_tree_clean: true

contract_compliance:
  direct_auto_promotion_removed: true
  length_proxy_removed: true
  demand_nexus_implemented: true
  multi_aspect_partial_tracked: true
  supporting_vs_related_decoupled: true
  epistemics_decoupled: true
  explainability_present: true

identified_gaps:
  - "Decomposição de demandas atômicas limitada a até 2 aspectos via conectivo único ('split(conj, 1)')."
  - "Averiguação de ortogonalidade de domínio depende de marcadores heurísticos (frontend, devops/ci), não de modelo ontológico universal."
  - "Antítese destrutiva sintática não diferencia desativação para teste de laboratório controlado vs produção."
  - "Testes contratuais existentes são co-desenhados com a implementação (n=24), exigindo validação cega externa (n=250)."
```

---

## 2. Arquivos Inspecionados

A auditoria inspecionou diretamente os seguintes componentes de código e governança:
1. [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py):
   - Linhas 1640–1678: Dataclasses de suporte (`DemandPropositionNexus`, `TechnicalProposition`, `QuestionDemand`, `AspectCoverage`, `EpistemicEvaluation`).
   - Linhas 2860–2868: Função de orquestração `_evaluate_semantic_relevance` (preservação do motor legado como default).
   - Linhas 2870–3410: Classe [`OpenDomainPropositionEngine`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py#L2870).
   - Linhas 3413–3420: Entrypoint público `evaluate_open_domain_semantic_relevance` e comparador diagnóstico `compare_semantic_engines`.
2. [`tests/test_stage_31_7_11_demand_proposition_nexus.py`](file:///d:/Projetos/TechLens/tests/test_stage_31_7_11_demand_proposition_nexus.py):
   - Suíte contratual de 8 classes de teste cobrindo categorias A a H.
3. [`tests/test_stage_31_7_8_open_domain_proposition_engine.py`](file:///d:/Projetos/TechLens/tests/test_stage_31_7_8_open_domain_proposition_engine.py):
   - Suíte unitária histórica de 16 testes sobre tecnologias abertas e invariância.
4. [`START_HERE.md`](file:///d:/Projetos/TechLens/START_HERE.md) e [`GEMINI_HANDOFF.md`](file:///d:/Projetos/TechLens/GEMINI_HANDOFF.md):
   - Registros de transição e histórico de governança.

---

## 3. Auditoria do Fluxo Efetivo de Execução

O fluxo de execução do método `evaluate_relevance(question, response)` em [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py#L3252) segue a cadeia formal:

```text
Entrada (question, response)
       ↓
[1. decompose_question]
       ↓ (Normalização, detecção de intenção, entidades e quebra de demandas multiaspecto)
QuestionIntent + tuple[QuestionDemand]
       ↓
[2. extract_response_propositions]
       ↓ (Extração sem proxy de comprimento; validação de mecanismos e ações funcionais)
tuple[TechnicalProposition]
       ↓
[3. evaluate_epistemic_status]
       ↓ (Avaliação independente: DEMONSTRATED_EXPERIENCE | CONCEPTUAL | DECLARATION | HYPOTHESIS | UNCERTAINTY)
EpistemicEvaluation
       ↓
[4. assess_demand_nexus (Pairwise per Demand)]
       ↓ (Avaliação par-a-par: Demanda vs Proposição)
tuple[DemandPropositionNexus]
       ↓
[5. Aggregation & Coverage Calculation]
       ↓
Decisão Final de Classificação:
  ├─ Se DOMAIN_DISJUNCT → OFF_TOPIC (alien_domain ou domain_disjunct)
  ├─ Se ANTITHESIS_OPPOSED → OFF_TOPIC (destructive_antithesis)
  ├─ Se IGNORANCE ou INSUFFICIENT → INSUFFICIENT
  ├─ Se EVASIVE → UNKNOWN
  ├─ Se multiaspecto (len > 1):
  │     ├─ ratio >= 0.75 → DIRECT
  │     ├─ ratio > 0.0 ou PARTIALLY_SOLVES → PARTIAL
  │     ├─ CONTRIBUTES_TO → SUPPORTING
  │     ├─ THEMATICALLY_ADJACENT → RELATED
  │     └─ fallback → OFF_TOPIC
  └─ Se demanda única:
        ├─ FUNCTIONALLY_SOLVES → DIRECT
        ├─ CONTRIBUTES_TO → SUPPORTING
        ├─ THEMATICALLY_ADJACENT → RELATED
        ├─ PARTIALLY_SOLVES ou UNMET_DEMAND → PARTIAL
        └─ fallback → OFF_TOPIC
```

---

## 4. Resultado da Auditoria dos Contratos Arquiteturais

### 4.1. Ausência de Promoção Automática para `DIRECT`
- **Fato Auditado:** No motor anterior (Stage 31.7.8), a linha `is_operative = len(r_words) >= 5 and (has_operative_mechanism or len(r_words) >= 8)` promovia qualquer texto com 8 palavras a operativo e, em seguida, `if prop.is_operative: return {"classification": "DIRECT", ...}` promovia incondicionalmente a `DIRECT`.
- **Código Atual:** A cláusula `len(r_words) >= 8` foi **100% removida**. A atribuição de operatividade agora requer `(has_operative_mech or has_functional_action) and not is_antithesis and not is_alien and not is_trivia and not is_evasive`. Respostas substantivas longas contendo apenas jargão ou narrativas biográficas recebem `is_operative = False`.
- **Veredito:** **CONFORME**. O proxy de comprimento foi eliminado.

### 4.2. Atendimento Funcional (`FUNCTIONALLY_SOLVES`)
- **Fato Auditado:** `FUNCTIONALLY_SOLVES` não é concedido pela mera presença de palavras da pergunta ou menção da entidade técnica. Ele é atribuído apenas quando há mecanismo técnico ou ação com efeito/restrição (`has_functional_action`), e desde que a proposição não pertença a um domínio ortogonal ou seja antítese.
- **Veredito:** **CONFORME**.

### 4.3. Cobertura por Demanda (Multi-Aspect Demands)
- **Fato Auditado:** Perguntas coordenadas por conectivos como `" e como "`, `" e de que forma "`, `" e garantir "` são particionadas em demandas atômicas (`demand_1` e `demand_2`). A cobertura é calculada por demanda individual. A omissão de um requisito essencial (ex: idempotência em um retry com backoff) resulta em `PARTIAL`, prevenindo falsos `DIRECT`.
- **Limitação Identificada:** O particionador utiliza `q_norm.split(conj, 1)` uma única vez, decompondo no máximo 2 demandas atômicas. Perguntas com 3 ou mais aspectos emaranhados acumulam os aspectos finais na segunda demanda.
- **Veredito:** **CONFORME COM LIMITAÇÃO DOCUMENTADA**.

### 4.4. Distinção entre Classes Canônicas
- **Fato Auditado:** As 7 classes canônicas do projeto possuem critérios de entrada e rotas formais de saída:
  - `DIRECT`: nexo funcional comprovado cobrindo as demandas primárias.
  - `PARTIAL`: atendimento demonstrado a subset de demandas ou aspecto incompleto.
  - `SUPPORTING`: suporte funcional auxiliar (observabilidade/monitoramento via `CONTRIBUTES_TO`).
  - `RELATED`: menção de ferramenta, hardware, trivia ou declaração de experiência sem mecanismo operativo (`THEMATICALLY_ADJACENT`).
  - `OFF_TOPIC`: domínios técnicos ortogonais (`DOMAIN_DISJUNCT`) ou antítese destrutiva (`ANTITHESIS_OPPOSED`).
  - `INSUFFICIENT`: carência probatória técnica (declaração de ignorância ou filler).
  - `UNKNOWN`: ambiguidade e vagueza explicativa (`EVASIVE`).
- **Veredito:** **CONFORME**.

### 4.5. Polaridade e Contexto
- **Fato Auditado:** Respostas que preconizam desativar controles críticos ("desativo todos os locks", "desligar transações acid", "remover validação") são detectadas por `antithesis_markers` e categorizadas como `ANTITHESIS_OPPOSED` → `OFF_TOPIC`.
- **Limitação Identificada:** A verificação atual é sintática sobre padrões lexicais de desligamento. Ela não possui modelagem semântica para diferenciar uma desativação destrutiva em produção de um procedimento legítimo de diagnóstico temporário em ambiente de laboratório isolado.
- **Veredito:** **CONFORME COM LIMITAÇÃO DOCUMENTADA**.

### 4.6. Desacoplamento Epistemológico
- **Fato Auditado:** A estrutura `EpistemicEvaluation` é instanciada separadamente da pertinência semântica. O código garante explicitamente que:
  ```python
  if is_decl and not has_demo_action and not has_functional_action:
      is_operative = False
  ```
  Isso faz com que declarações sem demonstração prática ("Tenho 8 anos de experiência em particionamento") recebam `DECLARATION` e sejam roteadas para `THEMATICALLY_ADJACENT` → `RELATED`, e não `DIRECT`. Por outro lado, respostas conceituais corretas sem declaração de experiência pessoal recebem `CONCEPTUAL` e `DIRECT`.
- **Veredito:** **CONFORME**.

### 4.7. Regras Ocultas e Dependência Lexical
- **Fato Auditado:**
  - O motor é **livre de catálogos ontológicos fechados**. Ele processa com sucesso tecnologias não cadastradas (TiKV, Dragonfly, ClickHouse, Novastream).
  - O motor **não possui whitelists de pares históricos**.
  - **Identificação de Vocabulário Simbólico:** O motor possui tuplas internas de palavras operativas (`self.operative_indicators` com ~60 termos), ações (`self.functional_actions`) e efeitos (`self.functional_effects`). Embora esses termos representem conceitos fundamentais de engenharia de software (sharding, consensus, locks, replication, caching), o motor depende da presença desses indicadores para inferir operatividade na ausência de ações funcionais contextuais.
- **Veredito:** **CONFORME COM LIMITAÇÃO DOCUMENTADA**.

### 4.8. Explicabilidade e Rastreabilidade
- **Fato Auditado:** O retorno canônico inclui o bloco `demand_nexus`, explicitando o par demanda-proposição, a relação estabelecida e o rationale. Não há decisões opacas baseadas em scores arbitrários sem rastreabilidade.
- **Veredito:** **CONFORME**.

---

## 5. Auditoria dos Testes Existentes

### 5.1 Suíte Contratual do Stage 31.7.11 (`tests/test_stage_31_7_11_demand_proposition_nexus.py`)
- **Total de Classes de Teste:** 8
- **Total de Casos de Teste Exercitados:** 17 casos específicos.
- **Distribuição de Cobertura:**
  - Categoria A (Atendimento Direto): 4 casos (TiKV, ClickHouse, Dragonfly, Concorrência zero-lexical).
  - Categoria B (Falsos Positivos): 5 casos (Buzzwords, Culinária alienígena, Frontend em concorrência, DevOps em SQL, Tautologia circular).
  - Categoria C (Supporting vs Related): 2 casos (Prometheus em latência vs Kafka biográfico).
  - Categoria D (Multiaspecto): 2 casos (Retry + Backoff + Idempotência completo vs parcial).
  - Categoria E (Polaridade): 1 caso (Desativar locks e ACID).
  - Categoria F (Epistemologia): 3 casos (Demonstrado vs Declaração vs Hipótese).
  - Categoria G (Invariância de Representação): 2 casos (Novastream conciso vs prolixo informal).
  - Categoria H (Limites de Inferência): 3 casos (Evasiva UNKNOWN vs Ignorância INSUFFICIENT vs Filler INSUFFICIENT).
- **Resultado:** 100% de aprovação (8/8 métodos, 0 falhas).

### 5.2 Suíte Histórica do Stage 31.7.8 (`tests/test_stage_31_7_8_open_domain_proposition_engine.py`)
- **Total de Testes:** 16 testes unitários.
- **Resultado:** 100% de aprovação (16/16 métodos, 0 falhas).

### 5.3 Regressão Canônica Global
- `py run_reference_runtime_tests.py`: **1013/1013 testes aprovados** (100% PASS, 0 falhas, 1 skipped).
- `py run_reference_harness.py`: **8/8 suítes executadas com status PASS_WITH_WARNINGS**.

---

## 6. Lacunas Identificadas nos Testes Existentes

1. **Risco de Co-Design:** Os 17 casos contratuais do Stage 31.7.11 foram elaborados no mesmo ciclo de desenvolvimento da implementação. Eles provam que as rotas de código funcionam para os exemplos testados, mas não constituem evidência independente de generalização estatística.
2. **Escassez de Casos de Fronteira Negativa:** Não há testes contratuais para outros domínios ortogonais além de Frontend e DevOps (ex: Machine Learning em Redes, Segurança de Criptografia em CSS, etc.).
3. **Casos Multiaspecto Complexos:** Apenas 1 par de teste multiaspecto (Retry + Idempotência) foi exercitado na suíte 31.7.11. Faltam perguntas com 3 ou 4 demandas concorrentes.
4. **Respostas Parcialmente Erradas com Mecanismo Válido:** Faltam casos onde o candidato descreve um mecanismo válido mas aplica-o ao problema invertido sem disparar os marcadores de antítese literal.

---

## 7. Dependências Lexicais e Heurísticas Encontradas

A auditoria localizou as seguintes heurísticas estáticas no código:
1. `alien_terms`: 18 termos de culinária e cotidiano. Qualquer atividade fora desse vocabulário que não seja computacional pode depender do fallback genérico.
2. `frontend_markers` e `devops_ci_markers`: tuplas fechadas de tecnologias de interface e automação usadas para identificar desconexão de domínio com concorrência e banco de dados.
3. `antithesis_markers`: 14 frases de desativação de proteção. A ausência de uma variação frasal pode impedir a detecção de uma antítese destrutiva.
4. `operative_indicators`: tupla de substantivos e verbos técnicos operacionais.

Essas heurísticas são justificáveis em um motor simbólico semântico determinístico, mas impõem limites à generalização em domínios não previstos. O benchmark independente deve estressar exatamente essas fronteiras.

---

## 8. Especificação do Benchmark Cego Independente (Stage 31.7.13)

Para assegurar uma validação semântica com poder estatístico equivalente ou superior às etapas anteriores, o benchmark cego do Stage 31.7.13 deve ser estruturado com:

- **Volume Total:** **250 casos independentes** (perguntas e respostas técnicas inéditas, nunca expostas ao runtime durante o desenvolvimento).
- **Composição Estratificada por Classe de Referência:**
  - `DIRECT`: 60 casos (24,0%) — Soluções diretas com e sem sobreposição lexical, tecnologias inéditas, respostas concisas.
  - `PARTIAL`: 35 casos (14,0%) — Respostas que atendem a subset de demandas multiaspecto ou omitem condições essenciais.
  - `SUPPORTING`: 30 casos (12,0%) — Observabilidade, telemetria, profiling e monitoramento que auxiliam sem mitigar a causa raiz.
  - `RELATED`: 35 casos (14,0%) — Menções de tecnologias do mesmo ecossistema, trivia histórica, especificações de hardware ou declarações de senioridade sem mecanismo demonstrado.
  - `OFF_TOPIC`: 50 casos (20,0%) — Respostas com antítese operacional destrutiva, domínios técnicos ortogonais (redes vs ML, frontend vs banco) e domínios não computacionais.
  - `INSUFFICIENT`: 25 casos (10,0%) — Admissão explícita de ignorância, desconhecimento ou confirmações conversacionais vazias ("sim", "com certeza").
  - `UNKNOWN`: 15 casos (6,0%) — Respostas evasivas, ambíguas, tautológicas ou circulares ("depende de muitas coisas").

### Distribuição em 16 Categorias Temáticas (A a P):
1. **Grupo A — Tecnologias Inéditas / Fictícias:** (15 casos) Sistemas com nomes inventados com mecanismos funcionais.
2. **Grupo B — Zero-Lexical Clássico:** (20 casos) Conceitos computacionais explicados sem compartilhar substantivos com a pergunta.
3. **Grupo C — Multiaspecto Coordenado:** (20 casos) Perguntas com 2 ou mais demandas primárias (cobertura total vs parcial).
4. **Grupo D — Observabilidade Auxiliar (Supporting):** (15 casos) APMs, métricas e logs frente a problemas de arquitetura.
5. **Grupo E — Antítese Operacional / Polaridade:** (15 casos) Recomendações que agravam a falha ou desativam segurança.
6. **Grupo F — Domínios Ortogonais Computacionais:** (20 casos) CSS para concorrência, ML para redes, DevOps para tuning SQL.
7. **Grupo G — Domínios Alienígenas Não Computacionais:** (15 casos) Gastronomia, futebol, vida doméstica, finanças pessoais.
8. **Grupo H — Trivia, Hardware e História:** (15 casos) Biografias de criadores, núcleos de CPU, ano de criação de software.
9. **Grupo I — Declaração de Experiência vs Demonstração:** (15 casos) "Trabalho há 10 anos com X" vs explicação operativa.
10. **Grupo J — Hipótese Especulativa:** (15 casos) "Acho que talvez dê para criar uma regra" vs certeza conceitual.
11. **Grupo K — Respostas Ultra-Concisas:** (15 casos) Respostas de 1 linha diretamente pertinentes (desafio ao length proxy).
12. **Grupo L — Jargão e Prolixidade sem Mecanismo (Buzzword Soup):** (20 casos) Respostas longas de 50+ palavras sem nexo funcional.
13. **Grupo M — Evasivas e Tautologias:** (15 casos) "Depende de muitos fatores estruturais".
14. **Grupo N — Ignorância e Filler:** (15 casos) "Não me recordo agora", "Sim, com certeza".
15. **Grupo O — Invariância de Representação:** (10 pares = 20 casos) Respostas formais vs coloquiais/gírias com idêntico conteúdo semântico.
16. **Grupo P — Mutações Semânticas Críticas:** (10 casos) Pares onde a remoção de uma única palavra inverte a adequação técnica.

---

## 9. Plano e Protocolo de Cegamento Estrito

O protocolo do Stage 31.7.13 deve garantir a separação metodológica absoluta:

```text
[Criador do Benchmark] ──> Arquivo com Gabarito (ground_truth.json) ──> SHA-256 Congelado
                                     │ (Gabarito Oculto)
                                     ▼
                            Dataset Cego (blind_input.json)
                            (apenas question_text + response_text)
                                     │
                                     ▼
[Executor Cego] ──────────> OpenDomainPropositionEngine
                                     │
                                     ▼
                            Predições do Motor (predictions.json)
                                     │
                                     ▼
[Comparador Independente] <──────────┘
(Compara Gabarito Congelado vs Predições)
         ↓
Matriz de Confusão & Métricas
```

### Regras de Cegamento:
1. O runtime sob teste (`reference_runtime/runtime.py`) NÃO pode ser alterado durante a validação.
2. O dataset cego fornecido ao executor deve conter estritamente `id`, `question_text` e `response_text`.
3. Os campos `expected_classification`, `expected_nexus` e `rationale` permanecem isolados no arquivo de gabarito.
4. O hash SHA-256 do gabarito deve ser calculado e registrado ANTES do início da execução das predições.
5. As predições geradas devem ser gravadas em disco antes da revelação do gabarito para confronto.

---

## 10. Separação entre Conjuntos de Dados

- **Conjunto de Desenvolvimento:** Os 17 casos de `test_stage_31_7_11_demand_proposition_nexus.py` e os 16 casos de `test_stage_31_7_8_open_domain_proposition_engine.py` permanecem como suíte de regressão de código.
- **Conjunto Histórico de Divergências:** Os 101 casos divergentes do Stage 31.7.9 pertencem ao histórico documental de RCA e NÃO devem ser reaproveitados como gabarito do benchmark cego.
- **Conjunto Cego do Stage 31.7.13:** Deve ser composto exclusivamente por casos inéditos (250 novos pares pergunta-resposta).
- **Proibição de Vazamento:** É expressamente proibido incorporar casos do benchmark cego aos testes de desenvolvimento antes da conclusão formal da validação e emissão do gate.

---

## 11. Métricas e Análise Pré-Definidas

Para evitar a falácia de avaliar apenas a concordância exata agregada, as seguintes métricas são obrigatórias para o Stage 31.7.13:

1. **Concordância Exata Global (Accuracy):**
   $$\text{Accuracy} = \frac{\sum \text{Concordâncias}}{250}$$
2. **Matriz de Confusão 7×7:**
   Cruzamento completo entre humano (ground truth) e sistema para todas as classes (`DIRECT`, `PARTIAL`, `SUPPORTING`, `RELATED`, `OFF_TOPIC`, `INSUFFICIENT`, `UNKNOWN`).
3. **Métricas Focais da Classe `DIRECT`:**
   - **Falsos DIRECT (Falsos Positivos de Relevância):** Respostas classificadas como `DIRECT` pelo sistema quando o humano atribuiu `RELATED`, `SUPPORTING`, `PARTIAL` ou `OFF_TOPIC`.
   - **Precisão de `DIRECT`:** $\frac{\text{True DIRECT}}{\text{True DIRECT} + \text{False DIRECT}}$.
   - **Recall de `DIRECT`:** $\frac{\text{True DIRECT}}{\text{True DIRECT} + \text{False Negative DIRECT}}$.
4. **Desempenho por Categoria Semântica:**
   Taxa de acerto segmentada por grupos temáticos (especialmente Grupo L - Buzzword Soup, Grupo K - Ultra-concisas, Grupo D - Observabilidade, Grupo E - Antítese).
5. **Taxa de Invariância de Representação:**
   Percentual de pares do Grupo O onde o sistema manteve a mesma classificação técnica apesar de variações drásticas de estilo e vocabulário.

---

## 12. Procedimento de Execução do Experimento

1. **Geração do Gabarito Cego:** Gerar `stage_31_7_13_ground_truth.json` com os 250 casos estratificados.
2. **Cálculo de Hash do Gabarito:** Registrar SHA-256 de `stage_31_7_13_ground_truth.json`.
3. **Geração da Entrada Cega:** Extrair `stage_31_7_13_blind_input.json` contendo apenas `id`, `question_text`, `response_text`.
4. **Execução Cega do Motor:** Executar script autônomo invocando `evaluate_open_domain_semantic_relevance(q, r)` para cada item, gerando `stage_31_7_13_system_predictions.json`.
5. **Cálculo de Hash das Predições:** Registrar SHA-256 de `stage_31_7_13_system_predictions.json`.
6. **Comparação e Auditoria:** Executar comparador independente confrontando gabarito e predições, gerando relatório de concordância e matriz de confusão.

---

## 13. Critérios de Aceite e Bloqueio para o Stage 31.7.13

### Condições para Aprovação (`GATE: INDEPENDENT_BLIND_SEMANTIC_REVALIDATION_COMPLETE`):
1. **Concordância Exata Global $\ge 75,0\%$** no benchmark de 250 casos.
2. **Taxa de Falsos `DIRECT` $\le 10,0\%$** do total de divergências (redução drástica frente aos 87,1% observados no Stage 31.7.9).
3. **Recall de `DIRECT` $\ge 85,0\%$** (garantindo que a correção de falsos positivos não destruiu a sensibilidade para respostas verdadeiramente pertinentes).
4. **Taxa de Invariância de Representação $\ge 80,0\%$** nos pares semanticamente equivalentes do Grupo O.
5. **Nenhum vazamento de gabarito ou quebra de cegamento.**

### Condições de Bloqueio (`GATE: INDEPENDENT_BLIND_SEMANTIC_REVALIDATION_BLOCKED`):
1. **Persistência de Falsos Positivos:** Se mais de 25 casos de `RELATED`, `SUPPORTING` ou `OFF_TOPIC` forem classificados como `DIRECT`.
2. **Hipercorreção por Falsos Negativos:** Se respostas genuinamente diretas (True DIRECT) forem maciçamente rebaixadas para `OFF_TOPIC` (Recall de `DIRECT` < 80%).
3. **Falha de Invariância:** Se o motor classificar uma resposta formal como `DIRECT` e sua paráfrase informal equivalente como `OFF_TOPIC` em mais de 20% dos pares de controle.
4. **Violação de Runtime:** Qualquer edição em `reference_runtime/runtime.py` durante o experimento.

---

## 14. Limitações Desta Etapa

1. **Auditoria Estática e Estrutural:** O Stage 31.7.12 é estritamente de auditoria de contratos e desenho de protocolo. Ele NÃO executa a validação cega nem altera o runtime.
2. **Não Substituição do Motor Legado:** O motor legado continua ativo como padrão. Nenhuma substituição é autorizada nesta etapa.
3. **Poder Amostral Dependente do Stage 31.7.13:** As conclusões estatísticas finais sobre a viabilidade de produção do `Demand-Proposition Nexus` dependem integralmente da execução do experimento cego no Stage 31.7.13.

---

## 15. Atualizações de Governança

- Atualizado [`START_HERE.md`](file:///d:/Projetos/TechLens/START_HERE.md) registrando a conclusão do Stage 31.7.12 e a prontidão do protocolo para o Stage 31.7.13.
- Atualizado [`GEMINI_HANDOFF.md`](file:///d:/Projetos/TechLens/GEMINI_HANDOFF.md) com a Seção 63 contendo os achados da auditoria e o desenho experimental.

---

## 16. Gate Final

```text
GATE: INDEPENDENT_CONTRACT_AUDIT_AND_BLIND_VALIDATION_DESIGN_COMPLETE
```

A implementação do Stage 31.7.11 foi formalmente auditada, os contratos arquiteturais foram comprovados no código real com suas limitações documentadas, e o protocolo experimental de validação cega independente foi integralmente especificado e está pronto para execução no Stage 31.7.13.

---

## 17. Próxima Etapa Recomendada

**Stage 31.7.13 — Independent Blind Semantic Revalidation Execution**

*Instrução de continuidade: A próxima etapa deve executar o protocolo cego de 250 casos definido neste artefato, mantendo o runtime 100% congelado e registrando os hashes dos artefatos antes e depois da execução.*
