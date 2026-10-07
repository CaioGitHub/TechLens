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
ATUAL
        ↓
Semantic Relevance
+
Representation Invariance

Stage 31.5
        ↓
PRÓXIMO APÓS 31.4 PASS

Stage 32
        ↓
Production Readiness

Stage 33
        ↓
Production Runtime
```

---

# 55. GATES HISTÓRICOS QUE NÃO DEVEM SER APAGADOS

Preservar:

```text
HUMAN_VS_SYSTEM_BLOCKED

POST_CORRECTION_BLIND_VALIDATION_BLOCKED
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
