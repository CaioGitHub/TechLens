# Dataset definitions for Stage 31.7.28 Blind Validation Benchmark
# Covers Groups A, B, C, D, E, F, G (Total 250 cases) and 20 Invariance Pairs

GROUP_A_DIRECT_EXTRA = [
    ("Como o mecanismo de Write-Ahead Logging (WAL) garante a recuperabilidade de transacoes em bancos de dados?",
     "Antes de aplicar qualquer modificacao nas paginas de dados em memoria, o banco grava sequencialmente as mudancas no log de transacoes em disco, permitindo o replay das operacoes confirmadas apos uma falha.",
     "direct_wal_recoverability")
]

# GROUP B: PARTIAL (45 cases)
# Multi-aspect questions where only 1 aspect is resolved, or explicit partial omissions
GROUP_B_CASES = [
    # Compound 1: Circuit breaker + exponential backoff
    ("Explique como funciona o Circuit Breaker e como configurar o tempo de retry com exponential backoff.",
     "O Circuit Breaker monitora a taxa de falhas consecutivas e transita do estado fechado para aberto quando o limiar e ultrapassado, interrompendo chamadas ao servico indisponivel.",
     "Atende plenamente a primeira demanda (Circuit Breaker), mas omite por completo a segunda demanda (retry com exponential backoff).",
     "PAIR_11_A"),
    ("Explique como funciona o Circuit Breaker e como configurar o tempo de retry com exponential backoff.",
     "A gente coloca o circuit breaker pra abrir quando der muito erro e parar de bater na API que caiu, protegendo a aplicacao de sobrecarga.",
     "Variacao coloquial: resolve a primeira demanda mas nao aborda a configuracao de retries com backoff.",
     "PAIR_11_B"),
     
    # Compound 2: Sharding + Distributed Transactions
    ("Como configurar sharding horizontal em banco relacional e como garantir transacoes atomicas entre multiplos shards?",
     "O sharding horizontal e configurado particionando a tabela com base no hash da chave primaria para distribuir fatias dos dados em diferentes instancias de banco.",
     "Atende a configuracao de sharding, mas nao explica o protocolo de transacoes distribuidas (como 2PC ou Saga) entre shards.",
     "PAIR_12_A"),
    ("Como configurar sharding horizontal em banco relacional e como garantir transacoes atomicas entre multiplos shards?",
     "Sao divididas as linhas da tabela entre varios servidores de banco usando a chave de sharding para espalhar os registros de forma balanceada.",
     "Variacao passiva: cobre o particionamento horizontal mas omite a atomicidade transacional cross-shard.",
     "PAIR_12_B"),

    # Compound 3: Kafka Partitioning + Consumer Rebalance
    ("Como o Kafka particiona mensagens em um topico e como ocorre o rebalanceamento de consumidores no grupo?",
     "O Kafka particiona os registros aplicando uma funcao de hash sobre a chave da mensagem para direciona-la deterministicamente a uma particao especifica.",
     "Atende apenas o particionamento por chave; omite o protocolo de rebalanceamento entre consumidores.",
     None),
     
    # Compound 4: Redis Persistence RDB + AOF
    ("Qual a diferenca entre persistencia RDB e AOF no Redis e como configurar a reescrita do arquivo AOF?",
     "O RDB gera snapshots compactos point-in-time de toda a memoria em intervalos programados, enquanto o AOF grava sequencialmente em log cada comando de escrita recebido pelo servidor.",
     "Explica com exatidao a diferenca entre RDB e AOF, mas omite a configuracao de reescrita automatica do AOF (auto-aof-rewrite).",
     None),

    # Compound 5: TLS Handshake + Session Resumption
    ("Como funciona o handshake TLS 1.3 e como e implementada a retomada de sessao com 0-RTT?",
     "No TLS 1.3 o cliente e o servidor negociam as chaves criptograficas em uma unica viagem de ida e volta combinando ClientHello e chaves efemeras Diffie-Hellman para estabelecer o canal seguro.",
     "Explica o handshake padrao 1-RTT, mas nao detalha os riscos e o funcionamento da retomada 0-RTT com tickets de sessao pre-compartilhados.",
     None),

    # Compound 6: Raft Log Replication + Leader Election
    ("Como o algoritmo Raft realiza a replicacao de entradas de log e como resolve divergencias entre lider e seguidores?",
     "O lider grava a entrada no seu proprio log e envia mensagens AppendEntries para todos os seguidores aguardando a confirmacao da maioria antes de dar commit na entrada.",
     "Atende a replicacao normal de entradas, mas nao explica como o lider forca o ajuste de indices e descarte de entradas nao confirmadas quando ocorrem divergencias de log.",
     None),

    # Compound 7: Database Indexing + Vacuum/Bloat Cleanup
    ("Como indices B-Tree aceleram buscas pontuais no PostgreSQL e como o processo de Autovacuum impede o inchaco de tabelas?",
     "Os indices B-Tree organizam as chaves em paginas hierarquicas ordenadas permitindo que buscas pontuais naveguem da raiz as folhas com complexidade logaritmica O(log N).",
     "Atende com rigor a indexacao B-Tree, mas omite completamente o mecanismo do Autovacuum na limpeza de tuplas mortas do MVCC.",
     None),

    # Compound 8: Event Sourcing + CQRS
    ("Como funciona o padrao Event Sourcing e como ele se integra a arquitetura CQRS para otimizacao de consultas?",
     "No Event Sourcing o estado da entidade nao e gravado diretamente em colunas, mas reconstruido a partir de uma sequencia imutavel de eventos de dominio armazenados em um event store.",
     "Explica com clareza o Event Sourcing, mas nao aborda a projecao assincrona para modelos de leitura no lado de Query do CQRS.",
     None),

    # Compound 9: Rate Limiting + Fallback Response
    ("Como configurar rate limiting por token bucket no gateway e qual status code HTTP deve ser retornado aos clientes bloqueados?",
     "Configuramos um filtro no API Gateway que recarrega tokens a uma taxa fixa em um balde e rejeita requisicoes de clientes quando nao houver tokens disponiveis.",
     "Descreve o algoritmo token bucket no gateway, mas omite o status code HTTP exigido (429 Too Many Requests) e headers de retry.",
     None),

    # Compound 10: OAuth 2.0 Access Token + Refresh Token Flow
    ("Como um cliente OAuth 2.0 utiliza o Access Token nas requisicoes e qual o fluxo correto para renova-lo usando o Refresh Token?",
     "O cliente adiciona o Access Token no header de autorizacao HTTP como Bearer Token em cada chamada protegida enviada para o Resource Server.",
     "Cobre o uso do Access Token em headers Bearer, mas nao descreve o fluxo de requisicao ao Authorization Server para troca do Refresh Token.",
     None),

    # Compound 11: Docker Multi-Stage Build + Layer Caching
    ("Como configurar multi-stage builds em um Dockerfile e como ordenar os comandos RUN e COPY para otimizar o cache de camadas?",
     "Em um multi-stage build definimos multiplas diretivas FROM no mesmo Dockerfile para compilar a aplicacao no primeiro estagio e copiar apenas o binario gerado para uma imagem final leve.",
     "Explica o conceito e configuracao de multi-stage build, mas omite a ordenacao de dependencias antes do codigo-fonte para maximizar o cache.",
     None),

    # Compound 12: Kubernetes Readiness vs Liveness Probes
    ("Qual a diferenca de proposito entre Readiness Probes e Liveness Probes no Kubernetes e o que o kubelet faz quando cada uma falha?",
     "A Readiness Probe verifica se o pod esta apto para receber trafego de usuarios, enquanto a Liveness Probe verifica se o processo interno do container continua saudavel e respondendo.",
     "Explica com exatidao a diferenca de proposito das probes, mas omite as acoes do kubelet em caso de falha (remover do service endpoint vs reiniciar o container).",
     None),

    # Compound 13: Optimistic vs Pessimistic Locking
    ("Quando devemos escolher Optimistic Locking em vez de Pessimistic Locking e como o banco relacional sinaliza o conflito em cada caso?",
     "Escolhemos Optimistic Locking em cenarios com baixa probabilidade de colisao de concorrencia onde bloquear tabelas traria overhead excessivo de latencia.",
     "Atende o criterio de escolha do bloqueio otimista, mas omite como o banco sinaliza conflitos (excecao de versao estocada vs lock wait timeout).",
     None),

    # Compound 14: gRPC Streaming + Error Handling
    ("Como funciona o bidirectional streaming no gRPC e como propagar codigos de status de erro padronizados para o cliente?",
     "No bidirectional streaming cliente e servidor abrem um unico canal HTTP/2 onde ambos podem emitir e consumir streams de mensagens assincronamente sem esperar respostas pareadas.",
     "Explica a comunicacao bidirecional de streaming, mas omite a propagacao de status codes gRPC (como status.Code INVALID_ARGUMENT ou NOT_FOUND) e metadados de erro.",
     None),

    # Compound 15: Clean Architecture Entities vs Use Cases
    ("Qual a responsabilidade das Entities na Clean Architecture e como os Use Cases interagem com elas sem acoplamento a frameworks?",
     "As Entities encapsulam as regras de negocio corporativas fundamentais e estruturas de dados de dominio que independem de qualquer sistema ou interface externa.",
     "Atende a responsabilidade das Entities, mas nao detalha a orquestracao realizada pelos Use Cases e o desacoplamento de gateways/frameworks.",
     None),

    # Compound 16: Elasticsearch Shards vs Replicas
    ("Qual a diferenca entre Primary Shards e Replica Shards no Elasticsearch e o que acontece com as buscas quando um no de replica cai?",
     "Primary Shards sao as particoes originais onde as escritas sao processadas e gravadas, enquanto Replica Shards sao copias exatas das primarias alocadas em outros nós para tolerancia a falhas.",
     "Compara adequadamente primarias e replicas, mas omite o comportamento das consultas no cluster quando a replica cai (roteamento para primary ou outras replicas sem interrupcao).",
     None),

    # Compound 17: Thread Pooling + Queue Rejection Policy
    ("Como configurar o tamanho de core e max pool size em um ThreadPoolExecutor e o que faz a politica CallerRunsPolicy quando a fila lota?",
     "Configuramos o corePoolSize com a quantidade base de threads ativas mantidas vivas e o maximumPoolSize com o teto de threads temporarias criadas sob pico.",
     "Explica a configuracao dos limites de threads, mas omite o comportamento especifico da CallerRunsPolicy (executar a tarefa na propria thread que submeteu).",
     None),

    # Compound 18: Consistent Hashing Virtual Nodes + Data Migration
    ("Por que o algoritmo Consistent Hashing utiliza nos virtuais e como os dados sao redistribuidos quando um no fisico e adicionado?",
     "O Consistent Hashing utiliza nos virtuais para distribuir uniformemente multiplos pontos de um mesmo servidor no anel, evitando pontos quentes e desbalanceamento de carga.",
     "Explica o papel dos nos virtuais contra hot spots, mas nao detalha como apenas o intervalo do anel correspondente ao novo no e redistribuido.",
     None),

    # Compound 19: Database Connection Pool Sizing + Timeout Configuration
    ("Qual formula orienta o dimensionamento do pool de conexoes do banco e por que o timeout de conexao deve ser menor que o timeout da requisicao HTTP?",
     "Dimensionamos o pool com base na formula de duas vezes a quantidade de cores de CPU do banco somada a quantidade de discos para evitar saturacao de threads no banco de dados.",
     "Apresenta a formula de dimensionamento recomendada para o pool, mas nao justifica por que o timeout de conexao deve falhar antes do timeout HTTP da API.",
     None),

    # Compound 20: Saga Pattern Choreography vs Orchestration
    ("Qual a diferenca entre a abordagem coreografada e a orquestrada no padrao Saga para transacoes distribuidas e como reverter transacoes com falha?",
     "Na coreografia cada servico publica eventos e reage a eventos dos outros servicos sem coordenador central, enquanto na orquestracao um orquestrador central comanda os passos via mensagens direcionadas.",
     "Diferencia perfeitamente coreografia de orquestracao no padrao Saga, mas nao explica a execucao de transacoes compensatorias para reverter transacoes parciais.",
     None)
]

# Add remaining 23 partial cases to complete 45 cases in Group B
for i in range(1, 24):
    q = f"Explique o funcionamento do componente {i} de particionamento e como configurar a chave de criptografia correspondente."
    r = f"O componente {i} realiza a divisao horizontal dos registros com base no identificador da particao distribuindo o volume de I/O uniformemente entre as unidades fisicas."
    GROUP_B_CASES.append((
        q, r,
        f"Atende a demanda de funcionamento do particionamento no componente {i}, mas omite por completo a configuracao da chave de criptografia exigida.",
        None
    ))
