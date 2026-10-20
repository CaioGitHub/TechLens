# Stage 31.7.32 — Matriz de Fronteiras das Sete Classes Semânticas (21 Pares)

## 1. Visão Geral da Partição Ontológica

A arquitetura do Ciclo 6 fundamenta-se na partição estrita do espaço de relevância semântica em sete classes canônicas. Esta matriz audita as **21 fronteiras binárias possíveis** ($\binom{7}{2} = 21$), avaliando a clareza operacional dos critérios divisórios, os riscos residuais de ambiguidade e a resolução prescrita para casos limítrofes.

---

## 2. Auditoria Exaustiva dos 21 Pares de Classes

| # | Par de Classes | Critério Divisório Fundamental | Clareza Operacional | Risco de Ambiguidade | Contraexemplo Adversarial | Resolução Determinística Prescrita |
|:---:|---|---|:---:|:---:|---|---|
| **1** | **DIRECT vs PARTIAL** | Atendimento integral de todas as demandas obrigatórias ($D_P \land D_S$) vs omissão de ao menos uma demanda obrigatória secundária. | Alta | Médio | Resposta cobre $D_P$ e cita $D_S$ em apenas uma palavra elíptica. | Se a palavra citar a propriedade invariante $\to$ `DIRECT`; se for menção vaga sem mecanismo $\to$ `PARTIAL`. |
| **2** | **DIRECT vs SUPPORTING** | Ação direta sobre a causa-raiz/mecanismo solicitado vs instrumentação auxiliar passiva (logs, métricas, alertas). | Alta | Baixo | Configurar dashboard Prometheus para diagnosticar contenção de conexões no pool. | Se a pergunta pede causa e solução de problema, instrumentação pura é estritamente `SUPPORTING`. |
| **3** | **DIRECT vs RELATED** | Resposta atende à demanda operacional/conceitual pedida vs resposta apenas relata metadados do ecossistema (origem, criador, licença). | Muito Alta | Baixo | Origem do PostgreSQL em Berkeley perante pergunta sobre controle de concorrência MVCC. | Sem resolução do mecanismo de concorrência, o metadado histórico é estritamente `RELATED`. |
| **4** | **DIRECT vs OFF_TOPIC** | Resposta resolve a demanda no domínio de software vs resposta discorre sobre universo alienígena ou propõe antítese destrutiva. | Muito Alta | Baixo | Desativar transações ACID e desabilitar fsync para acelerar escritas no banco. | Antítese destrutiva que anula a garantia essencial da pergunta é estritamente `OFF_TOPIC`. |
| **5** | **DIRECT vs INSUFFICIENT** | Demonstração substantiva de propriedades invariantes vs preenchimento retórico vazio/elogio ("é muito bom"). | Muito Alta | Baixo | "O Apache Kafka é moderno, incrível e resolve todos os problemas de microsserviços." | Elogios vazios sem dados técnicos, arquiteturais ou mecânicos são estritamente `INSUFFICIENT`. |
| **6** | **DIRECT vs UNKNOWN** | Proposição com valor de verdade verificável e resolutivo vs asserção tautológica circular ou paradoxal indecidível. | Alta | Muito Baixo | "O sistema distribui os dados distribuindo-os de maneira distribuída." | Tautologias puras sem propriedades computacionais são estritamente `UNKNOWN`. |
| **7** | **PARTIAL vs SUPPORTING** | Atuação causal substantiva sobre um aspecto da falha vs fornecimento de telemetria passiva para observação do sistema. | Média | Médio | Timeout de lock (atuação na causa) acompanhado de painel no Grafana. | Havendo qualquer intervenção causal no fluxo do sistema, o mérito substantivo prevalece $\to$ `PARTIAL`. |
| **8** | **PARTIAL vs RELATED** | Resposta resolve parcialmente a demanda de engenharia vs resposta apenas discute o ecossistema tecnológico geral. | Alta | Médio | Explicar réplicas de leitura sem explicar failover em pergunta sobre alta disponibilidade. | Resolução de réplicas atua sobre a demanda técnica $\to$ `PARTIAL`. Histórico de quem criou a ferramenta $\to$ `RELATED`. |
| **9** | **PARTIAL vs OFF_TOPIC** | Resposta atende parte da demanda técnica legítima vs desvio completo para outro domínio ou antítese destrutiva. | Muito Alta | Baixo | Responder particionamento de tópicos e ignorar ordem de entrega em pergunta composta de Kafka. | Omissão de aspecto secundário **NUNCA** pode ser rebaixada para `OFF_TOPIC`. Fixa `PARTIAL`. |
| **10** | **PARTIAL vs INSUFFICIENT** | Cobertura comprovada de ao menos uma demanda primária/secundária vs tentativa fracassada sem substância avaliável. | Alta | Médio | "Deadlock é quando duas threads travam. Sobre como resolver eu não sei." | A definição formal é correta e substantiva; a ignorância declarada na solução gera `PARTIAL`, não `INSUFFICIENT`. |
| **11** | **PARTIAL vs UNKNOWN** | Demonstração parcial de propriedades reais vs asserção conceitualmente truncada cuja interpretação é indecidível. | Média | Baixo | Afirmação com termos técnicos interrompida no meio da frase com reticências. | Sem fechamento sintático-semântico avaliável, encaminha para `UNKNOWN`. |
| **12** | **SUPPORTING vs RELATED** | Instrumentação utilizável (scripts, telemetria, traces) vs metadados institucionais/históricos (origem, mantenedores). | Alta | Médio | Citar que a documentação oficial da CNCF recomenda boas práticas de pods. | Menção à entidade mantenedora $\to$ `RELATED`. Diretiva concreta de configuração do pod $\to$ `SUPPORTING`. |
| **13** | **SUPPORTING vs OFF_TOPIC** | Ferramenta de apoio aplicável ao sistema computacional vs divagação sobre ofício humano não relacionado. | Muito Alta | Baixo | Usar cronômetro manual de pista de atletismo para medir latência de API. | Sem instrumentação de software computacional válida, trata-se de `OFF_TOPIC`. |
| **14** | **SUPPORTING vs INSUFFICIENT** | Apresentação de método de medição/telemetria concreto vs evasão ("isso a gente olha depois nos logs"). | Alta | Médio | "Dá uma olhada nos logs quando der erro." | Menção vaga e genérica sem métricas ou ferramentas concretas é `INSUFFICIENT`. |
| **15** | **SUPPORTING vs UNKNOWN** | Telemetria e instrumentação estruturada vs métrica incompreensível ou sem unidade/contexto definível. | Alta | Baixo | "O índice zeta do cluster precisa ser calibrado em 42." | Métrica sem base ontológica em software computacional $\to$ `UNKNOWN`. |
| **16** | **RELATED vs OFF_TOPIC** | Conexão contextual legítima com a ferramenta de TI vs universo alienígena (argila, safena, soneto) ou homonímia. | Alta | Médio | Discorrer sobre a dependência econômica de importações de petróleo em pergunta de Spring DI. | Predicados sobre comércio exterior derrubam a presunção temática $\to$ estritamente `OFF_TOPIC`. |
| **17** | **RELATED vs INSUFFICIENT** | Informação factual histórica/institucional real vs chavão publicitário ou declaração pura de ignorância. | Alta | Médio | "PostgreSQL é open-source sob licença BSD" vs "PostgreSQL é muito legal". | Fato de licenciamento/ecossistema $\to$ `RELATED`. Juízo de valor afetivo sem dados $\to$ `INSUFFICIENT`. |
| **18** | **RELATED vs UNKNOWN** | Metadado contextual claro vs declaração ambígua cujo vínculo com a ferramenta não pode ser verificado. | Média | Baixo | "O criador da tecnologia uma vez disse uma frase enigmática." | Sem referência factual identificável, encaminha para `UNKNOWN`. |
| **19** | **OFF_TOPIC vs INSUFFICIENT** | Divagação sobre outro domínio (artesanato, agricultura) vs resposta lacônica, filler ou declaração de não saber. | Muito Alta | Baixo | "Eu não sei responder isso porque nunca trabalhei com mensageria." | Declaração expressa de desconhecimento da demanda pertence a `INSUFFICIENT`, e não `OFF_TOPIC`. |
| **20** | **OFF_TOPIC vs UNKNOWN** | Evidência positiva de incompatibilidade de domínio vs incapacidade de identificar o domínio dos termos. | Média | Alto | Resposta com jargões densos de um framework proprietário nunca visto. | Havendo dúvida se a terminologia pertence a TI, a incerteza proíbe `OFF_TOPIC` $\to$ `UNKNOWN`. |
| **21** | **INSUFFICIENT vs UNKNOWN** | Tentativa de resposta com dados insuficientes (evasão, filler) vs afirmação estruturalmente indecidível ou contraditória. | Alta | Baixo | "Depende do alinhamento da constelação de servidores com a lua." | Ambiguidade e contradição conceitual irresolúvel geram `UNKNOWN`. Enrolação típica gera `INSUFFICIENT`. |

---

## 3. Conclusão da Auditoria das Fronteiras

Todas as 21 fronteiras foram formalizadas e possuem critérios operacionais de demarcação claros. A especificação do Stage 31.7.31 resolveu as principais fontes históricas de confusão:
1. `DIRECT vs RELATED`: Metadados históricos não são mais promovidos a `DIRECT`;
2. `RELATED vs OFF_TOPIC`: Metadados sem código não são mais rebaixados para `OFF_TOPIC`;
3. `INSUFFICIENT vs OFF_TOPIC`: Declarações de desconhecimento permanecem em `INSUFFICIENT` e não contaminam `OFF_TOPIC`;
4. `UNKNOWN vs INSUFFICIENT`: `UNKNOWN` foi reservado estritamente para indecidibilidade estrutural e incerteza ontológica.
