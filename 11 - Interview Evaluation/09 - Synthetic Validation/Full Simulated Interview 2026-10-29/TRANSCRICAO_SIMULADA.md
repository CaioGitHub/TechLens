# Entrevista simulada — desenvolvimento Java e sustentação de aplicações

**Material inteiramente fictício.** Pessoas, organização, projetos, experiências e timestamps foram criados para um ensaio diagnóstico. Não existe gravação de áudio associada. Este texto não é outra entrevista real nem uma versão da entrevista anterior.

Formato semelhante ao da fonte do projeto: abertura da coordenação, entrevista técnica, falas coloquiais e perguntas da pessoa candidata. Há passagens deliberadamente ambíguas ou comprometidas para simular problemas de transcrição. As condições conhecidas estão em CONDICOES_DA_SIMULACAO.md; devem acompanhar esta fonte na análise. Não confundir erro técnico de uma resposta com erro de transcrição.

```text
Helena Torres — 00:03
Bom dia, pessoal. Rafael, obrigada por participar. Eu sou a Helena, coordeno o time do projeto Portal Horizonte aqui na empresa fictícia Vetor Digital. O Bruno divide a coordenação comigo e a Camila vai conduzir a parte técnica.

Rafael Nunes — 00:22
Bom dia. Obrigado pelo convite.

Helena Torres — 00:27
A vaga é para desenvolvimento Java com participação na sustentação. Tem evolução de funcionalidades, mas também investigação de chamados. É uma plataforma de pedidos e acompanhamento de entregas. Você já trabalhou com esse tipo de operação?

Rafael Nunes — 00:49
Com entrega, especificamente, não. Eu trabalhei com sistemas de cadastro e depois com pedidos de uma rede de lojas. Tinha integração com estoque, mas a parte do transporte era outro time.

Helena Torres — 01:09
Certo. Camila, pode seguir. No final a gente deixa um espaço para as dúvidas dele.

Camila Duarte — 01:18
Oi, Rafael. Para começar, conta um pouco dos projetos em que você atuou, o que fazia e quais tecnologias usava.

Rafael Nunes — 01:29
Eu comecei fazendo manutenção em um sistema interno de cadastro, com Java e banco relacional. Depois fui para esse projeto de pedidos. A gente tinha APIs para consultar produto, criar pedido e integrar pagamento. Eu ficava mais no back-end, implementação de endpoint, ajuste de consulta e correção de problema que chegava pelo suporte.

Rafael Nunes — 02:02
No último ano eu participei mais da sustentação. Não era uma equipe só de incidente, mas tinha um rodízio. Quando eu estava na semana do suporte, pegava o chamado, tentava entender o comportamento e chamava alguém da funcionalidade quando precisava.

Camila Duarte — 02:24
E as versões de Java e os frameworks, quais eram?

Rafael Nunes — 02:31
No primeiro projeto era Java 11. No mais recente, 17. Eu estudei o 21, mas não trabalhei com ele em produção. A API era Spring Boot. A gente usava JPA em quase tudo e tinha umas consultas SQL escritas manualmente.

Camila Duarte — 02:59
Você comentou essas consultas. O que é JDBC e qual é a função dele em uma aplicação Java?

Rafael Nunes — 03:09
É a API do Java para conversar com o banco, abrir conexão e executar o SQL. Mesmo quando usa um framework por cima, tem essa comunicação embaixo. Eu não configurava o driver do zero no projeto, porque a configuração já vinha no serviço.

Camila Duarte — 03:38
Tá. E na API, qual é a diferença entre autenticação e autorização?

Rafael Nunes — 03:48
Autenticação é verificar quem está tentando acessar. Autorização é o que aquela pessoa pode fazer depois. Pode estar autenticada e não poder consultar um pedido de outra loja, por exemplo.

Camila Duarte — 04:14
E como vocês faziam isso no projeto?

Rafael Nunes — 04:22
Chegava um token na requisição. O serviço validava e olhava os papéis. Essa parte principal era mantida pelo time de plataforma. Eu mexi na regra de filtrar os pedidos pela loja do usuário. Não fui eu que implementei o serviço de identidade.

Camila Duarte — 04:52
Sobre organização do código, vocês usavam arquitetura em camadas, hexagonal ou outra organização?

Rafael Nunes — 05:02
Era em camadas. Tinha controller, serviço, repositório e umas classes de integração. Hexagonal eu conheço de estudo, não usei em um projeto profissional.

Camila Duarte — 05:22
Qual é a ideia principal da hexagonal e um benefício que você enxerga?

Rafael Nunes — 05:31
É não deixar a regra de negócio dependendo diretamente das tecnologias de fora. Você define os contratos e deixa a implementação de banco ou de API do lado de fora. Um benefício seria conseguir testar a regra sem subir o banco de verdade.

Camila Duarte — 06:01
E qual custo isso pode trazer? Em que tipo de projeto você teria cuidado para não complicar demais?

Rafael Nunes — 06:12
O benefício é que fica mais fácil trocar o banco ou outra integração sem sair mexendo em toda a regra. E os testes ficam melhores também.

Camila Duarte — 06:31
Você consegue pensar em alguma desvantagem?

Rafael Nunes — 06:38
De cabeça agora, não. Eu só usei num projeto de estudo. Não sei dizer como seria manter isso num time grande.

Camila Duarte — 06:57
Sem problema. O que significa uma operação ser idempotente?

Rafael Nunes — 07:06
Que repetir a mesma operação não muda o efeito final em relação a executar uma vez. Tipo definir um cadastro como inativo. Se já está inativo, fazer de novo não deveria criar outra alteração de estado.

Camila Duarte — 07:35
Isso quer dizer que ela sempre retorna exatamente a mesma resposta HTTP?

Rafael Nunes — 07:43
Não necessariamente. Eu entendo que é sobre o efeito. O código de resposta pode variar, dependendo do estado e de como a API foi feita.

Camila Duarte — 08:02
Quais ferramentas de observabilidade você já utilizou?

Rafael Nunes — 08:10
Usei Grafana para olhar os painéis e uma ferramenta de busca de logs. O nome dessa outra eu não lembro agora.

Camila Duarte — 08:27
E chegou a configurar alguma coleta ou instrumentação?

Rafael Nunes — 08:35
Eu acrescentei atributos em alguns registros de log. Na parte de coleta, o pessoal da plataforma estava começando a usar o open tele metal. Eu participei de uma reunião, mas não configurei esse coletor.

Camila Duarte — 09:03
Você tem experiência com os serviços de monitoramento da nuvem que o projeto utilizava? O que chegou a fazer diretamente?

Rafael Nunes — 09:14
Não sim a parte índice o banco painel que eles não, era nuvem tudo naquela acesso e depois eu que não...

Camila Duarte — 09:29
Certo, vamos para um cenário de investigação. Qual seria o seu primeiro passo se recebesse uma falha numa funcionalidade que ainda não conhece?

Rafael Nunes — 09:42
Eu pediria o horário, o que a pessoa estava tentando fazer e qual foi o sintoma. Aí olharia os eventos que estivessem disponíveis. Se eu não tivesse permissão para consultar as métricas, tentaria os registros a que eu tivesse acesso e pediria ajuda para alguém com a permissão. Minha preferência seria entender uma execução em teste, se fosse viável.

Camila Duarte — 10:19
Agora vou colocar mais condições. A falha está em produção, passa por três serviços e não conseguimos reproduzir em teste. Como você correlacionaria os eventos e verificaria uma hipótese de causa nessas condições?

Rafael Nunes — 10:36
Eu tentaria seguir o identificador da requisição nos três serviços, se ele estiver sendo propagado. Compararia os horários e onde aparece o primeiro erro. Para verificar a hipótese, por exemplo, se eu suspeitasse de timeout numa integração, compararia as chamadas que falharam com as que passaram e olharia o tempo dessa dependência.

Rafael Nunes — 11:04
Se não tiver esse identificador nos três, eu não vou conseguir garantir que dois registros são da mesma tentativa só porque têm horário parecido. Aí precisaria cruzar outras informações disponíveis. E não sairia alterando configuração sem combinar com o responsável do serviço.

Camila Duarte — 11:26
Você lembra de um incidente real que investigou? Conta as suas ações e como verificou o resultado.

Rafael Nunes — 11:38
Teve um endpoint de consulta de pedidos que começou a demorar mais. Eu peguei o horário dos chamados e vi que os lentos eram os que pediam um intervalo grande. Rodei a consulta num ambiente de teste com dados parecidos e o plano mostrava uma varredura de muita coisa. Eu propus um índice com o pessoal do banco e a gente testou de novo.

Rafael Nunes — 12:07
Depois da alteração, acompanhei os tempos no painel. Eu lembro que caiu bastante, mas não vou lembrar o percentil nem o número agora. E o teste não cobria todos os filtros, então ficou uma tarefa para ampliar essa verificação.

Camila Duarte — 12:30
Qual foi a sua participação e qual foi a do pessoal do banco?

Rafael Nunes — 12:37
Eu levantei as requisições lentas, reproduzi a consulta e levei o plano. A pessoa do banco revisou a proposta do índice. A execução no banco de produção foi com eles, não fui eu que rodei o comando lá.

Camila Duarte — 12:58
Um índice comum, sem restrição unique, impede gravar valores duplicados?

Rafael Nunes — 13:07
Sim, se colocou índice naquela coluna ele já evita duplicado. Para mim o unique seria mais para deixar isso explícito na definição.

Camila Duarte — 13:26
Certo. Mudando de tema: o que é cache e qual é um benefício?

Rafael Nunes — 13:36
É manter uma cópia de um dado para não buscar na origem toda vez. O benefício pode ser diminuir o tempo da resposta.

Camila Duarte — 13:54
E como decidiria se vale usar cache quando os dados podem ficar desatualizados?

Rafael Nunes — 14:04
Eu perguntaria quanto tempo de atraso é aceitável para aquela informação. Para catálogo de produto pode ser uma coisa, para saldo de estoque usado para confirmar venda é outra. Não colocaria o mesmo tempo de expiração para tudo. Também teria que ver como atualizar ou invalidar quando o dado muda.

Helena Torres — 14:35
Vou entrar um pouquinho. Você teria dificuldade em chamar pessoas de outros times quando precisasse entender um incidente?

Rafael Nunes — 14:44
Não. Eu prefiro chegar com o que já consegui observar e com uma pergunta mais específica. Mas quando é urgente eu não espero entender tudo para chamar ajuda.

Helena Torres — 15:02
E qual ferramenta vocês usam para organizar as tarefas?

Rafael Nunes — 15:10
Lá é o gira. A gente olha o quadro na reunião e vai pegando os chamados que estão priorizados.

Helena Torres — 15:28
Você vem usando assistentes de IA no dia a dia?

Rafael Nunes — 15:37
Uso um que a empresa disponibilizou dentro do editor. Eu uso para sugerir teste e explicar um trecho que eu ainda não conheço. Não colo chamado com dados de cliente. Confiro a sugestão antes, porque já aconteceu de ele sugerir um método que não existia na versão que a gente usava.

Helena Torres — 16:06
Quer fazer alguma pergunta sobre a equipe?

Rafael Nunes — 16:13
Quero sim. A pessoa que fica na sustentação consegue acessar os logs de produção ou precisa pedir para outro time?

Camila Duarte — 16:23
Depende do serviço e da permissão. Alguns painéis já ficam disponíveis. Para outras consultas existe um fluxo de solicitação e a gente registra a necessidade no chamado.

Rafael Nunes — 16:43
E tem documentação do fluxo entre os serviços? Pergunto porque no meu projeto anterior a gente tinha a documentação da API, mas nem sempre tinha o caminho completo da integração.

Bruno Lacerda — 17:00
Temos documentação das APIs e alguns diagramas dos fluxos mais usados. Ainda há partes que dependem bastante da troca com o time. Uma das atividades é melhorar essa documentação quando um incidente revela uma lacuna.

Rafael Nunes — 17:21
Entendi. E o atendimento fica em rodízio ou é a mesma pessoa sempre?

Helena Torres — 17:29
Existe um rodízio durante o horário de trabalho. As condições específicas de disponibilidade são combinadas com a gestão; não vou te passar uma regra fechada aqui sem confirmar a composição da equipe.

Rafael Nunes — 17:49
Tá certo. Para mim essas eram as principais dúvidas.

Helena Torres — 17:57
Obrigada, Rafael. A gente encerra a parte técnica por aqui e depois o recrutamento combina os próximos passos. Obrigada, Camila e Bruno.

Rafael Nunes — 18:08
Obrigado, pessoal. Bom dia para vocês.
```
