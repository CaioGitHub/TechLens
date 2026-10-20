# Registro de Rollback — Stage 31.7.34 (Incremento 0)

## 1. Identificação de Artefatos e Hashes SHA-256

- **Arquivo sob Governança**: `reference_runtime/runtime.py`
- **Hash de Baseline (Pré-INC-0)**:
  `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28`
- **Hash de Snapshot de Segurança**:
  `reference_runtime/runtime.py.stage_31_7_34_baseline`
  SHA-256: `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28`
- **Hash Pós-Implementação do INC-0**:
  `E047BA643A6E98975E42336C58339A12AB4D33D48082ED808FF26248478AB1B8`
- **Hash do Snapshot do INC-0**:
  `reference_runtime/runtime.py.stage_31_7_34_inc0`
  SHA-256: `E047BA643A6E98975E42336C58339A12AB4D33D48082ED808FF26248478AB1B8`

---

## 2. Gatilhos de Rollback

O procedimento de rollback deve ser executado imediatamente caso qualquer uma das seguintes condições ocorra:
1. Qualquer falha ou regressão na suíte de testes canônica (1.084 testes esperados).
2. Qualquer falha no Reference Harness (`tests.test_stage_26_reference_harness`, 15 testes esperados).
3. Qualquer falha na validação do schema Draft-07 de `EvidenceTraceabilityRecord`.
4. Qualquer divergência não intencional em classificações semânticas anteriores.
5. Inconsistência de hash ou corrupção de estado durante a continuidade para o INC-1.

---

## 3. Comandos Exatos de Rollback

Para reverter o arquivo de runtime ao estado exato do baseline de segurança:

```powershell
# 1. Restaurar o arquivo do runtime a partir do snapshot validado
Copy-Item "reference_runtime/runtime.py.stage_31_7_34_baseline" "reference_runtime/runtime.py" -Force

# 2. Confirmar a restauração do hash SHA-256 original
py -3 -c "import hashlib; h = hashlib.sha256(open('reference_runtime/runtime.py', 'rb').read()).hexdigest().upper(); print('Restored hash:', h); assert h == '6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28'"
```

---

## 4. Critérios de Verificação Pós-Reversão

Após a execução do rollback, os seguintes passos são mandatórios para atestar a restauração do ambiente:
1. **Verificação de Hash**: O hash de `reference_runtime/runtime.py` deve ser estritamente igual a `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28`.
2. **Execução da Suíte Canônica Pré-INC-0**:
   ```powershell
   py -3 -m unittest discover -s tests -p "test_*.py"
   ```
   Deve reportar exatamente 1.067 testes executados (1.066 OK, 1 skipped).
3. **Execução do Reference Harness**:
   ```powershell
   py -3 -m unittest tests.test_stage_26_reference_harness
   ```
   Deve reportar 15 testes executados, 15 OK.
