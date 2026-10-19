# Stage 31.7.30 — Verificação de Integridade e Congelamento do Runtime

## 1. Identificação do Runtime Canônico sob Revisão

- **Caminho Canônico:** `reference_runtime/runtime.py`
- **Tamanho:** 254.619 bytes
- **SHA-256 Verificado na Entrada:**
  $$\textbf{6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28}$$
- **Comparação com Stage 31.7.29:** Rigorosamente idêntico ao registrado nos documentos de encerramento do Stage 31.7.29.
- **Snapshot Dedicado de Entrada:** `reference_runtime/runtime.py.stage_31_7_30_freeze` (SHA-256 `6C44B7A8...`).

---

## 2. Inventário Criptográfico Completo de Snapshots e Runtimes

| Arquivo | Tamanho (bytes) | SHA-256 | Função / Papel |
|---|:---:|:---:|---|
| `reference_runtime/runtime.py` | 254.619 | `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28` | Runtime canônico congelado |
| `runtime.py.stage_31_7_30_freeze` | 254.619 | `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28` | Snapshot de entrada do Stage 31.7.30 |
| `runtime.py.stage_31_7_29_forensic_entry` | 254.619 | `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28` | Snapshot de preservação do Stage 31.7.29 |
| `runtime.py.stage_31_7_27_final` | 254.619 | `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28` | Snapshot homologado do Stage 31.7.27 |
| `runtime.py.stage_31_7_27_pre_regression_fix` | 254.536 | `3FD3F80D9BB8A13CCC3A2791759D08F2EED25271913B56F064710DB94B2BC229` | Snapshot pré-correções canônicas (Stage 31.7.27) |
| `runtime.py.stage_31_7_27_inc_a` | 249.495 | `22EBFFB7137BA786AA4C14D84298BA1C9BD84D076E2F78B767065998BAC77ABC` | Snapshot Incremento A do Stage 31.7.27 |
| `runtime.py.stage_31_7_26_baseline` | 241.085 | `36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7` | Baseline do Stage 31.7.26 (Ciclo 4) |
| `runtime.py.stage_31_7_24_pre_implementation` | 230.363 | `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC` | Snapshot histórico Ciclo 3 / Ciclo 4 |
| `runtime.py.stage_31_7_19_baseline` | 216.562 | `AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB` | Snapshot histórico Ciclo 2 |

---

## 3. Delimitação Estrita de Permissões de Arquivos

### Arquivos com Permissão Exclusiva de Leitura:
- `reference_runtime/*` (todos os runtimes e snapshots);
- `tests/*` (todas as suítes unitárias, de integração e de harness);
- `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_28_*` (benchmark, gabarito e predições do Stage 31.7.28);
- `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_29_*` (RCA e especificações do Stage 31.7.29);
- Relatórios e registros históricos de stages anteriores.

### Arquivos Permitidos para Criação e Edição (Exclusivos do Stage 31.7.30):
- `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_30_*` (todos os 11 artefatos mandatórios);
- `START_HERE.md` (atualização de governança ao final);
- `GEMINI_HANDOFF.md` (registro de transição ao final).

### Proibições Explícitas Vigentes:
- PROIBIDO modificar `reference_runtime/runtime.py` ou qualquer snapshot;
- PROIBIDO implementar classes, métodos ou heurísticas;
- PROIBIDO alterar limiares de tolerância ou critérios de decisão;
- PROIBIDO editar o ground truth ou predições de estágios passados.
