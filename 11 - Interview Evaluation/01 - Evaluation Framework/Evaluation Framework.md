---
type: reference
status: learning
created: 2026-09-09
updated: 2026-09-09
tags:
  - interview-evaluation
  - framework
---
# Evaluation Framework

Este documento define os princípios fundamentais da camada de avaliação técnica de candidatos. Ele estabelece o modelo conceitual que será utilizado pelas etapas futuras (taxonomia de perguntas, modelo de evidências, rubrica 0–10, motor de avaliação, etc.).

Esta nota **não** implementa rubricas, pesos, cálculo de média, score automático, classificação de senioridade ou recomendação de contratação. Esses elementos pertencem a etapas posteriores (ver [[Interview Evaluation MOC]]).

## 1. Avaliação baseada em evidências

A avaliação deve considerar apenas aquilo que o candidato efetivamente demonstrou durante a entrevista. Lacunas não devem ser preenchidas com suposições.

```text
O candidato não mencionou X.
```

não significa automaticamente:

```text
O candidato não conhece X.
```

Conclusão apropriada:

```text
Não houve evidência suficiente para avaliar o domínio de X.
```

## 2. Pergunta como unidade de avaliação

A unidade fundamental da avaliação é:

```text
Pergunta + Resposta + Contexto + Conhecimento técnico relacionado
```

Fluxo de análise:

```text
Pergunta
   ↓
O que está sendo perguntado?
   ↓
Qual conceito está sendo avaliado?
   ↓
Qual seria uma resposta tecnicamente aceitável?
   ↓
O que o candidato respondeu?
   ↓
Quais evidências existem?
```

## 3. O Second Brain como fonte de referência

O Second Brain é uma fonte de referência técnica, não um gabarito textual. A avaliação deve consultar as notas existentes relacionadas ao tema perguntado.

Exemplo:

```text
Pergunta: "O que é Arquitetura Hexagonal?"

Referências possíveis:
[[Arquitetura Hexagonal]]
[[Ports and Adapters]]
[[Dependency Inversion]]
```

O candidato não precisa reproduzir a mesma terminologia ou estrutura das notas. O que importa é a correção conceitual.

## 4. Avaliação semântica

A avaliação deve considerar significado, não apenas palavras-chave. Não utilizar regras simplistas como "mencionou todas as palavras da nota = correto" ou "não mencionou uma palavra = errado".

Avaliar:

- entendimento;
- coerência;
- relações entre conceitos;
- precisão técnica;
- aplicação;
- capacidade de explicar;
- reconhecimento de limitações;
- trade-offs quando pertinentes.

## 5. Respostas alternativas válidas

Uma resposta pode ser considerada correta mesmo quando:

- utiliza terminologia diferente;
- apresenta outra implementação;
- utiliza outro exemplo;
- segue outra ordem de explicação;
- apresenta uma solução arquitetural diferente;
- utiliza uma experiência prática diferente.

Desde que seja tecnicamente válida no contexto da pergunta.

## 6. Contexto técnico e versionamento

A mesma resposta pode ser correta em um contexto e incorreta em outro. Deve-se verificar:

- versão da tecnologia;
- contexto arquitetural;
- cenário apresentado;
- limitações e premissas;
- objetivo da solução.

Especialmente relevante para: Java 18, Java 21, Spring Boot, Azure, Azure Monitor, Application Insights, Log Analytics, KQL, Arquitetura Hexagonal.

## 7. Correção vs completude

```text
Correção ≠ Completude
```

Uma resposta pode estar tecnicamente correta e, ainda assim, incompleta.

Exemplo:

```text
"Virtual Threads são threads leves gerenciadas pela JVM."
```

Essa afirmação pode estar correta, mas insuficiente se a pergunta exigir funcionamento, vantagens, limitações e casos de uso.

Não classificar uma resposta correta como errada apenas por ser incompleta.

## 8. Profundidade

Profundidade é a quantidade e qualidade de entendimento técnico demonstrado:

```text
Definição
   ↓
Funcionamento
   ↓
Aplicação
   ↓
Relação com outros conceitos
   ↓
Trade-offs
   ↓
Limitações
   ↓
Raciocínio técnico
```

A profundidade exigida deve ser proporcional ao que a pergunta solicita. Não exigir profundidade que a pergunta não pede.

## 9. Conhecimento vs experiência

Manter separados:

- conhecimento conceitual;
- experiência prática;
- aplicação prática demonstrada.

Um candidato pode explicar Arquitetura Hexagonal sem nunca tê-la utilizado em produção (conhecimento conceitual sem experiência). Outro pode ter utilizado uma tecnologia sem conseguir explicar seus fundamentos (experiência sem conhecimento articulado).

## 10. Fato vs opinião

Distinguir:

- fato técnico;
- opinião técnica;
- preferência pessoal;
- experiência pessoal.

Não penalizar uma opinião apenas por divergir da abordagem mais comum. Quando uma opinião for apresentada como fato técnico e estiver incorreta, isso pode ser considerado na avaliação.

## 11. Incerteza

Reconhecer quando não há evidência suficiente para uma avaliação segura:

```text
Evidência forte
Evidência moderada
Evidência limitada
Sem evidência suficiente
```

Não transformar incerteza em certeza artificial.

## 12. Perguntas ambíguas

Se a pergunta estiver mal formulada, incompleta ou permitir múltiplas interpretações:

1. identificar a ambiguidade;
2. interpretar pelo contexto disponível;
3. registrar a interpretação utilizada;
4. evitar penalizar o candidato por uma interpretação razoável.

Se não for possível determinar o objetivo da pergunta, registrar em `## A validar`.

## 13. Transcrição imperfeita

Entrevistas obtidas por transcrição automática podem conter erros de reconhecimento, palavras trocadas, termos técnicos incorretos, frases incompletas, interrupções e sobreposição de falas.

Um erro evidente de transcrição não deve ser tratado automaticamente como erro técnico do candidato. Em caso de dúvida, registrar em `## A validar`.

## 14. Neutralidade

A avaliação deve se basear na resposta e nas evidências disponíveis. Não utilizar nome do candidato, empresa anterior, cargo informado, tempo de experiência, formação ou percepção pessoal como substitutos da evidência técnica apresentada.

O contexto profissional poderá ser utilizado posteriormente quando explicitamente necessário, mas não substitui a análise da resposta.

## 15. Separação entre avaliação e decisão

```text
Avaliação técnica ≠ Decisão de contratação
```

O objetivo do framework é medir o conhecimento técnico demonstrado. A decisão de contratação pertence ao processo humano e a outros fatores. Não concluir automaticamente "contratar" ou "reprovar" com base apenas na avaliação técnica.

## 16. Estrutura conceitual futura

O framework está preparado para suportar, em etapas futuras:

```text
Entrevista
   ↓
Pergunta
   ↓
Tema
   ↓
Conhecimento de referência
   ↓
Resposta
   ↓
Evidências
   ↓
Critérios
   ↓
Nota 0–10
   ↓
Justificativa
   ↓
Média
   ↓
Relatório
```

Os mecanismos de pontuação (rubrica, pesos, score, média) **não** são implementados nesta etapa.

## 17. Integração com a base técnica

A avaliação deve navegar pela rede de conhecimento existente para obter contexto, em vez de duplicá-lo.

Exemplos:

```text
Pergunta sobre Virtual Threads
   ↓
[[Virtual Threads]]
   ↓
[[Java 21]]
   ↓
[[Concurrency]]
```

```text
Pergunta sobre Arquitetura Hexagonal
   ↓
[[Arquitetura Hexagonal]]
   ↓
[[Ports and Adapters]]
   ↓
[[Dependency Inversion]]
```

```text
Pergunta sobre observabilidade no Azure
   ↓
[[Azure Monitor]]
   ↓
[[Application Insights]]
   ↓
[[Log Analytics]]
   ↓
[[KQL]]
```

## Ver também

- [[Interview Evaluation MOC]]
