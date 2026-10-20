# Stage 31.7.31 — Especificação Arquitetural Refinada do Motor Semântico (Ciclo 6)

## 1. Visão Geral e Princípios Arquiteturais

A arquitetura do Ciclo 6 reformulada no Stage 31.7.31 estabelece uma transição paradigmática no sistema TechLens: substitui heurísticas estáticas de casamento lexical e vetos absolutos simplistas por um **Pipeline Composicional de Decisão Semântica Baseado em Evidências Refutáveis**.

```text
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
 │                                 PIPELINE ARQUITETURAL DO CICLO 6                                 │
 └──────────────────────────────────────────────────────────────────────────────────────────────────┘
                                                  │
 1. EXTRAÇÃO DE DEMANDAS E INTENÇÃO               ▼
    - Classificação da Intenção em 10 Modos Formais
    - Decomposição em Demanda Principal (Dp), Secundárias (Ds) e Contexto (C)
    - Extração de Entidades-Alvo do Domínio (Eq)
                                                  │
 2. SEGMENTAÇÃO DISCURSIVA E PROPOSICIONAL        ▼
    - Isolamento de Preâmbulos Conversacionais / Ruído Fático
    - Identificação de Orações Subordinadas Analógicas ("funciona como...")
    - Mapeamento de Modificadores: Escopo de Negação, Condicionais e Concessões
    - Detecção de Autocorreções Explícitas ("pensei X, mas na verdade Y")
                                                  │
 3. CONEXÃO TEMÁTICA REFUTÁVEL E AFINIDADE        ▼
    - Formulação de Presunção de Conexão Temática por Entidade Compartilhada
    - Teste de Predicado: Refutação por Ação sobre Domínio Alienígena (Homonímia/Divagação)
    - Detecção de Disjunção Radical Aberta por Entidades Físicas Estranhas
                                                  │
 4. EQUIVALÊNCIA CONCEITUAL E FUNCIONAL           ▼
    - Resolução de Hiperônimos Técnicos e Descrições Funcionais sem Nome Literal
    - Reconhecimento de Tecnologias Inéditas/Fictícias com Mecânica Coerente
    - Veto a Pseudotermos com Propriedades Conflitantes
                                                  │
 5. TRATAMENTO DE ANALOGIAS PEDAGÓGICAS           ▼
    - Desacoplamento entre Domínio-Veículo (Mundo Real) e Domínio-Alvo (Software)
    - Verificação da Transposição e Aterrisagem no Sistema Computacional
    - Neutralização de Comparações Superficiais sem Mecanismo
                                                  │
 6. SUFICIÊNCIA RELATIVA À INTENÇÃO               ▼
    - Avaliação Bipartite de Cobertura de Demandas (Dp, Ds)
    - Aplicação de Critérios Específicos por Modo de Intenção (Definição vs Diagnóstico)
    - Detecção de Contradições Internas Destrutivas
                                                  │
 7. AGREGAÇÃO ONTOLÓGICA ESTRITA RECONCILIADA     ▼
    - Tabela de Decisão Determinística das 7 Classes Canônicas
    - Roteamento Explícito: THEMATICALLY_ADJACENT ──► RELATED
    - Eliminação do "Sumidouro" de OFF_TOPIC
    - Emissão de Trilha Auditável Causal e Grau de Confiança Epistêmica
```

---

## 2. Especificação Detalhada dos Sete Estágios do Pipeline

### 2.1. Estágio 1: Extração de Demandas e Intenção (`QuestionProfileExtractor`)
- **Entrada:** `question_text: str`
- **Saída:** `QuestionProfile`
- **Estrutura de Dados:**
  ```python
  @dataclass(frozen=True)
  class QuestionProfile:
      intent_mode: str               # 1 dos 10 modos (DEFINITION, MECHANISM, COMPARISON, etc.)
      primary_demand: QuestionDemand # Demanda principal obrigatória (Dp)
      secondary_demands: tuple[QuestionDemand, ...] # Demandas secundárias obrigatórias (Ds)
      target_entities: tuple[str, ...] # Entidades centrais do domínio (Eq: e.g. "PostgreSQL", "MVCC")
      domain_context: str            # Contexto opcional (e.g. "alta concorrência")
      requires_operational_verbs: bool # True somente para IMPLEMENTATION e TROUBLESHOOTING
  ```

### 2.2. Estágio 2: Segmentação Discursiva e Proposicional (`DiscourseSegmentationEngine`)
- **Entrada:** `response_text: str`
- **Saída:** `DiscourseProfile`
- **Responsabilidades:**
  1. *Filtro de Preâmbulo:* Sentenças iniciais contendo marcadores conversacionais ("hoje o trânsito estava péssimo", "antes de começar tomei um café") são marcadas como `CONVERSATIONAL_PREAMBLE` e isoladas, não contaminando o núcleo técnico.
  2. *Marcação de Analogias:* Orações iniciadas por conjunções comparativas (*"funciona como"*, *"é parecido com"*, *"se parece a"*) são etiquetadas como `ANALOGY_VEHICLE`.
  3. *Escopo de Negação e Condição:* Sintagmas condicionais (*"se o circuit breaker estiver aberto..."*) e operadores de negação (*"não devemos"*, *"evitar"*) são vinculados às proposições que modificam.
  4. *Autocorreção Explícita:* Em construções onde o candidato corrige uma asserção prévia (*"pensei que fosse X, mas no plano vi que é Y"*), a asserção retificada é marcada como `RETRACTED_ASSERTION` e a conclusão prevalece.

### 2.3. Estágio 3: Conexão Temática Refutável e Afinidade (`ThematicAffinityEngine`)
- **Princípio Operacional:** O compartilhamento de entidades ($E_R \cap E_Q \neq \emptyset$) estabelece uma **presunção preliminar de conexão temática**, e **NÃO** um veto absoluto a `OFF_TOPIC`.
- **Mecanismo de Refutação:**
  $$\text{Se } (E_R \cap E_Q \neq \emptyset) \text{ MAS } \text{Predicados}(E_R) \subseteq \text{Domínio Alienígena} \implies \textbf{Presunção Refutada (OFF\_TOPIC)}$$
  *(Exemplo: "Injeção de dependências no Spring é como a dependência econômica de petróleo". A entidade coincide, mas os predicados atuam sobre comércio exterior).*
- **Disjunção Radical:** Identificada quando os argumentos nucleares da oração pertencem a ofícios não-computacionais (argila, cimento, poda, safena) sem transposição analógica para a computação.

### 2.4. Estágio 4: Avaliação de Equivalência Conceitual e Funcional (`ConceptualEquivalenceEngine`)
- **Princípio:** Uma resposta pode ser 100% resolutiva sem repetir literalmente o nome do artefato da pergunta.
- **Mecanismos:**
  1. *Hiperônimos e Descrições Funcionais:* Reconhece que "árvore balanceada de chaves ordenadas" é equivalente a "B-tree", e "token de unicidade conferido em tabela" é implementação direta de "idempotência".
  2. *Tecnologias Inéditas / Fictícias:* Avalia se o princípio científico descrito (relógios vetoriais, consenso em duas fases) é logicamente coerente, aceitando a tecnologia desconhecida (e.g. VulcanDB) como `DIRECT`.
  3. *Detecção de Pseudotermos Incompatíveis:* Identifica quando o candidato utiliza termos de aparência técnica mas atribui propriedades fisicamente contraditórias (e.g. "fila assíncrona síncrona bloqueante").

### 2.5. Estágio 5: Resolução de Analogias Pedagógicas (`AnalogyResolutionEngine`)
- **Separação Analógica:**
  - `Domínio-Veículo` ($D_V$): O objeto da metáfora (disjuntor elétrico residencial, encanamento de água).
  - `Domínio-Alvo` ($D_T$): O sistema computacional sob análise (microsserviços, buffer de rede).
- **Regra de Aceitação:** Uma analogia pedagógica só confere mérito à resposta se houver **aterrissagem comprovada no domínio-alvo**:
  $$\text{Analogia Válida} \iff \text{Mapeamento}(D_V \to D_T) \land \text{Mecanismo Resolvido em } D_T$$
  Se o candidato apenas discursar sobre o disjuntor da casa sem explicar o que o software faz, a resposta é `INSUFFICIENT` ou `RELATED`, jamais `DIRECT`.

### 2.6. Estágio 6: Suficiência Relativa à Intenção (`SufficiencyAssessmentEngine`)
- **Matriz de Adequação por Intenção:**
  - `DEFINITION`: Exige definições de propriedades e garantias. Não exige código nem comandos.
  - `MECHANISM`: Exige elucidação dos componentes internos e fluxo causal.
  - `COMPARISON`: Exige contraste simétrico dos eixos estruturais de ambos os polos.
  - `DIAGNOSIS`: Exige procedimento sistemático de investigação. Não exige a correção do bug.
  - `IMPLEMENTATION`: Exige comandos, algoritmos ou mecanismos operacionais concretos.
- **Demandas Compostas:** Bipartite matching com cálculo de cobertura:
  $$\text{Cobertura} = \frac{\text{Demandas Plenamente Atendidas}}{\text{Total de Demandas Obrigatórias}}$$

### 2.7. Estágio 7: Agregação Ontológica Estrita Reconciliada (`StrictRelevanceAggregator`)
- **Tabela de Decisão Canônica:**
  ```python
  # 1. Vetos Sumários de Segurança e Disjunção
  if is_disjoint_alien or is_destructive_antithesis:
      return "OFF_TOPIC"
  
  # 2. Insuficiência e Evasão
  elif is_explicit_ignorance or is_evasive_consulting or is_empty_filler:
      return "INSUFFICIENT"
  
  # 3. Indeterminação e Tautologia
  elif is_unresolved_ambiguity or is_circular_tautology:
      return "UNKNOWN"
  
  # 4. Avaliação Composta (Multi-Demand)
  elif len(demands) > 1:
      if coverage == 1.0:
          return "DIRECT"
      elif coverage > 0.0 or has_partial_aspect:
          return "PARTIAL"
      elif has_supporting_only:
          return "SUPPORTING"
      elif has_thematic_metadata:
          return "RELATED"
      else:
          return "INSUFFICIENT" # ELIMINADO O SUMIDOURO DE OFF_TOPIC!
  
  # 5. Avaliação de Demanda Única
  else:
      nexus = single_demand_nexus
      if nexus == "FUNCTIONALLY_SOLVES":
          return "DIRECT"
      elif nexus == "PARTIALLY_SOLVES":
          return "PARTIAL"
      elif nexus == "CONTRIBUTES_TO":
          return "SUPPORTING"
      elif nexus == "THEMATICALLY_ADJACENT" or nexus == "NON_OPERATIVE":
          # CORREÇÃO ESTRUTURAL CRÍTICA DO CICLO 6:
          # Proposições que compartilham a entidade ou ecossistema mas não apresentam
          # mecanismo operacional são fixadas deterministicamente em RELATED!
          return "RELATED"
      else:
          return "INSUFFICIENT"
  ```

---

## 3. Modelo de Rastreabilidade e Auditoria Epistêmica

Cada avaliação gerará obrigatoriamente um registro auditável no formato JSON com 7 nós fundamentais:
1. `question_profile`: Intenção e demandas extraídas;
2. `discourse_segments`: Segmentos isolados (preâmbulos, analogias, núcleo técnico);
3. `thematic_evaluation`: Análise de presunção de entidade e teste de refutação;
4. `equivalence_evaluation`: Hiperônimos e equivalências funcionais aplicadas;
5. `analogy_evaluation`: Mapeamento entre domínio-veículo e domínio-alvo;
6. `demand_nexus_matrix`: Relações bipartites por demanda;
7. `aggregation_audit`: Regra determinística acionada e grau de incerteza residual.
