# Stage 31.7.33 — Protocolo de Rollback, Congelamento e Salvaguardas Criptográficas

## 1. Princípio Fundamental de Imutabilidade e Reversibilidade

Nenhuma modificação futura do runtime canônico [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py) será realizada sem salvaguardas estritas de integridade binária. Cada incremento implementado no Stage 31.7.34 deverá possuir rastreabilidade SHA-256 antes e depois da edição, com snapshots intermediários dedicados e procedimento de rollback determinístico.

---

## 2. Linha de Base e Cadeia de Snapshots do Ciclo 6

| Identificador do Snapshot | Caminho do Arquivo | SHA-256 Autorizado | Papel no Pipeline |
|---|---|:---:|---|
| **Freeze Inicial (31.7.30/31/32/33)** | `reference_runtime/runtime.py.stage_31_7_32_freeze` | `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28` | Baseline imutável de entrada |
| **Freeze INC-0** | `reference_runtime/runtime.py.stage_31_7_34_inc_0` | *A ser gerado no Stage 31.7.34* | Snapshot pós-fundação de dados |
| **Freeze INC-1** | `reference_runtime/runtime.py.stage_31_7_34_inc_1` | *A ser gerado no Stage 31.7.34* | Snapshot pós-perfil de intenção |
| **Freeze INC-2** | `reference_runtime/runtime.py.stage_31_7_34_inc_2` | *A ser gerado no Stage 31.7.34* | Snapshot pós-segmentação discursiva |
| **Freeze INC-3** | `reference_runtime/runtime.py.stage_31_7_34_inc_3` | *A ser gerado no Stage 31.7.34* | Snapshot pós-afinidade temática |
| **Freeze INC-4** | `reference_runtime/runtime.py.stage_31_7_34_inc_4` | *A ser gerado no Stage 31.7.34* | Snapshot pós-equivalência e analogias |
| **Freeze INC-5 (Final Ciclo 6)** | `reference_runtime/runtime.py.stage_31_7_34_final` | *A ser gerado no Stage 31.7.34* | Snapshot pós-agregação 7 classes |

---

## 3. Arquivos Autorizados a Mudar no Stage de Implementação

Durante a futura implementação (Stage 31.7.34), **APENAS** os seguintes arquivos possuem autorização expressa para modificação ou criação:
1. `reference_runtime/runtime.py` (runtime canônico editado em incrementos sucessivos);
2. `tests/test_stage_31_7_34_contract_tests.py` (nova suíte de testes dos 35 contratos e 15 adversariais);
3. Snapshots de rollback criados em `reference_runtime/runtime.py.stage_31_7_34_inc_*`;
4. Documentos de evidência e relatórios situados exclusivamente em `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/`;
5. Documentos de governança (`START_HERE.md` e `GEMINI_HANDOFF.md`).

**É TERMINANTEMENTE PROIBIDO MODIFICAR:**
- Snapshots históricos de estágios anteriores (`runtime.py.stage_31_7_26_baseline`, `runtime.py.stage_31_7_27_final`, etc.);
- A suíte de testes canônicos existente (`tests/test_*.py` legados);
- Arquivos de benchmark e gabaritos históricos;
- Notas de conhecimento técnico do Second Brain.

---

## 4. Condições de Interrupção Imediata (Trigger de Aborto)

O processo de implementação de qualquer incremento deverá ser **imediatamente interrompido**, acionando rollback, perante qualquer uma das seguintes condições:
1. **Quebra de Regressão Canônica:** Qualquer falha nos 1.047 testes da suíte canônica ou nos 15 testes do Reference Harness;
2. **Violação Contratual:** Falha em qualquer um dos contratos semânticos atribuídos ao incremento;
3. **Surgimento de Fallback Proibido:** Reintrodução de cláusulas genéricas `else: OFF_TOPIC`, `else: DIRECT` ou `else: UNKNOWN`;
4. **Introdução de Listas Fechadas:** Criação de dicionários estáticos de palavras proibidas ou regras específicas por caso;
5. **Perda de Rastreabilidade:** Incapacidade de emitir o registro JSON `EvidenceTraceabilityRecord` estruturado;
6. **Divergência Criptográfica:** Impossibilidade de verificar o hash do arquivo antes ou depois da modificação.

---

## 5. Procedimento Operacional de Rollback

Caso ocorra um trigger de aborto durante o incremento $K$:
1. **Identificar o Último Snapshot Válido:** $S_{K-1}$ (snapshot imutável do incremento anterior aprovado);
2. **Restaurar o Runtime Canônico:**
   ```bash
   py -3 -c "import shutil; shutil.copyfile('reference_runtime/runtime.py.stage_31_7_34_inc_{K-1}', 'reference_runtime/runtime.py')"
   ```
3. **Verificar Hash do Rollback:** Confirmar que o SHA-256 de `reference_runtime/runtime.py` coincide bit a bit com o hash registrado para $S_{K-1}$;
4. **Executar Regressão Canônica:** Revalidar os 1.047 testes e o Reference Harness para assegurar a restauração plena do estado verde;
5. **Preservar Evidências de Falha:** Registrar logs, diffs e relatórios de erro do incremento abortado na pasta do piloto sem sobrescrever arquivos históricos;
6. **Registrar Gate de Bloqueio:** Declarar formalmente o incremento como `BLOCKED` ou `FAIL` nos documentos de governança.
