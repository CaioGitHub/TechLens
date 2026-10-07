# Stage 31.7 — Post-Correction Human vs System Blind Revalidation

**Status:** Concluído  
**Data:** 2026-10-07  
**Gate:** `POST_CORRECTION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED`  
**Referência Metodológica:** `AGENTS.md`, `SECOND_BRAIN.md`, `GEMINI_GUARDRAILS.md`, `GEMINI_HANDOFF.md`, Stage 31.5, Stage 31.6  

---

## Status do Gate

```text
GATE: POST_CORRECTION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED
```

### Justificativa Síntese do Gate
A revalidação cega e independente do Reference Evaluation Engine após as correções estruturais do Stage 31.6 confirmou a estabilidade e calibração contra o piloto humano real (Candidato-Piloto-05), mantendo **MAE de 0.64 (0.6364)**, **4 concordâncias exatas**, **mediana de erro de 0.05** e **100% de aprovação na regressão histórica (716/716 PASS)**. Foram definitivamente eliminadas as causas do Stage 31.5 relativas a word-count proxy residual (`len <= 6`), colisão de substrings (`orm` em `performance`) e rigidez de flexões em palavras conhecidas.

Entretanto, em cumprimento estrito às Seções 9 e 30 do protocolo de validação cega, a auditoria profunda da estrutura `_FUNCTIONAL_CAPABILITIES` revelou uma **falha estrutural bloqueante de generalização**:
1. **Intercepção por Catálogo Obrigatório (`alien_defines`):** A estrutura `_FUNCTIONAL_CAPABILITIES` atua como um catálogo fechado prescritivo. Quando um candidato articula conceitos válidos que tocam termos definidores de um domínio catalogado (ex.: *SurrealDB multi-modelo combinando tabelas relacionais*), o motor dispara `alien_functional_domain` e classifica a resposta erradamente como `OFF_TOPIC` antes de avaliar a pertinência em domínio aberto.
2. **Colisão de Palavras Polissêmicas em Demandas de Domínio:** Termos isolados presentes em demandas de catálogo (como `"transação"` em `enterprise_framework_transactions` ou `"telemetria"` em `telemetry_and_query_analytics`) sequestram a interpretação da pergunta. Uma pergunta sobre rastreamento de transações distribuídas é forçada a exigir Spring `@Transactional`, rebaixando explicações corretas de distributed tracing (`trace`, `span`, `headers`) para `OFF_TOPIC`.
3. **Lacuna Semântica em Conceitos Livres de Tecnologia:** Quando a formulação de um problema arquitetural e seu mecanismo de solução não compartilham raízes lexicais idênticas (ex.: *Controle de Concorrência Otimista* — pergunta sobre *evitar conflitos de escrita concorrente*, resposta sobre *versionamento com timestamp*), o sistema falha em reconhecer a relação semântica e rotula o caso como `disjunct_open_domain` (`OFF_TOPIC`), a menos que o conceito seja previamente cadastrado no catálogo.

Conforme a Seção 30 do protocolo, a persistência de catálogo obrigatório que impede a generalização em domínio aberto impõe o gate `POST_CORRECTION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED`.

---

## 1. Runtime Version / Freeze

O runtime de avaliação foi estritamente congelado antes do início da validação cega, em conformidade com a Seção 3:

- **Arquivo Canônico:** `reference_runtime/runtime.py`
- **Runtime SHA-256:** `12792d2d5cac5022b401387751846cef53dde0f04de8c9dc29e24fcef12a28ed`
- **Estado do Repositório:** Congelado após o encerramento do Stage 31.6
- **Ambiente de Execução:** Python 3.13, Windows x64, execução puramente local
- **Garantia de Congelamento:** Nenhuma linha do runtime, rubrica, pesos ou modelo de relevância foi modificada durante este estágio.

---

## 2. Blindness

- **Separação Rígida:** O motor de avaliação (`run_interview_pipeline` e `run_real_pilot`) executou de forma 100% cega, sem acesso às notas da referência humana, sem target scores e sem conhecimento dos rótulos esperados.
- **Isolamento do Comparador:** Toda a comparação analítica, cálculo de MAE, métricas estatísticas e diagnósticos questão por questão foi executada em camada externa independente.
- **Não-Otimização:** Não houve nenhum ajuste retroativo de thresholds, constantes ou pesos para melhorar artificialmente os indicadores.

---

## 3. Human Reference

A referência humana independente utilizada neste estágio é a avaliação estruturada congelada no **Stage 31**:

- **Artefato Canônico:** `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/Stage 31 — Human Evaluation Independent.md`
- **Human Reference SHA-256:** `bb57672224368ee0d56134d456d8dfe8fc93674457fac84e68f63bfe88593331`
- **Transcrição de Entrada:** `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-01/Pilot Input - Source Transcript v3.md`
- **Source Transcript SHA-256:** `cc4f32704bfbbca7261b3637f04b36e6950850c2f07d00f4a3b4a89559a51523`
- **Scores Humanos Congelados:**
  `[Q1: 4.0, Q2: 7.0, Q3: 4.0, Q4: 8.0, Q5: 2.0, Q6: 5.0, Q7: 5.0, Q8: 7.0, Q9: 4.0, Q10: 6.0, Q11: 4.0]`
  - Média Humana: **`5.09`** (`5.0909`)
  - Mediana Humana: **`5.00`**
  - Desvio Padrão Humano: **`1.70`**

---

## 4. Stage Comparison

A tabela a seguir consolida a evolução métrica do Reference Evaluation Engine nas 11 questões do piloto real (**Candidato-Piloto-05**) através dos estágios da jornada de validação:

| Questão | Tema Central | Human (Stg 31) | System (Stg 31) | System (Stg 31.2) | System (Stg 31.5) | System (Stg 31.7) | Diff Stg 31.7 (Sys - Hum) | Classificação da Divergência |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Q1** | Trajetória / Java / Spring | 4.0 | 6.00 | 4.00 | 4.00 | **4.00** | **+0.00** | EXACT_AGREEMENT |
| **Q2** | CSS / Front-end | 7.0 | 7.00 | 7.05 | 7.05 | **7.05** | **+0.05** | MINIMAL_DISAGREEMENT |
| **Q3** | Banco de Dados / SQL | 4.0 | 6.00 | 4.00 | 4.00 | **4.00** | **+0.00** | EXACT_AGREEMENT |
| **Q4** | Java 21 / Virtual Threads | 8.0 | 8.00 | 7.05 | 7.05 | **7.05** | **-0.95** | VALID_TECHNICAL_DISAGREEMENT |
| **Q5** | REST Produces / Consumes | 2.0 | 7.05 | 4.45 | 4.45 | **4.45** | **+2.45** | VALID_TECHNICAL_DISAGREEMENT |
| **Q6** | JDBC / Banco | 5.0 | 7.00 | 5.85 | 5.85 | **5.85** | **+0.85** | VALID_TECHNICAL_DISAGREEMENT |
| **Q7** | Concorrência / Sincronização | 5.0 | 6.00 | 6.00 | 6.00 | **6.00** | **+1.00** | VALID_TECHNICAL_DISAGREEMENT |
| **Q8** | CI/CD / Jenkins | 7.0 | 8.00 | 7.05 | 7.05 | **7.05** | **+0.05** | MINIMAL_DISAGREEMENT |
| **Q9** | Arquitetura Hexagonal / SOLID | 4.0 | 6.00 | 4.00 | 4.00 | **4.00** | **+0.00** | EXACT_AGREEMENT |
| **Q10** | Investigação de Erro 500 | 6.0 | 7.00 | 7.65 | 7.65 | **7.65** | **+1.65** | DIMENSION_INTERPRETATION |
| **Q11** | IA Generativa / Adoção | 4.0 | 6.20 | 4.00 | 4.00 | **4.00** | **+0.00** | EXACT_AGREEMENT |

### Métricas Agregadas Comparativas

| Métrica | Stage 31 (Inicial) | Stage 31.2 (Pós-Correção) | Stage 31.5 (Pós-Redesign) | Stage 31.7 (Atual) |
|---|:---:|:---:|:---:|:---:|
| **Média do Sistema** | 6.93 | 5.55 | 5.55 | **5.55** (`5.5545`) |
| **Média Humana** | 5.09 | 5.09 | 5.09 | **5.09** (`5.0909`) |
| **Diferença das Médias** | +1.84 | +0.46 | +0.46 | **+0.46** (`+0.4636`) |
| **Mediana do Sistema** | 7.05 | 5.85 | 5.85 | **5.85** |
| **Mediana Humana** | 5.00 | 5.00 | 5.00 | **5.00** |
| **MAE (Mean Absolute Error)** | **2.01** | **0.64** | **0.64** | **0.64** (`0.6364`) |
| **Erro Máximo** | 5.05 (Q5) | 2.45 (Q5) | 2.45 (Q5) | **2.45** (Q5) |
| **Divergências Materiais ($> 1.0$)** | 6 questões | 2 questões | 2 questões | **2 questões** (Q5, Q10) |
| **Concordâncias Exatas ($\Delta = 0.0$)** | 0 questões | 4 questões | 4 questões | **4 questões** (Q1, Q3, Q9, Q11) |

---

## 5. Historical Failures Revalidated

Os casos históricos foram revalidados e confirmaram comportamento metodológico consistente:
- **D2 (Docker → Kubernetes):** Classificado como `OFF_TOPIC` (`alien_functional_domain`). Não existe regra par `docker ↔ kubernetes`.
- **D3 (SQL → Redis):** Classificado como `OFF_TOPIC` (`alien_functional_domain`). Não existe regra par `sql ↔ redis`.
- **L1 (Dependency Injection → Spring Data):** Classificado como `RELATED` (`thematic_adjacency_without_mechanism`). Não pontua como demonstração de injeção de dependência.
- **Q5 (REST Produces/Consumes vs Kafka):** A divergência humana (+2.45) permanece tecnicamente defensável: o candidato admitiu desconhecimento de REST e falou sobre Kafka consumers. O sistema atribuiu nota 4.45 (insufficient correctness + partial depth no fallback conceitual), enquanto o humano atribuiu 2.0.

---

## 6. Multi-Aspect Coverage

A verificação de cobertura multi-aspecto confirmou a remoção integral de contagem de palavras:
1. **Respostas Curtas:** Perguntas compostas respondidas com assertivas técnicas concisas (8 a 10 palavras, ex.: HTTP métodos e cliente-servidor) receberam `DIRECT` sem rebaixamento arbitrário.
2. **Respostas Prolixas com Omissão:** Respostas extensas (>40 palavras) abordando apenas uma partição receberam `PARTIAL`, com rastreabilidade explícita da demanda omitida (`partial_aspect_coverage`).
3. **Casos Ambíguos Multi-Aspecto:** Em 10 novos casos testados, 8 divergiram corretamente entre `DIRECT` e `PARTIAL` estritamente com base no alinhamento de proposições técnicas.

---

## 7. Functional Capability Audit

A auditoria sobre a estrutura `_FUNCTIONAL_CAPABILITIES` (Seção 9) revelou o **principal bloqueio arquitetural do sistema**:

### Achado Estrutural: Intercepção Indevida por `alien_defines`
No runtime ([`runtime.py:1419-1442`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py#L1419-L1442)), o bloco que verifica se o candidato mencionou termos definidores de um domínio catalogado é executado **antes** do casamento de domínio aberto.
- **Caso SurrealDB:** A pergunta indaga sobre *SurrealDB e modelo multi-modelo*. O candidato explica que ele combina *tabelas relacionais, documentos e grafos*. Como `"tabelas relacionais"` consta no `defining` de `relational_query_and_storage`, e a pergunta não continha as palavras de demanda de SQL relacional, o sistema conclui que o candidato fugiu do assunto e atribui `OFF_TOPIC`.
- **Caso Distributed Tracing:** A pergunta indaga sobre *rastrear uma transação que passa por múltiplos serviços sem perder o contexto*. A palavra `"transação"` faz o sistema assumir que a demanda é `enterprise_framework_transactions`. A resposta correta sobre `trace`, `span` e `headers` é rejeitada como `alien_functional_domain` (`OFF_TOPIC`).
- **Caso OpenTelemetry:** A pergunta indaga sobre *OpenTelemetry e padronização de telemetria*. A palavra `"telemetria"` ativa o domínio `telemetry_and_query_analytics` (que exige termos do Azure Kusto). A resposta sobre OTLP, traces e métricas é rejeitada como `OFF_TOPIC`.

**Conclusão da Auditoria:** `_FUNCTIONAL_CAPABILITIES` degenerou em um **catálogo obrigatório com falsos positivos de fuga de tema**, violando o princípio de domínio aberto da Seção 9.

---

## 8. Morphological Normalization Audit

A camada algorítmica de stemming (`_stem_word`) e normalização Unicode NFD foi auditada:
- **Sucessos:**
  - Variações morfológicas de verbos (*"correlacionar"*, *"correlação"*, *"correlacionando"*, *"correlacionou"*) reduzem para o radical `correl`, garantindo equivalência semântica.
  - Plurais e estrangeirismos técnicos (*"retry"* / *"retries"*, *"repetição"* / *"repetições"*) são devidamente normalizados.
  - Colisões de token boundary (`orm / performance`, `bus / business`, `api / apicultura`, `log / login`) são 100% prevenidas via boundary regex `\b`.
- **Limitações:**
  - O stemmer não possui redução para substantivos de agente terminados em `-ador` / `-edor` / `-idor` (*"provador"* vs *"prova"*, *"verificador"* vs *"verificação"*), impedindo o casamento em domínios abertos específicos.
  - A normalização morfológica não substitui relações semânticas entre conceitos expressos por palavras distintas sem sobreposição léxica.

---

## 9. Unknown Technologies

Foram testadas 10 tecnologias não mapeadas previamente no sistema:
1. **DuckDB (Analítico in-process):** `DIRECT` (Aprovado)
2. **CockroachDB (SQL distribuído / Raft):** `DIRECT` (Aprovado)
3. **SurrealDB (Multi-modelo):** `OFF_TOPIC` (Falso Negativo devido à intercepção de `tabelas relacionais`)
4. **Linkerd (Service mesh em Rust):** `DIRECT` (Aprovado)
5. **OpenTelemetry (Padronização OTLP):** `OFF_TOPIC` (Falso Negativo devido à intercepção da demanda `telemetria`)
6. **Polars (Dataframes em memória):** `DIRECT` (Aprovado)
7. **Redpanda (Streaming C++):** `RELATED` (Falso Positivo de adjacência por menção a Kafka)
8. **Triton Server (Inferência em GPU):** `DIRECT` (Aprovado)
9. **Spire / SPIFFE (Identidade criptográfica):** `DIRECT` (Aprovado)
10. **Fluentbit (Coleta de logs):** `DIRECT` (Aprovado)

**Resultado:** 7 de 10 tecnologias desconhecidas generalizaram corretamente; 3 falharam por intercepção indevida do catálogo prescritivo.

---

## 10. Technology-Free Concepts

Foram testados 10 conceitos formulados sem menção a produtos comerciais:
- **Aprovados:** Backpressure (DIRECT), Idempotência com deduplicação (DIRECT), Expiração TTL (DIRECT).
- **Falhas de Associação Semântica:**
  - *Controle de Concorrência Otimista:* Classificado como `OFF_TOPIC` por descontinuidade léxica entre a formulação da demanda (*"evitar conflito de escrita"*) e o mecanismo (*"versionamento com timestamp"*).
  - *Distributed Context Propagation:* Classificado como `OFF_TOPIC` por intercepção da palavra `"transação"` pelo catálogo de Spring transactions.
  - *Regression Detection P99:* Classificado como `OFF_TOPIC` por descontinuidade léxica entre a pergunta e os termos de telemetria.
  - *Token Bucket Rate Limiting:* Classificado como `OFF_TOPIC` por descontinuidade léxica.

---

## 11. Supporting vs Related

A discriminação funcional permaneceu robusta:
- Respostas diagnósticas ativas correlacionando logs e traces para erro 500 receberam `SUPPORTING` com contribuição funcional ativa.
- Respostas que citam ferramentas de documentação passivas (Swagger/OpenAPI) em perguntas conceituais de REST receberam `RELATED` sem contribuição funcional.

---

## 12. Experience Semantics

A separação epistêmica foi confirmada:
- Menção declarativa isolada (*"Trabalhei 2 anos com Kubernetes"*) -> `experience_declaration` com completude `Insufficient`.
- Hipótese (*"Eu hipotetizaria que o problema está na conexão"*) -> `hypothesis_formulation`.
- Demonstração prática detalhada com trade-offs e métricas -> `demonstrated_experience` com aplicação prática `Strong`.

---

## 13. Representation Invariance

Testes com formulações formais, informais, coloquiais e com pequenas incorreções gramaticais convergiram para a mesma classificação semântica (`DIRECT`), comprovando a estabilidade da invariância de representação.

---

## 14. False Positives

Respostas preenchidas deliberadamente com "sopa de jargões" (*"arquitetura ágil moderna em cloud com microsserviços e DevOps"*) em perguntas específicas sobre isolamento de containers foram rejeitadas com sucesso, não obtendo classificação `DIRECT` nem pontuação de mecanismo.

---

## 15. False Negatives

Respostas concisas porém diretas e tecnicamente corretas não foram rotuladas como `OFF_TOPIC`, desde que as proposições cobrissem a demanda essencial.

---

## 16. Mutation Tests

Os testes de mutação semântica demonstraram causalidade:
- Inversão ou omissão da proposição técnica converte `DIRECT` em `PARTIAL`.
- Adição de enchimento irrelevante em resposta parcial não inflaciona a qualificação.

---

## 17. Determinism

Execuções repetidas do pipeline completo sobre o piloto real e sobre fixtures controladas produziram exatamente os mesmos scores, dimensões e razões de avaliação.

---

## 18. Isolation

A permutação e inversão da ordem de execução de casos na suíte não alteraram em nenhuma fração os resultados individuais, confirmando a ausência de estado compartilhado ou vazamento entre entrevistas.

---

## 19. Runtime Audit

A auditoria estrutural no runtime confirmou:
- Ausência total de proxies baseados em contagem de palavras (`len <= 6`, `split()`).
- Ausência de regras de pares tecnológicos hardcoded (`docker ↔ kubernetes`).
- Presença de boundary regex `\b` prevenindo colisões de substring.
- Presença da falha de intercepção catalográfica em `alien_defines`.

---

## 20. Regression

- **Regressão Global (`run_reference_runtime_tests.py`):** **716 de 716 testes PASS (0 falhas)**.
- **Reference Harness (`run_reference_harness.py`):** **8 de 8 suítes PASS_WITH_WARNINGS**.
- **Suíte Estrutural do Stage 31.6 (`test_stage_31_6_controlled_correction.py`):** **35 de 35 PASS**.
- **Suíte Adversarial Cega do Stage 31.7 (`test_stage_31_7_blind_revalidation.py`):** **51 PASS, 14 FAIL (78.5% aprovação)**.

---

## 21. Residual Divergences

No piloto real (Candidato-Piloto-05), as divergências com o humano permaneceram em:
- **Q5 (+2.45):** O candidato falou de Kafka quando perguntado sobre REST produces/consumes. Divergência metodológica aceitável de fallback conceitual.
- **Q10 (+1.65):** O candidato sugeriu debug/print para investigar erro 500. O humano considerou fraco (6.0), enquanto a rubrica automatizada pontuou reasoning como Strong pela coerência da sequência lógica (7.65).

---

## 22. Root Cause Analysis (Falhas Identificadas no Stage 31.7)

1. **Root Cause 1 — Precedência Invertida do Catálogo (`alien_defines`):** A verificação de domínios alienígenas é executada antes da verificação de pertinência em domínio aberto. Se o candidato menciona qualquer termo do catálogo em uma resposta de domínio aberto, o sistema força `OFF_TOPIC`.
2. **Root Cause 2 — Demanda com Gatilho Monopalavra Polissêmico:** Termos como `"transação"` e `"telemetria"` em demandas forçam a classificação da pergunta para escopos específicos de framework corporativo (Spring/Kusto), gerando falso negativo em contextos distribuídos modernos (distributed tracing, OTel).
3. **Root Cause 3 — Falta de Mapeamento Semântico Demanda-Mecanismo:** Em conceitos livres de tecnologia, a ausência de interseção léxica entre o problema e a solução impede a conexão semântica no motor puramente lexical.

---

## 23. Historical Integrity

Todos os artefatos históricos (Stages 31, 31.1, 31.2, 31.3, 31.4, 31.4.1, 31.4.2, 31.5 e 31.6) permanecem inalterados, preservados e auditáveis no repositório.

---

## 24. Limitations

1. O motor de pertinência semântica ainda depende excessivamente da presença de radicais compartilhados no texto quando o conceito não está cadastrado em `_FUNCTIONAL_CAPABILITIES`.
2. O catálogo de capacidades necessita de reformulação estrutural para operar como suporte auxiliar e não como filtro eliminatório prévio.

---

## 25. Final Assessment

O Stage 31.7 cumpriu integralmente sua missão de validação cega independente:
- Demonstrou que as correções do Stage 31.6 eliminaram definitivamente os word-count proxies e as colisões de substring.
- Revelou com precisão cirúrgica a próxima barreira estrutural que impede o sistema de ser liberado para produção: **a intercepção indevida do catálogo prescritivo de capacidades funcionais**.

---

## 26. Gate Decision

Em cumprimento rigoroso aos critérios da Seção 30:

```text
GATE: POST_CORRECTION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED
```

O próximo passo é abrir o **Stage 31.7.1 — Root Cause Analysis & Architectural Decoupling of Functional Catalog**, para eliminar a intercepção indevida de domínio aberto sem recorrer a novas listas de exceções.
