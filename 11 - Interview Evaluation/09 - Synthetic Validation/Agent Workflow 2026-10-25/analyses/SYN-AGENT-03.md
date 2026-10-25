# Análise diagnóstica — Erros técnicos preservados e autocorreção delimitada

Caso fictício; execução não cega e não independente. Não é relatório de candidato real.

O recorte mostra autocorreção da primeira afirmação, mas conserva erros relevantes sobre DIP e teste isolado. Isso limita a evidência demonstrada neste cenário, sem inferência de senioridade ou contratação.

## Cobertura e preservação

- Oito turnos preservados, três perguntas técnicas e um encerramento; a autocorreção não virou uma quarta pergunta.
- As frases incorretas permanecem literais no original. Sua correção é explicação técnica do avaliador, não reconstrução da fala.
- A autocorreção de Q1 não apaga a resposta de Q2 e não autoriza duas notas para Q1.

## Perguntas, evidências e rubrica

### Q1 — 7.0 / 10

Estado: EVALUATED. Confiança do julgamento: medium.

Pergunta: SYN-AGENT-03-T01. Resposta: SYN-AGENT-03-T02, SYN-AGENT-03-T05.

A afirmação inicial de eliminação de todo acoplamento está incorreta. No turno 5, o candidato a retira espontânea e explicitamente, reconhecendo a importância do tipo e das abstrações. A resposta final cobre o núcleo da primeira pergunta com raciocínio adequado, embora a explicação ainda seja breve. A nota considera apenas as respostas vinculadas a Q1; o erro de Q2 não é uma penalização adicional aqui. A tensão entre os turnos é registrada como limite de confiança, não como desconto duplicado. Não há teto fixo por erro inicial nem segunda nota para a autocorreção.

| Dimensão | Aplicação |
| --- | --- |
| correctness | Núcleo final corrigido; afirmação inicial retirada |
| completeness | Adequada para a pergunta |
| depth | Explicação breve sobre tipo e abstração |
| reasoning | Autocorreção explícita com tensão de consistência |
| practical_application | N/A |
| trade_offs | N/A |

### Q2 — 2.0 / 10

Estado: EVALUATED. Confiança do julgamento: medium.

Pergunta: SYN-AGENT-03-T03. Resposta: SYN-AGENT-03-T04.

Inverte o DIP ao apresentar dependência direta do repositório concreto e alteração da regra de negócio como objetivo. O erro é central para a pergunta. A correção do turno 5 se refere explicitamente à primeira resposta; não tratar a segunda como retirada. A tensão é registrada, sem concluir que a pessoa não conhece o tema fora deste recorte.

| Dimensão | Aplicação |
| --- | --- |
| correctness | Erro central no princípio |
| completeness | Não cobre corretamente o núcleo |
| depth | Mecanismo descrito em sentido inverso |
| reasoning | Justificativa sustenta a direção errada |
| practical_application | N/A |
| trade_offs | N/A |

### Q3 — 2.0 / 10

Estado: EVALUATED. Confiança do julgamento: medium.

Pergunta: SYN-AGENT-03-T06. Resposta: SYN-AGENT-03-T07.

É incorreta a obrigatoriedade universal de banco real e a afirmação de que fakes ou mocks sempre invalidam testes. A base distingue isolamento, integração e ponta a ponta. Há uso legítimo de banco real em certos níveis, mas a universalização não responde ao teste isolado solicitado.

| Dimensão | Aplicação |
| --- | --- |
| correctness | Erro central de universalização |
| completeness | Não distingue os níveis |
| depth | Insuficiente para o cenário |
| reasoning | Conclusão incompatível com isolamento |
| practical_application | Estratégia inadequada para o caso |
| trade_offs | N/A |

## Evidência citada literalmente

**SYN-AGENT-03-E01 — SYN-AGENT-03-T02 — Candidato Sintético Técnico**

> Sim, só usar o construtor já elimina todo acoplamento, mesmo quando a classe depende diretamente de uma implementação concreta.

Evidência produzida no recorte; não equivale a confirmação de atuação profissional.

**SYN-AGENT-03-E02 — SYN-AGENT-03-T04 — Candidato Sintético Técnico**

> A regra de negócio deve importar diretamente o repositório concreto. Quando mudar o banco, mudar a regra de negócio é justamente o objetivo da inversão de dependência.

Evidência produzida no recorte; não equivale a confirmação de atuação profissional.

**SYN-AGENT-03-E03 — SYN-AGENT-03-T05 — Candidato Sintético Técnico**

> Antes de continuar, quero corrigir minha primeira resposta: o construtor sozinho não garante baixo acoplamento. O tipo do qual a classe depende importa; depender de abstrações pode permitir trocar a implementação sem mudar a regra. Minha afirmação de que o construtor elimina todo acoplamento estava errada.

Evidência produzida no recorte; não equivale a confirmação de atuação profissional.

**SYN-AGENT-03-E04 — SYN-AGENT-03-T07 — Candidato Sintético Técnico**

> Sim, todo teste do serviço precisa acessar um banco real. Usar fake ou mock sempre invalida qualquer teste.

Evidência produzida no recorte; não equivale a confirmação de atuação profissional.

## Propostas e exceções

Nenhuma mudança lexical proposta ou decisão humana exigida neste exercício.


## Fontes e limites

- `TRANSCRIPTION_AGENT_WORKFLOW.md`
- `AGENTS.md`
- `11 - Interview Evaluation/08 - Evidence Model/21 - Evidence Model.md`
- `11 - Interview Evaluation/04 - Rubrics/Scoring Rubric.md`
- `11 - Interview Evaluation/01 - Evaluation Framework/Evaluation Engine.md`
- `01 - Concepts/Architecture/Dependency Injection.md`
- `01 - Concepts/Architecture/Dependency Inversion.md`
- `02 - Technologies/Spring Boot/Spring Testing.md`

Not computed in this diagnostic exercise; individual rubric judgments only. Same agent authored cases, knew expectations and analyzed outputs. No independent quality measurement.

## Revisão do diagnóstico

F01: a justificativa inicial de Q1 podia misturar a inconsistência observada em Q2 ao julgamento da primeira pergunta. A revisão restringiu a nota às evidências de Q1 e manteve a tensão apenas como limite de confiança. A nota contextual passou de 6,0 a 7,0 sem alvo numérico de referência. A versão inicial está preservada em `revisions/`. Isso é uma revisão do relatório de exercício, não uma alteração do runtime ou da rubrica.
