# Plano de Implementação Controlada do Incremento 1 (INC-1) — Stage 31.7.35

## 1. Objetivo e Escopo Autorizado

Implementar de forma controlada o **Question Profile and Proposition Engine (INC-1)** em `reference_runtime/runtime.py`, fornecendo a representação formal da intenção da pergunta, a decomposição em demandas primárias e secundárias com flags de obrigatoriedade, e a segmentação de proposições da resposta com preservação de negações, condições, preâmbulos e autocorreções.

### 1.1. Limites Semânticos Estritos (O que NÃO é feito no INC-1)
O INC-1 **NÃO** deve:
1. Determinar afinidade temática final (atribuído ao INC-3);
2. Concluir que uma resposta é `OFF_TOPIC` (atribuído ao INC-3/INC-5);
3. Concluir equivalência conceitual aberta ou fechar ontologia (atribuído ao INC-4);
4. Validar analogias computacionais ou verificar aterrissagem em mecanismos (atribuído ao INC-4);
5. Decidir se a resposta satisfaz semanticamente todas as demandas da pergunta (atribuído ao INC-5);
6. Selecionar a classificação final entre as sete classes de relevância (atribuído ao INC-5);
7. Adicionar listas de casos específicos ou palavras proibidas ad-hoc.

O objetivo do INC-1 é **estritamente representacional e estruturante**: transformar perguntas e respostas em modelos estruturados (`QuestionProfile` e `DiscourseProfile`) auditáveis, preservando todas as distinções epistemológicas e operatórias necessárias para os incrementos semânticos subsequentes.

---

## 2. Componentes Arquiteturais a Implementar

### 2.1. `SemanticQuestionProfiler`
- **Responsabilidade**: Mapeamento de `raw_question: str` em `(QuestionProfile, EpistemicUncertaintyRecord)`.
- **Classificação de Intenção**: Identifica os 11 modos de intenção canônicos (`DEFINITION`, `CONCEPTUAL_EXPLANATION`, `MECHANISM`, `COMPARISON`, `HISTORICAL`, `CAUSALITY`, `DIAGNOSIS`, `IMPLEMENTATION`, `PROBLEM_SOLUTION`, `DECISION_JUSTIFICATION`, `TRADE_OFF_ANALYSIS`).
- **Decomposição de Demandas**: Separa perguntas compostas em Demanda Primária ($D_p$) e Demandas Secundárias ($D_s$), atribuindo identificadores (`demand_1`, `demand_2`) e marcadores de obrigatoriedade (`is_mandatory = True`).
- **Extração de Entidades e Qualificadores**: Identifica entidades alvo da computação e qualificadores contextuais restritivos (ex.: alta concorrência, consistência estrita, produção).
- **Registro de Incerteza Epistêmica**: Se a pergunta for sintética em excesso (≤ 2 palavras) ou ambígua, registra incerteza e limitações em `EpistemicUncertaintyRecord`.

### 2.2. `DiscoursePropositionEngine`
- **Responsabilidade**: Mapeamento de `raw_response: str` em `DiscourseProfile`.
- **Isolamento de Preâmbulos Fáticos (`isolated_preambles`)**: Detecta e isola preâmbulos conversacionais irrelevantes (anedotas de trânsito, saudações, agradecimentos, histórias pessoais) sem poluir o núcleo técnico.
- **Decomposição Proposicional Atômica**: Divide a resposta técnica em proposições atômicas (`DiscourseProposition`).
- **Papel Discursivo (`discourse_role`)**: Classifica cada proposição em `TECHNICAL_CORE`, `HISTORICAL_METADATA`, `OBSERVABILITY_SUPPORT`, `IGNORANCE_DECLARATION`, `EMPTY_FILLER`, `RETRACTED_ASSERTION`.
- **Preservação de Negações**: Identifica operadores de negação explícita e extrai o escopo da negação (`is_negated: bool`, `negation_scope: str`).
- **Preservação de Condicionais**: Identifica operadores condicionais e extrai a premissa condicional (`is_conditional: bool`, `condition_premise: str`).
- **Resolução de Autocorreção / Retratação (`SC-21`)**: Detecta marcadores de autocorreção ("na verdade não", "ou melhor", "quis dizer") e marca a proposição anterior contraditória como `RETRACTED_ASSERTION`.

---

## 3. Mapeamento Contratual Formal

| Identificador do Contrato | Descrição do Comportamento | Componente Responsável |
|---|---|---|
| `SC-01` | Identificação explícita de modo de intenção epistemológica | `SemanticQuestionProfiler` |
| `SC-02` | Decomposição aberta de demandas primárias e secundárias com obrigatoriedade | `SemanticQuestionProfiler` |
| `SC-05` | Suporte a perguntas comparativas (A vs B) decompondo ambas entidades | `SemanticQuestionProfiler` |
| `SC-06` | Identificação de qualificadores de restrição e contexto da pergunta | `SemanticQuestionProfiler` |
| `SC-17` | Isolamento de preâmbulos fáticos conversacionais no topo da resposta | `DiscoursePropositionEngine` |
| `SC-18` | Detecção e preservação de escopo de negações em proposições | `DiscoursePropositionEngine` |
| `SC-20` | Detecção e preservação de operadores e premissas condicionais | `DiscoursePropositionEngine` |
| `SC-21` | Detecção de autocorreções explícitas marcando asserção anterior como retratada | `DiscoursePropositionEngine` |
| `ADV-05` | Invariância estrutural da análise técnica na presença de preâmbulos fáticos | `DiscoursePropositionEngine` |
| `ADV-06` | Perguntas compostas com múltiplas demandas conjuntas obrigatórias | `SemanticQuestionProfiler` |
| `ADV-11` | Preservação de negações preventivas (ex.: "não usamos lock pessimista") | `DiscoursePropositionEngine` |
| `ADV-12` | Condicionais sob escopos distintos delimitando o campo de aplicação | `DiscoursePropositionEngine` |

---

## 4. Salvaguardas e Protocolo de Modificação

1. **Snapshot de Baseline**: `runtime.py.stage_31_7_35_entry` criado e conferido com hash idêntico ao pós-INC-0.
2. **Edição Não-Destrutiva**: Os novos componentes serão adicionados em `reference_runtime/runtime.py` sem alterar a assinatura de funções públicas existentes nem quebrar os branches do pipeline atual.
3. **Regressão Canônica Completa**: Execução dos 1.084 testes canônicos e dos 15 testes do Reference Harness.
4. **Critério de Aborto**: Qualquer falha na suíte canônica interrompe o estágio imediatamente e dispara o rollback automático.
