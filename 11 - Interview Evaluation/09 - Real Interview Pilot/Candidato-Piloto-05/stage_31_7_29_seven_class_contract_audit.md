# Stage 31.7.29 — Auditoria de Contratos e Fronteiras das Sete Classes Canônicas

## 1. Princípio Ontológico Fundamental

A avaliação semântica do TechLens opera sobre uma partição estrita de **sete classes canônicas de relevância**. Nenhuma classe pode ser tratada como resíduo informal ou sumidouro por exclusão. Cada classe exige critérios positivos de sustentação evidencial e salvaguardas negativas claras.

```text
                           ┌────────────────────────┐
                           │ Proposição sob Análise │
                           └───────────┬────────────┘
                                       │
            ┌──────────────────────────┴──────────────────────────┐
            ▼                                                     ▼
   [Pertinência Temática]                               [Incompatibilidade / Falta]
      │                                                           │
      ├─► Atendimento Pleno: DIRECT                               ├─► Disjunção Radical: OFF_TOPIC
      ├─► Atendimento Parcial: PARTIAL                            ├─► Antítese Destrutiva: OFF_TOPIC
      ├─► Suporte Auxiliar: SUPPORTING                            ├─► Falta de Evidência: INSUFFICIENT
      └─► Contexto Sem Mecanismo: RELATED                         └─► Indeterminação/Tautologia: UNKNOWN
```

---

## 2. Auditoria Individual das Sete Classes

### 2.1. Classe `DIRECT` (Atendimento Funcional Pleno)
- **Definição Canônica:** A resposta resolve, elucida ou define diretamente todas as demandas centrais obrigatórias da pergunta, com grau adequado de profundidade técnica.
- **Evidência Positiva Exigida:** Proposição funcionalmente operativa cujos substantivos, entidades e ações atuam diretamente sobre o domínio da demanda.
- **Salvaguardas Negativas Obrigatórias:**
  - NÃO pode aceitar proposições gramaticalmente ativas que operem sobre domínios alienígenas (artesanato, construção civil, culinária).
  - NÃO pode promover metadados históricos ou institucionais desprovidos de mecanismo.
  - NÃO pode aceitar respostas que atendam apenas metade de perguntas compostas multiaspecto.
- **Suficiência Relativa à Intenção:** Se a pergunta for conceitual (e.g. Idempotência), a definição formal é suficiente (`DIRECT`), sem exigir código operacional. Se for comparativa, os eixos de contraste são suficientes.

### 2.2. Classe `PARTIAL` (Atendimento Parcial de Demandas)
- **Definição Canônica:** A resposta atende legitimamente a uma parte das exigências obrigatórias da pergunta, mas omite ou falha em atender a outros aspectos essenciais.
- **Evidência Positiva Exigida:** Cobertura comprovada de ao menos 1 aspecto primário com lacuna explícita ou não resolução de outro aspecto primário obrigatório.
- **Fronteira com `DIRECT`:** A presença de demandas compostas (e.g., particionamento + ordenação) veta `DIRECT` caso apenas o particionamento seja explicado.
- **Fronteira com `RELATED`:** Uma resposta parcial precisa resolver ao menos um mecanismo de forma operativa, e não apenas discorrer perifericamente sobre o tema.

### 2.3. Classe `SUPPORTING` (Contribuição Auxiliar ou Instrumental)
- **Definição Canônica:** A resposta fornece informações úteis, mas estritamente instrumentais ou de suporte (observabilidade, telemetria, dashboards Prometheus/Grafana, tracing OpenTelemetry, métricas, logs), sem solucionar o mecanismo causal subjacente.
- **Evidência Positiva Exigida:** Proposição contendo mecanismos de monitoramento, diagnóstico passivo ou alertas voltados à infraestrutura da demanda.
- **Fronteira com `DIRECT`:** Se a pergunta indagar especificamente *"Como observar/monitorar X"*, a telemetria é `DIRECT`. Se indagar *"Como resolver contencao de locks"*, a telemetria é estritamente `SUPPORTING`.
- **Fronteira com `OFF_TOPIC`:** A instrumentação auxilia a operação do sistema em questão e, portanto, é funcionalmente conectada, jamais sendo disjunta.

### 2.4. Classe `RELATED` (Contexto Temático sem Atendimento Operacional)
- **Definição Canônica:** A resposta compartilha o contexto, a tecnologia, a categoria ou as entidades da pergunta (PostgreSQL, Linux, Docker, microsserviços), mas limita-se a metadados institucionais, história, criadores, licenças ou declarações biográficas sem descrever a mecânica exigida.
- **Evidência Positiva Exigida:** Afinidade de entidades com o tema da pergunta acompanhada de ausência de proposição técnica operativa resolutiva.
- **Fronteira Crítica com `OFF_TOPIC`:** A ausência de código ou de mecanismo operacional **NÃO transforma a resposta em `OFF_TOPIC`**. Compartilhar a entidade temática garante que o candidato está no mesmo assunto.
- **Fronteira com `DIRECT`:** Metadados sobre quem criou o Docker não respondem como o Docker isola processos com namespaces.

### 2.5. Classe `OFF_TOPIC` (Disjunção Ontológica ou Antítese Destrutiva)
- **Definição Canônica:** O conteúdo da resposta é completamente alienígena ao domínio computacional da pergunta, ou apresenta antítese destrutiva explícita (ações que anulam ou destroem as garantias operacionais básicas de transações, segurança ou concorrência).
- **Evidência Positiva Exigida:**
  1. *Disjunção Radical:* Entidades centrais pertencentes a universos não computacionais (farinha, argila, cimento, óleo 5W30, orquídeas) sem qualquer nexo com a tecnologia indagada.
  2. *Antítese Destrutiva:* Propostas de desligar travas, desativar WAL, remover fsync, desabilitar filtros de autenticação JWT ou arrancar circuit breakers para acelerar o sistema.
- **Salvaguarda Fundamental:** **Exige evidência positiva de disjunção ou destruição.** Não pode ser inferida por silêncio ou por simples falha de casamento de regras de outras classes.

### 2.6. Classe `INSUFFICIENT` (Substância Técnica Insuficiente ou Evasiva)
- **Definição Canônica:** A resposta representa uma tentativa de comunicação que não chega a articular conteúdo avaliável, incluindo declarações explícitas de ignorância (*"Não sei"*, *"Nunca trabalhei"*), deflexões evasivas corporativas/orçamentárias (*"Depende do orçamento e dos stakeholders"*), jargões vazios ("buzzword soup") ou preenchimentos conversacionais (*"Sim, com certeza"*).
- **Evidência Positiva Exigida:** Proposições de desconhecimento, evasão política/financeira ou enunciados conversacionais sem proposições técnicas.
- **Fronteira com `UNKNOWN`:** Ignorância declarada é falta de evidência do candidato (`INSUFFICIENT`), e não incerteza do sistema (`UNKNOWN`).

### 2.7. Classe `UNKNOWN` (Indeterminação Semântica e Tautologia Reflexiva)
- **Definição Canônica:** A resposta apresenta enunciados cujo conteúdo proposicional é intrinsecamente indeterminado (ambiguidade insolúvel, alternativas mutuamente excludentes sem critério) ou circularmente reflexivo (tautologias vazias: *"A replicação replica porque mantém tudo replicado"*).
- **Evidência Positiva Exigida:** Detecção de construções circulares predicado-sujeito ou cláusulas disjuntivas de indeterminação aberta sem parâmetros.
- **Fronteira com `INSUFFICIENT`:** O candidato tentou construir uma definição ou explicação técnica, mas sua estrutura formal resulta em valor nulo de informação semântica.

---

## 3. Matriz de Autoridade e Resolução de Conflitos entre Componentes

Para o Ciclo 6, a autoridade decisória deve seguir uma cadeia hierárquica imutável com rastreabilidade auditável:

| Nível de Precedência | Componente Responsável | Condição de Ativação | Decisão Final Resultante |
|:---:|---|---|:---:|
| **1 (Veto Absoluto)** | `SemanticDomainDisjunctionEngine` | Disjunção Radical Ontológica Comprovada | `OFF_TOPIC` |
| **2 (Veto de Segurança)** | `PropositionDiscourseFilter` | Antítese Destrutiva Comprovada (sem guarda) | `OFF_TOPIC` |
| **3 (Veto Epistêmico)** | `PropositionDiscourseFilter` | Ignorância Explícita / Evasão / Filler | `INSUFFICIENT` |
| **4 (Veto Lógico)** | `PropositionDiscourseFilter` | Tautologia Circular / Indeterminação Genuína | `UNKNOWN` |
| **5 (Afinidade Contextual)**| `DemandPropositionNexusMatcher` | Entidade Compartilhada sem Mecanismo Operacional | `RELATED` |
| **6 (Papel Instrumental)** | `DemandPropositionNexusMatcher` | Observabilidade / Telemetria Auxiliar | `SUPPORTING` |
| **7 (Decomposição Composta)**| `StrictOntologyRelevanceAggregator` | Satisfaz Parte das Demandas Obrigatórias | `PARTIAL` |
| **8 (Mérito Funcional)** | `StrictOntologyRelevanceAggregator` | Satisfaz Plenamente todas as Demandas | `DIRECT` |

### Regra de Ouro:
**Nenhum componente pode descartar para `OFF_TOPIC` uma resposta que compartilhe a entidade da pergunta.** O fluxo para `OFF_TOPIC` exige validação afirmativa de incompatibilidade ontológica radical.
