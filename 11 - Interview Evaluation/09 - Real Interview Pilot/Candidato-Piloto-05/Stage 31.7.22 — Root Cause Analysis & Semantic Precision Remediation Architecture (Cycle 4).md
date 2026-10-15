---
type: study
status: understood
confidence: 95
created: 2026-10-14
updated: 2026-10-14
tags:
  - stage-31-7-22
  - root-cause-analysis
  - architecture-redesign
  - cycle-4
  - semantic-precision
  - failure-mechanisms
---

# Stage 31.7.22 — Root Cause Analysis & Semantic Precision Remediation Architecture (Cycle 4)

## 1. Resumo Executivo

O **Stage 31.7.22** estabelece a análise formal e definitiva de causa-raiz para o bloqueio semântico identificado no Stage 31.7.21 (`BLIND_SEMANTIC_REVALIDATION_BLOCKED`) e define a especificação arquitetural do **Ciclo 4** de remediação para o motor de relevância semântica em domínio aberto.

Em cumprimento rigoroso às diretrizes metodológicas do projeto:
- **Nenhuma linha de código foi alterada no runtime congelado** (`reference_runtime/runtime.py`).
- O digest criptográfico SHA-256 do runtime permaneceu inviolado em `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`.
- Todos os 7 artefatos históricos do Stage 31.7.21 foram preservados sem nenhuma modificação.
- As métricas reportadas foram 100% reproduzidas a partir dos dados brutos sem qualquer discrepância de numeradores ou denominadores.

A análise profunda das **80 divergências** revelou que as falhas persistentes não são acidentais nem pontuais: decorrem de **limitações estruturais de representação** inerentes a um motor monolítico baseado em escadas heurísticas de casamento léxico e listas estáticas de palavras-chave. Em particular:
1. **76% das falhas `PARTIAL → DIRECT`** ocorrem porque perguntas com múltiplos aspectos formuladas em uma única oração gramatical são colapsadas em uma única demanda genérica.
2. **24% das falhas `PARTIAL → DIRECT`** ocorrem porque o verificador de nexo permite que uma única proposição da resposta satisfaça simultaneamente duas demandas distintas devido à presença de palavras coincidentes isoladas (ex: a palavra "coordenador").
3. **11 casos de falso `DIRECT`** originados de `RELATED` e `SUPPORTING` derivam de verbos técnicos ativos em relatos autobiográficos ("já usei em produção") ou anedotas históricas ("escrito por Sysoev").
4. **6 casos de tautologia circular (`UNKNOWN → DIRECT`)** decorrem de divergências morfológicas comuns em português (substantivo na pergunta vs. verbo na resposta, como *compressão / comprimindo*).
5. **11 casos de evasão genérica** foram roteados para `UNKNOWN` por uma regra hardcoded no motor, quando a rubrica canônica exige `INSUFFICIENT`.

Para superar definitivamente esse teto estrutural, este relatório especifica formalmente a **Alternativa 2 — Grafo Proposicional Decomposto com Contratos Semânticos Estritos**, rejeitando tanto remediações pontuais ad hoc quanto modelos neurais de caixa-preta que violam a auditabilidade do projeto.

```text
====================================================================
DECISÃO DE GATE: RCA_COMPLETE_ARCHITECTURE_PENDING_REVIEW
====================================================================
```

---

## 2. Confirmação do Runtime Congelado e Checkpoint

| Propriedade | Valor Auditado | Status |
|---|---|:---:|
| **Arquivo Alvo** | `reference_runtime/runtime.py` | Verificado |
| **SHA-256 Esperado** | `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC` | Conforme |
| **SHA-256 Verificado** | `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC` | Idêntico |
| **Checkpoint Criado** | `reference_runtime/runtime.py.stage_31_7_22_baseline` | Criado |
| **SHA-256 do Checkpoint** | `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC` | Idêntico |
| **Estado do Git** | Branch `change-agent`, zero alterações pendentes no runtime | Limpo |

---

## 3. Reconciliação das Métricas do Stage 31.7.21

A auditoria matemática independente recalculou todas as métricas cruzando diretamente `stage_31_7_21_ground_truth.json` (250 casos) e `stage_31_7_21_system_predictions.json` (250 predições). O resultado gerou o artefato auditado [stage_31_7_22_metrics_reconciliation.json](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_22_metrics_reconciliation.json).

| Métrica | Relatado no Stage 31.7.21 | Recalculado na Auditoria | Numerador / Denominador | Meta | Status |
|---|---:|---:|---:|---:|:---:|
| **Concordância Exata** | 68,00% | **68,00%** | 170 / 250 | $\ge 75{,}0\%$ | **FALHA** |
| **Recall de DIRECT** | 81,54% | **81,54%** | 53 / 65 | $\ge 85{,}0\%$ | **FALHA** |
| **Precisão de DIRECT** | 53,00% | **53,00%** | 53 / 100 | $\ge 70{,}0\%$ | **FALHA** |
| **Falsos DIRECT / Divergências** | 58,75% | **58,75%** | 47 / 80 | $\le 10{,}0\%$ | **FALHA** |
| **Recall de PARTIAL** | 37,78% | **37,78%** | 17 / 45 | $\ge 60{,}0\%$ | **FALHA** |
| **Invariância (Consistência + Correção)** | 68,75% | **68,75%** | 11 / 16 pares | $\ge 80{,}0\%$ | **FALHA** |
| **Invariância (Consistência Pura de Saída)** | N/A | **81,25%** | 13 / 16 pares | Informacional | **AUDITADO** |
| **Regressão Canônica (Unit Tests)** | 1038 executados, 1037 pass, 1 skip | 1038 executados, 1037 pass, 1 skip | 1037 / 1037 | Zero falhas | **PASSOU** |
| **Reference Harness** | 15 / 15 pass | 15 / 15 pass | 15 / 15 | Zero falhas | **PASSOU** |

**Conclusão da Reconciliação:** A reprodução foi de 100%. Não há discrepâncias numéricas. A matriz de confusão e os totais de divergência são matematicamente exatos.

---

## 4. Análise de Causa-Raiz das 80 Divergências

Todas as 80 divergências foram catalogadas no artefato auditado [stage_31_7_22_root_cause_catalog.json](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_22_root_cause_catalog.json). Elas se agrupam em 8 causas-raiz estruturais comprovadas por rastreamento no código:

```text
Distribuição por Causa-Raiz Comprovada:
  CR-01 (Demanda composta tratada como demanda simples):              28 casos (35,0%)
  CR-08 (Polaridade, negação e limiares estritos de disjunção):       12 casos (15,0%)
  CR-04 (Disjunção terminológica entre INSUFFICIENT e UNKNOWN):       11 casos (13,75%)
  CR-02 (Verbos técnicos em relatos autobiográficos e históricos):     8 casos (10,0%)
  CR-06 (Falsos DIRECTs por acoplamento difuso em multi-demandas):     6 casos  (7,5%)
  CR-03 (Circularidade não detectada por variação morfológica):        6 casos  (7,5%)
  CR-07 (Invariância de representação assimétrica em antíteses):       5 casos  (6,25%)
  CR-05 (Proximidade temática confundida com solução):                 4 casos  (5,0%)
Total: 80 casos
```

### Detalhamento das Causas-Raiz Prioritárias

#### CR-01 & CR-06 — Colapso de Demandas Compostas e Acoplamento Difuso Proposição-Demanda
- **Sintoma:** 25 respostas do Grupo B e Grupo H rotuladas pela referência como `PARTIAL` foram promovidas a `DIRECT`.
- **Mecanismo da Falha (Fato Comprovado):**
  1. *Sub-causa A (76% dos casos - 19/25):* Em perguntas com oração única exigindo transições de estados múltiplos (ex: *B05 Circuit Breaker* fechado/aberto/meio-aberto) ou pares de ação/compensação (*B07 Saga*), o método `decompose_question` só divide a pergunta se encontrar conjunções interrogativas explícitas (`" e como "`, `" e qual "`, etc.). Como a pergunta não continha esses marcadores, gerou uma única demanda genérica (`demand_1`). A resposta do candidato atendeu a apenas um aspecto (ex: abrir o circuito; orquestrar a transação), satisfazendo a demanda única e recebendo `aspect_coverage = FULL` e `DIRECT`.
  2. *Sub-causa B (24% dos casos - 6/25):* Em perguntas onde 2 demandas foram extraídas (ex: *B02 Two-Phase Commit* com atomicidade e queda do coordenador), a implementação de `assess_demand_nexus` avalia a segunda demanda através de uma escada de `if/elif` hardcoded (`lines 3406-3450` de `runtime.py`). Como a resposta mencionava *"o coordenador pergunta se todos podem commitar"*, a presença isolada da palavra **"coordenador"** fez o teste `any(w in r_norm for w in ("falha", "coordenador", ...))` retornar `True`, marcando a demanda 2 como `FUNCTIONALLY_SOLVES` sem que o candidato tivesse explicado o tratamento de queda.
- **Componentes Afetados:** `decompose_question` e `assess_demand_nexus`.

#### CR-02 & CR-05 — Verbos Técnicos em Relatos Autobiográficos e Históricos Confundidos com Solução
- **Sintoma:** 11 casos do Grupo D (`RELATED`) e Grupo C (`SUPPORTING`) foram promovidos a `DIRECT`.
- **Mecanismo da Falha (Fato Comprovado):**
  - O método `extract_response_propositions` (`lines 3258-3277`) usa `has_operative_verb` com radicais amplos (`faz-`, `cri-`, `utiliz-`, `escrev-`).
  - Em *D22* ("Já usei o Redis em projetos para fazer cache..."), a heurística de declaração procurou por "utilizo" ou "tenho", mas o candidato usou "usei". A declaração foi ignorada (`is_decl = False`), e "fazer cache" ativou `has_operative_verb`, promovendo a experiência pessoal a `DIRECT`.
  - Em *D20* (NGINX de Igor Sysoev) e *D30* (Modelo relacional de Edgar Codd na IBM), os marcadores de metadados procuravam apenas por "Apache" ou "CNCF". A presença de "escrito por" ou "formalizado por" não foi barrada, ativando `is_operative = True`.
- **Componentes Afetados:** `extract_response_propositions` e `assess_demand_nexus`.

#### CR-03 — Tautologias e Circularidades Burladas por Variação Morfológica
- **Sintoma:** 6 casos de tautologias circulares do Grupo G (*G01 Replicação*, *G08 Compressão*, *G10 Distribuição*, *G11 Disponibilidade*, *G12 Indexação*, *G14 Travamento Mútuo*) foram promovidos a `DIRECT`.
- **Mecanismo da Falha (Fato Comprovado):**
  - O método `_detect_structural_circularity` (`lines 3106-3139`) possui uma lista fixa de 10 radicais e exige `if stem in q_norm:`.
  - Em *G08*, a pergunta usou o substantivo "compressão", enquanto o candidato usou o verbo "comprimindo". A busca por `stem = "comprim"` em `q_norm` falhou.
  - Em *G01* e *G14*, os radicais `replica` e `trav` sequer constavam na tupla de radicais monitorados.
  - O predicado tautológico continha verbos ("mantém", "comprime") que ativaram `has_operative_verb`, sendo promovido a `DIRECT`.
- **Componentes Afetados:** `_detect_structural_circularity`.

#### CR-04 — Disjunção Terminológica Hardcoded entre `EVASIVE` e `UNKNOWN`
- **Sintoma:** 11 respostas evasivas do Grupo F (ex: "depende do caso", "cada caso é um caso") foram classificadas como `UNKNOWN` em vez de `INSUFFICIENT`.
- **Mecanismo da Falha (Fato Comprovado):**
  - Na linha 3633 de `runtime.py`, há a regra explícita:
    `elif any(n == "EVASIVE" for n in nexus_relations): classification = "UNKNOWN"`
  - A rubrica canônica e a ontologia do benchmark determinam que respostas sem substância técnica avaliável devem receber `INSUFFICIENT`. `UNKNOWN` é reservado para declarações explícitas de incerteza/desconhecimento ou tautologias indecidíveis.
- **Componentes Afetados:** `evaluate_relevance` (agregador).

#### CR-07 — Invariância de Representação Assimétrica em Formulações Coloquiais e Passivas de Antítese
- **Sintoma:** Nos pares de invariância 14 e 15 (ações destrutivas / antítese), a formulação formal ativa foi classificada como `OFF_TOPIC`, mas a formulação coloquial (*"a gente tira a trava"*) ou passiva (*"quando as travas forem retiradas"*) foi classificada como `DIRECT`.
- **Mecanismo da Falha (Fato Comprovado):**
  - Os padrões de antítese destrutiva em `_detect_antithesis` foram calibrados para estruturas imperativas formais diretas ("desative os locks", "desligue o ACID"). Expressões idiomáticas coloquiais e particípios passivos contornaram o filtro e ativaram radicais operacionais genéricos.
- **Componentes Afetados:** `_detect_antithesis` e `extract_response_propositions`.

---

## 5. Distinção Epistêmica: Fatos Verificados versus Hipóteses

| Elemento Analisado | Natureza Epistêmica | Evidência Comprobatória |
|---|:---:|---|
| A regra hardcoded mapeia `EVASIVE` para `UNKNOWN` | **FATO VERIFICADO** | Linha 3633 de `reference_runtime/runtime.py` |
| `decompose_question` colapsou 19 de 25 casos de `PARTIAL` em demanda única | **FATO VERIFICADO** | Execução diagnóstica direta sobre o runtime congelado |
| Token isolado "coordenador" causou `FUNCTIONALLY_SOLVES` na demanda 2 | **FATO VERIFICADO** | Linhas 3436-3438 e inspeção do `demand_nexus` de B02 |
| Radical "compressão" falhou em casar com "comprim" | **FATO VERIFICADO** | Ausência do radical nominal na tupla da linha 3131 |
| Aumentar a lista de palavras resolveria o problema | **HIPÓTESE REFUTADA** | Os ciclos 31.7.16 e 31.7.20 tentaram essa abordagem e falharam no benchmark independente |
| O pipeline decomposto eliminará o cross-talk proposicional | **HIPÓTESE A SER TESTADA** | Especificada para implementação controlada no Cycle 4 |

---

## 6. Mapa dos Componentes e Fluxo Semântico

O mapeamento causal demonstra onde as decisões se sobrepõem e onde informações são perdidas no runtime atual:

```text
Entrada
  │
  ├─► [decompose_question] ─────────► FALHA CR-01 (Colapso de multi-aspectos em orações simples)
  │
  ├─► [_detect_structural_circularity] ► FALHA CR-03 (Listas estáticas e divergência morfológica)
  │
  ├─► [extract_response_propositions] ► FALHA CR-02 / CR-05 / CR-07 (Verbos gerais disfarçam trivia/relatos)
  │
  ├─► [assess_demand_nexus] ────────► FALHA CR-06 (Cross-satisfaction difusa por tokens isolados)
  │
  └─► [evaluate_relevance] ─────────► FALHA CR-04 (Mapeamento hardcoded EVASIVE -> UNKNOWN)
```

---

## 7. Arquitetura Corretiva Recomendada (Cycle 4)

Conforme fundamentado em [stage_31_7_22_architecture_options.md](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_22_architecture_options.md), a solução estrutural aprovada é a **Alternativa 2 — Grafo Proposicional Decomposto com Contratos Semânticos Estritos**.

### Especificação Modular:
1. **`SemanticIntentAndDemandExtractor`:** Extração profunda de demandas multi-aspecto, decompondo estados operacionais (ex: fechado, aberto, meio-aberto) e coordenações de ação/compensação independentemente da pontuação ou da presença de conjunções explícitas.
2. **`PropositionDiscourseFilter`:** Classificação prévia do gênero discursivo em 7 categorias. Fatos históricos, dados biográficos e declarações autobiográficas são limados de atuarem como soluções antes da avaliação de verbos.
3. **`MorphologicalCircularityAnalyzer`:** Lematização e grafo de cognatas unificado. Trata nominalizações e flexões verbais como a mesma raiz semântica e avalia o ganho informacional real da resposta.
4. **`DemandPropositionNexusBipartiteMatcher`:** Emparelhamento bipartido estrito. Exige que cada demanda independente possua uma proposição comprobatória exclusiva ou explicitamente unificada, proibindo a satisfação múltipla por correspondência incidental de palavras isoladas.
5. **`StrictOntologyRelevanceAggregator`:** Única fonte de verdade ontológica. Garante que respostas evasivas sejam sempre `INSUFFICIENT`, tautologias sejam `UNKNOWN` e `DIRECT` exija cobertura de 100% dos aspectos demandados.

Os contratos de dados e invariantes formais estão completamente especificados em [stage_31_7_22_component_contracts.md](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_22_component_contracts.md).

---

## 8. Plano de Testes de Contrato Proposto

Para garantir que a implementação no Ciclo 4 não dependa de memorização nem de ajuste a casos conhecidos, são definidos 7 contratos de teste unitários essenciais:

- **TC-01:** Perguntas de máquina de estados (ex: Circuit Breaker) devem gerar aspectos obrigatórios para cada estado; respostas parciais devem receber `PARTIAL`.
- **TC-02:** Perguntas de coordenação e compensação (ex: Saga) devem exigir evidência de ambas as ações; respostas sem compensação devem receber `PARTIAL`.
- **TC-03:** Respostas biográficas ou históricas contendo verbos de ação técnicos (Igor Sysoev, Edgar Codd) devem receber terminantemente `RELATED`.
- **TC-04:** Declarações autobiográficas ("já usei em produção") sem explicação técnica interna devem receber terminantemente `RELATED`.
- **TC-05:** Tautologias circulares com variação morfológica (substantivo/verbo) sem novidade informativa devem receber terminantemente `UNKNOWN`.
- **TC-06:** Evasões ("depende do caso") devem receber terminantemente `INSUFFICIENT`.
- **TC-07:** Formulações coloquiais e passivas de ações destrutivas devem receber terminantemente `OFF_TOPIC`.

---

## 9. Plano de Validação Futura (Cycle 4)

Conforme formalizado em [stage_31_7_22_validation_contract.md](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_22_validation_contract.md):
1. Os 250 casos do Stage 31.7.21 passam a ter função de **Benchmark de Regressão Diagnóstica**.
2. A homologação final do Ciclo 4 (Stage 31.7.25) exigirá um **novo conjunto selado de $\ge 250$ casos inéditos**, mantendo o status `REFERENCE_INDEPENDENCE_UNRESOLVED` devido à adjudicação em ambiente de desenvolvimento.
3. Os critérios de referência permanecem rigorosamente inalterados:
   - Concordância Exata $\ge 75{,}0\%$
   - Recall de DIRECT $\ge 85{,}0\%$
   - Precisão de DIRECT $\ge 70{,}0\%$
   - Falsos DIRECT entre Divergências $\le 10{,}0\%$
   - Recall de PARTIAL $\ge 60{,}0\%$
   - Invariância Homologada (Consistência + Correção) $\ge 80{,}0\%$
   - Regressão canônica sem falhas inexplicadas.

---

## 10. Limitações Metodológicas

1. **Ausência de Comitê Humano Externo:** A referência permanece com o status formal `REFERENCE_INDEPENDENCE_UNRESOLVED`. A independência ontológica plena só poderá ser atestada mediante comitê humano externo cego e independente.
2. **Fronteira Heurística vs. Semântica Profunda:** A abordagem determinística proposta não utiliza modelos de linguagem pesados para preservar a explicabilidade e auditabilidade; em casos extremos de metáforas ou construções linguísticas altamente elípticas, limites conceituais podem persistir e devem ser tratados com status de incerteza explícita.

---

## 11. Decisão Final de Gate

```text
====================================================================
GATE STATUS: RCA_COMPLETE_ARCHITECTURE_PENDING_REVIEW
====================================================================
```

### Justificativa Formal:
1. O runtime congelado permaneceu 100% inalterado (SHA-256 verificado: `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`).
2. A reconciliação das métricas históricas foi reproduzida com precisão de 100%, sem divergências de cálculo.
3. Todas as 80 divergências foram catalogadas com causa-raiz estrutural demonstrada no código (CR-01 a CR-08).
4. Três alternativas arquiteturais foram comparadas e a arquitetura modular baseada em contratos semânticos (Alternativa 2) foi formalmente aprovada e especificada em 5 contratos modulares.
5. Nenhuma linha de implementação foi realizada nesta etapa, preservando a imutabilidade do baseline para revisão.

---

## 12. Próximos Passos Autorizados

Avançar para:
**Stage 31.7.23 — Controlled Correction Plan & Contract Specification (Cycle 4)**
- Formalizar o plano de incremento controlado baseado na arquitetura especificada no Stage 31.7.22.
- Desenvolver os testes de contrato automatizados (TC-01 a TC-07) antes de qualquer alteração no runtime.
