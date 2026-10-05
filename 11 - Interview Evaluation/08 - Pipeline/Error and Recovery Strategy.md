---
type: troubleshooting
status: understood
confidence: 100
created: 2026-10-04
updated: 2026-10-04
tags:
  - interview-evaluation
  - pipeline
  - error-handling
---

# Error and Recovery Strategy

## Error classes

| Class | Example | State | Recovery |
|---|---|---|---|
| Invalid input | missing `fixture_id`, participants or transcript | `FAILED` | correct input and rerun |
| Missing artifact | required upstream output absent | `BLOCKED` | restore the source artifact or restart from the owning stage |
| Validation blocker | central attribution/linking failure | `BLOCKED` | human review; do not infer |
| Runtime failure | component raises unexpectedly | `FAILED` | inspect failed stage, preserve result, retry after correction |
| Warning | limited reconstruction or ambiguous non-central segment | `COMPLETED_WITH_WARNINGS` | propagate warning; human review remains separate |
| Audit pending | Stage 23.1 not approved | `APPROVAL_REQUIRED` | complete or approve the audit |
| Report pending | no explicit report approval | `APPROVAL_REQUIRED` | request approval; do not generate report |
| Stale input | input hash differs from prior result | invalidation recorded | rerun dependent stages; preserve old version |
| Invalid reference | evaluation points to absent evidence/source | `BLOCKED` | repair the producing artifact; never fabricate a reference |

## Failure invariants

- A failed stage never produces a success-shaped downstream artifact.
- A blocked validation never produces Evidence Set, evaluations or report.
- Warnings are not converted into negative evidence.
- Retry reuses stable IDs and never deletes historical snapshots.
- Input content hashes, not timestamps, determine staleness.
- A changed input invalidates the dependent chain from the input boundary.

## Resume behavior

`resume_orchestration(previous_result, fixture, ...)`:

1. compares the previous input hash with the current content hash;
2. reuses the previous result when hashes match;
3. records invalidation and reruns the chain when hashes differ;
4. preserves the previous result in `OrchestrationStore`.

The store is intentionally in-memory and is a reference/test mechanism, not production persistence.

## Human intervention

Human review is mandatory before downstream processing in Stage 24. The orchestrator records `REQUIRES_HUMAN_REVIEW` when that approval is absent. It does not resolve ambiguity, approve the Structured Interview, approve the semantic audit or make hiring decisions.

## Report safety

The runtime's `report` artifact is a handoff representation. Final report generation is a separate explicit gate and is disabled unless both the global audit and report approval are present. Stage 24 does not write a real candidate report.
