# Stage 27 - Synthetic Interview Full Run

## Status

`COMPLETE_WITH_WARNINGS`

## Gate

`SYNTHETIC_INTERVIEW_FULL_RUN_COMPLETE_WITH_WARNINGS`

The raw-first execution completed without a blocked gate and preserved the
controlled ambiguity in the source transcript.

## Raw Transcript

- Source: `tests/synthetic_interview.py::synthetic_interview_fixture`, copied into the Stage 27 fixture as `raw_transcript`.
- Segments: 28.
- Participants: 3.
- Roles: candidate, interviewer, observer.
- The fixture does not provide a structured transcript, expected evidence set,
  or expected evaluations as runtime input.
- The original raw segments are preserved in the runtime output.

## 20.1-20.7 Transcription Processing

- 20.1 identified all three participants and the candidate.
- 20.2 attributed known speakers and preserved `RAW-26` as unknown/low
  confidence with `needs_review`.
- 20.3 extracted technical questions, follow-up/reformulation, candidate
  question, and conversational comments.
- 20.4 extracted 13 response records, including a multi-segment response,
  interruption handling, and two missing responses.
- 20.5 preserved original text and reconstructed the supported `Spring Boto`
  to `Spring Boot` normalization. Autocorrection and uncertainty remained in
  the original response text.
- 20.6 created links without forcing the ambiguous speaker into a response.
- 20.7 returned `READY_WITH_WARNINGS`.

Warnings:

- ambiguous speaker: `RAW-26`;
- speaker attribution requires review;
- candidate questions are preserved outside evaluation questions.

## 21 Evidence Model

The blind evidence derivation consumed the processed responses rather than an
expected evidence fixture. It produced 17 evidence records with source segment
IDs, including conceptual, reasoning, technical error, self-correction,
experience declaration, demonstrated experience, hypothesis, uncertainty,
practical, and trade-off evidence where supported.

The declaration `Já trabalhei bastante com Application Insights` remained an
`experience_declaration`. The concrete production/configuration/query/result
response produced `demonstrated_experience`.

## 22 Rubric

The runtime evaluation stage applied the existing bounded scoring contract.
No job context, seniority, CV, or hiring decision was supplied to the fixture
or used in the assertions.

## 23 Evaluation Engine

Ten evaluations were produced from the derived evidence set. Scores remained
within the 0-10 contract, confidence remained separate from score, and every
evaluation referenced evidence with source segment IDs.

## 23.1 Global Semantic Audit

The Stage 24 boundary exposed the Stage 23.1 gate as
`READY_WITH_WARNINGS` for the raw synthetic execution. The audit input was
derived from the runtime output and remained independent of the historical
`Interview Evaluation v1.md`.

## 23.2 Materialization

The Stage 24 boundary exposed the Stage 23.2 gate as
`READY_WITH_WARNINGS`. The materialized runtime report matched the evaluations
and traceability produced by the raw execution; no v1 report was copied.

The current synthetic runtime uses its structured artifact/report adapter for
these final boundary stages. The canonical Markdown pilot materializer remains
the implementation used for the controlled pilot path; this limitation is
documented rather than hidden.

## Traceability

The tested chain was:

`evaluation_id -> evidence_id -> response_id -> question_id -> source.segment_ids`

No evaluated evidence was orphaned, and missing responses were not converted
to evidence or zero scores.

## Mutation Tests

- Historical v1: changing a temporary historical report did not change the raw
  result; canonical files were preserved.
- Transcript source: changing a raw response changed reconstructed output and
  downstream evidence.
- Expected fixture: changing only the oracle did not change execution.
- Speaker: changing an explicit speaker changed the derived participant
  attribution.
- Response: changing technical response content changed its downstream
  evidence.

## Idempotency

`PASS` - repeated runs produced equivalent participants, questions, responses,
reconstructions, links, evidence, evaluations, report, and warnings.

## Isolation and Canonical Artifacts

`PASS` - tests execute from copied/in-memory fixture data and verify that the
canonical v1, v2, evidence, individual evaluation, and controlled structured
interview artifacts remain unchanged.

## Validation

- Stage 27 tests: 32/32 PASS.
- Runtime readiness: `READY_WITH_WARNINGS`.
- No `BLOCKED` result.
- No Stage 28 or later implementation was executed.

## Limitations

The raw synthetic runtime and the canonical Markdown pilot runtime currently
have different input contracts for the final audit/materialization components.
Stage 27 verifies the raw runtime boundary and its derived report adapter, and
records that contract difference explicitly. A future convergence step can
replace the adapter with a shared artifact contract without changing the raw
transcription invariants demonstrated here.
