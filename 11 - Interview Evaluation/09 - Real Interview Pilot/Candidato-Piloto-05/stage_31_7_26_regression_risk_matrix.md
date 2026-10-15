# Stage 31.7.26 — Matriz de Riscos de Regressão e Salvaguardas de Comportamentos Preservados (Ciclo 5)

## 1. Visão Geral

A implementação do Ciclo 5 visa sanar os 70 falsos `DIRECT` e a ausência de disjunção semântica identificados no Stage 31.7.25. Contudo, intervenções em mecanismos de filtragem semântica carregam o risco inerente de hipersensibilização, onde respostas corretas, formuladas de maneira atípica ou sem sobreposição lexical, podem ser indevidamente rebaixadas.

Este documento formaliza:
1. Os 14 comportamentos técnicos corretos cuja preservação é mandatória.
2. A análise detalhada de 12 riscos de regressão com severidade, probabilidade, detectabilidade e mitigações concretas.

---

## 2. Comportamentos Corretos Mandatórios a Preservar

A especificação do Ciclo 5 garante contratualmente a preservação dos seguintes padrões de resposta válidos:

1. **Respostas Corretas sem Sobreposição Lexical:**
   Respostas que explicam o mecanismo funcional da pergunta utilizando vocabulário inteiramente sinônimo ou conceitual sem repetir os termos exatos do enunciado (ex.: explicar coordenação e atomicidade em resposta à pergunta sobre 2PC).
2. **Explicações por Mecanismos ou Consequências Causais:**
   Respostas que demonstram o domínio técnico focando na cadeia de causa e efeito do sistema (ex.: descrever o surgimento de split-brain devido a partições de rede).
3. **Linguagem Coloquial e Informal:**
   Respostas em que o candidato expressa conceitos de alta senioridade em linguagem descontraída (ex.: "a gente pendura uma fila no meio pro worker não engasgar"), preservando a identificação do papel funcional do buffer/mensageria.
4. **Voz Passiva e Construções Impessoais:**
   Construções como "é realizado o particionamento das mensagens através do hash da chave" devem ser reconhecidas como operativas e equivalentes à voz ativa.
5. **Variações Morfológicas e Sintáticas:**
   Flexões verbais, substantivação de ações e variações de gênero/número não devem afetar a detecção das metas de aspecto.
6. **Entidades e Tecnologias Inéditas (Zero Catálogo Fechado):**
   Uso de bibliotecas, bancos de dados, linguagens ou ferramentas proprietárias ou recém-lançadas não deve disparar falsos `OFF_TOPIC` nem rebaixar para `INSUFFICIENT` se o papel causal for de engenharia.
7. **Respostas Conceituais Válidas:**
   Em perguntas sobre princípios de arquitetura (ex.: "O que é inversão de dependência?"), respostas conceituais e definições axiomáticas devem ser reconhecidas como `DIRECT` sem exigir código ou métricas operacionais desnecessárias.
8. **Respostas Práticas e Empíricas Válidas:**
   Em perguntas conceituais, candidatos que respondem exemplificando uma implementação prática concreta que atende ao princípio devem ser classificados como `DIRECT` ou `PARTIAL`, sem penalização por ausência de definição teórica formal.
9. **Perguntas Históricas, Institucionais ou Comparativas:**
   Em perguntas onde a demanda solicita expressamente evolução histórica, contexto de fundações ou trade-offs de adoção (ex.: "Por que o Kubernetes emergiu como padrão de orquestração?"), informações institucionais devem ser reconhecidas como atendimento direto da demanda.
10. **Respostas de Troubleshooting e Investigação:**
    Explicação metódica de processos de depuração, análise de heap dumps e isolamento de falhas devem ser reconhecidas como mecanismos operacionais válidos de diagnóstico.
11. **Distinção Estrita entre Resposta Parcial e Resposta Irrelevante:**
    Uma resposta que resolve com maestria 1 de 2 demandas não pode ser jogada para `RELATED` ou `OFF_TOPIC`; deve permanecer firmemente ancorada em `PARTIAL`.
12. **Distinção entre Insuficiência e Indeterminação:**
    Tentativa fraca de resposta técnica é `INSUFFICIENT`; silêncio, ruído ou recusa explícita é `UNKNOWN`.
13. **Proteção contra Circularidade e Tautologia:**
    Frases que apenas refraseiam a pergunta (ex.: "O particionamento no Kafka funciona particionando os tópicos") devem continuar sendo vetadas de `FUNCTIONALLY_SOLVES`.
14. **Invariância Semântica Pareada:**
    Garantia de que formulações paráfrases, pares sucintos vs prolixos e variações de estilo preservem a mesma classe semântica categorial (meta $\ge 80\%$).

---

## 3. Matriz Detalhada de Riscos de Regressão

| ID | Risco | Severidade | Probabilidade | Detectabilidade | Evidência Atual no Sistema | Mitigação Arquitetural Proposta |
|---|---|---|---|---|---|---|
| **R01** | **Falsos DIRECT Remanescentes** | Alta | Baixa | Alta | 70 casos no Stage 31.7.25 devido ao fallback irrestrito da linha 3434. | Eliminação completa do fallback incondicional; exigência de verificação explícita de domínio compatível e suficiência causal. |
| **R02** | **Falsos OFF_TOPIC (Hipersensibilização)** | Crítica | Média | Alta | 2 casos no Stage 31.7.25 onde respostas técnicas foram para `OFF_TOPIC`. | O `SemanticDomainDisjunctionEngine` exige evidência positiva de domínio disjunto radical (botânica, culinária, etc.); ausência de tokens não gera disjunção. |
| **R03** | **Falsos PARTIAL (Rebaixamento Indevido)** | Média | Média | Média | 1 caso `DIRECT -> PARTIAL` no benchmark do Ciclo 4. | O agregador só emite `PARTIAL` se houver demanda primária obrigatória formalmente não atendida; perguntas simples preservam `DIRECT`. |
| **R04** | **Perda de Respostas Válidas de Domínio Aberto** | Alta | Média | Média | O runtime anterior dependia de catálogo fechado de 25 palavras. | Contrato E (`OPEN_DOMAIN_PLAUSIBLE`): entidades desconhecidas são consideradas compatíveis se realizarem ações de engenharia de software. |
| **R05** | **Dependência Inadvertida de Vocabulário Fechado** | Alta | Baixa | Alta | Risco de desenvolvedores adicionarem listas estáticas de palavras para passar no benchmark. | Regra estrita de governança: proibido incluir listas de domínios específicos; validação em pipeline com linters de strings proibidas. |
| **R06** | **Generalização Insuficiente em Domínios Não Vistos** | Alta | Média | Baixa | Invariância caiu para 40% no Stage 31.7.25. | Avaliação baseada em papéis semânticos fundamentais (agente, ação, objeto, efeito) e não em entidades nominais. |
| **R07** | **Conflitos de Precedência entre Componentes** | Média | Baixa | Alta | Falta de clareza anterior entre `PropositionDiscourseFilter` e `NexusMatcher`. | Contratos formais A a G com responsabilidades e hierarquia estritas; autoridade exclusiva do `StrictOntologyRelevanceAggregator`. |
| **R08** | **Tratamento Incorreto de Perguntas Compostas** | Média | Média | Média | 5% das divergências históricas decorrentes de perguntas multirequisito. | Contrato A e D: identificação de demandas atômicas e exigência de cobertura para cada `aspect_goal` obrigatório. |
| **R09** | **Opacidade Decisória e Baixa Rastreabilidade** | Média | Baixa | Alta | Justificativas anteriores eram genéricas ("provides operative mechanism"). | Objeto `telemetry_trace` obrigatório em todas as predições, registrando o caminho lógico e os nexos individuais. |
| **R10** | **Indeterminismo ou Flutuação de Scores** | Crítica | Muito Baixa | Alta | O runtime é determinístico, mas novos módulos poderiam introduzir não-determinismo. | Garantia de execução estritamente determinística sem dependências estocásticas ou aleatórias. |
| **R11** | **Incerteza Mascarada por Classe Categorial** | Média | Média | Alta | Casos limítrofes recebiam `DIRECT` forçado. | Contrato G: se a confiança média dos nexos for $<0.5$, a predição é rebaixada para categoria de menor presunção (`INSUFFICIENT` ou `UNKNOWN`). |
| **R12** | **Regressão em Classes Estáveis (UNKNOWN e PARTIAL)** | Alta | Baixa | Alta | UNKNOWN atingiu 95.45% de recall e 100% de precisão no Stage 31.7.25; PARTIAL atingiu 93.33% de recall. | Conjunto de testes de não-regressão obrigatório para os 21 casos estáveis de UNKNOWN e 42 de PARTIAL antes de qualquer aprovação. |

---

## 4. Diretrizes para a Implementação Controlada no Ciclo 5

1. **Gate de Homologação Local:** Antes de qualquer submissão de benchmark cego, o runtime deve passar por um harness de teste unitário verificando os 14 comportamentos preservados.
2. **Critério de Parada:** Se qualquer teste de não-regressão das classes estáveis (`UNKNOWN`, `PARTIAL`) falhar, a modificação deve ser imediatamente revertida e investigada.
3. **Auditoria de Linhas de Código:** Nenhuma regra pode referenciar casos específicos do benchmark do Candidato-Piloto-05.
