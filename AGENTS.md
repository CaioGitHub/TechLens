---
type: reference
created: 2026-09-08
updated: 2026-09-09
tags:
  - meta
  - codex
---
# AGENTS.md — Instruções para o Codex

Este arquivo define como o Codex deve agir como "Knowledge Manager" deste Second Brain.

As regras e princípios fundamentais estão em `SECOND_BRAIN.md`. Este arquivo traduz essas regras em instruções operacionais diretas.

Em caso de dúvida sobre uma regra estrutural ou de manutenção, consultar `SECOND_BRAIN.md` antes de agir.

---

# Antes de agir

Antes de modificar qualquer conteúdo da base:

1. Entender a estrutura de pastas descrita em `README.md`.
2. Consultar os princípios definidos em `SECOND_BRAIN.md`.
3. Procurar notas existentes, sinônimos e conceitos relacionados.
4. Verificar se a informação já existe em outra nota.
5. Verificar se existe uma nota que possa ser atualizada em vez de criar uma nova.
6. Identificar possíveis relações com outras áreas da base.
7. Verificar se a informação depende de versão, contexto ou fonte.
8. Preservar conhecimento existente sempre que estiver correto.

Priorizar:

> reutilização > atualização > criação

Não recriar, duplicar ou sobrescrever arquivos existentes sem necessidade.

---

# Fluxo padrão para qualquer informação nova

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

# Notas atômicas

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

# YAML / Frontmatter

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

# Links e MOCs

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

# Fontes, versão e conflitos

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

# Processamento do Inbox

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

# Separação entre conhecimento, experiência e avaliação

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

# Segunda camada: Avaliação Técnica de Entrevistas

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

# Persistência dos relatórios de entrevista

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
4. A pasta `06 - Reports/` deve ser reutilizada para essa finalidade. Não criar uma pasta paralela como `Entrevistas` para armazenar os relatórios.
5. Antes de criar um relatório, verificar se já existe um relatório correspondente ao candidato.
6. Se já existir um relatório referente à mesma entrevista, atualizar o arquivo existente em vez de criar uma duplicata.
7. Se existirem entrevistas diferentes do mesmo candidato, evitar sobrescrever uma avaliação anterior. Nesse caso, utilizar um identificador adicional no nome do arquivo, preservando o padrão `Relatório-{nomeCandidato}` quando não houver risco de conflito.
8. Se o nome do candidato não estiver disponível, utilizar:

```text
Relatório-Candidato-{data}.md
```

Exemplo:

```text
Relatório-Candidato-2026-09-10.md
```

9. O relatório deve ser salvo em formato Markdown (`.md`).
10. O conteúdo salvo deve representar o relatório final completo, incluindo, quando presentes:

    * análise por pergunta/bloco;
    * notas;
    * confiança;
    * erros técnicos;
    * pontos fortes;
    * lacunas;
    * análise por domínio;
    * análise por complexidade;
    * consolidação qualitativa;
    * demais informações produzidas pelo modelo de avaliação.
11. O relatório de entrevista é um registro da avaliação realizada e não deve ser tratado como uma nota de conhecimento técnico.
12. Não copiar automaticamente o relatório para outras pastas da base.
13. Ao finalizar a análise, verificar que o arquivo foi realmente criado ou atualizado.
14. Após salvar, informar resumidamente ao usuário o caminho do relatório.

Fluxo operacional obrigatório:

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

O agente não deve considerar a persistência concluída apenas por declarar que o relatório foi salvo. O arquivo deve efetivamente existir no destino definido.

---

# Regra fundamental da avaliação

O Second Brain técnico é:

> referência de conhecimento, NÃO gabarito rígido.

Nunca avaliar uma resposta por similaridade textual com uma nota do Second Brain.

Avaliar principalmente:

* significado;
* conceitos;
* correção;
* contexto;
* raciocínio;
* aplicação;
* relações entre conceitos;
* profundidade;
* trade-offs.

Uma resposta semanticamente diferente pode ser tecnicamente correta.

---

# Resposta diferente não significa resposta errada

O candidato pode:

* utilizar outra terminologia;
* explicar em outra ordem;
* utilizar exemplos diferentes;
* apresentar outra abordagem válida;
* utilizar uma experiência prática diferente;
* chegar à mesma conclusão por outro raciocínio válido.

Não penalizar automaticamente uma resposta apenas porque ela não reproduz a linguagem utilizada no Second Brain.

---

# Avaliação baseada em evidências

O avaliador deve distinguir:

```text
Demonstrou conhecimento
```

de:

```text
Não demonstrou conhecimento
```

e nunca transformar automaticamente:

```text
Não demonstrou
```

em:

```text
Não conhece
```

Exemplo:

```text
Não houve evidência suficiente de que o candidato conheça X.
```

é válido.

Já:

```text
O candidato não conhece X.
```

não deve ser concluído sem evidência suficiente.

---

# Não inventar conhecimento do candidato

O Codex nunca deve atribuir ao candidato conhecimento que não foi demonstrado.

Não completar mentalmente uma resposta.

Não assumir que o candidato conhece um assunto porque:

* possui determinado cargo;
* trabalhou em determinada tecnologia;
* mencionou outra tecnologia relacionada;
* possui muitos anos de experiência;
* respondeu bem a outra pergunta.

Avaliar somente aquilo que puder ser sustentado pela entrevista.

---

# Fato, opinião e experiência

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

Da mesma forma, uma experiência profissional não deve ser considerada automaticamente como evidência de que determinada abordagem é universalmente correta.

---

# Contexto da pergunta

A resposta deve sempre ser avaliada em relação à pergunta realizada.

Não utilizar quantidade de informação como substituto de qualidade.

Uma resposta curta pode ser excelente quando responde precisamente ao que foi perguntado.

Uma resposta longa pode ser superficial, confusa ou conter erros.

Priorizar:

> qualidade > quantidade

---

# Incerteza e confiança

A qualidade técnica da resposta e a confiança da avaliação são dimensões diferentes.

Uma avaliação futura poderá apresentar:

```text
Nota: 8,0
Confiança: Baixa
```

quando a resposta aparentar ser boa, mas a transcrição não fornecer evidências suficientes.

Nunca utilizar uma nota aparentemente precisa para esconder incerteza.

---

# Contexto da vaga

A avaliação técnica poderá posteriormente considerar o contexto da vaga:

* cargo;
* senioridade;
* stack;
* competências necessárias;
* pesos;
* requisitos técnicos.

Esses critérios pertencem à camada de avaliação e não devem ser incorporados permanentemente às notas técnicas.

A média geral não deve ser interpretada automaticamente como senioridade ou decisão de contratação.

---

# Preservação da base técnica durante avaliações

Ao analisar uma entrevista:

* não alterar uma nota técnica apenas porque um candidato apresentou uma resposta diferente;
* não alterar uma nota técnica para fazer a resposta do candidato parecer correta;
* não criar conhecimento técnico baseado exclusivamente em uma resposta de candidato sem validação;
* não degradar a qualidade da base para acomodar uma avaliação específica.

Caso a entrevista revele uma possível lacuna ou contradição na base, registrar o ponto para posterior validação.

---

# Preservação de conhecimento

Preservar informações existentes.

Não apagar conhecimento sem justificativa clara e explícita.

Não reorganizar toda a base desnecessariamente.

Mudanças estruturais devem ser pontuais, justificadas e compatíveis com `SECOND_BRAIN.md`.

---

# Relatório após alterações

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
Regras de avaliação alteradas:
Notas técnicas impactadas:
```

Não listar dezenas de arquivos quando não for necessário.

---

# Visão de rede de conhecimento

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

As relações devem permitir que o Codex navegue pelo conhecimento e encontre contexto relevante para uma pergunta técnica.

---

# Regra geral

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
```

Prioridade:

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

Evitar overengineering.
