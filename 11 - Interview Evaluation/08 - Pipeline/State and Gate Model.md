---
type: reference
status: understood
confidence: 100
created: 2026-10-04
updated: 2026-10-04
tags:
  - interview-evaluation
  - pipeline
  - gates
---

# State and Gate Model

## Execution states

```text
PENDING
RUNNING
COMPLETED
COMPLETED_WITH_WARNINGS
BLOCKED
FAILED
REQUIRES_HUMAN_REVIEW
APPROVAL_REQUIRED
```

`readiness` remains structural. It is never a score, seniority, hiring or approval metric.

## State meanings

| State | Meaning | Downstream behavior |
|---|---|---|
| `PENDING` | not started | no component has run |
| `RUNNING` | execution in progress | incomplete result is not final |
| `COMPLETED` | stage completed without warnings | controlled handoff is allowed |
| `COMPLETED_WITH_WARNINGS` | stage completed with preserved limitations | handoff is allowed only when the contract permits it |
| `BLOCKED` | rule or structural blocker | stop; do not create downstream completion artifacts |
| `FAILED` | execution or input failure | stop; record failed stage and affected artifacts |
| `REQUIRES_HUMAN_REVIEW` | human decision is required | stop before downstream processing |
| `APPROVAL_REQUIRED` | a required gate was not approved | stop before the gated action |

## Gate rules

| Gate | Required state | Result |
|---|---|---|
| Stage 20.7 → Evidence Set | `READY` or `READY_WITH_WARNINGS` | continue |
| Stage 20.7 blocked | `BLOCKED` | stop and require review |
| Human review | explicit approval | continue; never automatic |
| Evidence Set → Evaluation | valid Evidence Set | continue |
| Global semantic audit → report | `PASS` or `PASS_WITH_WARNINGS` | report handoff may be requested |
| Report generation | explicit report approval | only then generate final report |

`READY_WITH_WARNINGS` is propagated and is never silently converted into approval.

## Pipeline state contract

```yaml
pipeline:
  id: PIPE-...
  status: PENDING
  current_stage: ""
  completed_stages: []
  warnings: []
  blockers: []
  failed_stage: null
  affected_artifacts: []
  candidate: null
  readiness: null
  input_hash: ""
  pipeline_version: "24-orchestration-1"
```

## Stage 24 gate

```text
PIPELINE_ORCHESTRATION_COMPLETE
```

or, when inherited warnings remain:

```text
PIPELINE_ORCHESTRATION_COMPLETE_WITH_WARNINGS
```

Stage 25 validates this model with synthetic fixtures only. It does not process the real pilot or persist a real report.
