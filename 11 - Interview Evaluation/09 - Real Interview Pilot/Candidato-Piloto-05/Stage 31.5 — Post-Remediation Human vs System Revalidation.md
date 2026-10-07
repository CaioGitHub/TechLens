# Stage 31.5 — Post-Remediation Human vs System Revalidation

## Status do Gate

```text
POST_REMEDIATION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED
```

### Justificativa Executiva

A validação cega e independente entre a avaliação humana estruturada e o Reference Evaluation Engine pós-implementação do Modelo de Pertinência Semântica (Stage 31.4.2) demonstrou avanços metodológicos expressivos, mas revelou **duas classes estruturais de falha** que impedem o gate `COMPLETE` segundo os critérios contratuais da Seção 35:

1. **Avanços Confirmados na Amostra Real (Candidato-Piloto-05)**:
   - O Mean Absolute Error (MAE) contra a referência humana manteve-se em **`0.64`** (`0.6364`), idêntico à calibração do Stage 31.2 e substancialmente superior ao Stage 31 histórico (`MAE 2.01`).
   - Média do sistema: **`5.55`** vs referência humana **`5.09`** (diferença de médias de apenas `+0.46`). Mediana do sistema: **`5.85`** vs humana **`5.00`**.
   - Concordância exata de score obtida em **4 questões (Q1, Q3, Q9, Q11 = 4.00)**, comprovando que declarações de experiência desprovidas de demonstração prática e ausência de sinais negativos não são mais indevidamente promovidas (eliminação dos Problemas A, D, E e F do Stage 31).
   - Casos históricos de pertinência semântica **D2 (Docker → Kubernetes)**, **D3 (SQL → Redis)** e **L1 (Dependency Injection → Spring Data)** são agora classificados corretamente como `OFF_TOPIC` e `RELATED` sem nenhuma regra de par tecnológico (`docker ↔ kubernetes`, `sql ↔ redis`) e sem closed vocabulary rígido.

2. **Causas do Bloqueio (Critérios da Seção 35)**:
   - **Presença de Word-Count Proxy em Verificação Semântica**: No runtime (`reference_runtime/runtime.py`, linhas 1184 e 1239), a verificação de perguntas multi-aspecto utiliza a heurística `len(r_words_list) <= 6` para classificar respostas parciais.
   - **Nova Classe Estrutural de Falso Positivo (`SYSTEM_FALSE_POSITIVE`)**: Quando uma resposta possui 7 ou mais palavras e aborda apenas o aspecto inicial de uma pergunta de múltiplas partes (ex.: Istio com mTLS omitindo roteamento canário; Nomad com scheduling omitindo failover; cache em memória omitindo invalidação), a condição `len <= 6` falha e o sistema promove a resposta a **`DIRECT`** em vez de **`PARTIAL`**.
   - **Nova Classe Estrutural de Falso Negativo (`SYSTEM_FALSE_NEGATIVE`)**: Na avaliação de conceitos de domínio aberto sem tecnologia nomeada, o algoritmo calcula a interseção exata de tokens (`q_words & r_words`) sem lematização ou stemming. Respostas técnicas válidas que utilizam flexões verbais ou nominais padrão da língua portuguesa (ex.: *correlacionar* na pergunta vs *correlação* na resposta; *retries* vs *repetições*) resultam em interseção vazia e são indevidamente rebaixadas para **`OFF_TOPIC`**.
   - **Colisão de Substring em Demandas de Domínio**: A verificação `any(d_term in q_lower for d_term in cap["demands"])` para `data_access_abstraction` contém o termo `"orm"`, que colide como substring na palavra `"performance"` (perf-orm-ance), sequestrando perguntas gerais de monitoramento de performance para o domínio de ORM e classificando respostas legítimas de latência como `OFF_TOPIC`.

Conforme a **Seção 4** deste protocolo, o runtime e os testes permaneceram estritamente congelados durante a validação. Nenhuma alteração foi introduzida no modelo para forçar aprovação artificial. O bloqueio é registrado e detalhado com rigor para subsidiar a correção controlada no Stage 31.6.

---

## 1. Runtime Validated

A validação foi executada sobre o runtime de referência congelado após a conclusão do Stage 31.4.2:

- **Arquivo do Runtime**: `reference_runtime/runtime.py`
- **Runtime SHA-256**: `21bb1f9e9c8536701751017f65158d9bb9024104a3d25083f4ee9de21ced8d71`
- **Mecanismos Auditados**:
  - `_evaluate_semantic_relevance(question, response)`: Modelo conceitual de pertinência de 7 classes.
  - `_FUNCTIONAL_CAPABILITIES`: Dicionário de domínios funcionais baseado em capacidades (sem regras de pares).
  - `_blind_dimensions(question, response, evidence)`: Avaliação dimensional desacoplada.
  - `_blind_evidence_specs(question, response)`: Extração de evidências e qualificações.
- **Congelamento Estrito**: Nenhuma linha do runtime, rubrica, modelo semântico ou oráculo humano foi alterada durante o Stage 31.5.

---

## 2. Blindness

A condição de **avaliação cega independente** foi integralmente assegurada:

1. **Sem Acesso a Metas**: O executor da pipeline e os módulos de avaliação do runtime operaram exclusivamente sobre os textos transcritos das perguntas e respostas.
2. **Ausência de Metadados nos Casos Adversariais**: Nenhuma fixture de teste continha scores humanos, rótulos esperados, pesos ou metadados de oráculo (`expected_score`, `human_score`, `evaluation_specs`).
3. **Isolamento do Comparador**: A comparação entre os resultados do sistema e as referências humanas foi executada por uma camada analítica externa, preservando o desacoplamento do motor de scoring.

---

## 3. Human Reference

A referência humana independente utilizada neste estágio é a avaliação estruturada congelada no **Stage 31**:

- **Artefato Canônico**: `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/Stage 31 — Human Evaluation Independent.md`
- **Human Reference SHA-256**: `bb57672224368ee0d56134d456d8dfe8fc93674457fac84e68f63bfe88593331`
- **Transcrição de Entrada**: `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-01/Pilot Input - Source Transcript v3.md`
- **Source Transcript SHA-256**: `cc4f32704bfbbca7261b3637f04b36e6950850c2f07d00f4a3b4a89559a51523`
- **Scores Humanos Congelados**:
  `[Q1: 4.0, Q2: 7.0, Q3: 4.0, Q4: 8.0, Q5: 2.0, Q6: 5.0, Q7: 5.0, Q8: 7.0, Q9: 4.0, Q10: 6.0, Q11: 4.0]`
  - Média Humana: **`5.09`**
  - Mediana Humana: **`5.00`**
  - Desvio Padrão Humano: **`1.70`**

Nenhum score humano foi ajustado retroativamente para favorecer a concordância do sistema.

---

## 4. Stage 31 Comparison

A tabela a seguir compara o comportamento do sistema através dos estágios da jornada de avaliação no piloto real (**Candidato-Piloto-05**):

| Questão | Tema Central | Human (Stg 31) | System (Stg 31) | System (Stg 31.2) | System (Stg 31.5) | Diff Stg 31.5 (Sys - Hum) | Classificação da Divergência |
|---|---|:---:|:---:|:---:|:---:|:---:|---|
| **Q1** | Trajetória / Java / Spring | 4.0 | 6.00 | 4.00 | **4.00** | **+0.00** | EXACT_AGREEMENT |
| **Q2** | CSS / Front-end | 7.0 | 7.00 | 7.05 | **7.05** | **+0.05** | MINIMAL_DISAGREEMENT |
| **Q3** | Banco de Dados / SQL | 4.0 | 6.00 | 4.00 | **4.00** | **+0.00** | EXACT_AGREEMENT |
| **Q4** | Java 21 / Virtual Threads | 8.0 | 8.00 | 7.05 | **7.05** | **-0.95** | VALID_TECHNICAL_DISAGREEMENT |
| **Q5** | REST Produces / Consumes | 2.0 | 7.05 | 4.45 | **4.45** | **+2.45** | VALID_TECHNICAL_DISAGREEMENT |
| **Q6** | JDBC / Banco | 5.0 | 7.00 | 5.85 | **5.85** | **+0.85** | VALID_TECHNICAL_DISAGREEMENT |
| **Q7** | Concorrência / Sincronização | 5.0 | 6.00 | 6.00 | **6.00** | **+1.00** | VALID_TECHNICAL_DISAGREEMENT |
| **Q8** | CI/CD / Jenkins | 7.0 | 8.00 | 7.05 | **7.05** | **+0.05** | MINIMAL_DISAGREEMENT |
| **Q9** | Arquitetura Hexagonal / SOLID | 4.0 | 6.00 | 4.00 | **4.00** | **+0.00** | EXACT_AGREEMENT |
| **Q10** | Investigação de Erro 500 | 6.0 | 7.00 | 7.65 | **7.65** | **+1.65** | DIMENSION_INTERPRETATION |
| **Q11** | IA Generativa / Adoção | 4.0 | 6.20 | 4.00 | **4.00** | **+0.00** | EXACT_AGREEMENT |

### Métricas Agregadas Comparativas

| Métrica | Stage 31 (Inicial) | Stage 31.2 (Pós-Correção) | Stage 31.5 (Pós-Redesign Semântico) |
|---|:---:|:---:|:---:|
| **Média do Sistema** | 6.93 | 5.55 | **5.55** |
| **Média Humana** | 5.09 | 5.09 | **5.09** |
| **Diferença das Médias** | +1.84 | +0.46 | **+0.46** |
| **Mediana do Sistema** | 7.05 | 5.85 | **5.85** |
| **Mediana Humana** | 5.00 | 5.00 | **5.00** |
| **MAE (Mean Absolute Error)** | **2.01** | **0.64** | **0.64** (`0.6364`) |
| **Diferença Máxima** | 5.05 (Q5) | 2.45 (Q5) | **2.45** (Q5) |
| **Divergências Materiais ($> 1.0$)** | 6 questões | 2 questões (Q5, Q10) | **2 questões** (Q5, Q10) |
| **Concordâncias Exatas ($\Delta = 0.0$)** | 0 questões | 4 questões (Q1, Q3, Q9, Q11) | **4 questões** (Q1, Q3, Q9, Q11) |

---

## 5. Historical Divergences

A revalidação auditou explicitamente os casos históricos de deficiência semântica identificados no Stage 31.3 e analisados no Stage 31.4:

### D2 — Docker → Kubernetes
- **Pergunta**: *"Como funciona Docker?"* (Demanda: `container_isolation`)
- **Resposta**: *"Kubernetes orquestra containers em clusters."*
- **Classificação no Stage 31.5**: **`OFF_TOPIC`** (`relation_type: alien_functional_domain`, `functional_contribution: False`, `evidence_strength: NONE`).
- **Auditoria de Regra**: Confirmada a ausência de par `docker ↔ kubernetes`. A exclusão decorre da verificação de que `container_orchestration` é um domínio alienígena não demandado pela questão.

### D3 — SQL → Redis
- **Pergunta**: *"Explique SQL."* (Demanda: `data_access_abstraction`)
- **Resposta**: *"Redis armazena dados em memória como chave e valor."*
- **Classificação no Stage 31.5**: **`OFF_TOPIC`** (`relation_type: alien_functional_domain`, `functional_contribution: False`, `evidence_strength: NONE`).
- **Auditoria de Regra**: Não existe regra `sql ↔ redis`. `in_memory_caching` é tratado como capacidade alienígena não requisitada.

### L1 — Dependency Injection → Spring Data
- **Pergunta**: *"Como funciona Dependency Injection?"* (Demanda: `dependency_injection_ioc`)
- **Resposta**: *"Spring Data fornece abstrações para acesso a bancos de dados."*
- **Classificação no Stage 31.5**: **`RELATED`** (`relation_type: thematic_adjacency_without_mechanism`, `functional_contribution: False`, `evidence_strength: NONE`).
- **Auditoria de Avaliação**: O sistema qualifica o candidate como `Insufficient` / `Weak` em correctness, não atribuindo crédito de demonstração conceitual ou prática meramente por pertencer ao ecossistema Spring.

### Resolução dos Problemas A–F do Stage 31
- **Problema A (Declaração tratada como demonstração)**: Corrigido. Em Q1, Q3, Q9 e Q11, menções verbais isoladas de tecnologias foram qualificadas como `experience_declaration(insufficient)`, garantindo nota 4.0.
- **Problema B (Fragmento tratado como resposta completa)**: Corrigido.
- **Problema C (Resposta relacionada tratada como direta)**: Corrigido via separação entre `DIRECT`, `SUPPORTING` e `RELATED`.
- **Problema D (Ausência de sinais negativos tratada como evidência positiva)**: Corrigido.
- **Problema E (Fallback conceitual positivo)**: Corrigido. O fallback agora exige substância técnica articulada.
- **Problema F (Nome de tecnologia como proxy de domínio)**: Corrigido.

---

## 6. New Adversarial Validation

Foi criada e executada uma suíte adversarial ampla e independente em [`tests/test_stage_31_5_revalidation.py`](file:///d:/Projetos/TechLens/tests/test_stage_31_5_revalidation.py), contendo **74 casos de teste** cobrindo domínios variados e todas as 7 classes canônicas:

```text
Total de testes executados: 74
Passaram: 62 (83.8%)
Falharam: 12 (16.2%)
```

### Distribuição dos Casos Adversariais

| Classe Taxonômica | Casos Planejados | Casos Executados | Casos Aprovados | Falhas Identificadas |
|---|:---:|:---:|:---:|:---:|
| **DIRECT** | $\ge 10$ | 10 | 5 | 5 (gap morfológico / colisão substring) |
| **PARTIAL** | $\ge 10$ | 10 | 4 | 6 (word count proxy $\le 6$ / gap morfológico) |
| **SUPPORTING** | $\ge 10$ | 10 | 9 | 1 (mismatch de intenção investigativa) |
| **RELATED** | $\ge 10$ | 10 | 10 | 0 |
| **OFF_TOPIC** | $\ge 10$ | 10 | 10 | 0 |
| **INSUFFICIENT** | $\ge 5$ | 5 | 5 | 0 |
| **UNKNOWN** | $\ge 5$ | 5 | 5 | 0 |
| **Invariância & Semântica** | $\ge 10$ | 10 | 10 | 0 |
| **Auditoria Piloto 05** | $\ge 4$ | 4 | 4 | 0 |
| **Total** | **$\ge 60$** | **74** | **62** | **12** |

---

## 7. Unknown Technologies

Foram testados 10 casos envolvendo tecnologias **estritamente ausentes do vocabulário do runtime**:

1. **Temporal**: Workflows distribuídos com event sourcing (`DIRECT` — PASS).
2. **NATS**: Pub/sub de altíssimo throughput e baixa latência (`DIRECT` — PASS).
3. **ClickHouse**: Banco analítico colunar com compressão vetorial (`DIRECT` — PASS).
4. **Pulumi**: Infraestrutura como código com linguagens de programação (`DIRECT` — PASS).
5. **Vault**: Gerenciamento de segredos dinâmicos e leases (`DIRECT` — PASS).
6. **OpenTelemetry**: Rastreabilidade distribuída e propagação de spans (`PARTIAL` — PASS).
7. **ArgoCD**: GitOps declarativo sem checagem de health checks (`PARTIAL` — PASS).
8. **Istio**: Malha de serviços com mTLS omitindo roteamento canário (`PARTIAL` — **FAIL / Falso Positivo** devido ao word-count proxy).
9. **Nomad**: Orquestrador leve omitindo failover (`PARTIAL` — **FAIL / Falso Positivo** devido ao word-count proxy).
10. **Dapr**: Sidecar com APIs padronizadas sem detalhar estado (`PARTIAL` — PASS).

**Achado**: O sistema processa tecnologias desconhecidas através do mecanismo de domínio aberto (`open_demonstrated_domain`), demonstrando que não há dependência de listas fechadas para casos `DIRECT` e `RELATED`. No entanto, quando a questão exige múltiplos aspectos, o runtime sofre do bug do word-count proxy.

---

## 8. Technology-Free Concepts

Foram executados 10 testes com conceitos formulados **sem menção ao nome da tecnologia**:

1. **Desacoplamento de instanciação**: Inversão de dependência sem citar Spring/DI (`DIRECT` — PASS).
2. **Bufferização assíncrona**: Fila para amortecer picos sem citar Kafka/Rabbit (`DIRECT` — PASS).
3. **Expiração de cache**: Armazenamento temporário com TTL sem citar Redis (`DIRECT` — PASS).
4. **Isolamento de falhas**: Bulkhead sem citar Resilience4j (`DIRECT` — PASS).
5. **Controle de concorrência otimista**: Versionamento para evitar conflito concorrente (`DIRECT` — **FAIL / Falso Negativo** devido a *atualizações* vs *atualização*).
6. **Correlação distribuída**: Propagação de header HTTP em microsserviços (`DIRECT` — **FAIL / Falso Negativo** devido a *correlacionar* vs *correlação*).
7. **Idempotência**: Chave única para evitar cobrança duplicada (`DIRECT` — **FAIL / Falso Negativo** devido a ausência de overlap léxico exato entre pergunta e resposta).
8. **Consistência eventual**: Reconciliação entre sistemas assíncronos (`DIRECT` — **FAIL / Falso Negativo** devido a ausência de overlap léxico exato).
9. **Detecção de regressão de latência**: Monitoramento de percentil p99 pós-deploy (`DIRECT` — **FAIL / Falso Negativo** devido a colisão de substring de `"orm"` em `"performance"`).
10. **Retry com backoff**: Repetições com intervalo crescente omitindo jitter (`PARTIAL` — **FAIL / Falso Negativo** devido a *retries* vs *repetições*).

---

## 9. Supporting vs Related

Foi avaliada a fronteira sutil entre contribuição funcional e adjacência passiva:

- **Cenário de Investigação de HTTP 500**:
  - *Resposta*: *"Eu começaria correlacionando logs, traces e métricas da requisição para identificar em qual etapa a falha ocorreu."*
  - *Classificação*: **`SUPPORTING`** (`functional_contribution: True`, `evidence_strength: STRONG`).
- **Cenário Adjacente no mesmo Contexto**:
  - *Resposta*: *"A aplicação utiliza Spring Data para persistência."*
  - *Classificação*: **`RELATED`** (`functional_contribution: False`, `evidence_strength: NONE`).

O sistema diferencia corretamente ações funcionais ativas de meras menções de ecossistema na esmagadora maioria dos cenários de investigação e resiliência.

---

## 10. Representation Invariance

Foram validadas variações estilísticas e representacionais mantendo a equivalência semântica:

1. **Curta vs Longa**:
   - Resposta concisa: *"Usaria retry com backoff exponencial."*
   - Resposta detalhada: Explicação longa dos mesmos conceitos.
   - Ambas recebem a mesma qualificação dimensional e classificação de pertinência.
2. **Formal vs Informal vs Coloquial**:
   - Formal: *"Trata-se de um erro interno no servidor decorrente de exceção não tratada."*
   - Coloquial: *"É tipo quando o back-end quebra e dá ruim na requisição."*
   - Ambas foram reconhecidas como conceitualmente válidas em correctness, sem penalização pelo estilo informal.
3. **Com Jargão vs Sem Jargão**:
   - O uso excessivo de buzzwords sem mecanismo (ex.: *"arquitetura reativa distribuída com DDD e CQRS"*) foi devidamente qualificado como `insufficient`, não obtendo pontuação elevada.

---

## 11. Experience Semantics

A hierarquia epistêmica foi verificada em progressões controladas:

1. **Declaração**: *"Já trabalhei bastante com Kubernetes."*
   - Evidência: `experience_declaration` (`qualification: insufficient`).
   - Score resultante: `4.0` (sem crédito prático).
2. **Hipótese**: *"Se ocorresse esse problema, eu configuraria probes e escalaria os pods."*
   - Evidência: `hypothesis` (`qualification: conditional`).
   - Não promovido a experiência demonstrada.
3. **Demonstração Prática**: *"Em produção, configuramos probes de liveness e readiness, investigamos restart loops no deployment e ajustamos os limites de CPU."*
   - Evidência: `demonstrated_experience` (`qualification: positive`).
   - Concede pontuação plena na dimensão de aplicação prática.

---

## 12. False Positives

### Análise Detalhada da Nova Classe Estrutural de Falso Positivo

- **Manifestação**: O sistema atribui `classification: DIRECT` a respostas que respondem a apenas um aspecto de uma pergunta composta.
- **Casos Comprovados**:
  - `test_partial_03_unseen_istio_omits_routing`: Pergunta pedia Istio e configuração de canary routing. Resposta abordou apenas mTLS e segurança (7 palavras). Classificada como `DIRECT`.
  - `test_partial_04_unseen_nomad_omits_failover`: Pergunta pedia Nomad e failover automático. Resposta abordou apenas agendamento de containers (7 palavras). Classificada como `DIRECT`.
  - `test_partial_08_tech_free_cache_omits_invalidation`: Pergunta pedia aceleração com cache e estratégias de invalidação. Resposta abordou apenas armazenamento em memória (7 palavras). Classificada como `DIRECT`.
  - `test_partial_09_tech_free_sharding_omits_resharding`: Pergunta pedia sharding e rebalanceamento de partições. Resposta abordou apenas particionamento por hash (10 palavras). Classificada como `DIRECT`.
- **Causa-Raiz**:
  Em `reference_runtime/runtime.py` (linhas 1183–1187 e 1238–1242):
  ```python
  if is_multi_aspect and (
      len(r_words_list) <= 6
      or ("trade-off" in q_lower and ...)
  ):
      return {"classification": "PARTIAL", ...}
  return {"classification": "DIRECT", ...}
  ```
  O autor da implementação utilizou a contagem de palavras ($\le 6$) como proxy para decidir se a resposta omitiu o segundo aspecto. Quando a resposta possui 7 ou mais palavras, a condição falha e o sistema assume erroneamente que todos os aspectos foram cobertos, promovendo a resposta a `DIRECT`.

---

## 13. False Negatives

### Análise Detalhada da Nova Classe Estrutural de Falso Negativo

- **Manifestação**: O sistema classifica como `OFF_TOPIC` respostas técnicas diretas e pertinentes formuladas em domínio aberto.
- **Casos Comprovados**:
  1. **Lacuna Morfológica (Falta de Stemming/Lematização)**:
     - `test_direct_06`: Pergunta contém *"atualizações"*, resposta contém *"atualização"*; pergunta contém *"concorrentes"*, resposta contém *"concorrência"*.
     - `test_direct_07`: Pergunta contém *"correlacionar"*, resposta contém *"correlação"*.
     - `test_partial_06`: Pergunta contém *"retries"*, resposta contém *"repetições"*.
     - Como o algoritmo faz interseção exata de strings `q_words & r_words`, a interseção resulta em `set()` vazio, ativando a cláusula `disjunct_open_domain` (`OFF_TOPIC`).
  2. **Variação Lexical / Paráfrase Semântica**:
     - `test_direct_08`: Pergunta aborda pagamento duplicado em retry; resposta propõe chave de idempotência por transação. Nenhum token chave compartilhado $\rightarrow$ `OFF_TOPIC`.
     - `test_direct_09`: Pergunta aborda sincronização sem transação compartilhada; resposta propõe consistência eventual e reconciliação. Sem overlap exato $\rightarrow$ `OFF_TOPIC`.
  3. **Colisão de Substring em Demandas Funcionais**:
     - `test_direct_10`: Pergunta continha a palavra *"performance"*.
     - O domínio `data_access_abstraction` possui em `demands` a string `"orm"`.
     - Como a verificação era `any(d_term in q_lower for d_term in cap["demands"])`, `"orm"` foi encontrado dentro de `"perf-orm-ance"`.
     - O sistema fixou incorretamente o domínio alvo como `data_access_abstraction` e rejeitou a resposta sobre latência e p99 como alienígena (`OFF_TOPIC`).

---

## 14. Determinism

A repetibilidade estrita foi verificada por execução triplicada do pipeline de avaliação sobre o conjunto adversarial e sobre o piloto real:

```text
Run 1 (Hash de Saída) == Run 2 (Hash de Saída) == Run 3 (Hash de Saída)
Variabilidade de Score: 0.00
Variabilidade de Evidências: 0.00
Determinismo: 100% PASS
```

---

## 15. Isolation

O isolamento foi verificado por execução com permutação aleatória de ordem de testes e execução em workspaces duplicados temporários via `run_reference_harness.py`:

- A ordem de processamento das entrevistas e perguntas não alterou nenhum resultado.
- Inexistência de vazamento de estado global ou contaminação de cache entre instâncias.

---

## 16. Regression

A regressão em toda a base de testes foi executada:

1. **Testes do Runtime de Referência (`run_reference_runtime_tests.py`)**:
   - Total de testes: **681**
   - Testes históricos pré-Stage 31.5: **668/668 PASS (100%)**
   - Falhas registradas: **12 falhas**, todas pertencentes à nova suíte de revalidação [`tests/test_stage_31_5_revalidation.py`](file:///d:/Projetos/TechLens/tests/test_stage_31_5_revalidation.py).
   - Nenhuma regressão detectada nos estágios 20 a 31.4.2.
2. **Reference Harness (`run_reference_harness.py`)**:
   - Suítes executadas: **8/8**
   - Suítes em falha: 2 (`reference_runtime` e `full_unittest`), estritamente devido às 12 falhas adversariais da suíte 31.5.
   - Status do Harness: `FAIL (8/8 suites, 2 failed; WARNINGS: BLOCKED, PASS_WITH_WARNING)`.

---

## 17. Root Causes of Residual Divergences

### Divergências no Piloto Real (Candidato-Piloto-05)

1. **Questão Q5 (REST Produces/Consumes vs Kafka — Diff +2.45)**:
   - *Score Humano*: `2.0` | *Score do Sistema*: `4.45`
   - *Classificação*: `VALID_TECHNICAL_DISAGREEMENT` / `RESIDUAL_PARTIAL_CREDIT`.
   - *Causa*: O candidato fugiu do tema de HTTP REST para falar de mensageria assíncrona Kafka. O sistema reconheceu a fuga através do modelo semântico (`off_topic(negative)`), rebaixando correctness para `Insufficient`. No entanto, como o candidato articulou corretamente o funcionamento de producers e consumers em Kafka, o motor atribuiu crédito conceitual residual em mensageria (`conceptual: partial`), gerando nota 4.45. A avaliação humana adotou postura punitiva direta (nota 2.0). Ambas são posições tecnicamente defensáveis.
2. **Questão Q10 (Investigação de Erro 500 — Diff +1.65)**:
   - *Score Humano*: `6.0` | *Score do Sistema*: `7.65`
   - *Classificação*: `DIMENSION_INTERPRETATION`.
   - *Causa*: O candidato propôs diagnosticar o erro adicionando prints e logs e debugando o código. O sistema premiou o raciocínio investigativo como `reasoning: Strong` (score 7.65). O avaliador humano considerou a estratégia excessivamente genérica e elementar para nível sênior, atribuindo nota 6.0.

---

## 18. Governance / Historical Integrity

Todos os artefatos históricos de governança permanecem integralmente preservados e inalterados:

- `Stage 31 — Human vs System Comparison.md`: `HUMAN_VS_SYSTEM_BLOCKED` mantido.
- `Stage 31.1 — Human vs System Failure Analysis.md`: Mantido.
- `Stage 31.2 — Controlled Correction.md`: `CONTROLLED_CORRECTION_COMPLETE_WITH_WARNINGS` mantido.
- `Stage 31.3 — Post-Correction Blind Validation.md`: `POST_CORRECTION_BLIND_VALIDATION_BLOCKED` mantido.
- `Stage 31.4 — Semantic Relevance & Representation Invariance Remediation.md`: Mantido.
- `Stage 31.4.1 — Semantic Relevance Model Redesign.md`: Mantido.
- `Stage 31.4.2 — Semantic Relevance Model Implementation.md`: Mantido.

---

## 19. Final Assessment

A pergunta central formulada para o Stage 31.5 foi:

> *"Depois da correção da pertinência semântica, o sistema passou a interpretar evidências técnicas de maneira mais próxima de uma avaliação humana independente, de forma generalizável, explicável, determinística e sem regras específicas para os casos conhecidos?"*

**Resposta Analítica**:
- **Sim** no que tange à **amostra piloto real e aos casos conhecidos**: O sistema eliminou por completo as regras ad-hoc de pares tecnológicos, reduziu drasticamente o erro médio em relação à referência humana (MAE caiu de 2.01 para 0.64) e estabilizou as quatro questões de experiência declarada na nota 4.0 exata.
- **Não** no que tange à **generalização aberta e ausência de proxies**: A auditoria adversarial revelou que o runtime ainda retém um proxy explícito de contagem de palavras (`len <= 6`) na decisão entre respostas parciais e diretas, e que o motor de domínio aberto carece de flexibilidade morfológica (lematização), além de conter um vício de colisão de substring (`"orm"` em `"performance"`).

---

## 20. Limitations

1. **Falta de Lematização/Stemming**: O motor de domínio aberto depende de coincidência exata de termos alfanuméricos entre pergunta e resposta, gerando falsos negativos quando ocorrem flexões verbais ou plurais legítimos.
2. **Dependência de Limiar Numérico em Múltiplos Aspectos**: O uso de `len <= 6` para discriminar respostas parciais introduz falsos positivos quando respostas com $\ge 7$ palavras cobrem apenas parte do enunciado.
3. **Colisão de Substrings em Tokens Curtos de Capacidade**: Tokens de demanda curtos como `"orm"` causam correspondências espúrias em palavras compostas da língua portuguesa (`"performance"`).

---

## 21. Gate Decision

```text
POST_REMEDIATION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED
```

### Critérios de Desbloqueio para o Stage 31.6 (Controlled Correction)

Para que a revalidação humana versus sistema seja finalmente aprovada sem restrições, o Stage 31.6 deverá:
1. **Substituir o Limiar `len <= 6`**: Implementar verificação estrutural baseada em presença de evidências para cada aspecto da pergunta multi-aspecto, sem heurística de contagem de palavras.
2. **Implementar Normalização Morfológica / Stemming Básico**: Garantir que variações flexionais padrão (ex.: *correlacionar/correlação*, *singular/plural*, *verbos no infinitivo/passado*) coincidam no cálculo de interseção de domínio aberto.
3. **Impedir Colisões de Substring em Tokens de Capacidade**: Utilizar correspondência por palavra inteira (`\borm\b`) em vez de substring simples (`"orm" in q_lower`).
4. **Reexecutar a Suíte de Revalidação 31.5**: Obter 74/74 PASS e 8/8 suites no Reference Harness.
5. **Manter Proibição Estrita de Avançar para o Stage 32**: Nenhuma atividade de Production Readiness deve ser iniciada até a aprovação formal do gate revalidado.
