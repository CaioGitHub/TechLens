# Stage 31.7.31 — Contrato Semântico de Conexão Temática Refutável

## 1. Princípio da Conexão Temática como Hipótese Intermediária

No Ciclo 6, o compartilhamento de entidades e termos entre pergunta e resposta **não opera como veto automático a `OFF_TOPIC` nem como garantia de `RELATED`**. O compartilhamento lexical atua estritamente como um **sinal indiciário inicial que formula uma hipótese refutável de pertinência temática**:

$$\text{Presunção de Conexão Temática } H_{tema} \iff (E_R \cap E_Q \neq \emptyset) \lor \text{Contexto}(E_R) \sim \text{Contexto}(E_Q)$$

Essa presunção é submetida a testes de refutação sintático-semânticos antes de qualquer decisão no pipeline.

---

## 2. Tipologia de Sinais e Demarcação Conceitual

| Tipo de Relação | Definição Semântica | Status da Presunção $H_{tema}$ | Ação do Motor |
|---|---|:---:|---|
| **Conexão Temática Legítima** | A resposta referencia a entidade tecnológica da pergunta e os predicados da oração atuam sobre o ecossistema de software correspondente. | **Confirmada** | Proíbe `OFF_TOPIC`. Avalia mérito funcional (`DIRECT`, `PARTIAL`, `SUPPORTING` ou `RELATED`). |
| **Coincidência Lexical Superficial** | A mesma palavra da pergunta aparece na resposta, mas em contexto puramente fático, coloquial ou como exemplo não técnico. | **Suspensa** | Submete a análise de desambiguação de contexto. |
| **Homonímia / Polissemia Desviante** | O termo é compartilhado, mas em acepção semântica radicalmente distinta (e.g. dependência em software vs dependência econômica de petróleo). | **Refutada com Certeza** | Classifica como `OFF_TOPIC`. A coincidência de string é descartada como ruído. |
| **Relação Indireta / Hiperonímica** | A resposta não cita o nome próprio da ferramenta, mas utiliza hiperônimos técnicos válidos (e.g. "árvore balanceada" para "B-tree"). | **Confirmada por Equivalência** | Concede presunção temática plena e avalia atendimento funcional (`DIRECT`). |
| **Conexão Plausível mas Fraca** | A resposta cita termos periféricos de TI sem ligação clara com a entidade-alvo. | **Incertidão / Atenuada** | Encaminha para `INSUFFICIENT` ou `RELATED` com confianca baixa (`confidence: LOW`). |

---

## 3. Critérios Formais de Refutação da Presunção

A hipótese preliminar $H_{tema}$ é formalmente **refutada** quando ocorrer qualquer uma das seguintes condições:
1. **Refutação por Predicado Alienígena:** O sujeito é a entidade da pergunta, mas os verbos de ação e complementos pertencem a outro domínio (e.g. geopolítica, culinária, biologia).
2. **Refutação por Uso Metonímico / Metafórico Não-Técnico:** A entidade é usada como nome de animal, vestimenta, piada ou elemento estético decorativo.
3. **Refutação por Antítese Destrutiva Desprovida de Guarda:** A entidade é mencionada no contexto de instruções explícitas para desativar suas garantias fundamentais de segurança/consistência.

---

## 4. Análise Rigorosa dos Quatro Casos Canônicos de Estresse

### Caso A: Mesmo Nome, Conteúdo Histórico
- **Pergunta:** *"Como o PostgreSQL implementa MVCC?"*
- **Resposta:** *"O PostgreSQL teve origem no projeto POSTGRES, na Universidade de Berkeley."*
- **Evidência Relevante:** Entidade `PostgreSQL` compartilhada; predicados históricos legítimos (`teve origem`, `projeto POSTGRES`, `Berkeley`); ausência de verbos de controle de concorrência.
- **Inferências Permitidas:** A resposta pertence ao domínio da tecnologia; o candidato conhece o contexto institucional da ferramenta.
- **Inferências Proibidas:** Inferir que a resposta explica o mecanismo de MVCC; rebaixar para `OFF_TOPIC` por falta de código.
- **Classificação Canônica Obrigatória:** $\textbf{RELATED}$
- **Justificativa:** Conexão temática confirmada, mas sem atendimento à demanda operacional da pergunta.

### Caso B: Mesmo Nome, Conteúdo Insuficiente (Filler / Elogio)
- **Pergunta:** *"Como o PostgreSQL implementa MVCC?"*
- **Resposta:** *"O PostgreSQL é ótimo."*
- **Evidência Relevante:** Entidade `PostgreSQL` citada literalmente; predicado de juízo de valor afetivo superficial (`é ótimo`); zero substância técnica ou histórica.
- **Inferências Permitidas:** O candidato ouviu a pergunta e repetiu o nome da tecnologia.
- **Inferências Proibidas:** Inferir conexão temática substantiva (`RELATED`); inferir resolução da pergunta (`DIRECT`).
- **Classificação Canônica Obrigatória:** $\textbf{INSUFFICIENT}$
- **Justificativa:** A mera menção do nome não transforma um preenchimento conversacional vazio em metadado técnico relevante.

### Caso C: Mesmo Termo, Sentido Diferente (Polissemia / Divagação)
- **Pergunta:** *"Como funciona a injeção de dependências no Spring?"*
- **Resposta:** *"A dependência econômica de um país pode aumentar quando ele importa petróleo."*
- **Evidência Relevante:** Compartilhamento do lexema `dependência`; argumentos nucleares pertencentes à economia internacional e comércio exterior (`país`, `importa`, `petróleo`).
- **Inferências Permitidas:** O candidato desviou para outro significado da palavra (homonímia/polissemia).
- **Inferências Proibidas:** Proibir `OFF_TOPIC` devido à presença da palavra "dependência"; classificar como `RELATED`.
- **Classificação Canônica Obrigatória:** $\textbf{OFF\_TOPIC}$
- **Justificativa:** Refutação categórica da presunção temática por predicados e complementos de domínio alienígena.

### Caso D: Resposta Correta sem Repetição do Nome Literal
- **Pergunta:** *"Como uma B-tree acelera uma consulta?"*
- **Resposta:** *"A estrutura mantém as chaves ordenadas em uma árvore balanceada, reduzindo o espaço de busca necessário para localizar um registro."*
- **Evidência Relevante:** Ausência das strings literais `B-tree` ou `índice`; presença dos conceitos fundamentais equivalentes (`chaves ordenadas`, `árvore balanceada`, `reduz espaço de busca`).
- **Inferências Permitidas:** O candidato compreende com precisão a estrutura e o mecanismo algorítmico do artefato indagado.
- **Inferências Proibidas:** Assumir ausência de conexão temática devido a $E_R \cap E_Q = \emptyset$; descartar para `OFF_TOPIC`.
- **Classificação Canônica Obrigatória:** $\textbf{DIRECT}$
- **Justificativa:** A equivalência funcional e conceitual prevalece sobre a identidade morfológica das palavras.
