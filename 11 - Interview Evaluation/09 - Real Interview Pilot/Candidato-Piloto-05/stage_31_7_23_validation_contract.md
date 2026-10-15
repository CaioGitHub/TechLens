---
type: reference
status: study
confidence: 95
created: 2026-10-14
updated: 2026-10-14
tags:
  - stage-31-7-23
  - validation-contract
  - metrics-specification
  - cycle-4
---

# Stage 31.7.23 — Contrato Formal de Validação Independente (Cycle 4)

## 1. Objetivo e Imutabilidade das Metas

Este contrato define as regras matemáticas, os limiares de aceitação quantitativos e o protocolo de execução cega para a homologação do runtime corrigido no **Ciclo 4** (a ser validado no **Stage 31.7.25**).

**Regra Fundamental:** Os limiares de aceitação são pré-fixados e imutáveis. Não é permitido afrouxar, ponderar ou modificar as fórmulas após a abertura das predições do sistema.

---

## 2. Critérios Quantitativos de Homologação

| Identificador | Métrica | Limiar de Aceite | Fórmula Matemática | Numerador / Denominador |
|---|---|:---:|---|---|
| **MET-01** | **Concordância Exata** | $\ge 75{,}0\%$ | $\frac{\sum_{i=1}^N \mathbb{I}(\hat{y}_i == y_i)}{N}$ | $\frac{\text{Predições Iguais à Referência}}{\text{Total de Casos Elegíveis no Benchmark}}$ |
| **MET-02** | **Recall de DIRECT** | $\ge 85{,}0\%$ | $\frac{\text{TP}_{\text{DIRECT}}}{\text{TP}_{\text{DIRECT}} + \text{FN}_{\text{DIRECT}}}$ | $\frac{\text{Casos Ref DIRECT previstos como DIRECT}}{\text{Total de Casos na Referência DIRECT}}$ |
| **MET-03** | **Precisão de DIRECT** | $\ge 70{,}0\%$ | $\frac{\text{TP}_{\text{DIRECT}}}{\text{TP}_{\text{DIRECT}} + \text{FP}_{\text{DIRECT}}}$ | $\frac{\text{Casos Ref DIRECT previstos como DIRECT}}{\text{Total de Predições emitidas como DIRECT}}$ |
| **MET-04** | **Falsos DIRECT entre Divergências** | $\le 10{,}0\%$ | $\frac{\text{FP}_{\text{DIRECT}}}{\text{Total de Divergências}}$ | $\frac{\text{Divergências onde Pred == DIRECT e Ref != DIRECT}}{\text{Total Geral de Divergências Observadas}}$ |
| **MET-05** | **Recall de PARTIAL** | $\ge 60{,}0\%$ | $\frac{\text{TP}_{\text{PARTIAL}}}{\text{TP}_{\text{PARTIAL}} + \text{FN}_{\text{PARTIAL}}}$ | $\frac{\text{Casos Ref PARTIAL previstos como PARTIAL}}{\text{Total de Casos na Referência PARTIAL}}$ |
| **MET-06** | **Invariância Homologada** | $\ge 80{,}0\%$ | $\frac{\sum_{p=1}^P \mathbb{I}(\hat{y}_{p,1} == \hat{y}_{p,2} == y_p)}{P}$ | $\frac{\text{Pares com Pred1 == Pred2 == Referência}}{\text{Total de Pares de Invariância Avaliados}}$ |
| **MET-07** | **Regressão Canônica** | Zero falhas | $\frac{\text{Testes Aprovados}}{\text{Total de Testes Executados}} == 1.0$ | $\frac{\text{Testes Unitários + Harness Aprovados}}{\text{Total de 1.038 Unit + 15 Harness Executados}}$ |

---

## 3. Especificação Detalhada da Métrica de Invariância de Representação

Para evitar a ambiguidade constatada na auditoria do Stage 31.7.22, a validação de invariância no Stage 31.7.25 reportará formalmente 3 indicadores separados:

### 3.1 Indicador A — Consistência Pura de Saída
Mede se a transformação linguística (formal vs. coloquial, ativa vs. passiva, conciso vs. detalhado) preserva a mesma classificação no motor, independentemente de ela estar correta em relação ao ground truth:
$$\text{Taxa de Consistência} = \frac{\text{Pares onde } \hat{y}_{p,1} == \hat{y}_{p,2}}{P}$$
*(Valor de referência histórico do Stage 31.7.21: 13/16 = 81,25%)*

### 3.2 Indicador B — Acurácia Individual dos Casos
Mede o percentual de acerto isolado em cada um dos membros individuais dos pares ($2P$ casos avaliados individualmente):
$$\text{Acurácia de Casos de Invariância} = \frac{\sum_{i=1}^{2P} \mathbb{I}(\hat{y}_i == y_i)}{2P}$$
*(Valor de referência histórico do Stage 31.7.21: 25/32 = 78,12%)*

### 3.3 Indicador C — Invariância Homologada (Critério MET-06)
Exige que ambas as formulações recebam a **mesma classificação** E que essa classificação corresponda **exatamente à referência humana adjudicada**:
$$\text{Invariância Homologada} = \frac{\text{Pares onde } \hat{y}_{p,1} == \hat{y}_{p,2} == y_p}{P}$$
*(Valor de referência histórico do Stage 31.7.21: 11/16 = 68,75%)*

**Regra Formal de Gate:** A meta $\ge 80{,}0\%$ aplica-se estritamente ao **Indicador C**. Um sistema que classifique consistentemente ambas as formulações de forma incorreta (ex: falso `DIRECT` em ambas) é contabilizado como **FALHA**.

---

## 4. Governança dos Conjuntos de Teste e Prevenção de Vazamento

1. **Benchmark Histórico Stage 31.7.21 (250 casos):** Permanece como **Benchmark de Diagnóstico e Regressão Semântica**. É expressamente proibido reutilizar esse arquivo como entrada para a validação cega do Stage 31.7.25.
2. **Benchmark Inédito Stage 31.7.25 ($\ge 250$ casos):** Deverá ser elaborado um novo conjunto de teste com zero sobreposição textual com todos os benchmarks anteriores (31.7.17, 31.7.21 e suítes de teste unitário).
3. **Selamento Criptográfico Pré-Execução:**
   - O ground truth do Stage 31.7.25 deve ser criado, auditado e selado com SHA-256 antes da geração das predições.
   - O script de predição consumirá unicamente o arquivo de entrada cega (`stage_31_7_25_blind_input.json`), desprovido de qualquer rótulo ou anotação semântica.
4. **Declaração de Independência:**
   Enquanto a adjudicação for realizada no ambiente de desenvolvimento de IA sem comitê externo duplo-cego, o status formal do benchmark deve ser mantido como:
   `REFERENCE_INDEPENDENCE_UNRESOLVED`

---

## 5. Protocolo de Resolução de Casos Ambíguos e Dados Ausentes

1. **Casos Ambíguos no Benchmark:** Qualquer pergunta ou resposta identificada como ambígua no ground truth deve possuir `has_ambiguity: true` e rationale explícito. Não é permitido descartar casos ambíguos a posteriori para inflar a concordância.
2. **Ausência de Denominador Válido:** Se em uma classe não houver predições emitidas (ex: denominador zero em precisão), a métrica deve ser reportada como `N/A` com justificativa formal e NÃO pode ser considerada aprovada por omissão.
3. **Inviolabilidade da Regressão Canônica:** Qualquer falha na suíte canônica de testes unitários ou no Reference Harness (15/15) resulta em bloqueio imediato (`GATE: BLIND_VALIDATION_BLOCKED_REGRESSION_FAILURE`), independentemente das métricas semânticas obtidas.
