# Stage 31.7.33 — Roadmap de Implementação Controlada (Ciclo 6)

## 1. Visão Geral e Princípios Metodológicos

O objetivo deste roadmap é estruturar a transposição da arquitetura semântica do Ciclo 6 (Stage 31.7.31/32) para o runtime canônico [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py) de forma estritamente controlada, modular, testável e reversível.

Para mitigar riscos de regressão e evitar improvisações durante a codificação, o trabalho foi dividido em **seis incrementos sequenciais autônomos (INC-0 a INC-5)**. Nenhum incremento avançará sem validação prévia de seus contratos e confirmação de zero regressão na suíte canônica do projeto.

---

## 2. Tabela Obrigatória de Incrementos de Implementação

| Incremento | Objetivo | Componentes | Contratos | Dependências | Testes | Critério de Aceitação |
|---|---|---|---|---|---|---|
| **INC-0** | Infraestrutura de Rastreabilidade e Tipos | Dataclasses de Perfil e Schema JSON Draft-07 com `applied_contract_ids` | TRACEABILITY-SCHEMA-DRAFT-07, FINDING-06 | Nenhuma | Testes unitários de tipagem, validação de schema e serialização | Schema JSON 100% válido, serialização sem perda de dados e compatibilidade com hash canônico |
| **INC-1** | Perfil da Pergunta e Suficiência por Intenção | `QuestionProfileExtractor` e `SufficiencyAssessmentEngine` | SC-01, SC-02, SC-05, SC-06, SC-07, SC-08, SC-11, SC-12, ADV-06 | INC-0 | Testes unitários dos 10 modos de intenção e de demandas compostas | Decomposição correta de $D_P$ e $D_S$ em 100% dos casos compostos e classificação de intenção sem heurísticas duras |
| **INC-2** | Segmentação Discursiva, Negações, Condicionais e Preâmbulos | `DiscourseSegmentationEngine` | SC-17, SC-18, SC-20, SC-21, SC-22, SC-32, SC-33, SC-34, ADV-05, ADV-09 a ADV-14, FINDING-05 | INC-0 | Testes de escopo de negação, condicionais, autocorreções e isolamento de preâmbulo | Isolamento de preâmbulo fático (Caso ADV-05), prevalência da correção e conciliação de contradições aparentes sob escopos distintos |
| **INC-3** | Afinidade Temática Refutável e Resolução de Homonímia | `ThematicAffinityEngine` | SC-29, SC-23-REV, ADV-01, FINDING-01, FINDING-04 | INC-0, INC-1, INC-2 | Testes de homonímia adversarial e de presunção refutável por predicados | Refutação categórica de homônimos alienígenas (Spring DI vs petróleo $\to$ `OFF_TOPIC`); emissão de `EQUIVALENCE_PENDING` quando $E_R \cap E_Q = \emptyset$ |
| **INC-4** | Equivalência Conceitual, Invariantes de CS e Analogias Ancoradas | `ConceptualEquivalenceEngine` e `AnalogyResolutionEngine` | SC-24-REV a SC-28-REV, SC-30, SC-31, ADV-02, ADV-04, ADV-07, ADV-08, FINDING-02, FINDING-03 | INC-0 a INC-3 | Testes de invariantes de CS sem tokens literais e de analogias ancoradas | Aprovação como `DIRECT` de B-tree como árvore balanceada e ChronoMesh; aceitação de analogia com aterrissagem e rebaixamento de metáforas sem transposição |
| **INC-5** | Agregação Estrita das Sete Classes e Roteamento Ontológico | `StrictRelevanceAggregator` | SC-03, SC-04, SC-09, SC-10, SC-13 a SC-16, SC-19, SC-35, ADV-03, ADV-15, Matriz 21 Pares | INC-0 a INC-4 | Testes de fronteira das 21 classes, regressão canônica completa (1.047 testes) e Reference Harness | Eliminação definitiva de `else: OFF_TOPIC`; roteamento de metadados para `RELATED` e chavões para `INSUFFICIENT`; emissão de JSON de rastreabilidade |

---

## 3. Fluxo de Dependências Causal

```text
  ┌──────────────────────────────────────────────────────────┐
  │ INC-0: Fundação de Rastreabilidade e Tipos (Data Model)  │
  └────────────────────────────┬─────────────────────────────┘
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
  ┌──────────────────────────┐         ┌──────────────────────────┐
  │ INC-1: Perfil da         │         │ INC-2: Segmentação       │
  │ Pergunta & Suficiência   │         │ Discursiva & Preâmbulos  │
  └─────────────┬────────────┘         └─────────────┬────────────┘
                │                                    │
                └──────────────────┬─────────────────┘
                                   ▼
  ┌──────────────────────────────────────────────────────────┐
  │ INC-3: Afinidade Temática Refutável & Status Transitório │
  └────────────────────────────┬─────────────────────────────┘
                               ▼
  ┌──────────────────────────────────────────────────────────┐
  │ INC-4: Equivalência Conceitual & Analogias Ancoradas     │
  └────────────────────────────┬─────────────────────────────┘
                               ▼
  ┌──────────────────────────────────────────────────────────┐
  │ INC-5: Agregação Estrita 7 Classes & Rastreabilidade JSON│
  └──────────────────────────────────────────────────────────┘
```

---

## 4. Portões de Decisão e Critérios de Progressão

Para cada incremento implementado no Stage 31.7.34, aplicar-se-ão os seguintes critérios formais:

- **`PASS`:** Todos os contratos do incremento foram satisfeitos; 100% dos testes da camada passaram; zero regressões canônicas na base do projeto; JSON de rastreabilidade validado; snapshot do incremento gerado com hash documentado.
- **`PASS_WITH_LIMITATIONS`:** Critérios essenciais satisfeitos, com limitações secundárias formalmente documentadas e autorizadas pela governança.
- **`BLOCKED`:** Dependência não satisfeita ou teste de contrato com ambiguidade não resolvida.
- **`FAIL`:** Qualquer falha em teste contratual, quebra de regressão canônica ou introdução de heurística proibida. Dispara rollback imediato para o snapshot do incremento anterior.
