---
type: reference
status: understood
confidence: 100
created: 2026-09-20
updated: 2026-09-20
tags:
  - interview-evaluation
  - calibration
  - semantic
  - validation
---
# Etapa 28 — Semantic / Blind Calibration

## 1. Objetivo

Validar se respostas sintéticas com características técnicas conhecidas por um oracle independente produzem Evidence Set, dimensões, score e confidence semanticamente coerentes, sem entregar o oracle ao runtime.

```text
RAW TRANSCRIPT
↓
20.1–20.7
↓
STRUCTURED INTERVIEW
↓
EVIDENCE MODEL
↓
EVIDENCE SET
↓
RUBRIC / EVALUATION ENGINE
↓
EVALUATION
↓
ORACLE COMPARISON
```

Nenhuma entrevista real foi processada. Não houve LLM, internet, Azure, OpenAI ou dependência externa.

## 2. Relação com Etapas 26 e 27

| Etapa | Validação |
|---|---|
| 26 | contratos internos e execução determinística com fixtures estruturados |
| 27 | execução end-to-end sobre uma transcrição bruta sintética |
| 28 | coerência semântica blind entre características independentes e avaliação produzida |

A Etapa 28 adiciona calibração; não substitui as etapas anteriores.

## 3. Blindness

Os fixtures executados contêm somente:

```text
fixture_id
pipeline_version
participants
raw_transcript
```

Os seguintes campos são mantidos em estrutura separada e removidos antes da execução:

```text
oracle
expected_score
expected_score_range
expected_dimensions
expected_quality
calibration_label
evidence_specs
evaluation_specs
```

O Evaluation Engine de referência recebe Evidence Set produzido pelo runtime. A comparação com o oracle ocorre somente após `run_pipeline` terminar.

Não há branches por `case_id`, score esperado ou oracle no runtime.

## 4. Casos

Foram definidos 20 casos lógicos, com 21 execuções porque `CAL28-20` possui duas versões para invariância de senioridade:

```text
CAL28-01 Excellent Answer
CAL28-02 Correct but Superficial
CAL28-03 Incomplete but Correct
CAL28-04 Technically Incorrect
CAL28-05 Partially Correct
CAL28-06 Strong Reasoning
CAL28-07 Strong Practical Application
CAL28-08 Trade-off Demonstration
CAL28-09 Experience Declaration Only
CAL28-10 Demonstrated Experience
CAL28-11 Self-Correction
CAL28-12 Hypothetical Answer
CAL28-13 Uncertainty
CAL28-14 Off-topic Answer
CAL28-15 N/A Dimension
CAL28-16 Contradictory Evidence
CAL28-17 Multiple Evidence Types
CAL28-18 Strong Answer With Few Words
CAL28-19 Verbose Without Additional Evidence
CAL28-20 Seniority Declaration Invariance
```

O oracle declara características, não scores rígidos. As faixas numéricas são deliberadamente amplas quando o julgamento integrado da Rubric permite variação.

## 5. Características verificadas

O Evidence Set e as avaliações foram comparados contra:

- correctness;
- completeness;
- depth;
- reasoning;
- practical application;
- trade-offs;
- technical error;
- experience declaration;
- demonstrated experience;
- self-correction;
- hypothesis;
- uncertainty;
- off-topic;
- contradiction;
- múltiplos tipos de evidência;
- N/A sem conversão para zero.

Também foram validadas source traceability, `confidence` separada de `score` e o consumo das avaliações pelo Report Handoff.

## 6. Resultado

Execução:

```text
py -3 .\run_semantic_blind_calibration.py --verbose
```

Resultado real:

```text
20 casos lógicos
21 execuções blind
21 PASS
0 FAIL
0 BLOCKED
```

Suítes:

```text
Stage 28: 29 testes
Stage 26 + Stage 27 + Stage 28: 140 testes
140/140 PASS
```

Status:

```text
READY_WITH_WARNINGS
```

## 7. Invariâncias

Passaram:

- verbosity: texto repetitivo não criou profundidade nem score superior;
- eloquence: estilo não foi usado como evidência técnica;
- seniority: declaração de senioridade não alterou score;
- complexity: não foi adicionada complexidade externa à resposta;
- CV/context: metadata externa permaneceu fora do Evidence Set e Evaluation;
- confidence: não foi usada como multiplicador automático do score.

## 8. Falhas iniciais e correções

### CAL28-01 — sinais semânticos insuficientes

```text
Falha: resposta correta superficial foi classificada como forte em completeness/depth.
Causa: heurística inicial usava somente tamanho e não distinguia resposta curta de resposta densa.
Correção: separar sinais de densidade, completude, raciocínio e repetição.
Regression: PASS.
```

### CAL28-04 — erro factual não detectado

```text
Falha: formulação "pior tempo de todas" não era reconhecida como technical_error.
Causa: vocabulário de erro insuficiente.
Correção: adicionar o sinal textual genérico à classificação blind.
Regression: PASS.
```

### CAL28-19 — verbosity superava resposta curta

```text
Falha: repetição de "latência" criava score maior que resposta curta densa.
Causa: comprimento era interpretado como completude.
Correção: detectar repetição sem evidência adicional e limitar depth/completeness.
Regression: PASS.
```

Nenhum peso, threshold, dimensão ou regra canônica da Rubric/Evaluation Engine foi alterado.

## 9. Limitações

1. O caminho blind é uma implementação determinística de referência baseada em sinais textuais controlados.
2. Ele não representa compreensão semântica geral nem substitui um modelo de produção.
3. As faixas do oracle são amplas e validam coerência, não uma nota decimal exata.
4. Os artefatos históricos das Etapas 19/19.1 continuam indisponíveis.
5. Os casos são sintéticos e não representam desempenho de candidato real.

## 10. Gate

```text
SEMANTIC_BLIND_CALIBRATION_COMPLETE
```

Critérios atendidos:

- oracle separado do input runtime;
- 20 casos lógicos executados;
- Evidence, dimensões, score e confidence comparados;
- experiência declarada separada de demonstrada;
- autocorreção, hipótese, incerteza e contradição preservadas;
- N/A validado;
- invariâncias validadas;
- traceability validada;
- Stage 26 e Stage 27 regressions passaram;
- 0 falhas.

Status final:

```text
READY_WITH_WARNINGS
```

O warning corresponde ao caráter sintético e determinístico do runtime e à ausência dos artefatos históricos de calibração.

## Ver também

- [[Reference Runtime]]
- [[Synthetic Interview Full Run]]
- [[Interview Evaluation Pipeline]]
- [[End-to-End Validation]]
- [[Evidence Model]]
- [[Scoring Rubric]]
- [[Evaluation Engine]]
- [[Interview Evaluation MOC]]
