---
type: study
status: understood
confidence: 95
created: 2026-10-14
updated: 2026-10-14
tags:
  - stage-31-7-23
  - correction-plan
  - component-contracts
  - cycle-4
  - architecture-specification
  - formal-plan
---

# Stage 31.7.23 — Controlled Correction Plan & Contract Specification (Cycle 4)

## 1. Resumo Executivo

O presente documento consolida o planejamento formal e a especificação contratual do **Ciclo 4** de remediação semântica do motor de avaliação de entrevistas em domínio aberto.

Com base no diagnóstico exaustivo estabelecido no Stage 31.7.22 — que confirmou 100% de reprodutibilidade matemática das métricas do Stage 31.7.21 e catalogou 80 divergências estruturais (CR-01 a CR-08) —, esta etapa transforma a arquitetura conceitual aprovada (**Alternativa 2 — Grafo Proposicional Decomposto com Contratos Semânticos Estritos**) em uma especificação executável, modular e auditável.

**Compromissos Metodológicos Desta Etapa:**
- **Zero Linhas de Código Alteradas no Runtime:** O arquivo [reference_runtime/runtime.py](file:///d:/Projetos/TechLens/reference_runtime/runtime.py) permaneceu 100% congelado sob o digest criptográfico auditado `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`.
- **Zero Modificações em Testes Existentes:** A suíte canônica de 1.038 testes unitários e o Reference Harness (15 testes) permanecem inalterados e protegidos.
- **Isolamento de Evidências:** Os artefatos históricos dos Stages 31.7.21 e 31.7.22 foram auditados e mantidos intocados.
- **Não-Proliferação de Heurísticas Ad Hoc:** Rejeita-se categoricamente a expansão de listas estáticas de palavras ou verbos. A correção atua sobre a estrutura da representação, através de 5 componentes especializados com contratos tipados e imutáveis.

```text
====================================================================
DECISÃO DE GATE: CORRECTION_PLAN_READY_FOR_CONTROLLED_IMPLEMENTATION
====================================================================
```

O plano estabelece 5 incrementos de implementação sequenciais (A a E), define 16 invariantes semânticos testáveis, formaliza 7 testes de contrato (TC-01 a TC-07) e congela as regras e limiares de validação independente para o Stage 31.7.25.

---

## 2. Baseline Imutável e Hashes Criptográficos

Antes de qualquer especificação, a integridade do baseline foi verificada via SHA-256 e um checkpoint formal foi estabelecido:

| Componente | Caminho do Arquivo | SHA-256 Auditado | Conformidade |
|---|---|---|:---:|
| **Runtime de Referência** | `reference_runtime/runtime.py` | `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC` | Idêntico |
| **Checkpoint do Baseline** | `reference_runtime/runtime.py.stage_31_7_23_baseline` | `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC` | Idêntico |
| **Ground Truth Stage 31.7.21** | `stage_31_7_21_ground_truth.json` | `D594BB067FE0A031720F75B416AB636D57D280D7E00E279557D9C8D8C6D120F6` | Idêntico |
| **Predições Stage 31.7.21** | `stage_31_7_21_system_predictions.json` | `577B308CA7FB3C827FF04776779E6E1C5916565982ED059B986E295B9958E168` | Idêntico |
| **Catálogo de RCA Stage 31.7.22** | `stage_31_7_22_root_cause_catalog.json` | `EE711719DADAC102086ACA8C21B9EAE0F1A7DB74C12B74C7BEC5DCFAE96963D5` | Idêntico |
| **Reconciliação Stage 31.7.22** | `stage_31_7_22_metrics_reconciliation.json` | `DFD17C7D5C1D1086408CC8CB8B9C18B446C04BF732CBDA6C21B750F38379B156` | Idêntico |

---

## 3. Reconciliação do Diagnóstico: Causas-Raiz Consideradas

O plano de remediação aborda sistematicamente as 8 causas-raiz catalogadas no Stage 31.7.22:

```text
Distribuição de Impacto das Causas-Raiz no Benchmark Inédito:
┌─────────────────────────────────────────────────────────────────────────────┐
│ CR-01: Demanda composta tratada como simples em orações únicas    (28 casos)│
│ CR-08: Polaridade, escopo de negação e limiares de disjunção       (12 casos)│
│ CR-04: Mapeamento hardcoded EVASIVE -> UNKNOWN em vez de INSUFFICIENT(11 c.)│
│ CR-02: Verbos técnicos em relatos autobiográficos e históricos    ( 8 casos)│
│ CR-06: Acoplamento difuso em multi-demandas via token isolado     ( 6 casos)│
│ CR-03: Tautologias circulares não capturadas por divergência morfológica(6) │
│ CR-07: Invariância assimétrica em antíteses coloquiais/passivas   ( 5 casos)│
│ CR-05: Proximidade temática e metadados promovidos a DIRECT       ( 4 casos)│
└─────────────────────────────────────────────────────────────────────────────┘
Total: 80 divergências históricas
```

### Síntese Mecânica das Falhas:
1. **CR-01 & CR-06:** Perguntas com múltiplos requisitos (ex: estados de Circuit Breaker ou coordenação/compensação de Saga) eram reduzidas a uma única demanda por ausência de conectivos interrogativos explícitos ("e como"). Em perguntas onde 2 demandas eram extraídas, a presença incidental de uma única palavra ("coordenador") no texto satisfazia ambas as demandas.
2. **CR-02 & CR-05:** Verbos de ação comuns ativavam radicais operacionais amplos (`faz-`, `cri-`, `utiliz-`) em contextos puramente históricos (Sysoev, Codd) ou autobiográficos ("já usei em produção"), promovendo contexto a solução técnica.
3. **CR-03:** A verificação estática de radicais falhava em unificar substantivos na pergunta com verbos na resposta (*compressão / comprimindo*), promovendo circularidades a `DIRECT`.
4. **CR-04:** Uma regra explícita na linha 3633 mapeava respostas com `is_evasive == True` para `UNKNOWN`, quando a ontologia canônica exige `INSUFFICIENT`.
5. **CR-07:** Formulações coloquiais e na voz passiva de ações perigosas contornavam padrões imperativos de antítese e eram promovidas a `DIRECT`.

---

## 4. Arquitetura Aprovada e Pipeline Decomposto

A arquitetura formalizada no documento [stage_31_7_23_component_contracts.md](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_23_component_contracts.md) desacopla o monolítico `OpenDomainPropositionEngine` em 5 componentes especializados:

```text
Entrada: (question_text, response_text)
                  │
                  ▼
┌────────────────────────────────────────────────────────┐
│ 1. SemanticIntentAndDemandExtractor                    │  --> Resolve CR-01 & CR-06
│    Decompõe intenção, demandas atômicas e aspectos      │
└────────────────────────────────────────────────────────┘
                  │ QuestionAnalysis
                  ▼
┌────────────────────────────────────────────────────────┐
│ 2. PropositionDiscourseFilter                          │  --> Resolve CR-02, CR-05 & CR-08
│    Classifica gênero discursivo em 7 categorias         │
└────────────────────────────────────────────────────────┘
                  │ tuple[FilteredProposition, ...]
                  ▼
┌────────────────────────────────────────────────────────┐
│ 3. MorphologicalCircularityAnalyzer                    │  --> Resolve CR-03
│    Unifica lemas e avalia ganho informacional          │
└────────────────────────────────────────────────────────┘
                  │ CircularityEvaluation
                  ▼
┌────────────────────────────────────────────────────────┐
│ 4. DemandPropositionNexusBipartiteMatcher              │  --> Resolve CR-01, CR-06 & CR-07
│    Valida emparelhamento 1-para-1 demanda/proposição    │
└────────────────────────────────────────────────────────┘
                  │ tuple[DemandNexusResult, ...]
                  ▼
┌────────────────────────────────────────────────────────┐
│ 5. StrictOntologyRelevanceAggregator                   │  --> Resolve CR-04 & Agregação
│    ÚNICA fonte de verdade para a classificação final   │
└────────────────────────────────────────────────────────┘
                  │
                  ▼
Saída: EvaluationResult (7 Classes Canônicas + Trilha Auditável)
```

---

## 5. Ontologia Canônica e Critérios de Classificação

O sistema opera estritamente sobre as **sete classes canônicas**, com fronteiras conceituais explícitas e contrastivas:

| Classe | Critério Operacional Rígido | Exemplo Positivo Típico | Exemplo Negativo Contrastivo |
|---|---|---|---|
| **`DIRECT`** | Satisfaz integralmente a demanda primária e todos os aspectos obrigatórios com mecanismo operacional comprovado. | Explica os 3 estados do Circuit Breaker (fechado, aberto, meio-aberto) e suas transições. | Explica apenas a abertura do circuito, omitindo meio-aberto (`PARTIAL`). |
| **`PARTIAL`** | Atende a um aspecto técnico substantivo, mas omite outro aspecto primário obrigatório da pergunta. | Explica a orquestração de transações locais na Saga, mas omite transações compensatórias. | Resposta vaga sem explicar nenhum mecanismo com precisão (`INSUFFICIENT`). |
| **`SUPPORTING`** | Apresenta telemetria, instrumentação ou métricas úteis, mas não resolve diretamente o mecanismo da falha. | Configura dashboards no Grafana e alertas de deadlock no Datadog. | Afirma apenas que "gosta de monitorar sistemas" (`RELATED`). |
| **`RELATED`** | Menciona a tecnologia, contexto institucional, biografia de criadores ou relato pessoal sem mecanismo resolutivo. | Declara que "já usou Redis em vários projetos" ou cita que "NGINX foi criado por Sysoev". | Descreve uma tecnologia de outro domínio sem conexão com a pergunta (`OFF_TOPIC`). |
| **`OFF_TOPIC`** | Pertence a domínio disjunto da computação ou propõe ação perigosa que desativa proteções (antítese). | Descreve regras de trânsito urbano ou propõe desativar locks concorrentes em produção. | Cita a ferramenta correta mas omite a solução interna (`RELATED`). |
| **`INSUFFICIENT`** | Conteúdo vago, evasivo ("depende do caso", consultoria genérica) ou declaração explícita de desconhecimento. | "Depende muito da arquitetura e do orçamento de cada cliente." | Raciocínio tautológico circular que reformula a pergunta (`UNKNOWN`). |
| **`UNKNOWN`** | Raciocínio circular (tautologia pura sem ganho informacional) ou contradição semântica indecidível. | "Garante alta disponibilidade mantendo os dados disponíveis para ficarem disponíveis." | Resposta que diz claramente "nunca trabalhei com essa tecnologia" (`INSUFFICIENT`). |

### Regras Contrastivas de Fronteira:
- **`RELATED` vs. `SUPPORTING`:** `SUPPORTING` exige instrumento técnico ativo (ex: Prometheus, APM, traces); `RELATED` é contexto estático, histórico ou autobiográfico.
- **`SUPPORTING` vs. `DIRECT`:** `SUPPORTING` não resolve a falha central; `DIRECT` resolve.
- **`PARTIAL` vs. `INSUFFICIENT`:** `PARTIAL` demonstra conhecimento correto e detalhado de parte do problema; `INSUFFICIENT` não demonstra profundidade em nenhum ponto.
- **`OFF_TOPIC` vs. `UNKNOWN`:** `OFF_TOPIC` é disjunção temática ou antítese ativa; `UNKNOWN` é circularidade tautológica da própria pergunta ou indecidibilidade.

---

## 6. Resolução de Conflitos e Propagação de Incerteza

Para garantir que a classificação decorra de regras explícitas e não da ordem arbitrária de execução de heurísticas:
1. **Autoridade Única de Decisão:** O componente `StrictOntologyRelevanceAggregator` é a **única fonte de verdade** para atribuir a classe canônica final. Nenhum componente intermediário pode forçar uma classe final diretamente.
2. **Prevalência do Gênero Discursivo:** Se uma frase contiver verbos de ação técnicos, mas pertencer a um relato autobiográfico (`PERSONAL_DECLARATION`) ou dado biográfico (`HISTORICAL_TRIVIA`), a operatividade técnica é desativada (`is_operative = False`).
3. **Preservação de Incerteza:** Se o analisador de circularidade classificar um caso como `uncertainty == 'BORDERLINE'`, o sistema NÃO forçará `UNKNOWN`; o caso será avaliado pela cobertura de aspectos com flag de incerteza preservada na trilha de auditoria.
4. **Não-Duplicação de Evidências:** Uma mesma proposição não pode satisfazer duas demandas independentes a menos que demonstre causalidade unificada explícita.

---

## 7. Dezesseis Invariantes Obrigatórios Testáveis

O plano de correção torna obrigatória a verificação dos seguintes 16 invariantes:

1. **INV-01:** Ausência de sobreposição léxica não implica `OFF_TOPIC`.
2. **INV-02:** Presença de tecnologia ou entidade não implica relevância direta (`DIRECT`).
3. **INV-03:** Presença de verbo operacional ativo não implica satisfação da demanda.
4. **INV-04:** Extensão da resposta não é indicativo de qualidade semântica.
5. **INV-05:** Relato de experiência autobiográfica não implica irrelevância técnica quando contextualizado.
6. **INV-06:** Resposta conceitual não comprova automaticamente experiência prática do candidato.
7. **INV-07:** Classificação `DIRECT` exige cumulativamente evidência positiva de atendimento a todos os aspectos obrigatórios.
8. **INV-08:** Qualquer aspecto primário obrigatório não atendido impede terminantemente a classificação `DIRECT`.
9. **INV-09:** Uma proposição pode satisfazer múltiplos aspectos apenas se demonstrar relação causal unificada explícita.
10. **INV-10:** Repetição léxica da pergunta sob conectivos causais não constitui ganho informacional.
11. **INV-11:** Negações e proibições devem ser interpretadas estritamente dentro de seu escopo gramatical.
12. **INV-12:** `INSUFFICIENT` e `UNKNOWN` permanecem conceitual e operacionalmente distintos.
13. **INV-13:** As 7 classes canônicas não podem ser renomeadas, fundidas ou suprimidas.
14. **INV-14:** Toda decisão final deve possuir trilha de justificativa auditável e reproduzível (`decision_trail`).
15. **INV-15:** A incerteza não pode ser descartada ou ocultada para forçar aprovação em cotas de métricas.
16. **INV-16:** A avaliação deve ser estritamente determinística para entradas idênticas.

---

## 8. Plano de Implementação Incremental (Stage 31.7.24)

Conforme detalhado em [stage_31_7_23_incremental_implementation_plan.md](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_23_incremental_implementation_plan.md), a implementação no Stage 31.7.24 obedecerá à seguinte ordem:

```text
Incremento A (Intenção e Demandas)
    ↓ [Verificação de Contratos TC-01, TC-02 + 1038 testes unitários]
Incremento B (Nexo Funcional e Cobertura Bipartida)
    ↓ [Verificação de Contrato TC-02B + Reference Harness 15/15]
Incremento C (Gênero Discursivo e Circularidade Morfológica)
    ↓ [Verificação de Contratos TC-03, TC-04, TC-05 + 1038 testes]
Incremento D (Polaridade, Evasão e Incerteza)
    ↓ [Verificação de Contratos TC-06, TC-07 + Reference Harness 15/15]
Incremento E (Agregação Canônica e Integração Final)
    ↓ [Execução Completa: 1038 Testes Canônicos + Harness 15/15 + Benchmark Diagnóstico]
Novo Runtime Congelado (SHA-256) -> Pronto para Stage 31.7.25
```

---

## 9. Contrato de Validação Independente (Stage 31.7.25)

Conforme formalizado em [stage_31_7_23_validation_contract.md](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_23_validation_contract.md):
- **Limiares Congelados:**
  - Concordância Exata $\ge 75{,}0\%$
  - Recall de DIRECT $\ge 85{,}0\%$
  - Precisão de DIRECT $\ge 70{,}0\%$
  - Falsos DIRECT entre Divergências $\le 10{,}0\%$
  - Recall de PARTIAL $\ge 60{,}0\%$
  - Invariância Homologada (Consistência + Correção) $\ge 80{,}0\%$
  - Regressão Canônica: 0 falhas inexplicadas.
- **Isolamento de Dados:** Os 250 casos do Stage 31.7.21 atuam como **Benchmark Diagnóstico**. A validação homologatória do Ciclo 4 exigirá um **novo conjunto selado de $\ge 250$ casos inéditos** no Stage 31.7.25.
- **Status de Independência:** O status permanece formalmente declarado como `REFERENCE_INDEPENDENCE_UNRESOLVED` devido à adjudicação em ambiente de desenvolvimento.

---

## 10. Gestão de Riscos e Procedimentos de Rollback

O documento [stage_31_7_23_risk_and_rollback_plan.md](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_23_risk_and_rollback_plan.md) formaliza as salvaguardas operacionais:
- Qualquer regressão na suíte de testes unitários ou no Reference Harness ativa rollback imediato via restauração de `reference_runtime/runtime.py.stage_31_7_23_baseline`.
- A complexidade computacional do emparelhamento bipartido foi desenhada para manter latência $< 5\text{ ms}$ por caso, impedindo estouros de tempo no Harness.

---

## 11. Artefatos Persistidos e Hashes Criptográficos

Todos os artefatos foram criados no diretório canônico `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/`:

- [stage_31_7_23_correction_plan.json](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_23_correction_plan.json) (5.420 bytes) — SHA-256: `6E8DEB6B3F02334F3294337DF05BE114C45A3945922BEB145EEDD64FFFE15EFE`
- [stage_31_7_23_component_contracts.md](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_23_component_contracts.md) (15.196 bytes) — SHA-256: `E50FE5A66B13460A3705C1FF5415C13D9C95BAAC26EAE24EBE9E441E7A03FEA0`
- [stage_31_7_23_incremental_implementation_plan.md](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_23_incremental_implementation_plan.md) (9.840 bytes) — SHA-256: `42A0D8D70F4D3C5237C3C1FA7FA8CC8DE8BA69D05A516DE6EFE62CA5788BE809`
- [stage_31_7_23_validation_contract.md](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_23_validation_contract.md) (5.922 bytes) — SHA-256: `CD03A762952E3E8513BF1E1683E2D8299C942EEEDDC6955CF115F61EB426BE05`
- [stage_31_7_23_risk_and_rollback_plan.md](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_23_risk_and_rollback_plan.md) (4.935 bytes) — SHA-256: `785F8DFEFB8BC0B800F362C0CBE3B6F45431DCEFD6D4586C45F4D3962F7642CE`
- [Stage 31.7.23 Report](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/Stage%2031.7.23%20%E2%80%94%20Controlled%20Correction%20Plan%20&%20Contract%20Specification%20%28Cycle%204%29.md) (16.890 bytes) — SHA-256: `E98E63E971E3C8B7201C6DBF20E2C85C0CE3BF05FEFA4C6B1C2DA0F6E66DE2DE`

Os documentos de governança [START_HERE.md](file:///d:/Projetos/TechLens/START_HERE.md) e [GEMINI_HANDOFF.md](file:///d:/Projetos/TechLens/GEMINI_HANDOFF.md) foram atualizados com a Seção 74.

---

## 12. Decisão Final de Gate

```text
====================================================================
GATE STATUS: CORRECTION_PLAN_READY_FOR_CONTROLLED_IMPLEMENTATION
====================================================================
```

### Justificativa Formal:
1. O baseline permaneceu 100% íntegro e congelado sob o hash auditado `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`.
2. Nenhuma alteração foi realizada no runtime ou nos testes existentes nesta etapa.
3. Todas as 8 causas-raiz foram mapeadas para contratos e incrementos com especificações verificáveis.
4. As 7 classes canônicas, seus invariantes e regras de resolução de conflitos estão plenamente formalizados.
5. O plano incremental permite testes controlados a cada passo e rollback automático diante de regressões.

---

## 13. Próximo Passo Autorizado

Avançar formalmente e com exclusividade para:
**Stage 31.7.24 — Controlled Implementation of the Approved Semantic Precision Remediation Plan (Cycle 4)**
