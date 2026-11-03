# Entrevista simulada — APIs, incidentes e consistência

Material inteiramente fictício, criado em 2026-11-02. Não existe áudio. Pessoas, empresa e acontecimentos não representam experiência real. Timestamps são identificadores dos inícios das falas, não intervalos comprovados.

```text
Marina Alves — 00:03
Olá, Lúcia. Eu coordeno o projeto fictício Pedidos Aurora, na empresa fictícia Horizonte Sistemas. O Diego vai conduzir as perguntas técnicas. No final você pode perguntar sobre o time.

Lúcia Martins — 00:18
Oi, obrigada. Podemos começar.

Diego Rocha — 00:27
Quais linguagens e ferramentas você utilizou nos últimos projetos?

Lúcia Martins — 00:36
Java 17, Spring Boot e SQL. Eu olhava painéis no grafano. Java 21 eu só estudei, não usei no trabalho.

Diego Rocha — 01:02
O que é uma transação de banco? Explique a ideia, sem precisar entrar em configuração.

Lúcia Martins — 01:12
É tratar um conjunto de alterações como uma unidade. Se uma falhar, você não quer deixar só metade gravada. Confirma o conjunto ou desfaz, dentro daquela transação.

Diego Rocha — 01:40
E se a transação no banco for desfeita, um e-mail que já foi enviado por uma API externa também é desfeito automaticamente?

Lúcia Martins — 01:51
Sim. Se a chamada saiu de dentro do método da transação, o rollback cancela o e-mail que já tinha sido enviado também.

Diego Rocha — 02:14
No HTTP, autenticação e autorização são a mesma coisa?

Lúcia Martins — 02:23
Autenticação é o que pode fazer... não, eu inverti. Autenticação é verificar quem está acessando. Autorização é verificar o que essa pessoa pode fazer. Alguém pode estar identificado e mesmo assim não ter permissão para uma operação.

Diego Rocha — 02:58
Você já participou de configuração de observabilidade?

Lúcia Martins — 03:06
Participei colocando um identificador de correlação nos logs da aplicação. O coletor foi configurado pelo pessoal de plataforma, não por mim.

Diego Rocha — 03:28
Explica um exemplo de como esse identificador ajudou vocês numa investigação. O que você fez e o que conseguiu concluir?

Lúcia Martins — 03:40
Tinha uma resposta 500. Eu busquei os registros pelo identificador e vi uma falha na integração de pagamento. Isso me ajudou a localizar onde olhar, mas eu não consegui concluir a causa só com aquilo. Passei os registros para o time da integração e não acompanhei o desfecho.

Diego Rocha — 04:13
Agora um cenário hipotético: a criação de um pedido falhou para o cliente, mas talvez o servidor tenha gravado antes de a conexão cair. Você repetiria a requisição sem verificar nada? Por quê?

Lúcia Martins — 04:29
Não repetiria às cegas, porque podia criar dois pedidos. Tentaria consultar o resultado daquela tentativa. Se a API tivesse uma chave para identificar e tratar a repetição, usaria a mesma chave conforme o contrato. Eu não estou dizendo que implementei isso; é como eu tentaria conduzir.

Diego Rocha — 05:05
Qual seria uma dificuldade de implementar esse tratamento de repetição? O que precisaria cuidar?

Lúcia Martins — 05:17
É bom porque dá mais confiança e evita duplicação. Também melhora a experiência do cliente quando a internet está ruim.

Diego Rocha — 05:42
Em outro incidente, sem acesso ao ambiente de teste, como começaria a investigar uma API lenta em produção?

Lúcia Martins — 05:55
Eu pediria os horários e quais operações ficaram lentas. Compararia duração e erros nos registros e painéis disponíveis. Minha preferência é reproduzir em teste quando dá, mas, nesse caso, começaria pelos dados de produção aos quais tivesse acesso. Não faria uma mudança sem combinar com o responsável.

Diego Rocha — 06:31
Você já ajustou um alerta de produção? Conta o que alterou e como verificou o efeito.

Lúcia Martins — 06:43
O não antes aquele ajuste a memória era não sim eles na fila então sem quando depois eu painel...

Diego Rocha — 07:04
Sobre cache: se o valor expira em um minuto, isso garante que o cliente sempre recebe o valor mais recente do banco?

Lúcia Martins — 07:16
Não. Durante esse minuto a origem pode ter mudado. Expirar limita o tempo de guardar aquela cópia, não garante que ela seja sempre a mais recente.

Marina Alves — 07:45
Você usa alguma ferramenta para organizar as tarefas?

Lúcia Martins — 07:54
Usava o quadro do jira, conferia o que estava priorizado na reunião. Eu não administrava a ferramenta.

Marina Alves — 08:15
Quer perguntar alguma coisa sobre o time?

Lúcia Martins — 08:23
Quem atende um incidente consegue consultar os logs ou precisa pedir acesso?

Diego Rocha — 08:34
Depende do serviço. Alguns acessos são liberados por papel e outros precisam de solicitação. A plataforma configura o coletor central e ajuda a investigar a infraestrutura.

Lúcia Martins — 08:58
Certo, obrigada. Era isso.

Marina Alves — 09:06
Obrigada. Encerramos por aqui.
```
