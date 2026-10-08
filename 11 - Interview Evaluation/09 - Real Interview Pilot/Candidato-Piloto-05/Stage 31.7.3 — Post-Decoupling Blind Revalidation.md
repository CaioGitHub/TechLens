# Stage 31.7.3 — Post-Decoupling Blind Revalidation

**Status:** Concluído (Bloqueado por Critério Metodológico)  
**Data:** 2026-10-08  
**Gate:** `POST_DECOUPLING_BLIND_REVALIDATION_BLOCKED`  
**Referência Metodológica:** `AGENTS.md`, `SECOND_BRAIN.md`, `GEMINI_GUARDRAILS.md`, `GEMINI_HANDOFF.md`, Stage 31.7, Stage 31.7.1, Stage 31.7.2  

---

## Status

```text
GATE: POST_DECOUPLING_BLIND_REVALIDATION_BLOCKED
```

A revalidação cega pós-desacoplamento foi executada de forma estritamente independente sobre o runtime congelado (`reference_runtime/runtime.py`). Em conformidade absoluta com as regras metodológicas do projeto (`AGENTS.md`, Seções 1, 16, 17 e 18), **nenhuma linha do runtime foi modificada durante esta etapa de validação**.

O processo de teste cego executou 92 casos de validação independente, revelando que a arquitetura implementada no Stage 31.7.2:
1. **Sanou com sucesso** as falhas de tecnologias inéditas abertas (10/10 PASS), independência de catálogo (PASS), isolamento do motor legado em Shadow Mode (PASS), determinismo (PASS) e alinhamento do piloto real (MAE 0.64);
2. **Porém, revelou novas classes estruturais de falha** (38 falhas em 92 casos, 58.7% PASS, 41.3% FAIL), demonstrando que o desacoplamento de `_FUNCTIONAL_CAPABILITIES` no Stage 31.7.2 foi incompleto: substituiu um catálogo global por blocos contextuais rígidos com mini-whitelists locais, manteve passe-livre para menções de entidade sem mecanismo demonstrado e reteve dependência de frases literais para resolver relações problema $\to$ mecanismo.

Seguindo o princípio inegociável de que **"um bloqueio é um resultado válido da validação"**, o gate é declarado `POST_DECOUPLING_BLIND_REVALIDATION_BLOCKED`. Nenhuma tentativa de correção artificial foi realizada no runtime.

---

## Gate

```text
GATE: POST_DECOUPLING_BLIND_REVALIDATION_BLOCKED
```

---

## Runtime Hash

Em cumprimento estrito à Seção 4 do mandato:

| Momento | Algoritmo | Hash SHA-256 | Status de Integridade |
| :--- | :---: | :--- | :---: |
| **Pré-Execução** | SHA-256 | `9B466EB010CD586E0BA8699CCE5529C52A3C28540969B7F8C17BD3CF0D4E0A44` | Base Congelada |
| **Pós-Execução** | SHA-256 | `9B466EB010CD586E0BA8699CCE5529C52A3C28540969B7F8C17BD3CF0D4E0A44` | 100% Idêntico |

O runtime permaneceu inviolado durante toda a fase de avaliação.

---

## Blindness Verification

A revalidação respeitou integralmente o princípio de separação entre execução e comparação:
1. **Isolamento de Entradas**: O motor foi executado recebendo unicamente dicionários de pergunta (`{"text": ...}`) e resposta (`{"reconstructed_text": ...}`).
2. **Ausência de Metadados Guia**: Nenhuma avaliação humana, score-alvo, histórico de falhas ou expectativa de classificação foi injetada no pipeline de execução.
3. **Persistência Prévia**: As saídas brutas do sistema foram registradas e capturadas antes de qualquer confronto com os oracles e asserções de validação.

---

## Historical Case Revalidation

Revalidação dos casos derivados das falhas históricas F01–F14 do Stage 31.7:

| ID | Tema do Caso | Esperado | Obtido no Runtime Congelado | Status |
|---|---|:---:|:---:|:---:|
| **F01** | Experiência declarada sem mecanismo | `RELATED` | `RELATED` (`thematic_adjacency_without_mechanism`) | PASS |
| **F02** | Hipótese formulada epistemologicamente | `hypothesis` | `hypothesis` (`conditional`) | PASS |
| **F03** | Zero-knowledge proofs em domínio aberto | `DIRECT` | `DIRECT` (`direct_mechanism_assertion`) | PASS |
| **F04** | REST + Paginação (apenas REST respondido) | `PARTIAL` | `DIRECT` (falha na detecção de aspecto secundário) | **FAIL** |
| **F05** | Consistência eventual com mensageria assíncrona | `DIRECT` | `PARTIAL` (rebaixamento indevido) | **FAIL** |
| **F06** | SurrealDB multi-modelo híbrido | `DIRECT` | `DIRECT` | PASS |
| **F07** | OpenTelemetry padronização OTLP | `DIRECT` | `DIRECT` | PASS |
| **F08** | Redpanda compatibilidade Kafka C++ | `DIRECT` | `DIRECT` | PASS |
| **F09** | OCC concorrência sem bloqueio de linha | `DIRECT` | `DIRECT` | PASS |
| **F10** | Propagação de contexto distribuído | `DIRECT` | `DIRECT` | PASS |
| **F11** | Circuit breaker com fallback | `DIRECT` / `SUPPORTING` | `DIRECT` | PASS |
| **F12** | Investigação de regressão P99 | `DIRECT` / `SUPPORTING` | `SUPPORTING` | PASS |
| **F13** | Isolamento de recursos via Bulkhead | `DIRECT` / `SUPPORTING` | `DIRECT` | PASS |
| **F14** | Token bucket protegendo endpoints | `DIRECT` | `DIRECT` | PASS |

**Resultado Histórico**: 12/14 casos passando (85.7% PASS, 14.3% FAIL). Permanecem pendências no particionamento semântico de demandas multi-aspecto (F04) e composição sinérgica de mensageria assíncrona (F05).

---

## Unseen Technology Cases

Foram avaliadas 10 tecnologias inéditas, ausentes de qualquer catálogo histórico:

| # | Tecnologia Inédita | Pergunta | Resposta | Resultado | Status |
| :-: | :--- | :--- | :--- | :---: | :---: |
| 1 | ClickHouse | Otimização para queries analíticas | Armazenamento colunar com compressão pesada por bloco e ordenação esparsa | `DIRECT` | PASS |
| 2 | ScyllaDB | Baixa latência e alta vazão | Arquitetura shard-per-core no Seastar sem locks globais | `DIRECT` | PASS |
| 3 | Temporal | Workflows de longa duração | Workflows como código determinístico com replay de eventos | `DIRECT` | PASS |
| 4 | Envoy Proxy | Gerenciamento L7 e conexões | Event loop não bloqueante com cadeia de filtros HTTP e service discovery | `DIRECT` | PASS |
| 5 | Apache Arrow | Troca de dados analíticos in-memory | Formato colunar padronizado em memória sem serialização entre processos | `DIRECT` | PASS |
| 6 | TiKV | Armazenamento transacional distribuído | Consenso Raft para replicação e Percolator para ACID distribuído | `DIRECT` | PASS |
| 7 | DuckDB | Processamento analítico embutido | Queries analíticas colunares in-process com execução vetorizada | `DIRECT` | PASS |
| 8 | Vector | Pipelines de telemetria de alta escala | Pipeline concorrente em Rust com buffers em disco e transformação declarativa | `DIRECT` | PASS |
| 9 | NATS JetStream | Streams e persistência leve | Streams distribuídos com garantias at-least-once e desduplicação nativa | `DIRECT` | PASS |
| 10 | Meilisearch | Busca instantânea com typo-tolerance | Índices invertidos com ordenação personalizada e distância de Levenshtein | `DIRECT` | PASS |

**Resultado**: 10/10 PASS (100%). O motor desacoplado reconhece tecnologias inéditas desde que o candidato articule suas proposições arquiteturais.

---

## Technology-Free Concept Cases

Avaliação de 10 conceitos fundamentais sem nomes de ferramentas ou produtos:

| # | Conceito Livre | Demanda da Pergunta | Proposição Técnica da Resposta | Esperado | Obtido | Status |
| :-: | :--- | :--- | :--- | :---: | :---: | :---: |
| 1 | Concorrência Otimista | Conflito em registros concorrentes sem bloqueio de linha | Versionamento com checagem no commit | `DIRECT` | `OFF_TOPIC` | **FAIL** |
| 2 | Propagação de Contexto | Correlacionar requisições através de múltiplos serviços | Injetar identificadores de correlação nos cabeçalhos | `DIRECT` | `DIRECT` | PASS |
| 3 | Circuit Breaking | Proteger arquitetura quando dependente falha continuamente | Disjuntor que interrompe requisições e aciona rota degradada | `SUPPORTING`/`DIRECT` | `OFF_TOPIC` | **FAIL** |
| 4 | Rate Limiting | Restringir volume de chamadas por usuário | Balde de fichas descartando requisições excedentes | `DIRECT` | `OFF_TOPIC` | **FAIL** |
| 5 | Degradação Suave | Manter operacional durante picos extremos de tráfego | Desativar módulos não essenciais e servir dados em cache | `SUPPORTING`/`DIRECT` | `OFF_TOPIC` | **FAIL** |
| 6 | Prevenção de Deadlock | Prevenir impasses mútuos com múltiplos recursos | Ordem estrita e global para aquisição de recursos | `DIRECT` | `DIRECT` | PASS |
| 7 | Isolamento Bulkhead | Compartimentar recursos de execução | Isolaria pools de processamento dedicados | `SUPPORTING`/`DIRECT` | `DIRECT` | PASS |
| 8 | Backpressure | Fluxo quando produção supera capacidade de consumo | Consumidor sinaliza ao produtor taxa que consegue absorver | `DIRECT` | `DIRECT` | PASS |
| 9 | Idempotência | Evitar efeitos colaterais duplicados em reenvios | Chave exclusiva na requisição validada antes de persistir | `DIRECT` | `OFF_TOPIC` | **FAIL** |
| 10 | Diagnóstico de Leak | Consumo progressivo de memória não liberada | Comparar capturas consecutivas de memória após coletas | `SUPPORTING`/`DIRECT` | `DIRECT` | PASS |

**Resultado**: 5/10 PASS, 5/10 FAIL.  
**Causa Identificada**: Quando a resposta usa vocabulário conceitual em português ("balde de fichas", "disjuntor", "chave exclusiva", "dados em cache") sem os termos em inglês ("token bucket", "circuit breaker", "idempotency key"), o sistema rejeita a resposta como `OFF_TOPIC`.

---

## Lexical Gap Cases

Avaliação de casos com zero sobreposição léxica entre a formulação da pergunta e a resposta:

| # | Problema | Mecanismo | Esperado | Obtido | Status |
| :-: | :--- | :--- | :---: | :---: | :---: |
| 1 | Duas requisições sobrescrevendo alterações | Versionamento timestamp com validação atômica pré-commit | `DIRECT` | `OFF_TOPIC` | **FAIL** |
| 2 | Lentidão de terceiro derrubando aplicação | Circuit breaker abrindo circuito com fallback | `SUPPORTING`/`DIRECT` | `DIRECT` | PASS |
| 3 | Acompanhar pedido por dezenas de instâncias | Injetar trace e span nos headers propagando contexto | `DIRECT` | `OFF_TOPIC` | **FAIL** |
| 4 | Conter disparos massivos de requisições | Token bucket ou sliding window limitando taxa | `DIRECT` | `OFF_TOPIC` | **FAIL** |
| 5 | Diagnosticar lentidão pós-atualização | Comparar percentil 99 com linha de base via telemetria | `SUPPORTING`/`DIRECT` | `OFF_TOPIC` | **FAIL** |
| 6 | Entrada de mensagens superando fila | Backpressure com buffers delimitados e desaceleração | `DIRECT` | `OFF_TOPIC` | **FAIL** |
| 7 | Impedir cobrança em dobro em clique duplo | Chave de idempotência validando se token já foi executado | `DIRECT` | `DIRECT` | PASS |
| 8 | Travamento de requisições com CPU em zero | Thread dump procurando estados bloqueados e espera mútua | `SUPPORTING`/`DIRECT` | `OFF_TOPIC` | **FAIL** |
| 9 | Esgotamento de conexões de parceiro afetando outros | Bulkhead com pools isolados e limites dedicados | `SUPPORTING`/`DIRECT` | `OFF_TOPIC` | **FAIL** |
| 10 | Evitar exibir dados desatualizados | TTL agressivo e invalidação ativa com write-through | `DIRECT` | `OFF_TOPIC` | **FAIL** |

**Resultado**: 2/10 PASS, 8/10 FAIL.  
**Causa Identificada**: As regras contextuais de problema $\to$ mecanismo no runtime dependem da presença exata de certas frases na pergunta (ex.: `"conflitos de escrita concorrente sem travar a linha no banco"`). Variações semânticas na pergunta ("duas requisições concorrentes sobrescrevendo alterações") não ativam a rota e sofrem queda em cascata para `OFF_TOPIC`.

---

## Entity Anchor Cases

Avaliação da Seção 8 e Seção 10: **menção ao nome da tecnologia não pode conferir classificação `DIRECT` sem mecanismo demonstrado**:

| # | Pergunta | Resposta (Entidade presente, mecanismo ausente) | Esperado | Obtido | Status |
| :-: | :--- | :--- | :---: | :---: | :---: |
| 1 | OpenTelemetry padronização OTLP | Usei OpenTelemetry durante dois anos na empresa anterior | `RELATED` | `RELATED` | PASS |
| 2 | Kubernetes readiness probe | Temos um cluster de Kubernetes gerenciado na nuvem | `RELATED` | `DIRECT` | **FAIL** |
| 3 | Kafka ordenação de mensagens | Kafka é uma plataforma amplamente adotada pela nossa equipe | `RELATED` | `DIRECT` | **FAIL** |
| 4 | Redis eviction policies | Instalei uma instância de Redis no ambiente local para testes | `RELATED` | `DIRECT` | **FAIL** |
| 5 | Spring Dependency Injection | Spring Boot é o framework utilizado em quase todos os projetos | `RELATED` | `DIRECT` | **FAIL** |
| 6 | PostgreSQL MVCC | PostgreSQL é o banco relacional padrão da infraestrutura | `RELATED` | `DIRECT` | **FAIL** |
| 7 | Docker namespaces e cgroups | Gosto de rodar imagens Docker para desenvolvimento diário | `RELATED` | `DIRECT` | **FAIL** |
| 8 | Istio interceptação de tráfego | A equipe de infraestrutura instalou Istio recentemente | `RELATED` | `DIRECT` | **FAIL** |
| 9 | SurrealDB modelo multi-modelo | O SurrealDB foi desenvolvido em Rust pela comunidade | `RELATED` | `DIRECT` | **FAIL** |
| 10 | ClickHouse ordenação esparsa | ClickHouse foi criado por engenheiros na Europa para analítica | `RELATED` | `DIRECT` | **FAIL** |

**Resultado**: 1/10 PASS, 9/10 FAIL.  
**Causa Estrutural Crítica**: O caso 1 (OpenTelemetry) passou apenas porque havia um filtro ad-hoc para declarações de experiência com `"usei"`. Nos demais casos, frases factuais biográficas ou operacionais que citam a tecnologia ("temos um cluster...", "instalamos...", "desenvolvido em Rust...") são capturadas pelo catálogo de Step 9 ou pelo fallback aberto como `DIRECT`. **A entidade continua operando como passe-livre para `DIRECT` na maioria dos cenários.**

---

## Supporting vs Related

Avaliação da capacidade de discriminar contribuição funcional (`SUPPORTING`) de adjacência de ecossistema (`RELATED`):

| Par | Pergunta | Resposta | Esperado | Obtido | Status |
| :-: | :--- | :--- | :---: | :---: | :---: |
| 1A | Investigar HTTP 500 | Correlacionar logs e traces | `SUPPORTING` | `SUPPORTING` | PASS |
| 1B | Investigar HTTP 500 | Nossa aplicação roda Spring Boot e Hibernate | `RELATED` | `OFF_TOPIC` | **FAIL** |
| 2A | Proteger contra queda de terceiros | Configurar fallback com cache e degradar gracefully | `SUPPORTING`/`DIRECT` | `OFF_TOPIC` | **FAIL** |
| 2B | Proteger contra queda de terceiros | Nossos microsserviços usam Maven para compilar | `RELATED` | `RELATED` | PASS |
| 3A | Investigar latência pós-deploy | Monitorar taxa de GC e pausas da JVM com APM | `SUPPORTING`/`DIRECT` | `OFF_TOPIC` | **FAIL** |
| 3B | Investigar latência pós-deploy | Deploy feito com esteira automatizada de CI/CD | `RELATED` | `RELATED` | PASS |
| 4A | Diagnosticar threads travadas | Capturar thread dump e inspecionar BLOCKED | `SUPPORTING`/`DIRECT` | `DIRECT` | PASS |
| 4B | Diagnosticar threads travadas | O servidor possui 16 núcleos Intel Xeon | `RELATED` | `OFF_TOPIC` | **FAIL** |
| 5A | Otimizar consultas lentas | Analisar plano com EXPLAIN ANALYZE | `SUPPORTING`/`DIRECT` | `OFF_TOPIC` | **FAIL** |
| 5B | Otimizar consultas lentas | A tabela possui mais de 10 milhões de registros | `RELATED` | `RELATED` | PASS |

**Resultado**: 5/10 PASS, 5/10 FAIL.

---

## Multi-Aspect

Avaliação de perguntas multi-aspecto:

| Teste | Pergunta | Resposta | Esperado | Obtido | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| REST + Paginação (Aspecto 1 apenas) | REST e paginação | Apenas verbos HTTP e recursos | `PARTIAL` | `DIRECT` | **FAIL** |
| REST + Paginação (Aspecto 2 apenas) | REST e paginação | Apenas limit, offset e cursor | `PARTIAL` | `DIRECT` | **FAIL** |
| REST + Paginação (Ambos conciso) | REST e paginação | HTTP para recursos + limit/offset | `DIRECT` | `DIRECT` | PASS |
| Retry + Rate Limiting (Aspecto 1 apenas) | Retry e rajadas | Apenas backoff com jitter | `PARTIAL` | `DIRECT` | **FAIL** |
| Retry + Rate Limiting (Ambos conciso) | Retry e rajadas | Backoff com jitter + circuit breaker | `DIRECT` | `DIRECT` | PASS |
| Kafka (Partição + Rebalanceamento com padding) | Partição e rebalance | Padding longo cobrindo só partição | `PARTIAL` | `PARTIAL` | PASS |
| Kafka (Ambos conciso) | Partição e rebalance | Partição determinística + rebalanceamento | `DIRECT` | `DIRECT` | PASS |

**Resultado**: 4/7 PASS, 3/7 FAIL.  
**Causa Identificada**: Respostas que cobrem apenas um aspecto ainda ganham `DIRECT` prematuramente quando o motor de aspecto falha em segmentar a pergunta composta por conectivos interrogativos naturais.

---

## Generic Token False Positives

Avaliação contra falsos positivos induzidos por tokens genéricos (`transaction`, `endpoint`, `thread`, `telemetry`, `service`, `resource`):

| Teste | Pergunta | Resposta com Buzzwords | Esperado | Obtido | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| G01 | Distributed tracing | "Uma transaction pode possuir vários endpoints" | $\neq$ `DIRECT` | `OFF_TOPIC` | PASS |
| G02 | Observabilidade | "O sistema possui várias threads e múltiplos services" | $\neq$ `DIRECT` | `OFF_TOPIC` | PASS |
| G03 | Circuit breaker | "A aplicação recebe requests e aloca resources" | $\neq$ `DIRECT` | `OFF_TOPIC` | PASS |
| G04 | Deadlocks | "Os services manipulam data em tabelas comuns" | $\neq$ `DIRECT` | `OFF_TOPIC` | PASS |
| G05 | Readiness probe | "O container roda uma application com telemetry" | $\neq$ `DIRECT` | `OFF_TOPIC` | PASS |

**Resultado**: 5/5 PASS (100%). O sistema resiste eficientemente ao empilhamento de jargões genéricos sem mecanismo.

---

## False Negative Cases

Avaliação de respostas válidas informais ou concisas:

| Teste | Pergunta | Resposta Válida Concisa / Informal | Esperado | Obtido | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| FN01 | Rate limiting | "Token bucket limitando taxa por cliente" | `DIRECT` | `DIRECT` | PASS |
| FN02 | Tracing causal | "Passando IDs de correlação nos envelopes HTTP" | `DIRECT` | `OFF_TOPIC` | **FAIL** |
| FN03 | Deadlock conciso | "Adquirindo travas em ordem hierárquica estrita" | `DIRECT` | `OFF_TOPIC` | **FAIL** |
| FN04 | Concorrência casual | "Boto uma coluna de versão lá e vejo se ninguém mudou antes" | `DIRECT` | `OFF_TOPIC` | **FAIL** |

**Resultado**: 1/4 PASS, 3/4 FAIL. As formulações informais e indiretas sofrem rejeição indevida.

---

## Experience / Epistemic Cases

Avaliação da separação entre declaração biográfica, hipótese e conhecimento demonstrado:

| Teste | Texto Avaliado | Dimensões Esperadas | Dimensões Obtidas | Status |
| :--- | :--- | :--- | :--- | :---: |
| EP01 | "Trabalhei dois anos com Kubernetes" | `experience_declaration` (sem `demonstrated_experience`) | `['experience_declaration']` | PASS |
| EP02 | "No Kubernetes, configuraria readiness probe..." | `conceptual: positive` | `['conceptual']` | PASS |
| EP03 | "Eu hipotetizaria que o gargalo está no pool..." | `hypothesis` | `['hypothesis']` | PASS |
| EP04 | "Trabalhei com Kubernetes e configurávamos readiness probe..." | `experience_declaration` + `demonstrated_experience` | `['experience_declaration', 'conceptual']` | **FAIL** |

**Resultado**: 3/4 PASS, 1/4 FAIL. A distinção básica é preservada, mas respostas mistas perdem a etiqueta de experiência demonstrada.

---

## Representation Invariance

Avaliação da estabilidade semântica frente a variações formais e de extensão:

| Caso | Variação A | Variação B | Esperado | Obtido | Status |
| :--- | :--- | :--- | :---: | :---: | :---: |
| Retry | Formal ("exponential backoff com jitter") | Informal ("backoff com jitter nos retries") | Mesma classe | `DIRECT` / `DIRECT` | PASS |
| OCC | Curta ("versionamento antes do commit") | Longa explicativa (4 linhas) | Mesma classe | `DIRECT` vs `OFF_TOPIC` | **FAIL** |
| Autocorreção | Com hesitação e autocorreção explícita | Direta | `DIRECT` | `DIRECT` | PASS |

**Resultado**: 2/3 PASS, 1/3 FAIL. Respostas longas que explicam o mecanismo sem as palavras-chave da lista curta de OCC são rejeitadas.

---

## Contradictory Meaning

Avaliação de sensibilidade a significados opostos com vocabulário similar:

- *Resposta Válida*: "Usaria circuit breaker para interromper chamadas e retornar fallback." $\to$ `DIRECT` (esperado).
- *Resposta Contraditória*: "Eu evitaria circuit breaker porque ele aumenta a propagação de falhas no sistema." $\to$ `OFF_TOPIC` (esperado: rejeição de mecanismo técnico válido).
- *Resultado*: FAIL na asserção porque a pergunta usou "serviço externo" em vez de "dependência externa", gerando `OFF_TOPIC` em ambas.

---

## UNKNOWN Cases

Avaliação de robustez estrutural sob entradas corrompidas ou ausentes:

| Teste | Condição de Entrada | Classificação Obtida | `needs_review` | Status |
| :--- | :--- | :---: | :---: | :---: |
| Resposta vazia | `reconstructed_text: ""` | `UNKNOWN` | `True` | PASS |
| Resposta desvinculada | `question_id: "unknown"` | `UNKNOWN` | `True` | PASS |
| Desconhecimento explícito | "Não conheço quase nada sobre isso, não sei" | `INSUFFICIENT` | `False` | PASS |

**Resultado**: 3/3 PASS (100%).

---

## Catalog Independence

- Comparação de tecnologia catalogada (Kafka) vs não-catalogada (Redpanda) com semântica idêntica: ambas classificadas como `DIRECT`.
- Ausência de tecnologia no catálogo não rebaixa automaticamente para `OFF_TOPIC`.
- **Status**: PASS.

---

## Legacy Independence

- Execução da função pública `evaluate_semantic_relevance_shadow(question, response)` confirmou que o motor legado é puramente observacional e não altera as decisões canônicas do motor desacoplado.
- **Status**: PASS.

---

## Mutation Tests

- **Mutação Semântica**: Alterar a relação técnica (validar conformidade com esquema JSON em vez de versão concorrente) altera a classificação de `DIRECT` para `OFF_TOPIC`/`RELATED`. (PASS)
- **Mutação Representacional**: Casing, espaços em branco e pontuação mantêm a classificação intacta. (PASS)

---

## Regression

Execução completa das suítes de teste do repositório:

```text
Ran 911 tests in 35.056s
PASSED: 873
FAILED: 38 (exclusivas da suíte cega do Stage 31.7.3)
Status: FAIL (em conformidade com o bloqueio da revalidação)
```

Suítes históricas preservadas:
- 819/819 testes históricos PASS (zero regressões no código existente).
- Suíte do Candidato Piloto real (Candidato-Piloto-05): MAE exatamente preservado em 0.64.

---

## Determinism

Execuções repetidas da suíte (5 iterações com diferentes permutações) produziram resultados 100% idênticos, confirmando total determinismo e ausência de efeitos colaterais de estado global.

---

## Metrics

| Métrica | Stage 31.7 | Stage 31.7.2 | Stage 31.7.3 (Atual) |
| :--- | :---: | :---: | :---: |
| **Total de Casos na Suíte Cega** | 65 | 38 | 92 |
| **Casos PASS** | 51 (78.5%) | 38 (100%) | 54 (58.7%) |
| **Casos FAIL** | 14 (21.5%) | 0 (0%) | 38 (41.3%) |
| **Tecnologias Inéditas PASS** | 0/10 | 10/10 | 10/10 (100%) |
| **Conceitos Livres de Tecnologia PASS** | 0/10 | 10/10 | 5/10 (50%) |
| **Ancoragem de Entidade sem Passe-Livre** | 0/10 | 1/1 | 1/10 (10%) |
| **Casos com Zero Lexical Gap PASS** | 0/10 | 3/3 | 2/10 (20%) |
| **Candidato-Piloto-05 MAE** | 0.64 | 0.64 | 0.64 |
| **Runtime SHA-256 Alterado?** | Sim | Sim | **NÃO (CONGELADO)** |

---

## Divergence Analysis

As 38 divergências identificadas foram categorizadas nas seguintes causas estruturais:

### Classe 1: Entidade como Passe-Livre (9 falhas)
Respostas contendo o nome da tecnologia e fatos irrelevantes ("temos um cluster...", "instalamos no servidor...", "criado em Rust...") continuam ganhando `DIRECT` porque Step 9 e Step 11 consideram qualquer menção substantiva de entidade como evidência direta.

### Classe 2: Fragilidade Lexical em Relações Problema $\to$ Mecanismo (13 falhas)
As regras de Step 4 foram construídas com padrões literais fechados na pergunta. Quando a formulação interrogativa muda (ex.: "duas requisições concorrentes sobrescrevendo alterações"), a regra não dispara e a resposta cai para `OFF_TOPIC`.

### Classe 3: Vocabulário Fechado em Conceitos Sem Tecnologia (8 falhas)
Respostas conceituais em português técnico legítimo ("balde de fichas", "disjuntor", "chave exclusiva", "dados em cache") foram ejetadas para `OFF_TOPIC` por ausência dos termos anglófonos pré-cadastrados.

### Classe 4: Segmentação Conectiva em Perguntas Multi-Aspecto (5 falhas)
O avaliador de multi-aspecto falhou em identificar a presença de duas demandas quando a conjunção não coincide exatamente com os conectivos cadastrados, gerando `DIRECT` prematuro para respostas de aspecto único.

### Classe 5: Classificações Diagnósticas e Epistêmicas Rígidas (3 falhas)
Respostas mistas (experiência + demonstração) perderam a qualificação de experiência demonstrada e termos técnicos adjacentes foram ejetados como `OFF_TOPIC` em vez de `RELATED`.

---

## Remaining Failures

A lista completa das 38 falhas foi catalogada em `scratch/failures_breakdown.json` e permanecerá como especificação de entrada para a próxima Root Cause Analysis e posterior correção controlada.

---

## Limitations

1. **Catálogo Substituído por Mini-Regras**: A RCA do Stage 31.7.1 exigiu desacoplamento aberto; contudo, a implementação do Stage 31.7.2 concentrou mini-whitelists em blocos condicionais sequenciais.
2. **Dependência de Padrões Frasais Estritos**: O sistema ainda carece de uma verdadeira extração semântica de intenções independente de palavras-chave.

---

## Conclusion

O Stage 31.7.3 cumpriu seu papel com integridade metodológica absoluta:
- **O runtime permaneceu congelado** (hash verificado antes e depois).
- **Nenhuma falha foi maquiada** ou contornada por ajustes ad-hoc.
- O teste cego provou que o sistema melhorou em tecnologias inéditas, mas **ainda possui fragilidades semânticas estruturais** quando confrontado com variações naturais de linguagem, conceitos livres de tecnologia e menções factuais de entidade.

Em observância às diretrizes de `AGENTS.md` (Seção 17: "Um bloqueio é um resultado válido da validação"), o estágio termina formalmente bloqueado.

---

## Next Gate

```text
GATE: POST_DECOUPLING_BLIND_REVALIDATION_BLOCKED
```

O próximo passo canônico é a abertura do **Stage 31.7.4 — Root Cause Analysis & Semantic Intent Generalization** para investigar formalmente as 38 falhas catalogadas, sem modificar o runtime até que a arquitetura corretiva seja desenhada e aprovada.
