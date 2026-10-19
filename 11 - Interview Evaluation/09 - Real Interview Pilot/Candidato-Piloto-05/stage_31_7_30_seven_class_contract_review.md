# Stage 31.7.30 — Revisão Adversarial dos Contratos Formais das Sete Classes Canônicas

## 1. Fundamentos e Princípios de Demarcação

O sistema TechLens opera sobre uma partição ontológica estrita e fechada de **sete classes de relevância semântica**. Nenhuma classe pode ser utilizada como "lixeira residual" ou inferida por mera falha de casamento de regras concorrentes. A classificação deve resultar de evidências afirmativas acumuladas ao longo do pipeline de raciocínio.

---

## 2. Revisão Exaustiva das Sete Classes

### 2.1. `DIRECT` (Atendimento Funcional Pleno)
1. **Condições Necessárias:** A resposta deve abordar a entidade e o fenômeno centrais indagados e cumprir todos os aspectos obrigatórios da intenção da pergunta (definição, mecanismo, comparação, diagnóstico ou implementação).
2. **Evidências Suficientes:** Proposição substantiva cujos predicados atuam de forma causal, conceitual ou operacional sobre as entidades do domínio da demanda, resolvendo o problema técnico sem omissão crítica.
3. **Distinção das Classes Vizinhas:**
   - *vs. RELATED:* `DIRECT` resolve o mecanismo ou elucida a definição; `RELATED` apenas menciona o contexto da tecnologia (origem, criadores, popularidade) sem atender à demanda.
   - *vs. SUPPORTING:* `DIRECT` atua sobre a causa-raiz da pergunta; `SUPPORTING` atua sobre a instrumentação periférica (telemetria, logs, dashboards).
4. **Contraexemplo Notável:** Descrição detalhada de como confeccionar argila com verbos transitivos ativos. Embora gramaticalmente operacional, atua sobre domínio estranho e deve ser rejeitada.
5. **Incertezas Limitantes:** Respostas excessivamente curtas ou elípticas onde o mecanismo está implícito mas não explicitado formalmente.
6. **Relação com a Intenção:** Para perguntas conceituais ("O que é"), a definição formal é suficiente; não se pode exigir código executável. Para perguntas de diagnóstico ("Como investigar"), o procedimento de isolamento é suficiente.
7. **Risco de Falso Positivo (FP):** Promoção de respostas de outros ofícios com verbos operacionais (como ocorreu no Ciclo 5).
8. **Risco de Falso Negativo (FN):** Rejeitar respostas formuladas em linguagem coloquial de engenharia ou com paráfrases de hiperônimos (e.g. "árvore balanceada" em vez de "B-tree").

### 2.2. `PARTIAL` (Atendimento Parcial de Demandas Múltiplas)
1. **Condições Necessárias:** A pergunta deve possuir mais de uma demanda primária obrigatória (pergunta composta), e o candidato deve responder com mérito a ao menos uma, deixando outra descoberta.
2. **Evidências Suficientes:** Demonstração inequívoca de cobertura do aspecto $A_1$ (e.g. particionamento por hash) e omissão/desconhecimento comprovado do aspecto $A_2$ (e.g. rebalanceamento de consumidores).
3. **Distinção das Classes Vizinhas:**
   - *vs. DIRECT:* `PARTIAL` possui lacunas em demandas obrigatórias; `DIRECT` cobre todas.
   - *vs. SUPPORTING:* `PARTIAL` atende de forma resolutiva a uma parte da causa-raiz; `SUPPORTING` fornece apenas suporte instrumental a toda a pergunta.
4. **Contraexemplo Notável:** Responder a uma pergunta composta fornecendo apenas observabilidade para as duas demandas. Isso é `SUPPORTING`, e não `PARTIAL`.
5. **Incertezas Limitantes:** Proposições densas onde uma única oração atende implicitamente às duas demandas (risco de fragmentação indevida).
6. **Relação com a Intenção:** Exige decomposição estruturada dos objetivos semânticos da pergunta.
7. **Risco de FP:** Fragmentar perguntas simples e rebaixar respostas diretas legítimas para `PARTIAL`.
8. **Risco de FN:** Aceitar respostas prolixas que resolvem apenas um ponto e ignoram o cerne do segundo aspecto, promovendo para `DIRECT`.

### 2.3. `SUPPORTING` (Suporte Auxiliar ou Instrumental)
1. **Condições Necessárias:** O conteúdo deve ser tecnicamente pertinente à infraestrutura ou à governança do sistema indagado, mas focar em observabilidade, monitoramento passivo, alertas ou logging.
2. **Evidências Suficientes:** Proposição descrevendo métricas Prometheus, dashboards Grafana, traces OpenTelemetry, healthchecks ou alertas em canais de mensageria voltados à tecnologia da pergunta.
3. **Distinção das Classes Vizinhas:**
   - *vs. DIRECT:* Se a pergunta for "Como diagnosticar lentidão na API", a observabilidade é `DIRECT`. Se a pergunta for "Como resolver contenção de locks", a observabilidade é `SUPPORTING` (ajuda a ver o lock, mas não o resolve).
   - *vs. OFF_TOPIC:* `SUPPORTING` é diretamente conectado à infraestrutura do software; `OFF_TOPIC` é disjunto.
4. **Contraexemplo Notável:** Monitorar o consumo de combustível de um caminhão em uma pergunta sobre banco de dados. Isso é `OFF_TOPIC`, pois a instrumentação pertence a outro domínio.
5. **Incertezas Limitantes:** Linha tênue entre pré-requisitos de governança e solução técnica principal.
6. **Risco de FP:** Classificar procedimentos ativos de diagnóstico (stack traces do heap dump) como mero suporte quando a pergunta pedia investigação.
7. **Risco de FN:** Rebaixar telemetria legítima para `OFF_TOPIC` por falta de comandos SQL ou código de negócio.

### 2.4. `RELATED` (Contexto Temático sem Mecanismo Operacional)
1. **Condições Necessárias:** A resposta deve compartilhar o ecossistema, a tecnologia, a categoria de software ou a ferramenta da pergunta, mas não fornecer a mecânica exigida pela intenção.
2. **Evidências Suficientes:** Proposição discutindo história (e.g. origem do PostgreSQL em Berkeley), fundações mantenedoras (Linux Foundation, CNCF), licenças de software, criadores, ou declarações genéricas de uso na carreira.
3. **Distinção das Classes Vizinhas:**
   - *vs. DIRECT:* Falta de mecanismo operacional; discute o contexto da ferramenta sem responder "como funciona".
   - *vs. OFF_TOPIC:* `RELATED` compartilha a tecnologia legítima de software; `OFF_TOPIC` fala sobre argila, cimento ou botânica.
4. **Contraexemplo Notável:** Citar o nome da ferramenta em uma frase sobre animais de estimação ou piadas familiares. Isso é `OFF_TOPIC` ou `INSUFFICIENT`, e não `RELATED`.
5. **Incertezas Limitantes:** Declarações de experiência que contêm termos operacionais esparsos sem atingir completude.
6. **Risco de FP:** Promover metadados institucionais a `DIRECT` se o candidato falar com eloquência e citar verbos ativos ("criou", "expandiu").
7. **Risco de FN:** Rebaixar metadados legítimos para `OFF_TOPIC` (a falha crônica eliminada no RCA do Ciclo 6).

### 2.5. `OFF_TOPIC` (Disjunção Radical ou Antítese Destrutiva)
1. **Condições Necessárias:** Evidência afirmativa de que as entidades nucleares pertencem a um universo não computacional sem transposição analógica, OU proposição de ações que destroem garantias básicas de operação/segurança.
2. **Evidências Suficientes:** Substantivos e predicados de agricultura, culinária, artesanato, medicina, esportes; OU instruções para desativar locks, desabilitar transações ACID, arrancar circuit breakers sem salvaguarda de evitação.
3. **Distinção das Classes Vizinhas:**
   - *vs. RELATED:* `OFF_TOPIC` não compartilha o ecossistema de software; `RELATED` compartilha o ecossistema mas não responde à mecânica.
   - *vs. INSUFFICIENT:* `INSUFFICIENT` tenta responder ao contexto computacional mas não tem substância; `OFF_TOPIC` fala sobre outro assunto inteiramente.
4. **Contraexemplo Notável:** Analogia pedagógica de disjuntor elétrico residencial para explicar circuit breaker. Deve ser `DIRECT`, e NÃO `OFF_TOPIC`.
5. **Incertezas Limitantes:** Termos homônimos ou metafóricos utilizados na engenharia de software (e.g. "árvore", "garfo/fork", "tubulação/pipeline").
6. **Risco de FP:** Bloquear analogias válidas ou tecnologias fictícias/novas não catalogadas.
7. **Risco de FN:** Aceitar processos de outros ofícios humanos como se fossem soluções computacionais diretas.

### 2.6. `INSUFFICIENT` (Substância Técnica Insuficiente ou Evasiva)
1. **Condições Necessárias:** Tentativa de resposta no contexto da entrevista que não chega a articular uma proposição técnica avaliável.
2. **Evidências Suficientes:** Declarações explícitas de ignorância ("Não sei", "Nunca estudei"), evasão corporativa/orçamentária ("Depende da reunião com a diretoria"), sopa de letrinhas vazia ("buzzword padding"), ou meros preenchimentos conversacionais ("Com certeza, perfeitamente").
3. **Distinção das Classes Vizinhas:**
   - *vs. UNKNOWN:* `INSUFFICIENT` é falta de conteúdo ou desconhecimento do candidato; `UNKNOWN` é indeterminação intrínseca do enunciado ou tautologia circular.
   - *vs. OFF_TOPIC:* `INSUFFICIENT` reconhece a pergunta ou tenta desvencilhar-se dela dentro do ambiente da entrevista; `OFF_TOPIC` discursa sobre outro universo temático.
4. **Contraexemplo Notável:** Dizer "Não sei" e em seguida tentar uma hipótese fundamentada. Se houver hipótese técnica, a resposta deve ser avaliada no mérito (`PARTIAL` ou `RELATED`), e não descartada como `INSUFFICIENT`.
5. **Risco de FP:** Classificar respostas concisas e certeiras como insuficientes devido ao tamanho curto do texto.
6. **Risco de FN:** Aceitar deflexões políticas ou enrolações corporativas como respostas arquiteturais válidas.

### 2.7. `UNKNOWN` (Indeterminação Semântica e Tautologia Reflexiva)
1. **Condições Necessárias:** Enunciados onde o significado proposicional é intrinsecamente indecidível (ambiguidade insolúvel sem critérios) ou formalmente vazio de informação (tautologia circular reflexiva).
2. **Evidências Suficientes:** Construções do tipo $X$ faz $Y$ porque $X$ é $X$ ("A replicação replica porque mantém o cluster replicado"), ou afirmações onde premissas contraditórias se anulam sem resolução condicional.
3. **Distinção das Classes Vizinhas:**
   - *vs. INSUFFICIENT:* Em `INSUFFICIENT`, o candidato declara que não sabe ou enrola; em `UNKNOWN`, ele constrói uma proposição gramaticalmente assertiva, mas cujo conteúdo semântico tem valor nulo de informação.
4. **Risco de FP:** Rotular respostas com trade-offs legítimos e condicionais bem formulados ("Depende: se for leitura pesada usamos X, se for escrita usamos Y") como ambíguas.
5. **Risco de FN:** Tratar tautologias circulares vazias como definições diretas conceituais.

---

## 3. Matriz de Diferenciações Críticas Obrigatórias

| Par de Fronteira | Critério Demarcador Inegociável | Decisão em Caso de Dúvida |
|---|---|:---:|
| **`DIRECT` vs. `RELATED`** | A resposta demonstra a mecânica causal/operacional da demanda ou elucida a definição formal requerida? Se demonstrar $\to$ `DIRECT`. Se apenas contextualizar a tecnologia $\to$ `RELATED`. | `RELATED` |
| **`RELATED` vs. `OFF_TOPIC`** | A resposta referencia legitimamente a tecnologia/ecossistema da pergunta? Se sim $\to$ `RELATED`. Se o conteúdo pertencer a universos não computacionais sem ligação $\to$ `OFF_TOPIC`. | `RELATED` |
| **`SUPPORTING` vs. `DIRECT`** | A proposição resolve o fenômeno central da pergunta ou atua apenas como telemetria/observabilidade periférica? | `SUPPORTING` |
| **`PARTIAL` vs. `SUPPORTING`** | Em perguntas compostas, a resposta resolve substantivamente um dos aspectos causais da demanda? Se sim $\to$ `PARTIAL`. Se oferecer apenas monitoramento para ambos $\to$ `SUPPORTING`. | `SUPPORTING` |
| **`INSUFFICIENT` vs. `UNKNOWN`** | O candidato declarou ignorância ou evasão (`INSUFFICIENT`), ou construiu uma assertiva circular/ambígua sem informação (`UNKNOWN`)? | `INSUFFICIENT` |
| **`INSUFFICIENT` vs. `OFF_TOPIC`** | O enunciado é um ruído conversacional da entrevista (`INSUFFICIENT`) ou uma dissertação sobre outro ofício humano (`OFF_TOPIC`)? | `INSUFFICIENT` |
