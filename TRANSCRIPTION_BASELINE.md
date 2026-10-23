# Marco de retomada — Transcrição

Registrado em 2026-10-23 a pedido do usuário. Este marco fixa uma origem reproduzível para a frente de transcrição; não declara homologação ou estabilidade semântica.

## Origem e preservação

- Nova branch: `codex/transcription-baseline`.
- Origem solicitada: `transcriptionProcessingModel`.
- Commit exato de origem: `06e506e18a7054b1012ea2829fe97551473cd8a5` (`31.3`).
- O checkout foi criado a partir dessa origem, sem copiar mudanças recentes do avaliador.
- Frente anterior preservada: `codex/inc1-contract-coverage`.
- Checkpoint das quatro alterações pendentes na frente anterior: `8c0280c`. Ele contém resultados diagnósticos, executor e contratos de integração ainda com falhas esperadas. Não é um checkpoint de aprovação semântica.
- Nenhum histórico ou runtime foi sobrescrito por restauração manual. A alteração do conteúdo do checkout decorre da troca de branch autorizada.

## Resultado medido nesta origem

Comando equivalente: `python -B -m unittest discover -s tests -p "test_*.py"`.
Execução real com o Python fornecido pelo ambiente: **526 testes, 521 aprovados, cinco falhas, zero erros, zero ignorados**, em 17,988 s.

Hash SHA-256 do runtime antes e depois: `F9FFFDC01F66ECC321DAD82EB8E9B0E8A2F45BF9417560D89236C98902349703`.
Saída completa preservada em `TRANSCRIPTION_BASELINE_TEST_RESULTS.json`.

Falhas existentes nesta base:

1. `test_semantic_blind_calibration.SemanticBlindCalibrationTests.test_all_oracles_compare_after_execution`: CAL28-08, reasoning esperado strong e obtido weak.
2. `test_stage_28_semantic_blind_calibration.Stage28SemanticBlindCalibrationTests.test_minimum_diverse_case_count`: relatório com duas falhas, esperado zero.
3. `test_stage_28_semantic_blind_calibration.Stage28SemanticBlindCalibrationTests.test_semantic_dimensions_are_compared_separately`: uma dimensão com falha, esperado zero.
4. `test_stage_30_1_pilot_failure_analysis.Stage301PilotFailureAnalysisTests.test_before_after_impact_is_limited_to_removed_context_question`: divergência 28 versus 24.
5. `test_stage_30_2_1_final_semantic_audit.Stage3021FinalSemanticAuditTests.test_determinism_and_global_proportionality`: média obtida 5,14 versus referência 5,55.

Estas são observações da execução. Não autorizam ajustar scores ou oracles para forçar aprovação. As causas ainda precisam ser investigadas.

## Limites do marco

O handoff desta origem já registra `POST_CORRECTION_BLIND_VALIDATION_BLOCKED` e Stage 31.4 em andamento. As etapas de processamento de transcript 20.1–20.7 constam como concluídas no histórico, mas isso não significa que exista ingestão de áudio ou reconhecimento de fala implementado.

Os achados de contrato e rastreabilidade da branch mais recente continuam preservados lá. Não foram automaticamente atribuídos a esta versão anterior sem conferência específica.

Estado do marco: `TRANSCRIPTION_BASELINE_RECORDED_WITH_KNOWN_FAILURES`.

## Continuidade

Este marco é uma âncora de versionamento, não uma autorização para pular os gates existentes. Antes de novas implementações, identificar a primeira falha relevante à frente de transcrição, fixar seu teste e executar a cobertura específica. Resolver falhas inesperadas antes de avançar ao próximo grupo. O desenvolvimento deve preservar o conhecimento e os contratos existentes, sem redesign automático do avaliador.

O escopo de transcrição deve distinguir processamento de texto já transcrito de conversão de áudio em texto. A base atual documenta explicitamente o primeiro. A seleção de serviço ou modelo de reconhecimento de fala não faz parte deste marco.


## Recuperação da regressão da base de transcrição — 2026-10-23

Ver [[TRANSCRIPTION_BASELINE_CORRECTIONS]]. Dois defeitos de evidência corrigidos, quatro testes novos e dois testes de snapshots históricos reescritos com autorização explícita para invariantes comportamentais. Regressão completa: 530/530 aprovados; harness 15/15. Estado limitado: `TRANSCRIPTION_BASELINE_REGRESSION_RECOVERED`. A baseline inicial de cinco falhas permanece preservada. Não houve aprovação semântica independente nem revogação dos bloqueios históricos. Próximo passo: plano incremental de transcrição sobre o fluxo de texto existente.
