"""
Update script to replace duplicate cases in scratch/build_stage_31_7_17_dataset.py
Ensures 100% strict novelty (0 duplicates in questions or responses against Stage 31.7.13).
"""

import json

replacements = {
    # P09
    '''add_case(
    "P09_compare_tcp_udp_omit_overhead", "PARTIAL_COVERAGE",
    "Compare os protocolos TCP e UDP quanto a garantias de entrega, overhead de conexão e cenários ideais de uso.",
    "O TCP garante entrega ordenada e sem perdas através de confirmações ACK e retransmissões, sendo ideal para aplicações onde integridade é crítica como navegação web.",
    "PARTIAL", ["garantias de entrega TCP vs UDP", "overhead de conexão e uso"],
    ["garantias de entrega TCP"],
    "Explica o TCP em garantias, mas não detalha o overhead do UDP nem o compara adequadamente.",
    form="formal", epistemic="CONCEPTUAL"
)''': '''add_case(
    "P09_compare_protobuf_json_omit_cpu", "PARTIAL_COVERAGE",
    "Compare a serialização de mensagens via Protocol Buffers binário e JSON textual quanto a consumo de banda de rede e sobrecarga de parsing de CPU.",
    "O Protobuf reduz drasticamente o tráfego de rede gerando cargas binárias compactas codificadas em varints, exigindo muito menos bytes trafegados por mensagem.",
    "PARTIAL", ["consumo de banda Protobuf vs JSON", "sobrecarga de parsing de CPU"],
    ["consumo de banda de rede com Protobuf"],
    "Explica a economia de banda de rede com Protobuf, mas omite a análise da sobrecarga de parsing de CPU entre formatos.",
    form="formal", epistemic="CONCEPTUAL"
)''',

    # P23
    '''add_case(
    "P23_compare_rest_graphql_omit_caching", "PARTIAL_COVERAGE",
    "Compare REST e GraphQL considerando over-fetching de dados em clientes móveis e complexidade de caching em proxies HTTP.",
    "O GraphQL resolve o problema de over-fetching ao permitir que o aplicativo cliente requisite exatamente os atributos específicos necessários na tela.",
    "PARTIAL", ["over-fetching REST vs GraphQL", "complexidade de caching em proxies"],
    ["over-fetching no GraphQL"],
    "Cobre o over-fetching, mas ignora a complexidade de caching em proxies HTTP (POST requests).",
    form="formal", epistemic="CONCEPTUAL"
)''': '''add_case(
    "P23_compare_dynamo_spanner_omit_stale", "PARTIAL_COVERAGE",
    "Compare o modelo de consistência eventual em Dynamo-style databases e linearizabilidade em Spanner quanto a latência de escrita e garantias contra leituras obsoletas.",
    "O modelo de consistência eventual em bancos Dynamo permite escritas ultra-rápidas com baixa latência local sem aguardar consenso síncrono global entre nós.",
    "PARTIAL", ["latência de escrita Dynamo vs Spanner", "garantias contra leituras obsoletas"],
    ["baixa latência de escrita em consistência eventual"],
    "Aborda a latência de escrita no Dynamo, mas omite as garantias contra leituras obsoletas e a comparação com linearizabilidade.",
    form="formal", epistemic="CONCEPTUAL"
)''',

    # R01-R06
    '''add_case(
    "R01_qdrant_description", "RELATED_THEMATIC",
    "Como o Qdrant executa busca vetorial aproximada em alta dimensão com filtros de metadados?",
    "O Qdrant é um banco de dados vetorial de código aberto escrito em Rust, projetado para armazenamento de embeddings de inteligência artificial.",
    "RELATED", ["executar busca vetorial com filtros de metadados"], ["nenhum mecanismo de busca ou filtragem demonstrado"],
    "Apenas descreve a ferramenta e linguagem sem explicar o algoritmo de busca vetorial ou filtragem.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R02_scylladb_description", "RELATED_THEMATIC",
    "Como o ScyllaDB atinge baixa latência substituindo a JVM pelo framework Seastar?",
    "O ScyllaDB é compatível com o Apache Cassandra e muito adotado para casos de uso de Internet das Coisas e telemetria de veículos.",
    "RELATED", ["como atinge baixa latência substituindo JVM por Seastar"], ["nenhum mecanismo de Seastar ou arquitetura demonstrado"],
    "Menciona compatibilidade e casos de uso sem explicar a arquitetura thread-per-core ou Seastar.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R03_omnimesh_fictional_description", "RELATED_THEMATIC",
    "Como a malha inventada OmniMesh balanceia carga de tráfego gRPC em tempo real?",
    "A OmniMesh é uma malha de serviços corporativa de última geração lançada este ano com foco em integração de nuvens híbridas.",
    "RELATED", ["como balanceia tráfego gRPC em tempo real"], ["nenhum mecanismo de balanceamento demonstrado"],
    "Descrição comercial de produto sem explicar nenhum algoritmo de roteamento ou balanceamento.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R04_git_trivia_linus", "RELATED_THEMATIC",
    "Como o Git calcula hashes criptográficos para assegurar a integridade de commits e objetos?",
    "O Git foi criado por Linus Torvalds em 2005 porque ele estava insatisfeito com a ferramenta proprietária BitKeeper após perder a licença gratuita.",
    "RELATED", ["como Git calcula hashes para integridade de commits"], ["nenhum mecanismo de hash SHA ou integridade demonstrado"],
    "Curiosidade biográfica sobre a origem do Git sem qualquer menção à árvore de objetos ou SHA.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R05_cpu_l1_cache_hardware", "RELATED_THEMATIC",
    "Como organizar estruturas de dados para otimizar localidade de referência em caches da CPU?",
    "O processador Intel Core i9 possui 32 kilobytes de cache de instruções L1 e 48 kilobytes de cache de dados L1 por núcleo de processamento.",
    "RELATED", ["organizar estruturas para localidade de referência em cache"], ["nenhum mecanismo de organização de estruturas demonstrado"],
    "Trivia de especificações físicas de hardware da CPU sem explicar alinhamento de memória ou contiguidade.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R06_c_language_bell_labs", "RELATED_THEMATIC",
    "Como o gerenciamento manual de memória via malloc e free previne fragmentação de heap em C?",
    "A linguagem C foi criada nos laboratórios Bell por Dennis Ritchie para reescrever o sistema operacional Unix em 1972.",
    "RELATED", ["como gerenciamento manual previne fragmentação de heap"], ["nenhum mecanismo de malloc ou free demonstrado"],
    "Fato histórico da criação de C e Unix sem responder à fragmentação de heap.",
    form="formal", epistemic="CONCEPTUAL"
)''': '''add_case(
    "R01_milvus_hnsw_description", "RELATED_THEMATIC",
    "Como o motor de busca vetorial Milvus constrói índices HNSW distribuídos para consultas de similaridade?",
    "O Milvus é um projeto de código aberto sob a Linux Foundation bastante utilizado por equipes de ciência de dados para projetos de embeddings corporativos.",
    "RELATED", ["construção de índices HNSW distribuídos no Milvus"], ["nenhum mecanismo de indexação HNSW demonstrado"],
    "Descreve a fundação mantenedora e adoção por equipes sem explicar o algoritmo de grafo HNSW.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R02_clickhouse_columnar_description", "RELATED_THEMATIC",
    "Como o ClickHouse processa consultas analíticas agregadas em alta velocidade através de armazenamento colunar vetorizado?",
    "O ClickHouse foi criado na Rússia para a plataforma de analytics Yandex Metrica e possui ampla documentação comunitária em diversos idiomas.",
    "RELATED", ["processamento analítico agregado com colunas vetorizadas no ClickHouse"], ["nenhum mecanismo vetorizado demonstrado"],
    "Fornece contexto de origem e documentação sem explicar a vetorização colunar.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R03_quantum_router_fictional_description", "RELATED_THEMATIC",
    "Como a ferramenta fictícia QuantumRouter otimiza rotas de pacotes IP usando algoritmos genéticos?",
    "O QuantumRouter é uma solução corporativa inovadora anunciada em um congresso de redes para transformar a governança de telecomunicações.",
    "RELATED", ["otimização de rotas IP via algoritmos genéticos"], ["nenhum mecanismo de roteamento ou algoritmo genético demonstrado"],
    "Discurso comercial de marketing sem apresentar nenhum algoritmo ou mecanismo operacional.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R04_sqlite_awards_history", "RELATED_THEMATIC",
    "Como o SQLite assegura atomicidade em transações de arquivo único utilizando journaling de rollback?",
    "O criador do SQLite recebeu prêmios de engenharia de software da ACM em reconhecimento pela sua contribuição à comunidade global de tecnologia.",
    "RELATED", ["atomicidade em arquivo único via rollback journal no SQLite"], ["nenhum mecanismo de rollback journal demonstrado"],
    "Menção a premiações do autor sem explicar o arquivo de journal de rollback.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R05_false_sharing_cache_line_trivia", "RELATED_THEMATIC",
    "Como prevenir falsas gravações em compartilhamento de linhas de cache (false sharing) em threads paralelas?",
    "A arquitetura x86_64 possui uma linha de cache padrão de 64 bytes que pode ser consultada no manual de microarquitetura da Intel.",
    "RELATED", ["prevenir false sharing em threads paralelas"], ["nenhum mecanismo de alinhamento ou padding demonstrado"],
    "Cita a dimensão física da linha de cache sem demonstrar alinhamento ou espaçamento de variáveis concorrentes.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R06_golang_gc_creators_trivia", "RELATED_THEMATIC",
    "Como o coletor de lixo do Go minimiza pausas de Stop-The-World através do algoritmo tricromático concorrente?",
    "A linguagem Go foi idealizada por Robert Griesemer, Rob Pike e Ken Thompson no Google em 2007 para simplificar a engenharia de software de grande porte.",
    "RELATED", ["minimização de Stop-The-World via algoritmo tricromático no Go"], ["nenhum mecanismo tricromático demonstrado"],
    "Cita os fundadores da linguagem e ano de criação sem explicar as cores do algoritmo tricromático de GC.",
    form="formal", epistemic="CONCEPTUAL"
)''',

    # O04, O05, O07
    '''add_case(
    "O04_antithesis_infinite_loop_no_timeout", "OFF_TOPIC_ANTITHESIS",
    "Como evitar sobrecarga e falhas em cascata quando um microsserviço dependente entra em colapso?",
    "Configuro os clientes para reenviar chamadas imediatamente sem timeout em loops infinitos contra o serviço degradado.",
    "OFF_TOPIC", ["evitar sobrecarga e falhas em cascata"], ["ação destrutiva de envio sem timeout em loops infinitos"],
    "Antítese operacional que intensifica a sobrecarga do serviço degradado.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O05_antithesis_grant_full_admin_no_auth", "OFF_TOPIC_ANTITHESIS",
    "Como aplicar o princípio do menor privilégio para conter riscos de movimentação lateral de invasores?",
    "Concedo permissões de superadministrador irrestritas para todas as contas e componentes sem necessidade de autenticação.",
    "OFF_TOPIC", ["aplicar princípio do menor privilégio para conter riscos"], ["ação destrutiva concedendo superadministrador sem autenticação"],
    "Propõe exatamente o inverso do princípio do menor privilégio.",
    form="active_1st", epistemic="CONCEPTUAL"
)''': '''add_case(
    "O04_antithesis_infinite_loop_no_timeout", "OFF_TOPIC_ANTITHESIS",
    "Como gerenciar timeouts e cancelamentos em pipelines de processamento assíncrono para liberar recursos presos?",
    "Elimino qualquer configuração de timeout e instruo as rotinas a esperarem eternamente em loops bloqueantes sem nunca desistir.",
    "OFF_TOPIC", ["gerenciar timeouts e cancelamentos para liberar recursos"], ["ação destrutiva que bloqueia eternamente em loop"],
    "Antítese operacional que perpetua o consumo de recursos bloqueados.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O05_antithesis_grant_full_admin_no_auth", "OFF_TOPIC_ANTITHESIS",
    "Como configurar políticas de segurança de rede (NetworkPolicies) em clusters Kubernetes para segmentar namespaces?",
    "Desabilito todo o firewall e libero todas as portas e tráfegos entre todos os pods e a internet pública sem nenhuma restrição.",
    "OFF_TOPIC", ["configurar NetworkPolicies para segmentar namespaces"], ["ação destrutiva desabilitando firewall e liberando tráfego irrestrito"],
    "Antítese que elimina qualquer segmentação de segurança de rede.",
    form="active_1st", epistemic="CONCEPTUAL"
)''',

    '''add_case(
    "O07_antithesis_disable_rate_limiting", "OFF_TOPIC_ANTITHESIS",
    "Como proteger servidores de autenticação contra ataques massivos de negação de serviço e força bruta?",
    "Removo qualquer controle de limitação de requisições e permito tentativas infinitas de login por segundo de qualquer IP.",
    "OFF_TOPIC", ["proteger contra DoS e força bruta"], ["ação destrutiva removendo rate limiting e permitindo tentativas infinitas"],
    "Elimina rate limiting expondo os servidores a exaustão de recursos.",
    form="active_1st", epistemic="CONCEPTUAL"
)''': '''add_case(
    "O07_antithesis_disable_rate_limiting", "OFF_TOPIC_ANTITHESIS",
    "Como proteger rotas públicas de reset de senha contra abuso automatizado e enumeração de e-mails?",
    "Retiro todos os limites de chamadas e envio e-mails para qualquer endereço solicitado sem validar existência ou frequência.",
    "OFF_TOPIC", ["proteger rotas de reset de senha contra abuso"], ["ação destrutiva retirando limites e enviando e-mails indiscriminadamente"],
    "Antítese que facilita o abuso automatizado de e-mails.",
    form="active_1st", epistemic="CONCEPTUAL"
)''',

    # O11 to O18
    '''add_case(
    "O11_frontend_css_grid_for_consensus", "OFF_TOPIC_ORTHOGONAL",
    "Como alcançar consenso tolerante a falhas em nós que executam o algoritmo Raft?",
    "Eu crio um container com display flex e coloco gap de 10 pixels entre os botões com background azul no CSS.",
    "OFF_TOPIC", ["alcançar consenso tolerante a falhas em Raft"], ["estilização visual CSS flexbox"],
    "Domínio frontend/CSS totalmente disjunto da questão de consenso distribuído em Raft.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O12_frontend_tailwind_for_kafka", "OFF_TOPIC_ORTHOGONAL",
    "Como rebalancear partições em um cluster Kafka sem interrupção de serviço aos consumidores?",
    "Utilizo classes utilitárias do Tailwind CSS como p-4 e text-center para estruturar as tags no HTML e centralizar os elementos.",
    "OFF_TOPIC", ["rebalancear partições no Kafka"], ["classes utilitárias de Tailwind CSS no HTML"],
    "Estilização HTML/Tailwind é funcionalmente irrelevante para particionamento de tópicos no Kafka.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O13_frontend_react_useeffect_for_deadlock", "OFF_TOPIC_ORTHOGONAL",
    "Como eliminar a possibilidade de deadlocks quando transações disputam múltiplos registros?",
    "Utilizo o hook useEffect do React com array de dependências vazio para renderizar o componente na tela assim que a página carregar.",
    "OFF_TOPIC", ["eliminar deadlocks entre transações concorrentes"], ["hook useEffect do React renderizando componente na tela"],
    "Ciclo de vida de componente React na interface web é ortogonal a deadlocks em banco transacional.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O14_frontend_webpack_code_splitting_for_quorum", "OFF_TOPIC_ORTHOGONAL",
    "Como calcular quórum de maioria em um cluster distribuído com tolerância a partições de rede?",
    "Configuro code splitting no Webpack para gerar bundles menores de JavaScript e otimizar o tempo de carregamento no navegador.",
    "OFF_TOPIC", ["calcular quórum de maioria sob partição de rede"], ["Webpack code splitting para bundles JS no navegador"],
    "Otimização de empacotamento JS para navegador não tem nexo causal com quórum distribuído.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O15_frontend_media_queries_for_wal", "OFF_TOPIC_ORTHOGONAL",
    "Como garantir durabilidade de transações em banco de dados sem persistir tabelas de imediato?",
    "Uso CSS Grid e media queries para criar design responsivo com padding adaptável para telas widescreen.",
    "OFF_TOPIC", ["garantir durabilidade sem persistir tabelas de imediato"], ["media queries e design responsivo para telas widescreen"],
    "Design responsivo de layout CSS em nada se relaciona à durabilidade de logs em banco de dados.",
    form="active_1st", epistemic="CONCEPTUAL"
)

# 5.3 Orthogonal Domain: AI / Machine Learning in Backend / Database Performance Questions
add_case(
    "O16_ml_linear_regression_deadlock", "OFF_TOPIC_ORTHOGONAL",
    "Como evitar deadlocks em transações financeiras com locks concorrentes?",
    "Treino um modelo de regressão linear supervisionado usando Scikit-Learn para calcular o erro médio quadrático dos dados.",
    "OFF_TOPIC", ["evitar deadlocks em transações concorrentes"], ["modelo de regressão linear com Scikit-Learn e erro médio quadrático"],
    "Regressão linear e Scikit-Learn são domínios de IA/ML disjuntos de concorrência e transações ACID.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O17_ml_kmeans_clustering_indexes", "OFF_TOPIC_ORTHOGONAL",
    "Como criar índices parciais no banco de dados para acelerar buscas por registros ativos?",
    "Executo o algoritmo k-means para agrupar clientes em quatro clusters não supervisionados baseando-se no valor de compras.",
    "OFF_TOPIC", ["criar índices parciais no banco para acelerar buscas"], ["algoritmo k-means agrupando clientes em clusters"],
    "Agrupamento não-supervisionado K-Means não tem pertinência causal com índices parciais de bancos de dados.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O18_ml_random_forest_tcp_handshake", "OFF_TOPIC_ORTHOGONAL",
    "Como funciona o handshake de três vias no protocolo TCP para estabelecer uma conexão confiável?",
    "Construo uma floresta aleatória com 100 árvores de decisão para classificar clientes com risco de cancelamento de assinatura.",
    "OFF_TOPIC", ["handshake de três vias no protocolo TCP"], ["floresta aleatória com 100 árvores de decisão"],
    "Classificação de churn por Random Forest é ortogonal ao protocolo de rede TCP.",
    form="active_1st", epistemic="CONCEPTUAL"
)''': '''add_case(
    "O11_frontend_css_grid_for_consensus", "OFF_TOPIC_ORTHOGONAL",
    "Como o algoritmo de Paxos garante que um único valor seja escolhido em um sistema assíncrono sujeito a falhas?",
    "Eu adiciono uma classe no elemento HTML com display flex e coloco justify-content center para centralizar os cards na tela.",
    "OFF_TOPIC", ["garantir valor único via Paxos em sistema assíncrono"], ["estilização visual CSS flexbox"],
    "Domínio frontend de centralização CSS totalmente disjunto de consenso em Paxos.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O12_frontend_tailwind_for_kafka", "OFF_TOPIC_ORTHOGONAL",
    "Como particionar tópicos no Apache Kafka para garantir ordem estrita por chave de mensagem?",
    "Uso as classes utilitárias text-gray-500 e border-rounded do Tailwind CSS para estipular a borda das caixas de texto no formulário.",
    "OFF_TOPIC", ["particionar tópicos garantindo ordem por chave no Kafka"], ["classes utilitárias de Tailwind CSS no formulário"],
    "Estilização de bordas no Tailwind não resolve particionamento de tópicos Kafka.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O13_frontend_react_useeffect_for_deadlock", "OFF_TOPIC_ORTHOGONAL",
    "Como o algoritmo de duas fases (2PL) previne inconsistências em execuções transacionais concorrentes?",
    "Crio um hook personalizado com useState no React para guardar o valor digitado no input do usuário na tela.",
    "OFF_TOPIC", ["prevenir inconsistências via 2PL em transações concorrentes"], ["hook useState do React para input de formulário"],
    "Estado de componente React no navegador não tem relação com controle de concorrência 2PL.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O14_frontend_webpack_code_splitting_for_quorum", "OFF_TOPIC_ORTHOGONAL",
    "Como definir a composição de grupos de replicação no Raft para sobreviver a falhas de minoria?",
    "Configuro dynamic imports no Vite para dividir o bundle em módulos menores carregados sob demanda na página inicial.",
    "OFF_TOPIC", ["composição de grupos no Raft para tolerar falhas de minoria"], ["divisão de bundles com dynamic imports no Vite"],
    "Otimização de bundling no Vite não tem nexo com quórum no Raft.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O15_frontend_media_queries_for_wal", "OFF_TOPIC_ORTHOGONAL",
    "Como sincronizar logs de transação com disco (fsync) para evitar perda de dados em quedas de energia?",
    "Aplico media queries com max-width de 768 pixels no CSS para ocultar a barra lateral em telas de smartphones.",
    "OFF_TOPIC", ["sincronizar logs de transação via fsync contra quedas de energia"], ["media queries ocultando barra lateral em smartphones"],
    "Responsividade CSS em telas móveis não se relaciona à persistência fsync de transações.",
    form="active_1st", epistemic="CONCEPTUAL"
)

# 5.3 Orthogonal Domain: AI / Machine Learning in Backend / Database Performance Questions
add_case(
    "O16_ml_linear_regression_deadlock", "OFF_TOPIC_ORTHOGONAL",
    "Como prevenir deadlocks distribuídos em transações de microsserviços via ordered locking?",
    "Ajusto os hiperparâmetros de uma regressão logística no Scikit-Learn calculando a matriz de confusão e a acurácia global do modelo.",
    "OFF_TOPIC", ["prevenir deadlocks distribuídos via ordered locking"], ["regressão logística no Scikit-Learn e matriz de confusão"],
    "Treinamento de regressão logística supervisionada é ortogonal à ordenação de locks distribuídos.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O17_ml_kmeans_clustering_indexes", "OFF_TOPIC_ORTHOGONAL",
    "Como estruturar índices compostos no PostgreSQL para suportar filtros de igualdade e ordenação por intervalo?",
    "Executo o método fit do algoritmo K-Means com k igual a cinco para agrupar clientes por faixa de renda.",
    "OFF_TOPIC", ["estruturar índices compostos para igualdade e ordenação"], ["K-Means agrupando clientes por faixa de renda"],
    "Clusterização não supervisionada de clientes é ortogonal à indexação no PostgreSQL.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O18_ml_random_forest_tcp_handshake", "OFF_TOPIC_ORTHOGONAL",
    "Como o algoritmo Nagle reduz o envio de pacotes minúsculos em fluxos de rede sob TCP?",
    "Treino um classificador XGBoost com profundidade máxima quatro para prever inadimplência bancária de proponentes.",
    "OFF_TOPIC", ["reduzir pacotes minúsculos via algoritmo de Nagle no TCP"], ["XGBoost prevendo inadimplência bancária"],
    "Classificação com XGBoost é disjunta de controle de buffering de pacotes em TCP.",
    form="active_1st", epistemic="CONCEPTUAL"
)''',

    # O21 to O25
    '''add_case(
    "O21_devops_dockerfile_for_sql_perf", "OFF_TOPIC_ORTHOGONAL",
    "Como otimizar o plano de execução de uma consulta SQL com ordenação volumosa em disco?",
    "Crio um arquivo Dockerfile com instrução FROM alpine e rodo apk add curl para instalar pacotes no container.",
    "OFF_TOPIC", ["otimizar plano de execução de consulta SQL com ordenação em disco"], ["Dockerfile com FROM alpine e apk add curl"],
    "Comandos de build de container Docker não resolvem plano de execução de SQL.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O22_devops_ci_pipeline_for_caching", "OFF_TOPIC_ORTHOGONAL",
    "Como implementar uma política de expiração LRU em cache distribuído na memória?",
    "Configuramos uma pipeline no GitHub Actions que roda testes unitários e faz deploy automático a cada commit na branch main.",
    "OFF_TOPIC", ["implementar política de expiração LRU em cache"], ["pipeline no GitHub Actions com deploy a cada commit"],
    "Esteira de CI/CD não tem relação com o algoritmo de remoção LRU em memória.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "O23_devops_jira_scrum_for_deadlock", "OFF_TOPIC_ORTHOGONAL",
    "Como eliminar a possibilidade de deadlocks quando transações disputam múltiplos registros?",
    "Organizamos sprints ágeis no Jira com reuniões diárias de standup e cerimônias de retrospectiva no final da semana.",
    "OFF_TOPIC", ["eliminar deadlocks entre transações"], ["sprints ágeis no Jira com cerimônias de standup e retrospectiva"],
    "Metodologia ágil e Jira não resolvem ordenação de locks transacionais em bancos de dados.",
    form="active_1st", epistemic="DECLARATION"
)
add_case(
    "O24_devops_selenium_for_b_tree", "OFF_TOPIC_ORTHOGONAL",
    "Como as árvores B-Tree mantêm tempo logarítmico determinístico em operações de busca pontual?",
    "Executo testes automatizados de ponta a ponta com Selenium WebDriver simulando cliques de usuários no formulário de login.",
    "OFF_TOPIC", ["árvores B-Tree mantendo tempo logarítmico"], ["testes E2E com Selenium WebDriver simulando cliques no login"],
    "Testes de interface com Selenium não explicam a estrutura algorítmica de árvores B-Tree.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "O25_devops_confluence_for_wal", "OFF_TOPIC_ORTHOGONAL",
    "Como garantir durabilidade de transações em banco de dados sem persistir tabelas de imediato?",
    "Crio páginas de documentação técnica no Confluence para registrar como a equipe deve documentar arquiteturas corporativas.",
    "OFF_TOPIC", ["garantir durabilidade sem persistir tabelas de imediato"], ["páginas de documentação no Confluence"],
    "Documentação corporativa no Confluence é disjunta da durabilidade transacional de bancos de dados.",
    form="active_1st", epistemic="DECLARATION"
)''': '''add_case(
    "O21_devops_dockerfile_for_sql_perf", "OFF_TOPIC_ORTHOGONAL",
    "Como reescrever subconsultas correlacionadas pesadas utilizando janelamento SQL (window functions)?",
    "Adiciono uma etapa no Dockerfile com a diretiva COPY requirements.txt e executo pip install para construir a imagem Docker.",
    "OFF_TOPIC", ["reescrever subconsultas correlacionadas com window functions"], ["diretiva COPY e pip install em Dockerfile"],
    "Instalação de pacotes em imagem Docker não responde à otimização de consultas SQL.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O22_devops_ci_pipeline_for_caching", "OFF_TOPIC_ORTHOGONAL",
    "Como configurar políticas de despejo LFU (Least Frequently Used) em nós de cache em memória?",
    "Criamos um workflow no GitLab CI que roda linters automáticos e publica artefatos no repositório de pacotes a cada tag criada.",
    "OFF_TOPIC", ["configurar políticas de despejo LFU em cache"], ["workflow no GitLab CI rodando linters e gerando tags"],
    "Esteira de lint no GitLab CI não resolve despejo de dados LFU em cache.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "O23_devops_jira_scrum_for_deadlock", "OFF_TOPIC_ORTHOGONAL",
    "Como usar grafos direcionados de alocação de recursos para detectar deadlocks em tempo de execução?",
    "Nós fazemos reuniões semanais de planejamento de sprint no Jira para estimar histórias de usuário em story points.",
    "OFF_TOPIC", ["usar grafos direcionados de alocação de recursos para detectar deadlocks"], ["reuniões de planejamento e story points no Jira"],
    "Estimativas em story points no Jira são ortogonais à análise de grafos de deadlock.",
    form="active_1st", epistemic="DECLARATION"
)
add_case(
    "O24_devops_selenium_for_b_tree", "OFF_TOPIC_ORTHOGONAL",
    "Como as árvores B-Tree mantêm tempo logarítmico determinístico em operações de busca pontual?",
    "Executo testes automatizados de ponta a ponta com Selenium WebDriver simulando cliques de usuários no formulário de login.",
    "OFF_TOPIC", ["árvores B-Tree mantendo tempo logarítmico"], ["testes E2E com Selenium WebDriver simulando cliques no login"],
    "Testes de interface com Selenium não explicam a estrutura algorítmica de árvores B-Tree.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "O25_devops_confluence_for_wal", "OFF_TOPIC_ORTHOGONAL",
    "Como o Write-Ahead Logging (WAL) permite recuperação rápida após falha catastrófica de processo no banco?",
    "Escrevemos artigos no Confluence organizados em pastas para catalogar as boas práticas de integração do time de suporte.",
    "OFF_TOPIC", ["como WAL permite recuperação após falha catastrófica"], ["artigos no Confluence organizados em pastas"],
    "Documentação de processos no Confluence é disjunta de logs WAL de banco de dados.",
    form="active_1st", epistemic="DECLARATION"
)''',

    # O27 to O35
    '''add_case(
    "O27_alien_sports_football", "OFF_TOPIC_ALIEN",
    "Como particionar dados em cluster distribuído minimizando migração ao adicionar nós?",
    "Acompanho as partidas de futebol no estádio todo domingo com meus amigos torcendo pelo campeonato estadual.",
    "OFF_TOPIC", ["particionar dados minimizando migração em cluster"], ["atividades de lazer acompanhando futebol no estádio"],
    "Domínio esportivo alienígena à engenharia de software.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O28_alien_outdoor_bicycle", "OFF_TOPIC_ALIEN",
    "Como proteger sistemas encadeados contra esgotamento de conexões quando um serviço falha?",
    "Costumo pedalar de bicicleta no parque pela manhã para respirar ar puro e passear com meu cachorro na grama.",
    "OFF_TOPIC", ["proteger sistemas contra esgotamento de conexões"], ["passeio de bicicleta e ar livre"],
    "Atividade física cotidiana sem relação técnica.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O29_alien_shopping_mall", "OFF_TOPIC_ALIEN",
    "Como evitar consultas desnecessárias ao disco para verificar registros inexistentes?",
    "Fui ao shopping no final de semana comprar sapatos novos e aproveitei para almoçar na praça de alimentação com meus primos.",
    "OFF_TOPIC", ["evitar consultas desnecessárias ao disco"], ["passeio ao shopping e almoço"],
    "Atividade social alienígena ao tema de bancos de dados.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O30_alien_cinema_movie", "OFF_TOPIC_ALIEN",
    "Como alcançar consenso tolerante a falhas em nós que executam o algoritmo Raft?",
    "Fui ao cinema assistir a uma comédia divertida e comi um balde grande de pipoca com manteiga durante a sessão.",
    "OFF_TOPIC", ["alcançar consenso tolerante a falhas em Raft"], ["ida ao cinema com pipoca"],
    "Atividade de lazer alienígena a sistemas distribuídos.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O31_alien_supermarket", "OFF_TOPIC_ALIEN",
    "Como garantir durabilidade de transações em banco de dados sem persistir tabelas de imediato?",
    "Passei no supermercado ontem à noite para comprar leite, pão e sabão em pó antes de voltar para casa.",
    "OFF_TOPIC", ["garantir durabilidade transacional"], ["compras domésticas em supermercado"],
    "Atividade doméstica cotidiana.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O32_alien_dishes_cleaning", "OFF_TOPIC_ALIEN",
    "Como mitigar race conditions em saldo compartilhado de conta corrente?",
    "Terminei de lavar a louça do almoço na pia da cozinha e aproveitei para organizar os pratos nos armários.",
    "OFF_TOPIC", ["mitigar race conditions em saldo compartilhado"], ["tarefas domésticas lavando louça"],
    "Atividade doméstica sem qualquer relação com sistemas de informação.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O33_alien_tv_soap_opera", "OFF_TOPIC_ALIEN",
    "Como o broker do Kafka atinge taxa massiva de transferência na leitura de tópicos para a rede?",
    "Eu assisto à novela das nove na televisão todas as noites enquanto descanso no sofá da sala.",
    "OFF_TOPIC", ["taxa massiva de transferência de leitura no Kafka"], ["assistir novela na televisão"],
    "Hábito doméstico alienígena.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O34_alien_videogame", "OFF_TOPIC_ALIEN",
    "Como aplicar limitação de taxa em chamadas de API suportando rajadas controladas?",
    "Fiquei jogando videogame de corrida online até tarde da noite com amigos no meu console.",
    "OFF_TOPIC", ["limitação de taxa suportando rajadas"], ["jogar videogame de corrida no console"],
    "Lazer com videogame alienígena à computação corporativa.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O35_alien_bank_account_personal", "OFF_TOPIC_ALIEN",
    "Como eliminar a possibilidade de deadlocks quando transações disputam múltiplos registros?",
    "Eu consultei o extrato da minha conta bancária pessoal no aplicativo do celular para conferir se o salário já havia caído.",
    "OFF_TOPIC", ["eliminar possibilidade de deadlocks"], ["consulta pessoal de extrato no celular"],
    "Ação pessoal financeira do usuário que coincide com a palavra 'bancária', mas é semanticamente desprovida de nexo com concorrência de software.",
    form="active_1st", epistemic="UNKNOWN"
)''': '''add_case(
    "O27_alien_sports_football", "OFF_TOPIC_ALIEN",
    "Como projetar esquemas de particionamento de tabelas por hash para balancear I/O de disco?",
    "Acompanhei a vitória do meu time de basquete no ginásio municipal vibrando a cada arremesso de três pontos marcado.",
    "OFF_TOPIC", ["projetar particionamento por hash para balancear I/O"], ["assistir jogo de basquete no ginásio"],
    "Tema esportivo recreativo alienígena à engenharia de software.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O28_alien_outdoor_bicycle", "OFF_TOPIC_ALIEN",
    "Como gerenciar pools de threads assíncronos para evitar rejeição de tarefas sob picos repentinos?",
    "Fiz uma caminhada relaxante na praia no fim da tarde ouvindo o barulho das ondas do mar e colhendo conchas.",
    "OFF_TOPIC", ["gerenciar pools de threads assíncronos contra rejeição de tarefas"], ["caminhada na praia colhendo conchas"],
    "Passeio na praia é atividade recreativa alienígena a sistemas concorrentes.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O29_alien_shopping_mall", "OFF_TOPIC_ALIEN",
    "Como calcular a assinatura de uma mensagem usando HMAC-SHA256 para autenticar webhooks externos?",
    "Visitei uma feira de artesanato na praça central para escolher vasos de cerâmica coloridos para decorar a varanda.",
    "OFF_TOPIC", ["calcular HMAC-SHA256 para autenticar webhooks"], ["comprar vasos de cerâmica em feira de artesanato"],
    "Compra de artesanato doméstico alienígena à criptografia.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O30_alien_cinema_movie", "OFF_TOPIC_ALIEN",
    "Como o algoritmo de consenso Zab do ZooKeeper garante ordenação estrita de atualizações de estado?",
    "Fui ao teatro assistir a uma peça dramática de época e gostei muito da atuação dos atores principais no palco.",
    "OFF_TOPIC", ["ordenação de atualizações via Zab no ZooKeeper"], ["assistir peça de teatro"],
    "Apreciação de peça de teatro alienígena a sistemas distribuídos.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O31_alien_supermarket", "OFF_TOPIC_ALIEN",
    "Como configurar replicação semissíncrona no MySQL para evitar perda de transações comprometidas?",
    "Passei na padaria pela manhã para comprar pão francês quentinho, queijo minas e café moído na hora.",
    "OFF_TOPIC", ["configurar replicação semissíncrona no MySQL"], ["compras matinais na padaria"],
    "Café da manhã doméstico é tema alienígena a bancos de dados relacionais.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O32_alien_dishes_cleaning", "OFF_TOPIC_ALIEN",
    "Como evitar condição de corrida em contadores distribuídos usando instruções atômicas compare-and-swap?",
    "Reguei todas as plantas da sala e podei os galhos secos da samambaia que fica pendurada na janela.",
    "OFF_TOPIC", ["evitar condição de corrida com compare-and-swap atômico"], ["cuidar de plantas e regar samambaia"],
    "Jardinagem doméstica é atividade alienígena à computação.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O33_alien_tv_soap_opera", "OFF_TOPIC_ALIEN",
    "Como o broker do Kafka atinge taxa massiva de transferência na leitura de tópicos para a rede?",
    "Eu assisto à novela das nove na televisão todas as noites enquanto descanso no sofá da sala.",
    "OFF_TOPIC", ["taxa massiva de transferência de leitura no Kafka"], ["assistir novela na televisão"],
    "Hábito doméstico alienígena.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O34_alien_videogame", "OFF_TOPIC_ALIEN",
    "Como balancear tráfego HTTP entre instâncias de aplicação usando o algoritmo de menor número de conexões?",
    "Montei um quebra-cabeça de mil peças com desenho de montanhas nevadas durante as minhas férias em família.",
    "OFF_TOPIC", ["balancear tráfego HTTP via least connections"], ["montar quebra-cabeça de montanhas"],
    "Jogo de quebra-cabeça é atividade lúdica alienígena à infraestrutura de rede.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
    "O35_alien_bank_account_personal", "OFF_TOPIC_ALIEN",
    "Como o isolation level Serializable previne anomalias de escrita distorcida (write skew)?",
    "Fui até a agência dos correios despachar uma encomenda postal que precisava ser entregue na casa da minha avó.",
    "OFF_TOPIC", ["prevenir anomalia write skew via isolation level Serializable"], ["despachar encomenda nos correios"],
    "Envio de pacote postal alienígena a anomalias de isolamento transacional.",
    form="active_1st", epistemic="UNKNOWN"
)''',

    # I10, I11, I12, I16
    '''add_case(
    "I10_evasive_consult_docs", "INSUFFICIENT_EVIDENCE",
    "Como configurar réplicas síncronas de escrita no PostgreSQL?",
    "Para responder isso você deve consultar o manual e a documentação oficial da ferramenta.",
    "INSUFFICIENT", ["configurar réplicas síncronas no PostgreSQL"], ["evasão transferindo para documentação"],
    "Transfere a resposta para a documentação sem fornecer nenhuma instrução técnica.",
    form="evasive", epistemic="UNKNOWN"
)
add_case(
    "I11_evasive_depends_on_budget", "INSUFFICIENT_EVIDENCE",
    "Como evitar perda de mensagens quando um broker de eventos sofre queda abrupta de nó?",
    "Isso vai depender exclusivamente de quanto dinheiro o cliente tem disponível para gastar na nuvem.",
    "INSUFFICIENT", ["evitar perda de mensagens sob queda de broker"], ["evasiva financeira"],
    "Evasão financeira sem articular replicação, acionamento de acks ou discos duráveis.",
    form="evasive", epistemic="UNKNOWN"
)
add_case(
    "I12_evasive_senior_consultant", "INSUFFICIENT_EVIDENCE",
    "Como particionar um banco relacional massivo que ultrapassou a capacidade do nó primário?",
    "Um bom consultor experiente precisaria analisar a situação durante várias semanas para opinar com certeza.",
    "INSUFFICIENT", ["particionar banco relacional que ultrapassou nó primário"], ["evasiva postergando para consultoria"],
    "Evasiva postergando a análise sem apresentar estratégias de sharding ou federação.",
    form="evasive", epistemic="UNKNOWN"
)''': '''add_case(
    "I10_evasive_consult_docs", "INSUFFICIENT_EVIDENCE",
    "Como configurar réplicas de leitura com balanceamento de carga no PostgreSQL?",
    "Para saber esses detalhes operacionais você precisa abrir o manual oficial e pesquisar nos guias da documentação.",
    "INSUFFICIENT", ["configurar réplicas de leitura com balanceamento no PostgreSQL"], ["evasiva orientando a buscar na documentação"],
    "Evasiva remetendo à documentação sem instrução técnica.",
    form="evasive", epistemic="UNKNOWN"
)
add_case(
    "I11_evasive_depends_on_budget", "INSUFFICIENT_EVIDENCE",
    "Como dimensionar o cluster de brokers para suportar um milhão de mensagens por segundo?",
    "Essa resposta depende inteiramente da verba financeira que a diretoria liberou para gastar em infraestrutura no trimestre.",
    "INSUFFICIENT", ["dimensionar cluster de brokers para 1M msg/s"], ["evasiva financeira orçamentária"],
    "Evasão orçamentária sem apontar cálculos de capacidade ou partições.",
    form="evasive", epistemic="UNKNOWN"
)
add_case(
    "I12_evasive_senior_consultant", "INSUFFICIENT_EVIDENCE",
    "Como remodelar tabelas transacionais legadas para viabilizar migração para banco distribuído?",
    "Seria preciso contratar uma consultoria especializada por vários meses para conseguir emitir qualquer parecer sobre isso.",
    "INSUFFICIENT", ["remodelar tabelas legadas para migração para banco distribuído"], ["evasiva adiando para consultoria externa"],
    "Evasão delegando a consultoria externa sem descrever padrões técnicos.",
    form="evasive", epistemic="UNKNOWN"
)''',

    '''add_case(
    "I16_evasive_generic_monitoring", "INSUFFICIENT_EVIDENCE",
    "Como conter contenção de locks concorrentes em tabelas transacionais?",
    "A gente usa ferramentas de monitoramento para ver como as coisas estão se comportando no geral.",
    "INSUFFICIENT", ["conter contenção de locks concorrentes"], ["evasiva com ferramentas genéricas"],
    "Menção genérica e vaga sem nomear ferramentas nem mecanismos operacionais.",
    form="evasive", epistemic="UNKNOWN"
)''': '''add_case(
    "I16_evasive_generic_monitoring", "INSUFFICIENT_EVIDENCE",
    "Como mitigar gargalos de contenção de travas em bancos de dados de alta concorrência?",
    "A gente costuma ligar observabilidade genérica para acompanhar como o sistema está reagindo como um todo.",
    "INSUFFICIENT", ["mitigar gargalos de contenção de travas"], ["evasiva genérica mencionando observabilidade"],
    "Vagueza sem ferramentas nem mecanismos de mitigação de locks.",
    form="evasive", epistemic="UNKNOWN"
)''',

    # U01 to U05
    '''add_case(
    "U01_tautology_fast_is_quick", "UNKNOWN_TAUTOLOGY",
    "Como o particionamento em tabelas acelera o desempenho de consultas volumosas?",
    "O particionamento acelera as consultas porque faz as operações rodarem de forma muito mais rápida.",
    "UNKNOWN", ["como particionamento acelera desempenho"], ["repetição circular tautológica"],
    "Tautologia circular: diz que acelera porque faz rodar mais rápido, sem explicar redução de escopo de I/O.",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U02_tautology_locks_block", "UNKNOWN_TAUTOLOGY",
    "Por que ocorrem deadlocks em transações financeiras com múltiplos recursos?",
    "Os deadlocks ocorrem porque as transações ficam travadas quando ocorre um travamento entre elas.",
    "UNKNOWN", ["por que ocorrem deadlocks"], ["repetição circular 'ficam travadas quando ocorre travamento'"],
    "Tautologia circular pura: define travamento dizendo que ocorre quando trava.",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U03_tautology_secure_is_safe", "UNKNOWN_TAUTOLOGY",
    "Como a validação de assinatura criptográfica em tokens JWT impede fraudes de alteração de payload?",
    "A validação de assinatura impede fraudes porque ela garante que os dados permaneçam seguros e sem alterações fraudulentas.",
    "UNKNOWN", ["como validação de assinatura impede fraudes"], ["repetição circular 'impede fraude porque fica sem fraude'"],
    "Tautologia circular: afirma que impede fraude porque fica seguro e sem fraude, omitindo a chave simétrica/assimétrica e o hash.",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U04_tautology_cache_stores", "UNKNOWN_TAUTOLOGY",
    "Como a camada de cache reduz a latência percebida em consultas frequentes?",
    "O cache reduz a latência armazenando os dados em um local de cacheamento para ficarem em cache.",
    "UNKNOWN", ["como cache reduz latência em consultas frequentes"], ["repetição circular 'armazena em cacheamento para ficar em cache'"],
    "Tautologia circular que repete a palavra cache sem citar acesso em memória RAM ou índices O(1).",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U05_tautology_indexes_index", "UNKNOWN_TAUTOLOGY",
    "Como índices em árvore B diminuem o custo de consultas pontuais?",
    "Eles diminuem o custo indexando os registros de modo que o índice indexe a tabela adequadamente.",
    "UNKNOWN", ["como índices em árvore B diminuem custo"], ["repetição circular 'indexando de modo que o índice indexe'"],
    "Tautologia circular pura sobre indexação.",
    form="tautology", epistemic="UNKNOWN"
)''': '''add_case(
    "U01_tautology_fast_is_quick", "UNKNOWN_TAUTOLOGY",
    "Como a desnormalização de tabelas analíticas acelera relatórios de fechamento mensal?",
    "A desnormalização acelera os relatórios analíticos porque ela faz com que as operações de leitura fiquem muito mais rápidas.",
    "UNKNOWN", ["como desnormalização acelera relatórios analíticos"], ["circularidade: acelera porque fica mais rápido"],
    "Tautologia circular pura: afirma que acelera porque faz ficar mais rápido, sem citar eliminação de joins.",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U02_tautology_locks_block", "UNKNOWN_TAUTOLOGY",
    "Por que transações que disputam locks exclusivos entram em estado de espera mútua?",
    "Elas entram em espera mútua porque uma transação fica esperando a outra esperar num processo em que ambas esperam.",
    "UNKNOWN", ["por que transações entram em espera mútua"], ["circularidade: esperam porque ficam esperando"],
    "Tautologia circular pura de espera repetida.",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U03_tautology_secure_is_safe", "UNKNOWN_TAUTOLOGY",
    "Como o mascaramento de dados sensíveis protege informações confidenciais em logs de auditoria?",
    "O mascaramento protege informações confidenciais porque ele garante que os dados fiquem protegidos de modo sigiloso e confidencial.",
    "UNKNOWN", ["como mascaramento protege informações em logs"], ["circularidade: protege porque fica protegido e confidencial"],
    "Tautologia circular sem citar hashing, truncamento ou ofuscação.",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U04_tautology_cache_stores", "UNKNOWN_TAUTOLOGY",
    "Como o armazenamento temporário em camadas de buffer reduz a pressão sobre discos magnéticos?",
    "O buffer reduz a pressão armazenando os dados em uma estrutura de bufferização que serve justamente de buffer.",
    "UNKNOWN", ["como buffer temporário reduz pressão em disco"], ["circularidade: bufferiza na estrutura de buffer que serve de buffer"],
    "Tautologia circular que repete buffer sem explicar agregação em memória ou escrita em lote.",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U05_tautology_indexes_index", "UNKNOWN_TAUTOLOGY",
    "Como a estruturação de chaves ordenadas simplifica buscas por prefixo em tabelas de dados?",
    "Chaves ordenadas simplificam as buscas porque quando estão ordenadas a busca acontece em ordem de maneira ordenada.",
    "UNKNOWN", ["como chaves ordenadas simplificam busca por prefixo"], ["circularidade: ordenadas porque busca ocorre em ordem ordenada"],
    "Tautologia circular pura de ordenação.",
    form="tautology", epistemic="UNKNOWN"
)'''
}

with open("scratch/build_stage_31_7_17_dataset.py", "r", encoding="utf-8") as f:
    text = f.read()

count = 0
for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new)
        count += 1
    else:
        print("MISSING BLOCK:", old[:50])

print(f"Applied {count}/{len(replacements)} blocks.")

with open("scratch/build_stage_31_7_17_dataset.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Saved scratch/build_stage_31_7_17_dataset.py.")
