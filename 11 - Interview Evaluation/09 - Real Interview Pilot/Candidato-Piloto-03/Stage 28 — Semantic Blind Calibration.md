# Stage 28 — Semantic Blind Calibration

## Status

`COMPLETE`

## Gate

`SEMANTIC_BLIND_CALIBRATION_COMPLETE`

## Cases

- Total: 21 calibration cases.
- PASS: 21.
- WARNING: 0.
- FAIL: 0.
- The collection includes declaration versus demonstration, conceptual versus
  applied knowledge, shallow/deep answers, troubleshooting, factual errors,
  autocorrection, uncertainty, contradiction, off-topic evidence, N/A,
  verbosity, and metadata invariance cases.

## Semantic Alignment

All independent reference checks passed. The comparator evaluated score ranges,
required/forbidden evidence types, qualitative dimensions, and confidence
without passing reference data to the blind runner.

The result is reported as semantic alignment, not as an artificial accuracy
percentage.

## Dimension Alignment

The comparator tracked `correctness`, `completeness`, `depth`, `reasoning`,
`practical_application`, and `trade_offs` independently. No dimension
divergence was reported.

## Confidence Alignment

Confidence was evaluated separately from extraction, reconstruction, linking,
and evidence confidence. The uncertainty case retained medium evaluation
confidence rather than being converted into negative knowledge.

## Divergences

No unresolved divergences. The static references remain outside the execution
input and are compared only after the runtime returns.

## Blindness Validation

The blind runner removes oracle/reference fields, expected scores, expected
dimensions, evidence specifications, and evaluation specifications before
calling the runtime. The resulting engine output contains no expected
reference fields.

Mutating a reference changes comparator output only; it does not change the
runtime evaluation.

## Mutation Tests

- Expected score range mutation: comparator changed, engine output did not.
- Expected rationale/reference mutation: reference comparison is isolated from
  execution.
- Input evidence mutation: changing the raw answer changed downstream
  evidence and evaluation.
- Seniority, CV years, and job title mutations: evaluation remained
  equivalent.

## Invariance Tests

The same technical content was not rewarded for verbosity, seniority,
curriculum, or title metadata. Declaration-only experience remained distinct
from concrete demonstrated experience. N/A dimensions were not converted to
zero.

## Reproducibility

`PASS` - repeated execution produced equivalent evidence and evaluation
artifacts for all cases.

## Isolation

`PASS` - the suite uses the existing reference-runtime execution model and
does not modify canonical pilot artifacts.

## Protected Artifacts

`PASS` - the scoring rubric and existing evaluation artifacts were preserved.
No canonical semantic implementation was changed to force calibration results.

## Limitations

The calibration references are static semantic fixtures and bounded score
ranges, not a statistically representative human-annotated dataset. The
current comparator reports alignment against these controlled cases and does
not claim population-level accuracy.

## Conclusion

The blind calibration demonstrates semantic consistency across the required
controlled cases: the runtime derives evidence and evaluation from the input
content, while independent references remain outside the engine boundary.
