---
type: reference
status: understood
confidence: 100
created: 2026-09-20
updated: 2026-09-20
tags:
  - interview-evaluation
  - runtime
  - synthetic
  - end-to-end
---
# Etapa 27 — Synthetic Interview Full Run / Raw Transcript Execution

## 1. Objetivo

Validar a cadeia completa a partir de uma transcrição bruta sintética:

```text
RAW TRANSCRIPT
↓
20.1–20.7
↓
STRUCTURED INTERVIEW
↓
EVIDENCE SET
↓
EVALUATIONS
↓
REPORT HANDOFF
```

Esta execução não processa entrevista real, não usa LLM, internet, Azure, OpenAI ou serviços externos.

## 2. Diferença em relação à Etapa 26

| Etapa | Entrada principal | O que foi validado |
|---|---|---|
| 26 | fixtures semanticamente estruturados | contratos internos, gates, traceability e idempotência |
| 27 | 28 segmentos de transcrição bruta sintética | adaptação controlada de texto bruto para 20.1–20.7 e execução end-to-end |

O runtime continua sendo uma implementação de referência determinística, não um parser NLP/LLM de produção.

## 3. Cenário

Participantes:

```text
Ana Martins   — candidate
Bruno Lima    — interviewer
Carla Souza   — observer
```

O cenário contém:

- timestamps e mudanças de speaker;
- 12 perguntas técnicas identificadas;
- 13 respostas estruturadas, incluindo respostas multi-segmento e respostas `missing`;
- follow-up e reformulação;
- pergunta feita pelo candidato;
- intervenção do entrevistador;
- comentário do observador;
- speaker ambíguo;
- erro de transcrição `"Spring Boto"`;
- resposta forte, superficial, incorreta, parcialmente correta e hipotética;
- autocorreção;
- experiência declarada e experiência demonstrada;
- `"não lembro"`;
- pergunta sem resposta.

O transcript bruto integral está em `tests/synthetic_interview.py` e é preservado no artefato `raw_transcript`.

## 4. Oracle

O oracle do cenário define propriedades observáveis, não instruções de implementação:

```yaml
oracle:
  must_preserve_original_transcript: true
  must_have_candidate_question: true
  must_have_missing_response: true
  must_have_ambiguous_segment: true
  must_have_experience_declaration: R8
  must_have_demonstrated_experience: R9
  must_have_self_correction: R6
  must_have_hypothesis: R10
  must_have_uncertainty: R11
  must_normalize_transcription_error: R12
```

Os scores e características de avaliação permanecem dados do cenário para o adaptador de referência do Evaluation Engine; não são regras especiais adicionadas ao pipeline.

## 5. Execução

Comando principal:

```text
py -3 .\run_synthetic_interview.py
```

Modo detalhado:

```text
py -3 .\run_synthetic_interview.py --verbose
```

Execução de um estágio:

```text
py -3 .\run_synthetic_interview.py --stage 20.1
py -3 .\run_synthetic_interview.py --stage 20.7
py -3 .\run_synthetic_interview.py --stage evidence
py -3 .\run_synthetic_interview.py --stage evaluation
```

## 6. Resultado real

Execução registrada em `2026-09-20`:

```text
Raw Transcript: PASS
20.1 Participant Identification: PASS
20.2 Speaker Attribution: PASS
20.3 Question Extraction: PASS
20.4 Response Extraction: PASS
20.5 Reconstruction: PASS
20.6 Question/Response Linking: PASS
20.7 Validation: PASS_WITH_WARNING
Structured Interview: PASS
Evidence Model: PASS
Evidence Set: PASS
Rubric: PASS
Evaluation Engine: PASS
Report Handoff: PASS
Traceability: PASS
Idempotency: PASS
Reprocessing: PASS
Stale Detection: PASS
Invariance Tests: PASS
Responsibility Tests: PASS
```

Contagens observadas:

```yaml
participants: 3
segments: 28
questions: 12
responses: 13
evidence: 11
evaluations: 10
```

Suíte automatizada:

```text
80 Stage 27 tests: PASS
111 total repository tests: PASS
0 FAIL
0 BLOCKED
```

O `READY_WITH_WARNINGS` é esperado porque o segmento `RAW-26` possui speaker ambíguo. O warning foi preservado através da validação, Evidence Set, Evaluation e Report Handoff.

## 7. Traceability

A cadeia foi validada:

```text
participant_id
  ↓
speaker_id / participant_id
  ↓
question_id
  ↓
response_id
  ↓
evidence_id
  ↓
evaluation.id
  ↓
report
  ↓
source.segment_ids + timestamps
  ↓
raw_transcript
```

O Report Handoff recebeu candidato, participantes, perguntas, respostas, evidências, avaliações, validação, warnings e rastreabilidade. Nenhum relatório foi persistido em `06 - Reports/`.

## 8. Invariantes

Passaram:

- tamanho/verbosidade: texto adicional não aumentou score;
- eloquência: score não dependeu de articulação superficial;
- senioridade declarada: metadata externa não alterou avaliação;
- complexidade: complexidade declarada não gerou crédito;
- CV/contexto externo: metadata externa não alterou Evidence Set ou Evaluation;
- Job Context: contexto da vaga não alterou evidência ou score;
- idempotência: IDs e artefatos permaneceram equivalentes;
- reprocessamento: alteração do transcript alterou artefatos derivados;
- stale detection: versões upstream/evidence divergentes produziram warning.

## 9. Fronteiras de responsabilidade

Os testes confirmaram:

- Transcription Processing não calcula score;
- Evidence Model não calcula score final;
- Rubric não extrai transcript;
- Evaluation Engine consome Evidence Set;
- Pipeline não redefine critérios nem recalcula score;
- Report Handoff consome avaliações existentes;
- Job Context não altera a evidência técnica.

## 10. Falhas e correções

### Initial Run — quantidade de perguntas

```text
Falha: teste esperava 12 perguntas.
Actual: 11 perguntas técnicas foram identificadas.
Causa: o transcript continha 11 perguntas do entrevistador; a pergunta do candidato foi corretamente excluída.
Correção: ajustar a expectativa do teste para a entrada real, sem inserir pergunta artificial.
Regression: suíte Stage 27 e suíte completa passaram.
```

Não houve alteração de Rubric, Evidence Model ou Evaluation Engine.

## 11. Limitações

1. O adaptador reconhece uma transcrição bruta sintética controlada por regras determinísticas.
2. Ele não é um parser NLP/LLM de produção.
3. As avaliações usam o adaptador de referência existente e características controladas do cenário.
4. Não houve entrevista real nem persistência de relatório de candidato.
5. Os artefatos históricos de calibração das Etapas 19/19.1 continuam indisponíveis.

## 12. Gate da Etapa 27

```text
SYNTHETIC_INTERVIEW_FULL_RUN_COMPLETE
```

Status:

```text
READY_WITH_WARNINGS
```

O pipeline recebeu uma transcrição bruta sintética, executou 20.1–20.7, produziu Structured Interview, Evidence Set, avaliações e Report Handoff. Os warnings são não críticos e documentados; não há falha que impeça confiar na validação do contrato.

## Ver também

- [[Reference Runtime]]
- [[Interview Evaluation Pipeline]]
- [[Transcription Processing Model]]
- [[End-to-End Validation]]
- [[Evidence Model]]
- [[Evaluation Engine]]
- [[Scoring Rubric]]
- [[Interview Evaluation MOC]]
