# Stage 31.7.31 — Contrato de Segmentação de Proposições e Composição de Contexto

## 1. Princípio da Composição Proposicional Contextualizada

A análise semântica não pode tratar frases isoladas como se fossem respostas estanques, nem descartar cegamente trechos que pareçam não-técnicos sem avaliar sua função modificadora. 

A proposição individual é uma **unidade intermediária de análise**, e a avaliação final resulta da **composição das proposições estruturadas segundo suas relações de dependência discursiva**:

$$\text{Relevância}(\text{Resposta}) = \text{Composição}\Big( \big\{ P_1, P_2, \dots, P_n \big\}, \mathcal{R}_{\text{discurso}} \Big)$$

---

## 2. Tipologia de Relações Discursivas e Modificadores

| Relação Discursiva | Marcadores Gramaticais Típicos | Efeito sobre a Avaliação Semântica |
|---|---|---|
| **Preâmbulo Fático / Ruído** | *"Hoje o dia foi corrido"*, *"o trânsito estava horrível"*, *"tomei um café"*. | Isolado como ruído de contato; não contamina a avaliação substantiva. |
| **Condicional Restritiva** | *"Se X acontecer..."*, *"caso o buffer atinja o limite..."*, *"sob condição de..."*. | Vincula o escopo de validade da afirmação; não pode ser descolada da consequência. |
| **Escopo de Negação** | *"Não devemos"*, *"sem recorrer a"*, *"para evitar"*, *"nunca"*. | Inverte a polaridade semântica da ação; impede falso disparo de antítese destrutiva. |
| **Concessão** | *"Embora aumente a latência..."*, *"apesar do custo de memória..."*. | Reconhece trade-offs; valoriza a maturidade técnica da resposta. |
| **Contradição Interna** | *"Na verdade não oferece garantia"*, *"mas isso não funciona"*. | Anula a asserção prévia; aciona rebaixamento por inconsistência lógica. |
| **Autocorreção Explícita** | *"Pensei que fosse X, mas na verdade vi que é Y"*, *"corrigindo o que eu disse..."*. | A asserção retificada é descartada; a asserção corretiva assume a autoridade. |
| **Composição Cumulativa** | *"Primeiro fazemos A. Em seguida, B. Por fim, C."* | As proposições somam-se para atingir a cobertura plena das demandas. |

---

## 3. Resolução dos Cinco Casos Canônicos de Composição

### Caso A: Preâmbulo Irrelevante e Resposta Correta
- **Texto:** *"Hoje o trânsito estava péssimo. Paxos permite que processos distribuídos cheguem a um acordo sob determinadas condições de falha."*
- **Estrutura Discursiva:** $P_1$ = Ruído Fático (`CONVERSATIONAL_PREAMBLE`); $P_2$ = Mecanismo de Consenso (`TECHNICAL_CORE`).
- **Resolução:** O motor isola $P_1$ e avalia $P_2$. A presença de "trânsito" não dispara disjunção nem contamina a resposta.
- **Classificação:** $\textbf{DIRECT}$

### Caso B: Resposta Correta Seguida de Contradição Destrutiva
- **Texto:** *"O isolamento serializável procura garantir um resultado equivalente a uma execução serial. Na verdade, ele não oferece nenhuma garantia de isolamento."*
- **Estrutura Discursiva:** $P_1$ = Definição correta; $P_2$ = Negação categórica que destrói o conceito prévio (`DISCURSIVE_CONTRADICTION`).
- **Resolução:** O motor **não pode** cometer o erro de pegar apenas $P_1$ e ignorar $P_2$. A contradição interna direta destrói o valor de verdade do enunciado.
- **Classificação:** $\textbf{INSUFFICIENT}$ (ou $\textbf{OFF\_TOPIC}$ por antítese conceitual)

### Caso C: Condicional Relevante com Escopo Restrito
- **Texto:** *"Se a dependência estiver indisponível e o Circuit Breaker estiver aberto, a chamada pode ser rejeitada sem executar uma nova tentativa contra o serviço."*
- **Estrutura Discursiva:** Prótase condicional ($P_{cond}$) acoplada à apódose resolutiva ($P_{res}$).
- **Resolução:** O motor avalia o conjunto $P_{cond} \to P_{res}$. A rejeição da chamada é uma ação correta *precisamente porque está sob a condição do circuito aberto*. O escopo condicional é integralmente preservado.
- **Classificação:** $\textbf{DIRECT}$

### Caso D: Autocorreção Explícita pelo Respondente
- **Texto:** *"Inicialmente pensei que o índice fosse usado, mas, analisando o plano de execução, percebi que o banco realizou uma varredura sequencial."*
- **Estrutura Discursiva:** $P_{antiga}$ = Hipótese inicial equivocada; $P_{nova}$ = Constatação fática baseada no plano (`CORRECTED_CONCLUSION`).
- **Resolução:** O marcador *"mas, analisando... percebi"* sinaliza autocorreção metodológica válida. $P_{antiga}$ é rotulada como retratada, e $P_{nova}$ é adotada como a conclusão real do candidato.
- **Classificação:** $\textbf{DIRECT}$

### Caso E: Resposta Distribuída entre Três Frases
- **Texto:** *"Idempotência é a propriedade de manter o mesmo estado final sob múltiplas execuções. No REST, implementamos com tokens únicos de transação no header. No entanto, ela aumenta a retenção de dados temporários no Redis."*
- **Estrutura Discursiva:**
  - $P_1$: Definição formal conceitual;
  - $P_2$: Mecanismo de implementação técnica;
  - $P_3$: Análise de trade-off de recursos.
- **Resolução:** Cada frase cobre um aspecto da resposta. O motor executa a **síntese composicional cumulativa**, consolidando definição + implementação + trade-off em uma única avaliação plena.
- **Classificação:** $\textbf{DIRECT}$ (com confiança máxima)
