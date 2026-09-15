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
# Interview Evaluation Model

Esta nota define como o Codex deve consolidar as avaliações individuais de perguntas técnicas (ver [[Evaluation Engine]]) em uma avaliação técnica da entrevista como um todo.

```text
Perguntas técnicas
   ↓
Respostas
   ↓
Evidências individuais
   ↓
Notas individuais
   ↓
Padrões observados
   ↓
Avaliação consolidada
```

O objetivo **não** é simplesmente calcular uma média. A avaliação final considera notas individuais, distribuição, complexidade das perguntas, importância dos temas, consistência do desempenho, pontos fortes, lacunas, erros críticos, profundidade, capacidade de aplicação, troubleshooting, arquitetura, relações entre conceitos, confiança das avaliações e cobertura efetiva da entrevista — tudo fundamentado em evidências observáveis.

## 1. Princípio fundamental

A avaliação da entrevista não responde apenas "qual foi a média das notas?". Responde: "o que o conjunto de respostas demonstra sobre o conhecimento técnico, a capacidade de raciocínio e a aplicação prática demonstrados pelo candidato durante esta entrevista?" A média é um indicador, não a conclusão.

## 2. Separação entre avaliação e decisão

- **Avaliação técnica**: o que foi demonstrado durante a entrevista.
- **Aderência à vaga**: se o conhecimento demonstrado atende aos requisitos de uma vaga específica (etapa futura).
- **Decisão de contratação**: decisão organizacional que pode envolver fatores além da avaliação técnica (fora do escopo desta camada).

Nesta etapa, avaliar apenas o desempenho técnico observado. Não recomendar contratação ou rejeição automaticamente.

## 3. Entrada

Quando disponíveis: perguntas; respostas; classificações das perguntas ([[Question Taxonomy]]); complexidade; notas individuais e confiança ([[Scoring Rubric]], [[Evaluation Engine]]); evidências; pontos fortes; lacunas; erros; erros críticos; domínios avaliados; dimensões avaliadas; relações entre conhecimentos.

```yaml
interview:
  questions: []
  evaluations: []
```

## 4. Validar avaliações individuais

Antes de consolidar, verificar se cada avaliação possui pergunta, resposta, tipo, domínio, complexidade, evidências, nota, confiança e justificativa. Se alguma avaliação estiver incompleta: não inventar informação; registrar a limitação; reduzir a confiança da avaliação global quando necessário.

## 4.1 Rastreabilidade das perguntas não pontuadas

Toda pergunta recebida no questionário/transcrição deve ser identificável na avaliação — nenhuma pergunta deve desaparecer silenciosamente da consolidação. Uma pergunta pode ser:

- **Pontuada**: recebeu nota 0–10 conforme [[Scoring Rubric]] e [[Evaluation Engine]].
- **Não pontuada — Contextual/Biográfica**: pergunta introdutória ou de levantamento de contexto (ex.: "quais tecnologias já trabalhou"), sem critério técnico de certo/errado isolado.
- **Não pontuada — Sem critério técnico isolado**: pergunta cuja resposta não permite avaliação numérica independente (ex.: puramente narrativa, sem elemento avaliável isoladamente).
- **Não avaliada por outro motivo justificável**: registrar o motivo explicitamente.

Para cada pergunta não pontuada, registrar de forma compacta:

```text
Pergunta: ...
Status: Não pontuada
Motivo: Contextual / Biográfica / Sem critério técnico isolado / [outro motivo]
Uso da evidência: Contextual, quando aplicável (ex.: alimenta a interpretação
de outra pergunta relacionada)
```

Regras:

- Não atribuir nota `0` a uma pergunta não pontuada.
- Não interpretar "não pontuada" como conhecimento ausente ou evidência negativa.
- Manter rastreável o fluxo `Questionário original → Perguntas avaliadas → Perguntas não pontuadas → Consolidação`, de forma que seja possível conferir que toda pergunta recebida foi contabilizada em uma das duas categorias.

## 5. Média das notas

```text
Média = soma das notas / quantidade de perguntas
```

A média não deve ser utilizada isoladamente. Exemplo: notas 10, 10, 10, 4, 4 → média 7,6, aparentemente boa, mas a distribuição pode revelar deficiência importante em um domínio específico — a análise deve continuar.

## 5.1 Integridade matemática e estrutural do relatório final

Antes de apresentar o relatório consolidado, validar sua integridade. A lista de notas efetivamente atribuídas às perguntas pontuadas é a **fonte única** para quantidade de perguntas pontuadas, distribuição por faixa, média e demais indicadores quantitativos derivados — não deve existir, no relatório final, mais de uma versão dessa lista, nem uma distribuição/média calculada a partir de dados diferentes da lista apresentada.

Validar obrigatoriamente antes de emitir o relatório:

```text
quantidade de notas apresentadas = quantidade de perguntas pontuadas
média apresentada = média das notas efetivamente listadas
distribuição apresentada = contagem das notas efetivamente listadas
nenhuma nota fantasma (nota citada que não corresponde a uma pergunta pontuada)
nenhuma nota duplicada
nenhuma nota "removida" apenas textualmente (i.e., mencionada e depois
descartada em texto, mas ainda presente nos cálculos)
```

Se for necessário corrigir um cálculo antes da emissão, apresentar apenas o resultado final corrigido e consistente — não apresentar simultaneamente uma "distribuição inicial" (incorreta) e uma "distribuição corrigida" no relatório final. O histórico de uma correção só deve ser exibido se explicitamente solicitado.

## 6. Distribuição das notas

Além da média, apresentar maior nota, menor nota, mediana (quando houver quantidade suficiente), quantidade de notas por faixa, distribuição por domínio e por complexidade.

Faixas descritivas (não são classificação de senioridade):

```text
0–2   → Muito fraco
2–4   → Fraco
4–6   → Parcial / abaixo do esperado
6–8   → Adequado / bom
8–10  → Forte / excelente
```

## 7. Consistência

Avaliar se o desempenho é consistente entre domínios. Exemplo: Java forte (8.0–9.0), Spring forte (7.5–8.0), Troubleshooting fraco (3.5–4.0) — a média geral pode parecer adequada, mas o padrão "conhecimento conceitual forte, troubleshooting mais fraco" é mais informativo que a média isolada.

## 8. Variabilidade de desempenho

Identificar diferenças relevantes entre respostas (ex.: forte em conceitos básicos, fraco em aplicação; forte em Java, fraco em Azure). Não interpretar automaticamente grande variação como inconsistência de conhecimento — pode refletir dificuldade da pergunta, experiência específica, área de atuação, contexto ou especialização. Descrever o padrão antes de interpretá-lo.

## 9. Desempenho por complexidade

Separar desempenho por Básica / Intermediária / Avançada. A média geral pode esconder que o candidato tem excelente domínio fundamental mas dificuldade em problemas complexos (ou vice-versa) — registrar isso explicitamente.

### Não penalizar por ausência de perguntas avançadas

Se a entrevista não avaliou determinado nível de complexidade, não presumir que o candidato não possui aquele conhecimento. Registrar `Não avaliada`, nunca `Fraca`.

## 10. Cobertura da entrevista

Avaliar quais domínios foram efetivamente testados, classificando cada um como Forte, Adequado, Parcial, Fraco ou **Não avaliado**. Nunca transformar "não avaliado" em "não sabe".

### Cobertura desigual

Se um domínio teve muitas perguntas e outro apenas uma, não tratá-los como igualmente representativos. Uma única resposta sobre um domínio não permite concluir domínio abrangente — registrar "evidência limitada".

## 11. Peso das perguntas

A média simples pode ser apresentada como referência. Quando apropriado, calcular também uma média ponderada considerando relevância da pergunta, importância do domínio, complexidade e qualidade da evidência — mas não inventar pesos que não foram definidos previamente. Se não houver pesos definidos, usar a média simples como principal e registrar a observação de que perguntas têm relevância/complexidade distintas (pesos específicos poderão vir do contexto da vaga em etapa futura).

## 12. Erros críticos

Verificar erros críticos das avaliações individuais e distinguir:

- **Isolado**: pode ser falha pontual.
- **Recorrente**: pode indicar lacuna conceitual mais profunda.
- **Em tema central**: pode ter impacto elevado na avaliação daquele domínio.

Não aplicar regra automática como "um erro crítico reprova o candidato" — o impacto depende do contexto técnico e da natureza do erro.

## 13. Lacunas recorrentes

Uma lacuna em uma única pergunta não deve necessariamente ser considerada deficiência consolidada. Procurar repetição, consistência, relevância e relação entre perguntas antes de declarar um gap relevante.

```text
Pergunta 1: não identificou métricas.
Pergunta 2: não utilizou logs.
Pergunta 3: não mencionou traces.
→ se as perguntas avaliavam observabilidade, há um padrão relevante.
```

## 14. Pontos fortes recorrentes

Mesma lógica para pontos fortes: identificar recorrência antes de generalizar para todo o domínio. Uma única resposta excelente não deve ser generalizada.

## 15. Conhecimento vs aplicação vs investigação vs decisão vs integração

Separar pelo menos:

- **Conhecimento conceitual**: sabe explicar conceitos?
- **Aplicação**: consegue utilizá-los em situações práticas?
- **Investigação**: consegue diagnosticar problemas?
- **Tomada de decisão**: consegue escolher entre alternativas e justificar?
- **Integração**: consegue conectar diferentes áreas?

Essa separação diferencia "sabe a definição" de "sabe utilizar o conhecimento".

## 16. Integração entre conhecimentos

Quando o candidato conecta conceitos corretamente (ex.: Java → Spring Boot → Hexagonal Architecture → Application Insights → Azure Monitor → KQL em um cenário real), registrar como evidência relevante de conhecimento integrado. Não confundir integração com quantidade de tecnologias citadas.

## 17. Profundidade

Avaliar evidência de entendimento superficial, funcional, sólido ou profundo, observando explicação de mecanismos, causa e efeito, limitações, consequências, trade-offs, aplicação e diagnóstico.

### Respostas aparentemente decoradas

Não considerar uma resposta excelente automaticamente decorada. Sinais que justificam cautela: definição correta sem capacidade de aprofundar, termos sem conexão, dificuldade quando a pergunta muda de contexto, incapacidade de aplicar, contradições ao explorar o assunto. Não afirmar "decorou" sem evidência — preferir: "evidência forte de conhecimento conceitual, evidência limitada de aplicação".

### Consistência entre profundidade e aplicação

Ex.: Conceitos 9.0, Aplicação 5.0 → não concluir "não sabe aplicar"; preferir "domínio conceitual forte, mas as respostas práticas avaliadas apresentaram evidência significativamente menor de aplicação".

## 18. Confiança global

Considerar quantidade de perguntas, qualidade das respostas, clareza da transcrição, cobertura dos domínios e complexidades, e consistência das evidências.

- **Alta**: evidência suficiente e consistente.
- **Média**: boa evidência, mas com limitações de cobertura ou quantidade.
- **Baixa**: evidência insuficiente para conclusão ampla.

## 19. Proporcionalidade ao tamanho da entrevista

Uma entrevista com poucas perguntas (ex.: 3) permite avaliar conceitos pontuais, mas não permite conclusões abrangentes como "excelente conhecimento geral de engenharia de software". A conclusão deve ser proporcional à quantidade de evidência.

## 19.1 Outliers na consolidação

Uma única pergunta com dificuldade, simplicidade ou comportamento extremo não deve dominar automaticamente a avaliação global da entrevista ou de um domínio. Antes de concluir a partir de uma nota isoladamente muito diferente das demais, analisar: distribuição das notas do domínio; complexidade da pergunta que gerou o outlier; relevância do domínio para a conclusão; quantidade de evidências disponíveis; existência de perguntas semelhantes que possam contextualizar o resultado; e consistência geral com as demais respostas.

Exemplo — domínio Java com notas `8, 8, 9` e uma pergunta extremamente difícil com nota `2`: não concluir automaticamente que o domínio Java é fraco; considerar a complexidade da pergunta que gerou o outlier antes de rebaixar a conclusão do domínio.

Da mesma forma, notas `8, 8, 9` e uma pergunta extremamente simples com nota `10` não devem elevar artificialmente a conclusão global — uma pergunta fácil bem respondida tem menor peso evidencial do que várias perguntas de complexidade comparável.

Isso não significa descartar o outlier: ele deve ser registrado e, quando relevante, mencionado no relatório (ver [[Interview Evaluation MOC]] e etapas de relatório) — apenas não deve, sozinho, determinar a conclusão sobre um domínio ou sobre a entrevista.

## 20. Perguntas muito semelhantes

Se várias perguntas avaliam praticamente o mesmo conhecimento, não tratar cada resposta como evidência totalmente independente. O desempenho conjunto aumenta a confiança sobre aquele conhecimento específico, mas não deve inflar a avaliação como se fossem áreas independentes. Identificar explicitamente quando houver forte sobreposição de conhecimento entre perguntas, para evitar que o mesmo conhecimento, perguntado várias vezes, receba peso artificialmente elevado na conclusão.

## 21. Evidência contraditória entre perguntas

Se o candidato responde corretamente a uma pergunta e de forma contraditória a outra sobre o mesmo tema, investigar diferença de contexto, mudança de premissa, interpretação da pergunta, erro pontual, desconhecimento ou inconsistência real, antes de concluir que não domina o tema.

## 22. Perfil técnico observado

Produzir um resumo do perfil demonstrado, mais útil que apresentar apenas a média:

```text
Perfil técnico observado:
- Fundamentos de Java: forte
- Spring Boot: forte
- Arquitetura: adequada
- Azure: parcial
- Observabilidade: forte
- Troubleshooting: adequado
- Integração entre conceitos: forte
```

## 23. Pontos fortes e gaps

**Pontos fortes**: identificar padrões recorrentes, cada um com evidência nas avaliações individuais.

**Gaps**, classificados como:

- **Pontual**: problema observado uma vez.
- **Relevante**: problema observado de maneira significativa.
- **Recorrente**: padrão observado em múltiplas respostas.

Evitar frases absolutas ("o candidato não sabe arquitetura"); preferir "as respostas avaliadas apresentaram evidência limitada de capacidade de justificar trade-offs arquiteturais".

## 24. Áreas não avaliadas

Criar seção explícita listando domínios não cobertos pela entrevista, para proteger contra conclusões indevidas.

## 25. Avaliação global

Produzir conclusão qualitativa que resuma evidências, aponte forças e lacunas, e indique limitações da entrevista — nunca reduzida a "Nota 8.0, candidato bom".

## 26. Nota global vs avaliação qualitativa

Apresentar ambas, deixando claro que a avaliação qualitativa não é simplesmente a média:

```text
Média: 7.8 / 10
Avaliação global: Forte em fundamentos e aplicação, com lacunas moderadas
em arquitetura avançada.
```

## 27. Sem equivalência automática com senioridade

Nunca produzir `7.0 = Júnior`, `8.0 = Pleno`, `9.0 = Senior`. A senioridade será avaliada em etapa posterior e dependerá de complexidade, consistência, autonomia, profundidade, arquitetura, troubleshooting, tomada de decisão, aplicação e contexto da vaga.

## 28. Sem ranking ou decisão

Nesta etapa não ranquear candidatos, compará-los, escolher o melhor, definir aprovação/reprovação ou recomendar contratação. O objetivo é produzir uma avaliação técnica consolidada.

## 29. Ausência não é deficiência

`Kubernetes: Não perguntado` não deve virar `Kubernetes: 0/10`. `Arquitetura avançada: Pouca evidência` não significa `Arquitetura avançada: Fraca`.

## 30. Cobertura mínima

Quando a entrevista tiver pouca cobertura, declarar explicitamente: "A evidência disponível é insuficiente para uma avaliação abrangente" e reduzir a confiança global quando necessário.

## 31. Estrutura final da avaliação

```markdown
# Avaliação Técnica da Entrevista

## Resumo
...

## Indicadores
Média das respostas: X.X / 10
Confiança global: Alta / Média / Baixa
Perguntas avaliadas: X

## Distribuição

| Faixa | Quantidade |
|---|---:|
| 0–2 | X |
| 2–4 | X |
| 4–6 | X |
| 6–8 | X |
| 8–10 | X |

## Desempenho por domínio

| Domínio | Avaliação | Evidência |
|---|---|---|
| Java | Forte | ... |
| Spring | Forte | ... |
| Arquitetura | Adequado | ... |
| Azure | Não avaliado | — |

## Desempenho por complexidade

| Complexidade | Avaliação |
|---|---|
| Básica | ... |
| Intermediária | ... |
| Avançada | ... |

## Dimensões observadas

### Conhecimento conceitual
...

### Aplicação prática
...

### Troubleshooting
...

### Tomada de decisão
...

### Integração entre conhecimentos
...

## Pontos fortes
- ...

## Gaps
- ...

## Erros relevantes
- ...

## Áreas não avaliadas
- ...

## Avaliação global
...

## Limitações da avaliação
...

## Confiança
...
```

## 32. Estrutura normalizada

```yaml
interview:
  questions_evaluated: 0

summary:
  average_score: 0.0
  median_score: 0.0
  confidence: ""

distribution:
  very_weak: 0
  weak: 0
  partial: 0
  adequate: 0
  strong: 0

domains:
  - name: ""
    assessment: ""
    evidence: []
    coverage: ""

complexity:
  basic:
    assessment: ""
    evidence: []
  intermediate:
    assessment: ""
    evidence: []
  advanced:
    assessment: ""
    evidence: []

dimensions:
  conceptual_knowledge:
    assessment: ""
    evidence: []
  practical_application:
    assessment: ""
    evidence: []
  troubleshooting:
    assessment: ""
    evidence: []
  decision_making:
    assessment: ""
    evidence: []
  integration:
    assessment: ""
    evidence: []

strengths: []

gaps:
  - type: ""
    description: ""
    evidence: []

critical_errors: []
not_evaluated: []
limitations: []
global_assessment: ""
```

## 33. Testes de consistência final

1. **Média** — foi calculada corretamente?
2. **Distribuição** — a média está escondendo alguma concentração ou deficiência?
3. **Complexidade** — o desempenho muda significativamente conforme a complexidade?
4. **Domínios** — existem domínios fortes ou fracos de forma consistente?
5. **Cobertura** — existem áreas importantes que simplesmente não foram avaliadas?
6. **Evidência** — cada conclusão possui evidência nas respostas?
7. **Generalização** — alguma conclusão está sendo extrapolada além da evidência disponível?
8. **Erros** — existem erros críticos ou recorrentes?
9. **Confiança** — é compatível com a quantidade e qualidade das evidências?
10. **Viés** — a avaliação foi influenciada por cargo, currículo, empresa, eloquência, confiança, tamanho das respostas, jargão ou impressão pessoal? Se sim, corrigir.

## 34. Regra de proporcionalidade

```text
Poucas perguntas → pouca evidência → conclusão limitada

Muitas perguntas + múltiplos domínios + múltiplas complexidades +
evidências consistentes → conclusão mais confiável
```

Nunca produzir uma conclusão mais abrangente do que a entrevista permite.

## 35. Regra de incerteza

Quando houver conflito entre uma conclusão forte e evidência insuficiente, preferir a conclusão mais conservadora. Em vez de "o candidato não possui conhecimento de Azure", usar "a entrevista forneceu evidência insuficiente para avaliar adequadamente o conhecimento de Azure".

## 36. Regra contra falsa objetividade

A existência de números não transforma a avaliação em ciência exata. Uma nota `7.8` não significa capacidade técnica mensurável com precisão de décimos — é uma representação estruturada da avaliação das evidências disponíveis. A análise qualitativa continua sendo necessária.

## 37. Resultado final esperado

O resultado permite responder "o que o candidato demonstrou tecnicamente nesta entrevista?", não apenas "qual foi sua média?":

```text
O que sabe
   ↓
O que sabe aplicar
   ↓
Onde demonstra profundidade
   ↓
Onde demonstra capacidade de investigação
   ↓
Onde toma boas decisões
   ↓
Quais gaps aparecem
   ↓
Quais áreas não foram avaliadas
   ↓
Quão confiável é essa conclusão
```

## 38. Limites desta etapa

Nesta etapa, **não** definir: senioridade final; aprovação ou reprovação; contratação; ranking de candidatos; aderência a uma vaga específica; pesos específicos de uma vaga; requisitos mínimos de uma posição. Esses elementos pertencem a etapas posteriores (ver [[Interview Evaluation MOC]]).

## Ver também

- [[Evaluation Framework]]
- [[Question Taxonomy]]
- [[Evidence Model]]
- [[Scoring Rubric]]
- [[Evaluation Engine]]
- [[Interview Evaluation MOC]]
