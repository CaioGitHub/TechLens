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
