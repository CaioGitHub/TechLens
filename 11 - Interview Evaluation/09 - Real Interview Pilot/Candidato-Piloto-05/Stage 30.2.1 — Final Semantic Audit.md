# Stage 30.2.1 — Final Semantic Audit

## Objetivo

Auditar semanticamente o piloto real completo, do transcript original à avaliação consolidada, verificando fidelidade, rastreabilidade, proporcionalidade e independência de informações externas.

## Escopo

Foram auditadas as camadas de participantes, speakers, perguntas, respostas, reconstruções, linking, validação, evidências, avaliações individuais, Evaluation Engine, avaliação global e revisão humana.

## Fonte de verdade

`Transcript Original.md` permaneceu a fonte primária do conteúdo verbal. O transcript original não foi alterado.

## Artefatos auditados

- `After Correction - Entrevista Estruturada.md`
- `After Correction - Evidence Set.md`
- `After Correction - Individual Evaluations.md`
- `After Correction - Interview Evaluation v2.md`
- `Stage 30 — After Correction.md`
- `Stage 30.1 — Pilot Failure Analysis.md`
- `Stage 30.2 — Human Review & Structured Interview Approval.md`

## Resultados da auditoria

### Estrutura e speakers

- 4 participantes identificados: 1 candidato, 2 entrevistadores e 1 observador.
- 11 perguntas avaliáveis e 5 perguntas do candidato preservadas fora da avaliação.
- 47 respostas preservadas com segmentos `RP05-*`.
- Não foi encontrada atribuição crítica incorreta de fala do candidato.

### Stage 30.1

`E tem uma Daily também, só nossa, né?` permanece fora das perguntas avaliáveis, evidências e avaliações. Perguntas técnicas reais com estrutura interrogativa semelhante continuam reconhecidas, incluindo observabilidade e JDBC.

### P1-02

`R26` e `R43` permanecem `unknown/needs_review`. A auditoria não encontrou pergunta avaliável suficientemente identificável nem evidência técnica perdida do conjunto. Vincular por proximidade seria semanticamente menos seguro.

### Reconstruction

As 47 reconstruções preservam `original_text == reconstructed_text`. Não houve adição, remoção ou correção técnica silenciosa. Hipóteses, incertezas, autocorreções e erros não foram fortalecidos artificialmente.

### Evidence

As 22 evidências auditadas:

- estão presentes no texto das respostas correspondentes;
- apontam para respostas e perguntas existentes;
- possuem `source.segment_ids` válidos;
- não contêm conteúdo inventado ou fonte desconhecida.

### Individual Evaluations

As 11 avaliações possuem score entre 0 e 10, usam evidências vinculadas à mesma pergunta e resposta e são reconstruíveis a partir do Evidence Set. Não houve score injection, uso de CV, senioridade, vaga, histórico ou score esperado.

### Global Evaluation

O resultado pós-correção possui 11 avaliações, média `6,93` e mediana `7,05`. A conclusão global permanece limitada ao conteúdo efetivamente coberto e não produz decisão de contratação, senioridade ou aderência à vaga.

## Achados

| ID | Severidade | Área | Descrição | Impacto | Status |
|---|---|---|---|---|---|
| FSA-001 | P2 | Global materialization | O artefato global não materializa análise qualitativa detalhada por domínio, complexidade, strengths e gaps. | Limita a auditoria qualitativa global; não quebra rastreabilidade nem gera conclusão falsa. | ACCEPTED |
| FSA-002 | P2 | Evidence taxonomy | A taxonomia materializada não explicita separadamente experiência declarada e experiência demonstrada. | Reduz granularidade; não promove declaração de experiência a demonstração. | ACCEPTED |
| FSA-003 | INFO | Linking | Respostas contextuais como `R26` e `R43` permanecem `unknown/needs_review`. | Cobertura menor, sem evidência avaliável perdida demonstrada; decisão conservadora. | ACCEPTED |
| FSA-004 | INFO | Human comparison | Não houve segundo avaliador humano independente para comparação numérica. | Reduz confiança comparativa, sem invalidar a auditoria de origem e rastreabilidade. | ACCEPTED |

Nenhum P0 ou P1 foi encontrado nesta auditoria.

## Rastreabilidade

A cadeia foi validada:

`global traceability → evaluation → evidence → response → question → source.segment_ids → Transcript Original`

Todos os IDs de segmentos referenciados existem no transcript processado. Cada evidência utilizada por avaliação pode ser localizada no texto da resposta e no segmento original. Não foram encontrados órfãos.

## Contaminação externa

Testes controlados com alterações de CV/contexto representado no fixture, senioridade, título, empresa, histórico, `expected_scores` e `expected_evaluations` mantiveram a projeção técnica inalterada. Nenhuma dessas fontes foi utilizada como evidência.

## Mutation Testing

| Mutação | Resultado esperado | Resultado observado |
|---|---|---|
| Alteração de evidência técnica no transcript | Saída afetada | PASS |
| Alteração de resposta técnica | Evidência/avaliação afetadas | PASS |
| Alteração de CV/contexto externo | Saída inalterada | PASS |
| Alteração de senioridade | Saída inalterada | PASS |
| Alteração de job context | Saída inalterada | PASS |
| Alteração de relatório histórico | Saída inalterada | PASS |
| Alteração de score esperado/referência esperada | Saída inalterada | PASS |

## Invariâncias

Foram preservadas:

- exclusão de perguntas do candidato da avaliação;
- exclusão de respostas `unknown` do Evidence Model;
- ausência de evidência inventada;
- validade dos scores;
- determinismo para a mesma entrada;
- preservação do transcript original;
- ausência de alteração do Engine, Rubric ou Evidence Model.

## Human Review vs System Evaluation

Não foi exigida igualdade numérica entre revisão humana e Evaluation Engine. A revisão humana e a auditoria sistêmica concordam quanto à estrutura dos speakers, exclusão do prompt da Daily, linking conservador, rastreabilidade e limitações. As notas foram consideradas defensáveis pelas evidências, sem recalibração.

## Limitações

- O artefato global pós-correção não contém análise qualitativa detalhada por domínio, complexidade, strengths e gaps.
- A taxonomia final de evidências é coarse-grained e não separa explicitamente experiência declarada de experiência demonstrada.
- Respostas contextuais sem vínculo seguro permanecem `unknown/needs_review`.
- Não houve segundo avaliador humano independente.
- Áreas não cobertas pela entrevista não devem ser interpretadas como deficiência técnica.
- O gate é válido para este piloto e escopo, não para produção ou decisão de contratação.

## Conclusão

O pipeline processou o piloto real desde o transcript original até a avaliação técnica consolidada sem introduzir conteúdo inexistente, sem atribuir falas críticas ao participante errado, sem demonstrar perda material de evidência técnica, sem contaminação externa e mantendo rastreabilidade suficiente para explicar as avaliações.

A avaliação é semanticamente defensável e proporcional às evidências para o escopo deste piloto. As limitações de materialização global, granularidade da taxonomia e ausência de segundo avaliador permanecem explícitas e impedem interpretar o resultado como validação definitiva de produção ou como decisão sobre o candidato.

## Gate

`FINAL_SEMANTIC_AUDIT_COMPLETE_WITH_WARNINGS`
