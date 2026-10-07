# Stage 30.1 — Pilot Failure Analysis

## 1. Objetivo

Reproduzir os achados do Stage 30, determinar sua causa real e aplicar somente correções gerais, mínimas e testáveis. O transcript bruto permaneceu a fonte de verdade.

## 2. Achados de entrada

- P0: 0.
- P1-01 / HR-001: prompt conversacional classificado como pergunta avaliável.
- P1-02 / HR-002: respostas contextuais permaneceram em `unknown/needs_review`.
- P2-01 / HR-003: normalização de ruído técnico deve permanecer conservadora.

## 3. P1-01 — Perguntas conversacionais

### Reprodução

O segmento `RP05-113`, `E tem uma Daily também, só nossa, né?`, terminava em uma tag question. O classificador reconhecia a interrogação final, mas não reconhecia que a fala era uma confirmação contextual sobre a rotina dos entrevistadores. Ela era emitida como `interviewer_question`, entrava como Q12 e gerava avaliação.

### Causa

Stage 20.3: `_question_kind()` tratava a forma interrogativa final como suficiente quando `_is_interviewer_comment()` não encontrava marcadores de comentário contextual.

### Impacto

Antes: 12 perguntas, 47 respostas, 23 evidências e 12 avaliações. Depois: 11 perguntas, 47 respostas, 22 evidências e 11 avaliações. A última avaliação, derivada exclusivamente da fala contextual, foi removida; as 11 avaliações restantes mantiveram os mesmos scores e a mesma origem.

### Correção

Foi ampliado o classificador geral de comentários para reconhecer confirmações contextuais com tag question quando há combinação de marcadores de rotina/coletividade, como `também`, `só nossa`, `a gente`, `nossa` ou `nosso`. Perguntas técnicas com tag question continuam avaliáveis, por exemplo `Você já usou Kafka, né?`.

### Testes

- Reprodução do prompt contextual do piloto.
- Prompt conversacional simples não extraído.
- Pergunta técnica com tag question preservada.
- Idempotência e rastreabilidade do piloto.

## 4. P1-02 — Respostas contextuais

### Reprodução

Foram examinadas todas as respostas com `question_id: unknown`. `R26` é uma continuação contextual após explicação dos entrevistadores sobre Azure; `R43` é uma pergunta do candidato sobre acesso a logs. Nenhuma das duas responde a uma pergunta técnica avaliável identificável.

### Causa

Stage 20.6 opera conservadoramente: sem pergunta anterior válida e sem evidência conversacional suficiente, mantém `unknown/needs_review`. O comportamento não é causado por perda de uma resposta técnica vinculável.

### Impacto

`R26` e `R43` não geram evidência nem avaliação. Não houve evidência órfã, conteúdo técnico inventado ou alteração de score. Vinculá-las por proximidade criaria relações sem suporte.

### Correção

Nenhuma correção de linking foi aplicada. O comportamento foi classificado como `EXPECTED_BEHAVIOR`, com limitação aceita e revisão explícita.

### Testes

- Resposta imediata, resposta separada por intervenção, resposta contextual e pergunta do candidato.
- Verificação de que `unknown` permanece quando não há evidência suficiente.
- Verificação de que `R26` e `R43` não entram no Evidence Model.

## 5. P2

### Reprodução

O Stage 30 não demonstrou uma reconstrução incorreta específica. A revisão mostrou apenas que ruído técnico e termos ambíguos devem ser preservados ou normalizados com evidência local.

### Causa

Stage 20.5 possui limitação de normalização conservadora; não foi reproduzido um bug determinístico.

### Impacto

Nenhum impacto mensurável em evidências, avaliações ou rastreabilidade.

### Decisão

`LIMITATION_ACCEPTED`. Nenhuma alteração foi aplicada ao Stage 20.5.

## 6. Alterações realizadas

- Atualizado somente `reference_runtime/runtime.py`, no classificador de comentários do Stage 20.3.
- Adicionados testes em `tests/test_stage_30_1_pilot_failure_analysis.py` e ampliados os testes do Stage 30.1.
- Nenhum artefato canônico, transcript original ou contrato de avaliação foi alterado.

## 7. Comparação Before/After

| Métrica | Antes | Depois | Impacto |
|---|---:|---:|---|
| Participantes | 4 | 4 | — |
| Perguntas | 12 | 11 | Q12 contextual removida |
| Respostas | 47 | 47 | — |
| Evidências | 23 | 22 | evidência derivada de Q12 removida |
| Avaliações | 12 | 11 | avaliação de Q12 removida |
| Média | 6,85 | 6,93 | efeito mecânico da remoção; não foi objetivo de otimização |
| Mediana | 7,05 | 7,05 | — |
| P1 | 2 | 1 | P1-01 corrigido; P1-02 classificado |
| P0 | 0 | 0 | — |

As 11 avaliações preservadas mantiveram seus scores e suas referências. A mudança de média é consequência da remoção da avaliação indevida, não critério de sucesso.

## 8. Human Review

A revisão confirmou a natureza contextual de `RP05-113` e verificou `R26`/`R43` contra os segmentos adjacentes. Não houve segundo avaliador humano independente.

## 9. Traceability

As evidências preservadas continuam rastreáveis por:

`evaluation -> evidence -> response -> question -> source.segment_ids`

Não foram adicionados segmentos, respostas, perguntas ou relações que não existam no transcript.

## 10. Regression

Foram executados os testes específicos do Stage 30.1, o Stage 30, a regressão completa, o Reference Harness, os Stages 27–29 e `git diff --check`. O resultado esperado é zero regressões.

## 11. Limitations

- O linking permanece conservador para respostas contextuais e perguntas do candidato.
- A normalização de ruído técnico continua limitada à evidência local.
- A revisão independente por segundo humano não está disponível.
- Os contratos de materialização raw e Markdown continuam distintos na fronteira final.

## 12. Conclusão

O P1-01 era uma falha real e generalizável do Stage 20.3, corrigida sem descartar perguntas técnicas válidas. O P1-02 e o P2 não demonstraram falha corrigível: permaneceram como comportamento esperado/limitação aceita, sem forçar vínculos ou reconstruções.

## 13. Gate

`PILOT_FAILURE_ANALYSIS_COMPLETE_WITH_WARNINGS`
