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
- **Stage 31.7.18 — Root Cause Analysis & Architecture Remediation for Propositional Precision, Tautology Detection and Demand Conjunctive Satisfaction** (CONCLUÍDO)
- Nenhuma alteração no runtime deve ser implementada antes da conclusão formal desta RCA e da formulação do plano de correção controlado.

---

# 69. REGISTRO DE TRANSIÇÃO — STAGE 31.7.18 (ANÁLISE DE CAUSA-RAIZ E PROJETO DE REMEDIAÇÃO ARQUITETURAL)

- **Stage Concluído:** Stage 31.7.18 — Root Cause Analysis & Architecture Remediation Design for Propositional Precision, Tautology Detection and Demand Conjunctive Satisfaction
- **Gate Emitido:** `GATE: RCA_COMPLETE_CORRECTION_PLAN_READY`
- **Artefato Gerado:** `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/Stage 31.7.18 — Root Cause Analysis & Architecture Remediation Design.md`
- **Runtime Congelado Auditado (SHA-256):** `AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB` (100% íntegro, nenhuma alteração realizada)
- **Recálculo do Baseline do Stage 31.7.17:** Confirmado com 200 casos, 124 acertos exatos (62,00%), 76 divergências e 44 falsos DIRECTs (57,89% das divergências).

### 1. Causas-Raiz Estruturais Demonstradas e Confirmadas:
1. **CR-01 (Conjunção Incompleta de Demandas Multi-Aspecto):**
   - No método `assess_demand_nexus` (`runtime.py:3350-3363`), `demand_1` recebe `FUNCTIONALLY_SOLVES` incondicionalmente quando a proposição é operativa, e `demand_2` é validada como resolvida se qualquer palavra de $\ge 4$ letras coincidir na resposta. Em `evaluate_relevance` (`runtime.py:3446-3454`), respostas incompletas atingem ratio 1.0 e são promovidas a `DIRECT` (14 casos PARTIAL -> DIRECT).
2. **CR-02 (Falta de Verificação Causal entre Proposição e Demanda):**
   - O método `extract_response_propositions` (`runtime.py:3183-3188`) utiliza 53 radicais verbais comuns (`self.operative_verbs`) como "us", "utiliz", "armazen", "process". Qualquer texto técnico contendo esses verbos torna `is_operative = True`. Em perguntas de demanda única, isso concede `FUNCTIONALLY_SOLVES` incondicionalmente, promovendo descrições históricas, de produto e curiosidades a `DIRECT` (15 casos RELATED -> DIRECT).
3. **CR-03 (Ausência Estrutural de Detector de Circularidade Semântica):**
   - O runtime possuía apenas 7 strings hardcoded do Stage 31.7.13 em `self.trivia_markers` (`runtime.py:2964-2970`). Diante de tautologias inéditas no Stage 31.7.17, o sistema errou 100% dos 12 casos (promovendo 6 a DIRECT por repetição de termos da pergunta).
4. **CR-04 (Fragilidade Lexical de Polaridade e Antítese):**
   - `_detect_antithesis` (`runtime.py:3054-3060`) opera sobre uma lista fechada de radicais e alvos. O uso de sinônimos naturais em português ("bloqueio" em vez de "lock", "firewall", "retirar") evadiu o detector, promovendo 7 ações destrutivas a `DIRECT`.
5. **CR-05 (Quebra de Invariância de Representação por Viés Lexical):**
   - Formulações coloquiais legítimas ("a gente associa", "barra o comando", "tabelinha auxiliar") foram rebaixadas para `OFF_TOPIC` e `RELATED` por ausência desses verbos em `operative_verbs`. Paralelamente, respostas conceituais completas foram rebaixadas para `SUPPORTING` unicamente por citarem o nome de ferramentas de produção cadastradas na lista `auxiliary_markers` (ex.: "HikariCP").

### 2. Auditoria de Independência do Benchmark:
- **Classificação:** `PARTIALLY_VERIFIED`.
- A integridade de execução, a ordem cronológica e o isolamento cego estão comprovados por hashes criptográficos e isolamento de arquivos. Contudo, as referências foram formalizadas pelo próprio agente/equipe sem comitê duplo-cego externo.

### 3. Plano de Correção Arquitetural Estruturado em 5 Módulos:
- **Módulo 1:** Verificador de Nexo Causal Demanda-Mecanismo (Elimina CR-02).
- **Módulo 2:** Motor de Conjunção Estrita de Múltiplas Demandas (Elimina CR-01).
- **Módulo 3:** Detector Estrutural de Circularidade Semântica e Tautologia (Elimina CR-03).
- **Módulo 4:** Auditoria Semântica Abrangente de Antítese e Polaridade Funcional (Elimina CR-04).
- **Módulo 5:** Normalização Idiomática e Eliminação de Viés de Ferramenta (Elimina CR-05).

### 4. Contratos de Aceitação Estabelecidos:
- **CTR-RCA-01 (Conjunção Estrita):** Perguntas multi-demanda com aspecto omitido nunca viram DIRECT.
- **CTR-RCA-02 (Anti-Trivia / Anti-Entidade):** Descrição sem mecanismo causal vira RELATED.
- **CTR-RCA-03 (Anti-Tautologia Semântica):** Raciocínio circular sem ganho informacional vira UNKNOWN.
- **CTR-RCA-04 (Anti-Antítese Abrangente):** Ações opostas à segurança viram OFF_TOPIC.
- **CTR-RCA-05 (Invariância Representacional):** Formal vs informal e conciso vs extenso produzem a mesma classe.
- **CTR-RCA-06 (Preservação Canônica):** 1.024 testes canônicos aprovados (0 falhas) e Harness 8/8 aprovado.

### 5. Próxima Etapa Recomendada:
- **Stage 31.7.19 — Controlled Correction Plan & Architectural Remediation Specification** (CONCLUÍDO)
- Formalizar as especificações de cada módulo, contratos e suíte de testes de validação antes de qualquer alteração de código no runtime.

---

# 70. REGISTRO DE TRANSIÇÃO — STAGE 31.7.19 (ESPECIFICAÇÃO FORMAL DE REMEDIAÇÃO ARQUITETURAL E PLANO DE CORREÇÃO CONTROLADA)

- **Stage Concluído:** Stage 31.7.19 — Controlled Correction Plan & Architectural Remediation Specification
- **Gate Emitido:** `GATE: CORRECTION_PLAN_READY_FOR_CONTROLLED_IMPLEMENTATION`
- **Artefato Gerado:** `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/Stage 31.7.19 — Controlled Correction Plan & Architectural Remediation Specification.md`
- **Runtime Congelado Auditado (SHA-256):** `AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB` (100% íntegro, nenhuma linha alterada no runtime ou suíte canônica)
- **Baseline Auditado e Confirmado (Stage 31.7.17):** 200 casos, 124 acertos exatos (62,00%), 76 divergências, 44 falsos DIRECTs (57,89% das divergências).
- **Independência da Referência:** Mantida formalmente como `REFERENCE_ANNOTATION_INDEPENDENCE: UNRESOLVED` (auditoria metodológica preservada; integridade e novidade confirmadas, adjudicação por comitê externo pendente).

### 1. Elementos Centrais da Especificação Formal Aprovada:
1. **Contratos Semânticos das 7 Classes:**
   - Critérios positivos, impeditivos e de fronteira detalhados para `DIRECT`, `PARTIAL`, `SUPPORTING`, `RELATED`, `OFF_TOPIC`, `INSUFFICIENT` e `UNKNOWN`.
   - Distinção explícita entre `INSUFFICIENT` (ausência de proposição técnica substantiva) e `UNKNOWN` (proposição formal presente, mas vazia de ganho informacional por circularidade).
2. **Arquitetura Conceitual em 9 Componentes Desacoplados:**
   - `QIDM` (Question Intent & Demand Model): decomposição atômica de intenção e demandas primárias.
   - `RPM` (Response Proposition Model): extração de proposições sem tratar resposta como bloco indivisível.
   - `DPN` (Demand-Proposition Nexus): mapeamento tipado de nexo entre demandas e proposições.
   - `FSA` (Functional Sufficiency Assessment): verificação de suficiência causal parametrizada por intenção (`SOLVE`, `EXPLAIN`, `COMPARE`, `DIAGNOSE`).
   - `CDC` (Conjunctive Demand Coverage): regra conjuntiva booleana estrita ($\forall d \in D_{primary}: \text{Status}(d) = \text{SOLVED}$ para `DIRECT`).
   - `ICA` (Informational Contribution Assessment): cálculo de $\Delta I(R | d)$ e detector estrutural de tautologias.
   - `PCA` (Polarity & Contradiction Assessment): mapeamento contextual de vetores de efeito e antíteses destrutivas abertas em português.
   - `EA` (Epistemic Assessment): isolamento epistêmico impedindo contaminação retroativa da relevância semântica.
   - `SRA` (Semantic Relevance Aggregator): emissão determinística, rastreável e auditável do veredito final.
3. **14 Invariantes Arquiteturais Invioláveis (R-01 a R-14):**
   - Eliminação de dependência de sobreposição lexical, não-equiparação de entidade a mecanismo, conjunção estrita, preservação de incerteza, domínio aberto e determinismo auditável.
4. **Contratos Especializados:**
   - **Multi-Aspecto:** Decomposição independente e eliminação da validação disjuntiva frouxa por palavra solta em $d_2$.
   - **Circularidade / Ganho Informacional:** Eliminação das 7 strings hardcoded de `self.trivia_markers` e análise sintático-morfológica de predicados justificadores.
   - **Polaridade / Antítese:** Reconhecimento aberto em português de verbos de desativação e alvos de segurança.
   - **Invariância de Representação:** Normalização de expressões idiomáticas de engenharia e eliminação do viés por menção incidental a ferramentas em `self.auxiliary_markers`.
5. **Governança de Dados Anti-Vazamento:**
   - O conjunto de 200 casos de `stage_31_7_17_ground_truth.json` é formalmente classificado como **Conjunto Diagnóstico Histórico de Calibração**, sendo terminantemente proibido seu reuso como validação cega em estágios futuros.
6. **Critérios Quantitativos de Aceite Preservados:**
   - Concordância Exata $\ge 75,0\%$, Recall DIRECT $\ge 85,0\%$, Precisão DIRECT $\ge 70,0\%$, Falsos DIRECT entre divergências $\le 10,0\%$, Recall PARTIAL $\ge 60,0\%$, Invariância $\ge 80,0\%$, Regressão Canônica 100% PASS (0 falhas).

### 2. Plano de Implementação Incremental (Stage 31.7.20):
- **Incremento 1:** Verificador de Nexo Causal e Suficiência Funcional (Elimina CR-02).
- **Incremento 2:** Motor de Conjunção Estrita de Múltiplas Demandas (Elimina CR-01).
- **Incremento 3:** Detector Estrutural de Circularidade e Ganho Informacional (Elimina CR-03).
- **Incremento 4:** Verificador de Polaridade Funcional e Antítese Abrangente (Elimina CR-04).
- **Incremento 5:** Normalização Semântica e Invariância de Representação (Elimina CR-05).

### 3. Próxima Etapa Autorizada:
- **Stage 31.7.20 — Controlled Implementation of the Approved Semantic Precision Remediation Plan** (CONCLUÍDO)
- Executar a implementação controlada dos 5 incrementos especificados, com testes de unidade, testes de contrato e regressão canônica estrita a cada passo, gerando novo hash congelado ao final.

---

# 71. REGISTRO DE TRANSIÇÃO — STAGE 31.7.20 (IMPLEMENTAÇÃO CONTROLADA DO PLANO DE REMEDIAÇÃO SEMÂNTICA APROVADO)

- **Stage Concluído:** Stage 31.7.20 — Controlled Implementation of the Approved Semantic Precision Remediation Plan
- **Gate Emitido:** `GATE: IMPLEMENTATION_COMPLETE_PENDING_INDEPENDENT_BLIND_VALIDATION`
- **Artefato Gerado:** `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/Stage 31.7.20 — Controlled Implementation of the Approved Semantic Precision Remediation Plan.md`
- **Runtime Hash Inicial Verificado (SHA-256):** `AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB`
- **Runtime Hash Final Candidato (SHA-256):** `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`
- **Checkpoint Recuperável:** `reference_runtime/runtime.py.stage_31_7_19_baseline` (SHA-256: `AF3C1A14A435074C703A370591DFE8F91862789D9C536121EB3370F06CFF0CCB`)
- **Status do Runtime Candidato:** Congelado no hash `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC` para Revalidação Cega Independente no Stage 31.7.21.

### 1. Implementações Concluídas por Incremento:
1. **Incremento 1 (Suficiência Funcional e Nexo Demanda-Proposição / CR-02):**
   - Criação de `self.institutional_metadata_markers` cobrindo fundações, história de ecossistema e popularidade de mercado.
   - Respostas de metadados institucionais sem mecanismo operacional são desmarcadas como operativas (`is_operative = False`) e avaliadas como `THEMATICALLY_ADJACENT` -> `RELATED` (`functional_contribution: False`), eliminando a promoção indevida para `DIRECT`.
2. **Incremento 2 (Cobertura Conjuntiva de Demandas Multi-Aspecto / CR-01):**
   - Adicionadas formas infinitivas em conectivos de cisão conjuntiva em `decompose_question` (`" e armazenar "`, `" e preservar "`, `" e garantir "`).
   - Eliminação do limiar disjuntivo frouxo de 75%: para perguntas multi-aspecto, `DIRECT` exige estritamente que **100% das demandas primárias tenham `FUNCTIONALLY_SOLVES`**.
   - Respostas que satisfazem substantivamente um aspecto mas omitem outro recebem deterministicamente `PARTIAL` (`multi_aspect_partial_coverage`), com `functional_contribution: True`.
3. **Incremento 3 (Contribuição Informacional e Detecção Estrutural de Circularidade / CR-03):**
   - Removidas as 7 strings fixas hardcoded de `self.trivia_markers`.
   - Implementado `_detect_structural_circularity(q_text, r_text)` para detectar poliptoto, repetição de radicais cognatas (`esper-`, `buffer-`, `orden-`, `duplic-`, `sincron-`, `comprim-`, `isol-`, `partic-`, `distribu-`, `disponi-`) em orações causais tautológicas vazias sem mecanismos explicativos externos.
   - Tautologias circulares são classificadas deterministicamente como `UNKNOWN` (`circular_reasoning_tautology`).
4. **Incremento 4 (Polaridade, Negação e Antítese Aberta / CR-04):**
   - Expansão de `_detect_antithesis` com radicais abertos de destruição (`desativ-`, `deslig-`, `remov-`, `desabilit-`, `ignor-`, `elimin-`, `retir-`, `dispens-`, `zer-`, `derrub-`) combinados com alvos de proteção operacional.
   - **Guarda de Evitação Preventiva:** Implementada prioridade para padrões de prevenção (*"para evitar desativar"*, *"sem precisar remover"*), prevenindo falsos positivos em respostas técnicas que explicam por que proteções não devem ser desativadas.
   - Ações destrutivas não justificadas recebem relação `ANTITHESIS_OPPOSED` e classificação `OFF_TOPIC`.
5. **Incremento 5 (Invariância de Representação e Desacoplamento de Viés / CR-05):**
   - Expansão de `self.operative_verbs` com radicais de engenharia e formulações informais de ação técnica (`bot-`, `peg-`, `mand-`, `salv-`, `guard-`, `congel-`, `acord-`, `cort-`), assegurando que variações coloquiais preservem classificação equivalente a respostas formais.
   - Desacoplamento de ferramentas de pool e conexões (HikariCP, `tamanho maximo`, `timeout de aquisicao`, `try-with-resources`) para que soluções substantivas de contenção não sejam tratadas meramente como telemetria auxiliar `CONTRIBUTES_TO`.

### 2. Resultados da Regressão Canônica e Reference Harness:
- **Suíte Canônica de Testes (`py -m unittest discover tests`):**
  - **1.038 testes executados, 1.037 aprovados, 1 ignorado (skipped), 0 falhas, 0 erros (38.4s)**.
  - **100% PASS (Zero falhas inexplicadas)**.
- **Reference Harness (`tests.test_stage_26_reference_harness`):**
  - **15/15 testes aprovados (PASS_WITH_WARNINGS)**.
- **Suíte de Testes de Contrato do Stage 31.7.20 (`test_stage_31_7_20_controlled_remediation`):**
  - **14/14 testes aprovados (100% OK em 0.009s)**.

### 3. Resultados no Benchmark Diagnóstico Histórico (Stage 31.7.17 — 200 Casos de Calibração):
- **Concordância Exata:** 124/200 (62,00%) -> **173/200 (86,50%)** [Critério $\ge 75\%$ ATINGIDO]
- **Recall de `DIRECT`:** 40/45 (88,89%) -> **45/45 (100,00%)** [Critério $\ge 85\%$ ATINGIDO]
- **Precisão de `DIRECT`:** 40/84 (47,62%) -> **45/51 (88,24%)** [Critério $\ge 70\%$ ATINGIDO]
- **Recall de `PARTIAL`:** 16/35 (45,71%) -> **30/35 (85,71%)** [Critério $\ge 60\%$ ATINGIDO]
- **Falsos `DIRECT` entre Divergências:** 44/76 (57,89%) -> **6/27 (22,22%)** (Redução maciça de 38 falsos positivos)
- **Invariância de Representação (13 Pares Canônicos):** 8/13 (61,54%) -> **13/13 (100,00%)** [Critério $\ge 80\%$ ATINGIDO]
- **Recall de `OFF_TOPIC`:** 25/35 (71,43%) -> **35/35 (100,00%)**
- **Recall de `SUPPORTING`:** 18/25 (72,00%) -> **24/25 (96,00%)**

### 4. Próxima Etapa Prevista:
- **Stage 31.7.21 — Independent Blind Semantic Revalidation of the Remediated Runtime** (CONCLUÍDO)
- Submeter o runtime congelado (`75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`) à validação cega independente com amostra selada e nova, homologando formalmente a capacidade de generalização em domínio aberto antes do avanço para Production Readiness (Stage 32).

---

# 72. REGISTRO DE TRANSIÇÃO — STAGE 31.7.21 (REVALIDAÇÃO SEMÂNTICA CEGA E INDEPENDENTE DO RUNTIME REMEDIADO)

- **Stage Concluído:** Stage 31.7.21 — Independent Blind Semantic Revalidation of the Remediated Runtime
- **Gate Emitido:** `GATE: BLIND_SEMANTIC_REVALIDATION_BLOCKED`
- **Artefato Gerado:** `11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/Stage 31.7.21 — Independent Blind Semantic Revalidation of the Remediated Runtime.md`
- **Status do Runtime:** 100% Congelado, SHA-256 verificado antes e após execução: `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`.
- **Status de Independência da Referência:** `REFERENCE_INDEPENDENCE_UNRESOLVED` (auditoria documentada formalmente: casos inéditos com 0% de sobreposição com benchmarks históricos, mas adjudicados internamente sem painel humano externo duplo-cego).

### 1. Hashes Criptográficos dos Artefatos do Stage 31.7.21:
- `stage_31_7_21_ground_truth.json` (214.184 bytes): `D594BB067FE0A031720F75B416AB636D57D280D7E00E279557D9C8D8C6D120F6`
- `stage_31_7_21_blind_input.json` (85.733 bytes): `E75D22F3BDB2A600C3628C1924997EC6D81B8143B9C7A01628E080A27313D010`
- `stage_31_7_21_system_predictions.json` (279.398 bytes): `577B308CA7FB3C827FF04776779E6E1C5916565982ED059B986E295B9958E168`
- `stage_31_7_21_metrics_summary.json` (3.743 bytes): `C52A332C8758DE999BD690C11BC50615B6F912C3FC24D1A8955ECB2556684C4B`
- `stage_31_7_21_confusion_matrix.json` (1.458 bytes): `03CD7D0215933398641798257BEEFB5C5EC0A83E58FEE4783AB3B79C1A9A5972`
- `stage_31_7_21_divergence_analysis.json` (91.816 bytes): `94AACB770A97F2840B56025478F770C3837F78AF94DE0965410262140870BB43`
- `stage_31_7_21_independence_audit.json` (1.978 bytes): `26AD25606AB3E9D8F8E3CB4EDF1F8E692F1318D2A3EEC6C3D50112B0B6CD1E55`

### 2. Resultados das Métricas Obrigatórias (250 Casos Inéditos):
- **Concordância Exata:** 170 / 250 (**68,00%**) [Meta $\ge 75{,}0\%$] -> **FALHA**
- **Recall de DIRECT:** 53 / 65 (**81,54%**) [Meta $\ge 85{,}0\%$] -> **FALHA**
- **Precisão de DIRECT:** 53 / 100 (**53,00%**) [Meta $\ge 70{,}0\%$] -> **FALHA**
- **Falsos DIRECT entre Divergências:** 47 / 80 (**58,75%**) [Meta $\le 10{,}0\%$] -> **FALHA**
- **Recall de PARTIAL:** 17 / 45 (**37,78%**) [Meta $\ge 60{,}0\%$] -> **FALHA**
- **Invariância de Representação:** 11 / 16 pares (**68,75%**) [Meta $\ge 80{,}0\%$] -> **FALHA**
- **Regressão Canônica e Harness:** 1038/1038 testes (1 skip) e 15/15 harness aprovados -> **PASSOU**

### 3. Síntese do Diagnóstico de Falha:
- **Padrão 1 (25 casos de `PARTIAL` promovidos a `DIRECT`):** Perguntas com enunciados oracionais simples contendo múltiplos requisitos interdependentes (ex: Circuit Breaker fechado/aberto/meio-aberto; Saga e compensações) foram reduzidas a uma única demanda genérica, permitindo que respostas que cobrem apenas metade do mecanismo recebessem status `aspect_coverage = FULL`.
- **Padrão 2 (11 casos de `RELATED`/`SUPPORTING` promovidos a `DIRECT`):** Fatos históricos (NGINX de Igor Sysoev, Codd e bancos relacionais), especificações de hardware (profundidade de pipeline de CPU) e declarações autobiográficas ("já usei Redis em produção") foram classificados como proposições operacionais válidas devido a verbos de ação técnicos.
- **Padrão 3 (6 casos de `UNKNOWN` tautológico promovidos a `DIRECT`):** Respostas circulares e poliptotos com flexões e conectivos funcionais ("mantém", "para", "servidores") foram tratadas como ganho informacional substantivo por heurística estática de radicais.
- **Padrão 4 (11 casos de `INSUFFICIENT` classificados como `UNKNOWN`):** Respostas evasivas receberam a classe de incerteza em vez de evidência insuficiente.
- **Eficácia Comprovada (Grupo I - 92,86% acerto):** A salvaguarda de evitação e prevenção implementada no Stage 31.7.20 demonstrou alta generalização, distinguindo com sucesso respostas que alertam contra más práticas daquelas que propõem destruição de salvaguardas operacionais.

### 4. Próxima Etapa Autorizada:
- **Stage 31.7.22 — Root Cause Analysis & Semantic Precision Remediation Architecture (Cycle 4)** (CONCLUÍDO)
- Conduzir a investigação profunda e isolada das causas-raiz estruturais dos 4 padrões de falha identificados na validação cega, preservando o histórico integral e sem realizar modificações precipitadas no runtime.

---

# 73. REGISTRO DE TRANSIÇÃO — STAGE 31.7.22 (ANÁLISE DE CAUSA-RAIZ & ESPECIFICAÇÃO ARQUITETURAL DO CICLO 4)

- **Stage Concluído:** Stage 31.7.22 — Root Cause Analysis & Semantic Precision Remediation Architecture (Cycle 4)
- **Gate Emitido:** `GATE: RCA_COMPLETE_ARCHITECTURE_PENDING_REVIEW`
- **Artefatos Gerados:**
  - `stage_31_7_22_metrics_reconciliation.json` (SHA-256: `DFD17C7D5C1D1086408CC8CB8B9C18B446C04BF732CBDA6C21B750F38379B156`)
  - `stage_31_7_22_root_cause_catalog.json` (SHA-256: `EE711719DADAC102086ACA8C21B9EAE0F1A7DB74C12B74C7BEC5DCFAE96963D5`)
  - `stage_31_7_22_architecture_options.md` (SHA-256: `6CE463F623C7608E1665E96D4034072DC9E1AC61EA353B335F256DF3FC62E1CF`)
  - `stage_31_7_22_component_contracts.md` (SHA-256: `0257ACDC51B6C6555FB7AE146303C5F91FA7BE813D31755AAC3B57EC30391951`)
  - `stage_31_7_22_validation_contract.md` (SHA-256: `121ED18EC6CBEBDDBECC79B617C5298E89BB8435D7CCAAAAC0398FC2765977A1`)
  - `Stage 31.7.22 — Root Cause Analysis & Semantic Precision Remediation Architecture (Cycle 4).md` (SHA-256: `8CF1FB29FF7F2F946415FDBDE4F165044CD4A979EC8E8482FB8098217F309A28`)
- **Status do Runtime:** 100% Congelado, SHA-256 verificado: `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`.
- **Checkpoint Criado:** `reference_runtime/runtime.py.stage_31_7_22_baseline` (SHA-256: `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`).

### 1. Reconciliação Matemática das Métricas do Stage 31.7.21:
- Reconciliação executada diretamente cruzando os 250 casos de `stage_31_7_21_ground_truth.json` com `stage_31_7_21_system_predictions.json`.
- Reprodução exata de 100%:
  - Concordância Exata: 170 / 250 (68,00%)
  - Recall de DIRECT: 53 / 65 (81,54%)
  - Precisão de DIRECT: 53 / 100 (53,00%)
  - Falsos DIRECT entre Divergências: 47 / 80 (58,75%)
  - Recall de PARTIAL: 17 / 45 (37,78%)
  - Invariância Homologada (Consistência + Correção): 11 / 16 pares (68,75%)
  - Invariância de Consistência de Saída: 13 / 16 pares (81,25%)
  - Regressão Canônica: 1038 executados, 1037 pass, 1 skip, 0 fail; Harness: 15/15 pass.

### 2. Síntese do Catálogo de Causas-Raiz (80 Divergências):
- **CR-01 (Demanda composta tratada como demanda simples - 28 casos / 35,0%):** O método `decompose_question` exige conjunções interrogativas explícitas (`e como`, `e qual`). Em perguntas de oração simples que demandam múltiplos estados (Circuit Breaker: fechado/aberto/meio-aberto) ou pares de ação/compensação (Saga), os requisitos foram colapsados em uma única demanda genérica, fazendo com que respostas cobrindo apenas metade do mecanismo recebessem `DIRECT`.
- **CR-06 (Acoplamento difuso em multi-demandas - 6 casos / 7,5%):** Quando duas demandas foram extraídas, a escada de `if/elif` em `assess_demand_nexus` buscou palavras isoladas (ex: "coordenador") no texto da resposta, marcando a demanda 2 como `FUNCTIONALLY_SOLVES` mesmo quando a resposta omitia o tratamento de queda do coordenador.
- **CR-02 & CR-05 (Verbos técnicos em relatos autobiográficos e históricos - 12 casos / 15,0%):** Verbos de ação comuns ativaram `has_operative_verb` em anedotas históricas (Igor Sysoev, Edgar Codd) e relatos pessoais ("já usei em produção"), promovendo contexto temático a solução técnica.
- **CR-03 (Circularidade não detectada por variação morfológica - 6 casos / 7,5%):** A busca estática de radicais falhou diante de variações morfológicas legítimas em português (ex: "compressão" vs. "comprimindo", "replicação" vs. "replicar"), promovendo tautologias a `DIRECT`.
- **CR-04 (Mapeamento terminológico hardcoded - 11 casos / 13,75%):** Respostas evasivas foram mapeadas por regra hardcoded na linha 3633 para `UNKNOWN` em vez de `INSUFFICIENT`.
- **CR-07 (Invariância assimétrica em antíteses - 5 casos / 6,25%):** Formulações coloquiais e passivas de remoção de travas/ACID contornaram os filtros imperativos formais de antítese e foram classificadas como `DIRECT`.
- **CR-08 (Polaridade e salvaguarda preventiva):** Alta taxa de acerto no Grupo I (92,86%), confirmando a eficácia da guarda preventiva introduzida no Stage 31.7.20.

### 3. Decisão Arquitetural para o Ciclo 4:
- Comparadas 3 alternativas:
  - *Alternativa 1 (Expansão Heurística Pontual):* Rejeitada por risco severo de overfitting e fragilidade contínua a variações de linguagem.
  - *Alternativa 3 (Modelo Neural de Embeddings):* Rejeitada por violação aos guardrails de determinismo, auditabilidade causal e explicabilidade do projeto.
  - *Alternativa 2 (Grafo Proposicional Decomposto com Contratos Estritos):* **Aprovada formalmente**.
- Pipeline modular em 5 componentes especificado:
  1. `SemanticIntentAndDemandExtractor`
  2. `PropositionDiscourseFilter`
  3. `MorphologicalCircularityAnalyzer`
  4. `DemandPropositionNexusBipartiteMatcher`
  5. `StrictOntologyRelevanceAggregator`

### 4. Próxima Etapa Autorizada:
- **Stage 31.7.23 — Controlled Correction Plan & Contract Specification (Cycle 4)** (CONCLUÍDO)
- Formalizar o plano de incremento controlado dos 5 componentes e especificar a suíte de testes de contrato unitários (TC-01 a TC-07) antes de qualquer implementação de código no runtime.

---

# 74. REGISTRO DE TRANSIÇÃO — STAGE 31.7.23 (PLANO DE CORREÇÃO CONTROLADA & ESPECIFICAÇÃO DE CONTRATOS DO CICLO 4)

- **Stage Concluído:** Stage 31.7.23 — Controlled Correction Plan & Contract Specification (Cycle 4)
- **Gate Emitido:** `GATE: CORRECTION_PLAN_READY_FOR_CONTROLLED_IMPLEMENTATION`
- **Artefatos Gerados:**
  - `stage_31_7_23_correction_plan.json` (SHA-256: `7A9A8D379D14A2ED486DCC24CFAD4107A45701F385A5CD8874FA2015449AE3A9`)
  - `stage_31_7_23_component_contracts.md` (SHA-256: `1D70B954635C7F31F8F5EE69B5DECD5EE3B7CD709E6ABA7F14AC00A94B24C3E9`)
  - `stage_31_7_23_incremental_implementation_plan.md` (SHA-256: `BF236B770B10987DAAE03641B99F18942025E171E61F41CDF37FF3560734AF4B`)
  - `stage_31_7_23_validation_contract.md` (SHA-256: `DBA8E45A3A5904541B51F2D58E64E710210B2FE4998F28BAFA537C2568805679`)
  - `stage_31_7_23_risk_and_rollback_plan.md` (SHA-256: `6D9F67ACF7F7B7A1CFA008B1A6A928345ABF2685B658C64F50E0B5976DBF645E`)
  - `Stage 31.7.23 — Controlled Correction Plan & Contract Specification (Cycle 4).md` (SHA-256: `DDB69DAE1D9771662C50B61853059DCB3D170DC64BD9C1C5DB9C45D406D2D05F`)
- **Status do Runtime:** 100% Congelado, SHA-256 verificado: `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`.
- **Checkpoint Criado:** `reference_runtime/runtime.py.stage_31_7_23_baseline` (SHA-256: `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`).

### 1. Especificações Formalizadas no Stage 31.7.23:
1. **Contratos dos 5 Componentes Desacoplados:**
   - `SemanticIntentAndDemandExtractor`: extração profunda de aspectos obrigatórios em orações simples sem exigir conjunções explícitas (resolve CR-01).
   - `PropositionDiscourseFilter`: classificação em 7 gêneros discursivos antes da avaliação de verbos, desqualificando relatos autobiográficos e anedotas históricas de atuarem como soluções operativas (resolve CR-02 e CR-05).
   - `MorphologicalCircularityAnalyzer`: unificação de famílias cognatas nominais e verbais, calculando o ganho informacional real para barrar tautologias morfológicas (resolve CR-03).
   - `DemandPropositionNexusBipartiteMatcher`: emparelhamento bipartido que elimina a cross-satisfaction difusa de múltiplas demandas por palavras coincidentes isoladas (resolve CR-06).
   - `StrictOntologyRelevanceAggregator`: única fonte de verdade ontológica; mapeia evasão para `INSUFFICIENT` e exige 100% de aspectos satisfeitos para conceder `DIRECT` (resolve CR-04).
2. **Dezesseis Invariantes Semânticos Testáveis:**
   - Formalizados de INV-01 a INV-16, estabelecendo regras formais que impedem a perda de incerteza, viés de extensão, ou conclusões apressadas por presença/ausência léxica.
3. **Plano de Implementação Incremental (5 Incrementos):**
   - Incremento A: Intenção e Demandas (`SemanticIntentAndDemandExtractor`).
   - Incremento B: Nexo Funcional e Cobertura Bipartida (`DemandPropositionNexusBipartiteMatcher`).
   - Incremento C: Gênero Discursivo e Circularidade Morfológica (`PropositionDiscourseFilter` & `MorphologicalCircularityAnalyzer`).
   - Incremento D: Polaridade, Evasão e Incerteza (`_detect_antithesis` e regra EVASIVE -> INSUFFICIENT).
   - Incremento E: Agregação Canônica e Integração Final (`StrictOntologyRelevanceAggregator`).
4. **Contrato de Validação Independente do Ciclo 4 (Stage 31.7.25):**
   - Limiares pré-fixados: Concordância $\ge 75\%$, Recall DIRECT $\ge 85\%$, Precisão DIRECT $\ge 70\%$, Falsos DIRECT $\le 10\%$, Recall PARTIAL $\ge 60\%$, Invariância Homologada $\ge 80\%$, Regressão zero falhas.
   - Separação explícita entre consistência pura de saída e invariância homologada (consistência + correção).
   - Benchmark histórico do Stage 31.7.21 preservado exclusivamente como diagnóstico.
   - Status mantido honestamente como `REFERENCE_INDEPENDENCE_UNRESOLVED`.
5. **Plano de Riscos e Rollback:**
   - Gatilhos automáticos de rollback perante qualquer regressão na suíte canônica (1038 testes) ou Reference Harness (15 testes).

### 2. Próxima Etapa Autorizada:
- **Stage 31.7.24 — Controlled Implementation of the Approved Semantic Precision Remediation Plan (Cycle 4)** (CONCLUÍDO)
- Executar exclusivamente a implementação controlada dos 5 incrementos especificados (A a E) em `reference_runtime/runtime.py`, validando os testes de contrato (TC-01 a TC-07) e garantindo regressão canônica 100% verde a cada passo, gerando novo hash congelado ao final.

---

# 75. REGISTRO DE TRANSIÇÃO — STAGE 31.7.24 (IMPLEMENTAÇÃO CONTROLADA DA ARQUITETURA DE PRECISÃO SEMÂNTICA DO CICLO 4)

- **Stage Concluído:** Stage 31.7.24 — Controlled Implementation of the Approved Semantic Precision Remediation Plan (Cycle 4)
- **Gate Emitido:** `GATE: IMPLEMENTATION_COMPLETE_PENDING_INDEPENDENT_BLIND_VALIDATION`
- **Artefatos Gerados:**
  - `stage_31_7_24_implementation_log.md`
  - `stage_31_7_24_component_test_results.json`
  - `stage_31_7_24_regression_results.json`
  - `stage_31_7_24_diagnostic_comparison.json`
  - `stage_31_7_24_runtime_manifest.json`
  - `stage_31_7_24_risk_and_rollback_results.md`
  - `Stage 31.7.24 — Controlled Implementation of the Approved Semantic Precision Remediation Plan (Cycle 4).md`
- **Status do Runtime:**
  - Baseline de Entrada: `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`
  - Exit SHA-256 Congelado: `36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7`
- **Checkpoints Preservados:**
  - `reference_runtime/runtime.py.stage_31_7_23_baseline` (SHA-256: `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`)
  - `reference_runtime/runtime.py.stage_31_7_24_pre_implementation` (SHA-256: `75C6841D14691D9AFC6FF628CA27F67F8201308EB48D6A46A35E41DEA997A6EC`)

### 1. Síntese da Implementação:
1. **Componentes Arquiteturais Implementados em `reference_runtime/runtime.py`:**
   - `SemanticIntentAndDemandExtractor`: segmentação de cláusulas coordenadas com conectivo `" e "` e sintagmas verbais autônomos; extração profunda de metas multi-estado (Circuit Breaker: fechado/aberto/meio-aberto; Sagas: coordenação/compensação; 2PC: commit/abort/crash do coordenador).
   - `PropositionDiscourseFilter`: categorização em gêneros discursivos formais (`MECHANISM_EXPLANATION`, `HISTORICAL_TRIVIA`, `PERSONAL_DECLARATION`, `EVASIVE_DEFLECTION`, `AMBIGUOUS_STATEMENT`, `SPECULATIVE_ASSERTION`); desqualificação de trivialidades e relatos pessoais de atuarem como proposições operativas; separação epistêmica rigorosa entre `is_ambiguous` (direcionado a `UNKNOWN`) e `is_evasive` (direcionado a `INSUFFICIENT`).
   - `MorphologicalCircularityAnalyzer`: unificação de 11 famílias de cognatos abertos em português (`comprim`/`compress`, `replic`/`duplic`, `trav`, `orden`, `indic`/`index`, `sincron`, `esper`, `partic`, `isol`, `buffer`, `disponi`); detecção estrutural de ausência de ganho informacional em tautologias reflexivas, protegida por salvaguarda de mecanismos técnicos externos.
   - `DemandPropositionNexusBipartiteMatcher`: emparelhamento bipartido estrito entre demandas atômicas e proposições técnicas; checagem operacional para recuperação de falhas (impedindo satisfação de crash por mera menção a coordenador); cálculo de graus de satisfação (`FUNCTIONALLY_SOLVES`, `PARTIAL_ASPECT`, `CONTRIBUTES_TO`, `THEMATICALLY_ADJACENT`, `UNMET`).
   - `StrictOntologyRelevanceAggregator`: consolidação das 7 classes canônicas por precedência ontológica inegociável; eliminação de fall-throughs permissivos; posicionamento prioritário da telemetria/observabilidade auxiliar antes da adjacência de entidade.
2. **Nova Suíte de Testes de Contrato:**
   - Criado [`tests/test_stage_31_7_24_contract_tests.py`](file:///d:/Projetos/TechLens/tests/test_stage_31_7_24_contract_tests.py) com 9 testes cobrindo os cenários TC-01 a TC-07 e verificação de reachability das 7 classes: **9/9 aprovados (100% OK em 0.013s)**.
3. **Regressão Canônica e Reference Harness:**
   - Suíte canônica: 1.047 testes executados (1.046 OK, 1 skipped, 0 falhas, 0 erros em 45.3s).
   - Reference Harness: 15/15 testes aprovados (`PASS_WITH_WARNINGS` em 30.9s).
   - Suítes semânticas: 58/58 testes específicos aprovados (100%).
4. **Auditoria Diagnóstica Não-Cega (Benchmark Histórico Stage 31.7.21 — 250 casos):**
   - Acurácia Global: 68.00% (170/250) $\to$ **78.80% (197/250)** (+10.80 pontos percentuais).
   - Casos com melhoria: **27**.
   - Casos com regressão: **0**.
   - Recall de `INSUFFICIENT`: 36.36% $\to$ **86.36% (+50.00%)** com **100% de precisão**.
   - Precisão de `UNKNOWN`: 38.89% $\to$ **100.00% (+61.11%)** com **85.71% de recall**.
   - Recall de `PARTIAL`: 37.78% $\to$ **53.33% (+15.55%)** e precisão de 65.38% $\to$ 72.73%.
   - Recall de `RELATED`: 65.62% $\to$ **75.00% (+9.38%)** com **100% de precisão**.
   - Precisão de `DIRECT`: 53.00% $\to$ **62.35% (+9.35%)** com recall de 81.54%.

### 2. Próxima Etapa Autorizada:
- **Stage 31.7.25 — Independent Blind Semantic Revalidation (Cycle 4)** (CONCLUÍDO COM BLOQUEIO METODOLÓGICO)
- Conduzir a validação cega independente sobre conjunto amostral inédito e balanceado (200–250 casos), mantendo o runtime 100% congelado no hash auditado `36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7`.

---

# 76. REGISTRO DE TRANSIÇÃO — STAGE 31.7.25 (VALIDAÇÃO CEGA INDEPENDENTE DO RUNTIME DO CICLO 4)

- **Stage Concluído:** Stage 31.7.25 — Independent Blind Semantic Revalidation of the Cycle 4 Remediated Runtime
- **Gate Emitido:** `GATE: BLIND_SEMANTIC_REVALIDATION_BLOCKED`
- **Artefatos Gerados:**
  - `stage_31_7_25_validation_plan.md`
  - `stage_31_7_25_benchmark_manifest.json`
  - `stage_31_7_25_blind_input.json`
  - `stage_31_7_25_ground_truth.json`
  - `stage_31_7_25_system_predictions.json`
  - `stage_31_7_25_metrics_summary.json`
  - `stage_31_7_25_confusion_matrix.json`
  - `stage_31_7_25_invariance_results.json`
  - `stage_31_7_25_divergence_analysis.json`
  - `stage_31_7_25_regression_results.json`
  - `stage_31_7_25_provenance_and_blinding_audit.md`
  - `Stage 31.7.25 — Independent Blind Semantic Revalidation of the Cycle 4 Remediated Runtime.md`
- **Status do Runtime:** 100% Congelado e Inviolado.
  - SHA-256 Inicial: `36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7`
  - SHA-256 Final: `36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7`
- **Status da Referência:** `REFERENCE_INDEPENDENCE_UNRESOLVED` (ausência de painel de juízes externos independentes mantida com honestidade intelectual).

### 1. Síntese dos Resultados da Validação Cega (250 Casos Inéditos):
1. **Métricas Globais vs. Limiares de Aceite:**
   - **Concordância Exata:** 60.80% (152/250) vs. limiar $\ge 75.00\%$ $\to$ **REPROVADO**.
   - **Recall de `DIRECT`:** 90.91% (50/55) vs. limiar $\ge 85.00\%$ $\to$ **APROVADO**.
   - **Precisão de `DIRECT`:** 41.67% (50/120) vs. limiar $\ge 70.00\%$ $\to$ **REPROVADO**.
   - **Falsos DIRECT entre Divergências:** 71.43% (70/98) vs. limiar $\le 10.00\%$ $\to$ **REPROVADO**.
   - **Recall de `PARTIAL`:** 93.33% (42/45) vs. limiar $\ge 60.00\%$ $\to$ **APROVADO**.
   - **Invariância Pareada Correta:** 40.00% (8/20) vs. limiar $\ge 80.00\%$ $\to$ **REPROVADO**.
   - **Regressão Canônica:** 1.047 testes (1.046 OK, 1 skipped, 0 fail em 47.1s) e Reference Harness (15/15 OK em 35.7s) $\to$ **APROVADO**.
2. **Diagnóstico Preliminar das 98 Divergências:**
   - **Gargalo da Permissividade de Domínio Aberto (70 casos de falso DIRECT):** O motor identificou com perfeição perguntas multi-aspecto parciais (93.3% recall) e tautologias circulares (95.5% recall). No entanto, quando submetido a perguntas de infraestrutura com respostas de domínios completamente disjuntos (ex: jardinagem, culinária, automobilismo) ou declarações institucionais com verbos articulados, o fallback do `DemandPropositionNexusBipartiteMatcher` presumiu que qualquer proposição operativa não filtrada soluciona a demanda (`FUNCTIONALLY_SOLVES`), inflando os falsos `DIRECT`.
   - **Fronteira Evasiva em `INSUFFICIENT`:** Respostas evasivas que continham cláusulas explicativas foram interpretadas como `OFF_TOPIC` (`non_operative_assertion`) ou promovidas a `DIRECT`.

### 2. Próxima Etapa Autorizada:
- **Stage 31.7.26 — Root Cause Analysis & Semantic Domain Disjunction Architecture (Cycle 5)** (CONCLUÍDO)
- Executar a investigação estrutural das 98 divergências identificadas na validação cega, especificando a arquitetura de ancoragem semântica e verificação de disjunção de domínio, com o runtime rigorosamente congelado.

---

# 77. REGISTRO DE TRANSIÇÃO — STAGE 31.7.26 (ROOT CAUSE ANALYSIS & SEMANTIC DOMAIN DISJUNCTION ARCHITECTURE — CICLO 5)

- **Stage Concluído:** Stage 31.7.26 — Root Cause Analysis & Semantic Domain Disjunction Architecture (Cycle 5)
- **Gate Emitido:** `GATE: RCA_COMPLETE_ARCHITECTURE_APPROVED_FOR_IMPLEMENTATION`
- **Artefatos Gerados:**
  - `stage_31_7_26_reproduction_and_metrics_audit.md` (SHA-256: `47B21F2765779BDBE56E189AC304FB3EABDC82FA30C097EF5DBFE20189CE3E65`)
  - `stage_31_7_26_false_direct_case_audit.json` (SHA-256: `B170FCC95071FC3E04DAFE2FDCB182515908BEAED93B42E4B51AEB00643DEAE2`)
  - `stage_31_7_26_root_cause_analysis.md` (SHA-256: `466876E2200C1B60CF8BEE53D37202C826F3177B9D991E4E134FAC04FC563CE2`)
  - `stage_31_7_26_semantic_domain_disjunction_architecture.md` (SHA-256: `E6CBDB3C481C7E6FFA1F45D850451B998F0F5A3FBEC784C622EF5D6998E795C9`)
  - `stage_31_7_26_semantic_contracts.json` (SHA-256: `D0AF0F7FF4E0E6157B0C3604F2036AF52F10D9950E56644D19A12CCE4473EC59`)
  - `stage_31_7_26_regression_risk_matrix.md` (SHA-256: `1EB9883E8DD9C67F5D45FAACEB19779A4ACDAFE704181196259D097ED6FD42A5`)
  - `stage_31_7_26_future_validation_plan.md` (SHA-256: `C82C86F9BEBE1311D678DA3DC16A2720CB8537FA2629A7FC2DFB0E0A735A8583`)
  - `Stage 31.7.26 — Root Cause Analysis & Semantic Domain Disjunction Architecture (Cycle 5).md`
- **Status do Runtime:** 100% Congelado e Inviolado.
  - SHA-256 Inicial e Final: `36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7` (ZERO alterações).
- **Status da Referência:** `REFERENCE_INDEPENDENCE_UNRESOLVED` (o benchmark de 250 casos é considerado diagnóstico e não poderá servir como teste cego no Ciclo 5).

### 1. Síntese do RCA e Resultados da Auditoria:
1. **Reprodução Independente de Métricas:**
   - Confirmada exata: 152 acertos / 250 casos (60.80% acurácia global).
   - Recall de `DIRECT`: 90.91% (50/55). Precisão de `DIRECT`: 41.67% (50/120).
   - Falsos `DIRECT` entre divergências: 71.43% (70/98).
   - Invariância pareada correta: 40.00% (8/20).
2. **Auditoria Individual dos 70 Falsos DIRECT:**
   - 34 casos `OFF_TOPIC → DIRECT`: Falta de verificação de disjunção semântica; o catálogo estático de 25 termos alienígenas não capturou botânica, culinária e mecânica veicular, que receberam `is_operative = True` pela sintaxe ativa.
   - 22 casos `RELATED → DIRECT`: Metadados institucionais/categoriais em orações transitivas ativas escaparam aos regexes e foram interpretados como mecanismos operacionais.
   - 7 casos `SUPPORTING → DIRECT`: Observabilidade/telemetria instrumental não foram ancoradas como papéis auxiliares e caíram no fallback de mecanismo direto.
   - 7 casos `INSUFFICIENT → DIRECT`: Respostas evasivas sintaticamente complexas ultrapassaram os filtros de evasão e receberam presunção de suficiência.
3. **Mecanismo da Falha Estrutural:**
   - Desacoplamento entre sintaxe e semântica: O `PropositionDiscourseFilter` classificava orações como `is_operative=True` baseado apenas em verbos gramaticais ativos, e o `DemandPropositionNexusBipartiteMatcher` executava o fallback incondicional na Linha 3434 (`FUNCTIONALLY_SOLVES`), promovido a `DIRECT` pelo agregador.
4. **Arquitetura do Ciclo 5 e Contratos Formais A a G:**
   - Introdução do `SemanticDomainDisjunctionEngine` para testar compatibilidade ontológica e disjunção radical com base em evidência positiva, sem vocabulário fechado.
   - Revogação definitiva do fallback incondicional da linha 3434 do matcher.
   - Formalização de contratos: Demanda Primária (A), Proposição (B), Nexo (C), Suficiência Causal (D), Compatibilidade Semântica (E), Disjunção Radical (F) e Agregação Final (G).
   - Salvaguarda de 14 comportamentos preservados (respostas conceituais sem sobreposição lexical, entidades inéditas, linguagem coloquial, voz passiva, troubleshooting).
   - Mapeamento de 12 riscos de regressão e protocolo de validação futura com os limiares canônicos estabelecidos.

### 2. Próxima Etapa Autorizada:
- **Stage 31.7.27 — Controlled Remediation of Semantic Domain Disjunction Architecture (Cycle 5)** (CONCLUÍDO)
- Implementar controladamente no runtime a arquitetura de disjunção semântica especificada e os contratos formais A a G, sob rigoroso monitoramento de testes unitários e regressão canônica.

---

# 78. REGISTRO DE TRANSIÇÃO — STAGE 31.7.27 (REMEDIAÇÃO CONTROLADA DA ARQUITETURA DE DISJUNÇÃO DE DOMÍNIO — CICLO 5)

- **Stage Concluído:** Stage 31.7.27 — Controlled Remediation of Semantic Domain Disjunction Architecture (Cycle 5)
- **Gate Emitido:** `GATE: IMPLEMENTATION_COMPLETE_PENDING_INDEPENDENT_BLIND_VALIDATION`
- **Artefatos Gerados:**
  - `stage_31_7_27_implementation_plan.md`
  - `stage_31_7_27_runtime_diff.md`
  - `stage_31_7_27_contract_tests.py`
  - `stage_31_7_27_test_results.json`
  - `stage_31_7_27_historical_diagnostic_metrics.json`
  - `stage_31_7_27_regression_results.json`
  - `stage_31_7_27_rollback_record.md`
  - `Stage 31.7.27 — Controlled Remediation of Semantic Domain Disjunction Architecture (Cycle 5).md`
- **Hashes Criptográficos do Runtime (`reference_runtime/runtime.py`):**
  - SHA-256 Inicial (Baseline): `36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7`
  - SHA-256 Final Homologado com 0 Regressões: `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28`
- **Snapshots de Segurança Persistidos:**
  - `reference_runtime/runtime.py.stage_31_7_26_baseline` (SHA-256: `36344F3E...`)
  - `reference_runtime/runtime.py.stage_31_7_27_inc_a`
  - `reference_runtime/runtime.py.stage_31_7_27_pre_regression_fix` (SHA-256: `3FD3F80D9BB8A13CCC3A2791759D08F2EED25271913B56F064710DB94B2BC229`)
  - `reference_runtime/runtime.py.stage_31_7_27_final` (SHA-256: `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28`)
- **Status Metodológico:** `REFERENCE_INDEPENDENCE_UNRESOLVED` (mantido estritamente; o benchmark histórico de 250 casos é considerado diagnóstico e não serve como validação cega).

### 1. Síntese das Modificações Arquiteturais Implementadas:
1. **Incremento A (`SemanticDomainDisjunctionEngine` & `DomainCompatibilityRecord`):**
   - Criação do classificador ontológico de compatibilidade de domínio semântico (linhas 1709–1960).
   - Detecção robusta de disjunção radical em domínios cotidianos não computacionais (botânica, culinária, mecânica automotiva, literatura, esportes) baseada em evidência positiva, sem vocabulário fechado.
   - Separação de metadados institucionais/históricos de produto (`THEMATIC_METADATA`) e evasão discursiva (`EVASIVE_DEFLECTION`).
2. **Incremento B (`DemandPropositionNexusBipartiteMatcher`):**
   - Revogação definitiva do fallback incondicional de domínio aberto da linha 3434.
   - Integração da matriz bipartite aos registros de domínio (`DOMAIN_DISJUNCT` $\to$ veto de DIRECT/PARTIAL, `THEMATICALLY_ADJACENT`, `EVASIVE`).
   - Reconhecimento antecipado de definições conceituais e matching de cognatos morfológicos em demandas secundárias de perguntas compostas.
3. **Incremento C (`PropositionDiscourseFilter`):**
   - Salvaguarda de prevenção contra antítese falsa (`avoidance_guard = re.search(...)`).
   - Detecção do gênero discursivo `CONCEPTUAL_DEFINITION` e suporte a locuções operacionais em linguagem coloquial e voz passiva.
4. **Incremento D (`StrictOntologyRelevanceAggregator`):**
   - Preservação da acessibilidade determinística e separação categorial de todas as 7 classes canônicas (`DIRECT`, `PARTIAL`, `SUPPORTING`, `RELATED`, `OFF_TOPIC`, `INSUFFICIENT`, `UNKNOWN`).
5. **Incremento E (`OpenDomainPropositionEngine`):**
   - Orquestração completa na API canônica `evaluate_relevance(question, response)` com enriquecimento de rastreabilidade.

### 2. Resultados de Testes e Regressão:
- **Testes de Contrato Obrigatórios:** 20/20 APROVADOS (100% de sucesso em 0.026s, `tests/test_stage_31_7_27_contract_tests.py`).
- **Suíte Canônica de Testes:** 1.047 testes executados, 1.046 aprovados, 1 ignorado (`skipped=1`), 0 falhas, 0 erros em 35.102s (**ZERO REGRESSÕES**).
- **Reference Harness (Stage 26):** 15/15 aprovados, 0 falhas, 0 erros em 38.004s (**ZERO REGRESSÕES**).
- **Benchmark Histórico Diagnóstico (250 Casos):**
  - Acurácia global: de 60.80% para **89.20%** (223/250, +71 acertos).
  - Falsos DIRECTs: de 70 para **6** (**redução de 91.43%**).
  - Precisão de DIRECT: de 41.67% para **89.66%**.
  - Recall de DIRECT: **94.55%** (52/55).
  - Recall de PARTIAL: **97.78%** (44/45).
  - Recall de OFF_TOPIC: **100.0%** (44/44, com 0 falsos DIRECTs).
  - Recall de UNKNOWN: **95.45%** (21/22, com 0 falsos DIRECTs).

### 3. Próxima Etapa Autorizada:
- **Stage 31.7.28 — Independent Blind Semantic Revalidation (Cycle 5)** (CONCLUÍDO)
- Executar validação semântica cega independente com o runtime rigorosamente congelado (`6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28`) sobre novo dataset balanceado de teste cego, verificando os limiares canônicos de aceitação para homologação definitiva.

---

# 79. REGISTRO DE TRANSIÇÃO — STAGE 31.7.28 (REVALIDAÇÃO SEMÂNTICA CEGA E INDEPENDENTE — CICLO 5)

- **Stage Concluído:** Stage 31.7.28 — Independent Blind Semantic Revalidation (Cycle 5)
- **Gate Emitido:** `GATE: BLIND_SEMANTIC_REVALIDATION_BLOCKED`
- **Artefatos Gerados:**
  - `stage_31_7_28_validation_plan.md`
  - `stage_31_7_28_benchmark_manifest.json`
  - `stage_31_7_28_blind_input.json` (SHA-256: `036EE47E7B9A4BBFE91B5C0A2AF61CCC0A73CCCE899C767A3D5AA574D5724954`)
  - `stage_31_7_28_ground_truth.json` (SHA-256: `C8C2822F18D1F5806A3EBF9FE18724F2972AA2C73799AD25A7072CD8C55DB5AF`)
  - `stage_31_7_28_system_predictions.json` (SHA-256: `F029BE72D8C91B4161E08555B1C9D52640FE272F56D449D9F5B069A51967D670`)
  - `stage_31_7_28_metrics_summary.json`
  - `stage_31_7_28_confusion_matrix.json`
  - `stage_31_7_28_invariance_results.json`
  - `stage_31_7_28_divergence_analysis.json`
  - `stage_31_7_28_regression_results.json`
  - `stage_31_7_28_provenance_audit.md`
  - `Stage 31.7.28 — Independent Blind Semantic Revalidation (Cycle 5).md`
- **Status do Runtime (`reference_runtime/runtime.py`):**
  - SHA-256 Inicial e Final: `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28` (100% íntegro, congelado e inviolado).
- **Status Metodológico:** `REFERENCE_INDEPENDENCE_UNRESOLVED` (mantido estritamente; o benchmark foi adjudicado pela equipe interna sem painel duplo-cego externo).

### 1. Resultados Quantitativos da Validação Cega (250 Casos Inéditos):
- **Acurácia Global Exata:** **67.20% (168/250)** vs. limiar $\ge 75.00\%$ $\to$ **REPROVADO**.
- **Recall de `DIRECT`:** **76.00% (38/50)** vs. limiar $\ge 85.00\%$ $\to$ **REPROVADO**.
- **Precisão de `DIRECT`:** **52.78% (38/72)** vs. limiar $\ge 70.00\%$ $\to$ **REPROVADO**.
- **Falsos DIRECT entre Divergências:** **41.46% (34/82)** vs. limiar $\le 10.00\%$ $\to$ **REPROVADO**.
- **Recall de `PARTIAL`:** **84.44% (38/45)** vs. limiar $\ge 60.00\%$ $\to$ **APROVADO**.
- **Recall de `SUPPORTING`:** **96.67% (29/30)**.
- **Recall de `UNKNOWN`:** **90.00% (18/20)**.
- **Recall de `INSUFFICIENT`:** **76.00% (19/25)**.
- **Invariância Pareada Simultaneamente Correta:** **65.00% (13/20 pares)** vs. limiar $\ge 80.00\%$ $\to$ **REPROVADO**.
- **Regressão Canônica:** 1.067 testes executados com 1.066 aprovações e 1 teste ignorado (`OK (skipped=1)`) em 46.392s, Reference Harness 15/15 OK em 34.687s $\to$ **APROVADO (ZERO REGRESSÕES)**.

### 2. Matriz de Confusão Completa (7x7):
```text
Ref \ Pred    DIRECT  PARTIAL  SUPPORTING  RELATED  OFF_TOPIC  INSUFFICIENT  UNKNOWN  TOTAL
DIRECT            38        3           3        3          3             0        0     50
PARTIAL            1       38           1        2          3             0        0     45
SUPPORTING         0        0          29        0          1             0        0     30
RELATED            5        0           0        8         22             0        0     35
OFF_TOPIC         26        1           0        0         18             0        0     45
INSUFFICIENT       1        0           0        1          4            19        0     25
UNKNOWN            1        0           0        0          1             0       18     20
-----------------------------------------------------------------------------------------
Pred Total        72       42          33       14         52            19       18    250
```

### 3. Diagnóstico Qualitativo e Causas-Raiz Identificadas:
1. **Dependência de Expressões Literais no `SemanticDomainDisjunctionEngine` (26 falsos DIRECTs de `OFF_TOPIC`):**
   - Respostas de cerâmica/artesanato em argila, construção civil (cimento, betoneira) e agricultura de outras plantas não coincidiram com as regexes fechadas dos 5 clusters do motor de disjunção.
   - Como consequência, não foram vetadas por disjunção ontológica.
   - A presença de verbos transitivos ativos ("requer", "exige") gerou `is_operative = True` no `PropositionDiscourseFilter`, e o fallback de domínio aberto promoveu indevidamente para `DIRECT`.
2. **Rebaixamento Indevido de Metadados Legítimos (22 casos de `RELATED → OFF_TOPIC`):**
   - Respostas com descrições históricas, de fundações (Apache, Linux, CNCF) ou origem acadêmica foram marcadas como `non_operative_assertion`, sendo roteadas pelo agregador diretamente para `OFF_TOPIC` em vez de `RELATED`, derrubando o recall de `RELATED` para 22.86%.

### 4. Próxima Etapa Autorizada:
- **Stage 31.7.29 — Root Cause Analysis & Domain Disjunction Generalization Architecture (Cycle 6)** (CONCLUÍDO)
- Investigar estruturalmente a falha de generalização do `SemanticDomainDisjunctionEngine` e o rebaixamento de `RELATED`, mantendo o runtime absolutamente congelado e projetando uma arquitetura invariante à extensão de vocabulário para o Ciclo 6.

---

# 80. REGISTRO DE TRANSIÇÃO — STAGE 31.7.29 (FORENSIC ROOT CAUSE ANALYSIS & DOMAIN DISJUNCTION GENERALIZATION — CICLO 6)

- **Stage Concluído:** Stage 31.7.29 — Forensic Root Cause Analysis & Domain Disjunction Generalization Architecture (Cycle 6)
- **Gates Emitidos:**
  - **Gate de Proveniência:** `GATE: RUNTIME_PROVENANCE_RECONCILED`
  - **Gate de RCA e Arquitetura:** `GATE: RCA_COMPLETE_ARCHITECTURE_PENDING_REVIEW`
- **Artefatos Gerados:**
  - `stage_31_7_29_runtime_provenance_audit.md`
  - `stage_31_7_29_runtime_hash_inventory.json`
  - `stage_31_7_29_runtime_comparison_report.md`
  - `stage_31_7_29_metrics_reproduction.json`
  - `stage_31_7_29_root_cause_analysis.md`
  - `stage_31_7_29_false_direct_case_audit.json`
  - `stage_31_7_29_related_off_topic_audit.json`
  - `stage_31_7_29_seven_class_contract_audit.md`
  - `stage_31_7_29_domain_disjunction_generalization_architecture.md`
  - `stage_31_7_29_semantic_contracts.json`
  - `stage_31_7_29_regression_risk_matrix.md`
  - `stage_31_7_29_future_validation_plan.md`
  - `Stage 31.7.29 — Forensic Root Cause Analysis & Domain Disjunction Generalization Architecture (Cycle 6).md`
- **Status do Runtime (`reference_runtime/runtime.py`):**
  - SHA-256 Inicial e Final: `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28` (100% íntegro, congelado e inviolado).
  - Snapshot de segurança preservado: `reference_runtime/runtime.py.stage_31_7_29_forensic_entry` (SHA-256 idêntico).
- **Status Metodológico:** `REFERENCE_INDEPENDENCE_UNRESOLVED` (mantido estritamente).

### 1. Reconciliação Forense dos Runtimes:
1. **Reconstituição Conclusiva:** O hash `3FD3F80D...` correspondeu ao snapshot intermediário gerado às 22:24:37 UTC no Stage 31.7.27, o qual apresentou 5 falhas na suíte canônica de testes (`test_avoidance_guard_does_not_trigger_antithesis`, `test_category_h_inference_limits_unknown_insufficient`, `test_all_seven_classes_reachable`). O hash `6C44B7A8...` correspondeu ao runtime resultante de 3 correções de salvaguarda pontuais às 22:36:27 UTC que atingiram zero regressões (1.046 testes OK, Reference Harness 15/15 OK). O registro de `3FD3F80D...` decorreu de erro administrativo de transcrição documental ao compilar os relatórios finais.
2. **Execução Comparativa:** Os 26 falsos DIRECTs e os 22 falsos OFF_TOPICs são rigorosamente idênticos em ambos os runtimes. As salvaguardas não introduziram nenhuma anomalia semântica. O runtime `6C44B7A8...` foi formalmente aprovado pelo usuário no início do Stage 31.7.28 e validado cegamente.

### 2. Causas-Raiz Confirmadas no RCA:
1. **Falsos DIRECTs (26 casos):** Falha do motor de disjunção baseado em regexes fechadas ao confrontar vocabulário inédito (artesanato em argila, construção civil, novas plantas). O filtro discursivo confundiu verbos transitivos ativos de processo ("requer", "exige") com pertinência técnica, ativando `is_operative = True` e caindo no fallback funcional do casador de nexo.
2. **Rebaixamento de Metadados (22 casos):** Respostas históricas e de fundações de software (PostgreSQL, Linux, Docker) foram marcadas como `is_operative = False`. O padrão de metadados institucionais falhou por engessamento de regex. O matcher emitiu `NON_OPERATIVE`, e o agregador continha um sumidouro incondicional `else:` que descarregava em `OFF_TOPIC`, violando a ontologia de `RELATED`.

### 3. Nova Arquitetura do Ciclo 6 (Aprovada para Revisão):
- **Vinculação de Entidades Nucleares e Afinidade Tópica Aberta:** Se a resposta compartilha a entidade da pergunta ($E_R \cap E_Q \neq \emptyset$), ela é tematicamente ancorada, vetando sumariamente qualquer rebaixamento para `OFF_TOPIC`.
- **Disjunção Aberta:** Detecção de alienação ontológica por presença de substantivos concretos de outros universos sem ligação com a tecnologia indagada, sem necessidade de catalogação exaustiva de profissões.
- **Roteamento Explícito para `RELATED`:** Proposições não operativas que compartilham a entidade são fixadas deterministicamente em `RELATED`.

### 4. Próxima Etapa Autorizada:
- **Stage 31.7.30 — Adversarial Architecture Review & Semantic Contract Stress Test (Cycle 6)** (CONCLUÍDO)

---

# 81. REGISTRO DE TRANSIÇÃO — STAGE 31.7.30 (ADVERSARIAL ARCHITECTURE REVIEW & SEMANTIC CONTRACT STRESS TEST — CICLO 6)

- **Stage Concluído:** Stage 31.7.30 — Adversarial Architecture Review & Semantic Contract Stress Test (Cycle 6)
- **Gates Emitidos:**
  - **Gate de Proveniência:** `GATE: RUNTIME_PROVENANCE_RECONCILED`
  - **Decisão Arquitetural:** `GATE: ARCHITECTURE_REQUIRES_REVISION`
- **Artefatos Gerados:**
  - `stage_31_7_30_runtime_integrity_check.md`
  - `stage_31_7_30_provenance_claim_audit.json`
  - `stage_31_7_30_entity_anchor_counterexamples.json`
  - `stage_31_7_30_domain_disjunction_stress_cases.json`
  - `stage_31_7_30_seven_class_contract_review.md`
  - `stage_31_7_30_demand_sufficiency_review.md`
  - `stage_31_7_30_invariance_contract_review.md`
  - `stage_31_7_30_contract_coverage_matrix.json` (28 contratos: 22 herdados + 6 novos adversariais)
  - `stage_31_7_30_architecture_risk_register.md`
  - `stage_31_7_30_architecture_decision.md`
  - `Stage 31.7.30 — Adversarial Architecture Review & Semantic Contract Stress Test (Cycle 6).md`
- **Status do Runtime (`reference_runtime/runtime.py`):**
  - SHA-256 Inicial e Final: `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28` (100% íntegro, congelado e inviolado).
  - Snapshot de segurança preservado: `reference_runtime/runtime.py.stage_31_7_30_freeze` (SHA-256 idêntico).
- **Status Metodológico:** `REFERENCE_INDEPENDENCE_UNRESOLVED` (mantido estritamente).

### 1. Auditoria Forense de Proveniência (`RUNTIME_PROVENANCE_RECONCILED`):
Todas as 9 alegações foram auditadas e classificadas como `VERIFIED`. O runtime `6C44B7A8...` foi o código efetivamente avaliado no Stage 31.7.28 com autorização explícita do usuário. A reprodução das 5 falhas no snapshot `3FD3...` e a equivalência das divergências nos 250 casos comprovam que a divergência documental não teve qualquer efeito nas causas semânticas do Ciclo 5.

### 2. Revisão Adversarial da Regra de Entidades (`ARCHITECTURE_REQUIRES_REVISION`):
A regra simplista de veto absoluto de `OFF_TOPIC` por presença de entidade proposta no Stage 31.7.29 foi formalmente refutada:
1. **Contraexemplo E (Homonímia / Divagação):** O candidato cita "injeção de dependências" e desvia para dependência de importações de petróleo. Um veto absoluto blindaria essa divagação contra `OFF_TOPIC`.
2. **Contraexemplo C (Hiperônimos sem Nome Literal):** Respostas perfeitas que explicam B-tree como "árvore balanceada de chaves" sem citar "B-tree" sofreriam risco de falso `OFF_TOPIC` sob a exigência estrita de intersecção lexical.
3. **Contraexemplo B (Elogios Triviais):** "PostgreSQL é popular" deve ser `INSUFFICIENT` e não `RELATED`.
4. **Casos STRESS-06 e STRESS-07:** Analogias pedagógicas (disjuntor elétrico para circuit breaker) e preâmbulos conversacionais (trânsito antes de Paxos) exigem regras específicas de isenção de analogia e segmentação oracional.

### 3. Prescrições Mandatórias para o Ciclo 6:
1. Substituir o veto absoluto por **Presunção Refutável de Conexão Temática** (derrubada se os predicados atuarem sobre domínios disjuntos).
2. Incorporar reconhecimento de **Equivalência Conceitual e Hiperônimos Técnicos**.
3. Criar regra de **Isenção para Analogias Pedagógicas**.
4. Implementar **Segmentação Oracional de Preâmbulos Ruidosos**.
5. Calibrar filtro de substância de metadados para rebaixar elogios vazios a `INSUFFICIENT`.

### 4. Próxima Etapa Autorizada:
- **Stage 31.7.31 — Architectural Remediation & Refined Specification (Cycle 6)** (CONCLUÍDO)

---

# 82. REGISTRO DE TRANSIÇÃO — STAGE 31.7.31 (ARCHITECTURAL REMEDIATION & REFINED SEMANTIC SPECIFICATION — CICLO 6)

- **Stage Concluído:** Stage 31.7.31 — Architectural Remediation & Refined Semantic Specification (Cycle 6)
- **Gates Emitidos:**
  - **Decisão Arquitetural:** `GATE: REFINED_ARCHITECTURE_READY_FOR_INDEPENDENT_REVIEW`
  - **Gate de Proveniência:** `GATE: RUNTIME_PROVENANCE_RECONCILED`
- **Artefatos Gerados (13 arquivos):**
  - `stage_31_7_31_refined_architecture.md`
  - `stage_31_7_31_thematic_connection_contract.md`
  - `stage_31_7_31_conceptual_equivalence_contract.md`
  - `stage_31_7_31_analogy_handling_contract.md`
  - `stage_31_7_31_proposition_composition_contract.md`
  - `stage_31_7_31_content_substance_contract.md`
  - `stage_31_7_31_demand_sufficiency_contract.md`
  - `stage_31_7_31_seven_class_decision_contract.md`
  - `stage_31_7_31_evidence_traceability_schema.json`
  - `stage_31_7_31_contract_counterexample_matrix.json` (35 contratos formais: 28 históricos + 7 novos)
  - `stage_31_7_31_architecture_risk_register.md` (18 riscos arquiteturais mapeados)
  - `stage_31_7_31_open_questions.md`
  - `Stage 31.7.31 — Architectural Remediation & Refined Semantic Specification (Cycle 6).md`
- **Status do Runtime (`reference_runtime/runtime.py`):**
  - SHA-256 Inicial e Final: `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28` (100% íntegro, congelado e inviolado).
  - Snapshots de segurança preservados: `reference_runtime/runtime.py.stage_31_7_31_freeze` e `runtime.py.stage_31_7_30_freeze`.
- **Status Metodológico:** `REFERENCE_INDEPENDENCE_UNRESOLVED` (mantido estritamente).

### 1. Cinco Avanços Conceituais Formalizados:
1. **Conexão Temática Refutável:** A presunção preliminar de pertinência por entidade compartilhada é submetida a teste de predicado, sendo formalmente refutada quando a oração atua sobre domínios disjuntos (Caso C: homonímia/petróleo em Spring DI $\to$ `OFF_TOPIC`).
2. **Equivalência Conceitual e Hiperônimos Abertos:** Reconhecimento de respostas tecnicamente corretas formuladas por hiperônimos ou descrições funcionais puras sem o token formal da pergunta (Caso D: árvore balanceada para B-tree $\to$ `DIRECT`).
3. **Bipolaridade de Analogias com Aterrissagem Obrigatória:** Desacoplamento entre domínio-veículo ($D_V$) e domínio-alvo ($D_T$). Analogias com aterrissagem no software geram `DIRECT`; analogias desprovidas de transposição computacional geram `INSUFFICIENT`.
4. **Segmentação Proposicional e Composição de Contexto:** Isolamento de preâmbulos fáticos de ruído (trânsito antes de Paxos $\to$ `DIRECT`), preservação de escopos de negação e condicionais, e detecção de contradições internas destrutivas e autocorreções explícitas.
5. **Roteamento Ontológico Explícito e Fim do Sumidouro de `OFF_TOPIC`:** Proposições temáticas sem mecanismo operacional (história, origem, licença) são encaminhadas deterministicamente para `RELATED`. Elogios vazios sem fatos vão para `INSUFFICIENT`.

### 2. Próxima Etapa Autorizada:
- **Stage 31.7.32 — Independent Adversarial Architecture Review (Cycle 6)** (CONCLUÍDO)

---

# 83. REGISTRO DE TRANSIÇÃO — STAGE 31.7.32 (INDEPENDENT ADVERSARIAL ARCHITECTURE REVIEW — CICLO 6)

- **Stage Concluído:** Stage 31.7.32 — Independent Adversarial Architecture Review (Cycle 6)
- **Gates Emitidos:**
  - **Decisão Arquitetural:** `GATE: ARCHITECTURE_APPROVED_FOR_IMPLEMENTATION_PLANNING`
  - **Gate de Proveniência:** `GATE: RUNTIME_PROVENANCE_RECONCILED`
- **Artefatos Gerados (9 arquivos):**
  - `stage_31_7_32_independent_architecture_review.md` (Relatório principal e respostas aos 13 quesitos)
  - `stage_31_7_32_contract_audit.json` (Auditoria dos 35 contratos: 21 aprovados, 14 com ressalva, 0 rejeitados)
  - `stage_31_7_32_seven_class_boundary_matrix.md` (Matriz das 21 fronteiras binárias entre as 7 classes)
  - `stage_31_7_32_adversarial_counterexamples.json` (15 cenários adversariais de estresse)
  - `stage_31_7_32_pipeline_contract_audit.md` (Auditoria dos 7 estágios sequenciais)
  - `stage_31_7_32_traceability_schema_audit.md` (Validação estrutural do schema JSON Draft-07)
  - `stage_31_7_32_architecture_findings.json` (Catálogo de achados: 0 BLOCKER, 0 CRITICAL, 2 MAJOR, 4 MODERATE, 1 MINOR)
  - `stage_31_7_32_gate_decision.md` (Decisão formal de gates e pendências para implementação)
  - `Stage 31.7.32 — Independent Adversarial Architecture Review (Cycle 6).md` (Relatório executivo)
- **Status do Runtime (`reference_runtime/runtime.py`):**
  - SHA-256 Inicial e Final: `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28` (100% íntegro, congelado e inviolado).
  - Snapshot de segurança preservado: `reference_runtime/runtime.py.stage_31_7_32_freeze`.
- **Status Metodológico:** `REFERENCE_INDEPENDENCE_UNRESOLVED` (mantido estritamente).

### 1. Síntese dos Achados e Aprovação Arquitetural:
1. **Inexistência de Impedimentos Críticos:** A especificação eliminou o veto simplista de `OFF_TOPIC`, removeu o sumidouro incondicional `else: OFF_TOPIC`, estruturou analogias ancoradas e preâmbulos fáticos, e definiu critérios nítidos para as 21 fronteiras das 7 classes.
2. **Diretrizes Mandatórias para a Implementação (Stage 31.7.33):**
   - Delimitar formalmente que a refutação de predicados deve operar sobre análise sintática de papéis semânticos (SRL) ou substantivos nucleares concretos do mundo físico, evitando listas fechadas de palavras proibidas (`FINDING-01`);
   - Focar a equivalência funcional nos invariantes essenciais de ciência da computação (árvores, locks, consenso, hashing) e tratar termos fora do escopo com incerteza calibrada (`UNKNOWN`) (`FINDING-02`);
   - Validar aterrissagem de analogias pela presença de entidades/predicados computacionais no agregado oracional, e não por fórmulas literais fixas (`FINDING-03`);
   - Implementar status `EQUIVALENCE_PENDING` no Estágio 3 para não descartar respostas formuladas por hiperônimos antes da análise do Estágio 4 (`FINDING-04`);
   - Reconciliar aparentes contradições verificando condições de escopo arquiteturais distintas (`FINDING-05`).

### 2. Próxima Etapa Autorizada:
- **Stage 31.7.33 — Controlled Implementation Planning (Cycle 6)** (CONCLUÍDO)

---

# 84. REGISTRO DE TRANSIÇÃO — STAGE 31.7.33 (CONTROLLED IMPLEMENTATION PLANNING — CICLO 6)

- **Stage Concluído:** Stage 31.7.33 — Controlled Implementation Planning (Cycle 6)
- **Gates Emitidos:**
  - **Decisão de Planejamento:** `GATE: IMPLEMENTATION_PLAN_READY_FOR_GOVERNANCE_APPROVAL`
  - **Gate de Proveniência:** `GATE: RUNTIME_PROVENANCE_RECONCILED`
- **Artefatos Gerados (11 arquivos):**
  - `stage_31_7_33_implementation_roadmap.md` (Roadmap dos 6 incrementos com tabela obrigatória)
  - `stage_31_7_33_increment_contracts.json` (Especificação contratual dos incrementos INC-0 a INC-5)
  - `stage_31_7_33_contract_to_component_traceability.json` (Mapeamento dos 35 contratos para componentes e testes)
  - `stage_31_7_33_test_strategy.md` (Estratégia de testes em 9 camadas concêntricas)
  - `stage_31_7_33_regression_baseline.md` (Baseline histórico do Stage 31.7.28 e métricas diagnósticas)
  - `stage_31_7_33_rollback_and_freeze_protocol.md` (Protocolo de snapshots e triggers de aborto)
  - `stage_31_7_33_architecture_findings_disposition.json` (Tratamento dos 7 achados do Stage 31.7.32)
  - `stage_31_7_33_implementation_risk_register.md` (Matriz exaustiva de riscos e mitigações)
  - `stage_31_7_33_open_dependencies.md` (Registro de capacidades não demonstradas e limitações)
  - `stage_31_7_33_gate_decision.md` (Decisão formal de gates e pendências para governança)
  - `Stage 31.7.33 — Controlled Implementation Planning (Cycle 6).md` (Relatório executivo formal)
- **Status do Runtime (`reference_runtime/runtime.py`):**
  - SHA-256 Inicial e Final: `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28` (100% íntegro, congelado e inviolado).
  - Snapshot de segurança preservado: `reference_runtime/runtime.py.stage_31_7_33_freeze`.
- **Status Metodológico:** `REFERENCE_INDEPENDENCE_UNRESOLVED` (mantido estritamente).

### 1. Síntese do Planejamento Aprovado:
1. **Tratamento dos Achados:** Todos os 7 achados foram endereçados sem recorrer a listas de palavras proibidas ou regras por caso. Predicados alienígenas foram vinculados a SRL e categorias físicas no INC-3, equivalência funcional aos invariantes canônicos de CS no INC-4 e contradições aparentes aos escopos condicionais no INC-2.
2. **Modularização em 6 Incrementos:** INC-0 (Fundação e Rastreabilidade), INC-1 (Perfil e Intenção), INC-2 (Segmentação e Preâmbulos), INC-3 (Afinidade Temática Refutável), INC-4 (Equivalência e Analogias Ancoradas) e INC-5 (Agregação 7 Classes).
3. **Salvaguardas de Rollback:** Snapshots dedicados para cada incremento (`runtime.py.stage_31_7_34_inc_*`), triggers de aborto por quebra de regressão canônica (1.047 testes) ou violação contratual, e restauração automática sem perda de evidências históricas.

### 2. Próxima Etapa Autorizada:
- **Stage 31.7.34 — Controlled Implementation of Foundation and Traceability Layer (Increment 0)** (CONCLUÍDO)

---

# 85. REGISTRO DE TRANSIÇÃO — STAGE 31.7.34 (CONTROLLED IMPLEMENTATION OF FOUNDATION AND TRACEABILITY LAYER — INCREMENT 0)

- **Stage Concluído:** Stage 31.7.34 — Controlled Implementation of Foundation and Traceability Layer (Increment 0)
- **Gates Emitidos:**
  - **Decisão de Implementação:** `GATE: INC0_FOUNDATION_IMPLEMENTED_AND_VERIFIED`
  - **Gate de Proveniência:** `GATE: RUNTIME_PROVENANCE_RECONCILED`
- **Artefatos Gerados (8 arquivos):**
  - `stage_31_7_34_inc0_implementation_plan.md` (Plano de implementação, limites e mapeamento contratual)
  - `stage_31_7_34_evidence_traceability_schema.json` (Schema Draft-07 atualizado com resolução do FINDING-06)
  - `stage_31_7_34_inc0_contracts.py` e `tests/test_stage_31_7_34_inc0_contracts.py` (Suíte de 17 testes contratuais e unitários)
  - `stage_31_7_34_test_results.json` (Resultados estruturados dos 17 testes do INC-0: 100% PASS)
  - `stage_31_7_34_regression_results.json` (Regressão canônica global: 1.084 testes OK; Reference Harness: 15/15 OK)
  - `stage_31_7_34_runtime_diff.md` (Diff documentado do runtime em relação à baseline)
  - `stage_31_7_34_rollback_record.md` (Protocolo, comandos exatos e critérios de reversão)
  - `Stage 31.7.34 — Controlled Implementation of Foundation and Traceability Layer (Increment 0).md` (Relatório formal executivo)
- **Status do Runtime (`reference_runtime/runtime.py`):**
  - SHA-256 Inicial (Baseline): `6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28`
  - SHA-256 Final (Pós-INC-0): `E047BA643A6E98975E42336C58339A12AB4D33D48082ED808FF26248478AB1B8`
  - Snapshot de segurança preservado: `reference_runtime/runtime.py.stage_31_7_34_baseline` (`6C44B7A8...`)
  - Snapshot do incremento: `reference_runtime/runtime.py.stage_31_7_34_inc0` (`E047BA64...`)
- **Status Metodológico:** `REFERENCE_INDEPENDENCE_UNRESOLVED` (mantido estritamente).

### 1. Síntese do Incremento Implementado:
1. **Fundação Estrutural e Tipagem Forte:** Foram introduzidas no runtime (`reference_runtime/runtime.py`) as dataclasses tipadas e serializáveis (`DemandSpecification`, `QuestionProfile`, `DiscourseProposition`, `DiscourseProfile`, `ThematicAffinityEvaluation`, `EquivalenceEvaluation`, `AnalogyEvaluation`, `DemandNexusEvaluation`, `CoverageEvaluation`, `EpistemicUncertaintyRecord`, `FinalDecisionRecord` e `EvidenceTraceabilityRecord`), estabelecendo o contrato de dados formal para todos os próximos incrementos (INC-1 a INC-5).
2. **Resolução Formal do FINDING-06:** O campo opcional `applied_contract_ids` foi adicionado à entidade `FinalDecisionRecord` e ao schema JSON Draft-07 de rastreabilidade causal (`stage_31_7_34_evidence_traceability_schema.json`), com semântica de lista de strings de identificadores de contratos semânticos aplicados, garantindo rastreabilidade semântica e 100% de retrocompatibilidade com esquemas prévios.
3. **Validador Determinístico de Schema:** Implementada a função `validate_evidence_traceability_record(data) -> tuple[bool, list[str]]`, validando tipos estritos, propriedades obrigatórias, enums restritos, limites numéricos de cobertura e padrões regex para hash de 64 caracteres e datas ISO 8601.
4. **Verificação Exaustiva em Três Níveis:**
   - **Testes Contratuais do INC-0 (`test_stage_31_7_34_inc0_contracts.py`):** 17 testes executados, 17 aprovados (**100% PASS** em 0,010 s).
   - **Suíte Canônica Global:** 1.084 testes executados, 1.083 aprovados, 0 falhas, 0 erros, 1 pulado (**100% OK, ZERO REGRESSÕES** em 36,26 s).
   - **Reference Harness:** 15 testes executados, 15 aprovados (**100% OK, ZERO REGRESSÕES** em 24,32 s).
5. **Invariância Semântica e Isolamento:** Nenhuma linha de lógica classificatória prévia foi alterada. O runtime preservou integralmente o comportamento semântico anterior enquanto disponibilizou a nova infraestrutura de dados para o INC-1.

### 2. Próxima Etapa Autorizada:
- **Stage 31.7.35 — Controlled Implementation of Question Profile and Proposition Engine (Increment 1)**:
  - Implementação de `SemanticQuestionProfiler` (Camada 1: extração formal de `QuestionProfile` e demandas).
  - Implementação de `PropositionDiscourseFilter` e isolamento de preâmbulos fáticos (Camada 2: extração de `DiscourseProfile`).
























## Auditoria e correções locais — 2026-10-23

Stage 31.7.35 permanece em andamento. Três falhas de extração foram corrigidas e cobertas por 13 novos testes. Regressão atual: 1.097 testes (1.096 aprovados, 1 ignorado), sem falhas ou erros. Classificador fora das duas classes INC-1 permaneceu inalterado por comparação AST. Gate limitado: `AUDIT_FIXES_VERIFIED_INC1_FULL_ACCEPTANCE_PENDING`. Ver [[stage_31_7_35_audit_fixes_report]]. A proveniência histórica dos snapshots continua não comprovada; esta nota não substitui os registros históricos.


## Cobertura complementar do Stage 31.7.35 — 2026-10-23

22 novos testes complementares e correções em grupos sequenciais. Regressão: 1119 testes (1118 aprovados, 1 ignorado), sem falhas ou erros; harness 15/15. Gate limitado: `CONTRACT_SCENARIOS_VERIFIED_GOVERNANCE_RECONCILIATION_PENDING`. Ver [[stage_31_7_35_remaining_contracts_report]]. Etapa continua aberta para reconciliação de escopo entre os planos e limites semânticos documentados; não houve promoção automática ao próximo incremento.
