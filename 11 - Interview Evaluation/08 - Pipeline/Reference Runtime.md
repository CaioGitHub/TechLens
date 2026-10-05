---
type: reference
status: understood
confidence: 100
created: 2026-10-04
updated: 2026-10-04
tags:
  - interview-evaluation
  - runtime
  - pipeline
---

# Etapa 26 — Reference Runtime

## Definition

The reference runtime is a deterministic Python standard-library implementation used to validate documented contracts with synthetic, annotated fixtures. It is not a production runtime and is not equivalent to a semantic evaluator for real interviews.

## Responsibilities

The runtime provides reference implementations for:

```text
20.1 participant identification
20.2 speaker attribution
20.3 question extraction
20.4 response extraction
20.5 reconstruction / normalization
20.6 question-response linking
20.7 validation
21 Evidence Set output
23 individual evaluation output contract
Report Handoff
Stage 24 orchestration
Stage 25 end-to-end checks
```

The Rubric, Evidence Model and semantic rules remain documented contracts. Fixture specifications provide deterministic outputs for testing; they do not constitute production scoring logic.

## Inputs and outputs

Input is a mapping containing a stable `fixture_id`, participants and a synthetic transcript. Optional fixture metadata controls explicit test cases such as warnings, reconstruction, N/A and blockers.

Outputs include:

- stable IDs derived from content and stage identifiers;
- structured interview artifacts;
- Evidence Set and individual evaluations;
- report handoff;
- stage statuses, warnings and errors;
- traceability from evaluation to evidence and source segments;
- orchestration hashes, gates and version snapshots.

Operational timestamps may be present in `run_pipeline` results. They are excluded only by the harness's `deterministic_projection`; all test-relevant artifacts remain included.

## States and errors

The runtime preserves `READY`, `READY_WITH_WARNINGS`, `BLOCKED` and `COMPLETED` semantics. The orchestration adds `FAILED`, `REQUIRES_HUMAN_REVIEW`, `APPROVAL_REQUIRED` and `COMPLETED_WITH_WARNINGS`.

Blocked validation, missing required artifacts and invalid references stop downstream completion. Warnings propagate as metadata and are never converted into negative candidate evidence.

## Determinism guarantees

For equal fixture content and component versions:

- stable IDs and artifact content are equivalent;
- ordering of questions, responses, evidence and evaluations is preserved;
- warnings and final states are equivalent;
- content hashes are equivalent;
- input changes are detectable and invalidate dependent artifacts.

Execution timestamps and process duration are operational metadata and are not deterministic.

## Isolation guarantees

Fixtures contain no real interview artifacts or candidate identifiers. The harness:

- runs from the repository root with explicit commands;
- sets `PYTHONDONTWRITEBYTECODE=1` for child suites;
- writes reports only when an explicit output path is provided;
- does not modify historical pilot files;
- uses in-memory version storage for controlled tests;
- does not contact external services.

## Limitations

The runtime does not parse free-form transcripts, perform production semantic evaluation, persist real candidate reports, or replace human review. Approvals in end-to-end tests are explicit simulated inputs.
