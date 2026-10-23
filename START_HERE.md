# START HERE

Este projeto possui histórico e metodologia já estabelecidos.

## Antes de fazer qualquer alteração

Leia obrigatoriamente:

1. `AGENTS.md`
2. `SECOND_BRAIN.md`
3. `GEMINI_GUARDRAILS.md`
4. `GEMINI_HANDOFF.md`

Depois identifique:

```text
Qual é o stage atual?
Qual foi o último gate?
Existe algum BLOCKED?
Quais warnings estão abertos?
Quais artefatos são históricos?
Quais testes devem continuar passando?
```

## Estado atual

O projeto está na sequência:

```text
Stage 31
    ↓
HUMAN_VS_SYSTEM_BLOCKED

Stage 31.1
    ↓
ROOT CAUSE IDENTIFIED

Stage 31.2
    ↓
CONTROLLED CORRECTION COMPLETE_WITH_WARNINGS

Stage 31.3
    ↓
POST_CORRECTION_BLIND_VALIDATION_BLOCKED

Stage 31.4
    ↓
CURRENT STAGE
```

O Stage 31.4 trata:

```text
Semantic Relevance
+
Representation Invariance
```

Não avançar para Production Readiness enquanto o problema atual não estiver validado.

## Regra fundamental

Não modificar o projeto apenas para fazer testes passarem.

Não criar regras específicas para casos individuais.

Não apagar histórico.

Não utilizar avaliação humana como alvo de score.

Não pular stages.

Não interpretar `BLOCKED` como aprovação.

## Princípio

> Não estamos construindo um sistema que parece inteligente. Estamos construindo um sistema cuja avaliação pode ser investigada, reproduzida, contestada e corrigida.


## Marco de retomada da transcrição — 2026-10-23

Branch `codex/transcription-baseline`, criada a partir de `transcriptionProcessingModel` no commit `06e506e`. Ver [[TRANSCRIPTION_BASELINE]]. A medição nesta origem executou 526 testes: 521 aprovados, cinco falhas, zero erros. Estado limitado: `TRANSCRIPTION_BASELINE_RECORDED_WITH_KNOWN_FAILURES`; não é homologação semântica. Os bloqueios históricos permanecem. A frente recente foi preservada na branch `codex/inc1-contract-coverage`, com checkpoint pendente `8c0280c`. Não transportar automaticamente para esta origem os achados de versões posteriores.
