---
type: reference
status: study
confidence: 95
created: 2026-10-14
updated: 2026-10-14
tags:
  - stage-31-7-25
  - validation-plan
  - blind-revalidation
  - cycle-4
---

# Stage 31.7.25 — Plano de Validação Cega e Auditoria Semântica Independente (Ciclo 4)

## 1. Objetivo e Escopo

O presente documento formaliza o plano de execução e o protocolo de governança para o **Stage 31.7.25 — Independent Blind Semantic Revalidation of the Cycle 4 Remediated Runtime**.

O objetivo primordial desta etapa é submeter o motor de relevância semântica em domínio aberto, congelado no Stage 31.7.24, a uma validação cega sobre um conjunto amostral de pelo menos 250 casos inéditos e representativos de engenharia de software e sistemas distribuídos, avaliando se as correções estruturais do Ciclo 4 (CR-01 a CR-08) generalizam com precisão, consistência e proporcionalidade sem degradar o rigor epistêmico.

### Regra Metodológica Suprema
Este estágio é **exclusivamente de validação e auditoria**.
- **PROIBIDO:** Modificar o código do runtime (`reference_runtime/runtime.py`).
- **PROIBIDO:** Ajustar heurísticas, adicionar exceções locais ou calibrar limiares.
- **PROIBIDO:** Adaptar os casos do benchmark às respostas do sistema.
- **PROIBIDO:** Alterar rótulos de referência após a observação das previsões.
- **PROIBIDO:** Mascarar ou descartar divergências semânticas difíceis.
- A integridade metodológica e o rigor científico prevalecem absolutamente sobre a obtenção de resultados favoráveis ou aprovação de gates.

---

## 2. Auditoria e Congelamento do Runtime

O runtime autorizado para a execução desta validação é:
- **Arquivo:** [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py)
- **SHA-256 Esperado:** `36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7`
- **Condição de Inviolabilidade:** O hash SHA-256 deve ser calculado imediatamente antes da inferência e recalculado após a geração de todos os artefatos. Qualquer divergência de hash invalida a execução imediatamente com o status `BLOCKED_RUNTIME_HASH_MISMATCH`.

---

## 3. Protocolo de Cegamento Estrito

Para assegurar cegamento metodológico absoluto e impossibilitar contaminação cognitiva ou vazamento de rótulos durante a inferência:

1. **Segregação Física e Lógica de Arquivos:**
   - `stage_31_7_25_blind_input.json`: Contém estritamente `id`, `question_text` e `response_text`.
   - `stage_31_7_25_ground_truth.json`: Contém a referência semântica completa, adjudicação, grupo, status epistêmico e justificativa humana.
   - `stage_31_7_25_system_predictions.json`: Armazena exclusivamente a saída bruta da inferência do runtime.
   - `stage_31_7_25_metrics_summary.json`: Calculado apenas após o congelamento e persistência das previsões.
2. **Neutralidade de Identificadores:**
   - Nenhum ID de caso conterá pistas sobre o grupo semântico ou a classe esperada (ao contrário de estágios anteriores que usavam prefixos como `A01`, `B02`, `OFF_TOPIC`).
   - Todos os casos utilizarão formato sequencial neutro: `CASE_001` até `CASE_250`.
3. **Ordem Temporal Inegociável:**
   - A inferência será executada consumindo exclusivamente `stage_31_7_25_blind_input.json`.
   - O arquivo `stage_31_7_25_system_predictions.json` será gerado e selado criptograficamente antes da leitura comparativa do ground truth.

---

## 4. Declaração Formal de Independência da Referência

Em estrita consonância com o princípio de governança e honestidade intelectual:
- O estado metodológico da independência da referência permanece explicitamente classificado como:
  ```text
  REFERENCE_INDEPENDENCE_UNRESOLVED
  ```
- **Justificativa:** Embora os casos do benchmark sejam 100% inéditos em relação a benchmarks históricos anteriores e a inferência seja executada sob cegamento estrito, a adjudicação de referência é elaborada e auditada internamente, sem painel de avaliadores humanos externos terceirizados e cegos ao projeto.
- **Consequência no Gate:** Mesmo que o sistema atinja 100% dos limiares quantitativos, o gate máximo permitido não será de aprovação irrestrita, mas sim:
  ```text
  BLIND_EXECUTION_COMPLETE_REFERENCE_INDEPENDENCE_UNRESOLVED
  ```

---

## 5. Especificação do Benchmark de 250 Casos Inéditos

### 5.1 Critérios de Novidade e Não-Sobreposição
Nenhum caso do benchmark do Stage 31.7.25 poderá constar nos benchmarks de estágios anteriores (Stages 31.7.6, 31.7.13, 31.7.17, 31.7.21) ou nas suítes de testes unitários em `tests/`.
- Verificação de sobreposição textual exata em perguntas e respostas: zero correspondências.
- Verificação de redundância de casos diagnósticos do Stage 31.7.21: reformulações substanciais e domínios tecnológicos novos.

### 5.2 Distribuição das Sete Classes Canônicas
O benchmark abrangerá uma distribuição balanceada entre as 7 classes:
- `DIRECT`: ~50 a 60 casos
- `PARTIAL`: ~40 a 50 casos
- `SUPPORTING`: ~25 a 35 casos
- `RELATED`: ~30 a 40 casos
- `OFF_TOPIC`: ~40 a 50 casos
- `INSUFFICIENT`: ~20 a 30 casos
- `UNKNOWN`: ~15 a 25 casos

### 5.3 Cobertura dos 16 Grupos Semânticos Obrigatórios (A a P)
- **Grupo A:** Respostas diretamente corretas com mecanismo operacional completo.
- **Grupo B:** Respostas multi-aspecto com omissão de estado secundário obrigatório (`PARTIAL`).
- **Grupo C:** Contribuição instrumental, telemetria e observabilidade (`SUPPORTING`).
- **Grupo D:** Proximidade temática e metadados institucionais sem mecanismo (`RELATED`).
- **Grupo E:** Respostas semanticamente disjuntas e domínios desconexos (`OFF_TOPIC`).
- **Grupo F:** Evasões, deferimentos e respostas vagas sem evidência (`INSUFFICIENT`).
- **Grupo G:** Incerteza epistemológica e ambiguidades genuínas (`UNKNOWN`).
- **Grupo H:** Demandas compostas com coordenação e compensação (*Sagas*, *2PC*).
- **Grupo I:** Antíteses destrutivas com e sem guarda de prevenção.
- **Grupo J:** Respostas em linguagem informal e termos técnicos coloquiais brasileiros.
- **Grupo K:** Relatos autobiográficos e anedotas históricas de criadores.
- **Grupo L:** Tautologias circulares nas 11 famílias de cognatos morfológicos.
- **Grupo M:** Menção de ferramentas e bibliotecas sem mecanismo suficiente.
- **Grupo N:** Respostas ultra-concisas versus prolixas e detalhadas.
- **Grupo O:** Pares de invariância representacional formalmente controlados.
- **Grupo P:** Lacunas e insuficiências de evidência para avaliação segura.

---

## 6. Limiares Quantitativos Contratuais de Aceite

| Indicador | Fórmula Matemática | Limiar de Aceite |
|---|---|:---:|
| **Concordância Exata** | $\frac{\text{Previsões Corretas}}{\text{Total de Casos Válidos (250)}}$ | $\ge 75,00\%$ |
| **Recall de `DIRECT`** | $\frac{\text{TP}_{\text{DIRECT}}}{\text{Total de Referências DIRECT}}$ | $\ge 85,00\%$ |
| **Precisão de `DIRECT`** | $\frac{\text{TP}_{\text{DIRECT}}}{\text{Total de Previsões DIRECT}}$ | $\ge 70,00\%$ |
| **Falsos DIRECT entre Divergências** | $\frac{\text{FP}_{\text{DIRECT}}}{\text{Total de Casos Divergentes}}$ | $\le 10,00\%$ |
| **Recall de `PARTIAL`** | $\frac{\text{TP}_{\text{PARTIAL}}}{\text{Total de Referências PARTIAL}}$ | $\ge 60,00\%$ |
| **Invariância Pareada Correta** | $\frac{\text{Pares com Previsões Iguais e Ambas Corretas}}{\text{Total de Pares Válidos}}$ | $\ge 80,00\%$ |
| **Regressão Canônica** | Falhas na suíte de testes unitários ou no Reference Harness | **0 Falhas** |

---

## 7. Rastreabilidade dos Entregáveis

Ao término da validação, os seguintes artefatos devem estar persistidos e catalogados em `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/`:
1. `stage_31_7_25_validation_plan.md` (este documento)
2. `stage_31_7_25_benchmark_manifest.json`
3. `stage_31_7_25_blind_input.json`
4. `stage_31_7_25_ground_truth.json`
5. `stage_31_7_25_system_predictions.json`
6. `stage_31_7_25_metrics_summary.json`
7. `stage_31_7_25_confusion_matrix.json`
8. `stage_31_7_25_invariance_results.json`
9. `stage_31_7_25_divergence_analysis.json`
10. `stage_31_7_25_regression_results.json`
11. `stage_31_7_25_provenance_and_blinding_audit.md`
12. `Stage 31.7.25 — Independent Blind Semantic Revalidation of the Cycle 4 Remediated Runtime.md`
