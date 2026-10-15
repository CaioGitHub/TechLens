# Stage 31.7.27 — Plano de Implementação Controlada da Arquitetura de Disjunção de Domínio Semântico (Ciclo 5)

## 1. Contexto e Objetivos

O Stage 31.7.25 executou a revalidação cega e independente do runtime remediado no Ciclo 4, revelando uma vulnerabilidade estrutural de permissividade de domínio aberto: sentenças com sintaxe ativa e bem formada em domínios disjuntos (botânica, jardinagem, culinária, mecânica) ou metadados institucionais/categoriais gerais foram promovidas indevidamente a `DIRECT`, gerando **70 falsos DIRECT** (71,43% das 98 divergências) e derrubando a precisão de `DIRECT` para **41,67%** (limiar $\ge 70\%$).

O Stage 31.7.26 conduziu a análise profunda de causa-raiz (RCA), auditou individualmente os 70 falsos `DIRECT`, comprovou a causa estrutural (desacoplamento contratual entre a flag sintática operativa e o fallback irrestrito da linha 3434) e especificou a **Semantic Domain Disjunction Architecture (Ciclo 5)** com os Contratos Formais A a G, aprovada pelo gate `RCA_COMPLETE_ARCHITECTURE_APPROVED_FOR_IMPLEMENTATION`.

O presente estágio (**Stage 31.7.27**) tem como objetivo **implementar de forma estritamente controlada e incremental a arquitetura do Ciclo 5** em `reference_runtime/runtime.py`.

### 1.1. Metas Estruturais Inegociáveis
1. **Eliminar o fallback incondicional** de domínio aberto que presumia atendimento direto a partir de mera operatividade sintática.
2. **Introduzir o componente `SemanticDomainDisjunctionEngine`** para identificar incompatibilidade ontológica e disjunção radical baseada em evidência positiva, sem recurso a dicionários fechados de palavras proibidas ou catalogações ad-hoc.
3. **Formalizar a Suficiência Relativa à Intenção da Pergunta**, sem impor cadeias universais de causalidade para perguntas puramente conceituais, comparativas, diagnósticas ou históricas.
4. **Preservar as distinções e contratos das sete classes canônicas**: `DIRECT`, `PARTIAL`, `SUPPORTING`, `RELATED`, `OFF_TOPIC`, `INSUFFICIENT`, `UNKNOWN`.
5. **Preservar os 14 comportamentos corretos de domínio aberto**: respostas sem sobreposição lexical, entidades inéditas, linguagem coloquial, voz passiva e proteção das classes já estabilizadas (`UNKNOWN` e `PARTIAL`).

---

## 2. Baseline de Entrada e Salvaguarda de Rollback

- **Arquivo:** `reference_runtime/runtime.py`
- **SHA-256 de Entrada (Baseline Homologado):**
  $$\textbf{36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7}$$
- **Backup Verificável Criado:**
  `reference_runtime/runtime.py.stage_31_7_26_baseline` (SHA-256 idêntico confirmado).
- **Procedimento de Rollback:**
  Se qualquer incremento introduzir regressão insolúvel ou violar os contratos semânticos estabelecidos, o runtime será restaurado imediatamente para o snapshot do incremento anterior ou para o baseline via cópia do arquivo de backup correspondente.

---

## 3. Plano Incremental de Implementação (Incrementos A a E)

A implementação no runtime será dividida em 5 incrementos atômicos e progressivos:

### Incremento A — Semantic Domain Disjunction Engine
- **Objetivo:** Criar e integrar a classe `SemanticDomainDisjunctionEngine` no pipeline.
- **Responsabilidades:**
  - Extrair o agrupamento ontológico do domínio da pergunta ($D_{dom}$).
  - Mapear os papéis semânticos e campos conceituais da proposição da resposta ($P_{dom}$).
  - Detectar evidência positiva de **Disjunção Radical** (ex.: processos biológicos, botânica, agricultura, culinária doméstica, mecânica automotiva básica) confrontados com problemas computacionais/sistêmicos.
  - Distinguir metadados institucionais/históricos (`THEMATIC_METADATA_ONLY`) de ações de engenharia de software.
  - Assegurar que entidades técnicas desconhecidas sejam consideradas abertas e plausíveis (`OPEN_DOMAIN_PLAUSIBLE`).
  - Emitir objeto estruturado `DomainCompatibilityRecord` com justificativa auditável.

### Incremento B — Demand-Proposition Nexus Bipartite Matcher
- **Objetivo:** Refatorar o emparelhamento bipartido entre demandas e proposições.
- **Responsabilidades:**
  - Revogar o fallback irrestrito da **Linha 3434** de `runtime.py`.
  - Integrar a checagem de compatibilidade do `SemanticDomainDisjunctionEngine`:
    - Se `is_disjoint == True`, emitir obrigatoriamente `nexus_relation = "DISJOINT_ONTOLOGY"`.
    - Se metadados institucionais, emitir `nexus_relation = "THEMATIC_MENTION_ONLY"`.
    - Se ação de observabilidade auxiliar, emitir `nexus_relation = "AUXILIARY_OBSERVABILITY"`.
    - Se ação técnica compatível e pertinente aos objetivos da demanda, emitir `FUNCTIONALLY_SOLVES` ou `PARTIAL_ASPECT`.
    - Se vaga, tautológica ou evasiva, emitir `INSUFFICIENT_EVIDENCE`.

### Incremento C — Cobertura e Suficiência Relativa à Intenção
- **Objetivo:** Ajustar a avaliação de suficiência da resposta ao tipo de intenção da pergunta.
- **Responsabilidades:**
  - Não exigir causalidade/mecanismo operacional para perguntas de definição conceitual (ex.: "O que é inversão de controle?"), perguntas comparativas ou perguntas históricas.
  - Exigir mecanismo causal somente quando a demanda explicitar funcionamento interno, protocolo, algoritmo ou troubleshooting.
  - Garantir que em perguntas compostas (múltiplas demandas obrigatórias), todas devam ser cobertas para viabilizar `DIRECT`. Se houver cobertura parcial genuína, direcionar para `PARTIAL`.
  - Permitir legitimamente que uma única proposição densa atenda a múltiplas demandas relacionadas sem penalização.

### Incremento D — Agregação Final (StrictOntologyRelevanceAggregator)
- **Objetivo:** Manter autoridade centralizada, explícita e determinística para a decisão da classe final.
- **Responsabilidades:**
  - Definir política formal de precedência entre as 7 classes:
    1. Se `UNKNOWN` (ignorância explícita ou ininteligível) $\to$ `UNKNOWN`.
    2. Se `DISJOINT_ONTOLOGY` sem nenhuma evidência técnica compatível $\to$ `OFF_TOPIC`.
    3. Se todas as demandas primárias obrigatórias possuem `FUNCTIONALLY_SOLVES` $\to$ `DIRECT`.
    4. Se subconjunto não vazio das demandas possui `FUNCTIONALLY_SOLVES` (ou atendimento parcial demonstrado) $\to$ `PARTIAL`.
    5. Se há evidência de observabilidade instrumental $\to$ `SUPPORTING`.
    6. Se há menção temática ou metadados institucionais $\to$ `RELATED`.
    7. Se há tentativa no domínio técnico mas todas as proposições são fracas/evasivas $\to$ `INSUFFICIENT`.
  - Tratamento formal de incerteza: se a confiança média dos nexos for $< 0.50$, rebaixar para classe de menor presunção.

### Incremento E — Rastreabilidade e Integração Completa
- **Objetivo:** Integrar os novos componentes à interface do runtime `evaluate_candidate_turn`.
- **Responsabilidades:**
  - Enriquecer o retorno com metadados detalhados de auditoria (`domain_disjunction_record`, `bipartite_nexus_matrix`, `telemetry_trace`).
  - Manter compatibilidade com harnesses de teste legados e pipeline canônico.

---

## 4. Estratégia de Testes de Contrato (20 Cenários Obrigatórios)

Será desenvolvida uma suíte abrangente em `tests/test_stage_31_7_27_contract_tests.py` (e duplicada/espelhada em `stage_31_7_27_contract_tests.py`) cobrindo rigorosamente os 20 cenários fundamentais:
1. Resposta correta sem sobreposição lexical.
2. Resposta de domínio semanticamente disjunto (`OFF_TOPIC`).
3. Resposta temática sem atendimento funcional (`RELATED`).
4. Contribuição auxiliar de observabilidade (`SUPPORTING`).
5. Atendimento parcial de pergunta composta (`PARTIAL`).
6. Atendimento completo de pergunta composta (`DIRECT`).
7. Resposta insuficiente / evasiva (`INSUFFICIENT`).
8. Indeterminação genuína / desconhecimento explícito (`UNKNOWN`).
9. Pergunta de definição sem exigência causal (`DIRECT`).
10. Pergunta histórica diretamente respondida (`DIRECT`).
11. Pergunta comparativa diretamente respondida (`DIRECT`).
12. Pergunta de diagnóstico/troubleshooting com exigência causal (`DIRECT`).
13. Tecnologia desconhecida / inédita usada em resposta válida (`DIRECT`).
14. Linguagem coloquial e voz passiva com validade técnica (`DIRECT`).
15. Resposta longa, ativa e operacional, mas de domínio disjunto (`OFF_TOPIC`).
16. Resposta curta e precisa (`DIRECT`).
17. Proposição única de alta densidade satisfazendo múltiplas demandas (`DIRECT`).
18. Circularidade e tautologia reflexiva (`INSUFFICIENT` ou `UNKNOWN`).
19. Contradição explícita / antítese técnica (`INSUFFICIENT` ou `OFF_TOPIC`).
20. Mutações superficiais e paráfrases mantendo invariância semântica.

---

## 5. Protocolo de Verificação e Regressão Canônica

1. **Execução da Suíte Canônica:**
   - Executar todos os testes da pasta `tests/` (1.047+ testes).
   - Meta: 0 falhas e 0 erros de regressão.
2. **Execução do Reference Harness:**
   - Executar os 15 testes de referência canônicos (`test_reference_harness.py`).
   - Meta: 15/15 aprovados (`PASS_WITH_WARNINGS` ou superior).
3. **Auditoria Diagnóstica no Benchmark Histórico:**
   - Executar os 250 casos do Stage 31.7.25 exclusivamente para avaliar a redução de falsos `DIRECT` e a preservação das demais classes.
   - Declarar explicitamente que este benchmark é diagnóstico e mantido sob `REFERENCE_INDEPENDENCE_UNRESOLVED`.
