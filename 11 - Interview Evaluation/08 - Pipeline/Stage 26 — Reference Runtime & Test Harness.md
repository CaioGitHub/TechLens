# Stage 26 — Reference Runtime & Test Harness

## Objetivo

Consolidar a infraestrutura para executar e validar o Reference Runtime de forma reproduzível, determinística, isolada, rastreável e segura para reprocessamento e regressão contínua.

Esta etapa não altera a semântica de transcrição, evidência, scoring, auditoria ou materialização.

## Arquitetura

```text
Reference Runtime
        │
        ├── Production-like execution path
        │
        └── Test Harness
                │
                ├── Registry de suites
                ├── Cópia isolada por suite
                ├── Execução sequencial ou paralela
                ├── Contrato estruturado de resultados
                └── Cleanup automático
```

O harness apenas executa processos, observa exit codes/output, compara estados e reporta resultados. Ele não recalcula avaliações.

## Reference Runtime

Foram inventariados:

* `reference_runtime/runtime.py`: runtime sintético controlado de 20.x–23;
* `reference_runtime/evaluation_engine.py`: consolidação Stage 23;
* `reference_runtime/global_audit.py`: auditoria independente Stage 23.1;
* `reference_runtime/materialization.py`: materialização Stage 23.2;
* `reference_runtime/interview_pipeline.py`: coordenação Stage 24;
* `reference_runtime/orchestration.py`: orchestration legado preservado;
* `reference_runtime/harness.py`: executor de regressão Stage 26.

As entradas e saídas permanecem explícitas e não há alteração dos contratos semânticos existentes.

## Test Harness

O registry atual contém oito suites:

| Suite | Executor | Fixture strategy | Escrita em artefato canônico |
|---|---|---|---|
| `reference_runtime` | `run_reference_runtime_tests.py` | cópia isolada | não |
| `stage_24_orchestration` | unittest | cópia isolada | não |
| `stage_25_end_to_end` | unittest | cópia isolada/temp | não |
| `full_unittest` | unittest discovery | cópia isolada | não |
| `synthetic_interview` | `run_synthetic_interview.py` | fixtures geradas | não |
| `semantic_blind_calibration` | `run_semantic_blind_calibration.py` | fixtures geradas | não |
| `adversarial_edge_cases` | `run_adversarial_edge_cases.py` | fixtures geradas | não |
| `stage_30_1` | unittest | cópia isolada | não |

`full_unittest` inclui os testes Stage 26; não foi criada uma segunda suite semântica para eles.

O executor aceita:

```text
py -3 .\run_reference_harness.py
py -3 .\run_reference_harness.py --parallel
```

`--parallel` executa suites concorrentes em cópias independentes do repositório. `--shared-workspace` existe apenas para diagnóstico e não é o modo recomendado.

## Contrato de resultado

Cada suite retorna:

```yaml
id: suite-name
name: suite-name
status: PASS | PASS_WITH_WARNINGS | FAIL | BLOCKED
duration_ms: number
return_code: number
warnings: []
errors: []
artifacts: []
fixture_strategy: isolated-copy
```

O relatório agregado contém:

```yaml
harness_version: 26-reference-harness-2
execution_id: deterministic-id
suites: []
executed: number
planned: number
passed: number
warnings_count: number
failed: number
blocked: number
parallel: boolean
isolated: boolean
status: PASS | PASS_WITH_WARNINGS | FAIL
```

Uma suite com falha não interrompe suites independentes. `BLOCKED` é preservado como estado distinto de `FAIL`; bloqueios esperados de cenários adversariais resultam em `PASS_WITH_WARNINGS` no agregado quando não há falha de implementação.

## Fixtures

| Classificação | Uso |
|---|---|
| `READ_ONLY` | Markdown canônico consumido pelo runtime, incluindo Evidence Set, Individual Evaluations, v1, v2 e Structured Interview |
| `COPY_ON_WRITE` | cópias históricas e fixtures alteradas por testes |
| `GENERATED` | fixtures de `tests/fixtures.py`, calibração, adversarial e entrevista sintética |

Os testes de materialização já utilizam destinos temporários. O harness agora garante uma cópia de filesystem por suite, impedindo escrita concorrente no checkout original.

## Isolamento

Cada suite recebe:

```text
TemporaryDirectory/
└── <suite-name>/
    ├── reference_runtime/
    ├── tests/
    └── scripts/
```

O checkout original é somente fonte de cópia. Caches `__pycache__`, `.git`, relatórios temporários e artefatos de execução são excluídos da cópia.

Os artefatos canônicos protegidos permanecem fora das áreas de escrita concorrente. A validação de hash antes/depois confirmou sua preservação.

## Determinismo

Foi mantida a projeção determinística do runtime, removendo apenas metadados operacionais como timestamps e duração. IDs semânticos, scores, evidências, warnings, gates e traceability são comparáveis entre execuções.

O `execution_id` do harness depende somente dos nomes das suites. `duration_ms` é operacional e não participa de comparações semânticas.

## Concorrência

O modo paralelo usa subprocessos independentes e cópia de filesystem por suite. Testes específicos confirmam:

* quatro suites concorrentes recebem workspaces distintos;
* falha de uma suite não corrompe as demais;
* os artefatos canônicos permanecem inalterados;
* resultados semânticos permanecem equivalentes ao modo sequencial.

## Race Condition Investigation

Na execução paralela observada na Etapa 25, a execução compartilhava o mesmo checkout entre processos. A implementação anterior do harness não criava workspace por suite e também parava no primeiro erro. Isso permitia concorrência sobre caches, arquivos temporários e materialização indireta dos testes.

A investigação foi reproduzida estruturalmente com suites que escrevem o mesmo nome de arquivo relativo. No modo isolado, cada suite escreveu em seu próprio workspace e não houve colisão. A correção foi aplicada no boundary do harness, não nos componentes semânticos.

Validação final da condição:

```text
SEQUENTIAL: suites isoladas, sem corrupção
PARALLEL: suites isoladas, sem corrupção
```

A condição de corrida foi **RESOLVIDA** por isolamento de processo/filesystem. O modo compartilhado permanece disponível somente como diagnóstico e não é considerado execução segura.

## Cleanup

Cada execução usa `TemporaryDirectory`; workspaces são removidos ao final, inclusive após falha normal. Interrupções de processo continuam sendo propagadas e não são reportadas como execução completa.

Falhas de cleanup do sistema operacional não são convertidas silenciosamente em sucesso; permanecem responsabilidade do ambiente de execução.

## Failure Handling

* exit code diferente de zero gera `FAIL`, exceto quando a saída identifica bloqueio explícito, que gera `BLOCKED`;
* warnings de suites são preservados;
* suites independentes continuam após uma falha;
* erros de subprocesso são registrados em `errors`;
* o relatório agregado não assume sucesso quando há falhas;
* status `BLOCKED` não é convertido em `FAIL` nem em `PASS` silencioso.

## Regression Baseline

| Validação | Baseline |
|---|---:|
| Stage 24 | 20/20 PASS |
| Stage 25 | 26/26 PASS |
| Full regression anterior | 362/362 PASS |
| Reference Harness | 8/8 suites |
| Synthetic | 81 PASS, 1 warning |
| Semantic Calibration | 20/20 PASS |
| Adversarial | 29 PASS, 4 warnings, 1 BLOCKED esperado |
| Stage 30.1 | 6/6 PASS |

## Testes

`tests/test_stage_26_reference_harness.py` valida:

* inicialização e contrato estruturado;
* descoberta e execução das suites;
* PASS, PASS_WITH_WARNINGS, FAIL e BLOCKED;
* isolamento de fixtures e filesystem;
* determinismo e repetição;
* permutações de ordem;
* execução paralela;
* isolamento de falhas;
* preservação de artefatos canônicos;
* propagação de erros de subprocesso;
* cleanup por workspace temporário;
* independência do v1, senioridade, hiring e Job Context por meio das suites existentes.

## Resultados

Resultados observados:

* Stage 26: `15/15 PASS`;
* suíte completa: `369/369 PASS`;
* Reference Harness sequencial: `8/8 suites`, `PASS_WITH_WARNINGS`;
* Reference Harness paralelo: `8/8 suites`, `PASS_WITH_WARNINGS`;
* Reference Runtime: `369/369 PASS`;
* Synthetic: `81 PASS`, `1 PASS_WITH_WARNING`, `0 FAIL`;
* Semantic Calibration: `20/20 casos lógicos PASS`, `0 FAIL`;
* Adversarial: `29 PASS`, `4 PASS_WITH_WARNING`, `1 BLOCKED esperado`, `0 FAIL`;
* Stage 30.1: `6/6 PASS`;
* projeção semântica sequencial/paralela: equivalente;
* cenário concorrente isolado repetido: `20/20 PASS`.

Os warnings observados são os estados esperados das suites Synthetic, Calibration e Adversarial.

## Limitações

* O harness não transforma scripts legados em APIs internas; executa seus comandos existentes.
* O modo paralelo depende da capacidade do ambiente de criar processos Python e diretórios temporários.
* Suites que deliberadamente exibem `BLOCKED` como cenário esperado continuam apresentando warnings no relatório.
* Uma tentativa de executar vinte ciclos completos do harness paralelo excedeu o limite operacional por custo de copiar oito workspaces e executar a suíte integral em cada ciclo; ela foi interrompida sem alteração do repositório. A evidência repetida de concorrência foi obtida no cenário isolado equivalente (`20/20 PASS`), além da execução completa sequencial/paralela.
* O harness não é runtime de produção.

## Gate

```text
REFERENCE_RUNTIME_HARNESS_COMPLETE_WITH_WARNINGS
```
