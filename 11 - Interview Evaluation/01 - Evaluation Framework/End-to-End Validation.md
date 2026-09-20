---
type: reference
status: learning
confidence: 100
created: 2026-09-20
updated: 2026-09-20
tags:
  - interview-evaluation
  - validation
  - end-to-end
  - meta
---
# Etapa 25 — End-to-End Validation

Esta nota valida os contratos ponta a ponta das Etapas 20–24 sem processar entrevista real. Os casos são sintéticos e controlados. Como o repositório não possui executor/runtime de pipeline, a execução operacional dos casos E2E permanece `NOT_EXECUTED`; as validações estruturais e as revisões manuais dos contratos são registradas separadamente.

## 1. Objetivo e escopo

Validar o encadeamento:

```text
RAW TRANSCRIPT
↓
Transcription Processing 20.1–20.7
↓
STRUCTURED INTERVIEW
↓
Evidence Model 21
↓
EVIDENCE SET
↓
Rubric 22
↓
Evaluation Engine 23
↓
EVALUATIONS
↓
Interview Evaluation Model
↓
FINAL INTERVIEW REPORT
```

A validação verifica:

- compatibilidade entre saída e entrada de cada etapa;
- preservação de conteúdo e metadata;
- propagação de warnings e `needs_review`;
- comportamento de `missing`, `unknown` e evidência ausente;
- gates, bloqueios e continuidade controlada;
- rastreabilidade ponta a ponta;
- idempotência, reprocessamento e staleness;
- invariâncias contra tamanho, eloquência, senioridade e complexidade;
- separação de responsabilidades.

Esta etapa não altera notas técnicas, pesos, regras da Rubrica ou avaliações históricas.

## 2. Artefatos avaliados

| Artefato | Função | Resultado estrutural |
|---|---|---|
| 20.1–20.6 | estruturar participantes, speakers, perguntas, respostas, reconstruções e links | PASS |
| 20.7 Validation | validar a Structured Interview e emitir readiness | PASS |
| 21 Evidence Model | produzir o Evidence Set rastreável | PASS |
| 22 Scoring Rubric | definir escala, dimensões, N/A e baselines | PASS_WITH_WARNING |
| 23 Evaluation Engine | produzir avaliações individuais | PASS_WITH_WARNING |
| 24 Interview Evaluation Pipeline | orquestrar handoffs e gates | PASS_WITH_WARNING |
| Interview Evaluation Model | consolidar avaliações sem recalcular silenciosamente | PASS |
| Job Context Model | permanecer separado da nota técnica | PASS |
| Report persistence | definir destino e preservação do relatório | PASS |

## 3. Fixture sintético nominal

O fixture abaixo é uma entrevista fictícia, sem nome de pessoa real. Ele existe somente como entrada controlada para revisão dos contratos:

```yaml
fixture_id: SYN-E2E-01
transcript:
  - id: S01
    speaker: interviewer
    text: "Como você investigaria aumento de latência em uma API?"
  - id: S02
    speaker: candidate
    text: "Eu começaria medindo p95 e p99, separaria aplicação de dependências e compararia com uma janela saudável."
  - id: S03
    speaker: interviewer
    text: "E se o banco fosse o principal suspeito?"
  - id: S04
    speaker: candidate
    text: "Eu verificaria queries lentas, planos de execução e saturação de conexões antes de alterar índices."
participants:
  - participant_id: P-INTERVIEWER
    role: interviewer
  - participant_id: P-CANDIDATE
    role: candidate
questions:
  - question_id: Q1
    source:
      segment_ids: [S01]
  - question_id: Q1.1
    follow_up_of: Q1
    source:
      segment_ids: [S03]
responses:
  - response_id: R1
    question_id: Q1
    source:
      segment_ids: [S02]
  - response_id: R1.1
    question_id: Q1.1
    source:
      segment_ids: [S04]
```

Resultado esperado do fixture:

```text
Participant → Speaker → Question → Response → Link
→ Validation READY → Evidence Set → Evaluation → Report handoff
```

O fixture não foi enviado a um executor de runtime e não gerou score persistido.

## 4. Casos E2E controlados

Status possíveis:

```text
PASS
PASS_WITH_WARNING
FAIL
BLOCKED
NOT_EXECUTED
```

`NOT_EXECUTED` não é contado como aprovação. Nos casos abaixo, `NOT_EXECUTED` significa que o comportamento foi especificado e revisado contra os contratos documentais, mas não executado em runtime.

| ID | Caso | Resultado esperado | Status | Evidência disponível |
|---|---|---|---|---|
| E2E-01 | fluxo nominal | Structured Interview → Evidence Set → Evaluation rastreável | NOT_EXECUTED | fixture sintético e revisão estrutural |
| E2E-02 | pergunta sem resposta | `response_status: missing`, sem evidência negativa automática | NOT_EXECUTED | contrato 20.4/20.6/20.7 |
| E2E-03 | resposta sem pergunta | `question_id: unknown`, sem vínculo forçado | NOT_EXECUTED | contrato 20.4/20.6/21 |
| E2E-04 | speaker ambíguo | `unknown`, `needs_review: true`, confidence reduzida | NOT_EXECUTED | contrato 20.1/20.2/20.7 |
| E2E-05 | erro de transcrição | `original_text` preservado; forma corrigida sem conteúdo novo | NOT_EXECUTED | contrato 20.5 |
| E2E-06 | resposta incorreta | incorreção preservada até Evidence/Evaluation | NOT_EXECUTED | contrato 20.5/21/23 |
| E2E-07 | autocorreção | afirmação inicial e correção preservadas em sequência | NOT_EXECUTED | contrato 20.4/20.5/21/23 |
| E2E-08 | resposta hipotética | hipótese não convertida em experiência real | NOT_EXECUTED | contrato 20.4/21/23 |
| E2E-09 | experiência declarada | `experience_declaration`, sem `demonstrated_experience` automático | NOT_EXECUTED | CAL-01 e Evidence Model |
| E2E-10 | experiência demonstrada | contexto, ação, decisão e resultado sustentam experiência demonstrada | NOT_EXECUTED | contrato 20.4/21 |
| E2E-11 | follow-up | `Q1.1.follow_up_of: Q1` preservado | NOT_EXECUTED | contrato 20.3/20.6 |
| E2E-12 | reformulação | `reformulation_of` preservado quando aplicável | NOT_EXECUTED | contrato 20.3/20.6 |
| E2E-13 | resposta em vários segmentos | ordem e `source.segment_ids` preservados | NOT_EXECUTED | contrato 20.4/20.5/20.7 |
| E2E-14 | entrevistador complementa | fala não incorporada à resposta do candidato | NOT_EXECUTED | contrato 20.2/20.4/21 |
| E2E-15 | candidato faz pergunta | pergunta não gera avaliação técnica indevida | NOT_EXECUTED | contrato 20.3/20.6/23 |
| E2E-16 | `needs_review` | marca e justificativa atravessam os handoffs | NOT_EXECUTED | contrato Pipeline §12 |
| E2E-17 | `READY_WITH_WARNINGS` | pipeline continua e warning é propagado | NOT_EXECUTED | gates 20.7/21/24 |
| E2E-18 | `BLOCKED` | Evidence, Evaluation e Report não são executados | NOT_EXECUTED | teste de bloqueio do Pipeline |
| E2E-19 | traceability | `evaluation → question → response → evidence → source` completo | NOT_EXECUTED | schemas canônicos |
| E2E-20 | idempotência | mesmos IDs e nenhum artefato duplicado | NOT_EXECUTED | contrato Pipeline §17 |
| E2E-21 | reprocessamento | dependentes downstream identificados para regeneração | NOT_EXECUTED | contrato Pipeline §18 |
| E2E-22 | stale artifacts | artefato desatualizado não é reutilizado silenciosamente | NOT_EXECUTED | contrato Pipeline §18 |
| E2E-23 | N/A e normalização | dimensão excluída e pesos restantes normalizados | NOT_EXECUTED | Rubric §28 e Engine §38 |
| E2E-24 | erro crítico | impacto proporcional, sem teto universal automático | NOT_EXECUTED | Rubric/Engine |
| E2E-25 | invariância de tamanho | texto maior não altera score por si só | NOT_EXECUTED | Rubric/Engine |
| E2E-26 | invariância de eloquência | articulação não cria evidência técnica | NOT_EXECUTED | Rubric/Engine |
| E2E-27 | invariância de senioridade | anos declarados não alteram avaliação | NOT_EXECUTED | Rubric/Engine/Job Context |
| E2E-28 | invariância de complexidade | complexidade não gera crédito automático | NOT_EXECUTED | Question Taxonomy/Rubric |
| E2E-29 | separação Job Context | contexto não altera Evidence ou score | NOT_EXECUTED | Job Context/Engine |
| E2E-30 | relatório final | Report consome Evaluation e não recalcula score | NOT_EXECUTED | Interview Evaluation Model/Pipeline |

**Resultado:** 30/30 casos definidos; 0/30 executados em runtime.

## 5. Casos de bloqueio e warning

### E2E-17 — `READY_WITH_WARNINGS`

Condição sintética:

```yaml
validation:
  status: READY_WITH_WARNINGS
  warnings:
    - code: V-REVIEW-001
      message: "speaker ambiguity limited to a non-central segment"
      needs_review: true
```

Resultado contratual:

```text
pipeline continua
warning preservado
Evidence Model executável
Evaluation executável quando a limitação não impedir a conclusão
warning rastreável até o Report
```

Status: `NOT_EXECUTED` em runtime; contrato revisado: `PASS_WITH_WARNING`.

### E2E-18 — `BLOCKED`

Condição sintética:

```yaml
validation:
  status: BLOCKED
  blockers:
    - code: V-CRITICAL-001
      message: "central candidate response has invalid source reference"
```

Resultado contratual:

```text
pipeline.status = BLOCKED
Evidence Model = não executado
Evaluation Engine = não executado
Final Report = não gerado
candidate_status = não inferido
```

Status: `NOT_EXECUTED` em runtime; contrato revisado: `PASS`.

## 6. Testes adicionais de integridade

| # | Teste | Resultado esperado | Status |
|---|---|---|---|
| A1 | IDs estáveis | nenhuma duplicação | PASS_WITH_WARNING |
| A2 | IDs duplicados | validação rejeita ou bloqueia | PASS_WITH_WARNING |
| A3 | referência órfã | não chega como avaliação válida | PASS_WITH_WARNING |
| A4 | `question_id` inexistente | erro estrutural identificado | PASS_WITH_WARNING |
| A5 | `response_id` inexistente | erro estrutural identificado | PASS_WITH_WARNING |
| A6 | `evidence_id` inexistente | Evaluation não referencia evidência fantasma | PASS_WITH_WARNING |
| A7 | `evaluation.id` duplicado | consolidação rejeita duplicata | PASS_WITH_WARNING |
| A8 | `source.segment_ids` inexistente | readiness reduzida ou bloqueada | PASS_WITH_WARNING |
| A9 | ciclo em `follow_up_of` | Validation identifica circularidade | PASS_WITH_WARNING |
| A10 | ordem temporal inconsistente | Validation identifica inconsistência | PASS_WITH_WARNING |

**Resultado:** 10/10 contratos revisados estruturalmente; 0/10 executados em runtime.

## 7. Testes de invariância

| ID | Invariante | Resultado estrutural |
|---|---|---|
| I1 | mesmos inputs produzem IDs estáveis | PASS_WITH_WARNING |
| I2 | texto irrelevante não cria evidência | PASS_WITH_WARNING |
| I3 | tom mais confiante não eleva score | PASS_WITH_WARNING |
| I4 | senioridade declarada não altera score | PASS_WITH_WARNING |
| I5 | correção upstream torna downstream potencialmente stale | PASS_WITH_WARNING |
| I6 | warning não desaparece sem justificativa | PASS_WITH_WARNING |
| I7 | `missing` não vira evidência negativa | PASS_WITH_WARNING |
| I8 | `unknown` não vira vínculo artificial | PASS_WITH_WARNING |
| I9 | source removido reduz readiness | PASS_WITH_WARNING |
| I10 | relatório repetido não duplica arquivo | PASS_WITH_WARNING |

**Resultado:** 10/10 invariantes revisados; 0/10 executados em runtime.

## 8. Separação de responsabilidades

| Fronteira | Regra verificada | Resultado |
|---|---|---|
| Transcription Processing | não pontua nem infere senioridade | PASS |
| Evidence Model | não calcula score nem corrige resposta | PASS |
| Rubric | não processa transcript nem cria evidência | PASS |
| Evaluation Engine | não reconstrói transcript nem substitui Evidence Set | PASS |
| Pipeline | não interpreta conhecimento nem calcula score | PASS |
| Report | não recalcula score, média ou dimensões | PASS |
| Job Context | não altera score individual | PASS |

**Resultado:** 7/7 fronteiras aprovadas na revisão documental.

## 9. Rastreabilidade ponta a ponta

A cadeia exigida é:

```text
participant_id
↓
speaker_id / participant_id
↓
question_id
↓
response_id
↓
evidence_id
↓
evaluation.id
↓
source.segment_ids
↓
raw transcript
```

Verificações estruturais:

- `question_id`, `response_id` e `evidence_id` são preservados nos schemas relevantes;
- `evaluation.id` é o identificador canônico do Engine;
- `source.segment_ids` aponta para a Structured Interview e, por consequência, para o transcript;
- `needs_review` e os campos de confidence permanecem separados;
- referências inexistentes e sources órfãos são tratados pela Validation;
- o Report consome a avaliação existente.

Status: `PASS_WITH_WARNING` — cadeia documental íntegra; percurso runtime não executado.

## 10. Gates verificados

| Gate | Verificação | Resultado |
|---|---|---|
| `TRANSCRIPTION_PROCESSING_COMPLETE` | Stage 20.7 permite somente `READY` ou `READY_WITH_WARNINGS` | PASS |
| `EVIDENCE_MODEL_COMPLETE` | Evidence Model bloqueia entrada Stage 20 `BLOCKED` | PASS |
| `RUBRIC_COMPLETE` | Rubrica define dimensões, N/A, pesos e baselines | PASS_WITH_WARNING |
| `EVALUATION_ENGINE_COMPLETE` | Engine possui schema, score, confidence e traceability | PASS_WITH_WARNING |
| `PIPELINE_READY` | Pipeline possui handoffs, bloqueio e propagação | PASS_WITH_WARNING |
| `END_TO_END_VALIDATION_COMPLETE` | esta nota registra o resultado e limitações | PASS_WITH_WARNING |

## 11. Comparação com calibração

Os casos aplicáveis foram comparados conceitualmente com os baselines documentados:

| Baseline | Correspondência E2E | Situação |
|---|---|---|
| CAL-01 | E2E-09 experiência declarada sem evidência | compatível por contrato |
| CAL-02 | não reproduzido por fixture específica | baseline não executado |
| CAL-03 | E2E-06 resposta incorreta | compatível por contrato |
| CAL-04 | não reproduzido por fixture específica | baseline não executado |
| CAL-05 | E2E-07 autocorreção | compatível por contrato |
| CAL-06 | E2E-01 troubleshooting | compatível por contrato |
| CAL-07 | não reproduzido por fixture específica | baseline não executado |
| CAL-08 | não reproduzido por fixture específica | baseline não executado |
| CAL-09 | E2E-25 resposta curta precisa | compatível por contrato |
| CAL-10 | não reproduzido por fixture específica | baseline não executado |

Isso não significa que qualquer baseline histórico foi executado. Os artefatos históricos das Etapas 19/19.1 continuam ausentes.

## 12. Divergências e correções

### Finding E2E-001

```text
Finding: ausência de executor/runtime no repositório
Evidence: não foram encontrados scripts, testes executáveis ou aplicação de pipeline
Impact: casos E2E não podem ser classificados como execução operacional
Correction: nenhuma alteração de regra; resultados marcados NOT_EXECUTED
Affected Stage: 25
Regression Risk: nenhum
```

### Finding E2E-002

```text
Finding: baselines CAL-01–CAL-10 não possuem artefatos históricos executáveis
Evidence: Rubric e Engine registram os valores como baselines documentados
Impact: comparação empírica histórica não pode ser afirmada
Correction: nenhuma; distinção documental preservada
Affected Stage: 22, 23, 25
Regression Risk: nenhum
```

Nenhuma divergência estrutural foi encontrada entre os contratos 20–24 durante a revisão.

## 13. Regression check

Validações realizadas após a criação desta nota:

- `git diff --check`;
- verificação de referências internas dos arquivos alterados;
- verificação dos gates e nomes canônicos;
- verificação de `missing`, `unknown`, `needs_review` e campos de confidence;
- contagem dos 30 casos E2E;
- contagem dos 10 testes adicionais;
- contagem dos 10 testes de invariância;
- verificação das 7 fronteiras de responsabilidade;
- confirmação de que nenhum arquivo de Rubric, Evidence Model, Evaluation Engine ou Stage 20 foi alterado.

Resultado: `PASS`.

## 14. Limitações

1. O repositório não possui executor/runtime de pipeline identificado.
2. Os 30 casos E2E foram definidos e revisados contra os contratos, mas não executados operacionalmente.
3. Os testes adicionais e invariantes foram revisados estruturalmente, não executados por runtime.
4. Os baselines históricos das Etapas 19/19.1 não estão disponíveis.
5. Não foi produzido score, avaliação ou relatório de candidato real.

## 15. Conclusão

Os contratos documentais das Etapas 20–24 são compatíveis:

```text
Transcription Processing ✓
Evidence Model ✓
Rubric ✓
Evaluation Engine ✓
Pipeline / Orchestration ✓
Interview Evaluation Model ✓
Job Context ✓
Report persistence ✓
Traceability ✓
```

A arquitetura está pronta para receber uma implementação/runtime de execução controlada, mas a execução ponta a ponta real não pode ser afirmada nesta base.

## 16. Gate da Etapa 25

```text
END_TO_END_VALIDATION_COMPLETE
```

Status:

```text
READY_WITH_WARNINGS
```

O status decorre exclusivamente da ausência de runtime executável e dos baselines históricos indisponíveis. Não há falha crítica documental conhecida.

```text
Nenhuma entrevista real foi processada.
Nenhum score real foi produzido.
Nenhum relatório real foi criado ou alterado.

## Runtime Validation

O Reference Runtime da Etapa 26 foi executado localmente com Python 3 via:

```text
py -3 .\run_reference_runtime_tests.py
```

Também é possível executar um caso individual:

```text
py -3 .\run_reference_runtime_tests.py --case=e2e-18
```

Execução registrada em `2026-09-20`:

```yaml
test_run:
  runtime: "reference_runtime"
  pipeline_version: "26-reference-1"
  total: 31
  passed: 31
  failed: 0
  blocked: 0
  not_executed: 0
  warnings: 0
  status: PASS
```

Resultado detalhado:

- `E2E-01` a `E2E-30`: `PASS`
- teste adicional de fronteiras de responsabilidade: `PASS`
- 31/31 testes executados
- 31/31 aprovados
- 0 falhas
- 0 bloqueios
- 0 `NOT_EXECUTED`

Os testes exercitam fixtures sintéticos anotados, não transcrição livre nem entrevista real. O runtime é uma implementação de referência determinística para os contratos; não é ainda um parser de produção nem uma integração com LLM.

O resultado de runtime não altera os registros anteriores de validação estrutural: eles continuam documentados separadamente. Os baselines históricos das Etapas 19/19.1 também continuam não executados.

## Gate atualizado

```text
REFERENCE_RUNTIME_COMPLETE
```

O Reference Runtime possui implementação local, fixtures, runner, execução repetível, bloqueio downstream, propagação de warnings, rastreabilidade, idempotência, stale detection e testes de separação de responsabilidades.

Status da Etapa 25 após a validação de runtime:

```text
READY_WITH_WARNINGS
```

O warning permanece por duas limitações conhecidas: o runtime é uma implementação de referência baseada em fixtures sintéticos anotados, não um parser de produção; e os baselines históricos das Etapas 19/19.1 continuam indisponíveis.
```

## Ver também

- [[Interview Evaluation Pipeline]]
- [[Transcription Processing Model]]
- [[20.7 - Validation]]
- [[Evidence Model]]
- [[Scoring Rubric]]
- [[Evaluation Engine]]
- [[Interview Evaluation Model]]
- [[Job Context Model]]
- [[Interview Evaluation MOC]]
