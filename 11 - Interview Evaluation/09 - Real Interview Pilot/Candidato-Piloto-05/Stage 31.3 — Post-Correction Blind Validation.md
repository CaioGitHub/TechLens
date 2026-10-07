# Stage 31.3 — Post-Correction Blind Validation

## Objetivo

Validar independentemente se a correção do Stage 31.2 melhorou a interpretação semântica de evidências sem introduzir falsos negativos ou depender de tamanho, jargão, senioridade ou contexto externo.

## Baseline do Stage 31

- Gate histórico: `HUMAN_VS_SYSTEM_BLOCKED`.
- MAE original: `2.01`.
- O relatório humano independente e a comparação histórica permaneceram congelados.

## Correção avaliada

Foi avaliado o runtime exatamente como estava após o Stage 31.2. Nenhum arquivo de produção foi alterado durante a validação. Nenhuma expectativa humana ou score do Stage 31.2 foi enviado ao executor.

## Metodologia blind

O executor recebeu somente fixtures com transcript, participantes e metadata opcional. Os oráculos semânticos e o comparador ficaram no arquivo de testes, separados da entrada do executor. Os oráculos não continham scores humanos nem os resultados do Stage 31.2.

Foram executados 26 casos independentes cobrindo respostas corretas, parciais, superficiais, off-topic, erradas, declarativas, demonstradas, hipotéticas, curtas, longas com jargão, incompletas, autocorrigidas, incertas, sem resposta, integradas e com linguagem informal.

## Casos de validação

As categorias A–T foram cobertas por `tests/test_stage_31_3_post_correction_blind_validation.py`. A execução confirmou:

- respostas corretas relacionadas continuam recebendo crédito;
- Q5 REST versus Kafka/Rabbit é representado como `off_topic` e não recebe `correctness: Strong`;
- declarações permanecem distintas de experiência demonstrada;
- hipóteses não são convertidas em experiência;
- experiência demonstrada concreta é reconhecida;
- senioridade e contexto externo não alteram a avaliação;
- a execução é determinística.

## Resultados por categoria

### Passaram

- Q5 nos quatro níveis: linking, evidência, pertinência e avaliação;
- respostas REST/Java/troubleshooting relacionadas;
- declaração versus demonstração;
- hipótese versus experiência;
- mutation directional básica;
- isolamento de contexto;
- idempotência e proteção dos artefatos históricos;
- ausência de falsos negativos críticos nos casos positivos principais.

### Falharam

| Caso | Esperado | Atual | Causa provável |
|---|---|---|---|
| D2 | `off_topic` para Docker → Kubernetes | `conceptual/insufficient`, score `4.0` | detector de incompatibilidade de domínio não generaliza para esse par |
| D3 | `off_topic` para SQL → Redis | `conceptual/positive`, `correctness: Strong`, score `6.0` | detector de incompatibilidade de domínio não generaliza para esse par |
| L1 | `off_topic` para Dependency Injection → Spring Data | `conceptual/positive`, `correctness: Strong`, score `6.0` | detector de incompatibilidade de domínio não generaliza para esse par |

Além disso, uma invariância de estilo falhou: `HTTP 500` em resposta curta recebeu `Insufficient`, enquanto a mesma ideia em linguagem informal recebeu `Strong`. Isso demonstra que a qualificação de insuficiência ainda depende excessivamente da forma lexical.

## Q5

O caso original permaneceu corretamente vinculado à Q5. A resposta contém Kafka/Rabbit e não contém explicação de REST. O Evidence Set contém `off_topic/negative` e `conceptual/partial`; a avaliação usa `correctness: Insufficient`, `confidence: medium` e não transfere conhecimento de mensageria para REST.

Q5 passou nos níveis de linking, evidência, pertinência e avaliação. O conteúdo Kafka/Rabbit não foi classificado como tecnicamente errado; foi classificado como tecnicamente válido, porém inadequado para a pergunta avaliada.

## Falsos positivos

Foram encontrados 3 falsos positivos semânticos residuais: D2, D3 e L1. D3 e L1 são críticos para o objetivo desta etapa porque ainda permitem `correctness: Strong` para respostas corretas sobre outro assunto.

## Falsos negativos

Não foram encontrados falsos negativos críticos nos casos independentes de REST, HTTP, troubleshooting, integração Java/Spring/Azure ou experiência concreta. A resposta curta correta recebeu crédito, embora a comparação curta versus informal tenha revelado uma falha de invariância de qualificação.

## Declaração vs demonstração

O par de experiência foi distinguido corretamente:

```text
declaração → experience_declaration
detalhes concretos → demonstrated_experience
troubleshooting concreto → progressão de evidência
```

Respostas hipotéticas permaneceram sem `demonstrated_experience`.

## Pertinência

Q5 passou, mas a generalização da pertinência falhou para Docker/Kubernetes, SQL/Redis e Dependency Injection/Spring Data. Portanto, a correção é parcialmente generalizável, mas não protege ainda todos os domínios equivalentes.

## Completude

Respostas parciais e superficiais receberam dimensões de profundidade/completude menores que respostas mais desenvolvidas nos casos testados. A resposta curta correta recebeu crédito, mas a invariância lexical curta/informal não foi preservada.

## Profundidade

Jargão isolado não demonstrou profundidade forte de forma consistente; contudo, o caso longo com jargão recebeu score maior que algumas respostas curtas. A métrica não caracteriza sozinha um falso positivo crítico, mas deve permanecer sob observação.

## Invariâncias

Passaram:

- senioridade declarada;
- cargo;
- CV/contexto externo;
- score esperado;
- avaliação humana;
- execução repetida;
- source traceability.

Falhou:

- equivalência semântica entre resposta curta correta e a mesma resposta em linguagem informal.

## Mutation Tests

Passaram as mutações de:

- resposta relacionada versus resposta Kafka off-topic;
- resposta parcial versus investigação mais completa;
- declaração sem demonstração;
- hipótese sem experiência;
- adição de contexto externo.

As mutações de domínio revelaram as falhas D2, D3 e L1.

## Context Isolation

Adicionar CV, cargo, senioridade, empresa, vaga, score esperado, score humano e relatório histórico não alterou os resultados do executor.

## FRA-001 → FRA-006

Os seis casos foram reexecutados de forma independente. Os resultados observados permaneceram:

| Caso | Score | Evidência principal | Resultado |
|---|---:|---|---|
| FRA-001 / Q1 | 4.0 | `conceptual/insufficient` | passou |
| FRA-002 / Q3 | 4.0 | fragmentos não promovidos a Strong | passou |
| FRA-003 / Q5 | 4.45 | `off_topic` + `partial` | passou |
| FRA-004 / Q6 | 5.85 | `conceptual/partial` | passou |
| FRA-005 / Q9 | 4.0 | `experience_declaration/insufficient` | passou |
| FRA-006 / Q11 | 4.0 | declaração sem reasoning forte | passou |

## Human vs System pós-correção

Foi utilizada a avaliação humana congelada do Stage 31 e o resultado independente já persistido após a correção:

- MAE baseline: `2.01`;
- MAE pós-correção: `0.64`;
- maior divergência: Q5, `2.45`;
- concordâncias ou diferenças até `0.05`: Q1, Q2, Q3, Q8, Q9 e Q11;
- divergências menores: Q4, Q6 e Q7;
- divergências materiais: Q5 e Q10.

A redução do MAE é consistente com melhoria semântica nos seis casos FRA, mas não é suficiente para aprovar esta etapa. As falhas independentes D2, D3, L1 e de invariância lexical impedem concluir que a correção seja generalizável.

## Divergências restantes

As divergências materiais restantes devem ser tratadas como `SYSTEM_ERROR` ou `UNRESOLVED`, não como erro humano, porque os oráculos independentes demonstram que a resposta é tecnicamente válida para outro domínio e não responde à pergunta.

## Regression

O runtime não foi alterado durante a validação. Os testes históricos anteriores ao Stage 31.3 permaneceram aprovados:

- Stage 31.3 focused suite: `12/12 PASS`, with 3 semantic findings recorded by the comparator;
- Stage 31.2 focado: `9/9 PASS`;
- Stages 31 relacionados: `25/25 PASS`;
- Stages 27–29: sem novas falhas;
- regressão completa final: `515/515 PASS`;
- Reference Harness final: `8/8 suites`, `0 failed`, `PASS_WITH_WARNINGS`.

A suíte nova do Stage 31.3 executou todos os testes de infraestrutura e determinismo com sucesso; o comparador semântico registrou 3 findings (`D2`, `D3`, `L1`). O gate permanece bloqueado por esses findings, não por falha de execução da suíte.

## Reproducibility

As execuções repetidas dos 26 casos produziram os mesmos artefatos, scores, evidências, IDs e confidence. O resultado é determinístico, embora determinismo não compense as falhas semânticas.

## Metrics

```yaml
validation:
  total_cases: 26
  passed: 23
  warnings: 0
  failed: 3
  blocked: 0

semantic:
  false_positive_failures: 3
  false_negative_failures: 0
  off_topic_cases: 4
  partial_cases: 4
  demonstrated_experience_cases: 4
  declared_experience_cases: 3
  hypothetical_cases: 1

human_comparison:
  baseline_mae: 2.01
  post_correction_mae: 0.64
  material_divergences: 2
  minor_divergences: 3
  agreements: 6

reproducibility:
  run_1: deterministic
  run_2: deterministic
  deterministic: true

regression:
  full_suite: 503/503 PASS before Stage 31.3 assertions
  harness: 8/8 suites, 0 failed, PASS_WITH_WARNINGS
```

## Limitations

- A validação não deve adicionar heurísticas ao runtime; por isso as falhas foram preservadas.
- A taxonomia atual não oferece uma relação explícita e geral entre domínio perguntado e domínio respondido.
- A validação humana continua sendo uma única avaliação independente.

## Gate

`POST_CORRECTION_BLIND_VALIDATION_BLOCKED`

## Decisão

A correção do Stage 31.2 foi semanticamente validada apenas parcialmente. Q5 foi corrigido de forma defensável e a comparação humana melhorou por uma mudança semântica real nos seis casos FRA. Entretanto, a generalização para outros pares off-topic falhou e existe uma falha de invariância entre resposta curta e informal. O sistema não deve avançar para Stage 32 nesta execução.
