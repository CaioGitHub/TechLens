# Revisão controlada do relatório de Ingrid — 2026-10-25

Estado limitado: `CONTROLLED_REVIEW_VERIFIED`.

## Decisões e alteração

O usuário reconfirmou diretamente a formulação de F01: produces e consumes em API REST. Essa confirmação esclarece a pergunta; não afirma acesso ao áudio pelo agente nem o que a candidata efetivamente ouviu. As quatro avaliações e suas justificativas foram preservadas integralmente: notas 0, 4, 8 e 4, média descritiva desse subconjunto 4,0. Não houve reavaliação para atingir uma nota-alvo.

A resposta integral de 07:22 foi considerada irrecuperável com base na revisão anterior do usuário. A versão inicial limitava a dúvida principalmente aos nomes e usava E07 para uma conclusão não pontuada sobre conhecimento em Azure/observabilidade. Esse uso foi retirado. Q9/R9 permanece adiada para qualquer julgamento sobre conhecimento, experiência ou desempenho; o original não foi reconstruído e o usuário não precisa fornecer novamente uma fonte já declarada indisponível.

O relatório agora se apresenta como análise parcial e o MOC reflete isso. A média das quatro respostas é estatística de um subconjunto, não uma avaliação completa da entrevista. A versão recebida do outro agente está preservada em `Relatório-Ingrid Mazoni.before-review.md`, com hash em `review_decisions.json`. O arquivo da transcrição recebida não foi alterado.

## Regra de regressão do método

Uma fonte comprometida como um todo não pode fundamentar conclusão favorável ou desfavorável sobre a candidata, mesmo sem nota. A regra foi explicitada no passo 5 de `TRANSCRIPTION_AGENT_WORKFLOW.md`.

O caso `regression_case.json` reproduz o uso qualitativo anterior de E07; `before_audit.json` registra a rejeição desse uso. O estado atual de dependências está em `verification_results.json`. Citações do original e explicações de adiamento são permitidas como registros de fonte/status, sem transformá-las em avaliação da pessoa.

## Verificação executada

- Oito testes da política aprovados: conclusões negativas, positivas e de experiência sem nota são bloqueadas; misturar fonte utilizável com uma irrecuperável não libera o julgamento; zero não substitui adiamento; registro literal, estado de adiamento e avaliações sustentadas por outras fontes permanecem permitidos.
- Doze verificações da revisão aprovadas, incluindo preservação da fonte e da versão inicial, igualdade integral das quatro seções de pontuação, manutenção da média, retirada de E07 e tratamento explícito de Q9/R9.
- Revisão manual de U01–U08 registrada. Não foi identificado outro uso indevido equivalente no escopo revisto; isso não é prova de ausência de todos os erros semânticos.

Para repetir as verificações, executar `verify_review.py` nesta pasta. Não foram alterados runtime ou rubrica; a regressão completa do runtime não foi executada nesta revisão documental. Os números de testes históricos mencionados no relatório não são resultados novos.

## Limites

O auditor verifica dependências explicitamente classificadas por um revisor. Ele não extrai nem compreende automaticamente todas as afirmações da prosa; rótulos de escopo incorretos podem escapar sem leitura humana/agente. Não há validação independente das notas, calibração estatística, recuperação de áudio ou homologação geral do método.

Os valores numéricos preservados são invariantes desta edição controlada, não respostas esperadas para futuros agentes nem alvos para ajustar o motor. A rodada sintética anterior e seus artefatos permanecem intactos. Os gates históricos de desenvolvimento não foram promovidos.
