# Stage 31.2 — Controlled Correction

## Baseline

Antes da correção, a reprodução dos seis casos FRA confirmou:

| ID | Question | Root Cause | Stage | Baseline |
|---|---|---|---|---|
| FRA-001 | Q1 | fallback conceptual positivo e correctness default Strong | 21 → 23 | score 6.0 |
| FRA-002 | Q3 | fallback positivo para resposta fragmentada | 21 → 23 | score 6.0 |
| FRA-003 | Q5 | ausência de pertinência REST versus Kafka/Rabbit | 21 → 23 | score 7.05 |
| FRA-004 | Q6 | query genérica promovida para evidência suficiente de JDBC | 21 → 23 | score 7.05 |
| FRA-005 | Q9 | declaração de ferramenta não reconhecida | 21 → 23 | score 7.05 |
| FRA-006 | Q11 | uso de Copilot e marcador conversacional promovidos a raciocínio | 21 → 23 | score 7.65 |

## Root Causes

O primeiro artefato semanticamente incorreto era o Evidence Set do Stage 21, onde respostas curtas, declarativas ou fora do domínio recebiam fallback `conceptual/positive`. O Stage 23 agravava o problema ao interpretar a ausência de sinais negativos como `correctness: Strong` e ao aceitar heurísticas de raciocínio sem demonstração suficiente.

Não houve defeito de speaker attribution, linking ou reconstruction. A cadeia de origem é `21 Evidence Model blind qualification → 23 dimensional evaluation`.

## Correção aplicada

A correção mínima e generalizável foi aplicada em `reference_runtime/runtime.py`:

- detectar declarações linguísticas adicionais sem promovê-las a `demonstrated_experience`;
- reconhecer conteúdo de ferramenta como declaração quando não há demonstração concreta;
- classificar respostas curtas e sinais explícitos de insuficiência como `conceptual/insufficient`;
- detectar incompatibilidade de domínio REST versus Kafka/Rabbit como `off_topic`, preservando a validade técnica da mensageria como conteúdo parcial;
- impedir que declarações, evidência insuficiente, conteúdo parcial ou off-topic recebam `correctness: Strong` por default;
- evitar que marcadores de reasoning em declarações gerem `reasoning: Strong`;
- exigir suporte específico para promover consultas a evidência prática de JDBC;
- preservar resposta correta, resposta parcialmente correta, hipótese, declaração e experiência demonstrada como casos distintos.

Nenhuma regra depende de Q1, Q3, Q5, Q6, Q9 ou Q11. Rubric, Question Taxonomy, schemas canônicos, avaliações humanas e relatórios históricos permaneceram inalterados.

## Primeiro estágio afetado

O primeiro estágio afetado é o Stage 21. O Stage 23 foi ajustado porque também convertia a qualificação insuficiente/parcial em dimensões excessivamente fortes. A correção não foi deslocada para Stage 23.1/23.2, pois o defeito nasce antes da agregação global.

## Q5

Pergunta: diferença entre producer/consumer em uma API REST.

Resposta reconstruída: explicação de producer/consumer em Kafka, Rabbit, fila e tópico.

Resultado pós-correção:

- Evidence Set: `off_topic/negative` e `conceptual/partial`;
- `correctness`: `Insufficient`;
- `completeness`: `Partial`;
- `reasoning`: `Weak`;
- score: `4.45`;
- confidence: `medium`.

A correção não afirma que Kafka/Rabbit está tecnicamente errado. Ela impede que conhecimento válido de mensageria seja transferido para REST.

## FRA-001 → FRA-006

| ID | Antes | Depois | Mudança principal |
|---|---:|---:|---|
| FRA-001 / Q1 | 6.0 | 4.0 | declaração curta → evidência insuficiente |
| FRA-002 / Q3 | 6.0 | 4.0 | fragmentos → não promovidos a correção forte |
| FRA-003 / Q5 | 7.05 | 4.45 | REST/Mensageria → off-topic + parcial |
| FRA-004 / Q6 | 7.05 | 5.85 | resposta direcional → correção parcial |
| FRA-005 / Q9 | 7.05 | 4.0 | nome de ferramenta → declaração |
| FRA-006 / Q11 | 7.65 | 4.0 | uso de Copilot → declaração sem reasoning forte |

## Testes da correção

Foram adicionados testes para:

- Q5 REST versus Kafka/Rabbit;
- resposta REST correta;
- resposta REST parcial;
- declaração versus experiência demonstrada;
- hipótese sem experiência demonstrada;
- mutação off-topic versus resposta correta;
- jargão sem evidência;
- isolamento de contexto e idempotência.

## Mutation Tests

As mutações demonstram que trocar uma resposta REST correta por mensageria altera a avaliação, trocar mensageria por REST melhora a avaliação e adicionar jargão sem evidência não aumenta artificialmente o score.

## Invariance Tests

CV, cargo, senioridade, contexto da vaga, histórico, score esperado e score humano não são lidos como evidência pela avaliação pós-correção. Execuções repetidas produziram artefatos idênticos.

## Regression

Resultados finais:

- Stage 31.2: `9/9 PASS`;
- Stage 31 e testes relacionados: `25/25 PASS`;
- Stage 30, 30.1, 30.2 e 30.2.1: `55/55 PASS`;
- Stage 27: `READY_WITH_WARNINGS`;
- Stage 28: `21/21 PASS`;
- Stage 29: `29 PASS`, `4 PASS_WITH_WARNING`, `1 BLOCKED` esperado, `0 FAIL`;
- regressão completa: `503/503 PASS`;
- Reference Harness: `8/8 suites`, `PASS_WITH_WARNINGS`, `0 failed`.

## Stage 31 pós-correção

O resultado pós-correção foi persistido separadamente em `Stage 31.2 — Human vs System Post-Correction.md`. O relatório histórico do Stage 31 permanece com `HUMAN_VS_SYSTEM_BLOCKED`.

## Human vs System pós-correção

Média humana: `5.09`.

Média do sistema pós-correção: `5.55`.

Diferença média absoluta: `0.64`, reduzida de `2.01`.

A comparação não foi usada para ajustar pesos ou scores.

## Divergências restantes

Q5 permanece a maior divergência, mas sua causa é semanticamente explicada e não é uma transferência indevida de conhecimento. Q10 permanece como divergência residual a investigar em etapa posterior se necessário; não há evidência de que seja causada pelo fallback corrigido.

## Efeitos colaterais

A correção alterou as avaliações do piloto real e aumentou a quantidade de evidências explícitas para representar qualificações parciais/off-topic. Não houve perda de source traceability, speaker attribution, linking ou reconstruction.

## Limitações

- A avaliação humana original continua sendo uma única revisão independente.
- Q5 contém ruído de transcrição, embora contenha referência explícita a REST.
- A correção é heurística do runtime de referência e deve ser validada contra novos exemplos equivalentes.

## Decisão

A causa-raiz foi reproduzida e corrigida de forma controlada. O comportamento semântico melhorou, Q5 deixou de receber `correctness: Strong` por fallback e a comparação independente melhorou sem calibração pelo score humano.

## Gate

`CONTROLLED_CORRECTION_COMPLETE_WITH_WARNINGS`
