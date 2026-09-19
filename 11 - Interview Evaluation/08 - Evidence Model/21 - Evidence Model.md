---
type: reference
status: learning
confidence: 100
created: 2026-09-19
updated: 2026-09-19
tags:
  - interview-evaluation
  - evidence-model
  - technical-evidence
---
# 21 — Evidence Model

Este documento define como transformar uma `Structured Interview` validada em um conjunto de evidências técnicas rastreáveis.

A pergunta central desta etapa é:

```text
Quais evidências podem ser extraídas daquilo que o candidato efetivamente
demonstrou em sua resposta?
```

O Evidence Model não responde qual nota a resposta merece. Essa decisão pertence à [[Scoring Rubric]] e ao [[Evaluation Engine]].

```text
Transcrição
↓
Structured Interview
↓
Evidence Model
↓
Evidence Set
↓
Scoring Rubric
↓
Evaluation Engine
```

> **Evidência é aquilo que pode ser sustentado pelo conteúdo efetivamente produzido pelo candidato na entrevista.**

## 1. Responsabilidade e limites

### 1.1 Transcription Processing — Stage 20

Os módulos 20.1 a 20.7 determinam:

```text
quem falou
↓
o que foi perguntado
↓
o que foi respondido
↓
como reconstruir e normalizar
↓
qual pergunta corresponde à resposta
↓
se a estrutura é suficientemente confiável
```

### 1.2 Evidence Model — Stage 21

O Stage 21 determina:

```text
quais evidências existem na resposta
↓
qual é a natureza de cada evidência
↓
qual trecho sustenta a evidência
↓
qual é a força e a confiança da extração
↓
se existem evidências contraditórias ou relacionadas
```

### 1.3 Rubric 0–10

A [[Scoring Rubric]] determina como as evidências se relacionam com critérios como correção, completude, profundidade, raciocínio, aplicação prática e trade-offs.

### 1.4 Evaluation Engine

O [[Evaluation Engine]] combina pergunta, resposta, evidências, conhecimento relevante e rubrica para produzir a avaliação da pergunta.

O Evidence Model não substitui nenhuma dessas etapas.

## 2. Entrada oficial

A entrada oficial é:

```text
Structured Interview
+
Validation Report
```

produzidos pelo Stage 20.

Fluxo:

```text
RAW TRANSCRIPT
↓
20.1–20.6 Transcription Processing
↓
20.7 Validation
↓
Structured Interview
↓
21 Evidence Model
```

O Evidence Model deve consumir perguntas, respostas, speakers, reconstruções, vínculos e sources já estruturados. Não deve retornar diretamente à transcrição bruta para reconstruir conteúdo quando existir uma representação validada.

O status `READY` ou `READY_WITH_WARNINGS` do Stage 20.7 permite o processamento posterior conforme os warnings registrados. O status `BLOCKED` impede o processamento normal:

```text
20.7 = BLOCKED
↓
Human Review
↓
Evidence Model somente após resolução ou decisão explícita
```

O Evidence Model referencia as regras de validação do Stage 20.7; não as recria nem as substitui.

## 3. Definição formal de evidência

Uma evidência é uma unidade específica de conteúdo produzido pelo candidato que pode sustentar uma descrição sobre conhecimento, raciocínio, aplicação ou experiência demonstrada.

Uma evidência deve ser:

- rastreável a uma pergunta, resposta e um ou mais segmentos;
- atribuível ao candidato quando for usada como evidência da resposta;
- sustentada pelo conteúdo observado;
- semanticamente preservada;
- separada da interpretação avaliativa;
- específica o suficiente para justificar sua existência;
- proporcional ao que foi demonstrado.

Uma fala não é evidência automaticamente. Ela pode ser social, contextual, irrelevante, especulativa, incompleta ou insuficiente para sustentar uma conclusão técnica.

```text
Fala observada
↓
É produzida pelo candidato?
↓
É relevante para a pergunta?
↓
Contém informação sustentada?
↓
Evidência estruturável
```

Uma evidência deve distinguir:

```text
statement
→ o que foi dito

interpretation
→ o que o trecho permite identificar

evaluation
→ o julgamento posterior da qualidade
```

O Evidence Model produz `statement` e, quando necessário, uma interpretação descritiva limitada. Não produz avaliação, score ou conclusão de senioridade.

## 4. Distinções fundamentais

### 4.1 Evidência encontrada vs. evidência esperada

```text
Evidência encontrada
≠
Evidência esperada
```

`Evidence` descreve o que o candidato demonstrou. `Expected Evidence` descreve sinais que uma pergunta ou critério pode exigir ou tornar relevantes.

Exemplo:

```text
Expected Evidence:
- carrier threads
- scheduler
- blocking behavior
- scalability

Candidate Evidence:
- menciona que Virtual Threads são leves;
- relaciona Virtual Threads à JVM.
```

A ausência dos demais elementos significa apenas que eles não foram demonstrados naquela resposta. Não significa automaticamente que o candidato não os conhece.

### 4.2 Evidência encontrada vs. ausência de evidência

```text
Evidência encontrada
≠
Evidência esperada

Ausência de evidência
≠
Ausência de conhecimento
```

Usar descrições como:

```text
not_demonstrated
not_observed
insufficient_evidence
```

quando apropriado. Não usar `candidate_does_not_know` ou `knowledge_absent` sem evidência explícita que sustente essa conclusão, e essa conclusão não pertence ao Evidence Model.

### 4.3 Evidência de entrevista, externa e declarada

Manter separados:

```text
Interview Evidence
≠
External Evidence
≠
Declared Experience
```

- **Interview Evidence**: conteúdo técnico produzido pelo candidato na resposta avaliada.
- **External Evidence**: currículo, portfólio, GitHub, certificações ou outros materiais externos.
- **Declared Experience**: afirmação verbal de que o candidato realizou algo, sem demonstração técnica suficiente na resposta.

O currículo, cargo, anos de experiência e confiança ao falar podem fornecer contexto em etapas apropriadas, mas não são evidência técnica da resposta.

## 5. Eixos independentes de classificação

Não misturar os seguintes eixos:

### 5.1 Natureza da evidência

O que o candidato demonstrou:

```text
conceptual
factual
architectural
implementation
practical
experience_declaration
demonstrated_experience
reasoning
tradeoff
troubleshooting
scenario_application
self_correction
uncertainty
contradiction
```

### 5.2 Qualificação da evidência

Como a afirmação se apresenta em relação ao que foi demonstrado:

```text
positive
partial
negative
contradictory
absent
insufficient
```

Esses valores correspondem à taxonomia já estabelecida no [[Evidence Model]] conceitual e no esquema de `evaluation.evidence` do [[Evaluation Engine]]. `negative` descreve uma afirmação tecnicamente incorreta observada; não é uma nota moral ou uma conclusão sobre o candidato.

`absent` e `insufficient` não são evidências textuais positivas extraídas de uma fala. São estados de cobertura usados quando o conjunto processado não sustenta determinado aspecto.

### 5.3 Explicitness

```text
explicit
implicit
```

- `explicit`: o candidato afirma diretamente o conteúdo.
- `implicit`: o conteúdo pode ser identificado de maneira limitada a partir da ação, relação ou explicação apresentada.

Inferência implícita deve permanecer controlada e nunca ultrapassar o suporte do trecho.

### 5.4 Força e confiança

`evidence_strength` descreve a clareza e especificidade do sinal:

```text
strong
moderate
weak
insufficient
```

`evidence_confidence` descreve a confiança de que a evidência foi identificada e interpretada adequadamente a partir da resposta:

```text
high
medium
low
```

Força e confiança são diferentes:

```text
evidence_strength: strong
evidence_confidence: low
```

é possível quando o trecho parece específico, mas há dúvida de transcrição, speaker, termo técnico ou contexto.

`evidence_confidence` não significa:

```text
confidence that the candidate is technically correct
confidence that the candidate is senior
confidence in the final evaluation
```

## 6. Taxonomia de evidências por natureza

Uma evidência pode possuir mais de uma dimensão de natureza quando isso for necessário, mas não deve ser duplicada apenas para repetir a mesma afirmação.

### 6.1 `conceptual`

Demonstra compreensão de um conceito ou princípio.

```text
Circuit Breaker impede que chamadas continuem sendo feitas
para um serviço que está falhando.
```

O Evidence Model registra a compreensão apresentada. A avaliação de correção fica para a Rubrica e o Evaluation Engine.

### 6.2 `factual`

Demonstra conhecimento de um comportamento, mecanismo, componente ou característica técnica observável.

```text
O candidato afirma que o componente X mantém o estado Y entre chamadas.
```

O fato deve ser registrado como foi apresentado, inclusive quando posteriormente for considerado incorreto.

### 6.3 `architectural`

Demonstra entendimento de arquitetura, componentes, responsabilidades, limites, dependências, direção de dependência ou integração entre componentes.

```text
Eu colocaria o adapter de banco fora do core e faria o caso de uso
depender de uma porta.
```

O trecho pode conter evidência arquitetural mesmo sem mencionar o nome `Hexagonal Architecture`.

### 6.4 `implementation`

Demonstra conhecimento de como implementar determinado comportamento, configuração, fluxo, algoritmo ou integração.

Não completar a implementação com passos que o candidato não mencionou.

### 6.5 `practical`

Demonstra aplicação concreta de conhecimento em uma situação, projeto, produção, configuração ou procedimento.

Aplicação prática não significa automaticamente experiência ampla ou domínio geral da tecnologia.

### 6.6 `experience_declaration`

Registra uma experiência afirmada pelo candidato sem detalhes técnicos suficientes:

```text
Já trabalhei bastante com Azure.
```

Essa evidência deve permanecer separada de `demonstrated_experience`.

### 6.7 `demonstrated_experience`

Registra experiência acompanhada de detalhes observáveis sobre contexto, problema, decisão, implementação, consequência ou dificuldade:

```text
Usei Application Insights para monitorar requests, dependencies e
exceptions e correlacionei os traces pelo operation ID.
```

O Evidence Model registra os detalhes demonstrados; não confirma externamente se a experiência ocorreu.

### 6.8 `reasoning`

Demonstra análise, causalidade, formulação de hipóteses, decomposição do problema, priorização, decisão ou validação.

```text
Primeiro eu isolaria o endpoint afetado, depois compararia métricas
de aplicação com dependências externas e validaria a hipótese pelos traces.
```

### 6.9 `tradeoff`

Demonstra consideração de alternativas, consequências, custos, limitações ou condições de uso:

```text
Usaria cache para reduzir latência, mas precisaria considerar
invalidação e o risco de dados desatualizados.
```

Não transformar uma preferência simples em trade-off se nenhuma consequência ou alternativa foi apresentada.

### 6.10 `troubleshooting`

Demonstra uma estratégia de investigar ou diagnosticar problemas técnicos, incluindo, quando presente, sintoma, hipótese, métrica, log, trace, correlação, isolamento, validação ou mitigação.

Não exigir todos esses elementos em toda resposta.

### 6.11 `scenario_application`

Demonstra como o candidato aplicaria conhecimento em um cenário hipotético:

```text
Se eu tivesse esse problema, usaria Circuit Breaker.
```

Isso não é `demonstrated_experience` sem evidência adicional de que ocorreu em contexto real.

### 6.12 `self_correction`

Registra uma autocorreção espontânea:

```text
Resposta inicial
+
Autocorreção
```

A autocorreção é evidência sobre a evolução do raciocínio e deve preservar a sequência. O Evidence Model não decide se ela compensa ou elimina a afirmação inicial.

### 6.13 `uncertainty`

Preserva expressões como:

```text
não sei
não lembro
acho que
se não me engano
nunca implementei
```

Incerteza não é automaticamente erro técnico. Também não é prova absoluta de ausência de conhecimento.

### 6.14 `contradiction`

Registra uma incompatibilidade sustentada entre afirmações. As afirmações conflitantes devem permanecer como evidências próprias, relacionadas por `contradicts`.

O Evidence Model não escolhe automaticamente qual afirmação é verdadeira.

## 7. Experiência declarada vs. demonstrada

Modelar explicitamente:

```text
declared_experience
≠
demonstrated_experience
```

Exemplo:

```text
Candidato:
  Trabalho com Kubernetes há três anos.

Evidence:
  type: experience_declaration
  qualification: positive
```

Isso não demonstra automaticamente domínio de Kubernetes.

Se o candidato acrescentar:

```text
Usei HPA para escalar pods conforme CPU e memória e configurei
readiness e liveness probes.
```

podem ser criadas evidências adicionais:

```text
type: demonstrated_experience
type: implementation
type: practical
```

As evidências continuam separadas. Não combiná-las automaticamente para produzir uma nota.

Anos de experiência declarados não aumentam `evidence_confidence`, `evidence_strength` ou score.

## 8. Perguntas hipotéticas e respostas incompletas

### 8.1 Hipótese

```text
Se eu tivesse que resolver esse problema, usaria Circuit Breaker.
```

Registrar `scenario_application`, e possivelmente `reasoning` ou `conceptual` se sustentados. Não registrar experiência real sem evidência adicional.

### 8.2 Resposta incompleta

```text
Eu começaria olhando o Application Insights...
```

Registrar somente a evidência de que o candidato começaria por esse recurso. Não adicionar mentalmente dependencies, traces, KQL ou outros passos esperados.

### 8.3 Resposta fora do tópico

Preservar a resposta estruturada, mas não fabricar evidência para preencher a lacuna. Se nenhum conteúdo relevante existir, o resultado pode conter `insufficient_evidence` para o aspecto solicitado.

### 8.4 Pergunta sem resposta

Não criar evidência:

```text
Q3
response_status: missing
↓
sem Evidence Set para Q3
```

Ausência de resposta não significa desconhecimento.

### 8.5 Resposta sem pergunta identificada

Quando `question_id: unknown`, preservar uma evidência se o trecho puder ser atribuído ao candidato e possuir conteúdo relevante. A evidência deve manter `question_id: unknown` e `response_id` válido, com `needs_review: true` quando a falta de contexto limitar a interpretação.

### 8.6 Fala do entrevistador

Não transformar explicações, dicas, correções ou exemplos do entrevistador em evidência do candidato.

### 8.7 Candidato perguntando ao entrevistador

Não tratar automaticamente a pergunta do candidato como resposta técnica. Ela pode ser registrada como contexto conversacional, mas não como evidência de conhecimento da resposta avaliada.

## 9. Evidence Inference Boundaries

O agente deve:

- extrair apenas o que é sustentado;
- separar afirmação observada de interpretação;
- manter condicionais, hipóteses e incertezas;
- não completar mentalmente a resposta;
- não assumir conhecimento não demonstrado;
- não usar CV, cargo, empresa, certificação ou anos de experiência como evidência da resposta;
- não usar confiança verbal, fluência, eloquência ou jargão como evidência técnica;
- não usar respostas de outras perguntas como prova automática;
- não usar conhecimento externo sobre o candidato;
- não transformar intenção em experiência;
- não transformar hipótese em experiência real;
- não transformar expectativa da pergunta em conteúdo efetivamente demonstrado;
- não inferir uma tecnologia específica quando o texto permite várias interpretações;
- não transformar uma preferência em fato técnico;
- não transformar uma experiência declarada em experiência demonstrada;
- não corrigir tecnicamente uma afirmação durante a extração.

> **A evidência deve ser proporcional ao que o candidato efetivamente demonstrou.**

Uma inferência implícita só é aceitável quando:

1. o trecho é suficientemente específico;
2. a relação inferida é necessária para descrever o conteúdo semântico apresentado;
3. não acrescenta conhecimento, contexto ou experiência ausente;
4. é marcada como `explicitness: implicit`;
5. possui `evidence_confidence` compatível.

Se a inferência for forte, controversa ou dependente de contexto ausente, usar `needs_review: true`.

## 10. Evidência positiva, negativa e contraditória

### 10.1 Positiva

Registra uma afirmação ou comportamento demonstrado pelo candidato.

```yaml
qualification: positive
```

`positive` significa que existe um sinal observável. Não significa que a afirmação já foi julgada correta pela Rubrica.

### 10.2 Parcial

Registra uma parte demonstrada de um aspecto mais amplo:

```yaml
qualification: partial
```

Parcial descreve cobertura limitada, não necessariamente erro.

### 10.3 Negativa / tecnicamente incorreta

Registra uma afirmação tecnicamente incorreta observada:

```yaml
qualification: negative
```

Exemplo:

```text
Virtual Threads são executadas diretamente em threads físicas do
sistema operacional.
```

Preservar a afirmação original. Não substituir por uma explicação correta.

### 10.4 Contraditória

Quando existirem afirmações incompatíveis, registrar cada uma separadamente e relacioná-las:

```text
E12 → statement: X
E18 → statement: Y
E18 relation: contradicts E12
```

Não resolver automaticamente a contradição.

### 10.5 Ausente

Usar `absent` como estado de cobertura quando um aspecto relevante esperado não foi demonstrado. Não criar uma citação fictícia nem atribuir essa ausência à falta de conhecimento.

### 10.6 Insuficiente

Usar `insufficient` quando o material existe, mas não permite sustentar uma evidência interpretável com segurança:

```text
Depende do cenário.
```

O Evidence Model deve registrar a limitação, não preenchê-la com conhecimento externo.

## 11. Preservação de respostas tecnicamente incorretas

O Evidence Model preserva evidências de respostas incorretas para que a Rubrica e o Evaluation Engine possam avaliá-las.

```text
Candidato:
Virtual Threads são executadas diretamente em threads físicas do
sistema operacional.

Evidence:
  qualification: negative
  content: "O candidato descreve Virtual Threads como diretamente executadas
             em threads físicas do sistema operacional."
```

Não substituir por:

```text
Virtual Threads são threads leves gerenciadas pela JVM.
```

Essa segunda frase pode pertencer ao conhecimento de referência, mas não é uma representação fiel da fala do candidato.

## 12. Granularidade

Criar uma evidência quando houver uma afirmação ou comportamento distinguível, relevante e rastreável.

Criar múltiplas evidências quando:

- existirem afirmações tecnicamente independentes;
- cada afirmação puder possuir tipo, source ou qualificação diferente;
- separar as afirmações melhorar a auditabilidade;
- uma afirmação for positiva e outra contraditória ou negativa;
- uma experiência incluir detalhes de implementação ou trade-offs distintos.

Manter uma única evidência quando:

- os segmentos formarem uma única afirmação inseparável;
- a divisão apenas repetir a mesma informação;
- fragmentar destruir a relação causal ou o contexto;
- as partes não possuírem valor analítico independente.

Exemplo:

```text
Usei Redis como cache para reduzir latência,
mas precisei lidar com invalidação e consistência.
```

Pode produzir:

```text
E1 — aplicação de cache
E2 — objetivo de reduzir latência
E3 — reconhecimento de invalidação
E4 — reconhecimento de consistência
```

desde que cada item seja sustentado e não seja apenas uma paráfrase redundante.

Evitar:

- evidências excessivamente fragmentadas;
- duplicação de uma mesma afirmação;
- uma evidência que mistura muitos conceitos sem necessidade;
- evidências derivadas somente do que era esperado.

## 13. Source traceability

Toda evidência utilizada posteriormente deve permitir o percurso:

```text
Question
↓
Response
↓
Evidence
↓
Source segment(s)
↓
Original Transcript
```

Reutilizar as estruturas de Stage 20:

```yaml
question_id: Q1
response_id: R1
evidence_id: E1
source:
  segment_ids:
    - S12
  start: "00:08:41"
  end: "00:08:57"
```

Quando a resposta possuir `original_text` e `reconstructed_text`, a evidência deve ser sustentada pela representação derivada sem perder a possibilidade de retornar ao `original_text`:

```text
Evidence
↓
reconstructed_text
↓
original_text
↓
source.segment_ids
```

Não criar evidência sem source quando a fonte deveria existir. Se a fonte estiver ausente na Structured Interview, registrar a limitação e marcar `needs_review: true`; não inventar segmentos ou timestamps.

O source de uma evidência deve conter somente trechos do candidato quando a evidência for atribuída ao candidato. Trechos do entrevistador podem ser registrados separadamente como contexto, nunca como evidência do candidato.

## 14. Evidence ID

O repositório já utiliza `evidence` como conceito central, mas não possuía anteriormente um padrão operacional explícito de `evidence_id`. Este documento define:

```text
E1
E2
E3
...
```

O escopo padrão é uma entrevista ou um Evidence Set. Dentro desse escopo, o ID deve ser único e estável após a criação.

`evidence_id`:

- é identificador técnico da unidade de evidência;
- não representa qualidade;
- não representa força;
- não representa score;
- não representa senioridade;
- não deve ser renumerado para esconder duplicações.

Não utilizar:

```text
E9_EXCELENTE
E4_JUNIOR
E7_SENIOR
```

Se o mesmo Evidence Set for atualizado, preservar IDs existentes quando a evidência continuar sendo a mesma. Criar um novo ID quando houver uma unidade materialmente diferente, sem apagar silenciosamente a evidência anterior.

## 15. Confidence

Manter separadas as dimensões já utilizadas no pipeline:

```text
participant_identification_confidence
attribution_confidence
extraction_confidence
reconstruction_confidence
linking_confidence
evidence_confidence
evaluation_confidence
```

O Evidence Model introduz apenas `evidence_confidence` para a confiança de que a evidência identificada está adequadamente sustentada pelo conteúdo da resposta.

```text
evidence_confidence
≠
confidence that the candidate is correct
≠
confidence that the candidate is senior
≠
evaluation_confidence
```

Exemplos:

```yaml
extraction_confidence: high
reconstruction_confidence: medium
linking_confidence:
  level: high
evidence_confidence: low
```

Isso pode ocorrer quando a resposta está corretamente identificada, mas uma expressão técnica ou uma inferência semântica permanece ambígua.

Não reutilizar um campo genérico `confidence` sem indicar sua dimensão.

## 16. `needs_review`

Uma evidência deve permitir:

```yaml
needs_review: true
review_reason: "..."
```

Usar `needs_review: true` quando houver:

- trecho ambíguo ou incompreensível;
- reconstrução com `reconstruction_confidence: low`;
- termo técnico possivelmente incorreto;
- interpretação implícita forte;
- conflito entre segmentos;
- speaker attribution problemática;
- linking incerto;
- evidência potencialmente duplicada;
- dificuldade de distinguir experiência real de hipótese;
- possível contradição;
- source ausente ou incompleto;
- dúvida sobre se a fala é do candidato ou do entrevistador.

`needs_review` é um indicador operacional de incerteza. Não é avaliação negativa do candidato, não reduz score automaticamente e não significa que a evidência esteja errada.

Se `needs_review: true`, registrar razão suficiente para permitir auditoria.

## 17. Relações entre evidências

Relações devem ser criadas somente quando sustentadas:

```text
supports
contradicts
refines
qualifies
expands
depends_on
derived_from
```

### 17.1 `supports`

Uma evidência adiciona suporte específico a outra, sem transformar a relação em julgamento.

### 17.2 `contradicts`

As afirmações são incompatíveis no contexto identificado. Preservar ambas.

### 17.3 `refines`

Uma evidência especifica ou delimita outra.

### 17.4 `qualifies`

Uma evidência adiciona condição, limitação ou premissa.

### 17.5 `expands`

Uma evidência adiciona detalhe relacionado, sem necessariamente justificar a primeira.

### 17.6 `depends_on`

Uma evidência depende de outra para ser interpretada, por exemplo, uma conclusão que depende da premissa explicitamente apresentada.

### 17.7 `derived_from`

Indica derivação estrutural ou semântica controlada, não conteúdo inventado. Toda derivação deve manter source e não ultrapassar o texto.

Não criar relações arbitrárias, relações baseadas somente em similaridade temática ou relações que expressem avaliação escondida.

## 18. Contradições

### 18.1 Dentro da mesma resposta

Registrar as afirmações separadamente:

```text
E12:
  content: "Virtual Threads são threads do sistema operacional."

E13:
  content: "Virtual Threads são gerenciadas pela JVM."

E13:
  relation:
    type: contradicts
    target_evidence_id: E12
```

Preservar a ordem e os sources. Não selecionar automaticamente a última afirmação como correta.

### 18.2 Entre respostas diferentes

Registrar as evidências de cada resposta e relacioná-las somente se o contexto sustentar que tratam do mesmo conceito:

```text
E12 → response_id: R4
E18 → response_id: R9
E18 contradicts E12
```

A resolução da contradição e seu impacto pertencem à avaliação posterior.

### 18.3 Autocorreção

Uma autocorreção deve preservar:

```text
statement inicial
↓
autocorreção
↓
ordem temporal
```

Pode haver relação `qualifies` ou `contradicts`, mas o Evidence Model não decide se a autocorreção elimina a afirmação inicial para fins de nota.

## 19. Evidence Leakage Prevention

O Evidence Model deve descrever a evidência sem contaminá-la com julgamento.

Evitar:

```text
Candidate demonstrates excellent knowledge.
Candidate gave a senior-level answer.
Candidate has weak Azure knowledge.
```

Preferir:

```text
Candidate identifies X and explains its relationship with Y.
Candidate discusses a trade-off between X and Y.
Candidate mentions Azure Monitor but does not provide additional
technical details in this response.
```

A última formulação descreve o que foi observado. Não deve ser transformada automaticamente em `candidate does not know Azure`.

Não usar nos campos de evidência:

- nota;
- peso;
- âncora da Rubrica;
- avaliação de senioridade;
- recomendação;
- aprovação ou reprovação;
- classificação global;
- comparação com outro candidato.

## 20. Integração com Question Taxonomy

O Evidence Model pode consumir `question.type`, `primary_type`, `secondary_dimensions`, `domain` e `complexity` como contexto:

```yaml
question:
  id: Q1
  primary_type: troubleshooting
  secondary_dimensions:
    - observability
    - reasoning
```

O tipo da pergunta não determina automaticamente o tipo, a qualidade ou a natureza da evidência.

Exemplos:

```text
Pergunta de experiência
→ pode produzir evidência conceitual ou de troubleshooting.

Pergunta técnica
→ pode produzir evidência de experiência demonstrada.

Pergunta de cenário
→ pode produzir evidência de raciocínio e aplicação hipotética.
```

Não criar regras rígidas que limitem essas combinações.

## 21. Expected Evidence

`Expected Evidence` deve permanecer separado do Evidence Set:

```text
Question Taxonomy + contexto técnico
↓
Expected Evidence

Structured Response
↓
Candidate Evidence
```

Uma representação conceitual:

```yaml
expected_evidence:
  - description: "Explicar que o Circuit Breaker interrompe chamadas após falhas."
    relevance: essential

evidence:
  - evidence_id: E1
    content: "O candidato afirma que o Circuit Breaker impede novas chamadas."
```

O Evidence Model pode transportar o esperado como contexto para a etapa seguinte, mas não deve marcar automaticamente como ausente todo item não mencionado. A relevância depende da pergunta, do contexto e da estrutura do critério posterior.

## 22. Modelo de dados

O esquema `evaluation` completo permanece canônico no [[Evaluation Engine]]. Esta seção define somente a unidade de Evidence Set e não duplica o objeto de avaliação, seus scores, dimensões ou pesos.

Modelo conceitual:

```yaml
evidence_set:
  source_validation_status: READY_WITH_WARNINGS
  evidence:
    - evidence_id: E1
      question_id: Q1
      response_id: R1

      type: conceptual
      qualification: positive
      content: "O candidato explica que as dependências são fornecidas externamente."
      interpretation: "Demonstra compreensão da injeção externa de dependências."

      source:
        segment_ids:
          - S12
        start: "00:08:41"
        end: "00:08:57"

      explicitness: explicit
      evidence_strength: strong
      evidence_confidence: high

      needs_review: false
      relations: []
```

Campos:

| Campo | Responsabilidade |
|---|---|
| `evidence_id` | ID estável e único no Evidence Set |
| `question_id` | Pergunta de origem, reutilizando o ID do Stage 20 |
| `response_id` | Resposta de origem, reutilizando o ID do Stage 20 |
| `type` | Natureza da evidência |
| `qualification` | `positive`, `partial`, `negative`, `contradictory`, `absent` ou `insufficient` |
| `content` | Descrição fiel do conteúdo observado |
| `interpretation` | Interpretação descritiva limitada, quando necessária |
| `source` | Segmentos e intervalos que sustentam a evidência |
| `explicitness` | `explicit` ou `implicit` |
| `evidence_strength` | Clareza e especificidade do sinal |
| `evidence_confidence` | Confiança da extração/interpretação da evidência |
| `needs_review` | Incerteza operacional que exige revisão |
| `review_reason` | Motivo de revisão quando necessário |
| `relations` | Relações estruturais com outras evidências |

`interpretation` não deve conter nota, julgamento de senioridade ou conclusão global.

### 22.1 Resposta hipotética

```yaml
evidence:
  - evidence_id: E2
    question_id: Q2
    response_id: R2
    type: scenario_application
    qualification: positive
    content: "O candidato propõe usar Circuit Breaker no cenário apresentado."
    explicitness: explicit
    evidence_confidence: high
    needs_review: false
```

Não usar `type: demonstrated_experience` sem evidência de ocorrência real.

### 22.2 Experiência declarada

```yaml
evidence:
  - evidence_id: E3
    question_id: Q3
    response_id: R3
    type: experience_declaration
    qualification: positive
    content: "O candidato declara ter trabalhado com Kubernetes."
    explicitness: explicit
    evidence_confidence: high
    needs_review: false
```

### 22.3 Limitação

```yaml
evidence:
  - evidence_id: E4
    question_id: Q4
    response_id: R4
    type: uncertainty
    qualification: positive
    content: "O candidato afirma não lembrar como o mecanismo funcionava."
    explicitness: explicit
    evidence_confidence: high
    needs_review: false
```

Isso registra uma limitação declarada. Não conclui desconhecimento absoluto.

### 22.4 Fonte ausente

Quando a Structured Interview não possuir source onde ele deveria existir:

```yaml
source: null
needs_review: true
review_reason: "A resposta possui conteúdo relevante, mas não há segmento de origem disponível."
```

Não criar source fictício. Dependendo do impacto, o Evidence Set pode terminar como `READY_WITH_WARNINGS` ou `BLOCKED`.

## 23. Pipeline formal

Executar:

```text
Structured Interview
↓
Verificar status READY ou READY_WITH_WARNINGS
↓
Ler pares Question/Response
↓
Identificar conteúdo produzido pelo candidato
↓
Excluir falas do entrevistador como evidência do candidato
↓
Identificar afirmações tecnicamente relevantes
↓
Segmentar evidências sem fragmentação excessiva
↓
Classificar natureza e qualificação
↓
Preservar significado original
↓
Anexar source
↓
Atribuir evidence_id
↓
Atribuir evidence_confidence
↓
Detectar contradições e relações sustentadas
↓
Marcar needs_review quando necessário
↓
Produzir Evidence Set
```

Nenhuma etapa produz score.

## 24. Saída para a Rubric e Evaluation Engine

O Evidence Model entrega:

```text
Question
↓
Response
↓
Evidence Set
↓
Rubric
↓
Evaluation Engine
```

O Evidence Set deve permitir que a etapa seguinte avalie, quando aplicável:

```text
correctness
completeness
depth
reasoning
practical_application
trade_offs
```

O Evidence Model não calcula essas dimensões, não aplica pesos e não seleciona âncoras 0–10.

O [[Evaluation Engine]] continua sendo o único esquema canônico para a avaliação completa `evaluation`, incluindo `evaluation.id`, `question`, `expected`, `evidence`, `dimensions`, `score`, `findings`, `rationale` e `related_knowledge`.

## 25. O que o Evidence Model não faz

O Evidence Model does NOT:

- atribuir nota;
- calcular média;
- aplicar pesos da Rubrica;
- aplicar âncoras de 0–10;
- classificar o candidato;
- determinar senioridade;
- decidir aprovação ou reprovação;
- decidir contratação;
- produzir conclusão global sobre o candidato;
- corrigir tecnicamente respostas;
- transformar ausência de evidência em desconhecimento;
- usar cargo, CV, anos de experiência ou eloquência como evidência;
- transformar hipótese em experiência real;
- transformar intenção em execução comprovada;
- substituir a transcrição ou a Structured Interview;
- criar expected evidence como se fosse candidate evidence;
- decidir se uma contradição foi resolvida;
- modificar a base técnica para acomodar uma resposta.

## 26. Casos especiais

### 26.1 `"Não sei"`

Preservar a declaração como `uncertainty` ou limitação. Não registrar conhecimento inexistente e não concluir ausência absoluta de conhecimento.

### 26.2 `"Não lembro"`

Preservar a incerteza e a possível experiência declarada. Não classificar a lacuna de memória automaticamente como erro técnico.

### 26.3 `"Nunca trabalhei com isso"`

Registrar a declaração como limitação ou `experience_declaration` negativa no sentido de ausência de experiência afirmada, sem concluir que o candidato não possui conhecimento conceitual.

### 26.4 Resposta hipotética

Registrar `scenario_application`, `reasoning` ou `conceptual` somente quando sustentados. Não registrar experiência real automaticamente.

### 26.5 Resposta parcial

Registrar somente as evidências existentes. Não completar o restante com expected evidence ou conhecimento do Second Brain.

### 26.6 Resposta fora do tópico

Não fabricar evidência para preencher a lacuna. A resposta pode produzir `insufficient_evidence` para a pergunta, quando essa estrutura for necessária para a etapa posterior.

### 26.7 Autocorreção

Preservar a afirmação inicial e a autocorreção, sources e sequência. Não apagar a primeira afirmação silenciosamente.

### 26.8 Resposta tecnicamente errada

Preservar a afirmação errada como `qualification: negative` quando a incorreção for identificada pelo processamento posterior ou pela relação com o conhecimento de referência. O Evidence Model não substitui o texto por uma versão correta.

### 26.9 Resposta sem pergunta identificada

Preservar a evidência quando atribuível ao candidato:

```yaml
question_id: unknown
response_id: R8
needs_review: true
```

### 26.10 Pergunta sem resposta

Não criar Evidence Set para uma resposta inexistente. Registrar apenas a ausência estrutural herdada do Stage 20 quando necessário.

### 26.11 Fala do entrevistador

Não promover explicação, sugestão, correção ou exemplo do entrevistador a evidência do candidato.

### 26.12 Candidato perguntando

Não interpretar automaticamente uma pergunta feita pelo candidato como demonstração de conhecimento. O conteúdo pode ser contexto, mas não responde por si só à pergunta avaliada.

## 27. Testes controlados

Os testes verificam extração, classificação, rastreabilidade, preservação e separação de responsabilidades. Nenhum teste atribui score.

### Caso 1 — Resposta técnica simples

**Input:** Q1/R1 do candidato: `"Dependency Injection fornece as dependências externamente."`

**Expected Evidence:** uma evidência sobre fornecimento externo de dependências.

**Expected Type:** `conceptual`.

**Expected Source:** segments de R1.

**Expected Confidence:** `high`, se o trecho for claro.

**Expected `needs_review`:** `false`.

**Expected non-evaluation behavior:** não calcular correção ou nota.

### Caso 2 — Resposta conceitual

**Input:** o candidato explica que Circuit Breaker interrompe chamadas para serviço em falha.

**Expected Evidence:** descrição da função conceitual do mecanismo.

**Expected Type:** `conceptual`.

**Expected Source:** source de R2.

**Expected Confidence:** `high`, se a atribuição for clara.

**Expected `needs_review`:** `false`.

**Expected non-evaluation behavior:** não aplicar âncora da Rubrica.

### Caso 3 — Resposta factual

**Input:** o candidato afirma um comportamento específico de uma API ou componente.

**Expected Evidence:** afirmação factual registrada como foi produzida.

**Expected Type:** `factual`.

**Expected Source:** segmentos que contêm a afirmação.

**Expected Confidence:** depende da transcrição, não da correção técnica.

**Expected `needs_review`:** `true` somente se houver ambiguidade de fonte ou conteúdo.

**Expected non-evaluation behavior:** não corrigir a afirmação durante a extração.

### Caso 4 — Resposta arquitetural

**Input:** `"Eu colocaria o adapter de banco fora do core e faria o caso de uso depender de uma porta."`

**Expected Evidence:** relação entre limite do core, adapter, porta e dependência.

**Expected Type:** `architectural`.

**Expected Source:** segmentos da resposta.

**Expected Confidence:** `high` quando o trecho for inequívoco.

**Expected `needs_review`:** `false`.

**Expected non-evaluation behavior:** não concluir senioridade ou nota de arquitetura.

### Caso 5 — Resposta prática

**Input:** o candidato descreve uma mudança aplicada em produção e seu contexto operacional.

**Expected Evidence:** aplicação concreta, sem confirmação externa automática.

**Expected Type:** `practical` e/ou `demonstrated_experience`.

**Expected Source:** segmentos da experiência.

**Expected Confidence:** proporcional à clareza dos detalhes.

**Expected `needs_review`:** `false`, salvo ambiguidade.

**Expected non-evaluation behavior:** não tratar a experiência como prova de domínio geral.

### Caso 6 — Experiência declarada sem detalhes

**Input:** `"Já trabalhei bastante com Azure."`

**Expected Evidence:** declaração de experiência.

**Expected Type:** `experience_declaration`.

**Expected Source:** segmento da declaração.

**Expected Confidence:** `high` para a existência da declaração.

**Expected `needs_review`:** `false` se o trecho for claro.

**Expected non-evaluation behavior:** não promover a experiência a demonstração técnica.

### Caso 7 — Experiência declarada com detalhes

**Input:** o candidato declara experiência e explica uso de Application Insights para requests, dependencies, exceptions e operation ID.

**Expected Evidence:** declaração separada de evidências práticas e de implementação.

**Expected Type:** `experience_declaration`, `demonstrated_experience`, `practical` e/ou `implementation`.

**Expected Source:** segments específicos de cada afirmação.

**Expected Confidence:** `high` se todos os trechos forem atribuídos ao candidato.

**Expected `needs_review`:** `false`, salvo source ou termo ambíguo.

**Expected non-evaluation behavior:** não combinar automaticamente evidências para gerar nota.

### Caso 8 — Cenário hipotético

**Input:** `"Se eu tivesse esse problema, usaria Circuit Breaker."`

**Expected Evidence:** aplicação em cenário e possível raciocínio.

**Expected Type:** `scenario_application`.

**Expected Source:** segmento da resposta.

**Expected Confidence:** `high`.

**Expected `needs_review`:** `false`.

**Expected non-evaluation behavior:** não registrar `demonstrated_experience`.

### Caso 9 — Raciocínio técnico

**Input:** o candidato propõe isolar endpoint, comparar métricas, investigar dependências e validar com traces.

**Expected Evidence:** sequência de investigação e relação causal.

**Expected Type:** `reasoning` e possivelmente `troubleshooting`.

**Expected Source:** segments correspondentes.

**Expected Confidence:** `high` se a ordem e autoria forem claras.

**Expected `needs_review`:** `false`.

**Expected non-evaluation behavior:** não avaliar se essa é a melhor estratégia.

### Caso 10 — Trade-off

**Input:** `"Usaria cache para reduzir latência, mas teria de lidar com invalidação e consistência."`

**Expected Evidence:** objetivo e consequências reconhecidas.

**Expected Type:** `tradeoff`, podendo também ser `conceptual`.

**Expected Source:** trecho completo.

**Expected Confidence:** `high`.

**Expected `needs_review`:** `false`.

**Expected non-evaluation behavior:** não aplicar peso de trade-offs.

### Caso 11 — Troubleshooting

**Input:** o candidato começa por observar métricas e traces antes de alterar configuração.

**Expected Evidence:** estratégia de diagnóstico baseada em observação e isolamento.

**Expected Type:** `troubleshooting` e `reasoning`.

**Expected Source:** segmentos da estratégia.

**Expected Confidence:** `high`.

**Expected `needs_review`:** `false`.

**Expected non-evaluation behavior:** não pontuar a resposta.

### Caso 12 — Autocorreção

**Input:** `"Eu usaria threads do sistema... quer dizer, Virtual Threads são gerenciadas pela JVM."`

**Expected Evidence:** afirmação inicial e autocorreção separadas, com ordem preservada.

**Expected Type:** `self_correction`, além dos tipos das afirmações.

**Expected Source:** os dois segmentos.

**Expected Confidence:** `high` para a sequência quando a transcrição for clara.

**Expected `needs_review`:** `false`, salvo dúvida sobre a fala.

**Expected non-evaluation behavior:** não decidir se a correção elimina o erro para a nota.

### Caso 13 — `"Não sei"`

**Input:** `"Não sei explicar como esse mecanismo funciona."`

**Expected Evidence:** declaração de limitação/incerteza.

**Expected Type:** `uncertainty`.

**Expected Source:** segmento da resposta.

**Expected Confidence:** `high`.

**Expected `needs_review`:** `false`.

**Expected non-evaluation behavior:** não concluir ausência absoluta de conhecimento.

### Caso 14 — `"Não lembro"`

**Input:** `"Eu já usei isso, mas não lembro os detalhes agora."`

**Expected Evidence:** experiência declarada e limitação de memória separadas.

**Expected Type:** `experience_declaration` e `uncertainty`.

**Expected Source:** segmentos correspondentes.

**Expected Confidence:** `high` para as declarações.

**Expected `needs_review`:** `false`.

**Expected non-evaluation behavior:** não classificar automaticamente como erro técnico.

### Caso 15 — Resposta parcial

**Input:** `"Eu começaria olhando o Application Insights..."`, sem outros passos.

**Expected Evidence:** apenas a ação inicial explicitamente mencionada.

**Expected Type:** `practical`, `troubleshooting` ou `implementation`, conforme contexto.

**Expected Source:** segmento disponível.

**Expected Confidence:** `high` para o trecho.

**Expected `needs_review`:** `false`.

**Expected non-evaluation behavior:** não completar com dependencies, traces ou KQL.

### Caso 16 — Resposta tecnicamente incorreta

**Input:** `"Virtual Threads são threads físicas do sistema operacional."`

**Expected Evidence:** afirmação original preservada.

**Expected Type:** `factual` ou `conceptual`, com `qualification: negative` quando a incorreção for identificada.

**Expected Source:** segmento original/reconstruído.

**Expected Confidence:** confiança na extração pode ser `high`, mesmo que a afirmação esteja errada.

**Expected `needs_review`:** `false` se a fala for clara.

**Expected non-evaluation behavior:** não substituir por uma explicação correta.

### Caso 17 — Contradição dentro da resposta

**Input:** a resposta contém `"é gerenciado pelo sistema operacional"` e depois `"é gerenciado pela JVM"`.

**Expected Evidence:** duas evidências e relação `contradicts`.

**Expected Type:** tipos próprios das afirmações e `contradiction` para a relação.

**Expected Source:** cada trecho correspondente.

**Expected Confidence:** `high` se ambos forem claros.

**Expected `needs_review`:** `true` se a contradição depender de transcrição ambígua.

**Expected non-evaluation behavior:** não escolher automaticamente uma afirmação.

### Caso 18 — Contradição entre respostas

**Input:** R4 afirma X e R9 afirma Y sobre o mesmo conceito, em perguntas diferentes.

**Expected Evidence:** evidências independentes ligadas por `contradicts` somente se o contexto sustentar a comparação.

**Expected Type:** tipos próprios das afirmações.

**Expected Source:** sources de R4 e R9.

**Expected Confidence:** depende da identificação do mesmo conceito.

**Expected `needs_review`:** `true` quando a relação entre perguntas não for clara.

**Expected non-evaluation behavior:** não resolver a contradição nem calcular impacto.

### Caso 19 — Resposta sem pergunta identificada

**Input:** R8 possui `question_id: unknown`, é fala do candidato e contém uma explicação técnica.

**Expected Evidence:** evidência preservada com contexto limitado.

**Expected Type:** conforme o conteúdo, por exemplo `conceptual`.

**Expected Source:** source de R8.

**Expected Confidence:** `medium` ou `low` por falta de pergunta.

**Expected `needs_review`:** `true`.

**Expected non-evaluation behavior:** não inventar Q8 nem descartar R8.

### Caso 20 — Evidência ambígua

**Input:** termo técnico pode ser `"Application Insights"` ou outro componente, e o linking é de baixa confiança.

**Expected Evidence:** interpretação conservadora ou representação original, com limitação registrada.

**Expected Type:** tipo provisório somente se sustentado.

**Expected Source:** segmento ambíguo preservado.

**Expected Confidence:** `low`.

**Expected `needs_review`:** `true`, com `review_reason`.

**Expected non-evaluation behavior:** não normalizar o termo por conveniência nem atribuir nota.

### Caso 21 — Fala do entrevistador

**Input:** entrevistador explica o conceito e o candidato apenas confirma `"sim"`.

**Expected Evidence:** nenhuma evidência técnica equivalente à explicação do entrevistador; a confirmação pode ser contexto.

**Expected Type:** nenhum tipo técnico derivado da fala do entrevistador.

**Expected Source:** somente fala do candidato se houver conteúdo relevante.

**Expected Confidence:** não aplicável à explicação do entrevistador.

**Expected `needs_review`:** conforme a atribuição da fala.

**Expected non-evaluation behavior:** não atribuir ao candidato o conhecimento explicado pelo entrevistador.

### Caso 22 — Pergunta sem resposta

**Input:** Q10 possui `response_status: missing`.

**Expected Evidence:** nenhum Evidence Set para uma resposta inexistente.

**Expected Type:** não aplicável.

**Expected Source:** não criar source.

**Expected Confidence:** não aplicável.

**Expected `needs_review`:** preservar o estado do Stage 20.

**Expected non-evaluation behavior:** não converter ausência em `candidate_does_not_know`.

### Caso 23 — Duplicação potencial

**Input:** dois segmentos expressam a mesma afirmação, mas pertencem a R1 e R1.1.

**Expected Evidence:** uma evidência consolidada ou duas com relação `refines`, conforme a diferença material.

**Expected Type:** tipo sustentado pelo conteúdo.

**Expected Source:** todos os segmentos relevantes.

**Expected Confidence:** `medium` se a consolidação for interpretativa.

**Expected `needs_review`:** `true` quando não for possível determinar se há informação nova.

**Expected non-evaluation behavior:** não duplicar evidências apenas para aumentar a quantidade.

### Caso 24 — Source ausente

**Input:** resposta possui texto reconstruído, mas nenhum `source.segment_id`.

**Expected Evidence:** evidência somente se a estrutura permitir, com source nulo e limitação explícita.

**Expected Type:** conforme conteúdo.

**Expected Source:** `null`, sem inventar IDs.

**Expected Confidence:** `low`.

**Expected `needs_review`:** `true`.

**Expected non-evaluation behavior:** não tratar a evidência como plenamente auditável nem atribuir score.

## 28. Gate de saída

O Evidence Model produz:

```text
EVIDENCE_MODEL_COMPLETE
```

somente quando as evidências foram estruturadas e o resultado recebeu um gate:

### READY

Usar quando:

- a entrada foi `READY` ou `READY_WITH_WARNINGS`;
- evidências relevantes possuem question, response e source quando disponíveis;
- IDs são únicos e estáveis;
- a atribuição ao candidato está preservada;
- o significado da resposta foi mantido;
- não há conteúdo inventado;
- ambiguidades residuais não impedem a auditoria;
- nenhuma falha impede a Rubrica de receber o Evidence Set.

```text
EVIDENCE_MODEL_COMPLETE
↓
READY
↓
Scoring Rubric
```

### READY_WITH_WARNINGS

Usar quando:

- existem fontes ausentes ou incompletas, mas o impacto é limitado;
- há evidências implícitas ou ambíguas com `needs_review: true`;
- uma resposta sem pergunta pode ser preservada, mas não contextualizada completamente;
- há duplicação potencial que não corrompe o conjunto;
- warnings do Stage 20.7 acompanham a evidência;
- a Rubrica ainda pode analisar o Evidence Set sem inferência excessiva.

```text
EVIDENCE_MODEL_COMPLETE
↓
READY_WITH_WARNINGS
↓
Scoring Rubric
+
Warnings
```

### BLOCKED

Usar quando:

- a entrada do Stage 20 está `BLOCKED`;
- não é possível atribuir evidências ao candidato;
- a rastreabilidade fundamental foi perdida;
- conteúdo inventado ou correção técnica alterou a representação da resposta;
- a maioria das evidências não possui source quando a fonte deveria existir;
- perguntas, respostas ou speakers estão estruturalmente misturados;
- o conjunto exigiria inferência excessiva para ser produzido;
- IDs duplicados ou conflitos impedem auditar qual evidência é qual;
- a extração não consegue preservar o significado da resposta.

```text
STOP
↓
Human Review
```

`BLOCKED` significa que o Evidence Set não é confiável. Não significa que o candidato foi reprovado.

O gate não decide:

```text
o que o candidato sabe
```

nem:

```text
se o candidato é adequado à vaga
```

Ele decide somente se as evidências foram estruturadas de forma confiável para permitir a avaliação posterior.

## 29. Critérios de qualidade

Um Evidence Model de qualidade:

- não inventa conteúdo;
- não corrige tecnicamente a fala;
- mantém rastreabilidade;
- separa evidência de interpretação e avaliação;
- diferencia experiência declarada de experiência demonstrada;
- preserva incerteza;
- preserva contradições;
- controla inferência;
- evita duplicações;
- possui IDs estáveis;
- possui `evidence_confidence` própria;
- usa `needs_review` quando necessário;
- permite auditoria posterior;
- é reproduzível;
- não depende de senioridade presumida;
- não depende do CV;
- não depende do cargo;
- não depende da eloquência;
- não transforma expected evidence em candidate evidence;
- não produz score, média ou conclusão global.

## 30. Compatibilidade com os estágios anteriores

O documento reutiliza:

```text
20.1 Participant Identification
→ participant_id, role, identification_confidence, needs_review

20.2 Speaker Attribution
→ speaker.participant_id, attribution_confidence, source

20.3 Question Extraction
→ question_id, question_status, follow_up_of, source

20.4 Response Extraction
→ response_id, question_id, response_status, response_type,
  original_segments, extraction_confidence, source

20.5 Reconstruction & Normalization
→ original_text, reconstructed_text, normalization_applied,
  reconstruction_confidence, source, needs_review

20.6 Question/Response Linking
→ question_id, response_id, relation_type, linking_confidence,
  source.question_segment_ids, source.response_segment_ids

20.7 Validation
→ status, issues, traceability, readiness, warnings
```

Nenhum desses documentos é alterado pelo Stage 21.

O Evidence Model deve respeitar:

- `question_id: unknown` quando a resposta não puder ser ligada;
- `response_status: missing` quando não existir resposta;
- `original_text` como fonte verbal preservada;
- `reconstructed_text` como representação derivada;
- `needs_review` como incerteza operacional, não como nota;
- confidence específicas de cada etapa;
- `READY`, `READY_WITH_WARNINGS` e `BLOCKED` como gates de processamento, não como avaliação do candidato.

## 31. Compatibilidade com estágios posteriores

### 31.1 Scoring Rubric

O Evidence Model entrega evidências para que a Rubrica possa analisar dimensões relevantes. Não aplica:

- pesos;
- âncoras;
- notas;
- normalização de pesos;
- categorias de erro para pontuação.

### 31.2 Evaluation Engine

O Evidence Model fornece o conteúdo do campo `evaluation.evidence` do esquema canônico, organizado conforme a natureza, qualificação e rastreabilidade da evidência. O Evaluation Engine continua responsável por combinar isso com:

```text
question
expected
dimensions
score
findings
rationale
related_knowledge
```

Não criar uma estrutura alternativa para substituir `evaluation`.

### 31.3 Job Context e Interview Evaluation

Informações externas e contexto de vaga devem permanecer separados de Interview Evidence. O Evidence Model não cria aderência à vaga, ranking, senioridade ou recomendação de contratação.

## 32. Regra fundamental do gate

> **O Evidence Model decide se as evidências foram estruturadas de forma confiável. Ele não decide o que o candidato sabe, sua senioridade ou sua adequação à vaga.**

> **Uma evidência ausente significa apenas que aquele aspecto não foi demonstrado na evidência processada, não que o candidato necessariamente não possui aquele conhecimento.**

## 33. Regra de ouro

> **O Evidence Model transforma respostas em evidências rastreáveis. Ele não transforma evidências em notas.**

> **O sistema deve avaliar aquilo que o candidato demonstrou, sem confundir ausência de demonstração com ausência de conhecimento.**

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
21 Evidence Model
        ↓
EVIDENCE SET
        ↓
Rubric 0–10
        ↓
Evaluation Engine
```

```text
Transcription Processing
    = "O que aconteceu na entrevista?"

Evidence Model
    = "O que o candidato efetivamente demonstrou?"

Rubric
    = "Como essas evidências se relacionam aos critérios?"

Evaluation Engine
    = "Qual é a avaliação da resposta?"
```

## Ver também

- [[Transcription Processing Model]]
- [[20.1 - Participant Identification]]
- [[20.2 - Speaker Attribution]]
- [[20.3 - Question Extraction]]
- [[20.4 - Response Extraction]]
- [[20.5 - Reconstruction & Normalization]]
- [[20.6 - Question-Response Linking]]
- [[20.7 - Validation]]
- [[Question Taxonomy]]
- [[Scoring Rubric]]
- [[Evaluation Engine]]
- [[Job Context Model]]
- [[Interview Evaluation MOC]]
