# Incerteza de transcrição ligada à avaliação

Data: 2026-10-23. Estado limitado: `TRANSCRIPTION_UNCERTAINTY_DEFERRAL_VERIFIED`.

## Comportamento implementado

A nova entrada opcional `transcription_uncertainties` recebe registros com `id`, `segment_id`, `original_sha256` (SHA-256 do texto UTF-8 exato do segmento), `status: unresolved`, `reason` e `reviewer`. A declaração de revisor é metadado do chamador, não autenticação ou prova de consulta de áudio. IDs repetidos, fonte inexistente, texto alterado, campos vazios e status incompatível são rejeitados. Não há detecção automática de erros nem inferência de substituição.

O original permanece preservado. Uma marcação na pergunta ou em qualquer turno de uma resposta adia conservadoramente a avaliação da pergunta inteira, inclusive respostas agrupadas. Para resposta sem pergunta identificada, adia somente aquela resposta: o marcador compartilhado `unknown` não é tratado como identidade de pergunta. Não atribui zero e não tenta avaliar o restante da mesma resposta isoladamente. As outras perguntas e respostas sem vínculo continuam no fluxo. Reconstruções que alterariam o texto de uma resposta afetada são rejeitadas enquanto a incerteza estiver aberta.

Os registros seguem nos segmentos, nas respostas reconstruídas e perguntas afetadas, na validação, no conjunto de evidências como metadados separados, no relatório e nas quatro exportações do piloto. O ledger `evaluation_deferrals` contém pergunta, respostas, IDs de revisão e segmentos, motivo e `score: null`. Ele fica separado da lista de avaliações numéricas. Texto marcado não gera evidência de desempenho nem sustenta contradição contra outras respostas.

A apresentação indica `assessment_complete: false`. A coordenação estruturada mantém `ready_for_next_stage: false`; perguntas adiadas não podem ser confundidas com uma avaliação integral concluída. Resultados anteriores com o mesmo identificador não são reutilizados quando houver marcação atual ou anterior, evitando ocultar uma revisão recém-informada.

## Validação

Foram escritos contratos antes dos ajustes, reproduzindo ausência de adiamento e de rastreabilidade. Um segundo grupo reproduziu exportação sem aviso e reutilização indevida de resultado anterior; ambos foram corrigidos antes da regressão final.

- 15 novos métodos de teste, incluindo a entrevista real e suas duas passagens irrecuperáveis.
- 38 testes direcionados aprovados (15 de incerteza, 19 de fidelidade e quatro de preservação).
- Regressão: 568/568 aprovados; harness: 15/15, sem falhas, erros ou skips.
- Na entrevista real, uma pergunta identificada e uma resposta sem vínculo confiável foram adiadas, com textos preservados; as quatro exportações incluem os registros e a incompletude. Um teste adicional reproduziu e corrigiu agrupamento indevido de respostas que compartilham o marcador `unknown`.
- Resultados e hashes em `TRANSCRIPTION_UNCERTAINTY_RESULTS.json`.

Não foram alteradas fórmulas, pesos, expectativas históricas ou conteúdo do candidato. A confirmação humana de seis trechos e a identificação dos dois erros permanecem em `TRANSCRIPTION_PILOT_USER_REVIEW.json`. Não é uma nova homologação dos bloqueios semânticos históricos.

## Limites e continuidade

A proteção depende de marcação explícita e válida na entrada de texto estruturada/bruta que passa pelo runtime. Não foi estendida retroativamente ao caminho `PilotPaths` que importa arquivos históricos já avaliados, nem a consumidores externos que descartem os metadados. Esses arquivos não devem ser usados para contornar o adiamento. A interface de revisão continua pendente.

Não há correção recuperada para os dois trechos, nem validação semântica independente. A regra conservadora adia a pergunta toda; liberar parcialmente uma resposta exigirá escopo e testes próprios. Não calcular uma conclusão global usando apenas as notas restantes como se a entrevista estivesse completa.

Próximos incrementos: entrada genérica de participantes e fontes, apresentação de revisão com estado de incerteza visível e uma entrevista distinta para avaliar generalização. Resolver uma marcação futuramente exigirá fonte e histórico de revisão explícitos; não basta renomear seu status como resolvido nesta entrada.
