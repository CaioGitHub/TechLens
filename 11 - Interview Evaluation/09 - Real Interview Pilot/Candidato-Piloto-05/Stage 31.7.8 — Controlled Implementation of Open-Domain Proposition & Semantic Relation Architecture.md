# Stage 31.7.8 — Controlled Implementation of Open-Domain Proposition & Semantic Relation Architecture

---

## 1. Entry Gate
- **Stage Anterior:** Stage 31.7.7 — Root Cause Analysis & Architecture Redesign for Zero-Lexical & Open-Domain Semantic Intent
- **Gate de Entrada:** `ROOT_CAUSE_ANALYSIS_AND_ARCHITECTURE_REDESIGN_COMPLETE`
- **Condição de Entrada:** Modelo arquitetural aprovado conceituando a cadeia semântica explícita e desativação do acoplamento lexical como critério determinante de relevância.

---

## 2. Baseline Hash & Runtime Integrity
- **Baseline SHA-256 (Entrada do Stage 31.7.8):**
  `A0CFE48B933F587459BFF6AAF8B2BECABA5B7C00C4C87E7B5DDB6BDE985E46A6`
- **Exit SHA-256 (Conclusão do Stage 31.7.8):**
  `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
- **Arquivo Modificado:** [reference_runtime/runtime.py](file:///d:/Projetos/TechLens/reference_runtime/runtime.py)
- **Princípio de Implementação Controlada:** A implementação foi introduzida em paralelo e desacoplada, preservando os contratos do motor legado (`engine="legacy"` default) para proteger o baseline histórico, enquanto expõe a nova arquitetura canônica através de `OpenDomainPropositionEngine`, `evaluate_open_domain_semantic_relevance` e `compare_semantic_engines`.

---

## 3. Architecture Implemented
A cadeia de processamento semanticamente explícita foi materializada no runtime:

```text
Question
   ↓
QuestionIntent (tipo funcional: definition | comparison | diagnosis | implementation | explanation | other)
   ↓
QuestionDemand (demandas atômicas e metas funcionais)
   ↓
QuestionPropositions (sujeito, ação, problema, restrições)
   ↓
ResponsePropositions (extração agnóstica de vocabulário da pergunta)
   ↓
EntityRole (target | context | example | comparison | dependency | incidental | alien)
   ↓
SemanticRelation (DEFINES | EXPLAINS | IMPLEMENTS | MITIGATES | PREVENTS | DIAGNOSES | etc.)
   ↓
AspectCoverage (cobertura atômica de demandas multiaspecto)
   ↓
EpistemicStatus (DEMONSTRATED_EXPERIENCE | CONCEPTUAL | DECLARATION | HYPOTHESIS | UNCERTAINTY | UNKNOWN)
   ↓
SemanticRelevance (DIRECT | PARTIAL | SUPPORTING | RELATED | OFF_TOPIC | INSUFFICIENT | UNKNOWN)
   ↓
Evidence & Rubric
```

A arquitetura opera sem depender de:
- Palavras compartilhadas (shared keywords)
- Stems compartilhados (shared stems)
- Catálogo fechado de tecnologias (catalog independence)
- Dicionários de sinônimos fechados (jargon normalization tables)
- Whitelists de pares tecnológicos ou pares problema-solução

---

## 4. QuestionIntent
O componente `QuestionIntent` extrai o objetivo funcional da pergunta:
- `intent_type`:
  - `definition`: "O que é X?", "Qual o conceito de X?"
  - `comparison`: "Qual a diferença entre X e Y?", "X versus Y"
  - `diagnosis`: "Como investigar picos de latência?", "Quais métricas analisaria?"
  - `implementation`: "Como evitar sobrescritas concorrentes?", "Como implementar X?"
  - `explanation`: "Como o Dragonfly processa requisições?", "Como funciona o Kubernetes?"
  - `other`: questões técnicas gerais
- **Campos Estruturais:** `intent_type`, `goal`, `demands`, `central_entities`, `confidence`, `rationale`.
- **Propriedade:** Responde à pergunta *"O que a pergunta está pedindo que a resposta demonstre?"* e não meramente *"quais palavras estão na pergunta"*.

---

## 5. QuestionDemand
O componente `QuestionDemand` decompõe a pergunta em demandas atômicas e funcionais:
- No caso de perguntas compostas (ex: *"Explique retries com backoff e como a idempotência protege contra duplicidade"*):
  - `demand_1`: Retries com backoff (demanda funcional de resiliência de rede)
  - `demand_2`: Idempotência contra duplicidade (demanda funcional de deduplicação e segurança transacional)
- Cada demanda é avaliada independentemente pelo motor de cobertura de aspectos (`AspectCoverage`).

---

## 6. TechnicalProposition
A abstração `TechnicalProposition` representa proposições técnicas elementares:
- `subject`: componente ou entidade foco
- `action`: operação ou mecanismo executado
- `is_operative`: indica se a proposição expressa ação técnica, transformação de estado ou arquitetura funcional
- `is_experience_declaration`: indica se a proposição apenas declara uso/tempo de carreira sem descrever mecanismo
- `is_alien_domain`: sinaliza proposições fora do domínio de engenharia de software (culinária, hobbies, vida cotidiana)
- `entity_role`: papel da entidade referenciada

---

## 7. Response Proposition Extraction
A extração de proposições da resposta opera sem exigir o vocabulário da pergunta:
- Detecta proposições operativas através de verbos de ação computacional, transformações de estado e configurações estruturais.
- Reconhece explicações funcionais puras sem exigir jargão específico (ex: *"comparo a versão lida antes de salvar e descarto se divergir"* extrai proposição de controle de concorrência com rejeição de escrita obsoleta sem precisar da palavra *optimistic locking*).
- Desconecta o reconhecimento proposicional da presença de entidades cadastradas.

---

## 8. SemanticRelation
O motor de relações semânticas calcula o vínculo funcional estruturado entre a proposição da pergunta e da resposta:
- `DEFINES`: Resposta define a natureza e o propósito do conceito.
- `COMPARES` / `CONTRASTS`: Resposta contrasta propriedades entre dois sujeitos técnicos.
- `MITIGATES` / `PREVENTS`: Resposta neutraliza a condição de falha ou conflito expressa na pergunta.
- `DIAGNOSES` / `MEASURES`: Resposta articula procedimentos de inspeção e métricas de diagnóstico.
- `IMPLEMENTS` / `EXPLAINS`: Resposta articula o mecanismo operativo de execução ou arquitetura interna.
- `THEMATIC_CONTEXT`: Resposta pertence ao mesmo universo técnico, mas não responde à demanda principal.
- `DISJUNCT`: Proposições de universos técnicos completamente incompatíveis.
- `ALIEN_DOMAIN`: Proposição não-técnica.

---

## 9. AspectCoverage
A cobertura de aspectos avalia demandas atômicas individualmente:
- Cobertura Total ($Ratio \ge 0.75$): `DIRECT` (todas as demandas essenciais foram atendidas).
- Cobertura Parcial ($0.0 < Ratio < 0.75$): `PARTIAL` (o candidato cobriu uma parte da pergunta, omitindo outra demanda atômica).
- Cobertura Nula ($Ratio = 0.0$): `RELATED` ou `OFF_TOPIC`.

---

## 10. EntityRole & Entity Anchor
Implementação explícita do princípio da não-autoridade da entidade:
```text
entity presence ≠ semantic relation
```
- **Target:** A entidade é o sujeito principal da pergunta (ex: *"Como funciona o Kubernetes?"*).
- **Context:** A entidade fornece o cenário de execução (ex: *"No meu projeto com Kubernetes, usei optimistic locking no banco"* $\to$ Kubernetes é contexto incidental; a relevância é DIRECT por causa da mitigação de concorrência).
- **Incidental:** Menção de entidade sem mecanismo funcional (ex: *"Eu utilizo Docker e Kubernetes diariamente na empresa"* $\to$ não responde como funciona a arquitetura interna $\to$ RELATED).
- **Alien:** A entidade é mencionada dentro de contexto alienígena (ex: *"Cozinhar lasanha vendo vídeos de Kubernetes"* $\to$ OFF_TOPIC).

---

## 11. EpistemicStatus
Avaliação epistemológica desacoplada da relevância e da correção técnica:
- `DEMONSTRATED_EXPERIENCE`: Candidato articula ações passadas concretas (*"criei partições", "configurei triggers", "implementei"*).
- `CONCEPTUAL`: Candidato articula explicação técnica/definição sem narrativa pessoal (*"é um padrão que...", "funciona particionando os nós"*).
- `DECLARATION`: Mera declaração de senioridade ou uso cotidiano (*"tenho 8 anos de experiência", "uso diariamente"*).
- `HYPOTHESIS`: Especulação (*"acho que talvez dê para criar alguma regra"*).
- `UNCERTAINTY`: Admissão de desconhecimento (*"não lembro", "não sei"*).
- `UNKNOWN`: Estado incerto.

---

## 12. Evidence Mapping
A evidência técnica materializada reflete exclusivamente:
- O que foi funcionalmente demonstrado pela resposta em relação à demanda da pergunta.
- Não é derivada de contagem de palavras-chave ou menções nominais de ferramentas.

---

## 13. Legacy vs Open-Domain Engine Separation
- O motor legado (`_decoupled_evaluate_semantic_relevance` / Step 11) permanece intacto e é invocado por padrão em `_evaluate_semantic_relevance(..., engine="legacy")`.
- O novo motor (`OpenDomainPropositionEngine`) é executado de forma isolada via `evaluate_open_domain_semantic_relevance`.
- O utilitário `compare_semantic_engines(question, response)` permite execução paralela lado a lado para fins de diagnóstico sem contaminar o baseline histórico.

---

## 14. Catalog Independence
- O novo motor executa independentemente do catálogo de tecnologias (`get_technology_catalog()`).
- O catálogo não possui autoridade semântica para forçar ou vetar classificações de relevância.
- Testado e validado em `test_catalog_independence`.

---

## 15. Zero Lexical Overlap
Testado com casos mandatórios onde não há compartilhamento de palavras, stems ou termos tecnológicos entre a pergunta e a resposta:
- Pergunta: *"Como evitar que duas atualizações concorrentes sobrescrevam uma à outra?"*
- Resposta: *"Comparo a versão lida com a versão atual no momento de persistir e descarto se houver divergência."*
- Classificação obtida: `DIRECT` (sem palavras compartilhadas significativas, $len > 4 \le 1$).

---

## 16. Representation Invariance
Validada a equivalência semântica entre:
- Resposta com jargão formal em inglês: *"Implementamos o pattern Saga com compensating transactions para reverter as mutações anteriores."* $\to$ `DIRECT`
- Resposta coloquial em português sem jargão: *"Se der erro no meio do caminho, executo uma rotina que desfaz e cancela tudo que já tinha sido gravado antes."* $\to$ `DIRECT`
- Invariância estrita mantida: $res_{formal} == res_{colloquial}$.

---

## 17. Independent Tests Suite
Criada e executada a suíte independente em [tests/test_stage_31_7_8_open_domain_proposition_engine.py](file:///d:/Projetos/TechLens/tests/test_stage_31_7_8_open_domain_proposition_engine.py), contendo 16 testes cobrindo todos os grupos exigidos:
- **Grupo A — Unseen & Fictional Entities:** Dragonfly, ClickHouse, TiKV, TechNova-X, DataMesh-Z $\to$ `DIRECT`
- **Grupo B — Zero Lexical Overlap:** Concorrência semântica, pressão de memória, thundering herd $\to$ `DIRECT`
- **Grupo C — Representation Invariance:** Jargão formal vs explicação coloquial $\to$ `DIRECT`
- **Grupo D — Entity Roles:** Target vs incidental vs declaration vs alien domain $\to$ `DIRECT` / `RELATED` / `OFF_TOPIC`
- **Grupo E — Definitions:** Circuit Breaker $\to$ `DIRECT` (`intent_type = definition`)
- **Grupo F — Comparisons:** SQL vs NoSQL escalabilidade $\to$ `DIRECT` (`intent_type = comparison`)
- **Grupo G — Causal Problems:** Contenção de locks transacionais $\to$ `DIRECT` (`intent_type = implementation`)
- **Grupo H — Diagnostics:** Picos de latência $\to$ `DIRECT` (`intent_type = diagnosis`)
- **Grupo I — Multi-Aspect:** Retries + Backoff + Idempotência (cobertura total $\to$ `DIRECT`, parcial $\to$ `PARTIAL`)
- **Grupo J — Epistemology:** Demonstração (`DEMONSTRATED_EXPERIENCE`) vs Declaração (`DECLARATION`) vs Hipótese (`HYPOTHESIS`)
- **Grupo K — UNKNOWN / Ambiguous:** Respostas vazias/vagas $\to$ `UNKNOWN` / `INSUFFICIENT`
- **Grupo L — Semantic Mutations:** Mecanismo oposto / alien domain com mesmas palavras superficiais $\to$ sensibilidade comprovada
- **Grupo Independente:** Deadlocks, Gossip Protocol, Dead Letter Queue (DLQ)
- **Resultado:** 16/16 testes passaram (100% de sucesso).

---

## 18. Mutation Testing
O motor demonstrou sensibilidade a mutações semânticas:
- Resposta válida de concorrência com versionamento: `DIRECT`
- Mutação alienígena (*"verifico o saldo pessoal antes de almoçar"*): revertida para `OFF_TOPIC`
- Mutação de mecanismo oposto (*"removo travas e deixo threads escreverem sem versão"*): classificada de acordo com a proposição contrária.

---

## 19. Regression & Historical Verification
Execução completa da suíte de regressão do runtime e do Reference Harness:
- **Runtime Tests:**
  `Ran 1005 tests in 43.176s`
  `OK (skipped=1)`
  `1005 passed, 0 failed, status: PASS` (989 históricos + 16 novos testes do Stage 31.7.8)
- **Reference Harness:**
  `REFERENCE HARNESS: PASS_WITH_WARNINGS (8/8 suites, 0 failed)`
  `WARNINGS: BLOCKED, PASS_WITH_WARNING`
- **Regressão:** Zero regressões em todo o histórico.

---

## 20. Determinism
- Testado com 20 execuções consecutivas para a mesma entrada em `test_engine_determinism`.
- Classificação, coberturas de aspectos e razões numéricas mantiveram determinismo estrito de 100%.

---

## 21. Comparison (Legacy vs Open-Domain Engine)
O utilitário `compare_semantic_engines(question, response)` foi validado:
- Executa ambos os motores em paralelo.
- Em casos de zero lexical overlap (ex: sobrescritas concorrentes vs comparação de versão antes de gravar), o motor legado reportava `OFF_TOPIC` (ou dependia de fallbacks de stem fracos), enquanto o motor de domínio aberto reporta `DIRECT` com fundamentação em proposições operativas.
- A comparação serve como ferramenta de diagnóstico e auditoria sem alterar os resultados históricos.

---

## 22. Known Limitations & Warnings
1. **Coexistência de Motores:** O motor legado (`_decoupled_evaluate_semantic_relevance`) e o Step 11 ainda permanecem no runtime como padrão para garantir compatibilidade histórica até que a validação cega independente formal ocorra.
2. **Gramática e Vocabulário Operativo:** A extração de proposições em português e inglês baseia-se em heurísticas estruturais de predicados operacionais e marcadores funcionais. Estruturas frasais elípticas ou extremamente fragmentadas ainda podem requerer refinamento de parsing.
3. **Validação Cega Pendente:** Esta etapa é estritamente de implementação e testes de unidade controlados. A validação formal de generalização semântica deverá ocorrer em etapa subsequente com benchmark cego e oráculo humano independente.

---

## 23. Gate
```text
GATE:
CONTROLLED_IMPLEMENTATION_COMPLETE_WITH_WARNINGS
```

---

## 24. Next Stage
- **Stage 31.7.9 — Blind Revalidation of Open-Domain Proposition Architecture:**
  Execução cega independente com 250+ novos casos não vistos, tecnologias inéditas e oráculo humano para avaliar se a taxa de concordância supera a barreira do Stage 31.7.6 antes da autorização para remoção definitiva do motor legado.
