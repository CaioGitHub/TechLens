---
type: study
status: mastered
confidence: 100
created: 2026-10-19
updated: 2026-10-19
tags:
  - stage-31-7-28
  - blind-semantic-revalidation
  - cycle-5
  - independent-validation
  - failure-audit
  - blocked-gate
---

# Stage 31.7.28 — Independent Blind Semantic Revalidation (Cycle 5)

## 1. Identificação do Runtime e Integridade Criptográfica

O presente estágio executou uma auditoria cega, independente e controlada sobre o runtime produzido no Stage 31.7.27, avaliando seu comportamento sobre um dataset de 250 casos 100% inédito, gerado e selado antes de qualquer inferência.

- **Arquivo Canônico Avaliado:** `reference_runtime/runtime.py`
- **SHA-256 Inicial Verificado:**
  $$\textbf{6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28}$$
- **SHA-256 Final Verificado:**
  $$\textbf{6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28}$$
- **Status do Runtime:** Absolutamente congelado, inviolado e imutável durante todo o estágio (zero modificações de código, parâmetros ou limiares).
- **Ambiente de Execução:** Python 3.13.9 em Windows 11 (AMD64), executado em 2026-10-19T15:00:00Z.
- **Artefatos Criptograficamente Selados do Benchmark:**
  - `stage_31_7_28_ground_truth.json`: SHA-256 `C8C2822F18D1F5806A3EBF9FE18724F2972AA2C73799AD25A7072CD8C55DB5AF`
  - `stage_31_7_28_blind_input.json`: SHA-256 `036EE47E7B9A4BBFE91B5C0A2AF61CCC0A73CCCE899C767A3D5AA574D5724954`
  - `stage_31_7_28_system_predictions.json`: SHA-256 `F029BE72D8C91B4161E08555B1C9D52640FE272F56D449D9F5B069A51967D670`

---

## 2. Respostas às Oito Perguntas Orientadoras da Seção 15

### 1. O runtime congelado melhorou em casos realmente inéditos?
**Parcialmente.** Houve ganhos expressivos na classe `PARTIAL` (recall de **84,44%**), na classe `SUPPORTING` (recall de **96,67%**) e na detecção de incerteza/tautologia `UNKNOWN` (recall de **90,00%**). Contudo, a acurácia global atingiu **67,20% (168/250)**, ficando abaixo do limiar obrigatório de $\ge 75,00\%$.

### 2. A redução de falsos DIRECT se mantém fora do benchmark histórico?
**Não de forma suficiente.** No benchmark histórico de 250 casos (onde os domínios disjuntos coincidiam com os termos previamente auditados), os falsos `DIRECT` haviam caído para 6 casos. Porém, no benchmark cego inédito com novas áreas (artesanato em argila, construção civil, novas plantas, medicina), os falsos `DIRECT` subiram para **34 casos** (**41,46% de todas as 82 divergências**), violando frontalmente o limiar estipulado de $\le 10,00\%$.

### 3. As sete classes continuam sendo distinguidas adequadamente?
**Com distorções nas fronteiras `OFF_TOPIC` e `RELATED`.** O motor distinguiu muito bem `PARTIAL` (38/45 acertos), `SUPPORTING` (29/30 acertos) e `UNKNOWN` (18/20 acertos). Entretanto, houve confusão mútua severa entre `OFF_TOPIC` e `DIRECT` (26 falsos DIRECTs de off-topic), e 22 casos de `RELATED` foram indevidamente rebaixados para `OFF_TOPIC` (`non_operative_assertion`).

### 4. As perguntas compostas e as respostas parciais são tratadas corretamente?
**Sim.** A decomposição multiaspecto e o matching bipartido consolidaram o recall de `PARTIAL` em **84,44% (38/45)**, com apenas 1 caso de falso `DIRECT` originário de resposta parcial.

### 5. A classificação permanece estável diante de paráfrases equivalentes?
**Parcialmente.** A consistência interna de predição atingiu **80,00% (16/20 pares)**, mas a taxa de pares simultaneamente consistentes e corretos foi de **65,00% (13/20 pares)**, abaixo do critério de $\ge 80,00\%$.

### 6. Existem novas falhas de falso OFF_TOPIC ou perda de respostas válidas?
**Sim.** Observou-se o surgimento de **22 casos de `RELATED → OFF_TOPIC`**, onde respostas que discutiam legitimamente metadados institucionais, história e categorias da tecnologia perguntada foram classificadas como fora do assunto devido à ausência de verbos operacionais de código.

### 7. A regressão canônica permanece sem falhas inexplicadas?
**Sim, com perfeição absoluta.** A suíte canônica de testes do projeto executou **1.067 testes com 1.066 aprovações e 1 teste ignorado esperado (`OK (skipped=1)`) em 46,392s**, e o Reference Harness do Stage 26 executou **15 testes com 100% de aprovação em 34,687s**. Houve zero regressões no repositório.

### 8. A proveniência das referências permite sustentar a alegação de validação independente?
**Não como independente externa.** Embora os dados sejam 100% inéditos (zero colisões com 633 perguntas e 688 respostas passadas) e o isolamento cego tenha sido estritamente mantido por arquivos e hashes separados, as referências foram formalizadas internamente sem comitê duplo-cego externo. A ressalva $\textbf{REFERENCE\_INDEPENDENCE\_UNRESOLVED}$ é mantida obrigatoriamente.

---

## 3. Avaliação dos Critérios Formais de Aceitação

| Indicador Metodológico | Critério Alvo | Resultado Obtido | Status |
|---|:---:|:---:|:---:|
| **Acurácia Exata Global** | $\ge 75,00\%$ | **67,20%** (168/250) | **REPROVADO (BLOCKED)** |
| **Recall de `DIRECT`** | $\ge 85,00\%$ | **76,00%** (38/50) | **REPROVADO (BLOCKED)** |
| **Precisão de `DIRECT`** | $\ge 70,00\%$ | **52,78%** (38/72) | **REPROVADO (BLOCKED)** |
| **Falsos DIRECT entre Divergências** | $\le 10,00\%$ | **41,46%** (34/82) | **REPROVADO (BLOCKED)** |
| **Recall de `PARTIAL`** | $\ge 60,00\%$ | **84,44%** (38/45) | **APROVADO (PASSED)** |
| **Invariância Pareada Simultaneamente Correta** | $\ge 80,00\%$ | **65,00%** (13/20 pares) | **REPROVADO (BLOCKED)** |
| **Regressões Canônicas Inexplicadas** | **0** | **0** (1.067 testes OK, Harness 15/15) | **APROVADO (PASSED)** |

---

## 4. Matriz de Confusão Completa (7x7)

$$\begin{array}{l|ccccccc|c}
\textbf{Ref \backslash Pred} & \textbf{DIR} & \textbf{PAR} & \textbf{SUP} & \textbf{REL} & \textbf{OFF} & \textbf{INS} & \textbf{UNK} & \textbf{Total} \\
\hline
\textbf{DIRECT}      & \mathbf{38} & 3 & 3 & 3 & 3 & 0 & 0 & 50 \\
\textbf{PARTIAL}     & 1 & \mathbf{38} & 1 & 2 & 3 & 0 & 0 & 45 \\
\textbf{SUPPORTING}  & 0 & 0 & \mathbf{29} & 0 & 1 & 0 & 0 & 30 \\
\textbf{RELATED}     & 5 & 0 & 0 & \mathbf{8} & 22 & 0 & 0 & 35 \\
\textbf{OFF\_TOPIC}  & 26 & 1 & 0 & 0 & \mathbf{18} & 0 & 0 & 45 \\
\textbf{INSUFFICIENT}& 1 & 0 & 0 & 1 & 4 & \mathbf{19} & 0 & 25 \\
\textbf{UNKNOWN}     & 1 & 0 & 0 & 0 & 1 & 0 & \mathbf{18} & 20 \\
\hline
\textbf{Pred Total}  & 72 & 42 & 33 & 14 & 52 & 19 & 18 & \mathbf{250}
\end{array}$$

### 4.1. Métricas Detalhadas por Classe

| Classe | TP | FP | FN | Suporte | Predições | Precisão | Recall | F1-Score |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **`DIRECT`** | 38 | 34 | 12 | 50 | 72 | 52,78% | 76,00% | 62,30% |
| **`PARTIAL`** | 38 | 4 | 7 | 45 | 42 | 90,48% | 84,44% | 87,36% |
| **`SUPPORTING`** | 29 | 4 | 1 | 30 | 33 | 87,88% | 96,67% | 92,06% |
| **`RELATED`** | 8 | 6 | 27 | 35 | 14 | 57,14% | 22,86% | 32,65% |
| **`OFF_TOPIC`** | 18 | 34 | 27 | 45 | 52 | 34,62% | 40,00% | 37,11% |
| **`INSUFFICIENT`**| 19 | 0 | 6 | 25 | 19 | 100,00% | 76,00% | 86,36% |
| **`UNKNOWN`** | 18 | 0 | 2 | 20 | 18 | 100,00% | 90,00% | 94,74% |

---

## 5. Auditoria Qualitativa e Causal das 82 Divergências

Todas as 82 divergências foram auditadas em [`stage_31_7_28_divergence_analysis.json`](file:///d:/Projetos/TechLens/11%20-%20Interview%20Evaluation/09%20-%20Real%20Interview%20Pilot/Candidato-Piloto-05/stage_31_7_28_divergence_analysis.json). Destacam-se dois agrupamentos causais primários que explicam 58,5% das divergências:

### 1. Fragilidade de Cobertura Lexical no `SemanticDomainDisjunctionEngine` (26 casos `OFF_TOPIC → DIRECT`)
- **Evidência:** Casos como `VAL-31-7-28-183` a `VAL-31-7-28-205` continham texto sobre confecção de cerâmica e artesanato (*"O processo de confecção de vasos de argila do artesanato tradicional requer amassamento da pasta mineral na roda de oleiro com posterior queima em forno a lenha"*).
- **Mecanismo da Falha:** O motor procurava a expressão estrita `\bescultura em argila\b`, mas o texto continha `vasos de argila` e `pasta mineral`. Como os padrões regex do `SemanticDomainDisjunctionEngine` operam por catálogo de expressões fechadas, o texto alienígena não ativou a flag `is_disjoint`. Em seguida, a presença do verbo transitivo ativo `"requer"` fez o `PropositionDiscourseFilter` marcar `is_operative = True`. Na ausência de veto de domínio, o motor gerou `open_domain_mechanism_assertion` e concedeu `FUNCTIONALLY_SOLVES`, promovendo artesanato a `DIRECT`.

### 2. Hipersensibilização de `non_operative_assertion` Rebaixando Metadados (22 casos `RELATED → OFF_TOPIC`)
- **Evidência:** Casos como `VAL-31-7-28-133` (*"O PostgreSQL teve origem no projeto POSTGRES liderado por Michael Stonebraker na Universidade de Berkeley e é amplamente elogiado pela sua conformidade com padrões SQL"*) e dezenas de descrições institucionais de ferramentas.
- **Mecanismo da Falha:** O motor identificou corretamente que a resposta não continha um mecanismo técnico operacional. Contudo, em vez de rotular a relação como `THEMATICALLY_ADJACENT` e direcionar para `RELATED`, a oração foi tratada como `non_operative_assertion`, que no agregador é descarregada em `OFF_TOPIC`. Isso derrubou o recall de `RELATED` para **22,86%**.

---

## 6. Governança, Transparência e Decisão Formal de Gate

Seguindo estritamente as regras de `AGENTS.md` (Seções 1, 16, 17, 22 e 23) e os princípios inegociáveis do Second Brain:
- Não foram feitos ajustes ad-hoc para mascarar o resultado.
- As métricas foram publicadas sem qualquer maquiagem estatística.
- O bloqueio não é considerado uma falha do projeto, mas a demonstração da integridade do método científico: a validação cega impediu que um modelo com overfitting léxico passasse para produção.

$$\textbf{Gate Oficial Emitido: BLIND\_SEMANTIC\_REVALIDATION\_BLOCKED}$$
$$\textbf{Ressalva Metodológica Mantida: REFERENCE\_INDEPENDENCE\_UNRESOLVED}$$

---

## 7. Próximos Passos Autorizados

Conforme o fluxo canônico de engenharia do projeto:

$$\text{Stage 31.7.28 (BLOCKED)} \longrightarrow \text{Stage 31.7.29 (Root Cause Analysis & Domain Disjunction Generalization — Cycle 6)}$$

1. **Stage 31.7.29 — Root Cause Analysis & Domain Disjunction Generalization Architecture (Cycle 6):**
   - Investigar a causa estrutural da dependência de regexes nominais no `SemanticDomainDisjunctionEngine`.
   - Projetar um mecanismo ontológico verdadeiramente invariante à expansão de vocabulário para disjunção de domínio (análise de pertinência ontológica baseada em papéis semânticos e categorias gramaticais de substantivos técnicos vs cotidianos).
   - Corrigir a rota de agregação de `RELATED` para impedir o rebaixamento de metadados institucionais legítimos para `OFF_TOPIC`.
   - Manter o runtime rigorosamente congelado durante todo o RCA do Stage 31.7.29.
