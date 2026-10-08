# Stage 31.7.6 — Post-Generalization Blind Human vs System Revalidation

**Status:** Concluído (Bloqueado por Critério Metodológico)  
**Data:** 2026-10-08  
**Gate:** `POST_GENERALIZATION_BLIND_REVALIDATION_BLOCKED`  
**Referência Metodológica:** `AGENTS.md`, `SECOND_BRAIN.md`, `GEMINI_GUARDRAILS.md`, `GEMINI_HANDOFF.md`, Stage 31.7.4, Stage 31.7.5  

---

## 1. Status

```text
GATE: POST_GENERALIZATION_BLIND_REVALIDATION_BLOCKED
```

A primeira revalidação cega independente pós-generalização (Stage 31.7.6) foi executada sobre o runtime estritamente congelado (`reference_runtime/runtime.py`). Em estrita observância às regras metodológicas do projeto (`AGENTS.md`, Seções 1, 2, 3, 16, 17, 18 e 25):

1. **O runtime permaneceu 100% congelado**: Nenhuma linha de código, rubrica, heurística, lista ou função foi alterada durante o processo de teste. O hash SHA-256 de entrada (`A0CFE48B933F587459BFF6AAF8B2BECABA5B7C00C4C87E7B5DDB6BDE985E46A6`) foi verificado antes e após a execução, confirmando invariância absoluta.
2. **Blindness Firewall preservado**: O conjunto de 250 casos de teste independentes foi executado de forma cega. O runtime recebeu unicamente `{ "text": q }` e `{ "reconstructed_text": r }`, sem acesso a avaliações humanas, oracles, históricos ou expectativas de score. As saídas brutas foram persistidas antes de qualquer comparação.
3. **Propriedades formais validadas**:
   - **Determinismo**: 100% idêntico entre execuções repetidas (Run A vs Run B byte-a-byte).
   - **Isolamento**: 100% idêntico sob permutação de ordem (execução sequencial vs reversa).
   - **Catalog Leakage**: Invariância comprovada (0 divergências ao esvaziar `_FUNCTIONAL_CAPABILITIES`).
4. **Resultado da Revalidação Cega**:
   - Total de Casos Avaliados: **250**
   - Casos com Concordância Exata: **143 (57.20%)**
   - Casos com Divergência: **107 (42.80%)**
   - **Falsos DIRECTs (Relevância Indevida)**: **21 casos**
   - **Falsos OFF_TOPICs (Rejeição Indevida)**: **79 casos** (incluindo 54 respostas que respondiam diretamente à pergunta e foram descartadas como `disjunct_open_domain`).
   - **Subconjunto Secreto sem Overlap Lexical (Grupo C)**: **Apenas 4/20 de acerto (20.0%)**, com 16 falhas sistemáticas.
   - **Representation Invariance (Grupo H)**: Embora 18/20 pares tenham mantido estabilidade de categoria, 2 pares falharam severamente por viés de jargão (explicações corretas em português coloquial foram rejeitadas como `OFF_TOPIC`, enquanto suas versões formais com jargão passaram como `DIRECT`).

Seguindo a regra suprema de que **"uma divergência bem identificada é superior a uma aprovação artificial"** e **"metodologia defensável é mais importante do que score"**, o gate é declarado **`POST_GENERALIZATION_BLIND_REVALIDATION_BLOCKED`**. Nenhuma tentativa de contornar ou mascarar as falhas foi realizada.

---

## 2. Gate

```text
GATE: POST_GENERALIZATION_BLIND_REVALIDATION_BLOCKED
```

**Motivo do Bloqueio:**  
A suíte cega independente revelou que a arquitetura implementada no Stage 31.7.5 **não generalizou autonomamente**. O fallback de domínio aberto (`Step 11` em `runtime.py`) depende criticamente de compartilhamento literal de tokens/stems (`shared_stems or shared`). Quando uma relação problema $\to$ mecanismo não compartilha palavras nem recai sobre um dos contextos previamente mapeados no código, o sistema descarta a resposta como `OFF_TOPIC` (`disjunct_open_domain`). Além disso, ancoragem em entidades e verbos declarativos não mapeados continuam produzindo falsos `DIRECT`.

---

## 3. Runtime Hash

Em cumprimento estrito à Seção 1 do mandato:

| Momento | Algoritmo | Hash SHA-256 | Status de Integridade |
| :--- | :---: | :--- | :---: |
| **Entrada (Stage 31.7.5)** | SHA-256 | `A0CFE48B933F587459BFF6AAF8B2BECABA5B7C00C4C87E7B5DDB6BDE985E46A6` | Base Registrada |
| **Pré-Execução Blind** | SHA-256 | `A0CFE48B933F587459BFF6AAF8B2BECABA5B7C00C4C87E7B5DDB6BDE985E46A6` | Verificado |
| **Pós-Execução Blind** | SHA-256 | `A0CFE48B933F587459BFF6AAF8B2BECABA5B7C00C4C87E7B5DDB6BDE985E46A6` | 100% Inalterado |

---

## 4. Blindness Firewall Verification

O processo de teste foi blindado de ponta a ponta:
1. **Separação de Arquivos**: O benchmark foi gerado em `stage_31_7_6_benchmark_raw.json` e fisicamente bipartido em:
   - `stage_31_7_6_blind_cases.json`: Contendo exclusivamente `id`, `group`, `question` e `response`.
   - `stage_31_7_6_human_results.json`: Contendo `human_relation`, `human_epistemic`, `rationale` e `confidence`.
2. **Execução Cega**: O script executor importou o runtime e alimentou unicamente os pares brutos de texto.
3. **Persistência Prévia**: Os resultados do sistema foram gravados em `stage_31_7_6_system_results.json` antes do carregamento dos oracles humanos.
4. **Comparação Posterior**: O módulo de auditoria carregou os dois arquivos independentes e gerou a matriz de confusão e relatório de divergências.

---

## 5. Formal System Properties Verification

Antes da análise semântica, foram auditadas as propriedades de sistema exigidas nas Seções 13, 16 e 17:

| Propriedade | Metodologia de Teste | Resultado | Status |
| :--- | :--- | :---: | :---: |
| **Determinismo** | Execução repetida do conjunto completo (Run A vs Run B) com comparação estrita de JSON | 250/250 idênticos | **PASS** |
| **Isolamento** | Execução com reversão completa da ordem dos casos (Run Invertida vs Run Sequencial) | 250/250 idênticos | **PASS** |
| **Catalog Independence** | Execução em Estado A (catálogo padrão) vs Estado B (`_FUNCTIONAL_CAPABILITIES.clear()`) | 0 diferenças | **PASS** |

> **Nota sobre o Catalog Leakage Test**: O teste confirmou que o dicionário global `_FUNCTIONAL_CAPABILITIES` não interfere mais na classificação do runtime. A dependência agora reside diretamente na lógica procedimental interna de `_decoupled_evaluate_semantic_relevance`.

---

## 6. Composição do Benchmark Independente (250 Casos)

O conjunto de teste foi construído do zero, sem reaproveitar perguntas ou respostas das suítes de desenvolvimento do Stage 31.7.5:

| Grupo | Descrição | Casos | Foco Metodológico |
| :--- | :--- | :---: | :--- |
| **Grupo A** | Tecnologias Inéditas | 20 | Tecnologias fora de qualquer catálogo prévio (Dragonfly, ClickHouse, TiKV, Cilium, Tempo, Zig, Axum, Kong, etc.) |
| **Grupo B** | Conceitos sem Tecnologia | 20 | Mecanismos de engenharia de software pura sem menção a produtos (2PC, WAL, Consistent Hashing, Bloom Filter, Saga, etc.) |
| **Grupo C** | Problema $\to$ Mecanismo sem Overlap Lexical | 20 | **Subconjunto Secreto**: A pergunta descreve uma falha ou sintoma; a resposta articula a solução técnica sem repetir termos da pergunta |
| **Grupo D** | Entity Anchor Traps | 20 | A entidade da pergunta aparece na resposta, mas a resposta varia entre DIRECT, RELATED (declaração/trivia) e OFF_TOPIC |
| **Grupo E** | Supporting vs Related | 20 | Pares com vocabulário semelhante, distinguindo contribuição funcional causal (`SUPPORTING`) de adjacência passiva (`RELATED`) |
| **Grupo F** | Multi-Aspect Demands | 20 | Perguntas com 2 ou 3 demandas explícitas avaliando cobertura total (`DIRECT`), parcial (`PARTIAL`) ou nula |
| **Grupo G** | Epistemologia & Experiência | 20 | Separação entre declaração de experiência, evidência demonstrada, hipótese, conceitual e incerteza |
| **Grupo H** | Representation Invariance | 40 (20 pares) | Mesma proposição técnica expressa de forma formal vs coloquial, curta vs longa, com jargão vs sem jargão |
| **Grupo I** | Generic Token Traps | 20 | Termos polissêmicos genéricos ("transação", "cluster", "endpoint", "thread", "serviço") usados em contextos cruzados |
| **Grupo J** | Valid Adjacent Mechanisms | 20 | Mecanismos adjacentes válidos que auxiliam causalmente o objetivo da pergunta |
| **Grupo K** | UNKNOWN / INSUFFICIENT | 15 | Respostas vazias, truncadas, fillers ("claro, com certeza"), ecos do entrevistador e ignorância admitida |
| **Grupo L** | Testes de Mutação Independente | 15 | Mutações semânticas (inversão de causalidade, descaracterização de mecanismos, alien domain) para testar sensibilidade |

---

## 7. Resultados Gerais da Revalidação

### 7.1 Métricas Globais

```text
Total de Casos Avaliados: 250
Total de Concordâncias Exatas: 143 (57.20%)
Total de Divergências: 107 (42.80%)

Falsos DIRECTs (Falso Positivo de Relevância): 21 casos
Falsos OFF_TOPICs (Falso Negativo de Relevância): 79 casos
Falsos PARTIALs: 2 casos
```

### 7.2 Matriz de Confusão Completa (Humano vs Sistema)

| Humano \ Sistema | DIRECT | SUPPORTING | RELATED | OFF_TOPIC | PARTIAL | INSUFFICIENT | UNKNOWN | Total Humano |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **DIRECT** | **73** | 1 | 2 | **54** | 2 | 0 | 0 | **132** |
| **SUPPORTING** | 5 | **10** | 0 | **12** | 0 | 0 | 0 | **27** |
| **RELATED** | 9 | 0 | **15** | **10** | 0 | 0 | 0 | **34** |
| **OFF_TOPIC** | 5 | 0 | 0 | **20** | 0 | 0 | 0 | **25** |
| **PARTIAL** | 1 | 0 | 0 | 1 | **11** | 0 | 0 | **13** |
| **INSUFFICIENT** | 1 | 0 | 0 | 3 | 0 | **12** | 0 | **16** |
| **UNKNOWN** | 0 | 0 | 0 | 1 | 0 | 0 | **2** | **3** |
| **Total Sistema** | **94** | **11** | **17** | **101** | **13** | **12** | **2** | **250** |

---

## 8. Desempenho por Grupo de Validação

| Grupo | Descrição | Casos | Acertos | Divergências | Taxa de Concordância |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **A** | Tecnologias Inéditas | 20 | 10 | 10 | **50.0%** |
| **B** | Conceitos sem Tecnologia | 20 | 11 | 9 | **55.0%** |
| **C** | Problema $\to$ Mecanismo (Zero Overlap Lexical) | 20 | 4 | 16 | **20.0%** (Falha Crítica) |
| **D** | Entity Anchor Traps | 20 | 12 | 8 | **60.0%** |
| **E** | Supporting vs Related | 20 | 13 | 7 | **65.0%** |
| **F** | Multi-Aspect Demands | 20 | 15 | 5 | **75.0%** |
| **G** | Epistemologia & Experiência | 20 | 9 | 11 | **45.0%** |
| **H** | Representation Invariance (Casos Individuais) | 40 | 24 | 16 | **60.0%** |
| **I** | Generic Token Traps | 20 | 12 | 8 | **60.0%** |
| **J** | Valid Adjacent Mechanisms | 20 | 10 | 10 | **50.0%** |
| **K** | UNKNOWN / INSUFFICIENT | 15 | 12 | 3 | **80.0%** |
| **L** | Testes de Mutação Independente | 15 | 11 | 4 | **73.3%** |

---

## 9. Análise do Subconjunto Secreto e Testes Especiais

### 9.1 Subconjunto Secreto sem Overlap Lexical (Grupo C)
- **Total de Casos:** 20
- **Concordâncias:** 4 (20.0%)
- **Divergências:** 16 (80.0%)
- **Diagnóstico:** Quando uma pergunta descreve um problema técnico real (e.g. `C01_latency_tail_spikes`: "Nossa API apresenta picos repentinos de latência no percentil 99...") e a resposta apresenta o mecanismo exato (e.g. "Implementamos hedge requests disparando chamadas concorrentes duplicadas..."), o sistema avalia como `OFF_TOPIC` (`disjunct_open_domain`). Como não há sobreposição de palavras entre a pergunta e a resposta e o tópico não é um dos contextos pré-codificados em `runtime.py`, o motor falha completamente em identificar a pertinência causal.

### 9.2 Invariância de Representação (Grupo H)
- **Pares Avaliados:** 20 pares (40 formulações)
- **Pares Estáveis:** 18 pares (90.0%)
- **Pares com Quebra de Invariância:** 2 pares (10.0%)
  - **Par H01 (OCC)**:
    - *Formal* (`H01_occ_formal`): "Aplicando controle de concorrência otimista com checagem atômica do contador de versão no momento do commit." $\to$ **`DIRECT`**
    - *Coloquial* (`H02_occ_colloquial`): "Coloco uma coluna de versão lá na tabela e na hora de salvar confiro se ninguém mudou a versão antes de mim." $\to$ **`OFF_TOPIC`**
  - **Par H15 (Saga Pattern)**:
    - *Formal* (`H29_saga_formal`): "Adotando padrão Saga com transações locais encadeadas e ações de compensação em caso de rollback." $\to$ **`DIRECT`**
    - *Linguagem Simples* (`H30_saga_plain`): "Fazemos cada serviço rodar sua parte e se algum der ruim a gente dispara operações de estorno pra desfazer o que já fez." $\to$ **`OFF_TOPIC`**
- **Diagnóstico:** O sistema exibe um forte **viés de jargão**. Explicações legítimas em linguagem natural são penalizadas e descartadas como irrelevantes se não utilizarem o léxico acadêmico/formal esperado pelas regras internas.

---

## 10. Classificação e Análise Detalhada das Divergências (D1 a D10)

As 107 divergências foram categorizadas conforme a taxonomia da Seção 19:

```text
D1 — Semantic false positive:           10 casos
D2 — Semantic false negative:           60 casos (Causa Raiz Dominante)
D3 — Entity-anchor error:                8 casos
D4 — Lexical dependency:                 8 casos
D5 — Multi-aspect error:                 5 casos
D6 — Supporting/Related confusion:       0 casos
D7 — Epistemic confusion:               11 casos
D8 — Representation invariance failure:  2 pares (4 casos em H)
D9 — UNKNOWN misuse:                     3 casos
D10 — Other (Mutações):                  2 casos
```

### Detalhamento das Classes Principais:

#### Classe D2: Falso Negativo Semântico (60 casos)
- **Ocorrência:** 54 respostas que respondem diretamente à pergunta (`DIRECT`) e 6 respostas complementares (`SUPPORTING`/`PARTIAL`) foram classificadas pelo sistema como `OFF_TOPIC`.
- **Exemplo Real:**
  - *Pergunta:* "Como o Dragonfly escala operações em memória comparado ao Redis tradicional?" (`A01_dragonfly`)
  - *Resposta:* "Utiliza arquitetura multi-threaded moderna sobre a biblioteca Seastar dividindo dados por cores sem lock global."
  - *Classificação Humana:* `DIRECT` (Articula exatamente a arquitetura multi-threaded core-per-thread do Dragonfly).
  - *Classificação do Sistema:* `OFF_TOPIC` (Rationale: "Response does not demonstrate technical propositions addressing the question demand.").
- **Mecanismo da Falha:** O motor não possui representação semântica abstrata para "Dragonfly" nem "Seastar". Como não encontrou palavras compartilhadas nem padrões das mini-whitelists, desceu até a cláusula final de escape e rotulou como `disjunct_open_domain`.

#### Classe D1 e D3: Falso Positivo Semântico e Erro de Ancoragem em Entidade (18 casos)
- **Ocorrência:** Respostas que apenas mencionam a entidade ou dão declarações genéricas de uso diário foram promovidas a `DIRECT`.
- **Exemplo Real:**
  - *Pergunta:* "Como o Docker impede que um contêiner monopolize a memória RAM da máquina hospedeira?" (`D09_docker_declarative`)
  - *Resposta:* "Uso Docker diariamente no meu ambiente de desenvolvimento para rodar imagens."
  - *Classificação Humana:* `RELATED` (Menciona uso cotidiano sem articular limites de memória ou cgroups).
  - *Classificação do Sistema:* `DIRECT` (Rationale: "Demonstrates technical assertion aligning with question subject: dock.").
- **Mecanismo da Falha:** O stem `dock` casou no Step 11 (`shared_stems`). Como o verbo conjugado `"Uso "` não estava na lista fixa `has_decl_marker` (que continha apenas `"usei "`, `"já usei"`, `"trabalhei "`), o sistema considerou a sentença como uma asserção técnica válida e atribuiu `DIRECT`.

#### Classe D7: Confusão Epistêmica (11 casos)
- **Ocorrência:** Respostas declarativas puras em tópicos sem tecnologia explícita foram avaliadas pelo sistema como `OFF_TOPIC` em vez de serem reconhecidas como `RELATED` com status epistêmico de `experience_declaration`.
- **Mecanismo da Falha:** Em vez de dissociar "relevância temática" de "status epistêmico", o motor rejeita a relevância temática quando a resposta não contém verbos de mecanismo.

---

## 11. Análise de Causa Raiz Arquitetural (RCA Preliminar)

A investigação empírica desta revalidação cega demonstra que o **Stage 31.7.5 resolveu os testes com os quais foi co-desenhado, mas não alcançou a Generalização de Intenção Semântica real**.

A arquitetura presente em `reference_runtime/runtime.py` ainda sofre de três vícios estruturais:
1. **Dependência Crítica de Overlap Lexical no Fallback (Step 11)**:
   ```python
   # runtime.py - Linhas 2699-2706
   shared = q_words & r_words
   shared_stems = q_stems & r_stems
   if shared_stems or shared:
       # atribui DIRECT ou RELATED
   return {"classification": "OFF_TOPIC", "relation_type": "disjunct_open_domain"}
   ```
   Se a pergunta não coincide em palavras com a resposta e o tema não é um dos 8 contextos embutidos no código, a resposta é invariavelmente tratada como lixo (`OFF_TOPIC`), destruindo a capacidade de responder relações problema $\to$ mecanismo.
2. **Contextos Rígidos Procedimentais**: Os contextos adicionados no Stage 31.7.5 (OCC, Rate limit, Tracing, Circuit breaker, etc.) agem como regras procedimentais duras. Eles funcionam magnificamente quando as palavras exatas aparecem nos testes, mas falham quando o candidato explica o conceito em suas próprias palavras ou quando a tecnologia é externa àqueles nichos.
3. **Whitelists Morfológicas Incompletas**: Verbos declarativos e marcadores de experiência são verificados por substrings estáticas (`"usei "`, `"trabalhei "`), que quebram diante de variações simples como `"Uso "`, `"Trabalho "` ou `"Atuo "`.

---

## 12. Regressão Histórica

As suítes canônicas do sistema foram reexecutadas com o runtime congelado, garantindo conformidade com o histórico:

| Suíte de Testes | Comando | Resultado | Status |
| :--- | :--- | :---: | :---: |
| **Reference Runtime Tests** | `py run_reference_runtime_tests.py` | 989/989 passaram (`OK (skipped=1)`) | **PASS** |
| **Reference Test Harness** | `py run_reference_harness.py` | 8/8 suites passaram (`0 failed`) | **PASS_WITH_WARNINGS** |

---

## 13. Artefatos Produzidos

Os artefatos completos da validação cega foram gerados e persistidos em:
`11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/`

1. `stage_31_7_6_blind_cases.json`: Conjunto cego de 250 casos executados.
2. `stage_31_7_6_system_results.json`: Saída bruta do runtime congelado.
3. `stage_31_7_6_human_results.json`: Oracles humanos independentes.
4. `stage_31_7_6_comparison.json`: Confronto detalhado caso a caso com matriz de confusão e métricas.
5. `stage_31_7_6_divergences.json`: Relatório estruturado das 107 divergências com rationales humano e do sistema.
6. `Stage 31.7.6 — Post-Generalization Blind Human vs System Revalidation.md`: Este relatório formal.

---

## 14. Conclusão Metodológica e Próximos Passos

O Stage 31.7.6 cumpriu seu propósito com rigor exemplar: **descobriu exatamente onde o runtime ainda é falho, sem modificar código para forçar aprovação artificial**.

O gate está **`BLOCKED`**.

O roadmap metodológico deve agora prosseguir para:
- **Stage 31.7.7 — Root Cause Analysis & Architecture Redesign for Zero-Lexical & Open-Domain Semantic Intent**: Análise profunda da causa-raiz das 107 divergências e modelagem formal de um avaliador semântico de relações causa-efeito que não dependa de sobreposição léxica de stems nem de dicionários procedimentais fechados.
