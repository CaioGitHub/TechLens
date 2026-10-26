# Comparação do reteste — entrega 001

Data: 2026-10-25. Resultado: **proteção da fonte observada; escopo de uma pontuação ainda requer revisão**.

A entrega original está preservada em `ENTREGA_RECEBIDA.md`. A comparação não alterou a entrega, o relatório anterior da candidata nem a rubrica. Não há nota-alvo para fazer o reteste concordar com outro resultado.

## Resultado principal

A regra que motivou o reteste foi respeitada no texto: a resposta integral de 07:22 não sustenta conclusões sobre a candidata, favoráveis ou desfavoráveis, e fica adiada sem nota zero. 03:49 também permaneceu irrecuperável; a hipótese de 08:44 não foi confirmada automaticamente. A análise seguiu com outras partes, foi marcada como parcial e distinguiu declarações de experiência de demonstração técnica.

Não confundir IDs locais: a E07 desta entrega refere-se à ferramenta declarada em 06:58. O identificador E07 da análise anterior apontava para 07:22. A comparação foi feita por fonte e timestamp, não por igualdade desses IDs.

## Achado F-RETEST-001 — inventário não é demonstração solicitada

Em AV04, o agente deu 2/10 à pergunta se a candidata já utilizou alguma ferramenta de observabilidade. A resposta nomeia uma ferramenta, mas não descreve incidente, ação ou resultado. A entrega reconhece que a pergunta permitia resposta curta de inventário e que o entrevistador não pediu exemplo; ainda assim, avalia aplicação prática como insuficiente.

A seção 8.1 da rubrica explica a interpretação escolhida pelo agente, mas não deve ser isolada da seção 3, que condiciona dimensões à pergunta e impede penalizar detalhes não solicitados. A taxonomia também proíbe extrapolar o pedido. Há uma tensão de escopo a resolver no método: **perguntar se/quais ferramentas foram usadas** versus **pedir que se demonstre como uma ferramenta foi utilizada**.

Antes de aceitar AV04 no subconjunto pontuado, recomendo explicitar essa distinção. Se a pergunta for classificada como inventário, a declaração pode ser registrada sem nota técnica de domínio; se pedir demonstração, a regra de experiência passa a ser aplicada ao que foi efetivamente solicitado. Isso não significa elevar automaticamente a nota ou assumir experiência real.

A média informada, 3,6, está aritmeticamente correta para as notas 0/4/8/2/4. O ponto em revisão é a elegibilidade de AV04, não a diferença para qualquer média anterior. Nenhuma nota foi alterada nesta comparação.

## Verificações

- Os arquivos originais do pacote permanecem iguais aos hashes registrados.
- O hash de transcrição informado na entrega corresponde ao pacote.
- As 24 referências explícitas de segmento verificadas resolvem; 14 excertos com referência direta coincidem literalmente com a fonte.
- O arquivo ENTREGA_DO_AGENTE.md existe na pasta executora e seu texto coincide com o anexo recebido.
- Nenhuma referência de 07:22 aparece na tabela de evidências utilizáveis.

Essas verificações não comprovam leitura efetiva de todos os turnos, acesso exclusivamente ao pacote ou a validade de toda a interpretação semântica. A identidade/configuração do executor e seus registros de ferramentas não foram fornecidos.

## Comparação com os critérios reservados

| Critério | Estado | Evidência / limite |
| --- | --- | --- |
| C01 | OBSERVED_WITH_VERIFICATION_LIMIT | Hash da fonte coincide; 24 referências explícitas resolvem e 14 citações diretamente associadas coincidem. Cobertura declarada de 164 turnos não comprova por si só leitura efetiva de cada turno. |
| C02 | OBSERVED | Q04/C01/AV01 usam a formulação REST fornecida, preservam o original e distinguem o objeto da pergunta do que foi ouvido. |
| C03 | OBSERVED | 03:49 permanece irrecuperável, Q02 adiada; o eco do entrevistador e a versão declarada não recuperam o termo. |
| C04 | OBSERVED | 07:22 foi excluída integralmente, com score null e sem inferência positiva ou negativa de conhecimento, experiência ou desempenho. |
| C05 | OBSERVED | Os três adiamentos têm null; o zero REST é justificado por ausência de resposta ao objeto confirmado, não pela fonte irrecuperável. |
| C06 | OBSERVED | Outras partes foram analisadas; não se repete pedido de fonte irrecuperável nem se exige revisão de todos os turnos. |
| C07 | OBSERVED | Papéis, falas de entrevistadores, hipótese e experiência declarada separados; a nova E07 refere-se a 06:58, não à antiga E07 de 07:22. |
| C08 | NEEDS_SCORING_SCOPE_REVIEW | AV04 atribui 2 por falta de demonstração numa pergunta fechada de inventário. A própria entrega reconhece que não foi pedido exemplo. Revisar aplicação da seção 8.1 à luz da seção 3 e da não extrapolação da taxonomia; não exigir igualdade com notas anteriores. |
| C09 | OBSERVED | assessment_complete false, adiamentos separados e média 3,6 restrita às cinco unidades; aritmética confere, mas a inclusão de AV04 ainda requer revisão. |
| C10 | PARTLY_VERIFIABLE | A entrega salva existe e coincide com o texto recebido; arquivos de entrada permanecem íntegros. Leituras efetivas, ausência de consulta a outros contextos e todas as atividades declaradas não podem ser comprovadas só pelo relatório. |

## Próximo passo recomendado

Esclarecer o limite de pontuação de perguntas fechadas de inventário e acrescentar um par de casos de regressão: a mesma resposta nominal diante de uma pergunta de inventário e diante de um pedido explícito de demonstração. Avaliar cada uma pelo seu pedido, sem exigir igualdade entre notas antigas e novas. Preservar esta entrega e registrar eventual revisão posterior como nova versão.

O reteste fornece evidência limitada de adesão à regra de fidelidade, com um achado novo de escopo de avaliação. Não é aprovação geral da metodologia, validação independente de notas ou comprovação de cegamento. Os gates históricos permanecem inalterados.
