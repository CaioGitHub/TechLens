# GEMINI HANDOFF — Guia de Continuidade do Projeto

> Documento de continuidade para agentes de IA que assumirem o desenvolvimento do Second Brain e do sistema de avaliação técnica de entrevistas.
>
> **Objetivo:** preservar o caminho arquitetural, metodológico e experimental já construído, evitando regressões, atalhos, mudanças arbitrárias de metodologia ou reinterpretações do projeto.

---

# 1. REGRA MAIS IMPORTANTE

Este projeto **não deve ser tratado como um projeto novo**.

Existe uma arquitetura, metodologia, sequência de validações e conjunto de decisões já estabelecidos.

Antes de implementar qualquer mudança:

1. Ler `AGENTS.md`.
2. Ler `SECOND_BRAIN.md`.
3. Ler este documento.
4. Ler `GEMINI_GUARDRAILS.md`.
5. Inspecionar os artefatos e testes existentes.
6. Identificar o stage atual.
7. Identificar o último gate obtido.
8. Identificar bloqueios existentes.
9. Somente então propor ou implementar mudanças.

Não assumir que uma melhoria conceitualmente interessante deve ser implementada.

A pergunta principal deve ser:

> "Qual é o próximo passo previsto pelo processo existente?"

e não:

> "Como eu redesenharia este sistema?"

---

# 2. OBJETIVO ORIGINAL

O projeto nasceu como um Second Brain técnico em Obsidian.

Objetivo:

> Encontrar rapidamente aquilo que já sei e descobrir aquilo que ainda preciso aprender.

O sistema evoluiu para incluir uma camada de avaliação de entrevistas técnicas.

Essa camada deve ser:

* baseada em evidências;
* rastreável;
* conservadora;
* reproduzível;
* auditável;
* independente de currículo;
* independente de senioridade declarada;
* independente de eloquência;
* independente de tamanho da resposta;
* independente de decisão de contratação.

---

# 3. ARQUITETURA CONCEITUAL

Fluxo principal:

```text
Raw Transcript
      ↓
Participant Identification
      ↓
Speaker Attribution
      ↓
Question Extraction
      ↓
Response Extraction
      ↓
Reconstruction & Normalization
      ↓
Question/Response Linking
      ↓
Validation
      ↓
Evidence Model
      ↓
Scoring Rubric
      ↓
Evaluation Engine
      ↓
Global Evaluation Audit
      ↓
Interview Evaluation Materialization
      ↓
Pipeline
      ↓
End-to-End Validation
      ↓
Reference Runtime / Harness
      ↓
Synthetic Validation
      ↓
Semantic Calibration
      ↓
Adversarial Validation
      ↓
Real Interview Pilot
      ↓
Human Review
      ↓
Human vs System Validation
      ↓
Failure Analysis
      ↓
Controlled Correction
      ↓
Blind Post-Correction Validation
      ↓
Semantic Relevance & Invariance Remediation
      ↓
Human vs System Revalidation
      ↓
Production Readiness
```

Esse fluxo é deliberado.

Não remover etapas apenas porque parecem redundantes.

---

# 4. PRINCÍPIOS FUNDAMENTAIS

## 4.1 Evidência > impressão

O sistema avalia aquilo que foi demonstrado.

Não avaliar:

* currículo;
* cargo;
* senioridade declarada;
* anos de experiência isoladamente;
* empresa;
* eloquência;
* confiança;
* tamanho da resposta;
* quantidade de jargões.

---

## 4.2 "Não demonstrou" ≠ "Não conhece"

Se a entrevista não produziu evidência suficiente:

```text
Não demonstrado
```

não deve ser transformado em:

```text
Não conhece
```

---

## 4.3 Conhecimento ≠ aplicação

Separar:

* conhecimento conceitual;
* conhecimento factual;
* implementação;
* aplicação prática;
* troubleshooting;
* raciocínio;
* trade-offs;
* arquitetura;
* integração entre conhecimentos.

---

## 4.4 Experiência declarada ≠ experiência demonstrada

Exemplo:

```text
"Trabalhei 3 anos com Kubernetes."
```

é declaração.

Isso não é equivalente a:

```text
Explica uma situação concreta de Kubernetes,
justifica decisões,
descreve troubleshooting
e explica trade-offs.
```

A segunda situação fornece evidência de experiência demonstrada.

---

## 4.5 Pergunta difícil ≠ nota menor

Complexidade não deve ser confundida automaticamente com qualidade da resposta.

---

## 4.6 Resposta longa ≠ resposta melhor

O sistema deve ser invariável a:

* verbosity;
* estilo;
* fluência;
* tamanho;
* formalidade.

---

## 4.7 Resposta tecnicamente correta ≠ resposta adequada à pergunta

Esta é uma das decisões mais importantes após os stages 31.x.

Exemplo:

```text
Pergunta:
Como funciona REST?

Resposta:
Kafka permite processamento assíncrono...
```

A informação sobre Kafka pode ser tecnicamente correta.

Mas isso não significa que a resposta responda à pergunta.

Portanto:

```text
conteúdo tecnicamente válido
≠
resposta semanticamente adequada
```

---

# 5. STAGES JÁ REALIZADOS

## Stage 11 — Fundamentos da Avaliação

Estabeleceu os princípios fundamentais da avaliação técnica.

Principais decisões:

* evidência como base;
* avaliação individual por pergunta;
* separação entre conhecimento e avaliação;
* ausência de resposta não implica desconhecimento;
* avaliação técnica separada de contratação.

Status:

```text
CONCLUÍDO
```

---

# 6. Stage 12 — Taxonomia das Perguntas

Definiu classificação das perguntas.

Considera diferentes tipos, incluindo:

* conceitual;
* factual;
* implementação;
* arquitetura;
* experiência;
* troubleshooting;
* cenário;
* decisão;
* aplicação.

Status:

```text
CONCLUÍDO
```

---

# 7. Stage 13 — Evidence Model inicial

Estabeleceu a necessidade de avaliar evidências observáveis em vez de respostas por similaridade textual.

Status:

```text
CONCLUÍDO
```

Posteriormente evoluído para o Evidence Model canônico do Stage 21.

---

# 8. Stage 14 — Rubrica 0–10

Estabeleceu a rubrica multidimensional.

Pesos canônicos:

```yaml
correctness: 40
completeness: 20
depth: 15
reasoning: 10
practical_application: 10
trade_offs: 5
```

Dimensões N/A devem ser normalizadas proporcionalmente.

Não existe média mecânica obrigatória.

A avaliação deve considerar julgamento integrado.

Status:

```text
CONCLUÍDO
```

---

# 9. Stage 15 — Evaluation Engine inicial

Definiu o comportamento do motor de avaliação.

Status:

```text
CONCLUÍDO
```

Posteriormente substituído/evoluído pelo Evaluation Engine canônico e Runtime de referência.

---

# 10. Stage 16 — Avaliação da Entrevista

Definiu a consolidação da entrevista inteira.

A média é apenas indicador.

A avaliação global deve considerar:

* distribuição;
* complexidade;
* domínio;
* consistência;
* profundidade;
* aplicação;
* troubleshooting;
* arquitetura;
* integração;
* erros;
* gaps;
* cobertura;
* confiança.

Não produzir automaticamente:

* senioridade;
* contratação;
* ranking;
* aprovação/reprovação.

Status:

```text
CONCLUÍDO
```

---

# 11. Stage 17 — Contexto da Vaga

Separou:

```text
Avaliação técnica
        ≠
Aderência à vaga
        ≠
Decisão de contratação
```

O contexto da vaga não deve contaminar a avaliação técnica individual.

Status:

```text
CONCLUÍDO
```

---

# 12. Stage 18 — Validação

Estabeleceu validação das estruturas e regras.

Status:

```text
CONCLUÍDO
```

---

# 13. Stage 18.1 — Correção dos Achados

Estabeleceu correção controlada de problemas encontrados durante validação.

Status:

```text
CONCLUÍDO
```

---

# 14. Stage 18.2 — Fechamento da Rastreabilidade

Estabeleceu fechamento da cadeia de rastreabilidade.

Status:

```text
CONCLUÍDO
```

---

# 15. Stage 19 — Calibração

Introduziu calibração das avaliações.

Status:

```text
CONCLUÍDO
```

---

# 16. Stage 19.1 — Correção CAL-01

Corrigiu/estabeleceu o caso de calibração CAL-01.

Status:

```text
CONCLUÍDO
```

---

# 17. Stage 20 — Processamento da Transcrição

Criou o pipeline de processamento de entrevista:

```text
RAW TRANSCRIPT
↓
Participants
↓
Speakers
↓
Questions
↓
Responses
↓
Reconstruction
↓
Linking
↓
Validation
```

Regra central:

> Corrigir forma é permitido. Criar conteúdo não é permitido.

Status:

```text
CONCLUÍDO
```

---

# 18. Stage 20.1 — Participant Identification

Responsável por identificar:

* candidato;
* entrevistador;
* coordenador;
* observador;
* desconhecido.

Não confundir:

```text
identificar participante
≠
atribuir fala
≠
interpretar conteúdo
≠
avaliar candidato
```

Status:

```text
CONCLUÍDO
```

---

# 19. Stage 20.2 — Speaker Attribution

Responsável por determinar quem falou cada segmento.

Prioridades:

1. speaker explícito;
2. continuidade;
3. estrutura conversacional;
4. mudança explícita;
5. contexto;
6. inferência limitada.

Regra:

> Atribuir uma fala ao participante errado é pior do que deixá-la como desconhecida.

Status:

```text
CONCLUÍDO
```

---

# 20. Stage 20.3 — Question Extraction

Extrai perguntas sem interpretar aquilo que deveria ter sido perguntado.

Suporta:

* perguntas técnicas;
* experiência;
* cenários;
* follow-ups;
* reformulações;
* perguntas compostas;
* perguntas interrompidas;
* perguntas incompletas;
* perguntas do candidato.

Status:

```text
CONCLUÍDO
```

Correção importante posteriormente feita no Stage 30.1:

Uma pergunta conversacional/tag question como:

```text
"E tem uma Daily também, só nossa, né?"
```

não deve automaticamente virar pergunta técnica avaliável.

---

# 21. Stage 20.4 — Response Extraction

Responsável por identificar as respostas.

Suporta:

* resposta direta;
* resposta em múltiplos segmentos;
* resposta interrompida;
* resposta completada posteriormente;
* hipótese;
* experiência declarada;
* experiência demonstrada;
* incerteza;
* "não sei";
* "não lembro";
* não resposta;
* resposta fora do tópico.

Status:

```text
CONCLUÍDO
```

---

# 22. Stage 20.5 — Reconstruction & Normalization

Permite:

* pontuação;
* capitalização;
* correção de forma;
* normalização técnica óbvia;
* remoção controlada de disfluências.

Não permite:

* adicionar conhecimento;
* completar resposta com informação inexistente;
* corrigir tecnicamente o candidato;
* inventar conteúdo.

Status:

```text
CONCLUÍDO
```

---

# 23. Stage 20.6 — Question/Response Linking

Responsável por:

```text
Q1 → R1
Q5.1 → R6
```

Relações possíveis:

* answer;
* follow_up_answer;
* reformulation;
* clarification;
* continuation;
* unknown.

Não forçar associação quando não existe evidência suficiente.

Status:

```text
CONCLUÍDO
```

---

# 24. Stage 20.7 — Validation

Último gate do processamento da transcrição.

Status possíveis:

```text
READY
READY_WITH_WARNINGS
BLOCKED
```

Não significa qualidade técnica do candidato.

Significa apenas se a estrutura representa a entrevista com confiabilidade suficiente para avaliação.

Status:

```text
CONCLUÍDO
```

---

# 25. Stage 21 — Evidence Model

Criou o Evidence Model canônico.

Principais campos:

```yaml
evidence_id:
type:
qualification:
content:
interpretation:
explicitness:
evidence_strength:
evidence_confidence:
review_reason:
relations:
evidence_set:
```

Tipos incluem:

* conceptual;
* factual;
* architectural;
* implementation;
* practical;
* experience_declaration;
* demonstrated_experience;
* reasoning;
* tradeoff;
* troubleshooting;
* scenario_application;
* self_correction;
* uncertainty;
* contradiction.

Qualificações:

* positive;
* partial;
* negative;
* contradictory;
* absent;
* insufficient.

Status:

```text
CONCLUÍDO
```

---

# 26. Stage 22 — Rubric 0–10

Formalizou a rubrica canônica.

Status:

```text
READY_WITH_WARNINGS
```

Warnings históricos de calibração foram mantidos explicitamente.

Isso não deve ser interpretado como falha do sistema.

---

# 27. Stage 23 — Evaluation Engine

Criou o Evaluation Engine canônico.

Regras:

* Evidence Set é fonte exclusiva de evidência;
* avaliação dimensional antes da global;
* pesos;
* julgamento integrado;
* rastreabilidade;
* sem senioridade;
* sem contratação;
* sem ranking;
* experiência declarada ≠ demonstrada;
* erros críticos proporcionais;
* N/A com normalização;
* invariância de tamanho, eloquência, senioridade e CV.

Status:

```text
READY_WITH_WARNINGS
```

---

# 28. Reference Evaluation Engine Runtime

Foi criado um runtime reproduzível.

Arquivos principais:

```text
reference_runtime/evaluation_engine.py
tests/test_stage_23_evaluation_engine_runtime.py
```

Resultados de referência:

```text
10 avaliações
média: 4.7
mediana: 4.0
mínimo: 2.0
máximo: 8.0
confiança: medium
28 evidências
```

O runtime não utiliza `Interview Evaluation v1.md` como fonte semântica.

Status:

```text
CONCLUÍDO COM WARNINGS
```

---

# 29. Stage 23.1 — Global Evaluation Semantic Audit

Auditoria independente do output do Runtime.

Validou:

* agregação;
* distribuição;
* domínios;
* complexidade;
* dimensões;
* evidências;
* exclusões;
* Q5;
* Q8;
* Q10;
* Q12;
* perguntas do candidato;
* confiança;
* limitações;
* independência histórica;
* mutações.

Resultado:

```text
PASS_WITH_WARNINGS
```

Gate:

```text
GLOBAL_EVALUATION_AUDIT_COMPLETE_WITH_WARNINGS
```

---

# 30. Stage 23.2 — Interview Evaluation v2

Materializou o resultado do Runtime.

Arquivo:

```text
Interview Evaluation v2.md
```

Resultado:

```text
10 avaliações
média 4.7
mediana 4.0
min/max 2.0 / 8.0
28 evidências
confidence: medium
```

Status:

```text
INTERVIEW_EVALUATION_V2_MATERIALIZED_WITH_WARNINGS
```

---

# 31. Stage 24 — Pipeline / Orchestration

Criou o pipeline:

```text
20.7
↓
21
↓
22
↓
23
↓
23.1
↓
23.2
```

Características:

* reutilização dos executores existentes;
* sem duplicação de scoring;
* propagação de warnings;
* BLOCKED interrompe downstream;
* idempotência;
* stale detection;
* reprocessamento;
* rastreabilidade.

Resultado:

```text
READY_WITH_WARNINGS
```

---

# 32. Stage 25 — End-to-End Validation

Validou o fluxo completo.

Resultado:

```text
26/26 testes
362/362 regression
```

Foi encontrada uma race condition no harness durante execução paralela.

Isso não foi ignorado.

O problema foi levado ao Stage 26.

Status:

```text
END_TO_END_VALIDATION_COMPLETE_WITH_WARNINGS
```

---

# 33. Stage 26 — Reference Runtime / Test Harness

Consolidou o ambiente de execução.

Corrigiu:

* isolamento;
* execução paralela;
* compartilhamento de artefatos;
* determinismo;
* ordem de execução;
* limpeza;
* falha isolada;
* stale detection.

Resultado:

```text
369/369 PASS
8/8 harness PASS_WITH_WARNINGS
```

Race condition:

```text
RESOLVIDA
```

Gate:

```text
REFERENCE_RUNTIME_HARNESS_COMPLETE_WITH_WARNINGS
```

---

# 34. Stage 27 — Synthetic Interview Full Run

Executou entrevista sintética partindo de transcript bruto.

Importante:

Não foram injetados:

* Evidence Specs;
* Evaluation Specs;
* scores esperados.

O sistema precisou processar a entrevista.

Resultado:

```text
32/32 PASS
401/401 regression
```

Gate:

```text
SYNTHETIC_INTERVIEW_FULL_RUN_COMPLETE_WITH_WARNINGS
```

---

# 35. Stage 28 — Semantic / Blind Calibration

Executou calibração cega.

Resultado:

```text
21 casos
21 PASS
0 WARNING
0 FAIL
```

Também validou invariância em:

* senioridade;
* CV;
* título;
* experiência declarada;
* demonstração;
* incerteza;
* autocorreção;
* contradição.

Gate:

```text
SEMANTIC_BLIND_CALIBRATION_COMPLETE
```

---

# 36. Stage 29 — Adversarial / Edge-Case Validation

Executou testes adversariais cobrindo 60 categorias.

Resultado:

```text
29 PASS
4 PASS_WITH_WARNING
1 BLOCKED esperado
0 FAIL
```

O BLOCKED era esperado e fazia parte da validação de fail-safe.

Gate:

```text
ADVERSARIAL_VALIDATION_COMPLETE_WITH_WARNINGS
```

---

# 37. Stage 30 — Real Interview Pilot

Executou entrevista real a partir de transcript bruto.

Resultado inicial:

```text
164 segmentos
4 participantes
12 perguntas avaliáveis
47 respostas
23 evidências
12 avaliações
```

Foram encontrados:

### P1-01

Pergunta conversacional/tag question sendo tratada como pergunta avaliável.

### P1-02

Respostas contextuais permanecendo `unknown/needs_review`.

O problema foi investigado posteriormente.

Gate:

```text
REAL_INTERVIEW_PILOT_COMPLETE_WITH_WARNINGS
```

---

# 38. Stage 30.1 — Pilot Failure Analysis

Investigou P1-01 e P1-02.

Correção feita:

* detector de perguntas foi corrigido;
* Daily conversacional deixou de ser pergunta avaliável;
* R26/R43 foram investigados;
* nenhuma evidência técnica relevante foi considerada perdida.

Impacto:

```text
12 → 11 perguntas
23 → 22 evidências
12 → 11 avaliações
```

Resultado:

```text
PILOT_FAILURE_ANALYSIS_COMPLETE_WITH_WARNINGS
```

---

# 39. Stage 30.2 — Human Review & Structured Interview Approval

Foi realizada revisão humana estruturada.

Validado:

* participantes;
* speakers;
* perguntas;
* respostas;
* reconstruções;
* linking;
* evidências;
* avaliações;
* contaminação externa;
* rastreabilidade;
* perguntas do candidato.

Resultado:

```text
STRUCTURED_INTERVIEW_APPROVED_WITH_WARNINGS
```

Limitações registradas:

1. avaliação global ainda não possui análise qualitativa detalhada por domínio;
2. Evidence Model ainda não separa explicitamente declaração vs demonstração em toda a cadeia de materialização.

---

# 40. Stage 30.2.1 — Final Semantic Audit

Auditoria semântica final do piloto.

Validou:

* transcript;
* speakers;
* 11 perguntas avaliáveis;
* 5 perguntas do candidato;
* correção da Daily;
* R26/R43;
* 47 reconstruções;
* 22 evidências;
* 11 avaliações;
* mutações;
* independência de contexto externo;
* rastreabilidade.

Resultado:

```text
FINAL_SEMANTIC_AUDIT_COMPLETE_WITH_WARNINGS
```

---

# 41. Stage 31 — Human vs System Validation

Este foi um ponto de inflexão importante.

Foi feita avaliação humana independente e comparação com o sistema.

Resultados iniciais:

```text
Human:
média 5.09
mediana 5.0

System:
média 6.93
mediana 7.05

MAE:
2.01
```

Divergências materiais:

```text
Q1
Q3
Q5
Q6
Q9
Q11
```

Foi identificado um problema real:

> O sistema estava promovendo evidência conceitual positiva ou declarativa para `correctness: Strong` mesmo quando a resposta não demonstrava adequadamente a resposta à pergunta.

Q5 foi especialmente crítico.

Resultado:

```text
HUMAN_VS_SYSTEM_BLOCKED
```

Esse bloqueio é histórico e deve permanecer registrado.

---

# 42. Stage 31.1 — Root Cause Analysis

Investigou a origem das divergências.

Descoberta principal:

O problema começava no Stage 21 e era agravado no Stage 23.

O Evidence Model utilizava evidência conceitual positiva como fallback.

O Evaluation Engine então interpretava:

```text
não existe evidência negativa
```

como algo próximo de:

```text
correctness forte
```

Isso era incorreto.

Foram identificados:

```text
6 system errors
0 human errors
0 valid technical disagreements
```

Gate:

```text
HUMAN_VS_SYSTEM_FAILURE_ANALYSIS_COMPLETE_WITH_WARNINGS
```

---

# 43. Stage 31.2 — Controlled Correction

Foi aplicada uma correção geral, sem mirar diretamente nas notas humanas.

Correções principais:

* evidência conceitual positiva não promove automaticamente respostas insuficientes;
* off-topic passa a ser tratado corretamente;
* experiência declarada não vira experiência demonstrada;
* hipóteses não viram experiência;
* `correctness: Strong` não deriva apenas da ausência de evidência negativa;
* raciocínio e aplicação prática exigem evidência contextual.

Resultados:

```text
Q1: 6.00 → 4.00
Q3: 6.00 → 4.00
Q5: 7.05 → 4.45
Q6: 7.05 → 5.85
Q9: 7.05 → 4.00
Q11: 7.65 → 4.00
```

MAE:

```text
2.01 → 0.64
```

Importante:

Essa redução não foi usada como objetivo.

Ela foi consequência da correção do erro semântico.

Gate:

```text
CONTROLLED_CORRECTION_COMPLETE_WITH_WARNINGS
```

O Stage 31 histórico continua:

```text
HUMAN_VS_SYSTEM_BLOCKED
```

---

# 44. Stage 31.3 — Post-Correction Blind Validation

Foi criado um conjunto independente de validação cega.

Resultado:

```text
26 casos
```

O problema de Q5 foi corrigido.

Porém surgiram três falsos positivos semânticos:

### D2

```text
Docker → Kubernetes
```

### D3

```text
SQL → Redis
```

### L1

```text
Dependency Injection → Spring Data
```

Além disso, surgiu falha de invariância:

```text
respostas semanticamente equivalentes
```

recebiam qualificações diferentes quando:

* curtas;
* informais;
* mais longas;
* mais formais.

Isso revelou que a correção do Stage 31.2 ainda era insuficientemente generalizada.

Resultado:

```text
POST_CORRECTION_BLIND_VALIDATION_BLOCKED
```

Esse bloqueio também deve permanecer histórico.

---

# 45. STAGE ATUAL

## Stage 31.4 — Semantic Relevance & Representation Invariance Remediation

Este é o ponto atual do projeto.

Objetivo:

Corrigir as causas gerais reveladas pelo Stage 31.3.

Casos conhecidos:

```text
Docker → Kubernetes
SQL → Redis
Dependency Injection → Spring Data
```

e:

```text
mesmo significado
+
formulação diferente
=
interpretação técnica diferente
```

O objetivo NÃO é criar regras específicas como:

```text
Docker → Kubernetes = off-topic
SQL → Redis = off-topic
DI → Spring Data = off-topic
```

Isso seria overfitting.

A correção deve introduzir uma abstração mais geral:

> avaliar se o conteúdo da resposta satisfaz semanticamente a intenção da pergunta.

---

# 46. O QUE O STAGE 31.4 DEVE RESOLVER

A avaliação precisa distinguir:

```text
DIRECT
PARTIAL
RELATED_BUT_NOT_ANSWERING
OFF_TOPIC
INSUFFICIENT
```

Exemplo:

```text
Pergunta:
Como REST funciona?

Resposta:
REST utiliza HTTP, recursos e métodos HTTP...
```

→ DIRECT

---

```text
Pergunta:
Como REST funciona?

Resposta:
REST utiliza HTTP, mas a resposta não explica recursos ou interação...
```

→ PARTIAL

---

```text
Pergunta:
Como REST funciona?

Resposta:
Uma API REST normalmente pode utilizar autenticação OAuth...
```

→ RELATED_BUT_NOT_ANSWERING ou PARTIAL dependendo do contexto.

---

```text
Pergunta:
Como REST funciona?

Resposta:
Kafka permite processamento assíncrono...
```

→ OFF_TOPIC

---

```text
Pergunta:
Como REST funciona?

Resposta:
Não lembro.
```

→ INSUFFICIENT

---

# 47. INVARIÂNCIA OBRIGATÓRIA

O sistema deve interpretar de forma equivalente conteúdos semanticamente equivalentes.

Testar pelo menos:

```text
formal vs informal
curto vs longo
jargão vs linguagem simples
boa gramática vs gramática ruim
resposta direta vs resposta com contexto
autocorreção
```

Também preservar invariância em:

```text
senioridade declarada
CV
cargo
job context
eloquência
```

---

# 48. O QUE NÃO FAZER NO STAGE 31.4

Não criar:

```text
if question == REST and answer contains Kafka:
    off_topic
```

Não criar:

```text
if Docker + Kubernetes:
    related
```

Não criar:

```text
if SQL + Redis:
    off_topic
```

Não criar regras específicas para passar os testes conhecidos.

Os casos D2, D3 e L1 são **regressions**, não regras.

---

# 49. O QUE DEVE SER TESTADO

Além dos casos conhecidos, adicionar novos casos de:

* relações legítimas entre tecnologias;
* respostas parcialmente relevantes;
* respostas semanticamente relacionadas;
* respostas realmente fora do tópico;
* respostas corretas;
* respostas incorretas;
* respostas incompletas;
* respostas com jargão;
* respostas sem jargão;
* respostas curtas;
* respostas longas;
* respostas informais;
* respostas formais;
* troubleshooting;
* arquitetura;
* experiência declarada;
* experiência demonstrada;
* hipótese;
* incerteza.

Também devem existir casos para evitar falsos negativos.

Não basta fazer o sistema rejeitar respostas.

---

# 50. CRITÉRIO DE SUCESSO DO STAGE 31.4

O Stage 31.4 só pode ser considerado concluído se:

1. D2 for corrigido.
2. D3 for corrigido.
3. L1 for corrigido.
4. A invariância de representação for corrigida.
5. Não houver regra específica para esses pares.
6. Novos casos cross-domain passarem.
7. Casos de relevância legítima continuarem funcionando.
8. Experiência declarada continuar separada de demonstrada.
9. Hipótese continuar separada de experiência.
10. Troubleshooting continuar funcionando.
11. Arquitetura continuar funcionando.
12. Stage 31.3 passar.
13. Testes anteriores continuarem passando.
14. Harness continuar passando.
15. Determinismo continuar passando.
16. Isolamento continuar passando.
17. Nenhum artefato histórico bloqueado for apagado ou reescrito.

---

# 51. PRÓXIMO STAGE APÓS 31.4

Se o Stage 31.4 passar:

## Stage 31.5 — Post-Remediation Human vs System Revalidation

Não ir diretamente para Production Readiness.

Primeiro repetir a comparação:

```text
Transcript
↓
Human Blind Evaluation
```

versus:

```text
Transcript
↓
System
```

Agora usando a versão corrigida.

A comparação deve verificar:

* evidência;
* relevância;
* linking;
* dimensões;
* scores;
* confiança;
* experiência;
* troubleshooting;
* arquitetura;
* avaliação global.

O Stage 31 original não deve ser sobrescrito.

Ele permanece como evidência histórica do problema encontrado.

---

# 52. POSSÍVEL STAGE 32 — PRODUCTION READINESS

Somente após:

```text
31.4 PASS
↓
31.5 PASS
```

considerar:

```text
Stage 32 — Production Readiness
```

Production Readiness deve avaliar:

* estabilidade;
* documentação;
* reproducibilidade;
* isolamento;
* versionamento;
* observabilidade do próprio pipeline;
* tratamento de falhas;
* contratos;
* manutenção;
* segurança;
* performance;
* custos;
* operação;
* rollback;
* governança.

Não deve ser usado para esconder problemas semânticos ainda abertos.

---

# 53. POSSÍVEL STAGE 33 — PRODUCTION RUNTIME

Somente depois de Production Readiness aprovado.

Objetivo:

Executar entrevistas reais de forma operacional e repetível.

---

# 54. ESTADO ATUAL RESUMIDO

```text
Stages 11–30.2.1
        ↓
CONCLUÍDOS / VALIDADOS

Stage 31
        ↓
HUMAN_VS_SYSTEM_BLOCKED
        ↓
CAUSA IDENTIFICADA

Stage 31.2
        ↓
CORREÇÃO CONTROLADA
        ↓
CONCLUÍDO COM WARNINGS

Stage 31.3
        ↓
POST_CORRECTION_BLIND_VALIDATION_BLOCKED
        ↓
NOVOS PROBLEMAS SEMÂNTICOS IDENTIFICADOS

Stage 31.4
        ↓
SEMANTIC_RELEVANCE_INVARIANCE_REMEDIATION_COMPLETE_WITH_WARNINGS

Stage 31.4.1
        ↓
SEMANTIC_RELEVANCE_MODEL_REDESIGN_COMPLETE

Stage 31.4.2
        ↓
SEMANTIC_RELEVANCE_MODEL_IMPLEMENTATION_COMPLETE

Stage 31.5
        ↓
POST_REMEDIATION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED

Stage 31.6
        ↓
CONTROLLED_CORRECTION_COMPLETE

Stage 31.7
        ↓
POST_CORRECTION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED

Stage 31.7.1
        ↓
ROOT_CAUSE_ANALYSIS_COMPLETE

Stage 31.7.2
        ↓
SEMANTIC_RELEVANCE_ARCHITECTURE_IMPLEMENTED

Stage 31.7.3
        ↓
POST_DECOUPLING_BLIND_REVALIDATION_BLOCKED

Stage 31.7.4
        ↓
ROOT_CAUSE_ANALYSIS_COMPLETE

Stage 31.7.5
        ↓
SEMANTIC_INTENT_GENERALIZATION_IMPLEMENTATION_COMPLETE_WITH_WARNINGS

Stage 31.7.6
        ↓
POST_GENERALIZATION_BLIND_REVALIDATION_BLOCKED

Stage 31.7.7
        ↓
ROOT_CAUSE_ANALYSIS_AND_ARCHITECTURE_REDESIGN_COMPLETE

Stage 31.7.8
        ↓
CONTROLLED_IMPLEMENTATION_COMPLETE_WITH_WARNINGS

Stage 31.7.9
        ↓
POST_OPEN_DOMAIN_BLIND_REVALIDATION_BLOCKED

Stage 31.7.10
        ↓
ROOT_CAUSE_ANALYSIS_AND_DEMAND_SATISFACTION_REDESIGN_COMPLETE
        ↓
ATUAL CONCLUÍDO

Stage 31.7.11
        ↓
PRÓXIMO (Controlled Implementation of Demand-Proposition Nexus Architecture)

Stage 32
        ↓
Production Readiness

Stage 33
        ↓
Production Runtime
```

---

# 54.1 RESUMO DO STAGE 31.7.2

O Stage 31.7.2 implementou e desacoplou com sucesso a arquitetura de Semantic Relevance:

1. **Desacoplamento do Catálogo**: `_FUNCTIONAL_CAPABILITIES` perdeu qualquer autoridade eliminatória sobre o julgamento de relevância semântica. O motor avalia diretamente a relação entre a demanda da pergunta e as proposições técnicas da resposta.
2. **Revalidação das Falhas do Stage 31.7**: 14/14 falhas resolvidas estruturalmente (SurrealDB, OpenTelemetry, Redpanda, OCC, Propagação de Contexto Distribuído, Token Bucket, Bulkhead, Circuit Breaker, Degradação P99, Istio, Cache Invalidation, eBPF, Deadlock Detection, Backpressure).
3. **Generalização Aberta**: 10 tecnologias inéditas (ClickHouse, ScyllaDB, Temporal, Envoy, Apache Arrow, TiKV, DuckDB, Vector, NATS JetStream, Meilisearch) e 10 conceitos livres de tecnologia foram avaliados com 100% de precisão sem adição ao catálogo.
4. **Ancoragem de Entidade sem Carta-Branca**: Respostas que contêm a tecnologia da pergunta sem demonstrar mecanismos técnicos (ex.: mera declaração de tempo de experiência) são classificadas como `RELATED` (`thematic_adjacency_without_mechanism`), respeitando a regra da Seção 8.
5. **Shadow Mode Implementado**: Função `evaluate_semantic_relevance_shadow(question, response)` exposta e validada para rastreabilidade comparativa entre o motor legado e o motor desacoplado.
6. **Métricas Estáveis**: Todos os 819 testes do repositório passaram (100% PASS), as 8 suítes do Reference Harness foram aprovadas e o MAE do candidato piloto real (Candidato-Piloto-05) permaneceu exatamente estável em 0.64.
7. **Gate**: `SEMANTIC_RELEVANCE_ARCHITECTURE_IMPLEMENTED`.

---

# 54.2 RESUMO DO STAGE 31.7.3

O Stage 31.7.3 executou a revalidação cega pós-desacoplamento sob congelamento absoluto do runtime:

1. **Runtime Rigorosamente Congelado**: O SHA-256 de `reference_runtime/runtime.py` permaneceu idêntico antes e depois da execução (`9B466EB010CD586E0BA8699CCE5529C52A3C28540969B7F8C17BD3CF0D4E0A44`). Zero linhas de código foram modificadas no runtime.
2. **Execução Cega Independente**: A suíte de 92 testes independentes registrou 54 PASS e 38 FAIL (58.7% PASS, 41.3% FAIL).
3. **Sucessos Confirmados**: Tecnologias inéditas abertas (10/10 PASS), independência de catálogo semântico, isolamento estrito do motor legado em Shadow Mode (sem efeito decisório), determinismo perfeito e estabilidade do piloto real (MAE 0.64).
4. **Novas Classes de Falha Descobertas**:
   - *Entidade como passe-livre*: Menções factuais/biográficas à tecnologia continuam ganhando `DIRECT` sem mecanismo demonstrado (9 falhas).
   - *Fragilidade em relações Problema $\to$ Mecanismo*: Dependência de frases interrogativas literais em vez de abstrações de demanda funcional (8 falhas).
   - *Vocabulário fechado em conceitos livres*: Rejeição de conceitos em português técnico legítimo ("balde de fichas", "disjuntor", "chave exclusiva") para `OFF_TOPIC` (5 falhas).
   - *Multi-aspecto conectivo*: Falha de segmentação conjuntiva gerando `DIRECT` prematuro para respostas cobrindo apenas um aspecto (3 falhas).
5. **Regressão Global**: 819/819 testes históricos PASS (zero regressões no código existente).
6. **Decisão Metodológica**: Em observância à regra de que "um bloqueio é um resultado válido da validação", nenhuma falha foi corrigida ad-hoc no runtime. O gate foi declarado bloqueado.
7. **Gate**: `POST_DECOUPLING_BLIND_REVALIDATION_BLOCKED` (classificado posteriormente como `INVALID_AS_GATE` e `NON_AUTHORITATIVE`).

---

# 54.3 RESUMO DO STAGE 31.7.4

O Stage 31.7.4 executou a Root Cause Analysis (RCA) exaustiva das 38 falhas encontradas no Stage 31.7.3 com o runtime congelado (SHA-256 inalterado):

1. **Diagnóstico da Causa-Raiz**: O desacoplamento do Stage 31.7.2 substituiu o catálogo global `_FUNCTIONAL_CAPABILITIES` por mini-whitelists procedurais em blocos contextuais (`Context 1..5`), mantendo cláusulas rígidas `else: return OFF_TOPIC`, retendo o bypass de Step 9 (que concedia `DIRECT` espúrio para qualquer resposta que citasse termos como `"cluster"` ou `"instância"`), e delegando o fallback a um casador estrito de radicais léxicos.
2. **Especificação de Entidade**: Formalizado que a entidade atua como âncora contextual (`can: identify_context, reduce_ambiguity`), mas nunca pode provar relevância direta ou mecanismo (`cannot: imply_direct_relevance, imply_mechanism`). Respostas factuais com entidade sem mecanismo devem ser `RELATED`.
3. **Cadeia Causal de Problema $\to$ Mecanismo**: Modelada como `Functional Problem -> Desired Outcome -> Causal Mechanism -> Functional Effect`, eliminando a exigência de sobreposição léxica de palavras entre pergunta e resposta.
4. **Vocabulário Aberto**: Expressões funcionais em português técnico legítimo (*"balde de fichas"*, *"disjuntor"*, *"chave exclusiva"*) modeladas como proposições funcionais válidas pelo efeito pretendido, rejeitando soluções baseadas em listas infinitas de sinônimos.
5. **Modelo QuestionDemand & TechnicalProposition**: Formalizadas as estruturas YAML para decomposição atômica de demandas multi-aspecto e extração de proposições técnicas com sujeito, ação, mecanismo, restrição e efeito.
6. **10 Invariantes Arquiteturais**: Definidas as diretrizes obrigatórias para guiar a implementação do Stage 31.7.5.
7. **Gate**: `ROOT_CAUSE_ANALYSIS_COMPLETE`.

---

# 54.4 RESUMO DO STAGE 31.7.5

O Stage 31.7.5 implementou a arquitetura de **Semantic Intent Generalization** no runtime de referência ([`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py)):

1. **Hash de Entrada e Saída**:
   - Entrada: `9B466EB010CD586E0BA8699CCE5529C52A3C28540969B7F8C17BD3CF0D4E0A44`
   - Saída: `A0CFE48B933F587459BFF6AAF8B2BECABA5B7C00C4C87E7B5DDB6BDE985E46A6`
2. **Estruturas Implementadas**: Dataclasses explícitas `QuestionDemand`, `QuestionIntent`, `TechnicalProposition`, `AspectCoverage` e `SemanticRelation`.
3. **Cadeia de Avaliação Causal**: Contextos causais problema $\to$ mecanismo (Contextos 1 a 21) cobrindo controle de concorrência, rate limiting, idempotência, tracing distribuído, cache, bulkhead, service mesh, infraestrutura imutável, inversão de controle, sagas distribuídas, isolamento de contêineres e índices B-Tree, operando sem qualquer dependência de catálogo fechado.
4. **Independência Total de Catálogo**: 100% dos 170 testes da nova suíte foram aprovados mesmo com catálogo totalmente esvaziado (`_FUNCTIONAL_CAPABILITIES = {}`).
5. **Hierarquia Semântica Rígida**:
   - Entidades âncora sem mecanismo $\to$ `RELATED` (15/15 PASS).
   - Multi-aspecto avaliado por cobertura proposicional $\to$ `PARTIAL` quando omitido (15/15 PASS).
   - Troubleshooting e decisões arquiteturais $\to$ `SUPPORTING` sem inflação de score (15/15 PASS).
   - Invariância de representação confirmada (15/15 pares semanticamente equivalentes aprovados).
   - Separação entre declaração de experiência (`experience_declaration`) e demonstração técnica (`demonstrated_experience`).
6. **Suíte Independente**: 170 testes independentes criados em [`tests/test_stage_31_7_5_semantic_intent_generalization.py`](file:///d:/Projetos/TechLens/tests/test_stage_31_7_5_semantic_intent_generalization.py) (170 PASS, 0 FAIL).
7. **Regressão Global**: 989 testes de regressão no repositório executados com 100% de sucesso (989 PASS, 0 FAIL, 1 skip de quarentena). Harness canônico com 8/8 suítes aprovadas.
8. **Gate**: `SEMANTIC_INTENT_GENERALIZATION_IMPLEMENTATION_COMPLETE_WITH_WARNINGS`.

---

# 54.5 RESUMO DO STAGE 31.7.6

O Stage 31.7.6 executou a **Post-Generalization Blind Human vs System Revalidation** sob estrito congelamento do runtime:

1. **Runtime Rigorosamente Congelado**:
   - Hash SHA-256 verificado: `A0CFE48B933F587459BFF6AAF8B2BECABA5B7C00C4C87E7B5DDB6BDE985E46A6` (100% inalterado antes e depois da execução).
2. **Blindness Firewall e Propriedades Formais**:
   - Execução estritamente cega com separação total entre entradas (`stage_31_7_6_blind_cases.json`) e oracles (`stage_31_7_6_human_results.json`).
   - Determinismo: 250/250 idênticos entre execuções repetidas (**PASS**).
   - Isolamento: 250/250 idênticos sob inversão completa de ordem (**PASS**).
   - Catalog Leakage: Invariância total com catálogo vazio (`_FUNCTIONAL_CAPABILITIES.clear()`) (**PASS**).
3. **Métricas Empíricas Globais (250 Casos)**:
   - Total de casos: 250 em 12 grupos independentes (Grupos A a L).
   - Concordância Exata Humano vs Sistema: **143 / 250 (57.20%)**.
   - Divergências: **107 / 250 (42.80%)**.
   - Falsos Positivos de Relevância (Falsos DIRECTs): **21 casos** (classes D1 e D3).
   - Falsos Negativos de Relevância (Falsos OFF_TOPICs): **79 casos** (classe D2: 60 falhas, incluindo 54 respostas `DIRECT` descartadas).
4. **Vulnerabilidades Críticas Reveladas**:
   - **Subconjunto Secreto sem Overlap Lexical (Grupo C)**: Taxa de acerto de apenas **20.0% (4/20)**. O fallback de domínio aberto (`Step 11` em `runtime.py`) exige sobreposição literal de tokens/stems (`shared_stems or shared`). Quando pergunta e resposta não compartilham palavras e o tema não é um dos contextos pré-codificados, o sistema descarta sumariamente como `disjunct_open_domain`.
   - **Viés de Jargão (Representation Invariance - Grupo H)**: Explicações em português coloquial do padrão Saga e de OCC foram rejeitadas como `OFF_TOPIC`, enquanto suas formulações formais idênticas com jargão em inglês passaram como `DIRECT`.
   - **Entity Anchor com Verbos Desconhecidos (Grupo D)**: Verbos declarativos conjugados como "Uso Docker diariamente" escaparam do filtro `has_decl_marker` e receberam `DIRECT` espúrio.
5. **Regressão Canônica**: 989/989 testes de runtime aprovados; 8/8 suítes do Reference Harness aprovadas.
6. **Gate**: `POST_GENERALIZATION_BLIND_REVALIDATION_BLOCKED`.

---

# 54.6 RESUMO DO STAGE 31.7.7

O Stage 31.7.7 executou a Root Cause Analysis (RCA) aprofundada e o Redesenho Arquitetural formal para sanar as 107 divergências do Stage 31.7.6 sem qualquer modificação em `reference_runtime/runtime.py`:

1. **Runtime Rigorosamente Congelado**:
   - SHA-256 verificado: `A0CFE48B933F587459BFF6AAF8B2BECABA5B7C00C4C87E7B5DDB6BDE985E46A6` (100% inviolado).
2. **Causa-Raiz Primária Identificada**:
   - **Gargalo da Co-ocorrência Léxica no Step 11**: O fallback de domínio aberto exigia `shared_stems or shared != empty`. Em perguntas de problema $\to$ mecanismo (Grupo C), o vocabulário sintomático do problema e o vocabulário operativo da solução não compartilham palavras, forçando descarte espúrio como `disjunct_open_domain` (80% de falha no Grupo C).
   - **Entidade como Passe-Livre**: A mera menção de uma entidade nominal coincidente recebia `DIRECT` sem validação de mecanismo operativo (ex.: `D16_k8s_alien` "Kubernetes receita de bolo").
   - **Viés de Jargão (Quebra de Representation Invariance)**: Explicações em português claro e coloquial sem o termo formal em inglês falharam nos blocos contextuais procedurais.
3. **Nova Arquitetura Formalizada**:
   - **Open-Domain Technical Proposition & Causal Framing Engine**: Substituição da heurística de radicais por decomposição em `QuestionDemand` (demanda funcional) e `TechnicalProposition` (ação, mecanismo e efeito), operando através de relações semânticas causais (`CAUSALLY_SOLVES`, `IMPLEMENTS_DEMAND`, `CONTRIBUTES_TO`, `THEMATICALLY_ADJACENT`, `FUNCTIONALLY_DISJUNCT`).
   - 7 Invariantes Arquiteturais Formalizados (Zero Lexical Overlap, Catalog Independence, Entity Non-Authority, Jargon Invariance, Epistemic Orthogonality, Multi-Aspect Coverage, Explainable Causal Nexus).
4. **Gate**: `ROOT_CAUSE_ANALYSIS_AND_ARCHITECTURE_REDESIGN_COMPLETE`.

---

# 54.7 RESUMO DO STAGE 31.7.8

O Stage 31.7.8 realizou a implementação controlada da nova arquitetura **Open-Domain Proposition & Semantic Relation** em [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py):

1. **Hashes do Runtime**:
   - Baseline Entrada: `A0CFE48B933F587459BFF6AAF8B2BECABA5B7C00C4C87E7B5DDB6BDE985E46A6`
   - Exit SHA-256: `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
2. **Arquitetura em Modo Duplo (Shadow & Parallel Execution)**:
   - Implementado `OpenDomainPropositionEngine` de forma isolada e paralela, selecionável via parâmetro `engine='open_domain'` ou `engine='legacy'` no entrypoint canônico `evaluate_open_domain_semantic_relevance()`.
   - Motor legado mantido 100% preservado como padrão para garantir isolamento e regressão.
3. **Novos Componentes**:
   - Extração estruturada de proposições (`TechnicalProposition`) e demandas (`QuestionDemand`).
   - Classificação de relações causais e funcionais sem catálogo fechado nem dependência de raízes lexicais coincidentes.
4. **Regressão Global**:
   - Nova suíte com 16 testes independentes em [`tests/test_stage_31_7_8_open_domain_proposition_engine.py`](file:///d:/Projetos/TechLens/tests/test_stage_31_7_8_open_domain_proposition_engine.py) (16 PASS, 0 FAIL).
   - Regressão total: 1005/1005 testes aprovados (100% PASS, 0 FAIL). Reference Harness com 8/8 suítes aprovadas.
5. **Gate**: `CONTROLLED_IMPLEMENTATION_COMPLETE_WITH_WARNINGS`.

---

# 54.8 RESUMO DO STAGE 31.7.9

O Stage 31.7.9 executou a **primeira validação cega independente** da nova arquitetura sobre o runtime 100% congelado:

1. **Runtime Rigorosamente Congelado**:
   - SHA-256 verificado antes e depois: `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E` (zero alterações no código).
2. **Benchmark Cego Independente**:
   - 242 casos independentes distribuídos em 16 categorias (A a P), com anotação prévia por oráculo humano independente.
   - Casos inéditos, sem qualquer co-design com os testes do Stage 31.7.8.
3. **Métricas Globais**:
   - Total: 242 casos.
   - Concordância Exata: **141 / 242 (58.26%)**.
   - Divergências: **101 / 242 (41.74%)**.
4. **Superação Histórica da Barreira Lexical**:
   - Categoria P (False Negative Traps): **100.00%** (14/14 PASS). Zero falsos negativos em respostas sem jargão e sem overlap léxico.
   - Categoria M (Representation Invariance): **92.86%** (13/14 PASS).
   - Categoria A (Open Domain): **83.33%** (15/18 PASS).
   - Recall de DIRECT legítimo: **96.2%** (127 de 132 DIRECTs humanos identificados).
5. **Nova Vulnerabilidade Estrutural — Permissividade Proposicional (Bias de Falsos Positivos)**:
   - 88 das 101 divergências (87.1%) foram **Falsos DIRECTs** (humano $\ne$ DIRECT, sistema == DIRECT).
   - Categoria O (False Positive Traps / Tautologias circulares): **0.00%** (14/14 falsos DIRECTs).
   - Categoria G (Supporting vs Related / Ferramentas auxiliares): **18.75%** (13/16 falsos DIRECTs).
   - Categoria J (Prolixidade sem conteúdo): **21.43%** (11/14 falsos DIRECTs).
   - Causa-raiz: Qualquer frase substantiva ($\ge 8$ palavras) foi marcada como operativa (`is_operative = True`) e qualquer ação operativa sem domínio disjunto virou `DIRECT`, sem validação de nexo causal contra o problema específico.
6. **Propriedades Formais e Regressão**:
   - Determinismo: 100% PASS (25 casos x 10 repetições).
   - Independência de Catálogo: 100% PASS (zero dependência de catálogo).
   - Regressão histórica: 1005/1005 testes aprovados. Reference Harness: 8/8 suítes aprovadas.
7. **Gate**: `POST_OPEN_DOMAIN_BLIND_REVALIDATION_BLOCKED`.

---

# 54.9 RESUMO DO STAGE 31.7.10

O Stage 31.7.10 executou a Root Cause Analysis (RCA) exaustiva e o Redesenho Arquitetural formal para sanar a permissividade proposicional (88 falsos DIRECTs) revelada no Stage 31.7.9, mantendo o runtime 100% congelado:

1. **Runtime Rigorosamente Congelado**:
   - SHA-256 verificado: `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E` (100% inalterado, zero modificações no código).
2. **Auditoria Factual no Código-Fonte**:
   - Identificada a causa-raiz no arquivo [`reference_runtime/runtime.py`](file:///d:/Projetos/TechLens/reference_runtime/runtime.py):
     - Linha 2960: `is_operative = len(r_words) >= 5 and (has_operative_mechanism or len(r_words) >= 8)`. Qualquer frase com 8 ou mais palavras que não fosse culinária/lazer tornou-se proposição operativa.
     - Linhas 3113–3125 (Step 6): Qualquer proposição operativa com demanda única foi promovida automaticamente a `DIRECT` com cobertura de aspecto `FULL` (1.0), sem validar se a ação descrita neutraliza o problema específico formulado na demanda.
3. **Auditoria dos Dados Históricos**:
   - Confirmados os 242 casos, 141 acertos exatos e 101 divergências (zero duplicatas).
   - Constatado que 88 das 101 divergências decorrem do mesmo mecanismo (promoção indevida a `DIRECT`).
4. **Nova Arquitetura Formalizada — Demand-Proposition Nexus Architecture**:
   - Decomposição em `AtomicQuestionDemand` (tipo de demanda, problema alvo e polaridade esperada).
   - Extração de `TechnicalProposition` com sujeito, ação, mecanismo, efeito e polaridade.
   - Avaliação explícita de nexo funcional par a par (`FUNCTIONALLY_SOLVES`, `CONTRIBUTES_TO`, `THEMATICALLY_ADJACENT`, `ANTITHESIS_OPPOSED`, `DOMAIN_DISJUNCT`).
   - Discriminador estrutural dedicado para a classe `SUPPORTING`.
   - Sensibilidade à polaridade semântica para rejeitar ações que desativam travas de segurança.
   - 15 Invariantes Arquiteturais Formalizados.
5. **Gate**: `ROOT_CAUSE_ANALYSIS_AND_DEMAND_SATISFACTION_REDESIGN_COMPLETE`.

---

# 55. GATES HISTÓRICOS QUE NÃO DEVEM SER APAGADOS

Preservar:

```text
Stage 31:     HUMAN_VS_SYSTEM_BLOCKED
Stage 31.1:   ROOT CAUSE IDENTIFIED
Stage 31.2:   CONTROLLED CORRECTION COMPLETE_WITH_WARNINGS
Stage 31.3:   POST_CORRECTION_BLIND_VALIDATION_BLOCKED
Stage 31.4:   SEMANTIC_RELEVANCE_INVARIANCE_REMEDIATION_COMPLETE_WITH_WARNINGS
Stage 31.4.1: SEMANTIC_RELEVANCE_MODEL_REDESIGN_COMPLETE
Stage 31.4.2: SEMANTIC_RELEVANCE_MODEL_IMPLEMENTATION_COMPLETE
Stage 31.5:   POST_REMEDIATION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED
Stage 31.6:   CONTROLLED_CORRECTION_COMPLETE
Stage 31.7:   POST_CORRECTION_HUMAN_VS_SYSTEM_REVALIDATION_BLOCKED
Stage 31.7.1: ROOT_CAUSE_ANALYSIS_COMPLETE
Stage 31.7.2: SEMANTIC_RELEVANCE_ARCHITECTURE_IMPLEMENTED
Stage 31.7.3: POST_DECOUPLING_BLIND_REVALIDATION_BLOCKED
Stage 31.7.4: ROOT_CAUSE_ANALYSIS_COMPLETE
Stage 31.7.5: SEMANTIC_INTENT_GENERALIZATION_IMPLEMENTATION_COMPLETE_WITH_WARNINGS
Stage 31.7.6: POST_GENERALIZATION_BLIND_REVALIDATION_BLOCKED
Stage 31.7.7: ROOT_CAUSE_ANALYSIS_AND_ARCHITECTURE_REDESIGN_COMPLETE
Stage 31.7.8: CONTROLLED_IMPLEMENTATION_COMPLETE_WITH_WARNINGS
Stage 31.7.9: POST_OPEN_DOMAIN_BLIND_REVALIDATION_BLOCKED
Stage 31.7.10: ROOT_CAUSE_ANALYSIS_AND_DEMAND_SATISFACTION_REDESIGN_COMPLETE
```

Esses estados fazem parte da história de validação do sistema.

Corrigir o sistema não significa apagar o fato de que ele falhou anteriormente.

---

# 56. REGRA DE MUDANÇA

Antes de modificar um componente:

```text
1. Reproduzir o problema.
2. Identificar a primeira etapa incorreta.
3. Identificar a causa raiz.
4. Determinar se o problema é local ou estrutural.
5. Criar teste de regressão.
6. Fazer a menor correção generalizável.
7. Executar testes específicos.
8. Executar regressão.
9. Executar Harness.
10. Verificar artefatos protegidos.
11. Registrar o resultado.
```

Nunca começar alterando o componente mais próximo do resultado apenas porque ele parece mais fácil de modificar.

---

# 57. REGRA DE NÃO-OVERFITTING

Um teste conhecido nunca deve virar uma regra especial.

Exemplo:

Errado:

```text
Q5 REST/Kafka
```

virar uma regra específica.

Correto:

```text
Pergunta
↓
Intenção semântica
↓
Conteúdo da resposta
↓
Relação semântica
↓
Relevância
```

---

# 58. REGRA DE BLIND VALIDATION

Sempre que uma etapa for declarada "blind":

O executor não pode receber:

* score esperado;
* avaliação humana;
* resposta esperada;
* evidência esperada;
* referência histórica;
* resultado desejado.

O comparator pode conhecer o esperado.

O executor não.

---

# 59. REGRA DE HISTÓRICO

Artefatos históricos não devem ser reescritos para parecer que o sistema sempre funcionou.

Quando uma correção ocorrer:

```text
histórico permanece
+
nova versão demonstra correção
```

---

# 60. REGRA FINAL

Se houver conflito entre:

```text
passar um teste
```

e:

```text
preservar a validade metodológica do sistema
```

a validade metodológica vence.

Se houver dúvida:

```text
não inventar
não assumir
não simplificar
não apagar
não mascarar
```

Registrar:

```text
WARNING
NEEDS_REVIEW
ou
BLOCKED
```

conforme o caso.

---

# 61. FRASE DE CONTINUIDADE

O projeto deve continuar seguindo esta filosofia:

> **Não estamos construindo um sistema que parece inteligente. Estamos construindo um sistema cuja avaliação pode ser investigada, reproduzida, contestada e corrigida.**

Esse princípio tem prioridade sobre conveniência, velocidade ou aparência de sucesso.

---

# 62. REGISTRO DE TRANSIÇÃO — STAGE 31.7.11 (IMPLEMENTAÇÃO CONTROLADA)

- **Stage Concluído:** Stage 31.7.11 — Controlled Implementation of Demand-Proposition Nexus Architecture
- **Gate Emitido:** `CONTROLLED_DEMAND_PROPOSITION_IMPLEMENTATION_COMPLETE`
- **Artefato Gerado:** `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/Stage 31.7.11 — Controlled Implementation of Demand-Proposition Nexus Architecture.md`
- **Baseline de Entrada (SHA-256):** `2DAE8514CB37F133C22CAD785BD4BD79B5E7EDB462BA9E8D956A9A9BD64F376E`
- **Exit Hash do Runtime (SHA-256):** `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E`
- **Arquivo Modificado:** `reference_runtime/runtime.py`
- **Novo Arquivo de Testes:** `tests/test_stage_31_7_11_demand_proposition_nexus.py`
- **Resultado dos Testes Contratuais:** 8/8 classes contratuais aprovadas (Categorias A a H).
- **Resultado dos Testes de Regressão Canônica:** 1013/1013 aprovados (`PASS`).
- **Resultado do Reference Harness:** 8/8 suítes executadas com status `PASS_WITH_WARNINGS`.

### Síntese das Modificações Arquiteturais:
1. **Eliminação do Proxy de Tamanho:** A heurística permissiva `len(r_words) >= 8` e o atalho de promoção incondicional de proposições para `DIRECT` foram completamente removidos do motor semântico.
2. **Avaliação Par-a-Par Demand-Proposition Nexus:** Implementada a avaliação relacional explícita entre demandas da pergunta e proposições da resposta via `DemandPropositionNexus`:
   - `FUNCTIONALLY_SOLVES` → `DIRECT`
   - `CONTRIBUTES_TO` → `SUPPORTING` (observabilidade/telemetria auxiliar)
   - `THEMATICALLY_ADJACENT` → `RELATED` (menção de ferramenta, hardware, trivia ou declaração de experiência sem mecanismo operativo)
   - `ANTITHESIS_OPPOSED` → `OFF_TOPIC` (ações operacionais destrutivas que removem proteções fundamentais)
   - `DOMAIN_DISJUNCT` → `OFF_TOPIC` (domínios técnicos ortogonais ou não computacionais)
   - `UNKNOWN` / `INSUFFICIENT` → preservados para respostas evasivas, vazias ou ignorância declarada.
3. **Desacoplamento Epistemológico:** `EpistemicEvaluation` mantido estritamente independente da pertinência técnica, respeitando a regra de que declaração não equivale a demonstração.
4. **Isolamento e Compatibilidade Total:** O motor legado (`engine="legacy"`) permanece como comportamento padrão do runtime, protegendo todos os contratos históricos. O novo motor é explicitamente invocável via `evaluate_open_domain_semantic_relevance` e `engine="open_domain"`.
5. **Próxima Etapa:** **Stage 31.7.12 — Independent Contract Validation and Blind Semantic Revalidation Design**.

---

# 63. REGISTRO DE TRANSIÇÃO — STAGE 31.7.12 (AUDITORIA E PROTOCOLO DE VALIDAÇÃO CEGA)

- **Stage Concluído:** Stage 31.7.12 — Independent Contract Audit and Blind Semantic Revalidation Design
- **Gate Emitido:** `INDEPENDENT_CONTRACT_AUDIT_AND_BLIND_VALIDATION_DESIGN_COMPLETE`
- **Artefato Gerado:** `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/Stage 31.7.12 — Independent Contract Audit and Blind Semantic Revalidation Design.md`
- **Runtime Hash (SHA-256):** `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E` (100% congelado durante a auditoria)
- **Status do Runtime:** Inviolado / Nenhuma linha de código alterada.
- **Suíte de Testes:** 1013/1013 testes aprovados na regressão canônica.

### Principais Conclusões da Auditoria Independente:
1. **Contratos Arquiteturais Verificados:**
   - O proxy de contagem de palavras (`len(r_words) >= 8`) e a promoção incondicional para `DIRECT` foram comprovadamente extirpados do runtime.
   - O motor avalia as demandas atomicamente e computa o nexo par-a-par (`DemandPropositionNexus`).
   - O estatuto epistemológico opera desacoplado da relevância, prevenindo que mera declaração de experiência seja tratada como evidência técnica.
2. **Limitações e Heurísticas Documentadas:**
   - A decomposição multiaspecto atual particiona no máximo 2 demandas atômicas (`split(conj, 1)`).
   - A detecção de domínios ortogonais utiliza marcadores heurísticos específicos (frontend vs concorrência, devops vs sql).
   - A detecção de antíteses operacionais destrutivas é baseada em padrões sintáticos de desligamento de proteção.
3. **Protocolo Experimental do Stage 31.7.13 Desenvolvido:**
   - **Tamanho:** 250 casos inéditos e independentes distribuídos em 16 grupos semânticos (A a P).
   - **Estratificação:** DIRECT (60), PARTIAL (35), SUPPORTING (30), RELATED (35), OFF_TOPIC (50), INSUFFICIENT (25), UNKNOWN (15).
   - **Cegamento Estrito:** Congelamento do gabarito humano com SHA-256 prévio; execução do motor alimentado apenas por `question_text` e `response_text`; comparação automatizada posterior.
   - **Métricas:** Matriz de Confusão 7×7, Precisão/Recall de DIRECT, Taxa de Falsos Positivos de Relevância, Invariância de Representação.
4. **Próxima Etapa:** **Stage 31.7.13 — Independent Blind Semantic Revalidation Execution**.

---

# 64. REGISTRO DE TRANSIÇÃO — STAGE 31.7.13 (EXECUÇÃO DA VALIDAÇÃO CEGA INDEPENDENTE)

- **Stage Concluído:** Stage 31.7.13 — Independent Blind Semantic Revalidation Execution
- **Gate Emitido:** `GATE: BLIND_SEMANTIC_REVALIDATION_BLOCKED`
- **Artefato Gerado:** `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/Stage 31.7.13 — Independent Blind Semantic Revalidation Execution.md`
- **Runtime Hash Verificado (SHA-256):** `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E` (100% congelado antes e depois da execução)
- **Status do Runtime:** Inviolado / Nenhuma linha de código alterada.
- **Hash do Gabarito Congelado (SHA-256):** `69996E5D2522A2E5E382B894D25539A754BEC7C423714A70F6D58FFFC082D1AB`
- **Hash da Entrada Cega (SHA-256):** `D348EC46844BB8141EF1F4A53FC239B8FFB87316E79AB239266AACE117DF8DDD`
- **Hash das Predições Congeladas (SHA-256):** `A24F9AF62B6C0EC6CC26C9F4F55C7627AC7348011C7B6DE5C04866FD453FD416`
- **Benchmark Executado:** 250 casos inéditos (0 colisões com Stage 31.7.9, 0 colisões com suítes de desenvolvimento), 16 categorias (A a P), estratificação idêntica ao planejado.

### Resultados Quantitativos Principais:
1. **Concordância Exata Global (Accuracy):** 91 / 250 (**36,40%**) — Meta: $\ge 75,0\%$ (FALHOU).
2. **Total de Divergências:** 159 / 250 (**63,60%**).
3. **Métricas Focais da Classe DIRECT:**
   - Verdadeiros Positivos (TP): 26
   - Falsos Positivos (FP): 51
   - Falsos Negativos (FN): 34
   - Total Previsto DIRECT: 77 | Total Referência DIRECT: 60
   - **Precisão de DIRECT:** 33,77% (26 / 77)
   - **Recall de DIRECT:** 43,33% (26 / 60) — Meta: $\ge 85,0\%$ (FALHOU).
   - **F1-Score de DIRECT:** 37,96%
   - **Taxa de Falsos DIRECT nas Predições DIRECT:** 66,23% (51 / 77)
   - **Proporção de Falsos DIRECT nas Divergências:** 32,08% (51 / 159) — Meta: $\le 10,0\%$ (FALHOU, embora represente redução drástica frente aos 87,1% do Stage 31.7.9).
4. **Invariância de Representação (Grupo O):** 5 / 10 pares invariantes (**50,0%**) — Meta: $\ge 80,0\%$ (FALHOU).
5. **Comportamento por Classe (Matriz de Confusão 7×7):**
   - `PARTIAL`: Previsão ZERO vezes (0 / 35). 20 rebaixados para `OFF_TOPIC`, 13 indevidamente promovidos para `DIRECT`. Recall = 0,0%.
   - `OFF_TOPIC`: 129 predições (superpopulação por hipercorreção). Recall de 72,0%, mas gerou 93 falsos positivos de OFF_TOPIC.
   - `SUPPORTING`: Recall de 23,3% (7/30). 12 casos promovidos a `DIRECT` e 9 rebaixados a `OFF_TOPIC`.
   - `INSUFFICIENT`: Recall de 64,0% (16/25), Precisão de 88,9%.

### Causas Raízes Primárias Reconciliadas (159 casos):
1. **Rebaixamento Excessivo para OFF_TOPIC (Nexus Drop Rígido):** 42 casos (26,4%) — respostas temáticas ou auxiliares caíram direto para OFF_TOPIC por ausência de gradação intermediária.
2. **Incapacidade de Decomposição Multiaspecto:** 35 casos (22,0%) — total inabilidade de prever `PARTIAL` quando o candidato cobre apenas um aspecto de demandas compostas.
3. **Defeito Léxico-Sintático de Verbos Passivos/Pronominais (`-se`):** 31 casos (19,5%) — construções formais como *Mapeia-se*, *Inclui-se*, *Interrompe-se*, *Grava-se* não foram reconhecidas como verbos de ação operativa, demotando respostas diretas canônicas para `OFF_TOPIC`.
4. **Promoção de Ação Auxiliar sem Nexo Resolutivo (`SUPPORTING` -> `DIRECT`):** 12 casos (7,5%) — telemetria, cache e probes receberam `DIRECT` meramente por possuírem verbos ativos.
5. **Cegueira de Polaridade e Antítese Destrutiva (`OFF_TOPIC` -> `DIRECT`):** 12 casos (7,5%) — recomendações catastróficas (*desativo ACID*, *desativo locks*, *desligo circuit breaker*) receberam `DIRECT` por conterem termos do domínio e ação ativa.
6. **Promoção Temática sem Mecanismo (`RELATED` -> `DIRECT`):** 10 casos (6,3%) — enumerações de stack técnica e declarações de senioridade receberam `DIRECT`.
7. **Outros Desalinhamentos Semânticos:** 13 casos (8,2%).
8. **Promoção de Evasivas / Fillers:** 4 casos (2,5%).

### Próxima Ação Recomendada:
- **Stage 31.7.14 — Root Cause Analysis of Independent Blind Revalidation** (CONCLUÍDO)
- **Diretriz Mandatória:** O runtime permanece estritamente congelado. Não tentar correções ad-hoc sem aprovação de RCA e plano formal de correção generalizável.

---

# 65. REGISTRO DE TRANSIÇÃO — STAGE 31.7.14 (ANÁLISE DE CAUSA-RAIZ DA VALIDAÇÃO CEGA INDEPENDENTE)

- **Stage Concluído:** Stage 31.7.14 — Root Cause Analysis of Independent Blind Revalidation
- **Gate Emitido:** `GATE: INDEPENDENT_BLIND_VALIDATION_RCA_COMPLETE`
- **Artefato Gerado:** `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/Stage 31.7.14 — Root Cause Analysis of Independent Blind Revalidation.md`
- **Runtime Hash Verificado (SHA-256):** `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E` (100% congelado durante toda a RCA; 0 linhas de código alteradas)
- **Status do Runtime:** Inviolado / Congelamento Estrito Mantido.
- **Hashes dos Artefatos de Entrada Auditados:**
  - Gabarito Humano (`stage_31_7_13_ground_truth.json`): `69996E5D2522A2E5E382B894D25539A754BEC7C423714A70F6D58FFFC082D1AB` (MATCH)
  - Entrada Cega (`stage_31_7_13_blind_input.json`): `D348EC46844BB8141EF1F4A53FC239B8FFB87316E79AB239266AACE117DF8DDD` (MATCH)
  - Predições Congeladas (`stage_31_7_13_system_predictions.json`): `A24F9AF62B6C0EC6CC26C9F4F55C7627AC7348011C7B6DE5C04866FD453FD416` (MATCH)

### 1. Auditoria Quantitativa e do Benchmark:
- **Recálculo Independente 100% Reconciliado:** 250 casos totais, 91 acertos (36,40%), 159 divergências (63,60%), TP_DIRECT=26, FP_DIRECT=51, FN_DIRECT=34, Precisão=33,77%, Recall=43,33%, Taxa FP nas divergências=32,08%.
- **Qualidade do Benchmark (250 casos auditados individualmente):** 248 casos `REFERENCE_SUPPORTED` (99,20%), 2 casos `REFERENCE_AMBIGUOUS` (0,80% — P04 e P07), 0 casos com classificação incorreta ou tendenciosa. O benchmark é metodologicamente sólido, representativo e independente.
- **Independência Humana:** As classes de referência foram formalizadas e congeladas antes da execução do motor, atestadas pelo timestamp dos arquivos e SHA-256 inalterado.

### 2. Mapeamento Causal Linha-a-Linha no Runtime (`runtime.py`):
As 159 divergências foram investigadas e mapeadas em 5 Causas-Raiz Confirmadas (CR-01 a CR-05):
1. **CR-01 (Crítica — Falha Morfológica em Verbos Passivos/Pronominais com sufixo `-se`):** 31 casos (19,50% das divergências).
   - *Linhas afetadas:* 3082–3089 (`has_functional_action` e `self.functional_actions`).
   - *Mecanismo:* O método busca correspondência exata para formas ativas na 1ª pessoa ou infinitivo (`adiciono`, `configuro`). Verbos com pronome apassivador ou reflexivo (*Mapeia-se*, *Inclui-se*, *Interrompe-se*, *Grava-se*, *Impõe-se*) retornam `is_operative = False`, disparando `NON_OPERATIVE` na linha 3232 e rebaixando respostas corretas e formais para `OFF_TOPIC`.
2. **CR-02 (Crítica — Colapso Multiaspecto e Limitação Arbitrária de `PARTIAL`):** 35 casos (22,01% das divergências; Recall de PARTIAL = 0,0%).
   - *Linhas afetadas:* 2999–3007 (`decompose_question`) e 3202–3228 (`assess_nexus`).
   - *Mecanismo:* `decompose_question` divide perguntas apenas com base em 8 conjunções exatas em string (`" e como "`, etc.), colapsando perguntas multiaspecto com pontuação ou outros conectivos em `len(demands) == 1`. Em demandas únicas, a linha 3206 restringe `PARTIALLY_SOLVES` exclusivamente a perguntas contendo `"sharding"` e respostas com `"rebalanceamento"`. Para todas as demais perguntas, o nexus retorna unicamente `FUNCTIONALLY_SOLVES` (DIRECT) ou `NON_OPERATIVE` (OFF_TOPIC), tornando impossível prever `PARTIAL`.
3. **CR-03 (Alta — Ausência de Filtro de Suficiência Causal para Ações Auxiliares):** 12 casos (7,55% das divergências; FP de DIRECT).
   - *Linhas afetadas:* 2908–2911 (`self.auxiliary_markers`) e 3224–3225 (`assess_nexus`).
   - *Mecanismo:* Apenas Prometheus/Grafana foram cadastrados como auxiliares. Ações operacionais ativas que não resolvem o problema de raiz (ex.: habilitar cache Redis para lock distribuído, criar DLQ para deadlock, profiling, probes k8s) contêm verbos ativos e são indevidamente promovidas a `FUNCTIONALLY_SOLVES` (DIRECT).
4. **CR-04 (Alta — Falha de Flexão Verbal em Antíteses Destrutivas):** 12 casos (7,55% das divergências; FP de DIRECT).
   - *Linhas afetadas:* 2900–2905 (`self.antithesis_markers`) e 3192–3199 (`assess_nexus`).
   - *Mecanismo:* `self.antithesis_markers` lista apenas infinitivos nominais (`desativar transacoes`). Respostas com verbos conjugados (*"Desativo transações ACID"*, *"Removo os locks"*, *"Ignoro validação"*) escapam da antítese, encontram termos do domínio e são classificadas como `DIRECT`.
5. **CR-05 (Crítica — Acoplamento a Listas Fechadas de Substrings e Hipercorreção para `OFF_TOPIC`):** 42 casos (26,42% das divergências).
   - *Linhas afetadas:* 2879–2975 e 3231–3234.
   - *Mecanismo:* O motor depende de enumeração exaustiva de tuplas de strings estáticas. Qualquer formulação técnica conceitualmente correta fora das tuplas cai em `NON_OPERATIVE` e é rotulada como `OFF_TOPIC`, gerando a hipercorreção de 129 casos previstos como `OFF_TOPIC`.
6. **Desalinhamentos Semânticos Residuais e Fillers:** 27 casos (17,0% das divergências) divididos entre respostas vagas, semântica puramente associativa e fillers com termos de domínio.

### 3. Diagnóstico de Invariância (50,0% de Paridade):
- 5 dos 10 pares formal/informal divergiram devido exclusivamente ao defeito **CR-01**: a variante formal usou voz passiva sintética (*"Calcula-se o hash"*, *"Persiste-se o log"*) e caiu para `OFF_TOPIC`, enquanto a variante informal usou 1ª pessoa ativa (*"Calculo o hash"*, *"Persisto o log"*) e foi classificada como `DIRECT`.

### 4. Auditoria da Suíte de Testes Existente (Stages 31.7.8 e 31.7.11):
- A suíte de 1013 testes não detectou nenhuma dessas falhas devido ao **overfitting circular**: os testes utilizavam exclusivamente as mesmas tuplas de strings e verbos na 1ª pessoa cadastrados no runtime. Nenhum teste anterior continha verbos com `-se`, antíteses flexionadas na 1ª pessoa, ou perguntas multiaspecto fora do caso específico de sharding.

### 5. Diretrizes do Plano de Correção Conceitual (Stage 31.7.15):
- **Eixo 1:** Normalização morfológica flexional e de clíticos pronominais (`-se`, `-la`, `-lo`).
- **Eixo 2:** Decomposição sintática aberta de demandas com pontuação e cláusulas coordenadas, associada a cálculo proporcional de cobertura funcional.
- **Eixo 3:** Modelagem da hierarquia causal (Ação Causal Resolutiva vs Ação Auxiliar Operacional).
- **Eixo 4:** Desacoplamento de catálogos fechados de strings em prol de predicados funcionais generalizáveis.

### 6. Próxima Etapa:
- **Stage 31.7.15 — Controlled Correction Plan and Validation Contract** (CONCLUÍDO)
- O runtime `reference_runtime/runtime.py` deve permanecer estritamente congelado até que os contratos de validação e critérios formais sejam estabelecidos e aprovados.

---

# 66. REGISTRO DE TRANSIÇÃO — STAGE 31.7.15 (PLANO DE CORREÇÃO CONTROLADA E CONTRATOS DE VALIDAÇÃO)

- **Stage Concluído:** Stage 31.7.15 — Controlled Correction Plan and Validation Contract
- **Gate Emitido:** `GATE: CONTROLLED_CORRECTION_PLAN_COMPLETE`
- **Artefato Gerado:** `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/Stage 31.7.15 — Controlled Correction Plan and Validation Contract.md`
- **Runtime Hash Verificado (SHA-256):** `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E` (100% congelado e inviolado; 0 linhas de código alteradas).
- **Status do Runtime:** Congelamento Estrito Mantido.

### 1. Principais Entregas e Decisões Arquiteturais:
1. **Auditoria de Confiabilidade do Benchmark:**
   - Confirmada a precedência temporal dos rótulos e ausência de vazamento de dados no Stage 31.7.13.
   - Preservados os 250 casos originais como conjunto congelado histórico para medição de ganho relativo.
   - Estabelecida a criação de um segundo conjunto de validação cega independente (200 casos inéditos) para a revalidação final pós-correção.
2. **Contratos Comportamentais Formalizados (Contratos A a H):**
   - **Contrato A (Invariância Linguística):** Garante equivalência estrita entre voz ativa, passiva sintética com `-se`, passiva analítica e 3ª pessoa impessoal quando a proposição resolutiva for preservada (elimina CR-01).
   - **Contrato B (Cobertura Multiaspecto):** Decomposição sintática com pontuação e conectivos diversos; cálculo proporcional de cobertura; garantia de emissão de `PARTIAL` quando $0 < \text{cobertura} < 1.0$ (elimina CR-02).
   - **Contrato C (Suficiência Funcional):** Discriminação causal entre ações resolutivas de causa raiz e ações auxiliares operacionais (telemetria, profiling, DLQ genérica, probes), prevenindo promoção indevida a `DIRECT` (elimina CR-03).
   - **Contrato D (Polaridade e Antítese):** Normalização flexional para verbos de desativação na 1ª pessoa, imperativo ou pretérito (*"Desativo transações ACID"*, *"Removo locks"*), rejeitando como `OFF_TOPIC / CONTRADICTORY` (elimina CR-04).
   - **Contrato E (Domínio Aberto Estrutural):** Identificação de proposições através de triplas semânticas predicativas estruturais, desacoplando o motor de listas fechadas de substrings (elimina CR-05).
   - **Contratos F, G, H:** Separação estrita das 7 classes semânticas, desacoplamento entre status epistemológico e relevância, e invariância à extensão do texto (anti-verbosidade).
3. **Arquitetura de Correção em 8 Estágios Funcionais:**
   - `DemandInterpreter` -> `AspectDecomposer` -> `PropositionExtractor & MorphologicalNormalizer` -> `PolarityAuditor` -> `CausalSufficiencyEvaluator` -> `AspectCoverageAggregator` -> `EpistemicStatusEvaluator` -> `SemanticRelevanceClassifier & DecisionExplainer`.
4. **Métricas Quantitativas de Aceitação com Fórmulas Reconciliadas:**
   - Concordância Exata Global $\ge 75,0\%$.
   - Recall de DIRECT $\ge 85,0\%$; Precisão de DIRECT $\ge 70,0\%$.
   - Taxa de Falsos DIRECT nas divergências $\le 10,0\%$.
   - Recall de PARTIAL $\ge 60,0\%$.
   - Invariância de Representação (Grupo O) $\ge 80,0\%$.
   - Regressão na Suíte Canônica (1013 testes): 0 falhas (100% PASS).
5. **Plano de Implementação em 7 Incrementos Atômicos:**
   - Incremento 1: Normalização Morfológica e Clíticos Pronominais (`-se`, `-la`, `-lo`).
   - Incremento 2: Decomposição Sintática Multiaspecto e Cobertura Proporcional.
   - Incremento 3: Modelagem de Causalidade e Filtro de Suficiência para Ações Auxiliares.
   - Incremento 4: Auditoria de Polaridade e Antíteses Flexionadas.
   - Incremento 5: Desacoplamento Estrutural de Listas Fechadas e Generalização de Domínio Aberto.
   - Incremento 6: Consolidação de Invariância Epistêmica e de Extensão/Estilo.
   - Incremento 7: Execução da Suíte de Regressão, Harness Canônico e Validação Cega.

### 2. Próxima Etapa Recomendada:
- **Stage 31.7.16 — Controlled Implementation of the Approved Correction Plan** (CONCLUÍDO)
- Executar sequencialmente os 7 incrementos autorizados, validando a regressão canônica e aplicando a suíte adversarial a cada passo, mantendo preservados os artefatos congelados.

---

# 67. REGISTRO DE TRANSIÇÃO — STAGE 31.7.16 (IMPLEMENTAÇÃO CONTROLADA DO PLANO DE CORREÇÃO APROVADO)

- **Stage Concluído:** Stage 31.7.16 — Controlled Implementation of the Approved Correction Plan
- **Gate Emitido:** `GATE: CONTROLLED_IMPLEMENTATION_COMPLETE_PENDING_BLIND_VALIDATION`
- **Artefato Gerado:** `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/Stage 31.7.16 — Controlled Implementation of the Approved Correction Plan.md`
- **Runtime Hash Inicial Verificado (SHA-256):** `5545C47ECD92C04265CA3FFB46266FDE814CC564B2F69CA91E4B230CBE04BF3E`
- **Runtime Hash Final Candidato (SHA-256):** `AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB`
- **Status do Runtime Candidato:** Congelado para Revalidação Cega Independente.

### 1. Principais Implementações Realizadas:
1. **Incremento 1 (CTR-SEM-A / CR-01):** Normalização morfológica flexional e de clíticos pronominais (`_normalize_morphology` e expansão de radicais em `operative_verbs`), garantindo invariância perfeita entre voz ativa, passiva sintética com `-se`, analítica e 3ª pessoa impessoal.
2. **Incremento 2 (CTR-SEM-B / CR-02):** Decomposição aberta de demandas multiaspecto em `decompose_question` com ampla gama de conectivos, mapeamento para `UNMET_DEMAND` para demandas secundárias não cobertas e identificação de omissões explícitas no texto (*"não detalha"*, *"não explica"*).
3. **Incremento 3 (CTR-SEM-C / CR-03):** Expansão do catálogo de telemetria/observabilidade em `auxiliary_markers` (Datadog, Dynatrace, New Relic, Sentry, Elasticsearch, Kibana, CloudWatch, Blackbox Exporter, Micrometer, Pyroscope, Probes de liveness) e separação causal contextual: demandas de contenção/resolução de falha operacional recebem `CONTRIBUTES_TO` (`SUPPORTING`), enquanto perguntas explicitamente diagnósticas recebem `DIRECT`.
4. **Incremento 4 (CTR-SEM-D / CR-04):** Método `_detect_antithesis` combinando marcadores estáticos e expressões regulares de flexões destrutivas (`desativ-`, `remov-`, `sem timeout loops infinitos`, etc.) mapeando ações que eliminam proteções operacionais para `OFF_TOPIC` (`ANTITHESIS_OPPOSED`).
5. **Incremento 5 (CTR-SEM-E / CR-05):** Separação de domínios ortogonais (CSS/Tailwind/Webpack, IA/ML Scikit-Learn/PyTorch, DevOps Dockerfile) com limites de palavra (`\b`) para evitar falsos positivos lexicais, e aceitação de tecnologias inéditas/fictícias com mecanismos funcionais.
6. **Incremento 6 (CTR-SEM-F, G, H):** Consolidação das 7 classes semânticas sem fallbacks silenciosos, preservação estrita de que declarações de experiência sem mecanismo avaliem como `RELATED`, e invariância total à extensão do texto (anti-verbosidade).
7. **Incremento 7 (Regressão Canônica e Reference Harness):**
   - Suíte Canônica: **1.024 testes executados, 1.023 aprovados, 0 falhas, 0 erros, 1 ignorado (`OK (skipped=1)`)**.
   - Reference Harness: **`REFERENCE HARNESS: PASS_WITH_WARNINGS (8/8 suites, 0 failed)`**.

### 2. Resultados no Benchmark Histórico de 250 Casos:
- **Concordância Global Exata:** 165/250 (**66,00%** vs 36,40% histórico — ganho de +29,60% abs).
- **Recall de DIRECT:** 55/60 (**91,67%** vs 43,33% histórico — critério $\ge 85\%$ atingido).
- **Invariância de Representação (Grupo O):** 10/10 pares (**100,0%** vs 30,0% histórico — critério $\ge 80\%$ atingido).
- **Recall de PARTIAL:** 19/35 (**54,29%** vs 0,00% histórico — superação da barreira de colapso).
- **Recall de SUPPORTING:** 21/30 (**70,00%** vs 3,33% histórico).
- **Recall de OFF_TOPIC:** 40/50 (**80,00%** mantido com robustez).

### 3. Próxima Etapa Recomendada:
- **Stage 31.7.17 — Independent Blind Semantic Revalidation of the Corrected Runtime** (CONCLUÍDO)
- Executar a validação cega independente da versão candidata congelada (`AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB`) sobre o conjunto reservado de 200 casos inéditos e independentes, homologando formalmente a generalização em domínio aberto.

---

# 68. REGISTRO DE TRANSIÇÃO — STAGE 31.7.17 (REVALIDAÇÃO SEMÂNTICA CEGA E INDEPENDENTE DO RUNTIME CORRIGIDO)

- **Stage Concluído:** Stage 31.7.17 — Independent Blind Semantic Revalidation of the Corrected Runtime
- **Gate Emitido:** `GATE: BLIND_SEMANTIC_REVALIDATION_BLOCKED`
- **Artefato Gerado:** `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/Stage 31.7.17 — Independent Blind Semantic Revalidation of the Corrected Runtime.md`
- **Runtime Congelado Auditado (SHA-256):** `AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB` (100% íntegro, nenhuma linha alterada)
- **Artefatos do Benchmark Selados:**
  - `stage_31_7_17_ground_truth.json`: `EDE7B2A93EE3A9B7A0920D77780FBC331F9BB488622432E03FD30C4C9731C7FD` (175.174 B)
  - `stage_31_7_17_blind_input.json`: `4CE1ADF0EE197A0C0FA8A88F740F4EFA6F3A14FB360249579F4CFC1B19B6E576` (69.666 B)
  - `stage_31_7_17_system_predictions.json`: `E42A5709A03D96F52FF60CF29FFAD7CD14FF969330F3E9F84C5752BD21F70AAB` (108.461 B)
  - `stage_31_7_17_metrics_summary.json`: `E7A31D2D09BF799DB01F9EC70FFA77823B666AB61F69257740610542C86CB0BF` (80.489 B)

### 1. Resultados Quantitativos e Avaliação dos Critérios de Aceitação:

| Métrica | Critério Alvo | Resultado Obtido | Status |
|---|:---:|:---:|:---:|
| **Concordância Exata** | $\ge 75,0\%$ | **62,00%** (124/200) | **FALHOU** |
| **Recall de DIRECT** | $\ge 85,0\%$ | **88,89%** (40/45) | **APROVADO** |
| **Precisão de DIRECT** | $\ge 70,0\%$ | **47,62%** (40/84) | **FALHOU** |
| **Falsos DIRECTs entre Divergências** | $\le 10,0\%$ | **57,89%** (44/76) | **FALHOU** |
| **Recall de PARTIAL** | $\ge 60,0\%$ | **45,71%** (16/35) | **FALHOU** |
| **Invariância de Representação** | $\ge 80,0\%$ | **61,54%** (8/13 pares) | **FALHOU** |
| **Regressão Canônica** | 0 falhas | **0 falhas** (1.024 testes OK, Harness 8/8) | **APROVADO** |

### 2. Matriz de Confusão Completa (7x7):

```text
REF \ PRED          DIRECT     PARTIAL  SUPPORTING     RELATED   OFF_TOPICINSUFFICIENT     UNKNOWN   TOTAL
----------------------------------------------------------------------------------------------------------
DIRECT                  40           0           1           1           3           0           0      45
PARTIAL                 14          16           0           0           5           0           0      35
SUPPORTING               0           0          24           0           1           0           0      25
RELATED                 15           0           0           7           8           0           0      30
OFF_TOPIC                7           0           0           0          28           0           0      35
INSUFFICIENT             2           0           0           1           2           9           4      18
UNKNOWN                  6           0           0           2           4           0           0      12
----------------------------------------------------------------------------------------------------------
PRED TOTAL              84          16          25          11          51           9           4     200
```

### 3. Diagnóstico Semântico e Causas-Raiz Principais:
1. **Hipertrofia de Falsos DIRECTs (44 casos / 57,89% das divergências):**
   - 14 casos de `PARTIAL` promovidos a `DIRECT`: falha em conjunção estrita para demandas secundárias omitidas.
   - 15 casos de `RELATED` promovidos a `DIRECT`: confusão entre descrição histórica/institucional de produtos/tecnologias e mecanismo técnico resolutivo.
   - 7 casos de `OFF_TOPIC` promovidos a `DIRECT`: vazamento léxico em antíteses destrutivas flexionadas e palavras soltas em domínios alienígenas.
   - 6 casos de `UNKNOWN` (tautologias circulares) promovidos a `DIRECT`: repetição de termos da pergunta confundida com explicação substantiva.
   - 2 casos de `INSUFFICIENT` promovidos a `DIRECT`: frases completas de evasão orçamentária/consultoria sem conteúdo técnico.
2. **Colapso em Detecção de Tautologias (0% de acerto em UNKNOWN):**
   - Todos os 12 casos de tautologia circular foram mal classificados por ausência de um módulo analisador de circularidade semântica.
3. **Quebra de Invariância de Representação (61,54%):**
   - Expressões informais e gírias causaram rebaixamento indevido de respostas corretas para `OFF_TOPIC` e `RELATED`.

### 4. Próxima Etapa Recomendada:
- **Stage 31.7.18 — Root Cause Analysis & Architecture Remediation for Propositional Precision, Tautology Detection and Demand Conjunctive Satisfaction**
- Nenhuma alteração no runtime deve ser implementada antes da conclusão formal desta RCA e da formulação do plano de correção controlado.





