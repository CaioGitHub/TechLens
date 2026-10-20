# Stage 31.7.31 — Contrato de Equivalência Conceitual e Funcional

## 1. Princípio da Equivalência Semântica Aberta

A avaliação de equivalência conceitual visa reconhecer a validade técnica de respostas expressas em terminologia heterogênea, sem recorrer a listas fechadas de sinônimos ou dicionários estáticos de tecnologias. A equivalência avalia a **preservação das propriedades invariantes e das relações causais requeridas pela pergunta**:

$$\text{Equivalência}(\text{Termo}_A, \text{Conceito}_B) \iff \text{Propriedades}(\text{Termo}_A) \supseteq \text{Propriedades\_Mandatórias}(\text{Conceito}_B)$$

---

## 2. A Hierarquia das Oito Relações de Equivalência

| Nível de Relação | Definição Formal | Impacto na Classificação | Exemplo Prático |
|:---:|---|:---:|---|
| **1. Sinonímia Contextual** | Termos intercambiáveis no contexto específico de engenharia de software sem alteração de escopo. | Equivalência Plena (`DIRECT`) | "Algoritmo de dispersão" $\equiv$ "Função de hash". |
| **2. Paráfrase** | Reconstrução sintática completa da proposição que preserva o mesmo valor de verdade e nexo causal. | Equivalência Plena (`DIRECT`) | "A partição é calculada pela chave" $\equiv$ "A chave direciona para a partição". |
| **3. Hiperônimo / Descrição de Categoria** | Referência à classe mais ampla sem descer ao mecanismo operacional específico. | Relação Parcial (`PARTIAL` ou `RELATED`) | "Utilizamos um banco relacional" em vez de especificar PostgreSQL. |
| **4. Explicação Funcional** | Descrição do comportamento, das garantias e da estrutura física sem citar o nome formal do padrão. | Equivalência Plena (`DIRECT`) | Explicar "árvore balanceada de busca" sem pronunciar a palavra "B-tree". |
| **5. Analogia Pedagógica** | Mapeamento estrutural entre um domínio conhecido e o domínio computacional. | Condicional (`DIRECT` se grounded, `INSUFFICIENT` se ungrounded) | Comparar Circuit Breaker a disjuntor elétrico residencial. |
| **6. Coincidência Lexical** | Mesma palavra em acepção semântica estranha ao software (homonímia/polissemia). | Disjunção (`OFF_TOPIC`) | "Dependência econômica de importações". |
| **7. Relação Associativa Periférica** | Termos que costumam coocorrer no mesmo ecossistema, mas que não se substituem funcionalmente. | Conexão Contextual (`RELATED` ou `SUPPORTING`) | Citar Docker ao responder sobre Kubernetes, sem explicar pods. |
| **8. Contradição Conceitual** | Uso de um termo seguido da atribuição de propriedades mutuamente excludentes. | Invalidação (`OFF_TOPIC` ou `INSUFFICIENT`) | "Fila assíncrona síncrona bloqueante que não prende a thread". |

---

## 3. Resolução dos Seis Cenários Obrigatórios

### Cenário 1: Descrição da Estrutura sem Citar o Nome Técnico
- **Pergunta:** *"Como um índice B-tree acelera a busca?"*
- **Resposta:** *"Ele organiza os dados em nós ordenados hierárquicos mantendo a árvore balanceada, de modo que cada nó orienta o ponteiro para o próximo nível em complexidade logarítmica."*
- **Análise Semântica:** O candidato elucida os invariantes formais da B-tree (nós hierárquicos, balanceamento, navegação logarítmica), satisfazendo a intenção explicativa.
- **Classificação:** $\textbf{DIRECT}$

### Cenário 2: Paráfrase Correta sem Jargão Esperado
- **Pergunta:** *"Como o Garbage Collector identifica objetos órfãos na memória heap?"*
- **Resposta:** *"O coletor parte das variáveis que estão ativas na pilha de execução e vai seguindo os apontamentos; tudo que não tiver nenhum caminho que chegue até ele é considerado lixo e tem o espaço liberado."*
- **Análise Semântica:** Paráfrase precisa do algoritmo de rastreamento por raízes (GC Roots e reachability analysis), expressa sem os termos em inglês.
- **Classificação:** $\textbf{DIRECT}$

### Cenário 3: Menção de Categoria Ampla sem o Mecanismo Específico
- **Pergunta:** *"Como o Redis persiste dados em disco sem degradar a latência de leitura?"*
- **Resposta:** *"O Redis utiliza técnicas padrão de persistência em armazenamento secundário comuns a bancos modernos."*
- **Análise Semântica:** Uso de hiperônimo abstrato ("técnicas padrão de persistência em armazenamento secundário") que omite os mecanismos reais (RDB snapshot via fork/copy-on-write ou AOF append).
- **Classificação:** $\textbf{INSUFFICIENT}$ (ou $\textbf{RELATED}$)
- **Justificativa:** Menção da categoria ampla não supre a demanda de explicar o mecanismo específico.

### Cenário 4: Analogia Correta sem Aterrissagem no Domínio Perguntado
- **Pergunta:** *"Como funciona o isolamento de transações com controle otimista de concorrência?"*
- **Resposta:** *"É exatamente como quando duas pessoas editam um documento compartilhado na nuvem sem travar a tela de ninguém."*
- **Análise Semântica:** A analogia com edição colaborativa é pertinente, mas o candidato interrompe a resposta sem explicar como o software implementa isso (verificação de timestamp/versão no commit).
- **Classificação:** $\textbf{PARTIAL}$ (ou $\textbf{INSUFFICIENT}$)
- **Justificativa:** Analogia válida mas desprovida de explicitação da mecânica computacional correspondente.

### Cenário 5: Termo Técnico com Propriedade Incompatível / Conflitante
- **Pergunta:** *"Qual a principal característica de uma fila de mensagens assíncrona?"*
- **Resposta:** *"A fila assíncrona exige que o consumidor processe a mensagem imediatamente em tempo real mantendo a conexão TCP travada até a confirmação síncrona."*
- **Análise Semântica:** O candidato cita o termo "fila assíncrona", mas descreve exatamente uma chamada síncrona bloqueante, contradizendo a propriedade fundamental do conceito.
- **Classificação:** $\textbf{OFF\_TOPIC}$ (Contradição Conceitual)
- **Justificativa:** A atribuição de propriedades diametralmente opostas invalida a resposta.

### Cenário 6: Tecnologia Fictícia com Descrição Funcional Coerente
- **Pergunta:** *"Como o mecanismo ChronoMesh garante a sincronização temporal no cluster?"*
- **Resposta:** *"O ChronoMesh utiliza relógios lógicos de Lamport combinados com algoritmos de desempate por identificador de nó para ordenar linearmente os eventos distribuídos."*
- **Análise Semântica:** A tecnologia "ChronoMesh" é fictícia, mas a explicação baseia-se em conceitos rigorosos da ciência da computação (relógios lógicos de Lamport, linearização determinística).
- **Classificação:** $\textbf{DIRECT}$
- **Justificativa:** Avaliação pelo mérito conceitual e funcional intrínseco, e não por catalogação prévia de nomes de mercado.

---

## 4. Declaração Explícita de Dependências Tecnológicas e Limites

Para operacionalizar a equivalência semântica aberta sem dicionários estáticos no futuro runtime:
1. **Mecanismo de Inferência Semântica Necessário:**
   - Extração de grafos de dependência sintática (Dependency Parsing);
   - Resolução de papéis temáticos (Semantic Role Labeling - SRL);
   - Mapeamento de sinonímia vetorial contextual ou modelo de linguagem calibrado.
2. **Entradas do Mecanismo:** Proposição textual normalizada + Perfil de Demanda.
3. **Saídas do Mecanismo:** Grau de compatibilidade de propriedades ($0.0$ a $1.0$) + Flag de incompatibilidade ontológica.
4. **Limitação Conhecida:** Regras léxicas determinísticas puras não conseguem cobrir 100% das paráfrases livres sem algum componente de inferência vetorial contextualizada. A especificação não assume que regexes possam resolver equivalência aberta.
