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
# Evidence Model

Este documento define o modelo de evidências utilizado para analisar respostas de candidatos durante entrevistas técnicas.

Responde:

```text
Quais evidências presentes na resposta permitem afirmar o que o candidato demonstrou saber?
```

Esta etapa **não** transforma evidências em notas. Não define nota 0–10, pesos, média, thresholds ou classificação de senioridade — isso pertence à etapa da rubrica (ver [[Interview Evaluation MOC]]).

Fluxo geral:

```text
Pergunta
   ↓
Taxonomia
   ↓
Conhecimento relevante
   ↓
Resposta
   ↓
Evidências
   ↓
Interpretação técnica
   ↓
(etapa futura: Rubrica 0–10)
```

## 1. O que é uma evidência

Evidência é uma informação observável na resposta do candidato que permite sustentar uma conclusão sobre determinado conhecimento, raciocínio, aplicação ou experiência. Uma evidência deve ser vinculável àquilo que foi efetivamente dito pelo candidato — não inventar detalhes não apresentados.

Exemplo:

```text
Pergunta: "O que é Dependency Injection?"
Resposta: "É um mecanismo em que as dependências de um objeto são fornecidas
           externamente, em vez de serem criadas pelo próprio objeto."

Evidência: O candidato demonstrou compreender que as dependências são
           fornecidas externamente ao objeto.
```

## 2. Evidência não é interpretação

Separar "o que o candidato disse" de "o que isso demonstra". A interpretação deve permanecer próxima da evidência, sem extrapolar além dela.

Exemplo:

```text
Resposta: "Eu uso interfaces para desacoplar as classes."

Evidência observada: O candidato relacionou interfaces a desacoplamento.
Interpretação: Há evidência de compreensão da utilização de abstrações
               para reduzir acoplamento.
```

## 3. Tipos de evidência quanto à correção

### 3.1 Evidência positiva
A resposta demonstra corretamente determinado conhecimento.

```text
O candidato explicou corretamente a diferença entre Platform Threads e
Virtual Threads e relacionou Virtual Threads ao modelo de threads leves da JVM.
```

### 3.2 Evidência parcial
O candidato demonstra parte do conhecimento esperado, mas deixa lacunas importantes. Parcial não significa incorreto.

```text
O candidato identificou corretamente o objetivo das Virtual Threads, mas não
conseguiu explicar suas limitações ou implicações de uso.
```

### 3.3 Evidência negativa / incorreta
O candidato apresenta uma afirmação tecnicamente incorreta, contradizendo o conhecimento técnico de referência. Registrar explicitamente a divergência, sem linguagem depreciativa — preferir "afirmação tecnicamente incorreta".

```text
O candidato afirmou que Virtual Threads são threads do sistema operacional
criadas diretamente para cada requisição.
```

### 3.4 Evidência contraditória
A resposta contém simultaneamente informações corretas e incorretas. Registrar as evidências separadamente; não resumir a resposta inteira como "correta" ou "incorreta" quando houver sinais mistos.

```text
O candidato explicou corretamente o objetivo da Arquitetura Hexagonal, mas
posteriormente afirmou que os adapters devem possuir dependências diretas
do domínio para que a arquitetura funcione.
```

### 3.5 Ausência de evidência
A ausência de determinada informação não deve ser automaticamente classificada como erro.

```text
Pergunta: "Explique Virtual Threads e suas limitações."
Resposta: "Virtual Threads são threads leves gerenciadas pela JVM."

Conclusão possível: Há evidência sobre a definição, mas não houve evidência
suficiente sobre limitações.
```

Não afirmar "o candidato desconhece as limitações".

### 3.6 Evidência insuficiente
A resposta não fornece material suficiente para uma conclusão confiável. Não preencher a lacuna com suposições.

```text
Resposta: "Depende do cenário."
Conclusão: Não há evidência suficiente para avaliar o conhecimento do
           candidato sobre o assunto.
```

## 4. Evidência por natureza do conhecimento

### 4.1 Aplicação prática
A resposta demonstra conhecimento através de aplicação, sem exagerar o que foi demonstrado.

```text
"Eu utilizaria uma porta para abstrair o acesso ao repositório e implementaria
o adapter fora do core."

Pode demonstrar: compreensão conceitual, aplicação arquitetural, entendimento
de Ports and Adapters, Dependency Inversion.
```

### 4.2 Raciocínio
Em perguntas abertas ou de cenário, procurar evidências do processo de raciocínio (abordagem sistemática, decomposição do problema, priorização de hipóteses).

```text
"Primeiro eu verificaria se o aumento de latência está concentrado em
determinada rota. Depois compararia métricas de aplicação com dependências
externas e analisaria traces."
```

### 4.3 Troubleshooting
Em perguntas de diagnóstico, procurar elementos como: sintoma, hipótese, métrica, log, trace, correlação, investigação, validação, causa, correção, prevenção. Não exigir todos os elementos em toda pergunta — a presença esperada depende da pergunta (ver [[Question Taxonomy]]).

```text
O candidato não começou alterando configuração. Primeiro propôs observar
métricas e traces para localizar o componente responsável pela latência.
```

### 4.4 Trade-off
Quando a pergunta envolve decisões técnicas, procurar comparação entre alternativas, vantagens, desvantagens, custos, limitações, contexto, consequências, justificativa.

```text
O candidato não respondeu apenas que escolheria microsserviços; explicou que
consideraria o custo operacional e a necessidade de independência de deploy
antes de adotar a abordagem.
```

### 4.5 Experiência prática
Experiência deve ser tratada como evidência específica. Não assumir que uma única experiência comprova domínio geral da tecnologia.

```text
"Em produção tivemos aumento de HTTP 500. Eu utilizei Application Insights
para identificar que o problema estava em uma dependência externa."
```

## 5. Conhecimento declarado vs demonstrado

Distinguir declaração de evidência técnica demonstrada. Declarações podem ser registradas, mas não devem receber o mesmo peso de conhecimento efetivamente demonstrado.

```text
"Eu conheço Kubernetes." → declaração.
O candidato explicou corretamente como Kubernetes gerencia determinado
cenário. → evidência técnica demonstrada.
```

### Explicação correta sem experiência

```text
O candidato explicou corretamente o funcionamento de Application Insights,
mas não apresentou experiência real de utilização.

Registrar: Conhecimento conceitual demonstrado. Experiência prática não demonstrada.
```

### Experiência sem explicação conceitual

```text
O candidato descreveu uma solução utilizada em produção, mas não conseguiu
explicar o motivo técnico da decisão.

Registrar: Experiência prática demonstrada. Fundamentação conceitual limitada.
```

Não concluir automaticamente que a experiência foi falsa.

## 6. Relação entre conceitos

Uma das evidências mais importantes para avaliar profundidade é a capacidade de conectar conceitos.

```text
"Eu usaria Ports na fronteira da aplicação para inverter a dependência e
conseguir substituir o adapter nos testes."

Ports → Dependency Inversion → Adapters → Testabilidade
```

Isso constitui evidência de conhecimento integrado.

## 7. Superficialidade

Uma resposta pode estar correta, mas apresentar pouca profundidade. Não classificar como tecnicamente incorreta apenas por ser superficial.

```text
"Spring Boot facilita criar aplicações Java."

Registrar: Evidência conceitual limitada e superficial (não cobre como,
por quê, mecanismos, limitações, aplicação).
```

## 8. Relevância vs volume

Uma resposta longa não representa automaticamente maior conhecimento. Identificar informação relevante e informação irrelevante separadamente. Uma resposta pode conter muitos detalhes verdadeiros sem responder adequadamente à pergunta.

## 9. Respostas com múltiplas afirmações

Dividir respostas complexas em afirmações relevantes e avaliar cada uma separadamente.

```text
Resposta: "Virtual Threads são leves, são gerenciadas pela JVM e sempre
melhoram o desempenho da aplicação."

Evidência 1: Afirmação correta sobre leveza.
Evidência 2: Afirmação correta sobre gerenciamento pela JVM.
Evidência 3: Generalização potencialmente incorreta — Virtual Threads não
             garantem automaticamente melhoria de desempenho em qualquer cenário.
```

## 10. Contradições internas

Se o candidato disser algo e posteriormente contradizer a própria resposta, registrar ambas as evidências. Não escolher arbitrariamente uma delas. Considerar o contexto em que a contradição ocorreu, quando possível.

## 11. Fato técnico vs recomendação/preferência

Distinguir fato técnico de recomendação/preferência (ver também [[Evaluation Framework]]).

```text
"Eu prefiro usar arquitetura monolítica em sistemas pequenos." → preferência
tecnicamente defensável; não é erro apenas por divergir de outras alternativas.

"Microsserviços sempre são mais baratos." → afirmação factual generalizante
potencialmente problemática.
```

## 12. Contexto e premissas

Identificar contexto, premissas e limitações sob as quais uma afirmação é válida. Não penalizar uma resposta válida apenas por não cobrir todos os contextos possíveis, quando a pergunta não exigia isso.

## 13. Versionamento das evidências

Quando uma afirmação depender de versão, registrar a versão relevante e comparar com a nota correspondente. Não utilizar conhecimento de uma versão para julgar uma pergunta explicitamente sobre outra versão.

```text
O candidato descreveu comportamento específico do Java 21.
```

## 14. Evidência e fonte de referência

Quando a análise depender de uma nota técnica, registrar a relação com a referência, sem copiar a nota técnica inteira para o registro da avaliação.

```text
Conhecimento de referência: [[Virtual Threads]]
Evidência: O candidato demonstrou compreensão do modelo de execução das
           Virtual Threads.
```

## 15. Força da evidência

Classificação conceitual — **não é uma nota**:

- **Forte**: evidência clara, específica e tecnicamente consistente.
- **Moderada**: evidência relevante, mas limitada ou incompleta.
- **Fraca**: algum sinal presente, mas informação vaga ou pouco conclusiva.
- **Insuficiente**: não há material suficiente para sustentar uma conclusão.

## 16. Confiança da interpretação

Separar força da evidência de confiança da interpretação.

```text
Evidência: Forte
Confiança: Baixa
Motivo: A transcrição possui possível erro em um termo técnico que pode
        alterar a interpretação.
```

## 17. Evidências conflitantes

Quando existirem evidências positivas e negativas sobre o mesmo conceito, não resumir imediatamente. Registrar evidência positiva, evidência negativa e interpretação separadamente. A resolução final será feita pela etapa de avaliação (rubrica).

## 18. O que NÃO é evidência suficiente

Não considerar isoladamente como evidência forte:

- tempo de experiência declarado;
- cargo;
- formação;
- empresa onde trabalhou;
- certificações;
- quantidade de tecnologias no currículo;
- autodeclaração de senioridade;
- confiança ao falar;
- quantidade de palavras;
- velocidade da resposta;
- utilização de termos sofisticados sem explicação.

Esses elementos podem fornecer contexto, mas não substituem evidência técnica.

## 19. Confiança não é domínio

Um candidato pode falar com muita confiança e estar errado. Um candidato pode demonstrar hesitação e estar tecnicamente correto. Não utilizar confiança, eloquência ou fluidez como substitutos da correção técnica — avaliar o conteúdo.

## 20. Silêncio não é desconhecimento

Se o candidato não mencionar determinado conceito, registrar ausência de evidência quando relevante. Não registrar automaticamente "desconhecimento".

## 21. Erro de transcrição vs erro técnico

Quando uma afirmação parecer tecnicamente absurda, verificar se pode existir erro de transcrição, palavra truncada, termo técnico confundido ou contexto omitido. Em caso de dúvida significativa, marcar como incerto (`## A validar`).

## 22. Estrutura conceitual de uma evidência

```text
Evidência
├── Trecho / afirmação observada
├── Conceito relacionado
├── Tipo de evidência
├── Interpretação
├── Força
├── Confiança
└── Observações
```

Não é necessário formalizar isso como YAML nesta etapa — o objetivo é definir o modelo conceitual.

## 23. Exemplo completo

```text
Pergunta: "Como você investigaria uma API Spring Boot que começou a
apresentar aumento de latência?"

Resposta hipotética: "Primeiro eu verificaria se o problema está concentrado
em algum endpoint. Depois olharia métricas de latência, identificaria
dependências lentas e utilizaria traces para entender onde o tempo está
sendo gasto."

Domínios: Spring, Performance, Observability, Troubleshooting

Evidência 1: Propôs identificar se a latência está concentrada em
             determinados endpoints. — Tipo: Diagnóstico — Força: Forte
Evidência 2: Propôs analisar métricas de latência. — Tipo: Observabilidade
             — Força: Forte
Evidência 3: Propôs identificar dependências lentas. — Tipo:
             Troubleshooting/Diagnóstico — Força: Forte
Evidência 4: Propôs utilizar traces para localizar onde o tempo está sendo
             consumido. — Tipo: Observabilidade/Diagnóstico — Força: Forte

Interpretação: A resposta demonstra uma estratégia estruturada de
investigação de latência utilizando métricas, dependências e traces.
```

Ainda **não** atribuir nota.

## 24. Exemplo de resposta parcialmente correta

```text
Pergunta: "Como investigaria uma API lenta?"
Resposta: "Eu verificaria o CPU e a memória e depois tentaria aumentar os
recursos da aplicação."

Positiva: O candidato considera métricas de infraestrutura.
Parcial: A abordagem não contempla inicialmente métricas de aplicação,
         dependências, logs ou traces.
Negativa: Aumentar recursos é apresentado como possível solução antes da
          identificação da causa.
```

Não atribuir nota nesta etapa.

## 25. Modelo mental final

```text
Resposta do candidato
   ↓
Afirmações observáveis
   ↓
Evidências
   ↓
Conceito relacionado
   ↓
Interpretação
   ↓
Força da evidência
   ↓
Confiança da interpretação
```

Somente posteriormente: Evidências → Rubrica → Nota 0–10 (etapas futuras).

## 26. Integração com a Taxonomia

O modelo de evidências deve consumir a classificação criada em [[Question Taxonomy]]. As evidências esperadas dependem da pergunta e da sua taxonomia — não utilizar uma lista fixa de evidências para todas as perguntas.

```text
Taxonomia: Tipo = Troubleshooting; Dimensões = Diagnóstico + Performance +
Observabilidade; Complexidade = Avançada

A análise da resposta deverá procurar evidências relacionadas a essas dimensões.
```

## 27. Integração com o Second Brain

As evidências devem ser comparadas ao conhecimento técnico existente, utilizando as notas como referência sem copiá-las para a avaliação.

```text
Pergunta → Taxonomia → [[Application Insights]], [[Azure Monitor]], [[KQL]]
→ Resposta → Evidências
```

## 28. Evidência de entrevista vs. evidência externa vs. experiência declarada

Todas as seções anteriores descrevem evidência produzida pela própria resposta do candidato durante a entrevista. Esta seção formaliza a distinção entre essa evidência e outras fontes de informação que podem estar disponíveis (ver também [[Job Context Model]], que consome esta distinção ao analisar aderência à vaga):

- **Interview Evidence** (evidência de entrevista): tudo aquilo produzido pela resposta do candidato durante a avaliação — é a evidência descrita nas seções 1 a 26 desta nota (positiva, parcial, incorreta, contraditória, ausente, insuficiente).
- **External Evidence** (evidência externa): informação proveniente de fontes fora da resposta avaliada — currículo, portfólio, GitHub, certificações, projetos declarados, documentação apresentada. Pode fornecer contexto adicional, mas **não deve ser tratada automaticamente como demonstração técnica equivalente à Interview Evidence**.
- **Declared Experience** (experiência declarada): afirmação do candidato sobre ter realizado algo ("já trabalhei com Kubernetes"), sem demonstração técnica concreta na resposta. É diferente de conhecimento demonstrado (ver seção 5) e diferente de evidência externa verificável.

Regra de separação:

```text
Declarado ≠ Demonstrado ≠ Verificado externamente
```

- Não promover Declared Experience ao mesmo peso de Interview Evidence.
- Não promover External Evidence ao mesmo peso de Interview Evidence.
- Registrar cada uma com seu rótulo próprio, nunca combinadas silenciosamente em uma única "evidência".

Exemplo:

```text
Interview Evidence: o candidato não foi questionado sobre Kubernetes.
External Evidence: o currículo declara 2 anos de experiência com Kubernetes.
Declared Experience: o candidato mencionou verbalmente "já usei Kubernetes
                      bastante", sem explicar como.

Conclusão: existe declaração e evidência externa de experiência, mas não há
Interview Evidence suficiente para avaliar tecnicamente o domínio de
Kubernetes.
```

## Ver também

- [[Evaluation Framework]]
- [[Question Taxonomy]]
- [[Interview Evaluation MOC]]
