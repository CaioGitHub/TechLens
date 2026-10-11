# Stage 31.7.11 — Controlled Implementation of Demand-Proposition Nexus Architecture

---

## 1. Objetivo

Implementar de forma controlada a arquitetura definida no Stage 31.7.10, estabelecendo uma avaliação semântica baseada na relação funcional entre as demandas de uma pergunta técnica e as proposições presentes na resposta.

A implementação visa corrigir estruturalmente os 88 falsos positivos de relevância (`DIRECT`) identificados no Stage 31.7.9, eliminando a heurística de proxy de tamanho de resposta (`len(r_words) >= 8`) e a promoção permissiva de operatividade sem nexo funcional com a demanda, sem introduzir novas heurísticas permissivas, vocabulários fechados ou regras específicas para casos históricos.

O motor responde à questão central:
> *A resposta fornece evidências semanticamente pertinentes de que atende, atende parcialmente, contribui para ou não atende às demandas técnicas da pergunta?*

Esta etapa implementa e isola a arquitetura no runtime de referência. A validação cega independente e a decisão de substituir o comportamento de referência legado permanecem reservadas para etapas posteriores (Stage 31.7.12).

---

## 2. Baseline e Integridade

- **Gate de Entrada:** `ROOT_CAUSE_ANALYSIS_AND_ARCHITECTURE_REDESIGN_COMPLETE` (Stage 31.7.10).
- **Runtime sob Implementação:** [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py).
- **Expected Entry Hash (SHA-256):**
  `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
- **Actual Entry Hash (SHA-256):**
  `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
- **Integridade Pré-Implementação:** **100% CONFIRMADA**. Sem divergências de hash antes do início das modificações autorizadas.

```yaml
stage: "31.7.11"

baseline:
  expected_hash: "2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E"
  actual_hash: "2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E"
  integrity_verified: true

implementation:
  target: "reference_runtime/runtime.py"
  legacy_behavior_preserved: true
  isolated_invocation_available: true

pre_implementation_diagnosis:
  confirmed_root_causes:
    - "Atribuição de operatividade por proxy de comprimento (len(r_words) >= 8) sem mecanismo funcional real."
    - "Promoção incondicional de qualquer proposição considerada operativa para DIRECT com cobertura 1.0 (aspect_coverage.ratio = 1.0)."
    - "Ausência de avaliação relacional par-a-par entre demanda e proposição técnica (Demand-Proposition Nexus)."
    - "Agrupamento indiferenciado de contribuições auxiliares de observabilidade (SUPPORTING) e menções de ecossistema (RELATED) sob DIRECT."
    - "Desconsideração de polaridade funcional e antitheses operacionais destrutivas."
  unconfirmed_hypotheses: []
  blockers: []
```

---

## 3. Diagnóstico Inicial Confirmado

A inspeção factual do código-fonte legado em `OpenDomainPropositionEngine` (linhas 2850 a 3163) confirmou os diagnósticos formulados no Stage 31.7.10:

1. **Proxy de Comprimento em `extract_response_propositions`:**
   ```python
   # Código anterior (Stage 31.7.8):
   is_operative = len(r_words) >= 5 and (has_operative_mechanism or len(r_words) >= 8)
   ```
   Qualquer resposta técnica com 8 ou mais palavras era declarada `is_operative = True`, mesmo sendo jargão desconexo, narrativa biográfica, tautologia vazia ou alheia à demanda.

2. **Atalho Permissivo para `DIRECT` em `evaluate_relevance`:**
   ```python
   # Código anterior (Stage 31.7.8):
   if prop.is_operative:
       return {
           "classification": "DIRECT",
           "relation_type": "open_domain_mechanism_assertion",
           "functional_contribution": True,
           "aspect_coverage": {"ratio": 1.0, "status": "FULL"},
           ...
       }
   ```
   Uma vez declarada operativa pelo tamanho, a resposta recebia `DIRECT` e cobertura 1.0 sem verificar se o mecanismo satisfazia a demanda da pergunta.

3. **Confusão entre Declaração de Experiência e Demonstração:**
   Respostas contendo substantivos técnicos da pergunta (ex: "particionamento") eram tratadas como contendo mecanismo operativo, obscurecendo a distinção epistemológica exigida pela regra 27 de `AGENTS.md`.

---

## 4. Arquitetura Implementada

A implementação materializou as cinco responsabilidades do redesenho arquitetural do Stage 31.7.10:

```text
Question
   ↓
[1. Question Demand Decomposition]
   → QuestionIntent (intent_type, primary_entity, goal)
   → QuestionDemand (demand_id, target_subject, target_problem, expected_polarity="SOLVE")
   ↓
Response
   ↓
[2. Response Proposition Extraction]
   → TechnicalProposition (eliminado length proxy; validação de mecanismos operativos ou ações funcionais com efeitos e restrições)
   ↓
[3. Demand-Proposition Nexus Assessment]
   → Pairwise evaluation (Demand × Proposition)
   → Relações: FUNCTIONALLY_SOLVES | CONTRIBUTES_TO | THEMATICALLY_ADJACENT | ANTITHESIS_OPPOSED | DOMAIN_DISJUNCT | UNKNOWN | INSUFFICIENT
   ↓
[4. Demand Coverage Aggregator]
   → Multi-aspect demand ratio, essenciais preservadas, mapeamento semântico
   ↓
[5. Decoupled Epistemic Assessment]
   → EpistemicEvaluation (DEMONSTRATED_EXPERIENCE | CONCEPTUAL | DECLARATION | HYPOTHESIS | UNCERTAINTY | UNKNOWN)
   ↓
Canonical Result Object
```

### Contratos das Relações de Nexus:
- **`FUNCTIONALLY_SOLVES`:** Mecanismo técnico e operativo que resolve funcionalmente o problema ou atende à demanda da pergunta. Gera `DIRECT` (ou compõe `PARTIAL` em perguntas multiaspecto).
- **`CONTRIBUTES_TO`:** Proposição que fornece suporte auxiliar de observabilidade, telemetria ou monitoramento, mas não implementa a mitigação causal direta da falha. Gera `SUPPORTING`.
- **`THEMATICALLY_ADJACENT`:** Proposição que cita a tecnologia ou ecossistema correto, declara experiência sem demonstração, relata hardware/trivia histórica ou apresenta tautologias circulares sem mecanismo funcional. Gera `RELATED`.
- **`ANTITHESIS_OPPOSED`:** Proposição que preconiza ação que desativa proteções fundamentais (ex: remover todos os locks, desativar transações ACID, desligar circuit breaker) sem justificativa diagnóstica contextual. Gera `OFF_TOPIC`.
- **`DOMAIN_DISJUNCT`:** Proposição pertencente a domínio técnico ortogonal (ex: CSS Grid/estilização frontend para resolver concorrência de saldo em banco; esteira de CI/CD para otimizar query SQL) ou domínio não computacional (vida cotidiana, culinária, esportes). Gera `OFF_TOPIC`.
- **`UNKNOWN` / `INSUFFICIENT`:** Proposição evasiva, vazia ou confirmação conversacional rasa ("sim, com certeza"). Preserva incerteza sem forçar `DIRECT` ou `OFF_TOPIC`.

---

## 5. Componentes Criados ou Reutilizados

### 5.1 Novos Modelos de Dados (Dataclasses)
- [`DemandPropositionNexus`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py#L1647-L1655):
  ```python
  @dataclass(frozen=True)
  class DemandPropositionNexus:
      demand_id: str
      proposition_idx: int = 0
      nexus_relation: str = "UNKNOWN"
      rationale: str = ""
      evidence_span: str = ""
      uncertainty: str = "LOW"
  ```
- **Extensões de Modelos Existentes:**
  - `QuestionDemand`: adicionado `expected_polarity: str = "SOLVE"`.
  - `TechnicalProposition`: adicionados flags estruturais (`is_antithesis`, `is_frontend`, `is_devops`, `is_auxiliary`, `is_trivia`, `is_evasive`, `is_ignorance`, `is_filler`) e `action_polarity: str = "ENABLE"`.

### 5.2 Refatoração de `OpenDomainPropositionEngine`
- `__init__`: marcadores léxicos abertos agrupados funcionalmente (alienígenas, ortogonais, antitéticos, auxiliares, trivia, evasivos e ações funcionais).
- `decompose_question`: particiona perguntas multiaspecto em demandas atômicas (`demand_1`, `demand_2`, etc.) e define `expected_polarity`.
- `extract_response_propositions`: extrai proposições técnicas eliminando qualquer proxy de contagem de palavras.
- `assess_demand_nexus`: avalia formalmente a relação relacional par-a-par (demanda vs proposição).
- `evaluate_epistemic_status`: classifica o estatuto epistemológico de forma desacoplada da pertinência técnica.
- `evaluate_relevance` / `evaluate`: agrega a cobertura e orquestra a classificação final com explicabilidade e rastreabilidade completas.

---

## 6. Contratos e Interfaces

A interface canônica de retorno de `evaluate_open_domain_semantic_relevance` foi preservada e enriquecida:

```json
{
  "classification": "DIRECT | PARTIAL | SUPPORTING | RELATED | OFF_TOPIC | INSUFFICIENT | UNKNOWN",
  "relation_type": "open_domain_mechanism_assertion | auxiliary_observability_support | thematic_adjacency_without_mechanism | destructive_antithesis_assertion | domain_disjunct_assertion | ...",
  "functional_contribution": true | false,
  "question_intent": {
    "type": "definition | comparison | diagnosis | implementation | explanation | other",
    "primary_entity": "string"
  },
  "question_demands": [
    {"id": "demand_1", "subject": "string"}
  ],
  "aspect_coverage": {
    "ratio": 1.0,
    "status": "FULL | PARTIAL | SUPPORTING_ONLY | RELATED_ONLY | NONE | UNKNOWN"
  },
  "epistemic_status": {
    "status": "DEMONSTRATED_EXPERIENCE | CONCEPTUAL | DECLARATION | HYPOTHESIS | UNCERTAINTY | UNKNOWN",
    "is_demonstrated": true | false
  },
  "demand_nexus": [
    {
      "demand_id": "demand_1",
      "nexus_relation": "FUNCTIONALLY_SOLVES",
      "rationale": "Operative technical proposition functionally addresses the demand."
    }
  ],
  "confidence": "HIGH | MEDIUM",
  "rationale": "string",
  "needs_review": false
}
```

---

## 7. Estratégia de Isolamento

- **Proteção do Caminho Legado:** O runtime canônico [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py) mantém o motor legado como padrão incondicional para chamadas do pipeline histórico:
  ```python
  def _evaluate_semantic_relevance(question, response, engine="legacy"):
      if engine == "open_domain":
          return evaluate_open_domain_semantic_relevance(question, response)
      return _decoupled_evaluate_semantic_relevance(question, response)
  ```
- **Invocação Canônica Isolada:** A nova arquitetura é explicitamente invocada via `evaluate_open_domain_semantic_relevance` ou instanciando `OpenDomainPropositionEngine()`.
- **Comparador Diagnóstico Disponível:** A função `compare_semantic_engines(question, response)` permite inspeção comparativa lado a lado entre ambos os motores sem efeitos colaterais.

---

## 8. Alterações Realizadas

1. **Dataclasses (linhas 1600–1677):**
   Adicionado `expected_polarity` em `QuestionDemand`, `action_polarity` e flags analíticos em `TechnicalProposition`, e criação de `DemandPropositionNexus`.
2. **OpenDomainPropositionEngine (linhas 2870–3190):**
   Substituição completa do motor provisório do Stage 31.7.8 pela arquitetura formal Demand-Proposition Nexus.
3. **Eliminação do length proxy:**
   Removida a regra `len(r_words) >= 8`. A operatividade agora requer mecanismo técnico explícito ou ação funcional contextual com efeitos/restrições.
4. **Resolução de Falsos Positivos:**
   Cadeia de avaliação de nexus isolando domínios ortogonais (`DOMAIN_DISJUNCT`), antitheses destrutivas (`ANTITHESIS_OPPOSED`), observabilidade auxiliar (`CONTRIBUTES_TO`), trivialidades/declarações sem mecanismo (`THEMATICALLY_ADJACENT`), e carência probatória (`UNKNOWN`/`INSUFFICIENT`).

---

## 9. Arquivos Modificados e Criados

- **Modificado:**
  - [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py)
- **Criado:**
  - [`tests/test_stage_31_7_11_demand_proposition_nexus.py`](file:///d:/Projetos/TechLens/tests/test_stage_31_7_11_demand_proposition_nexus.py) (Suíte de testes de contrato cobrindo Categorias A a H)

---

## 10. Hashes Antes e Depois

- **SHA-256 Antes (Baseline de Entrada):**
  `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
- **SHA-256 Depois (Código Implementado):**
  `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E`

---

## 11. Testes Contratuais

Foi desenvolvida e executada a suíte de testes contratuais [`tests/test_stage_31_7_11_demand_proposition_nexus.py`](file:///d:/Projetos/TechLens/tests/test_stage_31_7_11_demand_proposition_nexus.py), cobrindo rigorosamente as 8 categorias exigidas pela especificação:

| Categoria | Propriedade Contratual Verificada | Resultado |
| :--- | :--- | :---: |
| **A. Atendimento Direto** | Reconhecimento de `FUNCTIONALLY_SOLVES` → `DIRECT` em tecnologias inéditas, domínios abertos e zero-lexical. | **PASS** |
| **B. Falsos Positivos** | Rejeição de sopas de jargão (buzzwords), domínios alienígenas e domínios técnicos ortogonais (CSS para concorrência; CI/CD para SQL). Proibição de promoção a `DIRECT`. | **PASS** |
| **C. Supporting vs Related** | Separação estrita entre observabilidade auxiliar (`SUPPORTING`) e menção de tecnologia sem mecanismo (`RELATED`). | **PASS** |
| **D. Multiaspecto** | Decomposição atômica de demandas. Cobertura completa → `DIRECT`; omissão de aspectos essenciais (ex: idempotência) → `PARTIAL`. | **PASS** |
| **E. Polaridade e Contexto** | Detecção de ações destrutivas (remoção de locks e transações ACID) como `ANTITHESIS_OPPOSED` → `OFF_TOPIC`. | **PASS** |
| **F. Epistemologia Desacoplada** | Separação entre declaração de experiência (`DECLARATION` → `RELATED`), hipótese (`HYPOTHESIS`) e experiência demonstrada (`DEMONSTRATED_EXPERIENCE` → `DIRECT`). | **PASS** |
| **G. Invariância de Representação** | Equivalência semântica estrita sob variações de estilo, formalidade, prolixidade e tecnologias inventadas/fictícias. | **PASS** |
| **H. Limites de Inferência** | Preservação de `UNKNOWN` para respostas evasivas e `INSUFFICIENT` para declarações de ignorância ou filler, sem forçar classificações arbitrárias. | **PASS** |

### Execução da Suíte Contratual:
```text
py -m unittest tests/test_stage_31_7_11_demand_proposition_nexus.py
Ran 8 tests in 0.003s
OK
```

Adicionalmente, a suíte de testes unitários do Stage 31.7.8 foi executada e aprovada sem falhas:
```text
py -m unittest tests/test_stage_31_7_8_open_domain_proposition_engine.py
Ran 16 tests in 0.017s
OK
```

---

## 12. Testes de Regressão

Executou-se a suíte canônica completa de regressão do repositório:

```text
py run_reference_runtime_tests.py
```

### Resultado da Regressão:
- **Total de Testes:** 1013 (incluindo os novos testes contratuais)
- **Aprovados:** 1013
- **Falhas:** 0
- **Erros:** 0
- **Ignorados (skipped):** 1
- **Status:** **PASS** (100% de aprovação)

Nenhuma funcionalidade existente, contrato de stage histórico ou baseline de referência foi afetado negativamente.

---

## 13. Resultado do Reference Harness

Executou-se o Reference Harness determinístico:

```text
py run_reference_harness.py
```

### Resultado:
- **Suítes Planejadas:** 8
- **Suítes Executadas:** 8
- **Suítes Falhas:** 0
- **Status:** `REFERENCE HARNESS: PASS_WITH_WARNINGS (8/8 suites, 0 failed)`
- **Avisos do Harness:** `WARNINGS: BLOCKED, PASS_WITH_WARNING` (avisos canônicos documentados decorrentes dos gates históricos de calibração humana mantidos congelados na base).

---

## 14. Comparação Diagnóstica com o Legado

A execução do comparador `compare_semantic_engines` demonstra que a nova arquitetura corrige pontualmente os falsos positivos sem comprometer o atendimento legítimo:

1. **Caso "Buzzword Soup" (Frontend/DevOps para Concorrência):**
   - *Pergunta:* "Como mitigar race conditions em saldo compartilhado?"
   - *Resposta:* "Utilizamos Kubernetes com Istio e pods escaláveis com alta resiliência e esteira de microsserviços modernos na nuvem."
   - *Legado Decoupled (31.7.5):* `OFF_TOPIC` (rejeitado por ausência de conceitos).
   - *Motor Provisório (31.7.8):* `DIRECT` (falso positivo gerado pelo proxy de comprimento).
   - *Novo Motor (31.7.11):* `OFF_TOPIC` (`relation_type: domain_disjunct_assertion`, nexus: `DOMAIN_DISJUNCT`). **Corrigido com sucesso**.

2. **Caso "Auxiliary Observability" (Prometheus/Grafana para Incidente):**
   - *Pergunta:* "Como você investigaria e conteria picos anômalos de latência na aplicação?"
   - *Resposta:* "Adiciono métricas no Prometheus e crio alertas no Grafana para monitorar quanto tempo cada requisição demora."
   - *Motor Provisório (31.7.8):* `DIRECT` (falso positivo gerado por operatividade genérica).
   - *Novo Motor (31.7.11):* `SUPPORTING` (`relation_type: auxiliary_observability_support`, nexus: `CONTRIBUTES_TO`). **Corrigido com sucesso**.

3. **Caso "Destructive Antithesis" (Remover Locks):**
   - *Pergunta:* "Como resolver concorrência de escritas e deadlocks em transações financeiras?"
   - *Resposta:* "Para resolver isso, desativo todos os locks do banco e desabilito transações ACID para escrever direto sem travar."
   - *Motor Provisório (31.7.8):* `DIRECT` (falso positivo por conter palavras operativas).
   - *Novo Motor (31.7.11):* `OFF_TOPIC` (`relation_type: destructive_antithesis_assertion`, nexus: `ANTITHESIS_OPPOSED`). **Corrigido com sucesso**.

---

## 15. Casos que Continuam Falhando e Casos Limítrofes

Não foram detectadas falhas nas suítes contratuais ou na regressão canônica. Entretanto, foram identificados casos limítrofes metodológicos:
1. **Desativação Temporária Diagnóstica:** Se uma resposta propor desativar um mecanismo temporariamente em ambiente isolado estritamente para reprodução de um bug, o classificador sintático de antítese pode classificar como `ANTITHESIS_OPPOSED` a menos que a proposição contenha qualificadores contextuais claros de diagnóstico em laboratório.
2. **Perguntas com Mais de 3 Aspectos Compostos:** A decomposição de demandas atual trata eficientemente até 2 aspectos primários por conectivos. Casos com 4 ou 5 demandas emaranhadas exigirão validação específica de granularidade no Stage 31.7.12.

---

## 16. Limitações e Riscos

1. **Não Substituição Automática:** O motor implementado não substitui o caminho padrão do runtime de produção. Ele permanece isolado e opcional via parâmetro explícito `engine="open_domain"`.
2. **Ausência de Validação Cega:** Esta etapa é estritamente de implementação e verificação de contratos. Nenhuma validação cega independente foi executada ou declarada concluída nesta etapa.
3. **Escopo Semântico Simbólico:** A arquitetura continua estritamente determinística e simbólica, sem uso de embeddings proprietários, LLMs em runtime ou chamadas de rede.

---

## 17. Critérios de Aceite Verificados

- [x] **1. Integridade inicial confirmada:** Baseline hash `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E` verificado.
- [x] **2. Isolamento e invocação explícita:** Novo motor acessível via `evaluate_open_domain_semantic_relevance` e `engine="open_domain"`.
- [x] **3. Caminho legado preservado:** `engine="legacy"` mantido como default inalterado.
- [x] **4. Proposição não implica DIRECT:** Testado e comprovado em múltiplas classes de teste.
- [x] **5. Tamanho da resposta não determina pertinência:** Eliminado o proxy `len(r_words) >= 8`.
- [x] **6. Relação funcional avaliada explicitamente:** Pairwise `DemandPropositionNexus` implementado.
- [x] **7. Cobertura verificada por demanda:** Suporte a tracking atômico de demandas implementado.
- [x] **8. Demandas essenciais não ignoradas:** Omissão de aspectos essenciais resulta em `PARTIAL`.
- [x] **9. Contratos distintos entre SUPPORTING e RELATED:** Observabilidade auxiliar gera `SUPPORTING`; citações de tecnologia sem mecanismo geram `RELATED`.
- [x] **10. Polaridade contextual avaliada:** Proposições destrutivas geram `ANTITHESIS_OPPOSED` / `OFF_TOPIC`.
- [x] **11. Epistemologia separada da pertinência:** `EpistemicEvaluation` desacoplado da relevância técnica.
- [x] **12. Incerteza não convertida em DIRECT/OFF_TOPIC:** Preservados `UNKNOWN` e `INSUFFICIENT`.
- [x] **13. Justificativas rastreáveis:** Todos os nós de decisão registram `rationale` e `nexus_relation`.
- [x] **14. Sem regras ad hoc para casos históricos:** Nenhuma regra acoplada aos 101 casos do Stage 31.7.9.
- [x] **15. Testes contratuais executados:** 8/8 classes contratuais aprovadas.
- [x] **16. Suíte canônica de regressão executada:** 1013/1013 testes aprovados (`PASS`).
- [x] **17. Reference Harness executado:** 8/8 suítes aprovadas (`PASS_WITH_WARNINGS`).
- [x] **18. Hashes e arquivos documentados:** Mapeados e registrados.
- [x] **19. Nenhuma validação cega declarada:** Validação cega reservada formalmente para o Stage 31.7.12.
- [x] **20. Limitações explicitadas:** Registradas na seção 16.

---

## 18. Critérios Não Verificados

- **Substituição definitiva do motor legado:** Reservada para após conclusão bem-sucedida de validação cega independente.
- **Validação cega independente:** Reservada formalmente para o Stage 31.7.12.

---

## 19. Atualizações de Governança

- Atualizado `START_HERE.md` com o gate do Stage 31.7.11, o novo hash de runtime e o estado do motor.
- Atualizado `GEMINI_HANDOFF.md` documentando a implementação controlada da arquitetura Demand-Proposition Nexus e a preparação para o Stage 31.7.12.

---

## 20. Gate Final

```text
CONTROLLED_DEMAND_PROPOSITION_IMPLEMENTATION_COMPLETE
```

A arquitetura definida no Stage 31.7.10 está plenamente materializada, isolada, verificada contratualmente e aprovada em toda a suíte de regressão canônica e harness de referência.

---

## 21. Próxima Etapa Recomendada

**Stage 31.7.12 — Independent Contract Validation and Blind Semantic Revalidation Design**

*Nota de governança: O Stage 31.7.12 não deve ser iniciado automaticamente. A substituição do motor legado só poderá ser avaliada após a execução e aprovação de revalidação cega independente.*
