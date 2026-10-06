---
type: reference
status: understood
confidence: 100
created: 2026-10-05
updated: 2026-10-05
tags:
  - interview-evaluation
  - evaluation-engine
  - pipeline
  - reference-runtime
---

# Reference Evaluation Engine Runtime

## Purpose

This runtime implements the executable Stage 23 consolidation boundary. It consumes the canonical individual evaluations and Evidence Set, validates their cross-references, and produces an in-memory `Interview Evaluation` structure.

It does not process raw transcripts, identify speakers, extract questions, reconstruct responses, create evidence, recalculate individual scores, or execute Stage 23.1.

## Inputs

```text
Individual Evaluations v2.md
Evidence Set v1.md
```

The loader preserves the input sources as metadata. The runtime accepts the parsed `EvaluationInput` structure as well, which permits isolated tests without reading files.

## Output

The output is an in-memory dictionary with:

- Stage 23 status and gate;
- calculated count, average, median, minimum and maximum;
- explicit half-open score distribution (`0–2`, `2–4`, `4–6`, `6–8`, final `8–10`);
- domain and complexity summaries;
- dimension coverage that excludes `N/A`;
- strengths, gaps and existing errors;
- bounded limitations and confidence;
- global technical assessment;
- evaluation/question/evidence/source traceability.

No `Interview Evaluation v2.md` is created in this stage.

## Validation

Before aggregation, the runtime validates:

- unique evaluation and evidence IDs;
- scores in the `0–10` range;
- allowed confidence values;
- known dimensions;
- evaluation-to-evidence references;
- question and response references;
- non-empty source segment references;
- exclusion of candidate questions and excluded responses;
- exclusion of `R31`/`RAW-065` from the Q10 result.

Invalid input raises `EvaluationInputError`; it is not converted into a successful-looking result.

## Aggregation rules

The evaluated question set is derived from the input. Q8 and Q12 are represented as non-evaluated context and never receive an artificial score. Candidate questions are not part of the evaluation set.

Average, median, minimum, maximum and distribution are calculated from the supplied scores. The historical value `4.7` is only a regression expectation for the current pilot; it is not used as an input or constant.

Domains and complexity levels are derived from the individual evaluation metadata. Empty complexity levels are reported as `Not evaluated`, never as zero. Dimension summaries count only applicable dimensions; `N/A` is not treated as zero.

Confidence is deterministic and qualitative. The current rule produces `medium` when coverage is limited, advanced complexity is absent, or individual confidence is not uniform. This is a runtime limitation marker, not a candidate classification.

## Traceability and invariants

The output preserves:

```text
evaluation_id
    ↓
question_id
    ↓
evidence_id
    ↓
source.segment_ids
```

The runtime does not create evidence or alter individual scores. Existing error severities are consumed from the input; for example, Q5 remains `relevant` unless the caller changes the input.

The runtime is independent of:

- `Interview Evaluation v1.md`;
- transcripts;
- CV or LinkedIn data;
- Job Context;
- seniority;
- ranking;
- hiring decisions;
- external services.

## Determinism and immutability

Inputs are deep-copied before processing. The same input produces equivalent output regardless of evaluation order, and consistent ID renaming preserves numerical semantics. No timestamps, random values, filesystem iteration order or global mutable state participate in the calculation.

## Historical report relationship

`Interview Evaluation v1.md` is a historical/regression comparison artifact only. It is deliberately not loaded by `run_evaluation_engine`. Tests corrupt its displayed statistics and verify that the runtime still calculates from `Individual Evaluations v2.md` and `Evidence Set v1.md`.

## Limitations

- The Markdown loader is intentionally scoped to the current canonical evaluation and evidence schemas.
- Qualitative global prose is a deterministic bounded synthesis, not a semantic LLM evaluator.
- The runtime consolidates existing individual judgments; it does not independently reassess candidate answers.
- Stage 23.1 remains outside this component and is marked `NOT_EXECUTED`.
- The output is in memory; no historical pilot report is overwritten or generated.

## Tests

`tests/test_stage_23_evaluation_engine_runtime.py` covers input validation, aggregation, exclusions, Q5/Q8/Q10/Q12 rules, domains, complexity, dimensions, strengths, gaps, errors, confidence, traceability, idempotency, input immutability, invariance, historical independence and corruption resistance.

## Gate

```text
REFERENCE_EVALUATION_ENGINE_RUNTIME_COMPLETE_WITH_WARNINGS
```

The warning state reflects bounded coverage and the absence of advanced questions in the current pilot. This runtime does not authorize Stage 23.1 automatically.
