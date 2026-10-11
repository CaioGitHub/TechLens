# Stage 31.7.17 — Independent Blind Semantic Revalidation of the Corrected Runtime

```text
STATUS: BLOCKED
GATE: BLIND_SEMANTIC_REVALIDATION_BLOCKED
TIMESTAMP: 2026-10-11T01:06:00-03:00
FROZEN RUNTIME SHA-256: AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB
BENCHMARK NOVELTY: 100% (200/200 cases novel vs Stage 31.7.13 historical benchmark)
BLIND EXECUTION STATUS: COMPLETED (200 predictions generated without ground truth access)
```

---

## 1. Objetivo e Escopo

O objetivo do **Stage 31.7.17** é executar uma validação semântica cega, independente e rigorosa do runtime congelado no **Stage 31.7.16** (`AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB`), avaliando sua capacidade de generalização em domínio aberto sobre 200 casos técnicos inéditos cobrindo as 7 classes taxonômicas de relevância:
- `DIRECT`
- `PARTIAL`
- `SUPPORTING`
- `RELATED`
- `OFF_TOPIC`
- `INSUFFICIENT`
- `UNKNOWN`

O princípio metodológico central desta etapa é:
> *Uma implementação aprovada em testes de desenvolvimento ainda precisa demonstrar generalização em validação independente.*

Conforme os guardrails do projeto:
- **Nenhuma alteração de código** foi realizada no runtime durante esta etapa.
- O benchmark foi adjudicado e selado previamente à execução.
- A execução do runtime foi realizada às cegas sobre entradas contendo unicamente `id`, `question_text` e `response_text`.
- Os critérios de aceitação foram mantidos estritamente idênticos aos definidos no Stage 31.7.15.

---

## 2. Integridade Obrigatória do Runtime

Antes do início de qualquer avaliação, a integridade do runtime foi auditada e congelada.

### 2.1 Verificação Criptográfica SHA-256
- **Comando executado:**
  ```powershell
  Get-FileHash -Algorithm SHA256 reference_runtime/runtime.py
  ```
- **Hash esperado (Stage 31.7.16):**
  `AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB`
- **Hash obtido:**
  `AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB`
- **Resultado:** **CONFORME (100% bit-a-bit idêntico)**.

Nenhuma linha de `reference_runtime/runtime.py` foi modificada antes, durante ou após a execução do benchmark.

---

## 3. Método de Construção do Benchmark Independente (200 Casos)

O benchmark de validação independente foi construído para assegurar **0% de contaminação** e **variação semântica real**:

1. **Checagem de Novidade Estrita:**
   - Comparação automatizada contra todos os 250 casos do Stage 31.7.13 (`stage_31_7_13_ground_truth.json`).
   - Verificação de 0 duplicatas textuais de perguntas e 0 duplicatas textuais de respostas.
2. **Diversidade Semântica e Sintática:**
   - Domínios técnicos variados: Sistemas Distribuídos (Raft, Paxos, Zab), Bancos de Dados (LSM, B-Tree, WAL, HNSW, ClickHouse, SQLite, PostgreSQL), Redes (HTTP/2, QUIC, TLS 1.3, TCP/UDP), Microsserviços e Arquitetura (Sagas, Outbox CDC, Circuit Breaker, Sharding).
   - Variação morfológica e estilística: voz ativa, voz passiva, construções pronominais reflexivas ("utiliza-se", "configura-se"), respostas concisas (curtas) e verbosas (longas), linguagem formal e coloquial/informal.
   - Polaridade e antíteses destrutivas: propostas ativas que quebram garantias operacionais (ex.: remover locks, desligar transações, desabilitar autenticação).
   - Domínios ortogonais e alienígenas: CSS/Tailwind, AI/Machine Learning (Scikit-Learn, Regressão, K-Means), pipelines de CI/CD em contextos de algoritmos, atividades cotidianas de culinária, esportes e lazer.
   - Respostas evasivas, vazias, monossilábicas e tautologias circulares puras.

---

## 4. Evidências de Independência das Referências

1. **Separação de Papéis:** As referências humanas de ground truth foram estabelecidas com base nas definições conceituais dos contratos semânticos (CTR-SEM-A até CTR-SEM-H) e gravadas com justificativas por demanda e aspecto satisfeito antes da execução do sistema.
2. **Selo Criptográfico Prévio:** O arquivo `stage_31_7_17_ground_truth.json` foi gerado e congelado com hash SHA-256 antes da execução do script de inferência.
3. **Ausência de Retroalimentação:** Nenhuma previsão do sistema foi usada para revisar, abrandar ou ajustar classes de referência.
4. **Tratamento de Incerteza e Ambiguidade:** Casos com potencial ambiguidade foram sinalizados explicitamente no campo `has_ambiguity`.

---

## 5. Distribuição dos 200 Casos por Classe e Grupo

| Classe de Referência | Quantidade | % do Total | Justificativa de Representatividade |
|---|---:|---:|---|
| `DIRECT` | 45 | 22.5% | Resolução funcional completa e operativamente válida da demanda. |
| `PARTIAL` | 35 | 17.5% | Resolução de apenas um dos aspectos de perguntas multi-demanda ou resposta incompleta. |
| `SUPPORTING` | 25 | 12.5% | Ferramentas auxiliares, telemetria, dashboards e alertas operacionais. |
| `RELATED` | 30 | 15.0% | Conexão temática sem mecanismo resolutivo (história, trivia, descrições institucionais). |
| `OFF_TOPIC` | 35 | 17.5% | Antíteses destrutivas (10), domínios técnicos ortogonais (15), domínios alienígenas (10). |
| `INSUFFICIENT` | 18 | 9.0% | Respostas evasivas, declarações de ignorância, fillers monossilábicos. |
| `UNKNOWN` | 12 | 6.0% | Tautologias circulares puras sem conteúdo explicativo discriminável. |
| **TOTAL** | **200** | **100.0%** | **Distribuição semanticamente balanceada e representativa.** |

---

## 6. Protocolo de Execução Cega

A execução seguiu estritamente o protocolo estipulado:
1. Geração do arquivo cego `scratch/stage_31_7_17_blind_input.json` contendo apenas `id`, `question_text` e `response_text`.
2. Execução do entrypoint canônico:
   ```python
   from reference_runtime.runtime import evaluate_open_domain_semantic_relevance
   pred = evaluate_open_domain_semantic_relevance(case["question_text"], case["response_text"])
   ```
3. Gravação das previsões em `stage_31_7_17_system_predictions.json` em execução única e ininterrupta (tempo total: 0.044 segundos para 200 casos).
4. Cálculo determinístico de métricas e divergências por script independente (`evaluate_stage_31_7_17_metrics.py`).

---

## 7. Hashes SHA-256 dos Artefatos

| Artefato | Caminho Canônico | Hash SHA-256 | Tamanho |
|---|---|---|---:|
| Runtime Congelado | `reference_runtime/runtime.py` | `AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB` | 216,562 B |
| Ground Truth Selado | `11 - .../stage_31_7_17_ground_truth.json` | `EDE7B2A93EE3A9B7A0920D77780FBC331F9BB488622432E03FD30C4C9731C7FD` | 175,174 B |
| Input Cego | `11 - .../stage_31_7_17_blind_input.json` | `4CE1ADF0EE197A0C0FA8A88F740F4EFA6F3A14FB360249579F4CFC1B19B6E576` | 69,666 B |
| Previsões do Sistema | `11 - .../stage_31_7_17_system_predictions.json` | `E42A5709A03D96F52FF60CF29FFAD7CD14FF969330F3E9F84C5752BD21F70AAB` | 108,461 B |
| Sumário de Métricas | `11 - .../stage_31_7_17_metrics_summary.json` | `E7A31D2D09BF799DB01F9EC70FFA77823B666AB61F69257740610542C86CB0BF` | 80,489 B |

---

## 8. Métricas Gerais

| Métrica | Numerador / Denominador | Percentual Obtido | Critério de Aceitação | Resultado |
|---|:---:|:---:|:---:|:---:|
| **Concordância Exata** | 124 / 200 | **62.00%** | $\ge 75.0\%$ | **FALHOU** |
| **Recall de DIRECT** | 40 / 45 | **88.89%** | $\ge 85.0\%$ | **ATINGIDO** |
| **Precisão de DIRECT** | 40 / 84 | **47.62%** | $\ge 70.0\%$ | **FALHOU** |
| **Falsos DIRECT entre Divergências** | 44 / 76 | **57.89%** | $\le 10.0\%$ | **FALHOU** |
| **Recall de PARTIAL** | 16 / 35 | **45.71%** | $\ge 60.0\%$ | **FALHOU** |
| **Invariância de Representação** | 8 / 13 | **61.54%** | $\ge 80.0\%$ | **FALHOU** |
| **Macro-F1** | Média das 7 classes | **55.24%** | Informativo | Informativo |

---

## 9. Matriz de Confusão Completa (7x7)

Linhas = **Referência Humana Selada**, Colunas = **Previsão do Runtime Candidate**:

| REF \ PRED | DIRECT | PARTIAL | SUPPORTING | RELATED | OFF_TOPIC | INSUFFICIENT | UNKNOWN | TOTAL |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **DIRECT** | **40** | 0 | 1 | 1 | 3 | 0 | 0 | **45** |
| **PARTIAL** | 14 | **16** | 0 | 0 | 5 | 0 | 0 | **35** |
| **SUPPORTING** | 0 | 0 | **24** | 0 | 1 | 0 | 0 | **25** |
| **RELATED** | 15 | 0 | 0 | **7** | 8 | 0 | 0 | **30** |
| **OFF_TOPIC** | 7 | 0 | 0 | 0 | **28** | 0 | 0 | **35** |
| **INSUFFICIENT** | 2 | 0 | 0 | 1 | 2 | **9** | 4 | **18** |
| **UNKNOWN** | 6 | 0 | 0 | 2 | 4 | 0 | **0** | **12** |
| **TOTAL PRED** | **84** | **16** | **25** | **11** | **51** | **9** | **4** | **200** |

---

## 10. Resultados Detalhados por Classe

| Classe | Casos Ref | Previstos | TP | FP | FN | Precisão | Recall | F1-Score |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `DIRECT` | 45 | 84 | 40 | 44 | 5 | 47.62% | 88.89% | 62.02% |
| `PARTIAL` | 35 | 16 | 16 | 0 | 19 | 100.00% | 45.71% | 62.75% |
| `SUPPORTING` | 25 | 25 | 24 | 1 | 1 | 96.00% | 96.00% | 96.00% |
| `RELATED` | 30 | 11 | 7 | 4 | 23 | 63.64% | 23.33% | 34.15% |
| `OFF_TOPIC` | 35 | 51 | 28 | 23 | 7 | 54.90% | 80.00% | 65.12% |
| `INSUFFICIENT` | 18 | 9 | 9 | 0 | 9 | 100.00% | 50.00% | 66.67% |
| `UNKNOWN` | 12 | 4 | 0 | 4 | 12 | 0.00% | 0.00% | 0.00% |

---

## 11. Resultados por Grupo Semântico

| Grupo Semântico | Descrição / Foco | Acertos / Total | Acurácia |
|---|---|:---:|:---:|
| `DIRECT_TECH` | Resoluções funcionais completas | 40 / 45 | 88.9% |
| `PARTIAL_COVERAGE` | Questões multi-aspecto e coberturas parciais | 16 / 35 | 45.7% |
| `SUPPORTING_MONITORING` | Monitoramento, telemetria e dashboards | 24 / 25 | **96.0%** |
| `RELATED_THEMATIC` | Conexões temáticas sem mecanismo operacional | 7 / 30 | 23.3% |
| `OFF_TOPIC_ANTITHESIS` | Ações ativas destrutivas | 7 / 10 | 70.0% |
| `OFF_TOPIC_ORTHOGONAL` | Cruzamento de domínios (CSS/ML/DevOps em BD) | 13 / 15 | 86.7% |
| `OFF_TOPIC_ALIEN` | Assuntos alienígenas (esportes, culinária, lazer) | 8 / 10 | 80.0% |
| `INSUFFICIENT_EVIDENCE` | Evasivas, desconhecimento explícito, fillers | 9 / 18 | 50.0% |
| `UNKNOWN_TAUTOLOGY` | Raciocínios circulares e tautologias | 0 / 12 | **0.0%** |

---

## 12. Resultados de Invariância de Representação

Foram avaliados 13 pares de equivalência semântica desenhados para testar variações de registro linguístico, concisão e flexão:

| Par de Invariância | IDs dos Casos | Variação Testada | Pred A | Pred B | Invariante? |
|---|---|---|:---:|:---:|:---:|
| **Par 1 (HNSW)** | `D01_vector_hnsw` <-> `D02_vector_hnsw_informal` | Formal vs Informal | DIRECT | DIRECT | **SIM** |
| **Par 2 (LSM)** | `D03_compaction_lsm` <-> `D04_compaction_lsm_active` | Impessoal vs Ativo 1ª pessoa | DIRECT | DIRECT | **SIM** |
| **Par 3 (Raft)** | `D05_raft_log_matching` <-> `D06_raft_log_matching_short` | Verboso vs Conciso | OFF_TOPIC | OFF_TOPIC | **SIM** |
| **Par 4 (Lock Fencing)** | `D07_distributed_lock_fencing` <-> `D08_distributed_lock_fencing_informal` | Formal vs Informal | DIRECT | OFF_TOPIC | **NÃO** |
| **Par 5 (Zero-Copy)** | `D09_kafka_zero_copy` <-> `D10_kafka_zero_copy_active` | Impessoal vs Ativo 1ª pessoa | DIRECT | DIRECT | **SIM** |
| **Par 6 (CRDT)** | `D11_crdt_pn_counter` <-> `D12_crdt_pn_counter_informal` | Formal vs Informal | DIRECT | DIRECT | **SIM** |
| **Par 7 (Sharding)** | `D13_database_sharding_virtual_nodes` <-> `D14_database_sharding_virtual_nodes_active` | Impessoal vs Ativo 1ª pessoa | DIRECT | DIRECT | **SIM** |
| **Par 8 (Outbox CDC)** | `D15_outbox_debezium_cdc` <-> `D16_outbox_debezium_cdc_informal` | Formal vs Coloquial ("tabelinha") | DIRECT | RELATED | **NÃO** |
| **Par 9 (Saga)** | `D17_saga_choreography_compensating` <-> `D18_saga_choreography_compensating_short` | Detalhado vs Resumido | DIRECT | DIRECT | **SIM** |
| **Par 10 (JDBC Pool)** | `D43_long_direct_detailed` <-> `D44_short_direct_concise` | Extenso vs Muito Curto | SUPPORTING | DIRECT | **NÃO** |
| **Par 11 (Omissão Texto)** | `P05_explicit_omission_text` <-> `P06_explicit_omission_text_informal` | Formal vs Informal | PARTIAL | PARTIAL | **SIM** |
| **Par 12 (Idempotência)** | `P11_multi_aspect_idempotency_storage` <-> `P12_multi_aspect_idempotency_storage_informal` | Pronominal vs Informal | DIRECT | PARTIAL | **NÃO** |
| **Par 13 (Antítese Locks)** | `O01_antithesis_drop_locks` <-> `O02_antithesis_drop_locks_inflected` | Ativo formal vs Flexionado 1ª p. | OFF_TOPIC | DIRECT | **NÃO** |

- **Total de Pares Avaliados:** 13
- **Pares com Previsão Idêntica:** 8
- **Taxa de Invariância:** **61.54%** (Critério: $\ge 80.0\%$ — **FALHOU**)

---

## 13. Análise Detalhada das Divergências (76 Casos)

As 76 divergências distribuem-se nos seguintes padrões semânticos:

### 13.1 Hipertrofia de Falsos DIRECTs (44 casos / 57.89% das divergências)
O motor candidate sofre de uma tendência estrutural severa a promover respostas para `DIRECT` sempre que detecta termos técnicos legítimos:
1. **Promoção de `PARTIAL` para `DIRECT` (14 casos):**
   - Exemplos: `P01`, `P02`, `P04`, `P07`, `P08`, `P09`, `P10`, `P11`, `P13`, `P14`, `P15`, `P25`, `P27`, `P30`, `P31`.
   - *Causa:* O motor identifica que a proposição satisfaz fortemente a primeira demanda e não realiza a conjunção estrita exigindo a satisfação de todas as demandas independentes da pergunta.
2. **Promoção de `RELATED` para `DIRECT` (15 casos):**
   - Exemplos: `R01` (Milvus HNSW), `R02` (ClickHouse), `R04` (SQLite), `R05` (False sharing), `R14` (Rust), `R15` (Java Virtual Threads), `R17` (DuckDB), `R18` (ClickHouse), `R20` (gRPC), `R21` (GraphQL), `R22` (Redis), `R23` (Elasticsearch), `R24` (Nginx), `R25` (SQLite), `R30` (Kafka).
   - *Causa:* As respostas descrevem fatos verídicos, origens, histórico ou definições de produto das ferramentas ("O Milvus é um projeto sob a Linux Foundation...", "O SQLite foi criado..."). O motor avalia que as entidades coincidem e assume que a resposta é operativa, confundindo *descrição temática* com *resolução mecânica*.
3. **Promoção de `OFF_TOPIC` para `DIRECT` (7 casos):**
   - Exemplos: `O02` (antítese de locks flexionada: "Removo qualquer bloqueio..."), `O05` (antítese kubernetes: "Desabilito todo o firewall..."), `O07` (antítese auth: "Retiro todos os limites..."), `O14` (Webpack em quórum), `O15` (CSS em WAL), `O34` (videogame com palavra "balancear"), `O35` (correios com "bancária").
   - *Causa:* Frases que usam verbos transitivos afirmativos sem detecção de polaridade destrutiva ("removo", "desabilito") ou que possuem vazamento léxico acidental de palavras-chave.
4. **Promoção de `UNKNOWN` (Tautologias) para `DIRECT` (6 casos):**
   - Exemplos: `U02` (deadlocks), `U04` (cache), `U05` (índices), `U08` (compressão), `U09` (isolamento), `U11` (particionamento).
   - *Causa:* As tautologias repetem as palavras da pergunta ("transações entram em espera mútua porque uma transação fica esperando a outra esperar"). O motor calcula alta sobreposição proposicional e conclui erroneamente que a resposta é `DIRECT`.
5. **Promoção de `INSUFFICIENT` para `DIRECT` (2 casos):**
   - Exemplos: `I11` (evasiva orçamentária: "depende da verba financeira..."), `I12` (evasiva de consultoria: "precisaria contratar uma consultoria especializada...").
   - *Causa:* Frases completas que aparentam estrutura proposicional, mas que não contêm substância técnica.

### 13.2 Falsos Negativos e Rebaixamentos Incorretos (32 casos)
1. **Rebaixamento de `DIRECT` (5 casos):**
   - `D05` e `D06` (Raft log matching): Rebaixados para `OFF_TOPIC`. O motor não reconheceu a garantia de quórum de log commitado do Raft como resolução direta de integridade.
   - `D08` (Lock fencing informal): Rebaixado para `OFF_TOPIC` pela presença de termos informais ("A gente associa um número sequencial...").
   - `D16` (Outbox CDC informal): Rebaixado para `RELATED` pela gíria "tabelinha auxiliar".
   - `D43` (JDBC pool detalhado): Classificado como `SUPPORTING` por mencionar HikariCP e timeout, ignorando a resolução do esgotamento de conexões.
2. **Rebaixamento de `PARTIAL` para `OFF_TOPIC` (5 casos):**
   - `P03`, `P18`, `P19`, `P20`, `P24`.
3. **Classificação Falha de `UNKNOWN` (12 casos / 0% de acerto):**
   - O runtime previu `UNKNOWN` para apenas 4 casos de todo o benchmark (todos eles casos `INSUFFICIENT`), e errou **100% dos 12 casos de tautologia circular** (`UNKNOWN_TAUTOLOGY`), distribuindo-os entre `DIRECT` (6), `OFF_TOPIC` (4) e `RELATED` (2). O motor não possui detector de raciocínio circular.
4. **Confusão entre `INSUFFICIENT` e `UNKNOWN` (4 casos):**
   - Evasivas vagas como "A gente descobre olhando logs..." (`I09`) ou "É uma fila apenas" (`I13`) classificadas como `UNKNOWN` em vez de `INSUFFICIENT`.

---

## 14. Causas-Raiz Observadas e Grau de Confiança

| Causa-Raiz | Mecanismo Observado no Runtime | Impacto | Grau de Confiança |
|---|---|---|:---:|
| **CR-01: Ausência de Detector de Tautologia / Circularidade** | O motor compara termos da pergunta com a resposta. Uma tautologia que repete os termos centrais gera alto score de nexo sem adicionar conteúdo explicativo. | 0% acerto em UNKNOWN (6 Falsos DIRECTs) | **MUITO ALTO** |
| **CR-02: Confusão entre Descrição de Entidade e Resolução Operacional** | Quando o candidato cita uma tecnologia e descreve sua história, criador ou características gerais, o motor considera que o tema foi atendido diretamente. | 15 Falsos DIRECTs em RELATED | **MUITO ALTO** |
| **CR-03: Falha na Conjunção Multi-Aspecto** | O motor trata o atendimento de 1 demanda como suficiente para declarar `DIRECT`, ignorando omissões explícitas de aspectos secundários. | 14 Falsos DIRECTs em PARTIAL | **MUITO ALTO** |
| **CR-04: Insensibilidade à Polaridade Destrutiva** | O motor não distingue ações que protegem o sistema daquelas que removem as proteções essenciais ("desativo todos os locks", "removo rate limiting"). | 3 Falsos DIRECTs em OFF_TOPIC | **ALTO** |
| **CR-05: Vulnerabilidade a Variações Informais** | O uso de termos coloquiais ("a gente", "tabelinha", "dar tela preta") faz o motor perder o nexo e rebaixar respostas corretas para OFF_TOPIC ou RELATED. | Quebra em 5 dos 13 pares de invariância | **ALTO** |

---

## 15. Limitações Metodológicas

1. **Benchmark Fechado de 200 Casos:** Embora 100% inédito em relação ao histórico de 250 casos, o benchmark de 200 casos reflete domínios selecionados pela equipe de engenharia e pode conter sensibilidade a distribuições sintáticas específicas.
2. **Adjudicação Manual de Ground Truth:** As referências foram estabelecidas com base nas especificações dos contratos semânticos por engenheiro especialista. Não houve adjudicação por duplo-cego de dois avaliadores independentes com medição de Cohen's Kappa, o que representa uma limitação de independência formal.
3. **Ausência de Modelo de Linguagem de Alta Capacidade (LLM):** O runtime utiliza heurísticas algorítmicas de extração proposicional em Python puro, o que impõe limites estruturais severos na detecção de sutilezas pragmáticas como ironia, circularidade semântica e antíteses complexas.

---

## 16. Resultado da Regressão Canônica

A suíte canônica de testes e o Reference Harness foram executados integralmente após a validação cega sobre o runtime intacto:

1. **Testes Unitários e de Integração:**
   - **Comando:** `py -m unittest discover -s tests -p "test_*.py"`
   - **Total de testes:** 1.024
   - **Passaram:** 1.023
   - **Pulados:** 1 (skip configurado intencionalmente)
   - **Falhas / Erros:** **0**
   - **Tempo de execução:** 33.028 segundos.
2. **Reference Harness:**
   - **Comando:** `py run_reference_harness.py --shared-workspace`
   - **Resultado:** `PASS_WITH_WARNINGS (8/8 suites, 0 failed)`.

A integridade do código legado e a compatibilidade regressiva permanecem 100% preservadas.

---

## 17. Comparação com o Stage 31.7.13 (Benchmark Histórico)

| Dimensão | Stage 31.7.13 (Histórico 250 casos) | Stage 31.7.17 (Independente 200 casos) | Variação / Diagnóstico |
|---|:---:|:---:|---|
| **Base de Casos** | 250 casos históricos | 200 casos 100% inéditos | Domínio completamente novo |
| **Concordância Exata** | 56.40% | **62.00%** | +5.60 p.p. (avanço real, porém insuficiente) |
| **Recall de DIRECT** | 76.36% | **88.89%** | +12.53 p.p. (atingiu a meta $\ge 85\%$) |
| **Precisão de DIRECT** | 47.73% | **47.62%** | -0.11 p.p. (estagnação grave em falsos positivos) |
| **Falsos DIRECTs** | 46 / 109 (42.20%) | 44 / 76 (**57.89%**) | Piora percentual entre divergências |
| **Recall de PARTIAL** | 46.15% | **45.71%** | Estagnado abaixo da meta ($\ge 60\%$) |
| **Invariância** | 63.64% | **61.54%** | Estagnado abaixo da meta ($\ge 80\%$) |

*Conclusão da Comparação:* As correções do Stage 31.7.16 resolveram com sucesso o problema de Recall de DIRECT (que subiu para 88.89%), mas **não resolveram a hipertrofia de falsos DIRECTs** (Precisão 47.62%, taxa entre divergências 57.89%), demonstrando que o motor continua promovendo respostas parciais, relacionadas, antíteses e tautologias para DIRECT.

---

## 18. Avaliação Individual dos Critérios de Aceitação

| Critério | Métrica Avaliada | Alvo Estabelecido | Valor Real Obtido | Veredito Individual |
|---|---|:---:|:---:|:---:|
| **CRIT-01** | Concordância Exata | $\ge 75.0\%$ | 62.00% (124/200) | **FALHOU** |
| **CRIT-02** | Recall de DIRECT | $\ge 85.0\%$ | 88.89% (40/45) | **APROVADO** |
| **CRIT-03** | Precisão de DIRECT | $\ge 70.0\%$ | 47.62% (40/84) | **FALHOU** |
| **CRIT-04** | Falsos DIRECTs entre Divergências | $\le 10.0\%$ | 57.89% (44/76) | **FALHOU** |
| **CRIT-05** | Recall de PARTIAL | $\ge 60.0\%$ | 45.71% (16/35) | **FALHOU** |
| **CRIT-06** | Invariância de Representação | $\ge 80.0\%$ | 61.54% (8/13) | **FALHOU** |
| **CRIT-07** | Regressão Canônica | 0 falhas | 0 falhas (1024 testes OK, Harness 8/8) | **APROVADO** |

---

## 19. Gate Final

Em estrito cumprimento das regras operacionais e metodológicas do projeto:
- O protocolo de validação cega foi executado sem contaminação e sem violação do congelamento do runtime.
- 5 dos 7 critérios de aceitação quantitativos **não foram atingidos**.
- O motor de relevância semântica em domínio aberto demonstrou progresso em sensibilidade (Recall de DIRECT 88.89%), mas falhou criticamente em especificidade (Precisão de DIRECT 47.62%, Falsos DIRECTs 57.89%, Recall de PARTIAL 45.71%).

Portanto, o gate oficial e mandatório emitido para o Stage 31.7.17 é:

```text
================================================================================
GATE FINAL: BLIND_SEMANTIC_REVALIDATION_BLOCKED
================================================================================
```

---

## 20. Próxima Etapa Recomendada

Conforme a Seção 14 do protocolo:
> *"Se a validação for executada validamente e resultar em `BLIND_SEMANTIC_REVALIDATION_BLOCKED`, a próxima etapa deverá ser uma RCA específica para os erros observados no Stage 31.7.17."*

A próxima etapa é:
**Stage 31.7.18 — Root Cause Analysis & Remediation Architecture for Propositional Precision, Tautology Detection and Demand Conjunctive Satisfaction.**

Nenhuma alteração no runtime deve ser feita sem a formalização prévia dessa RCA e de seu respectivo plano de correção controlado.
