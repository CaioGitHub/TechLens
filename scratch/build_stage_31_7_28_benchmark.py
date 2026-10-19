import json
import hashlib
from pathlib import Path
from collections import Counter

# Load prior benchmark questions & responses to check overlap
prior_benchmarks = [
    "11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_17_ground_truth.json",
    "11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_21_ground_truth.json",
    "11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05/stage_31_7_25_ground_truth.json"
]

prior_q = set()
prior_r = set()
for pb in prior_benchmarks:
    p = Path(pb)
    if p.exists():
        d = json.load(open(p, encoding="utf-8"))
        cases = d if isinstance(d, list) else d.get("cases", [])
        for c in cases:
            q = c.get("question_text") or c.get("question")
            r = c.get("response_text") or c.get("response")
            if q: prior_q.add(q.strip().lower())
            if r: prior_r.add(r.strip().lower())

print(f"Loaded {len(prior_q)} prior questions and {len(prior_r)} prior responses for anti-overlap auditing.")

all_cases = []
current_id = 1

def add_case(group, semantic_family, q, r, ref_rel, rationale, q_type, ling_form, pair_id=None):
    global current_id
    cid = f"VAL-31-7-28-{current_id:03d}"
    current_id += 1
    
    # Audit overlap
    q_clean = q.strip().lower()
    r_clean = r.strip().lower()
    if q_clean in prior_q:
        raise ValueError(f"DUPLICATE QUESTION DETECTED: {q}")
    if r_clean in prior_r:
        raise ValueError(f"DUPLICATE RESPONSE DETECTED: {r}")
        
    case = {
        "id": cid,
        "group": group,
        "semantic_family": semantic_family,
        "question_text": q.strip(),
        "response_text": r.strip(),
        "reference_relevance": ref_rel,
        "adjudication_rationale": rationale.strip(),
        "question_type": q_type,
        "linguistic_form": ling_form,
        "invariance_pair_id": pair_id
    }
    all_cases.append(case)

# ==============================================================================
# GROUP A: DIRECT (Target: 50 cases)
# ==============================================================================
# Fam 1: Direct with lexical overlap
add_case("A_direct", "01_direct_with_lexical_overlap",
    "Como configurar o pool de conexoes do banco para evitar esgotamento de conexoes em picos de requisicao?",
    "Ajustamos o max_connections no banco e o maximumPoolSize no HikariCP para limitar as conexoes ativas e configuramos o connectionTimeout para falhar rapidamente quando o limite for atingido.",
    "DIRECT", "Atende diretamente as configuracoes necessarias de limite e timeout para evitar esgotamento.", "implementation", "formal_technical")

add_case("A_direct", "01_direct_with_lexical_overlap",
    "Como implementar paginacao baseada em cursor em tabelas com milhoes de registros?",
    "Utilizamos o valor do ultimo ID ou timestamp visto na clausula WHERE com operador maior que e ordenamos pela coluna indexada com LIMIT estrito.",
    "DIRECT", "Explica o mecanismo causal exato de paginacao por cursor com WHERE e coluna indexada.", "implementation", "formal_technical")

add_case("A_direct", "01_direct_with_lexical_overlap",
    "Como o Redis lida com a expiracao de chaves para liberar espaco na memoria?",
    "O Redis combina amostragem aleatoria periodica de chaves com TTL e verificacao passiva no momento em que a chave e acessada para expira-la se estiver vencida.",
    "DIRECT", "Descreve com precisao o algoritmo ativo e passivo de expiracao de chaves do Redis.", "explanation", "formal_technical")

# Fam 2: Direct without lexical overlap
add_case("A_direct", "02_direct_no_lexical_overlap",
    "Como assegurar que dados sensiveis nao fiquem expostos na camada de persistencia?",
    "Aplicamos criptografia de envelope em repouso nos discos do storage e ofuscamos colunas criticas com funcoes hash criptograficas salgadas.",
    "DIRECT", "Resolve plenamente a demanda de seguranca de persistencia sem repetir termos da pergunta.", "implementation", "formal_technical")

add_case("A_direct", "02_direct_no_lexical_overlap",
    "Como garantir que escritas concorrentes no mesmo saldo nao resultem em atualizacoes perdidas?",
    "Executamos a verificacao de versao no momento da confirmacao do registro e abortamos a operacao caso ocorra divergencia entre a versao lida e a atual.",
    "DIRECT", "Descreve o mecanismo funcional de controle de concorrencia otimista sem usar jargoes redundantes.", "implementation", "formal_technical")

add_case("A_direct", "02_direct_no_lexical_overlap",
    "Como manter a sincronia de configuracoes entre multiplas instancias sem necessidade de reinicializacao?",
    "Subscrevemos as instancias a um topico de mensageria que dissemina eventos de mudanca para recarregar os parametros dinamicamente na memoria dos nós.",
    "DIRECT", "Explica o mecanismo de propagacao reativa de configuracao dinamicamente.", "architecture", "formal_technical")

# Fam 9: Conceptual Definitions (Idempotence, Dependency Inversion, etc.)
add_case("A_direct", "09_conceptual_definition",
    "O que e o principio da Inversao de Dependencia na arquitetura de software?",
    "E o principio que estipula que modulos de alto nivel nao devem depender de modulos de baixo nivel, e sim ambos dependerem de abstracoes e contratos estaveis.",
    "DIRECT", "Define conceitualmente com rigor e exatidao o principio SOLID da inversao de dependencia.", "definition", "concise_conceptual")

add_case("A_direct", "09_conceptual_definition",
    "O que significa a propriedade de idempotencia em servicos web REST?",
    "E a garantia formal de que multiplas invocacoes consecutivas e identicas de uma requisicao produzem exatamente o mesmo estado final no servidor que uma unica invocacao.",
    "DIRECT", "Define a propriedade formal de idempotencia sem exigir codigo de implementacao.", "definition", "concise_conceptual")

add_case("A_direct", "09_conceptual_definition",
    "O que e isolamento Snapshot Isolation em bancos de dados relacionais?",
    "E o nivel de isolamento onde cada transacao enxerga uma fotografia consistente do estado dos dados no instante em que a transacao foi iniciada.",
    "DIRECT", "Define conceitualmente a semantica de Snapshot Isolation.", "definition", "concise_conceptual")

add_case("A_direct", "09_conceptual_definition",
    "O que significa o principio da Responsabilidade Unica no design de software?",
    "E a diretriz segundo a qual uma classe ou modulo deve possuir um unico motivo para mudar, concentrando apenas uma responsabilidade de negocio.",
    "DIRECT", "Define adequadamente o principio da responsabilidade unica.", "definition", "concise_conceptual")

# Fam 10: Historical Questions
add_case("A_direct", "10_historical_questions",
    "Por que o ecossistema Linux adotou um kernel monolitico em vez de um microkernel?",
    "Porque na epoca da sua criacao o kernel monolitico oferecia melhor desempenho em chamadas de sistema eliminando o overhead de troca de contexto de IPC presente nos microkernels.",
    "DIRECT", "Responde diretamente a razao historica e tecnica da escolha arquitetural do kernel Linux.", "historical", "formal_technical")

add_case("A_direct", "10_historical_questions",
    "Por que o protocolo HTTP/2 introduziu a multiplexacao de streams em uma unica conexao TCP?",
    "Para superar o bloqueio de cabeca de fila no navegador e eliminar a necessidade de abrir multiplas conexoes TCP simultaneas para carregar assets.",
    "DIRECT", "Explica com precisao historica e tecnica a motivacao do HTTP/2.", "historical", "formal_technical")

add_case("A_direct", "10_historical_questions",
    "Por que o Git foi projetado originalmente com uma estrutura de grafo aciclico dirigido (DAG)?",
    "Para viabilizar ramificacoes e fusoes nao lineares extremamente rapidas garantindo integridade de historico imutavel via apontadores de commits.",
    "DIRECT", "Explica a motivacao historica e funcional do design de DAG no Git.", "historical", "formal_technical")

# Fam 11: Comparative Questions
add_case("A_direct", "11_comparative_questions",
    "Qual e a diferenca fundamental entre processos e threads no gerenciamento de memoria pelo SO?",
    "Processos possuem espacos de enderecamento de memoria completamente isolados entre si, enquanto threads pertencentes a um mesmo processo compartilham o mesmo espaco virtual de memoria.",
    "DIRECT", "Atende com perfeicao os eixos de comparacao de isolamento e compartilhamento de memoria.", "comparison", "formal_technical")

add_case("A_direct", "11_comparative_questions",
    "Qual a diferenca entre indices baseados em B-Tree e LSM-Tree quanto ao perfil de operacoes?",
    "Indices B-Tree oferecem leituras pontuais mais rapidas com atualizacoes no proprio local do disco, enquanto LSM-Trees priorizam throughput de escrita realizando gravações sequenciais em log e compactacoes em lote.",
    "DIRECT", "Compara adequadamente os trade-offs de leitura e escrita entre B-Tree e LSM-Tree.", "comparison", "formal_technical")

add_case("A_direct", "11_comparative_questions",
    "Qual a diferenca entre autenticacao baseada em tokens JWT e sessoes stateful armazenadas no servidor?",
    "Tokens JWT sao stateless e carregam as claims assinadas criptograficamente dentro do proprio payload, enquanto sessoes stateful mantem o estado do usuario na memoria ou banco do servidor referenciado por um session ID.",
    "DIRECT", "Compara precisamente stateless vs stateful entre JWT e sessao.", "comparison", "formal_technical")

add_case("A_direct", "11_comparative_questions",
    "Qual a diferenca entre consistencia forte e consistencia eventual em sistemas distribuidos?",
    "Na consistencia forte qualquer leitura retorna imediatamente a escrita mais recente confirmada por todos os nos, enquanto na consistencia eventual as replicas convergem para o mesmo valor apos um intervalo de tempo sem garantias de sincronia imediata.",
    "DIRECT", "Diferencia com exatidao conceitual consistencia forte e eventual.", "comparison", "formal_technical")

# Fam 12: Diagnosis and Investigation
add_case("A_direct", "12_diagnosis_and_investigation",
    "Como diagnosticar vazamentos de memoria causados por conexoes nao fechadas no pool HikariCP?",
    "Inspecionamos thread dumps para identificar threads presas em estado blocked ou waiting e analisamos as metricas de conexoes ativas que nunca retornam ao pool dentro do bloco try-with-resources.",
    "DIRECT", "Apresenta o procedimento investigativo correto com thread dumps e analise de ciclo de vida.", "diagnosis", "formal_technical")

add_case("A_direct", "12_diagnosis_and_investigation",
    "Como identificar a causa raiz de throttling de CPU em containers sob execucao no Kubernetes?",
    "Analisamos a metrica container_cpu_cfs_throttled_periods_total em relacao aos limites de cpu definidos no pod e verificamos se ha threads paralelas disputando ciclos alem do cfs_quota configurado.",
    "DIRECT", "Explica o diagnostico causal de throttling via metricas de CFS e quotas.", "diagnosis", "formal_technical")

add_case("A_direct", "12_diagnosis_and_investigation",
    "Como descobrir por que uma consulta SQL com indice esta executando com Table Scan?",
    "Executamos o comando EXPLAIN ANALYZE para inspecionar o plano de execucao e verificamos se funcoes aplicadas na coluna ou tipos de dados inconversiveis estao anulando o uso do indice.",
    "DIRECT", "Apresenta o metodo de diagnostico correto com plano de execucao e verificacao de sargability.", "diagnosis", "formal_technical")

# Fam 13: Implementation Questions
add_case("A_direct", "13_implementation_questions",
    "Como configurar autenticacao mutua TLS (mTLS) entre microsservicos?",
    "Configuramos certificados X.509 assinados por uma CA interna em ambos os lados e exigimos validacao do certificado cliente no handshake SSL do servidor com client-auth ativado.",
    "DIRECT", "Descreve a implementacao correta de mTLS com certificados e validacao bilateral.", "implementation", "formal_technical")

add_case("A_direct", "13_implementation_questions",
    "Como implementar um mecanismo de rate limiting distribuido com janela deslizante?",
    "Utilizamos estruturas de dados Sorted Set no Redis onde cada requisicao grava um timestamp como score e removemos registros anteriores a janela atual contando os elementos restantes com ZCARD.",
    "DIRECT", "Explica o algoritmo de janela deslizante distribuida com Sorted Sets no Redis.", "implementation", "formal_technical")

add_case("A_direct", "13_implementation_questions",
    "Como configurar dead letter queues no RabbitMQ para mensagens rejeitadas?",
    "Definimos o argumento x-dead-letter-exchange na fila principal apontando para uma exchange dedicada e associamos uma fila de descarte para acolher mensagens rejeitadas com requeue false.",
    "DIRECT", "Detalha os parametros e fluxo de DLQ no RabbitMQ.", "implementation", "formal_technical")

# Fam 14: Colloquial engineering phrasing and passive voice
add_case("A_direct", "18_colloquial_and_passive",
    "Como evitar que um servico caia quando uma dependencia externa fica instavel?",
    "E colocado um circuit breaker no meio do fluxo pra cortar a comunicacao se der muitas falhas e a aplicacao responde com fallback sem prender as requisicoes.",
    "DIRECT", "Linguagem coloquial expressando a solucao funcional correta do circuit breaker.", "architecture", "colloquial_engineering", pair_id="PAIR_01_A")

add_case("A_direct", "18_colloquial_and_passive",
    "Como proteger uma API contra lentidao causada por consultas pesadas repetidas?",
    "Sao cacheadas as respostas no Redis com um tempo de vida curto para que as requisicoes subsequentes sejam servidas diretamente da memoria sem bater no banco.",
    "DIRECT", "Voz passiva sintatica descrevendo solucao valida de cache em memoria.", "implementation", "passive_voice", pair_id="PAIR_02_A")

add_case("A_direct", "18_colloquial_and_passive",
    "Como distribuir o processamento de tarefas pesadas em background sem travar a interface do usuario?",
    "A gente despacha a carga numa fila assincrona com workers consumindo os jobs em segundo plano e notifica o front via websocket quando terminar.",
    "DIRECT", "Expressao coloquial de engenharia que atende com rigor a demanda de processamento assincrono.", "architecture", "colloquial_engineering", pair_id="PAIR_03_A")

# Fam 21: Unseen/Fictional Technologies with sound mechanism
add_case("A_direct", "21_unseen_technologies",
    "Como o banco de dados distribuido ChronoStore resolve conflitos de particionamento?",
    "O ChronoStore utiliza carimbos logicos de relogios vetoriais para detectar divergencias concorrentes e aplica resolucao deterministica baseada no maior timestamp com reconciliacao de replicas.",
    "DIRECT", "Tecnologia ficticia operando sob mecanismo funcional distribuido valido.", "architecture", "formal_technical")

add_case("A_direct", "21_unseen_technologies",
    "Como a camada de comunicacao QuantumMesh garante entrega confiavel de eventos sob alta perda de pacotes?",
    "O QuantumMesh fragmenta as mensagens em blocos com codificacao de correcao de erros por erasure coding e retransmite blocos faltantes via acknowledgments seletivos.",
    "DIRECT", "Tecnologia inedita descrita com principio solido de erasure coding e retransmissao seletiva.", "architecture", "formal_technical")

# Fam 19: Short precise definitions
add_case("A_direct", "19_short_precise_answers",
    "O que e um deadlock em sistemas concorrentes?",
    "E a situacao onde dois ou mais processos ficam bloqueados indefinidamente porque cada um retem um recurso que o outro necessita para prosseguir.",
    "DIRECT", "Definicao concisa e perfeita de deadlock.", "definition", "concise_conceptual")

add_case("A_direct", "19_short_precise_answers",
    "O que e o algoritmo Consistent Hashing em sistemas de cache distribuido?",
    "E o algoritmo que mapeia chaves e servidores em um anel circular para minimizar a redistribuicao de dados quando nos sao adicionados ou removidos.",
    "DIRECT", "Definicao curta e precisa de consistent hashing.", "definition", "concise_conceptual")

# Fam 17: Dense propositions satisfying multiple demands
add_case("A_direct", "07_dense_compound_fulfillment",
    "Como o Kafka particiona mensagens e garante a ordenacao na entrega?",
    "O Kafka direciona a mensagem para uma particao calculando o hash da chave do registro, onde um offset sequencial monotonicamente crescente assegura a ordem estrita de entrega aos consumidores.",
    "DIRECT", "Uma unica proposicao densa resolve com perfeicao o mecanismo de particao e a garantia de ordem.", "compound", "formal_technical", pair_id="PAIR_04_A")

add_case("A_direct", "07_dense_compound_fulfillment",
    "Como o Elasticsearch indexa documentos textuais e realiza buscas rapidas por termos?",
    "O Elasticsearch processa o texto em um analisador lexico gerando tokens que sao gravados em um indice invertido associando cada termo a lista de documentos onde ele ocorre.",
    "DIRECT", "Proposicao densa que atende plenamente a indexacao de tokens e a recuperacao via indice invertido.", "compound", "formal_technical", pair_id="PAIR_05_A")

# Fill remaining Direct cases to reach exactly 50
direct_additional = [
    ("Como o protocolo TLS estabelece uma conexao segura entre cliente e servidor?",
     "Durante o handshake o cliente e o servidor negociam suites de cifras, trocam certificados digitais para autenticar a identidade e utilizam Diffie-Hellman para derivar chaves simetricas de sessao."),
    ("Como funciona o algoritmo de consenso Paxos em sistemas distribuidos?",
     "O Paxos opera em fases de prepare-promise e accept-accepted onde um proponente busca quorum de aceitacao da maioria antes de consolidar o valor escolhido."),
    ("Como o garbage collector ZGC do Java mantem pausas abaixo de um milissegundo?",
     "O ZGC utiliza ponteiros coloridos com referencias carregadas sob barreiras de leitura para executar a marcacao e compactacao concorrentemente com a execucao da aplicacao."),
    ("Como funciona a tecnica de isolamento Read Committed no PostgreSQL?",
     "O PostgreSQL utiliza MVCC onde cada comando dentro da transacao enxerga apenas os dados commitados antes do inicio daquele comando especifico."),
    ("Como um Web Application Firewall (WAF) mitiga ataques de SQL Injection?",
     "O WAF analisa os payloads das requisicoes HTTP inspecionando assinaturas e estruturas sintaticas maliciosas como comentarios de escape e tautologias booleanas para bloquear o trafego antes de chegar a aplicacao."),
    ("Como garantir que um job agendado execute apenas uma vez em um cluster com multiplas replicas?",
     "Utilizamos uma trava distribuida em um servico centralizado como Redis ou etcd com TTL curto garantindo que apenas a instancia que adquirir o lock execute o agendamento."),
    ("Como o protocolo gRPC alcanca maior performance em relacao a APIs REST com JSON?",
     "O gRPC utiliza HTTP/2 nativo com multiplexacao de conexoes e serializacao binaria eficiente de contratos fortemente tipados definidos em Protocol Buffers."),
    ("Como o algoritmo Raft realiza a eleicao de um novo lider?",
     "Quando um seguidor deixa de receber heartbeats ele incrementa o termo, torna-se candidato e solicita votos aos demais nos, assumindo o papel de lider caso obtenha a maioria dos votos do cluster."),
    ("Como mitigar problemas de N+1 queries em mapeamentos objeto-relacional?",
     "Configuramos consultas explicitas com join fetch ou carregamento em lote (batch fetching) para recuperar as entidades filhas associadas em uma unica requisicao SQL."),
    ("Como funciona o algoritmo Leaky Bucket para controle de vazao de requisicoes?",
     "As requisicoes entram em uma fila com capacidade finita e sao processadas a uma taxa constante, descartando requisicoes excedentes quando a fila atinge o limite maximo."),
    ("Como um reverse proxy distribui carga com algoritmo Least Connections?",
     "O proxy monitora a quantidade de conexoes ativas abertas em cada backend e encaminha a proxima requisicao para o servidor que possuir a menor contagem de conexoes ativas no momento."),
    ("Como funciona a replicacao Master-Slave assincrona em bancos de dados relacionais?",
     "O no primario executa e confirma as gravacoes localmente gravando o log binario, que e lido e reproduzido em segundo plano pelas replicas seguidoras."),
    ("Como o algoritmo Bloom Filter verifica a pertinencia de um elemento em um conjunto?",
     "O Bloom Filter aplica multiplas funcoes hash no elemento marcando posicoes em um vetor de bits, garantindo certeza absoluta quando o elemento nao pertence ao conjunto e aceitando probabilidade controlada de falso positivo."),
    ("Como implementar cancelamento gracioso de corrotinas em linguagens concorrentes?",
     "Propagamos um objeto de contexto com token de cancelamento atraves das chamadas e checamos periodicamente o status do canal para interromper o processamento liberando recursos alocados."),
    ("Como a tecnica de sharding distribui tabelas relacionais massivas em multiplos servidores?",
     "Definimos uma chave de sharding cujo hash determina qual particao fisica em servidores distintos armazenara e respondera pelas consultas daquele intervalo de registros."),
    ("Como o protocolo OAuth 2.0 utiliza o Authorization Code Grant com PKCE?",
     "O cliente envia um code challenge gerado a partir de um code verifier secreto na autorizacao e envia o verifier original na troca pelo token para comprovar sua legitimidade contra interceptacoes."),
    ("Como implementar deteccao de anomalias em streams de metricas com janelas de tempo?",
     "Agrupamos os eventos em janelas deslizantes calculando a media e o desvio padrao dinamico e emitimos alertas caso os valores correntes ultrapassem os limiares de desvio configurados.")
]

for q, r in direct_additional:
    add_case("A_direct", "01_direct_functional", q, r, "DIRECT", "Atendimento direto e funcional aos objetivos operacionais da pergunta.", "explanation", "formal_technical")

print(f"Total cases after Group A: {len(all_cases)}")
if len(all_cases) != 50:
    raise ValueError(f"Expected 50 cases in Group A, got {len(all_cases)}")
