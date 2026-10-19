# Stage 31.7.30 — Registro Adversarial de Riscos e Fragilidades Arquiteturais

## 1. Visão Geral da Análise de Riscos

A revisão adversarial do Stage 31.7.30 submeteu a arquitetura especificada no Stage 31.7.29 a um teste rigoroso de limites conceituais, revelando fragilidades teóricas que, se implementadas sem refatoração, gerariam novos padrões de erro sistêmico. Este registro formaliza os riscos residuais e prescreve as mitigações mandatórias.

---

## 2. Registro Detalhado de Riscos Arquiteturais

| ID | Título do Risco | Severidade | Probabilidade | Impacto | Mecanismo Concreto de Falha | Mitigação Arquitetural Mandatória |
|:---:|---|:---:|:---:|:---:|---|---|
| **AR-01** | **Veto Absoluto a OFF_TOPIC por Coincidência Lexical (Regra Incompatível com Homonímia)** | **Crítica** | Alta | Alto | O candidato usa o termo *"injeção de dependências"* mas divaga sobre dependência de importações de petróleo (Cenário E). A regra do Stage 31.7.29 proibiria `OFF_TOPIC`, forçando um falso `RELATED` ou `DIRECT`. | **Refatoração da Regra:** O compartilhamento de entidades gera apenas uma *presunção refutável* de conexão temática, que é derrubada se os predicados da oração atuarem sobre domínio alienígena. |
| **AR-02** | **Falso OFF_TOPIC em Respostas sem Repetição Literal de Entidade (Falha de Hiperônimos)** | **Crítica** | Média | Alto | Uma resposta explica perfeitamente B-tree chamando de *"árvore balanceada de chaves"* sem citar o termo literal *"B-tree"* (Cenário C). Uma checagem cega de $E_R \cap E_Q \neq \emptyset$ marcaria a resposta como desprovida de nexo. | **Expansão Ontológica de Equivalência:** O casamento de entidades deve reconhecer hiperônimos formais e definições conceituais canônicas, sem exigir identidade morfológica de strings. |
| **AR-03** | **Falso Disparo de Disjunção em Analogias Pedagógicas Válidas** | **Alta** | Média | Médio | O candidato explica Circuit Breaker comparando com o *"disjuntor elétrico residencial que desarma a chave"* (Caso STRESS-06). A detecção de termos físicos residenciais geraria falso `OFF_TOPIC`. | **Isolamento de Orações Analógicas:** Orações subordinadas comparativas (*"funciona como..."*, *"é similar a..."*) devem ser marcadas como analogias pedagógicas, avaliando o mérito sobre a oração principal. |
| **AR-04** | **Contaminação da Resposta por Preâmbulos Conversacionais de Ruído** | **Média** | Alta | Médio | O candidato inicia dizendo que *"o trânsito estava horrível"* e em seguida explica com perfeição o algoritmo Paxos (Caso STRESS-07). O preâmbulo ruidoso poderia contaminar a proposição técnica. | **Segmentação Oracional e Avaliação Proposicional Isolada:** O pipeline deve segmentar períodos independentes e avaliar a relevância da melhor proposição técnica substantiva. |
| **AR-05** | **Promoção de Elogios Triviais / Buzzwords para RELATED** | **Média** | Alta | Médio | Frases como *"O PostgreSQL é ótimo e muito popular"* (Cenário B) serem classificadas como `RELATED` simplesmente por conterem a palavra 'PostgreSQL'. | **Filtro de Substância Informacional:** Proposições de elogio superficial sem dados históricos, organizacionais ou arquiteturais devem ser rebaixadas para `INSUFFICIENT` (filler). |
| **AR-06** | **Ruptura de Contratos na Suíte Canônica Workspace (1.067 Testes)** | **Crítica** | Baixa | Extremo | A reestruturação de classes do agregador ontológico quebrar contratos dos testes unitários históricos das fases 20 a 31.7.27. | **Congelamento e Não-Regressão Obrigatória:** Nenhuma alteração no runtime pode ser aprovada sem 100% de passagem nos 1.067 testes canônicos e 15/15 no Reference Harness. |
| **AR-07** | **Incerteza Epistemológica de Independência de Referências** | **Alta** | Certa | Alto | O benchmark cego continuar sendo avaliado contra referências formalizadas internamente sem comitê duplo-cego externo. | **Manutenção Mandatória da Ressalva:** Preservar `REFERENCE_INDEPENDENCE_UNRESOLVED` em todas as fases até contratação de auditoria externa independente. |

---

## 3. Conclusão da Revisão de Riscos

A proposta do Stage 31.7.29 acertou no diagnóstico do RCA (identificando a falha das regexes fechadas e o sumidouro de `OFF_TOPIC`), mas errou ao propor uma regra de "veto absoluto" de `OFF_TOPIC` por simples presença de entidade. Essa regra é vulnerável a contraexemplos reais (Cenários B, C e E). A arquitetura necessita de **revisão corretiva condicionada** antes de receber autorização de plano de implementação.
