# GEMINI GUARDRAILS

## Propósito

Este documento contém regras obrigatórias para qualquer agente de IA que altere o projeto.

Não são sugestões.

---

# 1. NÃO RECOMEÇAR O PROJETO

Não redesenhar a arquitetura existente sem demonstrar primeiro que a arquitetura atual é inadequada.

Não substituir:

* Evidence Model;
* Rubric;
* Evaluation Engine;
* Transcription Pipeline;
* Pipeline;
* Reference Runtime;
* Harness;

por uma solução nova apenas por preferência arquitetural.

---

# 2. NÃO PULAR STAGES

Não avançar para um stage posterior enquanto o stage atual estiver:

```text
BLOCKED
```

especialmente:

```text
Stage 31
Stage 31.3
Stage 31.4
```

Um warning pode permitir continuidade.

Um BLOCKED exige investigação/correção antes do avanço.

---

# 3. NÃO APAGAR HISTÓRICO

Nunca apagar ou sobrescrever:

* relatórios históricos;
* resultados de validação;
* gates;
* failures;
* blocked stages;
* análises de causa raiz.

Uma correção deve gerar nova evidência.

---

# 4. NÃO OTIMIZAR PARA SCORE

Nunca alterar a lógica com objetivo explícito de:

* aumentar score;
* diminuir score;
* aproximar média humana;
* reduzir MAE artificialmente;
* passar um caso específico.

Se uma mudança aproximar os resultados humanos, isso deve ser consequência da correção semântica, não o objetivo.

---

# 5. NÃO USAR HUMAN SCORE COMO TARGET

Human evaluation pode ser usada para:

* encontrar divergências;
* investigar erros;
* validar comportamento.

Não pode ser usada como:

```text
expected score
```

durante execução cega.

---

# 6. NÃO CRIAR REGRAS POR TECNOLOGIA

Não criar listas específicas como:

```text
REST → Kafka = off-topic
Docker → Kubernetes = related
SQL → Redis = off-topic
```

Os casos de teste devem testar a abstração.

---

# 7. NÃO CONFUNDIR RELAÇÃO COM RESPOSTA

Uma resposta pode ser:

```text
tecnicamente correta
```

e ainda assim:

```text
não responder à pergunta
```

O sistema deve avaliar relevância semântica.

---

# 8. NÃO CONFUNDIR EXPERIÊNCIA

Nunca transformar:

```text
"Já trabalhei com X."
```

automaticamente em:

```text
experiência demonstrada
```

Da mesma forma:

```text
hipótese
```

não é:

```text
experiência real
```

---

# 9. NÃO CONFUNDIR AUSÊNCIA

Nunca transformar:

```text
evidência ausente
```

em:

```text
conhecimento inexistente
```

---

# 10. NÃO CONFIAR EM PALAVRAS-CHAVE

Keyword matching pode auxiliar.

Não pode ser a base semântica principal.

Exemplo:

```text
Docker
Kubernetes
container
```

não determinam sozinhos se uma resposta responde à pergunta.

---

# 11. NÃO ALTERAR TESTES PARA FAZER PASSAR

Se o sistema falhar:

1. investigar;
2. reproduzir;
3. classificar;
4. corrigir código se necessário;
5. só alterar teste se o teste estiver objetivamente incorreto.

Nunca mudar oracle apenas porque a implementação não passou.

---

# 12. NÃO REDUZIR O PROBLEMA

Se um teste revelar:

```text
D2
D3
L1
```

não implementar três patches isolados.

Perguntar:

> Qual propriedade comum está sendo violada?

---

# 13. SEMPRE PROCURAR A PRIMEIRA FALHA

Ao investigar:

```text
Transcript
↓
Question
↓
Response
↓
Linking
↓
Reconstruction
↓
Evidence
↓
Evaluation
↓
Global
```

encontrar o primeiro ponto em que o significado foi alterado incorretamente.

Corrigir preferencialmente ali.

---

# 14. BLIND MEANS BLIND

Durante execução cega:

O executor não pode conhecer:

* resultado esperado;
* score humano;
* score histórico;
* resposta de referência;
* evidência de referência.

---

# 15. PRESERVAR SEPARAÇÃO DE RESPONSABILIDADES

```text
20.x
→ processamento da transcrição

21
→ evidências

22
→ rubrica

23
→ avaliação

23.1
→ auditoria

23.2
→ materialização

24
→ orquestração

25+
→ validação
```

Não colocar scoring dentro de transcription processing.

Não colocar transcript parsing dentro do Evaluation Engine.

Não colocar lógica de contratação no Evaluation Engine.

---

# 16. NÃO ADICIONAR SENIORIDADE AUTOMÁTICA

Nunca inferir:

```text
7 = Pleno
8 = Senior
9 = Staff
```

Isso é proibido.

---

# 17. NÃO ADICIONAR DECISÃO DE CONTRATAÇÃO

Não produzir automaticamente:

```text
Aprovado
Reprovado
Contratar
Não contratar
Melhor candidato
```

A avaliação técnica é uma camada diferente.

---

# 18. PROTEÇÃO DE ARTEFATOS

Antes de qualquer alteração:

identificar artefatos canônicos e históricos.

Não modificar sem necessidade:

```text
AGENTS.md
SECOND_BRAIN.md
Evidence Model
Scoring Rubric
Evaluation Engine
Individual Evaluations
Evidence Set
Structured Interview
Interview Evaluation v1
Interview Evaluation v2
Stage reports
```

Se uma alteração nesses arquivos for realmente necessária:

* justificar;
* testar;
* documentar.

---

# 19. TODA CORREÇÃO DEVE TER REGRESSÃO

Toda mudança semântica deve possuir:

```text
reproduction test
+
regression test
```

Sempre que possível:

```text
mutation test
+
invariance test
```

---

# 20. RESULTADO BLOCKED É UM RESULTADO VÁLIDO

Não tentar transformar:

```text
BLOCKED
```

em:

```text
PASS
```

sem corrigir a causa.

Um bloqueio é informação.

---

# 21. WARNING NÃO É FAIL

Distinguir:

```text
PASS
PASS_WITH_WARNING
BLOCKED
FAIL
```

Não transformar warning em falha.

Não esconder warning.

---

# 22. NÃO MODIFICAR PRODUÇÃO DURANTE BLIND VALIDATION

Durante validação cega:

```text
runtime congelado
```

A validação deve avaliar a implementação existente.

---

# 23. ALTERAÇÕES DEVEM SER MÍNIMAS

Preferir:

```text
menor mudança
que resolve a causa geral
```

em vez de:

```text
grande refatoração
```

---

# 24. NÃO INTRODUZIR COMPLEXIDADE SEM NECESSIDADE

O objetivo não é construir o maior framework possível.

Cada nova abstração deve resolver um problema demonstrado.

---

# 25. ORDEM OBRIGATÓRIA DE RACIOCÍNIO

Antes de alterar código:

```text
Qual é o problema?
↓
Consigo reproduzir?
↓
Onde nasce?
↓
É local ou estrutural?
↓
Qual propriedade deveria existir?
↓
Como testar essa propriedade?
↓
Qual é a menor correção generalizável?
↓
Quais regressões podem acontecer?
```

---

# 26. CHECKPOINT OBRIGATÓRIO

Antes de finalizar qualquer stage, responder:

```text
[ ] Li AGENTS.md
[ ] Li SECOND_BRAIN.md
[ ] Li GEMINI_HANDOFF.md
[ ] Li GEMINI_GUARDRAILS.md
[ ] Identifiquei o stage atual
[ ] Identifiquei o gate anterior
[ ] Reproduzi o problema
[ ] Identifiquei causa raiz
[ ] Evitei overfitting
[ ] Criei regressão
[ ] Rodei regressão existente
[ ] Preservei histórico
[ ] Preservei rastreabilidade
[ ] Preservei separação de responsabilidades
[ ] Não introduzi senioridade/hiring
[ ] Não usei score humano como target
[ ] Não alterei teste apenas para passar
```

---

# 27. REGRA SUPREMA

Quando houver dúvida entre:

```text
uma solução que parece funcionar
```

e:

```text
uma solução que pode ser demonstrada, testada e explicada
```

escolher a segunda.

> **O objetivo não é fazer o pipeline passar. O objetivo é construir um pipeline em que o motivo de ele passar possa ser defendido.**
