import json
import hashlib
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, '.')

# Load prior benchmark questions & responses
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
seen_q_local = set()
seen_r_local = set()

def add_case(group, semantic_family, q, r, ref_rel, rationale, q_type, ling_form, pair_id=None):
    global current_id
    cid = f"VAL-31-7-28-{current_id:03d}"
    
    q_clean = q.strip().lower()
    r_clean = r.strip().lower()
    
    # Audit against prior benchmarks
    if q_clean in prior_q:
        raise ValueError(f"DUPLICATE QUESTION DETECTED WITH PRIOR BENCHMARKS: {q}")
    if r_clean in prior_r:
        raise ValueError(f"DUPLICATE RESPONSE DETECTED WITH PRIOR BENCHMARKS: {r}")
        
    # Audit within current dataset
    if q_clean in seen_q_local and pair_id is None:
        raise ValueError(f"DUPLICATE QUESTION WITHIN DATASET: {q}")
    if r_clean in seen_r_local:
        raise ValueError(f"DUPLICATE RESPONSE WITHIN DATASET: {r}")
        
    seen_q_local.add(q_clean)
    seen_r_local.add(r_clean)
    
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
    current_id += 1

# ==============================================================================
# GROUP A: DIRECT (Target: exactly 50 cases)
# ==============================================================================
# 10 Invariance Pairs (20 cases)
from scratch.dataset_stage_31_7_28_groups_c_to_g import GROUP_A_PAIR_COUNTERPARTS

# We add the 10 pairs (20 cases)
for q, r, rat, pid in GROUP_A_PAIR_COUNTERPARTS:
    add_case("A_direct", "22_invariance_pair", q, r, "DIRECT", rat, "explanation", "invariance_pair", pair_id=pid)

# Now add 30 single cases for Group A to complete 50
GROUP_A_SINGLES = [
    ("Como configurar o pool de conexoes do banco para evitar esgotamento de conexoes em picos de requisicao?",
     "Ajustamos o max_connections no banco e o maximumPoolSize no HikariCP para limitar as conexoes ativas e configuramos o connectionTimeout para falhar rapidamente quando o limite for atingido.",
     "Atende diretamente as configuracoes necessarias de limite e timeout para evitar esgotamento.", "implementation", "formal_technical"),

    ("Como implementar paginacao baseada em cursor em tabelas com milhoes de registros?",
     "Utilizamos o valor do ultimo ID ou timestamp visto na clausula WHERE com operador maior que e ordenamos pela coluna indexada com LIMIT estrito.",
     "Explica o mecanismo causal exato de paginacao por cursor com WHERE e coluna indexada.", "implementation", "formal_technical"),

    ("Como o Redis lida com a expiracao de chaves para liberar espaco na memoria?",
     "O Redis combina amostragem aleatoria periodica de chaves com TTL e verificacao passiva no momento em que a chave e acessada para expira-la se estiver vencida.",
     "Descreve com precisao o algoritmo ativo e passivo de expiracao de chaves do Redis.", "explanation", "formal_technical"),

    ("Como assegurar que dados sensiveis nao fiquem expostos na camada de persistencia?",
     "Aplicamos criptografia de envelope em repouso nos discos do storage e ofuscamos colunas criticas com funcoes hash criptograficas salgadas.",
     "Resolve plenamente a demanda de seguranca de persistencia sem repetir termos da pergunta.", "implementation", "formal_technical"),

    ("Como garantir que escritas concorrentes no mesmo saldo nao resultem em atualizacoes perdidas?",
     "Executamos a verificacao de versao no momento da confirmacao do registro e abortamos a operacao caso ocorra divergencia entre a versao lida e a atual.",
     "Descreve o mecanismo funcional de controle de concorrencia otimista sem usar jargoes redundantes.", "implementation", "formal_technical"),

    ("Como manter a sincronia de configuracoes entre multiplas instancias sem necessidade de reinicializacao?",
     "Subscrevemos as instancias a um topico de mensageria que dissemina eventos de mudanca para recarregar os parametros dinamicamente na memoria dos nós.",
     "Explica o mecanismo de propagacao reativa de configuracao dinamicamente.", "architecture", "formal_technical"),

    ("O que e o principio da Inversao de Dependencia na arquitetura de software?",
     "E o principio que estipula que modulos de alto nivel nao devem depender de modulos de baixo nivel, e sim ambos dependerem de abstracoes e contratos estaveis.",
     "Define conceitualmente com rigor e exatidao o principio SOLID da inversao de dependencia.", "definition", "concise_conceptual"),

    ("O que significa o principio da Responsabilidade Unica no design de software?",
     "E a diretriz segundo a qual uma classe ou modulo deve possuir um unico motivo para mudar, concentrando apenas uma responsabilidade de negocio.",
     "Define adequadamente o principio da responsabilidade unica.", "definition", "concise_conceptual"),

    ("O que e isolamento Snapshot Isolation em bancos de dados relacionais?",
     "E o nivel de isolamento onde cada transacao enxerga uma fotografia consistente do estado dos dados no instante em que a transacao foi iniciada.",
     "Define conceitualmente a semantica de Snapshot Isolation.", "definition", "concise_conceptual"),

    ("Por que o ecossistema Linux adotou um kernel monolitico em vez de um microkernel?",
     "Porque na epoca da sua criacao o kernel monolitico oferecia melhor desempenho em chamadas de sistema eliminando o overhead de troca de contexto de IPC presente nos microkernels.",
     "Responde diretamente a razao historica e tecnica da escolha arquitetural do kernel Linux.", "historical", "formal_technical"),

    ("Por que o protocolo HTTP/2 introduziu a multiplexacao de streams em uma unica conexao TCP?",
     "Para superar o bloqueio de cabeca de fila no navegador e eliminar a necessidade de abrir multiplas conexoes TCP simultaneas para carregar assets.",
     "Explica com precisao historica e tecnica a motivacao do HTTP/2.", "historical", "formal_technical"),

    ("Por que o Git foi projetado originalmente com uma estrutura de grafo aciclico dirigido (DAG)?",
     "Para viabilizar ramificacoes e fusoes nao lineares extremamente rapidas garantindo integridade de historico imutavel via apontadores de commits.",
     "Explica a motivacao historica e funcional do design de DAG no Git.", "historical", "formal_technical"),

    ("Qual e a diferenca fundamental entre processos e threads no gerenciamento de memoria pelo SO?",
     "Processos possuem espacos de enderecamento de memoria completamente isolados entre si, enquanto threads pertencentes a um mesmo processo compartilham o mesmo espaco virtual de memoria.",
     "Atende com perfeicao os eixos de comparacao de isolamento e compartilhamento de memoria.", "comparison", "formal_technical"),

    ("Qual a diferenca entre indices baseados em B-Tree e LSM-Tree quanto ao perfil de operacoes?",
     "Indices B-Tree oferecem leituras pontuais mais rapidas com atualizacoes no proprio local do disco, enquanto LSM-Trees priorizam throughput de escrita realizando gravações sequenciais em log e compactacoes em lote.",
     "Compara adequadamente os trade-offs de leitura e escrita entre B-Tree e LSM-Tree.", "comparison", "formal_technical"),

    ("Qual a diferenca entre autenticacao baseada em tokens JWT e sessoes stateful armazenadas no servidor?",
     "Tokens JWT sao stateless e carregam as claims assinadas criptograficamente dentro do proprio payload, enquanto sessoes stateful mantem o estado do usuario na memoria ou banco do servidor referenciado por um session ID.",
     "Compara precisamente stateless vs stateful entre JWT e sessao.", "comparison", "formal_technical"),

    ("Qual a diferenca entre consistencia forte e consistencia eventual em sistemas distribuidos?",
     "Na consistencia forte qualquer leitura retorna imediatamente a escrita mais recente confirmada por todos os nos, enquanto na consistencia eventual as replicas convergem para o mesmo valor apos um intervalo de tempo sem garantias de sincronia imediata.",
     "Diferencia com exatidao conceitual consistencia forte e eventual.", "comparison", "formal_technical"),

    ("Como identificar a causa raiz de throttling de CPU em containers sob execucao no Kubernetes?",
     "Analisamos a metrica container_cpu_cfs_throttled_periods_total em relacao aos limites de cpu definidos no pod e verificamos se ha threads paralelas disputando ciclos alem do cfs_quota configurado.",
     "Explica o diagnostico causal de throttling via metricas de CFS e quotas.", "diagnosis", "formal_technical"),

    ("Como descobrir por que uma consulta SQL com indice esta executando com Table Scan?",
     "Executamos o comando EXPLAIN ANALYZE para inspecionar o plano de execucao e verificamos se funcoes aplicadas na coluna ou tipos de dados inconversiveis estao anulando o uso do indice.",
     "Apresenta o metodo de diagnostico correto com plano de execucao e verificacao de sargability.", "diagnosis", "formal_technical"),

    ("Como configurar autenticacao mutua TLS (mTLS) entre microsservicos?",
     "Configuramos certificados X.509 assinados por uma CA interna em ambos os lados e exigimos validacao do certificado cliente no handshake SSL do servidor com client-auth ativado.",
     "Descreve a implementacao correta de mTLS com certificados e validacao bilateral.", "implementation", "formal_technical"),

    ("Como configurar dead letter queues no RabbitMQ para mensagens rejeitadas?",
     "Definimos o argumento x-dead-letter-exchange na fila principal apontando para uma exchange dedicada e associamos uma fila de descarte para acolher mensagens rejeitadas com requeue false.",
     "Detalha os parametros e fluxo de DLQ no RabbitMQ.", "implementation", "formal_technical"),

    ("Como o banco de dados distribuido ChronoStore resolve conflitos de particionamento?",
     "O ChronoStore utiliza carimbos logicos de relogios vetoriais para detectar divergencias concorrentes e aplica resolucao deterministica baseada no maior timestamp com reconciliacao de replicas.",
     "Tecnologia ficticia operando sob mecanismo funcional distribuido valido.", "architecture", "formal_technical"),

    ("Como a camada de comunicacao QuantumMesh garante entrega confiavel de eventos sob alta perda de pacotes?",
     "O QuantumMesh fragmenta as mensagens em blocos com codificacao de correcao de erros por erasure coding e retransmite blocos faltantes via acknowledgments seletivos.",
     "Tecnologia inedita descrita com principio solido de erasure coding e retransmissao seletiva.", "architecture", "formal_technical"),

    ("O que e um deadlock em sistemas concorrentes?",
     "E a situacao onde dois ou mais processos ficam bloqueados indefinidamente porque cada um retem um recurso que o outro necessita para prosseguir.",
     "Definicao concisa e perfeita de deadlock.", "definition", "concise_conceptual"),

    ("Como o protocolo TLS estabelece uma conexao segura entre cliente e servidor?",
     "Durante o handshake o cliente e o servidor negociam suites de cifras, trocam certificados digitais para autenticar a identidade e utilizam Diffie-Hellman para derivar chaves simetricas de sessao.",
     "Atendimento direto aos passos fundamentais do handshake TLS.", "explanation", "formal_technical"),

    ("Como funciona o algoritmo de consenso Paxos em sistemas distribuidos?",
     "O Paxos opera em fases de prepare-promise e accept-accepted onde um proponente busca quorum de aceitacao da maioria antes de consolidar o valor escolhido.",
     "Atendimento direto ao algoritmo de duas fases do Paxos.", "explanation", "formal_technical"),

    ("Como o garbage collector ZGC do Java mantem pausas abaixo de um milissegundo?",
     "O ZGC utiliza ponteiros coloridos com referencias carregadas sob barreiras de leitura para executar a marcacao e compactacao concorrentemente com a execucao da aplicacao.",
     "Atendimento direto aos ponteiros coloridos e load barriers do ZGC.", "explanation", "formal_technical"),

    ("Como funciona a tecnica de isolamento Read Committed no PostgreSQL?",
     "O PostgreSQL utiliza MVCC onde cada comando dentro da transacao enxerga apenas os dados commitados antes do inicio daquele comando especifico.",
     "Atendimento direto ao comportamento de snapshot por comando do Read Committed.", "explanation", "formal_technical"),

    ("Como um Web Application Firewall (WAF) mitiga ataques de SQL Injection?",
     "O WAF analisa os payloads das requisicoes HTTP inspecionando assinaturas e estruturas sintaticas maliciosas como comentarios de escape e tautologias booleanas para bloquear o trafego antes de chegar a aplicacao.",
     "Atendimento direto a analise de assinaturas e sintaxe do WAF.", "explanation", "formal_technical"),

    ("Como o algoritmo Raft realiza a eleicao de um novo lider?",
     "Quando um seguidor deixa de receber heartbeats ele incrementa o termo, torna-se candidato e solicita votos aos demais nos, assumindo o papel de lider caso obtenha a maioria dos votos do cluster.",
     "Atendimento direto ao processo eleitoral e termo do Raft.", "explanation", "formal_technical"),

    ("Como o mecanismo de Write-Ahead Logging (WAL) garante a recuperabilidade de transacoes em bancos de dados?",
     "Antes de aplicar qualquer modificacao nas paginas de dados em memoria, o banco grava sequencialmente as mudancas no log de transacoes em disco, permitindo o replay das operacoes confirmadas apos uma falha.",
     "Atendimento direto a ordem estrita de gravacao em log antes da persistencia de dados.", "explanation", "formal_technical")
]

for q, r, rat, q_type, ling in GROUP_A_SINGLES:
    add_case("A_direct", "01_direct_functional", q, r, "DIRECT", rat, q_type, ling)

print(f"Total cases after Group A: {len(all_cases)}")
if len(all_cases) != 50:
    raise ValueError(f"Expected 50 cases in Group A, got {len(all_cases)}")

# ==============================================================================
# GROUP B: PARTIAL (Target: exactly 45 cases)
# ==============================================================================
from scratch.dataset_stage_31_7_28_groups import GROUP_B_CASES

for q, r, rat, pid in GROUP_B_CASES:
    add_case("B_partial", "05_compound_partial", q, r, "PARTIAL", rat, "compound", "partial_aspect", pair_id=pid)

print(f"Total cases after Group B: {len(all_cases)}")
if len(all_cases) != 95:
    raise ValueError(f"Expected 95 cases after Group B, got {len(all_cases)}")

# ==============================================================================
# GROUP C: SUPPORTING (Target: exactly 30 cases)
# ==============================================================================
from scratch.dataset_stage_31_7_28_groups_c_to_g import GROUP_C_CASES

for q, r, rat, pid in GROUP_C_CASES:
    add_case("C_supporting", "04_auxiliary_observability", q, r, "SUPPORTING", rat, "troubleshooting", "observability_telemetry", pair_id=pid)

print(f"Total cases after Group C: {len(all_cases)}")
if len(all_cases) != 125:
    raise ValueError(f"Expected 125 cases after Group C, got {len(all_cases)}")

# ==============================================================================
# GROUP D: RELATED (Target: exactly 35 cases)
# ==============================================================================
from scratch.dataset_stage_31_7_28_groups_c_to_g import GROUP_D_CASES

for q, r, rat, pid in GROUP_D_CASES:
    add_case("D_related", "03_thematic_metadata", q, r, "RELATED", rat, "explanation", "institutional_metadata", pair_id=pid)

print(f"Total cases after Group D: {len(all_cases)}")
if len(all_cases) != 160:
    raise ValueError(f"Expected 160 cases after Group D, got {len(all_cases)}")

# ==============================================================================
# GROUP E: OFF_TOPIC (Target: exactly 45 cases)
# ==============================================================================
from scratch.dataset_stage_31_7_28_groups_c_to_g import GROUP_E_CASES

for q, r, rat, pid in GROUP_E_CASES:
    add_case("E_off_topic", "02_disjoint_or_antithesis", q, r, "OFF_TOPIC", rat, "explanation", "alien_domain_or_antithesis", pair_id=pid)

print(f"Total cases after Group E: {len(all_cases)}")
if len(all_cases) != 205:
    raise ValueError(f"Expected 205 cases after Group E, got {len(all_cases)}")

# ==============================================================================
# GROUP F: INSUFFICIENT (Target: exactly 25 cases)
# ==============================================================================
from scratch.dataset_stage_31_7_28_groups_c_to_g import GROUP_F_CASES

for q, r, rat, pid in GROUP_F_CASES:
    add_case("F_insufficient", "07_evasive_or_insufficient", q, r, "INSUFFICIENT", rat, "explanation", "evasive_deflection_or_ignorance", pair_id=pid)

print(f"Total cases after Group F: {len(all_cases)}")
if len(all_cases) != 230:
    raise ValueError(f"Expected 230 cases after Group F, got {len(all_cases)}")

# ==============================================================================
# GROUP G: UNKNOWN (Target: exactly 20 cases)
# ==============================================================================
from scratch.dataset_stage_31_7_28_groups_c_to_g import GROUP_G_CASES

for q, r, rat, pid in GROUP_G_CASES:
    add_case("G_unknown", "08_tautology_or_ambiguity", q, r, "UNKNOWN", rat, "explanation", "tautology_circular_or_ambiguous", pair_id=pid)

print(f"Total cases after Group G: {len(all_cases)}")
if len(all_cases) != 250:
    raise ValueError(f"Expected 250 cases in total, got {len(all_cases)}")

# Check Invariance Pairs
pairs = {}
for c in all_cases:
    pid = c["invariance_pair_id"]
    if pid:
        base_id = pid[:-2] if (pid.endswith("_A") or pid.endswith("_B")) else pid
        pairs.setdefault(base_id, []).append(c)

print(f"Total invariance pairs found: {len(pairs)}")
for pid, plist in pairs.items():
    if len(plist) != 2:
        raise ValueError(f"Pair {pid} does not have exactly 2 cases: {len(plist)}")

print(f"Verified all {len(pairs)} invariance pairs (40 cases)!")

# Verification of class distribution
dist = Counter(c["reference_relevance"] for c in all_cases)
print("Class Distribution:", dict(dist))

# Export deliverables
p_dir = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05")

# 1. stage_31_7_28_ground_truth.json
with open(p_dir / "stage_31_7_28_ground_truth.json", "w", encoding="utf-8") as f:
    json.dump({
        "stage": "31.7.28",
        "benchmark_type": "INDEPENDENT_BLIND_VALIDATION_BENCHMARK",
        "total_cases": len(all_cases),
        "class_distribution": dict(dist),
        "invariance_pairs_count": len(pairs),
        "cases": all_cases
    }, f, indent=2, ensure_ascii=False)

# 2. stage_31_7_28_blind_input.json (ONLY id, question, response - NO LABELS)
blind_input = [
    {
        "id": c["id"],
        "question_text": c["question_text"],
        "response_text": c["response_text"]
    }
    for c in all_cases
]
with open(p_dir / "stage_31_7_28_blind_input.json", "w", encoding="utf-8") as f:
    json.dump({
        "stage": "31.7.28",
        "total_cases": len(blind_input),
        "cases": blind_input
    }, f, indent=2, ensure_ascii=False)

# Compute hashes
gt_hash = hashlib.sha256((p_dir / "stage_31_7_28_ground_truth.json").read_bytes()).hexdigest().upper()
bi_hash = hashlib.sha256((p_dir / "stage_31_7_28_blind_input.json").read_bytes()).hexdigest().upper()

# 3. stage_31_7_28_benchmark_manifest.json
manifest = {
    "stage": "31.7.28",
    "timestamp_created_utc": "2026-10-19T14:50:00Z",
    "benchmark_name": "Stage 31.7.28 Independent Blind Validation Benchmark (Cycle 5)",
    "runtime_evaluated_path": "reference_runtime/runtime.py",
    "runtime_sha256": "6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28",
    "total_cases": len(all_cases),
    "class_distribution": dict(dist),
    "semantic_families_count": 22,
    "invariance_pairs_count": len(pairs),
    "invariance_cases_count": len(pairs) * 2,
    "provenance_status": "REFERENCE_INDEPENDENCE_UNRESOLVED",
    "ground_truth_file": "stage_31_7_28_ground_truth.json",
    "ground_truth_sha256": gt_hash,
    "blind_input_file": "stage_31_7_28_blind_input.json",
    "blind_input_sha256": bi_hash
}
with open(p_dir / "stage_31_7_28_benchmark_manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("\nAll benchmark files generated successfully!")
print("Ground truth SHA-256:", gt_hash)
print("Blind input SHA-256:", bi_hash)
