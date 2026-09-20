---
type: reference
status: learning
confidence: 100
created: 2026-09-17
updated: 2026-09-20
tags:
  - interview-evaluation
  - meta
---
# Stage 20 — Transcription Processing Model

Esta nota define o processo responsável por transformar uma transcrição bruta de entrevista em uma representação estruturada, rastreável e adequada ao [[Evaluation Engine]].

> **Corrigir forma é permitido. Criar conteúdo não é permitido.**

O processamento melhora a estrutura e a legibilidade da fonte sem alterar seu conteúdo factual ou técnico. A avaliação do conhecimento demonstrado permanece sob responsabilidade do [[Evidence Model]] e do [[Evaluation Engine]].

## 1. Objetivo e fluxo

```text
Transcrição Bruta
↓
Identificação de Participantes
↓
Normalização
↓
Detecção de Perguntas
↓
Reconstrução de Trechos
↓
Associação Pergunta ↔ Resposta
↓
Identificação de Follow-ups
↓
Validação
↓
Entrevista Estruturada
↓
Evidence Model
↓
Evidence Set
↓
Evaluation Engine
```

A Stage 20 interpreta a estrutura da transcrição, identifica participantes, perguntas, respostas e follow-ups, reconstrói apenas erros evidentes, marca ambiguidades, preserva a ordem temporal e mantém a origem das informações.

Ela **não** atribui notas, avalia conhecimento, determina senioridade, infere competência, melhora tecnicamente respostas, completa falas com conhecimento externo ou remove respostas por parecerem incorretas.

## 2. Preservação da evidência

A transcrição original é a fonte primária do conteúdo verbal. A forma pode ser normalizada quando houver evidência suficiente, mas o significado não pode ser alterado.

Reconstrução permitida:

```text
"Spring Boot ele facilita a criação de API REST por causa das configurações automática."
→
"Spring Boot facilita a criação de APIs REST por causa das configurações automáticas."
```

Reconstrução proibida:

```text
"Eu usaria o Application..."
→
"Eu usaria o Application Insights para analisar as dependências."
```

Quando o trecho não for identificável, preservar o conteúdo incompleto:

```text
"Eu usaria o Application [trecho não identificado]."
```

Respostas tecnicamente incorretas, hipóteses, condicionais, expressões de incerteza e experiências declaradas devem permanecer como foram ditas. O processamento não transforma `"Eu tentaria usar..."` em `"Eu usaria..."`, nem `"Já trabalhei com Azure"` em experiência comprovada.

## 3. Níveis de reconstrução

Cada reconstrução deve registrar sua confiança:

```yaml
reconstruction_confidence: high | medium | low
needs_review: true | false
```

- **Alta**: significado praticamente inequívoco, como `"Java vinte e um"` → `"Java 21"`.
- **Média**: contexto sustenta uma interpretação plausível, como `"application insight"` → `"Application Insights"` em uma conversa sobre Azure Monitor e Log Analytics.
- **Baixa**: há múltiplas interpretações possíveis; não escolher arbitrariamente e marcar para revisão.

Usar conhecimento técnico apenas para reconhecer termos quando o contexto sustentar a interpretação. Nunca utilizá-lo para completar uma frase ou fabricar uma resposta.

## 4. Participantes e candidato

Identificar participantes por informação explícita, contexto fornecido ou identificação consistente das falas. Não inferir nomes por voz, cargo, estilo ou conteúdo técnico.

```yaml
participants:
  - id: interviewer_1
    name: Caio
    role: interviewer
    confidence: high
  - id: candidate
    name: Ingrid
    role: candidate
    confidence: high
```

Papéis possíveis: `candidate`, `interviewer`, `coordinator`, `observer` e `unknown`. Quando só houver `"Pessoa 1"` e `"Pessoa 2"`, preservar esses identificadores.

O candidato deve ser identificado prioritariamente pela transcrição ou pelo contexto fornecido. Se não houver segurança suficiente:

```yaml
candidate_identification:
  status: uncertain
  confidence: low
```

## 5. Normalização

A normalização pode corrigir pontuação, ortografia evidente, números, abreviações, nomes técnicos, repetições causadas pela transcrição e timestamps redundantes da fala estruturada:

```text
"Java vinte e um" → "Java 21"
"Spring boot" → "Spring Boot"
"Azure monitor" → "Azure Monitor"
"c sharp" → "C#"
```

Ela não pode alterar uma afirmação técnica, remover uma resposta imperfeita ou sobrescrever a transcrição original. A fonte original deve ser preservada separadamente sempre que o processamento fizer parte de uma entrevista real.

## 6. Perguntas

Identificar perguntas explícitas, contextualizadas e implícitas somente quando a ação solicitada estiver efetivamente presente. Uma fala como `"Tá, e nesse cenário, como você faria?"` deve ser preservada como follow-up dependente do contexto anterior; não criar uma pergunta técnica que não foi feita.

Preservar também perguntas não técnicas: apresentação, comportamento, disponibilidade, experiência, dúvidas da vaga e questões administrativas. A classificação técnica pertence à [[Question Taxonomy]].

Cada pergunta recebe identificador estável (`Q1`, `Q2`, `Q3.1`), sem significado de qualidade, dificuldade, domínio ou nota.

## 7. Associação entre perguntas e respostas

Associar cada pergunta à resposta correspondente quando houver evidência suficiente:

```text
Q1
└── R1

Q3
├── R3
├── Q3.1
│   └── R3.1
└── Q3.2
    └── R3.2
```

Uma resposta pode ser direta, parcialmente direta, interrompida, composta por múltiplos trechos ou complementada por follow-ups.

Se houver resposta sem pergunta identificável:

```yaml
question_id: unknown
response_id: R08
question_status: missing
```

Não criar pergunta artificial. Se houver pergunta sem resposta:

```yaml
question_id: Q09
response_status: missing
```

Isso significa apenas que não há resposta identificável, nunca que o candidato não sabe.

## 8. Follow-ups, interrupções e sobreposição

Follow-ups preservam sua relação com a pergunta principal e não são tratados automaticamente como perguntas independentes:

```text
Q5: Como você investigaria um erro 500?
R5: Eu começaria pelos logs.
Q5.1: E se não encontrasse nada nos logs?
R5.1: Eu verificaria o Application Insights.
```

Interrupções e falas sobrepostas devem permanecer como falas separadas. Preservar a sequência temporal; quando a ordem for incerta:

```yaml
sequence_confidence: low
```

Não fundir artificialmente falas de entrevistador e candidato.

## 9. Ambiguidades e trechos incompreensíveis

Termos técnicos podem ser reconstruídos quando o contexto eliminar interpretações plausíveis alternativas:

```text
"application inside" → "Application Insights"
"azure monitores" → "Azure Monitor"
```

Para termos ambíguos, como `"monitor"`, marcar:

```yaml
ambiguity: true
needs_review: true
```

Quando não for possível reconstruir com segurança, usar `[trecho incompreensível]` ou `[inaudível]` e preservar o timestamp original quando disponível:

```yaml
source_timestamp: "08:42"
status: unclear
```

Uma pergunta como `"como que você faria aquele negócio lá de java..."` não pode ser transformada em uma pergunta específica de Java sem evidência adicional.

## 10. Rastreabilidade

Cada pergunta e resposta deve apontar para a transcrição original:

```yaml
question_id: Q07
source:
  start: "08:41"
  end: "08:57"

response_id: R07
source:
  start: "08:58"
  end: "09:34"
```

Quando houver vários trechos, usar uma lista de intervalos. A rastreabilidade é parte da confiabilidade e permite distinguir reconstrução de conteúdo original.

## 11. Estrutura mínima de saída

```yaml
interview:
  candidate:
  candidate_identification:
    status: identified | uncertain
    confidence: high | medium | low
  participants:
    - id:
      name:
      role:
      confidence:

  questions:
    - question_id:
      question:
      response:
      type:
      reconstruction_confidence:
      sequence_confidence:
      question_status: identified | partially_identified | uncertain | missing
      response_status: identified | partially_identified | uncertain | missing
      source:
      follow_up_of:
      needs_review: false
```

O resultado pode ser apresentado em Markdown para leitura humana, com pergunta, resposta, status, confiança de reconstrução e origem temporal.

## 12. Validação

Antes de enviar a entrevista ao `Evaluation Engine`, verificar:

- candidato e participantes identificados ou explicitamente marcados como incertos;
- cada pergunta possui identificador;
- perguntas e respostas reconstruídas possuem confiança;
- perguntas sem resposta e respostas sem pergunta foram preservadas;
- follow-ups estão vinculados corretamente;
- a ordem temporal e as sobreposições foram tratadas;
- nenhum conteúdo foi inventado;
- respostas não foram tecnicamente corrigidas;
- hipóteses, condicionais, declarações de experiência e incertezas foram preservadas;
- trechos incompreensíveis continuam identificados;
- toda pergunta e resposta possui origem quando disponível.

## 13. Gate de qualidade

A entrevista só segue para avaliação quando a estrutura for suficientemente confiável:

```text
READY
READY_WITH_WARNINGS
BLOCKED
```

- **READY**: estrutura de alta confiança, sem problemas relevantes.
- **READY_WITH_WARNINGS**: ambiguidades existem, mas não impedem a avaliação; os avisos acompanham o resultado.
- **BLOCKED**: problemas impedem identificar adequadamente perguntas ou respostas relevantes.

Uma entrevista `READY_WITH_WARNINGS` pode seguir para avaliação. O gate avalia a qualidade estrutural da transcrição, não o desempenho do candidato.

## 14. Relação com as etapas seguintes

```text
Transcrição
↓
Transcription Processing
↓
Pergunta + Resposta
↓
Evidence Model
↓
Evidências
↓
Evaluation Engine
↓
Nota
```

A Stage 20 organiza a fonte; não cria evidências técnicas. A [[Question Taxonomy]] classifica a intenção da pergunta. O [[Evidence Model]] interpreta o que foi demonstrado. O [[Evaluation Engine]] avalia correção, completude, profundidade, experiência demonstrada, lacunas e notas.

`reconstruction_confidence` e `evaluation_confidence` são independentes: uma reconstrução textual pode ter confiança média e ainda fornecer evidência suficiente para uma avaliação de alta confiança.

## 15. Persistência

Em entrevistas reais:

```text
05 - Interview Records/
├── Ingrid Mazoni - Transcrição Original.md
└── Ingrid Mazoni - Entrevista Estruturada.md
```

A transcrição original não deve ser sobrescrita. A entrevista estruturada deve apontar para sua origem.

O relatório final, quando a avaliação for concluída, permanece responsabilidade da camada de avaliação e deve ser salvo em:

```text
11 - Interview Evaluation/06 - Reports/Relatório-{nomeCandidato}.md
```

O processamento estruturado é uma etapa intermediária e não substitui nem gera diretamente o relatório final.

## Regra de ouro

> **Não inventar.**
>
> **Não avaliar.**
>
> **Não melhorar tecnicamente a resposta.**
>
> **Não transformar ausência de transcrição em ausência de conhecimento.**
>
> **Não transformar contexto técnico em conteúdo que não foi dito.**
>
> **Preservar incertezas e rastreabilidade.**
>
> **Separar reconstrução de avaliação.**

## Ver também

- [[Evaluation Framework]]
- [[Interview Evaluation Model]]
- [[Question Taxonomy]]
- [[Evidence Model]]
- [[Evaluation Engine]]
- [[Interview Evaluation MOC]]
