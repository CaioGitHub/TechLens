# Recuperação da regressão da base de transcrição

Data: 2026-10-23. Branch: `codex/transcription-baseline`.

## Causas corrigidas

A baseline registrada em `TRANSCRIPTION_BASELINE_TEST_RESULTS.json` tinha cinco testes com falha. Três falhas de teste refletiam dois casos de calibração:

- CAL28-08: uma escolha explicitamente justificada não gerava evidência de reasoning. Foi acrescentado reconhecimento de relação gramatical entre escolha e justificativa, sem cadastrar nomes de tecnologias ou ajustar pesos/scores.
- CAL28-19: palavras de transição em início de frase, seguidas de um sujeito pessoal, eram interpretadas como entidades técnicas. A extração agora trata esse padrão conservadoramente; a detecção de assunto técnico explicitamente distinto foi mantida.

Quatro testes novos verificam exemplos independentes de escolha justificada, preferência sem justificativa, modificadores em início de frase e preservação da detecção de assunto distinto.

## Dois testes históricos reescritos com autorização explícita do usuário

As asserções antigas exigiam quantidade fixa de evidências, uma sequência fixa de scores e média/mediana de uma versão anterior. O runtime já incorporava correções semânticas posteriores, portanto esses snapshots não exprimiam mais a propriedade que os testes deveriam proteger.

Não foi substituída a média histórica pela média atual nem ajustado o runtime para atingir os números antigos. Os relatórios históricos e a medição inicial permaneceram intactos.

- A preservação do efeito da remoção de uma pergunta contextual agora é testada por controle contrafactual: executar a mesma versão com e sem a fala contextual e exigir perguntas, respostas, evidências e avaliações idênticas, sem uso do segmento removido como evidência.
- A proporcionalidade global agora é verificada pelo agregador existente em relação às avaliações atuais: média e mediana conferidas independentemente por statistics, mínimo, máximo e distribuição consistentes. A verificação de determinismo foi preservada.

Essa mudança de oracle comportamental deve permanecer explícita na revisão; não se está afirmando que os testes numéricos originais passaram sem alteração.

## Validação em etapas

1. Regressores novos foram executados antes das correções e reproduziram os defeitos.
2. Após a primeira correção, dois testes direcionados aprovados antes do grupo seguinte.
3. Correções de calibração e novas regressões: 48 testes aprovados.
4. Testes históricos reescritos, calibração e regressões: 66 testes aprovados.
5. Regressão completa: **530 testes aprovados**, zero falhas, zero erros, zero ignorados; 19,849 s.
6. Reference Harness isolado: **15/15 aprovados**, zero falhas ou erros; 21,308 s.

Saídas completas e hashes estão em `TRANSCRIPTION_BASELINE_CORRECTIONS_RESULTS.json`. O hash do runtime permaneceu estável durante as execuções finais. O marco inicial e sua tag não foram reescritos.

## Estado e continuidade

`TRANSCRIPTION_BASELINE_REGRESSION_RECOVERED`.

Este estado significa recuperação da regressão automatizada desta branch. Não substitui os gates históricos de validação semântica, não comprova independência de avaliação e não declara produção pronta. O processamento existente usa texto já transcrito; áudio para texto requer um escopo e uma etapa próprios.

Próximo trabalho: plano incremental de transcrição, reutilizando as etapas 20.1–20.7 e preservando fonte, participantes, timestamps, ambiguidades e vínculos de evidência. Implementações posteriores devem manter testes entre grupos, correção de falhas inesperadas antes de avançar e checkpoints separados.
