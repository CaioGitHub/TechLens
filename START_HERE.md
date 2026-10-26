# START HERE

## Para analisar uma entrevista recebida como prompt

Começar por `TRANSCRIPTION_AGENT_WORKFLOW.md`. O agente escolhido pelo usuário consulta este projeto como método e referência; o projeto não precisa chamar ou hospedar modelos. O agente deve fazer a maior parte da análise e devolver relatório e exceções justificadas. Para desenvolvimento do projeto, seguir também a continuidade abaixo.


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


## Proteção do importador histórico — 2026-10-25

Ver [[TRANSCRIPTION_IMPORT_GUARD]] e `TRANSCRIPTION_IMPORT_GUARD_RESULTS.json`. Importação, carregadores individuais e geração direta verificam incerteza declarada; coordenação bloqueia antes de consolidar ou gravar. Revisão auxiliar opcional vinculada por hashes, conflitos e metadados inválidos bloqueados, reutilização antiga revalidada. 22 novos testes; 80 direcionados, 590 globais e 15 do harness aprovados. Ausência de marcação não prova fidelidade; revisão externa deve ser fornecida explicitamente. Entrada genérica e UI de revisão seguem pendentes. Bloqueios semânticos históricos preservados; este adendo é o estado atual e sucede os limites do checkpoint anterior quanto ao importador.


## Entrada genérica e responsabilidade da IA — 2026-10-25

Ver [[TRANSCRIPTION_GENERIC_INPUT]], `TRANSCRIPTION_GENERIC_INPUT_RESULTS.json` e [[TRANSCRIPTION_AI_ANALYSIS_CONTRACT]]. Entrada por turnos e participantes configuráveis implementada, com preservação de texto/IDs/timestamps, distinção entre entrevistadores e ambiguidade explícita. Dez testes novos; 70 direcionados, 600 globais e 15 do harness aprovados. Diretriz: IA analisa a entrevista inteira e prepara propostas e exceções; humano revisa decisões que exigem comprovação de fonte, sem reanalisar todos os turnos. Integração com modelo, importadores de arquivos e UI ainda pendentes; próxima etapa é o adaptador de IA com validação de saída. Nenhuma promessa de percentual de automação ou homologação semântica. Gates históricos preservados.


## Validação diagnóstica do roteiro — 2026-10-25

Ver `11 - Interview Evaluation/09 - Synthetic Validation/Agent Workflow 2026-10-25/RESULTS.md`: três cenários fictícios analisados, entradas fixadas, revisão F01 registrada, 30 verificações estruturais e dois controles negativos. Autoavaliação não cega, sem comprovação independente de qualidade semântica. Runtime e gates históricos inalterados.


## Revisão controlada de fidelidade do relatório real — 2026-10-25

Ver `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-01/Agent Report Review 2026-10-25/REVIEW.md`. O usuário reconfirmou F01; quatro avaliações e justificativas permaneceram intactas, com notas 0/4/8/4 e média descritiva 4,0. O uso qualitativo de 07:22 como E07 foi retirado; Q9/R9 permanece adiada e o relatório/MOC identificam análise parcial. Fonte preservada e versão inicial arquivada. Regra do guia ampliada: fonte irrecuperável não sustenta conclusão favorável nem desfavorável, mesmo sem nota. Oito testes de política e doze verificações da revisão aprovados. Auditor de dependências explícitas, com classificação manual; não valida automaticamente toda a semântica da prosa nem a calibração das notas. Sem alteração do runtime, da rubrica ou dos gates históricos.


## Pacote de reteste controlado pronto — 2026-10-25

Ver `11 - Interview Evaluation/09 - Real Interview Pilot/Agent Retest 2026-10-25/README.md`. Foi preparado um snapshot executor sem relatórios anteriores, com 164 turnos, 25 fontes de método e condições de origem explicitamente fornecidas pelo usuário (F01, 03:49 e frase integral 07:22). Critérios de comparação ficam fora do ZIP executor. Integridade do arquivo, hashes, preservação da contagem e exclusão dos diretórios de relatórios foram conferidas. A origem Git está fixada em build_spec.json; resultado local em package_verification.json.

Estado: `PACKAGE_READY_AWAITING_USER_AGENT_EXECUTION`. Não foi executado outro agente, não há resultado do reteste nem validação independente a declarar. Usar conversa nova e pasta separada, guardando a entrega antes da comparação. O pacote separa entradas, mas não impõe restrição técnica de acesso ao histórico/arquivos externos. Testa aplicação do método com limitações conhecidas, não detecção cega de texto irrecuperável. Runtime e gates históricos inalterados.


## Reteste — entrega 001 recebida em 2026-10-25

Comparação em `11 - Interview Evaluation/09 - Real Interview Pilot/Agent Retest 2026-10-25/submissions/001/REVIEW.md`. Entrega original preservada. Proteção de 07:22 observada, com adiamento e ausência de conclusões pessoais a partir dessa fonte. Entradas do pacote íntegras; hash da transcrição, 24 referências explícitas, 14 citações e persistência da entrega conferidos. F-RETEST-001: nota 2 em pergunta fechada de inventário de observabilidade requer revisão do escopo solicitado versus demonstração prática, à luz da rubrica e taxonomia. Não foram alteradas notas ou rubrica. Não há comprovação de isolamento de contexto, cegamento ou calibração independente. Resultado: proteção observada, escopo de uma pontuação ainda pendente; não homologação geral.
