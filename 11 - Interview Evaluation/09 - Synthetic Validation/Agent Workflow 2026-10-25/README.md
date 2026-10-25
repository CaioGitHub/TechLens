# Validação diagnóstica do roteiro do agente

Três casos inteiramente fictícios. Entradas e expectativas foram gravadas antes dos relatórios de análise e fixadas em `manifest.json`. Sem alvo numérico de score e sem transcrição corrigida artificial como referência.

Esta execução será feita pelo mesmo agente que criou os casos, com expectativas conhecidas. Não é cega, independente, benchmark de acurácia, validação humana ou entrevista real. A execução avalia o uso do projeto como fonte pelo agente, sem chamar provedores ou substituir a análise pelo runtime Python.

Para repetir em outro agente: disponibilizar `TRANSCRIPTION_AGENT_WORKFLOW.md` e suas referências, enviar somente um caso por vez de `cases/` e guardar a entrega antes de consultar `reference/`. O acesso desse outro agente às expectativas e histórico deve ser controlado externamente; a separação de pastas sozinha não garante cegamento.

Os relatórios aqui são artefatos do exercício diagnóstico, não avaliações de pessoas reais nem relatórios finais de candidatos. Os testes de regressão do runtime são evidência distinta e não medem qualidade da análise feita por um agente externo.
