# Stage 31.7.28 — Plano de Revalidação Semântica Cega e Independente (Ciclo 5)

## 1. Identificação do Estágio e Runtime sob Teste

- **Estágio:** Stage 31.7.28 — Independent Blind Semantic Revalidation (Cycle 5)
- **Objetivo Metodológico:** Executar auditoria de validação cega sobre o runtime remediado no Stage 31.7.27, avaliando se a nova arquitetura de disjunção semântica de domínio sustenta a drástica redução de falsos `DIRECT` e preserva a integridade discriminatória das sete classes canônicas em uma massa de casos 100% inédita.
- **Runtime Canônico Auditado:** `reference_runtime/runtime.py`
- **SHA-256 Autorizado e Congelado:**
  $$\textbf{6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28}$$
- **Snapshot de Backup Homologado:**
  `reference_runtime/runtime.py.stage_31_7_27_final` (SHA-256: `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28`)
- **Snapshot Histórico Intermediário Pré-Ajustes Canônicos:**
  `reference_runtime/runtime.py.stage_31_7_27_pre_regression_fix` (SHA-256: `3FD3F80D9BB8A13CCC3A2791759D08F2EED25271913B56F064710DB94B2BC229`)
- **Regra de Congelamento:** O runtime não receberá qualquer edição de código, ajuste de limiar, dicionário ou lógica inferencial durante este estágio.

---

## 2. Reconciliação dos Objetivos do Ciclo 5 e Riscos Auditados

O Stage 31.7.26 demonstrou que a versão anterior falhou com 70 falsos `DIRECT` devido à permissividade do fallback incondicional de domínio aberto da linha 3434. O Stage 31.7.27 remediou essa falha estrutural por meio de 5 incrementos arquiteturais.

A presente validação cega foi planejada para auditar se:
1. **Disjunção Radical de Domínio:** O `SemanticDomainDisjunctionEngine` rejeita com robustez respostas de domínios alienígenas (culinária, botânica, agricultura, mecânica, esportes, literatura) classificando-as como `OFF_TOPIC`, sem exigir catálogos exaustivos.
2. **Metadados Institucionais e Curiosidades:** Respostas que apenas descrevem licenças, fundações mantenedoras ou popularidade de mercado são corretamente delimitadas como `RELATED`, não sendo infladas para `DIRECT`.
3. **Observabilidade Instrumental:** Respostas que mencionam dashboards, métricas e alertas (Prometheus, Grafana, Datadog) sem resolver a falha de concorrência ou particionamento são ancoradas em `SUPPORTING`.
4. **Demandas Compostas Multiaspecto:** Perguntas que exigem 2 ou mais mecanismos obrigatórios recebem `PARTIAL` quando apenas uma demanda é atendida, e `DIRECT` apenas quando todas são plenamente satisfeitas (com suporte legítimo a proposições densas unificadas).
5. **Definições Conceituais e Suficiência Relativa à Intenção:** Perguntas conceituais (Idempotência, Inversão de Dependência) e comparativas (Processo vs Thread) recebem `DIRECT` por mérito explicativo sem a exigência artificial de código de implementação ou telemetria.
6. **Invariância de Representação:** Variações sintáticas de voz ativa, passiva sintética/analítica, formulações coloquiais de engenharia e paráfrases mantêm consistência e correção estritas.
7. **Detecção de Antítese Destrutiva:** Tentativas de resolver problemas desativando travas e garantias operacionais fundamentais (locks, WAL, fsync, autenticação) são rigorosamente vetadas como `OFF_TOPIC`.
8. **Detecção de Tautologias e Incerteza:** Tautologias circulares e enunciados genuinamente ambíguos são classificados como `UNKNOWN` sem vazamento para `DIRECT`.

---

## 3. Protocolo de Cegamento e Isolamento de Dados

Para garantir a validade científica e metodológica da avaliação:

1. **Separação Estrutural de Arquivos:**
   - `stage_31_7_28_ground_truth.json`: Contém os 250 casos com perguntas, respostas, classes de referência humanas adjudicadas, justificativas semânticas e metadados linguísticos.
   - `stage_31_7_28_blind_input.json`: Contém **estritamente** os identificadores opacos (`VAL-31-7-28-001` a `VAL-31-7-28-250`), `question_text` e `response_text`. Nenhuma menção a classes, intenções esperadas ou justificativas é exposta ao executor.
   - `stage_31_7_28_system_predictions.json`: Armazena as predições geradas exclusivamente a partir da entrada cega.
   - `stage_31_7_28_metrics_summary.json` e `stage_31_7_28_confusion_matrix.json`: Gerados por um módulo comparador independente após a conclusão total da inferência.
2. **Auditoria de Sobreposição:** O conjunto de 250 casos é verificado contra todos os benchmarks anteriores (Stages 31.7.6, 31.7.13, 31.7.17, 31.7.21, 31.7.25) e suítes contratuais para assegurar ausência de contaminação textual.
3. **Declaração de Proveniência:** Como as referências foram formalizadas internamente sem comitê duplo-cego externo independente, a ressalva metodológica `REFERENCE_INDEPENDENCE_UNRESOLVED` é mantida com honestidade intelectual em todos os relatórios.

---

## 4. Estrutura e Famílias Semânticas do Benchmark (250 Casos)

O dataset cobre as 7 classes canônicas e as 22 famílias semânticas obrigatórias:

| Classe Canônica | Meta de Casos | Percentual | Propósito Principal na Validação |
|---|:---:|:---:|---|
| **`DIRECT`** | 50 | 20,0% | Avaliar atendimento pleno funcional sem exigir sobreposição lexical; definições conceituais e respostas densas |
| **`PARTIAL`** | 45 | 18,0% | Avaliar decomposição de perguntas compostas multiaspecto e atendimento parcial comprovado |
| **`SUPPORTING`** | 30 | 12,0% | Avaliar papéis auxiliares de instrumentação, métricas e observabilidade sem resolução direta |
| **`RELATED`** | 35 | 14,0% | Avaliar metadados institucionais, história de produto, categorias gerais e declarações biográficas |
| **`OFF_TOPIC`** | 45 | 18,0% | Avaliar disjunção ontológica radical (outros domínios) e antítese destrutiva de garantias operacionais |
| **`INSUFFICIENT`** | 25 | 10,0% | Avaliar evasão discursiva, orçamentária e respostas vazias que não atingem evidência técnica |
| **`UNKNOWN`** | 20 | 8,0% | Avaliar tautologias reflexivas circulares e enunciados genuinamente ambíguos/indeterminados |
| **TOTAL** | **250** | **100,0%** | **Distribuição balanceada e desafiadora para todas as classes** |

### 4.1. Grupo de Invariância de Representação (Grupo O)
- **Quantidade:** 20 pares de sentenças (40 casos no total).
- **Variações:** Voz ativa vs. passiva, formal vs. coloquial, concisa vs. estendida, inversão oracional e paráfrases funcionais idênticas.

---

## 5. Critérios Formais de Aceitação e Fórmulas

Os critérios de aceite homologados no Stage 31.7.23 e reafirmados no Stage 31.7.26 permanecem inalterados:

| Indicador | Critério Alvo | Fórmula Matemática |
|---|:---:|---|
| **Acurácia Exata Global** | $\ge 75,0\%$ | $\frac{\text{Acertos Totais}}{250}$ |
| **Recall de `DIRECT`** | $\ge 85,0\%$ | $\frac{TP_{DIRECT}}{\text{Total Referências } DIRECT}$ |
| **Precisão de `DIRECT`** | $\ge 70,0\%$ | $\frac{TP_{DIRECT}}{\text{Total Predições } DIRECT}$ |
| **Falsos DIRECT entre Divergências** | $\le 10,0\%$ | $\frac{FP_{DIRECT}}{\text{Total de Divergências}}$ |
| **Recall de `PARTIAL`** | $\ge 60,0\%$ | $\frac{TP_{PARTIAL}}{\text{Total Referências } PARTIAL}$ |
| **Invariância Pareada Simultaneamente Correta** | $\ge 80,0\%$ | $\frac{\text{Pares com Predições Iguais E Ambas Corretas}}{20}$ |
| **Regressões Canônicas Inexplicadas** | **0** | Suíte canônica (1.047 testes) e Reference Harness (15 testes) |

---

## 6. Protocolo de Auditoria Individual de Divergências

Cada divergência observada entre a predição cega e a referência congelada será documentada em `stage_31_7_28_divergence_analysis.json` contendo:
- ID do caso;
- Pergunta e resposta;
- Classe de referência e classe predita;
- Família semântica;
- Mecanismo causal da divergência obtido da trilha de telemetria;
- Grau de certeza e classificação do erro (viés do motor vs. ambiguidade de adjudicação).
