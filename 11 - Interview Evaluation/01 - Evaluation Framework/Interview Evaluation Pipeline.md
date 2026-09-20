---
type: reference
status: understood
confidence: 100
created: 2026-09-20
updated: 2026-09-20
tags:
  - interview-evaluation
  - pipeline
  - orchestration
  - meta
---
# Etapa 24 — Interview Evaluation Pipeline

Esta nota define a orquestração canônica do pipeline de avaliação técnica de entrevistas. A Orchestration encadeia artefatos existentes, valida pré-condições, transporta saídas, propaga estados e preserva rastreabilidade.

Ela **não** cria lógica concorrente de transcrição, evidência, pontuação, agregação ou decisão de contratação.

## 1. Princípio fundamental

Cada etapa possui uma responsabilidade delimitada:

```text
20.x Transcription Processing
    ↓ estrutura e valida a entrevista
21 — Evidence Model
    ↓ estrutura o que foi demonstrado
22 — Rubric 0–10
    ↓ define critérios e escala
23 — Evaluation Engine
    ↓ produz avaliações individuais
Interview Evaluation Model / Report
    ↓ consolida e persiste o resultado
```

A Orchestration responde:

> Qual etapa deve ser executada, com qual entrada, qual saída produzida e em que condições o pipeline pode avançar?

Ela não responde o que o candidato sabe. Essa responsabilidade pertence às etapas de evidência e avaliação.

## 2. Pipeline canônico

```text
RAW TRANSCRIPT
      ↓
20.1 Participant Identification
      ↓
20.2 Speaker Attribution
      ↓
20.3 Question Extraction
      ↓
20.4 Response Extraction
      ↓
20.5 Reconstruction & Normalization
      ↓
20.6 Question/Response Linking
      ↓
20.7 Validation
      ↓
STRUCTURED INTERVIEW
      ↓
21 — Evidence Model
      ↓
EVIDENCE SET
      ↓
22 — Rubric 0–10
      ↓
23 — Evaluation Engine
      ↓
EVALUATIONS
      ↓
Interview Evaluation Model
      ↓
FINAL INTERVIEW REPORT
      ↓
11 - Interview Evaluation/06 - Reports/
```

A ordem não deve ser alterada sem uma dependência documentada. A Rubrica fornece regras; ela não é uma etapa que processa diretamente o transcript.

## 3. Responsabilidade e limites da Orchestration

A Orchestration deve:

1. verificar a disponibilidade e o estado da entrada;
2. executar ou encaminhar cada estágio na ordem correta;
3. validar os gates de saída;
4. transportar artefatos sem reinterpretar seu conteúdo;
5. propagar `status`, `warnings`, `blockers`, `needs_review` e campos de confiança;
6. impedir avanço quando uma pré-condição crítica falhar;
7. manter os IDs e as fontes originais;
8. identificar artefatos downstream potencialmente desatualizados;
9. registrar o estado final do pipeline;
10. encaminhar avaliações concluídas ao mecanismo existente de relatório.

A Orchestration não deve:

- identificar participantes, speakers, perguntas ou respostas;
- reconstruir transcript;
- criar, corrigir ou classificar evidências;
- calcular score, pesos, média ou confidence de avaliação;
- converter `missing`, `unknown` ou `needs_review` em evidência negativa;
- inferir senioridade, potencial ou contratação;
- alterar a Rubrica, o Evidence Model ou o Evaluation Engine;
- recalcular avaliações durante a geração do relatório;
- apagar artefatos anteriores durante reprocessamento.

## 4. Contrato global de estado

Quando um estado de execução for necessário, reutilizar o objeto de pipeline abaixo. Ele representa estado operacional, não qualidade ou senioridade do candidato.

```yaml
pipeline:
  id: ""
  status: NOT_STARTED
  current_stage: ""
  completed_stages: []
  warnings: []
  blockers: []
  failed_stage: null
  affected_artifacts: []
  candidate: null
  readiness: null
```

Estados permitidos:

```text
NOT_STARTED
IN_PROGRESS
READY_WITH_WARNINGS
READY
BLOCKED
```

`readiness` deve representar somente prontidão estrutural. Não criar `seniority_score`, `hiring_score`, `approval_score` ou qualquer métrica equivalente.

Se já existir uma implementação com nomes equivalentes, os nomes existentes prevalecem; o contrato semântico não muda.

## 5. Handoffs do Stage 20

### 5.1 20.1 → 20.2

```text
Entrada: transcript bruto + participantes identificados
Saída: identificação de participantes disponível para atribuição de speakers
```

O Speaker Attribution reutiliza `participant_id`, `role`, `identification_confidence`, `needs_review` e `review_reason`. O pipeline não resolve ambiguidades por conta própria.

### 5.2 20.2 → 20.3

```text
Entrada: transcript com speakers atribuídos
Saída: transcript speaker-aware
```

O Question Extraction utiliza a autoria preservada para distinguir entrevistador, candidato e falas desconhecidas.

### 5.3 20.3 → 20.4

```text
Entrada: perguntas extraídas com IDs estáveis
Saída: perguntas disponíveis para associação de respostas
```

O pipeline preserva `question_id`, `question_status`, `source`, `follow_up_of` e `needs_review`.

### 5.4 20.4 → 20.5

```text
Entrada: perguntas, respostas e transcript original
Saída: respostas extraídas disponíveis para reconstrução controlada
```

O Stage 20.5 somente normaliza ou reconstrói conforme suas regras. Ele não pode completar conteúdo técnico.

### 5.5 20.5 → 20.6

```text
Entrada: perguntas + respostas reconstruídas + metadata de origem
Saída: vínculos question ↔ response
```

Os vínculos reutilizam `question_id`, `response_id`, `follow_up_of`, `relation_type`, `source` e `linking_confidence`.

### 5.6 20.6 → 20.7

```text
Entrada: participantes, speakers, perguntas, respostas, links,
         reconstruções e fontes
Saída: Validation Report + Structured Interview readiness
```

O Validation Stage é a autoridade para determinar se a estrutura pode avançar.

## 6. Handoffs do Stage 20 para o Evidence Model

O avanço só é permitido quando:

```text
20.1 ✓
20.2 ✓
20.3 ✓
20.4 ✓
20.5 ✓
20.6 ✓
20.7 = READY ou READY_WITH_WARNINGS
```

Quando `20.7 = READY`:

```text
Structured Interview → Evidence Model
```

Quando `20.7 = READY_WITH_WARNINGS`:

```text
Structured Interview + Validation Warnings → Evidence Model
```

Quando `20.7 = BLOCKED`:

```text
STOP
↓
Human Review
```

Não executar Evidence Model, Rubric, Evaluation Engine ou Report como se o pipeline estivesse completo.

## 7. Handoff 20.7 → 21

O Evidence Model recebe:

```text
Structured Interview
Validation Report
Validation status
Validation warnings
```

Ele deve produzir o Evidence Set utilizando os artefatos existentes, sem reconstruir a entrevista. Warnings, `needs_review`, `missing`, `unknown` e limitações de source acompanham a evidência quando aplicável.

Regras obrigatórias:

- `response_status: missing` permanece ausência de resposta identificável;
- `question_id: unknown` permanece não vinculado quando não houver base suficiente;
- ausência de evidência não vira evidência negativa;
- `needs_review: true` não vira score baixo;
- nenhum ID ou `source.segment_id` pode ser inventado pela Orchestration.

## 8. Handoff 21 → Rubric / Evaluation Engine

O Evidence Model produz:

```text
Evidence Set
↓
EVIDENCE_MODEL_COMPLETE
```

O gate pode ser:

```text
READY
READY_WITH_WARNINGS
BLOCKED
```

`READY` e `READY_WITH_WARNINGS` permitem encaminhamento à avaliação quando a limitação não impedir a análise. `BLOCKED` interrompe o pipeline.

A Rubrica permanece como regra documental de avaliação:

```text
RUBRIC_COMPLETE
```

O Evaluation Engine recebe a pergunta, resposta e Evidence Set, aplica a Rubrica e produz o schema canônico de `evaluation`. A Orchestration não duplica pesos, não aplica N/A e não calcula score.

## 9. Handoff 22 → 23

```text
Rubric
    +
Evidence Set
    ↓
Evaluation Engine
```

As regras da Rubrica devem estar disponíveis e compatíveis com o Evidence Set. O Engine é responsável por:

- avaliação dimensional;
- tratamento de N/A;
- score;
- rationale;
- `evaluation.confidence`;
- referências de evidência;
- referência de pergunta, resposta e transcript.

A Orchestration somente verifica a pré-condição e transporta as referências.

## 10. Handoff 23 → Interview Evaluation Model / Report

O Evaluation Engine produz:

```text
EVALUATIONS
```

Cada avaliação individual deve preservar:

```text
evaluation.id
question.id
response.id
evidence_id
source.segment_ids
score
dimensions
confidence
rationale
warnings
needs_review
```

O `Interview Evaluation Model` consolida as avaliações sem fazer desaparecer perguntas não pontuadas. A média, quando apresentada, é derivada da lista canônica de avaliações e continua sendo apenas um indicador.

O Report consome as avaliações e a consolidação. Não recalcula silenciosamente score, média ou dimensões.

Após uma avaliação real concluída, a persistência segue:

```text
11 - Interview Evaluation/06 - Reports/Relatório-{nomeCandidato}.md
```

ou `Relatório-Candidato-{YYYY-MM-DD}.md` quando o nome não estiver disponível, conforme as regras da base. Esta etapa não cria ou atualiza relatório real.

## 11. Gates do pipeline

| Estágio | Gate | Permite avanço |
|---|---|---|
| 20.1–20.6 | saída estrutural da etapa | somente se a etapa concluir sem falha impeditiva |
| 20.7 Validation | `TRANSCRIPTION_PROCESSING_COMPLETE` | `READY` ou `READY_WITH_WARNINGS` |
| 21 Evidence Model | `EVIDENCE_MODEL_COMPLETE` | `READY` ou `READY_WITH_WARNINGS` |
| 22 Rubric | `RUBRIC_COMPLETE` | artefato compatível e disponível |
| 23 Evaluation Engine | `EVALUATION_ENGINE_COMPLETE` | `READY` ou `READY_WITH_WARNINGS` |
| Pipeline | `PIPELINE_READY` | todas as pré-condições satisfeitas |

Os gates descrevem prontidão do artefato ou fluxo. Nunca significam aprovação, reprovação, senioridade, ranking ou contratação.

### 11.1 READY

O pipeline pode declarar `READY` quando todos os gates necessários estão disponíveis, não há blocker estrutural e a rastreabilidade ponta a ponta está preservada.

### 11.2 READY_WITH_WARNINGS

O pipeline pode continuar com `READY_WITH_WARNINGS` quando os warnings não impedem o próximo handoff. Os warnings devem ser preservados no estado global e nos artefatos downstream relevantes.

### 11.3 BLOCKED

O pipeline deve declarar `BLOCKED` quando uma etapa produzir blocker estrutural, falhar, perder rastreabilidade essencial ou exigir inferência para continuar.

Exemplo:

```text
20.7 = BLOCKED
↓
pipeline.status = BLOCKED
pipeline.blockers = causa original
Evidence Model = não executado
Evaluation Engine = não executado
Report = não gerado
```

## 12. Propagação de warnings e `needs_review`

Warnings são metadata operacional, não evidência técnica negativa.

```text
20.7 warning
    ↓
Evidence Model warning
    ↓
Evaluation warning / confidence limitation, quando justificável
    ↓
Report limitation
```

O downstream pode reduzir a confiança da avaliação quando a limitação afetar a conclusão, mas não deve reduzir o score automaticamente apenas pela presença de um warning.

`needs_review` deve permanecer identificável em cada handoff:

```text
Structured Interview
↓
Evidence Set
↓
Evaluation
↓
Report
```

Não substituir `needs_review` por uma interpretação semântica diferente.

## 13. Source of Truth e rastreabilidade

O transcript bruto é a fonte original da fala:

```text
Raw Transcript
↓ representações derivadas
Structured Interview
↓
Evidence Set
↓
Evaluation
↓
Report
```

Nenhuma etapa posterior sobrescreve silenciosamente o transcript ou uma representação anterior.

A navegação ponta a ponta deve ser possível:

```text
Report
↓
Evaluation
↓
Question
↓
Response
↓
Evidence
↓
Transcript Segment
```

IDs obrigatórios quando aplicáveis:

```text
participant_id
speaker_id
question_id
response_id
evidence_id
evaluation.id
source.segment_ids
```

O pipeline não cria IDs concorrentes, não renomeia IDs estáveis sem justificativa e não aceita referências órfãs como se fossem válidas.

## 14. Propagação de metadata

Preservar, quando existente:

```text
candidate
participant_id
speaker_id
question_id
response_id
evidence_id
source
timestamps
needs_review
extraction_confidence
reconstruction_confidence
linking_confidence
evidence_confidence
evaluation.confidence
status
warnings
```

As confianças permanecem semanticamente separadas. A Orchestration não cria uma confidence global para substituir esses campos.

## 15. Missing e unknown

### 15.1 Missing response

```text
Q5
response_status: missing
```

Resultado:

```text
Q5 permanece sem resposta identificável.
```

Não produzir "o candidato não sabe", não criar evidência negativa e não fabricar resposta.

### 15.2 Unknown response

```text
R8
question_id: unknown
```

Resultado:

```text
R8 permanece não vinculado.
```

Não forçar `R8 → Q7` apenas para completar a estrutura.

## 16. Falhas parciais e retry

Se uma etapa falhar:

```text
stage = ERROR
```

o pipeline deve preservar:

```yaml
pipeline:
  status: BLOCKED
  failed_stage: ""
  blockers:
    - code: ""
      message: ""
  affected_artifacts: []
```

Não criar Evidence Set, Evaluation ou Report com aparência de conclusão.

Quando houver suporte a retry:

1. repetir somente a etapa necessária;
2. preservar resultados válidos anteriores;
3. reutilizar IDs estáveis;
4. evitar duplicação;
5. revalidar todos os dependentes downstream.

## 17. Idempotência

Executar novamente uma etapa com a mesma entrada lógica deve produzir o mesmo conjunto de IDs e não duplicar artefatos.

Regras:

- Question Extraction não cria Q13, Q14 ou Q15 duplicadas sem mudança justificável;
- Evidence Model não duplica evidências existentes;
- Evaluation Engine não cria avaliações paralelas para a mesma versão de pergunta/resposta;
- Report não cria cópia quando a operação corresponde à mesma entrevista;
- resultados existentes não são alterados silenciosamente.

Idempotência não significa ocultar mudanças reais. Se a entrada ou versão upstream mudou, o resultado pode ser regenerado com novo estado de proveniência.

## 18. Reprocessamento e staleness

Uma alteração upstream invalida potencialmente os artefatos downstream dependentes:

```text
20.5 corrigido
↓
20.6 pode estar stale
↓
20.7 precisa ser revalidado
↓
Evidence Set pode estar stale
↓
Evaluations podem estar stale
↓
Report pode estar stale
```

Quando a base não fornecer versionamento, hash ou `updated` suficiente, registrar explicitamente:

```text
downstream artifacts potentially stale
```

Não inventar um sistema de hashes nesta etapa. Não apagar os artefatos antigos automaticamente; marcar a necessidade de reprocessamento e revalidar dependências.

## 19. Job Context

O Job Context pode acompanhar o pipeline como contexto auxiliar:

```text
Interview Evidence ≠ Job Relevance
```

Ele não altera Evidence Set, score, dimensões ou `evaluation.confidence` da avaliação individual. A aderência à vaga é analisada separadamente, usando referências às avaliações existentes.

## 20. Agregação e relatório

Quando houver várias avaliações:

```text
Q1 → E1
Q2 → E2
Q3 → E3
```

o pipeline preserva cada avaliação, inclusive confidence, dimensões, evidências e rastreabilidade.

A agregação utiliza o mecanismo existente do `Interview Evaluation Model`. A média é um indicador e não pode ser convertida automaticamente em:

```text
seniority
ranking
hiring decision
approval / rejection
```

O relatório deve incluir limitações, warnings, perguntas não pontuadas e áreas não avaliadas quando aplicável, sem reinterpretar as avaliações.

## 21. Testes end-to-end controlados

Os cenários abaixo são testes arquiteturais sintéticos da Orchestration. Eles não processam entrevista real e não produzem score de candidato real.

| # | Cenário | Resultado esperado |
|---|---|---|
| 1 | entrevista válida completa | pipeline avança até Report handoff |
| 2 | múltiplas perguntas independentes | IDs e avaliações individuais preservados |
| 3 | múltiplos participantes | speakers e participantes mantidos nos handoffs |
| 4 | follow-up identificado | `follow_up_of` preservado |
| 5 | pergunta composta | estrutura composta não é recriada pela Orchestration |
| 6 | reconstrução com baixa confiança | warning propagado, sem correção técnica |
| 7 | speaker ambíguo | `needs_review` preservado |
| 8 | pergunta sem resposta | `response_status: missing` permanece sem resposta |
| 9 | resposta sem pergunta | `question_id: unknown` permanece não vinculada |
| 10 | `needs_review: true` | marca chega ao Evidence Set e à avaliação |
| 11 | participante criticamente não identificável | pipeline bloqueia se autoria principal for afetada |
| 12 | estrutura de perguntas inválida | Evidence Model não é executado |
| 13 | respostas corrompidas | pipeline bloqueia e registra etapa afetada |
| 14 | linking estrutural inconsistente | pipeline bloqueia ou encaminha para revisão conforme Validation |
| 15 | Validation `BLOCKED` | Evidence, Evaluation e Report não são executados |
| 16 | ausência de evidência | ausência não vira evidência negativa |
| 17 | evidências contraditórias | ambas seguem preservadas ao Engine |
| 18 | experiência somente declarada | declaração não vira experiência demonstrada |
| 19 | dimensão N/A | Engine trata N/A; Orchestration não calcula |
| 20 | erro crítico | Engine trata proporcionalmente; pipeline não aplica teto |
| 21 | confidence alta + score baixo | ambos permanecem distintos |
| 22 | resposta curta excelente | tamanho não é usado como proxy |
| 23 | resposta longa superficial | volume não melhora score |
| 24 | pergunta simples | complexidade não altera artificialmente a avaliação |
| 25 | pergunta complexa | complexidade não cria crédito automático |
| 26 | ID inexistente | validação bloqueia ou registra referência inválida |
| 27 | source inexistente | rastreabilidade inválida impede conclusão segura |
| 28 | evaluation sem response | schema incompleto não é encaminhado ao Report |
| 29 | evidence sem source | limitação é preservada; gate depende do impacto |
| 30 | downstream potencialmente stale | dependentes são marcados para reprocessamento |

**Cobertura documentada:** 30/30 cenários controlados.

## 22. Testes obrigatórios de bloqueio e warning

### 22.1 Bloqueio principal

```text
20.7.status = BLOCKED
```

Esperado:

```text
pipeline.status = BLOCKED
Evidence Model = não executado
Evaluation Engine = não executado
Report = não gerado
blockers = causa original
```

### 22.2 Warning principal

```text
20.7.status = READY_WITH_WARNINGS
```

Esperado:

```text
pipeline continua
warning preservado
Evidence Model = executável
Evaluation = executável quando a limitação permitir
warning rastreável até o Report
```

O warning não se transforma automaticamente em `negative evidence`.

## 23. Testes de invariância e integridade

| # | Teste | Invariante |
|---|---|---|
| I1 | executar o mesmo estágio duas vezes | mesmos IDs estáveis, sem duplicação |
| I2 | adicionar texto irrelevante | não cria evidência ou score |
| I3 | alterar apenas tom verbal | não altera avaliação técnica |
| I4 | adicionar senioridade declarada | não altera score |
| I5 | corrigir Stage 20.5 | dependentes ficam potencialmente stale |
| I6 | reexecutar após warning | warnings anteriores não desaparecem sem justificativa |
| I7 | preservar `missing` | não cria evidência negativa |
| I8 | preservar `unknown` | não cria vínculo artificial |
| I9 | remover source válido | rastreabilidade falha ou reduz readiness |
| I10 | gerar Report duas vezes | não cria relatório duplicado para a mesma entrevista |

**Cobertura documentada:** 10/10 invariantes.

## 24. Testes de separação de responsabilidades

| Componente | Não pode fazer |
|---|---|
| Transcription Processing | pontuar ou inferir conhecimento |
| Evidence Model | pontuar ou corrigir tecnicamente a resposta |
| Rubric | processar transcript ou atribuir speakers |
| Evaluation Engine | reconstruir transcript ou criar Evidence Set |
| Orchestration | interpretar conhecimento ou recalcular score |
| Report | recalcular score, média ou dimensões |
| Job Context | alterar score individual ou virar gabarito |

**Cobertura documentada:** 7/7 fronteiras.

## 25. Compatibilidade

| Componente | Compatibilidade |
|---|---|
| 20.1 Participant Identification | ✓ |
| 20.2 Speaker Attribution | ✓ |
| 20.3 Question Extraction | ✓ |
| 20.4 Response Extraction | ✓ |
| 20.5 Reconstruction & Normalization | ✓ |
| 20.6 Question/Response Linking | ✓ |
| 20.7 Validation | ✓ |
| 21 Evidence Model | ✓ |
| 22 Rubric | ✓ |
| 23 Evaluation Engine | ✓ |
| Job Context | ✓ |
| Report persistence | ✓ |
| Traceability | ✓ |

## 26. Gate da Etapa 24

O pipeline pode declarar:

```text
PIPELINE_READY
```

quando:

- a ordem canônica estiver preservada;
- os handoffs estiverem definidos;
- `BLOCKED` interromper o fluxo;
- `READY_WITH_WARNINGS` permitir continuidade controlada;
- warnings e `needs_review` forem propagados;
- `missing` e `unknown` não forem reinterpretados;
- source of truth e rastreabilidade estiverem preservados;
- confidence fields permanecerem separados;
- a Orchestration não calcular score;
- o Evaluation Engine não reconstruir transcript;
- o Report não recalcular avaliação;
- idempotência, reprocessamento e staleness estiverem documentados;
- falhas parciais estiverem tratadas;
- os testes controlados estiverem definidos;
- nenhuma entrevista real tiver sido processada.

O status desta nota é:

```text
READY_WITH_WARNINGS
```

O warning é herdado dos artefatos anteriores: a Rubrica e o Evaluation Engine documentam baselines de calibração, mas os artefatos históricos das Etapas 19/19.1 não estão disponíveis. Além disso, esta etapa formaliza contratos documentais; não existe executor de runtime no repositório para afirmar execução operacional desses cenários.

Esse status não representa falha de candidato, score ou decisão de contratação.

## 27. Resultado desta etapa

```text
PIPELINE_READY
```

Status operacional documental:

```text
READY_WITH_WARNINGS
```

Nenhuma entrevista real foi processada. Nenhum score real foi produzido. Nenhum relatório real foi gerado nesta etapa.

## Ver também

- [[Transcription Processing Model]]
- [[20.7 - Validation]]
- [[Evidence Model]]
- [[Scoring Rubric]]
- [[Evaluation Engine]]
- [[Interview Evaluation Model]]
- [[Job Context Model]]
- [[Interview Evaluation MOC]]
