---
type: reference
status: unresolved
confidence: 100
created: 2026-09-21
updated: 2026-09-21
tags:
  - interview-evaluation
  - real-interview-pilot
  - human-review
  - decisions
---
# Human Review Decisions v4

## Review status

```yaml
reviewer: human_reviewer
review_timestamp: pending
source: Pilot Input - Source Transcript v3.md
structured_interview: Structured Interview - Controlled Correction v4.md
decision_status: APPLIED
approval_status: APPROVED_WITH_WARNINGS
review_timestamp: 2026-09-21T21:15:33-03:00
```

This file is the decision register for Stage 30.2. It intentionally does not infer human decisions from the transcript or from runtime classifications. `PENDING` entries must be resolved explicitly before an approved Structured Interview can be created.

## Controlled decision values

```text
APPROVE
REJECT
REASSIGN
SPLIT
MERGE
KEEP_UNKNOWN
RECONSTRUCT
KEEP_ORIGINAL
MARK_NON_EVALUABLE
MARK_EVALUABLE
PENDING
```

## Unknown and unlinked responses

All 24 items require individual review. The runtime state is preserved until a human decision is recorded.

| ID | Source segment | Original text (transcript) | Current link | Human decision | Reviewer note | Confidence |
|---|---|---|---|---|---|---|
| R2 | RAW-009 | Tudo bem. | unknown | PENDING |  |  |
| R24 | RAW-048 | Não, nenhum. | unknown | PENDING |  |  |
| R26 | RAW-052 | É na parte de ferramentas de observability, não, mas todo o sistema deles está no o pessoal aqui está no ezure, né? Então todos os repositórios, tudo é no ezure. | unknown | PENDING |  |  |
| R35 | RAW-075 | Tranquilo. | unknown | PENDING |  |  |
| R36 | RAW-077 | Tudo bem. | unknown | PENDING |  |  |
| R37 | RAW-079 | É depois de analisar o meu currículo e o meu perfil aqui na entrevista, tem alguma coisa que faltou na opinião de vocês para dar match na vaga? | unknown | PENDING |  |  |
| R38 | RAW-093 | Entendi. | unknown | PENDING |  |  |
| R39 | RAW-098 | Entendi bacana. | unknown | PENDING |  |  |
| R40 | RAW-100 | É. | unknown | PENDING |  |  |
| R41 | RAW-105 | É o dia a dia. | unknown | PENDING |  |  |
| R43 | RAW-119 | E assim, uma dúvida, porque eu já trabalhei em equipe de sustentação e acontecia muitas vezes de não ter acesso a logs, essas coisas, como que é nesse sentido. Para quem está nessa equipe, existe esses acessos? | unknown | PENDING |  |  |
| R44 | RAW-121 | Entendi, bacana. | unknown | PENDING |  |  |
| R45 | RAW-122 | Acho que era isso mesmo de dúvida que eu tinha. | unknown | PENDING |  |  |
| R46 | RAW-127 | Tudo bem. | unknown | PENDING |  |  |
| R47 | RAW-128 | Tudo bem? | unknown | PENDING |  |  |
| R48 | RAW-135 | Entendi. | unknown | PENDING |  |  |
| R49 | RAW-136 | Beleza. | unknown | PENDING |  |  |
| R50 | RAW-140 | Eu estou pensando aqui. | unknown | PENDING |  |  |
| R51 | RAW-146 | Entendi. | unknown | PENDING |  |  |
| R52 | RAW-149 | Tem. | unknown | PENDING |  |  |
| R53 | RAW-151 | Entendi. | unknown | PENDING |  |  |
| R54 | RAW-153 | Acho que eu não tenho mais dúvidas. | unknown | PENDING |  |  |
| R55 | RAW-155 | Eu perguntei bastante coisa, né? | unknown | PENDING |  |  |
| R56 | RAW-163 | Eu que agradeço a disponibilidade de vocês e a possibilidade de participar do processo aqui com vocês. | unknown | PENDING |  |  |

For each item, the reviewer must also inspect the immediately preceding and following transcript segments before choosing `REASSIGN`, `KEEP_UNKNOWN`, `MARK_NON_EVALUABLE`, `MERGE`, `SPLIT` or another controlled value.

## Evaluation-question review

| ID | Source segment(s) | Current interpretation | Human decision | Reviewer note | Confidence |
|---|---|---|---|---|---|
| Q1 | RAW-002 | Open Finance context plus question | PENDING |  |  |
| Q2 | RAW-011 | Professional experience and projects prompt | PENDING |  |  |
| Q3 | RAW-022 | Technologies used | PENDING |  |  |
| Q4 | RAW-029 | Java version | PENDING |  |  |
| Q5 | RAW-032 | Producer/consumer wording in REST API | PENDING |  |  |
| Q6 | RAW-035 | JDBC and its function | PENDING |  |  |
| Q7 | RAW-039 | Architecture used | PENDING |  |  |
| Q8 | RAW-041 | Hexagonal architecture follow-up | PENDING |  |  |
| Q9 | RAW-049 | Observability tool experience | PENDING |  |  |
| Q10 | RAW-055 | Incident-investigation scenario | PENDING |  |  |
| Q11 | RAW-066 | Agile context and AI usage | PENDING |  |  |
| Q12 | RAW-113 | Daily/team routine prompt | PENDING |  |  |

The reviewer must decide whether each unit remains evaluable, is non-evaluable, or requires `SPLIT`, `MERGE`, `RECONSTRUCT` or `KEEP_ORIGINAL`. No technical correctness or score is decided here.

## Candidate-question review

| ID | Source segment | Original text | Current decision | Human decision | Reviewer note |
|---|---|---|---|---|---|
| CQ1 | RAW-102 | Como que é que? | candidate_question; evaluation_eligible=false | PENDING |  |
| CQ2 | RAW-103 | Como que é a equipe de trabalho aí? Como que funciona? | candidate_question; evaluation_eligible=false | PENDING |  |
| CQ3 | RAW-131 | Quais as tecnologias que vocês usam assim no geral, é Spring e o que mais? | candidate_question; evaluation_eligible=false | PENDING |  |
| CQ4 | RAW-143 | Como que é a parte de documentação de API de vocês, vocês usam swagger, essas coisas? | candidate_question; evaluation_eligible=false | PENDING |  |
| CQ5 | RAW-147 | E como que chega a demanda para vocês? A descrição no card, no Jira, é. | candidate_question; evaluation_eligible=false | PENDING |  |

Candidate questions must remain separate from evaluation questions and candidate technical evidence.

## Response-count analysis: 44 to 47

```yaml
initial_v3_responses: 44
corrected_v4_responses: 47
human_decision: PENDING
proposed_review_categories:
  - better_segmentation
  - previous_grouping_error
  - intervention_separation
  - candidate_question_separation
  - multi_segment_split
  - parser_correction
  - possible_duplication
  - other
```

The three additional records cannot be approved solely from the count change. The reviewer must compare v3 and v4 source-segment coverage and explicitly classify each affected response record as legitimate separation or duplication.

## Reconstruction and ambiguous terms

No automatic human approval is recorded for any reconstruction.

| Original term | Current reconstruction | Human decision | Confidence | Reviewer note |
|---|---|---|---|---|
| Beijava | unchanged | PENDING |  |  |
| C Sharpe | unchanged | PENDING |  |  |
| Angula | unchanged | PENDING |  |  |
| produtos e consumes | unchanged | PENDING |  |  |
| dyna trace | unchanged | PENDING |  |  |
| ezure | unchanged | PENDING |  |  |
| Lego Analytics | unchanged | PENDING |  |  |
| ZepSight | unchanged | PENDING |  |  |
| Springwood | unchanged | PENDING |  |  |

Permitted decisions are `APPROVE_RECONSTRUCTION`, `KEEP_ORIGINAL`, `RECONSTRUCT_WITH_WARNING` and `KEEP_AMBIGUOUS`, subject to the source transcript only. These labels are recorded here as review options and are not decisions.

## Needs-review segments

The 13 runtime-flagged segments require explicit classification:

```yaml
status: PENDING
required_outcomes:
  - RESOLVED
  - KEEP_WARNING
  - KEEP_UNKNOWN
  - RECONSTRUCT
  - REJECT_RECONSTRUCTION
```

The segment-level decision must preserve original text and source traceability.

## Generic decision record

Use one record per decision:

```yaml
decision:
  id: HR-30.2-<sequential-id>
  reviewer: human_reviewer
  timestamp: <required>
  target_type: response|question|candidate_question|segment|term|speaker|count_analysis
  target_id: <required>
  original_state: <required>
  decision: <controlled value>
  corrected_state: <required>
  reason: <required>
  source_segments:
    - <segment id>
  confidence: <0-100>
```

## Gate

```yaml
STRUCTURED_INTERVIEW_HUMAN_REVIEW_COMPLETE: false
STRUCTURED_INTERVIEW_APPROVED: false
status: BLOCKED
pending_items: 24 unknown links + 12 evaluation questions + 5 candidate questions + 13 needs-review segments + reconstruction/count decisions
downstream_allowed: false
```


## Applied human decisions ? 2026-09-21

The original preparation tables above are preserved as historical input. The following decisions were explicitly supplied and applied to v5 by `human_reviewer`.

```yaml
reviewer_status: APPROVED_WITH_WARNINGS
status: COMPLETE
unknowns: 24 reviewed individually
unknowns_kept_unlinked: 4
non_evaluable_acknowledgements_and_closings: 18
candidate_questions_confirmed_or_added: 7
question_evaluation_eligible: [Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q9, Q10, Q11]
question_non_evaluable: [Q8, Q12]
q8_relation: follow_up_of_Q7
needs_review_segments_resolved: [NR01, NR02, NR03, NR04, NR05, NR06, NR07, NR08, NR09, NR10, NR11, NR12, NR13]
reconstructions_approved: [T01, T02, T03, T04, T05, T06, T07, T09]
reconstructions_kept_ambiguous: [T08]
response_count_mapping: PENDING
validation_status: READY_WITH_WARNINGS
downstream_evaluation_executed: false
```

### Decision ledger

| Decision | Affected IDs | Rationale | Source | Reviewer status |
|---|---|---|---|---|
| MARK_NON_EVALUABLE | R2, R35, R36, R38, R39, R40, R41, R44, R45, R46, R48, R49, R50, R51, R53, R54, R56 | acknowledgement, confirmation, deliberation or closing; no technical evidence | Human Review Matrix v4 + supplied Stage 30.2 decisions | APPLIED |
| KEEP_UNKNOWN | R24 | context does not support safe reassignment | supplied Stage 30.2 decisions | APPLIED |
| KEEP_UNKNOWN | R26, R52 | relation remains structurally uncertain; preserve review warning | supplied Stage 30.2 decisions | APPLIED |
| CONFIRM_CANDIDATE_QUESTION | CQ1, CQ2, CQ3, CQ4, CQ5, R37, R43 | candidate questions remain outside evaluation and evidence | supplied Stage 30.2 decisions | APPLIED |
| MARK_NON_EVALUABLE | R47, R55 | candidate conversational questions/closings do not become technical questions | supplied Stage 30.2 decisions | APPLIED |
| MARK_EVALUABLE | Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q9, Q10, Q11 | explicit evaluation units retained | supplied Stage 30.2 decisions | APPLIED |
| MERGE / FOLLOW_UP | Q8 ? Q7 | hexagonal prompt is clarification/continuation, not independent question | supplied Stage 30.2 decisions | APPLIED |
| MARK_NON_EVALUABLE | Q12 | Daily/team routine is contextual, not a technical evaluation unit | supplied Stage 30.2 decisions | APPLIED |
| CLASSIFY_NON_EVALUABLE | NR01?NR13 | interventions, explanations, clarifications and contextual prompt preserved without candidate evidence | supplied Stage 30.2 decisions | APPLIED |
| RECONSTRUCT | T01, T02, T03, T04, T05, T06, T07, T09 | form-only reconstruction supported by transcript context | supplied Stage 30.2 decisions | APPLIED |
| KEEP_AMBIGUOUS | T08 | no safe reconstruction for ZepSight without external information | supplied Stage 30.2 decisions | APPLIED |
| KEEP_PENDING | D01, D02, D03 | v3 aggregate does not permit deterministic historical correspondence | supplied Stage 30.2 decisions | APPLIED |
```
