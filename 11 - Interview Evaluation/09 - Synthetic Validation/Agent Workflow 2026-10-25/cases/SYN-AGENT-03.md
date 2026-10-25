# Erros técnicos preservados e autocorreção delimitada — caso fictício

Transcrição íntegra. Não há indício de falha de reconhecimento. A correção do quinto turno é espontânea e se refere explicitamente apenas à primeira resposta.

**SYN-AGENT-03-T01 | 00:01 | Entrevistadora A (interviewer)**

Receber uma dependência pelo construtor garante baixo acoplamento?

**SYN-AGENT-03-T02 | 00:05 | Candidato Sintético Técnico (candidate)**

Sim, só usar o construtor já elimina todo acoplamento, mesmo quando a classe depende diretamente de uma implementação concreta.

**SYN-AGENT-03-T03 | 00:17 | Entrevistadora A (interviewer)**

No princípio da inversão de dependência, como a regra de negócio deve se relacionar com o repositório?

**SYN-AGENT-03-T04 | 00:23 | Candidato Sintético Técnico (candidate)**

A regra de negócio deve importar diretamente o repositório concreto. Quando mudar o banco, mudar a regra de negócio é justamente o objetivo da inversão de dependência.

**SYN-AGENT-03-T05 | 00:39 | Candidato Sintético Técnico (candidate)**

Antes de continuar, quero corrigir minha primeira resposta: o construtor sozinho não garante baixo acoplamento. O tipo do qual a classe depende importa; depender de abstrações pode permitir trocar a implementação sem mudar a regra. Minha afirmação de que o construtor elimina todo acoplamento estava errada.

**SYN-AGENT-03-T06 | 01:02 | Entrevistadora A (interviewer)**

Para testar isoladamente esse serviço, é obrigatório acessar um banco real?

**SYN-AGENT-03-T07 | 01:08 | Candidato Sintético Técnico (candidate)**

Sim, todo teste do serviço precisa acessar um banco real. Usar fake ou mock sempre invalida qualquer teste.

**SYN-AGENT-03-T08 | 01:20 | Entrevistadora A (interviewer)**

Obrigado, concluímos as perguntas.
