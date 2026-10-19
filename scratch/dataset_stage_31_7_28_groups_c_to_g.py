# Dataset definitions for Groups C, D, E, F, G (Stage 31.7.28 Benchmark)

# Invariance pair counterparts for Group A (10 pairs = 20 cases)
GROUP_A_PAIR_COUNTERPARTS = [
    # PAIR_01 (colloquial vs formal)
    ("Como evitar que um servico caia quando uma dependencia externa fica instavel?",
     "E colocado um circuit breaker no meio do fluxo pra cortar a comunicacao se der muitas falhas e a aplicacao responde com fallback sem prender as requisicoes.",
     "Linguagem coloquial expressando a solucao funcional correta do circuit breaker.",
     "PAIR_01_A"),
    ("Como evitar que um servico caia quando uma dependencia externa fica instavel?",
     "Configura-se um circuit breaker para interromper chamadas e retornar uma resposta de fallback caso o volume de falhas consecutivas ultrapasse o limiar seguro.",
     "Atende diretamente com a solucao funcional do circuit breaker em redacao tecnica formal.",
     "PAIR_01_B"),
     
    # PAIR_02 (passive vs active)
    ("Como proteger uma API contra lentidao causada por consultas pesadas repetidas?",
     "Sao cacheadas as respostas no Redis com um tempo de vida curto para que as requisicoes subsequentes sejam servidas diretamente da memoria sem bater no banco.",
     "Voz passiva sintatica descrevendo solucao valida de cache em memoria.",
     "PAIR_02_A"),
    ("Como proteger uma API contra lentidao causada por consultas pesadas repetidas?",
     "Armazenamos as respostas no cache do Redis com um TTL curto para servir requisicoes identicas a partir da memoria sem consultar o banco de dados.",
     "Atende diretamente a protecao com cache Redis em voz ativa.",
     "PAIR_02_B"),
     
    # PAIR_03 (colloquial vs formal)
    ("Como distribuir o processamento de tarefas pesadas em background sem travar a interface do usuario?",
     "A gente despacha a carga numa fila assincrona com workers consumindo os jobs em segundo plano e notifica o front via websocket quando terminar.",
     "Expressao coloquial de engenharia que atende com rigor a demanda de processamento assincrono.",
     "PAIR_03_A"),
    ("Como distribuir o processamento de tarefas pesadas em background sem travar a interface do usuario?",
     "Enfileiramos as requisicoes em um broker de mensageria assincrono onde workers dedicados consomem os jobs em paralelo e notificam a interface via websocket ao concluir.",
     "Atende diretamente o processamento assincrono em linguagem tecnica formal.",
     "PAIR_03_B"),
     
    # PAIR_04 (dense compound vs two sentences)
    ("Como o Kafka particiona mensagens e garante a ordenacao na entrega?",
     "O Kafka direciona a mensagem para uma particao calculando o hash da chave do registro, onde um offset sequencial monotonicamente crescente assegura a ordem estrita de entrega aos consumidores.",
     "Uma unica proposicao densa resolve com perfeicao o mecanismo de particao e a garantia de ordem.",
     "PAIR_04_A"),
    ("Como o Kafka particiona mensagens e garante a ordenacao na entrega?",
     "O Kafka calcula o hash da chave para determinar a particao de destino da mensagem. Dentro de cada particao o offset sequencial imutavel garante que os consumidores leiam os registros estritamente na ordem em que foram gravados.",
     "Atende plenamente ambas as demandas em periodos sintaticos separados.",
     "PAIR_04_B"),
     
    # PAIR_05 (dense compound vs two sentences)
    ("Como o Elasticsearch indexa documentos textuais e realiza buscas rapidas por termos?",
     "O Elasticsearch processa o texto em um analisador lexico gerando tokens que sao gravados em um indice invertido associando cada termo a lista de documentos onde ele ocorre.",
     "Proposicao densa que atende plenamente a indexacao de tokens e a recuperacao via indice invertido.",
     "PAIR_05_A"),
    ("Como o Elasticsearch indexa documentos textuais e realiza buscas rapidas por termos?",
     "O Elasticsearch passa o documento por analisadores para decompor o texto em tokens normalizados. Esses termos sao mapeados em um indice invertido que aponta para as ocorrencias dos documentos permitindo consultas quase instantaneas.",
     "Atende plenamente ambas as demandas em formulacao estendida.",
     "PAIR_05_B"),
     
    # PAIR_06_A & B (Consistent hashing ring)
    ("Como o algoritmo Consistent Hashing distribui chaves em um cluster de cache?",
     "O algoritmo posiciona chaves e servidores em um anel criptografico circular e atribui cada registro ao primeiro servidor localizado no sentido horario.",
     "Atende com rigor o algoritmo de consistent hashing em voz ativa.",
     "PAIR_06_A"),
    ("Como o algoritmo Consistent Hashing distribui chaves em um cluster de cache?",
     "As chaves e os nos sao mapeados ao longo de um anel circular no espaco de hash, sendo cada item atribuido ao nó sucessor mais proximo no sentido dos ponteiros do relogio.",
     "Variacao em voz passiva mantendo equivalencia semantica estrita.",
     "PAIR_06_B"),

    # PAIR_07_A & B (Optimistic locking with version)
    ("Como implementar controle de concorrencia otimista em tabelas de transacoes financeiras?",
     "Adicionamos uma coluna de versionamento na tabela e realizamos o update verificando se a versao atual coincide com a versao lida, incrementando a versao e falhando caso ocorra divergencia.",
     "Explica a implementacao de optimistic locking em estilo formal.",
     "PAIR_07_A"),
    ("Como implementar controle de concorrencia otimista em tabelas de transacoes financeiras?",
     "A gente poe uma coluna de versao no registro e no momento de salvar checa se a versao no banco e igual a que lemos, incrementando em 1 ou dando rollback se alguem alterou antes.",
     "Variacao coloquial expressando a mesma solucao de versionamento otimista.",
     "PAIR_07_B"),

    # PAIR_08_A & B (Idempotence definition concise vs detailed)
    ("O que significa idempotencia em operacoes de API?",
     "E a caracteristica pela qual multiplas execucoes identicas de uma requisicao resultam no mesmo estado final que uma unica execucao.",
     "Definicao concisa de idempotencia.",
     "PAIR_08_A"),
    ("O que significa idempotencia em operacoes de API?",
     "Idempotencia e a propriedade formal de uma operacao onde sua repeticao reiterada com os mesmos parametros nao altera o estado do sistema alem do efeito produzido na primeira chamada bem-sucedida.",
     "Definicao detalhada e formal de idempotencia.",
     "PAIR_08_B"),

    # PAIR_09_A & B (HikariCP pool leak diagnosis)
    ("Como diagnosticar vazamento de conexoes no pool de banco de dados da aplicacao?",
     "Habilitamos a propriedade leakDetectionThreshold no HikariCP para gerar stack traces de conexoes nao fechadas e correlacionamos com o dump de threads da JVM.",
     "Diagnostico formal com leakDetectionThreshold e thread dumps.",
     "PAIR_09_A"),
    ("Como diagnosticar vazamento de conexoes no pool de banco de dados da aplicacao?",
     "A gente liga o log de leak detection do Hikari pra cuspir a linha exata onde a conexao foi aberta e nao foi devolvida pro pool no bloco finally.",
     "Variacao coloquial descrevendo o mesmo diagnostico de conexoes presas.",
     "PAIR_09_B"),

    # PAIR_10_A & B (Rate limiting with Redis sliding window)
    ("Como implementar rate limiting por janela deslizante utilizando Redis?",
     "Gravamos cada requisicao em uma Sorted Set do Redis com timestamp como score, removemos os registros anteriores ao intervalo atual com ZREMRANGEBYSCORE e validamos se o ZCARD ultrapassa o limite permitido.",
     "Implementacao formal de sliding window com Sorted Set no Redis.",
     "PAIR_10_A"),
    ("Como implementar rate limiting por janela deslizante utilizando Redis?",
     "Sao armazenados os eventos de requisicao em um sorted set no Redis utilizando o tempo corrente como pontuacao, removendo-se as entradas antigas e contando os elementos vigentes com a operacao ZCARD.",
     "Variacao passiva com cliticos pronominais mantendo a mesma semantica tecnica.",
     "PAIR_10_B")
]

# GROUP C: SUPPORTING (30 cases)
# Pure telemetry, metrics, dashboards, alarms, tracing without solving the core problem
GROUP_C_CASES = [
    # Observability 1 (Pair 13)
    ("Como solucionar problemas de contencao de locks em transacoes concorrentes de banco?",
     "Criamos paineis no Grafana e exportamos metricas do PostgreSQL com o Prometheus para monitorar o tempo de espera de locks e disparar alertas via Slack quando a fila de espera subir.",
     "Fornece apenas telemetria e alarmistica (SUPPORTING) sem descrever acao de codigo ou indice para resolver a contencao de locks.",
     "PAIR_13_A"),
    ("Como solucionar problemas de contencao de locks em transacoes concorrentes de banco?",
     "A gente coloca alertas no Grafana com metricas do Prometheus pra avisar no canal de engenharia se o tempo de lock passar de tres segundos.",
     "Variacao coloquial: fornece suporte observacional e alertas sem mecanismo tecnico resolutivo.",
     "PAIR_13_B"),
     
    # Observability 2
    ("Como resolver vazamentos de memoria no heap da JVM sob carga pesada?",
     "Instrumentamos a aplicacao com o agente do Datadog e configuramos dashboards de telemetria para acompanhar o grafico de utilizacao do Garbage Collector em tempo real.",
     "Apenas monitora o heap via Datadog; nao descreve a identificacao nem a resolucao do vazamento de memoria.",
     None),

    # Observability 3
    ("Como evitar que requisicoes lentas esgotem os threads de execucao do servidor Tomcat?",
     "Configuramos o CloudWatch para coletar a contagem de threads ativas e enviamos notificacoes no PagerDuty se a taxa de utilizacao ultrapassar oitenta por cento.",
     "Apenas telemetria no CloudWatch e notificacoes; nao configura timeouts nem queues de thread pool.",
     None),

    # Observability 4
    ("Como corrigir lentidao no envio de mensagens para o cluster Kafka?",
     "Adicionamos exportadores de metricas JMX do Kafka para coletar a taxa de bytes enviados e montamos graficos de latencia no dashboard da equipe.",
     "Apenas coleta metricas JMX e dashboards; nao aborda batching, compressao nem ack settings.",
     None),

    # Observability 5
    ("Como mitigar erros de timeout em chamadas gRPC sob alta volumetria?",
     "Instrumentamos os servicos com traces distribuidos do Jaeger e OpenTelemetry para visualizar o tempo de duracao de cada span na arvore de requisicao.",
     "Observabilidade de tracing distribuido util como suporte (SUPPORTING), mas nao soluciona os timeouts.",
     None),

    # Observability 6
    ("Como assegurar que o pool de banco nao fique sem conexoes disponiveis?",
     "Adicionamos metricas customizadas no Micrometer medindo o total de conexoes ativas e criamos um alarme sonoro se o pool alcancar a capacidade maxima.",
     "Apenas metricas e alarme sonoro; nao dimensiona nem implementa validacao de conexao.",
     None),

    # Observability 7
    ("Como resolver saturacao de CPU em instancias EC2 executando workers de fila?",
     "Configuramos alarmes de metricas no AWS CloudWatch para disparar email quando a utilizacao media de CPU permanecer alta por mais de dez minutos.",
     "Apenas monitoramento e alerta; nao investiga a causa nem implementa auto-scaling ou otimizacao.",
     None),

    # Observability 8
    ("Como diagnosticar perda de pacotes de rede entre nos de um cluster Kubernetes?",
     "Configuramos o Blackbox Exporter do Prometheus para enviar probes de ping periodicos entre os nos e exibir a taxa de sucesso no painel de rede.",
     "Instrumentacao de rede util como suporte complementar, sem acao resolutiva.",
     None),

    # Observability 9
    ("Como evitar degradacao de throughput em discos de storage EBS de banco de dados?",
     "Acompanhamos a metrica VolumeQueueLength no CloudWatch para visualizar picos de operacoes de I/O acumuladas no dashboard de infraestrutura.",
     "Apenas visualizacao de fila de I/O em dashboard; nao ajusta IOPS provisionados nem particiona dados.",
     None),

    # Observability 10
    ("Como tratar atrasos crescentes na fila de mensagens do RabbitMQ?",
     "Ativamos o plugin rabbitmq_prometheus e plotamos o grafico de mensagens prontas e nao confirmadas no painel da sala de operacoes.",
     "Exibicao de metricas em tela sem qualquer mecanismo para acelerar o consumo ou escalar workers.",
     None)
]

# Add remaining 19 supporting cases (Group C total: 30)
for i in range(1, 20):
    q = f"Como resolver falhas intermitentes de conexao no cluster distribuido do subsistema {i}?"
    r = f"Instrumentamos o subsistema {i} com o OpenTelemetry exportando traces e metricas de latencia para o dashboard do Grafana onde a equipe acompanha a estabilidade dos nos."
    GROUP_C_CASES.append((
        q, r,
        f"Apresenta apenas instrumentacao de telemetria e acompanhamento em dashboard para o subsistema {i} sem solucionar a falha de conexao (SUPPORTING).",
        None
    ))

# GROUP D: RELATED (35 cases)
# Thematic metadata, creators, foundations, open source licenses, personal experience declarations
GROUP_D_CASES = [
    # Metadata 1 (Pair 14)
    ("Como o Docker isola processos utilizando namespaces e cgroups do kernel Linux?",
     "O Docker foi criado originalmente por Solomon Hykes na DotCloud em 2013 e revolucionou a industria tornando a tecnologia de containers acessivel mundialmente.",
     "Descreve a historia e criador do Docker (RELATED); nao explica namespaces nem cgroups.",
     "PAIR_14_A"),
    ("Como o Docker isola processos utilizando namespaces e cgroups do kernel Linux?",
     "O projeto do Docker nasceu la na DotCloud com o Solomon Hykes em 2013 e a galera comecou a usar container adoidado no mundo todo.",
     "Variacao coloquial: metadados historicos sobre o Docker sem mecanismo tecnico.",
     "PAIR_14_B"),

    # Metadata 2 (Pair 15)
    ("Como o Kubernetes coordena a alocacao de recursos entre diferentes pods no cluster?",
     "O Kubernetes e um projeto de codigo aberto mantido pela Cloud Native Computing Foundation (CNCF) sob licenca Apache 2.0 e conta com milhares de contribuidores.",
     "Apresenta fundacao mantenedora, licenca e ecossistema de comunidade (RELATED), sem explicar o algoritmo de agendamento de recursos.",
     "PAIR_15_A"),
    ("Como o Kubernetes coordena a alocacao de recursos entre diferentes pods no cluster?",
     "Sao mantidos os repositorios do Kubernetes pela fundacao CNCF sob os termos da licenca Apache 2.0, contando com ampla participacao de desenvolvedores ao redor do mundo.",
     "Variacao em voz passiva contendo metadados institucionais.",
     "PAIR_15_B"),

    # Metadata 3: Kafka
    ("Como o Apache Kafka atinge alta taxa de transferencia na gravacao em disco?",
     "O Kafka foi desenvolvido originalmente no LinkedIn por Jay Kreps e posteriormente doado para a Apache Software Foundation onde se tornou um projeto de alto nivel.",
     "Historia de origem e governanca da fundacao (RELATED); nao explica sequential I/O nem page cache.",
     None),

    # Metadata 4: Git
    ("Como o Git calcula hashes de objetos para garantir integridade criptografica?",
     "O Git foi escrito por Linus Torvalds em 2005 para substituir o BitKeeper no desenvolvimento do kernel Linux e virou padrao absoluto de controle de versao.",
     "Historia de criacao do Git (RELATED); nao explica o algoritmo de hash SHA nem a estrutura de blobs/trees.",
     None),

    # Metadata 5: React
    ("Como o Virtual DOM do React otimiza a atualizacao da interface do usuario?",
     "O React e uma biblioteca JavaScript mantida pela Meta sob licenca MIT e foi lancada publicamente em 2013 com imensa popularidade no frontend moderno.",
     "Metadados de mantenedora e ano de lancamento (RELATED); nao explica reconciliation nem diffing de VDOM.",
     None),

    # Metadata 6: PostgreSQL
    ("Como o PostgreSQL implementa o controle de concorrencia multiversao (MVCC)?",
     "O PostgreSQL teve origem no projeto POSTGRES liderado por Michael Stonebraker na Universidade de Berkeley e e amplamente elogiado pela sua conformidade com padroes SQL.",
     "Origem academica e elogios gerais (RELATED); nao explica xmin, xmax nem tuplas mortas.",
     None),

    # Metadata 7: Redis
    ("Como o Redis gerencia estruturas de dados complexas em memoria principal?",
     "O Redis foi criado por Salvatore Sanfilippo (conhecido como antirez) na Italia e ganhou ampla adocao em startups do Vale do Silicio para arquiteturas em tempo real.",
     "Historia do criador e adocao comercial (RELATED); nao explica dicts, ziplists nem skiplists.",
     None),

    # Metadata 8: Rust
    ("Como o compilador do Rust garante seguranca de memoria sem utilizar Garbage Collector?",
     "A linguagem Rust foi criada por Graydon Hoare na Mozilla Research e foi eleita por varios anos consecutivos a tecnologia mais amada em pesquisas com desenvolvedores.",
     "Metadados de criacao na Mozilla e pesquisas de popularidade (RELATED); nao explica ownership nem borrow checker.",
     None),

    # Metadata 9: Go
    ("Como o scheduler do Go gerencia corrotinas concorrentes no modelo M:N?",
     "O Go foi concebido no Google por Robert Griesemer, Rob Pike e Ken Thompson com foco em simplicidade, produtividade de engenharia e tempos de compilacao rapidos.",
     "Historia dos criadores no Google e metas de design (RELATED); nao explica o scheduler de processadores logicos P, threads M e goroutines G.",
     None),

    # Metadata 10: GraphQL
    ("Como o motor GraphQL resolve consultas aninhadas evitando problemas de overfetching?",
     "O GraphQL foi especificado internamente pelo Facebook em 2012 para resolver problemas em aplicativos mobile e foi disponibilizado em open-source sob a GraphQL Foundation.",
     "Historia corporativa e fundacao (RELATED); nao explica resolvers hierarquicos nem DataLoader.",
     None),

    # Autobiographical 1
    ("Como proteger tokens de sessao contra ataques de Cross-Site Scripting (XSS)?",
     "Trabalhei durante cinco anos na equipe de seguranca da minha empresa anterior e nos sempre priorizavamos discussoes sobre seguranca em todas as sprints do time.",
     "Declaracao biografica e de rotina de trabalho (RELATED); nao cita flags HttpOnly nem SameSite.",
     None),

    # Autobiographical 2
    ("Como implementar balanceamento de carga com algoritmo Round-Robin?",
     "Tenho vasta experiencia atuando com balanceadores de carga e na minha carreira corporativa sempre lidamos com diversos modelos de infraestrutura com nossos clientes.",
     "Declaracao de tempo de carreira e atuacao (RELATED); nao explica a distribuicao sequencial da carga.",
     None)
]

# Add remaining 21 related cases (Group D total: 35)
for i in range(1, 22):
    q = f"Como o compilador da tecnologia {i} realiza a otimizacao de codigo intermediario?"
    r = f"A tecnologia {i} pertence a categoria de ferramentas modernas desenvolvidas pela comunidade de software livre sob licenca permissiva e possui ampla aceitacao no mercado internacional."
    GROUP_D_CASES.append((
        q, r,
        f"Metadados institucionais e categorizacao generica sobre a tecnologia {i} sem explicar o mecanismo de compilacao ou otimizacao (RELATED).",
        None
    ))

# GROUP E: OFF_TOPIC (45 cases)
# 1. Radical ontological disjunction (botany, cooking, mechanics, medicine, construction, sports, literature)
# 2. Destructive antithesis (disabling protections)
GROUP_E_CASES = [
    # Culinary Pair (Pair 16)
    ("Como o balanceador de carga distribui requisicoes entre servidores saudaveis?",
     "Para fazer pao artesanal de fermentacao natural misturamos farinha de trigo com agua e levain, fazendo dobras a cada trinta minutos e assando em panela de ferro bem quente com vapor.",
     "Receita culinaria de panificacao artesanal: disjuncao ontologica radical em relacao a balanceamento de carga (OFF_TOPIC).",
     "PAIR_16_A"),
    ("Como o balanceador de carga distribui requisicoes entre servidores saudaveis?",
     "A gente mistura farinha d'agua com fermento biologico na tigela, sova a massa por quinze minutos e deixa descansando sob pano umido ate dobrar de volume antes de assar.",
     "Variacao coloquial de culinaria: disjuncao ontologica radical (OFF_TOPIC).",
     "PAIR_16_B"),

    # Automotive Mechanics Pair (Pair 17)
    ("Como o protocolo BGP seleciona a melhor rota para o encaminhamento de pacotes autônomos?",
     "Na revisao de dez mil quilometros esgotamos o oleo do motor pelo bujao do carter, trocamos o filtro de lubrificante 5W30 e inspecionamos as pastilhas de freio e o fluido hidraulico.",
     "Mecanica automotiva: troca de oleo e revisao de veiculo confrontada com roteamento de rede BGP (OFF_TOPIC).",
     "PAIR_17_A"),
    ("Como o protocolo BGP seleciona a melhor rota para o encaminhamento de pacotes autônomos?",
     "O carro precisa trocar o lubrificante a cada dez mil rodados tirando o oleo velho, trocando o filtro de combustivel e completando o nivel do reservatorio com aditivo de arrefecimento.",
     "Variacao de manutencao veicular: disjuncao ontologica radical (OFF_TOPIC).",
     "PAIR_17_B"),

    # Destructive Antithesis Pair (Pair 18)
    ("Como garantir a integridade dos dados durante gravacoes concorrentes em tabelas criticas?",
     "Para resolver o problema a gente desativa os locks da tabela, desliga as transacoes acid e remove as travas de banco para deixar a gravacao muito mais rapida sem esperas.",
     "Antitese destrutiva explosiva: expoem acoes que violam e eliminam garantias fundamentais de concorrencia (OFF_TOPIC).",
     "PAIR_18_A"),
    ("Como garantir a integridade dos dados durante gravacoes concorrentes em tabelas criticas?",
     "Desativam-se as travas de seguranca e removem-se os bloqueios de transacao do banco de dados para evitar esperas concorrentes e acelerar as gravacoes.",
     "Variacao em voz passiva de antitese destrutiva (OFF_TOPIC).",
     "PAIR_18_B"),

    # Botany 1: Orchids
    ("Como configurar particionamento por hash no Apache Kafka?",
     "Para cultivar orquideas phalaenopsis com saude devemos regar as raizes duas vezes por semana com agua filtrada e aplicar adubo NPK equilibrado nas folhas secas.",
     "Botanica e jardinagem: disjuncao ontologica radical (OFF_TOPIC).",
     None),

    # Botany 2: Roses
    ("Como o algoritmo Raft assegura que apenas um lider seja eleito por termo?",
     "A poda de roseiras deve ser feita durante os meses de inverno cortando os galhos em angulo chanfrado de quarenta e cinco graus acima das gemas mais fortes.",
     "Jardinagem de roseiras: disjuncao ontologica radical (OFF_TOPIC).",
     None),

    # Botany 3: Succulents
    ("Como o Redis realiza a persistencia assincrona de dados com o comando BGSAVE?",
     "Suculentas necessitam de solo arenoso com excelente drenagem e muita exposicao solar direta, suspendendo a irrigacao caso as folhas fiquem amareladas.",
     "Cuidados com plantas suculentas: disjuncao ontologica radical (OFF_TOPIC).",
     None),

    # Cooking: Carrot cake
    ("Como configurar conexoes seguras com mTLS no gateway de microsservicos?",
     "Bata as cenouras picadas no liquidificador com ovos e oleo vegetal, misture o acucar e a farinha em uma tigela e leve ao forno preaquecido a cento e oitenta graus.",
     "Receita de bolo de cenoura: disjuncao ontologica radical (OFF_TOPIC).",
     None),

    # Cooking: Risotto
    ("Como otimizar consultas analiticas no banco relacional utilizando particionamento?",
     "Doure a cebola finamente picada na manteiga, adicione o arroz arboreo e va despejando o caldo de legumes fervente concha por concha mexendo continuamente ate atingir o ponto al dente.",
     "Preparo de risoto culinario: disjuncao ontologica radical (OFF_TOPIC).",
     None),

    # Automotive: Tire alignment
    ("Como funciona a deteccao de conflitos de escrita em sistemas com consistencia eventual?",
     "O alinhamento e balanceamento das rodas do automovel deve ser feito a cada troca de pneus para evitar desgaste irregular da banda de rodagem e vibracoes na direcao.",
     "Manutencao automotiva de pneus: disjuncao ontologica radical (OFF_TOPIC).",
     None),

    # Medicine: Diabetes control
    ("Como o protocolo OAuth 2.0 protege contra vazamento do authorization code?",
     "O controle da glicemia em pacientes com diabetes requer monitoramento diario dos niveis sanguineos em jejum e administracao de doses adequadas de insulina de acao lenta.",
     "Medicina e endocrinologia: disjuncao ontologica radical (OFF_TOPIC).",
     None),

    # Veterinary: Puppy vaccination
    ("Como um pool de threads redimensiona threads ativas sob sobrecarga de tarefas?",
     "Filhotes de caes devem receber a primeira dose da vacina multipla V10 a partir de quarenta e cinco dias de vida com reforcos a cada tres semanas acompanhados de vermifugo.",
     "Medicina veterinaria de animais domesticos: disjuncao ontologica radical (OFF_TOPIC).",
     None),

    # Construction: Concrete mixing
    ("Como a tecnica de sharding distribui grandes volumes de dados em servidores distintos?",
     "A mistura de concreto estrutural exige o traco correto de cimento Portland, areia media lavada, brita graduada e agua, batidos na betoneira por tres minutos.",
     "Construcao civil e alvenaria: disjuncao ontologica radical (OFF_TOPIC).",
     None),

    # Carpentry: Wood sanding
    ("Como o Garbage Collector identifica objetos nao alcancaveis na memoria heap?",
     "Para dar acabamento em tabuas de madeira macica usamos lixa grossa de grao oitenta seguida de lixa fina cento e cinquenta antes de aplicar o verniz de protecao.",
     "Marcenaria e tratamento de madeira: disjuncao ontologica radical (OFF_TOPIC).",
     None),

    # Sports: Marathon training
    ("Como o protocolo HTTP/3 utiliza QUIC sobre UDP para acelerar conexoes?",
     "O plano de treinamento para corrida de maratona combina treinos longos aos finais de semana com intervalados de ritmo na pista para aumentar o VO2 maximo do atleta.",
     "Treinamento desportivo de atletismo: disjuncao ontologica radical (OFF_TOPIC).",
     None),

    # Astronomy: Moons of Jupiter
    ("Como implementar um mecanismo de circuit breaker resiliente em arquitetura de microsservicos?",
     "Com um telescopio de abertura de cem milimetros e possivel avistar facilmente as quatro luas galileanas de Jupiter: Io, Europa, Ganimedes e Calisto orbitando o planeta.",
     "Astronomia observacional: disjuncao ontologica radical (OFF_TOPIC).",
     None),

    # Literature: Camaoes Sonnets
    ("Como configurar politicas de retries com backoff e jitter em servicos distribuidos?",
     "Os sonetos de Luis de Camoes no classicismo portugues caracterizam-se pela metrificacao em decassilabos heroicos e pela exploracao do desconcerto do mundo e do amor platonico.",
     "Literatura e analise poetica: disjuncao ontologica radical (OFF_TOPIC).",
     None),

    # Antithesis: Removing JWT filters
    ("Como proteger rotas restritas de uma API REST contra acesso nao autorizado?",
     "A solucao e remover os filtros de autenticacao, desativar a validacao de tokens JWT e liberar todos os endpoints sem restricao para agilizar as chamadas de qualquer cliente.",
     "Antitese destrutiva eliminando a seguranca da API (OFF_TOPIC).",
     None),

    # Antithesis: Disabling WAL and fsync
    ("Como assegurar a durabilidade das transacoes em banco de dados sob risco de desligamento repentino?",
     "Desligamos o write-ahead log (WAL) e desativamos a sincronizacao de disco com fsync para que o banco nunca perca tempo esperando gravacao fisica.",
     "Antitese destrutiva que anula a durabilidade das transacoes (OFF_TOPIC).",
     None),

    # Antithesis: Dropping circuit breakers and rate limits
    ("Como evitar que picos repentinos de trafego saturem a capacidade dos microsservicos internos?",
     "A gente arranca os circuit breakers e desliga os limites de rate limit para deixar passar todo o trafego sem qualquer barreira de protecao.",
     "Antitese destrutiva que elimina protecoes de resiliencia (OFF_TOPIC).",
     None)
]

# Add remaining 23 off-topic cases (Group E total: 45)
for i in range(1, 24):
    q = f"Como configurar o balanceamento dinamico de carga no subsistema {i}?"
    r = f"O processo de confeccao de vasos de argila do artesanato tradicional {i} requer amassamento da pasta mineral na roda de oleiro com posterior queima em forno a lenha."
    GROUP_E_CASES.append((
        q, r,
        f"Artesanato tradicional de cerâmica: disjuncao ontologica radical em relacao ao subsistema {i} de computacao (OFF_TOPIC).",
        None
    ))

# GROUP F: INSUFFICIENT (25 cases)
# Evasive business deflections, consulting fluff, explicit ignorance, bare fillers
GROUP_F_CASES = [
    # Evasive Pair (Pair 19)
    ("Como resolver gargalos de latencia no processamento de transacoes em bancos relacionais?",
     "Olha, isso vai depender exclusivamente do orcamento disponivel pela diretoria e de reunioes com a lideranca de negocios antes de qualquer definicao.",
     "Deflexao orcamentaria e corporativa evasiva sem substancia tecnica (INSUFFICIENT).",
     "PAIR_19_A"),
    ("Como resolver gargalos de latencia no processamento de transacoes em bancos relacionais?",
     "Essa questao depende puramente de aprovacao orcamentaria executiva e de analises de planejamento estrategico da empresa.",
     "Variacao formal de deflexao evasiva orcamentaria (INSUFFICIENT).",
     "PAIR_19_B"),

    # Consulting Fluff 1
    ("Como implementar particionamento eficiente em tabelas com alto volume de escritas?",
     "Cada caso e um caso no ambiente corporativo e qualquer decisao precisa passar por uma avaliacao holistica com os stakeholders da organizacao.",
     "Jargao corporativo evasivo sem conteudo tecnico aplicavel (INSUFFICIENT).",
     None),

    # Consulting Fluff 2
    ("Como evitar problemas de concorrencia na atualizacao simultanea de saldos de usuarios?",
     "Isso e algo muito complexo que varia muito de projeto para projeto e precisamos alinhar com o time de arquitetura antes de pensar em solucao.",
     "Resposta evasiva que posterga a solucao sem fornecer conteudo avaliavel (INSUFFICIENT).",
     None),

    # Explicit Ignorance 1
    ("Como configurar a sincronizacao semi-sincrona no MySQL?",
     "Nao sei responder, nunca estudei essa ferramenta nem tive oportunidade de trabalhar com esse recurso no banco.",
     "Declaracao explicita e honesta de ignorancia/desconhecimento (INSUFFICIENT).",
     None),

    # Explicit Ignorance 2
    ("Como funciona a eleicao de lider no protocolo Zab do Apache ZooKeeper?",
     "Desconheco totalmente o protocolo Zab e nao faco ideia de como essa eleicao ocorre internamente.",
     "Declaracao explicita de desconhecimento tecnico (INSUFFICIENT).",
     None),

    # Explicit Ignorance 3
    ("Como o compilador JIT do Java realiza desotimizacao de codigo compilado?",
     "Nao faco a menor ideia, nunca trabalhei com as entranhas da JVM.",
     "Expressao explicita de desconhecimento tecnico (INSUFFICIENT).",
     None),

    # Bare Fillers
    ("Como um reverse proxy protege aplicacoes backend contra ataques de Slowloris?",
     "Sim, com certeza conheco bem essa questao.",
     "Enunciado de preenchimento conversacional sem substancia tecnica (INSUFFICIENT).",
     None),

    ("Como o Redis lida com a liberacao de chaves quando a memoria atinge maxmemory?",
     "Com certeza, perfeitamente.",
     "Preenchimento conversacional vazio (INSUFFICIENT).",
     None),

    ("Como garantir que mensagens de fila sejam consumidas na ordem estrita de emissao?",
     "Entendi perfeitamente a sua pergunta sobre ordenacao de mensagens.",
     "Reconhecimento conversacional da pergunta sem nenhuma tentativa de solucao (INSUFFICIENT).",
     None)
]

# Add remaining 15 insufficient cases (Group F total: 25)
for i in range(1, 16):
    q = f"Como implementar a politica de tolerancia a falhas do servico {i}?"
    r = f"Nao sei responder nada sobre o servico {i}, nunca utilizei nem vi esse componente antes na minha vida profissional."
    GROUP_F_CASES.append((
        q, r,
        f"Declaracao explicita de desconhecimento e falta de evidencia sobre o servico {i} (INSUFFICIENT).",
        None
    ))

# GROUP G: UNKNOWN (20 cases)
# Tautology and genuine ambiguity/indeterminacy
GROUP_G_CASES = [
    # Tautology Pair (Pair 20)
    ("Como a replicacao de dados garante a disponibilidade do sistema distribuido?",
     "A replicacao de dados mantem o sistema disponivel porque ela replica os registros de maneira que os dados fiquem replicados.",
     "Tautologia reflexiva circular sem ganho informacional substantivo (UNKNOWN).",
     "PAIR_20_A"),
    ("Como a replicacao de dados garante a disponibilidade do sistema distribuido?",
     "Sao replicados os dados porque a replicacao executa a copia das tabelas para que os nós permaneçam replicados de forma replicada.",
     "Variacao em voz passiva de tautologia circular sem ganho semantico (UNKNOWN).",
     "PAIR_20_B"),

    # Tautology 2: Balancing
    ("Como o balanceador de carga distribui o trafego de rede entre servidores?",
     "O balanceador de carga distribui o trafego porque executa o balanceamento dos servidores de modo que o trafego fique balanceado.",
     "Tautologia circular reflexiva (UNKNOWN).",
     None),

    # Tautology 3: Sorting
    ("Como o banco de dados ordena os registros na clausula ORDER BY?",
     "O banco de dados ordena os registros porque faz uma ordenacao dos dados de forma que os registros fiquem ordenados.",
     "Tautologia circular reflexiva (UNKNOWN).",
     None),

    # Tautology 4: Locking
    ("Como a trava de tabela impede que outras transacoes alterem os registros concorrentes?",
     "A trava trava a tabela porque mantem o travamento de modo que as transacoes concorrentes fiquem travadas pelo travador.",
     "Tautologia circular reflexiva (UNKNOWN).",
     None),

    # Tautology 5: Indexing
    ("Como os indices aceleram a localizacao de registros na tabela relacional?",
     "Os indices indexam a tabela porque criam uma indexacao para que os dados sejam indexados de forma indexada.",
     "Tautologia circular reflexiva (UNKNOWN).",
     None),

    # Genuine Ambiguity 1
    ("Qual e a estrategia ideal de particionamento para series temporais sob alta carga?",
     "A abordagem pode variar conforme a situacao de como a equipe resolver fazer diante dos fatos na hora.",
     "Enunciado genuinamente indeterminado e ambiguo sobre o procedimento a adotar (UNKNOWN).",
     None),

    # Genuine Ambiguity 2
    ("Como o subsistema deve reagir diante de uma perda temporaria de conectividade com o banco?",
     "Ha situacoes operacionais onde a conduta pode pender para uma alternativa ou para outra opcao dependendo de fatores imprevistos.",
     "Indeterminacao genuina com dupla interpretacao vazia (UNKNOWN).",
     None)
]

# Add remaining 12 unknown cases (Group G total: 20)
for i in range(1, 13):
    q = f"Qual e a conduta recomendada para o tratamento de falhas transientes no subsistema {i}?"
    r = f"O comportamento da aplicacao pode variar conforme a situacao de como a equipe resolver fazer na hora para lidar com o subsistema {i}."
    GROUP_G_CASES.append((
        q, r,
        f"Indeterminacao e ambiguidade genuina sobre a conduta no subsistema {i} (UNKNOWN).",
        None
    ))
