---
type: study
status: mastered
confidence: 100
created: 2026-10-19
updated: 2026-10-19
tags:
  - stage-31-7-29
  - forensic-rca
  - cycle-6
  - domain-disjunction-generalization
  - entity-affinity
  - provenance-reconciliation
---

# Stage 31.7.29 — Forensic Root Cause Analysis & Domain Disjunction Generalization Architecture (Cycle 6)

## 1. Visão Geral e Responsabilidades do Estágio

O Stage 31.7.29 foi convocado após a emissão do gate `BLIND_SEMANTIC_REVALIDATION_BLOCKED` no Stage 31.7.28, com duas responsabilidades estritas e sequenciais:

1. **Auditoria Forense de Integridade e Proveniência dos Runtimes:** Reconciliar documental e computacionalmente a discrepância entre o SHA-256 `3FD3F80D9BB8A13CCC3A2791759D08F2EED25271913B56F064710DB94B2BC229` (declarado na documentação do Stage 31.7.27) e o SHA-256 `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28` (verificado e validado cegamente no Stage 31.7.28).
2. **Análise de Causa-Raiz (RCA) e Especificação Arquitetural do Ciclo 6:** Diagnosticar estruturalmente os 26 casos de falsos `DIRECT` originários de domínios alienígenas e os 22 casos de rebaixamento indevido de `RELATED` para `OFF_TOPIC`, especificando uma arquitetura de generalização aberta baseada em vinculação de entidades, sem dicionários fechados.

O estágio é exclusivamente investigativo e analítico. **Nenhuma alteração foi implementada no runtime canônico, que permaneceu 100% congelado no hash `6C44B7A8...`.**

---

## 2. Auditoria Forense de Proveniência dos Runtimes

### 2.1. Reconstituição Temporal e Causa da Divergência
A reconstituição baseada em logs de auditoria e metadados de sistema de arquivos comprovou:
1. **14/10/2026 22:24:37 UTC:** Conclusão da integração inicial do Ciclo 5 gerando `runtime.py` com hash `3FD3F80D...`. Foi criado o snapshot `stage_31_7_27_final`.
2. **14/10/2026 22:27:08 UTC:** Execução da suíte canônica de testes resultando em **5 falhas de regressão** (`failures=5`), causadas por conflitos de antítese destrutiva sem guarda de evitação e pelo roteamento de ignorância para `UNKNOWN`.
3. **14/10/2026 22:36:27 UTC:** Aplicação de 3 correções pontuais de salvaguarda de regressão em `runtime.py`, gerando o hash definitivo `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28`. A suíte canônica passou integralmente com **1.046 testes aprovados e 0 falhas**, e o Reference Harness passou com **15/15 OK**.
4. **14/10/2026 22:50:00 UTC:** Erro administrativo de transcrição na compilação do relatório do Stage 31.7.27, onde o operador copiou inadvertidamente o hash prévio do snapshot (`3FD3F80D...`) em vez de recalcular o hash de `runtime.py`.
5. **Stage 31.7.28:** O operador detectou a divergência, submeteu a decisão ao usuário via modal interativo, e o usuário aprovou formalmente validar o runtime com 0 regressões (`6C44B7A8...`), preservando o estado pré-fix como `runtime.py.stage_31_7_27_pre_regression_fix`.

### 2.2. Execução Comparativa dos Dois Runtimes sobre o Benchmark de 250 Casos
A execução comparativa revelou:
- Em 234 dos 250 casos (93,6%), as predições de ambos os runtimes são absolutamente idênticas.
- Em exatamente 16 casos, o runtime pré-fix (`3FD3F80D...`) predisse `UNKNOWN` e o runtime final (`6C44B7A8...`) predisse `INSUFFICIENT`. Todos esses 16 casos consistem em declarações explícitas de ignorância (*"Não sei responder..."*), cujo gabarito oficial é `INSUFFICIENT`.
- **Os 26 falsos DIRECTs (`OFF_TOPIC → DIRECT`) e os 22 falsos OFF_TOPICs (`RELATED → OFF_TOPIC`) são rigorosamente idênticos em ambos os runtimes.** As 3 correções de salvaguarda não tiveram nenhuma influência sobre o bloqueio semântico do Stage 31.7.28.

### 2.3. Decisão Formal de Proveniência:
$$\textbf{GATE: RUNTIME\_PROVENANCE\_RECONCILED}$$

---

## 3. Reprodução das Métricas do Baseline Semântico (Stage 31.7.28)

Todas as métricas reportadas no relatório do Stage 31.7.28 foram reproduzidas com exatidão matemática de 100% a partir dos arquivos selados `stage_31_7_28_ground_truth.json` e `stage_31_7_28_system_predictions.json` ([`stage_31_7_29_metrics_reproduction.json`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_metrics_reproduction.json)):

- Total de Casos: 250 | Acertos: 168 (**67,20%**) | Divergências: 82 (**32,80%**)
- Falsos `DIRECT`: 34 casos (**41,46%** das divergências)
- Recall de `DIRECT`: 38/50 (**76,00%**) | Precisão de `DIRECT`: 38/72 (**52,78%**)
- Recall de `PARTIAL`: 38/45 (**84,44%**) | Recall de `SUPPORTING`: 29/30 (**96,67%**)
- Recall de `UNKNOWN`: 18/20 (**90,00%**) | Recall de `INSUFFICIENT`: 19/25 (**76,00%**)
- Recall de `RELATED`: 8/35 (**22,86%**) | Recall de `OFF_TOPIC`: 18/45 (**40,00%**)
- Invariância Pareada Simultaneamente Correta: 13/20 pares (**65,00%**)

---

## 4. Análise de Causa-Raiz (RCA)

### 4.1. Causa dos 26 Falsos DIRECTs (`OFF_TOPIC → DIRECT`)
- **Mecanismo da Falha:** O motor de disjunção utilizava clusters de expressões regulares estáticas (`\bescultura em argila\b`, `\bbolo de chocolate\b`, `\btroca de óleo\b`). Textos de artesanato com vocabulário inédito (*"vasos de argila"*, *"pasta mineral"*, *"roda de oleiro"*), construção civil (*"cimento Portland"*, *"betoneira"*) e agricultura não ativaram a flag de veto `is_disjoint`.
- Em seguida, por serem descrições de procedimentos ativos, continham verbos transitivos diretos (*"requer"*, *"exige"*, *"misturamos"*), levando o filtro discursivo a marcar `is_operative = True`.
- Na ausência de veto de domínio, o casador de nexo assumiu que uma frase operacional resolve funcionalmente a demanda (`FUNCTIONALLY_SOLVES`), e o agregador concedeu `DIRECT`.
- **Falha Conceitual:** **Equiparação de operatividade gramatical a pertinência técnica.**

### 4.2. Causa dos 22 Falsos OFF_TOPICs (`RELATED → OFF_TOPIC`)
- **Mecanismo da Falha:** Textos descrevendo a história, criadores ou mantenedores de tecnologias reais (e.g. PostgreSQL em Berkeley, Docker na DotCloud) não continham código ou ações operacionais, sendo marcados como `is_operative = False`.
- O padrão regex de metadados institucionais falhou por ser fechado (exigia *"categoria de soluções"* em vez de *"categoria de ferramentas"*).
- Sem casamento específico, o casador de nexo emitiu `nexus_relation = "NON_OPERATIVE"`.
- No agregador ontológico, qualquer relação não atendida por regras prioritárias caía no bloco final `else:`, que fixava `classification = "OFF_TOPIC"` com `relation_type = "non_operative_assertion"`.
- **Falha Conceitual:** **Tratar a ausência de um mecanismo operacional como prova positiva de disjunção de domínio, eliminando a classe `RELATED`.**

---

## 5. Especificação da Arquitetura de Generalização (Ciclo 6)

A arquitetura aprovada para o Ciclo 6 apoia-se em 4 pilares estruturais ([`stage_31_7_29_domain_disjunction_generalization_architecture.md`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_domain_disjunction_generalization_architecture.md)):

1. **Vinculação de Entidades e Afinidade Semântica Aberta:**
   - Extração explícita das entidades nucleares da pergunta ($E_Q$) e da resposta ($E_R$).
   - **Regra da Âncora Temática:** Se $E_R \cap E_Q \neq \emptyset$, o domínio é por definição tematicamente compatível, vetando categoricamente qualquer classificação `OFF_TOPIC`.
2. **Disjunção Radical Baseada em Entidades Alienígenas:**
   - A disjunção radical é detectada pela presença de substantivos concretos estranhos à computação sem qualquer ligação com a entidade da pergunta, e não por regras gramaticais ou ausência de termos.
3. **Desacoplamento entre Operatividade e Pertinência:**
   - Uma ação só recebe `FUNCTIONALLY_SOLVES` se atuar diretamente sobre as entidades da demanda. Ações sobre argila, cimento ou farinha são sumariamente neutralizadas.
4. **Agregador Reconciliado com Trilha Auditável:**
   - Proposições não-operativas que compartilham a entidade temática da pergunta são roteadas expressamente para `RELATED` (`thematic_adjacency_without_mechanism`), extinguindo o sumidouro `else: OFF_TOPIC`.

---

## 6. Inventário de Artefatos Persistidos (Stage 31.7.29)

Todos os 13 artefatos mandatórios foram gravados em [`11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05):
1. [`stage_31_7_29_runtime_provenance_audit.md`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_runtime_provenance_audit.md)
2. [`stage_31_7_29_runtime_hash_inventory.json`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_runtime_hash_inventory.json)
3. [`stage_31_7_29_runtime_comparison_report.md`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_runtime_comparison_report.md)
4. [`stage_31_7_29_metrics_reproduction.json`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_metrics_reproduction.json)
5. [`stage_31_7_29_root_cause_analysis.md`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_root_cause_analysis.md)
6. [`stage_31_7_29_false_direct_case_audit.json`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_false_direct_case_audit.json)
7. [`stage_31_7_29_related_off_topic_audit.json`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_related_off_topic_audit.json)
8. [`stage_31_7_29_seven_class_contract_audit.md`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_seven_class_contract_audit.md)
9. [`stage_31_7_29_domain_disjunction_generalization_architecture.md`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_domain_disjunction_generalization_architecture.md)
10. [`stage_31_7_29_semantic_contracts.json`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_semantic_contracts.json)
11. [`stage_31_7_29_regression_risk_matrix.md`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_regression_risk_matrix.md)
12. [`stage_31_7_29_future_validation_plan.md`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_29_future_validation_plan.md)
13. [`Stage 31.7.29 — Forensic Root Cause Analysis & Domain Disjunction Generalization Architecture (Cycle 6).md`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/Stage%2031.7.29%20%E2%80%94%20Forensic%20Root%20Cause%20Analysis%20%26%20Domain%20Disjunction%20Generalization%20Architecture%20%28Cycle%206%29.md)

---

## 7. Decisão Formal de Gates e Próximos Passos

$$\textbf{Gate de Proveniência: RUNTIME\_PROVENANCE\_RECONCILED}$$
$$\textbf{Gate de RCA e Arquitetura: RCA\_COMPLETE\_ARCHITECTURE\_PENDING\_REVIEW}$$
$$\textbf{Ressalva Metodológica Mantida: REFERENCE\_INDEPENDENCE\_UNRESOLVED}$$

### Próximo Passo Autorizado:
- **Revisão e Aprovação Formal de Governança pelo Usuário:**
  O Stage 31.7.30 (Implementação Controlada da Arquitetura do Ciclo 6) só poderá ser iniciado após a apreciação e aprovação explícita da especificação pelo usuário.
