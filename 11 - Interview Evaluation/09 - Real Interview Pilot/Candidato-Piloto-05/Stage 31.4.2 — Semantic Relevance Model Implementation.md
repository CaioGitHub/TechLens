# Stage 31.4.2 — Semantic Relevance Model Implementation & Migration

## Resumo Executivo e Contexto

No encerramento do **Stage 31.4.1**, formalizou-se o redesign conceitual e os contratos abstratos do **Modelo de Pertinência Semântica**, superando a dependência de dicionário léxico fechado, regras de pares tecnológicos hardcoded e heurísticas de contagem de palavras como proxy de qualidade.

O objetivo do presente **Stage 31.4.2** foi transformar o contrato conceitual do Stage 31.4.1 em **implementação executável** diretamente no Reference Evaluation Engine (`reference_runtime/runtime.py`).

A implementação:
1. **Eliminou integralmente todas as regras de technology-pair matching**, blacklists/allowlists de pares tecnológicos e verificações literais ad-hoc identificadas na auditoria (ex.: `virtual thread ↔ kql`, `spring ↔ virtual thread`).
2. **Eliminou o proxy de contagem de palavras** (`len < 15`) para completude, profundidade, exatidão técnica e scoring.
3. **Implementou a taxonomia canônica completa em 7 classes**: `DIRECT`, `PARTIAL`, `SUPPORTING`, `RELATED`, `OFF_TOPIC`, `INSUFFICIENT`, `UNKNOWN`.
4. **Implementou suporte generalizável para tecnologias desconhecidas** (ausentes de qualquer vocabulário interno, tais como Raft, Envoy, Cilium, eBPF, gRPC, WebAssembly, GraphQL, BGP, Terraform, Postgres).
5. **Implementou suporte para conceitos técnicos expressos sem nomes de tecnologias** (ex.: desacoplamento de instanciação sem citar DI/Spring; filas assíncronas para buffering sem citar Rabbit/Kafka; retenção em memória com expiração sem citar Redis/Cache).
6. **Diferenciou funcionalmente `SUPPORTING` de `RELATED`**, garantindo que ações investigativas/arquiteturais contribuam com crédito funcional em troubleshooting/resiliência, enquanto citações adjacentes sem mecanismo técnico permaneçam neutras (`functional_contribution: False`, `evidence_strength: NONE`).
7. **Preservou a separação conceitual entre 4 dimensões desacopladas**:
   $$\text{Semantic Relevance} \longrightarrow \text{Evidence Strength} \longrightarrow \text{Evaluation Dimensions} \longrightarrow \text{Rubric Score}$$
8. **Validou 69 novos testes adversariais independentes** em `tests/test_stage_31_4_2_semantic_relevance_implementation.py`, além de **607/607 testes do repositório integralmente aprovados** e **8/8 suítes do Reference Harness aprovadas com determinismo e isolamento estritos**.

---

## 1. Eliminação de Regras Hardcoded e Heurísticas de Contagem

### 1.1 Regras de Pares Tecnológicos Removidas
Durante a implementação, foram expurgadas as seguintes regras de tecnologia-par e vocabulários restritos:
- **`virtual thread ↔ kql`**: removida qualquer regra ou verificação explícita que associasse a pergunta de concorrência com o nome da tecnologia KQL para decidir off-topic.
- **`spring ↔ virtual thread`**: removida a verificação ad-hoc de compatibilidade tecnológica entre frameworks e threads virtuais.
- **`technology-pair allowlist/blacklist`**: qualquer dependência de pares fixos foi substituída por análise de intenção funcional versus proposição demonstrada.
- **`dicionário fechado de tecnologias alienígenas`**: removidas tecnologias como `cilium`, `ebpf`, `postgres`, `infrastructure_provisioning` que haviam sido adicionadas como vocabulário rígido. Tecnologias não catalogadas agora são processadas pelo motor semântico de domínio aberto.

### 1.2 Eliminação de Word Count Proxy
Na função `_blind_dimensions`:
- **Removido**: `short = len(semantic_text.split()) < 15`
- **Impacto corrigido**: O sistema não mais rebaixa mecanicamente uma resposta para `completeness: Partial` ou `depth: Weak` meramente por ter menos de 15 palavras. Respostas concisas e diretas (ex.: *"É um erro interno do servidor."* ou *"Usaria cache."*) recebem qualificação proporcional às proposições técnicas demonstradas, não à sua extensão estenográfica.
- **Anti-padding**: Respostas longas recheadas de jargões e buzzwords desconexos não ganham crédito por volume, mantendo-se qualificadas como `Insufficient` / `OFF_TOPIC`.

---

## 2. Arquitetura Executável do Modelo de Pertinência Semântica

### 2.1 Taxonomia Canônica de 7 Classes
A implementação em `_evaluate_semantic_relevance(question, response)` materializa a taxonomia contratual:

| Classificação | Definição Semântica | Contribuição Funcional | Força da Evidência |
|---|---|---|---|
| **`DIRECT`** | Proposição técnica responde diretamente à demanda central da pergunta | `True` | `STRONG` |
| **`PARTIAL`** | Responde a parte da demanda multi-aspecto, ou mistura mecanismo válido com domínio alienígena | `True` | `MODERATE` |
| **`SUPPORTING`** | Demonstra ação ou padrão que serve funcionalmente ao objetivo (troubleshooting, resiliência, trade-offs) | `True` | `STRONG` |
| **`RELATED`** | Menção a ecossistema, ferramenta ou tópico adjacente sem demonstração do mecanismo solicitado | `False` | `NONE` |
| **`OFF_TOPIC`** | Mecanismo pertencente a domínio completamente alheio ou proposição sem relação técnica | `False` | `NONE` |
| **`INSUFFICIENT`** | Fragmentação extrema ou admissão explícita de desconhecimento (*"bem por cima"*, *"quase nada"*) | `False` | `NONE` |
| **`UNKNOWN`** | Segmento truncado, ilegível, não vinculado ou ambiguidade estrutural da transcrição | `False` | `NONE` (`needs_review: True`) |

### 2.2 Detecção de Intenção Funcional Desacoplada
A intenção é extraída da estrutura da pergunta em quatro categorias canônicas:
1. **`diagnostic_troubleshooting`**: perguntas de diagnóstico de falhas, erros HTTP 500, incidentes e observabilidade. Ações diagnósticas (logs, traces, métricas, profiling, heap dumps) são reconhecidas como `SUPPORTING`. Domínios alinhados ao cenário (ex.: WAF em API de autenticação) não são tratados como alienígenas.
2. **`architectural_decision`**: perguntas de resiliência, escalabilidade e arquitetura. Padrões de resiliência (timeout, retry, circuit breaker) e análise de trade-offs são reconhecidos como `SUPPORTING`.
3. **`experience_verification`**: perguntas sobre trajetória, vivência prática e uso de stacks. Classificadas como `DIRECT` em relação à demanda de histórico, permitindo que a hierarquia de evidências avalie se houve declaração, hipótese ou demonstração.
4. **`factual_mechanism`**: perguntas de definição e funcionamento operacional de conceitos e ferramentas.

### 2.3 Generalização para Tecnologias Desconhecidas e Conceitos sem Nomes
- **Domínio Aberto (`open_demonstrated_domain`)**: Quando a pergunta versa sobre uma tecnologia ou conceito ausente de capacidades internas (ex.: Raft, Envoy, Cilium, eBPF, gRPC, WebAssembly, GraphQL, BGP), o runtime extrai as proposições substantivas semânticas (filtrando stop words da língua portuguesa) e mapeia a coerência proposicional entre a demanda e a resposta.
- **Conceitos sem Nomes de Ferramentas**: Respostas que explicam o mecanismo funcional sem usar marcas comerciais (ex.: inversão de controle sem citar Spring/DI; fila assíncrona desacoplando produtor e consumidor sem citar Kafka; dados mantidos em memória com expiração sem citar Redis) são mapeadas diretamente para a capacidade funcional correspondente como `DIRECT`.

### 2.4 Diferenciação Rigorosa entre `SUPPORTING` e `RELATED`
- **`SUPPORTING`**: Exige **contribuição funcional para a resolução do cenário** (ex.: analisar logs, traces e métricas para investigar um HTTP 500). Contribui positivamente para a avaliação (`functional_contribution: True`).
- **`RELATED`**: Identifica **adjacência temática ou tecnológica sem contribuição funcional** (ex.: falar de Spring Data quando perguntado sobre Dependency Injection; falar de tags HTML quando perguntado sobre CSS flexbox; falar de Git branches quando perguntado sobre CI/CD deploy; falar de Schema Registry quando perguntado sobre particionamento Kafka). Não pontua como demonstração do mecanismo solicitado (`functional_contribution: False`, `evidence_strength: NONE`).

---

## 3. Demonstração de Invariância de Representação e Propriedades

### 3.1 Invariância de Comprimento
- **Resposta Curta vs. Longa com Mesmo Significado**: A resposta concisa (*"Usaria cache para reduzir a latência de consultas repetidas ao banco."*) e a resposta extensa obtêm ambas qualificação `Strong` em `correctness` e score equivalente ($\Delta < 0.5$).
- **Anti-Padding**: Respostas prolixas recheadas de buzzwords sem mecanismo aplicável são rebaixadas para `OFF_TOPIC` com score $\le 5.0$ e exatidão `Insufficient`.

### 3.2 Invariância de Estilo e Fluência
Testada a equivalência técnica através de formulações:
- Formal;
- Informal / coloquial (*"A gente usa cache pra deixar as consultas mais rápidas"*);
- Hesitante com autocorreção (*"Acho que... é, na verdade usaria cache em memória"*);
- Jargão técnico (*"Implementaria caching layer com TTL"*).
Todas as variações preservaram exatamente a mesma classificação (`DIRECT`), a mesma exatidão (`Strong`) e scores equivalentes.

### 3.3 Hierarquia Epistêmica de Experiência
Validada a relação estrita entre as três modalidades de experiência:
$$\text{Declaração (score: 4.20)} < \text{Hipótese (score: 7.65)} < \text{Demonstração Prática (score: 8.70)}$$
- Uma mera declaração (*"Trabalhei 3 anos com Kubernetes"*) não ganha pontuação prática.
- Uma hipótese (*"Eu criaria um deployment se precisasse..."*) recebe qualificação condicional.
- Uma demonstração com ações, configuração de probes, investigação de crash loops e mitigação de gargalos em produção atinge pontuação sênior fundamentada.

### 3.4 Discriminação Semântica e Sensibilidade a Mutações
- **Similaridade Superficial vs. Conteúdo Oposto**: Duas respostas com vocabulário quase idêntico sobre RabbitMQ, uma afirmando que opera assincronamente com filas (`eval_c: 7.05`) e outra afirmando falsamente que opera sincronicamente bloqueando threads de chamada (`eval_i: 4.65`), são discriminadas com precisão ($\text{Score}_C > \text{Score}_I$).
- **Mutação Técnica**: Alterar o conteúdo técnico de uma resposta sobre índices relacionais para dados em memória chave-valor altera imediatamente a classificação de `DIRECT` para `OFF_TOPIC`.

---

## 4. Auditoria da Suíte de Testes Adversariais Independentes

Foi criada a nova suíte de testes de implementação em:
```text
tests/test_stage_31_4_2_semantic_relevance_implementation.py
```
Total de testes executados: **69 casos**, distribuídos nas 7 classes canônicas e dimensões de propriedades:

1. **DIRECT (10 casos)**: Casos cobrindo tecnologias desconhecidas (Raft, Envoy, Cilium), conceitos sem nomes (desacoplamento de instanciação, fila assíncrona, cache em memória), e múltiplos domínios técnicos (REST, B-Tree, CI/CD, Virtual Threads).
2. **PARTIAL (10 casos)**: Casos de multi-aspecto com cobertura parcial, omissão de trade-offs, misturas controladas com ferramentas alienígenas e tecnologias desconhecidas (gRPC/protobuf, WebAssembly/memória, GraphQL/overfetching).
3. **SUPPORTING (10 casos)**: Casos de diagnóstico com logs, traces, métricas, heap dump de GC roots, tcpdump, flamegraph de CPU, trade-offs de resiliência e investigações de sobrecarga de API.
4. **RELATED (10 casos)**: Casos de adjacência temática sem mecanismo cobrindo Dependency Injection ↔ Spring Data, CSS ↔ HTML, CI/CD ↔ Git branches, B-Tree ↔ Replicação, Virtual Threads ↔ Maven, Kafka ↔ Schema Registry, JWT ↔ CORS, REST ↔ Swagger/OpenAPI, Angular ↔ npm, KQL ↔ Azure RBAC.
5. **OFF_TOPIC (10 casos)**: Casos adversariais de desconexão funcional incluindo Docker ↔ Kubernetes (D2), SQL ↔ Redis (D3), Virtual Threads ↔ Docker, REST ↔ Kafka, Hexagonal ↔ SQL, receitas culinárias, BGP ↔ GraphQL e Envoy ↔ RabbitMQ.
6. **INSUFFICIENT (5 casos)**: Admissões de desconhecimento (*"bem por cima"*, *"não sei"*, *"muito pouco, quase nada"*, monossílabos soltos).
7. **UNKNOWN (5 casos)**: Transcrição vazia, segmento nulo, linking indefinido e marcadores de falha estrutural com `needs_review: True`.
8. **Testes de Invariância e Propriedades (9 casos)**: Invariância de comprimento, anti-padding, invariância de estilo (4 variações), discriminação semântica superficial, hierarquia de experiência, sensibilidade a mutação, determinismo de tripla execução e isolamento de permutações aleatórias.

Resultado: **69/69 PASS (100%)**.

---

## 5. Integridade Regressiva e Resultados do Piloto Real

### 5.1 Execução da Suíte Regressiva Global
Executou-se `py run_reference_runtime_tests.py`:
```text
Ran 607 tests in 17.682s
OK
test_run:
  runtime: reference_runtime
  total: 607
  passed: 607
  failed: 0
  blocked: 0
  not_executed: 0
  status: PASS
```

### 5.2 Execução do Reference Harness (8 Suítes)
Executou-se `py run_reference_harness.py`:
```text
test_reference_harness:
  runtime: reference_runtime
  total_suites: 8
  passed_suites: 8
  failed_suites: 0
  status: PASS_WITH_WARNINGS
  warnings:
    - active_stage_blocked: Stage 31 is BLOCKED (requires Stage 31.1, 31.2, 31.3, 31.4 before progressing)
  suites:
    - synthetic_interview: PASS (39/39)
    - calibration_cases: PASS (10/10)
    - adversarial_cases: PASS (15/15)
    - pilot_cases: PASS (11/11)
    - post_correction_blind_validation: PASS_WITH_WARNINGS (21/21)
    - semantic_relevance_invariance_remediation: PASS (17/17)
    - semantic_relevance_model_redesign: PASS (24/24)
    - semantic_relevance_implementation: PASS (69/69)
```

### 5.3 Estabilidade e Rastreabilidade do Piloto Real (Candidato-Piloto-05)
A reexecução do piloto real através do pipeline canônico (`run_real_pilot`) demonstrou total integridade:
- **Scores por questão (Q1–Q11)**: `[4.0, 7.05, 4.0, 7.05, 4.45, 5.85, 6.0, 7.05, 4.0, 7.65, 4.0]`
- **Média das notas**: `5.55` (preservação exata do baseline regressivo histórico)
- **Mediana das notas**: `5.85`
- **Total de evidências extraídas**: `24` itens

Casos históricos resolvidos organicamente pelo modelo geral (sem regras específicas):
- **D2 (Docker → Kubernetes)**: Classificado como `OFF_TOPIC` por desacoplamento funcional de capacidades operacionais.
- **D3 (SQL → Redis)**: Classificado como `OFF_TOPIC` por disjunção entre consultas relacionais e chave-valor em memória.
- **L1 (Dependency Injection → Spring Data)**: Classificado como `RELATED` por adjacência tecnológica no ecossistema Spring sem demonstração de mecanismo de injeção.

---

## 6. Preservação dos Gates Históricos e Não Execução do Stage 31.5

Em cumprimento estrito das Regras 1, 15, 17 e 39 de `AGENTS.md`:
- O relatório histórico do **Stage 31** permanece inalterado com gate `HUMAN_VS_SYSTEM_BLOCKED`.
- O relatório histórico do **Stage 31.3** permanece inalterado com gate `POST_CORRECTION_BLIND_VALIDATION_BLOCKED`.
- O relatório histórico do **Stage 31.4** permanece inalterado com gate `SEMANTIC_RELEVANCE_INVARIANCE_REMEDIATION_COMPLETE_WITH_WARNINGS`.
- O relatório do **Stage 31.4.1** permanece inalterado com gate `SEMANTIC_RELEVANCE_MODEL_REDESIGN_COMPLETE`.
- **Nenhum teste do Stage 31.5 (Human vs System Revalidation) foi executado** durante este estágio.

---

## 7. Gate e Conclusão

Todos os critérios de sucesso do Stage 31.4.2 foram integralmente atendidos:
- Contrato 31.4.1 implementado no Reference Evaluation Engine;
- Technology-pair matching e blacklists eliminados;
- Proxy de contagem de palavras eliminado;
- Pertinência semântica separada de força da evidência e de score;
- Tecnologias desconhecidas e conceitos sem nomes tecnológicos operacionalizados;
- Supporting e Related diferenciados sem ambiguidade;
- Invariância de representação e discriminação semântica comprovadas;
- 69 testes adversariais independentes aprovados;
- 607 testes de regressão global aprovados com determinismo estrito;
- 8/8 suítes do Reference Harness aprovadas.

**Gate do Stage 31.4.2:**
```text
SEMANTIC_RELEVANCE_MODEL_IMPLEMENTATION_COMPLETE
```
