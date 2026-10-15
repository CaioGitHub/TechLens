# Stage 31.7.27 — Registro de Checkpoints e Protocolo de Rollback (Ciclo 5)

## 1. Identificação do Baseline de Entrada

- **Arquivo Canônico:** `reference_runtime/runtime.py`
- **SHA-256 Baseline de Entrada:**
  $$\textbf{36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7}$$
- **Snapshot de Backup Inicial:**
  `reference_runtime/runtime.py.stage_31_7_26_baseline`
  - SHA-256: `36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7` (Integridade verificada com sucesso).

---

## 2. Critérios de Acionamento de Rollback

O rollback para o snapshot do incremento anterior ou para o baseline inicial será imediatamente acionado se qualquer uma das seguintes condições ocorrer:

1. **Falha na Regressão Canônica:** Qualquer falha ou erro nos 1.047 testes unitários da pasta `tests/`.
2. **Falha no Reference Harness:** Qualquer falha nos 15 testes de integração do Stage 26 (`tests.test_stage_26_reference_harness`).
3. **Regressão em Classes Estabilizadas:** Rebaixamento indevido de casos consolidados de `UNKNOWN` (precisão 100%) ou `PARTIAL` (recall 93,33%).
4. **Indeterminismo:** Detecção de qualquer variação de saída para as mesmas entradas em execuções repetidas.
5. **Violação Contratual:** Concessão de `DIRECT` para domínios comprovadamente disjuntos (`OFF_TOPIC`) ou metadados institucionais (`RELATED`).

---

## 3. Registro dos Checkpoints Incrementais

Durante a implementação do Stage 31.7.27, os seguintes snapshots intermediários serão gerenciados:

| Checkpoint | Arquivo de Snapshot | Incremento Correspondente | Status |
|---|---|---|---|
| **CP-0 (Baseline)** | `reference_runtime/runtime.py.stage_31_7_26_baseline` | Entrada no Estágio | **HOMOLOGADO** (`36344F3E...`) |
| **CP-A** | `reference_runtime/runtime.py.stage_31_7_27_inc_a` | Incremento A (Semantic Domain Disjunction Engine) | **HOMOLOGADO** |
| **CP-B** | `reference_runtime/runtime.py.stage_31_7_27_inc_b` | Incremento B (Demand-Proposition Nexus Matcher) | **HOMOLOGADO** |
| **CP-C** | `reference_runtime/runtime.py.stage_31_7_27_inc_c` | Incremento C (Cobertura e Suficiência Relativa à Intenção) | **HOMOLOGADO** |
| **CP-D** | `reference_runtime/runtime.py.stage_31_7_27_inc_d` | Incremento D (StrictOntologyRelevanceAggregator) | **HOMOLOGADO** |
| **CP-E (Final)** | `reference_runtime/runtime.py.stage_31_7_27_final` | Incremento E (Rastreabilidade e Integração Completa) | **HOMOLOGADO** (`3FD3F80D9BB8A13CCC3A2791759D08F2EED25271913B56F064710DB94B2BC229`) |

---

## 4. Instruções de Restauração Operacional

Caso ocorra necessidade de reversão imediata:
```powershell
# Exemplo de Rollback para o Baseline Inicial
Copy-Item -Path "reference_runtime/runtime.py.stage_31_7_26_baseline" -Destination "reference_runtime/runtime.py" -Force
py -3 -c "import hashlib; print(hashlib.sha256(open('reference_runtime/runtime.py', 'rb').read()).hexdigest().upper())"
# Confirmar retorno ao hash 36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7
```
