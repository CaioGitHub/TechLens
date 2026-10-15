# Stage 31.7.26 — Especificação Arquitetural: Semantic Domain Disjunction Engine (Ciclo 5)

## 1. Visão Geral da Arquitetura

O Ciclo 5 do sistema TechLens introduz uma camada estrutural explícita de **Verificação de Compatibilidade e Disjunção de Domínio Semântico** (`SemanticDomainDisjunctionEngine`), eliminando definitivamente o afunilamento permissivo de domínio aberto que causou 70 falsos `DIRECT` no Stage 31.7.25.

A nova arquitetura estabelece que nenhuma proposição pode ser promovida a `FUNCTIONALLY_SOLVES` apenas por ser sintaticamente bem formada ou conter verbos de ação. A atribuição de relevância direta exige a **triangulação formal entre operatividade, compatibilidade de domínio semântico e suficiência causal**.

```text
               Pergunta do Entrevistador
                          │
                          ▼
        ┌───────────────────────────────────┐
        │ SemanticIntentAndDemandExtractor   │
        └─────────────────┬─────────────────┘
                          │ (Demanda Primária: Sujeito, Metas, Domínio Ontológico)
                          ▼
        ┌───────────────────────────────────┐
        │  SemanticDomainDisjunctionEngine  │◄── Proposições da Resposta
        └─────────────────┬─────────────────┘    (extraídas via PropositionDiscourseFilter)
                          │
      ┌───────────────────┴───────────────────┐
      │                                       │
      ▼ (Se DISJUNÇÃO DEMONSTRADA)            ▼ (Se COMPATÍVEL ou NÃO-DISJUNTO)
┌───────────┐                       ┌────────────────────────────────────────┐
│ OFF_TOPIC │                       │ DemandPropositionNexusBipartiteMatcher │
└───────────┘                       └───────────────────┬────────────────────┘
                                                        │ (Nexus Relations:
                                                        │  FUNCTIONALLY_SOLVES,
                                                        │  PARTIALLY_SOLVES,
                                                        │  AUXILIARY_OBSERVABILITY,
                                                        │  THEMATIC_MENTION_ONLY,
                                                        │  INSUFFICIENT_EVIDENCE)
                                                        ▼
                                    ┌────────────────────────────────────────┐
                                    │ StrictOntologyRelevanceAggregator      │
                                    └───────────────────┬────────────────────┘
                                                        │
                                                        ▼
                                        Classificação Final Auditável
                                        (DIRECT, PARTIAL, SUPPORTING,
                                         RELATED, INSUFFICIENT, UNKNOWN)
```

---

## 2. Princípios de Desenho e Salvaguardas Semânticas

### 2.1. Não confundir domínio disjunto com ausência de sobreposição lexical (Invariância Semântica)
- A ausência de tokens idênticos entre a pergunta e a resposta **não** autoriza a inferência de `OFF_TOPIC`.
- **Exemplo Real:** Se a pergunta demanda a resolução de concorrência em transações distribuídas ("Como manter integridade sem bloqueio de tabela?") e o candidato explica atomicidade com coordenação em duas fases, logs de undo/redo e confirmação assíncrona sem repetir a palavra "integridade" ou "bloqueio", a arquitetura avalia o **tipo de problema funcional** (espaço de estados, concorrência, consistência). Os traços semânticos e operacionais do domínio técnico coincidem, atestando compatibilidade semântica.

### 2.2. Não confundir domínio disjunto com entidade desconhecida
- O sistema é ontologicamente aberto: a presença de uma ferramenta, biblioteca ou banco de dados nunca visto no treinamento (ex.: "Z-KVS", "HyperLogQueue") não invalida a resposta.
- A compatibilidade não depende de um cadastro prévio de nomes próprios de software, mas da **natureza da operação predicada** (armazenamento, roteamento, transformação de dados, tratamento de falhas) e de sua aplicabilidade ao domínio do problema.

### 2.3. Exigência de evidência positiva de atendimento
- Para atingir `DIRECT`, a resposta deve conter evidência positiva de que o mecanismo explicado satisfaz a demanda primária obrigatória.
- **Hierarquia de Validação:**
  1. *Sentença Operativa:* É apenas a forma gramatical ativa.
  2. *Sentença Operativa de Domínio Pertinente:* É uma ação aplicável ao universo da engenharia de software / infraestrutura.
  3. *Sentença Operativa com Nexo Causal:* É uma ação que efetivamente resolve o desafio proposto pela pergunta.
  4. *Atendimento Suficiente:* Cobre todas as demandas primárias obrigatórias sem lacunas críticas.

### 2.4. Preservação estrita da incerteza
- Quando as evidências lexicais, sintáticas e estruturais não permitirem concluir nem pela satisfação funcional nem pela disjunção absoluta, o sistema **não deve adivinhar**.
- Casos ambíguos ou incompletos devem transitar formalmente para `INSUFFICIENT` ou `UNKNOWN`, com telemetria explícita do nível de confiança.

---

## 3. Especificação dos Componentes e Fluxo de Decisão

### 3.1. `SemanticDomainDisjunctionEngine` (Novo Componente Central)
**Responsabilidade:** Avaliar a compatibilidade ontológica e funcional entre o espaço de domínio da demanda e o espaço de ação das proposições da resposta.
- **Entradas:**
  - `Demands`: Lista de demandas primárias com seus objetivos de aspecto e entidades centrais.
  - `Propositions`: Lista de proposições extraídas da resposta.
- **Mecanismo Interno:**
  1. *Extração do Domínio da Demanda ($D_{dom}$):* Classificação do problema computacional (ex.: persistência, mensageria, rede, concorrência, ciclo de vida, governança).
  2. *Extração do Domínio da Proposição ($P_{dom}$):* Análise dos semas e papéis temáticos do predicado da proposição.
  3. *Verificação de Disjunção Radical:* Identificação de evidência positiva de domínios ontologicamente incompatíveis (ex.: processos biológicos/botânicos, culinária, mecânica de combustão interna, artefatos artísticos) que operam em ordens de grandeza e universos de leis físicas totalmente alheios à computação.
  4. *Filtro de Metadados Categoriais:* Se a proposição apenas atribui a tecnologia a uma fundação mantenedora, licença ou categoria ampla sem predicado operacional de engenharia, classifica o nexo local como `THEMATIC_METADATA_ONLY` (direcionando para `RELATED`).
- **Saída:** Objeto `DomainCompatibilityRecord` contendo:
  - `is_disjoint`: booleano indicando incompatibilidade ontológica demonstrada.
  - `disjunction_type`: `RADICAL_DISJUNCTION` (leva a `OFF_TOPIC`), `THEMATIC_METADATA` (leva a `RELATED`), ou `COMPATIBLE_TECHNICAL_DOMAIN`.
  - `rationale`: justificativa formal auditável.

### 3.2. `PropositionDiscourseFilter` (Refatoração de Contrato)
- O filtro deixa de ter poder soberano sobre o status de atendimento da demanda.
- Sua atribuição é estritamente pragmática e discursiva:
  - Segmentar orações em proposições atômicas.
  - Detectar polaridade sintática (afirmativa, negativa, hipotética, antitética).
  - Identificar marcadores de evasão e ignorância fática.
  - Identificar proposições de experiência puramente declarada ("trabalhei 5 anos com isso").
  - Identificar orações de observabilidade instrumental (ex.: "olhamos as métricas no Datadog").

### 3.3. `DemandPropositionNexusBipartiteMatcher` (Remoção do Fallback Irrestrito)
- **Eliminação do Fallback da Linha 3434:** A concessão incondicional de `FUNCTIONALLY_SOLVES` para qualquer sentença operativa é revogada.
- **Novas Regras de Nexo Bipartido:**
  - Se a proposição for marcada como `is_disjoint = True` pelo `SemanticDomainDisjunctionEngine`, o nexo é sumariamente fixado como `DISJOINT_ONTOLOGY` (vetando `DIRECT` e `PARTIAL`).
  - Se a proposição for de metadados institucionais (`THEMATIC_METADATA`), o nexo é `THEMATIC_MENTION_ONLY` (ancorando em `RELATED`).
  - Se a proposição for instrumental/observabilidade, o nexo é `AUXILIARY_OBSERVABILITY` (ancorando em `SUPPORTING`).
  - Se a proposição descreve o mecanismo causal aplicável à demanda, o nexo é `FUNCTIONALLY_SOLVES`.
  - Se a proposição for vaga, evasiva ou tautológica, o nexo é `INSUFFICIENT_EVIDENCE`.

### 3.4. `StrictOntologyRelevanceAggregator` (Agregação com Governança Estrita)
- Recebe a matriz de nexos bipartite entre todas as demandas primárias obrigatórias e as proposições.
- **Regras Formais de Emissão da Classe Final:**
  - **`DIRECT`:** Todas as demandas primárias obrigatórias possuem ao menos uma proposição associada com nexo `FUNCTIONALLY_SOLVES`, com compatibilidade de domínio confirmada e sem predominância de contradição antitética.
  - **`PARTIAL`:** Em perguntas compostas (múltiplas demandas obrigatórias), ao menos uma demanda possui `FUNCTIONALLY_SOLVES`, mas uma ou mais demandas obrigatórias permanecem não atendidas; ou, em pergunta simples, atendimento de escopo parcial demonstrado.
  - **`SUPPORTING`:** Nenhuma demanda atinge `FUNCTIONALLY_SOLVES`, mas há presença de proposições com nexo `AUXILIARY_OBSERVABILITY` pertinentes ao ecossistema da pergunta.
  - **`RELATED`:** Nenhuma demanda atinge `FUNCTIONALLY_SOLVES`, mas há menções temáticas válidas da entidade ou metadados institucionais/categoriais (`THEMATIC_MENTION_ONLY`).
  - **`OFF_TOPIC`:** Presença de evidência positiva de disjunção ontológica radical (`DISJOINT_ONTOLOGY`) sem nenhuma proposição técnica compatível.
  - **`INSUFFICIENT`:** Resposta que tenta abordar o domínio técnico, mas cujo conjunto de proposições resulta exclusivamente em `INSUFFICIENT_EVIDENCE` ou evasão discursiva.
  - **`UNKNOWN`:** Nenhuma proposição inteligível extraída, ou todas as proposições são de ignorância declarada explícita.

---

## 4. Tratamento de Demandas Compostas e Cobertura

Em perguntas compostas (ex.: "Explique o particionamento no Kafka e como garantir entrega exatamente uma vez"):
1. **Decomposição Semântica:** A pergunta é decomposta em demandas atômicas obrigatórias ($D_1$ = Mecanismo de Particionamento, $D_2$ = Semântica Exactly-Once / Idempotência).
2. **Independência de Atendimento:** Cada demanda $D_i$ deve receber cobertura funcional independente.
3. **Proibições Estruturais:**
   - Proibido considerar uma pergunta atendida (`DIRECT`) se apenas $D_1$ for satisfeita (deve classificar como `PARTIAL`).
   - Proibido reaproveitar artificialmente o mesmo predicado sintático para satisfazer $D_1$ e $D_2$, a menos que a proposição formule explicitamente a causalidade unificada (ex.: "a chave de partição garante ordem local, e o offset transacional com produtor idempotente garante entrega exatamente uma vez").

---

## 5. Rastreabilidade e Auditoria Externa

Todas as decisões do runtime no Ciclo 5 devem gerar uma trilha de telemetria estruturada contendo:
- `identified_demands`: Lista de demandas com IDs e aspectos.
- `extracted_propositions`: Lista de proposições com flags sintáticas e papéis discursivos.
- `domain_disjunction_assessment`: Registro de análise de domínio ontológico com justificativa.
- `bipartite_nexus_matrix`: Mapeamento explícito $[D_i \times P_j]$ com o tipo de nexo atribuído.
- `aggregation_path`: Rota lógica percorrida pelo agregador para produzir a classe final.

Esta especificação assegura que nenhuma classificação ocorra por efeito colateral ou presunção cega, permitindo contestação e correção controlada em caso de anomalia.
