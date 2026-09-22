---
type: reference
status: learning
confidence: 100
created: 2026-09-22
updated: 2026-09-22
tags:
  - interview-evaluation
  - rubric
  - individual-evaluations
  - real-interview-pilot
---

# Stage 22 — Individual Evaluations v1

## Metadata

```yaml
stage: 22
status: RUBRIC_COMPLETE_WITH_WARNINGS
candidate: Candidato-Piloto-01
interview: REAL-PILOT-2026-09-14-01-v6
source_evidence_set: Evidence Set v1.md
rubric: Scoring Rubric.md
evaluation_engine: not_executed
global_consolidation: not_executed
overall_average: not_created
final_report: not_created
```

This artifact contains only individual question evaluations. It does not consolidate the interview, calculate an overall average, evaluate seniority, apply Job Context, or make a hiring decision.

For questions with more than one upstream response, `response.id` is represented as a list so every source response remains explicit. This is a traceability-only representation; it is not a new aggregation stage.

## Input gate

```yaml
pipeline_gate:
  stage_20_7: READY_WITH_WARNINGS
  human_review: PASS
  semantic_audit: PASS_WITH_WARNINGS
  stage_21: COMPLETE_WITH_WARNINGS
  accepted_for_stage_22: true
```

## Evaluation summary

```yaml
questions_evaluated: [Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q9, Q10, Q11]
questions_excluded: [Q8, Q12]
evidence_items_available: 28
evidence_items_used: 28
evidence_items_excluded_from_evaluation: 0
individual_evaluations: 10
global_score: not_created
global_average: not_created
```

## EV-Q1 — Q1

```yaml
evaluation:
  id: EV-Q1
  question:
    id: Q1
    text: "Você já ouviu falar um pouquinho do projeto open finance?"
    version: "Structured Interview v6"
    domain: [open_finance, project_context]
    primary_type: experience
    secondary_dimensions: [familiarity]
    complexity: basic
  response:
    id: [R1]
    text: "É muito pouco, bem por cima."
    source:
      segment_ids: [RAW-003]
  expected:
    essential: [descrever o grau de familiaridade com o projeto]
    relevant: [fornecer algum contexto sobre o projeto]
    optional: []
    contextual: [a resposta trata de familiaridade, não de uma explicação técnica extensa]
  weights:
    original: {correctness: 40, completeness: 20, depth: 15, reasoning: 10, practical_application: 10, trade_offs: 5}
    normalized: {correctness: 0.666667, completeness: 0.333333, depth: null, reasoning: null, practical_application: null, trade_offs: null}
  evidence:
    positive: []
    partial: []
    negative: []
    contradictory: []
    absent: []
    insufficient: [E-001]
  dimensions:
    correctness:
      applicable: true
      assessment: "A resposta é coerente com a pergunta de familiaridade, mas não fornece conteúdo técnico do projeto para uma verificação mais ampla."
      evidence: [E-001]
    completeness:
      applicable: true
      assessment: "Baixa: informa apenas que o contato foi superficial e não apresenta contexto adicional."
      evidence: [E-001]
    depth:
      applicable: false
      assessment: "N/A"
      evidence: []
    reasoning:
      applicable: false
      assessment: "N/A"
      evidence: []
    practical_application:
      applicable: false
      assessment: "N/A"
      evidence: []
    trade_offs:
      applicable: false
      assessment: "N/A"
      evidence: []
  score:
    value: 2.0
    confidence: high
  findings:
    strengths: ["Responde diretamente sobre o grau de familiaridade."]
    gaps: ["Não há demonstração de conhecimento ou experiência específica sobre o projeto."]
    errors: []
  rationale: "E-001 sustenta apenas familiaridade superficial. A resposta atende minimamente à pergunta, mas não demonstra conhecimento do projeto além de 'bem por cima'. A nota baixa representa a evidência limitada, não uma conclusão sobre o conhecimento geral da candidata."
  related_knowledge: []
```

## EV-Q2 — Q2

```yaml
evaluation:
  id: EV-Q2
  question:
    id: Q2
    text: "Conte sobre sua experiência profissional, projetos e contexto de atuação."
    version: "Structured Interview v6"
    domain: [professional_experience, software_projects]
    primary_type: experience
    secondary_dimensions: [practical_application]
    complexity: intermediate
  response:
    id: [R3, R4, R6, R7, R8, R9, R10]
    text: "Respostas compostas sobre formação, projetos, atuação bancária, financiamento, legado, microsserviços, APIs, manutenção e correção de bugs."
    source:
      segment_ids: [RAW-012, RAW-013, RAW-014, RAW-016, RAW-017, RAW-018, RAW-019, RAW-020, RAW-021]
  expected:
    essential: [relatar experiências e projetos relevantes]
    relevant: [descrever contexto, responsabilidades e atividades]
    optional: [explicar decisões técnicas, resultados ou trade-offs]
    contextual: [a pergunta é ampla e permite resposta composta]
  weights:
    original: {correctness: 40, completeness: 20, depth: 15, reasoning: 10, practical_application: 10, trade_offs: 5}
    normalized: {correctness: 0.470588, completeness: 0.235294, depth: 0.176471, reasoning: null, practical_application: 0.117647, trade_offs: null}
  evidence:
    positive: [E-002, E-003, E-004, E-006, E-008]
    partial: [E-005, E-007]
    negative: []
    contradictory: []
    absent: []
    insufficient: []
  dimensions:
    correctness:
      applicable: true
      assessment: "Boa no nível declarativo e descritivo: a candidata apresenta trajetória, projetos e atividades sem contradição observável no conjunto avaliado."
      evidence: [E-002, E-003, E-004, E-006, E-008]
    completeness:
      applicable: true
      assessment: "Média: cobre diversos projetos, domínios e atividades, mas há trechos incompletos e poucos detalhes sobre decisões, resultados ou responsabilidades técnicas específicas."
      evidence: [E-003, E-005, E-007, E-008]
    depth:
      applicable: true
      assessment: "Moderada-baixa: há contexto de projetos e atividades, mas a resposta permanece principalmente descritiva."
      evidence: [E-003, E-004, E-005, E-008]
    reasoning:
      applicable: false
      assessment: "N/A"
      evidence: []
    practical_application:
      applicable: true
      assessment: "Moderada: são mencionadas atividades concretas como desenvolvimento de APIs, manutenção, correção de bugs e atuação em projetos de financiamento."
      evidence: [E-003, E-005, E-008]
    trade_offs:
      applicable: false
      assessment: "N/A"
      evidence: []
  score:
    value: 6.0
    confidence: high
  findings:
    strengths: ["Relata múltiplos projetos e contextos de atuação.", "Menciona atividades práticas concretas."]
    gaps: ["Alguns trechos terminam incompletos.", "Não detalha decisões técnicas, resultados ou trade-offs."]
    errors: []
  rationale: "E-002 a E-008 demonstram experiência contextual e algumas atividades práticas. A cobertura é suficiente para uma resposta adequada à pergunta ampla, mas a profundidade técnica e a completude são limitadas. O score não usa tempo de carreira ou empresas como bônus; considera apenas o conteúdo efetivamente descrito."
  related_knowledge: []
```

## EV-Q3 — Q3

```yaml
evaluation:
  id: EV-Q3
  question:
    id: Q3
    text: "Quais tecnologias você utilizou nesses projetos?"
    version: "Structured Interview v6"
    domain: [technology_experience]
    primary_type: factual
    secondary_dimensions: [experience]
    complexity: basic
  response:
    id: [R12, R14]
    text: "Yes. Beijava. Is. Isso, só mexer com o back end."
    source:
      segment_ids: [RAW-023, RAW-024, RAW-026, RAW-027]
  expected:
    essential: [mencionar tecnologias efetivamente utilizadas]
    relevant: [distinguir tecnologia e área de atuação]
    optional: [contextualizar uso de cada tecnologia]
    contextual: []
  weights:
    original: {correctness: 40, completeness: 20, depth: 15, reasoning: 10, practical_application: 10, trade_offs: 5}
    normalized: {correctness: 0.571429, completeness: 0.285714, depth: null, reasoning: null, practical_application: 0.142857, trade_offs: null}
  evidence:
    positive: [E-009]
    partial: [E-010]
    negative: []
    contradictory: []
    absent: []
    insufficient: []
  dimensions:
    correctness:
      applicable: true
      assessment: "A menção reconstruída de Java é sustentada com alta confiança; 'back end' descreve área de atuação, não uma tecnologia específica."
      evidence: [E-009, E-010]
    completeness:
      applicable: true
      assessment: "Baixa: apenas Java é identificada como tecnologia e a resposta não apresenta a lista de tecnologias solicitada."
      evidence: [E-009]
    depth:
      applicable: false
      assessment: "N/A"
      evidence: []
    reasoning:
      applicable: false
      assessment: "N/A"
      evidence: []
    practical_application:
      applicable: true
      assessment: "Limitada: a atuação no back end é mencionada, mas sem explicar como as tecnologias eram utilizadas."
      evidence: [E-009, E-010]
    trade_offs:
      applicable: false
      assessment: "N/A"
      evidence: []
  score:
    value: 4.0
    confidence: high
  findings:
    strengths: ["Menciona Java.", "Indica atuação no back end."]
    gaps: ["Não fornece uma relação suficiente das tecnologias utilizadas.", "Não detalha aplicação."]
    errors: []
  rationale: "E-009 e E-010 sustentam apenas uma tecnologia e uma área de atuação. A resposta é parcialmente responsiva, mas cobre pouco do escopo solicitado. Não foram inferidas C#, Angular ou outras tecnologias a partir da pergunta do entrevistador."
  related_knowledge: []
```

## EV-Q4 — Q4

```yaml
evaluation:
  id: EV-Q4
  question:
    id: Q4
    text: "Qual era a versão do Java utilizada?"
    version: "Structured Interview v6"
    domain: [java, versioning]
    primary_type: factual
    secondary_dimensions: [experience]
    complexity: basic
  response:
    id: [R16]
    text: "Era começou com a 8, depois mudou para 17 e agora é 21."
    source:
      segment_ids: [RAW-030]
  expected:
    essential: [informar a versão ou sequência de versões mencionada]
    relevant: [distinguir versões utilizadas em momentos diferentes]
    optional: [explicar o motivo da migração]
    contextual: []
  weights:
    original: {correctness: 40, completeness: 20, depth: 15, reasoning: 10, practical_application: 10, trade_offs: 5}
    normalized: {correctness: 0.666667, completeness: 0.333333, depth: null, reasoning: null, practical_application: null, trade_offs: null}
  evidence:
    positive: [E-011]
    partial: []
    negative: []
    contradictory: []
    absent: []
    insufficient: []
  dimensions:
    correctness:
      applicable: true
      assessment: "Forte para o escopo da pergunta: a sequência Java 8, Java 17 e Java 21 é apresentada diretamente."
      evidence: [E-011]
    completeness:
      applicable: true
      assessment: "Alta para a pergunta de versão; a resposta informa a sequência solicitada."
      evidence: [E-011]
    depth:
      applicable: false
      assessment: "N/A"
      evidence: []
    reasoning:
      applicable: false
      assessment: "N/A"
      evidence: []
    practical_application:
      applicable: false
      assessment: "N/A"
      evidence: []
    trade_offs:
      applicable: false
      assessment: "N/A"
      evidence: []
  score:
    value: 8.0
    confidence: high
  findings:
    strengths: ["Responde diretamente com uma sequência de versões."]
    gaps: ["O motivo ou impacto da migração não é detalhado, mas isso era opcional para a pergunta."]
    errors: []
  rationale: "E-011 atende diretamente ao núcleo da pergunta. A ausência de explicação sobre migração não reduz a completude essencial, pois a pergunta solicitou a versão utilizada. A nota não exige profundidade ou trade-offs que não foram solicitados."
  related_knowledge: []
```

## EV-Q5 — Q5

```yaml
evaluation:
  id: EV-Q5
  question:
    id: Q5
    text: "Qual é a diferença entre producers e consumers em uma API REST?"
    version: "Structured Interview v6"
    domain: [rest_api, messaging]
    primary_type: conceptual
    secondary_dimensions: [comparison]
    complexity: intermediate
  response:
    id: [R17]
    text: "A candidata associa producer e consumer a Kafka/Rabbit e descreve consumer como algo que pega um item e producer como algo que coloca um item no tópico ou fila."
    source:
      segment_ids: [RAW-033, RAW-034]
  expected:
    essential: [explicar a diferença solicitada no contexto da pergunta]
    relevant: [distinguir responsabilidades dos dois termos]
    optional: [relacionar a implementação ao framework ou protocolo específico]
    contextual: [a resposta deve ser interpretada no contexto explícito de API REST]
  weights:
    original: {correctness: 40, completeness: 20, depth: 15, reasoning: 10, practical_application: 10, trade_offs: 5}
    normalized: {correctness: 0.533333, completeness: 0.266667, depth: 0.2, reasoning: null, practical_application: null, trade_offs: null}
  evidence:
    positive: []
    partial: [E-012, E-013, E-014]
    negative: []
    contradictory: []
    absent: []
    insufficient: []
  dimensions:
    correctness:
      applicable: true
      assessment: "Fraca em relação ao contexto perguntado: a resposta descreve papéis de mensageria em Kafka/Rabbit, mas não estabelece a diferença solicitada em uma API REST."
      evidence: [E-012, E-013, E-014]
    completeness:
      applicable: true
      assessment: "Baixa: não aborda o enquadramento REST pedido."
      evidence: [E-012, E-013, E-014]
    depth:
      applicable: true
      assessment: "Limitada: há uma distinção básica entre producer e consumer no contexto apresentado, sem aprofundamento aplicável ao contexto REST."
      evidence: [E-013, E-014]
    reasoning:
      applicable: false
      assessment: "N/A"
      evidence: []
    practical_application:
      applicable: false
      assessment: "N/A"
      evidence: []
    trade_offs:
      applicable: false
      assessment: "N/A"
      evidence: []
  score:
    value: 4.0
    confidence: high
  findings:
    strengths: ["Distingue, em algum nível, as funções de producer e consumer no contexto de fila/tópico."]
    gaps: ["Não responde ao contexto explícito de API REST.", "Não apresenta comparação aplicável ao que foi perguntado."]
    errors:
      - type: central
        severity: central
        evidence_id: E-012
        description: "A resposta desloca o contexto para mensageria Kafka/Rabbit e não responde à formulação sobre API REST."
  rationale: "E-012 a E-014 sustentam conteúdo observável sobre mensageria, mas o contexto da pergunta era API REST. O erro é central para a aderência ao escopo, embora exista algum conteúdo conceitual relacionado aos termos. Por isso a nota é parcial, não zero."
  related_knowledge: []
```

## EV-Q6 — Q6

```yaml
evaluation:
  id: EV-Q6
  question:
    id: Q6
    text: "O que é JDBC e qual é sua função na aplicação Java?"
    version: "Structured Interview v6"
    domain: [java, jdbc, database_access]
    primary_type: conceptual
    secondary_dimensions: [implementation]
    complexity: intermediate
  response:
    id: [R19]
    text: "O JDBC é associado a configuração com banco, queries e consulta de banco."
    source:
      segment_ids: [RAW-036, RAW-037]
  expected:
    essential: [explicar o papel de JDBC na aplicação Java]
    relevant: [relacionar JDBC ao acesso ou consulta a banco]
    optional: [detalhar mecanismo ou fluxo de implementação]
    contextual: []
  weights:
    original: {correctness: 40, completeness: 20, depth: 15, reasoning: 10, practical_application: 10, trade_offs: 5}
    normalized: {correctness: 0.470588, completeness: 0.235294, depth: 0.176471, reasoning: null, practical_application: 0.117647, trade_offs: null}
  evidence:
    positive: []
    partial: [E-015, E-016]
    negative: []
    contradictory: []
    absent: []
    insufficient: []
  dimensions:
    correctness:
      applicable: true
      assessment: "Parcial: a resposta relaciona JDBC a banco, queries e consultas, mas não explica claramente sua função como mecanismo de acesso."
      evidence: [E-015, E-016]
    completeness:
      applicable: true
      assessment: "Baixa: cobre apenas a associação geral com banco e consultas."
      evidence: [E-015, E-016]
    depth:
      applicable: true
      assessment: "Baixa: não há explicação de funcionamento, responsabilidades ou fluxo."
      evidence: [E-015, E-016]
    reasoning:
      applicable: false
      assessment: "N/A"
      evidence: []
    practical_application:
      applicable: true
      assessment: "Limitada: queries e consulta de banco são mencionadas, mas não há procedimento ou exemplo de uso."
      evidence: [E-016]
    trade_offs:
      applicable: false
      assessment: "N/A"
      evidence: []
  score:
    value: 4.0
    confidence: high
  findings:
    strengths: ["Relaciona JDBC a banco de dados e consultas."]
    gaps: ["Não explica suficientemente a função do JDBC na aplicação Java.", "Não detalha mecanismo ou uso."]
    errors: []
  rationale: "E-015 e E-016 fornecem uma associação correta em nível geral, mas insuficiente para cobrir a explicação solicitada. A nota reconhece a parte demonstrada sem converter a falta de detalhes em afirmação de desconhecimento."
  related_knowledge: []
```

## EV-Q7 — Q7

```yaml
evaluation:
  id: EV-Q7
  question:
    id: Q7
    text: "Nos projetos, vocês usam arquitetura hexagonal ou outro tipo de arquitetura?"
    version: "Structured Interview v6"
    domain: [software_architecture, layered_architecture, hexagonal_architecture]
    primary_type: architecture
    secondary_dimensions: [experience, reasoning]
    complexity: intermediate
  response:
    id: [R21, R22, R23]
    text: "A candidata identifica arquitetura em camadas como a utilizada, declara não ter usado arquitetura hexagonal, descreve separação entre regra de negócio e tecnologias externas e relaciona isso à troca de banco."
    source:
      segment_ids: [RAW-040, RAW-042, RAW-044]
  expected:
    essential: [identificar a arquitetura utilizada ou conhecida]
    relevant: [explicar responsabilidades, separação e consequências]
    optional: [descrever aplicação prática ou trade-offs]
    contextual: [Q8 é continuação/follow-up de Q7 e não gera avaliação independente]
  weights:
    original: {correctness: 40, completeness: 20, depth: 15, reasoning: 10, practical_application: 10, trade_offs: 5}
    normalized: {correctness: 0.421053, completeness: 0.210526, depth: 0.157895, reasoning: 0.105263, practical_application: 0.105263, trade_offs: null}
  evidence:
    positive: [E-017, E-018, E-020]
    partial: [E-019]
    negative: []
    contradictory: []
    absent: []
  dimensions:
    correctness:
      applicable: true
      assessment: "Boa: a resposta descreve arquitetura em camadas como contexto utilizado e apresenta uma descrição coerente da separação associada à arquitetura hexagonal."
      evidence: [E-017, E-018, E-019]
    completeness:
      applicable: true
      assessment: "Média: responde ao tipo de arquitetura e fornece explicação, mas o exemplo termina incompleto e não detalha toda a aplicação."
      evidence: [E-017, E-019]
    depth:
      applicable: true
      assessment: "Moderada: há relação entre separação arquitetural e troca de banco, além da distinção entre uso e conhecimento declarado."
      evidence: [E-018, E-019, E-020]
    reasoning:
      applicable: true
      assessment: "Boa em escala limitada: E-020 explicita uma consequência da separação apresentada."
      evidence: [E-020]
    practical_application:
      applicable: true
      assessment: "Parcial: a candidata declara não ter usado arquitetura hexagonal; a aplicação observável está mais associada à arquitetura em camadas mencionada."
      evidence: [E-017, E-018]
    trade_offs:
      applicable: false
      assessment: "N/A"
      evidence: []
  score:
    value: 7.0
    confidence: high
  findings:
    strengths: ["Identifica arquitetura em camadas.", "Explica separação entre negócio e tecnologia externa.", "Relaciona a separação à troca de banco."]
    gaps: ["Uso prático de arquitetura hexagonal não foi demonstrado.", "O exemplo termina incompleto.", "Não há discussão de trade-offs."]
    errors: []
  rationale: "E-017 a E-020 sustentam uma resposta arquitetural adequada, com raciocínio observável sobre a consequência da separação. A nota fica abaixo de forte/10 porque a experiência prática com arquitetura hexagonal foi explicitamente negada e o exemplo permanece parcial. Q8 não foi avaliada separadamente."
  related_knowledge: []
```

## EV-Q9 — Q9

```yaml
evaluation:
  id: EV-Q9
  question:
    id: Q9
    text: "Você já utilizou alguma ferramenta de observabilidade?"
    version: "Structured Interview v6"
    domain: [observability, tools]
    primary_type: experience
    secondary_dimensions: [practical_application]
    complexity: basic
  response:
    id: [R25]
    text: "Sim, é o Dynatrace. Também houve outra ferramenta cujo nome a candidata não lembra."
    source:
      segment_ids: [RAW-050]
  expected:
    essential: [informar se alguma ferramenta foi utilizada]
    relevant: [identificar a ferramenta]
    optional: [descrever uso, investigação ou contexto]
    contextual: []
  weights:
    original: {correctness: 40, completeness: 20, depth: 15, reasoning: 10, practical_application: 10, trade_offs: 5}
    normalized: {correctness: 0.571429, completeness: 0.285714, depth: null, reasoning: null, practical_application: 0.142857, trade_offs: null}
  evidence:
    positive: [E-021]
    partial: []
    negative: []
    contradictory: []
    absent: []
    insufficient: [E-022]
  dimensions:
    correctness:
      applicable: true
      assessment: "A resposta identifica explicitamente Dynatrace como ferramenta utilizada."
      evidence: [E-021]
    completeness:
      applicable: true
      assessment: "Média-baixa: responde à existência e identifica uma ferramenta, mas não descreve como ela foi utilizada."
      evidence: [E-021, E-022]
    depth:
      applicable: false
      assessment: "N/A"
      evidence: []
    reasoning:
      applicable: false
      assessment: "N/A"
      evidence: []
    practical_application:
      applicable: true
      assessment: "Baixa: há declaração de uso, sem investigação, configuração, decisão ou exemplo operacional."
      evidence: [E-021]
    trade_offs:
      applicable: false
      assessment: "N/A"
      evidence: []
  score:
    value: 4.0
    confidence: high
  findings:
    strengths: ["Responde afirmativamente e identifica Dynatrace."]
    gaps: ["Não demonstra aplicação prática da ferramenta.", "Outra ferramenta é mencionada sem nome."]
    errors: []
  rationale: "E-021 responde ao núcleo factual da pergunta, enquanto E-022 preserva a lembrança incompleta de outra ferramenta. Como a pergunta solicita apenas se alguma ferramenta foi utilizada, a resposta é parcialmente adequada; a ausência de detalhes limita a aplicação prática, mas não é tratada como erro técnico."
  related_knowledge: []
```

## EV-Q10 — Q10

```yaml
evaluation:
  id: EV-Q10
  question:
    id: Q10
    text: "Se você não tem conhecimento sobre a funcionalidade, como conduziria a investigação?"
    version: "Structured Interview v6"
    domain: [troubleshooting, debugging, investigation]
    primary_type: scenario
    secondary_dimensions: [reasoning, practical_application]
    complexity: intermediate
  response:
    id: [R27, R29, R31]
    text: "A candidata menciona olhar logs, inserir prints quando não houver logs, acompanhar, subir o debug localmente e 'Scroll'."
    source:
      segment_ids: [RAW-056, RAW-057, RAW-059, RAW-060, RAW-065]
  expected:
    essential: [propor uma abordagem de investigação]
    relevant: [indicar coleta de sinais, reprodução ou isolamento do problema]
    optional: [explicar hipóteses, validação e próximos passos]
    contextual: [a resposta é hipotética e não deve ser convertida em experiência demonstrada]
  weights:
    original: {correctness: 40, completeness: 20, depth: 15, reasoning: 10, practical_application: 10, trade_offs: 5}
    normalized: {correctness: 0.421053, completeness: 0.210526, depth: 0.157895, reasoning: 0.105263, practical_application: 0.105263, trade_offs: null}
  evidence:
    positive: []
    partial: [E-023, E-024, E-025, E-026]
    negative: []
    contradictory: []
    absent: []
    insufficient: []
  dimensions:
    correctness:
      applicable: true
      assessment: "Parcialmente adequada: logs, instrumentação por prints e debug local são abordagens plausíveis de investigação no contexto descrito."
      evidence: [E-023, E-024, E-026]
    completeness:
      applicable: true
      assessment: "Baixa-média: há algumas ações, mas não é apresentado um fluxo completo de hipótese, isolamento, validação e conclusão."
      evidence: [E-023, E-024, E-026]
    depth:
      applicable: true
      assessment: "Baixa: as ações são listadas sem explicar mecanismos, critérios de escolha ou validação dos resultados."
      evidence: [E-023, E-024, E-026]
    reasoning:
      applicable: true
      assessment: "Parcial: existe uma preferência por debug local e alternativas quando não há logs, mas a sequência de raciocínio não é desenvolvida."
      evidence: [E-023, E-024, E-026]
    practical_application:
      applicable: true
      assessment: "Moderada-baixa: as ações propostas são operacionais, porém não há exemplo de execução, resultado ou diagnóstico."
      evidence: [E-023, E-024, E-026]
    trade_offs:
      applicable: false
      assessment: "N/A"
      evidence: []
  score:
    value: 4.0
    confidence: high
  findings:
    strengths: ["Menciona logs.", "Propõe prints quando não há acesso a logs.", "Menciona debug local."]
    gaps: ["Não estrutura hipóteses e validação.", "Não explica como isolaria a causa.", "R31 não foi usado como evidência independente por insuficiência contextual."]
    errors: []
  rationale: "E-023, E-024 e E-026 demonstram algumas ações de troubleshooting, mas a resposta não apresenta uma estratégia investigativa completa. A nota reconhece aplicação operacional parcial sem transformar a hipótese em experiência real. R31 foi mantido fora do Evidence Set e não influencia o score."
  related_knowledge: []
```

## EV-Q11 — Q11

```yaml
evaluation:
  id: EV-Q11
  question:
    id: Q11
    text: "Você vem utilizando IA no seu dia a dia?"
    version: "Structured Interview v6"
    domain: [artificial_intelligence, developer_tools]
    primary_type: experience
    secondary_dimensions: [practical_application]
    complexity: basic
  response:
    id: [R32, R34]
    text: "A candidata afirma que utiliza Copilot e menciona uma limitação de licença."
    source:
      segment_ids: [RAW-067, RAW-068, RAW-070]
  expected:
    essential: [informar se utiliza alguma ferramenta de IA]
    relevant: [identificar a ferramenta utilizada]
    optional: [descrever tarefas, frequência ou efeitos do uso]
    contextual: []
  weights:
    original: {correctness: 40, completeness: 20, depth: 15, reasoning: 10, practical_application: 10, trade_offs: 5}
    normalized: {correctness: 0.571429, completeness: 0.285714, depth: null, reasoning: null, practical_application: 0.142857, trade_offs: null}
  evidence:
    positive: [E-027, E-028]
    partial: []
    negative: []
    contradictory: []
    absent: []
    insufficient: []
  dimensions:
    correctness:
      applicable: true
      assessment: "A resposta afirma explicitamente o uso de Copilot."
      evidence: [E-027, E-028]
    completeness:
      applicable: true
      assessment: "Média-baixa: identifica o uso, mas não descreve tarefas, frequência operacional ou exemplos de aplicação."
      evidence: [E-027, E-028]
    depth:
      applicable: false
      assessment: "N/A"
      evidence: []
    reasoning:
      applicable: false
      assessment: "N/A"
      evidence: []
    practical_application:
      applicable: true
      assessment: "Baixa: há declaração de uso, sem demonstração de como a ferramenta é aplicada."
      evidence: [E-027, E-028]
    trade_offs:
      applicable: false
      assessment: "N/A"
      evidence: []
  score:
    value: 4.0
    confidence: high
  findings:
    strengths: ["Responde afirmativamente.", "Identifica Copilot."]
    gaps: ["Não detalha o uso prático da ferramenta.", "A limitação de licença não constitui trade-off técnico demonstrado."]
    errors: []
  rationale: "E-027 e E-028 sustentam uma declaração explícita de uso de Copilot. A pergunta é respondida no nível básico, mas a aplicação prática não é demonstrada. A menção à licença é preservada como contexto e não é convertida em avaliação técnica."
  related_knowledge: []
```

## Excluded

```yaml
excluded:
  - id: Q8
    reason: follow_up_or_continuation_of_Q7
    independent_evaluation: false
  - id: Q12
    reason: non_evaluable_contextual_question
    independent_evaluation: false
  - id: R24
    reason: unlinked_response
  - id: R26
    reason: unlinked_response
  - id: R41
    reason: unlinked_response
  - id: R52
    reason: unlinked_response
  - id: CQ1-CQ7
    reason: candidate_questions
```

## Validation

```yaml
validation:
  all_evaluation_ids_unique: true
  all_question_ids_present: true
  all_evidence_ids_exist: true
  excluded_material_not_evaluated: true
  interviewer_speech_not_evaluated_as_candidate: true
  no_invented_evidence: true
  n_a_dimensions_normalized: true
  confidence_separated: true
  scores_within_range: true
  every_score_has_rationale: true
  errors_have_evidence_reference: true
  q8_not_independent: true
  no_global_score: true
  no_global_average: true
  no_ranking: true
  no_seniority: true
  no_hiring_decision: true
  idempotency: PASS
  traceability: PASS
  evidence_integrity: PASS
  no_invention: PASS
  no_external_information: PASS
  confidence_separation: PASS
```

## Gate

```text
RUBRIC_COMPLETE_WITH_WARNINGS
```

The warning state is preserved because upstream artifacts remain `READY_WITH_WARNINGS`, and the canonical Rubric documents that historical Stage 19/19.1 calibration artifacts are unavailable. This does not prevent the ten individual evaluations from being produced.

Stage 23 — Evaluation Engine was not executed.
