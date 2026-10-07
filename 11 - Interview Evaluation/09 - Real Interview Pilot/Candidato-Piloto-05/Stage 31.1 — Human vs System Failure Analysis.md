# Stage 31.1 — Human vs System Failure Analysis

## Objective

Investigar as divergências materiais do Stage 31 sem alterar o Evaluation Engine, Evidence Model, Rubric, Question Taxonomy, scores ou avaliações congeladas. O bloqueio histórico `HUMAN_VS_SYSTEM_BLOCKED` permanece preservado.

## Stage 31 Input

Foram usados:

- `Transcript Original.md` como fonte primária;
- `Stage 31 — Human Evaluation Independent.md`;
- `Stage 31 — Human vs System Comparison.md`;
- artefatos pós-correção de estrutura, evidência, avaliações e global;
- `Stage 30.2.1 — Final Semantic Audit.md`;
- Rubric, Evidence Model, Evaluation Framework e runtime de referência.

Não foram usados CV, senioridade, contexto da vaga ou histórico como evidência.

## Methodology

Cada divergência foi reconstruída pela cadeia:

`Transcript → Question → Response → Linking → Reconstruction → Evidence → Qualification → Dimensions → Score`

As causas foram classificadas somente com a taxonomia controlada da etapa. A análise distingue problema de extração/qualificação, problema de dimensão/score e divergência técnica válida. Nenhuma correção foi implementada.

## Divergence Matrix

| Questão | Divergência | Causa | Impacto | Correção necessária |
|---|---|---|---|---|
| FRA-001 / Q1 | Humano 4.0 vs sistema 6.0; resposta é declaração limitada | `SYSTEM_EVIDENCE_OVERINTERPRETATION` + `SYSTEM_DIMENSION_INTERPRETATION_ERROR` | HIGH | Sim; escopos 21/23 |
| FRA-002 / Q3 | Humano 4.0 vs sistema 6.0; resposta fragmentada sobre Java/backend | `SYSTEM_EVIDENCE_OVERINTERPRETATION` + `SYSTEM_SCORE_CALIBRATION_ERROR` | MEDIUM | Sim; escopos 21/23 |
| FRA-003 / Q5 | Humano 2.0 vs sistema 7.05; pergunta REST, resposta Kafka/Rabbit | `SYSTEM_EVIDENCE_OVERINTERPRETATION` + `SYSTEM_DIMENSION_INTERPRETATION_ERROR` | CRITICAL | Sim; escopos 21/23 |
| FRA-004 / Q6 | Humano 5.0 vs sistema 7.05; resposta parcial sobre JDBC | `SYSTEM_EVIDENCE_OVERINTERPRETATION` + `SYSTEM_SCORE_CALIBRATION_ERROR` | HIGH | Sim; escopos 21/23 |
| FRA-005 / Q9 | Humano 4.0 vs sistema 7.05; declaração de ferramenta sem demonstração | `SYSTEM_EVIDENCE_OVERINTERPRETATION` | HIGH | Sim; escopos 21/23 |
| FRA-006 / Q11 | Humano 4.0 vs sistema 7.65; declaração de uso de Copilot | `SYSTEM_EVIDENCE_OVERINTERPRETATION` + `SYSTEM_DIMENSION_INTERPRETATION_ERROR` | HIGH | Sim; escopos 21/23 |

## Q1

### Question

`RP05-002`: `você já ouviu falar um pouquinho do projeto open finance?`

### Response and reconstruction

`RP05-003`: `É muito pouco, bem por cima.` A reconstrução preserva o texto.

### Human versus system

- Humano: evidência insuficiente de conhecimento técnico; score `4.0`.
- Sistema: evidência `conceptual`, `positive`, `moderate`; `correctness: Strong (9)`, `completeness: Partial (6)`, score `6.0`.

### Root cause

A extração de evidência usa fallback conceitual positivo quando não detecta uma categoria específica. A dimensão de correção só reduz o resultado para confirmação, erro, off-topic, incerteza ou sinal parcial; uma declaração curta de familiaridade não ativa nenhuma dessas proteções. O score deriva dessas dimensões superestimadas.

### Classification and impact

`SYSTEM_EVIDENCE_OVERINTERPRETATION`, secundariamente `SYSTEM_DIMENSION_INTERPRETATION_ERROR`; `HIGH`. A resposta não foi inventada, mas a força da conclusão excede o que foi demonstrado.

### Correction required

`true`, futura correção nos escopos `21` e `23`. Não implementada nesta etapa.

## Q3

### Question

`RP05-022`: tecnologias utilizadas, incluindo Java, C# e Angular.

### Response and reconstruction

`RP05-023`–`RP05-027`: confirmações fragmentadas, `Yes`, `Beijava`, confirmação de Java/backend. Não houve reconstrução semântica adicional.

### Human versus system

- Humano: evidência parcial de Java/backend e baixa cobertura; score `4.0`.
- Sistema: evidência conceptual positiva; `correctness: Strong (9)`, score `6.0`.

### Root cause

O fallback de evidência transforma conteúdo não categorizado em evidência conceptual positiva. A classificação de correção não possui um limiar para resposta fragmentada/ambígua; a completude é reduzida, mas a correção permanece forte. A divergência final também contém componente de calibração de score.

### Classification and impact

`SYSTEM_EVIDENCE_OVERINTERPRETATION` + `SYSTEM_SCORE_CALIBRATION_ERROR`; `MEDIUM`.

### Correction required

`true`, futura correção nos escopos `21` e `23`. Não implementada nesta etapa.

## Q5

### Question

`RP05-032`: `Saberia explicar para mim qual é a diferença entre o produtos e consumes em um API rest?`

### Response and reconstruction

`RP05-033`–`RP05-034`: `Consumers. ... producer e consumer ... Kafka ... Rabbit ... fila ... tópico`. A resposta é tecnicamente relacionada a mensageria, mas não responde diretamente ao enquadramento REST.

### Human versus system

- Humano: evidência parcial sobre mensageria, ausência de evidência sobre a distinção REST; score `2.0`.
- Sistema: evidência conceptual positiva sobre a resposta inteira; `correctness: Strong (9)`, score `7.05`.

### Root cause

O detector `off_topic` do Evidence Model cobre somente combinações específicas não relacionadas a este caso; não identifica que a resposta Kafka/Rabbit é tecnicamente correta para outro domínio, mas insuficiente para a pergunta REST. Sem `off_topic` ou outro sinal de incompatibilidade, `_blind_dimensions()` cai no ramo padrão de `correctness: Strong`.

### Classification and impact

`SYSTEM_EVIDENCE_OVERINTERPRETATION` + `SYSTEM_DIMENSION_INTERPRETATION_ERROR`; `CRITICAL` para a avaliação da pergunta. Não houve erro de speaker, linking ou reconstrução.

### Correction required

`true`, futura correção nos escopos `21` e `23`. Não implementada nesta etapa. O teste mínimo reproduzível deve preservar a distinção entre mensageria correta e resposta REST insuficiente.

## Q6

### Question

`RP05-035`: explicação do que é JDBC e sua função na aplicação Java.

### Response and reconstruction

`RP05-036`–`RP05-037`: `Configuração com banco... Queries, consulta de banco.` O texto é preservado.

### Human versus system

- Humano: relação direcional com banco/queries, mas sem explicação suficiente do papel da API JDBC; score `5.0`.
- Sistema: evidência conceptual positiva; `correctness: Strong (9)`, score `7.05`.

### Root cause

O detector de evidência interpreta `query` como `practical`, mas não verifica se a resposta explica JDBC ou apenas menciona consultas. A dimensão de correção permanece forte por ausência de sinal de erro. Trata-se de qualificação e aplicação de dimensão, não de perda de texto.

### Classification and impact

`SYSTEM_EVIDENCE_OVERINTERPRETATION` + `SYSTEM_SCORE_CALIBRATION_ERROR`; `HIGH`.

### Correction required

`true`, futura correção nos escopos `21` e `23`. Não implementada nesta etapa.

## Q9

### Question

`RP05-049`: uso de ferramenta de observabilidade.

### Response and reconstruction

`RP05-050`: `Sim, é o dyna trace. ... teve uma outra ferramenta agora que eu esqueci o nome`. A reconstrução preserva o texto.

### Human versus system

- Humano: declaração de uma ferramenta, sem métricas, logs, traces, investigação ou resultado; score `4.0`.
- Sistema: evidência conceptual positiva; `correctness: Strong (9)`, score `7.05`.

### Root cause

A detecção de declaração de experiência não reconhece todas as formas de `já usei/uso`, e o fallback conceptual positivo não diferencia nome de ferramenta de demonstração de observabilidade. A avaliação não inventa uma ferramenta, mas transforma uma declaração curta em correção forte.

### Classification and impact

`SYSTEM_EVIDENCE_OVERINTERPRETATION`; `HIGH`.

### Correction required

`true`, futura correção nos escopos `21` e `23`. Não implementada nesta etapa.

## Q11

### Question

`RP05-066`: uso de IA no dia a dia.

### Response and reconstruction

`RP05-067`–`RP05-070`: uso de Copilot e limitação de licença. Não há explicação de tarefas, decisões, riscos ou resultados técnicos.

### Human versus system

- Humano: declaração de uso com aplicação não demonstrada; score `4.0`.
- Sistema: evidência conceptual positiva; `correctness: Strong (9)`, `reasoning: Strong (9)`, score `7.65`.

### Root cause

O detector não classifica `uso Copilot` como declaração de experiência, e o fallback conceptual positivo não bloqueia `reasoning: Strong`; a dimensão de raciocínio depende apenas de termos heurísticos de reasoning, não da existência de uma decisão ou explicação. O resultado superestima fortemente uma resposta declarativa.

### Classification and impact

`SYSTEM_EVIDENCE_OVERINTERPRETATION` + `SYSTEM_DIMENSION_INTERPRETATION_ERROR`; `HIGH`.

### Correction required

`true`, futura correção nos escopos `21` e `23`. Não implementada nesta etapa.

## Root Cause Analysis

Foi identificado um padrão recorrente, não seis defeitos independentes:

1. O Stage 21 gera evidência `conceptual/positive` como fallback para respostas que não ativam categorias específicas.
2. A taxonomia de experiência declarada não cobre todas as formas linguísticas de declaração, como uso de ferramenta.
3. O sinal `off_topic` é estreito e não detecta a troca de domínio REST → Kafka/Rabbit.
4. O Stage 23 trata ausência de sinal negativo como `correctness: Strong`, mesmo quando a resposta é curta, fragmentada, declarativa ou responde a outro domínio. Em Q11, uma heurística de reasoning também ativa `reasoning: Strong` sem explicação técnica correspondente.
5. O cálculo de score transforma essas dimensões em notas relativamente altas.

A causa dominante é `SYSTEM_EVIDENCE_OVERINTERPRETATION`, com efeitos secundários em `SYSTEM_DIMENSION_INTERPRETATION_ERROR` e `SYSTEM_SCORE_CALIBRATION_ERROR`. A origem observável está nos estágios `21` e `23`, não em 20.3, 20.4, 20.5 ou 20.6.

## Recurring Patterns

O padrão recorrente é:

`evidence fallback positive → correctness default Strong → score elevado`

Ele aparece em respostas declarativas, respostas curtas e respostas tecnicamente corretas, porém fora do enquadramento da pergunta. O caso Q5 é o exemplo mais grave porque demonstra que conhecimento correto sobre Kafka/Rabbit não pode ser transferido automaticamente para REST.

## Impact

- Impacto local: seis avaliações individuais divergentes.
- Impacto agregado: média sistêmica `6.93` versus média humana `5.09`; diferença média absoluta `2.01`.
- Impacto de integridade: não houve invenção textual, erro de speaker, perda de segmentos ou quebra de rastreabilidade.
- Impacto semântico: alto nas perguntas afetadas, especialmente Q5; suficiente para manter o bloqueio do Stage 31.

```yaml
analysis:
  questions_investigated: 6
  system_errors: 6
  human_errors: 0
  valid_technical_disagreements: 0
  insufficient_evidence: 0
  unresolved: 0
```

## Corrections Required

Nenhuma correção foi implementada nesta etapa. A análise indica correção futura necessária nos estágios `21` e `23`, com testes específicos para:

- declaração versus demonstração;
- resposta curta/insuficiente;
- conhecimento técnico correto mas off-topic;
- distinção entre correção e completude;
- aplicação de `N/A` quando dimensões não são solicitadas;
- preservação de evidência parcial sem promovê-la a evidência forte.

O Evaluation Engine, Rubric, Evidence Model canônico, Question Taxonomy e scores históricos permaneceram inalterados.

## Unresolved Issues

- Não foi determinado se a correção deve ser implementada somente no gerador de evidências, somente no cálculo dimensional, ou em ambos; a reprodução demonstra interação entre os dois.
- A pergunta Q5 pode conter ruído de transcrição (`produtos e consumes`), embora o texto explícito contenha `API rest`; isso não justifica transferir automaticamente a resposta para Kafka/Rabbit.
- Um único avaliador humano não permite separar completamente calibração humana de erro sistêmico em todas as dimensões.

## Regression Results

Foram executados testes de Stage 31.1 e regressões anteriores sem alteração de código de produção nesta etapa:

- Stage 31.1: 8/8 testes `PASS`;
- Stage 31 e stages 30.2.1, 30.2, 30.1 e 30: 55/55 testes `PASS`;
- Stages 27–29: mantidos, sem falhas;
- Reference Harness: 8/8 suites, `PASS_WITH_WARNINGS`;
- regressão completa: 494/494 testes `PASS`.

## Conclusion

O bloqueio do Stage 31 é causado por um defeito sistêmico real e recorrente de sobreinterpretação de evidências, concentrado na interação entre Stage 21 e Stage 23. Q5 é uma falha semântica clara de proteção contra resposta correta porém fora do tópico; Q1, Q3, Q6, Q9 e Q11 demonstram promoção indevida de evidência limitada/declarativa para correção forte e scores elevados.

As divergências não são explicadas por erro humano isolado nem por diferença técnica válida. A correção é necessária, mas foi deliberadamente adiada conforme o escopo desta etapa.

## Gate

`HUMAN_VS_SYSTEM_FAILURE_ANALYSIS_COMPLETE_WITH_WARNINGS`
