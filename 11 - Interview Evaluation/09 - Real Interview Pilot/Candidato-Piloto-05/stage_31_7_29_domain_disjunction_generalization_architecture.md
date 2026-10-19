# Stage 31.7.29 — Arquitetura de Generalização de Disjunção de Domínio (Ciclo 6)

## 1. Visão Geral da Arquitetura do Ciclo 6

A arquitetura do Ciclo 6 substitui a enumeração estática de regexes por um modelo formal de **Vinculação de Entidades e Afinidade Semântica (Entity-Domain Binding & Semantic Affinity)**, eliminando definitivamente a dependência de dicionários fechados de profissões ou setores cotidianos, e restaurando o papel ontológico legítimo da classe `RELATED`.

```text
 ┌──────────────────────────────────────────────────────────────────────────────────┐
 │                            ARQUITETURA DO CICLO 6                               │
 └──────────────────────────────────────────────────────────────────────────────────┘
                                         │
 1. EXTRAÇÃO DE DEMANDA                 ▼
    - Entidades Nucleares da Pergunta (Target Entities: e.g. "PostgreSQL", "Kafka")
    - Intenção da Pergunta (Conceptual, Comparative, Diagnostic, Implementation, Historical)
    - Demandas Obrigatórias (Aspects 1..N)
                                         │
 2. EXTRAÇÃO DE PROPOSIÇÕES             ▼
    - Segmentação Oracional
    - Entidades Nucleares da Resposta (Subject Entities: e.g. "Berkeley", "Cimento")
    - Modalidade Gramatical (Operative Action, Descriptive History, Observability, Filler)
                                         │
 3. COMPATIBILIDADE DE DOMÍNIO          ▼
    - Teste de Afinidade de Entidade (Entity-Topic Affinity)
    - Detecção de Disjunção Radical Aberta (Alien Domain Binding)
    - Salvaguarda: Compartilhar a Entidade da Pergunta VETA OFF_TOPIC!
                                         │
 4. MATRIZ DE RELAÇÃO FUNCIONAL         ▼
    - Bipartite Nexus Matching baseado em Ação sobre a Entidade da Demanda
    - Desacoplamento entre Operatividade e Pertinência
                                         │
 5. SUFICIÊNCIA RELATIVA À INTENÇÃO     ▼
    - Definições e Comparações dispensam código operacional
                                         │
 6. COBERTURA DE EXIGÊNCIAS             ▼
    - Avaliação de Decomposição Composta (Full vs Partial)
                                         │
 7. AGREGAÇÃO ONTOLÓGICA ESTRITA        ▼
    - Roteamento Explícito: THEMATICALLY_ADJACENT ──► RELATED
    - Eliminação do "Sumidouro" de OFF_TOPIC
    - Trilha de Auditoria Causal Completa
```

---

## 2. Especificação dos Componentes do Ciclo 6

### 2.1. Componente 1: Extrator de Demandas e Entidades-Alvo (`QuestionDemandAndEntityExtractor`)
- **Responsabilidade:** Extrair não apenas o texto da demanda, mas as **Entidades Nucleares do Domínio da Pergunta** ($E_Q$).
- **Contrato de Saída:**
  ```python
  @dataclass(frozen=True)
  class TargetEntityProfile:
      entity_stems: tuple[str, ...]      # e.g. ("postgres", "banco", "tabela", "mvcc")
      is_computing_domain: bool          # True se pertence a software/infraestrutura
      intent_type: str                   # "CONCEPTUAL", "COMPARATIVE", "HISTORICAL", "OPERATIVE"
      demands: tuple[QuestionDemand, ...]
  ```

### 2.2. Componente 2: Extrator de Proposições e Entidades de Resposta (`PropositionEntityExtractor`)
- **Responsabilidade:** Isolar as **Entidades Nucleares da Proposição** ($E_R$) e sua relação com os verbos de ação.
- **Contrato de Saída:**
  ```python
  @dataclass(frozen=True)
  class PropositionEntityProfile:
      proposition_id: str
      text: str
      entity_stems: tuple[str, ...]      # e.g. ("berkeley", "stonebraker", "sql") ou ("cimento", "betoneira")
      grammatical_mode: str              # "OPERATIVE_ACTION", "DESCRIPTIVE_METADATA", "TELEMETRY", "EVASIVE"
      is_antithesis: bool
      is_ambiguous: bool
      is_ignorance: bool
  ```

### 2.3. Componente 3: Motor Generalizável de Afinidade e Disjunção (`OpenDomainAffinityEngine`)
- **Responsabilidade:** Substituir as listas fechadas de regexes por dois testes universais:
  1. **Regra de Afinidade Compartilhada (Thematic Anchor):**
     Se a proposição compartilha ao menos uma entidade nuclear com a pergunta ($E_R \cap E_Q \neq \emptyset$), ou referencia diretamente a tecnologia indagada (e.g. "PostgreSQL", "Docker", "Linux"), a proposição é **TEMATICAMENTE COMPATÍVEL**.
     $$\textbf{Veto Inegociável:} \quad (E_R \cap E_Q \neq \emptyset) \implies \text{is\_disjoint} = \text{False}$$
     Essa regra impede categoricamente que respostas sobre a história ou criadores de uma tecnologia sejam classificadas como `OFF_TOPIC`.
  2. **Regra de Disjunção Radical Aberta (Alien Domain Separation):**
     Se a proposição possui substantivos nucleares concretos ($E_R$) que não possuem nenhuma intersecção com a pergunta ($E_R \cap E_Q = \emptyset$) E não possuem nenhum token do léxico amplo de computação/sistemas E não atuam sobre a entidade da pergunta, a proposição é marcada como **`DISJOINT_ONTOLOGY`**.
     Isso detecta cerâmica, construção, botânica e culinária **sem precisar de listas prévias dessas profissões**.

### 2.4. Componente 4: Casador de Nexo Demanda-Proposição (`SemanticNexusBipartiteMatcher`)
- **Responsabilidade:** Mapear a relação entre a demanda e a proposição com base em **Ação sobre a Entidade**:
  - `FUNCTIONALLY_SOLVES`: A proposição executa uma ação ou fornece uma definição válida **sobre a entidade da demanda**.
  - `CONTRIBUTES_TO`: A proposição fornece observabilidade, telemetria ou suporte auxiliar **sobre a entidade da demanda**.
  - `THEMATICALLY_ADJACENT`: A proposição compartilha a entidade da demanda ($E_R \cap E_Q \neq \emptyset$), mas fornece apenas metadados, contexto histórico, criadores ou declarações de uso, sem mecânica resolutiva.
  - `ANTITHESIS_OPPOSED`: A proposição propõe ações destrutivas (sem guarda de evitação) que anulam travas/proteções.
  - `DOMAIN_DISJUNCT`: A proposição opera sobre entidades alienígenas sem qualquer nexo com a demanda.
  - `EVASIVE` / `IGNORANCE` / `INSUFFICIENT`: Respostas sem substância técnica avaliável.
  - `AMBIGUOUS` / `TAUTOLOGY`: Indeterminação ou repetição circular vazia.

### 2.5. Componente 5: Agregador Ontológico Estrito Reconciliado (`ReconciledOntologyAggregator`)
- **Responsabilidade:** Eliminar o sumidouro `else: OFF_TOPIC` e implementar a tabela de decisão canônica:
  ```python
  if any(n == "DOMAIN_DISJUNCT" for n in nexuses) or any(n == "ANTITHESIS_OPPOSED" for n in nexuses):
      return "OFF_TOPIC"
  elif any(n == "IGNORANCE" for n in nexuses) or any(n == "INSUFFICIENT" for n in nexuses) or any(n == "EVASIVE" for n in nexuses):
      return "INSUFFICIENT"
  elif any(n == "AMBIGUOUS" for n in nexuses) or any(n == "TAUTOLOGY" for n in nexuses):
      return "UNKNOWN"
  elif len(demands) > 1:
      # Avaliação composta: DIRECT se todas atendidas, PARTIAL se >=1 atendida
      ...
  else:
      # Demanda única
      nx = nexuses[0]
      if nx == "FUNCTIONALLY_SOLVES":
          return "DIRECT"
      elif nx == "PARTIALLY_SOLVES":
          return "PARTIAL"
      elif nx == "CONTRIBUTES_TO":
          return "SUPPORTING"
      elif nx == "THEMATICALLY_ADJACENT" or nx == "NON_OPERATIVE":
          # CORREÇÃO ESTRUTURAL CRÍTICA:
          # Se a proposição não é operativa, mas compartilha o tema da pergunta,
          # ela é obrigatoriamente RELATED, e NUNCA OFF_TOPIC!
          return "RELATED"
  ```

---

## 3. Trilha de Auditoria Causal Obrigatória

Toda predição do Ciclo 6 deve obrigatoriamente conter uma trilha explicativa formal:
1. `question_entities`: Entidades nucleares detectadas na pergunta;
2. `response_entities`: Entidades nucleares detectadas na resposta;
3. `entity_overlap`: Entidades em comum entre pergunta e resposta;
4. `domain_affinity_status`: `COMPATIBLE_ANCHORED`, `DISJOINT_ALIEN`, `GENERAL_COMPUTING`;
5. `grammatical_mode`: `OPERATIVE_ACTION`, `DESCRIPTIVE_METADATA`, `TELEMETRY_AUXILIARY`, `INSUFFICIENT_FILLER`;
6. `nexus_relations`: Relações atribuídas por demanda;
7. `aggregation_rule`: Regra determinística que justificou a classe final;
8. `epistemic_confidence`: Grau de certeza da predição.
