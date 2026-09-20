---
type: reference
status: understood
confidence: 100
created: 2026-09-20
updated: 2026-09-20
tags:
  - interview-evaluation
  - runtime
  - test-harness
  - meta
---
# Etapa 26 — Reference Runtime / Test Harness

Esta nota documenta a implementação de referência local e determinística criada para executar os contratos das Etapas 20–25 e a execução de transcrição bruta sintética da Etapa 27. Ela não é um sistema de produção, não usa LLM, internet ou serviços externos e não processa entrevistas reais.

## 1. Localização e tecnologia

Tecnologia escolhida:

```text
Python 3 — biblioteca padrão
```

Motivo:

- o repositório não possuía código executável, manifestos ou test runner;
- Python está disponível no ambiente;
- `unittest`, `argparse`, `dataclasses` e estruturas nativas são suficientes;
- não foram adicionadas dependências externas.

Arquivos:

```text
reference_runtime/
  __init__.py
  runtime.py

tests/
  __init__.py
  fixtures.py
  test_reference_runtime.py

run_reference_runtime_tests.py
```

O runtime fica fora de `11 - Interview Evaluation/` e consome contratos documentais sem substituir as notas canônicas.

## 2. Unidade de execução

O runtime produz um `PipelineRun` com:

```text
run_id
input_id
pipeline_version
started_at
completed_at
status
readiness
stages
warnings
errors
artifacts
job_context
```

Os IDs são determinísticos para o mesmo fixture e versão. Timestamps registram execução, mas não participam da identidade dos artefatos.

Estados de execução:

```text
RUNNING
COMPLETED
BLOCKED
```

Estados de readiness:

```text
READY
READY_WITH_WARNINGS
BLOCKED
```

## 3. Responsabilidades implementadas

O runtime implementa referências mínimas para:

```text
20.1 participants
20.2 speaker attribution
20.3 question extraction
20.4 response extraction
20.5 reconstruction / normalization
20.6 question-response linking
20.7 validation gate
21 Evidence Set
23 Evaluation Engine output contract
Report handoff
```

A Rubrica é consumida como contrato documental. O Pipeline coordena as etapas; não calcula score por conta própria.

O estágio 23 recebe o Evidence Set e materializa a avaliação sintética definida pelo fixture. Isso permite testar o contrato sem alegar que o runtime é um avaliador semântico de produção.

## 4. Fixtures

O fixture nominal e os casos especializados ficam em `tests/fixtures.py`. Os fixtures são anotados de forma determinística para representar situações que um parser ou estágio upstream teria produzido:

```text
missing_response
unknown_question
ambiguous_speaker
reconstruction
technical_error
self_correction
hypothetical_answer
experience_declaration
demonstrated_experience
follow_up
reformulation
multi_segment_response
candidate_question
needs_review
ready_with_warnings
blocked
na_dimension
critical_error
```

Nenhum fixture representa uma pessoa real.

## 5. Runner

Executar todos os testes:

```text
py -3 .\run_reference_runtime_tests.py
```

Executar um caso:

```text
py -3 .\run_reference_runtime_tests.py --case=e2e-18
```

O runner imprime o diagnóstico individual do `unittest` e um resumo agregado:

```yaml
test_run:
  runtime: reference_runtime
  total: 31
  passed: 31
  failed: 0
  blocked: 0
  not_executed: 0
  status: PASS
```

## 6. Contratos testados

Os testes verificam:

- bloqueio downstream quando 20.7 retorna `BLOCKED`;
- continuidade com `READY_WITH_WARNINGS`;
- preservação de `missing`, `unknown` e `needs_review`;
- source traceability;
- original e reconstructed text;
- autocorreção e hipótese;
- experiência declarada versus demonstrada;
- follow-up e reformulação;
- múltiplos segmentos;
- exclusão de perguntas do candidato da avaliação;
- idempotência;
- alteração controlada e stale warning;
- N/A;
- erro técnico;
- invariância de tamanho, eloquência, senioridade e complexidade;
- separação de Job Context;
- relatório consumindo avaliações existentes;
- fronteiras de responsabilidade.

## 7. Resultado da execução

Execução local realizada em `2026-09-20`:

```text
31/31 PASS
0 FAIL
0 BLOCKED
0 NOT_EXECUTED
```

Os 31 testes são:

```text
E2E-01 a E2E-30
1 teste adicional de separação de responsabilidades
```

## 8. Limitações

1. O runtime usa fixtures anotados; não interpreta transcrição livre.
2. O estágio de avaliação materializa especificações sintéticas do fixture; não substitui um modelo semântico de produção.
3. Não há integração com LLM, Azure, OpenAI ou serviços externos.
4. Não há persistência de relatório de candidato: o Report é um artefato em memória de teste.
5. Os baselines históricos das Etapas 19/19.1 continuam indisponíveis.

Essas limitações não foram ocultadas nem usadas para alterar a Rubrica ou o Evaluation Engine.

## 9. Gate da Etapa 26

```text
REFERENCE_RUNTIME_COMPLETE
```

Critérios atendidos:

- runtime mínimo existe;
- test harness existe;
- fixtures existem;
- runner executa todos os testes e caso individual;
- contratos essenciais são testáveis;
- resultados são determinísticos;
- rastreabilidade é verificada;
- `BLOCKED` interrompe downstream;
- não houve alteração indevida das regras anteriores;
- 31/31 testes passaram.

Status:

```text
READY_WITH_WARNINGS
```

O warning é limitado ao escopo de referência: fixtures anotados, ausência de parser de produção e baselines históricos indisponíveis.

## 10. Etapa 27 — raw synthetic transcript

A Etapa 27 reutiliza este runtime com o adaptador `raw_transcript` e executa:

```text
raw transcript
→ 20.1–20.7
→ Structured Interview
→ Evidence Set
→ Evaluation
→ Report Handoff
```

O adaptador é determinístico e controlado por regras para o cenário sintético. Ele preserva o transcript bruto, timestamps, labels, intervenções, ambiguidades, `missing`, autocorreção, hipótese, experiência e source traceability. Não transforma o runtime em parser NLP/LLM de produção.

Resultado registrado:

```text
28 segmentos
3 participantes
12 perguntas
80 testes Stage 27
READY_WITH_WARNINGS
```

Consulte [[Synthetic Interview Full Run]] para o oracle, a matriz de rastreabilidade, as invariantes e os resultados detalhados.
