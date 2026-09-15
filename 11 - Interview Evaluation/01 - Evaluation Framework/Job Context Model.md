---
type: concept
status: understood
confidence: 100
created: 2026-09-09
updated: 2026-09-09
tags:
  - interview-evaluation
  - meta
---
# Job Context Model

Esta nota define como o Codex deve utilizar o contexto específico de uma vaga para interpretar a avaliação técnica de um candidato produzida em [[Interview Evaluation Model]].

```text
Conhecimento técnico demonstrado
        ↓
Avaliação técnica da entrevista
        ↓
Requisitos da vaga
        ↓
Aderência técnica à vaga
```

Objetivo: "Dado aquilo que o candidato demonstrou e aquilo que esta vaga exige, qual é o nível de aderência técnica observado?"

Esta etapa **não** altera notas individuais das respostas, **não** altera artificialmente a avaliação técnica da entrevista, e **não** transforma requisitos da vaga em critérios retroativos para perguntas que não os avaliaram.

## 1. Princípio fundamental — três conceitos independentes

- **Conhecimento demonstrado**: aquilo que o candidato efetivamente demonstrou durante a avaliação.
- **Avaliação técnica**: conclusão sobre o desempenho técnico observado na entrevista (ver [[Interview Evaluation Model]]).
- **Aderência à vaga**: comparação entre o conhecimento demonstrado e os requisitos técnicos específicos da posição.

```text
Candidato: conhecimento forte em Java e Spring.
Vaga: exige Java, Spring e Kubernetes.

Java       → Forte
Spring     → Forte
Kubernetes → Não avaliado

Aderência: evidência insuficiente para concluir domínio de Kubernetes.
```

Não converter isso em "candidato fraco".

## 2. A vaga como contexto, não como gabarito

Os requisitos da vaga contextualizam a avaliação; não modificam retroativamente perguntas, respostas, notas ou evidências. Uma resposta que recebeu 8.0 continua 8.0 independentemente da vaga — o que muda é a interpretação (ex.: "8.0 em Java, e Java é requisito central da vaga = forte aderência nesse requisito").

## 3. Entrada

```yaml
job:
  title: ""
  seniority: ""
  required: []
  preferred: []
  responsibilities: []
  technical_context: []
```

Pode incluir: título; senioridade esperada; responsabilidades; requisitos obrigatórios/desejáveis; tecnologias; arquitetura; práticas de engenharia; cloud; observabilidade; segurança; banco de dados; DevOps; experiências esperadas; contexto do produto/equipe; restrições e requisitos específicos.

## 4. Obrigatório vs desejável

- **Obrigatório**: conhecimento ou experiência essencial para a posição.
- **Desejável**: aumenta a aderência, mas sua ausência não necessariamente inviabiliza a posição.

Não tratar todos os itens da descrição da vaga como igualmente importantes.

## 5. Importância do requisito

Classificar, quando possível: **Crítico** (ausência provavelmente inviabiliza as principais responsabilidades) · **Alto** (importante para desempenho consistente) · **Médio** (relevante, mas pode ser desenvolvido) · **Baixo** (complementar). Se a descrição não fornecer contexto suficiente, registrar "Importância não determinada" — não inventar.

## 6. Conhecimento demonstrado vs requisito

Para cada requisito: foi avaliado? existe evidência? qual a força? qual a aderência observada? Estados: Forte evidência, Evidência adequada, Evidência parcial, Evidência fraca, Evidência contraditória, Não avaliado.

## 7. "Não avaliado" ≠ "não possui" (regra obrigatória)

```text
Vaga exige Kubernetes; entrevista não fez pergunta relacionada.

Kubernetes: Não avaliado
```

Nunca `Fraco`, nunca `0/10`, nunca "o candidato não sabe Kubernetes".

## 8. Evidência externa

Currículo, portfólio, GitHub, certificações, experiência declarada e projetos apresentados fora da resposta avaliada constituem **External Evidence**, e devem ser mantidos separados da **Interview Evidence** (evidência efetivamente demonstrada durante a entrevista — ver [[Evidence Model]], seção 28). Quando o candidato afirma ter realizado algo sem demonstrar tecnicamente na resposta, isso é **Declared Experience**, não Interview Evidence.

```text
Interview Evidence: Não avaliado.
External Evidence (currículo): declara 2 anos de experiência com Kubernetes.

Conclusão: existe Declared Experience relacionada a Kubernetes, mas a
entrevista não forneceu Interview Evidence suficiente para avaliar a
profundidade desse conhecimento.
```

Não transformar External Evidence ou Declared Experience em evidência equivalente a demonstração técnica (Interview Evidence). External Evidence pode fornecer contexto adicional e ajudar a priorizar o que investigar em futuras entrevistas, mas não substitui, nem eleva por si só, a aderência técnica de um requisito.

## 9. Senioridade da vaga como contexto

Vaga "Senior" não significa que toda resposta deve receber nota baixa se não apresentar conhecimento avançado. A pergunta correta é: "o nível de conhecimento demonstrado é compatível com as responsabilidades e complexidade esperadas para esta posição?", considerando complexidade, autonomia, profundidade, arquitetura, troubleshooting, tomada de decisão, aplicação e consistência.

## 10. Sem equivalência automática

Nunca usar `8.0 = Senior`, `7.0 = Pleno`, `6.0 = Junior`. Um candidato pode ter média 8 e não demonstrar autonomia arquitetural; média 7 e forte capacidade prática em domínio central; média 9 em fundamentos, mas pouca evidência em responsabilidades essenciais da vaga. A análise deve ser contextual.

## 11. Matriz de aderência

```text
| Requisito   | Importância | Avaliado? | Evidência | Aderência     |
|-------------|-------------|-----------|-----------|---------------|
| Java        | Crítico     | Sim       | Forte     | Alta          |
| Spring Boot | Crítico     | Sim       | Forte     | Alta          |
| Azure       | Alto        | Sim       | Parcial   | Média         |
| Kubernetes  | Alto        | Não       | —         | Não avaliada  |
| KQL         | Médio       | Sim       | Forte     | Alta          |
```

A matriz deve representar evidência, não suposições.

## 11.1 Rastreabilidade requisito → pergunta → avaliação → evidência

Cada requisito, quando avaliado, deve poder ser rastreado até a(s) pergunta(s) e avaliação(ões) individuais que geraram sua aderência, sem depender apenas de texto livre:

```text
Requisito
   ↓
Pergunta (question.id, ver [[Evaluation Engine]])
   ↓
Avaliação (identificador da avaliação individual)
   ↓
Evidência (Interview Evidence demonstrada)
   ↓
Aderência
```

Exemplo:

```text
Java
  → Pergunta Q03
  → Avaliação E03
  → Evidência demonstrada
  → Aderência: Alta
```

Isso permite responder "por que este requisito recebeu esta classificação de aderência?" consultando diretamente `source_evaluations` (ver seção 31) em vez de depender só da justificativa textual. A relação formal é:

```text
source_evaluations.evaluation_id  =  evaluation.id (ver [[Evaluation Engine]], seção 27)
```

`evaluation_id` referencia o identificador da avaliação (ex.: `E03`), não o identificador da pergunta — `question_id` (ao lado dele, na mesma entrada de `source_evaluations`) referencia `evaluation.question.id` (ex.: `Q03`). Os dois permanecem semanticamente distintos. Se não houver avaliação correspondente a um requisito, registrar `Aderência: Não avaliada` e não inventar uma referência de origem.

## 12. Categorias de aderência por requisito

- **Alta**: evidência compatível ou superior ao que o requisito demanda.
- **Adequada**: evidência indica capacidade suficiente para o contexto conhecido.
- **Parcial**: existe conhecimento, mas com lacunas relevantes.
- **Baixa**: evidência significativamente abaixo do necessário.
- **Não avaliada**: não existe evidência suficiente na entrevista.
- **Incerta**: informações conflitantes ou insuficientes para conclusão confiável.

## 13. Requisitos críticos fracos

Se um requisito crítico for avaliado como fraco, registrar explicitamente, incluindo o impacto:

```text
Requisito crítico: Spring Boot
Aderência: Baixa
Impacto: relevante, pois Spring Boot é utilizado diretamente nas principais
responsabilidades da posição.
```

Não esconder uma deficiência importante atrás de uma média geral alta.

## 14. Requisitos críticos não avaliados

Não assumir aprovação nem reprovação. Registrar: "A entrevista não forneceu evidência suficiente para determinar a aderência a este requisito crítico." Isso reduz a confiança da avaliação de aderência, não necessariamente a avaliação técnica geral do candidato.

## 15. Conhecimento transferível

Conhecimento relacionado (ex.: Docker → containers → possível transferência para Kubernetes) não equivale a domínio do requisito. Se Kubernetes não foi avaliado, não afirmar domínio apenas por conhecer Docker. Pode-se registrar: "existe conhecimento adjacente potencialmente relevante."

## 16. Tecnologias diferentes com responsabilidades semelhantes

Se a vaga exige uma tecnologia e o candidato demonstra outra equivalente, investigar conceito subjacente, experiência transferível, similaridade, diferenças importantes e curva de aprendizado.

```text
Vaga: Spring Boot
Candidato: ASP.NET Core

Pode demonstrar experiência relevante em APIs, DI, middleware,
configuração, observabilidade, arquitetura — mas não comprova domínio de
Spring Boot.

Conclusão: boa transferência de fundamentos, mas evidência direta de
Spring Boot limitada.
```

## 17. Requisitos compostos

Separar requisitos com múltiplos componentes (ex.: "experiência com arquitetura de microservices em Azure" → Microservices, Azure, Arquitetura, Distribuição, Experiência prática) e avaliar cada componente quando houver evidência, em vez de classificar o requisito inteiro como simplesmente forte/fraco.

## 18. Responsabilidades da vaga

Além dos requisitos, analisar responsabilidades (ex.: "investigar incidentes de produção" exige troubleshooting, observabilidade, logs, métricas, traces, análise de causa, tomada de decisão). A aderência deve considerar o conjunto de competências necessárias.

## 19. Contexto arquitetural e operacional

Quando a vaga possuir contexto técnico específico (Monolith, Microservices, Event-driven, Hexagonal, Clean Architecture, Serverless, Cloud-native) ou operacional (produção, incidentes, disponibilidade, SLA, observabilidade, escalabilidade, segurança, performance, custo), avaliar a relevância desse contexto para a aderência. Não presumir que uma arquitetura é universalmente superior. Uma vaga de produção crítica pode exigir evidência diferente de uma vaga focada em desenvolvimento de features.

## 20. Conhecimento vs aplicação vs experiência

- **Conhecimento**: o candidato consegue explicar.
- **Aplicação**: consegue demonstrar como utilizaria.
- **Experiência**: demonstra ter enfrentado situações reais.

Se a vaga exige especificamente experiência, não considerar conhecimento conceitual equivalente a experiência prática.

## 21. Pontos de aderência e gaps

- **Pontos de aderência**: onde a evidência combina bem com a vaga.
- **Gaps técnicos**: onde existe diferença entre o demonstrado e o necessário.
- **Gaps não avaliados**: onde a entrevista não forneceu evidência.

### Classificação de gaps

- **Crítico**: diferença relevante em competência essencial.
- **Relevante**: diferença importante, mas potencialmente administrável.
- **Desenvolvível**: conhecimento que pode razoavelmente ser adquirido no contexto esperado.
- **Incerto**: evidência insuficiente para determinar.

Não estimar tempo de aprendizado sem base suficiente, e não inferir capacidade de aprendizagem (ex.: nunca concluir "aprenderia Kubernetes em 2 meses" sem evidência específica). Pode-se dizer "o requisito não foi avaliado" ou "existe conhecimento adjacente que pode facilitar a transferência".

## 22. Evitar dupla contagem

A mesma evidência (ex.: uma resposta sobre Spring que demonstra DI, IoC e Spring Boot) pode contribuir para diferentes requisitos relacionados, mas não deve ser tratada como três demonstrações independentes de experiência profunda.

## 23. Cobertura da vaga

Avaliar requisitos críticos avaliados vs não avaliados, e requisitos altos avaliados vs não avaliados. Quanto maior a quantidade de requisitos críticos não avaliados, menor deve ser a confiança da conclusão de aderência.

## 24. Resultado de aderência

- **Alta aderência**: maioria dos requisitos relevantes com evidência forte/adequada, incluindo os críticos avaliados.
- **Aderência adequada**: principais requisitos com evidência suficiente, com lacunas menores.
- **Aderência parcial**: gaps relevantes ou requisitos importantes sem evidência suficiente.
- **Baixa aderência**: deficiências relevantes em requisitos essenciais avaliados.
- **Indeterminada**: entrevista sem evidência suficiente para determinar a aderência (especialmente relevante com pouca cobertura).

## 25. Aderência não é aprovação nem qualidade absoluta

Mesmo com "alta aderência", não concluir automaticamente "aprovado" — aderência técnica é apenas uma dimensão de uma decisão de contratação.

Avaliação técnica forte + aderência parcial não é contraditório: pode significar forte capacidade técnica geral, mas gaps em requisitos específicos desta posição. Da mesma forma, avaliação adequada + aderência alta pode ocorrer quando o candidato tem exatamente os conhecimentos necessários para uma vaga de escopo específico, sem amplitude além dela.

## 26. Relação com o Second Brain

O Second Brain continua sendo a referência técnica. A vaga define quais partes do conhecimento são relevantes — não redefine o que é tecnicamente correto.

```text
Second Brain → Conhecimento técnico → Avaliação do candidato →
Contexto da vaga → Aderência
```

Nunca: "Descrição da vaga define o que é tecnicamente correto".

## 27. Perguntas sem relação com a vaga

Se uma pergunta não possui relação significativa com a vaga, não utilizá-la como evidência importante de aderência (mas ela continua fazendo parte da avaliação técnica geral).

```text
Pergunta: detalhes avançados de JVM
Vaga: Frontend Angular

A resposta pode demonstrar conhecimento técnico forte, mas possui baixa
relevância direta para a aderência à vaga.
```

## 28. Requisitos ausentes na entrevista

Se a vaga exigir algo que não apareceu na entrevista, registrar "Não avaliado" e, quando relevante, o impacto: "limita a confiança da avaliação de aderência."

## 29. Requisitos conflitantes ou vaga genérica

Se a descrição possuir requisitos conflitantes (ex.: "experiência avançada" + "conhecimento básico"), não inventar interpretação — registrar a inconsistência e reduzir a confiança quando isso alterar significativamente a avaliação.

Se a descrição for muito genérica (ex.: "conhecimento em cloud"), não criar requisitos técnicos arbitrários (não assumir Azure, AWS, GCP, Kubernetes, Terraform automaticamente). Avaliar apenas o que está explicitamente descrito ou claramente contextualizado.

## 30. Estrutura final

```markdown
# Aderência Técnica à Vaga

## Contexto
Cargo: ...
Senioridade esperada: ...

## Resumo
...

## Matriz de requisitos

| Requisito | Importância | Avaliado | Evidência | Aderência |
|---|---|---|---|---|
| Java | Crítico | Sim | Forte | Alta |
| Spring Boot | Crítico | Sim | Forte | Alta |
| Azure | Alto | Sim | Parcial | Média |
| Kubernetes | Alto | Não | — | Não avaliada |

## Responsabilidades

| Responsabilidade | Evidência | Aderência |
|---|---|---|
| Desenvolvimento backend | ... | Alta |
| Troubleshooting | ... | Adequada |
| Arquitetura | ... | Parcial |

## Pontos de aderência
- ...

## Gaps técnicos
- ...

## Requisitos não avaliados
- ...

## Gaps críticos
- ...

## Avaliação de aderência
Alta / Adequada / Parcial / Baixa / Indeterminada

## Confiança
Alta / Média / Baixa

## Justificativa
...

## Limitações
...
```

## 31. Estrutura normalizada

```yaml
job:
  title: ""
  seniority: ""

requirements:
  - name: ""
    importance: ""
    required: true
    evaluated: false
    evidence: []
    source_evaluations:        # rastreabilidade — ver seção 11.1
      - question_id: ""        # = evaluation.question.id (ver [[Evaluation Engine]] §27)
        evaluation_id: ""      # = evaluation.id (ver [[Evaluation Engine]] §27)
    external_evidence: []       # currículo, portfólio, GitHub, certificações (ver seção 8)
    declared_experience: []     # experiência afirmada pelo candidato, não demonstrada tecnicamente
    adherence: ""
    confidence: ""

responsibilities:
  - name: ""
    evidence: []
    adherence: ""

summary:
  adherence: ""
  confidence: ""

strengths: []

gaps:
  - type: ""
    description: ""
    impact: ""

not_evaluated: []
limitations: []
rationale: ""
```

## 32. Testes de consistência

1. **Nota** — a nota individual permaneceu inalterada?
2. **Evidência** — cada conclusão possui evidência?
3. **Requisito** — o requisito realmente está presente na vaga?
4. **Cobertura** — o requisito foi efetivamente avaliado?
5. **Não avaliado** — algum "não avaliado" foi transformado indevidamente em "fraco"?
6. **Transferência** — conhecimento relacionado foi confundido com domínio direto?
7. **Experiência** — conhecimento conceitual foi confundido com experiência prática?
8. **Senioridade** — a senioridade da vaga foi usada como contexto, não como gabarito?
9. **Generalização** — alguma conclusão excede a evidência?
10. **Decisão** — o sistema evitou recomendar contratação ou rejeição automaticamente?

## 33. Regra de ouro

Sempre separar em três passos:

```text
1. O candidato demonstrou X.
2. A vaga exige X.
3. Portanto, existe determinada aderência entre X demonstrado e X exigido.
```

Nunca pular de "a vaga exige X" diretamente para "o candidato não sabe X" quando X não foi avaliado.

## 34. Resultado esperado

Ao final desta etapa, o Second Brain deve conseguir produzir três respostas independentes:

1. **O candidato é tecnicamente forte?** — baseado na avaliação da entrevista ([[Interview Evaluation Model]]).
2. **O candidato possui os conhecimentos exigidos por esta vaga?** — baseado na aderência entre evidências e requisitos.
3. **Quais requisitos ainda precisam ser validados?** — baseado nas áreas não avaliadas.

## 35. Limites desta etapa

Nesta etapa, **não**: alterar notas individuais; alterar a média técnica; inventar conhecimento; assumir conhecimento não avaliado; transformar currículo em prova técnica; definir contratação ou rejeição; criar ranking; comparar candidatos; criar requisitos inexistentes; presumir capacidade de aprendizagem; definir senioridade exclusivamente pela média.

Esta nota produz uma análise de aderência técnica contextualizada pela vaga, mantendo separadas evidência, avaliação técnica e decisão de contratação.

## Ver também

- [[Evaluation Framework]]
- [[Question Taxonomy]]
- [[Evidence Model]]
- [[Scoring Rubric]]
- [[Evaluation Engine]]
- [[Interview Evaluation Model]]
- [[Interview Evaluation MOC]]
