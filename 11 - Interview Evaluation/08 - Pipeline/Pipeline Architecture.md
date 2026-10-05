---
type: architecture
status: understood
confidence: 100
created: 2026-10-04
updated: 2026-10-04
tags:
  - interview-evaluation
  - pipeline
  - orchestration
---

# Pipeline Architecture

## Purpose

Stage 24 coordinates the existing contracts. It does not reimplement transcription processing, Evidence Model, Rubric, Evaluation Engine or semantic auditing.

## Canonical flow

```text
Raw transcription
  ↓
20.1 Participant identification
  ↓
20.2 Speaker attribution
  ↓
20.3 Question extraction
  ↓
20.4 Response extraction
  ↓
20.5 Reconstruction and normalization
  ↓
20.6 Question/response linking
  ↓
20.7 Validation
  ↓
Explicit human review / approval
  ↓
Structured Interview handoff
  ↓
21 Evidence Model / Evidence Set
  ↓
22 Rubric contract
  ↓
23 Evaluation Engine
  ↓
23.1 Global semantic audit
  ↓
Explicit report approval
  ↓
Report handoff / final report generation
```

The reference runtime provides the deterministic component execution for 20.1–20.7, Evidence Set, individual evaluations and Report Handoff. `reference_runtime/orchestration.py` supplies the Stage 24 state, approval, integrity, version and recovery boundary around it.

## Boundaries

The orchestration layer:

- validates required inputs before execution;
- requires explicit human approval;
- transports artifacts and warnings;
- stops after a blocking validation result;
- verifies evidence-to-source references;
- records content hashes and versions;
- exposes audit and report approval gates;
- preserves prior versions in `OrchestrationStore`.

It does not:

- resolve ambiguous speakers;
- invent questions, answers, evidence IDs or source segments;
- calculate scores or weights;
- reinterpret missing/unknown/needs-review;
- infer seniority, job fit or hiring decisions;
- persist a real candidate report during Stage 24.

## Pilot compatibility

The real pilot remains historical input only. Stage 24 does not reprocess its transcript, change its Evidence Set, alter individual evaluations, replace the consolidated evaluation or create a report.

## Implementation

```text
reference_runtime/orchestration.py
```

The implementation is deterministic for equal input content and component versions. Execution timestamps are not part of the input identity.
