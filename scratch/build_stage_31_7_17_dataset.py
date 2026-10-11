"""
Script to build the 200-case independent blind semantic validation benchmark for Stage 31.7.17.
Ensures zero textual overlap with Stage 31.7.13 (250 cases) and tests.
Covers all 7 relevance classes, multi-aspect demands, morphological variations,
destructive antitheses, auxiliary monitoring, orthogonal domains, and representation invariance pairs.
"""

import json
import hashlib
from pathlib import Path

# Load Stage 31.7.13 historical benchmark to verify strict novelty
p_hist = "C:/Users/caiop/.gemini/antigravity-ide/brain/8baa1ac5-b48e-4706-9d0f-5c766d5d6bc4/scratch/stage_31_7_13_ground_truth.json"
hist_data = json.load(open(p_hist, encoding="utf-8"))
hist_questions = {c["question_text"].strip().lower() for c in hist_data}
hist_responses = {c["response_text"].strip().lower() for c in hist_data}

cases = []

def add_case(cid, group, q, r, ref, demands, satisfied, rationale, form="formal", epistemic="CONCEPTUAL", ambiguity=False):
    # Verify novelty
    q_norm = q.strip().lower()
    r_norm = r.strip().lower()
    assert q_norm not in hist_questions, f"Duplicate question in historical benchmark: {q}"
    assert r_norm not in hist_responses, f"Duplicate response in historical benchmark: {r}"
    
    cases.append({
        "id": cid,
        "group": group,
        "question_text": q.strip(),
        "response_text": r.strip(),
        "human_classification": ref,
        "demands": demands,
        "satisfied_aspects": satisfied,
        "semantic_rationale": rationale,
        "linguistic_form": form,
        "epistemic_status": epistemic,
        "adjudication_confidence": "HIGH",
        "has_ambiguity": ambiguity
    })

# =========================================================================
# GROUP 1: DIRECT (45 cases) — Full operative functional resolution
# Varied domains, active/passive/pronominal, novel tech, short/long
# =========================================================================

# 1.1 Concurrency & Distributed Systems (Direct)
add_case(
    "D01_vector_hnsw", "DIRECT_TECH",
    "Como o banco vetorial Milvus realiza buscas aproximadas de vizinhos mais próximos em larga escala?",
    "Constrói-se um grafo hierárquico navegável de mundo pequeno (HNSW), indexando os vetores em camadas com saltos longos nas camadas superiores e busca gulosa refinada nas camadas inferiores.",
    "DIRECT", ["busca aproximada de vizinhos mais próximos em larga escala"], ["grafo hierárquico navegável HNSW em camadas"],
    "Descreve detalhadamente o mecanismo algorítmico do grafo HNSW resolvendo a busca vetorial em larga escala.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D02_vector_hnsw_informal", "DIRECT_TECH",
    "Como o banco vetorial Milvus realiza buscas aproximadas de vizinhos mais próximos em larga escala?",
    "A gente monta uma malha de grafos em camadas estilo HNSW: você pula rápido pelas conexões distantes no topo e vai descendo até achar os vetores mais parecidos bem no fundo.",
    "DIRECT", ["busca aproximada de vizinhos mais próximos em larga escala"], ["malha de grafos HNSW em camadas"],
    "Expressão informal que descreve exatamente o mecanismo funcional de busca em camadas com HNSW.",
    form="informal", epistemic="CONCEPTUAL"
)
add_case(
    "D03_compaction_lsm", "DIRECT_TECH",
    "Como o RocksDB impede a explosão de arquivos e desaloca dados excluídos na arquitetura LSM-Tree?",
    "Executa-se compactação leveled em segundo plano, mesclando ordenadamente SSTables de níveis menores para níveis maiores e descartando registros marcados com marcadores de deleção (tombstones).",
    "DIRECT", ["impedir explosão de arquivos e desalocar dados excluídos"], ["compactação leveled com mesclagem e tombstones"],
    "Explica o processo de compactação leveled e o uso de tombstones para expurgar registros.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D04_compaction_lsm_active", "DIRECT_TECH",
    "Como o RocksDB impede a explosão de arquivos e desaloca dados excluídos na arquitetura LSM-Tree?",
    "Eu configuro a compactação leveled para rodar em background, consolidando os arquivos SSTable entre os níveis e eliminando as chaves que possuem tombstones.",
    "DIRECT", ["impedir explosão de arquivos e desalocar dados excluídos"], ["compactação leveled e tombstones"],
    "Formulação ativa em 1ª pessoa descrevendo a mesma mecânica operacional de compactação e tombstones.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "D05_raft_log_matching", "DIRECT_TECH",
    "Como o protocolo Raft assegura que entradas de log confirmadas nunca sejam sobrescritas por um novo líder?",
    "A eleição de líder só elege nós com log estritamente mais atualizado que a maioria, e novos líderes nunca truncam entradas já comitadas pelo quórum anterior.",
    "DIRECT", ["assegurar que entradas comitadas nunca sejam sobrescritas"], ["restrição de eleição baseada no quórum e invariância de log"],
    "Aborda a propriedade de Log Matching e a restrição de eleição garantindo consistência no Raft.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "D06_raft_log_matching_short", "DIRECT_TECH",
    "Como o protocolo Raft assegura que entradas de log confirmadas nunca sejam sobrescritas por um novo líder?",
    "Exigindo que o novo líder contenha todas as entradas comitadas da maioria antes de receber votos para assumir.",
    "DIRECT", ["assegurar que entradas comitadas nunca sejam sobrescritas"], ["exigência de log comitado majoritário na eleição"],
    "Resposta concisa direta que atende perfeitamente ao requisito essencial de consenso do Raft.",
    form="concise", epistemic="CONCEPTUAL"
)
add_case(
    "D07_distributed_lock_fencing", "DIRECT_TECH",
    "Como evitar que um cliente pausado por Stop-the-World cause corrupção de dados ao despertar e gravar no storage?",
    "Utiliza-se um fencing token monotônico gerado pelo coordenador de locks, de forma que o storage rejeite qualquer gravação cujo token seja inferior ao último aceito.",
    "DIRECT", ["evitar corrupção por cliente pausado após perda de lock"], ["fencing token monotônico validado no storage"],
    "Explica a solução canônica de fencing tokens monotônicos para clientes pausados por GC.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D08_distributed_lock_fencing_informal", "DIRECT_TECH",
    "Como evitar que um cliente pausado por Stop-the-World cause corrupção de dados ao despertar e gravar no storage?",
    "A gente associa um número sequencial crescente que o lock entrega; se a thread congelar e acordar atrasada, o banco vê que o número dela é velho e barra o comando na porta.",
    "DIRECT", ["evitar corrupção por cliente pausado após perda de lock"], ["número sequencial crescente validado no banco"],
    "Paráfrase informal correta e funcional do conceito de fencing token.",
    form="informal", epistemic="CONCEPTUAL"
)
add_case(
    "D09_kafka_zero_copy", "DIRECT_TECH",
    "Como o broker do Kafka atinge taxa massiva de transferência na leitura de tópicos para a rede?",
    "Emprega-se a chamada de sistema sendfile (Zero-Copy), transferindo blocos do page cache do sistema operacional diretamente para o buffer da placa de rede sem copiar para o espaço de usuário.",
    "DIRECT", ["atingir taxa massiva de transferência de leitura para rede"], ["chamada sendfile zero-copy do page cache para socket"],
    "Explica o mecanismo de Zero-Copy via sendfile da Linux VFS para o socket.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D10_kafka_zero_copy_active", "DIRECT_TECH",
    "Como o broker do Kafka atinge taxa massiva de transferência na leitura de tópicos para a rede?",
    "O Kafka utiliza o recurso de zero-copy através da syscall sendfile, direcionando os dados do pagecache direto para a interface de rede sem passar pela memória da JVM.",
    "DIRECT", ["atingir taxa massiva de transferência de leitura para rede"], ["syscall sendfile do pagecache para rede sem JVM"],
    "Voz ativa em 3ª pessoa descrevendo com exatidão a redução de contexto de memória.",
    form="active_3rd", epistemic="CONCEPTUAL"
)
add_case(
    "D11_crdt_pn_counter", "DIRECT_TECH",
    "Como sincronizar um contador distribuído com incrementos e decrementos sem usar travas globais?",
    "Modela-se o estado como um PN-Counter (CRDT), mantendo dois vetores monotônicos de soma para adições e subtrações e calculando a diferença entre as somas parciais por fusão de estados.",
    "DIRECT", ["sincronizar contador com adições e subtrações sem travas"], ["PN-Counter CRDT com dois vetores monotônicos de soma"],
    "Descreve a estrutura matemática e funcional de um PN-Counter convergente.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D12_crdt_pn_counter_informal", "DIRECT_TECH",
    "Como sincronizar um contador distribuído com incrementos e decrementos sem usar travas globais?",
    "A gente cria duas listas que só crescem: uma que soma todas as entradas e outra que soma todas as saídas de cada máquina, depois junta tudo fazendo o total de uma menos a outra.",
    "DIRECT", ["sincronizar contador com adições e subtrações sem travas"], ["listas monotônicas de entrada e saída com diferença"],
    "Explicação conceitual informal de um PN-Counter sem termos em inglês, perfeitamente válida.",
    form="informal", epistemic="CONCEPTUAL"
)
add_case(
    "D13_database_sharding_virtual_nodes", "DIRECT_TECH",
    "Como evitar hot spots de tráfego em partições ao adicionar novos servidores a um anel distribuído?",
    "Atribui-se múltiplos nós virtuais para cada servidor físico ao longo do espaço de hash, espalhando uniformemente os intervalos do anel e equilibrando a redistribuição de chaves.",
    "DIRECT", ["evitar hot spots de tráfego ao adicionar servidores"], ["nós virtuais por servidor físico no anel de hash"],
    "Mecanismo de nós virtuais em consistent hashing para distribuição uniforme de carga.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D14_database_sharding_virtual_nodes_active", "DIRECT_TECH",
    "Como evitar hot spots de tráfego em partições ao adicionar novos servidores a um anel distribuído?",
    "Eu crio nós virtuais para cada nó físico no consistent hashing, garantindo que a carga seja fatiada em centenas de posições aleatórias no anel.",
    "DIRECT", ["evitar hot spots de tráfego ao adicionar servidores"], ["nós virtuais no consistent hashing"],
    "Formulação ativa direta explicando o mesmo mecanismo de dispersão estatística.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "D15_outbox_debezium_cdc", "DIRECT_TECH",
    "Como publicar eventos garantindo que uma transação de banco de dados e a emissão da mensagem sejam atômicas?",
    "Grava-se o evento em uma tabela de outbox na mesma transação relacional dos dados e captura-se a alteração assincronamente via Change Data Capture (CDC) lendo o log binário do banco.",
    "DIRECT", ["publicar eventos com atomicidade entre banco e mensageria"], ["tabela outbox na transação local e CDC lendo log binário"],
    "Descreve o Transactional Outbox Pattern com integração CDC lendo WAL.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D16_outbox_debezium_cdc_informal", "DIRECT_TECH",
    "Como publicar eventos garantindo que uma transação de banco de dados e a emissão da mensagem sejam atômicas?",
    "Você salva o evento numa tabelinha auxiliar junto com os dados na mesma transação com begin/commit, e coloca um conector ouvindo o log do banco pra mandar a mensagem pro Kafka.",
    "DIRECT", ["publicar eventos com atomicidade entre banco e mensageria"], ["tabela auxiliar na transação com begin/commit e conector no log"],
    "Paráfrase informal correta do Transactional Outbox Pattern.",
    form="informal", epistemic="CONCEPTUAL"
)
add_case(
    "D17_saga_choreography_compensating", "DIRECT_TECH",
    "Como desfazer operações parciais em múltiplos serviços autônomos sem usar transações distribuídas de duas fases?",
    "Implementa-se o padrão Saga coreografado onde a falha de uma etapa dispara eventos de compensação que executam estornos lógicos nos serviços participantes.",
    "DIRECT", ["desfazer operações parciais em múltiplos serviços sem 2PC"], ["padrão Saga com eventos de compensação e estorno lógico"],
    "Explica o funcionamento de Sagas com transações de compensação sem locks globais.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D18_saga_choreography_compensating_short", "DIRECT_TECH",
    "Como desfazer operações parciais em múltiplos serviços autônomos sem usar transações distribuídas de duas fases?",
    "Disparando transações compensatórias em cascata para estornar as etapas executadas anteriormente.",
    "DIRECT", ["desfazer operações parciais em múltiplos serviços sem 2PC"], ["transações compensatórias em cascata"],
    "Resposta curta direta e suficiente.",
    form="concise", epistemic="CONCEPTUAL"
)
add_case(
    "D19_tls_session_resumption", "DIRECT_TECH",
    "Como reduzir a latência de handshake em conexões HTTPS recorrentes para o mesmo cliente?",
    "Utiliza-se Session Tickets (TLS Resumption), onde o servidor emite um tíquete criptografado que o cliente reenvia para restabelecer a chave simétrica em uma única viagem de ida e volta (1-RTT).",
    "DIRECT", ["reduzir latência de handshake HTTPS recorrente"], ["TLS Session Tickets criptografados em 1-RTT"],
    "Explica TLS Session Tickets com restabelecimento de chave em 1-RTT.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D20_rate_limiting_sliding_window", "DIRECT_TECH",
    "Como aplicar limitação de taxa em APIs evitando o problema de rajada concentrada na virada de janela?",
    "Implementa-se o algoritmo de janela deslizante (Sliding Window Log ou Counter), ponderando a contagem de requisições da janela anterior pela fração de tempo transcorrido no minuto atual.",
    "DIRECT", ["limitação de taxa evitando rajadas na virada de janela"], ["algoritmo de janela deslizante com ponderação temporal"],
    "Explica Sliding Window com ponderação temporal entre janelas consecutivas.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D21_grpc_bidirectional_streaming", "DIRECT_TECH",
    "Como manter comunicação contínua e assíncrona de dados estruturados em tempo real entre dois microsserviços?",
    "Adota-se gRPC com streaming bidirecional sobre HTTP/2, multiplexando múltiplos canais de requisições e respostas sobre a mesma conexão TCP persistente com serialização Protobuf.",
    "DIRECT", ["comunicação contínua e assíncrona em tempo real entre microsserviços"], ["gRPC streaming bidirecional sobre HTTP/2 com multiplexação e Protobuf"],
    "Descreve gRPC bidirecional com HTTP/2 e Protobuf.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D22_epoll_event_loop", "DIRECT_TECH",
    "Como servidores de rede de alta performance conseguem atender dezenas de milhares de conexões simultâneas com poucas threads?",
    "Utiliza-se multiplexação de I/O não bloqueante via epoll (ou kqueue), registrando os descritores de socket em um loop de eventos que só acorda as threads quando ocorrem notificações prontas para leitura ou escrita.",
    "DIRECT", ["atender dezenas de milhares de conexões simultâneas com poucas threads"], ["I/O não bloqueante com epoll e event loop baseado em notificações"],
    "Explica multiplexação com epoll e event-driven I/O.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D23_memory_pool_fragmentation", "DIRECT_TECH",
    "Como evitar fragmentação de memória e pausas imprevisíveis em sistemas de negociação financeira de baixa latência?",
    "Aloca-se previamente buffers contíguos de tamanho fixo em pools de objetos na inicialização da aplicação, reaproveitando as estruturas sem solicitar memória do sistema operacional em tempo de execução.",
    "DIRECT", ["evitar fragmentação de memória e pausas imprevisíveis em baixa latência"], ["buffers contíguos em pools de objetos de tamanho fixo pré-alocados"],
    "Explica memory pools contíguos e reaproveitamento de objetos para zero-allocation runtime.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D24_circuit_breaker_half_open", "DIRECT_TECH",
    "Como um circuit breaker determina com segurança se um microsserviço com falhas se recuperou antes de liberar todo o tráfego?",
    "Transita-se para o estado meio-aberto (half-open) após um período de repouso, permitindo a passagem de uma quantidade restrita de requisições de teste e fechando o circuito apenas se a taxa de sucesso for total.",
    "DIRECT", ["determinar com segurança recuperação de microsserviço antes de liberar tráfego"], ["estado meio-aberto half-open com requisições de teste limitadas"],
    "Explica o estado half-open e a transição gradual com amostras de teste.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D25_wal_checkpoint_truncate", "DIRECT_TECH",
    "Como os motores de banco de dados impedem o crescimento infinito do log de escrita sequencial (WAL)?",
    "Realizam-se checkpoints periódicos sincronizando todas as páginas sujas da memória para os arquivos de dados em disco e truncando os segmentos do WAL anteriores ao ponto de verificação.",
    "DIRECT", ["impedir crescimento infinito do WAL"], ["checkpoints periódicos sincronizando páginas sujas e truncando segmentos"],
    "Explica checkpoints periódicos e expurgo de logs anteriores ao flush.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D26_deadlock_detection_cycle", "DIRECT_TECH",
    "Como um banco de dados relacional detecta e resolve travamentos mútuos entre transações concorrentes?",
    "O motor constrói um grafo de espera direcionado (wait-for graph), identifica ciclos de dependência circular entre as transações e aborta a transação de menor custo computacional executando rollback.",
    "DIRECT", ["detectar e resolver travamentos mútuos concorrentes"], ["grafo de espera com detecção de ciclos e rollback da transação de menor custo"],
    "Mecanismo completo de wait-for graph, cycle detection e rollback de vítima.",
    form="active_3rd", epistemic="CONCEPTUAL"
)
add_case(
    "D27_optimistic_locking_version_check", "DIRECT_TECH",
    "Como garantir que duas alterações simultâneas no mesmo saldo não causem perda de atualizações?",
    "Inclui-se um número de versão no registro e executa-se o update com a condição de que a versão na tabela seja idêntica à versão lida, incrementando a versão ou abortando caso nenhuma linha seja afetada.",
    "DIRECT", ["garantir que alterações simultâneas não causem perda de atualizações"], ["coluna de versão com condição no update e incremento ou abort"],
    "Explicação técnica completa de optimistic locking com cláusula WHERE version = v.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D28_consistent_hashing_ring_walk", "DIRECT_TECH",
    "Como mapear chaves para servidores de armazenamento minimizando o número de chaves realocadas ao redimensionar nós?",
    "Mapeia-se as chaves e os nós em um anel circular de 0 a 2^32-1, onde cada chave é armazenada no primeiro nó encontrado ao percorrer o anel em sentido horário a partir da sua posição de hash.",
    "DIRECT", ["mapear chaves minimizando realocações ao redimensionar nós"], ["anel circular de hash percorrido em sentido horário para o primeiro nó"],
    "Explica hashing consistente e o anel percorrido em sentido horário.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D29_token_bucket_refill_rate", "DIRECT_TECH",
    "Como controlar vazão de requisições aceitando surtos pontuais sem sobrecarregar a capacidade da infraestrutura?",
    "Emprega-se um balde de fichas (token bucket) que acumula tokens em uma taxa fixa de reposição até o limite do balde, consumindo um token por requisição e rejeitando chegadas quando o balde estiver vazio.",
    "DIRECT", ["controlar vazão aceitando surtos pontuais sem sobrecarregar"], ["token bucket acumulando fichas em taxa fixa até limite e rejeitando sem tokens"],
    "Descreve o algoritmo de balde de fichas acomodando rajadas.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D30_bloom_filter_bit_array", "DIRECT_TECH",
    "Como evitar operações caras de leitura em disco para verificar se uma chave inexiste em arquivos de armazenamento?",
    "Consulta-se um filtro de Bloom em memória RAM contendo um vetor de bits calculado por múltiplas funções hash; se qualquer bit correspondente for zero, tem-se a garantia matemática de que a chave não existe no disco.",
    "DIRECT", ["evitar leituras caras em disco para chaves inexistentes"], ["filtro de Bloom em RAM com vetor de bits e múltiplas funções hash"],
    "Explica o filtro de Bloom em RAM garantindo ausência de falsos negativos.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D31_read_repair_quorum", "DIRECT_TECH",
    "Como bancos NoSQL distribuídos corrigem divergências silenciosas entre réplicas durante consultas comuns de clientes?",
    "Aplica-se Read Repair: quando o cliente consulta com quórum e recebe hashes de versão divergentes entre as réplicas, o nó coordenador detecta a versão mais recente e atualiza assincronamente as réplicas desatualizadas.",
    "DIRECT", ["corrigir divergências silenciosas entre réplicas durante consultas"], ["Read Repair com quórum identificando versão recente e atualizando réplicas defasadas"],
    "Descreve o mecanismo de Read Repair em Cassandra/Dynamo.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D32_gossip_protocol_failure_detector", "DIRECT_TECH",
    "Como os nós de um cluster descentralizado detectam falhas de servidores sem depender de um mestre centralizador?",
    "Utiliza-se o protocolo de fofoca (Gossip Protocol) com detector de falhas Phi Accural, enviando heartbeats periódicos aleatórios entre nós e calculando a probabilidade de falha com base no histórico de intervalos de chegada.",
    "DIRECT", ["detectar falhas sem mestre centralizador"], ["Gossip protocol com detector Phi Accrual e heartbeats periódicos aleatórios"],
    "Explica Gossip com Phi Accrual Failure Detector descentralizado.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D33_write_behind_caching", "DIRECT_TECH",
    "Como desonerar o banco relacional de picos extremos de escrita em rotinas de contabilidade?",
    "Adota-se write-behind caching (write-back), confirmando as alterações instantaneamente na camada de cache em memória e persistindo-as em lote no banco relacional de forma assíncrona por meio de um processo em fila.",
    "DIRECT", ["desonerar banco relacional de picos de escrita"], ["write-behind caching confirmando em memória e persistindo em lote assíncrono"],
    "Explica o padrão de write-behind para agregação de escritas em lote.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D34_idempotent_consumer_database_dedup", "DIRECT_TECH",
    "Como evitar duplicidade ao processar eventos de pagamento entregues mais de uma vez por um broker at-least-once?",
    "Registra-se a chave de idempotência do evento em uma tabela com restrição de unicidade (unique constraint) antes de processar a cobrança, descartando a mensagem caso ocorra colisão de chave duplicada.",
    "DIRECT", ["evitar duplicidade ao processar eventos at-least-once"], ["tabela com unique constraint na chave de idempotência descartando colisões"],
    "Explica idempotência estrita com restrição de unicidade transacional.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D35_vector_quantization_ivf_pq", "DIRECT_TECH",
    "Como comprimir vetores em bancos vetoriais de larga escala sem esgotar a memória RAM disponível?",
    "Aplica-se quantização de produto (Product Quantization com índice IVF-PQ), decompondo os vetores em sub-espaços menores e substituindo cada vetor por centróides representados por códigos de 8 bits.",
    "DIRECT", ["comprimir vetores em larga escala sem esgotar memória RAM"], ["Product Quantization IVF-PQ decompondo em sub-espaços e centróides de 8 bits"],
    "Descreve Product Quantization para compressão e busca em memória vetorial.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D36_two_phase_commit_coordinator", "DIRECT_TECH",
    "Como garantir atomicidade rigorosa quando uma transação altera simultaneamente dados em dois bancos independentes?",
    "Executa-se o protocolo Two-Phase Commit (2PC): o coordenador envia a mensagem prepare solicitando que os nós travem recursos e confirmem prontidão, e somente envia commit final se todas as réplicas votarem afirmativamente.",
    "DIRECT", ["garantir atomicidade entre dois bancos independentes"], ["protocolo 2PC com fase prepare de travamento e fase commit sob consenso unânime"],
    "Explica a mecânica de 2PC com coordenador, fases de prepare e commit.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D37_database_partition_pruning", "DIRECT_TECH",
    "Como o otimizador de consultas de banco de dados reduz o volume de blocos lidos em tabelas particionadas por data?",
    "Aplica-se poda de partição (Partition Pruning), analisando os predicados de filtro da cláusula WHERE na compilação da query para ignorar completamente os índices e diretórios das partições fora do intervalo solicitado.",
    "DIRECT", ["reduzir blocos lidos em tabelas particionadas por data"], ["Partition Pruning analisando WHERE para ignorar partições fora do intervalo"],
    "Descreve Partition Pruning estático e dinâmico.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D38_lock_striping_concurrency", "DIRECT_TECH",
    "Como diminuir contenção de bloqueios em estruturas de dados compartilhadas acessadas por dezenas de threads simultâneas?",
    "Emprega-se segmentação de travas (Lock Striping), distribuindo o acesso sobre um arranjo de múltiplos locks independentes onde cada chave ou bucket da coleção adquire apenas a trava associada ao seu hash.",
    "DIRECT", ["diminuir contenção de bloqueios em estruturas compartilhadas"], ["Lock Striping distribuindo chaves sobre arranjo de locks independentes por hash"],
    "Descreve Lock Striping (técnica de ConcurrentHashMap).",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D39_btree_prefix_compression", "DIRECT_TECH",
    "Como diminuir o espaço ocupado por índices em colunas de strings longas sem degradar o tempo de busca?",
    "Aplica-se compressão de prefixo nas páginas da árvore B, armazenando o prefixo comum dos registros uma única vez no cabeçalho da página e gravando apenas os sufixos diferenciadores em cada nó folha.",
    "DIRECT", ["diminuir espaço de índices de strings sem degradar busca"], ["compressão de prefixo armazenando prefixo comum no cabeçalho e gravando sufixos"],
    "Explica compressão de prefixo em blocos de B-Tree.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D40_read_committed_snapshot_isolation", "DIRECT_TECH",
    "Como permitir leituras concorrentes em tabelas sem bloquear transações de escrita e sem ler dados sujos?",
    "Habilita-se Snapshot Isolation (RCSI) via controle de concorrência multiversão (MVCC), permitindo que consultas leiam a última versão confirmada no histórico de linhas antes do início do comando.",
    "DIRECT", ["permitir leituras sem bloquear escrita e sem ler dados sujos"], ["Snapshot Isolation via MVCC lendo última versão confirmada no histórico"],
    "Explica Snapshot Isolation e MVCC.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D41_unseen_technology_supergraph", "DIRECT_TECH",
    "Como a tecnologia fictícia ChronoSync preserva a consistência de estado entre réplicas móveis desconectadas?",
    "Ela calcula vetores de relógio de Lamport em cada mutação offline e executa uma mesclagem de três vias baseada em árvores de Merkle assim que a conexão de rede é restabelecida.",
    "DIRECT", ["preservar consistência entre réplicas móveis desconectadas"], ["vetores de Lamport offline e mesclagem de três vias com árvores de Merkle"],
    "Tecnologia fictícia com mecanismo técnico perfeitamente articulado e direto.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "D42_unseen_technology_nanoshard", "DIRECT_TECH",
    "Como a ferramenta emergente FlowPlex gerencia o escalonamento horizontal de pipelines de agregação em tempo real?",
    "Mapeia-se as mensagens em micro-partições dinâmicas na memória e reatribui-se os workers utilizando tabelas de dispersão distribuídas quando a taxa de chegada ultrapassa o limiar de consumo.",
    "DIRECT", ["gerenciar escalonamento horizontal de agregação em tempo real"], ["micro-partições dinâmicas em memória com reatribuição de workers por dispersão"],
    "Tecnologia emergente com mecanismo operacional direto.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "D43_long_direct_detailed", "DIRECT_TECH",
    "Como evitar esgotamento de conexões JDBC em microsserviços de alto tráfego sob concorrência intensa?",
    "Configura-se um pool de conexões otimizado como HikariCP definindo tamanho máximo estrito compatível com os núcleos do banco, ativando timeout de aquisição de 2 segundos para falhar rápido e garantindo que todas as transações fechem os recursos em blocos try-with-resources imediatamente após a execução da query.",
    "DIRECT", ["evitar esgotamento de conexões JDBC sob alta concorrência"], ["pool HikariCP dimensionado aos núcleos, timeout de aquisição e try-with-resources"],
    "Explicação longa e abrangente que atende com precisão cirúrgica à demanda operacional.",
    form="verbose", epistemic="CONCEPTUAL"
)
add_case(
    "D44_short_direct_concise", "DIRECT_TECH",
    "Como isolar a execução de código não confiável em funções serverless de borda (edge computing)?",
    "Executando as funções dentro de WebAssembly sandboxes isoladas com restrição rigorosa de acesso a memória e chamadas de sistema.",
    "DIRECT", ["isolar execução de código não confiável em edge computing"], ["WebAssembly sandboxes isoladas com restrição de memória e syscalls"],
    "Resposta concisa e direta que resolve exatamente a demanda de isolamento.",
    form="concise", epistemic="CONCEPTUAL"
)
add_case(
    "D45_active_1st_direct_experience", "DIRECT_TECH",
    "Como resolver problemas de lock exclusivo prolongado provocado por comandos de criação de índices em bancos de produção?",
    "Eu executo a criação do índice utilizando a cláusula CONCURRENTLY do PostgreSQL, permitindo que as consultas e escritas continuem operando normalmente enquanto o banco constrói o índice em duas passagens sequenciais.",
    "DIRECT", ["resolver lock exclusivo por criação de índices em produção"], ["CREATE INDEX CONCURRENTLY permitindo operações contínuas em duas passagens"],
    "Experiência demonstrada em 1ª pessoa com mecanismo exato e adequado.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)

# =========================================================================
# GROUP 2: PARTIAL (35 cases) — Partial aspect satisfaction, omissions
# Multi-aspect questions with unaddressed demands, explicit omissions
# =========================================================================

add_case(
    "P01_multi_aspect_omit_jitter", "PARTIAL_COVERAGE",
    "Como implementar retries com backoff exponencial e como adicionar jitter para prevenir o problema de thundering herd?",
    "Implementa-se uma rotina de retentativa que multiplica o tempo de espera por dois a cada falha consecutiva até atingir o tempo máximo pré-determinado.",
    "PARTIAL", ["implementar retries com backoff exponencial", "adicionar jitter para prevenir thundering herd"],
    ["implementar retries com backoff exponencial"],
    "Apresenta o backoff exponencial de forma correta, mas omite completamente o mecanismo de jitter e thundering herd.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "P02_multi_aspect_omit_rebalance", "PARTIAL_COVERAGE",
    "Como escolher a chave de sharding e como rebalancear as partições quando ocorre crescimento desbalanceado de dados?",
    "Seleciona-se uma chave de partição com alta cardinalidade para espalhar uniformemente os registros entre os servidores do cluster.",
    "PARTIAL", ["escolher chave de sharding", "rebalancear partições sob crescimento desbalanceado"],
    ["escolher chave de sharding"],
    "Responde com precisão à escolha da chave, porém não aborda o rebalanceamento de partições.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "P03_compare_jwt_session_omit_revocation", "PARTIAL_COVERAGE",
    "Compare autenticação stateless via JWT e stateful via sessão quanto a escalabilidade horizontal e facilidade de revogação de acessos.",
    "O JWT permite escalabilidade horizontal imediata porque os nós da aplicação não precisam consultar armazenamento compartilhado para checar credenciais.",
    "PARTIAL", ["comparar JWT e sessão em escalabilidade horizontal", "comparar facilidade de revogação de acessos"],
    ["comparar JWT em escalabilidade horizontal"],
    "Cobre a escalabilidade do JWT, mas não compara a facilidade de revogação de sessão.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P04_compare_b_tree_lsm_omit_writes", "PARTIAL_COVERAGE",
    "Compare árvores B-Tree e LSM-Tree quanto a velocidade de leitura pontual e vazão de escrita em lote.",
    "As árvores B-Tree possuem excelente desempenho em leituras pontuais aleatórias porque mantêm as páginas balanceadas e ordenadas em disco com saltos determinísticos.",
    "PARTIAL", ["velocidade de leitura pontual B-Tree vs LSM", "vazão de escrita em lote B-Tree vs LSM"],
    ["velocidade de leitura pontual B-Tree"],
    "Cobre as leituras em B-Tree, mas omite a vazão de escritas massivas em LSM-Tree.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P05_explicit_omission_text", "PARTIAL_COVERAGE",
    "Como o algoritmo Raft conduz a eleição de um líder e como sincroniza os logs com os seguidores?",
    "Ele elege o líder por meio de votação por maioria simples de quórum com timeouts aleatórios, mas não detalha como as entradas de log são transmitidas e replicadas aos seguidores.",
    "PARTIAL", ["eleição de líder no Raft", "sincronização de logs com seguidores"],
    ["eleição de líder no Raft"],
    "A própria resposta declara expressamente que não detalha a sincronização dos logs.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P06_explicit_omission_text_informal", "PARTIAL_COVERAGE",
    "Como configurar replicação síncrona no PostgreSQL e como gerenciar o failover automático do primário?",
    "A gente configura synchronous_commit para forçar gravação nas réplicas, porém não explica como configurar o script de failover nem o orquestrador que promove a máquina secundária.",
    "PARTIAL", ["configurar replicação síncrona", "gerenciar failover automático"],
    ["configurar replicação síncrona"],
    "Contém marcador explícito de omissão ('porém não explica como configurar o script de failover').",
    form="informal", epistemic="CONCEPTUAL"
)
add_case(
    "P07_compare_sync_async_omit_burst", "PARTIAL_COVERAGE",
    "Quais as diferenças entre chamadas síncronas HTTP e comunicação assíncrona por mensageria quanto a acoplamento temporal e resiliência a picos?",
    "No modelo síncrono HTTP o remetente fica bloqueado aguardando o processamento do destinatário, enquanto na mensageria assíncrona o remetente despacha a mensagem e continua seu fluxo desacoplado no tempo.",
    "PARTIAL", ["acoplamento temporal HTTP vs mensageria", "resiliência a picos de tráfego"],
    ["acoplamento temporal HTTP vs mensageria"],
    "Analisa exaustivamente o acoplamento temporal, mas omite a absorção de picos de tráfego (buffering).",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P08_compare_optimistic_pessimistic_omit_threads", "PARTIAL_COVERAGE",
    "Em que cenários deve-se optar por bloqueio pessimista e em quais por controle otimista, e qual o impacto em contenção de threads?",
    "Usa-se bloqueio pessimista quando a probabilidade de colisão é alta e lock otimista quando colisões são raras.",
    "PARTIAL", ["cenários para bloqueio pessimista vs otimista", "impacto em contenção de threads"],
    ["cenários para bloqueio pessimista vs otimista"],
    "Identifica os cenários de uso, mas não analisa o impacto na contenção e enfileiramento de threads no pool.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P09_compare_protobuf_json_omit_cpu", "PARTIAL_COVERAGE",
    "Compare a serialização de mensagens via Protocol Buffers binário e JSON textual quanto a consumo de banda de rede e sobrecarga de parsing de CPU.",
    "O Protobuf reduz drasticamente o tráfego de rede gerando cargas binárias compactas codificadas em varints, exigindo muito menos bytes trafegados por mensagem.",
    "PARTIAL", ["consumo de banda Protobuf vs JSON", "sobrecarga de parsing de CPU"],
    ["consumo de banda de rede com Protobuf"],
    "Explica a economia de banda de rede com Protobuf, mas omite a análise da sobrecarga de parsing de CPU entre formatos.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P10_compare_modular_monolith_microservices_omit_sagas", "PARTIAL_COVERAGE",
    "Compare arquiteturas monolíticas modulares e microsserviços distribuídos quanto a fronteiras transacionais no banco de dados e overhead de latência de rede entre domínios.",
    "Monólitos modulares executam operações entre domínios dentro de um mesmo processo compartilhando transações ACID locais no banco, eliminando a sobrecarga de round-trips de rede entre serviços.",
    "PARTIAL", ["fronteiras transacionais monólito vs microsserviços", "overhead de latência de rede entre domínios"],
    ["fronteiras transacionais locais e eliminação de overhead no monólito"],
    "Explica a transacionalidade local do monólito modular, mas não aprofunda o impacto de transações distribuídas e latência em microsserviços.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P11_multi_aspect_idempotency_storage", "PARTIAL_COVERAGE",
    "Como projetar endpoints de pagamento garantindo idempotência e como armazenar os comprovantes com expiração?",
    "Gera-se um hash único da transação financeira na chegada e valida-se se a cobrança já foi confirmada anteriormente.",
    "PARTIAL", ["garantir idempotência em pagamento", "armazenar comprovantes com expiração"],
    ["garantir idempotência em pagamento"],
    "Aborda a geração de hash de idempotência, mas omite o armazenamento com TTL/expiração de comprovantes.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "P12_multi_aspect_idempotency_storage_informal", "PARTIAL_COVERAGE",
    "Como projetar endpoints de pagamento garantindo idempotência e como armazenar os comprovantes com expiração?",
    "Eu coloco uma chave única no payload da requisição para barrar se o cliente tentar cobrar duas vezes a mesma conta.",
    "PARTIAL", ["garantir idempotência em pagamento", "armazenar comprovantes com expiração"],
    ["garantir idempotência em pagamento"],
    "Atende à primeira demanda de forma informal, mas ignora a expiração do comprovante.",
    form="informal", epistemic="CONCEPTUAL"
)
add_case(
    "P13_event_sourcing_cqrs_omit_projections", "PARTIAL_COVERAGE",
    "Em arquiteturas orientadas a eventos, compare os padrões Event Sourcing e CQRS quanto a rastreabilidade histórica de mutações e complexidade de projeção de visões de leitura.",
    "O Event Sourcing garante rastreabilidade temporal absoluta registrando cada mutação como um evento imutável em um log sequencial de append-only.",
    "PARTIAL", ["rastreabilidade histórica em Event Sourcing", "complexidade de projeção em CQRS"],
    ["rastreabilidade temporal absoluta no Event Sourcing"],
    "Cobre a rastreabilidade via log append-only do Event Sourcing, mas omite as projeções de leitura e sincronização assíncrona do CQRS.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P14_cache_aside_omit_invalidation", "PARTIAL_COVERAGE",
    "Como implementar a estratégia Cache-Aside e como lidar com a invalidação de dados desatualizados?",
    "A aplicação primeiro consulta o cache em memória; se houver miss, busca o registro no banco de dados e salva o resultado no cache antes de responder.",
    "PARTIAL", ["implementar fluxo Cache-Aside", "invalidação de dados desatualizados"],
    ["implementar fluxo Cache-Aside"],
    "Descreve perfeitamente o fluxo de leitura Cache-Aside, mas não explica a estratégia de invalidação na escrita.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P15_two_phase_commit_omit_failure", "PARTIAL_COVERAGE",
    "Como opera o protocolo Two-Phase Commit e como o sistema se recupera caso o coordenador falhe durante a fase de commit?",
    "O coordenador envia a ordem de prepare para todas as réplicas participantes e, recebendo aprovação unânime, despacha a ordem de commit definitivo.",
    "PARTIAL", ["operação do Two-Phase Commit", "recuperação sob falha do coordenador em commit"],
    ["operação do Two-Phase Commit"],
    "Explica o caminho feliz de 2PC, mas omite a resolução de bloqueio quando o coordenador cai.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P16_cqrs_omit_eventual_consistency", "PARTIAL_COVERAGE",
    "Como estruturar uma arquitetura CQRS separando comandos de consultas e como lidar com o delay de consistência eventual na interface?",
    "Separa-se o modelo de escrita com comandos que alteram o estado em tabelas transacionais e projeta-se tabelas desnormalizadas em views para atender as leituras com alta velocidade.",
    "PARTIAL", ["estruturar arquitetura CQRS", "lidar com delay de consistência eventual na UI"],
    ["estruturar arquitetura CQRS"],
    "Explica a separação de modelos em CQRS, mas ignora a mitigação do delay de leitura na interface.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "P17_kafka_partitions_omit_rebalance", "PARTIAL_COVERAGE",
    "Como particionar tópicos no Kafka para permitir processamento paralelo e como tratar rebalanceamentos sem travar os consumidores?",
    "Configura-se múltiplas partições no tópico distribuindo as mensagens por hash da chave de negócio, permitindo que cada consumidor do grupo processe sua partição concorrentemente.",
    "PARTIAL", ["particionar tópicos para processamento paralelo", "tratar rebalanceamentos sem travamentos"],
    ["particionar tópicos para processamento paralelo"],
    "Explica o paralelismo por partição, mas omite o tratamento de rebalanceamento (Cooperative Sticky Assignor).",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "P18_deadlock_detection_omit_victim_selection", "PARTIAL_COVERAGE",
    "Como os bancos relacionais identificam ciclos de deadlocks e qual o critério utilizado para selecionar a transação que sofrerá rollback?",
    "O banco de dados inspeciona as dependências de locks ativos montando um grafo direcionado e detectando a existência de ciclos fechados de espera.",
    "PARTIAL", ["identificar ciclos de deadlocks no grafo", "critério de seleção da transação vítima"],
    ["identificar ciclos de deadlocks no grafo"],
    "Explica a identificação de ciclos, mas não menciona o critério de custo para escolha da vítima.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P19_redis_distributed_lock_omit_clock_drift", "PARTIAL_COVERAGE",
    "Como funciona o algoritmo Redlock para bloqueios distribuídos em múltiplos nós Redis e como mitigar riscos de desvio de relógio (clock drift)?",
    "O cliente tenta adquirir a trava com o mesmo valor aleatório na maioria estrita das instâncias independentes de Redis com timeout curto.",
    "PARTIAL", ["funcionamento do algoritmo Redlock", "mitigação de riscos de clock drift"],
    ["funcionamento do algoritmo Redlock"],
    "Descreve a aquisição majoritária no Redlock, mas omite o impacto e a mitigação de clock drift.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P20_mutation_omit_version_check", "PARTIAL_COVERAGE",
    "Como aplicar concorrência otimista com versionamento para impedir atualizações concorrentes sujas?",
    "Lê-se o registro do banco de dados na aplicação e na hora de salvar grava-se diretamente o novo valor na tabela de forma transacional.",
    "PARTIAL", ["concorrência otimista com versionamento"],
    ["leitura e gravação na tabela"],
    "Omite a verificação da cláusula de versão no update; apenas descreve uma gravação transacional simples.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "P21_mutation_omit_idempotency_lookup", "PARTIAL_COVERAGE",
    "Como processar requisições em gateways de pagamentos garantindo deduplicação de cobranças repetidas?",
    "Recebo a requisição do cliente com o valor e despacho a cobrança imediatamente para o adquirente de cartão de crédito.",
    "PARTIAL", ["deduplicação de cobranças repetidas"],
    ["receber requisição e despachar cobrança"],
    "Processa o pagamento mas omite qualquer consulta a chaves de deduplicação ou idempotência.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "P22_mutation_omit_token_bucket_limit", "PARTIAL_COVERAGE",
    "Como proteger APIs contra excesso de tráfego utilizando algoritmos de balde de fichas (token bucket)?",
    "A gente adiciona fichas continuamente em uma variável de controle para registrar as chamadas que chegam dos usuários.",
    "PARTIAL", ["proteger APIs via token bucket"],
    ["adicionar fichas em variável de controle"],
    "Menciona o acúmulo de fichas, mas não define a limitação nem o bloqueio quando as fichas esgotam.",
    form="informal", epistemic="CONCEPTUAL"
)
add_case(
    "P23_compare_dynamo_spanner_omit_stale", "PARTIAL_COVERAGE",
    "Compare o modelo de consistência eventual em Dynamo-style databases e linearizabilidade em Spanner quanto a latência de escrita e garantias contra leituras obsoletas.",
    "O modelo de consistência eventual em bancos Dynamo permite escritas ultra-rápidas com baixa latência local sem aguardar consenso síncrono global entre nós.",
    "PARTIAL", ["latência de escrita Dynamo vs Spanner", "garantias contra leituras obsoletas"],
    ["baixa latência de escrita em consistência eventual"],
    "Aborda a latência de escrita no Dynamo, mas omite as garantias contra leituras obsoletas e a comparação com linearizabilidade.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P24_compare_sql_nosql_omit_consistency", "PARTIAL_COVERAGE",
    "Compare bancos relacionais SQL e NoSQL colunares quanto a flexibilidade de schema e garantias de consistência ACID.",
    "Bancos NoSQL oferecem esquemas dinâmicos flexíveis permitindo que cada linha possua campos distintos sem necessidade de migrações pesadas de DDL.",
    "PARTIAL", ["flexibilidade de schema SQL vs NoSQL", "garantias de consistência ACID"],
    ["flexibilidade de schema NoSQL"],
    "Trata da flexibilidade de esquema, mas omite a comparação de garantias transacionais ACID.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P25_compare_grpc_rest_omit_browser", "PARTIAL_COVERAGE",
    "Compare gRPC e REST HTTP/JSON quanto a overhead de serialização e facilidade de depuração no navegador.",
    "O gRPC utiliza codificação binária Protocol Buffers que reduz drasticamente o tamanho do payload e o processamento de serialização se comparado com o formato textual JSON do REST.",
    "PARTIAL", ["overhead de serialização gRPC vs REST", "depuração no navegador"],
    ["overhead de serialização gRPC com Protobuf"],
    "Analisa a serialização binária com Protobuf, mas omite a depuração humana em DevTools de navegadores.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P26_circuit_breaker_omit_fallback", "PARTIAL_COVERAGE",
    "Como configurar circuit breakers com timeouts agressivos e como fornecer respostas de fallback gracioso para manter a experiência do usuário?",
    "Ajusta-se o disjuntor para abrir a conexão instantaneamente após três falhas consecutivas ou requisições que excedam 500 milissegundos de espera.",
    "PARTIAL", ["configurar circuit breaker com timeout", "fornecer fallback gracioso na UI"],
    ["configurar circuit breaker com timeout"],
    "Define o limiar de abertura e timeout, mas omite o retorno de fallback de degradação graciosa.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "P27_tls_handshake_omit_alpn", "PARTIAL_COVERAGE",
    "Como o handshake TLS 1.3 reduz o tempo de estabelecimento de conexão e como negocia a versão do protocolo de aplicação via ALPN?",
    "No TLS 1.3 o cliente envia suas chaves de compartilhamento Diffie-Hellman na mensagem ClientHello inicial, reduzindo a negociação para apenas um round-trip (1-RTT).",
    "PARTIAL", ["redução de tempo em TLS 1.3", "negociação de protocolo via ALPN"],
    ["redução de tempo de negociação TLS 1.3 em 1-RTT"],
    "Explica o 1-RTT do TLS 1.3, mas omite a extensão ALPN para negociação HTTP/2.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P28_kubernetes_hpa_omit_custom_metrics", "PARTIAL_COVERAGE",
    "Como o Horizontal Pod Autoscaler escala pods baseado em uso de CPU e como configura escalonamento por métricas customizadas de mensageria?",
    "O controlador compara periodicamente o consumo médio de CPU dos containers contra o alvo definido no manifesto, aumentando o número de réplicas quando o limiar for excedido.",
    "PARTIAL", ["escalar pods baseado em CPU", "escalonamento por métricas customizadas de mensageria"],
    ["escalar pods baseado em CPU"],
    "Explica HPA por CPU, mas omite escalonamento por métricas customizadas (tamanho de fila/lag).",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P29_distributed_tracing_omit_propagation", "PARTIAL_COVERAGE",
    "Como instrumentar tracing distribuído gerando spans em microsserviços e como propagar o contexto de rastreio entre requisições HTTP?",
    "Cada serviço gera um identificador único de span para marcar o início e término da execução interna das suas funções de negócio.",
    "PARTIAL", ["gerar spans em microsserviços", "propagar contexto de rastreio entre requisições HTTP"],
    ["gerar spans em microsserviços"],
    "Explica a criação do span interno, mas não aborda a injeção e extração de headers W3C Trace Context.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P30_speculation_partitioning_partial_novel", "PARTIAL_COVERAGE",
    "Como mitigar contenção extrema de locks em tabelas de auditoria volumosas?",
    "Acho que talvez dê para criar partições por intervalo de data, embora eu não tenha certeza exata de como configurar a criação automática das partições no banco.",
    "PARTIAL", ["mitigar contenção extrema de locks em tabelas volumosas"],
    ["particionamento por data hipotético"],
    "Apresenta a ideia válida de particionamento, mas declara expressamente desconhecimento sobre a implementação.",
    form="speculative", epistemic="HYPOTHESIS"
)
add_case(
    "P31_speculation_circuit_partial_novel", "PARTIAL_COVERAGE",
    "Como proteger um microsserviço de backend contra sobrecarga em cascata de terceiros?",
    "Imagino que uma ideia seria interceptar as chamadas e cortar o tráfego com circuit breaker, mas nunca configurei o limiar de transição na prática.",
    "PARTIAL", ["proteger microsserviço contra sobrecarga em cascata"],
    ["ideia de circuit breaker hipotética"],
    "Apresenta o padrão arquitetural correto, mas expressa incerteza e omite a parametrização.",
    form="speculative", epistemic="HYPOTHESIS"
)
add_case(
    "P32_multi_aspect_oauth_omit_pkce", "PARTIAL_COVERAGE",
    "Como implementar fluxo de autorização OAuth 2.0 Authorization Code e como utilizar PKCE para proteger clientes públicos sem chave secreta?",
    "O cliente redireciona o usuário para o servidor de autorização, obtém um código temporário de autorização e troca esse código pelo token de acesso.",
    "PARTIAL", ["fluxo Authorization Code", "proteger com PKCE em clientes públicos"],
    ["fluxo Authorization Code básico"],
    "Explica o fluxo Authorization Code, mas omite completamente o Code Verifier e Code Challenge do PKCE.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "P33_multi_aspect_database_index_omit_covering", "PARTIAL_COVERAGE",
    "Como otimizar consultas analíticas criando índices compostos e como utilizar índices de cobertura (covering index) para eliminar acessos à tabela?",
    "Cria-se um índice composto ordenando as colunas de acordo com a seletividade e filtros mais utilizados na cláusula WHERE.",
    "PARTIAL", ["otimizar consultas com índices compostos", "eliminar acessos à tabela via covering index"],
    ["índices compostos baseados na seletividade do WHERE"],
    "Aborda o índice composto, mas omite a cláusula INCLUDE e o conceito de covering index.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "P34_multi_aspect_docker_multistage_omit_security", "PARTIAL_COVERAGE",
    "Como utilizar builds multi-estágio no Docker para diminuir o tamanho da imagem e como garantir a execução com usuário não-root?",
    "Utiliza-se uma imagem pesada com compilador para gerar o binário na primeira etapa e copia-se apenas o executável final para uma imagem distroless enxuta na segunda etapa.",
    "PARTIAL", ["diminuir tamanho com multi-stage build", "garantir execução com usuário não-root"],
    ["multi-stage build com compilação e cópia do binário"],
    "Explica com perfeição o multi-stage build, mas omite a criação e troca para usuário não-root.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "P35_multi_aspect_cqrs_event_sourcing_omit_snapshot", "PARTIAL_COVERAGE",
    "Como reconstruir o estado de entidades em Event Sourcing e como utilizar snapshots periódicos para acelerar a inicialização?",
    "Reconstrói-se o estado corrente lendo a sequência imutável de eventos passados a partir do log e aplicando cada mutação sequencialmente sobre o objeto.",
    "PARTIAL", ["reconstruir estado em Event Sourcing", "utilizar snapshots periódicos para aceleração"],
    ["reconstruir estado lendo eventos imutáveis em sequência"],
    "Descreve o replay de eventos, mas ignora completamente a geração de snapshots periódicos.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)

# =========================================================================
# GROUP 3: SUPPORTING (25 cases) — Auxiliary contributions, telemetry,
# observability, profiling, health checks, secondary mitigations
# =========================================================================

add_case(
    "S01_prometheus_grafana_deadlock", "SUPPORTING_MONITORING",
    "Como resolver travamentos mútuos frequentes (deadlocks) em rotinas de fechamento bancário?",
    "Configuro alertas no Grafana e exponho métricas do Prometheus para identificar quais transações demoram mais tempo presas.",
    "SUPPORTING", ["resolver deadlocks em fechamento bancário"], ["métricas no Prometheus e alertas no Grafana para identificação"],
    "Métricas e alertas ajudam a diagnosticar mas não resolvem a causa raiz dos deadlocks.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S02_prometheus_grafana_deadlock_pronominal", "SUPPORTING_MONITORING",
    "Como resolver travamentos mútuos frequentes (deadlocks) em rotinas de fechamento bancário?",
    "Instrumentam-se as rotinas com métricas no Prometheus e alarmes no Grafana para monitorar a frequência de travamentos.",
    "SUPPORTING", ["resolver deadlocks em fechamento bancário"], ["métricas e alarmes para monitorar frequência"],
    "Formulação passiva pronominal com ferramenta de monitoramento que fornece auxílio diagnóstico sem resolver o defeito.",
    form="pronominal_se", epistemic="CONCEPTUAL"
)
add_case(
    "S03_datadog_apm_concurrency", "SUPPORTING_MONITORING",
    "Como eliminar concorrência descontrolada e corrupção de saldo em pagamentos compartilhados?",
    "Instalamos o agente do Datadog para coletar traces distribuídos e criamos um dashboard para acompanhar a taxa de requisições por segundo.",
    "SUPPORTING", ["eliminar concorrência descontrolada e corrupção de saldo"], ["agente Datadog com traces distribuídos e dashboard"],
    "Traces do Datadog oferecem suporte diagnóstico mas não eliminam concorrência descontrolada.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S04_new_relic_db_bottleneck", "SUPPORTING_MONITORING",
    "Como resolver gargalos de escrita e contenção de linhas em banco relacional sobrecarregado?",
    "Configuro o New Relic APM para inspecionar os tempos de execução das queries e receber notificações quando o banco atingir saturação.",
    "SUPPORTING", ["resolver gargalos de escrita e contenção de linhas"], ["New Relic APM inspecionando tempos de execução"],
    "Notificações de APM dão visibilidade operacional mas não resolvem a contenção de linhas.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S05_cloudwatch_memory_leak", "SUPPORTING_MONITORING",
    "Como conter vazamento contínuo de memória que causa travamentos diários na aplicação?",
    "Configuro alarmes no AWS CloudWatch para disparar alertas por e-mail sempre que a taxa de uso de RAM ultrapassar 85%.",
    "SUPPORTING", ["conter vazamento contínuo de memória"], ["alarmes no CloudWatch disparando e-mails de consumo de RAM"],
    "Alarmes no CloudWatch alertam sobre o sintoma mas não contêm a causa do vazamento de memória.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S06_elasticsearch_kibana_crash", "SUPPORTING_MONITORING",
    "Como solucionar falhas intermitentes de processamento de lote em microsserviço financeiro?",
    "Envio todos os logs para o Elasticsearch e monto painéis no Kibana para visualizar a quantidade de exceções registradas a cada hora.",
    "SUPPORTING", ["solucionar falhas intermitentes de processamento de lote"], ["envio de logs para Elasticsearch e painéis no Kibana"],
    "Centralização de logs no Kibana apoia o diagnóstico mas não corrige os erros no lote.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S07_blackbox_exporter_dns", "SUPPORTING_MONITORING",
    "Como mitigar indisponibilidade provocada por resolução defeituosa de DNS entre regiões?",
    "Configuro sondas do Blackbox Exporter para efetuar requisições a cada 15 segundos e emitir alerta quando o endpoint falhar.",
    "SUPPORTING", ["mitigar indisponibilidade por falha de DNS"], ["sondas Blackbox Exporter alertando sobre falhas"],
    "Sondas de monitoramento sintético apenas detectam a falha, sem resolver a resolução de DNS.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S08_pyroscope_cpu_spike", "SUPPORTING_MONITORING",
    "Como conter picos severos de uso de CPU que travam a aplicação em horários de pico?",
    "Instalo o Pyroscope na aplicação para coletar flamegraphs contínuos de execução e identificar os métodos com maior consumo de ciclos.",
    "SUPPORTING", ["conter picos severos de uso de CPU"], ["Pyroscope com flamegraphs contínuos identificando métodos"],
    "Profiling com Pyroscope é ferramenta auxiliar para mapear onde a CPU é gasta, sem consertar o código.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S09_opentelemetry_traces_latency", "SUPPORTING_MONITORING",
    "Como diminuir latência de processamento em cadeia de chamadas síncronas entre microsserviços?",
    "Instrumento o código com OpenTelemetry exportando traces distribuídos para o Jaeger para localizar onde as requisições engasgam.",
    "SUPPORTING", ["diminuir latência de processamento em cadeia síncrona"], ["instrumentação OpenTelemetry e Jaeger para localizar atrasos"],
    "Mapeamento de gargalos com OpenTelemetry é diagnóstico auxiliar, sem diminuir a latência diretamente.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S10_sentry_exceptions_audit", "SUPPORTING_MONITORING",
    "Como evitar interrupções de checkout provocadas por exceções não tratadas no pagamento?",
    "Adiciono o Sentry na aplicação para capturar o stack trace exato e receber aviso no Slack assim que ocorrer um erro 500.",
    "SUPPORTING", ["evitar interrupções de checkout por exceções"], ["Sentry capturando stack trace e enviando aviso no Slack"],
    "Captura de stack trace pelo Sentry é telemetria auxiliar; não evita a interrupção do checkout.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S11_micrometer_jmx_connection_pool", "SUPPORTING_MONITORING",
    "Como resolver esgotamento de conexões no pool de banco de dados sob tráfego massivo?",
    "Exponho métricas de conexões ativas e pendentes via Micrometer e JMX para acompanhar o volume de threads represadas.",
    "SUPPORTING", ["resolver esgotamento de conexões no pool"], ["métricas de conexões ativas e pendentes via Micrometer e JMX"],
    "Expor métricas de pool apoia a visibilidade mas não resolve o esgotamento das conexões.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S12_k8s_liveness_probe_leak", "SUPPORTING_MONITORING",
    "Como eliminar vazamento contínuo de memória em processo de backend?",
    "Configuro liveness probes no Kubernetes para reiniciar os pods automaticamente assim que o container parar de responder.",
    "SUPPORTING", ["eliminar vazamento contínuo de memória"], ["liveness probe reiniciando pods automaticamente"],
    "Reiniciar pods via probe mitiga a indisponibilidade, mas não elimina o vazamento de memória do código.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S13_read_replica_write_bottleneck", "SUPPORTING_MONITORING",
    "Como eliminar o gargalo de escrita em banco de dados que atingiu o limite físico de IOPS do disco primário?",
    "Crio duas réplicas de leitura para balancear as consultas analíticas e aliviar o servidor principal de queries de select.",
    "SUPPORTING", ["eliminar gargalo de escrita em banco com IOPS saturado"], ["réplicas de leitura balanceando consultas e aliviando selects"],
    "Réplicas de leitura aliviam leituras, mas não eliminam o limite de IOPS de escrita no nó primário.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S14_redis_cache_write_locks", "SUPPORTING_MONITORING",
    "Como solucionar contenção severa de bloqueios em linhas concorrentes de atualização de saldo?",
    "Adiciono cache Redis na frente para desafogar as consultas de leitura frequentes da conta.",
    "SUPPORTING", ["solucionar contenção de bloqueios em linhas de atualização de saldo"], ["cache Redis para desafogar leituras da conta"],
    "Aliviar consultas de saldo com Redis é mitigação periférica; não soluciona a contenção nas escritas concorrentes.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S15_fluentbit_log_aggregator", "SUPPORTING_MONITORING",
    "Como conter corrupção de dados gerada por cancelamentos inesperados de sessões de usuários?",
    "Instalo o FluentBit nos servidores para centralizar todos os arquivos de log e auditar os registros de cancelamento depois do ocorrido.",
    "SUPPORTING", ["conter corrupção de dados gerada por cancelamentos"], ["FluentBit centralizando logs para auditar depois"],
    "Auditoria post-mortem de logs não contém nem impede a corrupção de dados.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S16_datadog_synthetic_tests", "SUPPORTING_MONITORING",
    "Como prevenir degradação de performance na rota crítica de autenticação sob cargas extremas?",
    "Agendo transações sintéticas periódicas no Datadog para monitorar o tempo de resposta do endpoint a cada minuto.",
    "SUPPORTING", ["prevenir degradação de performance na rota de autenticação"], ["transações sintéticas no Datadog monitorando tempo de resposta"],
    "Testes sintéticos apoiam o monitoramento, sem prevenir a degradação de desempenho.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S17_dynatrace_anomaly_detection", "SUPPORTING_MONITORING",
    "Como resolver falhas misteriosas de conectividade entre instâncias de banco de dados distribuído?",
    "Ativo o módulo de inteligência do Dynatrace para mapear a topologia e sinalizar anomalias de conexão na infraestrutura.",
    "SUPPORTING", ["resolver falhas de conectividade entre instâncias"], ["Dynatrace mapeando topologia e sinalizando anomalias"],
    "Detecção de anomalias oferece auxílio analítico mas não resolve a causa física de conectividade.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S18_prometheus_alerts_disk_full", "SUPPORTING_MONITORING",
    "Como evitar colapso de nós de dados por esgotamento repentino de espaço em disco?",
    "Configuro alertas no Prometheus para avisar no canal de suporte assim que o volume do disco atingir 90% de ocupação.",
    "SUPPORTING", ["evitar colapso por esgotamento de disco"], ["alertas no Prometheus avisando quando o disco atingir 90%"],
    "Alertar sobre disco cheio é proteção auxiliar de monitoramento, sem gerenciar ou expurgar os dados.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S19_grafana_dashboard_threads", "SUPPORTING_MONITORING",
    "Como solucionar travamento de threads causado por loops infinitos em processamento assíncrono?",
    "Monto um painel no Grafana para exibir quantas threads estão em execução e o consumo agregado de memória.",
    "SUPPORTING", ["solucionar travamento de threads causado por loops"], ["painel no Grafana exibindo threads em execução e memória"],
    "Visualizar contagem de threads não corrige o loop infinito.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S20_kibana_error_rate_visualization", "SUPPORTING_MONITORING",
    "Como conter falhas silenciosas de cálculo financeiro em microsserviço de faturamento?",
    "Crio visualizações no Kibana para acompanhar a taxa percentual de erros por minuto nas mensagens processadas.",
    "SUPPORTING", ["conter falhas silenciosas de cálculo financeiro"], ["visualizações no Kibana acompanhando taxa de erros"],
    "Exibir taxa de erro é telemetria auxiliar de suporte operacional.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S21_cloudwatch_io_throttling", "SUPPORTING_MONITORING",
    "Como mitigar travamentos de escrita provocados por saturação de IOPS em banco relacional na nuvem?",
    "Configuro alarmes no AWS CloudWatch para monitorar a métrica de IOPS consumidas e enviar alerta quando houver estrangulamento.",
    "SUPPORTING", ["mitigar travamentos de escrita por saturação de IOPS"], ["alarmes no CloudWatch monitorando métrica de IOPS e throttling"],
    "Alerta no CloudWatch sobre estrangulamento de IOPS é diagnóstico complementar.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S22_sentry_release_tracking", "SUPPORTING_MONITORING",
    "Como prevenir bugs de regressão funcional introduzidos em novos deploys de microsserviços?",
    "Integro o Sentry na esteira para rastrear novos lançamentos e notificar os desenvolvedores quando um novo erro aparecer.",
    "SUPPORTING", ["prevenir bugs de regressão funcional em deploys"], ["Sentry rastreando lançamentos e notificando sobre novos erros"],
    "Rastreamento de erros pós-deploy auxilia a equipe mas não previne a introdução do bug no código.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S23_hikaricp_leak_detection_threshold", "SUPPORTING_MONITORING",
    "Como eliminar vazamento silencioso de conexões em rotinas legadas com queries abertas?",
    "Ativo o leakDetectionThreshold do HikariCP para gerar logs com stack trace quando uma conexão demorar mais de 5 segundos para ser devolvida ao pool.",
    "SUPPORTING", ["eliminar vazamento silencioso de conexões em rotinas legadas"], ["leakDetectionThreshold do HikariCP gerando logs com stack trace"],
    "Identificação de vazamento via threshold de pool é diagnóstico de suporte sem corrigir a query legada.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S24_blackbox_http_probes", "SUPPORTING_MONITORING",
    "Como resolver indisponibilidade crônica de rede entre microsserviços em diferentes data centers?",
    "Configuro sondas do Blackbox Exporter para testar requisições HTTP entre os nós e avisar se a latência subir.",
    "SUPPORTING", ["resolver indisponibilidade de rede entre data centers"], ["sondas do Blackbox Exporter testando HTTP e avisando sobre latência"],
    "Monitoramento de latência por sondas auxilia na percepção da falha, sem resolver a estabilidade da rede.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)
add_case(
    "S25_pyroscope_memory_allocations", "SUPPORTING_MONITORING",
    "Como diminuir pausas de garbage collector provocadas por alocações massivas de objetos efêmeros?",
    "Instalo o Pyroscope para mapear a taxa de alocação de memória por método e ver quais trechos do código estão instanciando mais dados.",
    "SUPPORTING", ["diminuir pausas de garbage collector por alocações massivas"], ["Pyroscope mapeando alocações de memória por método"],
    "Mapeamento de alocações via flamegraph fornece evidência diagnóstica auxiliar sem alterar as estruturas de dados.",
    form="active_1st", epistemic="DEMONSTRATED_EXPERIENCE"
)

# =========================================================================
# GROUP 4: RELATED (30 cases) — Thematic connection without operational
# mechanism, tool descriptions, history/trivia, pure experience declaration
# =========================================================================

add_case(
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
)
add_case(
    "R07_declaration_kubernetes_experience", "RELATED_THEMATIC",
    "Como configurar políticas de rede (NetworkPolicies) no Kubernetes para isolar namespaces sensíveis?",
    "Eu utilizo Kubernetes diariamente na minha empresa e tenho mais de 8 anos de experiência em administração de clusters corporativos.",
    "RELATED", ["configurar NetworkPolicies no Kubernetes para isolar namespaces"], ["nenhum mecanismo de NetworkPolicy demonstrado"],
    "Declaração pura de experiência profissional sem demonstrar configuração técnica de NetworkPolicy.",
    form="active_1st", epistemic="DECLARATION"
)
add_case(
    "R08_declaration_postgresql_experience", "RELATED_THEMATIC",
    "Como otimizar consultas analíticas complexas com Window Functions no PostgreSQL?",
    "Eu trabalho com PostgreSQL há mais de 10 anos na nossa empresa e sou especialista sênior em bancos de dados relacionais.",
    "RELATED", ["otimizar consultas com Window Functions no PostgreSQL"], ["nenhum mecanismo de Window Functions demonstrado"],
    "Declaração de senioridade e tempo de carreira sem demonstrar mecanismo técnico de Window Functions.",
    form="active_1st", epistemic="DECLARATION"
)
add_case(
    "R09_declaration_kafka_experience", "RELATED_THEMATIC",
    "Como evitar perda de mensagens quando um broker do Kafka é encerrado forçadamente?",
    "Eu utilizo Apache Kafka nos projetos da minha empresa no dia a dia e conheço bem a plataforma de mensageria.",
    "RELATED", ["evitar perda de mensagens sob encerramento de broker"], ["nenhum mecanismo de acks, min.insync.replicas demonstrado"],
    "Declaração genérica de uso cotidiano sem explicar configurações de resiliência.",
    form="active_1st", epistemic="DECLARATION"
)
add_case(
    "R10_declaration_redis_experience", "RELATED_THEMATIC",
    "Como configurar persistência AOF com fsync a cada segundo no Redis?",
    "Eu tenho 7 anos de experiência com Redis e atuo como líder técnico em arquitetura de caches corporativos.",
    "RELATED", ["configurar persistência AOF com fsync a cada segundo no Redis"], ["nenhum mecanismo de persistência AOF demonstrado"],
    "Declaração de cargo e anos de atuação sem fornecer os parâmetros de configuração do Redis.",
    form="active_1st", epistemic="DECLARATION"
)
add_case(
    "R11_kubernetes_docker_tautology", "RELATED_THEMATIC",
    "Como o Kubernetes gerencia a integridade e ciclo de vida de containers em nós de computação?",
    "O Kubernetes é um orquestrador de pods muito robusto que gerencia containers em clusters grandes com muita facilidade.",
    "RELATED", ["como Kubernetes gerencia ciclo de vida de containers"], ["nenhum mecanismo de kubelet, pod lifecycle demonstrado"],
    "Repetição tautológica laudatória sobre gerenciar containers com facilidade, sem mecanismo.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R12_linux_kernel_history", "RELATED_THEMATIC",
    "Como o agendador CFS (Completely Fair Scheduler) do kernel Linux equilibra o tempo de CPU entre processos concorrentes?",
    "O kernel Linux foi lançado inicialmente em 1991 como um projeto pessoal de um estudante finlandês baseado no sistema Minix.",
    "RELATED", ["como CFS equilibra tempo de CPU entre processos"], ["nenhum mecanismo de CFS, vruntime, red-black tree demonstrado"],
    "Histórico sobre o surgimento do kernel sem responder à mecânica do agendador CFS.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R13_python_gil_history", "RELATED_THEMATIC",
    "Como contornar o Global Interpreter Lock (GIL) do Python para acelerar processamento matemático paralelo?",
    "O Python foi concebido por Guido van Rossum no final dos anos 80 nos Países Baixos como sucessor da linguagem ABC.",
    "RELATED", ["contornar o GIL do Python para processamento paralelo"], ["nenhum mecanismo de multiprocessing, ctypes, nogil demonstrado"],
    "Curiosidade biográfica sobre o criador do Python sem explicar como contornar o GIL.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R14_rust_memory_model_history", "RELATED_THEMATIC",
    "Como o compilador do Rust assegura segurança de memória em tempo de compilação sem usar garbage collector?",
    "O Rust foi desenvolvido originalmente por Graydon Hoare na Mozilla e eleito a linguagem favorita em pesquisas do Stack Overflow.",
    "RELATED", ["como compilador Rust assegura segurança de memória sem GC"], ["nenhum mecanismo de borrow checker, lifetimes demonstrado"],
    "Fatos históricos e pesquisas de popularidade sem explicar ownership, borrowing ou lifetimes.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R15_java_virtual_threads_history", "RELATED_THEMATIC",
    "Como as Virtual Threads do Java mapeiam milhares de tarefas concorrentes sobre poucos threads de sistema operacional?",
    "O projeto Loom levou vários anos de desenvolvimento dentro do OpenJDK até ser lançado oficialmente na versão 21 do Java.",
    "RELATED", ["como Virtual Threads mapeiam tarefas sobre threads de SO"], ["nenhum mecanismo de carrier threads, continuations demonstrado"],
    "Histórico da release e do Projeto Loom sem explicar carrier threads ou continuações de runtime.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R16_surrealdb_general_opinion", "RELATED_THEMATIC",
    "Como o SurrealDB conecta registros em formato de grafo sem necessidade de joins relacionais pesados?",
    "O SurrealDB é um banco de dados moderno excelente para trabalhar com múltiplos modelos de dados de forma unificada.",
    "RELATED", ["como SurrealDB conecta registros em formato de grafo sem joins"], ["nenhum mecanismo de ponteiros diretos em grafo demonstrado"],
    "Elogio de marketing sobre modelo unificado sem explicar ponteiros de nós.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R17_duckdb_general_opinion", "RELATED_THEMATIC",
    "Como o motor DuckDB processa consultas analíticas colunares executando em processo no cliente?",
    "O DuckDB é uma ferramenta analítica muito leve frequentemente chamada de SQLite das consultas de Big Data.",
    "RELATED", ["como DuckDB processa consultas analíticas colunares em processo"], ["nenhum mecanismo de execução colunar vetorizada demonstrado"],
    "Metáfora comercial ('SQLite do Big Data') sem detalhar execução analítica vetorizada.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R18_clickhouse_general_opinion", "RELATED_THEMATIC",
    "Como o ClickHouse atinge alta taxa de compressão e velocidade em leituras colunares massivas?",
    "O ClickHouse foi criado pela Yandex e é famoso mundialmente por ser incrivelmente veloz em análises de telemetria de web.",
    "RELATED", ["como ClickHouse atinge alta compressão e velocidade colunar"], ["nenhum mecanismo de compressão por coluna demonstrado"],
    "Origem e reputação de velocidade sem demonstrar algoritmos de compressão de blocos.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R19_etcd_raft_general_opinion", "RELATED_THEMATIC",
    "Como o etcd gerencia a consistência de chave-valor distribuída sob partições de rede?",
    "O etcd é um componente de infraestrutura mantido pela Cloud Native Computing Foundation amplamente utilizado na nuvem.",
    "RELATED", ["como etcd gerencia consistência de chave-valor sob partições"], ["nenhum mecanismo de quórum ou Raft demonstrado"],
    "Metadados institucionais (CNCF, nuvem) sem explicar o algoritmo de consenso Raft.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R20_grpc_protobuf_general_opinion", "RELATED_THEMATIC",
    "Como o compilador protoc gera stubs tipados a partir de definições de serviço em arquivos proto?",
    "O Protocol Buffers foi criado pelo Google para serialização corporativa interna e possui excelente documentação pública.",
    "RELATED", ["como protoc gera stubs tipados a partir de arquivos proto"], ["nenhum mecanismo de compilação ou geração de stubs demonstrado"],
    "Origem corporativa do Google sem explicar a geração de código pelo protoc.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R21_graphql_facebook_history", "RELATED_THEMATIC",
    "Como o GraphQL compila e resolve campos encadeados em um grafo de tipos unificado?",
    "O GraphQL foi desenvolvido pelo Facebook em 2012 para resolver problemas nos aplicativos móveis de notícias.",
    "RELATED", ["como GraphQL compila e resolve campos encadeados"], ["nenhum mecanismo de AST, resolvers demonstrado"],
    "Histórico de desenvolvimento pelo Facebook sem explicar a árvore de resolvers.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R22_redis_antirez_history", "RELATED_THEMATIC",
    "Como o Redis gerencia estruturas de dados em memória utilizando um único loop de eventos?",
    "O Redis foi criado pelo programador italiano Salvatore Sanfilippo (antirez) enquanto tentava melhorar a performance de um site.",
    "RELATED", ["como Redis gerencia estruturas em memória via loop de eventos"], ["nenhum mecanismo de single-threaded event loop demonstrado"],
    "Histórico biográfico do criador do Redis sem explicar a arquitetura single-threaded.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R23_elasticsearch_shay_banon_history", "RELATED_THEMATIC",
    "Como o Elasticsearch distribui sharding e índices invertidos entre os nós de um cluster?",
    "O criador Shay Banon desenvolveu o predecessor Compass para criar um livro de receitas culinárias para sua esposa.",
    "RELATED", ["como Elasticsearch distribui sharding e índices invertidos"], ["nenhum mecanismo de Lucene, índice invertido demonstrado"],
    "Curiosidade anedótica da origem do projeto sem responder ao mecanismo de busca textual.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R24_nginx_igor_sysoev_history", "RELATED_THEMATIC",
    "Como o Nginx utiliza processos de trabalho baseados em eventos para atingir baixa latência como proxy reverso?",
    "O software foi criado pelo desenvolvedor russo Igor Sysoev nos anos 2000 para lidar com o problema do site Rambler.",
    "RELATED", ["como Nginx usa processos de trabalho baseados em eventos"], ["nenhum mecanismo de worker processes, non-blocking sockets demonstrado"],
    "Fato histórico sem explicar arquitetura de eventos do Nginx.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R25_sqlite_richard_hipp_history", "RELATED_THEMATIC",
    "Como o SQLite gerencia concorrência em transações locais utilizando arquivos de lock no sistema de arquivos?",
    "O criador Richard Hipp inventou o SQLite enquanto trabalhava na Marinha americana para dispensar instalação de servidores dedicados.",
    "RELATED", ["como SQLite gerencia concorrência via locks de filesystem"], ["nenhum mecanismo de lock de arquivo do SQLite demonstrado"],
    "Anedota militar sem responder ao funcionamento de locks no SQLite.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R26_declaration_docker_daily", "RELATED_THEMATIC",
    "Como o Docker utiliza namespaces de PID e cgroups do kernel Linux para isolar containers?",
    "Eu utilizo Docker e Kubernetes diariamente na minha empresa e conheço bastante sobre containerização moderna.",
    "RELATED", ["como Docker usa namespaces de PID e cgroups"], ["nenhum mecanismo de kernel namespaces ou cgroups demonstrado"],
    "Declaração de familiaridade e uso corporativo sem explicar os primitivos de isolamento do Linux.",
    form="active_1st", epistemic="DECLARATION"
)
add_case(
    "R27_declaration_react_seniority", "RELATED_THEMATIC",
    "Como o Virtual DOM reconcilia alterações de estado através do algoritmo de diffing em árvore?",
    "Eu tenho 6 anos de experiência com React e desenvolvo aplicações web ricas todos os dias no meu trabalho.",
    "RELATED", ["como Virtual DOM reconcilia alterações via diffing"], ["nenhum mecanismo de diffing em árvore demonstrado"],
    "Declaração de tempo de experiência no ecossistema sem demonstrar algoritmo de reconciliação.",
    form="active_1st", epistemic="DECLARATION"
)
add_case(
    "R28_hardware_ram_ddr5_trivia", "RELATED_THEMATIC",
    "Como alinhar estruturas de dados na memória para evitar penalidades de acesso não alinhado na CPU?",
    "Minha máquina corporativa tem 64 gigabytes de memória RAM DDR5 com frequência de 5600 megatransfers por segundo.",
    "RELATED", ["alinhar estruturas na memória para evitar penalidades de acesso"], ["nenhum mecanismo de alinhamento de memória demonstrado"],
    "Detalhes da máquina pessoal do candidato sem demonstrar técnica de alinhamento de memória.",
    form="active_1st", epistemic="DECLARATION"
)
add_case(
    "R29_hardware_nvme_disk_trivia", "RELATED_THEMATIC",
    "Como funcionam operações de escrita sequencial em SSDs NVMe para prolongar a vida útil das células de memória flash?",
    "O servidor possui quatro discos SSD NVMe em RAID com barramento PCI Express 4.0 de altíssima velocidade.",
    "RELATED", ["operações de escrita sequencial em SSD NVMe e vida útil"], ["nenhum mecanismo de wear leveling demonstrado"],
    "Especificação da placa controladora do servidor sem responder à preservação das células flash.",
    form="formal", epistemic="CONCEPTUAL"
)
add_case(
    "R30_software_version_trivia", "RELATED_THEMATIC",
    "Como o Apache Kafka 3.0 opera sem o ZooKeeper através do protocolo de metadados KRaft?",
    "A versão 3.0 do Apache Kafka foi lançada em setembro de 2021 pela equipe de desenvolvedores da Confluent.",
    "RELATED", ["como Kafka 3.0 opera sem ZooKeeper através do KRaft"], ["nenhum mecanismo de KRaft demonstrado"],
    "Data de lançamento da versão sem explicar o protocolo de metadados KRaft.",
    form="formal", epistemic="CONCEPTUAL"
)

# =========================================================================
# GROUP 5: OFF_TOPIC (35 cases) — Destructive antitheses, orthogonal domains
# (CSS/Tailwind, AI/ML Scikit-Learn, DevOps pipelines in DB context), alien
# =========================================================================

# 5.1 Destructive Antitheses (Proposing actions that defeat operational safety)
add_case(
    "O01_antithesis_drop_locks", "OFF_TOPIC_ANTITHESIS",
    "Como resolver concorrência de escritas e prevenir sobreposições em tabelas financeiras concorrentes?",
    "Para resolver isso, desativo todos os locks do banco e deixo todas as transações gravarem livremente sem controle de concorrência.",
    "OFF_TOPIC", ["prevenir sobreposições em tabelas financeiras concorrentes"], ["ação destrutiva que desativa locks e piora a corrupção"],
    "Propõe desligar travas de proteção, violando a exigência de segurança operacional.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O02_antithesis_drop_locks_inflected", "OFF_TOPIC_ANTITHESIS",
    "Como resolver concorrência de escritas e prevenir sobreposições em tabelas financeiras concorrentes?",
    "Removo qualquer bloqueio ou restrição de concorrência e autorizo escritas simultâneas diretas na tabela sem travar linhas.",
    "OFF_TOPIC", ["prevenir sobreposições em tabelas financeiras concorrentes"], ["ação destrutiva de remoção de bloqueios"],
    "Flexão verbal na 1ª pessoa que propõe a remoção de mecanismos de proteção contra corrupção.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O03_antithesis_drop_acid_transactions", "OFF_TOPIC_ANTITHESIS",
    "Como garantir consistência em transferências bancárias que debitam de uma conta e creditam em outra?",
    "Desligo transações ACID para escrever direto no banco sem intermediários, acelerando o processo e ignorando falhas no meio.",
    "OFF_TOPIC", ["garantir consistência em transferências bancárias"], ["ação destrutiva de desligar transações ACID"],
    "Elimina a garantia atômica indispensável em transferências financeiras.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
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
)
add_case(
    "O06_antithesis_plain_text_passwords", "OFF_TOPIC_ANTITHESIS",
    "Como proteger credenciais de usuários e tokens sensíveis contra vazamentos em banco de dados?",
    "Gravo senhas em texto puro no banco de dados para evitar custo de computação com funções hash criptográficas.",
    "OFF_TOPIC", ["proteger credenciais e tokens contra vazamentos"], ["ação destrutiva de gravar senhas em texto puro"],
    "Prática destrutiva frontalmente oposta à segurança criptográfica de senhas.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O07_antithesis_disable_rate_limiting", "OFF_TOPIC_ANTITHESIS",
    "Como proteger rotas públicas de reset de senha contra abuso automatizado e enumeração de e-mails?",
    "Retiro todos os limites de chamadas e envio e-mails para qualquer endereço solicitado sem validar existência ou frequência.",
    "OFF_TOPIC", ["proteger rotas de reset de senha contra abuso"], ["ação destrutiva retirando limites e enviando e-mails indiscriminadamente"],
    "Antítese que facilita o abuso automatizado de e-mails.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O08_antithesis_drop_indexes_for_perf", "OFF_TOPIC_ANTITHESIS",
    "Como acelerar consultas críticas em tabelas com milhões de registros que sofrem lentidão severa?",
    "Removo todos os índices da tabela para que o banco não gaste processamento gerenciando árvores de índices.",
    "OFF_TOPIC", ["acelerar consultas críticas em tabelas volumosas"], ["ação destrutiva de remoção de todos os índices"],
    "A remoção de índices força table scan completo em milhões de linhas, piorando a lentidão.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O09_antithesis_skip_quorum_writes", "OFF_TOPIC_ANTITHESIS",
    "Como evitar inconsistência de dados em cluster distribuído sujeito a partições de rede?",
    "Aceite escritas livremente sem checar a maioria das réplicas, gravando em qualquer nó isolado que responder primeiro.",
    "OFF_TOPIC", ["evitar inconsistência em cluster sob partição"], ["ação destrutiva de aceitar escritas sem quórum"],
    "Gera split-brain e divergência irreparável de dados.",
    form="active_3rd", epistemic="CONCEPTUAL"
)
add_case(
    "O10_antithesis_skip_signature_validation", "OFF_TOPIC_ANTITHESIS",
    "Como validar tokens JWT com segurança para impedir que atacantes forjem permissões no payload?",
    "Aceito qualquer token recebido sem validar assinatura criptográfica para diminuir latência na checagem de autorização.",
    "OFF_TOPIC", ["validar tokens JWT impedindo forja de permissões"], ["ação destrutiva de aceitar tokens sem validação de assinatura"],
    "Anula completamente a segurança de assinatura de tokens de acesso.",
    form="active_1st", epistemic="CONCEPTUAL"
)

# 5.2 Orthogonal Domain: Frontend / CSS / Webpack in Backend / Concurrency Questions
add_case(
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
)
add_case(
    "O19_ml_pytorch_cnn_consistent_hashing", "OFF_TOPIC_ORTHOGONAL",
    "Como o consistent hashing distribui chaves de armazenamento entre múltiplos nós de um cluster?",
    "Eu defino uma rede neural convolucional no PyTorch com camadas de convolução de filtros 3x3 e max pooling para classificar imagens.",
    "OFF_TOPIC", ["consistent hashing distribuindo chaves entre nós"], ["CNN no PyTorch com filtros 3x3 e max pooling"],
    "Classificação de imagens com redes convolucionais é completamente disjunta de hashing consistente.",
    form="active_1st", epistemic="CONCEPTUAL"
)
add_case(
    "O20_ml_nlp_stopwords_sharding", "OFF_TOPIC_ORTHOGONAL",
    "Como escolher a chave de sharding em bancos de dados distribuídos para pulverizar registros?",
    "Aplico remoção de stopwords e lematização de textos em português com a biblioteca NLTK para processamento de linguagem natural.",
    "OFF_TOPIC", ["escolher chave de sharding em banco distribuído"], ["remoção de stopwords e lematização com NLTK"],
    "Pré-processamento textual com NLTK é ortogonal ao particionamento de tabelas em bancos distribuídos.",
    form="active_1st", epistemic="CONCEPTUAL"
)

# 5.4 Orthogonal Domain: DevOps / Dockerfile / CI Pipeline in Pure SQL / Algorithmic Questions
add_case(
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
)

# 5.5 Alien Domains (Cooking, Sports, Everyday Life)
add_case(
    "O26_alien_cooking_lasagna", "OFF_TOPIC_ALIEN",
    "Como implementar controle de concorrência otimista com versionamento em registros disputados?",
    "Eu gosto de preparar lasanha de berinjela aos sábados, fatiando os ingredientes com molho de tomate e assando no forno médio.",
    "OFF_TOPIC", ["controle de concorrência otimista com versionamento"], ["receita de culinária preparando lasanha de berinjela"],
    "Domínio culinário completamente alienígena à computação.",
    form="active_1st", epistemic="UNKNOWN"
)
add_case(
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
)

# =========================================================================
# GROUP 6: INSUFFICIENT (18 cases) — Uninformative, evasive, ignorant, filler
# =========================================================================

add_case(
    "I01_ignorant_never_used", "INSUFFICIENT_EVIDENCE",
    "Como o mecanismo de consenso Raft elege um novo líder após expiração de heartbeat?",
    "Nunca usei essa tecnologia e não sei como responder.",
    "INSUFFICIENT", ["eleição de líder no Raft"], ["declaração de ignorância"],
    "Candidato declara explicitamente ignorância e falta de uso.",
    form="concise", epistemic="UNCERTAINTY"
)
add_case(
    "I02_ignorant_dont_remember", "INSUFFICIENT_EVIDENCE",
    "Como configurar balanceamento de nós virtuais em consistent hashing?",
    "Não lembro agora de cabeça como funciona isso.",
    "INSUFFICIENT", ["configurar nós virtuais em consistent hashing"], ["declaração de esquecimento"],
    "Candidato expressa esquecimento, não fornecendo proposição técnica.",
    form="concise", epistemic="UNCERTAINTY"
)
add_case(
    "I03_ignorant_never_studied", "INSUFFICIENT_EVIDENCE",
    "Como funciona a detecção de ciclos em grafos de espera para resolução de deadlocks?",
    "Nunca estudei esse assunto a fundo na minha carreira.",
    "INSUFFICIENT", ["detecção de ciclos em grafos de espera"], ["declaração de falta de estudo"],
    "Declaração explícita de desconhecimento.",
    form="concise", epistemic="UNCERTAINTY"
)
add_case(
    "I04_filler_monosyllabic_sim", "INSUFFICIENT_EVIDENCE",
    "Você saberia explicar como o protocolo Paxos garante consenso em redes assíncronas?",
    "Sim, com certeza.",
    "INSUFFICIENT", ["explicar como Paxos garante consenso"], ["confirmação conversacional monossilábica"],
    "Filler conversacional vazio sem conteúdo técnico avaliável.",
    form="filler", epistemic="UNKNOWN"
)
add_case(
    "I05_filler_ok_beleza", "INSUFFICIENT_EVIDENCE",
    "Como evitar concorrência descontrolada em atualizações de saldo?",
    "Beleza, ok.",
    "INSUFFICIENT", ["evitar concorrência descontrolada"], ["interjeição de preenchimento"],
    "Apenas interjeição conversacional sem substância.",
    form="filler", epistemic="UNKNOWN"
)
add_case(
    "I06_filler_conheco_bem", "INSUFFICIENT_EVIDENCE",
    "Como o Kafka lida com offsets de mensagens não confirmadas?",
    "Conheço bem, sim.",
    "INSUFFICIENT", ["como Kafka lida com offsets"], ["afirmação conversacional de conhecimento"],
    "Afirma conhecer mas não articula nenhuma proposição explicativa.",
    form="filler", epistemic="UNKNOWN"
)
add_case(
    "I07_evasive_depends_on_factors", "INSUFFICIENT_EVIDENCE",
    "Qual a melhor estratégia para particionar um banco de dados relacional massivo?",
    "Isso depende de muitos fatores e varia conforme a situação específica de cada empresa.",
    "INSUFFICIENT", ["estratégia para particionar banco relacional"], ["frase evasiva genérica"],
    "Evasiva genérica sem apontar critérios ou mecanismos técnicos.",
    form="evasive", epistemic="UNKNOWN"
)
add_case(
    "I08_evasive_we_use_tools", "INSUFFICIENT_EVIDENCE",
    "Como isolar componentes lentos para evitar esgotamento de conexões?",
    "A gente usa ferramentas para isso no dia a dia olhando os servidores.",
    "INSUFFICIENT", ["isolar componentes lentos para evitar esgotamento"], ["evasiva genérica mencionando ferramentas"],
    "Resposta vaga que não cita nem descreve nenhuma ferramenta ou técnica.",
    form="evasive", epistemic="UNKNOWN"
)
add_case(
    "I09_evasive_looking_logs", "INSUFFICIENT_EVIDENCE",
    "Como identificar se uma consulta SQL está causando table scan em produção?",
    "A gente descobre olhando logs quando o sistema começa a reclamar.",
    "INSUFFICIENT", ["identificar table scan em produção"], ["evasiva genérica 'olhando logs'"],
    "Falta mecanismo técnico (explain analyze, execution plan, etc.).",
    form="evasive", epistemic="UNKNOWN"
)
add_case(
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
)
add_case(
    "I13_evasive_just_a_queue", "INSUFFICIENT_EVIDENCE",
    "Como o RabbitMQ garante entrega confiável com confirmações de publicação e consumo?",
    "É uma fila apenas.",
    "INSUFFICIENT", ["como RabbitMQ garante entrega com confirmações"], ["definição minimalista vazia"],
    "Definição minimalista de quatro palavras que não explica confirmações de publisher ou consumer acks.",
    form="concise", epistemic="UNKNOWN"
)
add_case(
    "I14_filler_uhum_ok", "INSUFFICIENT_EVIDENCE",
    "Como o protocolo Raft gerencia o envio de heartbeats para manter liderança?",
    "Uhum, ok, beleza.",
    "INSUFFICIENT", ["gerenciamento de heartbeats no Raft"], ["interjeições conversacionais"],
    "Conteúdo sem proposições técnicas.",
    form="filler", epistemic="UNKNOWN"
)
add_case(
    "I15_ignorant_never_read_about_it", "INSUFFICIENT_EVIDENCE",
    "Como funciona a compressão de prefixos em nós internos de índices em árvore B?",
    "Nunca li nada sobre isso.",
    "INSUFFICIENT", ["compressão de prefixos em árvore B"], ["declaração de ignorância"],
    "Declaração de desconhecimento absoluto.",
    form="concise", epistemic="UNCERTAINTY"
)
add_case(
    "I16_evasive_generic_monitoring", "INSUFFICIENT_EVIDENCE",
    "Como mitigar gargalos de contenção de travas em bancos de dados de alta concorrência?",
    "A gente costuma ligar observabilidade genérica para acompanhar como o sistema está reagindo como um todo.",
    "INSUFFICIENT", ["mitigar gargalos de contenção de travas"], ["evasiva genérica mencionando observabilidade"],
    "Vagueza sem ferramentas nem mecanismos de mitigação de locks.",
    form="evasive", epistemic="UNKNOWN"
)
add_case(
    "I17_filler_aham", "INSUFFICIENT_EVIDENCE",
    "Como funciona o handshake do protocolo TCP para sincronização de números de sequência?",
    "Aham, sim.",
    "INSUFFICIENT", ["handshake do protocolo TCP"], ["filler conversacional"],
    "Sem proposição técnica avaliável.",
    form="filler", epistemic="UNKNOWN"
)
add_case(
    "I18_ignorant_dont_recall", "INSUFFICIENT_EVIDENCE",
    "Como um Bloom Filter calcula a probabilidade de falsos positivos com base no número de funções hash?",
    "Não recordo agora como é a fórmula disso.",
    "INSUFFICIENT", ["cálculo de falsos positivos no Bloom Filter"], ["declaração de esquecimento"],
    "Expressão explícita de esquecimento.",
    form="concise", epistemic="UNCERTAINTY"
)

# =========================================================================
# GROUP 7: UNKNOWN (12 cases) — Circular tautologies, undecidable semantic
# content, circular reasoning without mechanism
# =========================================================================

add_case(
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
)
add_case(
    "U06_tautology_duplicate_duplicates", "UNKNOWN_TAUTOLOGY",
    "Como réplicas síncronas evitam perda de dados quando um servidor sofre pane física?",
    "As réplicas evitam perdas porque os dados ficam duplicados em vários lugares duplicados.",
    "UNKNOWN", ["como réplicas síncronas evitam perda de dados"], ["repetição circular 'duplicados em lugares duplicados'"],
    "Tautologia circular sem explicar o quórum ou a confirmação de escrita em disco.",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U07_tautology_sync_synchronizes", "UNKNOWN_TAUTOLOGY",
    "Como o protocolo Raft mantém a consistência de dados entre múltiplos servidores?",
    "Ele mantém a consistência porque os nós ficam sincronizados mantendo uma sincronia sincronizada.",
    "UNKNOWN", ["como Raft mantém consistência entre servidores"], ["repetição circular 'sincronizados em sincronia sincronizada'"],
    "Tautologia circular sem explicar eleição de líder ou quórum de confirmação de log.",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U08_tautology_compression_compresses", "UNKNOWN_TAUTOLOGY",
    "Como algoritmos de compressão reduzem o tráfego de rede na transferência de grandes volumes de dados?",
    "Eles reduzem o tráfego comprimindo os pacotes de forma que o tamanho fique comprimido e com compressão aplicada.",
    "UNKNOWN", ["como compressão reduz tráfego de rede"], ["repetição circular 'comprimindo de forma que fique comprimido'"],
    "Tautologia circular sem explicar dicionários, Huffman ou eliminação de redundâncias de bytes.",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U09_tautology_isolated_isolates", "UNKNOWN_TAUTOLOGY",
    "Como o isolamento em transações ACID impede que operações concorrentes interfiram entre si?",
    "O isolamento impede interferências isolando as transações para que cada uma fique isolada em isolamento próprio.",
    "UNKNOWN", ["como isolamento impede interferência entre transações"], ["repetição circular 'isolando para ficar isolada em isolamento'"],
    "Tautologia circular sem citar locks, versionamento de linhas ou níveis de isolamento ANSI SQL.",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U10_tautology_durable_durability", "UNKNOWN_TAUTOLOGY",
    "Como a durabilidade de banco de dados assegura que dados confirmados não se percam após queda de energia?",
    "A durabilidade assegura isso tornando os dados duráveis para que permaneçam com durabilidade garantida.",
    "UNKNOWN", ["como durabilidade assegura sobrevivência a queda de energia"], ["repetição circular 'duráveis para permanecer com durabilidade'"],
    "Tautologia circular sem citar escrita em meio persistente não-volátil ou fsync.",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U11_tautology_partition_partitions", "UNKNOWN_TAUTOLOGY",
    "Como a divisão de tabelas em partições melhora a velocidade de varreduras em bancos de dados?",
    "A divisão melhora a velocidade particionando a tabela em várias partições particionadas.",
    "UNKNOWN", ["como divisão em partições melhora velocidade"], ["repetição circular 'particionando em partições particionadas'"],
    "Tautologia circular pura.",
    form="tautology", epistemic="UNKNOWN"
)
add_case(
    "U12_tautology_resilient_resilience", "UNKNOWN_TAUTOLOGY",
    "Como padrões de resiliência mantêm a disponibilidade de serviços de backend sob falhas parciais?",
    "Eles mantêm a disponibilidade fornecendo resiliência para que o sistema se torne resiliente com alta resiliência.",
    "UNKNOWN", ["como padrões mantêm disponibilidade sob falhas"], ["repetição circular 'fornecendo resiliência para ficar resiliente'"],
    "Tautologia circular sem descrever circuit breaker, timeout ou retries.",
    form="tautology", epistemic="UNKNOWN"
)

# =========================================================================
# Validation: Ensure exactly 200 cases and distribution summary
# =========================================================================

assert len(cases) == 200, f"Expected 200 cases, got {len(cases)}"

from collections import Counter
counts = Counter([c["human_classification"] for c in cases])
print("Dataset successfully assembled!")
print("Total Cases:", len(cases))
print("Class Distribution:", dict(counts))

# Export sealed ground truth and blind input
sealed_gt_path = "scratch/stage_31_7_17_ground_truth.json"
blind_in_path = "scratch/stage_31_7_17_blind_input.json"

with open(sealed_gt_path, "w", encoding="utf-8") as f:
    json.dump(cases, f, indent=2, ensure_ascii=False)

blind_cases = [
    {
        "id": c["id"],
        "question_text": c["question_text"],
        "response_text": c["response_text"]
    }
    for c in cases
]

with open(blind_in_path, "w", encoding="utf-8") as f:
    json.dump(blind_cases, f, indent=2, ensure_ascii=False)

gt_bytes = open(sealed_gt_path, "rb").read()
in_bytes = open(blind_in_path, "rb").read()

h_gt = hashlib.sha256(gt_bytes).hexdigest().upper()
h_in = hashlib.sha256(in_bytes).hexdigest().upper()

print("\nSealed Artifact Hashes:")
print(f"stage_31_7_17_ground_truth.json: {h_gt} ({len(gt_bytes)} bytes)")
print(f"stage_31_7_17_blind_input.json:    {h_in} ({len(in_bytes)} bytes)")
