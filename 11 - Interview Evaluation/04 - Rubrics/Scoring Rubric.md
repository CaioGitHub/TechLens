---
type: concept
status: understood
confidence: 100
created: 2026-09-09
updated: 2026-09-19
tags:
  - interview-evaluation
  - meta
---
# Scoring Rubric

Esta nota define a rubrica utilizada para transformar as evidências identificadas em [[Evidence Model]] em uma nota de 0 a 10 para uma resposta técnica individual.

Esta etapa define **como pontuar uma resposta**. Ela não implementa o motor completo de avaliação da entrevista, nem:

- média final da entrevista;
- pesos entre perguntas;
- avaliação de senioridade;
- ranking de candidatos;
- decisão de contratação;
- contexto específico da vaga;
- motor automatizado completo;
- processamento de transcrições;
- classificação final do candidato.

Esses elementos pertencem a etapas posteriores (ver [[Interview Evaluation MOC]]).

## 1. Princípio fundamental

A nota representa a qualidade da evidência técnica apresentada na resposta em relação ao que a pergunta solicita.

Não avaliar: eloquência isoladamente, quantidade de texto, quantidade de termos técnicos, confiança do candidato, cargo atual, anos de experiência, empresa onde trabalha, formação, velocidade da resposta, uso de palavras "de senior", ou semelhança literal com uma resposta existente no Second Brain.

```text
Pergunta      = o contexto
Resposta      = a evidência
Second Brain  = a referência técnica
Nota          = a conclusão fundamentada
```

## 2. Escala

Escala contínua de `0.0` a `10.0`. Quando a evidência não justificar maior precisão, preferir notas inteiras ou incrementos de `0.5` (ex.: 3.0, 4.5, 6.0, 7.5, 8.0, 9.5). Evitar precisão artificial (ex.: 7.83) sem evidência que a sustente.

## 3. Dimensões de avaliação

| Dimensão | Peso de referência |
|---|---|
| Correção técnica | 40% |
| Completude | 20% |
| Profundidade | 15% |
| Raciocínio e clareza | 10% |
| Aplicação prática | 10% |
| Trade-offs / decisão técnica | 5% |

Esses pesos são referência geral, não regra matemática absoluta.

### Dimensões condicionais

Nem toda pergunta exige todas as dimensões. Identificar, usando a classificação de [[Question Taxonomy]] (tipo, dimensões, complexidade), quais dimensões são relevantes antes de avaliar. Não penalizar o candidato por não abordar algo que a pergunta não solicitou.

Exemplos:
- "O que é uma interface em Java?" → aplicação prática e trade-offs podem ter pouca ou nenhuma relevância.
- "Como você escolheria entre interface e classe abstrata?" → correção, profundidade, raciocínio, aplicação e trade-offs tendem a ser relevantes.
- "Como investigaria uma API Spring Boot lenta?" → correção, completude, raciocínio, aplicação prática, observabilidade e troubleshooting tendem a ser mais relevantes.

### N/A e normalização de pesos

Uma dimensão marcada `N/A` **não participa** da avaliação daquela resposta e **não é tratada como zero**. Os pesos das dimensões aplicáveis devem ser normalizados proporcionalmente para representar 100% da importância relativa restante.

Exemplo — se `Trade-offs` (5%) for `N/A`:

```text
Pesos originais:
Correção 40% · Completude 20% · Profundidade 15% · Raciocínio 10% · Aplicação 10% · Trade-offs 5%

Pesos aplicáveis normalizados (÷ 0,95):
Correção ≈ 42,11% · Completude ≈ 21,05% · Profundidade ≈ 15,79% ·
Raciocínio ≈ 10,53% · Aplicação ≈ 10,53%
```

Esses valores são referência relativa para o julgamento integrado (ver seção 3.1) — não substituem a avaliação qualitativa. Se uma dimensão simplesmente não fizer sentido para a pergunta (ex.: pergunta puramente conceitual com Trade-offs = N/A e Aplicação prática = N/A), removê-la do conjunto avaliável e não penalizar a resposta por não demonstrar algo que a pergunta não solicitou.

### 3.1 Mecânica da nota final (reconciliação entre pesos, âncoras e julgamento)

O sistema combina três elementos que devem ser usados de forma reconciliada, não conflitante:

```text
Evidências
   ↓
Avaliação das dimensões aplicáveis (qualitativa)
   ↓
Referência de pesos (importância relativa, seção 3)
   ↓
Julgamento integrado
   ↓
Âncora 0–10 (seção 10)
   ↓
Nota final
```

**Decisão arquitetural:** a nota final é uma **avaliação integrada** baseada nas evidências e nas dimensões relevantes da resposta. Os pesos representam a importância relativa das dimensões e servem como estrutura de julgamento — **não constituem uma fórmula mecânica obrigatória** que converte rótulos qualitativos (Forte/Moderada/Fraca/etc.) em números e os some automaticamente. As dimensões são avaliadas qualitativamente (ver seções 4–9) e servem para **justificar** a nota; elas não são convertidas automaticamente em números por uma regra fixa.

A pergunta que orienta a nota final é sempre:

```text
"Considerando o que foi demonstrado e a importância das dimensões
aplicáveis, em qual ponto da escala 0–10 esta resposta se encontra?"
```

A nota deve ser posicionada preferencialmente nas âncoras `0, 2, 4, 6, 8, 10` (seção 10), podendo usar valores intermediários em incrementos de `0,5` quando houver evidência suficiente para justificar maior precisão. Evitar falsa precisão (ex.: 7,13 · 8,27 · 9,46).

**Regra contra média mecânica:** a nota não deve ser calculada mecanicamente como média das dimensões quando isso produzir uma representação inadequada da qualidade da resposta. Casos ilustrativos:

- **Caso 1 — erro central com boas demais dimensões:** uma resposta com Clareza: Forte, Aplicação: Forte e Profundidade: Forte, mas que contém um erro central sobre o conceito perguntado, não deve ter esse erro "compensado" pelas demais dimensões — a correção tem peso dominante na conclusão.
- **Caso 2 — excelente correção, pouca profundidade:** uma resposta objetiva e correta pode receber nota alta mesmo sem demonstrar profundidade adicional, quando a pergunta não exige profundidade além da correção.
- **Caso 3 — pergunta simples:** não exigir profundidade ou trade-offs que não sejam relevantes para a pergunta (consistente com "Dimensões condicionais" acima).

O esquema de dados normalizado desta avaliação (campos, tipos e nomes) está definido de forma canônica em [[Evaluation Engine]] — esta nota não duplica esse esquema (ver seção 19).

## 4. Correção técnica

Avalia se o que o candidato afirmou está tecnicamente correto: fatos, conceitos, relações entre conceitos, funcionamento, comportamento, limitações, afirmações condicionais, versão tecnológica relevante.

Níveis orientativos: **Forte** (correta, sem erros relevantes) · **Moderada** (majoritariamente correta, pequenas imprecisões que não comprometem o conceito central) · **Fraca** (erros relevantes, mas parte do entendimento correta) · **Muito baixa** (conceito central incorreto ou incompatível com o solicitado).

### Erros centrais vs periféricos vs críticos

- **Erro periférico**: imprecisão secundária que não altera o entendimento principal. Pode reduzir a nota, mas não deve destruir a avaliação inteira.
- **Erro relevante**: afeta parte importante da resposta, mas não o conceito central perguntado. Reduz a nota de forma proporcional à importância da parte afetada, sem necessariamente comprometer toda a avaliação.
- **Erro central**: altera fundamentalmente o conceito avaliado (ex.: atribuir a um mecanismo uma responsabilidade que pertence a outro componente). Deve impactar significativamente a nota.
- **Erro crítico**: erro grave, central e potencialmente incompatível com o cenário avaliado — ocorre quando o erro invalida a decisão técnica, demonstra desconhecimento fundamental, pode gerar solução tecnicamente perigosa, envolve segurança, perda de dados, confiabilidade grave, ou contradiz diretamente o requisito central da pergunta.

**Faixa orientativa para erro crítico** (não é um teto rígido universal): um erro crítico central normalmente impede notas de excelência (9–10) e pode limitar a nota para uma faixa baixa ou intermediária, dependendo do restante das evidências. A nota final deve considerar: centralidade do erro; gravidade; impacto; contexto; se o candidato corrigiu espontaneamente (ver seção 16); e se o restante da resposta demonstra compreensão suficiente para contextualizar o erro. Não transformar isso em uma regra fixa do tipo "erro crítico = nota máxima X" — a decisão permanece contextual e deve ser explicada na justificativa (seção 18). Registrar explicitamente sempre que um erro crítico ocorrer.

## 5. Completude

Avalia quanto do que era razoavelmente necessário para responder à pergunta foi abordado, relativo à pergunta, tipo, complexidade e contexto. Não exigir resposta enciclopédica.

Níveis: **Alta** (cobre praticamente todos os aspectos essenciais) · **Média** (cobre o núcleo, mas deixa lacunas relevantes) · **Baixa** (aborda apenas uma parte pequena do necessário) · **Insuficiente** (não apresenta elementos suficientes para responder).

## 6. Profundidade

Profundidade não significa quantidade de texto. Avaliar entendimento de causa e efeito, compreensão de mecanismos, relações entre conceitos, limitações, consequências, condições de uso, capacidade de explicar "por quê", capacidade de ir além da definição superficial.

Exemplo: "Virtual Threads são threads leves" pode estar correto, mas com pouca profundidade. Uma explicação que também aborda modelo de execução, uso apropriado, limitações e relação com I/O demonstra maior profundidade.

## 7. Raciocínio e clareza

Avaliar estrutura lógica, relação causa/consequência, coerência, capacidade de justificar decisões, capacidade de explicar o processo de pensamento técnico, identificação de premissas relevantes.

Não confundir clareza técnica com sotaque, estilo pessoal de fala, velocidade, vocabulário sofisticado ou capacidade de falar muito. Uma resposta curta e logicamente consistente pode receber pontuação alta.

## 8. Aplicação prática

Avaliar se o candidato conecta o conhecimento à prática quando relevante: exemplos reais, implementação, configuração, troubleshooting, arquitetura, decisões tomadas, consequências observadas, experiência prática demonstrada.

Não exigir experiência prática em perguntas puramente conceituais. Não assumir experiência apenas porque o candidato afirmou possuí-la — diferenciar "eu já fiz isso" de uma demonstração concreta de como, por que e com quais consequências.

### 8.1 Perguntas de Experiência prática — critério de pontuação

Perguntas do tipo `Experiência prática` (ver [[Question Taxonomy]], §2.14) continuam recebendo nota `0–10` normalmente — não existe regra que force `N/A` para esse tipo de pergunta. A nota reflete **o que foi demonstrado na resposta**, nunca uma conclusão sobre a vida profissional real do candidato.

**Regra fundamental:**

```text
Experiência declarada ≠ Experiência demonstrada ≠ Ausência de experiência
```

A pergunta que orienta a nota é sempre "o que esta resposta demonstrou?", nunca "o candidato possui ou não possui essa experiência?" quando a resposta não fornece evidência suficiente para essa segunda pergunta.

**Escala de demonstração** (orientativa, não é um novo esquema de pontuação — apenas descreve o padrão de evidência esperado ao aplicar a escala 0–10 desta rubrica a perguntas de experiência):

- **Apenas declaração** (ex.: "Sim, trabalhei bastante com observabilidade", sem exemplos, ferramentas, decisões ou situações concretas): Experiência declarada presente; Experiência demonstrada e evidência técnica insuficientes. Nota baixa, coerente com a insuficiência da resposta ao que foi solicitado — não com uma conclusão de que o candidato não tem a experiência.
- **Declaração + poucos detalhes técnicos** (ex.: menciona uma ferramenta e um uso genérico, sem aprofundar): experiência demonstrada parcial; evidência técnica presente, porém limitada. Nota superior ao caso anterior, quando a pergunta permitir essa distinção.
- **Experiência concreta** (descreve o que fazia, com que ferramenta, em que situação): experiência demonstrada presente; nota reflete a força dessa evidência nas dimensões aplicáveis (aplicação prática, raciocínio, etc.).
- **Experiência + raciocínio/trade-offs** (descreve também o porquê das decisões, consequências, ou trade-offs considerados): evidência mais forte; nota mais alta que os casos anteriores, quando a pergunta permitir avaliar essas dimensões.

Essa escala de demonstração não substitui as âncoras 0–10 da seção 10 — apenas orienta como posicionar a nota dentro delas quando a pergunta é do tipo Experiência prática.

**Casos específicos:**

- **Erro técnico dentro de uma experiência concreta**: se o candidato descreve uma experiência real, mas comete um erro técnico relevante ao explicá-la (ex.: afirma algo tecnicamente incorreto sobre a ferramenta que diz ter usado), avaliar normalmente pelas regras de correção técnica (seção 4) — existe evidência concreta, e parte dela é tecnicamente incorreta. Não reduzir a resposta a "experiência insuficiente"; tratar como experiência demonstrada com erro técnico identificado, com impacto proporcional à centralidade do erro.
- **"Não lembro" / detalhes esquecidos**: registrar experiência declarada presente e demonstração/evidência limitada ou insuficiente, conforme o restante da resposta. Não inferir automaticamente ausência de experiência, nem classificar a lacuna de memória como erro técnico.
- **Resposta hipotética** (ex.: "se eu tivesse esse problema, eu começaria verificando..."): pode demonstrar conhecimento conceitual e raciocínio, mas **não** demonstra experiência prática. Registrar essas evidências separadamente — conhecimento/raciocínio demonstrado (possivelmente forte) e experiência prática demonstrada (insuficiente) — e não atribuir experiência prática com base apenas na resposta hipotética.

**Regras de invariância** (reforçando regras já existentes contra viés, seção 1 e seção 20):

- Anos de experiência declarados (2 anos vs. 12 anos) não alteram a nota quando a evidência técnica apresentada é a mesma.
- O tom de confiança verbal ao declarar experiência ("tenho bastante experiência" vs. "acredito que tenho alguma experiência") não altera a nota quando a evidência técnica é a mesma.
- Extensão da resposta não substitui evidência (ver seção 15) — também se aplica a respostas de experiência.

**Justificativa e confiança:** ao atribuir nota baixa por declaração sem demonstração, a justificativa deve usar linguagem como "a resposta demonstra experiência apenas de forma declarativa, sem evidências técnicas suficientes para avaliar aplicação prática ou profundidade" — nunca "o candidato não possui experiência". A confiança pode ser Alta mesmo com nota baixa, pois é possível ter certeza de que a resposta não demonstrou o que foi pedido; isso não equivale a ter certeza de que o candidato carece da experiência na vida real (ver [[Evidence Model]], seção 28, e [[Job Context Model]], seção 8, para a distinção entre Interview Evidence, External Evidence e Declared Experience).

## 9. Trade-offs e tomada de decisão

Avaliar reconhecimento de que decisões técnicas têm consequências: vantagens, desvantagens, custos, complexidade, performance, manutenção, segurança, escalabilidade, confiabilidade, contexto, alternativas.

Não exigir trade-offs em perguntas que não envolvam decisão; não penalizar a ausência quando a pergunta não os solicita.

## 10. Escala de referência (âncoras)

| Nota | Descrição |
|---|---|
| **0** | Sem evidência válida — não responde à pergunta, resposta completamente incorreta, desconhecimento total do conceito central, ou evidência insuficiente para considerar que houve resposta técnica válida. |
| **2** | Muito fraca — fragmentos corretos podem existir; conceito central incorreto ou extremamente superficial; pouca ou nenhuma compreensão demonstrada; não sustenta a resposta. |
| **4** | Fraca / parcial — demonstra algum conhecimento; parte correta; lacunas importantes ou erros relevantes; não cobre adequadamente o que a pergunta exige. |
| **6** | Adequada — responde corretamente ao núcleo da pergunta; conhecimento funcional; pode ter lacunas; profundidade limitada; pode precisar de complementação em cenários mais complexos. |
| **8** | Forte — tecnicamente correta; boa cobertura dos aspectos relevantes; entendimento além da definição básica; bom raciocínio; conecta conceitos quando relevante; pequenas lacunas sem comprometer a qualidade geral. |
| **10** | Excelente — tecnicamente sólida e completa para o contexto; demonstra profundidade; explica mecanismos e consequências quando relevantes; bom raciocínio; aplicação prática quando solicitada; reconhece limitações e trade-offs quando relevantes; não depende de jargões para parecer sofisticada. |

### Interpolação entre âncoras

Notas intermediárias representam estados entre as âncoras.

- **7**: entre adequada e forte — claramente correta e com bom domínio, mas com lacuna ou profundidade menor que uma resposta nível 8.
- **9**: entre forte e excelente — domínio muito elevado, mas com pequena lacuna, simplificação ou ausência de algum aspecto secundário.

Não usar a nota 10 como sinônimo de "resposta muito boa" — deve representar uma resposta praticamente completa para o que foi solicitado.

## 11. Complexidade da pergunta

A complexidade definida em [[Question Taxonomy]] (Básica/Intermediária/Avançada) deve ser considerada na interpretação da resposta, mas **complexidade da pergunta não é qualidade da resposta**.

- Uma excelente resposta a uma pergunta básica continua excelente para aquela pergunta.
- Uma resposta correta a uma pergunta avançada pode receber nota adequada mesmo sem demonstrar domínio de conhecimentos que a pergunta não exigiu.

Não aumentar a nota apenas porque a pergunta é difícil; não reduzir a nota apenas porque a pergunta é fácil.

## 12. Respostas alternativas válidas

O Second Brain não é gabarito rígido. Se a solução do candidato diferir da registrada na base, verificar se é tecnicamente válida, em quais contextos funciona, quais suas limitações, se existe alternativa igualmente válida, e se a diferença representa preferência, trade-off ou erro. Não classificar automaticamente como incorreta uma resposta que não esteja registrada na base.

### 12.1 Neutralidade de tecnologia/framework/stack

Uma resposta tecnicamente válida não deve receber redução de nota apenas por utilizar uma tecnologia, framework, biblioteca ou padrão diferente daquele que o candidato declarou como principal, **quando a pergunta não exigiu explicitamente esse stack**. Analisar primeiro o que a pergunta efetivamente solicitou:

```text
Pergunta pede conceito/comportamento genérico (ex.: "diferença entre
@Produces e @Consumes em APIs REST") + resposta correta em outro
stack/framework (ex.: JAX-RS/Jakarta REST em vez de Spring MVC)
   → conceito correto + aplicação tecnicamente válida = evidência positiva
   → não penalizar apenas por divergir do stack declarado como principal.

Pergunta exige explicitamente um stack (ex.: "como você implementaria isso
usando Spring Boot?") + resposta usa exclusivamente outro framework sem
relacionar ao stack pedido
   → pode haver lacuna de aplicação específica ao stack exigido
     (ver seção 14, "Ausência de informação") — registrar como lacuna,
     não converter automaticamente em erro conceitual se o raciocínio
     geral estiver correto.
```

Considerar a diferença de tecnologia/framework como fator negativo apenas quando: (1) a pergunta exigir explicitamente determinado framework/stack; (2) a resposta afirmar algo tecnicamente incorreto sobre o framework exigido; (3) o candidato demonstrar confusão relevante entre conceitos incompatíveis entre os dois stacks; ou (4) a diferença tecnológica impedir que a resposta satisfaça o que foi efetivamente solicitado. Manter sempre distintos:

```text
Erro técnico ≠ Diferença de stack ≠ Diferença de estilo ≠
Não utilização da tecnologia declarada como principal
```

A diferença de stack pode ser registrada como observação/contexto na justificativa, mas não deve, isoladamente, reduzir a nota.

## 13. Respostas condicionais

Uma resposta do tipo "eu usaria X quando... mas Y quando..." deve ser avaliada verificando se a condição faz sentido, se o raciocínio é tecnicamente válido, se o candidato reconheceu o contexto, e se a decisão possui justificativa. Não considerar evasiva uma resposta condicional quando a própria pergunta possui múltiplos contextos possíveis.

## 14. Ausência de informação

Não confundir "não mencionou X" com "não sabe X". A ausência pode reduzir a completude quando X era necessária, mas não deve gerar automaticamente conclusão de desconhecimento — registrar como evidência ausente (ver [[Evidence Model]]).

## 15. Extensão da resposta

- **Resposta curta**: pode receber 8, 9 ou 10 se responder correta e suficientemente ao que foi perguntado. Não exigir explicação longa para nota alta.
- **Resposta longa**: não recebe nota alta automaticamente. Avaliar relevância, precisão, coerência, profundidade e completude. Informação irrelevante não conta positivamente; jargão sem demonstração de entendimento não conta como evidência forte.

## 16. Contradições e autocorreção

**Contradições internas**: identificar a contradição, registrar as duas afirmações, determinar se afeta o conceito central, e reduzir a nota proporcionalmente à relevância. Uma contradição central tem impacto maior que uma inconsistência periférica.

**Autocorreção espontânea**: se o candidato inicialmente errar e depois se corrigir espontaneamente, registrar ambas as evidências. A autocorreção demonstra capacidade de revisão do raciocínio — não tratar como se o erro inicial nunca tivesse ocorrido, mas também não penalizar como quem permaneceu no erro.

## 17. Confiança da avaliação

Independente da nota. Níveis: **Alta** (evidências claras e suficientes) · **Média** (evidência razoável, mas com ambiguidade ou ausência que limita a certeza) · **Baixa** (transcrição, pergunta, resposta ou contexto não fornece evidência suficiente para avaliação precisa).

Exemplo: `Nota: 7.0 · Confiança: Baixa` significa "a melhor estimativa é 7.0, mas não há evidência suficiente para afirmar isso com alta segurança". Não transformar baixa confiança automaticamente em nota baixa.

## 18. Justificativa obrigatória

Toda nota deve possuir justificativa baseada nas evidências, explicando por que a nota foi atribuída — não repetindo a resposta do candidato.

Formato recomendado:

```text
Nota: 7.5
Confiança: Alta

Justificativa:
A resposta demonstra entendimento correto do conceito central e apresenta
bom raciocínio sobre sua aplicação. Entretanto, não aborda X, que era
um aspecto relevante da pergunta, e não discute Y.

Evidências principais:
- Positiva: ...
- Positiva: ...
- Ausente: ...
- Parcial: ...
```

## 19. Esquema de dados canônico

O esquema normalizado (YAML) para representar a avaliação de uma pergunta — incluindo pergunta, esperado, evidências, dimensões, nota, confiança, achados e justificativa — é definido de forma **canônica em [[Evaluation Engine]]** (seção "Estrutura normalizada"). Esta nota não duplica esse esquema; ao produzir dados estruturados, utilizar exclusivamente o formato definido lá, preenchendo as dimensões e a nota conforme as regras desta rubrica (seções 3–18).

## 20. Regras contra viés de avaliação

Nunca aumentar a nota por: falar muito, usar termos técnicos, citar frameworks ou empresas, afirmar experiência, demonstrar confiança, possuir cargo elevado ou muitos anos de experiência.

Nunca reduzir a nota por: responder de forma objetiva, usar linguagem simples, não usar jargões, apresentar abordagem diferente do Second Brain, não citar um detalhe que não era necessário.

Avaliar sempre o conteúdo técnico efetivamente demonstrado.

## 21. Exemplos

### Estratégia coerente de troubleshooting

```text
Pergunta: "Como você investigaria uma API Spring Boot que começou a
apresentar aumento de latência?"

Resposta: "Primeiro eu verificaria se o problema está concentrado em algum
endpoint. Depois olharia métricas de latência e identificaria se alguma
dependência está demorando mais. Também utilizaria traces para entender
em qual etapa da requisição o tempo está sendo gasto."

Nota: 8.0 · Confiança: Alta
Justificativa: estratégia coerente de investigação (escopo → métricas →
dependências → traces), demonstrando troubleshooting e observabilidade
aplicados. Não recebe 10 por não abordar comparação temporal, análise de
logs, correlação com mudanças recentes ou validação da hipótese.
```

### Resposta superficial, mas correta

```text
Pergunta: "O que é uma Virtual Thread em Java?"
Resposta: "É uma thread mais leve do Java que permite executar muitas tarefas."

Nota: 6.0 · Confiança: Alta
A resposta captura corretamente o conceito básico, mas com pouca
profundidade. Não reduzir excessivamente por não explicar todos os
detalhes internos.
```

### Erro central

```text
Pergunta: "Qual é o objetivo da Inversão de Dependência?"
Resposta: "O objetivo é fazer com que módulos de alto nível dependam
diretamente das implementações concretas dos módulos de baixo nível."

Nota: 2.0 · Confiança: Alta
O erro atinge diretamente o conceito central da pergunta.
```

### Estrutura alternativa válida

```text
Pergunta: "Como você estruturaria uma aplicação seguindo Hexagonal Architecture?"

O Second Brain pode registrar uma organização baseada em Domain, Application,
Ports, Adapters, Infrastructure. Se o candidato apresentar organização
diferente, não considerar a diferença estrutural como erro automaticamente.
Avaliar: direção das dependências, isolamento do core, papel dos ports,
adapters, independência das regras de negócio, testabilidade e coerência
arquitetural — não a estrutura de pastas em si.
```

## 22. Nota não representa senioridade

Não converter automaticamente `8.0 = Senior`, `7.0 = Pleno`, `6.0 = Júnior` — essa relação é inválida. A nota representa a qualidade da resposta àquela pergunta específica.

A avaliação de senioridade exigirá, em etapas posteriores, conjunto de perguntas, complexidade, consistência, profundidade, aplicação, troubleshooting, arquitetura, tomada de decisão, experiência demonstrada e contexto da vaga.

## 23. Regra final

O Codex deve sempre conseguir responder: "Qual evidência presente na resposta justifica essa nota?" Se não conseguir responder, a nota possui fundamentação insuficiente.

Ordem correta:

```text
Pergunta → Evidências → Dimensões relevantes → Qualidade da resposta →
Nota 0–10 → Confiança → Justificativa
```

Nunca:

```text
Pergunta → Resposta parece boa → Nota intuitiva
```

## 24. Auditoria da Etapa 19 e da Etapa 19.1

A rubrica existente foi auditada contra os requisitos de calibração informados para as Etapas 19 e 19.1. A busca no repositório não encontrou documentos separados para essas etapas nem registros persistidos dos casos `CAL-01` a `CAL-10`. Portanto, os resultados abaixo são mantidos como **baseline de regressão declarado para esta etapa**, não como evidência de que uma execução histórica foi reprocessada neste momento.

Não substituir esses resultados por uma nova interpretação. Qualquer execução futura deve comparar a nota produzida com a faixa esperada e registrar a justificativa quando houver divergência.

| Caso | Cenário | Resultado esperado |
|---|---|---|
| `CAL-01` | Experiência declarada sem evidência concreta | aproximadamente `2.0`; `confidence: high` significa alta confiança de que a experiência não foi demonstrada, não que o candidato não conhece o assunto |
| `CAL-02` | Virtual Threads superficial | aproximadamente `4.0`; terminologia correta sem explicação suficiente não deve inflar a nota |
| `CAL-03` | Virtual Threads e Platform Threads invertidos | aproximadamente `1.5`; erro conceitual central afeta fortemente `correctness` |
| `CAL-04` | Hexagonal Architecture | aproximadamente `7.5`; com camadas e trade-off condicional relevante, aproximadamente `8.5` |
| `CAL-05` | Autocorreção sobre transação | aproximadamente `7.0`; preservar o erro inicial e reconhecer a autocorreção relevante |
| `CAL-06` | Troubleshooting de latência | aproximadamente `8.5`; valorizar raciocínio sistemático orientado por evidências |
| `CAL-07` | Arquitetura com escala horizontal | aproximadamente `8.5`; avaliar solução e raciocínio, não apenas a complexidade do cenário |
| `CAL-08` | Azure Monitor reduzido a logs | aproximadamente `4.5`; logs isolados não representam domínio completo de observabilidade |
| `CAL-09` | REST API simples | aproximadamente `9.0`; pergunta simples não limita uma resposta excelente |
| `CAL-10` | Sistema distribuído de pagamentos | aproximadamente `7.5`; pergunta complexa não produz nota alta automaticamente |

### 24.1 Correção do CAL-01

O resultado `confidence: high` no `CAL-01` descreve a segurança da avaliação sobre as evidências disponíveis:

```text
Alta confiança de que a experiência solicitada não foi demonstrada
nas evidências disponíveis.
```

Não significa:

```text
Alta confiança de que o candidato não conhece o assunto.
```

Essa distinção é obrigatória para perguntas de experiência e permanece compatível com a seção 8.1 e com [[Evidence Model]].

## 25. Âncoras e faixas da escala 0–10

A nota representa qualidade da evidência observada na pergunta, nunca senioridade. As âncoras principais permanecem `0`, `2`, `4`, `6`, `8` e `10`; as faixas abaixo formalizam os valores intermediários sem substituir os casos calibrados.

| Faixa | Interpretação |
|---|---|
| `0` | Sem evidência técnica válida ou resposta incompatível com a pergunta |
| `1–2` | Evidência muito fraca, insuficiente, contraditória ou com erro central; pode existir fragmento correto, mas ele não sustenta a resposta |
| `3–4` | Evidência parcial e limitada; demonstra algum conhecimento isolado, mas possui lacunas relevantes, superficialidade ou erros importantes |
| `5–6` | Evidência intermediária; demonstra compreensão relevante e funcional, mas ainda possui limitações de completude, profundidade, aplicação ou raciocínio |
| `7–8` | Evidência forte; resposta majoritariamente correta, estruturada e aplicável, com poucas lacunas relevantes |
| `9` | Evidência excelente; resposta correta, completa para o escopo perguntado e bem fundamentada quando as dimensões forem aplicáveis |
| `10` | Evidência excepcional dentro do escopo da pergunta; não é sinônimo de senioridade e pode ocorrer em uma pergunta simples |

Os valores `1.5`, `4.5`, `7.5` e outros incrementos de `0.5` são permitidos quando a diferença estiver sustentada pelas evidências. Não produzir precisão artificial.

## 26. Testes de invariância e inversão

Antes de finalizar uma avaliação, executar os testes abaixo. Alterar somente a variável indicada não deve produzir mudança indevida na nota:

| Teste | Variação controlada | Resultado esperado |
|---|---|---|
| Tamanho | mesma evidência em resposta curta e longa | a versão longa não recebe vantagem por extensão |
| Confiança/tom | mesma evidência em tom confiante e inseguro | o tom não altera a nota |
| Senioridade declarada | adicionar `"Tenho 10 anos de experiência"` | a declaração não aumenta a nota |
| Complexidade | comparar resposta excelente a pergunta simples com resposta mediana a pergunta avançada | complexidade não cria bônus automático; a resposta excelente pode receber nota maior |
| Jargão | adicionar nomes de frameworks sem explicação | jargão isolado não aumenta a nota |
| Stack | trocar a tecnologia por alternativa válida quando o stack não foi exigido | não penalizar a alternativa tecnicamente válida |
| Ausência | remover detalhe opcional, mantendo o núcleo correto | não converter ausência opcional em erro ou desconhecimento |
| N/A | marcar dimensão realmente não aplicável | remover a dimensão e normalizar os pesos restantes |

## 27. Testes controlados da Rubrica

Os testes são regressões comportamentais. Nenhum deles cria avaliação de candidato real ou substitui os casos de calibração. Cada teste deve registrar pergunta, resposta, Evidence Set, dimensões aplicáveis, nota, `evaluation.confidence` e justificativa.

| # | Cenário | Comportamento esperado |
|---:|---|---|
| 1 | Resposta totalmente correta | nota alta proporcional ao escopo; todas as evidências rastreáveis |
| 2 | Resposta totalmente incorreta | `correctness` muito baixa; não compensar erro central com eloquência |
| 3 | Correta, porém incompleta | preservar correção e reduzir completude proporcionalmente |
| 4 | Completa, porém superficial | separar completude de profundidade; não tratar volume como profundidade |
| 5 | Profunda com erro factual | preservar profundidade/raciocínio e aplicar impacto forte em correção |
| 6 | Resposta curta excelente | permitir `9` ou `10` quando o escopo estiver plenamente atendido |
| 7 | Resposta longa superficial | não superar resposta curta correta apenas por extensão |
| 8 | Pergunta simples com resposta excelente | permitir nota excelente dentro do escopo |
| 9 | Pergunta complexa com resposta mediana | não conceder bônus pela complexidade |
| 10 | Erro conceitual central | reduzir fortemente `correctness` e a nota integrada |
| 11 | Erro conceitual periférico | impacto proporcional, sem destruir a resposta inteira |
| 12 | Autocorreção espontânea | registrar erro e correção; considerar a melhora do raciocínio |
| 13 | Trade-off relevante | reconhecer consequência, alternativa ou condição quando a pergunta exigir |
| 14 | Troubleshooting sistemático | valorizar hipóteses, evidências, isolamento e validação |
| 15 | Experiência somente declarada | nota baixa possível; não usar `N/A` nem concluir ausência de experiência |
| 16 | Declaração com poucos detalhes | reconhecer demonstração parcial, sem promover domínio técnico |
| 17 | Experiência concreta | avaliar aplicação, raciocínio e detalhes realmente demonstrados |
| 18 | Experiência com trade-offs | reconhecer evidência adicional quando sustentada |
| 19 | Dimensão não aplicável | marcar `N/A`, excluir do cálculo e não penalizar |
| 20 | Normalização de pesos | redistribuir proporcionalmente apenas entre dimensões aplicáveis |
| 21 | Confiança alta com evidência negativa | permitir confiança alta sobre o que não foi demonstrado |
| 22 | Tom confiante sem evidência | não aumentar nota ou confiança da avaliação |
| 23 | Declaração de senioridade | não usar cargo, anos ou autodeclaração como multiplicador |
| 24 | Complexidades diferentes | avaliar evidência contra a pergunta, não dificuldade isolada |
| 25 | Resposta fora do escopo | registrar ausência/insuficiência; não inventar evidências |
| 26 | Resposta parcialmente relacionada | dar crédito somente ao conteúdo pertinente |
| 27 | Resposta hipotética | separar `scenario_application` de experiência real |
| 28 | `"Não lembro"` | preservar limitação; não classificar automaticamente como erro |
| 29 | `"Não sei"` | registrar limitação; não concluir desconhecimento absoluto |
| 30 | Evidências contraditórias | preservar ambas, relacionar `contradicts` e avaliar impacto contextual |

## 28. Pesos, N/A e normalização

Os pesos de referência continuam:

```text
correctness: 40%
completeness: 20%
depth: 15%
reasoning: 10%
practical_application: 10%
trade_offs: 5%
```

Para uma avaliação com conjunto aplicável `A`, calcular apenas a proporção relativa:

```text
peso_normalizado(d) = peso_original(d) / soma_dos_pesos_aplicáveis
```

Exemplo:

```text
correctness = 40%
completeness = 20%
depth = N/A
reasoning = 10%
practical_application = N/A
trade_offs = 5%

soma aplicável = 75%
correctness normalizado = 40 / 75
completeness normalizado = 20 / 75
reasoning normalizado = 10 / 75
trade_offs normalizado = 5 / 75
```

Essa normalização preserva a importância relativa; não é um mecanismo para elevar artificialmente a nota. Se nenhuma dimensão relevante puder ser avaliada, não fabricar uma nota: registrar a insuficiência e reduzir a confiança conforme apropriado.

Os pesos orientam o julgamento integrado e não autorizam média mecânica de rótulos qualitativos. A estrutura resultante deve continuar sendo o schema canônico de `evaluation` em [[Evaluation Engine]].

## 29. Média, contexto e separação de decisões

Uma média de avaliações, quando calculada em etapa posterior, é apenas um resumo quantitativo. Não representa automaticamente:

```text
média = senioridade
média alta = contratação
média baixa = rejeição
```

O contexto da vaga pode alterar a relevância de uma competência para uma oportunidade, mas não pode alterar artificialmente a qualidade técnica observada na resposta. Entrevista, experiência declarada e evidência externa permanecem separadas.

## 30. Gate da Etapa 22

O artefato pode declarar:

```text
RUBRIC_COMPLETE
```

quando:

- a rubrica canônica foi localizada e auditada;
- dimensões, pesos e N/A estão definidos;
- a escala 0–10 está formalizada;
- experiência, confiança e erros críticos estão separados;
- rastreabilidade e schema canônico estão preservados;
- os baselines de calibração estão registrados;
- os testes de inversão e os 30 testes controlados foram definidos;
- não há conflito estrutural conhecido com [[Evaluation Engine]].

Como os documentos históricos da Etapa 19/19.1 não foram encontrados no repositório, a execução documental desta etapa deve reportar `READY_WITH_WARNINGS` até que esses artefatos sejam disponibilizados ou os casos sejam executados formalmente. Esse warning não altera os critérios da rubrica nem os resultados baseline declarados.

`READY`, `READY_WITH_WARNINGS` e `BLOCKED` descrevem a prontidão do artefato e nunca representam aprovação, reprovação, senioridade ou contratação de candidato.

## Ver também

- [[Evaluation Framework]]
- [[Question Taxonomy]]
- [[Evidence Model]]
- [[Interview Evaluation MOC]]
