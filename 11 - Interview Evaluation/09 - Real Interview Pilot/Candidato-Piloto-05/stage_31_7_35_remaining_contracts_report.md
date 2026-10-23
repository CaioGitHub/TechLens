# Stage 31.7.35 — Contratos complementares e validação incremental

Data: 2026-10-23. Runtime final SHA-256: `E537ED4DD81892B1378877536976E668A14ECCF975B8EE87BFF1245746E8E6B0`.

## Resultado

Adicionados 22 testes complementares, cobrindo cenários dos 12 contratos do plano atual. A execução inicial dos primeiros 21 testes produziu dez registros de falha, incluindo subtestes. As falhas foram preservadas em `stage_31_7_35_contracts_baseline.json` antes das mudanças.

Mudanças aplicadas e testadas sequencialmente:

1. Perguntas: comparação imperativa, recuperação de entidades pelo contraste, limites numéricos abertos, pedidos secundários opcionais e incerteza explícita para intenção não reconhecida. 38 testes direcionados aprovados.
2. Preâmbulos: reconhecimento de narrativas longas. Uma inspeção adicional encontrou perda de conteúdo técnico em frase mista; ela foi corrigida e coberta antes de continuar. 41 testes direcionados aprovados após a correção.
3. Escopos: remoção do corte arbitrário em 40 caracteres de negações e condições. 46 testes direcionados aprovados.
4. Autocorreções: segmentação de reformulações na mesma frase, mantendo o teste conservador de reversão explícita. 52 testes direcionados aprovados.

## Verificação final

- Regressão: 1119 testes, 1118 aprovados, 1 ignorado, zero falhas/erros; 38.875 s.
- Reference Harness isolado: 15/15 aprovados; 34.229 s.
- Hash inalterado durante as execuções. AST inalterada fora das duas classes de extração.
- Saídas e contagens reais persistidas nos arquivos `stage_31_7_35_contracts_canonical.json` e `stage_31_7_35_contracts_harness.json`.
- Snapshots anteriores a cada grupo preservados sob `runtime.py.inc1_contracts_*_entry`.

## Rastreabilidade dos testes

| Contrato | Métodos da suíte complementar | Estado |
| --- | --- | --- |
| SC-01 | test_sc01_all_eleven_intents, test_sc01_unrecognized_intent_records_uncertainty | Cenários aprovados |
| SC-02 | test_sc02_four_requests_preserve_order, test_sc02_optional_secondary_demand | Cenários aprovados |
| SC-05 | test_sc05_open_lowercase_entities | Cenários aprovados |
| SC-06 | test_sc06_open_numeric_context, test_sc06_shared_operational_context | Cenários aprovados |
| SC-17 | test_sc17_long_preamble_keeps_technical_core, test_sc17_technical_narrative_is_retained, test_sc17_mixed_traffic_sentence_preserves_technical_clause | Cenários aprovados |
| SC-18 | test_sc18_complete_long_negation_scope, test_sc18_negation_does_not_leak | Cenários aprovados |
| SC-20 | test_sc20_trailing_condition, test_sc20_complete_long_condition | Cenários aprovados |
| SC-21 | test_sc21_same_sentence_explicit_correction, test_sc21_same_sentence_refinement_is_not_retracted, test_sc21_unrelated_assertion_not_retracted | Cenários aprovados |
| ADV-05 | test_adv05_long_preamble_pair_invariance | Cenários aprovados |
| ADV-06 | test_adv06_implicit_joint_demands | Cenários aprovados |
| ADV-11 | test_adv11_prevention_and_destructive_action_differ | Cenários aprovados |
| ADV-12 | test_adv12_conditions_remain_local, test_sc21_conditional_polarity_is_not_global_retraction | Cenários aprovados |

## Limitações e governança

Gate: `CONTRACT_SCENARIOS_VERIFIED_GOVERNANCE_RECONCILIATION_PENDING`.

A cobertura dos cenários não homologa irrestritamente o INC-1 nem a arquitetura. O roadmap do Stage 31.7.33 atribui segmentação ao INC-2 e suficiência ao INC-1; o plano do Stage 31.7.35 reúne representação da pergunta e discurso e proíbe suficiência semântica. Há ainda diferença entre dez e onze intenções. Esta execução segue o escopo representacional do plano atual e registra a divergência; não declara atendidos os contratos de suficiência nem concluído o INC-2 histórico.

Extração de entidades e preâmbulos continua heurística. Escopos são locais às cláusulas, sem parser sintático geral. A retratação exige correspondência conservadora, sem resolver paráfrases ou alvos remotos. A proveniência histórica do snapshot rotulado como Stage 31.7.27 permanece não comprovada. Nenhuma validação cega independente foi executada.

## Reprodução

As suítes específicas são `tests.test_stage_31_7_35_remaining_contracts`, `tests.test_stage_31_7_35_inc1_audit_fixes` e `tests.test_stage_31_7_34_inc0_contracts`. Executor de resultados: `scratch/run_stage_31_7_35_contract_verification.py canonical` ou `harness`, a partir da raiz do projeto e com Python disponível. O executor registra a integridade e as saídas reais.

## Versionamento

Branch de trabalho: `codex/inc1-contract-coverage`. Checkpoint anterior aprovado: `b5538f3`. Estas mudanças formam um novo checkpoint separado após testes. Relatórios históricos não foram sobrescritos.
