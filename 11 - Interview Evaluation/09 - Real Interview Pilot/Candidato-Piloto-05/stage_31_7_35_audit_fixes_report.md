# Stage 31.7.35 — Correções dos achados de auditoria

Data: 2026-10-23.

## Mudanças verificadas

- Perguntas com solicitações explícitas repetidas são decompostas por todas as fronteiras reconhecidas, preservando ordem e identificadores. Coordenações internas entre entidades não são divididas automaticamente.
- Trechos conversacionais são isolados a partir do texto original, sem consumir proposições anteriores nem usar índices calculados sobre texto normalizado.
- Uma complementação não retrata automaticamente a proposição anterior. A retratação automática exige reversão explícita de polaridade da mesma afirmação. Casos mais amplos permanecem fora desta correção.
- AST idêntica fora de SemanticQuestionProfiler e DiscoursePropositionEngine; classificador existente não foi editado.

## Validação

- 13 novos testes específicos + 17 testes da fundação: 30/30 aprovados.
- Regressão: 1.097 testes, 1.096 aprovados, um ignorado, nenhuma falha ou erro (37,160 s).
- Reference Harness isolado: 15/15 aprovados, nenhuma falha ou erro (45,396 s).
- Python fornecido pelo ambiente; testes com opção -B, sem gerar bytecode.
- Snapshot de entrada novo: `reference_runtime/runtime.py.audit_20261023_pre_fix`.
- Diff: `stage_31_7_35_audit_fixes_runtime.diff`.
- Resultados: `stage_31_7_35_audit_fixes_results.json`.

## Gate e limitações

`AUDIT_FIXES_VERIFIED_INC1_FULL_ACCEPTANCE_PENDING`

Estas correções resolvem as três reproduções auditadas, mas não homologam todo o INC-1. Ainda é necessária uma matriz de cobertura integral dos contratos previstos e análise dos limites de segmentação, escopos e intenção. Retratações na mesma frase e contradições mais amplas não são resolvidas por esta alteração. A proveniência histórica dos snapshots continua não comprovada. Não restaurar arquivos com base apenas em seus nomes. Não houve nova validação semântica independente.

Relatórios históricos foram preservados. A etapa de continuidade continua sendo 31.7.35.
