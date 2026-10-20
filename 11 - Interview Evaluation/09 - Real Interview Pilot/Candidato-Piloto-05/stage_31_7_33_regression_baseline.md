# Stage 31.7.33 — Baseline de Regressão e Métricas Diagnósticas

## 1. Contexto e Demarcação Epistemológica

Este documento estabelece o protocolo de comparação entre o runtime histórico e a nova implementação do Ciclo 6, definindo métricas preservadas, critérios de bloqueio e salvaguardas contra manipulação de gabaritos ou conclusões prematuras.

> **DEMARCAÇÃO FUNDAMENTAL:**
> Os resultados históricos reportados no Stage 31.7.28 pertencem estritamente àquele ciclo avaliativo. Eles constituem uma **ferramenta de diagnóstico de regressão**, e **NÃO** representam uma prova de validação independente nem uma meta que autorize ajustes ad-hoc de código ou de gabarito para "forçar aprovação".

---

## 2. Resultados Históricos de Referência (Stage 31.7.28)

| Métrica Diagnóstica | Valor Histórico (31.7.28) | Papel no Ciclo 6 |
|---|:---:|---|
| **Tamanho da Amostra Diagnóstica** | 250 casos | Diagnóstico comparativo de regressão |
| **Acurácia Exata Global** | 67,20% (168/250) | Métrica diagnóstica secundária |
| **Recall da Classe DIRECT** | 76,00% | Métrica de sensibilidade funcional |
| **Precisão da Classe DIRECT** | 52,78% | Métrica crítica (alvo de melhoria estrutural) |
| **Taxa de Falsos DIRECT nas Divergências** | 41,46% | Métrica de auditoria causal de sobrelevação |
| **Recall da Classe PARTIAL** | 84,44% | Métrica diagnóstica de completude |
| **Paired Invariance (Invariância Pareada)** | 65,00% | Métrica de robustez discursiva |
| **Status da Independência do Benchmark** | `UNRESOLVED` | Ressalva metodológica ativa e imutável |

---

## 3. Classificação das Métricas e Critérios de Bloqueio

### 3.1. Métricas Bloqueantes (Gate de Progressão)
A violação de qualquer um dos seguintes critérios bloqueia categoricamente a aceitação da implementação no Ciclo 6:
1. **Regressão Canônica do Projeto:**
   - Suíte Unitária Canônica (1.047 testes): Deve manter exatamente 1.046 OK, 1 skipped e **0 falhas/erros**.
   - Reference Harness (15 testes): Deve manter **15/15 OK (100%)**.
2. **Contratos Semânticos (35 Contratos):**
   - Cobertura obrigatória de **35/35 (100%)** dos contratos formais sem exceções de código.
3. **Casos Adversariais de Estresse (15 Cenários):**
   - Cobertura obrigatória de **15/15 (100%)** dos cenários ADV-01 a ADV-15.
4. **Integridade da Rastreabilidade:**
   - 100% das predições devem emitir o registro JSON `EvidenceTraceabilityRecord` em conformidade com o schema Draft-07.

### 3.2. Métricas Diagnósticas e Analíticas (Não Bloqueantes)
As métricas globais sobre os 250 casos históricos (acurácia global, recall e precisão) serão calculadas exclusivamente para fins de diagnóstico comparativo de evolução arquitetural.
- Uma eventual variação na acurácia global decorrente da reclassificação legítima de casos limítrofes entre `RELATED`, `SUPPORTING` e `INSUFFICIENT` não constitui por si só motivo de bloqueio, desde que a decisão seja rastreável e defensável sob os contratos formais.
- É terminantemente proibido reajustar thresholds, alterar gabaritos ou introduzir regras lexicais para inflar a acurácia global do benchmark diagnóstico.

---

## 4. Salvaguardas contra Comparação Indevida e Contaminação
1. **Gabaritos Congelados:** O arquivo de referência histórica não será editado em hipótese alguma.
2. **Ambiente Limpo:** Cada execução diagnóstica consumirá a entrada pura do benchmark e gerará artefatos de predição identificados com timestamp e hash do runtime avaliado.
3. **Proibição de Overfitting por Gabarito:** Se o runtime divergir do gabarito histórico, a divergência será auditada para verificar se o runtime acertou ou se houve falha conceitual, preservando a honestidade epistemológica do projeto.
