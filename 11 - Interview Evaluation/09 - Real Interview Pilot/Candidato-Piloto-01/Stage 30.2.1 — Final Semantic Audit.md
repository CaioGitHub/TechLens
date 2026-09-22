---
type: reference
status: unresolved
confidence: 100
created: 2026-09-21
updated: 2026-09-21
tags:
  - interview-evaluation
  - real-interview-pilot
  - semantic-audit
  - human-review
---
# Stage 30.2.1 — Final Semantic Audit

## Audit metadata

```yaml
audit:
  status: BLOCKED_PENDING_STRUCTURAL_CORRECTION
  audited_artifact: Structured Interview - Controlled Correction v5.md
  source_of_truth: Pilot Input - Source Transcript v3.md
  unlinked_responses: [R24, R26, R41, R52]
  candidate_questions: 7
  evaluation_questions: 12
  reconstructions: 9
  response_count_discrepancy:
    v3: 44
    v5: 47
    explained: false
    warning: true
  evidence_boundary: WARNING
  confidence_separation: WARNING
  readiness: BLOCKED
  correction_required: true
  downstream_executed: false
```

This was a read-only audit. No v5, source transcript, v4 artifact, human-review matrix, rubric, Evidence Model, Evaluation Engine or report artifact was modified during the audit.

## 1. Audit scope and method

The audit compared the v5 structured records with the source transcript and the canonical 20.1–20.7 rules. It did not evaluate technical correctness, candidate quality, seniority or hiring suitability.

The audit used only:

```text
Pilot Input - Source Transcript v3.md
Structured Interview - Controlled Correction v4.md
Structured Interview - Controlled Correction v5.md
Human Review Decisions v4.md
Human Review Matrix v4.md
20.1–20.7 canonical processing documents
```

No external source was consulted.

## 2. Unlinked responses

| ID | Speaker | Original | Context | Current status | Recommended action | Confidence | Reason |
|---|---|---|---|---|---|---:|---|
| R24 | Ingrid Mazoni | `Não, nenhum.` | Follows the interviewer's communication-comfort prompt and precedes the observability question. | `unknown`, non-evaluable | `KEEP_UNKNOWN` | 0.98 | The response is structurally a contextual answer, but the exact prompt boundary is not represented as an evaluation question. Linking to Q8 or Q9 would be speculative. |
| R26 | Ingrid Mazoni | `É na parte de ferramentas de observability... tudo é no ezure.` | Follows the interviewer’s observability/Azure exposition and precedes `Mhm.`; no explicit candidate-directed question immediately precedes it. | `unknown`, `needs_review: true` | `KEEP_UNKNOWN` | 0.96 | Technical vocabulary does not establish the question-response link. The current safe boundary is preserved. |
| R41 | Ingrid Mazoni | `É o dia a dia.` | Follows the interviewer clarification `Você diz o dia a dia?` after CQ1/CQ2 and precedes an interviewer explanation. | `unknown`, non-evaluable | `MARK_NON_EVALUABLE` while retaining `question_id: unknown` | 0.99 | It is a contextual confirmation, not an independently evaluable technical response. No technical link should be created. |
| R52 | Ingrid Mazoni | `Tem.` | Follows the interviewer’s answer about API documentation and precedes `Entendi.`; the object of the confirmation is not independently represented. | `unknown`, `needs_review: true` | `KEEP_UNKNOWN` | 0.97 | The referent of `Tem.` cannot be reconstructed safely. Do not infer the question or object. |

### R24 context

```text
06:32 interviewer: pergunta sobre desconforto em chamar pessoas para conversar
06:43 candidate: "Não, nenhum."
06:46 interviewer: pergunta sobre ferramenta de observabilidade
```

### R26 context

```text
06:46 interviewer: pergunta sobre observabilidade
06:58 candidate: Dynatrace
07:08 interviewer: Azure, Azure Monitor, Log Analytics, ZepSight
07:22 candidate: fala sobre observability/Azure/repositórios
07:34 interviewer: "Mhm."
```

### R41 context

```text
13:35 candidate: "Como que é que?"
13:37 candidate: "Como que é a equipe de trabalho aí? Como que funciona?"
13:41 interviewer: "Você diz o dia a dia?"
13:43 candidate: "É o dia a dia."
13:44 interviewer: chama Caio para explicar
```

### R52 context

```text
17:50 candidate: pergunta sobre documentação de API/Swagger
18:24 candidate: pergunta sobre chegada das demandas
18:33 candidate: "Tem."
19:06 candidate: "Entendi."
```

## 3. Candidate questions

| ID | Original | Speaker | Question type | Evaluation eligible | Current decision | Recommended action | Confidence | Reason |
|---|---|---|---|---|---|---|---:|---|
| CQ1 | `Como que é que?` | Ingrid Mazoni | fragment | false | candidate question | `KEEP_ORIGINAL` plus `continuation_of: CQ2` | 0.99 | It is an audible candidate fragment immediately continued by CQ2; preserve it without treating it as an independent information request. |
| CQ2 | `Como que é a equipe de trabalho aí? Como que funciona?` | Ingrid Mazoni | complete candidate question | false | candidate question | `CONFIRM_CANDIDATE_QUESTION` | 0.99 | Explicitly asks about the team and work routine. |
| CQ3 | `Quais as tecnologias que vocês usam assim no geral, é Spring e o que mais?` | Ingrid Mazoni | complete candidate question | false | candidate question | `CONFIRM_CANDIDATE_QUESTION` | 0.99 | Explicit request for information about team technologies. |
| CQ4 | `Como que é a parte de documentação de API de vocês, vocês usam swagger, essas coisas?` | Ingrid Mazoni | complete candidate question | false | candidate question | `CONFIRM_CANDIDATE_QUESTION` | 0.99 | Explicit request for information about API documentation. |
| CQ5 | `E como que chega a demanda para vocês? A descrição no card, no Jira, é.` | Ingrid Mazoni | complete candidate question | false | candidate question | `CONFIRM_CANDIDATE_QUESTION` | 0.98 | Explicit request about demand intake and ticket tools. |
| CQ6 | `É depois de analisar o meu currículo e o meu perfil aqui na entrevista, tem alguma coisa que faltou na opinião de vocês para dar match na vaga?` | Ingrid Mazoni | complete candidate question | false | candidate question | `CONFIRM_CANDIDATE_QUESTION` | 0.99 | Explicit question about the interviewer's view of fit; not technical evidence. |
| CQ7 | `E assim, uma dúvida... para quem está nessa equipe, existe esses acessos?` | Ingrid Mazoni | complete candidate question | false | candidate question | `CONFIRM_CANDIDATE_QUESTION` | 0.99 | Explicit question about access to production logs. |

### Candidate-question finding

The seven candidate-question units are correctly excluded from evaluation. However, the v5 artifact does not explicitly encode the CQ1→CQ2 continuation relationship. This is a P1 structural correction, not a technical-evaluation decision.

`R37`/`CQ6` and `R43`/`CQ7` are supported by explicit question wording and context. They are not acknowledgements or candidate evidence.

`R55` (`Eu perguntei bastante coisa, né?`) is not one of the seven candidate-question units and should not carry `candidate_question: true`; it is a conversational closing question.

## 4. Evaluation questions

| ID | Expected structural state | Audit result |
|---|---|---|
| Q1 | evaluable | Consistent |
| Q2 | evaluable | Consistent |
| Q3 | evaluable | Consistent; interviewer-suggested technologies remain distinguishable from candidate speech |
| Q4 | evaluable | Consistent |
| Q5 | evaluable | Consistent; no completion of `Consumers.` |
| Q6 | evaluable | Consistent; incomplete JDBC response preserved |
| Q7 | evaluable | Consistent |
| Q8 | follow-up/continuation of Q7 | Relation intended, but explicit v5 relationship metadata should be corrected/verified |
| Q9 | evaluable | Consistent; R25 links to Q9 while R26 remains unknown |
| Q10 | evaluable | Consistent |
| Q11 | evaluable | Consistent as contextual/experiential prompt |
| Q12 | contextual/non-evaluable | Question classification is correct, but R42 remains `evaluation_eligible: true`, which is inconsistent |

## 5. Reconstruction audit

| ID | Original | Reconstruction | Confidence | Supported? | Needs review |
|---|---|---|---:|---|---|
| T01 | Beijava | Java | high | Yes, immediate technology-list context | No |
| T02 | C Sharpe | C# | high | Yes, immediate technology-list context | No |
| T03 | Angula | Angular | high | Yes, immediate technology-list context | No |
| T04 | produtos e consumes | producers e consumers | high | Yes, question wording only | No |
| T05 | dyna trace | Dynatrace | high | Yes, candidate names an observability tool | No |
| T06 | ezure | Azure | high | Yes, immediate Azure/repository context | No |
| T07 | Lego Analytics | Log Analytics | high | Yes as form-only reconstruction of interviewer speech | No |
| T08 | ZepSight | no reconstruction | low | No safe transcript-only reconstruction | Yes |
| T09 | Springwood | Spring Boot | high | Yes as form-only reconstruction of interviewer speech in Spring/Java context | No |

All audited transformations preserve `original_text`. They do not add technical explanation or turn interviewer content into candidate evidence. T08 correctly remains unreconstructed.

## 6. Response count discrepancy

```yaml
v3_responses: 44
v5_responses: 47
explained: false
warning: true
historical_reconciliation: not possible from preserved v3 aggregate
```

The 47 v5 responses have stable IDs and source segment references. No duplicate ID was detected in the v5 artifact. The three additional historical units cannot be attributed deterministically to a specific split, intervention, candidate question or parser correction because v3 preserves only the aggregate count. The discrepancy must remain a warning; no retroactive reconciliation is justified.

## 7. Evidence boundary

### Result: WARNING — correction required

The v5 artifact correctly excludes candidate questions and interviewer explanations from the main evaluation-question list. However, `R42` is linked to non-evaluable `Q12` while still carrying `evaluation_eligible: true`. This is a structural eligibility leak that must be corrected before Stage 21.

`R55` also carries `candidate_question: true` in its response record even though it is a conversational closing and is not represented as a candidate-question unit. This is a classification inconsistency that must be corrected.

No score, average, ranking, seniority, hiring decision or technical candidate verdict was found in the structured interview content.

## 8. Confidence separation

### Result: WARNING

The artifact separates `attribution_confidence`, `reconstruction_confidence` and the downstream evaluation boundary. T08 has independent low reconstruction confidence, and R26/R52 retain linking uncertainty through `question_id: unknown` and `needs_review`.

The v5 artifact does not expose a complete explicit `extraction_confidence` and `linking_confidence` field for every question/response record. This is a metadata completeness warning, not evidence contamination. It should be preserved or addressed in v6 without inventing confidence values.

## 9. Required structural corrections

No correction was applied during the read-only phase. The following corrections are justified by the source and the v5 inconsistency:

```yaml
corrections_required:
  - id: AUDIT-30.2.1-001
    target: R42
    action: MARK_NON_EVALUABLE
    reason: R42 belongs to contextual/non-evaluable Q12; it must not remain evaluation eligible.
  - id: AUDIT-30.2.1-002
    target: R55
    action: KEEP_ORIGINAL
    reason: conversational closing; remove candidate_question flag from the response record.
  - id: AUDIT-30.2.1-003
    target: CQ1
    action: KEEP_ORIGINAL
    reason: preserve fragment and add explicit continuation relationship to CQ2.
```

These corrections do not change the transcript, technical content, question set, score or evaluation rules. Because they affect evaluation eligibility and candidate-question structure, a v6 artifact is required before release.

## 10. Audit conclusion

```yaml
v5_semantic_fidelity: mostly_consistent
material_structural_issues: 2
non_material_warnings: 2
correction_required: true
v6_required: true
stage_21_release: blocked_pending_v6
```

The v5 representation is not released to Stage 21 yet. The remaining unknowns themselves are safe; the blocker is the inconsistent eligibility metadata identified above.


## 11. Post-audit correction and revalidation

The read-only findings were applied in a new artifact; v5 was not overwritten.

```yaml
correction_artifact: Structured Interview - Controlled Correction v6.md
decision_log: Human Review Decisions v5.md
corrections_applied: 3
R42_evaluation_eligible: false
R55_candidate_question_flag: false
CQ1_continuation_of: CQ2
semantic_audit_result: PASS_WITH_WARNINGS
validation_result: READY_WITH_WARNINGS
stage_21_release: allowed_with_warnings
evidence_model_executed: false
```

The remaining warnings do not create material candidate-evidence contamination: unknown responses remain excluded from evaluation, T08 remains ambiguous and unreconstructed, and the historical 44?47 mapping remains unresolved without retroactive invention.

## 12. Final audit gate

```text
STRUCTURED_INTERVIEW_SEMANTIC_AUDIT_COMPLETE
STRUCTURED_INTERVIEW_APPROVED_WITH_WARNINGS
STATUS: READY_WITH_WARNINGS
STRUCTURED_INTERVIEW_RELEASED_FOR_STAGE_21: true
STAGE_21_EXECUTED: false
```
