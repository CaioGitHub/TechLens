---
type: study
status: unresolved
confidence: 90
created: 2026-10-13
updated: 2026-10-13
tags:
  - stage-31-7-21
  - blind-validation
  - semantic-revalidation
  - open-domain-evaluation
  - evidence-audit
  - failure-analysis
---

# Stage 31.7.21 — Independent Blind Semantic Revalidation of the Remediated Runtime

## 1. Resumo Executivo

O presente relatório consolida a execução do **Stage 31.7.21**, cujo propósito metodológico exclusivo foi realizar uma **validação semântica cega, independente e sem vazamento de informação** do runtime corrigido no Stage 31.7.20 (`reference_runtime/runtime.py`).

Conforme determinado pelas diretrizes do projeto:
- **Nenhuma alteração de código foi realizada no runtime** durante esta etapa.
- **Nenhum teste foi modificado ou afrouxado** para mascarar divergências.
- **Nenhuma exceção ou lista lexical ad hoc foi injetada** para forçar aprovação.
- O runtime permaneceu **100% congelado** com SHA-256 verificado antes e depois da execução: `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`.

A revalidação foi executada sobre um conjunto de **250 casos de teste inéditos** cobrindo todas as 7 classes canônicas (`DIRECT`, `PARTIAL`, `SUPPORTING`, `RELATED`, `OFF_TOPIC`, `INSUFFICIENT`, `UNKNOWN`) e 10 grupos funcionais/adversariais (Grupos A a J), com zero sobreposição textual com benchmarks históricos.

### Veredito Quantitativo e Decisão de Gate

| Métrica | Critério de Referência | Resultado Observado | Status |
|---|---:|---:|:---:|
| **Concordância Exata** | $\ge 75{,}0\%$ | **68,00%** (170 / 250) | **FALHA** |
| **Recall de DIRECT** | $\ge 85{,}0\%$ | **81,54%** (53 / 65) | **FALHA** |
| **Precisão de DIRECT** | $\ge 70{,}0\%$ | **53,00%** (53 / 100) | **FALHA** |
| **Falsos DIRECT entre Divergências** | $\le 10{,}0\%$ | **58,75%** (47 / 80) | **FALHA** |
| **Recall de PARTIAL** | $\ge 60{,}0\%$ | **37,78%** (17 / 45) | **FALHA** |
| **Invariância de Representação** | $\ge 80{,}0\%$ | **68,75%** (11 / 16 pares) | **FALHA** |
| **Regressão Canônica** | Zero falhas inexplicadas | **1038 / 1038 pass (1 skip)**, Harness **15 / 15 pass** | **PASSOU** |

**Decisão de Gate:** `BLIND_SEMANTIC_REVALIDATION_BLOCKED`

Embora a regressão operacional tenha obtido 100% de conformidade e as salvaguardas de antithesis/evitação (Grupo I) tenham atingido 92,86% de acerto demonstrando a solidez da correção implementada no Stage 31.7.20 para polaridade, o comportamento semântico em cenários abertos falhou em 6 dos 7 critérios de aceite quantitativos. O principal gargalo reside na **sobre-promoção de respostas incompletas (`PARTIAL`) a `DIRECT` (25 casos)** e na **atribuição de `DIRECT` a respostas contextuais (`RELATED`) e circulares (`UNKNOWN`)**.

Em obediência irrestrita aos guardrails do projeto, **não se declara aprovação artificial**. O resultado é documentado como evidência científica primária para guiar a subsequente análise de causa-raiz.

---

## 2. Hashes e Integridade do Runtime Congelado

Antes do início e após o término da avaliação cega, a integridade do artefato de código do runtime foi confirmada via digest criptográfico SHA-256.

| Artefato | Caminho | SHA-256 Registrado | Conformidade |
|---|---|---|:---:|
| **Runtime Autorizado (Inicial)** | `reference_runtime/runtime.py` | `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC` | Idêntico ao esperado |
| **Checkpoint Congelado** | `reference_runtime/runtime.py.stage_31_7_21_frozen` | `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC` | Idêntico |
| **Runtime Autorizado (Final)** | `reference_runtime/runtime.py` | `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC` | Inalterado |

---

## 3. Protocolo de Cegamento Metodológico

Para eliminar qualquer contaminação epistêmica ou indução de parâmetros durante a predição, o fluxo obedeceu rigorosamente à separação de fases:

```text
1. Elaboração dos Casos Inéditos & Adjudicação Semântica
               ↓
2. Selamento Criptográfico do Ground Truth (`stage_31_7_21_ground_truth.json`)
               ↓
3. Extração da Entrada Cega (`stage_31_7_21_blind_input.json`)
   (Eliminação de rótulos, justificativas, demandas extraídas e metadados)
               ↓
4. Verificação de Congelamento do Runtime (SHA-256)
               ↓
5. Execução Cega das Predições (`stage_31_7_21_system_predictions.json`)
   (Ingestão EXCLUSIVA de `id`, `question_text`, `response_text`)
               ↓
6. Selamento das Predições do Sistema & Verificação Pós-Execução do Runtime
               ↓
7. Abertura do Ground Truth & Cálculo Automatizado de Métricas
               ↓
8. Auditoria de Independência e Análise Qualitativa de Divergências
```

O script executor `scratch/run_stage_31_7_21_blind_execution.py` operou isoladamente, sem acesso a referências humanas ou a resultados parciais.

---

## 4. Método de Criação e Adjudicação das Referências

O conjunto de teste foi construído abrangendo domínios de engenharia de software distribuída, bancos de dados transacionais e colunares, redes de baixa latência e concorrência que não constavam nas regras pré-programadas do motor.

Cada caso contém:
- Demanda primária e aspectos funcionais essenciais identificados formalmente.
- Racional semântico explícito justificando por que a resposta é `DIRECT`, `PARTIAL`, `SUPPORTING`, `RELATED`, `OFF_TOPIC`, `INSUFFICIENT` ou `UNKNOWN`.
- Forma linguística catalogada (formal, coloquial, passiva, sinteticamente densa, prolixa).
- Status epistêmico demarcado.

---

## 5. Auditoria de Independência Metodológica

### Declaração de Independência
Em observância estrita à Seção 4 da especificação:
> **Status:** `REFERENCE_INDEPENDENCE_UNRESOLVED`

**Justificativa Técnica:** Embora todas as 250 perguntas e respostas tenham sido redigidas e auditadas com 0% de sobreposição textual em relação a estágios anteriores, a adjudicação dos rótulos ocorreu em ambiente sintético de engenharia/IA, sem painel de comitê humano externo duplo-cego totalmente desvinculado do projeto. O hash criptográfico atesta a inviolabilidade do artefato, mas não a independência ontológica externa.

### Auditoria de Sobreposição Lexical e Semântica

| Base Comparada | Total de Casos | Colisões Exatas de Perguntas | Colisões Exatas de Respostas | Sobreposição Parcial Elevada |
|---|---:|---:|---:|:---:|
| `stage_31_7_17_ground_truth.json` | 200 | 0 | 0 | 0 |
| `stage_31_7_6_benchmark_raw.json` | 100 | 0 | 0 | 0 |
| Casos de Teste Unitário Históricos | 1038 | 0 | 0 | 0 |

*(Nota: Na fase de montagem preliminar, 2 questões com termos idênticos foram detectadas e imediatamente substituídas por problemas inéditos de rate limiting distribuído antes do selamento final).*

---

## 6. Composição e Distribuição do Conjunto de Teste

### Distribuição por Classe Canônica

| Classe | Casos na Referência | Proporção (%) | Justificativa de Cobertura |
|---|---:|---:|---|
| `DIRECT` | 65 | 26,0% | Soluções operativas completas, concisas e coloquiais |
| `PARTIAL` | 45 | 18,0% | Atendimento de aspecto único em demandas compostas e omissões |
| `SUPPORTING` | 28 | 11,2% | Instrumentações, métricas e práticas auxiliares não resolutivas |
| `RELATED` | 32 | 12,8% | Metadados institucionais, história, hardware e declarações de uso |
| `OFF_TOPIC` | 44 | 17,6% | Disjunções completas e ações antitéticas perigosas |
| `INSUFFICIENT` | 22 | 8,8% | Respostas evasivas, consultoria vaga e preenchimentos genéricos |
| `UNKNOWN` | 14 | 5,6% | Tautologias puras, poliptotos circulares e raciocínio vazio |
| **Total** | **250** | **100,0%** | **Distribuição balanceada para garantia de cobertura** |

### Distribuição por Grupo Funcional

| Grupo | Descrição | Casos | Acertos | Acurácia do Grupo |
|---|---|---:|---:|---:|
| **A** | Satisfação Funcional Aberta | 30 | 26 | **86,67%** |
| **B** | Respostas Parciais e Omissão de Aspectos | 30 | 7 | **23,33%** |
| **C** | Contribuição Auxiliar (`SUPPORTING`) | 28 | 25 | **89,29%** |
| **D** | Proximidade Temática sem Solução (`RELATED`) | 32 | 21 | **65,62%** |
| **E** | Totalmente Fora do Tópico (`OFF_TOPIC`) | 30 | 27 | **90,00%** |
| **F** | Evidência Insuficiente e Evasiva (`INSUFFICIENT`) | 22 | 8 | **36,36%** |
| **G** | Incerteza e Circularidade Tautológica (`UNKNOWN`) | 14 | 7 | **50,00%** |
| **H** | Demandas Compostas Multi-Aspecto | 18 | 11 | **61,11%** |
| **I** | Polaridade, Evitação e Salvaguarda Preventiva | 14 | 13 | **92,86%** |
| **J** | Pares de Invariância de Representação (16 pares) | 32 | 25 | **78,12%** |
| **Total** | | **250** | **170** | **68,00%** |

---

## 7. Hashes Criptográficos dos Artefatos Gerados

Todos os artefatos foram persistidos no diretório canônico `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/`:

| Artefato | Tamanho (bytes) | SHA-256 | Função Metodológica |
|---|---:|---|---|
| `stage_31_7_21_ground_truth.json` | 214.184 | `D594BB067FE0A031720F75B416AB636D57D280D7E00E279557D9C8D8C6D120F6` | Rótulos de referência selados |
| `stage_31_7_21_blind_input.json` | 85.733 | `E75D22F3BDB2A600C3628C1924997EC6D81B8143B9C7A01628E080A27313D010` | Entrada cega desprovida de rótulos |
| `stage_31_7_21_system_predictions.json` | 279.398 | `577B308CA7FB3C827FF04776779E6E1C5916565982ED059B986E295B9958E168` | Predições autônomas do runtime |
| `stage_31_7_21_metrics_summary.json` | 3.743 | `C52A332C8758DE999BD690C11BC50615B6F912C3FC24D1A8955ECB2556684C4B` | Resumo estatístico consolidado |
| `stage_31_7_21_confusion_matrix.json` | 1.458 | `03CD7D0215933398641798257BEEFB5C5EC0A83E58FEE4783AB3B79C1A9A5972` | Matriz de confusão 7x7 |
| `stage_31_7_21_divergence_analysis.json` | 91.816 | `94AACB770A97F2840B56025478F770C3837F78AF94DE0965410262140870BB43` | Auditoria caso a caso das 80 divergências |
| `stage_31_7_21_independence_audit.json` | 1.978 | `26AD25606AB3E9D8F8E3CB4EDF1F8E692F1318D2A3EEC6C3D50112B0B6CD1E55` | Registro formal de independência |

---

## 8. Métricas Obrigatórias com Numeradores e Denominadores

### Resumo Comparativo com Metas de Aceite

| Métrica | Numerador | Denominador | Percentual | Meta Exigida | Desvio | Status |
|---|---:|---:|---:|---:|---:|:---:|
| **Concordância Exata** | 170 | 250 | **68,00%** | $\ge 75{,}0\%$ | $-7{,}00\%$ | **REPROVADO** |
| **Recall de DIRECT** | 53 | 65 | **81,54%** | $\ge 85{,}0\%$ | $-3{,}46\%$ | **REPROVADO** |
| **Precisão de DIRECT** | 53 | 100 | **53,00%** | $\ge 70{,}0\%$ | $-17{,}00\%$ | **REPROVADO** |
| **Falsos DIRECT / Divergências** | 47 | 80 | **58,75%** | $\le 10{,}0\%$ | $+48{,}75\%$ | **REPROVADO** |
| **Recall de PARTIAL** | 17 | 45 | **37,78%** | $\ge 60{,}0\%$ | $-22{,}22\%$ | **REPROVADO** |
| **Invariância de Representação** | 11 | 16 | **68,75%** | $\ge 80{,}0\%$ | $-11{,}25\%$ | **REPROVADO** |
| **Regressão Canônica** | 1037 | 1037 | **100,00%** | Zero falhas | $0{,}00\%$ | **APROVADO** |

---

## 9. Matriz de Confusão Completa

A matriz a seguir relaciona a classe de referência humana (linhas) com a predição emitida pelo sistema congelado (colunas):

```text
REF \ PRED       DIRECT   PARTIAL SUPPORTING   RELATED OFF_TOPIC INSUFFICIENT   UNKNOWN    TOTAL
DIRECT               53         9          0         0         3            0         0       65
PARTIAL              25        17          1         0         2            0         0       45
SUPPORTING            3         0         25         0         0            0         0       28
RELATED               8         0          0        21         3            0         0       32
OFF_TOPIC             5         0          0         0        39            0         0       44
INSUFFICIENT          0         0          0         0         3            8        11       22
UNKNOWN               6         0          0         0         1            0         7       14
TOTAL PREVISTO      100        26         26        21        51            8        18      250
```

### Análise de Desempenho por Classe

| Classe | TP | FP | FN | Suporte | Precisão (%) | Recall (%) | F1-Score (%) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `DIRECT` | 53 | 47 | 12 | 65 | 53,00% | 81,54% | 64,24% |
| `PARTIAL` | 17 | 9 | 28 | 45 | 65,38% | 37,78% | 47,89% |
| `SUPPORTING` | 25 | 1 | 3 | 28 | 96,15% | 89,29% | 92,59% |
| `RELATED` | 21 | 0 | 11 | 32 | 100,00% | 65,62% | 79,25% |
| `OFF_TOPIC` | 39 | 12 | 5 | 44 | 76,47% | 88,64% | 82,11% |
| `INSUFFICIENT` | 8 | 0 | 14 | 22 | 100,00% | 36,36% | 53,33% |
| `UNKNOWN` | 7 | 11 | 7 | 14 | 38,89% | 50,00% | 43,75% |
| **Macro Média** | — | — | — | 250 | **75,70%** | **64,18%** | **66,17%** |

---

## 10. Análise Detalhada de Divergências e Causas-Raiz

As 80 divergências foram integralmente catalogadas em `stage_31_7_21_divergence_analysis.json`. Elas se distribuem nas seguintes causas-raiz demonstradas:

### Distribuição por Categoria de Causa Provável

```text
1. partial_coverage_classified_as_complete            : 25 ocorrências (31,25%)
2. evasive_or_insufficient_content_overinterpreted    : 14 ocorrências (17,50%)
3. auxiliary_or_thematic_confused_with_solution       : 11 ocorrências (13,75%)
4. demand_decomposition_or_partial_underestimation    :  9 ocorrências (11,25%)
5. circularity_or_epistemic_uncertainty_undetected    :  7 ocorrências  (8,75%)
6. off_topic_or_antithesis_misclassified              :  5 ocorrências  (6,25%)
7. polarity_or_lexical_absence_overpenalized          :  5 ocorrências  (6,25%)
8. solution_confused_with_auxiliary_or_thematic       :  4 ocorrências  (5,00%)
```

### Análise dos Principais Padrões de Falha

#### Padrão 1: Colapso de Aspectos em Perguntas de Enunciado Simples (`PARTIAL` → `DIRECT`: 25 casos)
- **Mecanismo da Falha:** Em perguntas compostas por uma única oração gramatical onde múltiplos mecanismos interdependentes são requeridos (ex: *B05 Circuit Breaker* exigindo fechado/aberto/meio-aberto, ou *B07 Saga* exigindo orquestração e transações compensatórias), o parser decompôs a pergunta em uma única demanda genérica (`demand_1`).
- **Efeito:** Como a resposta do candidato ofereceu uma proposição operativa válida atendendo a apenas metade do problema (ex: explicou abertura mas ignorou meio-aberto; explicou orquestração mas omitiu compensações), o motor avaliou a demanda única como `FUNCTIONALLY_SOLVES` e atribuiu `aspect_coverage = FULL`, inflando o score para `DIRECT`.

#### Padrão 2: Falsos DIRECTs em Tópicos Correlatos e Históricos (`RELATED` → `DIRECT`: 8 casos)
- **Mecanismo da Falha:** Respostas do Grupo D contendo dados históricos (*D20 NGINX de Igor Sysoev*, *D30 Banco Relacional de Edgar Codd*), especificações de hardware (*D27 Pipelines de CPU com 20 estágios*) ou declarações de experiência (*D22 "Já usei Redis em produção..."*, *D25 "Nossa equipe sobe pods diariamente..."*).
- **Efeito:** A presença de verbos de ação técnicos ("escrito", "atender", "fazer cache", "subir pods") foi classificada como proposição operativa funcional voltada para a pergunta, burlando o filtro de contextualização temática.

#### Padrão 3: Tautologias e Poliptotos sem Ganho Informacional (`UNKNOWN` → `DIRECT`: 6 casos)
- **Mecanismo da Falha:** Casos do Grupo G (*G01 Replicação*, *G08 Compressão*, *G10 Distribuição de Carga*, *G11 Disponibilidade*, *G12 Indexação de Índices*, *G14 Travamento Mútuo*).
- **Efeito:** As frases circulares usaram formas flexionadas ("replicados", "replicadas", "distribuindo", "distribuição") combinadas com conectivos ("mantém", "para", "de forma que"). A regra de ganho informacional baseada em radicais léxicos estáticos considerou "mantém" ou "servidores" como novidade informativa relevante, falhando em identificar a circularidade semântica da resposta.

#### Padrão 4: Disjunção entre `INSUFFICIENT` e `UNKNOWN` (11 casos)
- **Mecanismo da Falha:** Respostas evasivas do Grupo F (ex: "depende do orçamento", "cada caso é um caso") foram classificadas como `UNKNOWN` em vez de `INSUFFICIENT`.
- **Efeito:** Embora ambos os rótulos indiquem ausência de solução técnica pelo candidato, a métrica de concordância exata penaliza essa divergência terminológica interna.

---

## 11. Análise de Invariância de Representação (Grupo J)

O Grupo J avaliou 16 pares idênticos em substância semântica, formulados sob diferentes estilos linguísticos (formal vs. coloquial, voz ativa vs. passiva, conciso vs. detalhado).

### Resultados por Par

| Par | Tema | Ref | Pred 1 | Pred 2 | Consistente? |
|---|---|:---:|:---:|:---:|:---:|
| **Par 01** | eBPF XDP Driver Hook | `DIRECT` | `DIRECT` (Formal) | `DIRECT` (Coloquial) | **SIM** |
| **Par 02** | Ceph CRUSH Algorithmic | `DIRECT` | `DIRECT` (Ativa) | `DIRECT` (Pronominal) | **SIM** |
| **Par 03** | CockroachDB Multi-Raft | `DIRECT` | `DIRECT` (Detalhado) | `DIRECT` (Conciso) | **SIM** |
| **Par 04** | SQLite WAL Append/Shm | `DIRECT` | `DIRECT` (Formal) | `DIRECT` (Coloquial) | **SIM** |
| **Par 05** | Parquet Dictionary/RLE | `DIRECT` | `DIRECT` (Ativa) | `DIRECT` (Passiva) | **SIM** |
| **Par 06** | Token Bucket Algorithm | `DIRECT` | `DIRECT` (Formal) | `DIRECT` (Coloquial) | **SIM** |
| **Par 07** | Fencing Tokens Lock | `DIRECT` | `PARTIAL` (Detalhado) | `PARTIAL` (Conciso) | **NÃO** *(Ambos errados)* |
| **Par 08** | Outbox Pattern CDC | `DIRECT` | `DIRECT` (Ativa) | `DIRECT` (Passiva) | **SIM** |
| **Par 09** | Kafka Zero-Copy Sendfile | `DIRECT` | `DIRECT` (Formal) | `DIRECT` (Coloquial) | **SIM** |
| **Par 10** | Raft Leader Election | `DIRECT` | `DIRECT` (Detalhado) | `OFF_TOPIC` (Conciso) | **NÃO** *(Assimetria)* |
| **Par 11** | Parcial: Exponential Backoff | `PARTIAL` | `PARTIAL` (Formal) | `PARTIAL` (Coloquial) | **SIM** |
| **Par 12** | Parcial: Database Sharding | `PARTIAL` | `PARTIAL` (Ativa) | `PARTIAL` (Passiva) | **SIM** |
| **Par 13** | Parcial: Two-Phase Commit | `PARTIAL` | `DIRECT` (Detalhado) | `DIRECT` (Conciso) | **NÃO** *(Ambos errados)* |
| **Par 14** | Antithesis: Locks Desligados | `OFF_TOPIC` | `OFF_TOPIC` (Formal) | `DIRECT` (Coloquial) | **NÃO** *(Coloquial burlou)* |
| **Par 15** | Antithesis: ACID Desligado | `OFF_TOPIC` | `OFF_TOPIC` (Ativa) | `DIRECT` (Passiva) | **NÃO** *(Passiva burlou)* |
| **Par 16** | Antithesis: Timeouts Zerados | `OFF_TOPIC` | `OFF_TOPIC` (Detalhado) | `OFF_TOPIC` (Conciso) | **SIM** |

- **Pares Consistentes e Corretos:** 11 / 16 (**68,75%**)
- **Meta Exigida:** $\ge 80{,}0\%$
- **Diagnóstico:** As formulações coloquiais e na voz passiva de ações destrutivas (Pares 14 e 15) não acionaram os radicais de antítese no runtime, sendo promovidas a `DIRECT`.

---

## 12. Validação da Salvaguarda de Evitação / Polaridade (Grupo I)

Um dos pontos focais do Stage 31.7.20 foi a criação de um **Avoidance / Risk / Preventative Guard** para impedir que respostas que explicam *por que não realizar uma ação perigosa* fossem taxadas como `OFF_TOPIC`.

O Grupo I testou 14 casos deste cenário adversarial:
- **13 de 14 casos classificados com perfeição (92,86% de acurácia)!**
- Respostas explicando "para evitar desativar locks...", "não se deve ignorar transações..." mantiveram corretamente o rótulo `DIRECT` sem serem capturadas pela antítese.
- Ações destrutivas afirmativas foram corretamente marcadas como `OFF_TOPIC`.
- **Conclusão:** A intervenção arquitetural CR-04 do Stage 31.7.20 demonstrou alta generalização e eficácia neste domínio específico.

---

## 13. Resultados de Integridade e Regressão Canônica

Antes e após a execução do benchmark cego, toda a suíte de regressão automatizada do projeto foi executada:

```powershell
py -m unittest discover tests
Ran 1038 tests in 25.543s: OK (skipped=1, failures=0, errors=0)

py -m unittest tests.test_stage_26_reference_harness
Ran 15 tests in 18.776s: OK (failures=0, errors=0)
```

- **Falhas de regressão:** Zero.
- A estabilidade estrutural do motor e o isolamento dos estágios anteriores foram preservados.

---

## 14. Limitações Metodológicas e Ameaças à Validade

1. **Ausência de Comitê Humano Externo Independente:** A referência foi adjudicada internamente. Isso é documentado formalmente como `REFERENCE_INDEPENDENCE_UNRESOLVED`.
2. **Dependência de Regras Gramaticais Estáticas:** O runtime atual baseia-se em análise léxico-sintática heurística (radicais, classes de verbos, lemas). Casos complexos em que a semântica depende da estrutura lógica profunda (aspectos ocultos em orações simples, metáforas, disjunções lógicas sutis) revelam os limites intrínsecos de abordagens determinísticas puramente baseadas em superfície textual.

---

## 15. Decisão Final de Gate

```text
====================================================================
GATE STATUS: BLIND_SEMANTIC_REVALIDATION_BLOCKED
====================================================================
```

### Justificativa Formal:
1. O protocolo de cegamento foi executado com rigor e integridade impecáveis, gerando evidências auditáveis e reproduzíveis.
2. 6 dos 7 critérios de aceite quantitativos falharam de maneira expressiva:
   - Concordância: 68,00% (alvo $\ge 75\%$)
   - Precisão de DIRECT: 53,00% (alvo $\ge 70\%$)
   - Falsos DIRECTs entre divergências: 58,75% (alvo $\le 10\%$)
   - Recall de PARTIAL: 37,78% (alvo $\ge 60\%$)
   - Invariância de Representação: 68,75% (alvo $\ge 80\%$)
3. A independência da referência permanece `UNRESOLVED`.

Em conformidade com a Seção 11 e a regra canônica do projeto:
> *"Preservar a validade do experimento é mais importante do que obter aprovação."*

O runtime **não está homologado** para produção nem para o fechamento do ciclo de relevância semântica.

---

## 16. Recomendações Objetivas para a Próxima Etapa

Avançar formalmente para:

**Stage 31.7.22 — Root Cause Analysis & Semantic Precision Remediation Architecture (Cycle 4)**

### Linhas de Investigação Mandatórias:
1. **Decomposição Semântica de Demandas Ocultas (RCA-01):** Desenvolver mecanismo para detectar multi-aspectos conceituais em perguntas que não utilizam conjunções explícitas ("e como", "e qual"), impedindo que respostas a aspectos parciais sejam promovidas a `DIRECT`.
2. **Validação de Nexus Unívoco entre Demandas e Proposições (RCA-02):** Corrigir `_evaluate_demand_nexus` para que uma mesma proposição da resposta não possa satisfazer simultaneamente duas demandas distintas apenas por correspondência difusa de palavras-chave.
3. **Detecção Avançada de Circularidade e Ganho Informacional (RCA-03):** Refinar o detector de tautologias para que variações gramaticais e conectivos funcionais ("mantém", "para", "servidores") não sejam contabilizados como "novidade informativa".
4. **Filtro de Desqualificação para Afirmações Triviais e Declarações de Experiência (RCA-04):** Garantir que menções biográficas, histórico institucional e declarações autobiográficas ("já usei em produção") sejam categorizadas terminantemente como `RELATED`, nunca como solução funcional.
