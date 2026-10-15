---
type: reference
status: study
confidence: 95
created: 2026-10-14
updated: 2026-10-14
tags:
  - stage-31-7-22
  - validation-contract
  - metrics-specification
  - cycle-4
---

# Stage 31.7.22 — Contrato de Validação Futura e Critérios de Homologação (Cycle 4)

## 1. Objetivo do Contrato de Validação

Este documento estabelece as regras formais, os critérios quantitativos imutáveis e as definições matemáticas de numeradores e denominadores para os próximos estágios do Ciclo 4:
- **Stage 31.7.23:** Plano de Correção Controlada e Especificação de Testes de Contrato.
- **Stage 31.7.24:** Implementação Controlada dos 5 Componentes Desacoplados.
- **Stage 31.7.25:** Revalidação Semântica Cega e Independente do Runtime Refatorado.

O objetivo é impedir a flexibilização a posteriori de metas e garantir que o benchmark do Stage 31.7.21 seja preservado como evidência diagnóstica histórica, sem vazamento para o conjunto de teste de homologação do Ciclo 4.

---

## 2. Critérios Quantitativos de Homologação (Cycle 4)

| Métrica de Aceite | Limiar Mínimo Exigido | Definição Matemática | Numerador / Denominador |
|---|:---:|---|---|
| **Concordância Exata** | $\ge 75{,}0\%$ | Casos com classe prevista estritamente igual à referência humana | $\frac{\text{Acertos Exatos}}{\text{Total de Casos Elegíveis}}$ |
| **Recall de DIRECT** | $\ge 85{,}0\%$ | Casos de referência `DIRECT` previstos como `DIRECT` | $\frac{\text{TP}_{\text{DIRECT}}}{\text{Total de Referência DIRECT}}$ |
| **Precisão de DIRECT** | $\ge 70{,}0\%$ | Predições `DIRECT` confirmadas pela referência humana | $\frac{\text{TP}_{\text{DIRECT}}}{\text{Total de Predições DIRECT}}$ |
| **Falsos DIRECT entre Divergências** | $\le 10{,}0\%$ | Divergências onde o sistema previu indevidamente `DIRECT` | $\frac{\text{FP}_{\text{DIRECT}}}{\text{Total de Divergências Observadas}}$ |
| **Recall de PARTIAL** | $\ge 60{,}0\%$ | Casos de referência `PARTIAL` previstos como `PARTIAL` | $\frac{\text{TP}_{\text{PARTIAL}}}{\text{Total de Referência PARTIAL}}$ |
| **Invariância de Representação** | $\ge 80{,}0\%$ | Pares equivalentes com predições consistentes E semanticamente corretas | $\frac{\text{Pares Consistentes e Corretos}}{\text{Total de Pares Avaliados}}$ |
| **Regressão Canônica** | Zero falhas inexplicadas | 100% dos testes unitários e Reference Harness aprovados | $\frac{\text{Testes Aprovados}}{\text{Total de Testes Executados}}$ |

---

## 3. Especificação do Cálculo de Invariância de Representação

Conforme demandado pela auditoria do Stage 31.7.22, a invariância deve ser reportada separando duas grandezas distintas:

### A. Consistência de Saída do Par (Invariância Pura de Representação)
Mede se o sistema atribui o **mesmo rótulo** a ambas as formulações linguísticas do par (ex: formal vs. coloquial, ativa vs. passiva), independentemente de o rótulo estar correto:
$$\text{Consistência} = \frac{\sum_{i=1}^{N} \mathbb{I}(\text{Pred}_1^{(i)} == \text{Pred}_2^{(i)})}{N}$$

### B. Correção Semântica do Par (Invariância Homologada)
Mede se o sistema é consistente **E** semanticamente correto em relação à referência humana adjudicada:
$$\text{Invariância Homologada} = \frac{\sum_{i=1}^{N} \mathbb{I}(\text{Pred}_1^{(i)} == \text{Pred}_2^{(i)} == \text{Ref}^{(i)})}{N}$$

**Regra de Aceite:** O critério de $\ge 80{,}0\%$ aplica-se estritamente à **Invariância Homologada (B)**. Um sistema consistentemente incorreto (ex: prevendo `DIRECT` para ambas as versões de uma resposta que é `PARTIAL`) é computado como **FALHA** no aceite final.

---

## 4. Preservação de Dados Históricos e Prevenção de Overfitting

1. **Status do Benchmark Stage 31.7.21:** O arquivo `stage_31_7_21_ground_truth.json` (250 casos) passa a ter status de **Benchmark Diagnóstico de Regressão Semântica**.
2. **Proibição de Vazamento:** O conjunto de dados do Stage 31.7.21 NÃO poderá ser reutilizado como teste cego no Stage 31.7.25.
3. **Novo Benchmark Cego Inédito (Stage 31.7.25):** Para a homologação do Ciclo 4, um novo conjunto selado de $\ge 250$ casos inéditos deverá ser elaborado e adjudicado antes da execução cega.
4. **Independência Metodológica:** Enquanto a adjudicação for realizada no ambiente de desenvolvimento de IA sem comitê humano externo desvinculado, o status formal DEVE ser mantido como:
   `REFERENCE_INDEPENDENCE_UNRESOLVED`

---

## 5. Requisitos para Testes de Contrato da Implementação

Durante o Stage 31.7.23 e 31.7.24, deverão ser construídos testes de contrato unitários cobrindo as 5 causas-raiz principais:

1. **TC-01 (Decomposição de Estados em Frase Simples):** Pergunta sobre Circuit Breaker fechado/aberto/meio-aberto deve gerar 3 aspectos obrigatórios; resposta cobrindo apenas 2 estados deve receber deterministicamente `PARTIAL`.
2. **TC-02 (Desacoplamento de Ação e Compensação):** Pergunta sobre Saga com coordenação e compensação deve exigir evidência de ambos; resposta sem compensação deve receber `PARTIAL`.
3. **TC-03 (Desqualificação de Fatos Históricos):** Respostas sobre biografia de autores (Igor Sysoev, Edgar Codd) contendo verbos técnicos devem receber terminantemente `RELATED`, nunca `DIRECT`.
4. **TC-04 (Desqualificação de Relato Autobiográfico):** Respostas declarando experiência ("já usei em produção", "subimos pods diariamente") sem mecanismo interno devem receber terminantemente `RELATED`, nunca `DIRECT`.
5. **TC-05 (Detecção de Circularidade Morfológica):** Respostas tautológicas com variação entre substantivo e verbo (ex: replicação/replicar, compressão/comprimir, travamento/travar) sem novidade informativa devem receber terminantemente `UNKNOWN`.
6. **TC-06 (Mapeamento Ontológico de Evasão):** Respostas vagas ("depende do caso", "cada caso é um caso") devem receber terminantemente `INSUFFICIENT`, nunca `UNKNOWN`.
7. **TC-07 (Invariância em Ações Destrutivas):** Formulações coloquiais e passivas de remoção de proteções operacionais devem receber terminantemente `OFF_TOPIC` (antítese destrutiva).
