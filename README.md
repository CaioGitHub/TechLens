---
type: reference
created: 2026-09-08
updated: 2026-09-09
tags:
  - meta
---
# Second Brain Técnico

## Propósito

Este repositório é um Second Brain técnico construído para organizar, conectar e reutilizar conhecimento sobre:

* Java 18+;
* JVM;
* Spring;
* Arquitetura de Software;
* Arquitetura Hexagonal;
* Clean Architecture;
* SOLID;
* DDD;
* Azure;
* Azure Monitor;
* Application Insights;
* Log Analytics;
* KQL;
* Observabilidade;
* Cloud;
* Troubleshooting;
* projetos práticos.

O objetivo não é apenas armazenar anotações, mas construir uma rede de conhecimento conectada por links internos do Obsidian.

A base deve permitir:

> Encontrar rapidamente aquilo que eu já sei e descobrir aquilo que ainda preciso aprender.

---

# Como a estrutura está organizada

```text
00 - Inbox/ — entrada de conteúdo bruto, ainda não processado.

01 - Concepts/ — conceitos fundamentais e reutilizáveis.

02 - Technologies/ — conhecimento sobre ferramentas e tecnologias específicas.

03 - Architecture/ — estilos e arquiteturas de software.

04 - Patterns/ — padrões de projeto e design patterns.

05 - Observability/ — conhecimento sobre observabilidade.

06 - Guides/ — guias práticos passo a passo.

07 - Troubleshooting/ — problemas reais, diagnóstico e solução.

08 - Projects/ — aplicações práticas do conhecimento em projetos.

09 - References/ — materiais externos, fontes e referências.

10 - Integration/ — visão end-to-end conectando as áreas técnicas.

11 - Interview Evaluation/ — regras, modelos e artefatos
relacionados à avaliação técnica de candidatos.

99 - Templates/ — modelos reutilizáveis para criação de novas notas.
```

---

# Visão de navegação

```text
Fundamentos
    ↓
Java
    ↓
Arquitetura
    ↓
Framework
    ↓
Cloud
    ↓
Observabilidade
    ↓
Investigação
    ↓
Integração
```

A porta de entrada para a visão integrada é:

```text
10 - Integration/
```

A avaliação técnica utiliza essa base como fonte de conhecimento, mas permanece separada dela:

```text
Base técnica
    ↓
10 - Integration/
    ↓
11 - Interview Evaluation/
```

---

# Papel de cada diretório

Cada diretório representa uma finalidade específica.

## 00 - Inbox

Entrada de conteúdo bruto:

* anotações rápidas;
* dúvidas;
* descobertas;
* ideias;
* trechos de estudo;
* informações ainda não classificadas.

O Inbox não deve se transformar em uma segunda base de conhecimento.

---

## 01 - Concepts

Conceitos fundamentais.

Foco:

> o que é e por quê.

Exemplos:

* Dependency Inversion;
* Dependency Injection;
* Immutability;
* Concurrency;
* Coupling;
* Cohesion.

---

## 02 - Technologies

Tecnologias e ferramentas específicas.

Foco:

> como funciona e como utilizar.

Exemplos:

* Java;
* Spring Boot;
* Azure;
* Application Insights;
* Log Analytics.

---

## 03 - Architecture

Arquiteturas e estilos arquiteturais.

Exemplos:

* Arquitetura Hexagonal;
* Clean Architecture;
* princípios arquiteturais;
* decisões arquiteturais.

---

## 04 - Patterns

Padrões de projeto e soluções recorrentes.

---

## 05 - Observability

Conhecimento relacionado a:

* Azure Monitor;
* Application Insights;
* Log Analytics;
* KQL;
* métricas;
* logs;
* traces;
* alertas;
* investigação de incidentes.

---

## 06 - Guides

Procedimentos e guias práticos.

---

## 07 - Troubleshooting

Problemas reais e reutilizáveis.

Uma nota de troubleshooting deve, quando aplicável, registrar:

```text
Sintoma
Contexto
Hipóteses
Diagnóstico
Causa
Solução
Prevenção
Comandos / Queries
```

---

## 08 - Projects

Experiências aplicadas a projetos concretos.

---

## 09 - References

Fontes externas utilizadas para validar ou aprofundar conhecimento.

---

## 10 - Integration

Camada de integração técnica.

Seu objetivo é conectar conceitos de diferentes domínios em fluxos end-to-end.

Exemplo:

```text
Java
  ↓
Spring Boot
  ↓
Arquitetura Hexagonal
  ↓
Application Service
  ↓
Repository Port
  ↓
Adapter
  ↓
Azure
  ↓
Application Insights
  ↓
Azure Monitor
  ↓
Log Analytics
  ↓
KQL
```

Esta camada não substitui as notas individuais.

Ela demonstra como os conceitos trabalham juntos.

---

# 11 - Interview Evaluation

Esta é uma camada separada da base de conhecimento técnico.

Seu objetivo é utilizar o conhecimento existente para auxiliar na análise de entrevistas técnicas.

O fluxo futuro será aproximadamente:

```text
Agenda / Transcrição
        ↓
Perguntas técnicas
        ↓
Identificação do tema
        ↓
Identificação do tipo de pergunta
        ↓
Consulta ao Second Brain
        ↓
Análise da resposta
        ↓
Evidências
        ↓
Avaliação
        ↓
Nota
        ↓
Relatório
```

A pasta `11 - Interview Evaluation/` deve conter regras e estruturas relacionadas à avaliação.

Ela não deve duplicar o conhecimento existente em:

```text
01 - Concepts/
02 - Technologies/
03 - Architecture/
05 - Observability/
...
```

Quando a avaliação precisar consultar um conceito técnico, deve utilizar links para a nota existente.

---

# Separação entre conhecimento e avaliação

A base possui duas funções distintas:

```text
BASE DE CONHECIMENTO
        │
        │ responde:
        │ "O que é tecnicamente correto?"
        ▼
01–10

CAMADA DE AVALIAÇÃO
        │
        │ responde:
        │ "Quanto desse conhecimento o candidato demonstrou?"
        ▼
11 - Interview Evaluation/
```

Essa separação é fundamental.

Uma nota técnica não deve ser alterada simplesmente para acomodar a resposta de um candidato.

---

# Como o Inbox deve ser utilizado

O Inbox é o ponto de entrada para conteúdo ainda não organizado.

Nada deve ficar "polido" aqui.

O objetivo é:

> capturar rápido, organizar depois.

Quando o conteúdo for processado:

```text
Inbox
  ↓
Interpretação
  ↓
Classificação
  ↓
Pesquisa de conhecimento existente
  ↓
Atualização / criação
  ↓
Links
  ↓
MOCs
```

---

# Como o Codex deverá atuar

O Codex atuará como:

> **Knowledge Manager**

da base.

Suas principais responsabilidades são:

* criar notas;
* atualizar notas;
* evitar duplicações;
* criar relações;
* manter MOCs;
* identificar lacunas;
* processar Inbox;
* preservar conhecimento;
* validar consistência;
* considerar versionamento;
* registrar fontes quando necessário.

Além disso, o Codex poderá atuar como:

> **Technical Interview Evaluator**

quando explicitamente solicitado.

Nesse papel, deverá consultar a base técnica e aplicar as regras presentes em:

```text
11 - Interview Evaluation/
```

---

# Princípios básicos

1. Uma nota, um conceito.
2. Procure antes de criar.
3. Prefira reutilização.
4. Rede antes de hierarquia.
5. Use links para representar relações.
6. Use MOCs para navegação.
7. Mantenha YAML consistente.
8. Registre versões quando relevantes.
9. Preserve conhecimento válido.
10. Não invente informações.
11. Evite duplicação.
12. Evite overengineering.
13. Separe conhecimento técnico de experiência.
14. Separe conhecimento técnico de avaliação de candidatos.

---

# Objetivo de longo prazo

A evolução esperada do Second Brain é:

```text
CONHECIMENTO
     ↓
CONEXÕES
     ↓
CONTEXTO
     ↓
RECUPERAÇÃO
     ↓
ANÁLISE
```

A base deve ser capaz de fornecer contexto técnico suficiente para que o Codex consiga analisar problemas, estudar conceitos e, posteriormente, auxiliar na avaliação técnica de candidatos.

A camada de avaliação deve utilizar a base como referência sem transformar o conhecimento em um gabarito rígido.
