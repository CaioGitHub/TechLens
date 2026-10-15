---
type: architecture
status: study
confidence: 95
created: 2026-10-14
updated: 2026-10-14
tags:
  - stage-31-7-22
  - architecture-options
  - rca
  - semantic-relevance
  - open-domain-evaluation
---

# Stage 31.7.22 — Análise Comparativa de Alternativas Arquiteturais (Cycle 4)

## 1. Contexto e Motivação

A validação cega independente realizada no **Stage 31.7.21** demonstrou que o runtime congelado (`reference_runtime/runtime.py`), embora operacionalmente estável (100% de aprovação na suíte canônica de 1.038 testes e 15 testes de Harness), falhou em 6 dos 7 critérios semânticos de referência quando confrontado com 250 casos inéditos de domínio aberto.

A análise minuciosa das 80 divergências catalogadas em `stage_31_7_22_root_cause_catalog.json` comprovou que o motor `OpenDomainPropositionEngine` sofre de limitações estruturais decorrentes de:
1. **Acoplamento Monolítico:** Regras de intenção, discurso, morfologia e avaliação de nexo misturadas no mesmo fluxo procedimental.
2. **Escadas Heurísticas de Casamento Léxico Estático:** Listas fixas de palavras-chave ("revogação", "coordenador", "vazão de escrita") que falham diante de novas formulações e criam falsos nexos causais.
3. **Ausência de Desacoplamento Proposição-Demanda:** Uma única proposição da resposta satisfazendo simultaneamente múltiplas demandas primárias distintas.
4. **Fragilidade Morfológica:** Detectores de tautologia e declaração de experiência que falham diante de flexões verbais e nominalizações comuns da língua portuguesa (ex: "compressão" vs. "comprimindo", "usei" vs. "utilizo").
5. **Mapeamento Ontológico Inconsistente:** Respostas evasivas mapeadas para `UNKNOWN` em vez de `INSUFFICIENT`.

Para superar definitivamente esse ciclo recorrente de remediações parciais, este documento compara três alternativas arquiteturais materialmente distintas.

---

## 2. Comparativo das Alternativas Arquiteturais

### Alternativa 1: Expansão Heurística e Endurecimento Léxico Incremental
- **Conceito:** Manter a estrutura monolítica atual de `OpenDomainPropositionEngine` em `runtime.py`, adicionando mais radicais a `self.operative_verbs`, mais marcadores a `self.trivia_markers`, novas tuplas em `_detect_structural_circularity` e mais conectivos conjuntivos em `decompose_question`.
- **Mecanismo:** Ajustes pontuais baseados nas 80 divergências observadas no Stage 31.7.21.

### Alternativa 2: Grafo Proposicional Decomposto com Contratos Semânticos Estritos (Recomendada)
- **Conceito:** Refatorar o motor em um pipeline modular de 5 componentes especializados e desacoplados, com contratos de dados imutáveis (dataclasses tipadas) e uma única fonte de verdade para cada decisão semântica.
- **Componentes:**
  1. `SemanticIntentAndDemandExtractor`: Decomposição profunda de demandas multi-aspecto, detectando transições de estado (fechado/aberto/meio-aberto), ações coordenadas ("coordena X e compensa Y") e dependências causais mesmo em orações simples.
  2. `PropositionDiscourseFilter`: Classificação preliminar do tipo de discurso (autobiográfico, trivia histórica/hardware, telemetria/auxiliar, antítese destrutiva ou proposição funcional operativa) ANTES de avaliar a operatividade técnica.
  3. `MorphologicalCircularityAnalyzer`: Analisador morfológico baseado em lematização e grafos de cognatas para medir o ganho informacional real da resposta em relação à pergunta, imune a variações entre verbo e substantivo.
  4. `DemandPropositionNexusBipartiteMatcher`: Mecanismo de emparelhamento bipartido que exige que cada demanda primária independente seja satisfeita por uma evidência proposicional distinta ou comprovadamente unificada, impedindo a sobre-promoção de respostas parciais.
  5. `StrictOntologyRelevanceAggregator`: Agregador determinístico que traduz a matriz de cobertura e o status epistêmico nas 7 classes canônicas, garantindo que respostas evasivas sejam sempre `INSUFFICIENT` e tautologias puras sejam `UNKNOWN`.

### Alternativa 3: Modelo Neural de Embeddings Densos / Cross-Encoder
- **Conceito:** Substituir a análise léxico-sintática determinística por um modelo pré-treinado de representação vetorial densa (ex: BERTimbau / sentence-transformers) para calcular a similaridade semântica entre demandas e respostas via produto escalar ou classificação supervisionada.
- **Mecanismo:** Inferência de rede neural profunda local.

---

## 3. Matriz Comparativa Multidimensional

| Critério de Avaliação | Alternativa 1: Expansão Heurística | Alternativa 2: Grafo Decomposto (Recomendada) | Alternativa 3: Embeddings Neurais |
|---|:---:|:---:|:---:|
| **Capacidade de Resolver CR-01 a CR-08** | **BAIXA** (Trata sintomas, não causas) | **ALTA** (Resolve causas estruturais) | **MÉDIA** (Opaca em demandas multi-aspecto) |
| **Determinismo e Reprodutibilidade** | **100% Determinístico** | **100% Determinístico** | **Risco de Variação de Ponto Flutuante** |
| **Auditabilidade e Explicabilidade Causal** | **MÉDIA** (Difícil rastrear conflitos) | **ALTA** (Trilha completa e unívoca) | **NULA** (Caixa-preta, pesos latentes) |
| **Independência de Catálogos Fechados** | **PÉSSIMA** (Proliferação de listas) | **ALTA** (Contratos estruturais e lemas) | **ALTA** (Generalização estatística) |
| **Conformidade com Guardrails do Projeto** | **BAIXA** (Risco severo de overfitting) | **TOTAL** (Preserva auditabilidade) | **VIOLAÇÃO** (Opacidade metodológica) |
| **Custo de Implementação** | Baixo | Moderado / Alto | Alto (Dependências pesadas) |
| **Risco de Regressão Canônica** | Alto (Efeito colateral em testes existentes) | Baixo (Isolamento por interfaces) | Crítico (Ambiente e performance) |
| **Facilidade de Validação Independente** | Baixa | Alta | Baixa |

---

## 4. Análise Crítica e Justificativa da Decisão

### Por que a Alternativa 1 é Rejeitada?
A Alternativa 1 repete exatamente a falha metodológica dos ciclos anteriores: tentar consertar um problema de representação semântica adicionando mais palavras e expressões a listas estáticas. O Stage 31.7.21 provou categoricamente que esse caminho é insustentável. Sempre que um candidato utilizar um verbo legítimo não previsto ou uma construção pronominal ligeiramente distinta, o motor falhará. Essa abordagem viola a Seção 19 de `AGENTS.md` (Regra contra overfitting).

### Por que a Alternativa 3 é Rejeitada?
A Alternativa 3 introduz dependências complexas (PyTorch, transformers, modelos de centenas de megabytes) e, mais gravemente, **destrói a auditabilidade causal** do sistema de avaliação. Conforme estipulado no princípio norteador de `SECOND_BRAIN.md`:
> *"Não estamos construindo um sistema que parece inteligente. Estamos construindo um sistema cuja avaliação pode ser investigada, reproduzida, contestada e corrigida."*
Um score de similaridade de cosseno de `0.78` não explica *qual* aspecto de uma saga orquestrada o candidato deixou de responder, nem permite ao candidato contestar a evidência extraída.

### Por que a Alternativa 2 é a Escolha Arquitetural Superior?
A Alternativa 2 ataca a causa-raiz formal do problema sem abrir mão do determinismo nem da explicabilidade. Ao decompor o pipeline em componentes com responsabilidade única:
1. Elimina a escada de `if/elif` que confundia palavras isoladas (como "coordenador") com a solução de falhas complexas.
2. Impede que relatos autobiográficos ("já usei em produção") ou triviais ("escrito por Sysoev") sejam promovidos a soluções técnicas apenas por conterem verbos ativos.
3. Fornece uma trilha de auditoria completa: para cada demanda, registra-se explicitamente qual proposição a satisfez, por que a satisfez e qual o grau de cobertura obtido.
4. Preserva integralmente o isolamento e a compatibilidade com o Reference Harness e os 1.038 testes unitários existentes.

---

## 5. Decisão Formal

**Arquitetura Aprovada para Especificação no Stage 31.7.22:**
> **Alternativa 2 — Grafo Proposicional Decomposto com Contratos Semânticos Estritos**

A especificação formal dos contratos de cada um dos 5 componentes é detalhada em `stage_31_7_22_component_contracts.md`.
