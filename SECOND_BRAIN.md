---
type: reference
created: 2026-09-08
updated: 2026-09-08
tags:
  - meta
---
# SECOND_BRAIN.md — Constituição da Base de Conhecimento

Este documento define como esta base de conhecimento funciona: princípios, regras e fluxos de decisão.

`AGENTS.md` traduz estas regras em instruções operacionais para o Codex.

`README.md` descreve a estrutura de pastas e a navegação da base.

---

# 1. Objetivo

Construir uma rede de conhecimento técnico pessoal, não um arquivo de anotações.

A base deve otimizar para:

> "Encontrar rapidamente aquilo que eu já sei e descobrir aquilo que ainda preciso aprender."

Foco inicial:

* Java 18+;
* JVM;
* Spring;
* Arquitetura de Software;
* Hexagonal Architecture;
* Clean Architecture;
* SOLID;
* DDD;
* Azure;
* Azure Monitor;
* Application Insights;
* Log Analytics;
* KQL;
* Observability;
* Cloud;
* Troubleshooting;
* projetos reais.

A base permanece aberta a novos domínios.

---

# 2. Princípios de organização

## Notas atômicas

Uma nota representa um conceito ou unidade de conhecimento que pode ser entendido e reutilizado de forma independente.

## Reutilização antes de criação

Sempre procurar antes de criar.

## Rede antes de hierarquia

As conexões através de `[[links]]` importam mais do que a posição da nota no diretório.

## MOCs como mapas

MOCs organizam e direcionam a navegação.

Não devem duplicar o conteúdo das notas.

## Simplicidade

Evitar:

* burocracia;
* campos desnecessários;
* tags em excesso;
* estruturas profundas sem benefício;
* automações sem benefício claro.

---

# 3. Estrutura de conhecimento

```text
01 - Concepts/
02 - Technologies/
03 - Architecture/
04 - Patterns/
05 - Observability/
06 - Guides/
07 - Troubleshooting/
08 - Projects/
09 - References/
10 - Integration/
11 - Interview Evaluation/
99 - Templates/
````

A pasta `11 - Interview Evaluation/` é uma camada funcional sobre a base técnica e não substitui nenhuma das camadas anteriores.

Dentro de `11 - Interview Evaluation/`, os relatórios de entrevistas devem ser armazenados em:

```text
11 - Interview Evaluation/
└── 06 - Reports/
```

A pasta `06 - Reports/` é o destino padrão para os relatórios finais das entrevistas avaliadas.

Não criar uma pasta adicional chamada `Entrevistas` para essa finalidade quando `06 - Reports/` já existir.

---

# 4. Regras para criação de notas

Criar uma nova nota quando o conceito:

* possui identidade própria;
* pode ser referenciado por outras notas;
* possui explicação própria;
* possui exemplos ou trade-offs próprios;
* provavelmente será consultado novamente;
* possui relações importantes com outros conceitos.

Não criar uma nota nova para cada pequeno detalhe.

Exemplos:

```text
Virtual Threads.md
Structured Concurrency.md
Dependency Inversion.md
Application Insights Sampling.md
KQL summarize.md
```

Evitar:

```text
Java e Spring e Azure.md
Tudo sobre Java.md
```

---

# 5. Regras para atualização

Se o conceito já existir:

> atualizar a nota existente.

Ao atualizar:

* preservar o que estiver correto;
* adicionar informação;
* não sobrescrever silenciosamente conhecimento relevante;
* atualizar `updated`.

---

# 6. Regras para links

Usar `[[Nome da Nota]]` quando existir uma nota correspondente.

Criar links para:

* conceitos relacionados;
* tecnologias utilizadas em conjunto;
* padrões;
* arquiteturas;
* troubleshooting;
* projetos;
* dependências conceituais.

Links devem representar relações úteis.

Não fazer `every-word linking`.

---

# 7. Regras para tags

Tags são metadados/classificação.

Não substituem links.

Preferir:

```text
[[Application Insights]]
```

a:

```text
#application-insights
```

Manter vocabulário pequeno e estável:

```text
#java
#azure
#architecture
#observability
#troubleshooting
#moc
#meta
```

---

# 8. YAML / Frontmatter

Campos permitidos:

```yaml
type:
status:
confidence:
created:
updated:
tags:
```

## type

Valores:

```text
concept
technology
architecture
troubleshooting
study
reference
project
```

## status

Valores:

```text
inbox
learning
understood
mastered
unresolved
deprecated
```

## confidence

Representa a confiança do autor no entendimento do assunto.

Escala:

```text
0–100
```

Não representa confiabilidade da fonte.

Nunca alterar automaticamente sem justificativa explícita.

---

# 9. Fontes e confiabilidade

Priorizar:

1. documentação oficial / especificações oficiais;
2. documentação técnica dos fabricantes;
3. RFCs / JEPs / especificações;
4. artigos técnicos confiáveis;
5. livros;
6. comunidade.

Java:

* documentação oficial;
* JEPs;
* especificações.

Azure:

* documentação oficial da Microsoft.

Em conflitos:

* registrar o conflito;
* verificar versão;
* verificar contexto;
* priorizar fontes primárias;
* registrar a divergência quando relevante.

---

# 10. Versionamento

Quando uma informação depender de versão, registrar explicitamente.

Exemplo:

```text
Java 21
```

em vez de:

```text
Java
```

quando a funcionalidade ou comportamento for específico da versão.

Diferenciar:

* conceito;
* versão;
* implementação;
* comportamento específico da versão.

Aplicar o mesmo princípio ao Azure e seus serviços.

---

# 11. Conhecimento conceitual vs experiência prática

Conhecimento geral:

```text
01 - Concepts/
02 - Technologies/
03 - Architecture/
04 - Patterns/
05 - Observability/
06 - Guides/
```

Experiência:

```text
07 - Troubleshooting/
08 - Projects/
```

Fluxo:

```text
Projeto
  ↓
Problema real
  ↓
Diagnóstico
  ↓
Solução
  ↓
Insight reutilizável
  ↓
Nota de conhecimento
```

Quando uma experiência gerar conhecimento reutilizável, criar ou atualizar a nota conceitual correspondente e conectar as duas.

---

# 12. Troubleshooting

Uma nota de troubleshooting deve responder, quando aplicável:

* sintoma;
* contexto;
* hipóteses;
* diagnóstico;
* causa;
* solução;
* prevenção;
* comandos;
* queries.

Sempre que possível, conectar ao conhecimento correspondente.

Exemplo:

```text
[[Application Insights]]
[[Log Analytics]]
[[KQL]]
```

---

# 13. Fluxo Inbox → Conhecimento

O Inbox recebe informação bruta.

Ao processar:

```text
Interpretar
→ identificar conceitos
→ procurar notas existentes
→ detectar duplicações
→ decidir destino
→ atualizar/criar
→ criar links
→ atualizar MOCs
→ marcar item como processado
```

---

# 14. Conhecimento duplicado

Antes de criar:

* pesquisar sinônimos;
* pesquisar termos equivalentes;
* pesquisar conceitos relacionados;
* verificar possíveis duplicações.

Quando houver duplicação:

> unificar em uma única representação de conhecimento.

Ajustar links quando necessário.

---

# 15. Conhecimento conflitante

Quando uma informação contradizer uma nota existente:

Não substituir silenciosamente.

Investigar:

```text
Versão?
Contexto?
Fonte?
Implementação?
Mudança histórica?
```

Preservar histórico relevante.

---

# 16. Informações incompletas

Nunca inventar o que falta.

Utilizar:

```text
## Dúvidas
```

ou:

```text
## A validar
```

quando necessário.

---

# 17. Conhecimento obsoleto

Não apagar automaticamente.

Utilizar:

```yaml
status: deprecated
```

Registrar:

* versão;
* contexto;
* motivo;
* alternativa atual, quando conhecida.

---

# 18. Conexões entre domínios

Buscar ativamente relações entre áreas.

Exemplo:

```text
Java
  ↓
Spring Boot
  ↓
Arquitetura Hexagonal
  ↓
Dependency Injection
  ↓
Azure
  ↓
Application Insights
  ↓
Log Analytics
  ↓
KQL
```

Outro exemplo:

```text
Hexagonal Architecture
  ↓
Ports
  ↓
Adapters
  ↓
Repository
  ↓
Database
  ↓
Observability
```

As conexões devem representar relações conceituais ou práticas reais.

---

# 19. Como o Codex deve tomar decisões

Fluxo padrão:

```text
Entender informação
→ identificar conceitos
→ pesquisar base existente
→ pesquisar sinônimos
→ encontrar notas relacionadas
→ detectar duplicações
→ verificar conflitos
→ decidir destino
→ atualizar ou criar
→ criar links
→ atualizar MOCs
→ registrar fonte
→ validar consistência
```

Antes de qualquer alteração:

```text
Já existe nota?
Existe conceito semelhante?
É realmente informação nova?
Onde pertence?
Quais notas se relacionam?
Quais MOCs precisam ser atualizados?
Depende de versão?
Há fonte?
Há conflito?
A mudança é necessária?
```

---

# 20. Evitar overengineering

Priorizar:

```text
Conhecimento útil
>
Facilidade de consulta
>
Conexões
>
Consistência
>
Manutenção simples
```

Não criar:

* campos YAML desnecessários;
* tags excessivas;
* pastas profundas;
* abstrações desnecessárias;
* automações sem benefício comprovado.

---

# 21. Qualidade das notas

Uma nota boa deve ser:

* clara;
* objetiva;
* reutilizável;
* independente;
* conectada;
* versionada quando necessário;
* baseada em fonte quando a fonte for relevante.

Evitar:

* textos gigantes;
* redundância;
* cópia integral de documentação;
* conteúdo sem fonte quando a fonte for importante.

Preferir exemplos pequenos e concretos.

---

# 22. Camada de Avaliação Técnica

O Second Brain possui uma camada adicional destinada à avaliação técnica de candidatos durante processos seletivos.

Localização:

```text
11 - Interview Evaluation/
```

Essa camada não representa uma nova área de conhecimento técnico.

Ela representa um mecanismo de utilização do conhecimento existente.

Seu objetivo é responder:

> "Quanto do conhecimento técnico relevante o candidato demonstrou durante a entrevista?"

A camada de avaliação deve consultar:

```text
01 - Concepts/
02 - Technologies/
03 - Architecture/
04 - Patterns/
05 - Observability/
06 - Guides/
07 - Troubleshooting/
10 - Integration/
```

quando forem relevantes para a pergunta analisada.

---

# 23. Separação entre conhecimento e avaliação

A base técnica responde:

> "O que é tecnicamente correto?"

A camada de avaliação responde:

> "O que o candidato demonstrou conhecer?"

Essas duas responsabilidades devem permanecer separadas.

Uma avaliação de candidato não deve alterar automaticamente uma nota técnica.

Uma nota técnica não deve ser modificada para favorecer ou prejudicar um candidato.

---

# 24. Second Brain como referência, não gabarito

O conhecimento armazenado nesta base deve servir como referência para avaliação.

Não utilizar correspondência textual como critério principal.

O avaliador deve analisar:

* significado;
* correção técnica;
* contexto;
* completude;
* profundidade;
* raciocínio;
* aplicação;
* relações entre conceitos;
* trade-offs.

Uma resposta diferente da linguagem utilizada no Second Brain pode ser completamente válida.

---

# 25. Evidência de conhecimento

A avaliação deve distinguir:

```text
Conhecimento demonstrado
```

de:

```text
Conhecimento não demonstrado
```

e de:

```text
Conhecimento contradito por uma afirmação incorreta
```

Não transformar automaticamente ausência de evidência em ausência de conhecimento.

Exemplo:

```text
Não mencionou KQL.
```

não permite concluir:

```text
Não conhece KQL.
```

Conclusão apropriada:

```text
Não houve evidência suficiente sobre o domínio de KQL nesta resposta.
```

---

# 26. Pergunta como unidade de avaliação

A unidade básica futura de avaliação será:

```text
Pergunta
+
Resposta
+
Contexto
+
Conhecimento relevante
```

A resposta deve ser avaliada em relação ao que a pergunta realmente solicitou.

---

# 27. Correção vs completude

Uma resposta pode ser:

```text
correta
+
incompleta
```

ou:

```text
correta
+
completa
+
profunda
```

Essas dimensões devem permanecer separadas.

Não considerar uma resposta incorreta apenas porque ela não contém todos os detalhes existentes no Second Brain.

---

# 28. Profundidade

Profundidade representa o nível de entendimento demonstrado.

Indicadores possíveis:

```text
Definição
    ↓
Funcionamento
    ↓
Relação com outros conceitos
    ↓
Aplicação
    ↓
Consequências
    ↓
Trade-offs
```

A profundidade deve ser proporcional ao que a pergunta exige.

---

# 29. Experiência vs conhecimento

Uma experiência prática não comprova automaticamente conhecimento geral.

Da mesma forma, conhecimento conceitual não comprova automaticamente experiência profissional.

Manter separados:

```text
Conhecimento
Experiência
Aplicação demonstrada
```

---

# 30. Fato vs opinião

O avaliador deve diferenciar:

```text
Fato técnico
Opinião
Preferência
Experiência pessoal
```

Uma preferência técnica não deve ser tratada como erro simplesmente por não coincidir com a abordagem armazenada na base.

---

# 31. Incerteza

A avaliação deve reconhecer quando não existe evidência suficiente.

Futuramente será utilizado um mecanismo de confiança separado da nota técnica.

Exemplo:

```text
Nota: 8,0
Confiança: Baixa
```

A confiança representa a segurança da avaliação, não a confiança do autor na nota técnica.

Esse conceito deve permanecer separado do campo `confidence` das notas de conhecimento.

---

# 32. Limites da avaliação

A camada de avaliação pode analisar:

* conhecimento técnico demonstrado;
* correção;
* completude;
* profundidade;
* raciocínio;
* aplicação;
* troubleshooting demonstrado;
* trade-offs;
* relações entre conceitos.

Ela não deve concluir automaticamente:

* inteligência;
* personalidade;
* caráter;
* potencial;
* experiência não demonstrada;
* competência não evidenciada;
* senioridade definitiva;
* contratação ou rejeição.

A avaliação deve servir como:

> apoio à decisão humana.

Não como decisão autônoma de contratação.

---

# 33. Contexto da vaga

Posteriormente, a avaliação poderá considerar:

```text
Cargo
Senioridade
Stack
Competências esperadas
Pesos
Requisitos
```

O contexto da vaga não deve alterar o conhecimento técnico armazenado.

Ele altera a interpretação da relevância daquele conhecimento para determinada oportunidade.

---

# 34. Evolução da camada de avaliação

A camada será construída progressivamente:

```text
Etapa 11
Fundamentos da Avaliação
        ↓
Etapa 12
Taxonomia das Perguntas
        ↓
Etapa 13
Modelo de Evidências
        ↓
Etapa 14
Rubrica 0–10
        ↓
Etapa 15
Motor de Avaliação
        ↓
Etapa 16
Avaliação da Entrevista
        ↓
Etapa 17
Contexto da Vaga
```

Não implementar conceitos das etapas seguintes antecipadamente sem necessidade.

---

# 35. Princípio de evolução da base

A construção da camada de avaliação pode revelar lacunas na base técnica.

Quando isso acontecer:

```text
Avaliação
   ↓
Identifica necessidade de conhecimento
   ↓
Validação
   ↓
Atualização da base técnica
```

A atualização deve ser feita na nota técnica apropriada.

Não duplicar conhecimento dentro de `11 - Interview Evaluation/`.

---

# 36. Persistência dos relatórios de entrevistas

Toda entrevista que for efetivamente analisada e receber uma avaliação técnica completa deve ter seu relatório final salvo automaticamente na pasta:

```text
11 - Interview Evaluation/06 - Reports/
```

Essa persistência faz parte do fluxo normal de avaliação e não deve depender de uma solicitação adicional do usuário após a análise.

## Nome do arquivo

O nome padrão do arquivo deve seguir exatamente o formato:

```text
Relatório-{nomeCandidato}.md
```

Exemplo:

```text
Relatório-João Silva.md
```

Quando o nome do candidato não estiver disponível na entrevista, utilizar:

```text
Relatório-Candidato-{data}.md
```

Exemplo:

```text
Relatório-Candidato-2026-09-10.md
```

A data deve utilizar o formato:

```text
YYYY-MM-DD
```

## Conteúdo do relatório

O arquivo deve conter o relatório completo produzido pela avaliação da entrevista, preservando:

* perguntas avaliadas;
* análise das respostas;
* notas;
* evidências;
* erros técnicos identificados;
* pontos fortes;
* lacunas;
* análise por domínio;
* análise por complexidade;
* confiança;
* consolidação qualitativa;
* demais informações relevantes produzidas pelo modelo de avaliação.

Não salvar apenas um resumo quando o relatório completo estiver disponível.

## Momento da gravação

O relatório deve ser salvo após a conclusão da avaliação completa da entrevista.

Fluxo:

```text
Entrevista
    ↓
Perguntas + respostas
    ↓
Análise técnica
    ↓
Avaliação completa
    ↓
Relatório final
    ↓
11 - Interview Evaluation/06 - Reports/
    ↓
Relatório-{nomeCandidato}.md
```

## Preservação da avaliação

Salvar o relatório não deve alterar:

* notas;
* critérios;
* pesos;
* âncoras;
* regras de avaliação;
* conclusões;
* conhecimento técnico.

A gravação é apenas uma operação de persistência do resultado final da avaliação.

## Relatórios existentes

Antes de criar um novo relatório:

1. verificar se já existe um relatório para o mesmo candidato;
2. verificar se a entrevista corresponde a uma avaliação já registrada;
3. evitar duplicação desnecessária;
4. atualizar o relatório existente quando a operação representar uma continuação ou revisão da mesma entrevista;
5. criar um novo arquivo somente quando representar uma entrevista ou avaliação distinta.

Não criar uma pasta chamada `Entrevistas` para substituir ou duplicar `06 - Reports/`.

---

# 37. Regra final

O Second Brain deve continuar sendo, antes de tudo:

> uma rede de conhecimento técnico confiável, navegável, reutilizável e conectada.

A camada de avaliação existe para utilizar essa rede de forma estruturada durante processos seletivos.

Os relatórios produzidos pela camada de avaliação devem ser preservados em:

```text
11 - Interview Evaluation/06 - Reports/
```

para permitir histórico, consulta e comparação de avaliações futuras.

O objetivo não é fazer o candidato "bater com o Second Brain".

O objetivo é determinar, com base nas evidências disponíveis:

> **qual nível de conhecimento técnico o candidato demonstrou em relação ao que foi perguntado.**

