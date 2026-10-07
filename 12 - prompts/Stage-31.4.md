# Stage 31.4 — Semantic Relevance & Representation Invariance Remediation

## Objetivo

Corrigir de forma controlada os problemas residuais identificados no:

```text
Stage 31.3 — Post-Correction Blind Validation
```

O Stage 31.3 foi corretamente encerrado com:

```text
POST_CORRECTION_BLIND_VALIDATION_BLOCKED
```

Foram identificadas duas classes principais de falha:

### Classe A — Pertinência semântica insuficiente

Casos:

```text
D2 — Docker → Kubernetes
D3 — SQL → Redis
L1 — Dependency Injection → Spring Data
```

O sistema ainda pode atribuir:

```text
conceptual / positive
correctness: Strong
```

a uma resposta tecnicamente válida, porém inadequada à pergunta.

### Classe B — Falha de invariância de representação

Uma resposta curta correta e uma formulação informal semanticamente equivalente receberam qualificações diferentes.

O objetivo desta etapa é corrigir as causas-raiz dessas duas classes sem:

* calibrar scores diretamente para o humano;
* criar regras específicas para tecnologias;
* criar listas de pares de tecnologias;
* introduzir dependência de senioridade;
* alterar histórico;
* mascarar os findings do Stage 31.3.

---

# 1. Regra fundamental

Não transformar:

```text
Stage 31.3 findings
```

em regras específicas:

```text
if REST → Kafka
if Docker → Kubernetes
if SQL → Redis
if DI → Spring Data
```

Isso é proibido.

A correção deve ser baseada em uma abstração generalizável de:

```text
pergunta
+
resposta
+
intenção
+
relação semântica
```

---

# 2. Histórico

Preservar integralmente:

```text
Stage 31 — Human Evaluation Independent.md
Stage 31 — Human vs System Comparison.md
Stage 31.1 — Human vs System Failure Analysis.md
Stage 31.2 — Controlled Correction.md
Stage 31.2 — Human vs System Post-Correction.md
Stage 31.3 — Post-Correction Blind Validation.md
```

Não alterar os gates históricos.

Especialmente:

```text
Stage 31 = HUMAN_VS_SYSTEM_BLOCKED

Stage 31.3 =
POST_CORRECTION_BLIND_VALIDATION_BLOCKED
```

Esses resultados permanecem históricos.

---

# 3. Antes de corrigir

Reproduzir novamente os casos:

```text
D2
D3
L1
```

e o caso de invariância identificado no Stage 31.3.

Para cada um, registrar:

```text
Question
Response
Evidence
Qualification
Dimensions
Score
```

Localizar o primeiro estágio em que a interpretação diverge do comportamento esperado.

Investigar:

```text
20.x
↓
21 Evidence Model
↓
22 Rubric
↓
23 Evaluation
↓
23.1
↓
23.2
```

Não assumir que o problema pertence ao Stage 23.

---

# 4. Pertinência não é similaridade lexical

A correção não deve utilizar:

```text
keyword overlap
```

como critério suficiente.

Também não deve utilizar:

```text
technology name mismatch
```

como critério suficiente.

Exemplo:

```text
Pergunta:
Como investigaria uma falha 500?

Resposta:
Eu verificaria logs, traces, dependências e métricas da aplicação.
```

A resposta utiliza conceitos diferentes das palavras da pergunta, mas é semanticamente pertinente.

Portanto:

```text
ausência de palavra da pergunta
≠
off_topic
```

---

# 5. Pertinência semântica

Definir uma abstração clara para:

```text
question_intent
```

e:

```text
response_relevance
```

Sem necessariamente adicionar campos ao schema canônico se o comportamento puder ser implementado com os contratos existentes.

A avaliação deve conseguir distinguir:

### Caso A

```text
Resposta diretamente responde à pergunta.
```

### Caso B

```text
Resposta responde parcialmente.
```

### Caso C

```text
Resposta possui conhecimento relacionado, mas não responde à pergunta.
```

### Caso D

```text
Resposta é tecnicamente correta, mas completamente fora do tópico.
```

### Caso E

```text
Resposta não fornece evidência suficiente.
```

---

# 6. Q5, D2, D3 e L1 devem ser casos de teste, não regras

Os quatro casos devem continuar existindo como regressão.

Porém, a correção não deve depender de:

```text
Q5
D2
D3
L1
```

nem dos nomes das tecnologias envolvidas.

Criar novos casos equivalentes utilizando tecnologias diferentes.

Exemplo:

```text
Pergunta A → resposta sobre domínio B
Pergunta C → resposta sobre domínio D
```

O sistema deve identificar a falta de pertinência pela relação semântica, e não pelo par específico.

---

# 7. Teste de generalização por domínio

Criar pelo menos 10 novos casos de pares de domínios não presentes nos findings originais.

Misturar:

* backend;
* frontend;
* banco;
* cloud;
* observabilidade;
* arquitetura;
* mensageria;
* containers;
* segurança;
* testes.

Exemplo conceitual:

```text
Pergunta sobre autenticação
→ resposta sobre cache

Pergunta sobre índices SQL
→ resposta sobre filas

Pergunta sobre Docker networking
→ resposta sobre CI/CD

Pergunta sobre Angular Signals
→ resposta sobre CSS
```

Não utilizar esses pares como regras.

Eles servem apenas para validar a generalização.

---

# 8. Pertinência legítima

Também criar casos onde conceitos diferentes aparecem legitimamente.

Exemplo:

```text
Pergunta:
Como investigaria aumento de latência?

Resposta:
Eu verificaria métricas, logs, traces e dependências externas.
```

Não classificar como off_topic.

Outro exemplo:

```text
Pergunta:
Como projetaria uma API resiliente?

Resposta:
Usaria timeout, retry com backoff, circuit breaker e observabilidade.
```

Os conceitos são diferentes da palavra "API", mas respondem diretamente à intenção.

---

# 9. Relação entre conceitos

Testar:

```text
conceito perguntado
        ↓
conceitos auxiliares legítimos
        ↓
resposta pertinente
```

versus:

```text
conceito perguntado
        ↓
conceito tecnicamente válido
        ↓
sem relação suficiente com a pergunta
```

O sistema deve diferenciar os dois.

---

# 10. Respostas parcialmente pertinentes

Criar casos onde apenas parte da resposta responde à pergunta.

Exemplo:

```text
Pergunta:
Como você investigaria um erro 500?

Resposta:
Primeiro verificaria logs. Também explicaria como Kafka funciona e como configurar consumidores.
```

Esperado:

```text
parte pertinente
+
parte não pertinente
```

Não classificar a resposta inteira como:

```text
Strong
```

apenas porque existe uma parte correta.

Também não classificar automaticamente toda a resposta como:

```text
negative
```

se existe evidência válida.

---

# 11. Invariância de representação

Investigar a causa da diferença encontrada no Stage 31.3:

```text
mesmo conteúdo semântico
+
formulação diferente
=
avaliação diferente
```

Criar pares semanticamente equivalentes:

### Par A — formal

```text
A aplicação utiliza cache para reduzir a latência das consultas.
```

### Par B — informal

```text
A gente usa cache pra deixar as consultas mais rápidas.
```

Esperado:

```text
mesma interpretação técnica
```

---

# 12. Variações de linguagem

Testar equivalência entre:

* português formal;
* português informal;
* pequenos erros gramaticais;
* abreviações comuns;
* hesitações;
* frases curtas;
* frases longas;
* ordem diferente dos elementos;
* sinônimos;
* termos técnicos equivalentes.

Não exigir texto idêntico.

---

# 13. Variação de tamanho

Comparar:

```text
Resposta curta
```

com:

```text
Resposta mais longa semanticamente equivalente
```

Esperado:

```text
mesma correctness
```

Se a resposta longa acrescentar evidência real de:

* profundidade;
* aplicação;
* raciocínio;

ela pode melhorar dimensões correspondentes.

Mas:

```text
mais palavras
≠
mais conhecimento
```

---

# 14. Variação de jargão

Criar:

```text
Resposta A:
linguagem simples

Resposta B:
mesmo conteúdo com jargão técnico
```

Esperado:

```text
mesma avaliação quando o conteúdo semântico é equivalente
```

Jargão adicional sem evidência não deve melhorar a avaliação.

---

# 15. Variação de fluência

Criar:

```text
Resposta A:
fluente

Resposta B:
hesitante

Resposta C:
com pequenos erros linguísticos
```

Se o conteúdo técnico for equivalente:

```text
technical evaluation ≈ equivalente
```

Não penalizar automaticamente:

* sotaque textual;
* gramática imperfeita;
* informalidade;
* hesitação.

---

# 16. Autocorreção

Criar equivalências:

```text
"X é síncrono... quer dizer, assíncrono."
```

versus:

```text
"X é assíncrono."
```

Quando a autocorreção é clara, ambas devem resultar em interpretação compatível.

Não penalizar a primeira formulação simplesmente por conter um erro imediatamente corrigido.

---

# 17. Invariância de senioridade

Manter exatamente a mesma resposta.

Alterar somente:

```text
Junior
Pleno
Senior
```

Esperado:

```text
technical evidence equivalente
```

---

# 18. Invariância de currículo

Executar:

```text
Resposta
```

com e sem:

```text
CV
```

A resposta deve produzir a mesma avaliação técnica.

O CV não pode completar automaticamente evidências ausentes.

---

# 19. Invariância de contexto da vaga

Executar a mesma resposta com diferentes:

* cargos;
* vagas;
* requisitos;
* senioridades esperadas.

A avaliação técnica da resposta deve permanecer equivalente.

Aderência à vaga pertence a etapa posterior.

---

# 20. Não transformar pertinência em gabarito rígido

A correção não deve criar:

```text
pergunta → lista fixa de respostas aceitáveis
```

O sistema deve continuar aceitando múltiplas respostas tecnicamente válidas.

Exemplo:

```text
Pergunta:
Como investigar latência?

Respostas possíveis:
logs
métricas
traces
profiling
dependências
banco
network
APM
```

A ausência de uma palavra específica não deve gerar off_topic.

---

# 21. Falsos negativos

Criar pelo menos 10 casos onde:

```text
pergunta
+
resposta semanticamente pertinente
```

utiliza conceitos que não aparecem literalmente na pergunta.

Nenhum deve ser rejeitado apenas por falta de correspondência lexical.

---

# 22. Falsos positivos

Criar pelo menos 10 casos onde:

```text
resposta tecnicamente correta
+
sem pertinência suficiente
```

O sistema não deve promover essa resposta para:

```text
correctness: Strong
```

sem evidência de que ela realmente responde à pergunta.

---

# 23. Testes de pares mínimos

Para cada par:

```text
Resposta A = pertinente
Resposta B = tecnicamente válida, mas fora do tópico
```

esperar:

```text
A > B
```

em pertinência/correctness.

Porém, não exigir uma diferença específica de score.

---

# 24. Teste de resposta correta curta

Garantir que:

```text
"REST é um estilo arquitetural para APIs baseado em recursos."
```

não receba avaliação inferior apenas porque é curta.

---

# 25. Teste de resposta correta informal

Garantir que:

```text
"REST é basicamente um jeito de fazer API usando recursos e HTTP."
```

não receba avaliação inferior apenas pela informalidade, se o conteúdo estiver tecnicamente adequado ao nível da pergunta.

---

# 26. Teste de resposta polida

Garantir que:

```text
resposta longa
+
jargão
+
boa escrita
```

não seja promovida quando:

```text
evidência técnica
```

não sustenta a conclusão.

---

# 27. Teste de experiência

Preservar os testes anteriores:

```text
declaração
<
demonstração
<
demonstração + raciocínio/troubleshooting
```

A correção de pertinência não pode quebrar essa distinção.

---

# 28. Teste de troubleshooting

Criar pares:

```text
Pergunta:
Como investigaria erro 500?

Resposta A:
Verificaria logs, traces e dependências.

Resposta B:
Eu usaria Kubernetes porque ele gerencia containers.
```

A resposta A é pertinente.

A resposta B pode ser tecnicamente válida, mas não demonstra uma investigação adequada do problema.

---

# 29. Teste de arquitetura

Criar pares semelhantes para:

* SOLID;
* Hexagonal;
* Clean Architecture;
* microservices;
* event-driven;
* resiliency.

Garantir que conceitos relacionados sejam aceitos quando respondem à intenção, mas conceitos simplesmente técnicos não sejam promovidos automaticamente.

---

# 30. Não adicionar regra específica de domínio

É proibido criar:

```text
REST_KAFKA_RULE
DOCKER_KUBERNETES_RULE
SQL_REDIS_RULE
DI_SPRING_DATA_RULE
```

Também é proibido criar listas fixas:

```text
off_topic_pairs = [...]
```

A correção deve operar em nível semântico.

---

# 31. Localizar a causa-raiz

Determinar se o problema está em:

```text
Stage 20
Stage 21
Stage 22
Stage 23
```

ou na interação entre eles.

Documentar:

```text
first_incorrect_artifact
```

e:

```text
correction_scope
```

---

# 32. Correção mínima

A alteração deve:

* ser generalizável;
* preservar schemas quando possível;
* preservar compatibilidade;
* não alterar scores humanos;
* não introduzir regras específicas;
* não depender de candidato;
* não depender de pergunta;
* não depender de tecnologia específica;
* ser testável.

---

# 33. Testes antes da alteração

Criar reproduções que falhem no baseline:

```text
D2
D3
L1
```

e também:

* equivalência curta/informal;
* equivalência formal/informal;
* pertinência semântica;
* conceito relacionado legítimo;
* conceito tecnicamente válido porém fora do tópico.

---

# 34. Aplicar correção

Somente depois das reproduções estarem congeladas:

```text
baseline failing
↓
minimal correction
↓
tests
```

Não alterar o comportamento para satisfazer scores humanos.

---

# 35. Mutation Tests

Executar:

### Mutation A

Trocar resposta pertinente por resposta fora do tópico.

Esperado:

```text
avaliação diminui
```

### Mutation B

Trocar resposta fora do tópico por pertinente.

Esperado:

```text
avaliação melhora
```

### Mutation C

Trocar linguagem formal por informal.

Esperado:

```text
avaliação equivalente
```

### Mutation D

Adicionar jargão sem evidência.

Esperado:

```text
avaliação equivalente
```

### Mutation E

Adicionar evidência técnica real.

Esperado:

```text
dimensões relevantes podem melhorar
```

---

# 36. Blind revalidation

Após a correção:

* não reutilizar os resultados do baseline como expected;
* executar novamente os casos;
* utilizar oráculos independentes;
* registrar Before/After.

O validador deve permanecer separado do código corrigido.

---

# 37. Reexecutar Stage 31.3

Após a correção, reexecutar integralmente:

```text
Stage 31.3
```

Não alterar seu oracle apenas porque o comportamento mudou.

Se um caso anteriormente bloqueado passar:

```text
registrar como resolved
```

Se surgir novo comportamento incorreto:

```text
registrar como regression
```

---

# 38. Reexecutar Stage 31.2

Garantir:

```text
Stage 31.2 tests
```

continuam passando.

---

# 39. Reexecutar Stages anteriores

Executar:

```text
Stage 27
Stage 28
Stage 29
Stage 30
Stage 30.1
Stage 30.2
Stage 30.2.1
Stage 31
Stage 31.1
Stage 31.2
Stage 31.3
```

Não alterar os resultados históricos.

---

# 40. Regressão completa

Executar:

```text
python run_reference_runtime_tests.py
python run_reference_harness.py
```

Registrar resultados.

---

# 41. Determinismo

Executar a suíte pelo menos duas vezes.

Esperado:

```text
Run 1 == Run 2
```

---

# 42. Isolamento

Garantir que resultados não dependam de:

* cache;
* execução anterior;
* ordem;
* arquivos temporários;
* resultados humanos;
* histórico;
* CV;
* vaga;
* senioridade.

---

# 43. Artefatos

Criar:

```text
tests/
    test_stage_31_4_semantic_relevance_invariance_remediation.py
```

e:

```text
11 - Interview Evaluation/
└── 09 - Real Interview Pilot/
    └── Candidato-Piloto-05/
        └── Stage 31.4 — Semantic Relevance & Representation Invariance Remediation.md
```

Não sobrescrever:

```text
Stage 31.3 — Post-Correction Blind Validation.md
```

---

# 44. Relatório

O relatório deve conter:

```text
# Stage 31.4 — Semantic Relevance & Representation Invariance Remediation

## Baseline

## D2

## D3

## L1

## Invariance Finding

## Root Cause

## First Incorrect Artifact

## Correction

## Generalization Strategy

## Positive Cases

## Negative Cases

## Pertinence Tests

## Invariance Tests

## Experience Tests

## Troubleshooting Tests

## Architecture Tests

## Mutation Tests

## Blind Revalidation

## Stage 31.3 After Correction

## Regression

## Determinism

## Limitations

## Gate
```

---

# 45. Métricas

Registrar:

```yaml
validation:
  total_cases:
  passed:
  warnings:
  failed:
  blocked:

relevance:
  false_positive_cases:
  false_negative_cases:
  legitimate_related_cases:
  off_topic_cases:

invariance:
  equivalent_pairs:
  equivalent_results:
  divergent_results:

experience:
  declarations:
  demonstrated:
  hypothetical:

regression:
  stage_31_3:
  stage_31_2:
  full_suite:
  harness:
```

Não inventar métricas.

---

# 46. Critério de sucesso

A etapa pode ser:

```text
SEMANTIC_RELEVANCE_INVARIANCE_REMEDIATION_COMPLETE
```

se:

* D2 resolvido;
* D3 resolvido;
* L1 resolvido;
* invariância resolvida;
* casos novos passam;
* nenhum falso negativo crítico;
* nenhuma regra específica de tecnologia;
* mutation tests passam;
* regressão passa;
* determinismo passa;
* Stage 31.3 pós-correção passa.

---

# 47. Complete with warnings

Usar:

```text
SEMANTIC_RELEVANCE_INVARIANCE_REMEDIATION_COMPLETE_WITH_WARNINGS
```

quando:

* correção funciona;
* não existem falhas críticas;
* existem limitações não bloqueantes;
* algum cenário residual permanece devidamente caracterizado.

---

# 48. Blocked

Usar:

```text
SEMANTIC_RELEVANCE_INVARIANCE_REMEDIATION_BLOCKED
```

se:

* pertinência continuar incorreta;
* falsos negativos críticos forem introduzidos;
* invariância continuar quebrada de forma material;
* correção depender de regras específicas;
* regressão crítica surgir;
* runtime precisar ser alterado repetidamente apenas para fazer testes passarem.

---

# 49. Proibição de overfitting

Não criar:

```text
if Q5
if D2
if D3
if L1
```

Não criar listas de pares de tecnologias.

Não usar scores humanos como target.

Não ajustar pesos para reproduzir o avaliador humano.

Não alterar os oráculos para acomodar o runtime.

---

# 50. Regra final

O objetivo não é fazer:

```text
Docker → Kubernetes
SQL → Redis
DI → Spring Data
```

serem reconhecidos como off_topic individualmente.

O objetivo é corrigir o princípio:

```text
conteúdo tecnicamente válido
        ≠
resposta semanticamente adequada à pergunta
```

e garantir simultaneamente:

```text
mesmo conteúdo semântico
+
formulação diferente
=
mesma interpretação técnica
```

A arquitetura desejada é:

```text
Question
   ↓
Question Intent
   ↓
Response
   ↓
Semantic Relevance
   ↓
Evidence Qualification
   ↓
Dimensions
   ↓
Score
```

e não:

```text
Response contains technical concept
        ↓
conceptual positive
        ↓
correctness Strong
```

Somente depois de demonstrar que essa distinção é generalizável, invariável à forma de expressão e livre de regressões o sistema poderá retornar à validação do Stage 31 e, posteriormente, considerar o Stage 32.
