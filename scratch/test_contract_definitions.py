import sys, json, re
from pathlib import Path

sys.path.insert(0, '.')
from reference_runtime import runtime

# Let's inspect the 20 contract test scenarios to make sure our test suite is completely defined
CONTRACT_TEST_CASES = [
    {
        "id": "TC_01_NO_LEXICAL_OVERLAP_CORRECT",
        "question": "Como garantir que um cluster mantenha um unico estado consistente durante particoes de rede?",
        "response": "Os nos utilizam um quorum de maioria e um lider eleito para validar qualquer transicao de estado antes de persistir.",
        "expected": "DIRECT",
        "description": "Resposta correta sem sobreposicao lexical."
    },
    {
        "id": "TC_02_SEMANTICALLY_DISJOINT_DOMAIN",
        "question": "Como funciona o roteamento de pacotes no protocolo BGP?",
        "response": "Para cuidar de orquideas regamos duas vezes por semana com adubo foliar equilibrado e poda cuidadosa das folhas secas.",
        "expected": "OFF_TOPIC",
        "description": "Resposta de dominio semanticamente disjunto (botanica)."
    },
    {
        "id": "TC_03_THEMATIC_NO_FUNCTIONAL_MECHANISM",
        "question": "Como o Kafka particiona as mensagens em um topico?",
        "response": "O Apache Kafka pertence a categoria de solucoes modernas de computacao e foi desenvolvido pela fundacao de software livre com ampla popularidade de mercado.",
        "expected": "RELATED",
        "description": "Resposta tematica sem atendimento funcional (metadados institucionais/categoriais)."
    },
    {
        "id": "TC_04_AUXILIARY_OBSERVABILITY_SUPPORT",
        "question": "Como evitar vazamento de memoria em processos concorrentes?",
        "response": "Adicionamos metricas no Prometheus e criamos alertas no Grafana para acompanhar o uso de memoria no dashboard.",
        "expected": "SUPPORTING",
        "description": "Contribuicao auxiliar de observabilidade/telemetria que nao resolve a demanda."
    },
    {
        "id": "TC_05_COMPOUND_PARTIAL_FULFILLMENT",
        "question": "Explique como funciona o Circuit Breaker e como configurar o tempo de retry com exponential backoff.",
        "response": "O Circuit Breaker transita entre os estados fechado, aberto e meio-aberto para interromper chamadas a servicos com falha.",
        "expected": "PARTIAL",
        "description": "Atendimento parcial de pergunta composta (atende circuit breaker, omite retry/backoff)."
    },
    {
        "id": "TC_06_COMPOUND_FULL_FULFILLMENT",
        "question": "Explique como funciona o Circuit Breaker e como configurar o tempo de retry com exponential backoff.",
        "response": "O Circuit Breaker transita entre fechado, aberto e meio-aberto para barrar chamadas com falha, e o retry aplica exponential backoff aumentando progressivamente o intervalo entre tentativas.",
        "expected": "DIRECT",
        "description": "Atendimento completo de pergunta composta (ambas as demandas primarias satisfeitas)."
    },
    {
        "id": "TC_07_INSUFFICIENT_DEFLECTION",
        "question": "Como solucionar problemas de concorrencia em transacoes de banco?",
        "response": "Olha, isso vai depender exclusivamente do orcamento e de muitos fatores de negocio antes de qualquer coisa.",
        "expected": "INSUFFICIENT",
        "description": "Resposta insuficiente e evasiva com predicado generico."
    },
    {
        "id": "TC_08_GENUINE_UNKNOWN",
        "question": "Como devemos tratar falhas intermitentes de conexao na replicacao do banco de dados?",
        "response": "A abordagem pode variar conforme a situacao de como a equipe resolver fazer na hora diante da replicacao.",
        "expected": "UNKNOWN",
        "description": "Indeterminacao genuina com expressao semanticamente indeterminada/ambigua."
    },
    {
        "id": "TC_09_DEFINITION_NO_CAUSALITY_REQUIRED",
        "question": "O que e o principio da Inversao de Dependencia?",
        "response": "E o principio que dita que modulos de alto nivel nao devem depender de modulos de baixo nivel, mas ambos devem depender de abstracoes.",
        "expected": "DIRECT",
        "description": "Pergunta de definicao sem exigencia causal operacional satisfeita com rigor conceitual."
    },
    {
        "id": "TC_10_HISTORICAL_DIRECT_ANSWER",
        "question": "Por que o Kubernetes foi doado para a Cloud Native Computing Foundation?",
        "response": "Para fomentar um ecossistema neutro de governanca aberta de containers sem controle exclusivo de um unico fornecedor corporativo.",
        "expected": "DIRECT",
        "description": "Pergunta historica diretamente respondida."
    },
    {
        "id": "TC_11_COMPARISON_DIRECT_ANSWER",
        "question": "Qual a diferenca entre processo e thread no sistema operacional?",
        "response": "Processos possuem espacos de enderecamento de memoria isolados entre si, enquanto threads de um mesmo processo compartilham o mesmo espaco de memoria.",
        "expected": "DIRECT",
        "description": "Pergunta comparativa diretamente respondida com os criterios fundamentais."
    },
    {
        "id": "TC_12_DIAGNOSIS_CAUSAL_ANSWER",
        "question": "Como diagnosticar vazamentos de conexoes no pool de banco de dados HikariCP?",
        "response": "Analisamos se conexoes ativas ultrapassam o limite do pool sem serem devolvidas no bloco try-finally e inspecionamos thread dumps para identificar a linha de codigo retendo a conexao.",
        "expected": "DIRECT",
        "description": "Pergunta de diagnostico que exige fundamentacao causal atendida com mecanismo investigativo."
    },
    {
        "id": "TC_13_UNSEEN_TECH_VALID_RESPONSE",
        "question": "Como o banco distribuido ZetaKVS lida com conflitos de concorrencia?",
        "response": "O ZetaKVS utiliza carimbos de tempo logicos de Lamport e locks otimistas com verificacao de versao no momento do commit.",
        "expected": "DIRECT",
        "description": "Tecnologia desconhecida/inedita (ZetaKVS) operando sob mecanismo canonico valido."
    },
    {
        "id": "TC_14_COLLOQUIAL_AND_PASSIVE_VOICE",
        "question": "Como lidar com pico repentino de requisicoes sem derrubar a API?",
        "response": "E colocada uma fila no meio do caminho pro consumidor ir puxando as mensagens no ritmo dele sem engasgar o banco.",
        "expected": "DIRECT",
        "description": "Linguagem coloquial e voz passiva expressando solucao tecnica correta."
    },
    {
        "id": "TC_15_LONG_OPERATIVE_DISJOINT",
        "question": "Como o protocolo Raft garante a consistencia do log entre lideres e seguidores?",
        "response": "A troca de oleo do motor do carro deve ser realizada a cada dez mil quilometros rodados usando lubrificante sintetico 5W30 e substituindo o filtro de combustivel e pastilhas de freio para garantir a longevidade do cabecote.",
        "expected": "OFF_TOPIC",
        "description": "Resposta longa, ativa e operacional, mas pertencente a dominio disjunto (mecanica automotiva)."
    },
    {
        "id": "TC_16_SHORT_PRECISE_DIRECT",
        "question": "O que e idempotencia em APIs REST?",
        "response": "E a propriedade onde multiplas requisicoes identicas produzem exatamente o mesmo efeito que uma unica requisicao.",
        "expected": "DIRECT",
        "description": "Resposta curta que atende integralmente a pergunta."
    },
    {
        "id": "TC_17_SINGLE_DENSE_PROPOSITION_MULTIPLE_DEMANDS",
        "question": "Como o Kafka particiona mensagens e garante a ordem de entrega?",
        "response": "O Kafka calcula o hash da chave da mensagem para direciona-la a uma particao especifica onde os offsets sequenciais garantem a ordenacao estrita.",
        "expected": "DIRECT",
        "description": "Uma unica proposicao densa satisfazendo legitimamente ambas as demandas da pergunta."
    },
    {
        "id": "TC_18_CIRCULAR_TAUTOLOGY",
        "question": "Como funciona a ordenacao no banco de dados?",
        "response": "A ordenacao no banco funciona ordenando os dados para que eles fiquem devidamente ordenados.",
        "expected": "UNKNOWN",
        "description": "Tautologia circular reflexiva sem ganho informacional."
    },
    {
        "id": "TC_19_DESTRUCTIVE_ANTITHESIS",
        "question": "Como garantir a durabilidade e seguranca dos dados gravados no banco relacional?",
        "response": "A gente desativa o write-ahead log (WAL) e desliga a sincronizacao em disco com fsync para ficar mais rapido sem travas.",
        "expected": "OFF_TOPIC",
        "description": "Antitese destrutiva que projeta acoes contrarias a protecao exigida."
    },
    {
        "id": "TC_20_PARAPHRASE_INVARIANCE",
        "question": "Como um load balancer distribui carga entre instancias?",
        "response": "As requisicoes sao distribuidas pelo balanceador de carga entre os servidores disponiveis utilizando a tecnica de round-robin sequencial.",
        "expected": "DIRECT",
        "description": "Variacao sintatica em voz passiva mantendo equivalencia semantica estrita."
    }
]

print(f"Loaded {len(CONTRACT_TEST_CASES)} contract test cases.")
