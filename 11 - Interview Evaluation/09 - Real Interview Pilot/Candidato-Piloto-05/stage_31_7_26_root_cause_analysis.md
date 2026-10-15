# Stage 31.7.26 — Análise de Causa-Raiz (RCA): Falsos DIRECTs e Disjunção de Domínio Semântico (Ciclo 5)

## 1. Contexto e Escopo

No Stage 31.7.25, a revalidação cega e independente do runtime remediado no Ciclo 4 (`reference_runtime/runtime.py`, SHA-256: `36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7`) resultou em `BLIND_SEMANTIC_REVALIDATION_BLOCKED`.
Apesar do alto recall de `DIRECT` (90,91%), a precisão despencou para **41,67%** (limiar mínimo $\ge 70\%$) devido a **70 falsos DIRECTs** dentre 120 predições positivas, representando **71,43%** de todas as 98 divergências observadas.

Este documento formaliza a investigação causal profunda, responde às dez questões fundamentais do RCA, audita os grupos diagnósticos de falhas e avalia rigorosamente oito hipóteses concorrentes por meio de testes de refutação baseados na mecânica interna do código e nas evidências empíricas dos 250 casos do benchmark.

---

## 2. Respostas às Dez Questões Fundamentais do RCA

### 2.1. Por que respostas de domínios semanticamente disjuntos estão sendo classificadas como DIRECT?
**Evidência direta no código:**
Em `PropositionDiscourseFilter.filter_propositions`, a identificação de domínios alienígenas (`is_alien`) baseia-se estritamente em uma tupla estática de 25 termos lexicais (`alien_terms` em `OpenDomainPropositionEngine.__init__`: `"cozinhar"`, `"lasanha"`, etc.). Respostas sobre botânica (`"orquídeas"`, `"jardinagem"`), manutenção automotiva (`"óleo do motor"`), ou culinária não catalogada passam pelo filtro com `is_alien_domain = False`.
Em seguida, o filtro avalia se a frase é "operativa": se contiver verbos de ação gramaticalmente ativos (ex.: `"exigem"`, `"deve ser realizada"`, `"bater"`, `"misturar"`) e tamanho $\ge 6$ palavras, marca `is_operative = True`.
Ao chegar no `DemandPropositionNexusBipartiteMatcher.assess_demand_nexus`:
1. Nenhum ramo específico de domínio (2PC, Sagas, Kafka) casa com o texto da botânica/mecânica.
2. Na linha 3434, o matcher executa seu fallback padrão de domínio aberto:
   ```python
   return DemandPropositionNexus(
       demand_id=demand.demand_id,
       nexus_relation="FUNCTIONALLY_SOLVES",
       rationale="Response proposition provides operative mechanism satisfying demand."
   )
   ```
3. O `StrictOntologyRelevanceAggregator.aggregate_relevance` recebe `FUNCTIONALLY_SOLVES` para a demanda e, na linha 3548, emite a classificação final `DIRECT`.

**Conclusão:** Respostas de domínios disjuntos tornam-se `DIRECT` porque o sistema confunde a *presença de uma oração operativa bem formada* (estrutura sintática ativa) com a *pertinência semântica e funcional da ação em relação ao domínio da pergunta*.

---

### 2.2. Por que respostas tematicamente relacionadas, mas insuficientes para satisfazer a pergunta, estão sendo classificadas como DIRECT?
**Evidência direta no código:**
Respostas que abordam metadados institucionais (ex.: `"Kafka é mantido pela Apache Software Foundation"`, `"Docker foi criado pela DotCloud em 2013"`, ou discussões de adoção de mercado) possuem termos da mesma área tecnológica ampla da pergunta (ex.: "Kafka", "Docker").
No Ciclo 4, foi introduzido o filtro `_is_institutional_metadata(p)`. No entanto, esse filtro utiliza padrões de regex limitados. Quando a formulação do candidato utiliza uma estrutura transitiva comum (ex.: `"O Kafka pertence à fundação Apache e foi doado pelo LinkedIn"`), a sentença não casa com os regexes estritos de trivias e é classificada como proposição operativa (`is_operative = True`).
Como a entidade da pergunta está presente, o bipartite matcher não encontra impedimento e cai no fallback permissivo, concedendo `FUNCTIONALLY_SOLVES`.
O sistema falhou em reconhecer que *mencionar a entidade ou seu ecossistema não equivale a descrever o mecanismo técnico exigido pela demanda* (ex.: particionamento, idempotência, isolamento).

---

### 2.3. Em quais caminhos internos o DemandPropositionNexusBipartiteMatcher pode aceitar uma relação funcional sem evidência semântica suficiente?
A auditoria minuciosa da classe `DemandPropositionNexusBipartiteMatcher` (linhas 3150 a 3440 de `runtime.py`) revelou três caminhos críticos de concessão não fundamentada:
1. **Fallback incondicional de domínio aberto (Linha 3434):**
   Se uma proposição é marcada como `is_operative = True` e não foi interceptada pelos filtros heurísticos de antitítese, evasão ou catálogo estático de alienígenas, o matcher concede `nexus_relation="FUNCTIONALLY_SOLVES"`. Não há verificação se o sujeito/verbo/objeto da proposição guardam qualquer compatibilidade semântica com os `aspect_goals` da demanda.
2. **Atribuição cega por menção de entidade sem mecanismo (Linha 3380-3400):**
   Se o sujeito da proposição contém o nome da entidade primária da pergunta (ex.: `"Kafka"`, `"2PC"`), o matcher infere que a proposição está "tratando da tecnologia", dispensando a comprovação de que a ação predicada realiza a resolução do problema.
3. **Ignorância da disjunção semântica entre predicado e demanda:**
   O matcher não possui representação formal de *incompatibilidade semântica de domínio*. Ele opera sob a premissa de presunção de pertinência: "se não é expressamente antitético e é operativo, assume-se que resolve".

---

### 2.4. O fallback de domínio aberto é realmente a causa comum dos falsos DIRECT, ou existem múltiplas causas independentes?
**Constatação:** Existem **quatro mecanismos causais independentes**, embora todos convirjam para o mesmo afunilamento de vulnerabilidade (o fallback permissivo da linha 3434):
- **Causa 1 (Disjunção Semântica Não Detectada - 34 casos OFF_TOPIC):** Falta total de um componente de verificação de disjunção de domínio semântico (catálogo fechado de 25 palavras alienígenas).
- **Causa 2 (Vazamento de Metadados Institucionais / Categoriais - 22 casos RELATED):** Regexes de metadados institucionais frágeis; predicados relacionais gerais confundidos com operatividade técnica.
- **Causa 3 (Desalinhamento de Ações Auxiliares / Observabilidade - 7 casos SUPPORTING):** Verbos de monitoramento/telemetria tratados como mecanismos diretos em vez de evidências de suporte, por falta de amarração de dependência funcional.
- **Causa 4 (Evasão Sintaticamente Complexa - 7 casos INSUFFICIENT):** Frases evasivas com estruturas gramaticais ativas (ex.: `"isso vai depender de múltiplos fatores de negócio"`) que escaparam da lista de marcadores de ignorância/evasão e foram tratadas como proposições operativas.

Portanto, a falha não é um único bug isolado, mas uma deficiência arquitetural sistêmica: **a presunção de suficiência sem comprovação de ancoragem semântica.**

---

### 2.5. O que diferencia semanticamente RELATED, SUPPORTING, OFF_TOPIC, INSUFFICIENT e UNKNOWN?
A taxonomia semântica formal do sistema estabelece:
- **`DIRECT`:** Atendimento funcional cabal de todas as demandas primárias obrigatórias da pergunta, com demonstração do mecanismo/conceito específico solicitado.
- **`PARTIAL`:** Atendimento funcional correto e pertinente de um subconjunto estrito das demandas primárias obrigatórias em perguntas compostas, ou cobertura conceitual incompleta mas tecnicamente sólida.
- **`SUPPORTING`:** A resposta fornece informações tecnicamente verdadeiras e auxiliares (ex.: ferramentas de observabilidade, métricas secundárias, telemetria, boas práticas de infraestrutura) que complementam a resolução, mas *não descrevem o mecanismo primário exigido*.
- **`RELATED`:** A resposta aborda o tema, ecossistema ou tecnologia mencionada na pergunta (ex.: histórico, criadores, licença, adoção, características institucionais gerais), mas *não fornece contribuição funcional operacional para a demanda técnica específica*.
- **`OFF_TOPIC`:** A resposta pertence a um domínio ontológico ou funcional inteiramente disjunto do problema técnico demandado (ex.: botânica, culinária, jardinagem, pintura, mecânica pesada em pergunta de software).
- **`INSUFFICIENT`:** O candidato tenta responder ao problema proposto, mas o conteúdo é vago, evasivo, superficial, inconclusivo ou redundante, não constituindo evidência de domínio técnico.
- **`UNKNOWN`:** O conteúdo transcrito é ininteligível, fragmentário, puramente fático sobre o processo de entrevista, ou expressa incapacidade explícita de responder ("não sei", "nunca vi esse termo").

---

### 2.6. Como preservar respostas válidas de domínios incomuns, formulações coloquiais, tecnologias desconhecidas e explicações sem sobreposição lexical?
A solução **não pode** consistir na adição de catálogos de palavras proibidas ou listas fechadas de tecnologias válidas.
Para preservar a generalização:
1. **Análise de Invariância Lexical e Funcional:** A pertinência semântica deve ser avaliada pela compatibilidade de *papéis temáticos e fluxos operacionais* (ex.: agente que particiona, meio de transmissão, garantia de integridade, barreira de sincronização), e não pela presença de nomes específicos como "Kafka" ou "Postgres".
2. **Independência de Entidades:** Tecnologias desconhecidas (ex.: "Z-Database", "FluxProtocol") devem ser aceitas se o predicado descrever adequadamente a ação funcional demandada (ex.: coordenar commit de duas fases, balancear carga em anel hash).
3. **Ancoragem Semântica por Contexto de Problema:** Uma resposta é compatível se a cadeia causal que ela descreve atua sobre as grandezas do domínio do problema (ex.: concorrência, latência, durabilidade, isolamento, consistência), diferenciando-a de processos biológicos, botânicos ou culinários.

---

### 2.7. Como impedir que verbos operacionais, extensão da resposta, vocabulário técnico ou presença de mecanismos sejam tratados como prova suficiente de atendimento?
A arquitetura do Ciclo 5 deve aplicar uma regra de **triangulação semântica obrigatória**:
$$\text{Atendimento Direto} = \text{Operatividade Sintática} \land \text{Compatibilidade de Domínio} \land \text{Suficiência Funcional da Demanda}$$
- A operatividade sintática ($V \in \text{Verbos Ativos}$) é apenas uma **condição necessária**, jamais suficiente.
- A presença de jargão técnico (ex.: "deploy", "pipeline", "cluster") em uma resposta não autoriza `DIRECT` se o predicado não atuar sobre a meta da demanda específica (ex.: resolver deadlock de banco).
- A extensão textual (número de palavras) deve ser completamente desacoplada do cálculo de pertinência.

---

### 2.8. Como distinguir uma resposta que menciona o contexto da pergunta de uma resposta que efetivamente satisfaz a demanda?
Distinção entre **Papel Temático Tópico** e **Papel Funcional Predicativo**:
- **Menção de Contexto (`RELATED`):** O sujeito da proposição é a tecnologia/contexto, mas o predicado é estático, descritivo, histórico ou relacional (ex.: $P(\text{Kafka}) = \text{foi criado pelo LinkedIn em 2011}$). O estado do problema técnico permanece inalterado.
- **Satisfação da Demanda (`DIRECT`/`PARTIAL`):** O predicado descreve a transformação de estado, o protocolo ou a operação causal que atinge o objetivo da pergunta (ex.: $P(\text{Kafka}) = \text{armazena mensagens em partições ordenadas com offsets sequenciais}$).

---

### 2.9. Quais falhas são de extração de demanda, quais são de interpretação de proposições, quais são de relação semântica e quais são de agregação?
A auditoria dos 70 falsos `DIRECT` e das 28 outras divergências mapeou com precisão a localização estrutural das falhas no pipeline:
- **Extração de Demanda:** $\approx 5\%$ das divergências (perguntas compostas onde o split de demandas não isolou adequadamente os aspectos obrigatórios).
- **Interpretação e Filtragem de Proposições:** $\approx 45\%$ das falhas (incapacidade do `PropositionDiscourseFilter` de reconhecer disjunção de domínio fora do catálogo de 25 palavras, e falha na identificação de evasão complexa e metadados institucionais).
- **Relação Semântica (Nexus Matcher):** $\approx 45\%$ das falhas (o `DemandPropositionNexusBipartiteMatcher` concede `FUNCTIONALLY_SOLVES` via fallback irrestrito na ausência de evidência negativa explícita).
- **Agregação:** $\approx 5\%$ das falhas (o `StrictOntologyRelevanceAggregator` projeta `FUNCTIONALLY_SOLVES` diretamente para `DIRECT` sem validar a consistência e a amplitude dos papéis funcionais).

---

### 2.10. Que evidências permitiriam verificar que a arquitetura proposta generaliza para casos inéditos?
Para garantir generalização sem overfitting:
1. **Zero Referências Nominais no Código:** O código não conterá strings de casos de teste (ex.: "botânica", "orquídeas", "troca de óleo", "LinkedIn", "Apache").
2. **Protocolo Cego com Dataset Sintético e Real Inédito:** Submissão a um conjunto balanceado de teste contendo domínios não técnicos nunca vistos antes (ex.: marcenaria, arquitetura barroca, arqueologia) e tecnologias inventadas (ex.: "HyperLedgerX", "OmegaQueue").
3. **Métricas Estritas de Desempenho:** Atingimento simultâneo de Precisão `DIRECT` $\ge 70\%$, Falsos `DIRECT` $\le 10\%$, e Preservação de Recall `DIRECT` $\ge 85\%$ sem rebaixamento de respostas corretas atípicas.

---

## 3. Auditoria Detalhada dos 70 Casos Falsos DIRECT

A auditoria individual estruturada dos 70 casos classificados como `DIRECT` pelo runtime, mas que possuíam referência diferente no ground truth, encontra-se serializada em `stage_31_7_26_false_direct_case_audit.json`. Abaixo apresenta-se o diagnóstico quantitativo e causal por classe de referência.

### 3.1. Casos OFF_TOPIC (34 casos)
- **Natureza dos casos:** Perguntas técnicas exigindo protocolos de computação distribuída, rede, persistência ou concorrência (ex.: "Como o protocolo 2PC lida com falha do coordenador?", "Como funciona o particionamento no Kafka?"). As respostas apresentavam conteúdo de botânica, culinária não catalogada, pintura ou mecânica veicular.
- **Comportamento do runtime:**
  - `PropositionDiscourseFilter`: `is_alien_domain = False` porque os termos não continham nenhuma das 25 palavras estáticas do catálogo `alien_terms`. Verbo de ação presente e tamanho $>6$ palavras $\rightarrow$ `is_operative = True`.
  - `DemandPropositionNexusBipartiteMatcher`: Caiu na linha 3434 $\rightarrow$ `FUNCTIONALLY_SOLVES`.
  - `StrictOntologyRelevanceAggregator`: Linha 3548 $\rightarrow$ `DIRECT`.
- **Causa-Raiz Primária:** `SEMANTIC_DOMAIN_DISJUNCTION_ABSENCE`. Ausência de ancoragem semântica entre o espaço ontológico da demanda e o espaço de ação da proposição.

### 3.2. Casos RELATED (22 casos)
- **Natureza dos casos:** Respostas que discutiam histórico de criação, licenças open-source, fundações mantenedoras ou popularidade no GitHub de ferramentas como Kafka, Docker, Kubernetes, mas sem explicar os mecanismos operacionais exigidos.
- **Comportamento do runtime:**
  - O filtro de metadados institucionais não interceptou frases com estruturas predicativas transitivas gerais (ex.: "pertence à fundação", "foi desenvolvido originalmente por").
  - Marcadas como `is_operative = True`, foram tratadas pelo matcher como atendimento do sujeito da tecnologia $\rightarrow$ `FUNCTIONALLY_SOLVES`.
- **Causa-Raiz Primária:** `INSTITUTIONAL_METADATA_REGEX_LEAKAGE` e confusão entre menção relacional de tecnologia e mecanismo funcional.

### 3.3. Casos SUPPORTING (7 casos)
- **Natureza dos casos:** O candidato respondeu descrevendo métricas de monitoramento em Prometheus/Grafana ou práticas de telemetria auxiliar quando a pergunta solicitava o algoritmo de balanceamento de carga ou o mecanismo de atomicidade de banco.
- **Comportamento do runtime:**
  - A ação descrita era real ("monitoramos latência via Prometheus"), classificada como `is_operative = True`. O matcher não distinguiu uma ação *instrumental de observabilidade* de um *mecanismo causal de resolução da demanda*.
- **Causa-Raiz Primária:** `AUXILIARY_OBSERVABILITY_STEM_MISALIGNMENT` e falta de verificação de papel causal primário versus papel auxiliar.

### 3.4. Casos INSUFFICIENT (7 casos)
- **Natureza dos casos:** Respostas evasivas, genéricas ou tautológicas com formulações sintaticamente complexas (ex.: "a forma como isso é resolvido varia amplamente conforme as restrições da arquitetura e as demandas de escala do ambiente").
- **Comportamento do runtime:**
  - A presença de verbos ("varia", "atende", "demanda") e extensão razoável evitou o filtro de respostas curtas/ignorância.
  - Marcada como operativa, caiu no fallback permissivo.
- **Causa-Raiz Primária:** `EVASIVE_DEFLECTION_REGEX_LEAKAGE` e presunção de suficiência em orações subordinadas sem conteúdo factual.

---

## 4. Avaliação de Hipóteses Concorrentes e Testes de Refutação

Investigamos oito hipóteses concorrentes para explicar a ocorrência massiva dos 70 falsos `DIRECT`.

| ID | Hipótese | Evidências Favoráveis | Evidências Contrárias | Casos Explicados | Casos Não Explicados | Teste de Refutação | Decisão |
|---|---|---|---|---|---|---|---|
| **H1** | **Permissividade Irrestrita do Fallback de Domínio Aberto** | Linha 3434 de `runtime.py` retorna `FUNCTIONALLY_SOLVES` sempre que `prop.is_operative=True`. | Nenhuma. O código confirma execução explícita desse ramo em 100% dos falsos DIRECTs. | Todos os 70 falsos DIRECTs. | Nenhum. | Inserir asserção na linha 3434: 70/70 casos passam por ali. | **CONFIRMADA** |
| **H2** | **Ausência de Mecanismo de Disjunção Semântica** | `alien_terms` possui apenas 25 termos; botânica/mecânica não catalogadas passam livremente. | Respostas técnicas sem overlap lexical poderiam ser afetadas se a disjunção for mal desenhada. | 34 casos OFF_TOPIC. | 36 casos RELATED/SUPPORTING/INSUFFICIENT. | Testar frases de botânica: `is_alien_domain` resulta `False`. | **CONFIRMADA** |
| **H3** | **Relação Semântica Excessivamente Permissiva** | O matcher assume presunção de suficiência sem validar a correlação entre predicado e meta da demanda. | O matcher possui regras estritas para alguns domínios específicos (2PC, Sagas). | Casos fora dos domínios específicos. | Casos que caem nas regras estritas de 2PC/Sagas. | Proposições sem palavras de 2PC em pergunta de 2PC caem no fallback geral. | **CONFIRMADA** |
| **H4** | **Erro na Extração de Demanda** | Algumas perguntas complexas têm metas múltiplas. | A maioria das perguntas que sofreram falso DIRECT possui apenas 1 demanda clara e bem formulada. | $\approx 3$ casos de demandas compostas. | 67 casos com demandas perfeitamente extraídas. | Inspecionar `decompose_question` nos 70 casos: 67/70 extraíram a demanda corretamente. | **REJEITADA COMO CAUSA PRIMÁRIA** |
| **H5** | **Extração Inadequada de Proposições** | Regexes de segmentação de sentenças podem truncar frases. | As frases foram segmentadas e preservadas integralmente como proposições em 100% dos 70 casos. | 0 casos. | Todos os 70 casos. | Inspecionar `raw_text` das proposições: texto completo preservado. | **REJEITADA** |
| **H6** | **Agregação Incorreta de Evidências** | O agregador promove `FUNCTIONALLY_SOLVES` a `DIRECT` na presença de 1 única demanda. | O agregador apenas seguiu a instrução formal do contrato anterior: se a demanda foi dada como `FUNCTIONALLY_SOLVES`, a classificação é `DIRECT`. | Todos os 70 casos recebem o rótulo do nexus. | O erro já veio consolidado do matcher. | Rastrear o objeto nexus: ele já continha `FUNCTIONALLY_SOLVES`. | **PARCIALMENTE CONFIRMADA (Causa Contribuinte)** |
| **H7** | **Interação Não Prevista entre Componentes** | `PropositionDiscourseFilter` marca `is_operative=True` baseado apenas em sintaxe, e `Matcher` assume que "operativo" significa "tecnicamente pertinente". | Cada componente cumpriu seu contrato local isolado, mas a composição gerou uma falha sistêmica. | Todos os 70 casos. | Nenhum. | Isolar os componentes: o matcher confia cegamente na flag sintática do filtro. | **CONFIRMADA (Falha de Contrato Arquitetural)** |
| **H8** | **Insuficiência de Rastreabilidade** | Rastreabilidade do Ciclo 4 não registrava a justificativa da disjunção de domínio. | O objeto `prediction` contém `predicted_rationale`, permitindo rastrear o fallback da linha 3434. | Permitiu auditar o problema, mas faltaram dados intermediários de domínio. | Não é a causa do erro de classificação em si. | Auditoria dos logs: o motivo foi identificado apesar da telemetria esparsa. | **REJEITADA COMO CAUSA DO ERRO** |

---

## 5. Síntese da Causa-Raiz Estrutural

A causa-raiz dos 70 falsos DIRECTs reside no **Desacoplamento Contratual entre Análise Sintática e Validação Semântica**:
1. O `PropositionDiscourseFilter` declara uma proposição como `is_operative = True` baseando-se unicamente em traços sintáticos superficiais (verbo ativo, ausência de marcadores conhecidos de evasão/antitítese/alienígenas).
2. O `DemandPropositionNexusBipartiteMatcher` interpreta `is_operative = True` como garantia de que a proposição oferece um mecanismo de engenharia válido para a demanda, executando o fallback irrestrito da linha 3434.
3. Não existia entre o filtro e o matcher nenhuma camada responsável por verificar a **Pertinência e Disjunção de Domínio Semântico**, permitindo que orações ativas sobre orquídeas, fundações mantenedoras ou orações evasivas complexas recebessem o status de `FUNCTIONALLY_SOLVES`.

No Ciclo 5, a introdução obrigatória de um componente formal de **Semantic Domain Disjunction** e a reestruturação dos contratos do Bipartite Matcher resolverão definitivamente essa vulnerabilidade estrutural.
