# Stage 30 ? Real Interview Pilot

## 1. Identifica??o do piloto

- Identificador controlado: `Candidato-Piloto-05`
- Fonte hist?rica somente leitura: `Candidato-Piloto-01/Pilot Input - Source Transcript v3.md`
- Fonte derivada preservada em: `Transcript Original.md`
- N?o foram fornecidos perguntas, respostas, evid?ncias, scores ou specs esperados ao runtime.

## 2. Fonte utilizada

- Transcript bruto completo, cobertura aproximada de 00:03?20:01.
- Segmentos processados: 164.
- A c?pia original n?o foi alterada durante o processamento.

## 3. Participantes

- Candidate: `P-05-CANDIDATE`
- Interviewer: `P-05-INTERVIEWER-1`
- Interviewer: `P-05-INTERVIEWER-2`
- Observer: `P-05-OBSERVER`

## 4. Resultado da Transcription Processing

- 20.1: identifica??o conclu?da; 4 participantes.
- 20.2: atribui??o conclu?da para os speakers conhecidos.
- 20.3: 12 perguntas extra?das; 5 perguntas do candidato preservadas fora da avalia??o.
- 20.4: 47 respostas extra?das.
- 20.5: reconstru??es preservaram os segmentos de origem; nenhuma conclus?o t?cnica foi adicionada.
- 20.6: links gerados; respostas sem v?nculo seguro permaneceram revis?veis.
- 20.7: `READY_WITH_WARNINGS`.

Warnings:

- candidate questions preserved outside evaluation questions
- conversational prompts require classification review
- response extraction requires review
- responses without a confident question link require review

## 5. Evidence Model

- Evid?ncias derivadas: 23.
- Cada evid?ncia avaliada possui `response_id`, `question_id` e `source.segment_ids`.
- N?o foram usados curr?culo, cargo, senioridade ou contexto externo.

## 6. Individual Evaluations

- Avalia??es produzidas: 12.
- Scores foram calculados pelo runtime a partir das evid?ncias derivadas.
- N?o foram fornecidos scores esperados ou avalia??es manuais ao executor.

## 7. Global Evaluation

- Stage 23.1: `READY_WITH_WARNINGS`; gate exposto pelo boundary do pipeline.
- Stage 23.2: `READY_WITH_WARNINGS`; artefato derivado materializado sem usar o relat?rio hist?rico v1 como fonte.
- Nenhuma conclus?o de contrata??o, aprova??o, reprova??o ou senioridade foi produzida.

## 8. Human Review

Revis?o estruturada registrada em `Human Review.md`. N?o houve segundo avaliador humano independente dispon?vel nesta execu??o; essa limita??o permanece expl?cita.

## 9. Diverg?ncias

- Diverg?ncia relevante: prompts conversacionais foram inclu?dos pelo executor como perguntas avali?veis em alguns pontos.
- Diverg?ncia relevante: o v?nculo de algumas respostas contextuais permanece `unknown`/`needs_review`, reduzindo a cobertura.
- N?o foi observada diverg?ncia cr?tica de origem, evid?ncia inventada ou uso de metadata proibida.

## 10. Achados

- `HR-001` ? P1 ? Stage 20.3: classifica??o de prompt conversacional como pergunta avali?vel.
- `HR-002` ? P1 ? Stage 20.6: respostas contextuais sem v?nculo expl?cito permanecem fora de avalia??o, mas exigem revis?o.
- `HR-003` ? P2 ? Stage 20.5: normaliza??o de ru?do t?cnico depende de evid?ncia local e deve permanecer conservadora.
- `HR-004` ? INFO ? revis?o humana independente adicional n?o dispon?vel.

## 11. Problemas P0

`0` ? nenhum problema de integridade cr?tica encontrado.

## 12. Problemas P1

`2` ? HR-001 e HR-002. N?o corrigidos silenciosamente.

## 13. Problemas P2

`1` ? HR-003.

## 14. Traceability

A cadeia validada foi:

`evaluation -> evidence -> response -> question -> source.segment_ids`

N?o foram encontrados IDs de evid?ncia ?rf?os entre as avalia??es produzidas.

## 15. Reproducibility

`PASS` ? duas execu??es sobre o mesmo transcript produziram perguntas, respostas, evid?ncias, avalia??es e warnings equivalentes.

## 16. Idempotency

`PASS` ? o processamento n?o duplicou IDs ou conte?do e n?o alterou a fonte original.

## 17. Limitations

- O runtime sint?tico/can?nico ainda possui contratos distintos para materializa??o final de fixtures raw e arquivos Markdown do piloto.
- A extra??o autom?tica trata alguns prompts conversacionais como perguntas avali?veis.
- A revis?o independente por um segundo humano n?o foi realizada.
- A avalia??o cobre somente o conte?do verbal efetivamente identificado no transcript.

## 18. Conclus?o

O sistema conseguiu processar o transcript real sem fornecer estruturas esperadas manualmente, preservar a origem das evid?ncias e produzir uma avalia??o rastre?vel. O resultado ? interpret?vel, mas requer corre??es futuras nos achados P1 antes de ser considerado sem warnings.

## 19. Gate

`REAL_INTERVIEW_PILOT_COMPLETE_WITH_WARNINGS`
