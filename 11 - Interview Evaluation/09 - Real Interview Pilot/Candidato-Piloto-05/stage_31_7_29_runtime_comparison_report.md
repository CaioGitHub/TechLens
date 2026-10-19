# Stage 31.7.29 — Relatório Comparativo entre os Runtimes 3FD3F80D... e 6C44B7A8...

## 1. Visão Geral e Identificação dos Artefatos

O objetivo deste relatório é dissecar as diferenças técnicas e semânticas entre:
- **Runtime Pré-Fix:** `reference_runtime/runtime.py.stage_31_7_27_pre_regression_fix`
  - SHA-256: `3FD3F80D9BB8A13CCC3A2791759D08F2EED25271913B56F064710DB94B2BC229`
  - Tamanho: 254.536 bytes | Data: 14/10/2026 22:24:37 UTC
- **Runtime Final Homologado:** `reference_runtime/runtime.py` (idêntico a `stage_31_7_27_final`)
  - SHA-256: `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28`
  - Tamanho: 254.619 bytes | Data: 14/10/2026 22:36:27 UTC

---

## 2. Anatomia Exata das Alterações no Código

O diff unificado entre os dois arquivos consiste em 84 linhas modificadas distribuídas em 3 blocos funcionais estritamente delimitados:

### Bloco 1: Salvaguarda contra Falso Gatilho de Antítese Destrutiva (Linhas 3275–3279)
```diff
-        # 3b. Destructive antithesis regex matching
-        antithesis_pat = r'\b(desativ|remover|deslig|arranc|elimin|dispens|retir)[a-z]*\b[^.]{0,50}\b(locks?|travas?|transac[a-z]*|circuit\s+breaker|rate\s+limit|timeout|filtros?\s+de\s+autentica[a-z]*|tokens?\s+jwt|firewall|wal|fsync)\b'
-        is_antithesis = is_antithesis or bool(re.search(antithesis_pat, r_norm))
+        # 3b. Destructive antithesis regex matching (respecting avoidance guard)
+        avoidance_guard = bool(re.search(r'\b(para evitar|sem precisar|ao inves de|em vez de|nao devemos|nunca|evitar)\s+(desativ\w*|remov\w*|deslig\w*|retir\w*|elimin\w*|tir\w*|arranc\w*)', r_morph))
+        if not avoidance_guard:
+            antithesis_pat = r'\b(desativ|remover|deslig|arranc|elimin|dispens|retir)[a-z]*\b[^.]{0,50}\b(locks?|travas?|transac[a-z]*|circuit\s+breaker|rate\s+limit|timeout|filtros?\s+de\s+autentica[a-z]*|tokens?\s+jwt|firewall|wal|fsync)\b'
+            is_antithesis = is_antithesis or bool(re.search(antithesis_pat, r_norm))
```
- **Causa da Mudança:** No runtime `3FD3F80D...`, frases como *"Para evitar desativar travas..."* ou *"Sem precisar desligar o circuit breaker..."* eram flagradas como antítese destrutiva por causa do verbo *"desativar"* próximo a *"travas"*.
- **Impacto nos Testes:** Corrigiu as falhas nos testes unitários `test_avoidance_guard_does_not_trigger_antithesis` e `test_tc_07_colloquial_and_passive_antithesis`.

### Bloco 2: Proteção de Ambiguidade no Nexo de Evasão (Linha 3399)
```diff
-        if domain_record and domain_record.disjunction_type == "EVASIVE_DEFLECTION":
+        if domain_record and domain_record.disjunction_type == "EVASIVE_DEFLECTION" and not prop.is_ambiguous:
             return DemandPropositionNexus(
                 demand_id=demand.demand_id,
                 nexus_relation="EVASIVE",
```
- **Causa da Mudança:** No runtime `3FD3F80D...`, proposições ambíguas que continham marcadores evasivos eram forçadas para `EVASIVE`, impedindo a detecção de indeterminação semântica genuína.
- **Impacto nos Testes:** Corrigiu a regressão no teste `test_category_h_inference_limits_unknown_insufficient`.

### Bloco 3: Preservação da Ontologia de Ignorância vs Incerteza (Linhas 3693–3745)
```diff
-        # 1. Explicit ignorance -> UNKNOWN (Contract 8, Stage 31.7.27)
-        if any(n == "IGNORANCE" for n in nexus_relations):
-            classification = "UNKNOWN"
-            ...
-        # 2. Domain disjunction -> OFF_TOPIC
-        elif any(n == "DOMAIN_DISJUNCT" for n in nexus_relations):
+        # 1. Domain disjunction -> OFF_TOPIC
+        if any(n == "DOMAIN_DISJUNCT" for n in nexus_relations):
             ...
+        # 3. Ignorance / Insufficient / Filler -> INSUFFICIENT
+        elif any(n == "IGNORANCE" for n in nexus_relations) or any(n == "INSUFFICIENT" for n in nexus_relations):
+            classification = "INSUFFICIENT"
```
- **Causa da Mudança:** No Stage 31.7.27 inicial (`3FD3F80D...`), a declaração explícita de ignorância (*"Não sei"*) foi roteada para `UNKNOWN`. Isso violou o contrato ontológico canônico fixado nos Stages 31.7.11, 31.7.20 e 31.7.24, onde ignorância é falta de evidência técnica (`INSUFFICIENT`), e `UNKNOWN` é reservado para indeterminação semântica e tautologias circulares.
- **Impacto nos Testes:** Corrigiu as falhas em `test_all_seven_classes_reachable` e `test_all_seven_canonical_classes_reachable`.

---

## 3. Avaliação Comparativa sobre o Benchmark Cego (250 Casos)

Ambos os runtimes foram executados de forma idêntica sobre os 250 casos de `stage_31_7_28_blind_input.json`.

| Métrica | Runtime Pré-Fix (`3FD3F80D...`) | Runtime Final (`6C44B7A8...`) | Diferença |
|---|:---:|:---:|:---:|
| **Total de Acertos** | 152 / 250 | **168 / 250** | **+16 acertos no runtime final** |
| **Acurácia Global** | 60,80% | **67,20%** | **+6,40% no runtime final** |
| **Falsos DIRECT (`OFF_TOPIC → DIRECT`)** | **26 casos** | **26 casos** | **Idêntico (0% alteração)** |
| **Rebaixamento de Metadados (`RELATED → OFF_TOPIC`)** | **22 casos** | **22 casos** | **Idêntico (0% alteração)** |
| **Falso UNKNOWN em Ignorância (`INSUFFICIENT → UNKNOWN`)**| 16 casos | **0 casos** | **-16 erros no runtime final** |

### Conclusões Forenses:
1. **O runtime `6C44B7A8...` é estritamente superior ao runtime `3FD3F80D...`:** ele respeita a ontologia histórica de 7 classes, possui zero regressões canônicas na suíte do repositório (1.067 testes OK) e é 6,4 pontos percentuais mais preciso.
2. **A causa-raiz do bloqueio do Stage 31.7.28 é idêntica em ambos os runtimes:** os 26 casos de falso DIRECT e os 22 casos de falso OFF_TOPIC já estavam presentes e inalterados em `3FD3F80D...`. A transição para `6C44B7A8...` não introduziu nem mascarou nenhuma dessas falhas estruturais.
