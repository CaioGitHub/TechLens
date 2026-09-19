---
type: concept
status: understood
confidence: 100
created: 2026-09-09
updated: 2026-09-19
tags:
  - interview-evaluation
  - meta
---
# Evaluation Engine

Esta nota define o processo operacional que o Codex deve executar para avaliar uma pergunta técnica e a respectiva resposta de um candidato, combinando [[Question Taxonomy]], [[Evidence Model]] e [[Scoring Rubric]] em uma avaliação única, fundamentada e auditável.

O motor transforma:

```text
Pergunta + Resposta do candidato + Taxonomia + Conhecimento relevante do
Second Brain + Modelo de Evidências + Rubrica 0–10
```

em:

```text
Avaliação fundamentada + Nota 0–10 + Confiança + Pontos fortes + Lacunas +
Justificativa
```

O motor deve ser consistente, explicável, auditável, baseado em evidências, tolerante a respostas alternativas, resistente a palavras-chave e a respostas excessivamente longas, consciente de contexto e versão, capaz de lidar com perguntas ambíguas e de reconhecer ausência de evidência suficiente.

Esta etapa avalia **uma pergunta + uma resposta**. Ainda não implementa média da entrevista, pesos entre perguntas, classificação de senioridade, recomendação de contratação, comparação de candidatos ou aderência à vaga — isso pertence a etapas posteriores (ver [[Interview Evaluation MOC]]).

## 1. Princípio central

O motor não avalia "a resposta parece boa?". Avalia: "quais evidências a resposta apresenta em relação ao que esta pergunta exige e ao conhecimento técnico relevante?"

```text
Pergunta
   ↓
Entender o que está sendo solicitado
   ↓
Classificar pergunta
   ↓
Determinar conhecimento relevante
   ↓
Analisar resposta
   ↓
Extrair evidências
   ↓
Comparar evidências com conhecimento
   ↓
Avaliar dimensões relevantes
   ↓
Identificar erros e lacunas
   ↓
Determinar nota
   ↓
Determinar confiança
   ↓
Gerar justificativa
```

## 2. Entradas do motor

**Obrigatórias**: pergunta; resposta do candidato.

**Contexto**: domínio; tipo de pergunta; complexidade; versão tecnológica; contexto apresentado pelo entrevistador.

**Second Brain**: notas relevantes; conceitos relacionados; arquitetura; padrões; troubleshooting; experiências documentadas; relações entre conceitos; limitações; trade-offs; informações específicas de versão.

Não assumir que a ausência de uma informação no Second Brain significa que a informação está errada.

## 3. Etapa 1 — Entender a pergunta

Antes de avaliar a resposta, identificar o que está sendo perguntado, qual ação o candidato precisa executar, qual conhecimento está sendo testado, quais aspectos são essenciais vs opcionais, e se há dependência de contexto ou de versão.

Exemplo: "Como você investigaria uma API Spring Boot que começou a apresentar aumento de latência?" não deve ser reduzida a "pergunta sobre Spring Boot" — o objetivo principal é avaliar uma estratégia de troubleshooting, observabilidade, diagnóstico e investigação de performance.

## 4. Etapa 2 — Classificação

Utilizar a taxonomia de [[Question Taxonomy]]:

```yaml
domain: []
primary_type: ""
secondary_dimensions: []
complexity: ""
version_relevance: ""
```

Quando a pergunta envolver múltiplos domínios, manter todos os relevantes. Não forçar uma pergunta multidisciplinar em uma única categoria.

## 5. Etapa 3 — Determinar o esperado

Construir internamente uma representação do que uma boa resposta precisa demonstrar, separada em:

- **Essencial**: elementos necessários para responder corretamente.
- **Relevante**: elementos que aumentam qualidade, profundidade ou completude.
- **Opcional**: elementos que podem enriquecer a resposta, mas não devem ser exigidos.
- **Contextual**: elementos que dependem de premissas específicas.

Exemplo — "O que é Dependency Injection?":

```text
Essencial: conceito de injeção de dependência; objeto recebe suas
           dependências externamente.
Relevante: redução de acoplamento; relação com IoC; testabilidade.
Opcional:  exemplo com Spring.
Contextual: tipos de injection; detalhes específicos do framework.
```

Não exigir elementos opcionais como se fossem obrigatórios.

## 6. Etapa 4 — Consultar o Second Brain

Priorizar: nota diretamente relacionada; notas vinculadas; conceitos relacionados; MOCs; conhecimento integrado; informações de versão. Não utilizar toda a base indiscriminadamente — o objetivo é recuperar contexto técnico relevante, não produzir uma pesquisa completa.

### O Second Brain não é gabarito

Funciona como referência técnica para validação e contextualização, não como resposta única obrigatória. Aceitar abordagens, nomenclaturas, arquiteturas, estratégias e soluções diferentes, desde que equivalentes ou condicionalmente válidas.

```text
Divergência
   ↓
É tecnicamente inválida?
   ├── Sim → registrar erro
   └── Não
        ↓
        É uma alternativa válida?
        ├── Sim → aceitar
        └── Não → investigar contexto
```

## 7. Etapa 5 — Extrair evidências

Separar as afirmações tecnicamente relevantes da resposta. Para cada uma, identificar conteúdo, tipo de evidência (positiva, parcial, incorreta, contraditória, ausente, insuficiente — ver [[Evidence Model]]), força, relação com a pergunta e relação com o conhecimento do Second Brain.

Exemplo:

```text
Resposta: "Eu começaria verificando se a latência está concentrada em algum
endpoint. Depois analisaria traces para descobrir se alguma dependência
está demorando."

Evidências:
+ Identifica concentração do problema por endpoint.
+ Utiliza traces para investigação.
+ Considera dependências como possível causa.
```

## 8. Separar evidência de interpretação

Manter duas camadas: **Evidência** (o que o candidato efetivamente demonstrou) e **Interpretação** (o que essa evidência permite concluir). Nunca apresentar a interpretação como se tivesse sido literalmente dita pelo candidato.

```text
Evidência: O candidato propôs utilizar traces para identificar onde o
           tempo está sendo consumido.
Interpretação: Demonstra conhecimento prático de observabilidade distribuída.
```

## 9. Etapa 6 — Avaliar cada dimensão relevante

Usar as dimensões de [[Scoring Rubric]] (Correção, Completude, Profundidade, Raciocínio, Aplicação prática, Trade-offs). Para cada dimensão aplicável, determinar avaliação, evidências e eventuais lacunas. Dimensões irrelevantes devem ser marcadas `N/A` — não atribuir artificialmente uma nota a uma dimensão que a pergunta não exige.

## 10. Etapa 7 — Determinação da nota

Combinar as dimensões relevantes usando os pesos de referência de [[Scoring Rubric]] (Correção 40% · Completude 20% · Profundidade 15% · Raciocínio 10% · Aplicação prática 10% · Trade-offs 5%).

Quando uma dimensão for `N/A`: removê-la do conjunto avaliado e redistribuir proporcionalmente o peso entre as dimensões aplicáveis (ver [[Scoring Rubric]], seção "N/A e normalização de pesos"), sem penalizar o candidato pela ausência de uma dimensão irrelevante e sem tratar `N/A` como zero.

### A nota é uma avaliação integrada, não uma fórmula mecânica

**Decisão arquitetural (reconciliação):** os pesos são referência estruturada de importância relativa entre dimensões; a nota final resulta de julgamento integrado sobre as evidências e dimensões aplicáveis, posicionado nas âncoras 0/2/4/6/8/10 (com incrementos de 0,5 quando justificável — ver [[Scoring Rubric]], seção "Mecânica da nota final"). Os pesos **não** obrigam a converter avaliações qualitativas de dimensão em números somados mecanicamente.

Se o candidato erra o conceito central de que a pergunta depende, não permitir que dimensões periféricas mantenham artificialmente a nota alta. Da mesma forma, uma pequena imprecisão periférica não deve destruir uma resposta essencialmente correta. A nota deve representar o quadro técnico geral da resposta.

Evitar falsa precisão (ex.: 7,13 · 8,27) quando a evidência não a justificar (ver seção 29).

## 11. Erros críticos

Classificar cada erro identificado como periférico, relevante, central ou crítico (ver [[Scoring Rubric]], categorias de erro). Um erro é **crítico** quando invalida a decisão técnica, demonstra desconhecimento fundamental, pode gerar solução tecnicamente perigosa, envolve segurança, perda de dados ou confiabilidade grave, ou contradiz diretamente o requisito central da pergunta.

Quando existir erro crítico: registrar, avaliar relevância, aplicar impacto proporcional (faixa orientativa: normalmente impede notas 9–10, podendo limitar a nota a uma faixa baixa ou intermediária conforme o restante das evidências — não um teto rígido universal) e explicar claramente o impacto na justificativa. Não usar "erro crítico" para qualquer pequeno detalhe.

## 12. Lacunas

Classificar como:

- **Essencial ausente**: falta um elemento necessário para responder adequadamente.
- **Relevante ausente**: a resposta continua válida, mas perde profundidade ou completude.
- **Opcional ausente**: não deve impactar significativamente a nota.

Nunca transformar uma informação opcional em requisito obrigatório.

## 13. Respostas parcialmente corretas

Dar crédito proporcional. Se a pergunta exige três elementos essenciais e o candidato apresenta dois corretos e um incorreto, não resumir como "errado" — registrar os elementos corretos e incorretos e calcular a nota considerando relevância de cada elemento, impacto do erro, qualidade do raciocínio e profundidade demonstrada.

## 14. Perguntas de troubleshooting

Avaliar principalmente o processo de raciocínio, sem exigir sequência única. Diante de "API retornando HTTP 500", estratégias que comecem por logs, traces, métricas, correlação, mudanças recentes, dependências ou análise do endpoint podem ser igualmente válidas. Avaliar coerência, capacidade de formular hipóteses, coleta de evidências, isolamento da causa, validação da hipótese e capacidade de distinguir sintoma de causa.

## 15. Perguntas de arquitetura

Avaliar requisitos identificados, separação de responsabilidades, dependências, acoplamento, escalabilidade (quando relevante), testabilidade, manutenção, segurança e confiabilidade (quando relevantes) e trade-offs. Não avaliar arquitetura apenas pela presença de determinadas tecnologias.

## 16. Perguntas de implementação

Avaliar correção, entendimento do mecanismo, adequação da solução, edge cases (quando relevantes), manutenção, testes (quando solicitados) e complexidade (quando relevante). Não exigir implementação idêntica à do Second Brain.

## 17. Perguntas de comparação

Para perguntas do tipo "X ou Y?", avaliar compreensão de X, compreensão de Y, diferenças relevantes, contexto de utilização, trade-offs e capacidade de justificar a escolha. Uma resposta que apenas afirma "eu prefiro X" possui pouca evidência de capacidade de decisão.

## 18. Perguntas de opinião

Perguntas como "microservices ou monolith?" não devem ser avaliadas pela preferência em si. Avaliar justificativa, contexto, trade-offs, experiência, consequências e capacidade de reconhecer quando a alternativa poderia ser melhor. Não considerar uma preferência diferente da do Second Brain como erro.

## 19. Perguntas de experiência

Quando o candidato afirma "já implementei isso", separar **Declaração** (afirmação de possuir experiência) de **Evidência demonstrada** (explicação de contexto, problema, decisão, implementação, motivo, resultado, dificuldades, trade-offs). A segunda possui maior valor como evidência técnica. Não classificar automaticamente a declaração como falsa.

A pergunta continua recebendo nota 0–10 normalmente; a nota reflete o que a resposta demonstrou, não uma conclusão sobre a experiência real do candidato (ver critério de pontuação detalhado em [[Scoring Rubric]], seção 8.1). Se a resposta for puramente hipotética (ex.: "se eu tivesse esse problema, eu faria X"), registrar conhecimento/raciocínio possivelmente demonstrado separadamente de experiência prática demonstrada (insuficiente) — não atribuir experiência prática com base em uma resposta explicitamente hipotética. Se o candidato relatar não lembrar detalhes de uma experiência declarada, registrar experiência declarada presente e demonstração limitada/insuficiente, sem inferir ausência de experiência nem classificar a lacuna de memória como erro técnico.

## 20. Versionamento

Se a pergunta ou resposta depender de versão, identificar a versão, consultar o conhecimento correspondente, verificar se a afirmação era válida naquela versão e evitar aplicar conhecimento de outra versão incorretamente. Uma resposta correta para Java 21 não deve ser penalizada por uma funcionalidade inexistente em Java 17, se a pergunta era explicitamente sobre Java 21 — e vice-versa.

## 21. Pergunta ambígua

Identificar a ambiguidade, determinar interpretações plausíveis, avaliar a resposta dentro da interpretação mais razoável e reduzir a confiança se a ambiguidade afetar significativamente a avaliação. Não penalizar o candidato por uma interpretação razoável da pergunta.

## 22. Problemas de transcrição

Considerar possíveis erros de transcrição, palavras trocadas, termos técnicos reconhecidos incorretamente, frases incompletas, interrupções e fala sobreposta. Não considerar automaticamente um termo transcrito incorretamente como erro técnico do candidato. Quando a transcrição impedir uma avaliação confiável, registrar `Confiança: Baixa` e a limitação encontrada.

## 23. Respostas com informações irrelevantes

Ignorar conteúdo que não contribui para responder à pergunta — isso não deve aumentar a nota. Também não reduzir a nota apenas pela existência de conteúdo irrelevante, salvo quando ele prejudica o raciocínio, introduz contradições, substitui a resposta ou demonstra confusão sobre o tema.

## 24. Jargão

Não considerar jargão como evidência suficiente. Ex.: "Eu aplicaria SOLID, DDD, CQRS e event-driven" não demonstra domínio por si só. Perguntar implicitamente: o candidato explicou como, por quê e em qual contexto? Se não, a evidência é fraca.

## 25. Testes de consistência

Antes de finalizar a nota, executar:

1. **Evidência** — existe evidência concreta para a nota?
2. **Pergunta** — a nota responde ao que foi perguntado?
3. **Alternativas** — uma solução diferente, porém válida, foi aceita?
4. **Complexidade** — a complexidade da pergunta foi considerada corretamente?
5. **Versão** — existe dependência de versão?
6. **Viés** — a nota foi influenciada por eloquência, tamanho, confiança, cargo, experiência declarada ou jargão? Se sim, corrigir.
7. **Confiança** — a confiança corresponde à qualidade da evidência?

## 26. Formato final de saída

```markdown
## Avaliação

Pergunta: ...
Tipo: ...
Domínio: ...
Complexidade: ...

Nota: 8.0 / 10
Confiança: Alta

### Resumo
...

### Dimensões

| Dimensão | Avaliação | Evidência |
|---|---|---|
| Correção | Forte | ... |
| Completude | Boa | ... |
| Profundidade | Boa | ... |
| Raciocínio | Forte | ... |
| Aplicação prática | N/A | — |
| Trade-offs | N/A | — |

### Pontos fortes
- ...

### Lacunas
- ...

### Erros
- ...

### Justificativa
...

### Conhecimentos relacionados
- ...
```

## 27. Estrutura normalizada (esquema canônico)

Este é o **único esquema YAML canônico** para representar a avaliação de uma pergunta + resposta em todo o sistema. Nenhum outro documento (incluindo [[Scoring Rubric]]) deve definir uma estrutura alternativa para o mesmo objeto — ver [[Scoring Rubric]], seção "Esquema de dados canônico".

```yaml
evaluation:
  id: ""                # identificador único da própria avaliação (ex.: "E03")
  question:
    id: ""              # identificador da pergunta (ex.: "Q03"), quando existir
    text: ""
    version: ""          # versão da entrevista/pergunta, quando aplicável
    domain: []
    primary_type: ""
    secondary_dimensions: []
    complexity: ""

  response:
    id: ""              # identificador da resposta (ex.: "R03"), quando existir
    text: ""
    source:
      segment_ids: []

  expected:
    essential: []
    relevant: []
    optional: []
    contextual: []

  evidence:
    positive: []
    partial: []
    negative: []          # afirmações tecnicamente incorretas
    contradictory: []
    absent: []
    insufficient: []

  dimensions:
    correctness:
      applicable: true
      assessment: ""
      evidence: []
    completeness:
      applicable: true
      assessment: ""
      evidence: []
    depth:
      applicable: true
      assessment: ""
      evidence: []
    reasoning:
      applicable: true
      assessment: ""
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
    value: 0.0             # âncoras 0/2/4/6/8/10, incrementos de 0,5 quando justificável
    confidence: ""

  findings:
    strengths: []
    gaps: []
    errors: []             # cada erro classificado como periférico | relevante | central | crítico

  rationale: ""

  related_knowledge: []    # notas do Second Brain consultadas, ex.: "Dependency Inversion"
```

Nem todos os campos precisam receber conteúdo quando a dimensão ou o elemento não for relevante à pergunta (usar `[]`, `"N/A"` ou omitir conforme o caso).

### `evaluation.id` vs `evaluation.question.id`

- **`evaluation.id`**: identificador único da própria avaliação realizada para uma pergunta específica dentro de uma entrevista (ex.: `"E03"`). Deve ser único dentro do contexto da entrevista, permanecer estável após a criação da avaliação, e ser a referência utilizada por qualquer estrutura externa que precise apontar para esta avaliação (ex.: `source_evaluations` em [[Job Context Model]]). Não carrega significado técnico ou de qualidade — é apenas um identificador.
- **`evaluation.question.id`**: identificador da pergunta em si (ex.: `"Q03"`). Uma mesma pergunta poderia, em tese, ser reavaliada; os dois identificadores permanecem conceitualmente distintos e não devem ser usados de forma intercambiável.

Este esquema é referenciado — não duplicado — por [[Scoring Rubric]] e por [[Job Context Model]] (campo `source_evaluations`, cujo `evaluation_id` referencia exatamente `evaluation.id` definido aqui).

## 28. Regra de auditabilidade

Outra pessoa deve conseguir olhar para pergunta + resposta + evidências + nota e entender como a conclusão foi produzida. A avaliação não pode depender de uma "intuição interna" não explicada.

## 29. Regra contra falsa precisão

Se existirem poucas evidências, não produzir uma justificativa excessivamente precisa. `Nota: 6.5 · Confiança: Baixa` é preferível a `Nota: 6.73 · Confiança: Alta` quando a resposta possui pouca informação.

## 30. Regra de consistência entre perguntas

A mesma lógica deve ser aplicada a candidatos diferentes. Isso não significa que todas as perguntas devam possuir exatamente o mesmo padrão de evidência — a avaliação deve ser consistente no processo, não necessariamente idêntica no conteúdo.

## 31. Regra de não antecipação

Este motor avalia uma pergunta + uma resposta. Ainda não deve: calcular desempenho global; calcular média da entrevista; classificar senioridade; recomendar contratação; comparar candidatos; definir aderência à vaga. Esses aspectos pertencem a etapas posteriores.

## 32. Fluxo operacional final

```text
1. Receber pergunta e resposta
2. Entender a pergunta
3. Classificar pergunta
4. Determinar evidências esperadas
5. Consultar Second Brain
6. Analisar resposta
7. Extrair evidências
8. Separar evidência de interpretação
9. Avaliar dimensões relevantes
10. Identificar lacunas
11. Identificar erros
12. Verificar erros críticos
13. Considerar alternativas válidas
14. Calcular/estimar nota
15. Determinar confiança
16. Executar testes de consistência
17. Produzir avaliação auditável
```

## 33. Resultado esperado

Ao final desta etapa, o Second Brain possui um processo capaz de responder:

```text
Dada esta pergunta e esta resposta, quais evidências foram apresentadas, o
que elas demonstram e qual nota de 0 a 10 é justificável?
```

Sem depender de gabarito literal, palavras-chave, quantidade de texto, cargo, experiência declarada ou preferência pessoal do avaliador. A avaliação deve ser fundamentada no conhecimento técnico, nas evidências e no contexto da pergunta.

## 34. Responsabilidade operacional do Evaluation Engine

O Evaluation Engine transforma um conjunto de evidências técnicas em uma avaliação estruturada segundo a [[Scoring Rubric]]:

```text
Question
↓
Response
↓
Evidence Set
↓
Rubric 0–10
↓
Evaluation
```

O Engine deve:

1. receber a pergunta e sua taxonomia;
2. receber a resposta estruturada;
3. receber o Evidence Set já produzido pelo Stage 21;
4. identificar as dimensões aplicáveis;
5. aplicar os pesos de referência;
6. excluir dimensões `N/A` e normalizar os pesos restantes;
7. considerar evidências positivas, parciais, negativas, contraditórias, ausentes e insuficientes;
8. considerar erros periféricos, relevantes, centrais e críticos;
9. produzir avaliação dimensional;
10. produzir score de `0–10`;
11. produzir `rationale` proporcional e rastreável;
12. produzir `evaluation.confidence`;
13. preservar as referências de pergunta, resposta, evidência e transcript.

O Engine não deve reconstruir evidências. Se uma evidência não estiver no Evidence Set, não pode ser criada apenas para completar uma dimensão ou melhorar a coerência da avaliação.

## 35. O que não pertence ao Engine

Permanecem nos estágios próprios:

```text
20.1–20.2 → participantes e speakers
20.3       → perguntas
20.4       → respostas
20.5       → reconstrução e normalização
20.6       → linking
20.7       → validação da Structured Interview
21         → extração e estruturação de evidências
22         → critérios e escala da Rubrica
23         → avaliação da pergunta + resposta
```

O Evaluation Engine não deve:

- identificar participantes, atribuir speakers ou extrair perguntas;
- reconstruir ou corrigir transcrições;
- inventar, completar ou corrigir tecnicamente evidências;
- inferir conhecimento não demonstrado;
- usar currículo, cargo, anos de experiência ou confiança verbal como multiplicador;
- inferir senioridade, potencial ou adequação absoluta;
- criar ranking, recomendação de contratação ou decisão de aprovação/reprovação;
- alterar o Evidence Model, a Rubrica ou a base técnica para acomodar uma resposta.

## 36. EvaluationInput canônico

O objeto de entrada deve reutilizar as estruturas existentes:

```text
EvaluationInput
├── question
├── response
├── evidence_set
├── applicable_dimensions
└── contextual_metadata
```

Representação conceitual:

```yaml
evaluation_input:
  question:
    id: Q1
    text: "..."
    primary_type: troubleshooting
    secondary_dimensions:
      - reasoning
      - observability
    complexity: advanced

  response:
    id: R1
    text: "..."
    source:
      segment_ids:
        - S12

  evidence_set:
    source_validation_status: READY
    evidence_ids:
      - E1
      - E2

  applicable_dimensions:
    - correctness
    - completeness
    - reasoning
    - practical_application

  contextual_metadata:
    version: ""
    job_context_id: ""
```

`evaluation_input` é uma entrada operacional; o objeto de saída continua sendo exclusivamente `evaluation`, conforme o schema canônico da seção 27. Não criar outro schema de avaliação.

O `contextual_metadata` pode registrar versão, contexto técnico e referência de vaga, mas não pode alterar artificialmente a qualidade técnica da resposta. A referência de vaga informa relevância posterior; não é evidência da entrevista.

## 37. Evidence Set como fonte exclusiva

O Engine deve seguir:

```text
Evidence Set
↓
Relevância para a pergunta
↓
Força e qualificação da evidência
↓
Dimensional assessment
↓
Score integrado
```

Para cada dimensão, selecionar somente `evidence_id` existentes e relevantes. A ausência de uma evidência esperada não autoriza criar uma evidência negativa:

```text
absent ≠ incorrect
insufficient ≠ candidate_does_not_know
```

Evidências `experience_declaration`, `scenario_application`, `uncertainty` e `demonstrated_experience` devem conservar sua natureza. Uma hipótese não pode ser convertida em experiência real; uma declaração não pode ser promovida automaticamente a demonstração técnica.

## 38. Avaliação dimensional e pesos

Cada dimensão aplicável deve ser analisada antes do score integrado:

```yaml
dimensions:
  correctness:
    applicable: true
    assessment: "..."
    evidence:
      - E1
  completeness:
    applicable: true
    assessment: "..."
    evidence:
      - E1
      - E2
  depth:
    applicable: false
    assessment: "N/A"
    evidence: []
```

As dimensões canônicas e os pesos são:

```text
correctness            40%
completeness           20%
depth                  15%
reasoning              10%
practical_application  10%
trade_offs              5%
```

Quando uma dimensão não for aplicável:

```text
dimension.applicable = false
dimension.assessment = "N/A"
dimension.evidence = []
```

Ela é excluída do conjunto avaliável. Para o conjunto `A` de dimensões aplicáveis:

```text
normalized_weight(d) = original_weight(d) /
                       sum(original_weight(a) for a in A)
```

Não usar `N/A` para evitar uma dimensão difícil. Não tratar `N/A` como zero.

## 39. Score integrado e julgamento

Os pesos orientam a importância relativa das dimensões, mas a Rubrica determina julgamento integrado, não uma média mecânica obrigatória de rótulos qualitativos.

Quando houver avaliações numéricas dimensionais explicitamente disponíveis, a referência matemática é:

```text
score_reference =
Σ(dimension_score × normalized_weight)
```

Essa referência não substitui:

- a centralidade da correção para a pergunta;
- o impacto contextual de erro central ou crítico;
- a distinção entre dimensão aplicável e não aplicável;
- a necessidade de evitar dupla contagem da mesma evidência;
- o julgamento integrado exigido pela Rubrica.

O score final deve usar as âncoras `0`, `2`, `4`, `6`, `8` e `10`, com incrementos de `0.5` quando sustentados. Não criar teto universal para erro crítico. Um erro crítico central deve produzir impacto proporcional e ser explicado no `rationale`.

## 40. Evidências positivas, negativas e contraditórias

O Engine deve:

- preservar todas as evidências utilizadas;
- relacionar cada evidência às dimensões afetadas;
- permitir `positive`, `partial`, `negative`, `contradictory`, `absent` e `insufficient`;
- não tratar ausência como erro;
- não deixar que muitas evidências positivas irrelevantes anulem um erro central;
- não resolver contradições inventando uma terceira afirmação;
- reduzir `evaluation.confidence` quando a contradição impedir conclusão segura;
- explicar no `rationale` como a contradição afetou a avaliação.

Autocorreções devem ser avaliadas como sequência completa: preservar a afirmação inicial, a correção e a qualidade técnica demonstrada depois. Não penalizar automaticamente toda autocorreção nem apagar o erro inicial.

## 41. Rationale e confidence

Toda saída deve possuir `rationale` proporcional às evidências. Deve explicar:

```text
quais evidence_ids foram considerados
↓
quais dimensões foram afetadas
↓
quais limitações, ausências ou contradições existem
↓
por que o score é compatível com a Rubrica
```

Evitar `"boa resposta"` ou qualquer conclusão não rastreável.

`evaluation.confidence` é independente do score e das confianças anteriores:

```text
evaluation.confidence
≠ extraction_confidence
≠ reconstruction_confidence
≠ linking_confidence
≠ evidence_confidence
```

Pode existir:

```text
score: 2.0
evaluation.confidence: high
```

quando houver alta confiança de que a experiência solicitada não foi demonstrada. Não usar tom, eloquência, cargo, senioridade ou currículo para elevar a confidence.

## 42. Experiência, hipótese e limitação

Perguntas de experiência continuam recebendo `0–10`:

```text
Nível 1 → somente declaração
Nível 2 → declaração + poucos detalhes
Nível 3 → experiência concreta
Nível 4 → experiência concreta + raciocínio/trade-offs
```

O Engine deve manter:

```text
experience_declaration
≠ demonstrated_experience
≠ absence_of_experience
```

Para `"não sei"`, `"não lembro"`, `"acho que"` e `"se não me engano"`, avaliar somente o conteúdo efetivamente produzido. Não converter automaticamente incerteza em erro nem em desconhecimento absoluto.

## 43. Job Context e agregação

O [[Job Context Model]] pode informar requisitos, tecnologias e responsabilidades, mas não altera retroativamente a nota técnica:

```text
Interview Evidence
≠ Job Relevance
```

Uma tecnologia prioritária para a vaga não recebe bônus; uma tecnologia menos relevante não recebe penalidade automática.

Quando várias avaliações forem agregadas, preservar:

- `evaluation.id`;
- score individual;
- `evaluation.confidence`;
- dimensões;
- evidências;
- `question.id`, `response.id` e sources.

Uma média é apenas um indicador quantitativo. Não transformá-la automaticamente em senioridade, ranking, contratação ou aprovação/reprovação.

## 44. Rastreabilidade obrigatória

Toda avaliação deve permitir:

```text
Evaluation
↓
Question
↓
Response
↓
Evidence Set
↓
Evidence
↓
source.segment_ids
↓
Transcript
```

Verificar antes de concluir:

- `evaluation.id` existe, é único e estável;
- `evaluation.question.id` existe quando a pergunta foi identificada;
- `evaluation.response.id` existe quando a resposta foi identificada;
- cada `evidence_id` referenciado existe;
- cada evidência utilizada possui source quando disponível;
- `source.segment_ids` pertencem à Structured Interview;
- nenhum ID é criado para corrigir ou mascarar uma referência quebrada.

Uma falha de rastreabilidade deve reduzir a confidence e pode bloquear a avaliação quando impedir auditoria da evidência central.

## 45. Testes de invariância

O Engine deve passar por testes de invariância:

| Teste | Alteração isolada | Resultado esperado |
|---|---|---|
| Tamanho | adicionar texto irrelevante | score não aumenta |
| Tom | tornar a fala mais confiante sem mudar conteúdo | score e confidence não aumentam |
| Senioridade | adicionar `"Tenho 15 anos de experiência"` | score não muda |
| Currículo | adicionar experiência no CV | não altera Interview Evidence nem score |
| Complexidade | trocar pergunta simples por cenário mais complexo sem mudar o escopo avaliado | não conceder bônus automático |
| Terminologia | adicionar jargão sem explicação | não aumentar score |
| N/A | remover dimensão realmente não aplicável | normalizar pesos restantes |
| Stack | usar alternativa válida quando stack não foi exigido | não penalizar por si só |

## 46. Baselines de calibração

Os casos abaixo são **baselines documentados** na [[Scoring Rubric]], não execuções históricas verificadas nesta base:

```text
CAL-01 ≈ 2.0
CAL-02 ≈ 4.0
CAL-03 ≈ 1.5
CAL-04 ≈ 7.5 / 8.5
CAL-05 ≈ 7.0
CAL-06 ≈ 8.5
CAL-07 ≈ 8.5
CAL-08 ≈ 4.5
CAL-09 ≈ 9.0
CAL-10 ≈ 7.5
```

O Engine deve preservar especialmente:

- `CAL-01`: `confidence: high` sobre a não demonstração, não sobre desconhecimento absoluto;
- `CAL-09`: pergunta simples pode receber nota excelente;
- `CAL-10`: pergunta complexa não recebe bônus automático.

Não afirmar que os casos foram executados quando os artefatos históricos das Etapas 19/19.1 não estão disponíveis.

## 47. Testes controlados da Etapa 23

Os testes seguintes devem ser usados como regressão. Não processam candidatos reais:

| # | Caso | Resultado esperado |
|---:|---|---|
| 1 | resposta correta | score alto proporcional ao escopo |
| 2 | resposta incorreta | correctness baixa e rationale rastreável |
| 3 | resposta parcialmente correta | preservar evidências corretas e incorretas |
| 4 | resposta incompleta | reduzir completude, não inventar lacunas preenchidas |
| 5 | resposta superficial | separar profundidade de correção |
| 6 | resposta profunda | reconhecer relações, mecanismos e consequências sustentadas |
| 7 | erro factual | impactar correctness proporcionalmente |
| 8 | erro conceitual central | impacto forte, sem compensação por evidências irrelevantes |
| 9 | erro periférico | impacto proporcional |
| 10 | erro crítico | impacto contextual, sem teto universal |
| 11 | trade-off correto | reconhecer consequência e condição sustentadas |
| 12 | trade-off incorreto | registrar erro na dimensão afetada |
| 13 | troubleshooting | valorizar investigação orientada por evidências |
| 14 | cenário arquitetural | avaliar solução e raciocínio, não rótulo arquitetural |
| 15 | experiência declarada | nota baixa possível, sem N/A automático |
| 16 | experiência com poucos detalhes | demonstração parcial |
| 17 | experiência concreta | avaliar aplicação realmente descrita |
| 18 | experiência + trade-offs | reconhecer raciocínio adicional |
| 19 | `"não sei"` | registrar limitação, não desconhecimento absoluto |
| 20 | `"não lembro"` | preservar experiência declarada e limitação |
| 21 | resposta hipotética | separar cenário de experiência real |
| 22 | autocorreção | avaliar sequência e correção final |
| 23 | fora do escopo | registrar falta de aderência sem criar nova pergunta |
| 24 | pergunta composta | avaliar somente subtemas efetivamente perguntados |
| 25 | dimensão N/A | excluir e normalizar pesos |
| 26 | normalização de pesos | preservar proporções originais |
| 27 | evidências contraditórias | preservar, relacionar e reduzir confidence quando necessário |
| 28 | confidence alta + score baixo | permitir combinação |
| 29 | confidence baixa + score alto | permitir quando evidência parece forte, mas é ambígua |
| 30 | resposta curta excelente | permitir 9 ou 10 |
| 31 | resposta longa superficial | não premiar extensão |
| 32 | senioridade declarada | não alterar score |
| 33 | tom excessivamente confiante | não alterar score |
| 34 | pergunta simples | não limitar score |
| 35 | pergunta complexa | não conceder bônus |
| 36 | Job Context relevante | não alterar qualidade da resposta |
| 37 | Job Context irrelevante | não contaminar a avaliação |
| 38 | múltiplas evidências positivas | considerar relevância, não quantidade |
| 39 | evidência positiva + negativa | preservar ambas e avaliar centralidade |
| 40 | ausência de evidência | usar `absent`/`insufficient`, não `candidate_does_not_know` |

## 48. Testes de rastreabilidade e separação

Antes de declarar uma avaliação concluída:

```text
evaluation.id existe?
question.id existe?
response.id existe?
todo evidence_id existe?
todo evidence source existe quando esperado?
source.segment_ids existem?
```

Também verificar que o Engine não:

- extrai perguntas;
- reconstrói respostas;
- cria evidências;
- atribui speakers;
- decide senioridade;
- decide contratação.

## 49. Gate da Etapa 23

O Engine pode declarar:

```text
EVALUATION_ENGINE_COMPLETE
```

quando:

- o artefato canônico foi localizado;
- Rubrica, Evidence Model e Question Taxonomy são compatíveis;
- pesos e N/A estão compatíveis;
- o schema de `evaluation` é único;
- dimensões, score, confidence e rationale estão definidos;
- rastreabilidade é preservada;
- Job Context não altera artificialmente o score;
- baselines CAL-01–CAL-10 estão documentados;
- testes controlados, invariância e rastreabilidade estão definidos;
- não há conflito estrutural conhecido.

Os baselines não foram executados historicamente nesta base porque os artefatos das Etapas 19/19.1 não foram encontrados. Por isso, o status documental desta execução é:

```text
READY_WITH_WARNINGS
```

O warning não representa falha do candidato nem do mecanismo conceitual; representa ausência de evidência histórica de execução da calibração.

`READY`, `READY_WITH_WARNINGS` e `BLOCKED` descrevem prontidão do artefato e nunca aprovação, reprovação, senioridade, ranking ou contratação.

## Ver também

- [[Evaluation Framework]]
- [[Question Taxonomy]]
- [[Evidence Model]]
- [[Scoring Rubric]]
- [[Interview Evaluation MOC]]
