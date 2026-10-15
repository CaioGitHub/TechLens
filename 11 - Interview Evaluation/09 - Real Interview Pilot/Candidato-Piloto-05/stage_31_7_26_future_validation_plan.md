# Stage 31.7.26 — Plano de Validação Semântica Independente Futura (Ciclo 5)

## 1. Princípios e Requisitos Metodológicos Fundamentais

Este plano formaliza o protocolo para a futura validação empírica e cega do runtime após a implementação controlada da arquitetura do Ciclo 5 (em estágio posterior autorizado).

### 1.1. Status da Independência de Referência
O status de governança da independência do ground truth permanece rigorosamente fixado como:
$$\textbf{REFERENCE\_INDEPENDENCE\_UNRESOLVED}$$
Nenhuma alegação de validação cega ou independência poderá ser realizada utilizando datasets cujos casos foram consultados ou diagnosticados durante as auditorias dos Ciclos 1 a 4. O benchmark de 250 casos do Stage 31.7.25 é classificado como **Diagnóstico Histórico (Contaminado)** e não poderá ser utilizado como prova de generalização cega no Ciclo 5.

### 1.2. Requisito de Benchmark Inédito e Partição Cega
Para a futura validação:
1. Deve ser gerado ou coletado um novo conjunto de teste com casos rigorosamente inéditos.
2. A separação entre arquivo de entrada do runtime (`blind_input.json`) e arquivo de gabarito (`ground_truth.json`) deve ser estrita, com geração de hashes SHA-256 independentes antes de qualquer execução.
3. O executor do teste não deve ter acesso ao gabarito, e o validador não deve intervir no runtime.

---

## 2. Tipologia Estruturada dos Casos de Validação

O dataset de validação futura deverá conter uma distribuição balanceada abrangendo obrigatoriamente 17 grupos diagnósticos de teste:

1. **Domínio Semanticamente Disjunto (OFF_TOPIC):**
   Casos com perguntas técnicas e respostas tratando de domínios ontologicamente alheios (ex.: marcenaria, arquitetura clássica, agricultura, culinária, geologia). Exige identificação de disjunção sem dependência de catálogo fechado de palavras proibidas.
2. **Relação Temática sem Atendimento Funcional (RELATED):**
   Respostas contendo metadados institucionais, histórico de software, licenças de código aberto e popularidade de ferramentas da pergunta sem explicar o mecanismo técnico exigido.
3. **Contribuição Auxiliar (SUPPORTING):**
   Respostas descrevendo observabilidade periférica, ferramentas de telemetria ou boas práticas operacionais que complementam mas não resolvem a demanda primária.
4. **Satisfação Direta (DIRECT):**
   Respostas que fornecem o mecanismo causal completo e correto para todas as demandas primárias obrigatórias.
5. **Atendimento Parcial (PARTIAL):**
   Respostas que cobrem satisfatoriamente apenas uma parcela das demandas em perguntas compostas, ou fornecem explicação correta mas conceitualmente incompleta da demanda simples.
6. **Tentativa Insuficiente (INSUFFICIENT):**
   Respostas vagas, genéricas, com jargão difuso ou que apenas enunciam obviedades sem evidência técnica substantiva.
7. **Indeterminação Genuína (UNKNOWN):**
   Declarações explícitas de desconhecimento ("não sei", "nunca trabalhei com isso"), silêncio, fragmentos ininteligíveis ou saudações desprovidas de conteúdo.
8. **Perguntas Compostas com Dependências:**
   Perguntas com dois ou mais requisitos obrigatórios (ex.: partição + idempotência; isolamento ACID + resolução de deadlocks), testando a decomposição e agregação.
9. **Respostas Corretas sem Sobreposição Lexical:**
   Respostas conceitualmente perfeitas que não utilizam os substantivos ou verbos contidos no enunciado da pergunta (teste de invariância semântica profunda).
10. **Linguagem Coloquial e Expressões Informais:**
    Candidatos que utilizam metáforas práticas do dia a dia da engenharia (ex.: "jogar na esteira", "dar um bypass no cache") para expressar soluções corretas.
11. **Entidades e Tecnologias Inéditas:**
    Perguntas e respostas utilizando nomes de tecnologias hipotéticas ou recém-lançadas (ex.: "NovaQueue", "ZetaDB") operando sob princípios canônicos de computação.
12. **Mutações Pareadas Equivalentes (Invariância Semântica):**
    Pares de respostas com o mesmo significado técnico em diferentes estilos (longo vs curto, formal vs informal, voz ativa vs passiva).
13. **Respostas Extremas por Extensão:**
    Respostas ultracurtas e precisas (que devem ser DIRECT) versus respostas prolixas e vazias (que devem ser INSUFFICIENT ou RELATED).
14. **Circularidade e Tautologia:**
    Respostas que apenas repetem a pergunta em outras palavras sem adicionar nenhum mecanismo causal novo.
15. **Polaridade e Contradição Explícita:**
    Respostas que afirmam o inverso do funcionamento técnico correto (antítese explícita), que devem ser rejeitadas de `DIRECT`.
16. **Satisfação Válida de Múltiplas Demandas por Proposição Unificada:**
    Sentenças únicas de alta densidade semântica que resolvem simultaneamente dois aspectos da pergunta de forma legítima.
17. **Divergência entre Interpretação Local e Escopo Global:**
    Respostas com uma oração sintaticamente plausível, mas cujo contexto discursivo geral invalida a relevância técnica.

---

## 3. Limiares Contratuais de Validação e Fórmulas Explícitas

A aprovação do runtime no Ciclo 5 exigirá o cumprimento simultâneo dos seguintes limiares matemáticos estritos:

### 3.1. Concordância Exata Global ($\ge 75\%$)
$$\text{Exact Agreement} = \frac{\sum_{i=1}^{N} \mathbb{I}(y_i = \hat{y}_i)}{N} \ge 0.75$$
- *Numerador:* Número total de predições idênticas ao ground truth.
- *Denominador:* Número total de casos avaliados ($N$).

### 3.2. Recall de DIRECT ($\ge 85\%$)
$$\text{Recall}_{\text{DIRECT}} = \frac{\text{TP}_{\text{DIRECT}}}{\text{TP}_{\text{DIRECT}} + \text{FN}_{\text{DIRECT}}} \ge 0.85$$
- *Numerador:* Casos com ground truth `DIRECT` classificados pelo sistema como `DIRECT`.
- *Denominador:* Total de casos com ground truth `DIRECT`.

### 3.3. Precisão de DIRECT ($\ge 70\%$)
$$\text{Precision}_{\text{DIRECT}} = \frac{\text{TP}_{\text{DIRECT}}}{\text{TP}_{\text{DIRECT}} + \text{FP}_{\text{DIRECT}}} \ge 0.70$$
- *Numerador:* Casos com ground truth `DIRECT` classificados pelo sistema como `DIRECT`.
- *Denominador:* Total de casos classificados pelo sistema como `DIRECT` ($\text{TP}_{\text{DIRECT}} + \text{FP}_{\text{DIRECT}}$).

### 3.4. Taxa de Falsos DIRECT entre Divergências ($\le 10\%$)
$$\text{False DIRECT Rate} = \frac{\text{FP}_{\text{DIRECT}}}{\text{Total Divergences}} \le 0.10$$
- *Numerador:* Total de falsos positivos da classe `DIRECT` ($\text{FP}_{\text{DIRECT}}$).
- *Denominador:* Total de casos divergentes no benchmark ($N - \text{Acertos}$).

### 3.5. Recall de PARTIAL ($\ge 60\%$)
$$\text{Recall}_{\text{PARTIAL}} = \frac{\text{TP}_{\text{PARTIAL}}}{\text{TP}_{\text{PARTIAL}} + \text{FN}_{\text{PARTIAL}}} \ge 0.60$$
- *Numerador:* Casos com ground truth `PARTIAL` classificados como `PARTIAL`.
- *Denominador:* Total de casos com ground truth `PARTIAL`.

### 3.6. Taxa de Invariância Semântica Pareada ($\ge 80\%$)
$$\text{Invariance Rate} = \frac{\sum_{p \in \text{Pares}} \mathbb{I}(\hat{y}_{p.1} = \hat{y}_{p.2} \land \hat{y}_{p.1} = y_{p}^*)}{|\text{Pares}|} \ge 0.80$$
- *Numerador:* Pares semanticamente equivalentes onde ambas as variantes recebem a mesma predição e esta coincide com o ground truth.
- *Denominador:* Total de pares testados.

### 3.7. Não-Regressão em Classes Estáveis (Zero Falhas Injustificadas)
- Zero rebaixamento não justificado nos casos das classes estáveis confirmadas no Ciclo 4 (`UNKNOWN` com recall $\ge 95\%$ e precisão $= 100\%$; `PARTIAL` com recall $\ge 90\%$).

---

## 4. Protocolo de Auditoria e Handoff de Governança

1. O relatório de execução da validação deverá registrar o log completo de predições, matriz de confusão e métricas recalculadas.
2. Todas as discrepâncias entre classes adjacentes deverão ser acompanhadas da justificativa emitida pelo `StrictOntologyRelevanceAggregator`.
3. Se qualquer limiar for violado, o estágio deverá registrar formalmente o status `BLOCKED` e convocar novo ciclo de RCA, preservando a integridade metodológica do sistema.
