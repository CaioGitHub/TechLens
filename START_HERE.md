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


## Recuperação da regressão da base de transcrição — 2026-10-23

Ver [[TRANSCRIPTION_BASELINE_CORRECTIONS]]. Dois defeitos de evidência corrigidos, quatro testes novos e dois testes de snapshots históricos reescritos com autorização explícita para invariantes comportamentais. Regressão completa: 530/530 aprovados; harness 15/15. Estado limitado: `TRANSCRIPTION_BASELINE_REGRESSION_RECOVERED`. A baseline inicial de cinco falhas permanece preservada. Não houve aprovação semântica independente nem revogação dos bloqueios históricos. Próximo passo: plano incremental de transcrição sobre o fluxo de texto existente.


## Núcleo de correção fiel da transcrição — 2026-10-23

Ver [[TRANSCRIPTION_CORRECTION_FIDELITY]] e [[TRANSCRIPTION_IMPLEMENTATION_PLAN]]. Propostas e original separados; aprovação explícita ligada à fonte, rejeição e aplicação revisada integradas à reconstrução 20.5 antes da avaliação. 549 testes globais e 15 do harness aprovados. Estado limitado: `FAITHFUL_TRANSCRIPT_REVIEW_CORE_IMPLEMENTED_AND_REGRESSION_VERIFIED`. Não é corretor semântico geral nem validação humana independente; os bloqueios históricos permanecem.


## Piloto de referência real — 2026-10-23

Ver [[TRANSCRIPTION_REFERENCE_SET_PLAN]] e `TRANSCRIPTION_REFERENCE_SET_MANIFEST.json`: oito trechos localizados, três arquivos de uma entrevista, duas versões de conteúdo, zero referências humanas validadas. Critérios de aceite e procedimento incremental registrados. Revisão fundamentada desta entrevista pendente; outra entrevista distinta necessária para ampliar generalização. Runtime e gates históricos inalterados.


## Incerteza de transcrição — checkpoint de implementação

Ver [[TRANSCRIPTION_UNCERTAINTY]] e `TRANSCRIPTION_UNCERTAINTY_RESULTS.json`. Marcações ligadas à fonte propagadas até evidências, relatório e quatro exportações. Perguntas afetadas adiadas sem nota; texto original preservado; coordenação impede avanço como avaliação integral. 14 novos testes; 37 direcionados, 567 globais e 15 do harness aprovados. Na entrevista real, as duas perguntas afetadas ficam adiadas. Limite: nova entrada do runtime, sem proteção retroativa do importador de arquivos históricos. UI e generalização com outra entrevista continuam pendentes; bloqueios semânticos históricos preservados.


## Incerteza de transcrição — checkpoint de implementação

Ver [[TRANSCRIPTION_UNCERTAINTY]] e `TRANSCRIPTION_UNCERTAINTY_RESULTS.json`. Marcações ligadas à fonte propagadas até evidências, relatório e quatro exportações. Perguntas afetadas adiadas sem nota; texto original preservado; coordenação impede avanço como avaliação integral. 15 novos testes; 38 direcionados, 568 globais e 15 do harness aprovados. Na entrevista real, uma pergunta identificada e uma resposta sem vínculo confiável ficam adiadas, sem contaminar outras respostas com marcador `unknown`. Limite: nova entrada do runtime, sem proteção retroativa do importador de arquivos históricos. UI e generalização com outra entrevista continuam pendentes; bloqueios semânticos históricos preservados.
