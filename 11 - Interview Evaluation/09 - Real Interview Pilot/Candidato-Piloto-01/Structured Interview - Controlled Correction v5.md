---
type: reference
status: understood
confidence: 100
created: 2026-09-21
updated: 2026-09-21
tags:
  - interview-evaluation
  - real-interview-pilot
  - human-review
  - controlled-correction
  - v5
---

# Stage 30.2 ? Structured Interview ? Controlled Correction v5

## Run metadata

```yaml
pilot_id: REAL-PILOT-2026-09-14-01-v5
source_version: REAL-PILOT-2026-09-14-01-v3
derived_from: Structured Interview - Controlled Correction v4.md
human_review_source: Human Review Matrix v4.md
reviewer: human_reviewer
review_timestamp: 2026-09-21T21:15:33-03:00
human_review_status: COMPLETE
approval: APPROVED_WITH_WARNINGS
readiness: READY_WITH_WARNINGS
downstream_evidence_model: NOT_EXECUTED
downstream_evaluation_engine: NOT_EXECUTED
```

## Source and preservation rules

The source of verbal content is `Pilot Input - Source Transcript v3.md`. v3 and v4 are preserved. Original text remains available for every reconstructed term; no transcript segment was deleted or overwritten.

## Participants

```json
[
  {
    "participant_id": "P-CANDIDATE",
    "name": "Ingrid Mazoni",
    "role": "candidate"
  },
  {
    "participant_id": "P-MICHELLY",
    "name": "Morais, Michelly Pereira de",
    "role": "interviewer"
  },
  {
    "participant_id": "P-CAIO",
    "name": "Paes, Caio Victor Pessoa de Vasconcelos",
    "role": "interviewer"
  },
  {
    "participant_id": "P-RODRIGO",
    "name": "Nascimento, Rodrigo Borges do",
    "role": "interviewer"
  }
]
```

## Counts

```yaml
participants: 4
segments: 164
evaluation_questions: 10
contextual_questions_preserved: 2
candidate_questions: 7
responses: 47
unresolved_unknown_links: 4
needs_review_responses: 2
needs_review_segments: 0
reconstruction_terms: 9
unreconstructed_ambiguous_terms: 1
v3_response_count: 44
v4_response_count: 47
historical_added_units: 3
```

## Evaluation questions

### Q1

```json
{
  "question_id": "Q1",
  "text": "Trabalho aqui no projeto do open finance do Bradesco, tá? Eu divido aqui a coordenação com o Rodrigo, que está aqui. É, você já ouviu falar um pouquinho do projeto open finance?",
  "primary_type": "technical",
  "source": {
    "segment_ids": [
      "RAW-002"
    ],
    "timestamps": [
      "00:19"
    ]
  },
  "question_status": "identified",
  "question_kind": "interviewer_question",
  "evaluation_eligible": true,
  "follow_up_of": null,
  "reformulation_of": null,
  "needs_review": false,
  "response_ids": [
    "R1"
  ]
}
```

### Q2

```json
{
  "question_id": "Q2",
  "text": "Beleza. E aí Ingrid, tudo certo? Pra começar, eu queria entender, queria que tu contasse mais ou menos um pouco da tua experiência profissional, qual foram os projetos que tu já atuou, tecnologias, um contexto assim.",
  "primary_type": "technical",
  "source": {
    "segment_ids": [
      "RAW-011"
    ],
    "timestamps": [
      "01:40"
    ]
  },
  "question_status": "identified",
  "question_kind": "interviewer_question",
  "evaluation_eligible": true,
  "follow_up_of": null,
  "reformulation_of": null,
  "needs_review": false,
  "response_ids": [
    "R3",
    "R4",
    "R6",
    "R7",
    "R8",
    "R9",
    "R10"
  ]
}
```

### Q3

```json
{
  "question_id": "Q3",
  "text": "Entendi, e nesses projetos, qual foram as tecnologias que tu usou? Java, C Sharpe, Angula, foi o que?",
  "primary_type": "technical",
  "source": {
    "segment_ids": [
      "RAW-022"
    ],
    "timestamps": [
      "03:42"
    ]
  },
  "question_status": "identified",
  "question_kind": "interviewer_question",
  "evaluation_eligible": true,
  "follow_up_of": null,
  "reformulation_of": null,
  "needs_review": false,
  "reconstructed_text": "Entendi, e nesses projetos, qual foram as tecnologias que tu usou? Java, C#, Angular, foi o que?",
  "original_text": "Entendi, e nesses projetos, qual foram as tecnologias que tu usou? Java, C Sharpe, Angula, foi o que?",
  "response_ids": [
    "R12",
    "R14"
  ]
}
```

### Q4

```json
{
  "question_id": "Q4",
  "text": "Perfeito, certo? A versão do Java, ela era qual é 17? Era mais avançada. Tu lembra qual é?",
  "primary_type": "technical",
  "source": {
    "segment_ids": [
      "RAW-029"
    ],
    "timestamps": [
      "03:56"
    ]
  },
  "question_status": "identified",
  "question_kind": "interviewer_question",
  "evaluation_eligible": true,
  "follow_up_of": null,
  "reformulation_of": null,
  "needs_review": false,
  "response_ids": [
    "R16"
  ]
}
```

### Q5

```json
{
  "question_id": "Q5",
  "text": "Saberia explicar para mim qual é a diferença entre o produtos e consumes em um API rest?",
  "primary_type": "technical",
  "source": {
    "segment_ids": [
      "RAW-032"
    ],
    "timestamps": [
      "04:27"
    ]
  },
  "question_status": "identified",
  "question_kind": "interviewer_question",
  "evaluation_eligible": true,
  "follow_up_of": null,
  "reformulation_of": null,
  "needs_review": false,
  "reconstructed_text": "Saberia explicar para mim qual é a diferença entre o producers e consumers em um API rest?",
  "original_text": "Saberia explicar para mim qual é a diferença entre o produtos e consumes em um API rest?",
  "response_ids": [
    "R17"
  ]
}
```

### Q6

```json
{
  "question_id": "Q6",
  "text": "Certo, e tu saberia também explicar o que é o JDBC e a função dele na aplicação Java?",
  "primary_type": "technical",
  "source": {
    "segment_ids": [
      "RAW-035"
    ],
    "timestamps": [
      "04:56"
    ]
  },
  "question_status": "identified",
  "question_kind": "interviewer_question",
  "evaluation_eligible": true,
  "follow_up_of": null,
  "reformulation_of": null,
  "needs_review": false,
  "response_ids": [
    "R19"
  ]
}
```

### Q7

```json
{
  "question_id": "Q7",
  "text": "Certo, nos projetos que tu já atuou e atua atualmente, vocês usam arquitetura hexagonal ou outro tipo de arquitetura?",
  "primary_type": "technical",
  "source": {
    "segment_ids": [
      "RAW-039"
    ],
    "timestamps": [
      "05:16"
    ]
  },
  "question_status": "identified",
  "question_kind": "interviewer_question",
  "evaluation_eligible": true,
  "follow_up_of": null,
  "reformulation_of": null,
  "needs_review": false,
  "follow_up_ids": [
    "Q8"
  ],
  "response_ids": [
    "R21",
    "R22",
    "R23"
  ]
}
```

### Q9

```json
{
  "question_id": "Q9",
  "text": "Perfeito é sobre investigação assim de análise, problemas, incidentes no geral, tu já chegou a usar alguma ferramenta de observabilidade?",
  "primary_type": "technical",
  "source": {
    "segment_ids": [
      "RAW-049"
    ],
    "timestamps": [
      "06:46"
    ]
  },
  "question_status": "identified",
  "question_kind": "interviewer_question",
  "evaluation_eligible": true,
  "follow_up_of": null,
  "reformulation_of": null,
  "needs_review": false,
  "response_ids": [
    "R25"
  ]
}
```

### Q10

```json
{
  "question_id": "Q10",
  "text": "E que tu não tem conhecimento sobre a funcionalidade, como é que tu iria conduzir a investigação?",
  "primary_type": "technical",
  "source": {
    "segment_ids": [
      "RAW-055"
    ],
    "timestamps": [
      "07:54"
    ]
  },
  "question_status": "identified",
  "question_kind": "interviewer_question",
  "evaluation_eligible": true,
  "follow_up_of": null,
  "reformulation_of": null,
  "needs_review": false,
  "response_ids": [
    "R27",
    "R29",
    "R31"
  ]
}
```

### Q11

```json
{
  "question_id": "Q11",
  "text": "Boa. E falando aí do movimento, do momento, IA, você vem utilizando IA aí no seu dia a dia, como que está? Aí não utiliza muito.",
  "primary_type": "technical",
  "source": {
    "segment_ids": [
      "RAW-066"
    ],
    "timestamps": [
      "08:46"
    ]
  },
  "question_status": "identified",
  "question_kind": "contextual_experiential",
  "evaluation_eligible": true,
  "follow_up_of": null,
  "reformulation_of": null,
  "needs_review": false,
  "response_ids": [
    "R32",
    "R34"
  ]
}
```

## Contextual and follow-up questions preserved

### Q8

```json
{
  "question_id": "Q8",
  "text": "Camada, mas hexagonal tem conhecimento, já chegou a usar.",
  "primary_type": "technical",
  "source": {
    "segment_ids": [
      "RAW-041"
    ],
    "timestamps": [
      "05:31"
    ]
  },
  "question_status": "identified",
  "question_kind": "follow_up",
  "evaluation_eligible": false,
  "follow_up_of": "Q7",
  "reformulation_of": null,
  "needs_review": false,
  "response_ids": []
}
```

### Q12

```json
{
  "question_id": "Q12",
  "text": "E tem uma Daily também, só nossa, né?",
  "primary_type": "technical",
  "source": {
    "segment_ids": [
      "RAW-113"
    ],
    "timestamps": [
      "15:04"
    ]
  },
  "question_status": "identified",
  "question_kind": "contextual_question",
  "evaluation_eligible": false,
  "follow_up_of": null,
  "reformulation_of": null,
  "needs_review": false,
  "response_ids": [
    "R42"
  ]
}
```

## Candidate questions

### CQ1

```json
{
  "id": "RAW-102",
  "timestamp": "13:35",
  "speaker_label": "Ingrid Mazoni",
  "speaker_role": "candidate",
  "text": "Como que é que?",
  "kind": "candidate_question",
  "candidate_question": true,
  "question_id": "CQ1",
  "question_kind": "candidate_question",
  "evaluation_eligible": false,
  "speaker_id": "candidate",
  "participant_id": "P-CANDIDATE",
  "attribution_confidence": "high",
  "needs_review": false
}
```

### CQ2

```json
{
  "id": "RAW-103",
  "timestamp": "13:37",
  "speaker_label": "Ingrid Mazoni",
  "speaker_role": "candidate",
  "text": "Como que é a equipe de trabalho aí? Como que funciona?",
  "kind": "candidate_question",
  "candidate_question": true,
  "question_id": "CQ2",
  "question_kind": "candidate_question",
  "evaluation_eligible": false,
  "speaker_id": "candidate",
  "participant_id": "P-CANDIDATE",
  "attribution_confidence": "high",
  "needs_review": false
}
```

### CQ3

```json
{
  "id": "RAW-131",
  "timestamp": "16:40",
  "speaker_label": "Ingrid Mazoni",
  "speaker_role": "candidate",
  "text": "Quais as tecnologias que vocês usam assim no geral, é Spring e o que mais?",
  "kind": "candidate_question",
  "candidate_question": true,
  "question_id": "CQ3",
  "question_kind": "candidate_question",
  "evaluation_eligible": false,
  "speaker_id": "candidate",
  "participant_id": "P-CANDIDATE",
  "attribution_confidence": "high",
  "needs_review": false
}
```

### CQ4

```json
{
  "id": "RAW-143",
  "timestamp": "17:50",
  "speaker_label": "Ingrid Mazoni",
  "speaker_role": "candidate",
  "text": "Como que a como que a como que é a parte de documentação de API de vocês, vocês usam swagger, essas coisas?",
  "kind": "candidate_question",
  "candidate_question": true,
  "question_id": "CQ4",
  "question_kind": "candidate_question",
  "evaluation_eligible": false,
  "speaker_id": "candidate",
  "participant_id": "P-CANDIDATE",
  "attribution_confidence": "high",
  "needs_review": false
}
```

### CQ5

```json
{
  "id": "RAW-147",
  "timestamp": "18:24",
  "speaker_label": "Ingrid Mazoni",
  "speaker_role": "candidate",
  "text": "E como que chega a demanda para vocês? É, a descrição no card, no Jira, é.",
  "kind": "candidate_question",
  "candidate_question": true,
  "question_id": "CQ5",
  "question_kind": "candidate_question",
  "evaluation_eligible": false,
  "speaker_id": "candidate",
  "participant_id": "P-CANDIDATE",
  "attribution_confidence": "high",
  "needs_review": false
}
```

### CQ6

```json
{
  "id": "RAW-079",
  "timestamp": "10:45",
  "speaker_label": "Ingrid Mazoni",
  "speaker_role": "candidate",
  "text": "É depois de analisar o meu currículo e o meu perfil aqui na entrevista, tem alguma coisa que faltou na opinião de vocês para dar match na vaga?",
  "kind": "candidate_question",
  "candidate_question": true,
  "question_id": "CQ6",
  "question_kind": "candidate_question",
  "evaluation_eligible": false,
  "speaker_id": "candidate",
  "participant_id": "P-CANDIDATE",
  "attribution_confidence": "high",
  "needs_review": false,
  "source": {
    "segment_ids": [
      "RAW-079"
    ],
    "timestamps": [
      "10:45"
    ]
  }
}
```

### CQ7

```json
{
  "id": "RAW-119",
  "timestamp": "15:28",
  "speaker_label": "Ingrid Mazoni",
  "speaker_role": "candidate",
  "text": "E assim, uma dúvida, porque eu já trabalhei em equipe de sustentação e acontecia muitas vezes de não ter acesso a logs, essas coisas, como que é nesse sentido. Para quem está nessa equipe, existe esses acessos?",
  "kind": "candidate_question",
  "candidate_question": true,
  "question_id": "CQ7",
  "question_kind": "candidate_question",
  "evaluation_eligible": false,
  "speaker_id": "candidate",
  "participant_id": "P-CANDIDATE",
  "attribution_confidence": "high",
  "needs_review": false,
  "source": {
    "segment_ids": [
      "RAW-119"
    ],
    "timestamps": [
      "15:28"
    ]
  }
}
```

## Responses and links

Unknown links remain unknown where the transcript does not support a safe association. Candidate questions and conversational utterances remain excluded from evaluation eligibility.

### R1

```json
{
  "response_id": "R1",
  "question_id": "Q1",
  "text": "É muito pouco, bem por cima.",
  "original_segments": [
    "RAW-003"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-003"
    ],
    "timestamps": [
      "00:35"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "É muito pouco, bem por cima.",
  "reconstructed_text": "É muito pouco, bem por cima."
}
```

### R2

```json
{
  "response_id": "R2",
  "question_id": "unknown",
  "text": "Tudo bem.",
  "original_segments": [
    "RAW-009"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-009"
    ],
    "timestamps": [
      "01:36"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Tudo bem.",
  "reconstructed_text": "Tudo bem."
}
```

### R3

```json
{
  "response_id": "R3",
  "question_id": "Q2",
  "text": "Tudo bem. Bem, a minha trajetória com programação, ela começou lá atrás, quando eu fiz o técnico na Etec e depois na Fatec. Na Fatec, o Centro Paula Souza, ali tinha uma parceria com a central de transplantes para fazer um sistema.",
  "original_segments": [
    "RAW-012",
    "RAW-013"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-012",
      "RAW-013"
    ],
    "timestamps": [
      "01:43",
      "01:56"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": true,
  "evaluation_eligible": true,
  "original_text": "Tudo bem. Bem, a minha trajetória com programação, ela começou lá atrás, quando eu fiz o técnico na Etec e depois na Fatec. Na Fatec, o Centro Paula Souza, ali tinha uma parceria com a central de transplantes para fazer um sistema.",
  "reconstructed_text": "Tudo bem. Bem, a minha trajetória com programação, ela começou lá atrás, quando eu fiz o técnico na Etec e depois na Fatec. Na Fatec, o Centro Paula Souza, ali tinha uma parceria com a central de transplantes para fazer um sistema."
}
```

### R4

```json
{
  "response_id": "R4",
  "question_id": "Q2",
  "text": "Ali, porque na época a questão de captação de órgãos era tudo muito manual. Então o objetivo desse sistema era que ocorresse tudo em tempo real, sabe? Eu participei desse projeto e foi o primeiro grande projeto. É assim que eu.",
  "original_segments": [
    "RAW-014"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-014"
    ],
    "timestamps": [
      "02:12"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "Ali, porque na época a questão de captação de órgãos era tudo muito manual. Então o objetivo desse sistema era que ocorresse tudo em tempo real, sabe? Eu participei desse projeto e foi o primeiro grande projeto. É assim que eu.",
  "reconstructed_text": "Ali, porque na época a questão de captação de órgãos era tudo muito manual. Então o objetivo desse sistema era que ocorresse tudo em tempo real, sabe? Eu participei desse projeto e foi o primeiro grande projeto. É assim que eu."
}
```

### R6

```json
{
  "response_id": "R6",
  "question_id": "Q2",
  "text": "Tive a oportunidade de participar, desenvolver. Depois eu entrei na Accenture. Eu estou há quase 8 anos na Accenture e o primeiro projeto que eu peguei foi um cliente bancário, foi o Santander. Na parte de financiamento imobiliário, eu fiquei mais ou menos 5 a 6 anos nesse projeto.",
  "original_segments": [
    "RAW-016",
    "RAW-017"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-016",
      "RAW-017"
    ],
    "timestamps": [
      "02:28",
      "02:44"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "Tive a oportunidade de participar, desenvolver. Depois eu entrei na Accenture. Eu estou há quase 8 anos na Accenture e o primeiro projeto que eu peguei foi um cliente bancário, foi o Santander. Na parte de financiamento imobiliário, eu fiquei mais ou menos 5 a 6 anos nesse projeto.",
  "reconstructed_text": "Tive a oportunidade de participar, desenvolver. Depois eu entrei na Accenture. Eu estou há quase 8 anos na Accenture e o primeiro projeto que eu peguei foi um cliente bancário, foi o Santander. Na parte de financiamento imobiliário, eu fiquei mais ou menos 5 a 6 anos nesse projeto."
}
```

### R7

```json
{
  "response_id": "R7",
  "question_id": "Q2",
  "text": "Então eu via toda a parte de simulação, de financiamento, a parte de gestão de contratos, de financiamento imobiliário e trabalhava muito com desenvolvimento nesse projeto. Eu fiz de",
  "original_segments": [
    "RAW-018"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-018"
    ],
    "timestamps": [
      "02:53"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "Então eu via toda a parte de simulação, de financiamento, a parte de gestão de contratos, de financiamento imobiliário e trabalhava muito com desenvolvimento nesse projeto. Eu fiz de",
  "reconstructed_text": "Então eu via toda a parte de simulação, de financiamento, a parte de gestão de contratos, de financiamento imobiliário e trabalhava muito com desenvolvimento nesse projeto. Eu fiz de"
}
```

### R8

```json
{
  "response_id": "R8",
  "question_id": "Q2",
  "text": "Tudo. Eu passei por várias equipes, então eu trabalhei com legado, eu trabalhei com desenvolvimento de microsserviços, eu trabalhei com a parte de bet.",
  "original_segments": [
    "RAW-019"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-019"
    ],
    "timestamps": [
      "03:08"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "Tudo. Eu passei por várias equipes, então eu trabalhei com legado, eu trabalhei com desenvolvimento de microsserviços, eu trabalhei com a parte de bet.",
  "reconstructed_text": "Tudo. Eu passei por várias equipes, então eu trabalhei com legado, eu trabalhei com desenvolvimento de microsserviços, eu trabalhei com a parte de bet."
}
```

### R9

```json
{
  "response_id": "R9",
  "question_id": "Q2",
  "text": "eu circulei por todas as equipes desse projeto depois é atualmente eu tô no outro cliente bancário só que é a questão de financiamento de alto que é o C6 e",
  "original_segments": [
    "RAW-020"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-020"
    ],
    "timestamps": [
      "03:19"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "eu circulei por todas as equipes desse projeto depois é atualmente eu tô no outro cliente bancário só que é a questão de financiamento de alto que é o C6 e",
  "reconstructed_text": "eu circulei por todas as equipes desse projeto depois é atualmente eu tô no outro cliente bancário só que é a questão de financiamento de alto que é o C6 e"
}
```

### R10

```json
{
  "response_id": "R10",
  "question_id": "Q2",
  "text": "É praticamente a mesma coisa, desenvolvimento de APIs, manutenção, correção de bugs.",
  "original_segments": [
    "RAW-021"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-021"
    ],
    "timestamps": [
      "03:35"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "É praticamente a mesma coisa, desenvolvimento de APIs, manutenção, correção de bugs.",
  "reconstructed_text": "É praticamente a mesma coisa, desenvolvimento de APIs, manutenção, correção de bugs."
}
```

### R12

```json
{
  "response_id": "R12",
  "question_id": "Q3",
  "text": "Yes. Beijava.",
  "original_segments": [
    "RAW-023",
    "RAW-024"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-023",
      "RAW-024"
    ],
    "timestamps": [
      "03:46",
      "03:49"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "Yes. Beijava.",
  "reconstructed_text": "Yes. Java."
}
```

### R14

```json
{
  "response_id": "R14",
  "question_id": "Q3",
  "text": "Is. Isso, só mexer com o back end.",
  "original_segments": [
    "RAW-026",
    "RAW-027"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-026",
      "RAW-027"
    ],
    "timestamps": [
      "03:52",
      "03:54"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "Is. Isso, só mexer com o back end.",
  "reconstructed_text": "Is. Isso, só mexer com o back end."
}
```

### R16

```json
{
  "response_id": "R16",
  "question_id": "Q4",
  "text": "Era começou com a 8, depois mudou para 17 e agora é 21. O pessoal está migrando tudo, não é?",
  "original_segments": [
    "RAW-030"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-030"
    ],
    "timestamps": [
      "04:05"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": true,
  "evaluation_eligible": true,
  "original_text": "Era começou com a 8, depois mudou para 17 e agora é 21. O pessoal está migrando tudo, não é?",
  "reconstructed_text": "Era começou com a 8, depois mudou para 17 e agora é 21. O pessoal está migrando tudo, não é?"
}
```

### R17

```json
{
  "response_id": "R17",
  "question_id": "Q5",
  "text": "Consumers. Bom, quando você fala em producer e consumer, eu lembro muito que ele é da parte de Kafka. Consumer, que eu me lembro, ele pega um item da fila do Kafka ou do Rabbit, e producer, ele joga o item no tópico ou na fila.",
  "original_segments": [
    "RAW-033",
    "RAW-034"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-033",
      "RAW-034"
    ],
    "timestamps": [
      "04:34",
      "04:37"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "Consumers. Bom, quando você fala em producer e consumer, eu lembro muito que ele é da parte de Kafka. Consumer, que eu me lembro, ele pega um item da fila do Kafka ou do Rabbit, e producer, ele joga o item no tópico ou na fila.",
  "reconstructed_text": "Consumers. Bom, quando você fala em producer e consumer, eu lembro muito que ele é da parte de Kafka. Consumer, que eu me lembro, ele pega um item da fila do Kafka ou do Rabbit, e producer, ele joga o item no tópico ou na fila."
}
```

### R19

```json
{
  "response_id": "R19",
  "question_id": "Q6",
  "text": "O JDBC me vem muito ali a é. Configuração com banco, entendeu? Queries, consulta de banco.",
  "original_segments": [
    "RAW-036",
    "RAW-037"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-036",
      "RAW-037"
    ],
    "timestamps": [
      "05:04",
      "05:10"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": true,
  "evaluation_eligible": true,
  "original_text": "O JDBC me vem muito ali a é. Configuração com banco, entendeu? Queries, consulta de banco.",
  "reconstructed_text": "O JDBC me vem muito ali a é. Configuração com banco, entendeu? Queries, consulta de banco."
}
```

### R21

```json
{
  "response_id": "R21",
  "question_id": "Q7",
  "text": "Ele é mais arquitetura em camadas.",
  "original_segments": [
    "RAW-040"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-040"
    ],
    "timestamps": [
      "05:28"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": true,
  "evaluation_eligible": true,
  "original_text": "Ele é mais arquitetura em camadas.",
  "reconstructed_text": "Ele é mais arquitetura em camadas."
}
```

### R22

```json
{
  "response_id": "R22",
  "question_id": "Q7",
  "text": "Eu não cheguei a usar, mas eu tenho conhecimento sim. Eu sei que a parte do hexagonal, ele meio que separa ali a regra de negócio, a lógica do negócio de tecnologias externas. Então, por exemplo, entendeu? Se hoje um sistema ali usa Oracle,",
  "original_segments": [
    "RAW-042"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-042"
    ],
    "timestamps": [
      "05:36"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "Eu não cheguei a usar, mas eu tenho conhecimento sim. Eu sei que a parte do hexagonal, ele meio que separa ali a regra de negócio, a lógica do negócio de tecnologias externas. Então, por exemplo, entendeu? Se hoje um sistema ali usa Oracle,",
  "reconstructed_text": "Eu não cheguei a usar, mas eu tenho conhecimento sim. Eu sei que a parte do hexagonal, ele meio que separa ali a regra de negócio, a lógica do negócio de tecnologias externas. Então, por exemplo, entendeu? Se hoje um sistema ali usa Oracle,"
}
```

### R23

```json
{
  "response_id": "R23",
  "question_id": "Q7",
  "text": "É com essa separação, é muito mais fácil trocar o banco e não afetar o sistema.",
  "original_segments": [
    "RAW-044"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-044"
    ],
    "timestamps": [
      "05:53"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "É com essa separação, é muito mais fácil trocar o banco e não afetar o sistema.",
  "reconstructed_text": "É com essa separação, é muito mais fácil trocar o banco e não afetar o sistema."
}
```

### R24

```json
{
  "response_id": "R24",
  "question_id": "unknown",
  "text": "Não, nenhum.",
  "original_segments": [
    "RAW-048"
  ],
  "response_status": "identified",
  "response_type": "contextual_answer",
  "source": {
    "segment_ids": [
      "RAW-048"
    ],
    "timestamps": [
      "06:43"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Não, nenhum.",
  "reconstructed_text": "Não, nenhum."
}
```

### R25

```json
{
  "response_id": "R25",
  "question_id": "Q9",
  "text": "Sim, é o dyna trace. É, teve uma outra ferramenta agora que eu esqueci o nome, mas foi mais o dyna trace nos últimos tempos.",
  "original_segments": [
    "RAW-050"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-050"
    ],
    "timestamps": [
      "06:58"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "Sim, é o dyna trace. É, teve uma outra ferramenta agora que eu esqueci o nome, mas foi mais o dyna trace nos últimos tempos.",
  "reconstructed_text": "Sim, é o Dynatrace. É, teve uma outra ferramenta agora que eu esqueci o nome, mas foi mais o Dynatrace nos últimos tempos."
}
```

### R26

```json
{
  "response_id": "R26",
  "question_id": "unknown",
  "text": "É na parte de ferramentas de observability, não, mas todo o sistema deles está no o pessoal aqui está no ezure, né? Então todos os repositórios, tudo é no ezure.",
  "original_segments": [
    "RAW-052"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-052"
    ],
    "timestamps": [
      "07:22"
    ]
  },
  "needs_review": true,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "É na parte de ferramentas de observability, não, mas todo o sistema deles está no o pessoal aqui está no ezure, né? Então todos os repositórios, tudo é no ezure.",
  "reconstructed_text": "É na parte de ferramentas de observability, não, mas todo o sistema deles está no o pessoal aqui está no Azure, né? Então todos os repositórios, tudo é no Azure."
}
```

### R27

```json
{
  "response_id": "R27",
  "question_id": "Q10",
  "text": "Debug olhar o log se não tiver acesso a log é printar ali é colocar prints em partes do código e é e acompanhando Acho que tem várias formas de procurar um erro, não é?",
  "original_segments": [
    "RAW-056",
    "RAW-057"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-056",
      "RAW-057"
    ],
    "timestamps": [
      "08:01",
      "08:16"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "Debug olhar o log se não tiver acesso a log é printar ali é colocar prints em partes do código e é e acompanhando Acho que tem várias formas de procurar um erro, não é?",
  "reconstructed_text": "Debug olhar o log se não tiver acesso a log é printar ali é colocar prints em partes do código e é e acompanhando Acho que tem várias formas de procurar um erro, não é?"
}
```

### R29

```json
{
  "response_id": "R29",
  "question_id": "Q10",
  "text": "Mas a principal para mim é o debug subir. local e entendendo, né?",
  "original_segments": [
    "RAW-059",
    "RAW-060"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-059",
      "RAW-060"
    ],
    "timestamps": [
      "08:21",
      "08:26"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "Mas a principal para mim é o debug subir. local e entendendo, né?",
  "reconstructed_text": "Mas a principal para mim é o debug subir. local e entendendo, né?"
}
```

### R31

```json
{
  "response_id": "R31",
  "question_id": "Q10",
  "text": "Scroll.",
  "original_segments": [
    "RAW-065"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-065"
    ],
    "timestamps": [
      "08:44"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "Scroll.",
  "reconstructed_text": "Scroll."
}
```

### R32

```json
{
  "response_id": "R32",
  "question_id": "Q11",
  "text": "Sim, eu utilizo bastante. Hoje eu estou com copilot, mas o pessoal aqui usa cloud é porque a licença aqui não deu para todo mundo, né? Então eu acabei ficando sem a licença do cloud.",
  "original_segments": [
    "RAW-067",
    "RAW-068"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-067",
      "RAW-068"
    ],
    "timestamps": [
      "09:00",
      "09:04"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "Sim, eu utilizo bastante. Hoje eu estou com copilot, mas o pessoal aqui usa cloud é porque a licença aqui não deu para todo mundo, né? Então eu acabei ficando sem a licença do cloud.",
  "reconstructed_text": "Sim, eu utilizo bastante. Hoje eu estou com copilot, mas o pessoal aqui usa cloud é porque a licença aqui não deu para todo mundo, né? Então eu acabei ficando sem a licença do cloud."
}
```

### R34

```json
{
  "response_id": "R34",
  "question_id": "Q11",
  "text": "E eu uso copilot.",
  "original_segments": [
    "RAW-070"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-070"
    ],
    "timestamps": [
      "09:19"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "E eu uso copilot.",
  "reconstructed_text": "E eu uso copilot."
}
```

### R35

```json
{
  "response_id": "R35",
  "question_id": "unknown",
  "text": "Tranquilo.",
  "original_segments": [
    "RAW-075"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-075"
    ],
    "timestamps": [
      "10:09"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": true,
  "evaluation_eligible": false,
  "original_text": "Tranquilo.",
  "reconstructed_text": "Tranquilo."
}
```

### R36

```json
{
  "response_id": "R36",
  "question_id": "unknown",
  "text": "Tudo bem.",
  "original_segments": [
    "RAW-077"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-077"
    ],
    "timestamps": [
      "10:41"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Tudo bem.",
  "reconstructed_text": "Tudo bem."
}
```

### R37

```json
{
  "response_id": "R37",
  "question_id": "unknown",
  "text": "É depois de analisar o meu currículo e o meu perfil aqui na entrevista, tem alguma coisa que faltou na opinião de vocês para dar match na vaga?",
  "original_segments": [
    "RAW-079"
  ],
  "response_status": "identified",
  "response_type": "candidate_question",
  "source": {
    "segment_ids": [
      "RAW-079"
    ],
    "timestamps": [
      "10:45"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "É depois de analisar o meu currículo e o meu perfil aqui na entrevista, tem alguma coisa que faltou na opinião de vocês para dar match na vaga?",
  "reconstructed_text": "É depois de analisar o meu currículo e o meu perfil aqui na entrevista, tem alguma coisa que faltou na opinião de vocês para dar match na vaga?",
  "candidate_question": true
}
```

### R38

```json
{
  "response_id": "R38",
  "question_id": "unknown",
  "text": "Entendi.",
  "original_segments": [
    "RAW-093"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-093"
    ],
    "timestamps": [
      "12:29"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Entendi.",
  "reconstructed_text": "Entendi."
}
```

### R39

```json
{
  "response_id": "R39",
  "question_id": "unknown",
  "text": "Entendi bacana.",
  "original_segments": [
    "RAW-098"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-098"
    ],
    "timestamps": [
      "13:25"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Entendi bacana.",
  "reconstructed_text": "Entendi bacana."
}
```

### R40

```json
{
  "response_id": "R40",
  "question_id": "unknown",
  "text": "É.",
  "original_segments": [
    "RAW-100"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-100"
    ],
    "timestamps": [
      "13:33"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "É.",
  "reconstructed_text": "É."
}
```

### R41

```json
{
  "response_id": "R41",
  "question_id": "unknown",
  "text": "É o dia a dia.",
  "original_segments": [
    "RAW-105"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-105"
    ],
    "timestamps": [
      "13:43"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "É o dia a dia.",
  "reconstructed_text": "É o dia a dia."
}
```

### R42

```json
{
  "response_id": "R42",
  "question_id": "Q12",
  "text": "You think she?",
  "original_segments": [
    "RAW-114"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-114"
    ],
    "timestamps": [
      "15:05"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": true,
  "original_text": "You think she?",
  "reconstructed_text": "You think she?"
}
```

### R43

```json
{
  "response_id": "R43",
  "question_id": "unknown",
  "text": "E assim, uma dúvida, porque eu já trabalhei em equipe de sustentação e acontecia muitas vezes de não ter acesso a logs, essas coisas, como que é nesse sentido. Para quem está nessa equipe, existe esses acessos?",
  "original_segments": [
    "RAW-119"
  ],
  "response_status": "identified",
  "response_type": "candidate_question",
  "source": {
    "segment_ids": [
      "RAW-119"
    ],
    "timestamps": [
      "15:28"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "E assim, uma dúvida, porque eu já trabalhei em equipe de sustentação e acontecia muitas vezes de não ter acesso a logs, essas coisas, como que é nesse sentido. Para quem está nessa equipe, existe esses acessos?",
  "reconstructed_text": "E assim, uma dúvida, porque eu já trabalhei em equipe de sustentação e acontecia muitas vezes de não ter acesso a logs, essas coisas, como que é nesse sentido. Para quem está nessa equipe, existe esses acessos?",
  "candidate_question": true
}
```

### R44

```json
{
  "response_id": "R44",
  "question_id": "unknown",
  "text": "Entendi, bacana.",
  "original_segments": [
    "RAW-121"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-121"
    ],
    "timestamps": [
      "15:53"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Entendi, bacana.",
  "reconstructed_text": "Entendi, bacana."
}
```

### R45

```json
{
  "response_id": "R45",
  "question_id": "unknown",
  "text": "Acho que era isso mesmo de dúvida que eu tinha.",
  "original_segments": [
    "RAW-122"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-122"
    ],
    "timestamps": [
      "15:57"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Acho que era isso mesmo de dúvida que eu tinha.",
  "reconstructed_text": "Acho que era isso mesmo de dúvida que eu tinha."
}
```

### R46

```json
{
  "response_id": "R46",
  "question_id": "unknown",
  "text": "Tudo bem.",
  "original_segments": [
    "RAW-127"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-127"
    ],
    "timestamps": [
      "16:22"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Tudo bem.",
  "reconstructed_text": "Tudo bem."
}
```

### R47

```json
{
  "response_id": "R47",
  "question_id": "unknown",
  "text": "Tudo bem?",
  "original_segments": [
    "RAW-128"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-128"
    ],
    "timestamps": [
      "16:33"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Tudo bem?",
  "reconstructed_text": "Tudo bem?",
  "candidate_question": true
}
```

### R48

```json
{
  "response_id": "R48",
  "question_id": "unknown",
  "text": "Entendi.",
  "original_segments": [
    "RAW-135"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-135"
    ],
    "timestamps": [
      "17:29"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Entendi.",
  "reconstructed_text": "Entendi."
}
```

### R49

```json
{
  "response_id": "R49",
  "question_id": "unknown",
  "text": "Beleza.",
  "original_segments": [
    "RAW-136"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-136"
    ],
    "timestamps": [
      "17:33"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Beleza.",
  "reconstructed_text": "Beleza."
}
```

### R50

```json
{
  "response_id": "R50",
  "question_id": "unknown",
  "text": "Eu estou pensando aqui.",
  "original_segments": [
    "RAW-140"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-140"
    ],
    "timestamps": [
      "17:40"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Eu estou pensando aqui.",
  "reconstructed_text": "Eu estou pensando aqui."
}
```

### R51

```json
{
  "response_id": "R51",
  "question_id": "unknown",
  "text": "Entendi.",
  "original_segments": [
    "RAW-146"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-146"
    ],
    "timestamps": [
      "18:22"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Entendi.",
  "reconstructed_text": "Entendi."
}
```

### R52

```json
{
  "response_id": "R52",
  "question_id": "unknown",
  "text": "Tem.",
  "original_segments": [
    "RAW-149"
  ],
  "response_status": "identified",
  "response_type": "direct",
  "source": {
    "segment_ids": [
      "RAW-149"
    ],
    "timestamps": [
      "18:33"
    ]
  },
  "needs_review": true,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Tem.",
  "reconstructed_text": "Tem."
}
```

### R53

```json
{
  "response_id": "R53",
  "question_id": "unknown",
  "text": "Entendi.",
  "original_segments": [
    "RAW-151"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-151"
    ],
    "timestamps": [
      "19:06"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Entendi.",
  "reconstructed_text": "Entendi."
}
```

### R54

```json
{
  "response_id": "R54",
  "question_id": "unknown",
  "text": "Acho que eu não tenho mais dúvidas.",
  "original_segments": [
    "RAW-153"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-153"
    ],
    "timestamps": [
      "19:13"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Acho que eu não tenho mais dúvidas.",
  "reconstructed_text": "Acho que eu não tenho mais dúvidas."
}
```

### R55

```json
{
  "response_id": "R55",
  "question_id": "unknown",
  "text": "Eu perguntei bastante coisa, né?",
  "original_segments": [
    "RAW-155"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-155"
    ],
    "timestamps": [
      "19:18"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": false,
  "evaluation_eligible": false,
  "original_text": "Eu perguntei bastante coisa, né?",
  "reconstructed_text": "Eu perguntei bastante coisa, né?",
  "candidate_question": true
}
```

### R56

```json
{
  "response_id": "R56",
  "question_id": "unknown",
  "text": "Eu que agradeço a disponibilidade de vocês e a possibilidade de participar do processo aqui com vocês.",
  "original_segments": [
    "RAW-163"
  ],
  "response_status": "identified",
  "response_type": "conversational",
  "source": {
    "segment_ids": [
      "RAW-163"
    ],
    "timestamps": [
      "19:54"
    ]
  },
  "needs_review": false,
  "speaker_id": "candidate",
  "reconstruction_confidence": null,
  "prompted_by_interviewer": true,
  "evaluation_eligible": false,
  "original_text": "Eu que agradeço a disponibilidade de vocês e a possibilidade de participar do processo aqui com vocês.",
  "reconstructed_text": "Eu que agradeço a disponibilidade de vocês e a possibilidade de participar do processo aqui com vocês."
}
```

## Follow-up structure

```yaml
Q7:
  follow_up: Q8
  response_ids: [R21, R22, R23]
Q8:
  relation: clarification_or_continuation
  evaluation_eligible: false
```

Q8 is retained for traceability but is not an independent evaluation question. The initial layered-architecture response and the later hexagonal-knowledge response remain separate.

## Reconstruction metadata

```json
[
  {
    "id": "T01",
    "original_text": "Beijava",
    "reconstructed_text": "Java",
    "source_segment_ids": [
      "RAW-023",
      "RAW-024"
    ],
    "reconstruction_confidence": "high",
    "needs_review": false,
    "rationale": "technical context lists Java, C Sharpe and Angula"
  },
  {
    "id": "T02",
    "original_text": "C Sharpe",
    "reconstructed_text": "C#",
    "source_segment_ids": [
      "RAW-022"
    ],
    "reconstruction_confidence": "high",
    "needs_review": false,
    "rationale": "form correction only"
  },
  {
    "id": "T03",
    "original_text": "Angula",
    "reconstructed_text": "Angular",
    "source_segment_ids": [
      "RAW-022"
    ],
    "reconstruction_confidence": "high",
    "needs_review": false,
    "rationale": "form correction only"
  },
  {
    "id": "T04",
    "original_text": "produtos e consumes",
    "reconstructed_text": "producers e consumers",
    "source_segment_ids": [
      "RAW-032"
    ],
    "reconstruction_confidence": "high",
    "needs_review": false,
    "rationale": "question wording normalization only"
  },
  {
    "id": "T05",
    "original_text": "dyna trace",
    "reconstructed_text": "Dynatrace",
    "source_segment_ids": [
      "RAW-050"
    ],
    "reconstruction_confidence": "high",
    "needs_review": false,
    "rationale": "term form normalization only"
  },
  {
    "id": "T06",
    "original_text": "ezure",
    "reconstructed_text": "Azure",
    "source_segment_ids": [
      "RAW-052"
    ],
    "reconstruction_confidence": "high",
    "needs_review": false,
    "rationale": "term form normalization only"
  },
  {
    "id": "T07",
    "original_text": "Lego Analytics",
    "reconstructed_text": "Log Analytics",
    "source_segment_ids": [
      "RAW-051"
    ],
    "reconstruction_confidence": "high",
    "needs_review": false,
    "rationale": "interviewer speech only; never candidate evidence"
  },
  {
    "id": "T08",
    "original_text": "ZepSight",
    "reconstructed_text": null,
    "source_segment_ids": [
      "RAW-051"
    ],
    "reconstruction_confidence": "low",
    "needs_review": true,
    "rationale": "ambiguous; no external lookup"
  },
  {
    "id": "T09",
    "original_text": "Springwood",
    "reconstructed_text": "Spring Boot",
    "source_segment_ids": [
      "RAW-132"
    ],
    "reconstruction_confidence": "high",
    "needs_review": false,
    "rationale": "contextual form reconstruction only; interviewer speech"
  }
]
```

T08 (`ZepSight`) remains unreconstructed with low confidence and `needs_review: true`. No external search was used.

## Human review applications

The following decisions were explicitly applied from the supplied review instructions: acknowledgements and closings were made non-evaluable; R37 and R43 were preserved as candidate questions; R26 and R52 remain unknown with review; Q8 became a Q7 follow-up; Q12 became contextual/non-evaluable; NR01?NR13 were structurally classified; T01?T07 and T09 received form-only reconstructions; T08 remained ambiguous; and D01?D03 remain historically indeterminate.

## Response-count discrepancy

```yaml
v3_responses: 44
v4_responses: 47
additional_units: 3
correspondence_to_v3: unknown
human_decision: PENDING_FOR_HISTORICAL_MAPPING_ONLY
structural_effect: no retroactive v3 mutation
```

The three additional units are not asserted to be R2, R24 or R26. Those records are retained as the comparison set required by the human decision, not as a historical claim.

## Stage 20.7 validation

```yaml
status: READY_WITH_WARNINGS
errors: 0
errors_detail: []
warnings: 4
warnings_detail: ["4 unresolved unknown links retained safely", "ZepSight remains ambiguous and unreconstructed", "historical correspondence of v3 44?v4 47 cannot be determined from aggregate v3 artifact", "candidate questions and contextual/interviewer units preserved outside technical evaluation"]
questions: 12
evaluation_questions: 10
responses: 47
unanswered_evaluation_questions: 0
unlinked_responses: 4
needs_review: 2 responses + 1 ambiguous reconstruction + historical count mapping
traceability: PASS
participant_integrity: PASS
speaker_attribution: PASS
question_integrity: PASS
response_integrity: PASS
reconstruction_integrity: PASS
linking_integrity: PASS
evidence_boundary: PASS
readiness_for_evidence_model: APPROVED_WITH_WARNINGS
evidence_model_executed: false
evaluation_engine_executed: false
```

## Gate

```text
STRUCTURED_INTERVIEW_HUMAN_REVIEW_COMPLETE
STRUCTURED_INTERVIEW_APPROVED_WITH_WARNINGS
STATUS: READY_WITH_WARNINGS
DOWNSTREAM_EVIDENCE_MODEL: ALLOWED_BY_GATE_BUT_NOT_EXECUTED
DOWNSTREAM_EVALUATION_ENGINE: NOT_EXECUTED
FINAL_REPORT: NOT_CREATED
```

## Protections

- Transcript v3 preserved.
- Structured Interview v4 preserved.
- Human Review Matrix v4 preserved.
- No Rubric, Evidence Model or Evaluation Engine changes.
- No score, average, ranking, seniority or hiring decision produced.
- No final interview report created or modified.
- No external source was used.
