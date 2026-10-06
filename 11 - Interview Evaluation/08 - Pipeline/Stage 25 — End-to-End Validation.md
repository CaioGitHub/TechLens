# Stage 25 — End-to-End Validation

## Objetivo

Validar a integração ponta a ponta entre Transcription Processing, Validation, Evidence Model, Individual Evaluation, Evaluation Engine, Global Semantic Audit e Materialization, consumindo o orchestrator do Stage 24.

Esta etapa valida interfaces e invariantes. Não cria rubrica, scoring, taxonomia ou regras semânticas novas.

## Escopo

O fluxo validado foi:

```text
20.7 → 21 → 22 → 23 → 23.1 → 23.2
```

Foram usados:

* o piloto `Candidato-Piloto-01` para a regressão canônica;
* fixtures controlados existentes para respostas ausentes, links desconhecidos, `needs_review`, warnings, autocorreção, hipótese, declaração de experiência, contradição e erro crítico;
* `run_interview_pipeline()` como único sistema sob teste;
* caminho de materialização temporário para preservar os artefatos canônicos.

## Pipeline validado

```text
Entrevista
  ↓
20.7 — Validation
  ↓
21 — Evidence Set
  ↓
22 — Individual Evaluations
  ↓
23 — Evaluation Result
  ↓
23.1 — Global Evaluation Audit
  ↓
23.2 — Interview Evaluation v2
```

O Stage 25 não recalcula scores, médias, evidências, auditoria ou o relatório v2.

## Ambiente

* Windows
* Python `py -3`
* Runtime determinístico baseado somente na biblioteca padrão
* Entrada canônica: `Individual Evaluations v2.md` e `Evidence Set v1.md`
* Saída de materialização do teste: arquivo temporário

## Casos executados

| ID | Caso | Resultado |
|---|---|---|
| E2E-01 | Happy Path | PASS |
| E2E-02 | Integridade do resultado e baseline do piloto | PASS |
| E2E-03 | Traceability completa | PASS |
| E2E-04 | Question sem Response | PASS |
| E2E-05 | Response sem Question | PASS |
| E2E-06 | `needs_review` | PASS |
| E2E-07 | Propagação de warnings | PASS |
| E2E-08 | Propagação de BLOCKED | PASS |
| E2E-09 | Gate de materialização | PASS |
| E2E-10 | Independência de v1 | PASS |
| E2E-11 | Isolamento de Job Context | PASS |
| E2E-12 | Isolamento de senioridade | PASS |
| E2E-13 | Isolamento de hiring | PASS |
| E2E-14 | Invariância a alterações superficiais | PASS |
| E2E-15 | Resposta hipotética | PASS |
| E2E-16 | Declaração de experiência | PASS |
| E2E-17 | Autocorreção | PASS |
| E2E-18 | Contradição | PASS |
| E2E-19 | Erro crítico | PASS |
| E2E-20 | Evidência excluída | PASS |
| E2E-21 | Idempotência | PASS |
| E2E-22 | Artefato stale | PASS |
| E2E-23 | Falha parcial | PASS |
| E2E-24 | Reprocessamento | PASS |
| E2E-25 | Regressão completa do piloto e preservação | PASS |

Resultado da suíte Stage 25: **26/26 PASS**.

## Invariantes

| ID | Invariante | Resultado |
|---|---|---|
| I1 | Nenhum downstream executa após BLOCKED | PASS |
| I2 | Warnings são preservados | PASS |
| I3 | IDs permanecem rastreáveis | PASS |
| I4 | Evidências excluídas não retornam como avaliações | PASS |
| I5 | v1 não é fonte operacional | PASS |
| I6 | Job Context não interfere | PASS |
| I7 | Senioridade não é inferida | PASS |
| I8 | Hiring decision não é produzida | PASS |
| I9 | Evaluation Engine permanece responsável pelo scoring | PASS |
| I10 | Materialization permanece responsável pela v2 | PASS |
| I11 | Pipeline é idempotente | PASS |
| I12 | Artefatos stale não são usados silenciosamente | PASS |
| I13 | Falha parcial preserva resultados anteriores | PASS |
| I14 | Reprocessamento é seguro | PASS |
| I15 | Confidence permanece separada por camada | PASS |
| I16 | Resposta ausente não vira “não sabe” | PASS |
| I17 | Não avaliado não vira fraco | PASS |
| I18 | Declaração de experiência não vira experiência demonstrada | PASS |
| I19 | Complexidade não vira senioridade | PASS |
| I20 | Resultado é proporcional às evidências disponíveis | PASS |

## Regression Baseline

| Validação | Resultado |
|---|---|
| Stage 25 | 26/26 PASS |
| Suíte completa | 362/362 PASS |
| Reference Harness | 8/8 suites, `PASS_WITH_WARNINGS` |
| Reference Runtime | 362 testes, PASS |
| Synthetic | 81 PASS, 1 `PASS_WITH_WARNING`, 0 FAIL |
| Semantic Calibration | 20/20 casos lógicos PASS, 0 FAIL |
| Adversarial | 29 PASS, 4 `PASS_WITH_WARNING`, 1 BLOCKED esperado, 0 FAIL |
| Stage 30.1 | 6/6 PASS |

Os harnesses posteriores foram executados somente como regressão dos componentes existentes; nenhuma etapa posterior foi implementada ou incorporada ao pipeline Stage 25.

## Warnings

O status final é `PASS_WITH_WARNINGS` devido a warnings legítimos já produzidos pelos componentes anteriores, incluindo o estado `READY_WITH_WARNINGS` de validação/transcrição, limitações de cobertura do piloto e ausência de avaliação de complexidade avançada. Esses warnings foram preservados sem bloquear a materialização permitida.

## Falhas

Nenhuma falha de integração foi identificada na suíte Stage 25 ou na suíte completa.

## Limitações

* O caminho canônico representa 20.7, 21 e 22 como dependências/artefatos consumidos pelo orchestrator; não foi criado um novo processador NLP de produção nesta etapa.
* Os cenários de borda são fixtures controlados do Runtime existente, não uma validação de prontidão produtiva.
* A validação não avalia senioridade, decisão de contratação ou readiness de produção.

## Conclusão

O fluxo integrado executa corretamente sobre o piloto, preserva os valores de regressão, mantém traceability entre as entidades, propaga warnings e bloqueios, respeita os gates de auditoria/materialização, detecta artefatos stale, permite reprocessamento seguro e preserva os artefatos protegidos.

## Gate

```text
END_TO_END_VALIDATION_COMPLETE_WITH_WARNINGS
```

