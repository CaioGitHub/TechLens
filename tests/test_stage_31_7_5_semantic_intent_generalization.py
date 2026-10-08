"""Stage 31.7.5 — Independent Test Suite for Semantic Intent Generalization.

Validates the decoupled semantic architecture implemented in Stage 31.7.5.

FIREWALL AND BLINDNESS GOVERNANCE RULES:
1. Zero human scores imported.
2. Zero MAE or PilotInterviewAlignment imported.
3. Zero reference to Candidate-Pilot-05 target scores.
4. Independent semantic derivation of expected relations.
5. Catalog independence: Must work without reliance on closed _FUNCTIONAL_CAPABILITIES.
"""

from __future__ import annotations

import copy
import unittest
from typing import Any

from reference_runtime.runtime import (
    _evaluate_semantic_relevance,
    _blind_evidence_specs,
    _evaluate_multi_aspect_coverage,
    _FUNCTIONAL_CAPABILITIES,
)


class Stage3175UnseenTechnologiesTests(unittest.TestCase):
    """Category A: Technologies completely outside the historical catalog (>= 15 cases)."""

    def test_unseen_01_duckdb(self):
        q = {"text": "Como o DuckDB otimiza o processamento de consultas analíticas?"}
        r = {"reconstructed_text": "Ele utiliza um motor de execução colunar e vetorizada in-process."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_unseen_02_cockroachdb(self):
        q = {"text": "Como o CockroachDB garante consenso e transações distribuídas?"}
        r = {"reconstructed_text": "Utiliza consenso Raft em múltiplos nós com transações serializable distribuídas."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_unseen_03_surrealdb(self):
        q = {"text": "Qual o modelo de dados suportado pelo SurrealDB?"}
        r = {"reconstructed_text": "Ele unifica tabelas relacionais, documentos e conexões de grafos com SurrealQL."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_unseen_04_linkerd(self):
        q = {"text": "Como o Linkerd implementa seu plano de dados em service mesh?"}
        r = {"reconstructed_text": "Usa micro-proxies sidecars ultra-leves escritos em Rust para mTLS e roteamento L7."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_unseen_05_polars(self):
        q = {"text": "Por que o Polars apresenta alta performance no processamento de dataframes?"}
        r = {"reconstructed_text": "Ele foi construído em Rust sobre Apache Arrow com paralelismo e execução lazy."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_unseen_06_redpanda(self):
        q = {"text": "Como o Redpanda alcança baixa latência na ingestão de eventos?"}
        r = {"reconstructed_text": "Adota arquitetura thread-per-core em C++ sem JVM, compatível com a API do Kafka."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_unseen_07_triton(self):
        q = {"text": "Como o Triton Inference Server otimiza o throughput de inferência?"}
        r = {"reconstructed_text": "Agrupa requisições em lotes dinâmicos concorrentes executando na GPU."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_unseen_08_spire(self):
        q = {"text": "Como o SPIRE emite e valida identidades de workloads?"}
        r = {"reconstructed_text": "Emite identidades criptográficas SPIFFE SVID através de certificados X.509 assinados."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_unseen_09_fluentbit(self):
        q = {"text": "Qual a função do Fluentbit na infraestrutura de logs?"}
        r = {"reconstructed_text": "Coleta logs de containers, aplica filtros de parsing e encaminha eventos para sinks."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_unseen_10_ebpf(self):
        q = {"text": "Como o eBPF permite monitoramento e segurança no kernel Linux?"}
        r = {"reconstructed_text": "Executa bytecode seguro dentro do kernel acoplado a hooks de rede e XDP."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_unseen_11_nats_jetstream(self):
        q = {"text": "Como o NATS JetStream oferece persistência de mensagens?"}
        r = {"reconstructed_text": "Implementa streams persistentes com confirmação at-least-once e desduplicação nativa."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_unseen_12_meilisearch(self):
        q = {"text": "Como o Meilisearch entrega busca instantânea com tolerância a erros?"}
        r = {"reconstructed_text": "Utiliza índice invertido e calcula distância de Levenshtein para typo tolerance."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_unseen_13_vector(self):
        q = {"text": "Como o Vector atua no pipeline de observabilidade?"}
        r = {"reconstructed_text": "Pipeline concorrente em Rust com buffers em disco e transformação declarativa."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_unseen_14_scylladb(self):
        q = {"text": "Como o ScyllaDB atinge alta taxa de transferência em bancos NoSQL?"}
        r = {"reconstructed_text": "Utiliza arquitetura shared-nothing e modelo assíncrono Seastar sem bloqueios globais."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_unseen_15_temporal(self):
        q = {"text": "Como o Temporal garante execução durável de workflows?"}
        r = {"reconstructed_text": "Persiste histórico de eventos e executa replay determinístico em caso de falha de workers."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))


class Stage3175TechnologyFreeConceptsTests(unittest.TestCase):
    """Category B: Concepts described without naming specific branded technologies (>= 15 cases)."""

    def test_concept_01_optimistic_concurrency(self):
        q = {"text": "Como evitar que duas operações simultâneas sobrescrevam alterações no mesmo registro?"}
        r = {"reconstructed_text": "Cada registro possui um versionamento e o commit valida se a versão não mudou."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_concept_02_idempotency(self):
        q = {"text": "Como evitar duplicidade de efeitos colaterais em reenvios de chamadas?"}
        r = {"reconstructed_text": "Associando uma chave de idempotência exclusiva e rejeitando execuções redundantes."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_concept_03_circuit_breaking(self):
        q = {"text": "Como proteger uma arquitetura quando um serviço dependente começa a falhar continuamente?"}
        r = {"reconstructed_text": "Implementaria um disjuntor que interrompe requisições temporariamente e aciona uma resposta degradada."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_concept_04_rate_limiting(self):
        q = {"text": "Como restringir o volume de chamadas por usuário para evitar sobrecarga?"}
        r = {"reconstructed_text": "Aplicaria algoritmo de balde de fichas para descartar requisições que excedam a taxa permitida."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_concept_05_graceful_degradation(self):
        q = {"text": "Como manter o sistema operacional durante picos extremos de tráfego?"}
        r = {"reconstructed_text": "Desativaria módulos não essenciais e serviria dados pré-computados em cache para aliviar a carga."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_concept_06_deadlock_prevention(self):
        q = {"text": "Como prevenir impasses mútuos quando múltiplos processos requisitam múltiplos recursos?"}
        r = {"reconstructed_text": "Estabeleceria uma ordem estrita e global para aquisição de recursos em todas as operações."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_concept_07_bulkhead(self):
        q = {"text": "Como compartimentar recursos de execução para evitar que uma falha isolada derrube o sistema inteiro?"}
        r = {"reconstructed_text": "Isolaria pools de processamento dedicados para cada cliente ou componente crítico."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_concept_08_backpressure(self):
        q = {"text": "Como equilibrar o fluxo quando a produção de itens supera a capacidade de consumo?"}
        r = {"reconstructed_text": "O consumidor sinaliza ao produtor a taxa que consegue absorver, aplicando contrapressão no fluxo."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_concept_09_distributed_tracing(self):
        q = {"text": "Como rastrear o ciclo de vida de uma operação que atravessa dezenas de nós em rede?"}
        r = {"reconstructed_text": "Injetaria identificadores únicos de trace e span nos cabeçalhos repassando o contexto downstream."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_concept_10_cache_invalidation(self):
        q = {"text": "Como manter leituras rápidas garantindo que dados obsoletos sejam descartados?"}
        r = {"reconstructed_text": "Definiria tempo de vida com TTL e configuraria invalidação explícita nos eventos de alteração."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_concept_11_performance_regression(self):
        q = {"text": "Como identificar degradação de performance após um novo deploy?"}
        r = {"reconstructed_text": "Compararia percentil 99 de latência e taxa de erro da nova versão contra baseline histórica."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_concept_12_eventual_consistency(self):
        q = {"text": "Como garantir consistência entre dois serviços sem transação distribuída em duas fases?"}
        r = {"reconstructed_text": "Adotaria consistência eventual com publicação de eventos assíncronos e rotinas de reconciliação."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_concept_13_zero_knowledge(self):
        q = {"text": "Como provar a posse de um segredo sem revelá-lo?"}
        r = {"reconstructed_text": "Usaria provas de conhecimento zero onde o provador convence o verificador matematicamente."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_concept_14_dependency_inversion(self):
        q = {"text": "Como desacoplar a criação de objetos facilitando testes unitários?"}
        r = {"reconstructed_text": "Receberia as dependências externamente via construtor em vez de instanciar diretamente na classe."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_concept_15_event_driven(self):
        q = {"text": "Como comunicar múltiplos componentes de forma assíncrona desacoplada?"}
        r = {"reconstructed_text": "Publicaria eventos em um canal compartilhado onde consumidores desacoplados reagem aos fatos."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")


class Stage3175ZeroLexicalOverlapTests(unittest.TestCase):
    """Category C: Functional problem -> mechanism with zero/minimal lexical overlap (>= 15 cases)."""

    def test_lexical_01_lost_updates(self):
        q = {"text": "Como evitar que duas escritas concorrentes sobrescrevam alterações?"}
        r = {"reconstructed_text": "Cada registro possui um timestamp ou versão atômica checada no momento do commit."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_02_tracing_path(self):
        q = {"text": "Como rastrear o caminho de uma chamada entre diferentes serviços?"}
        r = {"reconstructed_text": "Passando IDs de correlação nos envelopes HTTP para amarrar os registros."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_03_cascade_failure(self):
        q = {"text": "Como evitar que a lentidão de um terceiro derrube a nossa aplicação?"}
        r = {"reconstructed_text": "Colocaria circuit breaker para abrir o circuito e retornar fallback rápido."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_lexical_04_traffic_burst(self):
        q = {"text": "Como conter disparos massivos de requisições de um único cliente?"}
        r = {"reconstructed_text": "Usaria token bucket ou sliding window limitando a taxa permitida."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_05_double_charge(self):
        q = {"text": "Como evitar cobrança em dobro caso o cliente aperte duas vezes o botão de compra?"}
        r = {"reconstructed_text": "Gero uma chave exclusiva na requisição e deduplico transações que já foram salvas."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_06_deadlock_hierarchical(self):
        q = {"text": "Como prevenir impasses mútuos entre transações?"}
        r = {"reconstructed_text": "Adquirindo travas em ordem hierárquica estrita."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_07_fast_producer(self):
        q = {"text": "O que fazer quando a entrada de mensagens supera o esgotamento da fila?"}
        r = {"reconstructed_text": "Aplicaria backpressure com buffers delimitados e desaceleração do fluxo de ingestão."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_08_thread_exhaustion(self):
        q = {"text": "Como evitar que uma dependência lenta esgote as threads do servidor?"}
        r = {"reconstructed_text": "Isolaria pools de threads com bulkhead para impedir congelamento global."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_lexical_09_stale_data(self):
        q = {"text": "Como garantir que um cache não sirva dados desatualizados após uma edição cadastral?"}
        r = {"reconstructed_text": "Disparo eventos de mutação para expurgar a chave da memória imediatamente."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_10_untraceable_order(self):
        q = {"text": "Como acompanhar um pedido passando por dezenas de instâncias autônomas?"}
        r = {"reconstructed_text": "Injetaria trace e span nos headers HTTP propagando o contexto adiante."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_11_post_deploy_slowdown(self):
        q = {"text": "Como diagnosticar lentidão após atualizar a versão em produção?"}
        r = {"reconstructed_text": "Compararia percentil 99 com linha de base anterior via telemetria distribuída."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_lexical_12_concurrency_no_locks(self):
        q = {"text": "Como evitar conflito de escrita simultânea sem lock?"}
        r = {"reconstructed_text": "Boto uma coluna de versão lá e na hora de salvar vejo se ninguém mudou antes de mim."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_13_abusive_endpoint_protection(self):
        q = {"text": "Como proteger endpoints contra rajadas abusivas?"}
        r = {"reconstructed_text": "Token bucket limitando taxa por cliente."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_14_dependent_service_failing(self):
        q = {"text": "Como proteger o sistema contra indisponibilidade de serviços terceiros?"}
        r = {"reconstructed_text": "Configurar fallback com cache e degradar gracefully."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_lexical_15_async_consistency_without_2pc(self):
        q = {"text": "Como sincronizar dados entre serviços sem travar tudo em transação distribuída?"}
        r = {"reconstructed_text": "Uso consistência eventual com eventos assíncronos e reconciliação em background."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")


class Stage3175EntityAnchorTests(unittest.TestCase):
    """Category D: Entity match != DIRECT; mere presence without mechanism yields RELATED (>= 15 cases)."""

    def test_anchor_01_kubernetes(self):
        q = {"text": "Como configurar readiness probe no Kubernetes?"}
        r = {"reconstructed_text": "Temos um cluster de Kubernetes gerenciado na nuvem."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_02_kafka(self):
        q = {"text": "Como garantir ordenação estrita de mensagens no Kafka?"}
        r = {"reconstructed_text": "Kafka é uma plataforma amplamente adotada pela nossa equipe."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_03_redis(self):
        q = {"text": "Como configurar eviction policies no Redis para evitar falta de memória?"}
        r = {"reconstructed_text": "Instalei uma instância de Redis no ambiente local para testes."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_04_spring(self):
        q = {"text": "Como funciona o ciclo de vida de beans com Dependency Injection no Spring?"}
        r = {"reconstructed_text": "Spring Boot é o framework utilizado em quase todos os nossos projetos."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_05_postgresql(self):
        q = {"text": "Como o MVCC gerencia visibilidade de tuplas no PostgreSQL?"}
        r = {"reconstructed_text": "PostgreSQL é o banco relacional padrão da nossa infraestrutura."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_06_docker(self):
        q = {"text": "Como o Docker utiliza namespaces e cgroups para isolar containers?"}
        r = {"reconstructed_text": "Gosto de rodar imagens Docker para desenvolvimento diário."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_07_istio(self):
        q = {"text": "Como o Istio intercepta tráfego de rede no cluster?"}
        r = {"reconstructed_text": "A equipe de infraestrutura instalou Istio recentemente."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_08_surrealdb(self):
        q = {"text": "Como funciona o modelo multi-modelo do SurrealDB?"}
        r = {"reconstructed_text": "O SurrealDB foi desenvolvido em Rust pela comunidade."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_09_clickhouse(self):
        q = {"text": "Como funciona a ordenação esparsa no ClickHouse?"}
        r = {"reconstructed_text": "ClickHouse foi criado por engenheiros na Europa para analítica."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_10_opentelemetry(self):
        q = {"text": "Como configurar o exporter OTLP no OpenTelemetry?"}
        r = {"reconstructed_text": "OpenTelemetry é uma iniciativa muito popular na CNCF."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_11_duckdb(self):
        q = {"text": "Como funciona a vetorização de dados no DuckDB?"}
        r = {"reconstructed_text": "DuckDB é bastante utilizado por engenheiros de dados recentemente."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_12_linkerd(self):
        q = {"text": "Como o Linkerd realiza autenticação mTLS entre pods?"}
        r = {"reconstructed_text": "Instalamos o Linkerd em ambiente de homologação no mês passado."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_13_redpanda(self):
        q = {"text": "Como o Redpanda gerencia consensus Raft por partição?"}
        r = {"reconstructed_text": "A empresa cogitou adotar Redpanda em substituição ao Kafka."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_14_polars(self):
        q = {"text": "Como funciona o motor lazy de otimização no Polars?"}
        r = {"reconstructed_text": "Polars tem muitos adeptos que gostam de velocidade em Python."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_anchor_15_spire(self):
        q = {"text": "Como funciona a validação de nós no Spire Server?"}
        r = {"reconstructed_text": "Spire é uma ferramenta de segurança de código aberto."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")


class Stage3175SupportingVsRelatedTests(unittest.TestCase):
    """Category E: Functional contribution (SUPPORTING) vs passive thematic adjacency (RELATED) (>= 15 cases)."""

    def test_pair_01_http500(self):
        q = {"text": "Como investigar erro HTTP 500 na aplicação?"}
        r_a = {"reconstructed_text": "Correlacionar logs e traces para investigar falhas."}
        r_b = {"reconstructed_text": "Nossa aplicação roda Spring Boot e Hibernate na nuvem."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_02_resilience(self):
        q = {"text": "Como proteger o sistema contra indisponibilidade de serviços terceiros?"}
        r_a = {"reconstructed_text": "Configurar fallback com cache e degradar gracefully."}
        r_b = {"reconstructed_text": "Nossos microsserviços usam Maven para compilar os pacotes."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_03_latency(self):
        q = {"text": "Como investigar aumento súbito de latência após deploy?"}
        r_a = {"reconstructed_text": "Monitorar taxa de GC e pausas da JVM com métricas JMX e APM."}
        r_b = {"reconstructed_text": "O deploy foi feito usando esteira automatizada de CI/CD."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_04_thread_blocking(self):
        q = {"text": "Como diagnosticar threads travadas em produção?"}
        r_a = {"reconstructed_text": "Capturar thread dump e inspecionar threads em estado BLOCKED com traces."}
        r_b = {"reconstructed_text": "O servidor possui 16 núcleos de processamento Intel Xeon."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_05_slow_query(self):
        q = {"text": "Como otimizar consultas lentas no banco de dados?"}
        r_a = {"reconstructed_text": "Analisar plano de execução com EXPLAIN ANALYZE procurando sequential scans."}
        r_b = {"reconstructed_text": "A tabela do banco possui mais de 10 milhões de registros salvos."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_06_cpu_spike(self):
        q = {"text": "Como identificar a causa de alto consumo de CPU na aplicação?"}
        r_a = {"reconstructed_text": "Faria profiling de CPU para inspecionar hot methods que consomem ciclos."}
        r_b = {"reconstructed_text": "A instância está configurada em uma VM na nuvem Azure."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_07_connection_exhaustion(self):
        q = {"text": "Como investigar esgotamento de conexões no pool do banco?"}
        r_a = {"reconstructed_text": "Verificaria transações longas em aberto e conexões travadas sem commit."}
        r_b = {"reconstructed_text": "O banco relacional utiliza porta padrão 5432 na rede interna."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_08_memory_leak(self):
        q = {"text": "Como investigar consumo progressivo de memória até OutOfMemory?"}
        r_a = {"reconstructed_text": "Capturaria um heap dump para inspecionar os maiores dominadores de memória."}
        r_b = {"reconstructed_text": "A aplicação está hospedada em servidores Linux Ubuntu."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_09_api_errors_401(self):
        q = {"text": "Como diagnosticar falhas de autenticação 401 em cascata?"}
        r_a = {"reconstructed_text": "Checaria a expiração do token JWT e o alinhamento da chave pública de validação."}
        r_b = {"reconstructed_text": "O cliente mobile foi desenvolvido com framework React Native."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_10_disk_full(self):
        q = {"text": "Como diagnosticar saturação de disco em nós de produção?"}
        r_a = {"reconstructed_text": "Analisaria retenção de arquivos de log e purgaria diretórios temporários acumulados."}
        r_b = {"reconstructed_text": "O cluster de armazenamento possui discos SSD de alta velocidade."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_11_packet_loss(self):
        q = {"text": "Como diagnosticar perda intermitente de pacotes entre serviços?"}
        r_a = {"reconstructed_text": "Coletaria métricas de retransmissão TCP e analisaria timeout nos sockets."}
        r_b = {"reconstructed_text": "A rede é operada por provedores de nuvem certificados."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_12_consumer_lag(self):
        q = {"text": "Como investigar crescimento do lag de consumidores no Kafka?"}
        r_a = {"reconstructed_text": "Analisaria tempo de processamento por mensagem e commits de offset bloqueados."}
        r_b = {"reconstructed_text": "O Kafka foi instalado em versão recente pela equipe."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_13_intermittent_timeouts(self):
        q = {"text": "Como investigar timeouts intermitentes em chamadas HTTP externas?"}
        r_a = {"reconstructed_text": "Checaria latência de resolução DNS e tempos de handshake TLS na telemetria."}
        r_b = {"reconstructed_text": "As requisições utilizam HTTP/2 sobre internet pública."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_14_slow_microservice_boot(self):
        q = {"text": "Como investigar lentidão excessiva na inicialização de um serviço?"}
        r_a = {"reconstructed_text": "Mediria o tempo de injeção de dependências e conexão síncrona aos bancos no startup."}
        r_b = {"reconstructed_text": "O código é empacotado em JAR executável padronizado."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")

    def test_pair_15_deadlock_database(self):
        q = {"text": "Como diagnosticar deadlocks ocorrendo com frequência no banco?"}
        r_a = {"reconstructed_text": "Inspecionaria os logs de lock do banco para ver as consultas concorrentes em disputa."}
        r_b = {"reconstructed_text": "O banco de dados relacional foi criado há cinco anos."}
        self.assertIn(_evaluate_semantic_relevance(q, r_a)["classification"], ("SUPPORTING", "DIRECT"))
        self.assertEqual(_evaluate_semantic_relevance(q, r_b)["classification"], "RELATED")


class Stage3175MultiAspectTests(unittest.TestCase):
    """Category F: Independent evaluation of multiple question demands (>= 15 cases)."""

    def test_multi_01_rest_and_pagination(self):
        q = {"text": "Como projetar uma API REST e estruturar a paginação de recursos?"}
        r = {"reconstructed_text": "REST expõe recursos via HTTP com verbos semânticos e status codes."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_multi_02_circuit_breaker_and_bulkhead(self):
        q = {"text": "Explique como funciona bulkhead e circuit breaker em resiliência."}
        r = {"reconstructed_text": "Bulkhead isola pools de threads para evitar que falhas se espalhem."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_multi_03_btree_and_write_overhead(self):
        q = {"text": "Como o índice B-Tree acelera buscas e qual seu impacto nas operações de escrita?"}
        r = {"reconstructed_text": "A árvore B permite busca logarítmica rápida nas consultas."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_multi_04_jwt_claims_and_signature(self):
        q = {"text": "Como o JWT transporta dados e como a assinatura criptográfica garante a integridade?"}
        r = {"reconstructed_text": "O JWT carrega informações no payload codificadas em base64."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_multi_05_kafka_partitions_and_rebalance(self):
        q = {"text": "Como o Kafka particiona mensagens e como gerencia o rebalanceamento de consumidores?"}
        r = {"reconstructed_text": "Distribui mensagens por chave hash entre as diferentes partições."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_multi_06_virtual_threads_and_carrier(self):
        q = {"text": "O que são virtual threads e qual o papel da carrier thread na execução?"}
        r = {"reconstructed_text": "São threads leves gerenciadas pela JVM que evitam bloquear threads do SO."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_multi_07_docker_namespaces_and_cgroups(self):
        q = {"text": "Como o Docker utiliza namespaces e como gerencia limites com cgroups?"}
        r = {"reconstructed_text": "Namespaces isolam processos, redes e pontos de montagem no kernel."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_multi_08_cicd_build_and_deploy(self):
        q = {"text": "Como estruturar um pipeline de CI/CD e quais etapas automatizadas incluir?"}
        r = {"reconstructed_text": "CI/CD executa compilação contínua e roda testes automatizados."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING", "PARTIAL"))

    def test_multi_09_oauth2_token_and_refresh(self):
        q = {"text": "Como funciona o fluxo de token de acesso e qual o papel do refresh token?"}
        r = {"reconstructed_text": "O token de acesso autoriza chamadas aos recursos protegidos na API."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_multi_10_cache_ttl_and_eviction(self):
        q = {"text": "Como configurar tempo de expiração TTL e quais estratégias de eviction usar?"}
        r = {"reconstructed_text": "Defino TTL para que chaves antigas expirem automaticamente."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_multi_11_polars_lazy_and_arrow(self):
        q = {"text": "Como o Polars utiliza o Apache Arrow e como otimiza consultas com execução lazy?"}
        r = {"reconstructed_text": "Ele armazena tabelas em memória usando o formato colunar do Apache Arrow."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_multi_12_ports_and_adapters(self):
        q = {"text": "Explique portas e adaptadores na arquitetura hexagonal."}
        r = {"reconstructed_text": "As portas definem as interfaces do núcleo de negócio com o exterior."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_multi_13_signals_computed_and_effects(self):
        q = {"text": "Como o Angular Signals gerencia reatividade e como funciona computed?"}
        r = {"reconstructed_text": "Signals emitem notificações reativas quando seus valores mudam."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_multi_14_retry_and_jitter(self):
        q = {"text": "Como evitar retry agressivo e tempestade de requisições?"}
        r = {"reconstructed_text": "Utilizaria backoff exponencial com jitter para espaçar as tentativas."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("PARTIAL", "SUPPORTING", "DIRECT"))

    def test_multi_15_both_aspects_covered(self):
        q = {"text": "Como projetar uma API REST e estruturar a paginação de recursos?"}
        r = {"reconstructed_text": "REST usa verbos HTTP para recursos e a paginação usa cursor ou limit e offset."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")


class Stage3175EpistemologyAndExperienceTests(unittest.TestCase):
    """Category G: Epistemic status separated from semantic relevance (>= 15 cases)."""

    def test_epistemic_01_declaration(self):
        text = "Trabalhei dois anos com Kubernetes na empresa anterior."
        q = {"text": "Qual sua experiência com Kubernetes?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("experience_declaration", types)
        self.assertNotIn("demonstrated_experience", types)

    def test_epistemic_02_demonstrated(self):
        text = "Trabalhei com Kubernetes por dois anos e, quando tínhamos crashloop, configurávamos readiness probe."
        q = {"text": "Como você lida com falhas no Kubernetes?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("experience_declaration", types)
        self.assertIn("demonstrated_experience", types)

    def test_epistemic_03_hypothesis(self):
        text = "Eu investigaria o problema usando thread dumps se a CPU ficasse travada."
        q = {"text": "Como diagnosticar contenção de threads?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("hypothesis", types)

    def test_epistemic_04_pure_conceptual(self):
        text = "Virtual threads são montadas em carrier threads gerenciadas pela JVM."
        q = {"text": "Como funcionam virtual threads?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("conceptual", types)

    def test_epistemic_05_concrete_production(self):
        text = "Em produção, implementei o particionamento de tópicos no Kafka para suportar 50 mil eventos por segundo."
        q = {"text": "Como você utilizou Kafka?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("demonstrated_experience", types)

    def test_epistemic_06_hypothetical_redis(self):
        text = "Eu usaria Redis se precisássemos reduzir a latência de leitura no catálogo."
        q = {"text": "Como você aceleraria consultas repetidas?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("hypothesis", types)

    def test_epistemic_07_spring_declaration(self):
        text = "Tenho experiência com Spring Boot na empresa anterior desenvolvendo microsserviços."
        q = {"text": "Qual seu histórico com Spring?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("experience_declaration", types)

    def test_epistemic_08_incident_resolution(self):
        text = "Resolvíamos incidentes de lentidão gerando dump e identificando locks no banco."
        q = {"text": "Como sua equipe lidava com lentidão no banco?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("demonstrated_experience", types)

    def test_epistemic_09_possibility_hypothesis(self):
        text = "Uma possibilidade seria criar réplicas de leitura para desafogar o nó primário."
        q = {"text": "Como escalar leituras em banco relacional?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("hypothesis", types)

    def test_epistemic_10_career_declaration(self):
        text = "Atuei cinco anos como engenheiro backend em sistemas distribuídos."
        q = {"text": "Conte sobre sua trajetória profissional."}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("experience_declaration", types)

    def test_epistemic_11_investigation_result(self):
        text = "Investiguei o incidente de degradação e corrigi a retenção de conexões órfãs no pool."
        q = {"text": "Como você atuou no último incidente de produção?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("demonstrated_experience", types)

    def test_epistemic_12_circuit_hypothesis(self):
        text = "Provavelmente eu colocaria um circuit breaker na chamada para isolar a falha."
        q = {"text": "O que você faria se um parceiro ficasse lento?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("hypothesis", types)

    def test_epistemic_13_rabbitmq_declaration(self):
        text = "Já usei RabbitMQ em projetos anteriores na fintech onde trabalhei."
        q = {"text": "Você já trabalhou com mensageria?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("experience_declaration", types)

    def test_epistemic_14_pipeline_configuration(self):
        text = "Configurei esteiras de CI/CD automatizadas integradas ao SonarQube."
        q = {"text": "Qual sua experiência prática com automação de build?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("demonstrated_experience", types)

    def test_epistemic_15_starting_hypothesis(self):
        text = "Eu começaria analisando os logs da aplicação para entender o padrão de erro."
        q = {"text": "Por onde você iniciaria uma investigação de falha 500?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("hypothesis", types)


class Stage3175RepresentationInvarianceTests(unittest.TestCase):
    """Category H: Semantic equivalence preserved across linguistic variants (>= 15 pairs)."""

    def _assert_equivalent(self, q: dict[str, Any], r1: dict[str, Any], r2: dict[str, Any]):
        rec1 = _evaluate_semantic_relevance(q, r1)
        rec2 = _evaluate_semantic_relevance(q, r2)
        self.assertEqual(rec1["classification"], rec2["classification"], f"Variants differ in classification: {rec1} vs {rec2}")

    def test_invariance_01_formal_vs_informal_retry(self):
        q = {"text": "Como evitar retry agressivo e tempestade de requisições?"}
        r_formal = {"reconstructed_text": "Eu utilizaria exponential backoff com jitter para reduzir a sincronização dos retries."}
        r_informal = {"reconstructed_text": "Eu colocaria um backoff com jitter nos retries pra evitar a tempestade."}
        self._assert_equivalent(q, r_formal, r_informal)

    def test_invariance_02_short_vs_long_docker(self):
        q = {"text": "Como o Docker isola processos?"}
        r_short = {"reconstructed_text": "Usa namespaces e cgroups no kernel."}
        r_long = {"reconstructed_text": "O mecanismo de isolamento é construído essencialmente combinando namespaces para visibilidade e cgroups para controle de recursos no kernel."}
        self._assert_equivalent(q, r_short, r_long)

    def test_invariance_03_technical_vs_plain_concurrency(self):
        q = {"text": "Como evitar que duas escritas concorrentes sobrescrevam alterações?"}
        r_tech = {"reconstructed_text": "Implementando optimistic concurrency control com versionamento atômico no commit."}
        r_plain = {"reconstructed_text": "Boto uma coluna de versão lá e na hora de salvar vejo se ninguém mudou antes de mim."}
        self._assert_equivalent(q, r_tech, r_plain)

    def test_invariance_04_self_correction_occ(self):
        q = {"text": "Como evitar conflito de escrita simultânea sem lock pessimista?"}
        r_clean = {"reconstructed_text": "Uso versionamento atômico checado no momento do commit."}
        r_corrected = {"reconstructed_text": "Eu usaria lock pessimista... quer dizer, na verdade para não bloquear a linha eu uso controle otimista com versionamento antes do commit."}
        self._assert_equivalent(q, r_clean, r_corrected)

    def test_invariance_05_circuit_breaker(self):
        q = {"text": "Como proteger uma arquitetura quando um serviço dependente começa a falhar continuamente?"}
        r_en = {"reconstructed_text": "Colocaria circuit breaker para abrir o circuito e retornar fallback."}
        r_pt = {"reconstructed_text": "Implementaria um disjuntor que interrompe requisições temporariamente e aciona uma resposta degradada."}
        self._assert_equivalent(q, r_en, r_pt)

    def test_invariance_06_tracing_correlation(self):
        q = {"text": "Como rastrear chamadas através de múltiplos microsserviços?"}
        r_a = {"reconstructed_text": "Injetaria trace e span nos headers propagando o contexto downstream."}
        r_b = {"reconstructed_text": "Passo correlation ID no cabeçalho HTTP repassando pra cada serviço chamado."}
        self._assert_equivalent(q, r_a, r_b)

    def test_invariance_07_rate_limit(self):
        q = {"text": "Como restringir o volume de chamadas por usuário para evitar sobrecarga?"}
        r_a = {"reconstructed_text": "Token bucket limitando taxa por cliente."}
        r_b = {"reconstructed_text": "Aplicaria algoritmo de balde de fichas para descartar requisições que excedam a taxa permitida."}
        self._assert_equivalent(q, r_a, r_b)

    def test_invariance_08_idempotency(self):
        q = {"text": "Como evitar duplicidade de cobrança em compras online?"}
        r_a = {"reconstructed_text": "Usaria token de idempotência checado em tabela de deduplicação."}
        r_b = {"reconstructed_text": "Gero uma chave única na transação e rejeito requisições repetidas."}
        self._assert_equivalent(q, r_a, r_b)

    def test_invariance_09_deadlock(self):
        q = {"text": "Como prevenir impasses mútuos entre transações?"}
        r_a = {"reconstructed_text": "Adquirindo travas em ordem hierárquica estrita."}
        r_b = {"reconstructed_text": "Estabeleceria uma ordem estrita e global para aquisição de recursos em todas as operações."}
        self._assert_equivalent(q, r_a, r_b)

    def test_invariance_10_backpressure(self):
        q = {"text": "O que fazer quando a entrada de mensagens supera o esgotamento da fila?"}
        r_a = {"reconstructed_text": "Aplicaria backpressure com buffers delimitados e desaceleração do fluxo de ingestão."}
        r_b = {"reconstructed_text": "O consumidor sinaliza ao produtor a taxa que consegue absorver, aplicando contrapressão no fluxo."}
        self._assert_equivalent(q, r_a, r_b)

    def test_invariance_11_duckdb_execution(self):
        q = {"text": "Como o DuckDB processa consultas com alta performance?"}
        r_a = {"reconstructed_text": "Execução colunar e vetorizada in-process."}
        r_b = {"reconstructed_text": "Ele processa os dados de forma colunar e vetorizada diretamente no mesmo processo da aplicação."}
        self._assert_equivalent(q, r_a, r_b)

    def test_invariance_12_virtual_threads(self):
        q = {"text": "Como funcionam as virtual threads no Java?"}
        r_a = {"reconstructed_text": "São threads virtuais leves montadas em carrier threads pela JVM."}
        r_b = {"reconstructed_text": "A JVM gerencia threads leves de usuário que não ocupam threads do sistema operacional enquanto bloqueadas."}
        self._assert_equivalent(q, r_a, r_b)

    def test_invariance_13_dependency_injection(self):
        q = {"text": "Qual o objetivo da inversão de controle?"}
        r_a = {"reconstructed_text": "Desacoplar componentes injetando dependências externamente."}
        r_b = {"reconstructed_text": "Permitir que a classe receba o que precisa de fora sem instanciar os objetos por conta própria."}
        self._assert_equivalent(q, r_a, r_b)

    def test_invariance_14_cache_ttl(self):
        q = {"text": "Como evitar acúmulo de dados desatualizados na memória de cache?"}
        r_a = {"reconstructed_text": "Configurar TTL com expiração automática e invalidação explícita."}
        r_b = {"reconstructed_text": "Colocar tempo de vida nas chaves e expurgar sempre que houver atualização no registro."}
        self._assert_equivalent(q, r_a, r_b)

    def test_invariance_15_regression_detection(self):
        q = {"text": "Como detectar degradação de performance após um novo deploy?"}
        r_a = {"reconstructed_text": "Compararia percentil 99 de latência e taxa de erro da nova versão contra baseline histórica."}
        r_b = {"reconstructed_text": "Analisaria o P99 de resposta comparando com as métricas antes do deploy via telemetria."}
        self._assert_equivalent(q, r_a, r_b)


class Stage3175GenericTokenTrapsTests(unittest.TestCase):
    """Category I: Generic tokens (cluster, recurso, transação, etc.) cannot falsely produce DIRECT (>= 15 cases)."""

    def test_generic_01_recurso_in_rest(self):
        q = {"text": "Como configurar particionamento de tópicos no Kafka?"}
        r = {"reconstructed_text": "Dividimos recursos importantes em instâncias separadas para organizar os dados."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")

    def test_generic_02_transacao_in_concurrency(self):
        q = {"text": "Como configurar o isolamento de rede entre containers Docker?"}
        r = {"reconstructed_text": "A transação entre sistemas requer validações frequentes no banco."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "OFF_TOPIC")

    def test_generic_03_cluster_in_kubernetes(self):
        q = {"text": "Como funciona o modelo de atores em concorrência?"}
        r = {"reconstructed_text": "Nosso cluster de computadores tem nós espalhados pelo mundo."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")

    def test_generic_04_endpoint_in_api(self):
        q = {"text": "Como otimizar consultas relacionais usando índices B-Tree?"}
        r = {"reconstructed_text": "Criamos um endpoint rápido para receber dados de clientes."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "OFF_TOPIC")

    def test_generic_05_dados_in_cache(self):
        q = {"text": "Como funciona o garbage collection na JVM?"}
        r = {"reconstructed_text": "Os dados trafegam pela rede e são gravados no disco rígido."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")

    def test_generic_06_servico_in_architecture(self):
        q = {"text": "Como funciona a ordenação esparsa no ClickHouse?"}
        r = {"reconstructed_text": "Um serviço de atendimento deve prestar bom suporte aos usuários."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")

    def test_generic_07_instancia_in_cloud(self):
        q = {"text": "Como evitar conflito de escrita simultânea sem lock?"}
        r = {"reconstructed_text": "Subimos uma nova instância da máquina virtual para suportar a demanda."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "OFF_TOPIC")

    def test_generic_08_tabela_in_sql(self):
        q = {"text": "Como o Istio intercepta tráfego de rede no cluster?"}
        r = {"reconstructed_text": "Coloquei as informações em uma tabela organizada no Excel."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")

    def test_generic_09_rede_in_networking(self):
        q = {"text": "Como desacoplar classes usando inversão de controle?"}
        r = {"reconstructed_text": "A rede Wi-Fi do escritório estava instável na semana passada."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")

    def test_generic_10_camada_in_architecture(self):
        q = {"text": "Como o eBPF filtra pacotes de rede no kernel?"}
        r = {"reconstructed_text": "Passamos uma camada de verniz para proteger o acabamento da mesa."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "OFF_TOPIC")

    def test_generic_11_processo_in_os(self):
        q = {"text": "Como funciona o algoritmo Raft no CockroachDB?"}
        r = {"reconstructed_text": "O processo de compras da empresa passa por aprovação da gerência."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")

    def test_generic_12_sistema_in_systems(self):
        q = {"text": "Como configurar o exporter OTLP no OpenTelemetry?"}
        r = {"reconstructed_text": "O sistema solar é composto por planetas orbitando em torno do sol."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "OFF_TOPIC")

    def test_generic_13_token_in_auth(self):
        q = {"text": "Como o DuckDB executa consultas colunares vetorizadas?"}
        r = {"reconstructed_text": "Comprei um token de metrô para pegar o trem no centro da cidade."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")

    def test_generic_14_nuvem_in_cloud(self):
        q = {"text": "Como evitar que uma falha em cascata derrube o sistema?"}
        r = {"reconstructed_text": "Havia uma nuvem escura no céu prevendo chuva forte à tarde."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")

    def test_generic_15_objeto_in_oop(self):
        q = {"text": "Como o NATS JetStream oferece entrega at-least-once?"}
        r = {"reconstructed_text": "Esqueci um objeto metálico sobre a bancada do laboratório."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")


class Stage3175ValidAdjacentMechanismsTests(unittest.TestCase):
    """Category J: Legitimate alternative mechanisms solving the question demand (>= 15 cases)."""

    def test_adjacent_01_cas_for_concurrency(self):
        q = {"text": "Como evitar inconsistências em escritas concorrentes sem locks de banco?"}
        r = {"reconstructed_text": "Usaria instruções atômicas compare-and-swap CAS em memória compartilhada."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_adjacent_02_distributed_lock_for_concurrency(self):
        q = {"text": "Como evitar escritas concorrentes simultâneas no mesmo recurso distribuído?"}
        r = {"reconstructed_text": "Usaria lock distribuído com chave exclusiva temporária e renovação de lease."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_adjacent_03_outbox_for_consistency(self):
        q = {"text": "Como garantir consistência entre dois serviços sem transação distribuída em duas fases?"}
        r = {"reconstructed_text": "Adotaria transactional outbox pattern persistindo eventos na mesma transação local do banco."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_adjacent_04_saga_for_transactions(self):
        q = {"text": "Como orquestrar transações de negócios entre múltiplos microsserviços?"}
        r = {"reconstructed_text": "Implementaria padrão Saga com compensação de falhas em caso de rollback."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_adjacent_05_leaky_bucket_for_rate_limiting(self):
        q = {"text": "Como restringir o volume de chamadas por usuário para evitar sobrecarga?"}
        r = {"reconstructed_text": "Aplicaria algoritmo de leaky bucket com taxa de saída constante."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_adjacent_06_sliding_window_for_rate_limiting(self):
        q = {"text": "Como proteger endpoints públicos contra rajadas abusivas de requisições?"}
        r = {"reconstructed_text": "Usaria sliding window log limitando requisições no intervalo de tempo."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_adjacent_07_w3c_tracecontext(self):
        q = {"text": "Como rastrear requisições através de múltiplos serviços sem perder o contexto?"}
        r = {"reconstructed_text": "Propagaria cabeçalhos no padrão W3C TraceContext com traceparent e tracestate."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_adjacent_08_cursor_pagination(self):
        q = {"text": "Como estruturar a paginação de recursos em uma API de alto volume?"}
        r = {"reconstructed_text": "Adotaria paginação baseada em cursor para evitar o custo de offsets profundos."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_adjacent_09_dead_letter_queue(self):
        q = {"text": "Como lidar com mensagens corrompidas que quebram consumidores na fila?"}
        r = {"reconstructed_text": "Encaminharia para uma dead-letter queue após esgotar o limite de retentativas."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_adjacent_10_change_data_capture(self):
        q = {"text": "Como sincronizar alterações do banco relacional com um motor de busca sem travar a escrita?"}
        r = {"reconstructed_text": "Utilizaria Change Data Capture CDC lendo o WAL do banco assincronamente."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_adjacent_11_read_replicas(self):
        q = {"text": "Como acelerar consultas de leitura sem comprometer as transações de escrita do banco?"}
        r = {"reconstructed_text": "Direcionaria consultas analíticas para réplicas de leitura com replicação assíncrona."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_adjacent_12_graphql_dataloader(self):
        q = {"text": "Como resolver o problema N+1 de consultas no backend?"}
        r = {"reconstructed_text": "Implementaria DataLoader para agrupar e acumular IDs em uma única consulta em lote."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_adjacent_13_mtls_service_mesh(self):
        q = {"text": "Como garantir criptografia e autenticação mútua de ponta a ponta entre pods?"}
        r = {"reconstructed_text": "Habilitaria mTLS automático no service mesh com rotação de certificados."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_adjacent_14_immutable_infrastructure(self):
        q = {"text": "Como garantir reprodutibilidade e evitar desvios de configuração em servidores?"}
        r = {"reconstructed_text": "Adotaria infraestrutura imutável gerando imagens de máquinas pré-construídas."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_adjacent_15_bloom_filter(self):
        q = {"text": "Como verificar rapidamente se uma chave não existe antes de fazer leitura em disco?"}
        r = {"reconstructed_text": "Usaria um filtro de Bloom probabilístico em memória para eliminar leituras desnecessárias."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))


class Stage3175UnknownAndUncertaintyTests(unittest.TestCase):
    """Category K: Structurally insufficient evidence yields UNKNOWN or INSUFFICIENT (>= 10 cases)."""

    def test_unknown_01_empty_response(self):
        q = {"text": "Como funciona o garbage collection na JVM?"}
        r = {"reconstructed_text": ""}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec.get("needs_review"))

    def test_unknown_02_unlinked_response(self):
        q = {"text": "Como funciona o garbage collection na JVM?"}
        r = {"question_id": "unknown", "reconstructed_text": "Qualquer coisa aqui."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec.get("needs_review"))

    def test_unknown_03_conversational_filler(self):
        q = {"text": "Como você estruturaria a observabilidade da aplicação?"}
        r = {"reconstructed_text": "Sim, beleza, concordo."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    def test_unknown_04_admitted_ignorance(self):
        q = {"text": "Como o eBPF insere probes dinâmicos no kernel?"}
        r = {"reconstructed_text": "Eu não sei, conheço muito pouco dessa parte."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    def test_unknown_05_fragmented_sim(self):
        q = {"text": "Como funciona o particionamento no Kafka?"}
        r = {"reconstructed_text": "Sim, aham."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    def test_unknown_06_superficial_acknowledgment(self):
        q = {"text": "Qual a diferença entre threads virtuais e threads de plataforma?"}
        r = {"reconstructed_text": "Top, perfeito, entendi."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    def test_unknown_07_admitted_shallow_knowledge(self):
        q = {"text": "Como configurar políticas de eviction no Redis?"}
        r = {"reconstructed_text": "Sei bem por cima, quase nada na verdade."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    def test_unknown_08_memory_blank(self):
        q = {"text": "Como funciona o handshake TLS 1.3?"}
        r = {"reconstructed_text": "Não lembro agora de cabeça."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    def test_unknown_09_not_mastered(self):
        q = {"text": "Como implementar consensus Paxos em sistemas distribuídos?"}
        r = {"reconstructed_text": "Não domino essa parte teórica."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    def test_unknown_10_whitespace_response(self):
        q = {"text": "Como projetar uma fila com alta tolerância a falhas?"}
        r = {"reconstructed_text": "   \n\t  "}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec.get("needs_review"))


class Stage3175MutationTests(unittest.TestCase):
    """Category L: Semantic mutation tests (>= 10 mutations). Corrupting the mechanism must change relation."""

    def test_mutation_01_circuit_breaker_inverted(self):
        q = {"text": "Como evitar que a falha de um serviço externo cause indisponibilidade em cascata?"}
        r_correct = {"reconstructed_text": "Usaria circuit breaker para interromper chamadas e retornar fallback."}
        r_inverted = {"reconstructed_text": "Eu evitaria circuit breaker porque ele aumenta a propagação de falhas no sistema."}
        rec_correct = _evaluate_semantic_relevance(q, r_correct)
        rec_inverted = _evaluate_semantic_relevance(q, r_inverted)
        self.assertIn(rec_correct["classification"], ("DIRECT", "SUPPORTING"))
        self.assertNotEqual(rec_inverted.get("relation_type"), "direct_mechanism_assertion")

    def test_mutation_02_alien_domain_substitution(self):
        q = {"text": "Como funciona o isolamento no Docker?"}
        r_correct = {"reconstructed_text": "Usa namespaces e cgroups para isolar processos no kernel."}
        r_mutated = {"reconstructed_text": "Para isolar criamos tabelas no banco relacional com chaves primárias e SQL."}
        rec_correct = _evaluate_semantic_relevance(q, r_correct)
        rec_mutated = _evaluate_semantic_relevance(q, r_mutated)
        self.assertEqual(rec_correct["classification"], "DIRECT")
        self.assertEqual(rec_mutated["classification"], "OFF_TOPIC")

    def test_mutation_03_remove_mechanism_keep_entity(self):
        q = {"text": "Como configurar readiness probe no Kubernetes?"}
        r_full = {"reconstructed_text": "No Kubernetes configuramos a probe no pod com kubelet checando a saúde."}
        r_mutated = {"reconstructed_text": "Temos um cluster de Kubernetes gerenciado na nuvem."}
        rec_full = _evaluate_semantic_relevance(q, r_full)
        rec_mutated = _evaluate_semantic_relevance(q, r_mutated)
        self.assertEqual(rec_full["classification"], "DIRECT")
        self.assertEqual(rec_mutated["classification"], "RELATED")

    def test_mutation_04_buzzword_dilution(self):
        q = {"text": "Como o índice B-Tree acelera consultas no banco relacional?"}
        r_correct = {"reconstructed_text": "A árvore B organiza nós balanceados permitindo busca logarítmica com seek."}
        r_diluted = {"reconstructed_text": "Adotamos arquitetura moderna com escalabilidade em cloud e microsserviços ágeis com metodologia ágil."}
        rec_correct = _evaluate_semantic_relevance(q, r_correct)
        rec_diluted = _evaluate_semantic_relevance(q, r_diluted)
        self.assertEqual(rec_correct["classification"], "DIRECT")
        self.assertEqual(rec_diluted["classification"], "OFF_TOPIC")

    def test_mutation_05_deadlock_lock_order_mutation(self):
        q = {"text": "Como prevenir impasses mútuos entre transações concorrentes?"}
        r_correct = {"reconstructed_text": "Adquirindo travas em ordem hierárquica estrita e global."}
        r_mutated = {"reconstructed_text": "Cada transação adquire travas em ordem aleatória sem nenhuma coordenação prévia."}
        rec_correct = _evaluate_semantic_relevance(q, r_correct)
        rec_mutated = _evaluate_semantic_relevance(q, r_mutated)
        self.assertEqual(rec_correct["classification"], "DIRECT")
        self.assertNotEqual(rec_mutated["classification"], "DIRECT")

    def test_mutation_06_tracing_correlation_removal(self):
        q = {"text": "Como rastrear o caminho de uma chamada entre diferentes serviços?"}
        r_correct = {"reconstructed_text": "Passando IDs de correlação nos envelopes HTTP para amarrar os registros."}
        r_mutated = {"reconstructed_text": "Rodamos os serviços em servidores com bastante memória RAM e discos rápidos."}
        rec_correct = _evaluate_semantic_relevance(q, r_correct)
        rec_mutated = _evaluate_semantic_relevance(q, r_mutated)
        self.assertEqual(rec_correct["classification"], "DIRECT")
        self.assertEqual(rec_mutated["classification"], "OFF_TOPIC")

    def test_mutation_07_rate_limit_inverted_action(self):
        q = {"text": "Como proteger endpoints contra rajadas abusivas?"}
        r_correct = {"reconstructed_text": "Token bucket limitando taxa por cliente e descartando excessos."}
        r_mutated = {"reconstructed_text": "Permitimos que qualquer cliente faça chamadas ilimitadas sem nenhum descarte."}
        rec_correct = _evaluate_semantic_relevance(q, r_correct)
        rec_mutated = _evaluate_semantic_relevance(q, r_mutated)
        self.assertEqual(rec_correct["classification"], "DIRECT")
        self.assertNotEqual(rec_mutated["classification"], "DIRECT")

    def test_mutation_08_multi_aspect_dropped_demand(self):
        q = {"text": "Como projetar uma API REST e estruturar a paginação de recursos?"}
        r_full = {"reconstructed_text": "REST usa verbos HTTP para recursos e a paginação usa cursor ou limit e offset."}
        r_dropped = {"reconstructed_text": "REST expõe recursos via HTTP com verbos semânticos e status codes."}
        rec_full = _evaluate_semantic_relevance(q, r_full)
        rec_dropped = _evaluate_semantic_relevance(q, r_dropped)
        self.assertEqual(rec_full["classification"], "DIRECT")
        self.assertEqual(rec_dropped["classification"], "PARTIAL")

    def test_mutation_09_experience_declaration_to_demonstration(self):
        q = {"text": "Qual sua experiência com Kubernetes?"}
        r_decl = {"reconstructed_text": "Trabalhei dois anos com Kubernetes na empresa anterior."}
        r_demo = {"reconstructed_text": "Trabalhei com Kubernetes por dois anos e, quando tínhamos crashloop, configurávamos readiness probe."}
        specs_decl = _blind_evidence_specs(q, r_decl)
        specs_demo = _blind_evidence_specs(q, r_demo)
        types_decl = [s["type"] for s in specs_decl]
        types_demo = [s["type"] for s in specs_demo]
        self.assertNotIn("demonstrated_experience", types_decl)
        self.assertIn("demonstrated_experience", types_demo)

    def test_mutation_10_empty_catalog_invariance(self):
        """Verifies that clearing _FUNCTIONAL_CAPABILITIES does NOT break semantic classification."""
        q = {"text": "Como funciona o isolamento no Docker?"}
        r = {"reconstructed_text": "Usa namespaces e cgroups para isolar processos e recursos no kernel."}
        # Run with normal catalog
        rec_normal = _evaluate_semantic_relevance(q, r)
        # Run with emptied catalog
        original_cap = dict(_FUNCTIONAL_CAPABILITIES)
        try:
            _FUNCTIONAL_CAPABILITIES.clear()
            rec_empty = _evaluate_semantic_relevance(q, r)
            self.assertEqual(rec_normal["classification"], rec_empty["classification"])
            self.assertEqual(rec_empty["classification"], "DIRECT")
        finally:
            _FUNCTIONAL_CAPABILITIES.update(original_cap)


if __name__ == "__main__":
    unittest.main()
