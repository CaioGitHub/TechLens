---
type: reference
status: understood
confidence: 100
created: 2026-10-05
updated: 2026-10-05
tags:
  - interview-evaluation
  - pipeline
  - orchestration
  - reference-runtime
---

# Reference Interview Evaluation Pipeline Runtime

## Objetivo

`reference_runtime/interview_pipeline.py` é a fronteira executável da Etapa 24. Ele coordena os componentes existentes sem duplicar a semântica de transcrição, evidência, pontuação, auditoria ou materialização.

O runtime suporta:

```text
20.7 → 21 → 22 → 23 → 23.1 → 23.2
```

Para o piloto canônico, os artefatos já produzidos pelos estágios 20.x, 21 e 22 são consumidos como dependências documentais protegidas. O Runtime executa novamente o Evaluation Engine, a auditoria independente e a materialização v2.

## Entradas

O modo canônico recebe `PilotPaths` com:

- `Individual Evaluations v2.md`;
- `Evidence Set v1.md`;
- destino de `Interview Evaluation v2.md`;
- referências opcionais ao Structured Interview v6 e ao relatório Stage 23.1.

Também aceita um fixture estruturado para regressão do pipeline 20.x–23 existente. Não implementa processamento linguístico novo para transcript bruto.

## Gates e estados

Os estados operacionais são `RUNNING`, `READY`, `READY_WITH_WARNINGS`, `BLOCKED` e `FAILED`. Eles descrevem processamento do pipeline, não qualidade do candidato, senioridade ou decisão de contratação.

Um bloqueio em 20.7, 21, 23 ou 23.1 interrompe os estágios dependentes. Warnings são acumulados e propagados até o resultado final. O gate aprovado da auditoria é:

```text
GLOBAL_EVALUATION_AUDIT_COMPLETE
GLOBAL_EVALUATION_AUDIT_COMPLETE_WITH_WARNINGS
```

## Responsabilidades

O orquestrador:

- preserva a ordem e as dependências;
- encaminha artefatos existentes;
- executa `run_evaluation_engine`, `audit_global_output` e `materialize_interview_evaluation_v2`;
- preserva IDs, warnings, erros, `needs_review` e confidence por camada;
- impede materialização quando a auditoria falha;
- detecta versões downstream stale;
- permite reuso determinístico de um resultado anterior.

Ele não recalcula scores individuais, não cria evidências, não interpreta respostas, não usa `Interview Evaluation v1.md`, não recebe Job Context, não produz senioridade e não toma decisões de contratação.

## Saída

O resultado contém:

```text
pipeline
stages
artifacts
warnings
errors
confidence
traceability
readiness
```

A rastreabilidade preserva question IDs, response IDs, evidence IDs e evaluation IDs. No piloto atual, são preservadas 10 perguntas, 28 evidências e 10 avaliações.

## Idempotência e reprocessamento

Execuções com o mesmo `run_id` e resultado anterior reutilizam o resultado sem alterar sua semântica. `semantic_projection()` remove apenas identidade operacional para comparações.

`detect_stale_artifacts()` compara versões upstream/downstream e bloqueia o pipeline quando um artefato downstream foi produzido a partir de uma versão diferente.

Falhas parciais preservam os artefatos já produzidos no resultado e não fabricam artefatos posteriores.

## Limitações

- O modo canônico não recria os estágios 20.x, 21 ou 22; consome seus artefatos oficiais.
- A implementação não é um processador de linguagem natural.
- O runtime não altera artefatos canônicos protegidos.
- A materialização é responsabilidade do componente Stage 23.2 reutilizado pelo orquestrador.

## Testes

`tests/test_stage_24_pipeline_orchestration.py` verifica happy path, bloqueios, warnings, separação de confidence, `needs_review`, rastreabilidade, idempotência, stale artifacts, falha parcial, reprocessamento, independência do v1, ausência de Job Context/senioridade/hiring e não duplicação de scoring/evidências.

## Gate

```text
READY_WITH_WARNINGS
```

O piloto permanece com warnings legítimos de cobertura limitada e ausência de avaliação avançada.
