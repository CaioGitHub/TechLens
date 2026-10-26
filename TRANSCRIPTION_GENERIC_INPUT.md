# Entrada genérica de transcrições


## Atualização de uso — 2026-10-26

Este documento conserva o checkpoint de implementação descrito abaixo. Para o estado corrente e a distinção entre implementação e validação semântica, consultar `TRANSCRIPTION_PROJECT_STATUS_2026-10-26.md`. O uso vigente é a transcrição enviada ao agente do usuário, que consulta o projeto como método; conectar provedor/modelo interno não é requisito nem próximo incremento obrigatório. A entrada genérica e a proteção do importador já existem; outra entrevista distinta permanece pendente.


Data: 2026-10-25. Estado limitado: `GENERIC_TRANSCRIPTION_INPUT_VERIFIED`.

`reference_runtime.transcription_input.build_transcription_fixture(turns, participants, interview_id=...)` recebe turnos e participantes configuráveis. Não depende de nomes, tecnologias ou prefixos de IDs de um piloto.

Cada turno requer `id`, `speaker`, `timestamp` e `text` como strings não vazias. Timestamp é preservado como informação da fonte, sem inferir tempos ausentes; este adaptador não interpreta todos os formatos de tempo ou arquivos de plataformas. Cada participante requer `participant_id`, `name` (rótulo exato da fonte) e `role` entre candidate/interviewer/observer. IDs e rótulos de participantes e IDs de turnos devem ser únicos; é necessário configurar ao menos candidato e entrevistador.

O adaptador preserva texto exato, quebras de linha, rótulos, timestamps e IDs sem mutar entradas. Registra hashes por texto e fingerprint da entrada recebida. Isso vincula a entrada, mas não comprova correspondência com áudio. Falantes não mapeados permanecem na fonte, marcados como ambíguos, sem papel ou identidade arbitrariamente atribuídos.

O runtime agora respeita IDs explícitos ligados ao rótulo configurado, preservando a distinção entre vários entrevistadores. Um ID que conflita com a configuração é rejeitado. Marcação de fala ambígua atravessa a adaptação e exige revisão. Metadados de fonte acompanham os artefatos; as regras de correção revisada e adiamento continuam aplicáveis.

## Verificação

Foram criados contratos antes da implementação. A integração reproduziu troca da identidade do primeiro entrevistador pela do segundo e perda da flag de ambiguidade; ambas foram corrigidas antes da regressão.

- Dez métodos novos de teste.
- 70 testes direcionados aprovados.
- Regressão completa: 600/600 aprovados; harness: 15/15, sem falhas, erros ou skips.
- Resultado e hashes em `TRANSCRIPTION_GENERIC_INPUT_RESULTS.json`.

Não foram alterados scores, rubricas, testes históricos ou conteúdo do candidato.

## Escopo e continuidade

Este incremento entrega a entrada por lista de turnos já identificados pela plataforma/camada de importação. Importadores específicos de arquivos, identificação automática de participantes, interface e conexão a modelo permanecem pendentes. O parser e o adaptador dos pilotos existentes foram preservados.

A diretriz de a IA fazer a maior parte da análise está definida em [[TRANSCRIPTION_AI_ANALYSIS_CONTRACT]]. Próximo passo: integrar o analisador de IA com saída verificável e preservação da fonte, antes de construir a fila/interface de revisão. Nenhum modelo foi conectado nem transcrição enviada externamente neste checkpoint.
