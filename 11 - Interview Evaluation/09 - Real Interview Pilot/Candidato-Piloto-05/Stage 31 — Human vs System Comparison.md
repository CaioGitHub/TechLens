# Stage 31 — Human vs System Comparison

## Objective

Comparar uma avaliação humana independente, produzida a partir do transcript original e da rubrica, com a avaliação congelada do sistema. A comparação é um estudo de caso de um único piloto e não constitui benchmark estatístico.

## Independence

A avaliação humana foi congelada em `Stage 31 — Human Evaluation Independent.md` antes da consulta aos artefatos do sistema. Ela utiliza IDs próprios `H-E##`. Nenhum score, ID de evidência ou conclusão do sistema foi reutilizado como evidência humana.

## Questions Compared

Foram comparadas 11 perguntas avaliáveis. A fala `E tem uma Daily também, só nossa, né?` foi considerada não avaliável por ambas as análises. `R26` e `R43` foram considerados segmentos contextuais sem unidade avaliável suficiente, sem vínculo artificial.

## Evidence Comparison

| Pattern | Result |
|---|---|
| Same semantic evidence | Encontrado em Q2, Q4, Q6, Q8 e Q10: ambas as avaliações identificam o núcleo observável da resposta, embora com IDs e redações independentes. |
| Different evidence, equivalent conclusion | Encontrado em Q3 e Q7: o sistema usa uma evidência mais estreita, enquanto a avaliação humana registra a limitação de completude. |
| Same evidence, different interpretation | Encontrado em Q1, Q5, Q9 e Q11: o sistema trata evidência limitada/declarativa como correctness forte; a avaliação humana mantém qualificação parcial ou insuficiente. |
| Human-only / system-only | A avaliação humana explicita a divergência de enquadramento REST versus mensageria em Q5 e a natureza declarativa de experiência em Q2, Q9 e Q11. O sistema não explicita essas distinções no Evidence Set materializado. |

## Dimension Comparison

As dimensões sistêmicas usam um padrão repetido de `correctness: Strong`, `depth: Partial/Weak`, `practical_application: Weak` e `trade_offs: Weak`. A avaliação humana aplicou `N/A` quando a pergunta não exigia a dimensão e qualificou separadamente conhecimento, experiência declarada e evidência insuficiente.

| Category | Questions | Classification |
|---|---|---|
| Semantically aligned | Q2, Q4, Q8 | AGREEMENT or MINOR_DIVERGENCE |
| Limited evidence interpreted differently | Q1, Q3, Q6, Q7, Q9, Q11 | MATERIAL_DIVERGENCE; mostly `EVIDENCE_OVERINTERPRETED` / `SCORE_CALIBRATION` |
| Question/answer mismatch | Q5 | MATERIAL_DIVERGENCE; `QUESTION_CLASSIFICATION` and `SYSTEM_ERROR` |
| Troubleshooting weighting | Q10 | MATERIAL_DIVERGENCE; `DIMENSION_INTERPRETATION`, with a defensible human/system disagreement on the value of the proposed debugging path |

## Score Comparison

| Question | Human | System | Difference | Cause | Classification | Impact |
|---|---:|---:|---:|---|---|---|
| Q1 | 4.0 | 6.0 | 2.00 | Limited declaration treated as technically strong | EVIDENCE_OVERINTERPRETED / SYSTEM_ERROR | System overstates Open Finance evidence |
| Q2 | 7.0 | 7.05 | 0.05 | Same broad experience evidence; different precision | MINOR_DIVERGENCE | No material impact |
| Q3 | 4.0 | 6.0 | 2.00 | Fragmented Java/backend answer treated as strong correctness | EVIDENCE_OVERINTERPRETED / SYSTEM_ERROR | Technology coverage overstated |
| Q4 | 8.0 | 7.05 | 0.95 | Calibration around a direct factual answer | VALID_TECHNICAL_DISAGREEMENT | No material traceability impact |
| Q5 | 2.0 | 7.05 | 5.05 | Kafka/Rabbit explanation does not answer REST framing | QUESTION_CLASSIFICATION / SYSTEM_ERROR | Largest divergence; materially affects evaluation |
| Q6 | 5.0 | 7.05 | 2.05 | JDBC answer is directionally correct but vague | EVIDENCE_OVERINTERPRETED / SYSTEM_ERROR | Completeness and correctness overstated |
| Q7 | 5.0 | 6.0 | 1.00 | Architecture declaration without explanation | EVIDENCE_OVERINTERPRETED / SCORE_CALIBRATION | Limited impact |
| Q8 | 7.0 | 7.65 | 0.65 | Same conceptual evidence; integrated reasoning weighted differently | VALID_TECHNICAL_DISAGREEMENT | No material integrity impact |
| Q9 | 4.0 | 7.05 | 3.05 | Tool declaration treated as broad observability competence | EVIDENCE_OVERINTERPRETED / SYSTEM_ERROR | Experience demonstration overstated |
| Q10 | 6.0 | 7.65 | 1.65 | Debug/log/print path weighted as strong reasoning | DIMENSION_INTERPRETATION | Material calibration difference, but reasoning is technically defensible |
| Q11 | 4.0 | 7.65 | 3.65 | Copilot-use declaration treated as strong answer | EVIDENCE_OVERINTERPRETED / SYSTEM_ERROR | AI-use evidence materially overstated |

Descriptive indicators:

- Questions compared: `11`
- Human average: `5.09`
- System average: `6.93`
- Mean absolute difference: `2.01`
- Maximum difference: `5.05` (Q5)
- Human median: `5.0`
- System median: `7.05`

These numbers are descriptive for one interview and are not an accuracy metric.

## Experience Comparison

Both analyses preserve the distinction between experience declaration and demonstrated experience at the source level. The human evaluation makes the distinction explicit for Q2, Q9 and Q11; the system's materialized taxonomy does not expose dedicated `experience_declaration` versus `demonstrated_experience` categories in this pilot. This is a known limitation and contributes to `EVIDENCE_OVERINTERPRETED` classifications, but no invented experience was added.

## Troubleshooting Comparison

Both analyses identify logs and debugging as evidence in Q10. The human evaluation treats this as a plausible but incomplete investigation path, lacking metrics, traces, isolation, validation and root cause. The system emphasizes reasoning more strongly. This is a material dimension divergence, but the proposed approach itself is technically defensible; no `SYSTEM_ERROR` is assigned solely for preferring a different weighting.

## Architecture Comparison

For Q7/Q8, both analyses recognize the candidate's distinction between layered architecture and conceptual knowledge of hexagonal architecture. The human evaluation gives Q8 a 7.0 because the explanation is correct but lacks implementation detail; the system gives 7.65. This is a `VALID_TECHNICAL_DISAGREEMENT`, not evidence of a traceability failure.

## Global Assessment Comparison

The human assessment describes a technically mixed interview: concrete professional history, defensible Java/version and hexagonal concepts, but limited demonstration in JDBC, observability, troubleshooting depth and AI usage, with a significant mismatch on Q5.

The system provides 11 evaluations and a mean of 6.93, but its materialized global artifact does not contain a detailed qualitative strengths/gaps assessment. Therefore the global comparison is limited: the numerical system result is higher and less differentiated than the human interpretation, and the system cannot be credited with a detailed global conclusion that it did not materialize.

## Divergences

The most important divergences are Q5, Q9 and Q11, plus Q1/Q3/Q6. They are not explained by missing source segments or speaker errors. In those cases, the system's Evidence Set contains source-supported text, but the evaluation assigns stronger correctness/completeness than the text supports. These are classified as `SYSTEM_ERROR` because the problem is interpretive, not merely numerical calibration.

Q4 and Q8 are `VALID_TECHNICAL_DISAGREEMENT`. Q10 is a controlled `DIMENSION_INTERPRETATION` divergence: both readings are technically defensible, although the system weights the limited troubleshooting path more favorably.

No human contamination was found. The human evaluation was frozen before system artifacts were opened. No human-review error was necessary to explain the material divergences identified.

## Summary

The system is traceable and preserves the transcript, but this single-pilot comparison does not support unconditional approval of the evaluation quality. The principal risk is overinterpretation of sparse or declarative evidence, especially when a response is directionally related to a topic but does not fully answer the question.

This result does not justify changing the Evaluation Engine during Stage 31. The divergences must first be reproduced in a subsequent controlled correction/audit stage. No score, rubric, evidence model or engine was changed here.

## Limitations

- Uma entrevista e um avaliador humano não permitem estimar concordância geral ou accuracy.
- Não houve segundo humano independente para medir a variabilidade da avaliação humana.
- A transcrição contém ruído e algumas perguntas têm formulação ambígua.
- A comparação usa o materializador pós-correção disponível; sua ausência de análise global detalhada limita a comparação qualitativa.

## Gate

`HUMAN_VS_SYSTEM_BLOCKED`
