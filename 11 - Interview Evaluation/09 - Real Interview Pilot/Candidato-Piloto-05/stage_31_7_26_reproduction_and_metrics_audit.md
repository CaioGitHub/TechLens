---
type: reference
status: study
confidence: 100
created: 2026-10-14
updated: 2026-10-14
tags:
  - stage-31-7-26
  - reproduction-audit
  - metrics-reconciliation
  - cycle-5
---

# Stage 31.7.26 — Relatório de Reprodução e Auditoria de Métricas do Stage 31.7.25

## 1. Resumo da Auditoria e Verificação de Integridade

Em cumprimento estrito à Seção 5 do mandato do Stage 31.7.26, foi realizada a reprodução independente e automatizada de todos os cálculos, contagens, células da matriz de confusão e indicadores contratuais do Stage 31.7.25.

### 1.1 Auditoria do Runtime de Referência
- **Arquivo:** [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py)
- **SHA-256 Auditado:** `36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7`
- **SHA-256 Esperado (Stage 31.7.24 / 31.7.25):** `36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7`
- **Status:** **EXACT MATCH (100% INVIOLADO E CONGELADO)**.
- **Ambiente de Auditoria:** Python 3.13.9 (MSC v.1944 64 bit AMD64), Windows 11, diretório `D:\Projetos\TechLens`.

### 1.2 Hashes Criptográficos dos Artefatos de Entrada Auditados
Todos os 12 artefatos do Stage 31.7.25 foram localizados e tiveram seus hashes SHA-256 verificados:

| Arquivo do Stage 31.7.25 | SHA-256 Verificado | Status |
|---|---|:---:|
| `stage_31_7_25_validation_plan.md` | `BF0FCA9F049307D0EBFCA54853A2FC95472CB5B3BF239206A52D95EC59EF1987` | Íntegro |
| `stage_31_7_25_benchmark_manifest.json` | `F7470F5537777F8D137DC3CC4C3D2E37845AB180518B1F858EEFF413E49F0D16` | Íntegro |
| `stage_31_7_25_blind_input.json` | `8FAC4CAE5F7D7B6DB611B72DC48C5D03654AAB70002828BBFF9832D153855847` | Íntegro |
| `stage_31_7_25_ground_truth.json` | `5285F745C26AB1E641EFBC013ACB4C59AA166BF0C757467EC2764879A6E72C0F` | Íntegro |
| `stage_31_7_25_system_predictions.json` | `A53CA9FA51BF9D991EFB841FDE124658192BFD4E4C4537A848B3BA4418942F4A` | Íntegro |
| `stage_31_7_25_metrics_summary.json` | `87403350350102E1C8C0D7E84F88225CEC7E1EDDFDD9ACB4EA284CDBB9C6D8FD` | Íntegro |
| `stage_31_7_25_confusion_matrix.json` | `0CD105636E4DC298A4017F1300DD917DCC558726F962E17C586E32670418D9D9` | Íntegro |
| `stage_31_7_25_invariance_results.json` | `A88A0F09D95237F1894A06E288396D873C87506D7D7CCC6105789089219F4CDD` | Íntegro |
| `stage_31_7_25_divergence_analysis.json` | `CF35BCE965DA01DC8F5CD67835DAF3A08DB96428D5D3139E9EEAD9A163EB7129` | Íntegro |
| `stage_31_7_25_regression_results.json` | `942651C01991171A6AB32242A1FB6C90B652F66B56C400B56FBD736733D453A5` | Íntegro |
| `stage_31_7_25_provenance_and_blinding_audit.md` | `7CA1244C85BE2BE644C7B767FBF132ECBF0741642452C8859EC3E9EA7CC4F8A2` | Íntegro |
| `Stage 31.7.25 — Independent Blind Semantic Revalidation...` | `F9E1038040E1AF9B283825470F72B2E33F95D377D0249AA1DB80A8387FB56604` | Íntegro |

---

## 2. Reconciliação Matemática dos Indicadores e Totais

Os dados foram recalculados diretamente a partir do emparelhamento entre as 250 previsões em `stage_31_7_25_system_predictions.json` e as 250 referências em `stage_31_7_25_ground_truth.json`:

### 2.1 Reconciliação de Casos e Balanço Global
- **Total de Casos Avaliados:** 250 (Exatamente 250 casos)
- **Previsões Corretas:** 152 casos (60,80%)
- **Divergências Identificadas:** 98 casos (39,20%)
- **Equação de Balanço:** $\text{Corretos} (152) + \text{Divergências} (98) = 250$. **CONCILIADO COM SUCESSO**.
- **Soma das Células da Matriz de Confusão:** $\sum_{i,j} M_{ij} = 250$. **CONCILIADO COM SUCESSO**.

### 2.2 Fórmulas, Numeradores e Denominadores Recalculados

| Indicador | Fórmula Matemática | Numerador | Denominador | Valor Recalculado | Limiar Contratual | Status |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **Concordância Exata** | $\frac{\text{Previsões Corretas}}{\text{Total Casos}}$ | 152 | 250 | **60,80%** | $\ge 75,00\%$ | **FALHOU** |
| **Recall de DIRECT** | $\frac{\text{TP}_{\text{DIRECT}}}{\text{Total Ref DIRECT}}$ | 50 | 55 | **90,91%** | $\ge 85,00\%$ | **PASSOU** |
| **Precisão de DIRECT** | $\frac{\text{TP}_{\text{DIRECT}}}{\text{Total Pred DIRECT}}$ | 50 | 120 | **41,67%** | $\ge 70,00\%$ | **FALHOU** |
| **Falsos DIRECT entre Divergências** | $\frac{\text{FP}_{\text{DIRECT}}}{\text{Total Divergências}}$ | 70 | 98 | **71,43%** | $\le 10,00\%$ | **FALHOU** |
| **Recall de PARTIAL** | $\frac{\text{TP}_{\text{PARTIAL}}}{\text{Total Ref PARTIAL}}$ | 42 | 45 | **93,33%** | $\ge 60,00\%$ | **PASSOU** |
| **Invariância Pareada Correta** | $\frac{\text{Pares Corretos Conjuntos}}{\text{Total Pares}}$ | 8 | 20 | **40,00%** | $\ge 80,00\%$ | **FALHOU** |
| **Consistência de Saída em Pares** | $\frac{\text{Pares com Previsões Iguais}}{\text{Total Pares}}$ | 10 | 20 | **50,00%** | - | Informativo |

---

## 3. Reconciliação dos 70 Falsos DIRECT

A auditoria matemática confirmou exatamente a composição dos 70 falsos positivos de `DIRECT`:

| Transição Semântica Indevida | Quantidade de Casos | Proporção entre Falsos DIRECT | Proporção entre Divergências (98) |
|---|:---:|:---:|:---:|
| **`OFF_TOPIC → DIRECT`** | **34** | 48,57% | 34,69% |
| **`RELATED → DIRECT`** | **22** | 31,43% | 22,45% |
| **`SUPPORTING → DIRECT`** | **7** | 10,00% | 7,14% |
| **`INSUFFICIENT → DIRECT`** | **7** | 10,00% | 7,14% |
| **Total de Falsos DIRECT** | **70** | **100,00%** | **71,43%** |

---

## 4. Reconciliação das 28 Divergências Não-DIRECT

As 28 divergências restantes foram reexaminadas célula por célula:
- `DIRECT → PARTIAL`: 1 caso
- `DIRECT → RELATED`: 2 casos
- `DIRECT → OFF_TOPIC`: 2 casos
- `PARTIAL → RELATED`: 1 caso
- `PARTIAL → OFF_TOPIC`: 2 casos
- `SUPPORTING → PARTIAL`: 1 caso
- `SUPPORTING → OFF_TOPIC`: 3 casos
- `RELATED → OFF_TOPIC`: 4 casos
- `INSUFFICIENT → OFF_TOPIC`: 11 casos (respostas evasivas cuja oração explicativa foi classificada como `non_operative_assertion`, conduzindo a `OFF_TOPIC`)
- `UNKNOWN → OFF_TOPIC`: 1 caso
- **Total:** $1 + 2 + 2 + 1 + 2 + 1 + 3 + 4 + 11 + 1 = 28$ casos.
- **Soma Total:** $70 + 28 = 98$ casos.

---

## 5. Conclusão da Auditoria de Reprodução

1. Não foram identificadas discrepâncias numéricas ou inconsistências de arredondamento nos artefatos do Stage 31.7.25.
2. A matriz de confusão salva em `stage_31_7_25_confusion_matrix.json` corresponde exatamente à inferência executada pelo runtime.
3. O status `BLIND_SEMANTIC_REVALIDATION_BLOCKED` é perfeitamente legítimo, necessário e matematicamente inquestionável.
4. O processo de investigação de causa-raiz pode prosseguir sobre dados 100% auditados e reproduzíveis.
