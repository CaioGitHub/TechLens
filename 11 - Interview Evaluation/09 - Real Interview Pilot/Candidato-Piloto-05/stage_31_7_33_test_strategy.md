# Stage 31.7.33 — Estratégia de Testes em Nove Camadas (Ciclo 6)

## 1. Visão Geral da Arquitetura de Testes

A validação da implementação do Ciclo 6 fundamenta-se em uma estratégia piramidal rigorosa dividida em **nove camadas concêntricas de teste**. A passagem em testes unitários ou em baterias sintéticas não substitui a conformidade com as salvaguardas canônicas de regressão nem a auditoria causal de rastreabilidade.

---

## 2. As Nove Camadas de Teste

### Camada 1 — Testes Unitários de Componentes
- **Escopo:** Verificação isolada de cada classe e função implementada nos incrementos (`QuestionProfileExtractor`, `DiscourseSegmentationEngine`, `ThematicAffinityEngine`, `ConceptualEquivalenceEngine`, `AnalogyResolutionEngine`, `StrictRelevanceAggregator`).
- **Critério:** Cobertura de ramos lógicos, tratamento de entradas nulas/vazias, determinismo estrito de execução.

### Camada 2 — Testes Contratuais Formais (35 Contratos)
- **Escopo:** Execução automatizada dos 35 contratos semânticos catalogados em [`stage_31_7_31_contract_counterexample_matrix.json`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_31_contract_counterexample_matrix.json) e auditados em [`stage_31_7_32_contract_audit.json`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_32_contract_audit.json).
- **Critério:** 35/35 (100%) de aprovação sem nenhuma exceção por caso.

### Camada 3 — Testes de Integração de Pipeline
- **Escopo:** Verificação da propagação de dados ao longo do pipeline $1 \to 2 \to 3 \to 4 \to 5 \to 6 \to 7$.
- **Critério:** Ausência de perdas de evidências intermediárias; confirmação de que o status transitório `EQUIVALENCE_PENDING` do Estágio 3 é consumido e resolvido pelo Estágio 4.

### Camada 4 — Testes Adversariais de Fronteira (15 Cenários)
- **Escopo:** Execução dos 15 cenários de estresse definidos em [`stage_31_7_32_adversarial_counterexamples.json`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_32_adversarial_counterexamples.json).
- **Critério:**
  - Homonímia alienígena (ADV-01) $\to$ `OFF_TOPIC`;
  - Equivalência aberta sem token literal (ADV-02) $\to$ `DIRECT`;
  - Elogio vazio com tecnologia (ADV-03) $\to$ `INSUFFICIENT`;
  - Preâmbulo conversacional com núcleo técnico (ADV-05) $\to$ `DIRECT`;
  - Analogia aterrisada (ADV-07) $\to$ `DIRECT` vs analogia desancorada (ADV-08) $\to$ `INSUFFICIENT`;
  - Contradição aparente reconciliada (ADV-13) $\to$ `DIRECT` vs contradição destrutiva (ADV-12) $\to$ `INSUFFICIENT`.

### Camada 5 — Testes de Invariância Semântica
- **Escopo:** Verificação de que transformações na forma discursiva que preservam o significado mantêm a classificação estável:
  - Paráfrase e sinonímia;
  - Reordenação de períodos oracionais;
  - Resposta concisa vs prolixa com o mesmo conteúdo;
  - Presença de preâmbulo fático inofensivo;
  - Ausência do termo literal quando o mecanismo é elucidado.
- **Critério:** 100% de consistência pareada nas permutações.

### Camada 6 — Testes de Não-Invariância Semântica
- **Escopo:** Verificação de que alterações sutis que modificam o valor de verdade ou a cobertura da resposta alteram legitimamente a classificação:
  - Inserção de operador de negação $\to$ altera verdade/política;
  - Remoção de cláusula condicional restritiva $\to$ generalização indevida;
  - Substituição de mecanismo operacional por juízo afetivo $\to$ `DIRECT` cai para `INSUFFICIENT`;
  - Omissão de demanda secundária obrigatória $\to$ `DIRECT` cai para `PARTIAL`.
- **Critério:** O motor deve detectar a mudança e rebaixar a classe sem inércia classificatória.

### Camada 7 — Regressão Canônica e Reference Harness
- **Escopo:** Execução integral da suíte de testes existente do projeto:
  - Suíte Canônica: `py -3 -m unittest discover -s tests -p "test_*.py"` (1.047 testes; meta: 1.046 OK, 1 skipped, 0 falhas);
  - Reference Harness: `py -3 -m unittest tests.test_stage_26_reference_harness` (15 testes; meta: 15/15 OK).
- **Critério:** ZERO tolerância a regressão. Qualquer quebra bloqueia imediatamente a progressão do incremento.

### Camada 8 — Testes de Rastreabilidade Causal do Schema JSON
- **Escopo:** Validação estrutural e semântica do registro `EvidenceTraceabilityRecord` emitido para cada predição.
- **Critério:**
  - Validação estrita contra [`stage_31_7_31_evidence_traceability_schema.json`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_31_evidence_traceability_schema.json);
  - Auditor independente deve conseguir justificar a decisão final examinando exclusivamente os campos estruturados do JSON (demandas, proposições, nexos, refutações, coberturas e regras formais), sem depender de resumos em prosa.

### Camada 9 — Validação Independente Futura (Duplo-Cego)
- **Escopo:** Processo externo de validação com novos casos de candidatos reais não vistos durante o desenvolvimento.
- **Critério:** Manutenção estrita da ressalva `REFERENCE_INDEPENDENCE_UNRESOLVED` até a conclusão desta etapa.
