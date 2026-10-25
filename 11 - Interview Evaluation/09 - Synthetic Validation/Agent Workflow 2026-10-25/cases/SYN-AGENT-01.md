# Transcrição clara — caso fictício

Participantes e papéis explícitos. Transcrição íntegra. Sem áudio ou experiência profissional adicional disponíveis.

**SYN-AGENT-01-T01 | 00:01 | Entrevistadora A (interviewer)**

O que é injeção de dependência e que problema ela resolve?

**SYN-AGENT-01-T02 | 00:05 | Candidata Sintética Clara (candidate)**

A classe recebe as dependências de fora, por exemplo pelo construtor, em vez de criar as implementações dentro dela. Eu faria o serviço depender de uma interface e escolheria a implementação na composição. Isso separa a criação do uso e facilita substituir colaboradores em testes.

**SYN-AGENT-01-T03 | 00:24 | Entrevistadora A (interviewer)**

Como você testaria esse serviço?

**SYN-AGENT-01-T04 | 00:28 | Candidata Sintética Clara (candidate)**

Não implementei isso em produção. Eu criaria o serviço com um repositório fake, executaria a operação e verificaria o resultado e as interações esperadas. Separadamente, faria um teste de integração do adaptador com o banco. Não sei qual estratégia seria melhor para limpar os dados desse teste.

**SYN-AGENT-01-T05 | 00:53 | Entrevistador B (interviewer)**

Existe algum custo ou situação em que você evitaria criar uma interface?

**SYN-AGENT-01-T06 | 00:57 | Candidata Sintética Clara (candidate)**

Eu evitaria criar uma interface para cada objeto de valor simples só por padrão. Abstrações sem necessidade podem aumentar a navegação e a complexidade. Eu priorizaria fronteiras onde uma implementação pode variar ou onde exista colaboração externa a substituir no teste.
