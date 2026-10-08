# Stage 31.7.1 — Root Cause Analysis & Architectural Decoupling of Functional Catalog

**Status:** Concluído  
**Data:** 2026-10-07  
**Gate:** `ROOT_CAUSE_ANALYSIS_COMPLETE`  
**Referência Metodológica:** `AGENTS.md`, `SECOND_BRAIN.md`, `GEMINI_GUARDRAILS.md`, `GEMINI_HANDOFF.md`, Stage 31.6, Stage 31.7  

---

## Status

```text
GATE: ROOT_CAUSE_ANALYSIS_COMPLETE
```

O diagnóstico estrutural e a Root Cause Analysis (RCA) foram integralmente concluídos. A primeira decisão incorreta do pipeline foi identificada e rastreada passo a passo em todas as 14 falhas observadas na revalidação cega do Stage 31.7. As invariantes arquiteturais e a proposta de desacoplamento do catálogo foram formalizadas sem nenhuma modificação no runtime congelado.

---

## Objetivo

O objetivo deste estágio foi determinar, de forma reprodutível, auditável e tecnicamente fundamentada:
1. **Por que o modelo atual de Semantic Relevance trata `_FUNCTIONAL_CAPABILITIES` como autoridade prescritiva eliminatória** em vez de metadados auxiliares de referência?
2. **Qual é a primeira decisão arquitetural incorreta** que faz o sistema rejeitar respostas válidas de tecnologias desconhecidas e conceitos livres de tecnologia?
3. **Qual é o desenho arquitetural generalizável** que desacopla o julgamento semântico do catálogo de palavras-chave, preservando os ganhos métricos estáveis do piloto real (MAE 0.64) sem recorrer a novas exceções ad-hoc?

### Regra de Congelamento
Em cumprimento estrito às instruções da Seção 2:
- `runtime = FROZEN` (SHA-256: `12792d2d5cac5022b401387751846cef53dde0f04de8c9dc29e24fcef12a28ed`)
- `human oracle = FROZEN`
- `rubric = FROZEN`
- `existing tests = FROZEN`
- Nenhuma linha de código foi editada no runtime ou nas suítes canônicas durante esta etapa investigativa.

---

## Estado Inicial

O histórico de gates do projeto permanece inalterado e preservado:

```text
Stage 31:    HUMAN_VS_SYSTEM_BLOCKED
Stage 31.1:  ROOT CAUSE IDENTIFIED
Stage 31.2:  CONTROLLED CORRECTION COMPLETE_WITH_WARNINGS
Stage 31.3:  POST_CORRECTION_BLIND_VALIDATION_BLOCKED
Stage 31.4:  SEMANTIC_RELEVANCE_INVARIANCE_REMEDIATION_COMPLETE_WITH_WARNINGS
Stage 31.4.1: SEMANTIC_RELEVANCE_MODEL_REDESIGN_COMPLETE
Stage 31.4.2: SEMANTIC_RELEVANCE_MODEL_IMPLEMENTATION_COMPLETE
Stage 31.5:  POST_REMEDIATION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED
Stage 31.6:  CONTROLLED_CORRECTION_COMPLETE
Stage 31.7:  POST_CORRECTION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED
```

---

## Evidências do Stage 31.7

A revalidação cega do Stage 31.7 demonstrou que a correção do Stage 31.6 eliminou com sucesso os word-count proxies e as colisões de substring, mas a suíte adversarial cega (`test_stage_31_7_blind_revalidation.py`) registrou **14 falhas em 65 testes (78.5% PASS, 21.5% FAIL)**.

O comportamento observado nessas 14 falhas não decorre de imprecisão numérica ou calibragem de score, mas de **erros categóricos de classificação semântica**:
- Respostas tecnicamente impecáveis em domínio aberto foram classificadas como `OFF_TOPIC` com `functional_contribution: False`.
- Respostas cobrindo arquiteturas compostas foram rebaixadas para `PARTIAL` sob alegação de "mistura com domínio alienígena".
- Declarações vazias de experiência foram promovidas para `conceptual: positive` simplesmente por repetirem a tecnologia demandada.

---

## Inventário de Usos de `_FUNCTIONAL_CAPABILITIES`

Auditoria estrita no código-fonte [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py) identificou todos os 8 pontos de acoplamento com a estrutura `_FUNCTIONAL_CAPABILITIES`:

| Ponto | Linhas no Runtime | Função | Entrada | Saída | Responsabilidade Atual | Classificação | Justificativa |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | 695–698 | `_extract_evidence_specs` | `cleaned_decl`, `_FUNCTIONAL_CAPABILITIES.values()` | `has_conceptual_content: bool` | Dita se menção verbal isolada vira evidência conceitual positiva. | **INDEVIDO** | Confere crédito conceitual espúrio se o candidato repetir qualquer palavra do catálogo, sem avaliar profundidade. |
| **U2** | 914–918 | `_evaluate_multi_aspect_coverage` | `target_domain`, `r_norm`, `cap["valid"]` | `cov1: bool` | Determina cobertura do Aspecto 1 em pergunta multi-aspecto. | **INDEVIDO** | Faz a cobertura de uma demanda da pergunta depender de termos pré-catalogados, em vez da proposição técnica da resposta. |
| **U3** | 983–1064 | Módulo global | Dicionário estático | Estrutura de dados | Repositório de termos organizados em `demands`, `valid`, `defining`. | **QUESTIONÁVEL** | Estruturado como ontologia prescritiva eliminatória em vez de guia semântico ou metadados de taxonomia. |
| **U4** | 1242–1249 | `_evaluate_semantic_relevance` | `r_lower`, `q_lower`, `cap["defining"]` | `alien_domains: list` | Ejeção para `OFF_TOPIC` em perguntas diagnósticas. | **QUESTIONÁVEL** | Assume que qualquer termo definidor citado em troubleshooting é desvio de assunto se não houver palavras de diagnóstico. |
| **U5** | 1334–1338 | `_evaluate_semantic_relevance` | `q_lower`, `cap["demands"]` | `target_domains: list` | Roteamento rígido da intenção da pergunta para domínios catalogados. | **INDEVIDO** | Sequestro semântico: uma única palavra polissêmica (`transação`, `telemetria`) fecha a pergunta em um único escopo tecnológico. |
| **U6** | 1341–1382 | `_evaluate_semantic_relevance` | `r_lower`, `cap["valid"]` | `has_valid: bool`, retorno `OFF_TOPIC` / `RELATED` | Whitelist eliminatória: se `not has_valid`, descarta a resposta. | **INDEVIDO** | **Autoridade semântica eliminatória máxima.** Se o candidato explicar o mecanismo correto com vocabulário fora de `valid`, é forçado para `OFF_TOPIC`. |
| **U7** | 1384–1396 | `_evaluate_semantic_relevance` | `r_lower`, `other_cap["defining"]` | `other_defines: list`, retorno `PARTIAL` | Rebaixamento por contaminação de domínio (`mixed_target_and_alien`). | **INDEVIDO** | Penaliza arquiteturas compostas e sinérgicas legítimas (ex.: mensageria assíncrona usada para viabilizar consistência eventual). |
| **U8** | 1426–1445 | `_evaluate_semantic_relevance` | `r_lower`, `cap["defining"]` | `alien_defines: list`, retorno `OFF_TOPIC` | Intercepção global prévia antes da avaliação de domínio aberto. | **INDEVIDO** | **Intercepção catalográfica destrutiva.** Bloqueia respostas de domínio aberto se o candidato citar qualquer conceito catalogado em outro lugar. |

---

## Análise das 14 Falhas do Stage 31.7

A tabela a seguir consolida o rastreamento exaustivo de cada falha observada em `tests/test_stage_31_7_blind_revalidation.py`:

| ID | Teste | Resultado Observado vs Esperado | Primeira Decisão Incorreta | Causa Imediata | Causa Estrutural | Família da Falha |
|---|---|:---:|---|---|---|---|
| **F01** | `test_experience_declaration_without_mechanism` | `conceptual: positive` (7.05) vs `experience_declaration` (4.0) | Linha 693: `has_conceptual_content = True` | A menção ao nome da tecnologia (`Kubernetes`) foi rotulada como asserção técnica direta. | Confusão entre repetição do nome do tópico e demonstração de mecanismo técnico. | `EXPERIENCE` |
| **F02** | `test_hypothesis_formulation_is_tagged_epistemically` | `conceptual: positive` vs `hypothesis_formulation` | Linha 573: ausência de `"eu hipotetizaria"` na lista hardcoded de marcadores | Termo de hipótese não constava na tupla estática de strings (`"eu faria"`, `"uma possibilidade"`). | Detecção epistêmica baseada em lista fechada de prefixos gramaticais. | `EXPERIENCE` |
| **F03** | `test_zero_knowledge_proofs_open_domain` | `OFF_TOPIC` vs `DIRECT` | Linha 1446: `shared_stems == set()` | O stemmer sufixal não reduziu substantivos de agente (`provador` vs `prova`, `verificador` vs `verificação`). | Dependência estrita de interseção léxica exata em domínio aberto sem expansão morfológica derivacional. | `LEXICAL_GAP` |
| **F04** | `test_01_rest_and_pagination` | `DIRECT` vs `PARTIAL` | Linha 888: `cov2 = True` em `_evaluate_multi_aspect_coverage` | A palavra genérica `"recursos"` constava no Aspecto 2 e foi encontrada na resposta que só cobriu Aspecto 1. | Avaliação de aspecto por presença de palavras isoladas compartilhadas, sem validar a demanda específica (paginação). | `MULTI_ASPECT` |
| **F05** | `test_07_eventual_consistency_and_idempotency` | `PARTIAL` vs `DIRECT` | Linha 1384: disparo de `mixed_target_and_alien` | A resposta citou `"mensageria assíncrona"` como meio de entrega de eventos para consistência eventual. | O catálogo proíbe menção a capacidades de outros domínios, punindo sinergia arquitetural legítima. | `CATALOG_INTERCEPTION` |
| **F06** | `test_03_unseen_surrealdb_multimodel` | `OFF_TOPIC` vs `DIRECT` | Linha 1426: intercepção por `alien_defines` | A resposta citou `"tabelas relacionais"` para explicar o modelo híbrido do SurrealDB. | `alien_defines` roda antes do domínio aberto e aborta a avaliação se qualquer termo catalogado for citado. | `CATALOG_INTERCEPTION` |
| **F07** | `test_05_unseen_opentelemetry_collector` | `OFF_TOPIC` vs `DIRECT` | Linha 1334: sequestro de demanda por `"telemetria"` | A palavra `"telemetria"` forçou a pergunta para `telemetry_and_query_analytics` (catálogo Azure/Kusto). | A pergunta foi fechada em uma ontologia restrita que não reconhece o padrão aberto OTel. | `POLYSEMY` / `CATALOG_INTERCEPTION` |
| **F08** | `test_07_unseen_redpanda_streaming` | `RELATED` vs `DIRECT` | Linha 1350: `not has_valid` em `asynchronous_messaging` | A explicação técnica (C++, thread-per-core, sem JVM) não usou palavras da whitelist (`producer`, `consumer`). | Autoridade eliminatória da whitelist: ausência de palavras literais do catálogo rebaixa explicação profunda de engine. | `CATALOG_INTERCEPTION` |
| **F09** | `test_01_optimistic_concurrency_control` | `OFF_TOPIC` vs `DIRECT` | Linha 1448: `shared_stems == set()` | O problema (*evitar conflito de escrita sem lock*) e o mecanismo (*versionamento com timestamp*) não têm palavras em comum. | Incapacidade do motor lexical de mapear relações funcionais problema-mecanismo sem cadastro prévio. | `LEXICAL_GAP` |
| **F10** | `test_04_distributed_context_propagation` | `OFF_TOPIC` vs `DIRECT` | Linha 1334: sequestro de demanda por `"transação"` | A palavra `"transação"` forçou a pergunta para `enterprise_framework_transactions` (Spring `@Transactional`). | Polissemia não resolvida: transação distribuída/rastreável foi tratada como transação de banco relacional. | `POLYSEMY` / `CATALOG_INTERCEPTION` |
| **F11** | `test_05_circuit_breaker_graceful_fallback` | `OFF_TOPIC` vs `SUPPORTING` | Linha 1448: `shared_stems == set()` | A pergunta não usou as palavras `"circuit breaker"` e a resposta não repetiu as palavras da pergunta. | Descontinuidade léxica entre a descrição da falha e o padrão de resiliência. | `LEXICAL_GAP` |
| **F12** | `test_07_regression_detection_p99_baseline` | `OFF_TOPIC` vs `DIRECT` | Linha 1448: `shared_stems == set()` | Pergunta sobre degradação após deploy; resposta sobre baseline P99 de telemetria. | Descontinuidade léxica entre a meta de detecção e a técnica estatística adotada. | `LEXICAL_GAP` |
| **F13** | `test_08_bulkhead_resource_isolation` | `DIRECT` vs `SUPPORTING` | Linha 1478: fallback aberto rotula como `DIRECT` | A palavra `"thread"` permitiu casamento aberto, mas sem classificar a função de suporte à resiliência. | Ausência de taxonomia de intenção funcional em domínio aberto; tudo que casa vira `DIRECT`. | `SUPPORTING_VS_RELATED` |
| **F14** | `test_10_token_bucket_rate_limiting` | `OFF_TOPIC` vs `DIRECT` | Linha 1334: sequestro de demanda por `"endpoints"` | A palavra `"endpoints"` forçou a pergunta para `api_design_and_protocols`, que exigia verbos HTTP. | Proteção de endpoint via rate limiting foi avaliada como falha em descrever o protocolo REST. | `POLYSEMY` / `CATALOG_INTERCEPTION` |

---

## Primeira Decisão Incorreta

O rastreamento passo a passo das falhas revelou onde o pipeline erra pela primeira vez:

```text
[Pipeline Canônico Estabelecido]
1. Question Text
   ↓
2. Intent Analysis (factual / diagnostic / architectural / experience)
   ↓
3. Demand Extraction (O que a pergunta está pedindo?)
   ↓ [AQUI OCORRE A PRIMEIRA DECISÃO INCORRETA]
   >>> Decisão Falha: A demanda não é extraída da semântica da frase.
   >>> Em vez disso, o sistema escaneia _FUNCTIONAL_CAPABILITIES procurando palavras isoladas.
   ↓
4. Domain Assignment
   >>> Se encontrou uma palavra: atribui o domínio do catálogo e impõe sua whitelist ("valid").
   >>> Se não encontrou: joga para o domínio aberto puramente lexical ("shared_stems").
   ↓
5. Candidate Response Evaluation
   >>> Se caiu no catálogo: se não usou termos de "valid" -> OFF_TOPIC / RELATED.
   >>> Se citou termo de outro catálogo ("defining") -> alien_defines -> OFF_TOPIC.
   >>> Se caiu no domínio aberto: se não repetiu termos da pergunta -> OFF_TOPIC.
```

### O Ponto de Ruptura
A **primeira decisão incorreta** ocorre no momento em que o sistema delega a **compreensão da demanda da pergunta para um casamento léxico com o dicionário `_FUNCTIONAL_CAPABILITIES`**:
1. Se uma palavra isolada da pergunta colide com uma demanda do catálogo (ex.: `"transação"`, `"telemetria"`, `"endpoints"`), o sistema **abandona o restante da pergunta** e assume que o entrevistador exigiu estritamente a tecnologia mapeada naquele catálogo (Spring, Kusto, REST methods).
2. O sistema **inverte a relação de autoridade**: em vez de o catálogo servir como apoio taxonômico para rotular conceitos encontrados, ele passa a atuar como um **filtro prescritivo eliminatório**: o que não está na lista `valid` daquele domínio é declarado `alien` e descartado como `OFF_TOPIC`.

---

## Root Cause

A **Causa-Raiz Primária** é:

> **O acoplamento do julgamento de Semantic Relevance a uma autoridade prescritiva fechada (`_FUNCTIONAL_CAPABILITIES`), onde o domínio de uma pergunta é inferido por correspondência de palavras isoladas e a validade de uma resposta é determinada pela presença obrigatória de termos em uma whitelist estática.**

Esse modelo viola os princípios do Stage 31.4.1 porque:
- Trata **ausência de menção no catálogo** como **ausência de pertinência semântica**.
- Trata **menção a conceitos complementares legítimos** como **contaminação alienígena**.
- Trata **pertinência em domínio aberto** como mera **interseção literal de radicais** (`shared_stems`).

---

## Contributing Causes

1. **Precedência Invertida de `alien_defines`:** A verificação de fuga de tema executa antes da análise de domínio aberto, interceptando e penalizando ferramentas modernas que combinam paradigmas (ex.: SurrealDB combinando tabelas e grafos).
2. **Polissemia Léxica Monotoken:** Termos que possuem múltiplos significados em engenharia de software (`transação` em banco vs `transação` em tracing distribuído; `endpoints` em design HTTP vs `endpoints` em segurança/rate limit) foram cadastrados como gatilhos monovalentes rígidos.
3. **Ausência de Inferência de Mecanismo em Domínio Aberto:** O motor aberto só reconhece relevância se a resposta repetir as palavras da pergunta. Quando o candidato explica a solução de um problema sem repetir a descrição do problema (OCC, Bulkhead, Fallback), o sistema é cego para a relação funcional problema $\to$ solução.
4. **Vazamento de Heurísticas de Evidência para Semântica:** A extração de evidências confunde a repetição do nome da tecnologia com demonstração conceitual, atribuindo notas altas a declarações puras de experiência.

---

## Deep Dives Específicos

### 1. Caso SurrealDB (Multi-Modelo)
- **Pergunta:** *"Como o SurrealDB organiza dados multi-modelo?"*
- **Resposta:** *"SurrealDB combina tabelas relacionais, documentos e conexões de grafo em um único motor de persistência."*
- **Mecanismo da Falha:** A pergunta não contém termos do catálogo de SQL relacional. A resposta contém a expressão `"tabelas relacionais"`. O bloco `alien_defines` (linha 1426) identifica que `"tabelas relacionais"` é termo definidor de `relational_query_and_storage`. Como a pergunta não demandou SQL relacional, o sistema assume que o candidato fugiu do assunto e classifica como `OFF_TOPIC`.
- **Decisão Correta:** O candidato abordou diretamente o SurrealDB e respondeu como ele organiza o modelo híbrido. A menção a tabelas relacionais é um aspecto legítimo da capacidade multi-modelo. O sistema deve verificar a pertinência com a entidade principal da pergunta (`SurrealDB`), e não abortar a avaliação por colisão com capacidades de terceiros.

### 2. Caso Distributed Tracing (Polissemia de "Transação")
- **Pergunta:** *"Como rastrear uma transação que passa por múltiplos serviços sem perder o contexto?"*
- **Resposta:** *"Injetaria identificadores de trace e span nos headers das requisições repassando o contexto em cada chamada downstream."*
- **Mecanismo da Falha:** A palavra `"transação"` ativou `_FUNCTIONAL_CAPABILITIES["enterprise_framework_transactions"]`. Esse domínio exige `@Transactional`, `commit`, `rollback`. Ao explicar `trace`, `span` e `headers`, a resposta não continha termos de transação ACID de banco, sendo ejetada como `OFF_TOPIC`.
- **Decisão Correta:** A intenção da pergunta é observabilidade e rastreabilidade distribuída (*"rastrear... que passa por múltiplos serviços sem perder o contexto"*). A palavra `"transação"` refere-se à transação de negócio ou fluxo de requisição, não à transação JDBC/Spring. A resposta é `DIRECT`.

### 3. Caso OpenTelemetry (Ontologia Monolítica)
- **Pergunta:** *"Como o OpenTelemetry padroniza a exportação de telemetria?"*
- **Resposta:** *"OpenTelemetry padroniza a coleta de traces, métricas e logs exportando para backends analíticos via protocolo OTLP."*
- **Mecanismo da Falha:** A palavra `"telemetria"` roteou para `telemetry_and_query_analytics`. Esse domínio foi historicamente populado com termos do Azure Monitor e Kusto (`kusto`, `application insights`, `summarize`, `project`). Como o OpenTelemetry é um padrão aberto que utiliza OTLP, a resposta não continha as palavras da Microsoft, sendo rejeitada como `OFF_TOPIC`.
- **Decisão Correta:** OpenTelemetry é o padrão da indústria para instrumentação e exportação de telemetria. A resposta é `DIRECT`. O sistema não pode tratar um domínio geral (`telemetria`) como sinônimo exclusivo de uma única implementação proprietária (Kusto).

### 4. Caso Optimistic Concurrency Control (Abismo Léxico Problema $\to$ Mecanismo)
- **Pergunta:** *"Como evitar conflitos de escrita concorrente sem travar a linha no banco?"*
- **Resposta:** *"Utilizaria versionamento por timestamp ou contador de versão onde o update valida se o registro não foi alterado antes de commitar."*
- **Mecanismo da Falha:** A pergunta formula a restrição operacional (*evitar conflito*, *sem travar linha*). A resposta formula o mecanismo técnico (*versionamento*, *timestamp*, *contador de versão*, *validação no commit*). Nenhuma palavra essencial da pergunta foi repetida na resposta. Como OCC não estava em `_FUNCTIONAL_CAPABILITIES`, o domínio aberto encontrou `shared_stems == set()` e concluiu `disjunct_open_domain` (`OFF_TOPIC`).
- **Decisão Correta:** Esta é a prova irrefutável de que **interseção lexical $\neq$ relação semântica**. Em arquitetura e engenharia sênior, perguntas frequentemente descrevem sintomas ou requisitos, e respostas descrevem padrões de projeto que resolvem o problema sem repetir as palavras da pergunta.

---

## Stemmer Analysis

A auditoria sobre `_stem_word` confirmou que o stemmer algorítmico do Stage 31.6 cumpre adequadamente seu papel de normalização flexional (verbos e plurais), mas possui fronteiras bem delimitadas:
1. **Responsabilidade Legítima:** Reduzir variantes de flexão gramatical (`correlacionar` $\to$ `correl`, `retries` $\to$ `retry`).
2. **Limitação de Derivação:** Não faz redução morfológica derivacional para agentes (`provador` permanece `provador`, `verificador` permanece `verificador`).
3. **Limite Arquitetural:** O stemmer **não resolve e não deve ser forçado a resolver sinonímia ou relações de causa e efeito** (ex.: ligar *concorrência* a *timestamp*). Tentar resolver problemas semânticos ampliando o stemmer destruiria a discriminação lexical e criaria falsas equivalências espúrias (`log / login`, `síncrono / assíncrono`).

---

## Separação Conceitual: Três Dimensões Distintas

A RCA demonstra que o runtime confunde sistematicamente três perguntas epistemológicas diferentes:

| Dimensão | Pergunta Canônica que Responde | Onde Deve Ser Determinada | Onde o Runtime Atual Erra |
| :--- | :--- | :--- | :--- |
| **Semantic Relevance** | *"Esta resposta aborda aquilo que foi perguntado?"* | Relação funcional e intencional entre Proposição da Pergunta e Proposição da Resposta. | Delega para o catálogo: se usou palavra da lista `valid`, é relevante; se não usou, é `OFF_TOPIC`. |
| **Evidence Strength** | *"Quanto de domínio técnico foi efetivamente demonstrado na resposta?"* | Análise epistêmica da evidência: profundidade do mecanismo, decisões, justificativas e trade-offs. | Confunde repetição de palavras com demonstração: repetir o nome da ferramenta atribui crédito forte. |
| **Evaluation Quality** | *"Qual nota a resposta merece de acordo com a rubrica?"* | Aplicação da rubrica dimensional (0 a 10) baseada no conjunto consolidado de evidências. | O score é forçado para cima ou para baixo com base na classificação de relevância catalográfica. |

---

## Supporting versus Related

A distinção entre `SUPPORTING` e `RELATED` deve ser estritamente funcional e intencional:
- **`SUPPORTING`:** A proposição técnica contribui ativamente para resolver a demanda ou meta formulada na pergunta (ex.: citar *logs e traces* para investigar um incidente; citar *circuit breaker* para mitigar falha em cascata; citar *bulkhead* para isolar recursos).
- **`RELATED`:** A proposição pertence ao mesmo ecossistema temático ou tecnológico, mas não descreve nem apoia o mecanismo demandado (ex.: citar *Swagger/OpenAPI* para explicar o funcionamento do protocolo REST; citar *Spring Data* para explicar injeção de dependência).
- **Erro Atual:** O runtime classifica como `RELATED` respostas que não continham palavras de sua whitelist (como Redpanda em streaming), transformando `RELATED` em uma categoria de penalização lexical.

---

## Por que Expandir o Catálogo é Insustentável

Uma tentação recorrente seria simplesmente adicionar `SurrealDB`, `OpenTelemetry`, `DuckDB`, `OCC` e `Polars` a `_FUNCTIONAL_CAPABILITIES`.

A presente RCA prova formalmente por que essa abordagem é **tecnicamente indefensável**:
1. **Explosão Combinatória:** O ecossistema de software moderno possui dezenas de milhares de ferramentas, bibliotecas e padrões. Qualquer catálogo estático será eternamente incompleto.
2. **Agravamento da Polissemia:** Quanto maior o catálogo, mais palavras polissêmicas (`transação`, `evento`, `filtro`, `canal`, `tabela`) colidirão entre domínios, multiplicando os falsos positivos de intercepção alienígena (`alien_defines`).
3. **Impossibilidade em Conceitos Sem Nome:** Padrões arquiteturais conceituais (OCC, backpressure, idempotência, bulkhead) podem ser formulados em centenas de variações de linguagem natural que não contêm nomes de produtos.
4. **Violação Metodológica de Generalização:** Um sistema de avaliação técnica que exige cadastrar uma tecnologia antes de poder avaliá-la não é um motor de avaliação semântica; é apenas um sistema de checagem de palavras-chave.

---

## Invariantes Arquiteturais Obrigatórias

Para governar a futura correção estrutural no Stage 31.7.2, ficam estabelecidas as seguintes 10 invariantes invioláveis:

1. **Invariante 1 (Agnosticismo a Cadastro):** Nenhuma tecnologia precisa estar previamente cadastrada em dicionários para que sua resposta seja avaliada como semanticamente relevante (`DIRECT`, `PARTIAL`, `SUPPORTING`).
2. **Invariante 2 (Anti-Sequestro Polissêmico):** Nenhuma palavra isolada da pergunta pode determinar sozinha o domínio pretendido quando a frase contiver verbos, substantivos ou contexto que desambigúem a demanda real.
3. **Invariante 3 (Não-Punição por Sinergia de Paradigmas):** A menção a conceitos legítimos de outros domínios técnicos (ex.: mensageria em arquitetura, tabelas relacionais em banco multi-modelo) nunca deve tornar uma resposta `OFF_TOPIC` se ela atender à demanda principal da pergunta.
4. **Invariante 4 (Precedência do Domínio Aberto):** A verificação de fuga de tema (`alien_defines`) nunca deve executar como barreira preliminar antes de avaliar o alinhamento da proposição técnica com a pergunta.
5. **Invariante 5 (Desacoplamento do Julgamento Semântico):** `_FUNCTIONAL_CAPABILITIES` não deve exercer autoridade eliminatória (`OFF_TOPIC` / `RELATED`). Deve atuar exclusivamente como referência taxonômica de metadados para etiquetagem de conceitos reconhecidos.
6. **Invariante 6 (Separação entre Relevância e Interseção Léxica):** A ausência de radicais léxicos compartilhados entre a formulação de um problema e a formulação de uma solução não pode resultar automaticamente em `OFF_TOPIC`.
7. **Invariante 7 (Discriminação Funcional de Suporte):** A qualificação `SUPPORTING` deve ser atribuída a mecanismos que apoiam a resolução da meta formulada (diagnóstico, resiliência, mitigação), independentemente de estarem na whitelist da tecnologia primária.
8. **Invariante 8 (Independência entre Relevância e Força de Evidência):** Uma resposta pode ser 100% `DIRECT` e conter evidência `Weak` (one-liner superficial); uma resposta pode ser `SUPPORTING` e conter evidência `Strong` (demonstração profunda).
9. **Invariante 9 (Preservação da Separação Epistêmica):** A repetição verbal do nome de uma tecnologia ou ferramenta em resposta a uma pergunta de experiência nunca deve gerar evidência conceitual positiva (`conceptual: positive`).
10. **Invariante 10 (Invariância de Representação):** Estilo de formulação (formal, informal, prolixo, conciso, pequenos erros) não deve alterar a relação semântica fundamental.

---

## Proposta Arquitetural Conceitual (Desacoplamento)

Para o Stage 31.7.2, propõe-se um **Modelo de Relevância Baseado em Proposições Funcionais (Proposition-Based Relevance)**:

```text
[Arquitetura Proposta para Stage 31.7.2]

1. Question Intent & Functional Goal Extraction
   - Extrai o objetivo funcional da pergunta:
     * Diagnostic / Troubleshooting (investigar falhas, identificar causas)
     * Architectural Decision / Resilience (proteger contra falhas, escalar, sincronizar)
     * Factual / Core Mechanism (o que é X, como funciona X)
     * Experience Verification (trajetória, histórico declarado)
   - Extrai as Entidades Primárias da pergunta (tecnologias, componentes, padrões).

2. Response Proposition Extraction
   - Extrai as proposições técnicas da resposta (asserções de mecanismo, ações, decisões).

3. Semantic Alignment Engine (Sem Autoridade Prescritiva)
   - Passo A: Verificação de Entidade Principal
     Se a pergunta indaga sobre Entidade E (ex.: SurrealDB, OpenTelemetry, REST), e a resposta
     articula mecanismos de E -> DIRECT (Aberto).
   - Passo B: Verificação de Contribuição Funcional ao Objetivo
     Se a pergunta busca investigar erro 500, e a resposta propõe telemetria -> SUPPORTING.
     Se a pergunta busca resiliência, e a resposta propõe isolamento/fallback -> SUPPORTING.
   - Passo C: Resolução de Problema -> Mecanismo (Domain-Agnostic Patterns)
     Se a pergunta formula um problema de concorrência ou dados, e a resposta articula
     um mecanismo causal de engenharia -> DIRECT / SUPPORTING.
   - Passo D: Discriminação de Adjacência Passiva
     Se a resposta menciona apenas ferramentas de suporte passivo sem explicar mecanismo -> RELATED.
   - Passo E: Detecção Real de Alien Domain
     Apenas declara OFF_TOPIC quando a resposta aborda um mecanismo completamente desconectado
     e sem nenhuma contribuição funcional para a pergunta.

4. Papel Redefinido de _FUNCTIONAL_CAPABILITIES
   - Deixa de ser: Whitelist eliminatória de aprovação/rejeição.
   - Passa a ser: Vocabulário taxonômico de apoio para padronizar nomes de conceitos
     demonstrados nos relatórios (metadata tagging).
```

---

## O que NÃO Deve Mudar

1. O pipeline canônico de 20 etapas de avaliação.
2. A rubrica oficial dimensional de 0 a 10.
3. A separação estrita entre conhecimento técnico, experiência prática e relatórios de avaliação.
4. O isolamento de pontuação (não calibrar scores para aproximar MAE).
5. A preservação dos artefatos históricos congelados.
6. A inexistência de heurísticas baseadas em contagem de palavras (`len <= 6`).
7. O casamento por token boundary (`\b`) prevenindo colisões de substring.

---

## O que Deve Ser Redesenhado no Stage 31.7.2

1. **Remover a autoridade eliminatória de `cap["valid"]`:** Respostas que não contenham termos de `valid` devem ser avaliadas por suas proposições técnicas abertas, não descartadas automaticamente para `OFF_TOPIC`.
2. **Remover a intercepção precoce de `alien_defines`:** A verificação de fuga de tema deve respeitar se a resposta está atendendo à entidade principal da pergunta.
3. **Desacoplar a demanda de palavras isoladas polissêmicas:** Demandas como `"transação"` ou `"telemetria"` devem analisar o contexto da pergunta (ex.: *transação distribuída* $\neq$ *Spring @Transactional*).
4. **Implementar alinhamento problema $\to$ mecanismo para conceitos sem tecnologia.**
5. **Corrigir a extração de evidência para não promover declarações puras de experiência.**

---

## Estratégia de Validação para o Stage 31.7.2

1. Reexecutar a suíte de 65 testes adversariais (`test_stage_31_7_blind_revalidation.py`), visando **65/65 PASS**.
2. Garantir que as 35 suítes do Stage 31.6 continuem **35/35 PASS**.
3. Garantir que a regressão global histórica permaneça **716/716 PASS**.
4. Garantir que o Reference Harness permaneça **8/8 suítes PASS_WITH_WARNINGS**.
5. Revalidar que o MAE do piloto real (Candidato-Piloto-05) se mantenha $\le 0.64$ sem distorções de score.

---

## Limitações Desta Etapa

Esta etapa produziu exclusivamente uma investigação analítica e um desenho arquitetural conceitual. Nenhuma linha de código foi implementada ou testada em ambiente de execução nesta etapa, respeitando a proibição estrita de implementação no Stage 31.7.1.

---

## Conclusão e Gate

A investigação comprovou de forma inequívoca que o bloqueio do Stage 31.7 resulta do uso de `_FUNCTIONAL_CAPABILITIES` como autoridade prescritiva eliminatória. O problema está completamente isolado, reproduzido e compreendido em todas as suas 14 ocorrências. As invariantes arquiteturais e o caminho de desacoplamento estão claramente definidos.

```text
GATE: ROOT_CAUSE_ANALYSIS_COMPLETE
```

O próximo passo canônico é o:
```text
Stage 31.7.2 — Implementation & Decoupling of Semantic Relevance Architecture
```
