---

type: reference
created: 2026-09-08
updated: 2026-10-07
tags:

* meta
* agents
* codex
* gemini
* second-brain

---

# AGENTS.md — Instruções para Agentes de IA

Este arquivo define como agentes de IA devem agir como "Knowledge Manager" e agentes de desenvolvimento deste Second Brain.

As regras e princípios fundamentais estão em:

```text
SECOND_BRAIN.md
```

Este arquivo traduz essas regras em instruções operacionais diretas.

O projeto também possui documentação específica de continuidade e governança:

```text
START_HERE.md
GEMINI_HANDOFF.md
GEMINI_GUARDRAILS.md
```

Em caso de dúvida sobre uma regra estrutural, metodológica ou de manutenção, consultar esses documentos antes de agir.

---

# 1. Regra obrigatória de continuidade

Este projeto possui histórico de desenvolvimento, validação, experimentação, correções e decisões arquiteturais.

O agente NÃO deve tratar o projeto como um projeto novo.

Antes de qualquer implementação, alteração, correção ou refatoração significativa, o agente DEVE consultar:

```text
AGENTS.md
SECOND_BRAIN.md
GEMINI_GUARDRAILS.md
GEMINI_HANDOFF.md
```

Se existir documentação específica para o stage em execução, ela também deve ser consultada.

Quando o projeto estiver sendo continuado por outro agente, o agente deve utilizar `GEMINI_HANDOFF.md` como fonte do estado histórico e roadmap, e não reconstruir esse histórico por inferência.

---

# 2. START HERE

Se o arquivo:

```text
START_HERE.md
```

existir, ele deve ser consultado primeiro para obter uma visão rápida do estado atual.

O fluxo recomendado é:

```text
START_HERE.md
    ↓
AGENTS.md
    ↓
SECOND_BRAIN.md
    ↓
GEMINI_GUARDRAILS.md
    ↓
GEMINI_HANDOFF.md
    ↓
Stage atual
```

---

# 3. Descoberta obrigatória do estado atual

Antes de modificar qualquer conteúdo ou código relacionado ao sistema de avaliação de entrevistas, identificar:

1. Qual é o stage atual.
2. Qual foi o último stage concluído.
3. Qual foi o gate do último stage.
4. Se existe algum stage `BLOCKED`.
5. Quais warnings estão abertos.
6. Quais testes existem para o stage.
7. Quais artefatos são canônicos.
8. Quais artefatos são históricos.
9. Se existe trabalho parcialmente implementado.
10. Quais restrições metodológicas estão vigentes.

Não assumir que o próximo stage é simplesmente o próximo número.

Consultar `GEMINI_HANDOFF.md`.

---

# 4. Não replanejar o projeto sem necessidade

O agente não deve:

* redesenhar a arquitetura existente;
* substituir componentes existentes;
* remover stages;
* pular gates;
* apagar histórico;
* alterar metodologia;
* criar uma nova rubrica;
* criar um novo Evidence Model;
* criar um novo Evaluation Engine;
* substituir o pipeline existente;

apenas porque uma solução diferente parece mais simples ou elegante.

Antes de qualquer mudança estrutural, deve existir um problema concreto, reproduzível e documentado que justifique a alteração.

Priorizar:

> correção mínima e generalizável > refatoração ampla

---

# 5. Antes de agir

Antes de modificar qualquer conteúdo da base:

1. Entender a estrutura de pastas descrita em `README.md`.
2. Consultar os princípios definidos em `SECOND_BRAIN.md`.
3. Consultar `GEMINI_GUARDRAILS.md`.
4. Consultar `GEMINI_HANDOFF.md` quando a tarefa envolver a camada de avaliação.
5. Procurar notas existentes, sinônimos e conceitos relacionados.
6. Verificar se a informação já existe em outra nota.
7. Verificar se existe uma nota que possa ser atualizada em vez de criar uma nova.
8. Identificar possíveis relações com outras áreas da base.
9. Verificar se a informação depende de versão, contexto ou fonte.
10. Preservar conhecimento existente sempre que estiver correto.

Priorizar:

> reutilização > atualização > criação

Não recriar, duplicar ou sobrescrever arquivos existentes sem necessidade.

---

# 6. Fluxo padrão para qualquer informação nova

Sempre seguir esta sequência antes de gravar qualquer conteúdo:

1. Entender a informação recebida.

2. Identificar o(s) conceito(s) principal(is).

3. Pesquisar a base existente por título, sinônimos e conceitos relacionados.

4. Verificar se a informação pertence a uma nota existente.

5. Verificar duplicações.

6. Verificar possíveis conflitos.

7. Decidir o destino:

   * atualizar nota existente;
   * criar nova nota;
   * criar nota especializada;
   * colocar no Inbox;
   * apenas criar relações com conhecimento existente.

8. Aplicar o template correspondente em `99 - Templates/`, quando aplicável.

9. Criar links `[[...]]` relevantes.

10. Atualizar o(s) MOC(s) correspondente(s), quando necessário.

11. Registrar a fonte, quando houver ou quando for relevante.

12. Registrar a versão quando o conhecimento depender dela.

13. Validar YAML, status, confidence, versão e possíveis contradições.

14. Preservar conhecimento existente que continue válido.

---

# 7. Notas atômicas

Uma nota deve representar um único conceito ou unidade de conhecimento reutilizável.

Uma nota deve ser:

* compreensível de forma independente;
* reutilizável;
* suficientemente específica;
* conectável a outras notas.

Não criar uma nota nova para cada pequeno detalhe.

Preferir:

```text
Virtual Threads
Structured Concurrency
Dependency Inversion
Application Insights Sampling
KQL summarize
```

em vez de criar notas excessivamente fragmentadas ou uma única nota gigantesca.

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

Valores permitidos para `type`:

```text
concept
technology
architecture
troubleshooting
study
reference
project
```

Valores permitidos para `status`:

```text
inbox
learning
understood
mastered
unresolved
deprecated
```

Regras:

* `confidence` representa a confiança do autor no entendimento do assunto.
* `confidence` utiliza escala de 0–100.
* `confidence` não representa a confiabilidade da fonte.
* Nunca alterar `confidence` automaticamente sem justificativa explícita.
* Sempre atualizar `updated` ao editar uma nota.
* Não adicionar novos campos YAML sem necessidade clara e justificável.

---

# 9. Links e MOCs

A base é uma rede de conhecimento.

Criar links `[[...]]` quando representarem relações úteis, como:

* conceitos relacionados;
* dependências conceituais;
* tecnologias utilizadas em conjunto;
* padrões arquiteturais;
* troubleshooting relacionado;
* projetos que aplicam o conceito;
* conceitos de outros domínios.

Não utilizar links em excesso apenas para aumentar a quantidade de conexões.

Quando uma nova nota relevante for criada ou uma relação importante for adicionada, verificar se o MOC correspondente precisa ser atualizado.

Se houver nomes de notas ambíguos entre pastas, utilizar caminho completo ou alias para desambiguar.

Exemplo:

```text
[[02 - Technologies/Java/Java]]
```

---

# 10. Fontes, versão e conflitos

Registrar a fonte quando relevante.

Priorizar:

1. documentação oficial / especificações oficiais;
2. documentação técnica dos fabricantes;
3. RFCs / JEPs / especificações;
4. artigos técnicos confiáveis;
5. livros;
6. conteúdo de comunidade.

Java:

* priorizar documentação oficial;
* JEPs;
* especificações.

Azure:

* priorizar documentação oficial da Microsoft.

Quando uma informação depender de versão, registrar explicitamente a versão.

Exemplo:

```text
Disponível a partir do Java 21.
```

em vez de:

```text
Java possui Virtual Threads.
```

Se uma informação nova contradizer uma nota existente:

* não substituir silenciosamente;
* identificar a possível causa;
* verificar versão;
* verificar contexto;
* verificar fonte;
* preservar histórico relevante;
* registrar a divergência quando necessário.

Se uma informação estiver incompleta:

* não inventar;
* utilizar `## Dúvidas` ou `## A validar`.

Conhecimento obsoleto não deve ser apagado automaticamente.

Utilizar:

```yaml
status: deprecated
```

e registrar a versão/contexto correspondente.

---

# 11. Processamento do Inbox

Quando o usuário disser:

> "Processe meu Inbox"

seguir:

1. Listar os itens encontrados.
2. Agrupar informações relacionadas.
3. Identificar duplicações.
4. Identificar conceitos envolvidos.
5. Verificar notas existentes.
6. Propor a classificação.
7. Atualizar ou criar as notas necessárias.
8. Criar links relevantes.
9. Atualizar os MOCs impactados.
10. Marcar os itens processados no Inbox.

Nunca descartar silenciosamente conteúdo do Inbox.

---

# 12. Separação entre conhecimento, experiência e avaliação

Manter três categorias conceitualmente distintas.

## Conhecimento técnico

Informação geral e reutilizável:

```text
01 - Concepts/
02 - Technologies/
03 - Architecture/
04 - Patterns/
05 - Observability/
06 - Guides/
```

## Experiência prática

Experiências de projetos, incidentes e problemas reais:

```text
07 - Troubleshooting/
08 - Projects/
```

## Avaliação de candidatos

Informações, regras, critérios e resultados relacionados à avaliação técnica:

```text
11 - Interview Evaluation/
```

Não misturar avaliações de candidatos com notas de conhecimento técnico.

Uma nota de Java, por exemplo, não deve conter avaliações de candidatos.

---

# 13. Segunda camada: Avaliação Técnica de Entrevistas

O Second Brain possui uma camada específica para auxiliar na avaliação de respostas técnicas de candidatos.

Essa camada está localizada em:

```text
11 - Interview Evaluation/
```

Ela utiliza a base técnica existente como referência.

Fluxo conceitual:

```text
Pergunta
    ↓
Identificação do tema
    ↓
Identificação do tipo de pergunta
    ↓
Consulta ao conhecimento relevante
    ↓
Análise da resposta
    ↓
Evidências
    ↓
Avaliação
```

A camada de avaliação NÃO deve alterar automaticamente a base técnica apenas porque uma resposta de candidato foi analisada.

---

# 14. Pipeline canônico da avaliação

O pipeline estabelecido para avaliação de entrevistas é:

```text
Raw Transcript
      ↓
20.1 Participant Identification
      ↓
20.2 Speaker Attribution
      ↓
20.3 Question Extraction
      ↓
20.4 Response Extraction
      ↓
20.5 Reconstruction & Normalization
      ↓
20.6 Question/Response Linking
      ↓
20.7 Validation
      ↓
21 Evidence Model
      ↓
22 Scoring Rubric
      ↓
23 Evaluation Engine
      ↓
23.1 Global Evaluation Semantic Audit
      ↓
23.2 Interview Evaluation Materialization
      ↓
24 Pipeline / Orchestration
      ↓
25 End-to-End Validation
      ↓
26 Reference Runtime / Test Harness
      ↓
27 Synthetic Interview Full Run
      ↓
28 Semantic / Blind Calibration
      ↓
29 Adversarial Validation
      ↓
30 Real Interview Pilot
      ↓
30.1 Pilot Failure Analysis
      ↓
30.2 Human Review & Structured Interview Approval
      ↓
30.2.1 Final Semantic Audit
      ↓
31 Human vs System Validation
      ↓
31.1 Failure Analysis / Root Cause Analysis
      ↓
31.2 Controlled Correction
      ↓
31.3 Post-Correction Blind Validation
      ↓
31.4 Semantic Relevance & Representation Invariance Remediation
      ↓
31.5 Human vs System Revalidation
      ↓
32 Production Readiness
      ↓
33 Production Runtime
```

Esta sequência é deliberada.

Não remover, pular ou reordenar stages sem justificativa explícita e validação do impacto.

---

# 15. Estado atual do sistema de avaliação

O estado atual e o histórico detalhado estão em:

```text
GEMINI_HANDOFF.md
```

No momento, o fluxo encontra-se na região:

```text
31
 ↓
HUMAN_VS_SYSTEM_BLOCKED

31.1
 ↓
ROOT CAUSE IDENTIFIED

31.2
 ↓
CONTROLLED CORRECTION COMPLETE_WITH_WARNINGS

31.3
 ↓
POST_CORRECTION_BLIND_VALIDATION_BLOCKED

31.4
 ↓
CURRENT STAGE
```

O Stage 31.4 trata:

```text
Semantic Relevance
+
Representation Invariance
```

Não avançar para Production Readiness enquanto os bloqueios metodológicos dessa sequência não forem resolvidos e revalidados.

---

# 16. Regra para stages

Cada stage deve ser tratado como uma unidade de trabalho com:

```text
Objetivo
↓
Pré-condições
↓
Implementação
↓
Testes
↓
Validação
↓
Gate
↓
Registro
```

Antes de iniciar um stage:

1. consultar o handoff;
2. consultar a documentação específica do stage;
3. verificar o gate anterior;
4. verificar se existem bloqueios;
5. verificar os testes existentes.

Ao finalizar:

1. executar os testes específicos;
2. executar regressão;
3. verificar o Harness;
4. verificar determinismo quando aplicável;
5. verificar isolamento quando aplicável;
6. verificar rastreabilidade;
7. verificar artefatos protegidos;
8. registrar warnings;
9. registrar limitações;
10. registrar o gate final.

---

# 17. Regra para BLOCKED

Se o stage atual estiver:

```text
BLOCKED
```

não avançar simplesmente para o próximo stage.

Executar:

```text
Reproduzir
    ↓
Investigar
    ↓
Identificar causa
    ↓
Corrigir
    ↓
Testar
    ↓
Regredir
    ↓
Revalidar
```

Não alterar o gate apenas para permitir continuidade.

Um bloqueio é um resultado válido da validação.

---

# 18. Regra de mudança controlada

Antes de modificar qualquer componente da avaliação:

1. Reproduzir o problema.
2. Identificar a primeira etapa incorreta.
3. Identificar a causa raiz.
4. Determinar se o problema é local ou estrutural.
5. Criar teste de reprodução/regressão.
6. Aplicar a menor correção generalizável.
7. Executar os testes específicos.
8. Executar regressão completa.
9. Executar o Reference Harness.
10. Verificar artefatos históricos.
11. Registrar impacto.
12. Revalidar o stage afetado.

Nunca corrigir apenas o resultado final sem investigar onde o significado foi alterado.

---

# 19. Regra contra overfitting

Um caso de teste conhecido nunca deve ser transformado em uma regra específica.

Exemplo proibido:

```text
REST → Kafka = off-topic
Docker → Kubernetes = related
SQL → Redis = off-topic
```

Esses casos devem representar propriedades gerais.

O objetivo é avaliar:

```text
Intenção da pergunta
        ↓
Conteúdo da resposta
        ↓
Relação semântica
        ↓
Relevância
```

e não uma lista de pares tecnológicos.

---

# 20. Relevância semântica

Uma resposta pode ser tecnicamente correta e ainda assim não responder adequadamente à pergunta.

O sistema deve distinguir, quando aplicável:

```text
DIRECT
PARTIAL
RELATED_BUT_NOT_ANSWERING
OFF_TOPIC
INSUFFICIENT
```

Exemplo:

```text
Pergunta:
Como REST funciona?

Resposta:
Kafka permite processamento assíncrono...
```

A informação pode ser tecnicamente correta.

Isso não significa que ela responda à pergunta.

Regra:

> conteúdo tecnicamente válido ≠ resposta semanticamente adequada à pergunta

---

# 21. Representation Invariance

O sistema deve manter interpretação técnica equivalente quando o significado é equivalente.

Testar invariância para:

* resposta curta vs longa;
* formal vs informal;
* linguagem simples vs jargão;
* boa gramática vs gramática imperfeita;
* respostas com diferentes estilos de explicação;
* autocorreções que preservam o significado;
* diferentes níveis de fluência.

Também deve ser invariável a fatores externos como:

* senioridade declarada;
* currículo;
* cargo;
* empresa;
* contexto da vaga;
* eloquência.

---

# 22. Não utilizar avaliação humana como target

Avaliações humanas podem ser utilizadas para:

* identificar divergências;
* investigar problemas;
* validar comportamento;
* identificar possíveis erros do sistema;
* identificar possíveis erros humanos.

Não devem ser utilizadas como:

```text
score esperado
```

durante execução cega.

O objetivo é corrigir a metodologia e o comportamento semântico do sistema, e não fazer o sistema "imitar" uma nota humana específica.

---

# 23. Blind Validation

Quando uma etapa for declarada `blind`, o executor não pode receber:

* score esperado;
* avaliação humana;
* resposta esperada;
* evidência esperada;
* resultado histórico;
* referência desejada;
* resultado desejado.

O comparator pode conhecer o resultado esperado.

O executor não.

---

# 24. Separação de responsabilidades

Preservar a separação:

```text
20.x
→ processamento da transcrição

21
→ extração/modelagem de evidências

22
→ rubrica

23
→ avaliação

23.1
→ auditoria da avaliação global

23.2
→ materialização

24
→ orquestração

25+
→ validação e experimentação
```

Não colocar scoring dentro do processamento da transcrição.

Não colocar parsing de transcript dentro do Evaluation Engine.

Não colocar decisão de contratação dentro do Evaluation Engine.

---

# 25. Evidência > impressão

O sistema avalia aquilo que foi demonstrado.

Não utilizar como evidência técnica principal:

* currículo;
* cargo;
* senioridade declarada;
* anos de experiência isoladamente;
* empresa;
* eloquência;
* confiança;
* tamanho da resposta;
* quantidade de jargões.

---

# 26. "Não demonstrou" ≠ "Não conhece"

Se a entrevista não produziu evidência suficiente:

```text
Não demonstrado
```

não deve ser transformado automaticamente em:

```text
Não conhece
```

Exemplo válido:

```text
Não houve evidência suficiente de que o candidato conheça X.
```

Evitar:

```text
O candidato não conhece X.
```

sem evidência suficiente.

---

# 27. Experiência declarada ≠ experiência demonstrada

Exemplo:

```text
"Trabalhei 3 anos com Kubernetes."
```

é uma declaração de experiência.

Isso não equivale automaticamente a:

```text
Explica uma situação concreta,
justifica decisões,
descreve troubleshooting
e explica trade-offs.
```

Separar:

```text
experience_declaration
```

de:

```text
demonstrated_experience
```

Hipóteses também não devem ser convertidas automaticamente em experiência.

---

# 28. Conhecimento ≠ aplicação

Separar, quando aplicável:

* conhecimento conceitual;
* conhecimento factual;
* implementação;
* aplicação prática;
* troubleshooting;
* raciocínio;
* tomada de decisão;
* trade-offs;
* arquitetura;
* integração entre conhecimentos.

---

# 29. Resposta diferente não significa resposta errada

O candidato pode:

* utilizar outra terminologia;
* explicar em outra ordem;
* utilizar exemplos diferentes;
* apresentar outra abordagem válida;
* utilizar experiência prática diferente;
* chegar à mesma conclusão por outro raciocínio válido.

Não penalizar automaticamente uma resposta porque ela não reproduz a linguagem utilizada no Second Brain.

---

# 30. Contexto da pergunta

A resposta deve sempre ser avaliada em relação à pergunta realizada.

Não utilizar quantidade de informação como substituto de qualidade.

Uma resposta curta pode ser excelente quando responde precisamente ao que foi perguntado.

Uma resposta longa pode ser superficial, confusa ou conter erros.

Priorizar:

> qualidade > quantidade

---

# 31. Não inventar conhecimento do candidato

O agente nunca deve atribuir ao candidato conhecimento que não foi demonstrado.

Não completar mentalmente uma resposta.

Não assumir que o candidato conhece um assunto porque:

* possui determinado cargo;
* trabalhou em determinada tecnologia;
* mencionou outra tecnologia relacionada;
* possui muitos anos de experiência;
* respondeu bem a outra pergunta.

Avaliar somente aquilo que puder ser sustentado pela entrevista.

---

# 32. Fato, opinião e experiência

Diferenciar:

```text
Fato técnico
```

de:

```text
Opinião
```

e:

```text
Experiência pessoal
```

Uma preferência pessoal não deve ser classificada como erro técnico simplesmente por não corresponder à abordagem mais comum do Second Brain.

Uma experiência profissional também não deve ser considerada automaticamente como evidência de que determinada abordagem é universalmente correta.

---

# 33. Incerteza e confiança

A qualidade técnica da resposta e a confiança da avaliação são dimensões diferentes.

Uma avaliação poderá apresentar:

```text
Nota: 8,0
Confiança: Baixa
```

quando a resposta aparentar ser boa, mas a transcrição não fornecer evidências suficientes.

Nunca utilizar uma nota aparentemente precisa para esconder incerteza.

---

# 34. Complexidade não determina score

Não assumir automaticamente:

```text
pergunta avançada = score menor
pergunta básica = score maior
```

A complexidade da pergunta e a qualidade da resposta são dimensões diferentes.

Também não utilizar:

```text
7 = Júnior
8 = Pleno
9 = Senior
```

Não inferir senioridade automaticamente a partir de score.

---

# 35. Decisão de contratação

Esta camada não deve automaticamente:

* aprovar candidato;
* reprovar candidato;
* recomendar contratação;
* recomendar rejeição;
* ranquear candidatos;
* escolher o melhor candidato.

A avaliação técnica é distinta da decisão organizacional.

---

# 36. Contexto da vaga

A avaliação técnica pode posteriormente ser combinada com contexto da vaga:

* cargo;
* senioridade;
* stack;
* competências;
* requisitos;
* pesos.

Porém:

```text
Avaliação técnica
≠
Aderência à vaga
≠
Decisão de contratação
```

O contexto da vaga não deve contaminar retroativamente a avaliação técnica individual.

---

# 37. Preservação da base técnica durante avaliações

Ao analisar uma entrevista:

* não alterar uma nota técnica porque um candidato apresentou resposta diferente;
* não alterar uma nota técnica para fazer a resposta do candidato parecer correta;
* não criar conhecimento técnico baseado exclusivamente em resposta de candidato sem validação;
* não degradar a qualidade da base para acomodar uma avaliação específica.

Caso a entrevista revele uma possível lacuna ou contradição na base, registrar o ponto para posterior validação.

---

# 38. Persistência dos relatórios de entrevista

Toda entrevista técnica concluída e analisada deve gerar automaticamente um relatório persistido na pasta:

```text
11 - Interview Evaluation/06 - Reports/
```

O nome padrão do arquivo deve ser:

```text
Relatório-{nomeCandidato}.md
```

Exemplo:

```text
Relatório-Caio.md
```

Regras:

1. O relatório deve conter a avaliação final completa produzida pelo agente.
2. O relatório deve ser salvo somente após a conclusão da análise da entrevista.
3. O salvamento do relatório não deve alterar notas, critérios, pesos, regras ou conclusões da avaliação.
4. A pasta `06 - Reports/` deve ser reutilizada para essa finalidade.
5. Antes de criar um relatório, verificar se já existe um relatório correspondente ao candidato.
6. Se já existir um relatório referente à mesma entrevista, atualizar o arquivo existente em vez de criar uma duplicata.
7. Se existirem entrevistas diferentes do mesmo candidato, evitar sobrescrever avaliação anterior. Utilizar identificador adicional quando necessário.
8. Se o nome do candidato não estiver disponível:

```text
Relatório-Candidato-{data}.md
```

9. O relatório deve ser salvo em Markdown.
10. O conteúdo deve representar o relatório final completo.
11. O relatório de entrevista é um registro da avaliação realizada e não deve ser tratado como nota de conhecimento técnico.
12. Não copiar automaticamente o relatório para outras pastas.
13. Ao finalizar a análise, verificar que o arquivo realmente foi criado ou atualizado.
14. Após salvar, informar resumidamente ao usuário o caminho do relatório.

Fluxo obrigatório:

```text
Concluir entrevista
    ↓
Consolidar avaliação final
    ↓
Identificar nome do candidato
    ↓
Verificar relatório existente
    ↓
Criar ou atualizar relatório
    ↓
Validar arquivo
    ↓
Informar caminho salvo
```

O agente não deve considerar a persistência concluída apenas por declarar que o relatório foi salvo.

---

# 39. Preservação histórica dos stages

Relatórios históricos de stages não devem ser apagados ou sobrescritos para refletir o estado corrigido.

Exemplo:

```text
Stage 31
HUMAN_VS_SYSTEM_BLOCKED
```

continua sendo um resultado histórico válido mesmo depois de uma correção posterior.

A correção deve gerar nova evidência por meio de:

```text
novo stage
novo teste
nova validação
novo relatório
```

e não apagar a falha anterior.

---

# 40. Testes são parte do contrato

Toda correção semântica significativa deve possuir:

```text
teste de reprodução
+
teste de regressão
```

Quando aplicável, também:

```text
teste de mutação
+
teste de invariância
+
teste de determinismo
+
teste de isolamento
```

Não alterar um teste apenas porque a implementação não passou.

Antes de modificar um oracle:

1. verificar se o oracle está objetivamente incorreto;
2. documentar o motivo;
3. verificar impacto;
4. preservar a intenção original do teste.

---

# 41. Resultado dos testes

Distinguir:

```text
PASS
PASS_WITH_WARNINGS
BLOCKED
FAIL
```

Não esconder warnings.

Não transformar `BLOCKED` em `PASS` sem corrigir a causa.

Não interpretar `BLOCKED` como rejeição do candidato.

---

# 42. Não otimizar para score

Não alterar lógica com objetivo explícito de:

* aumentar score;
* diminuir score;
* aproximar artificialmente score humano;
* reduzir MAE artificialmente;
* passar um caso específico.

Uma mudança pode melhorar concordância com avaliações humanas, mas isso deve ser consequência da correção semântica.

---

# 43. Regra de primeira falha

Ao investigar uma divergência, seguir:

```text
Transcript
↓
Question
↓
Response
↓
Reconstruction
↓
Linking
↓
Evidence
↓
Evaluation
↓
Global Evaluation
```

Identificar o primeiro ponto em que o significado foi alterado incorretamente.

Preferir corrigir a origem em vez de mascarar o problema no estágio final.

---

# 44. Proteção contra overengineering

Não criar abstrações, frameworks ou camadas apenas para aumentar a sofisticação técnica.

Cada nova abstração deve resolver um problema demonstrado.

Preferir:

> menor mudança que resolve a causa geral

em vez de:

> grande refatoração que resolve o caso atual.

---

# 45. Regra de continuidade entre agentes

Quando um agente assumir o projeto de outro:

1. não apagar o trabalho anterior;
2. não assumir que decisões anteriores estavam erradas;
3. ler os documentos de handoff;
4. identificar o último gate;
5. identificar bloqueios;
6. reproduzir o estado atual quando necessário;
7. continuar do ponto documentado.

O agente deve deixar o projeto em estado compreensível para o próximo agente.

---

# 46. Checkpoint obrigatório antes de concluir um stage

Antes de declarar um stage concluído:

```text
[ ] Li AGENTS.md
[ ] Li SECOND_BRAIN.md
[ ] Li GEMINI_HANDOFF.md
[ ] Li GEMINI_GUARDRAILS.md
[ ] Identifiquei o stage correto
[ ] Identifiquei o gate anterior
[ ] Verifiquei bloqueios
[ ] Reproduzi o problema quando aplicável
[ ] Identifiquei a causa raiz
[ ] Evitei overfitting
[ ] Criei teste de reprodução/regressão
[ ] Rodei os testes específicos
[ ] Rodei a regressão
[ ] Rodei o Harness quando aplicável
[ ] Verifiquei determinismo quando aplicável
[ ] Verifiquei isolamento quando aplicável
[ ] Preservei rastreabilidade
[ ] Preservei artefatos históricos
[ ] Não usei score humano como target
[ ] Não introduzi senioridade automática
[ ] Não introduzi decisão de contratação
[ ] Não alterei testes apenas para fazê-los passar
[ ] Registrei warnings e limitações
[ ] Registrei o gate final
```

---

# 47. Relatório após alterações

Ao final de qualquer alteração significativa, relatar resumidamente:

```text
Criado:
Atualizado:
Links adicionados:
MOCs atualizados:
Dúvidas / pontos a validar:
```

Ao trabalhar na camada de avaliação, também informar quando aplicável:

```text
Stage:
Gate:
Testes:
Regressão:
Warnings:
Limitações:
Regras de avaliação alteradas:
Notas técnicas impactadas:
Artefatos históricos preservados:
```

Não listar dezenas de arquivos quando não for necessário.

---

# 48. Visão de rede de conhecimento

Esta base é uma rede de conhecimento, não apenas uma hierarquia de pastas.

Priorizar relações significativas entre conceitos.

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
Azure Adapter
  ↓
Application Insights
  ↓
Azure Monitor
  ↓
Log Analytics
  ↓
KQL
```

As relações devem permitir que o agente navegue pelo conhecimento e encontre contexto relevante para uma pergunta técnica.

---

# 49. Regra geral

Antes de criar ou modificar qualquer coisa, perguntar internamente:

```text
Já existe uma nota para isso?
Existe conceito semelhante?
É realmente informação nova?
Onde pertence?
Quais notas se relacionam?
Quais MOCs precisam ser atualizados?
Depende de versão?
Existe fonte?
Existe conflito?
A alteração é realmente necessária?
Qual é o stage atual?
Qual é o gate atual?
Existe algum BLOCKED?
Estou corrigindo a causa ou apenas o sintoma?
Estou criando uma regra específica para um teste?
Estou preservando o histórico?
```

Prioridade:

```text
Conhecimento útil
>
Evidência
>
Rastreabilidade
>
Reprodutibilidade
>
Generalização
>
Facilidade de consulta
>
Conexões
>
Consistência
>
Manutenção simples
>
Conveniência
```

---

# 50. Regra suprema

O objetivo deste projeto não é construir um sistema que simplesmente:

```text
passe nos testes
```

ou:

```text
pareça inteligente
```

O objetivo é construir um sistema cuja avaliação possa ser:

```text
investigada
reproduzida
contestada
explicada
corrigida
```

Quando houver conflito entre:

```text
fazer o pipeline passar
```

e:

```text
preservar a validade metodológica
```

a validade metodológica vence.

Quando houver dúvida:

```text
não inventar
não assumir
não simplificar
não apagar
não mascarar
```

Registrar:

```text
WARNING
NEEDS_REVIEW
ou
BLOCKED
```

conforme o caso.

Princípio final:

> **O projeto deve preferir uma conclusão limitada, porém defensável, a uma conclusão forte baseada em evidência insuficiente.**
