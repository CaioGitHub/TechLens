---
type: study
status: unresolved
confidence: 100
created: 2026-10-10
updated: 2026-10-10
tags:
  - interview-evaluation
  - pilot
  - validation
  - blind-revalidation
  - demand-proposition-nexus
  - stage-31-7-13
  - gate-blocked
---

# Stage 31.7.13 — Independent Blind Semantic Revalidation Execution

## 1. Objetivo e Escopo

O objetivo do **Stage 31.7.13** foi executar a validação semântica independente, cega e reproduzível da arquitetura `Demand-Proposition Nexus`, introduzida no Stage 31.7.11 e auditada no Stage 31.7.12.

Esta etapa é exclusivamente de **validação e auditoria experimental**. Conforme exigido pelas diretrizes metodológicas e pelas regras de integridade do projeto:
- O código do runtime (`reference_runtime/runtime.py`) permaneceu **100% congelado**, sem qualquer alteração de heurísticas, limiares, classificadores, vocabulários ou expressões regulares.
- O benchmark foi executado em regime de cegamento estrito: o motor recebeu exclusivamente os campos de identificação e texto (`id`, `question_text`, `response_text`), permanecendo as classificações e justificativas humanas congeladas e isoladas em arquivo separado com hash verificado antes da execução.
- O confronto com o gabarito foi realizado em processo post-hoc automatizado e auditável.

---

## 2. Hash e Integridade do Runtime

Antes do início da execução e imediatamente após a conclusão dos testes, a integridade criptográfica do runtime foi atestada:

- **Arquivo sob teste:** `reference_runtime/runtime.py`
- **Hash SHA-256 Esperado (Stage 31.7.11 / 31.7.12):**
  `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E`
- **Hash SHA-256 Calculado Pré-Execução:**
  `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E`
- **Status Pré-Execução:** `INTEGRITY_VERIFIED_MATCH`
- **Hash SHA-256 Calculado Pós-Execução:**
  `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E`
- **Status Pós-Execução:** `INTEGRITY_VERIFIED_STILL_MATCH`
- **Interface e Motor Auditados:** Invocação direta da função `evaluate_open_domain_semantic_relevance(question, response)` que instancia `OpenDomainPropositionEngine` (arquitetura `Demand-Proposition Nexus`), garantindo que o motor legado (`legacy`) não foi chamado por engano.

---

## 3. Auditoria de Independência do Benchmark

Antes de liberar a entrada para o motor, os 250 casos foram submetidos a auditoria automatizada de colisão e independência:

1. **Unicidade de Identificadores:** 250 identificadores únicos (`id`), 0 colisões internas.
2. **Unicidade de Pares (Pergunta, Resposta):** 250 pares distintos, 0 duplicatas.
3. **Colisão com o Benchmark do Stage 31.7.9 (242 casos):**
   - Pares `(question, response)` compartilhados: **0** (100% inéditos).
   - Perguntas idênticas compartilhadas: **0**.
4. **Colisão com a Suíte de Testes Unitários de Desenvolvimento (`tests/test_stage_31_7_*.py`):**
   - Pares ou textos compartilhados: **0** (todas as formulações de desenvolvimento foram isoladas e substituídas por formulações independentes).
5. **Declaração de Independência Metodológica:**
   - Embora o benchmark seja 100% livre de sobreposição textual com os estágios anteriores e utilize tecnologias inéditas (SurrealDB, DuckDB, Tigris, Valkey) e inventadas (AetherDB, VortexStream, ChronoSync, ZenithKV), declaramos que a elaboração foi realizada pela mesma equipe técnica de engenharia de avaliação. Portanto, o protocolo é classificado formalmente como **Blind Revalidation Independente de Dados**, evitando o uso inadequado do termo *double-blind* externo não supervisionado.

---

## 4. Distribuição Planejada versus Distribuição Efetiva

A distribuição efetiva do benchmark de 250 casos correspondeu **com exatidão absoluta (100,0%)** às classes planejadas e aprovadas no Stage 31.7.12:

| Classe Canônica | Casos Planejados | % Planejada | Casos Efetivos | % Efetiva | Diferença |
|---|---:|---:|---:|---:|---:|
| `DIRECT` | 60 | 24,0% | 60 | 24,0% | 0 |
| `PARTIAL` | 35 | 14,0% | 35 | 14,0% | 0 |
| `SUPPORTING` | 30 | 12,0% | 30 | 12,0% | 0 |
| `RELATED` | 35 | 14,0% | 35 | 14,0% | 0 |
| `OFF_TOPIC` | 50 | 20,0% | 50 | 20,0% | 0 |
| `INSUFFICIENT` | 25 | 10,0% | 25 | 10,0% | 0 |
| `UNKNOWN` | 15 | 6,0% | 15 | 6,0% | 0 |
| **Total** | **250** | **100,0%** | **250** | **100,0%** | **0** |

### Distribuição pelos 16 Grupos Temáticos (A a P):

| Grupo | Categoria Semântica | Casos | Classes Contidas |
|---|---|---:|---|
| **Grupo A** | Tecnologias Inéditas e Fictícias | 15 | DIRECT (8), PARTIAL (4), RELATED (3) |
| **Grupo B** | Zero-Lexical Clássico (Sem sobreposição de palavras) | 15 | DIRECT (10), PARTIAL (5) |
| **Grupo C** | Multiaspecto Coordenado (Demandas compostas) | 19 | DIRECT (5), PARTIAL (14) |
| **Grupo D** | Observabilidade Auxiliar (APM, Logs, Tracing, Métricas) | 33 | SUPPORTING (28), DIRECT (3), RELATED (2) |
| **Grupo E** | Antítese Operacional / Polaridade Destrutiva | 12 | OFF_TOPIC (10), DIRECT (2) |
| **Grupo F** | Domínios Ortogonais Computacionais (CSS vs Consenso, etc.) | 15 | OFF_TOPIC (12), RELATED (3) |
| **Grupo G** | Domínios Alienígenas Não Computacionais (Culinária, Esportes) | 12 | OFF_TOPIC (12) |
| **Grupo H** | Trivia, Hardware e História | 10 | RELATED (8), OFF_TOPIC (2) |
| **Grupo I** | Declaração de Experiência vs Demonstração Concreta | 12 | RELATED (7), DIRECT (5) |
| **Grupo J** | Hipótese Especulativa ("Acho que dá", Proposta teórica) | 12 | PARTIAL (5), RELATED (4), DIRECT (3) |
| **Grupo K** | Respostas Ultra-Concisas (Desafio ao length proxy) | 10 | DIRECT (8), RELATED (2) |
| **Grupo L** | Jargão e Prolixidade sem Mecanismo (Buzzword Soup) | 15 | OFF_TOPIC (9), RELATED (6) |
| **Grupo M** | Evasivas e Tautologias ("Depende de tudo", circularidade) | 15 | UNKNOWN (15) |
| **Grupo N** | Ignorância e Filler ("Não lembro", "Sim, com certeza") | 25 | INSUFFICIENT (25) |
| **Grupo O** | Invariância de Representação (10 pares formal vs informal) | 20 | DIRECT (14), PARTIAL (4), SUPPORTING (2) |
| **Grupo P** | Mutações Semânticas Críticas (Inversão de segurança/ordem) | 10 | DIRECT (2), PARTIAL (3), OFF_TOPIC (5) |
| **Total** | **16 Grupos Temáticos Cobertos** | **250** | **Todas as 7 classes distribuídas** |

---

## 5. Protocolo de Cegamento Executado

O experimento seguiu estritamente o protocolo sequencial de quatro estágios independentes:

1. **Geração e Congelamento do Gabarito:**
   - O arquivo `scratch/stage_31_7_13_ground_truth.json` foi gerado contendo todas as referências humanas, justificativas técnicas detalhadas e anotações epistemológicas.
   - O SHA-256 do gabarito foi registrado antes de qualquer execução de predição.
2. **Geração da Entrada Cega:**
   - O arquivo `scratch/stage_31_7_13_blind_input.json` foi derivado contendo estritamente os campos `id`, `question_text` e `response_text`.
   - Nenhuma classe, grupo temático, pista léxica ou justificativa foi fornecida.
3. **Execução Cega pelo Runtime Congelado:**
   - O script `scratch/run_stage_31_7_13_blind_execution.py` processou os 250 casos através do motor `evaluate_open_domain_semantic_relevance`.
   - As 250 predições foram persistidas em `scratch/stage_31_7_13_system_predictions.json`.
   - O SHA-256 do arquivo de predições foi calculado e congelado antes da revelação do gabarito.
4. **Confronto Post-Hoc Automatizado:**
   - O script `scratch/evaluate_stage_31_7_13_results.py` leu ambos os arquivos congelados e realizou a auditoria estatística e diagnóstica.

---

## 6. Hashes dos Artefatos

Todos os arquivos gerados e validados possuem rastreabilidade por SHA-256:

| Artefato | Caminho do Arquivo | SHA-256 |
|---|---|---|
| **Runtime sob Teste** | `reference_runtime/runtime.py` | `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E` |
| **Gabarito Humano Congelado** | `scratch/stage_31_7_13_ground_truth.json` | `69996E5D2522A2E5E382B894D25539A754BEC7C423714A70F6D58FFFC082D1AB` |
| **Entrada Cega do Motor** | `scratch/stage_31_7_13_blind_input.json` | `D348EC46844BB8141EF1F4A53FC239B8FFB87316E79AB239266AACE117DF8DDD` |
| **Predições Congeladas do Motor** | `scratch/stage_31_7_13_system_predictions.json` | `A24F9AF62B6C0EC6CC26C9F4F55C7627AC7348011C7B6DE5C04866FD453FD416` |

---

## 7. Concordância Global

- **Total de Casos Avaliados:** 250
- **Concordâncias Exatas (Predição = Referência):** 91
- **Divergências:** 159
- **Concordância Exata Global (Accuracy):** **36,40%** (91 / 250)
- **Meta Definida no Stage 31.7.12:** $\ge 75,0\%$
- **Resultado Operacional:** **REPROVADO (Abaixo da meta em 38,60 pontos percentuais)**

---

## 8. Matriz de Confusão 7 × 7

A matriz de confusão apresenta os 250 casos confrontando as classes de referência humana (linhas) com as predições geradas pelo motor (colunas):

| Classe de Referência | DIRECT | PARTIAL | SUPPORTING | RELATED | OFF_TOPIC | INSUFFICIENT | UNKNOWN | Total Referência |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **DIRECT** | **26** | 0 | 0 | 2 | 31 | 1 | 0 | **60** |
| **PARTIAL** | 13 | **0** | 0 | 1 | 20 | 1 | 0 | **35** |
| **SUPPORTING** | 12 | 0 | **7** | 2 | 9 | 0 | 0 | **30** |
| **RELATED** | 10 | 0 | 2 | **5** | 18 | 0 | 0 | **35** |
| **OFF_TOPIC** | 12 | 0 | 0 | 2 | **36** | 0 | 0 | **50** |
| **INSUFFICIENT** | 1 | 0 | 0 | 3 | 5 | **16** | 0 | **25** |
| **UNKNOWN** | 3 | 0 | 0 | 1 | 10 | 0 | **1** | **15** |
| **Total Previsto** | **77** | **0** | **9** | **16** | **129** | **18** | **1** | **250** |

### Achados Imediatos da Matriz:
1. **Ausência Absoluta de Predições `PARTIAL`:** O motor previu `PARTIAL` exatamente **0 vezes**. Todos os 35 casos parciais foram polarizados: 20 rebaixados para `OFF_TOPIC`, 13 indevidamente promovidos para `DIRECT`.
2. **Superpopulação de `OFF_TOPIC` (129 predições):** O motor sofreu hipercorreção severa, condenando 31 respostas verdadeiramente diretas (`DIRECT`) ao status de `OFF_TOPIC`.
3. **Persistência de Falsos `DIRECT` (51 casos):** O motor promoveu 51 respostas não-diretas para `DIRECT` (12 de Supporting, 13 de Partial, 12 de Off-Topic, 10 de Related, 3 de Unknown e 1 de Insufficient).

---

## 9. Métricas Focais da Classe DIRECT

A classe `DIRECT` é a mais crítica do sistema de avaliação de candidatos: falsos positivos promovem respostas inadequadas ou destrutivas; falsos negativos desqualificam candidatos que apresentaram soluções tecnicamente perfeitas.

- **Verdadeiros Positivos (`TP_DIRECT`):** 26
- **Falsos Positivos (`FP_DIRECT`):** 51
- **Falsos Negativos (`FN_DIRECT`):** 34
- **Verdadeiros Negativos (`TN_DIRECT`):** 139
- **Total de Previsões `DIRECT`:** 77 (26 TP + 51 FP)
- **Total de Casos de Referência `DIRECT`:** 60 (26 TP + 34 FN)
- **Total de Divergências no Benchmark:** 159

### Métricas Calculadas:

1. **Precisão de DIRECT:**
   $$\text{Precision} = \frac{26}{26 + 51} = \frac{26}{77} = \mathbf{33,77\%}$$
2. **Taxa de Falsos DIRECT entre Previsões DIRECT:**
   $$\text{FP Rate in Predictions} = \frac{51}{77} = \mathbf{66,23\%}$$
   *(A cada 3 respostas que o motor declara como DIRECT, 2 são falsos positivos).*
3. **Proporção de Falsos DIRECT entre Todas as Divergências:**
   $$\text{Proporção} = \frac{51}{159} = \mathbf{32,08\%}$$
   - **Meta Definida no Stage 31.7.12:** $\le 10,0\%$
   - **Resultado:** **REPROVADO (32,08% vs meta de 10,0%)**.
4. **Recall de DIRECT:**
   $$\text{Recall} = \frac{26}{60} = \mathbf{43,33\%}$$
   - **Meta Definida no Stage 31.7.12:** $\ge 85,0\%$
   - **Resultado:** **REPROVADO (43,33% vs meta de 85,0%)**.
5. **F1-Score de DIRECT:** **37,96%**.

---

## 10. Métricas por Classe Canônica

| Classe | Casos Ref. | Casos Prev. | Acertos (TP) | Falsos Positivos (FP) | Falsos Negativos (FN) | Precisão | Recall | F1-Score | Padrão Principal de Confusão |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **`DIRECT`** | 60 | 77 | 26 | 51 | 34 | 33,8% | 43,3% | 38,0% | Rebaixado para OFF_TOPIC (31), RELATED (2) |
| **`PARTIAL`** | 35 | 0 | 0 | 0 | 35 | 0,0% | 0,0% | 0,0% | Rebaixado para OFF_TOPIC (20), promovido a DIRECT (13) |
| **`SUPPORTING`** | 30 | 9 | 7 | 2 | 23 | 77,8% | 23,3% | 35,9% | Promovido a DIRECT (12), rebaixado a OFF_TOPIC (9) |
| **`RELATED`** | 35 | 16 | 5 | 11 | 30 | 31,2% | 14,3% | 19,6% | Rebaixado para OFF_TOPIC (18), promovido a DIRECT (10) |
| **`OFF_TOPIC`** | 50 | 129 | 36 | 93 | 14 | 27,9% | 72,0% | 40,2% | Falsos positivos massivos (93 não-offtopics viraram off-topic) |
| **`INSUFFICIENT`** | 25 | 18 | 16 | 2 | 9 | 88,9% | 64,0% | 74,4% | Confundido com OFF_TOPIC (5), RELATED (3) |
| **`UNKNOWN`** | 15 | 1 | 1 | 0 | 14 | 100,0% | 6,7% | 12,5% | Rebaixado para OFF_TOPIC (10), promovido a DIRECT (3) |

---

## 11. Métricas por Grupo Temático (A a P)

| Grupo | Categoria Semântica | Casos | Acertos | Divergências | Acurácia | FP DIRECT | FN DIRECT | Padrão Dominante de Erro |
|---|---|---:|---:|---:|---:|---:|---:|---|
| **Grupo A** | Tecnologias Inéditas e Fictícias | 15 | 4 | 11 | 26,7% | 3 | 4 | DIRECT -> OFF_TOPIC |
| **Grupo B** | Zero-Lexical Clássico | 15 | 2 | 13 | 13,3% | 3 | 8 | DIRECT -> OFF_TOPIC |
| **Grupo C** | Multiaspecto Coordenado | 19 | 4 | 15 | 21,1% | 6 | 1 | PARTIAL -> OFF_TOPIC |
| **Grupo D** | Observabilidade Auxiliar (Supporting) | 33 | 6 | 27 | 18,2% | 12 | 2 | SUPPORTING -> DIRECT |
| **Grupo E** | Antítese Operacional / Polaridade Destrutiva | 12 | 9 | 3 | 75,0% | 2 | 1 | OFF_TOPIC -> DIRECT |
| **Grupo F** | Domínios Ortogonais Computacionais | 15 | 7 | 8 | 46,7% | 6 | 0 | OFF_TOPIC -> DIRECT |
| **Grupo G** | Domínios Alienígenas Não Computacionais | 12 | 9 | 3 | 75,0% | 2 | 0 | OFF_TOPIC -> DIRECT |
| **Grupo H** | Trivia, Hardware e História | 10 | 5 | 5 | 50,0% | 2 | 0 | RELATED -> OFF_TOPIC |
| **Grupo I** | Declaração de Experiência vs Demonstração | 12 | 4 | 8 | 33,3% | 1 | 3 | RELATED -> OFF_TOPIC |
| **Grupo J** | Hipótese Especulativa | 12 | 1 | 11 | 8,3% | 1 | 2 | RELATED -> OFF_TOPIC |
| **Grupo K** | Respostas Ultra-Concisas | 10 | 5 | 5 | 50,0% | 1 | 3 | DIRECT -> OFF_TOPIC |
| **Grupo L** | Jargão e Prolixidade sem Mecanismo (Buzzword Soup) | 15 | 7 | 8 | 46,7% | 4 | 0 | RELATED -> OFF_TOPIC |
| **Grupo M** | Evasivas e Tautologias | 15 | 1 | 14 | 6,7% | 3 | 0 | UNKNOWN -> OFF_TOPIC |
| **Grupo N** | Ignorância e Filler | 25 | 16 | 9 | 64,0% | 1 | 0 | INSUFFICIENT -> OFF_TOPIC |
| **Grupo O** | Invariância de Representação (Formal vs Informal) | 20 | 7 | 13 | 35,0% | 2 | 9 | DIRECT -> OFF_TOPIC |
| **Grupo P** | Mutações Semânticas Críticas | 10 | 4 | 6 | 40,0% | 2 | 1 | PARTIAL -> OFF_TOPIC |

---

## 12. Invariância de Representação (Grupo O)

Avaliou-se a sensibilidade do motor à mudança de estilo (formal versus informal / coloquial / gírias), mantendo idêntico o conteúdo técnico:

| Par | Conceito Técnico Avaliado | Classe Ref. | Predição Formal | Predição Informal | Invariante? | Status da Invariância |
|---|---|---|---|---|:---:|---|
| **Par 1** | Consistent Hashing | `DIRECT` | `RELATED` | `DIRECT` | **Não** | Quebra: Formal subestimado para RELATED |
| **Par 2** | Optimistic Locking | `DIRECT` | `DIRECT` | `DIRECT` | **Sim** | Invariante e Correto (Ambos DIRECT) |
| **Par 3** | Deadlock Ordering | `DIRECT` | `DIRECT` | `OFF_TOPIC` | **Não** | Quebra: Informal despencou para OFF_TOPIC |
| **Par 4** | Token Bucket Algorithm | `DIRECT` | `OFF_TOPIC` | `OFF_TOPIC` | **Sim** | Invariante por Duplo Falso Negativo |
| **Par 5** | Circuit Breaker Pattern | `DIRECT` | `DIRECT` | `OFF_TOPIC` | **Não** | Quebra: Informal com gíria virou OFF_TOPIC |
| **Par 6** | Write-Ahead Logging (WAL) | `DIRECT` | `OFF_TOPIC` | `OFF_TOPIC` | **Sim** | Invariante por Duplo Falso Negativo |
| **Par 7** | Bloom Filter | `DIRECT` | `OFF_TOPIC` | `OFF_TOPIC` | **Sim** | Invariante por Duplo Falso Negativo |
| **Par 8** | Exponential Backoff (Sem Jitter) | `PARTIAL` | `OFF_TOPIC` | `DIRECT` | **Não** | Quebra: Formal virou OFF_TOPIC, Informal virou DIRECT |
| **Par 9** | Sharding Strategy (Sem Rebalance) | `PARTIAL` | `DIRECT` | `OFF_TOPIC` | **Não** | Quebra: Formal virou DIRECT, Informal virou OFF_TOPIC |
| **Par 10** | Observabilidade Auxiliar | `SUPPORTING` | `SUPPORTING` | `SUPPORTING` | **Sim** | Invariante e Correto (Ambos SUPPORTING) |

### Resumo de Invariância de Representação:
- **Pares Rigorosamente Invariantes (Mesma Predição):** 5 / 10 (**50,0%**)
- **Pares Invariantes e Simultaneamente Corretos:** 2 / 10 (**20,0%** — Pares 2 e 10)
- **Pares Invariantes por Falha Coletiva (Ambos OFF_TOPIC):** 3 / 10 (**30,0%** — Pares 4, 6 e 7)
- **Pares com Quebra de Invariância (Predições Diferentes):** 5 / 10 (**50,0%**)
- **Meta Definida no Stage 31.7.12:** $\ge 80,0\%$
- **Resultado Operacional:** **REPROVADO (50,0% vs meta de 80,0%)**.

---

## 13. Análise Qualitativa das Divergências e Causa-Raiz

O confronto das 159 divergências revelou com precisão cirúrgica a anatomia das falhas no motor semântico `reference_runtime/runtime.py`:

### Reconciliação Rigorosa de Causas Primárias (Total Exato: 159)

```text
Total de Divergências = 159
│
├── 1. Rebaixamento Excessivo para OFF_TOPIC (Nexus Drop Rígido)   : 42 casos (26,4%)
├── 2. Incapacidade de Decomposição Multiaspecto (PARTIAL Miss)     : 35 casos (22,0%)
├── 3. Falha Sintática em Verbos Passivos/Pronominais (-se)         : 31 casos (19,5%)
├── 4. Promoção de Ação Auxiliar sem Nexo Resolutivo (Supporting)  : 12 casos ( 7,5%)
├── 5. Cegueira de Polaridade e Antítese Destrutiva                 : 12 casos ( 7,5%)
├── 6. Promoção de Relação Temática sem Mecanismo (Related)         : 10 casos ( 6,3%)
├── 7. Outros Desalinhamentos Semânticos Isolados                   : 13 casos ( 8,2%)
└── 8. Promoção Indevida de Evasivas ou Fillers                     :  4 casos ( 2,5%)
──────────────────────────────────────────────────────────────────────────────────
Soma Reconciliada                                                   : 159 casos (100,0%)
```

---

### Diagnóstico Detalhado das Três Falhas Estruturais Críticas:

#### Causa 1: O Defeito Sintático dos Verbos Pronominais/Passivos (`-se`) — Origem de 31 Falsos Negativos
Quando a resposta utiliza construções impessoais ou reflexivas com partícula apassivadora (comuns na linguagem culta de engenharia de software em língua portuguesa):
- *`Mapeia-se` os nós num anel circular...* (`B01_consistent_hashing`)
- *`Inclui-se` um atributo numérico sequencial...* (`B02_optimistic_concurrency`)
- *`Interrompe-se` temporariamente o tráfego...* (`B03_circuit_breaker`)
- *`Grava-se` a operação cronologicamente em log...* (`B04_wal`)
- *`Impõe-se` uma sequência padronizada de locks...* (`B09_deadlock_ordering`)

O tokenizador e o chunker de proposições de `runtime.py` falharam em reconhecer formas verbais unidas por hífen (`-se`) ou particípios/gerúndios como verbos de ação proposicional. O motor marcou a proposição como `non_operative_assertion`, assumindo que a frase não continha um mecanismo técnico ativo. Consequentemente, respostas que explicavam a solução com rigor matemático foram condenadas a `OFF_TOPIC`.

#### Causa 2: Ausência de Filtro de Suficiência Causal (Ação != Resolução) — Origem de 12 Falsos Positivos de `SUPPORTING`
O motor implementou uma regra permissiva: ao detectar um verbo ativo ("Adiciono", "Configuro", "Instalo", "Redireciono") acompanhado de substantivo técnico ("Prometheus", "Redis", "Loki", "Kafka"), ele declara:
> `Response functionally solves the question demand.`

O motor verificou apenas a *presença de uma ação técnica*, e **não se essa ação soluciona a causa raiz da demanda**:
- Adicionar cache Redis na frente reduz leituras, mas **não resolve contenção de lock em débitos de saldo** (`D21`).
- Reiniciar pods com liveness probe mitiga a queda, mas **não resolve o memory leak da aplicação** (`D23`).
- Mandar eventos para Dead Letter Queue isola a falha, mas **não corrige a serialização corrompida** (`D24`).
O motor promoveu 12 casos auxiliares a `DIRECT` por falta de modelagem de causalidade.

#### Causa 3: Colapso do Classificador Multiaspecto e Ausência da Classe `PARTIAL`
Nenhum caso do benchmark recebeu a predição `PARTIAL` (0 / 35).
Quando uma pergunta exigia dois aspectos coordenados (ex: *Consistência vs Disponibilidade sob Partição* ou *Compare SQL e NoSQL em schema e transações ACID*):
- Se o motor identificava uma proposição operativa cobrindo o primeiro aspecto, ele imediatamente atribuía `multi_aspect_full_coverage` e emitia `DIRECT` (13 casos).
- Se o motor encontrava assimetria entre o texto e as demandas mapeadas, ele considerava a resposta inoperante e emitia `OFF_TOPIC` (20 casos).
Não existiu caminho no código de `runtime.py` capaz de atribuir proporcionalmente a classe `PARTIAL` com evidência de cobertura incompleta.

#### Causa 4: Cegueira de Polaridade e Antítese Destrutiva
O motor classificou como `DIRECT` propostas sabidamente destrutivas:
- *"Desativo transações ACID para que cada débito seja salvo isoladamente..."* (`P09`)
- *"Ignoro validação de assinatura e confio em qualquer payload enviado..."* (`P10`)
- *"Para resolver concorrência de saldos, desativo todos os locks do banco..."* (`P06`)
O motor extraiu os verbos ("Desativo", "Ignoro") e os conceitos ("transações ACID", "assinatura JWT", "locks"), sem inferir que anular ou desativar o mecanismo de proteção inverte a polaridade da demanda de segurança e integridade.

---

## 14. Verificação dos Contratos Arquiteturais

| Contrato Arquitetural Auditado (Stage 31.7.12) | Status no Benchmark | Evidência Observada |
|---|:---:|---|
| **9.1 Atendimento Funcional** | **FALHA** | 51 casos não-atendidos (Supporting, Partial, Antithetical) foram promovidos a `DIRECT`. |
| **9.2 Relações sem Sobreposição Lexical** | **FALHA** | No Grupo B (Zero-Lexical), o motor errou 13 de 15 casos (acurácia de 13,3%), caindo em falsos negativos massivos por falha sintática. |
| **9.3 SUPPORTING versus RELATED** | **FALHA PARCIAL** | Apenas 7 de 30 casos de Supporting foram classificados corretamente. 12 viraram `DIRECT` e 9 viraram `OFF_TOPIC`. |
| **9.4 Cobertura Multiaspecto** | **FALHA CRÍTICA** | 0 casos classificados como `PARTIAL`. O sistema atua como binário `DIRECT` ou `OFF_TOPIC`. |
| **9.5 Polaridade e Antítese** | **FALHA** | Recomendações catastróficas foram promovidas a `DIRECT` em 7,5% das divergências (P06, P09, P10). |
| **9.6 Epistemologia** | **PARCIAL** | `INSUFFICIENT` atingiu 64% de recall e 88,9% de precisão, mas declarações de senioridade pura (`I01-I07`) foram confundidas com `OFF_TOPIC`. |
| **9.7 Representação e Extensão** | **PARCIAL** | Respostas ultra-concisas (`Grupo K`) atingiram 50% de acerto; respostas prolixas sem nexo (`Grupo L`) tiveram 4 falsos DIRECT. |
| **9.8 Tecnologias Inéditas** | **FALHA PARCIAL** | No Grupo A, o motor errou 11 de 15 casos (26,7% de acerto), demonstrando que o motor ainda não generaliza adequadamente para novos domínios abertos. |

---

## 15. Limitações Metodológicas

1. **Benchmark Fechado para Avaliação:** Os 250 casos foram desenhados especificamente para o protocolo de validação cega deste projeto e refletem a interpretação dos autores da avaliação sobre engenharia de software distribuída.
2. **Ambiente Sintético vs Real:** Embora os casos tenham sido elaborados com base em dilemas reais de sistemas de produção, tratam-se de transcrições curtas e controladas, não de diálogos multifacetados e caóticos de entrevistas orais completas.
3. **Avaliação Focada na Camada Semântica:** O teste auditou isoladamente a função de relevância proposicional semântica (`OpenDomainPropositionEngine`), sem testar as etapas anteriores de segmentação, atribuição de speaker ou normalização de texto.

---

## 16. Resultado dos Critérios de Aceite

| Critério de Aceite | Meta Estabelecida | Resultado Efetivo | Avaliação |
|---|---:|---:|:---:|
| **Concordância Exata Global** | $\ge 75,0\%$ | **36,40%** (91 / 250) | **REPROVADO** |
| **Proporção de Falsos DIRECT nas Divergências** | $\le 10,0\%$ | **32,08%** (51 / 159) | **REPROVADO** |
| **Recall da Classe DIRECT** | $\ge 85,0\%$ | **43,33%** (26 / 60) | **REPROVADO** |
| **Invariância de Representação (Grupo O)** | $\ge 80,0\%$ | **50,00%** (5 / 10 pares) | **REPROVADO** |
| **Integridade do Runtime Congelado** | SHA-256 Idêntico | 100% Preservado | **APROVADO** |
| **Ausência de Vazamento de Gabarito** | Cegamento Rigoroso | 100% Auditável | **APROVADO** |

---

## 17. Conclusão Proporcional às Evidências

A validação cega independente cumpriu seu papel de governança científica com excelência: **ela expôs a realidade factual sem concessões.**

A implementação preliminar do `Demand-Proposition Nexus` (concluída no Stage 31.7.11):
1. **Reduziu a proporção histórica de falsos DIRECT entre divergências de 87,1% (Stage 31.7.9) para 32,08% (Stage 31.7.13)**, comprovando que a exigência de uma relação proposicional teve impacto corretivo real.
2. No entanto, **o motor ainda não está maduro para produção**. Ele apresenta:
   - Uma **hipercorreção severa por falsos negativos** (Recall de DIRECT de apenas 43,33%), descartando respostas perfeitas por limitações léxico-sintáticas na extração de verbos pronominais e reflexivos em português.
   - Uma **inabilidade estrutural de classificar respostas parciais** (0% de identificação de `PARTIAL`).
   - A **persistência de 51 falsos DIRECT**, promovendo ações meramente auxiliares de observabilidade e ignorando antíteses de polaridade destrutiva.

Portanto, avançar para *Production Readiness* sob essas condições violaria os princípios de governança do projeto. O bloqueio metodológico é mandatório e saudável.

---

## 18. Gate Final

```text
GATE: BLIND_SEMANTIC_REVALIDATION_BLOCKED
```

O benchmark cego independente foi concluído com integridade de runtime estritamente preservada (SHA-256 verificado), mas o motor não atingiu as metas operacionais de acurácia global (36,4% vs 75%), proporção de falsos DIRECT (32,08% vs 10%), recall de DIRECT (43,33% vs 85%) e invariância de representação (50% vs 80%).

---

## 19. Próxima Ação Recomendada

Recomenda-se uma única próxima ação estruturada:

**Stage 31.7.14 — Root Cause Analysis of Independent Blind Revalidation**

*Instruções para o próximo estágio:*
1. Investigar a causa raiz da falha de tokenização de verbos pronominais/passivos com hífen (`-se`) no chunker de proposições.
2. Investigar a ausência da classe `PARTIAL` no motor e desenhar o mecanismo de cálculo de cobertura fracionária de demandas multiaspecto.
3. Desenhar o filtro de suficiência causal para separar ações auxiliares (`SUPPORTING`) de soluções definitivas (`DIRECT`).
4. Desenhar o analisador de polaridade e antítese destrutiva para bloquear a promoção de recomendações contraproducentes a `DIRECT`.
5. **NÃO modificar o runtime até que a RCA formal e o plano de correção controlada sejam documentados e aprovados.**
