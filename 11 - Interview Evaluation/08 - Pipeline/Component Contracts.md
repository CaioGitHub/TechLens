---
type: reference
status: understood
confidence: 100
created: 2026-10-04
updated: 2026-10-04
tags:
  - interview-evaluation
  - pipeline
  - contracts
---

# Component Contracts

| Component | Input | Output | Preconditions | Postconditions | Blocking conditions |
|---|---|---|---|---|---|
| 20.1 Participant identification | raw transcript | participants | transcript mapping exists | stable participant IDs and roles are available | invalid or missing input |
| 20.2 Speaker attribution | participants + transcript | speaker-aware transcript | participant contract available | attribution and review metadata preserved | attribution failure affecting primary evidence |
| 20.3 Question extraction | speaker-aware transcript | questions | speaker roles available | question IDs and source segments preserved | questions cannot be identified safely |
| 20.4 Response extraction | questions + transcript | responses | question IDs available | missing/unknown responses remain explicit | response structure is corrupt |
| 20.5 Reconstruction/normalization | responses + source transcript | reconstructed responses | response source preserved | original text remains available | reconstruction would require invented content |
| 20.6 Linking | questions + responses | links | both collections are available | uncertain links remain unknown/reviewable | central link cannot be established |
| 20.7 Validation | all Stage 20 artifacts | Structured Interview + validation | all prior outputs available | readiness and warnings are explicit | structural blocker or lost attribution |
| Human review | validation output | approved Structured Interview | review is explicitly completed | human decisions and exclusions are preserved | unresolved ambiguity or no approval |
| 21 Evidence Model | approved Structured Interview | Evidence Set | Stage 20 is `READY` or `READY_WITH_WARNINGS` | every evidence item has source traceability | upstream block or orphan source |
| 22 Rubric | Evidence Set + rubric contract | rubric-compatible evaluation input | Evidence Set available | dimensions and N/A rules remain canonical | incompatible schema |
| 23 Evaluation Engine | question/response + Evidence Set | individual evaluations | evidence is valid and attributable | score, rationale, confidence and IDs preserved | missing required evidence or invalid reference |
| 23.1 Semantic audit | consolidated evaluation + individual evaluations | audit decision | Stage 23 output available | findings, status and gate are explicit | material inconsistency |
| Report handoff | approved consolidation | report handoff | audit passed with or without warnings | report consumes existing evaluations | audit or report approval absent |

## Shared invariants

1. IDs are stable and are never invented by orchestration.
2. Warnings are metadata, not negative candidate evidence.
3. `missing`, `unknown` and `needs_review` retain their meaning.
4. Confidence fields remain semantically separate.
5. The report does not silently recalculate evaluation results.
6. A blocking upstream state prevents downstream artifacts from appearing complete.

## Repeatability

The same fixture content and versions produce the same artifact content hashes. Timestamps are operational metadata only. Input changes invalidate the dependent chain from Stage 20.1; previous snapshots remain available in `OrchestrationStore`.
