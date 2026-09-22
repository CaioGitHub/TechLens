---
type: reference
status: learning
confidence: 100
created: 2026-09-21
updated: 2026-09-21
tags:
  - interview-evaluation
  - evidence-model
  - real-interview-pilot
---

# Stage 21 — Evidence Set v1

## Run metadata

```yaml
stage: 21
status: COMPLETE_WITH_WARNINGS
source_artifact: Structured Interview - Controlled Correction v6.md
source_validation_status: READY_WITH_WARNINGS
source_of_verbal_content: Pilot Input - Source Transcript v3.md
evidence_model_executed: true
rubric_executed: false
evaluation_engine_executed: false
final_report_generated: false
```

This artifact structures interview evidence only. It does not assign scores, calculate averages, evaluate seniority, classify the candidate, or make a hiring recommendation.

## Input gate

```yaml
pipeline_gate:
  participant_identification: PASS
  speaker_attribution: PASS
  question_extraction: PASS
  response_extraction: PASS
  reconstruction_normalization: PASS
  question_response_linking: PASS_WITH_WARNINGS
  validation: READY_WITH_WARNINGS
  human_review: PASS
  semantic_audit: PASS_WITH_WARNINGS
  accepted_for_stage_21: true
```

## Inherited warnings

```yaml
warnings:
  - id: W-001
    type: unlinked_responses
    affected_response_ids: [R24, R26, R41, R52]
    handling: excluded_from_technical_evidence
    reason: "No safe question-response link was established upstream."
  - id: W-002
    type: unreconstructed_term
    term: ZepSight
    handling: preserved_upstream
    reason: "No transcript-only reconstruction was safe; no external lookup was used."
  - id: W-003
    type: historical_response_count_discrepancy
    v3_responses: 44
    v6_responses: 47
    handling: preserved_as_warning
    reason: "The preserved v3 artifact contains only an aggregate count."
  - id: W-004
    type: confidence_metadata_completeness
    handling: preserved_as_warning
    reason: "Upstream extraction_confidence and linking_confidence are not explicit for every record; no values were invented."
```

## Evidence boundaries

- Only responses with `evaluation_eligible: true` and `speaker_id: candidate` were processed as candidate evidence.
- Candidate questions `CQ1`–`CQ7` were excluded from technical evidence.
- `Q12` is non-evaluable and generated no evidence.
- `R42` is non-evaluable after the v6 correction and generated no evidence.
- `R24`, `R26`, `R41` and `R52` remained unlinked and generated no evidence.
- Interviewer speech, prompts, explanations and supplied technology terms were not attributed to the candidate.
- Original and reconstructed response text were preserved in every evidence source below.

## Evidence by question

```text
Q1  → E-001
Q2  → E-002, E-003, E-004, E-005, E-006, E-007, E-008
Q3  → E-009, E-010
Q4  → E-011
Q5  → E-012, E-013, E-014
Q6  → E-015, E-016
Q7  → E-017, E-018, E-019, E-020
Q8  → No evidence; follow-up/contextual continuation preserved upstream
Q9  → E-021, E-022
Q10 → E-023, E-024, E-025, E-026
Q11 → E-027, E-028
Q12 → No evidence; non-evaluable
```

## Evidence items

```yaml
evidence_set:
  source_validation_status: READY_WITH_WARNINGS
  evidence:
    - evidence_id: E-001
      question_id: Q1
      response_id: R1
      type: uncertainty
      qualification: insufficient
      content: "A candidata diz que ouviu falar muito pouco do projeto, 'bem por cima'."
      interpretation: "A resposta registra familiaridade declarada como limitada, sem detalhar o projeto."
      explicitness: explicit
      evidence_strength: weak
      evidence_confidence: high
      source:
        segment_ids: [RAW-003]
        timestamps: ["00:35"]
        original_text: "É muito pouco, bem por cima."
        reconstructed_text: "É muito pouco, bem por cima."
      needs_review: false
      relations: []

    - evidence_id: E-002
      question_id: Q2
      response_id: R3
      type: demonstrated_experience
      qualification: positive
      content: "A candidata relata formação técnica na Etec e na Fatec e participação em um projeto de sistema para uma central de transplantes."
      interpretation: "A resposta contém relato de trajetória e de participação em um projeto específico."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-012, RAW-013]
        timestamps: ["01:43", "01:56"]
        original_text: "Tudo bem. Bem, a minha trajetória com programação, ela começou lá atrás, quando eu fiz o técnico na Etec e depois na Fatec. Na Fatec, o Centro Paula Souza, ali tinha uma parceria com a central de transplantes para fazer um sistema."
        reconstructed_text: "Tudo bem. Bem, a minha trajetória com programação, ela começou lá atrás, quando eu fiz o técnico na Etec e depois na Fatec. Na Fatec, o Centro Paula Souza, ali tinha uma parceria com a central de transplantes para fazer um sistema."
      needs_review: false
      relations: []

    - evidence_id: E-003
      question_id: Q2
      response_id: R4
      type: practical
      qualification: positive
      content: "A candidata relata que a captação de órgãos era manual, que o objetivo do sistema era ocorrer em tempo real e que participou do projeto."
      interpretation: "A resposta descreve contexto de projeto, objetivo declarado e participação da candidata."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-014]
        timestamps: ["02:12"]
        original_text: "Ali, porque na época a questão de captação de órgãos era tudo muito manual. Então o objetivo desse sistema era que ocorresse tudo em tempo real, sabe? Eu participei desse projeto e foi o primeiro grande projeto. É assim que eu."
        reconstructed_text: "Ali, porque na época a questão de captação de órgãos era tudo muito manual. Então o objetivo desse sistema era que ocorresse tudo em tempo real, sabe? Eu participei desse projeto e foi o primeiro grande projeto. É assim que eu."
      needs_review: false
      relations: []

    - evidence_id: E-004
      question_id: Q2
      response_id: R6
      type: demonstrated_experience
      qualification: positive
      content: "A candidata relata atuação na Accenture, em um projeto bancário do Santander relacionado a financiamento imobiliário, por aproximadamente cinco a seis anos."
      interpretation: "A resposta fornece contexto temporal e de domínio para uma experiência profissional relatada."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-016, RAW-017]
        timestamps: ["02:28", "02:44"]
        original_text: "Tive a oportunidade de participar, desenvolver. Depois eu entrei na Accenture. Eu estou há quase 8 anos na Accenture e o primeiro projeto que eu peguei foi um cliente bancário, foi o Santander. Na parte de financiamento imobiliário, eu fiquei mais ou menos 5 a 6 anos nesse projeto."
        reconstructed_text: "Tive a oportunidade de participar, desenvolver. Depois eu entrei na Accenture. Eu estou há quase 8 anos na Accenture e o primeiro projeto que eu peguei foi um cliente bancário, foi o Santander. Na parte de financiamento imobiliário, eu fiquei mais ou menos 5 a 6 anos nesse projeto."
      needs_review: false
      relations: []

    - evidence_id: E-005
      question_id: Q2
      response_id: R7
      type: practical
      qualification: partial
      content: "A candidata menciona simulação, financiamento, gestão de contratos e desenvolvimento no projeto de financiamento imobiliário."
      interpretation: "A resposta apresenta áreas de atuação, mas termina de forma incompleta."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: medium
      source:
        segment_ids: [RAW-018]
        timestamps: ["02:53"]
        original_text: "Então eu via toda a parte de simulação, de financiamento, a parte de gestão de contratos, de financiamento imobiliário e trabalhava muito com desenvolvimento nesse projeto. Eu fiz de"
        reconstructed_text: "Então eu via toda a parte de simulação, de financiamento, a parte de gestão de contratos, de financiamento imobiliário e trabalhava muito com desenvolvimento nesse projeto. Eu fiz de"
      needs_review: false
      relations: []

    - evidence_id: E-006
      question_id: Q2
      response_id: R8
      type: experience_declaration
      qualification: positive
      content: "A candidata declara ter passado por várias equipes e ter trabalhado com sistemas legados, desenvolvimento de microsserviços e a parte de 'bet'."
      interpretation: "A resposta registra áreas e contextos de experiência declarados, preservando o termo 'bet' sem interpretação adicional."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: medium
      source:
        segment_ids: [RAW-019]
        timestamps: ["03:08"]
        original_text: "Tudo. Eu passei por várias equipes, então eu trabalhei com legado, eu trabalhei com desenvolvimento de microsserviços, eu trabalhei com a parte de bet."
        reconstructed_text: "Tudo. Eu passei por várias equipes, então eu trabalhei com legado, eu trabalhei com desenvolvimento de microsserviços, eu trabalhei com a parte de bet."
      needs_review: true
      review_reason: "O termo 'bet' permanece sem interpretação adicional."
      relations: []

    - evidence_id: E-007
      question_id: Q2
      response_id: R9
      type: experience_declaration
      qualification: partial
      content: "A candidata relata circulação por equipes e atuação atual em outro cliente bancário, identificado na fala como C6, relacionada a financiamento."
      interpretation: "A resposta contém contexto profissional, mas a frase termina incompleta."
      explicitness: explicit
      evidence_strength: weak
      evidence_confidence: medium
      source:
        segment_ids: [RAW-020]
        timestamps: ["03:19"]
        original_text: "eu circulei por todas as equipes desse projeto depois é atualmente eu tô no outro cliente bancário só que é a questão de financiamento de alto que é o C6 e"
        reconstructed_text: "eu circulei por todas as equipes desse projeto depois é atualmente eu tô no outro cliente bancário só que é a questão de financiamento de alto que é o C6 e"
      needs_review: true
      review_reason: "A resposta termina incompleta; nenhuma conclusão adicional foi inferida."
      relations: []

    - evidence_id: E-008
      question_id: Q2
      response_id: R10
      type: practical
      qualification: positive
      content: "A candidata menciona desenvolvimento de APIs, manutenção e correção de bugs como atividades."
      interpretation: "A resposta lista atividades práticas sem detalhar implementação ou contexto adicional."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-021]
        timestamps: ["03:35"]
        original_text: "É praticamente a mesma coisa, desenvolvimento de APIs, manutenção, correção de bugs."
        reconstructed_text: "É praticamente a mesma coisa, desenvolvimento de APIs, manutenção, correção de bugs."
      needs_review: false
      relations: []

    - evidence_id: E-009
      question_id: Q3
      response_id: R12
      type: factual
      qualification: positive
      content: "A candidata menciona Java como uma das tecnologias utilizadas."
      interpretation: "A resposta registra a tecnologia mencionada, com a forma reconstruída 'Java' rastreável ao original 'Beijava'."
      explicitness: explicit
      evidence_strength: weak
      evidence_confidence: high
      source:
        segment_ids: [RAW-023, RAW-024]
        timestamps: ["03:46", "03:49"]
        original_text: "Yes. Beijava."
        reconstructed_text: "Yes. Java."
      needs_review: false
      relations: []

    - evidence_id: E-010
      question_id: Q3
      response_id: R14
      type: implementation
      qualification: partial
      content: "A candidata diz que atuava somente no back end."
      interpretation: "A resposta delimita a área de atuação mencionada, sem identificar outras tecnologias não ditas."
      explicitness: explicit
      evidence_strength: weak
      evidence_confidence: high
      source:
        segment_ids: [RAW-026, RAW-027]
        timestamps: ["03:52", "03:54"]
        original_text: "Is. Isso, só mexer com o back end."
        reconstructed_text: "Is. Isso, só mexer com o back end."
      needs_review: false
      relations: []

    - evidence_id: E-011
      question_id: Q4
      response_id: R16
      type: factual
      qualification: positive
      content: "A candidata afirma que começou com Java 8, mudou para Java 17 e atualmente usa Java 21."
      interpretation: "A resposta apresenta uma sequência de versões de Java mencionadas pela candidata."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-030]
        timestamps: ["04:05"]
        original_text: "Era começou com a 8, depois mudou para 17 e agora é 21. O pessoal está migrando tudo, não é?"
        reconstructed_text: "Era começou com a 8, depois mudou para 17 e agora é 21. O pessoal está migrando tudo, não é?"
      needs_review: false
      relations: []

    - evidence_id: E-012
      question_id: Q5
      response_id: R17
      type: conceptual
      qualification: positive
      content: "A candidata associa producer e consumer à parte de Kafka."
      interpretation: "A resposta apresenta uma associação explícita entre os termos e Kafka."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-033, RAW-034]
        timestamps: ["04:34", "04:37"]
        original_text: "Consumers. Bom, quando você fala em producer e consumer, eu lembro muito que ele é da parte de Kafka. Consumer, que eu me lembro, ele pega um item da fila do Kafka ou do Rabbit, e producer, ele joga o item no tópico ou na fila."
        reconstructed_text: "Consumers. Bom, quando você fala em producer e consumer, eu lembro muito que ele é da parte de Kafka. Consumer, que eu me lembro, ele pega um item da fila do Kafka ou do Rabbit, e producer, ele joga o item no tópico ou na fila."
      needs_review: false
      relations: []

    - evidence_id: E-013
      question_id: Q5
      response_id: R17
      type: conceptual
      qualification: partial
      content: "A candidata descreve consumer como algo que pega um item da fila do Kafka ou do Rabbit."
      interpretation: "A resposta contém uma descrição explícita do papel atribuído a consumer."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-033, RAW-034]
        timestamps: ["04:34", "04:37"]
        original_text: "Consumers. Bom, quando você fala em producer e consumer, eu lembro muito que ele é da parte de Kafka. Consumer, que eu me lembro, ele pega um item da fila do Kafka ou do Rabbit, e producer, ele joga o item no tópico ou na fila."
        reconstructed_text: "Consumers. Bom, quando você fala em producer e consumer, eu lembro muito que ele é da parte de Kafka. Consumer, que eu me lembro, ele pega um item da fila do Kafka ou do Rabbit, e producer, ele joga o item no tópico ou na fila."
      needs_review: false
      relations: []

    - evidence_id: E-014
      question_id: Q5
      response_id: R17
      type: conceptual
      qualification: partial
      content: "A candidata descreve producer como algo que coloca um item no tópico ou na fila."
      interpretation: "A resposta contém uma descrição explícita do papel atribuído a producer."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-033, RAW-034]
        timestamps: ["04:34", "04:37"]
        original_text: "Consumers. Bom, quando você fala em producer e consumer, eu lembro muito que ele é da parte de Kafka. Consumer, que eu me lembro, ele pega um item da fila do Kafka ou do Rabbit, e producer, ele joga o item no tópico ou na fila."
        reconstructed_text: "Consumers. Bom, quando você fala em producer e consumer, eu lembro muito que ele é da parte de Kafka. Consumer, que eu me lembro, ele pega um item da fila do Kafka ou do Rabbit, e producer, ele joga o item no tópico ou na fila."
      needs_review: false
      relations: []

    - evidence_id: E-015
      question_id: Q6
      response_id: R19
      type: conceptual
      qualification: partial
      content: "A candidata associa JDBC à configuração com banco."
      interpretation: "A resposta identifica uma relação entre JDBC e configuração de banco, sem expandir o mecanismo."
      explicitness: explicit
      evidence_strength: weak
      evidence_confidence: high
      source:
        segment_ids: [RAW-036, RAW-037]
        timestamps: ["05:04", "05:10"]
        original_text: "O JDBC me vem muito ali a é. Configuração com banco, entendeu? Queries, consulta de banco."
        reconstructed_text: "O JDBC me vem muito ali a é. Configuração com banco, entendeu? Queries, consulta de banco."
      needs_review: false
      relations: []

    - evidence_id: E-016
      question_id: Q6
      response_id: R19
      type: implementation
      qualification: partial
      content: "A candidata relaciona JDBC a queries e consulta de banco."
      interpretation: "A resposta menciona atividades de acesso/consulta a banco, sem acrescentar passos de implementação."
      explicitness: explicit
      evidence_strength: weak
      evidence_confidence: high
      source:
        segment_ids: [RAW-036, RAW-037]
        timestamps: ["05:04", "05:10"]
        original_text: "O JDBC me vem muito ali a é. Configuração com banco, entendeu? Queries, consulta de banco."
        reconstructed_text: "O JDBC me vem muito ali a é. Configuração com banco, entendeu? Queries, consulta de banco."
      needs_review: false
      relations: []

    - evidence_id: E-017
      question_id: Q7
      response_id: R21
      type: architectural
      qualification: positive
      content: "A candidata identifica a arquitetura usada como arquitetura em camadas."
      interpretation: "A resposta fornece uma caracterização arquitetural explícita."
      explicitness: explicit
      evidence_strength: weak
      evidence_confidence: high
      source:
        segment_ids: [RAW-040]
        timestamps: ["05:28"]
        original_text: "Ele é mais arquitetura em camadas."
        reconstructed_text: "Ele é mais arquitetura em camadas."
      needs_review: false
      relations: []

    - evidence_id: E-018
      question_id: Q7
      response_id: R22
      type: experience_declaration
      qualification: positive
      content: "A candidata declara que não chegou a usar arquitetura hexagonal, mas afirma ter conhecimento sobre ela."
      interpretation: "A resposta separa uso declarado e conhecimento declarado; não demonstra uso prático da arquitetura."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-042]
        timestamps: ["05:36"]
        original_text: "Eu não cheguei a usar, mas eu tenho conhecimento sim. Eu sei que a parte do hexagonal, ele meio que separa ali a regra de negócio, a lógica do negócio de tecnologias externas. Então, por exemplo, entendeu? Se hoje um sistema ali usa Oracle,"
        reconstructed_text: "Eu não cheguei a usar, mas eu tenho conhecimento sim. Eu sei que a parte do hexagonal, ele meio que separa ali a regra de negócio, a lógica do negócio de tecnologias externas. Então, por exemplo, entendeu? Se hoje um sistema ali usa Oracle,"
      needs_review: false
      relations: []

    - evidence_id: E-019
      question_id: Q7
      response_id: R22
      type: architectural
      qualification: partial
      content: "A candidata descreve uma separação entre a regra/lógica de negócio e tecnologias externas, mencionando Oracle como exemplo de tecnologia."
      interpretation: "A resposta apresenta uma relação arquitetural e termina antes de concluir o exemplo."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-042]
        timestamps: ["05:36"]
        original_text: "Eu não cheguei a usar, mas eu tenho conhecimento sim. Eu sei que a parte do hexagonal, ele meio que separa ali a regra de negócio, a lógica do negócio de tecnologias externas. Então, por exemplo, entendeu? Se hoje um sistema ali usa Oracle,"
        reconstructed_text: "Eu não cheguei a usar, mas eu tenho conhecimento sim. Eu sei que a parte do hexagonal, ele meio que separa ali a regra de negócio, a lógica do negócio de tecnologias externas. Então, por exemplo, entendeu? Se hoje um sistema ali usa Oracle,"
      needs_review: false
      relations: []

    - evidence_id: E-020
      question_id: Q7
      response_id: R23
      type: reasoning
      qualification: positive
      content: "A candidata relaciona a separação arquitetural à possibilidade de trocar o banco sem afetar o sistema."
      interpretation: "A resposta explicita uma consequência associada à separação descrita."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-044]
        timestamps: ["05:53"]
        original_text: "É com essa separação, é muito mais fácil trocar o banco e não afetar o sistema."
        reconstructed_text: "É com essa separação, é muito mais fácil trocar o banco e não afetar o sistema."
      needs_review: false
      relations:
        - type: expands
          target_evidence_id: E-019

    - evidence_id: E-021
      question_id: Q9
      response_id: R25
      type: experience_declaration
      qualification: positive
      content: "A candidata declara uso recente de Dynatrace."
      interpretation: "A resposta registra uma ferramenta de observabilidade mencionada pela candidata, sem detalhes de configuração ou investigação."
      explicitness: explicit
      evidence_strength: weak
      evidence_confidence: high
      source:
        segment_ids: [RAW-050]
        timestamps: ["06:58"]
        original_text: "Sim, é o dyna trace. É, teve uma outra ferramenta agora que eu esqueci o nome, mas foi mais o dyna trace nos últimos tempos."
        reconstructed_text: "Sim, é o Dynatrace. É, teve uma outra ferramenta agora que eu esqueci o nome, mas foi mais o Dynatrace nos últimos tempos."
      needs_review: false
      relations: []

    - evidence_id: E-022
      question_id: Q9
      response_id: R25
      type: uncertainty
      qualification: insufficient
      content: "A candidata diz que utilizou outra ferramenta, mas não lembra o nome."
      interpretation: "A resposta preserva a incerteza e não identifica a ferramenta ausente."
      explicitness: explicit
      evidence_strength: weak
      evidence_confidence: high
      source:
        segment_ids: [RAW-050]
        timestamps: ["06:58"]
        original_text: "Sim, é o dyna trace. É, teve uma outra ferramenta agora que eu esqueci o nome, mas foi mais o dyna trace nos últimos tempos."
        reconstructed_text: "Sim, é o Dynatrace. É, teve uma outra ferramenta agora que eu esqueci o nome, mas foi mais o Dynatrace nos últimos tempos."
      needs_review: false
      relations: []

    - evidence_id: E-023
      question_id: Q10
      response_id: R27
      type: troubleshooting
      qualification: partial
      content: "A candidata propõe olhar o log durante a investigação de um erro."
      interpretation: "A resposta apresenta uma etapa de investigação, sem completar um fluxo diagnóstico."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-056, RAW-057]
        timestamps: ["08:01", "08:16"]
        original_text: "Debug olhar o log se não tiver acesso a log é printar ali é colocar prints em partes do código e é e acompanhando Acho que tem várias formas de procurar um erro, não é?"
        reconstructed_text: "Debug olhar o log se não tiver acesso a log é printar ali é colocar prints em partes do código e é e acompanhando Acho que tem várias formas de procurar um erro, não é?"
      needs_review: false
      relations: []

    - evidence_id: E-024
      question_id: Q10
      response_id: R27
      type: troubleshooting
      qualification: partial
      content: "A candidata propõe inserir prints em partes do código e acompanhar o comportamento quando não houver acesso a logs."
      interpretation: "A resposta apresenta uma alternativa operacional para investigação, sem inferir outros instrumentos."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-056, RAW-057]
        timestamps: ["08:01", "08:16"]
        original_text: "Debug olhar o log se não tiver acesso a log é printar ali é colocar prints em partes do código e é e acompanhando Acho que tem várias formas de procurar um erro, não é?"
        reconstructed_text: "Debug olhar o log se não tiver acesso a log é printar ali é colocar prints em partes do código e é e acompanhando Acho que tem várias formas de procurar um erro, não é?"
      needs_review: false
      relations: []

    - evidence_id: E-025
      question_id: Q10
      response_id: R27
      type: reasoning
      qualification: partial
      content: "A candidata afirma que existem várias formas de procurar um erro."
      interpretation: "A resposta expressa uma generalização sobre alternativas de investigação, sem enumerar outras formas além das mencionadas."
      explicitness: explicit
      evidence_strength: weak
      evidence_confidence: high
      source:
        segment_ids: [RAW-056, RAW-057]
        timestamps: ["08:01", "08:16"]
        original_text: "Debug olhar o log se não tiver acesso a log é printar ali é colocar prints em partes do código e é e acompanhando Acho que tem várias formas de procurar um erro, não é?"
        reconstructed_text: "Debug olhar o log se não tiver acesso a log é printar ali é colocar prints em partes do código e é e acompanhando Acho que tem várias formas de procurar um erro, não é?"
      needs_review: false
      relations: []

    - evidence_id: E-026
      question_id: Q10
      response_id: R29
      type: troubleshooting
      qualification: partial
      content: "A candidata identifica como principal abordagem subir o debug localmente e entender o comportamento."
      interpretation: "A resposta apresenta uma abordagem de investigação local, sem detalhar os passos seguintes."
      explicitness: explicit
      evidence_strength: moderate
      evidence_confidence: high
      source:
        segment_ids: [RAW-059, RAW-060]
        timestamps: ["08:21", "08:26"]
        original_text: "Mas a principal para mim é o debug subir. local e entendendo, né?"
        reconstructed_text: "Mas a principal para mim é o debug subir. local e entendendo, né?"
      needs_review: false
      relations: []

    - evidence_id: E-027
      question_id: Q11
      response_id: R32
      type: experience_declaration
      qualification: positive
      content: "A candidata declara que utiliza Copilot e menciona uma limitação de licença no contexto em que o pessoal usa 'cloud'."
      interpretation: "A evidência de uso atribuível à candidata é Copilot; a fala sobre o uso de 'cloud' pelo pessoal não foi convertida em experiência própria."
      explicitness: explicit
      evidence_strength: weak
      evidence_confidence: high
      source:
        segment_ids: [RAW-067, RAW-068]
        timestamps: ["09:00", "09:04"]
        original_text: "Sim, eu utilizo bastante. Hoje eu estou com copilot, mas o pessoal aqui usa cloud é porque a licença aqui não deu para todo mundo, né? Então eu acabei ficando sem a licença do cloud."
        reconstructed_text: "Sim, eu utilizo bastante. Hoje eu estou com copilot, mas o pessoal aqui usa cloud é porque a licença aqui não deu para todo mundo, né? Então eu acabei ficando sem a licença do cloud."
      needs_review: false
      relations: []

    - evidence_id: E-028
      question_id: Q11
      response_id: R34
      type: experience_declaration
      qualification: positive
      content: "A candidata afirma: 'Eu uso copilot.'"
      interpretation: "A resposta registra uso declarado da ferramenta, sem detalhes adicionais de aplicação."
      explicitness: explicit
      evidence_strength: weak
      evidence_confidence: high
      source:
        segment_ids: [RAW-070]
        timestamps: ["09:19"]
        original_text: "E eu uso copilot."
        reconstructed_text: "E eu uso copilot."
      needs_review: false
      relations: []
```

## Excluded material

```yaml
excluded:
  unlinked_responses:
    - response_id: R24
      reason: unlinked_response
    - response_id: R26
      reason: unlinked_response
    - response_id: R41
      reason: unlinked_response
    - response_id: R52
      reason: unlinked_response
  candidate_questions:
    - question_id: CQ1
      reason: candidate_question
    - question_id: CQ2
      reason: candidate_question
    - question_id: CQ3
      reason: candidate_question
    - question_id: CQ4
      reason: candidate_question
    - question_id: CQ5
      reason: candidate_question
    - question_id: CQ6
      reason: candidate_question
    - question_id: CQ7
      reason: candidate_question
  non_evaluable:
    - question_id: Q12
      reason: non_evaluable_contextual_question
    - response_id: R42
      reason: non_evaluable_conversational_response
  insufficient_without_evidence_item:
    - response_id: R31
      question_id: Q10
      reason: "The text 'Scroll.' does not sustain a contextualized evidence claim without adding interpretation."
```

## Traceability summary

```yaml
traceability:
  evidence_items: 28
  questions_with_evidence: 10
  evaluation_questions_with_source: 10
  responses_used_as_evidence: 21
  responses_with_source: 21
  unique_segments_used: 30
  orphan_evidence: 0
  invalid_question_references: 0
  invalid_response_references: 0
  invalid_segment_references: 0
  candidate_attribution_preserved: true
  reconstruction_preserved: true
```

Q8 and Q12 are intentionally absent from the evidence map. Q8 is a follow-up/contextual continuation of Q7 without an eligible response, and Q12 is non-evaluable.

## Evidence Set validation

```yaml
validation:
  traceability: PASS
  source_integrity: PASS
  candidate_attribution: PASS
  candidate_questions_excluded: PASS
  q12_r42_excluded: PASS
  unlinked_responses_excluded: PASS
  no_invention: PASS
  reconstruction_preservation: PASS
  confidence_separation: PASS_WITH_WARNING
  no_scoring: PASS
  no_external_information: PASS
  structural_status: COMPLETE_WITH_WARNINGS
  warnings:
    - "Inherited v6 warnings remain attached to the Evidence Set."
    - "R31 is eligible upstream but does not sustain a standalone evidence claim."
    - "CQ1-CQ5 have no explicit source object in v6; they are excluded and do not affect candidate evidence traceability."
```

## Output gate

```text
EVIDENCE_MODEL_COMPLETE_WITH_WARNINGS
READY_WITH_WARNINGS
```

Stage 22 — Rubric, Stage 23 — Evaluation Engine and final report generation were not executed.
