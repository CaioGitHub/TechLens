# Plano de implementação — correção fiel da transcrição

Data: 2026-10-23. Branch: `codex/transcription-baseline`.

## Objetivo confirmado pelo usuário

Receber o texto transcrito por uma plataforma, corrigir possíveis erros de reconhecimento e encaminhar uma versão auditável à análise da entrevista, preservando o que o candidato efetivamente disse. Não corrigir conhecimento técnico incorreto, completar frases, converter hipótese em experiência ou remover negação/incerteza.

Áudio para texto não é o primeiro escopo. O agente de análise serve como referência contextual para sugerir termos, não como autorização para melhorar respostas.

## Base verificada

Checkpoint `9ae7781`: 530 testes globais e 15 do harness aprovados. A recuperação da regressão e a reescrita autorizada de dois oracles históricos estão documentadas em `TRANSCRIPTION_BASELINE_CORRECTIONS.md`. Os bloqueios históricos de validação semântica continuam preservados.

## Etapas testáveis

| Etapa | Entrega | Critério de aceite |
| --- | --- | --- |
| 1. Proposta e proteção de significado | Plano de correções com original, intervalos, termos sugeridos, suporte contextual e IDs de fonte | Propostas não alteram a resposta; números, negações, modalidades e afirmações de experiência protegidos; mudanças lexicais exigem revisão explícita |
| 2. Aplicação revisada e integração | Aplicação apenas de sugestões aceitas, ligada à reconstrução 20.5 | A versão avaliada é exatamente a versão revisada; original e histórico de alterações preservados; sugestões pendentes interrompem o encaminhamento por esta nova entrada |
| 3. Entrada genérica de entrevistas | Participantes configuráveis e importação sem nomes fixos de um piloto | Fonte e timestamps preservados; participantes desconhecidos não são inferidos arbitrariamente; nomes dos pilotos não aparecem na configuração genérica |
| 4. Propostas contextualizadas pelo agente | Uso controlado do glossário técnico/contexto para localizar possíveis erros de transcrição | A sugestão mostra a origem contextual; ausência de apoio vira revisão, não invenção; erro técnico do candidato não é transformado em resposta correta |
| 5. Revisão e exportação | Comparação original/proposto/revisado e exportação rastreável | O revisor vê cada mudança; conteúdo original permanece recuperável; arquivo existente não é sobrescrito silenciosamente |
| 6. Validação com entrevistas distintas | Testes de fidelidade, invariância e integração | Mesma fala sem alterações de conteúdo mantém evidência; alterações de significado são bloqueadas ou explicitamente revisadas; regressão e harness aprovados no mesmo checkpoint |

## Regras operacionais

- Uma etapa por vez, com testes de reprodução antes da mudança e regressão antes de avançar.
- Glossário e contexto podem fundamentar propostas, mas não provam sozinhos que a plataforma errou. Correções lexicais devem aguardar conferência explícita da fonte pelo revisor.
- A primeira implementação usa propostas determinísticas de aliases próximos e auditáveis. Ela não é apresentada como um corretor semântico geral ou um modelo de reconhecimento de fala.
- O caminho histórico `reconstructions` existe para compatibilidade dos fixtures. A nova entrada deve passar por validação própria e não misturar substituições históricas com planos revisados.
- Não alterar pesos, scores, rubricas ou oracles para acomodar a correção da transcrição.
- Cada checkpoint deve registrar resultado real, limitações e diferença entre fidelidade textual e correção técnica.

## Casos mínimos

“Spring Boto” pode gerar proposta de “Spring Boot” se houver referência contextual, preservando ambos até revisão. “Eu usaria o Application...” não pode virar uma frase completa. “Não usei”, “talvez”, “eu tentaria”, números e versões não podem desaparecer. Uma afirmação tecnicamente errada continua errada na transcrição se isso foi o que o candidato disse.

Próximo trabalho autorizado: implementar e verificar as etapas 1 e 2 com testes, mantendo os limites acima explícitos.


## Atualização de execução — 2026-10-23

Etapas 1 e 2 implementadas no escopo conservador documentado em [[TRANSCRIPTION_CORRECTION_FIDELITY]]. A aplicação exige revisão explícita das propostas lexicais e confirmação de fonte; não é uma prova automática de equivalência semântica. Há 19 novos métodos de teste, integração à reconstrução e regressão final registrada. Entrada genérica, UI, base técnica automática e propostas semânticas amplas permanecem etapas futuras, sem promoção automática de seus critérios.


## Piloto de referência real — 2026-10-23

Ver [[TRANSCRIPTION_REFERENCE_SET_PLAN]] e `TRANSCRIPTION_REFERENCE_SET_MANIFEST.json`: oito trechos localizados, três arquivos de uma entrevista, duas versões de conteúdo, zero referências humanas validadas. Critérios de aceite e procedimento incremental registrados. Revisão fundamentada desta entrevista pendente; outra entrevista distinta necessária para ampliar generalização. Runtime e gates históricos inalterados.


## Incerteza de transcrição — checkpoint de implementação

Ver [[TRANSCRIPTION_UNCERTAINTY]] e `TRANSCRIPTION_UNCERTAINTY_RESULTS.json`. Marcações ligadas à fonte propagadas até evidências, relatório e quatro exportações. Perguntas afetadas adiadas sem nota; texto original preservado; coordenação impede avanço como avaliação integral. 14 novos testes; 37 direcionados, 567 globais e 15 do harness aprovados. Na entrevista real, as duas perguntas afetadas ficam adiadas. Limite: nova entrada do runtime, sem proteção retroativa do importador de arquivos históricos. UI e generalização com outra entrevista continuam pendentes; bloqueios semânticos históricos preservados.


## Incerteza de transcrição — checkpoint de implementação

Ver [[TRANSCRIPTION_UNCERTAINTY]] e `TRANSCRIPTION_UNCERTAINTY_RESULTS.json`. Marcações ligadas à fonte propagadas até evidências, relatório e quatro exportações. Perguntas afetadas adiadas sem nota; texto original preservado; coordenação impede avanço como avaliação integral. 15 novos testes; 38 direcionados, 568 globais e 15 do harness aprovados. Na entrevista real, uma pergunta identificada e uma resposta sem vínculo confiável ficam adiadas, sem contaminar outras respostas com marcador `unknown`. Limite: nova entrada do runtime, sem proteção retroativa do importador de arquivos históricos. UI e generalização com outra entrevista continuam pendentes; bloqueios semânticos históricos preservados.


## Proteção do importador histórico — 2026-10-25

Ver [[TRANSCRIPTION_IMPORT_GUARD]] e `TRANSCRIPTION_IMPORT_GUARD_RESULTS.json`. Importação, carregadores individuais e geração direta verificam incerteza declarada; coordenação bloqueia antes de consolidar ou gravar. Revisão auxiliar opcional vinculada por hashes, conflitos e metadados inválidos bloqueados, reutilização antiga revalidada. 22 novos testes; 80 direcionados, 590 globais e 15 do harness aprovados. Ausência de marcação não prova fidelidade; revisão externa deve ser fornecida explicitamente. Entrada genérica e UI de revisão seguem pendentes. Bloqueios semânticos históricos preservados; este adendo é o estado atual e sucede os limites do checkpoint anterior quanto ao importador.


## Entrada genérica e responsabilidade da IA — 2026-10-25

Ver [[TRANSCRIPTION_GENERIC_INPUT]], `TRANSCRIPTION_GENERIC_INPUT_RESULTS.json` e [[TRANSCRIPTION_AI_ANALYSIS_CONTRACT]]. Entrada por turnos e participantes configuráveis implementada, com preservação de texto/IDs/timestamps, distinção entre entrevistadores e ambiguidade explícita. Dez testes novos; 70 direcionados, 600 globais e 15 do harness aprovados. Diretriz: IA analisa a entrevista inteira e prepara propostas e exceções; humano revisa decisões que exigem comprovação de fonte, sem reanalisar todos os turnos. Integração com modelo, importadores de arquivos e UI ainda pendentes; próxima etapa é o adaptador de IA com validação de saída. Nenhuma promessa de percentual de automação ou homologação semântica. Gates históricos preservados.


## Fluxo esclarecido: agente do usuário consulta o projeto — 2026-10-25

Diretriz vigente em [[TRANSCRIPTION_AGENT_WORKFLOW]]: a transcrição é enviada como prompt ao agente já utilizado pelo usuário, e este projeto fornece método, critérios e conhecimento. A IA realiza a análise completa; a intervenção humana fica nas exceções justificadas, sem revisão obrigatória de todos os turnos. Não há necessidade de conectar modelos, APIs ou agentes dentro do projeto para esse uso. README, START_HERE e AGENTS apontam para o roteiro.

O experimento não publicado de adaptadores/conectores foi preservado localmente e retirado da entrega. Código permanece no checkpoint publicado `fcfefc4`, com a entrada genérica e as proteções existentes. Os testes desse experimento não devem ser usados como resultado da entrega atual. Próxima validação: executar o roteiro com uma transcrição por um agente que tenha acesso às fontes e auditar a saída; outra entrevista distinta continua necessária para generalização. Gates históricos permanecem preservados.


## Primeira validação diagnóstica do roteiro — 2026-10-25

Resultados em `11 - Interview Evaluation/09 - Synthetic Validation/Agent Workflow 2026-10-25/RESULTS.md`. Três casos fictícios e 20 turnos analisados pelo agente usando a base como método; entradas e 15 expectativas fixadas antes dos relatórios. 30 verificações estruturais aprovadas e dois controles negativos detectados. Uma justificativa de Q1 foi revisada para evitar contaminação por outra pergunta, preservando a versão inicial. Não houve alteração do runtime, critérios ou fontes históricas.

Execução não cega e não independente: o mesmo agente criou casos, conheceu expectativas, analisou e revisou as saídas. Não é prova de acurácia ou homologação semântica. O caso ambíguo ficou parcial e sua segunda pergunta é informativa, deixando pendente um controle adicional de nota técnica não afetada. Ainda faltam avaliação independente e entrevista distinta; gates históricos permanecem preservados. Não foram executados testes de regressão do runtime nesta rodada de documentação e artefatos.


## Revisão controlada de fidelidade do relatório real — 2026-10-25

Ver `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-01/Agent Report Review 2026-10-25/REVIEW.md`. O usuário reconfirmou F01; quatro avaliações e justificativas permaneceram intactas, com notas 0/4/8/4 e média descritiva 4,0. O uso qualitativo de 07:22 como E07 foi retirado; Q9/R9 permanece adiada e o relatório/MOC identificam análise parcial. Fonte preservada e versão inicial arquivada. Regra do guia ampliada: fonte irrecuperável não sustenta conclusão favorável nem desfavorável, mesmo sem nota. Oito testes de política e doze verificações da revisão aprovados. Auditor de dependências explícitas, com classificação manual; não valida automaticamente toda a semântica da prosa nem a calibração das notas. Sem alteração do runtime, da rubrica ou dos gates históricos.
