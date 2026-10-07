# Stage 31.4 — Semantic Relevance & Representation Invariance Remediation

## Baseline

No encerramento do Stage 31.3, o gate foi registrado como:

```text
POST_CORRECTION_BLIND_VALIDATION_BLOCKED
```

Foram documentadas duas classes principais de falhas semânticas residuais:

1. **Classe A — Pertinência semântica insuficiente**: Respostas tecnicamente corretas para domínios ou tecnologias não perguntadas recebiam qualificação positiva (`conceptual / positive`) e pontuação máxima na dimensão de exatidão (`correctness: Strong`). Casos emblemáticos:
   - `D2`: Pergunta sobre Docker ("Como funciona Docker?"), resposta definindo Kubernetes ("Kubernetes orquestra containers em clusters.").
   - `D3`: Pergunta sobre SQL ("Explique SQL."), resposta definindo Redis ("Redis armazena dados em memória como chave e valor.").
   - `L1`: Pergunta sobre Dependency Injection ("Como funciona Dependency Injection?"), resposta definindo Spring Data ("Spring Data fornece abstrações para acesso a bancos de dados.").

2. **Classe B — Falha de invariância de representação**: Variações expressivas de mesmo conteúdo semântico (formulações formais vs. informais, hesitações ou pequenas variações sintáticas) divergiam na avaliação técnica.

## D2

- **Pergunta**: "Como funciona Docker?"
- **Resposta**: "Kubernetes orquestra containers em clusters."
- **Baseline (Stage 31.3)**:
  - Evidence: `[('conceptual', 'positive')]`
  - Correctness: `Strong` (score 9)
  - Score: `6.0`
- **Pós-Correção (Stage 31.4)**:
  - Evidence: `[('off_topic', 'negative')]`
  - Correctness: `Insufficient` (score 4)
  - Score: `4.0`
- **Diagnóstico**: O candidato explicou orquestração de containers (Kubernetes) sem responder como a tecnologia perguntada (Docker) opera. A divergência foi corrigida no Evidence Model via abstração de domínios semânticos desacoplados.

## D3

- **Pergunta**: "Explique SQL."
- **Resposta**: "Redis armazena dados em memória como chave e valor."
- **Baseline (Stage 31.3)**:
  - Evidence: `[('conceptual', 'positive')]`
  - Correctness: `Strong` (score 9)
  - Score: `6.0`
- **Pós-Correção (Stage 31.4)**:
  - Evidence: `[('off_topic', 'negative')]`
  - Correctness: `Insufficient` (score 4)
  - Score: `4.0`
- **Diagnóstico**: O candidato respondeu sobre armazenamento chave-valor em memória (Redis) diante de pergunta sobre linguagem relacional (SQL). A resposta é tecnicamente válida em si mesma, mas semanticamente inadequada à pergunta.

## L1

- **Pergunta**: "Como funciona Dependency Injection?"
- **Resposta**: "Spring Data fornece abstrações para acesso a bancos de dados."
- **Baseline (Stage 31.3)**:
  - Evidence: `[('conceptual', 'positive')]`
  - Correctness: `Strong` (score 9)
  - Score: `6.0`
- **Pós-Correção (Stage 31.4)**:
  - Evidence: `[('off_topic', 'negative')]`
  - Correctness: `Insufficient` (score 4)
  - Score: `4.0`
- **Diagnóstico**: O candidato explicou acesso a dados (Spring Data) em resposta a padrão de arquitetura/inversão de controle (Dependency Injection). Corrigido como off-topic.

## Invariance Finding

No Stage 31.3, variações equivalentes de respostas curtas e informais recebiam dimensões divergentes:
- Resposta formal: "A aplicação utiliza cache para reduzir a latência das consultas."
- Resposta informal: "A gente usa cache pra deixar as consultas mais rápidas."
- Resposta curta direta: "Cache reduz a latência das consultas."
- Resposta com hesitação: "Bom, a gente usa cache, né, pra consulta ficar mais rápida."

Todas as 4 variantes compartilham o núcleo técnico semântico: uso de caching com a finalidade de otimização de latência/velocidade de consultas. No Stage 31.4, as 4 formulações convergem estritamente para `correctness: Strong`.

## Root Cause

A investigação rastreou a causa-raiz através dos estágios:
- **Stage 20.x (Transcrição)**: Neutro. Não houve corrupção de texto ou speaker attribution.
- **Stage 21 (Evidence Model — `_blind_evidence_specs`)**: **Primeiro estágio incorreto**.
  1. A detecção de evidências qualificava qualquer resposta sem erros explícitos como `conceptual: positive` caso houvesse termos técnicos genéricos, sem validar a pertinência semântica entre o domínio da pergunta e o domínio demonstrado na resposta.
  2. Tentativas anteriores de vincular "âncoras técnicas" por capitalização (`_technical_anchors`) falhavam gravemente em linguagem natural por capturar palavras comuns em início de frase ("Tudo", "Tive", "Ele", "Isso", "Beleza", "Certo") e nomes próprios, introduzindo falsos positivos de off-topic.
- **Stage 22 (Rubric)**: Neutro. A rubrica penaliza adequadamente evidências `negative` e `insufficient`.
- **Stage 23 (Evaluation Engine — `_blind_dimensions`)**: As dimensões traduziam fielmente as evidências recebidas do Stage 21.

## First Incorrect Artifact

- **Artefato**: `Evidence Set` gerado no Stage 21 (`reference_runtime/runtime.py::_blind_evidence_specs`).
- **Problema**: Ausência de validação de pertinência entre a intenção da pergunta e os conceitos definidores da resposta.

## Correction

A correção foi implementada em `reference_runtime/runtime.py` com as seguintes características fundamentais:

1. **Abstração de Domínios Semânticos (`_SEMANTIC_DOMAINS`)**:
   - Mapeamento declarativo de conceitos característicos por domínio tecnológico (backend, frontend, bancos relacionais, caching, mensageria, segurança/autenticação, containers, orquestração, CI/CD, arquitetura hexagonal, event-driven, SOLID, etc.).
   - Distinção entre conceitos válidos auxiliares e conceitos definidores de um domínio alienígena.

2. **Classificação de Intenção da Pergunta (`question_intent`)**:
   - `experience`: Perguntas sobre trajetória, projetos e tecnologias utilizadas no histórico do candidato ("projetos", "atuou", "trajetória", "tecnologias que você usou", "já precisou usar") aceitam descrição legítima do ecossistema do candidato sem falso off-topic.
   - `investigation`: Perguntas sobre resolução de incidentes ("como investigaria", "erro 500", "latência") aceitam legitimamente ações diagnósticas (logs, traces, métricas, dependências, baseline, p95).
   - `resilience`: Perguntas sobre resiliência aceitam padrões de estabilidade (timeout, retry, backoff, circuit breaker, observabilidade).
   - `tradeoff`: Perguntas de comparação ("como escolheria", "como decidiria") aceitam avaliação de prós/contras, latência e consistência.

3. **Critério Semântico Generalizado de Desconexão (`_is_semantic_off_topic`)**:
   - Se a pergunta tem como alvo o domínio $D_Q$, e a resposta não apresenta conceitos válidos de $D_Q$, mas expressa conceitos definidores de um domínio diferente $D_R$, a resposta é classificada como `off_topic` com qualificação `negative`.
   - Se a resposta combina o domínio perguntado com um domínio não correlato (resposta mista), emite `conceptual: partial`.

4. **Invariância de Representação**:
   - A exatidão técnica não penaliza formulações informais ("a gente usa", "pra deixar mais rápido"), hesitações ("bom", "né") nem brevidade concisa quando o conceito central responde diretamente à pergunta.
   - Respostas autocorrrectoras ("X é síncrono... quer dizer, assíncrono") preservam a qualificação técnica pretendida.
   - Comprimento e jargões empilhados sem substância não promovem a pontuação técnica.

## Generalization Strategy

A solução não utiliza tabelas de pares de tecnologia (`REST -> Kafka`, `Docker -> Kubernetes`, `SQL -> Redis`). Em vez disso, opera em nível de relação semântica entre a intenção da pergunta e a substância técnica apresentada.

Domínios validados na suíte:
- Autenticação / OAuth vs. Caching
- Índices SQL vs. Mensageria (Kafka)
- Redes Docker vs. CI/CD (Jenkins)
- Reatividade Frontend (Angular Signals) vs. Estilização (CSS)
- Proteção de API vs. Cache em memória (Redis)
- Arquitetura Hexagonal vs. Assinatura de Tokens (JWT)
- Arquitetura Event-Driven vs. Autenticação (JWT)
- Testes de Integração de Endpoint vs. Orquestração (Kubernetes)
- Seleção de Banco Relacional vs. Cache Chave-Valor (Redis)

## Positive Cases

Casos em que conceitos auxiliares não literais aparecem legitimamente e são reconhecidos como pertinentes:
- `R1`: Pergunta sobre erro 500 → Resposta citando logs, traces, dependências e métricas (Pertinente).
- `R2`: Pergunta sobre API resiliente → Resposta citando timeout, retry com backoff, circuit breaker (Pertinente).
- `R3`: Pergunta sobre transação no Spring → Resposta citando `@Transactional` (Pertinente).
- `R4`: Pergunta sobre observabilidade → Resposta citando correlação com métricas, logs e traces (Pertinente).
- `R5`: Pergunta sobre redes Docker → Resposta citando rede bridge e DNS interno (Pertinente).
- `CAL28-01`: Investigação de latência p95/p99 com análise de dependências (Pertinente).
- `CAL28-08`: Trade-off entre cache local e distribuído (Pertinente, `reasoning: Strong`).

## Negative Cases

Casos tecnicamente válidos, porém sem relação suficiente com a pergunta, que são corretamente classificados como `off_topic`:
- `D2`: Docker → Kubernetes
- `D3`: SQL → Redis
- `L1`: Dependency Injection → Spring Data
- `N1`: OAuth → Caching
- `N2`: Índices SQL → Tópicos e consumidores Kafka
- `N3`: Docker networking → Jenkins pipelines
- `N4`: Angular Signals → CSS styling
- `N5`: Proteção de API → Redis
- `N6`: Arquitetura Hexagonal → JWT
- `N7`: Event-driven → JWT
- `N8`: Teste de endpoint → Kubernetes
- `N9`: Banco relacional → Redis
- `N10`: Docker networking → Jenkins pipelines

## Pertinence Tests

- Pares mínimos avaliados: Resposta Pertinente vs. Resposta Desconectada.
- Em 100% dos pares (ex: Troubleshooting 500, SOLID, Hexagonal, Event-Driven), a resposta pertinente obteve score superior à desconectada.
- Resposta parcialmente pertinente (investigação 500 misturada com explicação de Kafka) preserva evidência conceitual com teto restrito (`correctness != Strong`).

## Invariance Tests

1. **Formal vs. Informal**: `EQ0` (formal), `EQ1` (informal), `EQ2` (curto direto) e `EQ3` (coloquial com hesitação) receberam unanimemente `correctness: Strong`.
2. **Autocorreção**: Resposta com hesitação e autocorreção imediata ("síncrono... quer dizer, assíncrono") recebeu qualificação técnica equivalente à resposta direta sem erro.
3. **Extensão e Jargão**: Resposta prolixa infundida de buzzwords ("REST, HTTP, microservices, CQRS, DDD, SOLID...") obteve score estritamente menor ou igual à resposta curta precisa.
4. **Senioridade e Metadados**: A variação dos metadados de senioridade (Junior, Pleno, Senior, Staff) e presença/ausência de CV na requisição produziu projeções de evidência e score idênticas.

## Experience Tests

A progressão metodológica de experiência foi integralmente preservada:
- `EXP-A` (Declaração pura: "Já trabalhei com Kubernetes."): `experience_declaration: insufficient`, score 4.0.
- `EXP-B` (Demonstração prática: "Configurei deployments e probes."): `demonstrated_experience: positive`, score 7.05.
- `EXP-C` (Demonstração com troubleshooting: "Investiguei restart loop, eventos e probes."): score 7.65.
- Relação estrita: `Score(Declaração) < Score(Demonstração) <= Score(Troubleshooting)`.

## Troubleshooting Tests

- `PAIR-G0`: Pergunta de erro 500 com investigação diagnóstica (logs, traces, dependências) obteve score `6.0`.
- `PAIR-B0`: Pergunta de erro 500 com sugestão desconectada de containers ("Eu usaria Kubernetes porque ele gerencia containers.") obteve score `4.0` (`off_topic`).

## Architecture Tests

- SOLID: Responsabilidades e abstrações (`6.0`) vs. Caching em memória (`4.0`).
- Hexagonal: Portas e adapters invertendo dependências (`6.0`) vs. CSS (`4.0`).
- Event-Driven: Eventos, consumidores desacoplados e idempotência (`6.0`) vs. JWT (`4.0`).

## Mutation Tests

- **Mutação A** (Pertinente → Off-topic): Score sofreu degradação imediata de 6.0 para 4.0.
- **Mutação B** (Off-topic → Pertinente): Score subiu de 4.0 para 6.0.
- **Mutação C** (Linguagem formal → informal): Score e dimensões permaneceram rigorosamente idênticos.
- **Mutação D** (Adição de jargão vazio): Não elevou o score técnico.
- **Mutação E** (Adição de evidência técnica demonstrada): Promoveu adequadamente as dimensões correspondentes.

## Blind Revalidation

- Execução cega sem conhecimento de oráculos externos no runtime.
- Todos os testes de blind calibration (Stage 28 e Stage 31.3) foram reexecutados de forma independente.
- Divergências residuais do Stage 31.3 (`D2`, `D3`, `L1`) foram sanadas sem overfitting.

## Stage 31.3 After Correction

- Os 12 testes de `tests/test_stage_31_3_post_correction_blind_validation.py` foram executados e passaram com 100% de sucesso.
- O gate histórico do Stage 31.3 permanece documentado como `POST_CORRECTION_BLIND_VALIDATION_BLOCKED` para fins de governança e auditoria histórica.

## Regression

- `tests/test_stage_31_4_semantic_relevance_invariance_remediation.py`: 11/11 PASS.
- `tests/test_stage_31_3_post_correction_blind_validation.py`: 12/12 PASS.
- `tests/test_stage_31_2_controlled_correction.py`: 9/9 PASS.
- `tests/test_stage_30_1_pilot_failure_analysis.py`: 6/6 PASS.
- `tests/test_stage_30_2_1_final_semantic_audit.py`: 12/12 PASS.
- `tests/test_stage_28_semantic_blind_calibration.py`: 15/15 PASS.
- Suíte completa (`py run_reference_runtime_tests.py`): **526/526 PASS (0 falhas)**.
- Reference Harness (`py run_reference_harness.py`): **8/8 suites PASS_WITH_WARNINGS (0 falhas)**.

## Determinism

- Execução múltipla consecutiva da pipeline completa e do Reference Harness:
  - `Run 1 == Run 2` em todos os artefatos estruturados (`questions`, `responses`, `evidence`, `evaluations`).
  - Totalmente determinístico.

## Limitations

1. **Vocabulário de Domínios**: A abstração semântica baseia-se em conceitos representativos declarados por domínio. Novos domínios tecnológicos especializados requerem inclusão de seus termos no modelo conceitual do sistema.
2. **Respostas Extremamente Concisas**: Respostas com até 2 palavras são tratadas conservadoramente como evidência insuficiente (`fragmented / insufficient`), priorizando segurança semântica sobre inferência não comprovada.
3. **Isolamento de Avaliação**: O sistema avalia exclusivamente o conteúdo verbal contido no transcript, mantendo invariância a metadados externos de senioridade e CV.

## Gate

```text
SEMANTIC_RELEVANCE_INVARIANCE_REMEDIATION_COMPLETE
```

---

## Métricas

```yaml
validation:
  total_cases: 526
  passed: 526
  warnings: 2
  failed: 0
  blocked: 0

relevance:
  false_positive_cases: 0
  false_negative_cases: 0
  legitimate_related_cases: 7
  off_topic_cases: 13

invariance:
  equivalent_pairs: 8
  equivalent_results: 8
  divergent_results: 0

experience:
  declarations: 5
  demonstrated: 4
  hypothetical: 2

regression:
  stage_31_3: PASS (12/12)
  stage_31_2: PASS (9/9)
  full_suite: PASS (526/526)
  harness: PASS_WITH_WARNINGS (8/8)
```
