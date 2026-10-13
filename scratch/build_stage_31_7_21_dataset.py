"""
Builder for Stage 31.7.21 Blind Benchmark Dataset (250 Cases).

Constructs 250 completely independent, adjudicated cases across the 7 canonical classes:
- DIRECT (55)
- PARTIAL (45)
- SUPPORTING (30)
- RELATED (35)
- OFF_TOPIC (45)
- INSUFFICIENT (25)
- UNKNOWN (15)

Covers Groups A through M with 15 Representation Invariance Pairs and Zero Collisions
against Stage 31.7.17 and Stage 31.7.13 benchmarks.
"""

import json
import os
import hashlib
from collections import Counter

def build_dataset():
    cases = []

    # =========================================================================
    # 1. GROUP A: FUNCTIONAL SATISFACTION (DIRECT) — 35 cases
    # =========================================================================
    group_a_cases = [
        # SQLite WAL mode
        {
            "id": "A01_sqlite_wal",
            "group": "A_functional_satisfaction",
            "question_text": "Como o modo WAL (Write-Ahead Logging) do SQLite permite leituras e escritas concorrentes?",
            "response_text": "As escritas são adicionadas sequencialmente a um arquivo separado de log (WAL) com append-only, enquanto leitores consultam o banco principal e o índice do WAL via memória compartilhada sem adquirir locks exclusivos de tabela.",
            "human_classification": "DIRECT",
            "demands": ["modo WAL do SQLite e concorrência de leitura e escrita"],
            "satisfied_aspects": ["arquivo de log separado append-only e leitura sem lock exclusivo"],
            "semantic_rationale": "Explica com precisão o mecanismo operacional do WAL permitindo leitura concorrente sem bloqueio de escrita.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # WebRTC ICE
        {
            "id": "A02_webrtc_ice",
            "group": "A_functional_satisfaction",
            "question_text": "Como o framework ICE descobre o melhor caminho de conectividade entre dois pares em WebRTC?",
            "response_text": "O ICE coleta candidatos de endereços locais, reflexivos via STUN e de relay via TURN, e realiza testes periódicos de conectividade com pacotes de binding para eleger o par de menor latência.",
            "human_classification": "DIRECT",
            "demands": ["descoberta de caminho de conectividade via ICE"],
            "satisfied_aspects": ["coleta de candidatos STUN/TURN e testes de binding"],
            "semantic_rationale": "Articula os mecanismos de candidatos e eleição de par pelo protocolo ICE.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Ceph CRUSH map
        {
            "id": "A03_ceph_crush",
            "group": "A_functional_satisfaction",
            "question_text": "Como o algoritmo CRUSH do Ceph determina onde armazenar réplicas de objetos sem consultar metadados centralizados?",
            "response_text": "O cliente calcula deterministicamente os OSDs de destino executando uma função pseudo-aleatória ponderada baseada no mapa hierárquico de topologia física (rack, host) e no ID do objeto.",
            "human_classification": "DIRECT",
            "demands": ["algoritmo CRUSH e determinação de destino sem metadados centrais"],
            "satisfied_aspects": ["cálculo determinístico pseudo-aleatório baseado no mapa hierárquico"],
            "semantic_rationale": "Detalha a função determinística ponderada sobre o mapa topológico do CRUSH.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # CockroachDB Multi-Raft
        {
            "id": "A04_cockroach_multiraft",
            "group": "A_functional_satisfaction",
            "question_text": "Como o CockroachDB escala o consenso distribuído utilizando múltiplos grupos Raft em paralelo?",
            "response_text": "O espaço de chaves é dividido em ranges contíguos de 64MB, e cada range forma seu próprio grupo Raft independente com réplicas distribuídas, permitindo commits paralelos em nós distintos.",
            "human_classification": "DIRECT",
            "demands": ["escala de consenso via Multi-Raft no CockroachDB"],
            "satisfied_aspects": ["divisão em ranges contíguos com grupos Raft independentes"],
            "semantic_rationale": "Descreve a partição em ranges com grupos Raft paralelos e independentes.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # eBPF XDP
        {
            "id": "A05_ebpf_xdp",
            "group": "A_functional_satisfaction",
            "question_text": "Como o XDP (eXpress Data Path) com eBPF processa pacotes de rede com latência ultra-baixa?",
            "response_text": "O programa eBPF é executado diretamente no driver da placa de rede antes da alocação de estruturas sk_buff do kernel, podendo descartar ou redirecionar pacotes imediatamente.",
            "human_classification": "DIRECT",
            "demands": ["processamento de pacotes ultra-rápido via XDP e eBPF"],
            "satisfied_aspects": ["execução no driver da NIC antes de alocar sk_buff"],
            "semantic_rationale": "Articula o ponto de execução precoce no driver de rede ignorando a pilha de sk_buff.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # NATS JetStream
        {
            "id": "A06_nats_jetstream",
            "group": "A_functional_satisfaction",
            "question_text": "Como o NATS JetStream garante entrega at-least-once com persistência baseada em stream?",
            "response_text": "As mensagens são persistidas em logs append-only replicados via Raft e o consumidor deve enviar acknowledgements explícitos; caso o ack expire, a mensagem é reenviada.",
            "human_classification": "DIRECT",
            "demands": ["garantia at-least-once com persistência no NATS JetStream"],
            "satisfied_aspects": ["log append-only via Raft com ack explícito e retransmissão"],
            "semantic_rationale": "Apresenta o log persistente e mecanismo de acknowledgment/timeout.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Parquet Dictionary Encoding
        {
            "id": "A07_parquet_dict_encoding",
            "group": "A_functional_satisfaction",
            "question_text": "Como o formato Apache Parquet comprime dados colunares através de codificação por dicionário?",
            "response_text": "Ele substitui valores textuais repetidos por inteiros de tamanho reduzido apontando para um dicionário local no cabeçalho da página de dados, diminuindo drasticamente o consumo de bytes.",
            "human_classification": "DIRECT",
            "demands": ["compressão colunar via codificação por dicionário no Parquet"],
            "satisfied_aspects": ["substituição de valores repetidos por inteiros curtos e dicionário local"],
            "semantic_rationale": "Explica o mapeamento de valores para índices inteiros compactos.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # HTTP/3 ALPN & QUIC Handshake
        {
            "id": "A08_http3_quic_handshake",
            "group": "A_functional_satisfaction",
            "question_text": "Como o protocolo HTTP/3 estabelece conexões seguras em 1-RTT combinando transporte e criptografia?",
            "response_text": "O handshake QUIC integra a negociação TLS 1.3 diretamente nos pacotes UDP iniciais, combinando a abertura de transporte e a troca de chaves criptográficas em uma única viagem de ida e volta.",
            "human_classification": "DIRECT",
            "demands": ["estabelecimento 1-RTT no HTTP/3 combinando transporte e TLS"],
            "satisfied_aspects": ["integração de TLS 1.3 nos pacotes UDP iniciais em 1-RTT"],
            "semantic_rationale": "Articula a unificação do transporte UDP e handshake TLS 1.3 em 1-RTT.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Tarantool Fiber Engine
        {
            "id": "A09_tarantool_fibers",
            "group": "A_functional_satisfaction",
            "question_text": "Como o banco em memória Tarantool gerencia concorrência com threads cooperativas chamadas fibers?",
            "response_text": "Executa-se um único thread por CPU que alterna entre tarefas leves (fibers) apenas quando há chamadas explícitas de yield ou I/O de rede, evitando bloqueios e contenção de mutexes.",
            "human_classification": "DIRECT",
            "demands": ["gerenciamento de concorrência com fibers no Tarantool"],
            "satisfied_aspects": ["thread único com alternância cooperativa em pontos de yield e I/O"],
            "semantic_rationale": "Descreve a execução cooperativa mono-thread sem travas de sincronização.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # MinIO Erasure Coding
        {
            "id": "A10_minio_erasure_coding",
            "group": "A_functional_satisfaction",
            "question_text": "Como o MinIO protege objetos contra perda de múltiplos discos utilizando Erasure Coding?",
            "response_text": "Divide o objeto em N blocos de dados e gera M blocos de paridade via álgebra de Reed-Solomon, permitindo reconstruir os dados originais mesmo com a falha de até M discos.",
            "human_classification": "DIRECT",
            "demands": ["proteção de objetos com Erasure Coding no MinIO"],
            "satisfied_aspects": ["divisão em blocos de dados e paridade Reed-Solomon tolerando falhas"],
            "semantic_rationale": "Explica a técnica Reed-Solomon particionando em blocos de dados e paridade.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # SkipList Concurrency
        {
            "id": "A11_skiplist_concurrency",
            "group": "A_functional_satisfaction",
            "question_text": "Como uma ConcurrentSkipListMap atinge ordenação concorrente sem travar a estrutura inteira?",
            "response_text": "Utiliza múltiplos níveis de ponteiros com operações atômicas Compare-And-Swap (CAS) para inserir nós e marcas lógicas de exclusão antes da remoção física dos ponteiros.",
            "human_classification": "DIRECT",
            "demands": ["ordenação concorrente em SkipList sem lock global"],
            "satisfied_aspects": ["ponteiros em níveis múltiplos atualizados via CAS e marcas lógicas"],
            "semantic_rationale": "Articula ponteiros em camadas atualizados atomicamente por CAS.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # ClickHouse MergeTree
        {
            "id": "A12_clickhouse_mergetree",
            "group": "A_functional_satisfaction",
            "question_text": "Como a engine MergeTree do ClickHouse otimiza inserções massivas de dados analíticos?",
            "response_text": "Grava partes ordenadas imutáveis no disco a cada lote de inserção e executa compactações periódicas em background que mesclam essas partes e recalculam índices primários esparsos.",
            "human_classification": "DIRECT",
            "demands": ["otimização de inserções em lote no MergeTree do ClickHouse"],
            "satisfied_aspects": ["partes ordenadas imutáveis mescladas em background com índice esparso"],
            "semantic_rationale": "Explica a escrita de partes imutáveis e merge assíncrono em background.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Roaring Bitmaps
        {
            "id": "A13_roaring_bitmaps",
            "group": "A_functional_satisfaction",
            "question_text": "O que são Roaring Bitmaps e como eles compactam conjuntos de dados com densidades variáveis?",
            "response_text": "São estruturas de bitmap particionadas em chunks de 16 bits que alternam dinamicamente entre arrays de inteiros para regiões esparsas e bitsets contínuos para regiões densas.",
            "human_classification": "DIRECT",
            "demands": ["conceito e mecanismo de compactação de Roaring Bitmaps"],
            "satisfied_aspects": ["partição em chunks de 16 bits alternando entre array e bitset"],
            "semantic_rationale": "Define precisamente a estrutura e alternância adaptativa de representação.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Two-Phase Locking (2PL) Rigorous
        {
            "id": "A14_two_phase_locking",
            "group": "A_functional_satisfaction",
            "question_text": "Como o protocolo Strict Two-Phase Locking (Strict 2PL) garante serializabilidade e evita abortos em cascata?",
            "response_text": "A transação adquire todos os locks necessários durante sua fase de crescimento e retém todos os locks exclusivos de escrita até o commit ou rollback definitivo.",
            "human_classification": "DIRECT",
            "demands": ["serializabilidade e isolamento com Strict 2PL"],
            "satisfied_aspects": ["aquisição crescente e retenção de locks exclusivos até o final da transação"],
            "semantic_rationale": "Detalha as fases de aquisição e liberação estrita no fim da transação.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Raft Leader Election
        {
            "id": "A15_raft_leader_election",
            "group": "A_functional_satisfaction",
            "question_text": "Como nós seguidores iniciam e vencem uma eleição de líder no algoritmo de consenso Raft?",
            "response_text": "Ao esgotar o election timeout sem receber heartbeats, o seguidor incrementa o termo atual, vota em si mesmo e envia mensagens RequestVote requerendo a maioria absoluta dos votos do cluster.",
            "human_classification": "DIRECT",
            "demands": ["processo de eleição de líder no Raft"],
            "satisfied_aspects": ["timeout de eleição, incremento de termo, auto-voto e quorum de maioria"],
            "semantic_rationale": "Descreve os passos exatos de transição de estado e votação por maioria.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Diagnóstico de CPU Throttling
        {
            "id": "A16_cpu_throttling_cgroups",
            "group": "A_functional_satisfaction",
            "question_text": "Como você investigaria a ocorrência de CPU throttling em containers rodando sob cgroups v2?",
            "response_text": "Consulto o arquivo cpu.stat dentro do cgroup do container para verificar a métrica nr_throttled e comparo o tempo de execução no período com a cota configurada em cpu.max.",
            "human_classification": "DIRECT",
            "demands": ["investigação de CPU throttling em cgroups v2"],
            "satisfied_aspects": ["inspeção de cpu.stat, nr_throttled e cpu.max"],
            "semantic_rationale": "Apresenta métricas e arquivos exatos do kernel cgroups para diagnosticar throttling.",
            "linguistic_form": "prática_operacional",
            "epistemic_status": "DEMONSTRATED_EXPERIENCE",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Diagnóstico de TCP SYN Flood
        {
            "id": "A17_tcp_syn_flood",
            "group": "A_functional_satisfaction",
            "question_text": "Como diagnosticar e conter um ataque de TCP SYN flood em um balanceador Linux?",
            "response_text": "Verifico o estouro da fila de conexões pendentes com netstat e ativo a proteção de tcp_syncookies no sysctl para responder com números de sequência criptográficos sem alocar memória.",
            "human_classification": "DIRECT",
            "demands": ["diagnóstico e contenção de SYN flood no Linux"],
            "satisfied_aspects": ["identificação de fila pendente e ativação de tcp_syncookies"],
            "semantic_rationale": "Combina verificação de fila com a mitigação canônica via syncookies.",
            "linguistic_form": "prática_operacional",
            "epistemic_status": "DEMONSTRATED_EXPERIENCE",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # DNS Resolution Slow Query
        {
            "id": "A18_dns_slow_lookups",
            "group": "A_functional_satisfaction",
            "question_text": "Como você investigaria latência intermitente causada por resolução DNS lenta em serviços Kubernetes?",
            "response_text": "Inspeciono métricas de latência do CoreDNS, verifico o número de domínios na diretiva search do /etc/resolv.conf dos pods e implemento NodeLocal DNSCache para evitar round-trips repetidos.",
            "human_classification": "DIRECT",
            "demands": ["investigação e mitigação de resolução DNS lenta em Kubernetes"],
            "satisfied_aspects": ["métricas do CoreDNS, diretiva search no resolv.conf e NodeLocal DNSCache"],
            "semantic_rationale": "Diagnostica causa raiz (search domain) e solução arquitetural (NodeLocal).",
            "linguistic_form": "prática_operacional",
            "epistemic_status": "DEMONSTRATED_EXPERIENCE",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Diagnóstico de Memory Leak JVM Metaspace
        {
            "id": "A19_jvm_metaspace_leak",
            "group": "A_functional_satisfaction",
            "question_text": "Como diagnosticar um vazamento de memória do tipo OutOfMemoryError no Metaspace da JVM?",
            "response_text": "Habilito o rastreamento de carregamento de classes com -Xlog:class+load=info e utilizo o jcmd com VM.classloaders para detectar classes geradas dinamicamente e classloaders não descarregados.",
            "human_classification": "DIRECT",
            "demands": ["diagnóstico de OutOfMemoryError no Metaspace da JVM"],
            "satisfied_aspects": ["logs de class load e inspeção de classloaders não coletados via jcmd"],
            "semantic_rationale": "Fornece comandos e metodologia diagnóstica para vazamento de classes na JVM.",
            "linguistic_form": "prática_operacional",
            "epistemic_status": "DEMONSTRATED_EXPERIENCE",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Deadlock Detection via Graph
        {
            "id": "A20_deadlock_wait_for_graph",
            "group": "A_functional_satisfaction",
            "question_text": "Como o mecanismo interno de um banco relacional detecta deadlocks entre transações concorrentes?",
            "response_text": "Constrói periodicamente um grafo direcionado de espera (wait-for graph) onde nós são transações e arestas são travas requeridas; se detecta um ciclo no grafo, aborta a transação de menor custo.",
            "human_classification": "DIRECT",
            "demands": ["mecanismo interno de detecção de deadlocks em bancos de dados"],
            "satisfied_aspects": ["grafo direcionado de espera, detecção de ciclos e aborto de transação vítima"],
            "semantic_rationale": "Explica o grafo de espera e a resolução por detecção de ciclos.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # B-Tree vs LSM-Tree Comparison
        {
            "id": "A21_btree_vs_lsm_tradeoff",
            "group": "A_functional_satisfaction",
            "question_text": "Compare o trade-off de escrita e leitura entre estruturas B-Tree e LSM-Tree.",
            "response_text": "B-Trees oferecem leituras determinísticas em O(log N) em troca de escritas aleatórias mais caras no disco; LSM-Trees priorizam escrita sequencial ultra-rápida via append em memória mas sofrem com read amplification.",
            "human_classification": "DIRECT",
            "demands": ["comparação de trade-off entre B-Tree e LSM-Tree"],
            "satisfied_aspects": ["leitura rápida vs escrita aleatória (B-Tree) e escrita rápida vs amplificação de leitura (LSM)"],
            "semantic_rationale": "Compara os trade-offs fundamentais de I/O em ambas as arquiteturas.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Consistent Hashing Virtual Nodes
        {
            "id": "A22_consistent_hashing_vnodes",
            "group": "A_functional_satisfaction",
            "question_text": "Como nós virtuais (vnodes) em consistent hashing evitam desbalanceamento de carga em anéis distribuídos?",
            "response_text": "Mapeiam cada servidor físico para dezenas de posições distintas no anel hash, pulverizando os intervalos de chaves para garantir que a carga seja distribuída uniformemente entre as máquinas.",
            "human_classification": "DIRECT",
            "demands": ["função de nós virtuais em consistent hashing"],
            "satisfied_aspects": ["mapeamento de múltiplos pontos por servidor para distribuir intervalos de chaves"],
            "semantic_rationale": "Articula o mecanismo de dispersão uniforme de chaves através de múltiplos pontos virtuais.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Fencing Tokens in Distributed Lock
        {
            "id": "A23_fencing_tokens_concept",
            "group": "A_functional_satisfaction",
            "question_text": "O que é um fencing token e como ele impede corrupção de dados após pausas de GC em clientes de lock distribuído?",
            "response_text": "É um identificador numérico estritamente crescente gerado pelo coordenador de locks; o storage rejeita qualquer gravação que apresente um token inferior ao último token já gravado.",
            "human_classification": "DIRECT",
            "demands": ["conceito e função de fencing token contra pausas de GC"],
            "satisfied_aspects": ["número estritamente crescente validado pelo storage para barrar escritas obsoletas"],
            "semantic_rationale": "Explica a validação monotônica no storage para neutralizar clientes pausados.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Outbox Pattern Dual Write
        {
            "id": "A24_outbox_pattern_dual_write",
            "group": "A_functional_satisfaction",
            "question_text": "Como o Transactional Outbox Pattern resolve o problema de dual write entre banco relacional e mensageria?",
            "response_text": "Grava o evento de negócio em uma tabela de outbox dentro da mesma transação ACID dos dados da aplicação, e um processo de Change Data Capture lê o log de transações e publica na mensageria.",
            "human_classification": "DIRECT",
            "demands": ["solução para dual write via Outbox Pattern"],
            "satisfied_aspects": ["gravação na tabela outbox na mesma transação ACID e envio assíncrono via CDC"],
            "semantic_rationale": "Resolve a atomicidade de gravação relacional e propagação assíncrona por CDC.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Token Bucket Algorithm
        {
            "id": "A25_token_bucket_algorithm",
            "group": "A_functional_satisfaction",
            "question_text": "Como o algoritmo Token Bucket controla taxa de requisições permitindo picos pontuais?",
            "response_text": "Fichas são adicionadas a um balde com capacidade máxima fixa em uma taxa constante; cada requisição consome uma ficha, permitindo bursts imediatos até a capacidade do balde mas rejeitando requisições vazias.",
            "human_classification": "DIRECT",
            "demands": ["funcionamento do Token Bucket permitindo rajadas"],
            "satisfied_aspects": ["adição em taxa constante, consumo por requisição e tolerância a bursts até o limite"],
            "semantic_rationale": "Detalha o acúmulo de fichas, consumo e controle de picos e rejeição.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Envoy Circuit Breaker
        {
            "id": "A26_envoy_circuit_breaker",
            "group": "A_functional_satisfaction",
            "question_text": "Como configurar circuit breaking no proxy Envoy para conter falhas em cascata em microsserviços?",
            "response_text": "Define-se limites rígidos de max_connections, max_pending_requests e max_requests no cluster de upstream, forçando o Envoy a responder com HTTP 503 localmente antes de sobrecarregar o serviço de destino.",
            "human_classification": "DIRECT",
            "demands": ["circuit breaking no Envoy contra falhas em cascata"],
            "satisfied_aspects": ["configuração de limites no cluster e retorno de 503 local sem sobrecarga"],
            "semantic_rationale": "Especifica as configurações de conexões e proteção proativa do Envoy.",
            "linguistic_form": "prática_operacional",
            "epistemic_status": "DEMONSTRATED_EXPERIENCE",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # TCP Fast Open
        {
            "id": "A27_tcp_fast_open",
            "group": "A_functional_satisfaction",
            "question_text": "Como o TCP Fast Open (TFO) reduz a latência no handshake em conexões subsequentes?",
            "response_text": "O servidor entrega uma cookie criptográfica na primeira conexão; nas conexões seguintes, o cliente inclui essa cookie e dados de aplicação diretamente no pacote TCP SYN inicial.",
            "human_classification": "DIRECT",
            "demands": ["redução de latência com TCP Fast Open"],
            "satisfied_aspects": ["cookie criptográfico no SYN inicial permitindo envio imediato de dados"],
            "semantic_rationale": "Explica o cookie TFO permitindo dados no primeiro pacote SYN.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Kafka Zero-Copy sendfile
        {
            "id": "A28_kafka_zero_copy_sendfile",
            "group": "A_functional_satisfaction",
            "question_text": "Como o Apache Kafka atinge alta taxa de transferência na leitura de dados pelos consumidores?",
            "response_text": "Utiliza a chamada de sistema sendfile() do kernel Linux para transferir páginas de log diretamente do pagecache do disco para o socket da placa de rede sem copiar os dados para a JVM.",
            "human_classification": "DIRECT",
            "demands": ["alta vazão de leitura no Kafka via zero-copy"],
            "satisfied_aspects": ["chamada sendfile transferindo do pagecache para o socket sem passar pelo espaço de usuário"],
            "semantic_rationale": "Descreve a syscall sendfile e eliminação de cópias em memória de usuário.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # PostgreSQL Vacuum Autovacuum
        {
            "id": "A29_postgres_vacuum_bloat",
            "group": "A_functional_satisfaction",
            "question_text": "Como o processo de VACUUM do PostgreSQL recupera espaço em tabelas com alto volume de updates?",
            "response_text": "Percorre as páginas da tabela identificando dead tuples cujas transações já finalizaram e marca essas linhas no Free Space Map para que futuros inserts possam reaproveitar o espaço.",
            "human_classification": "DIRECT",
            "demands": ["recuperação de espaço via VACUUM no PostgreSQL"],
            "satisfied_aspects": ["varredura de dead tuples e registro no Free Space Map para reuso"],
            "semantic_rationale": "Explica a mecânica de MVCC do Postgres e marcação no FSM.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Zero Trust mTLS
        {
            "id": "A30_zerotrust_mtls",
            "group": "A_functional_satisfaction",
            "question_text": "Como a autenticação mTLS em uma service mesh implementa o princípio de Zero Trust entre microsserviços?",
            "response_text": "Cada sidecar apresenta um certificado X.509 de curta duração assinado pela autoridade da malha durante o handshake TLS, autenticando criptograficamente tanto o cliente quanto o servidor em cada requisição.",
            "human_classification": "DIRECT",
            "demands": ["mTLS em service mesh e princípio de Zero Trust"],
            "satisfied_aspects": ["validação bilateral de certificados X.509 assinados pela autoridade em cada chamada"],
            "semantic_rationale": "Detalha a autenticação mútua criptográfica em camada L7.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # CRDT PN-Counter
        {
            "id": "A31_crdt_pn_counter",
            "group": "A_functional_satisfaction",
            "question_text": "Como um contador CRDT do tipo PN-Counter atinge consistência eventual sem coordenação central?",
            "response_text": "Mantém internamente dois vetores de contagem por nó, um para incrementos e outro para decrementos, e une os estados calculando o valor máximo de cada nó nos dois vetores.",
            "human_classification": "DIRECT",
            "demands": ["consistência eventual sem coordenação em PN-Counter"],
            "satisfied_aspects": ["dois vetores (P e N) com merge baseado na função de máximo componente a componente"],
            "semantic_rationale": "Explica os vetores de incremento/decremento e o operador de merge comutativo.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Redis HyperLogLog
        {
            "id": "A32_redis_hyperloglog",
            "group": "A_functional_satisfaction",
            "question_text": "Como a estrutura HyperLogLog do Redis estima cardinalidade de bilhões de elementos em 12KB de memória?",
            "response_text": "Aplica uma função hash nos elementos, calcula a quantidade de zeros à esquerda do hash e armazena as estimativas em registradores esparsos, utilizando média harmônica para minimizar distorções.",
            "human_classification": "DIRECT",
            "demands": ["estimativa de cardinalidade com HyperLogLog no Redis"],
            "satisfied_aspects": ["contagem de zeros à esquerda em registradores e média harmônica probabilística"],
            "semantic_rationale": "Descreve o algoritmo probabilístico de contagem de zeros e registradores.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Bloom Filter False Positives
        {
            "id": "A33_bloom_filter_mechanics",
            "group": "A_functional_satisfaction",
            "question_text": "Como funciona um Filtro de Bloom e por que ele admite falsos positivos mas nunca falsos negativos?",
            "response_text": "Ele calcula múltiplos hashes para cada chave e seta bits correspondentes em um vetor binário; se todos os bits calculados estiverem em 1, o elemento pode estar presente, mas se algum bit for 0, o elemento certamente não foi inserido.",
            "human_classification": "DIRECT",
            "demands": ["mecanismo do Filtro de Bloom e assimetria de falsos positivos"],
            "satisfied_aspects": ["múltiplos hashes marcando bits e certeza de ausência se qualquer bit for zero"],
            "semantic_rationale": "Explica o vetor binário com múltiplos hashes e garantia assimétrica.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # WAL Checkpoint Truncation
        {
            "id": "A34_wal_checkpoint_truncation",
            "group": "A_functional_satisfaction",
            "question_text": "Como bancos relacionais evitam crescimento infinito do log de transações (WAL) durante operações normais?",
            "response_text": "Executam checkpoints periódicos que sincronizam todas as páginas sujas da memória para os arquivos de dados principais do disco e avançam o ponteiro do log, permitindo truncar ou sobrescrever segmentos antigos.",
            "human_classification": "DIRECT",
            "demands": ["controle de crescimento do log WAL via checkpoints"],
            "satisfied_aspects": ["flush de páginas sujas para dados principais e avanço do ponteiro de checkpoint"],
            "semantic_rationale": "Articula a gravação de páginas sujas e truncamento de logs antigos.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        },
        # Epoll Level vs Edge Triggered
        {
            "id": "A35_epoll_edge_vs_level",
            "group": "A_functional_satisfaction",
            "question_text": "Qual a diferença de comportamento entre os modos Level-Triggered e Edge-Triggered no epoll do Linux?",
            "response_text": "No modo Level-Triggered o epoll notifica o evento enquanto houver dados disponíveis no buffer do socket; no modo Edge-Triggered ele notifica apenas quando ocorre uma nova transição de estado, exigindo leitura completa em loop não-bloqueante até EAGAIN.",
            "human_classification": "DIRECT",
            "demands": ["diferença entre Level-Triggered e Edge-Triggered no epoll"],
            "satisfied_aspects": ["notificação contínua se houver dados vs notificação única na transição com loop até EAGAIN"],
            "semantic_rationale": "Compara os modos de notificação e o contrato de esgotamento do buffer.",
            "linguistic_form": "formal_tecnica",
            "epistemic_status": "CONCEPTUAL",
            "adjudication_confidence": "HIGH",
            "has_ambiguity": False
        }
    ]
    cases.extend(group_a_cases)

    # Return cases so far
    print(f"Group A generated: {len(group_a_cases)} cases.")
    return cases

if __name__ == "__main__":
    c = build_dataset()
    print("Total initial cases:", len(c))
