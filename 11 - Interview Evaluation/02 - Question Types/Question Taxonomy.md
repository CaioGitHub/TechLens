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
# Question Taxonomy

Esta nota define a taxonomia utilizada para classificar perguntas técnicas de entrevistas.

## Princípio fundamental

A taxonomia responde:

```text
O que esta pergunta está tentando avaliar?
```

Ela **não** responde:

```text
O candidato respondeu corretamente?
```

A classificação da pergunta acontece antes da avaliação da resposta (ver [[Evaluation Framework]]). O modelo de evidências (etapa futura) responderá "o que devo procurar na resposta?" e a rubrica (etapa futura) responderá "quanto vale essa evidência?". Esta nota não implementa nota 0–10, pesos, score, média, classificação de senioridade ou recomendação de contratação.

## Estrutura de classificação

```text
Pergunta
├── Domínio(s)
├── Tipo principal
├── Dimensões secundárias
├── Complexidade
├── Versão relevante (quando aplicável)
└── Conhecimentos relacionados
```

Tipo, dimensão e complexidade são eixos independentes — não devem ser tratados como a mesma coisa:

- **Tipo principal**: a intenção predominante da pergunta (o que ela pede).
- **Dimensões secundárias**: aspectos adicionais avaliados junto ao tipo principal.
- **Complexidade**: a dificuldade da pergunta, independente do tipo ou da qualidade da resposta.

## 1. Domínio técnico

Primeiro nível de classificação. Lista inicial, não definitiva:

```text
Java
JVM
Spring
Architecture
Design Patterns
Azure
Observability
Troubleshooting
Software Engineering
Security
Database
Distributed Systems
DevOps
Testing
Performance
```

Uma pergunta pode pertencer a mais de um domínio; registrar todos os relevantes.

Exemplo:

```text
Pergunta: "Como você faria tracing distribuído entre microsserviços Spring Boot no Azure?"

Domínios: Spring, Distributed Systems, Azure, Observability
```

## 2. Tipo principal da pergunta

Representa a intenção predominante. Evitar múltiplas classificações principais quando uma for suficiente.

### 2.1 Conceitual
Avalia se o candidato entende o conceito.
Exemplo: "O que é Dependency Injection?"

### 2.2 Fundamentos
Avalia fundamentos técnicos que sustentam uma tecnologia ou conceito.
Exemplo: "Como funciona o Garbage Collector?"

### 2.3 Comparação
Pede comparação entre tecnologias, conceitos ou abordagens.
Exemplo: "Qual a diferença entre HashMap e ConcurrentHashMap?"

### 2.4 Implementação
Avalia capacidade de transformar conhecimento em implementação.
Exemplo: "Como você implementaria isso usando Spring Boot?"

### 2.5 Código
Avalia interpretação, correção, implementação ou análise de código.
Exemplo: "O que há de errado neste código?"

### 2.6 Arquitetura
Avalia decisões arquiteturais e estrutura de sistemas.
Exemplo: "Como você estruturaria uma aplicação utilizando Arquitetura Hexagonal?"

### 2.7 Design
Avalia capacidade de projetar uma solução para determinado problema.
Exemplo: "Como você desenharia uma API para esse cenário?"

### 2.8 Troubleshooting
Avalia capacidade de investigar e diagnosticar problemas.
Exemplo: "Como você investigaria uma aplicação com aumento de erros em produção?"

### 2.9 Performance
Avalia capacidade de identificar, analisar ou solucionar problemas de desempenho.
Exemplo: "Como você investigaria uma aplicação Java com alto consumo de CPU?"

### 2.10 Segurança
Avalia conhecimento e aplicação de práticas de segurança.
Exemplo: "Como você protegeria uma API REST?"

### 2.11 Observabilidade
Avalia utilização e compreensão de mecanismos de observabilidade.
Exemplo: "Como você utilizaria Application Insights para investigar uma falha?"

### 2.12 Cloud / Azure
Avalia conhecimento e tomada de decisão relacionada a cloud.
Exemplo: "Qual serviço do Azure você utilizaria nesse cenário?"

### 2.13 Trade-off / Decisão técnica
Avalia capacidade de comparar alternativas e justificar decisões.
Exemplo: "Quando você escolheria uma abordagem em vez de outra?"

### 2.14 Experiência prática
Avalia experiência real do candidato.
Exemplo: "Conte sobre um problema de produção que você resolveu."

### 2.15 Cenário / Caso prático
Apresenta um cenário e solicita solução ou raciocínio. **Uso restrito** (ver seção 9 e "Critério de desempate", seção 9.1): utilizar como tipo principal apenas quando o cenário for o formato central da pergunta e a ação solicitada não se enquadrar adequadamente em nenhum tipo mais específico (Troubleshooting, Arquitetura, Trade-off/Decisão técnica, Performance, Segurança, etc.). Quando um tipo mais específico for identificável, ele deve prevalecer — "Cenário/Caso prático" funciona como *fallback*, não como categoria padrão para toda pergunta que descreve uma situação.
Exemplo (uso válido, sem tipo mais específico aplicável): "Imagine que sua API recebe 10 milhões de requisições por dia. Como você projetaria essa solução?" → se a resposta esperada for predominantemente arquitetural, classificar como Arquitetura (ver 9.1); use Cenário/Caso prático somente se nenhuma categoria mais específica capturar adequadamente a intenção.

## 3. Dimensões secundárias

Lista inicial:

```text
Conhecimento conceitual
Fundamentos
Aplicação prática
Implementação
Diagnóstico
Arquitetura
Performance
Segurança
Observabilidade
Escalabilidade
Confiabilidade
Manutenibilidade
Testabilidade
Concorrência
Distribuição
Trade-offs
Tomada de decisão
Experiência prática
```

Usar apenas as dimensões que agreguem informação útil. Não preencher todas as dimensões em todas as perguntas (ver regra de não extrapolação, seção 8).

## 4. Complexidade da pergunta

Classificação independente do tipo e das dimensões. Representa a dificuldade da pergunta, não a senioridade do candidato nem a qualidade da resposta.

### Básica
Exige definição, reconhecimento, fundamentos, utilização simples.
Exemplo: "O que é uma interface em Java?"

### Intermediária
Exige compreensão, aplicação, comparação, relacionamento entre conceitos.
Exemplo: "Qual a diferença entre uma interface e uma classe abstrata e quando você utilizaria cada uma?"

### Avançada
Exige raciocínio, arquitetura, trade-offs, diagnóstico, múltiplos conceitos, decisões técnicas, análise de cenários complexos.
Exemplo: "Uma aplicação distribuída apresenta aumento de latência após uma alteração arquitetural. Como você investigaria o problema utilizando observabilidade no Azure?"

### Complexidade não é nota

```text
Complexidade da pergunta ≠ Qualidade da resposta ≠ Senioridade
```

Uma pergunta avançada pode receber uma resposta excelente ou ruim. Uma pergunta básica também pode revelar falta de conhecimento fundamental. A complexidade pertence à pergunta; a nota pertence à resposta (etapa futura). Não aumentar a complexidade atribuída a uma pergunta porque o candidato respondeu muito bem, nem reduzi-la porque respondeu mal — a classificação é sobre a exigência cognitiva/técnica da pergunta em si, determinada antes e independentemente da resposta.

### Justificativa da complexidade

Ao classificar a complexidade, quando relevante para a análise (ex.: perguntas de cenário avançado ou perguntas cuja complexidade não seja óbvia), registrar brevemente os fatores que a justificam:

```text
Complexidade: Avançada

Motivo: a pergunta exige investigação sem documentação, formulação de
hipóteses, uso de evidências, isolamento de causas e definição de
mitigação e correção definitiva.
```

Essa justificativa deve se basear apenas na exigência da pergunta (nível de raciocínio, número de conceitos envolvidos, ambiguidade, necessidade de diagnóstico ou decisão), nunca no desempenho do candidato.

## 5. Conhecimentos relacionados

Após classificar a pergunta, identificar quais notas do Second Brain são potencialmente relevantes para avaliá-la, utilizando links existentes. Não criar novas notas técnicas apenas para classificar uma pergunta.

Exemplos:

```text
Pergunta: "Explique Arquitetura Hexagonal."
Conhecimentos: [[Arquitetura Hexagonal]], [[Ports and Adapters]], [[Dependency Inversion]]
```

```text
Pergunta: "Como investigaria erros de uma aplicação no Azure?"
Conhecimentos: [[Azure Monitor]], [[Application Insights]], [[Log Analytics]], [[KQL]]
```

```text
Pergunta: "Quando utilizar Virtual Threads?"
Conhecimentos: [[Virtual Threads]], [[Java 21]], [[Concurrency]]
```

## 6. Relação com versões

Quando a pergunta depender de uma versão específica, registrar essa dependência.

Exemplo: "Como funcionam Virtual Threads no Java 21?" → Versão: Java 21.

Se a pergunta disser apenas "Como funcionam Virtual Threads?", verificar quais versões são relevantes na base. Não assumir que o comportamento de uma versão é universal.

## 7. Perguntas com múltiplos conceitos

Uma pergunta pode envolver vários conceitos e domínios sem deixar de ser uma única unidade de avaliação. Não transformar automaticamente cada conceito em uma pergunta separada.

Exemplo:

```text
Pergunta: "Como você implementaria um serviço Spring Boot utilizando Arquitetura Hexagonal e publicaria no Azure?"

Domínios: Spring, Architecture, Azure
Tipo principal: Implementação
Dimensões: Arquitetura, Aplicação prática, Cloud
Conhecimentos: [[Spring Boot]], [[Arquitetura Hexagonal]], [[Azure]]
```

## 8. Regra de não extrapolação

A taxonomia deve refletir o que a pergunta realmente solicita. Não adicionar dimensões ou conhecimentos apenas porque um assunto relacionado poderia, indiretamente, ser mencionado.

Exemplo: para "O que é Application Insights?", não adicionar automaticamente Performance, Troubleshooting, KQL ou Distributed Systems, mesmo que relacionados. Adicionar somente o que for relevante para a intenção da pergunta.

## 9. Perguntas de cenário

Classificar principalmente pela ação solicitada, não apenas pelo assunto mencionado no cenário.

Exemplo:

```text
Pergunta: "Você possui uma API lenta em produção. Como investigaria?"

Tipo: Troubleshooting
Dimensões: Diagnóstico, Performance, Observabilidade
```

### 9.1 Critério de desempate — Cenário/Caso prático vs. tipo específico

Esta regra resolve explicitamente a relação entre §2.15 ("Cenário / Caso prático") e a orientação acima: quando uma pergunta puder ser classificada simultaneamente como "Cenário / Caso prático" **e** como outro tipo mais específico, **o tipo mais específico sempre prevalece**. "Cenário / Caso prático" é um *fallback*, usado apenas quando nenhum tipo mais específico capturar adequadamente a ação solicitada.

```text
Cenário + Troubleshooting → Troubleshooting
Cenário + Arquitetura     → Arquitetura
Cenário + Segurança       → Segurança
Cenário + Performance     → Performance
Cenário + Trade-off       → Trade-off / Decisão técnica
```

Exemplos aplicando o desempate:

```text
"Uma API começou a retornar 500. Como você investigaria?"
→ Tipo principal: Troubleshooting (não Cenário/Caso prático)

"Imagine que você precise projetar uma API para suportar milhões de
requisições. Como faria?"
→ Tipo principal: Arquitetura (não Cenário/Caso prático)

"Você recebe este cenário e precisa decidir entre duas abordagens. Qual
escolheria e por quê?"
→ Tipo principal: Trade-off / Decisão técnica (não Cenário/Caso prático)
```

Usar "Cenário / Caso prático" apenas quando o formato de caso aplicado for o elemento central e não houver tipo mais específico adequado.

## 10. Perguntas de opinião

Não classificar automaticamente como correta ou incorreta.

Exemplo:

```text
Pergunta: "Você prefere arquitetura monolítica ou microsserviços?"

Tipo: Trade-off / Decisão técnica
Dimensões: Arquitetura, Tomada de decisão, Trade-offs
```

A avaliação posterior deverá verificar a justificativa técnica apresentada.

## 11. Perguntas comportamentais com conteúdo técnico

Quando a pergunta misturar experiência e conhecimento técnico, classificar o tipo principal como Experiência prática, sem tratá-la exclusivamente como pergunta conceitual.

Exemplo:

```text
Pergunta: "Conte sobre uma situação em que você precisou investigar um problema de performance em produção."

Tipo principal: Experiência prática
Dimensões: Troubleshooting, Performance, Experiência prática
```

## 12. Perguntas mal formuladas

Quando a pergunta estiver incompleta, ambígua, depender de contexto ausente ou tiver transcrição aparentemente incorreta, registrar a incerteza em vez de inventar contexto.

Exemplo:

```text
Classificação: Possivelmente Troubleshooting
Confiança da classificação: Baixa
Motivo: A pergunta possui contexto insuficiente.
```

## 13. Transcrições automáticas

Perguntas podem vir de transcrições automáticas e conter erros, por exemplo:

```text
"Java 21" → "Java vinte e um"
"Azure Monitor" → "Azure monitores"
"Application Insights" → "Application inside"
```

Usar o contexto para identificar possíveis termos técnicos corretos, sem modificar silenciosamente a transcrição original. Quando a interpretação não for segura, marcar para validação (`## A validar`).

## 14. Exemplos completos

```text
Pergunta: "Qual a diferença entre Platform Threads e Virtual Threads e quando você escolheria cada uma?"

Domínios: Java, JVM, Concurrency
Tipo principal: Comparação
Dimensões: Fundamentos, Concorrência, Trade-offs, Tomada de decisão
Complexidade: Intermediária
Versão relevante: Java 21
Conhecimentos relacionados: [[Virtual Threads]], [[Java 21]], [[Concurrency]]
```

```text
Pergunta: "Você possui uma aplicação Spring Boot rodando no Azure que começou a apresentar aumento de erros 500. Como investigaria?"

Domínios: Spring, Azure, Observability, Troubleshooting
Tipo principal: Troubleshooting
Dimensões: Diagnóstico, Observabilidade, Aplicação prática
Complexidade: Avançada
Conhecimentos relacionados: [[Spring Boot]], [[Azure Monitor]], [[Application Insights]], [[Log Analytics]], [[KQL]]
```

## Ver também

- [[Evaluation Framework]]
- [[Interview Evaluation MOC]]
