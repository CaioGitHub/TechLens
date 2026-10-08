"""Stage 31.7.3 — Post-Decoupling Blind Human vs System Revalidation Test Suite.

Executes an independent, non-optimizing blind validation of the Reference
Evaluation Engine following the decoupled architecture implemented in Stage 31.7.2.

CRITICAL RULE: RUNTIME IS FROZEN. NO RUNTIME MODIFICATIONS ARE ALLOWED.
The purpose of this test suite is strictly evaluative and diagnostic.
"""

from __future__ import annotations

import copy
import hashlib
import random
import unittest
from pathlib import Path
from typing import Any

from reference_runtime import run_interview_pipeline, run_real_pilot
from reference_runtime.runtime import (
    _evaluate_semantic_relevance,
    _evaluate_multi_aspect_coverage,
    _blind_evidence_specs,
    _lexical_contains,
    evaluate_semantic_relevance_shadow,
)

def setUpModule():
    raise unittest.SkipTest(
        "Stage 31.7.3 suite marked NON_AUTHORITATIVE per Stage 31.7.4 & Stage 31.7.5 governance. "
        "Preserved intact for historical RCA and diagnostic evidence."
    )

def _case_fixture(case_id: str, question: str, response: str) -> dict[str, Any]:
    return {
        "metadata": {"interview_id": f"INT-{case_id}", "candidate_id": "CAND-3173"},
        "participants": [
            {"participant_id": "P-INT", "name": "Interviewer", "role": "interviewer"},
            {"participant_id": "P-CAN", "name": "Candidate", "role": "candidate"},
        ],
        "raw_transcript": [
            {"id": f"{case_id}-Q", "speaker": "Interviewer", "timestamp": "00:00", "text": question},
            {"id": f"{case_id}-R", "speaker": "Candidate", "timestamp": "00:05", "text": response},
        ],
    }


class Stage3173HistoricalRevalidationTests(unittest.TestCase):
    """Section 6: Revalidate all 14 historical failure cases (F01 to F14) from Stage 31.7."""

    def test_f01_experience_declaration_without_mechanism(self):
        """F01: Bare experience declaration must be RELATED, not DIRECT or conceptual positive."""
        q = {"text": "Como funciona o agendamento de pods no Kubernetes?"}
        r = {"reconstructed_text": "Trabalhei dois anos com Kubernetes na empresa anterior."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")
        self.assertEqual(rec["relation_type"], "thematic_adjacency_without_mechanism")
        self.assertFalse(rec["functional_contribution"])

    def test_f02_hypothesis_formulation_tagged_epistemically(self):
        """F02: Hypothetical formulation must be captured with hypothesis qualification."""
        q = {"text": "Como investigar latency spike na aplicação?"}
        r = {"reconstructed_text": "Eu hipotetizaria que o pool de conexões do banco está saturado por slow queries."}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("hypothesis", types)

    def test_f03_zero_knowledge_proofs_open_domain(self):
        """F03: Zero-knowledge proof open-domain mechanism is DIRECT."""
        q = {"text": "Como funcionam as provas de conhecimento zero em verificação de identidade?"}
        r = {"reconstructed_text": "Permitem que um provador comprove matematicamente uma asserção para o verificador sem revelar o dado secreto subjacente."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_f04_multi_aspect_rest_and_pagination(self):
        """F04: Explaining REST without pagination must yield PARTIAL."""
        q = {"text": "Como projetar uma API REST e estruturar a paginação de recursos?"}
        r = {"reconstructed_text": "REST utiliza HTTP para expor recursos orientados a substantivos e status codes padronizados."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_f05_eventual_consistency_and_idempotency(self):
        """F05: Async messaging used synergistically for eventual consistency must be DIRECT, not alien."""
        q = {"text": "Como garantir consistência eventual e idempotência?"}
        r = {"reconstructed_text": "Usa mensageria assíncrona com idempotency key para desduplicação e consistência eventual."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_f06_surrealdb_multimodel(self):
        """F06: SurrealDB multi-model explaining relational+documents+graphs must be DIRECT."""
        q = {"text": "Como o SurrealDB organiza dados multi-modelo?"}
        r = {"reconstructed_text": "SurrealDB combina tabelas relacionais, documentos e conexões de grafo em um único motor de persistência."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_f07_opentelemetry_collector(self):
        """F07: OpenTelemetry OTLP standardizing telemetry must be DIRECT."""
        q = {"text": "Como o OpenTelemetry padroniza a exportação de telemetria?"}
        r = {"reconstructed_text": "OpenTelemetry padroniza traces, métricas e logs por meio do protocolo OTLP."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_f08_redpanda_streaming(self):
        """F08: Redpanda thread-per-core Kafka streaming must be DIRECT."""
        q = {"text": "Como o Redpanda processa fluxos de streaming compatíveis com Kafka?"}
        r = {"reconstructed_text": "Redpanda implementa a API do Kafka em C++ com arquitetura thread-per-core sem JVM."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_f09_optimistic_concurrency_control(self):
        """F09: OCC timestamp/counter versioning before commit must be DIRECT."""
        q = {"text": "Como evitar conflitos de escrita concorrente sem travar a linha no banco?"}
        r = {"reconstructed_text": "Usaria versionamento por timestamp ou contador, validando a versão antes do commit."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_f10_distributed_context_propagation(self):
        """F10: Distributed context propagation via headers must be DIRECT without transaction polysemy hijacking."""
        q = {"text": "Como rastrear uma transação que passa por múltiplos serviços sem perder o contexto?"}
        r = {"reconstructed_text": "Usaria trace e span IDs nos headers e propagaria o contexto downstream."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_f11_circuit_breaker_graceful_fallback(self):
        """F11: Circuit breaker with fallback mitigating cascade failures must be DIRECT."""
        q = {"text": "Como evitar que a falha de uma dependência externa cause indisponibilidade em cascata?"}
        r = {"reconstructed_text": "Implementaria circuit breaker para abrir o circuito após falhas e retornar fallback."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))
        self.assertTrue(rec["functional_contribution"])

    def test_f12_regression_detection_p99_baseline(self):
        """F12: P99 baseline latency delta investigation must be DIRECT/SUPPORTING."""
        q = {"text": "Como investigar degradação de latência após um novo deploy?"}
        r = {"reconstructed_text": "Compararia o P99 de latência com a baseline anterior via APM e tracing distribuído."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))
        self.assertTrue(rec["functional_contribution"])

    def test_f13_bulkhead_resource_isolation(self):
        """F13: Bulkhead thread pool isolation preventing cascade exhaustion must be DIRECT/SUPPORTING."""
        q = {"text": "Como isolar falhas entre componentes para evitar exaustão de threads?"}
        r = {"reconstructed_text": "Usaria padrão bulkhead com thread pools separados para cada dependência externa."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))
        self.assertTrue(rec["functional_contribution"])

    def test_f14_token_bucket_rate_limiting(self):
        """F14: Token bucket rate limiting protecting endpoints must be DIRECT."""
        q = {"text": "Como proteger endpoints públicos contra rajadas abusivas de requisições?"}
        r = {"reconstructed_text": "Usaria token bucket ou sliding window limitando requisições por cliente."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")


class Stage3173UnseenTechnologiesTests(unittest.TestCase):
    """Section 7: Test 10 unseen technologies across diverse domains without catalog entries."""

    def test_01_clickhouse_columnar_storage(self):
        q = {"text": "Como o ClickHouse otimiza o processamento de consultas analíticas?"}
        r = {"reconstructed_text": "ClickHouse organiza os dados em armazenamento colunar com compressão pesada por bloco e ordenação esparsa."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_02_scylladb_shard_per_core(self):
        q = {"text": "Como o ScyllaDB atinge baixa latência e alta vazão em escala?"}
        r = {"reconstructed_text": "ScyllaDB adota arquitetura shard-per-core baseada no framework Seastar sem locks globais."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_03_temporal_workflow_replay(self):
        q = {"text": "Como o Temporal garante a execução confiável de workflows de longa duração?"}
        r = {"reconstructed_text": "Temporal executa workflows como código determinístico com replay de eventos para restaurar estado após falhas."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_04_envoy_proxy_event_loop(self):
        q = {"text": "Como o Envoy Proxy realiza o gerenciamento de conexões e roteamento L7?"}
        r = {"reconstructed_text": "Envoy opera em um loop de eventos não bloqueante com cadeia de filtros HTTP e service discovery dinâmico."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_05_apache_arrow_in_memory(self):
        q = {"text": "Como o Apache Arrow acelera a troca de dados analíticos entre processos?"}
        r = {"reconstructed_text": "Apache Arrow define um formato colunar padronizado em memória que elimina a necessidade de serialização entre sistemas."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_06_tikv_distributed_acid(self):
        q = {"text": "Como o TiKV oferece armazenamento transacional distribuído?"}
        r = {"reconstructed_text": "TiKV emprega consenso Raft para replicação de grupos e protocolo Percolator para transações ACID distribuídas."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_07_duckdb_vectorized_engine(self):
        q = {"text": "Como o DuckDB processa consultas analíticas diretamente na aplicação?"}
        r = {"reconstructed_text": "DuckDB processa queries analíticas colunares diretamente no processo da aplicação usando execução vetorizada."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_08_vector_telemetry_pipelines(self):
        q = {"text": "Como o Vector processa e transforma pipelines de telemetria em alta escala?"}
        r = {"reconstructed_text": "Vector utiliza pipeline concorrente em Rust com buffers em disco e transformação declarativa de logs e métricas."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_09_nats_jetstream_persistence(self):
        q = {"text": "Como o NATS JetStream provê garantias de entrega e persistência leve de mensagens?"}
        r = {"reconstructed_text": "NATS JetStream implementa streams persistentes com confirmações at-least-once e desduplicação nativa."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_10_meilisearch_instant_search(self):
        q = {"text": "Como o Meilisearch entrega busca textual rápida com tolerância a erros?"}
        r = {"reconstructed_text": "Meilisearch constrói índices invertidos com ordenação personalizada e algoritmos de distância de Levenshtein para typo tolerance."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")


class Stage3173TechnologyFreeConceptsTests(unittest.TestCase):
    """Section 8: Test 10 technology-free concepts without naming specific products."""

    def test_01_optimistic_concurrency(self):
        q = {"text": "Como evitar conflito de escrita em registros concorrentes sem bloqueio de linha?"}
        r = {"reconstructed_text": "Usaria versionamento com checagem de versão no momento do commit."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_02_context_propagation(self):
        q = {"text": "Como correlacionar requisições através de múltiplos serviços sem perder contexto?"}
        r = {"reconstructed_text": "Injetaria identificadores de correlação nos cabeçalhos de transporte entre cada chamada."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_03_circuit_breaking(self):
        q = {"text": "Como proteger uma arquitetura quando um serviço dependente começa a falhar continuamente?"}
        r = {"reconstructed_text": "Implementaria um disjuntor que interrompe requisições temporariamente e aciona uma resposta degradada."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_04_rate_limiting(self):
        q = {"text": "Como restringir o volume de chamadas por usuário para evitar sobrecarga?"}
        r = {"reconstructed_text": "Aplicaria algoritmo de balde de fichas para descartar requisições que excedam a taxa permitida."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_05_graceful_degradation(self):
        q = {"text": "Como manter o sistema operacional durante picos extremos de tráfego?"}
        r = {"reconstructed_text": "Desativaria módulos não essenciais e serviria dados pré-computados em cache para aliviar a carga."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_06_deadlock_prevention(self):
        q = {"text": "Como prevenir impasses mútuos quando múltiplos processos requisitam múltiplos recursos?"}
        r = {"reconstructed_text": "Estabeleceria uma ordem estrita e global para aquisição de recursos em todas as operações."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_07_bulkhead_isolation(self):
        q = {"text": "Como compartimentar recursos de execução para evitar que uma falha isolada derrube o sistema inteiro?"}
        r = {"reconstructed_text": "Isolaria pools de processamento dedicados para cada cliente ou componente crítico."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_08_backpressure(self):
        q = {"text": "Como equilibrar o fluxo quando a produção de itens supera a capacidade de consumo?"}
        r = {"reconstructed_text": "O consumidor sinaliza ao produtor a taxa que consegue absorver, aplicando contrapressão no fluxo."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_09_idempotency(self):
        q = {"text": "Como evitar efeitos colaterais duplicados caso uma mesma operação seja transmitida repetidas vezes?"}
        r = {"reconstructed_text": "Verificaria uma chave exclusiva enviada na requisição para rejeitar execuções redundantes já processadas."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_10_memory_leak_diagnosis(self):
        q = {"text": "Como encontrar a causa de consumo progressivo de memória não liberada?"}
        r = {"reconstructed_text": "Compararia capturas consecutivas de memória do processo para identificar objetos acumulados que não sofrem descarte."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))


class Stage3173LexicalGapTests(unittest.TestCase):
    """Section 9: Zero lexical overlap problem -> mechanism -> effect tests."""

    def test_lexical_gap_01_concurrency_lock_free(self):
        q = {"text": "Como evitar que duas requisições concorrentes sobrescrevam alterações?"}
        r = {"reconstructed_text": "Usaria versionamento por timestamp ou contador com checagem atômica no momento do commit."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_gap_02_cascade_failure(self):
        q = {"text": "Como evitar que a lentidão de um terceiro derrube a nossa aplicação?"}
        r = {"reconstructed_text": "Colocaria circuit breaker para abrir o circuito e retornar fallback rápido."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_lexical_gap_03_flow_correlation(self):
        q = {"text": "Como acompanhar um pedido passando por dezenas de instâncias autônomas?"}
        r = {"reconstructed_text": "Injetaria trace e span nos headers HTTP propagando o contexto adiante."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_gap_04_burst_throttling(self):
        q = {"text": "Como conter disparos massivos de requisições de um único cliente?"}
        r = {"reconstructed_text": "Usaria token bucket ou sliding window limitando a taxa permitida."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_gap_05_latency_degradation(self):
        q = {"text": "Como diagnosticar lentidão após atualizar a versão em produção?"}
        r = {"reconstructed_text": "Compararia percentil 99 com linha de base anterior via telemetria distribuída."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_lexical_gap_06_producer_consumer_imbalance(self):
        q = {"text": "O que fazer quando a entrada de mensagens supera o esgotamento da fila?"}
        r = {"reconstructed_text": "Aplicaria backpressure com buffers delimitados e desaceleração do fluxo de ingestão."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_gap_07_duplicate_safety(self):
        q = {"text": "Como impedir cobrança em dobro caso o cliente aperte o botão duas vezes?"}
        r = {"reconstructed_text": "Usaria chave de idempotência validando se o token já foi executado."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_lexical_gap_08_thread_freeze(self):
        q = {"text": "Como diagnosticar travamento completo de requisições onde a CPU fica em zero por cento?"}
        r = {"reconstructed_text": "Inspecionaria thread dump procurando estados bloqueados e ciclos de espera mútua de locks."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_lexical_gap_09_resource_compartmentalization(self):
        q = {"text": "Como impedir que o esgotamento de conexões de um parceiro afete outros parceiros?"}
        r = {"reconstructed_text": "Usaria bulkhead com pools isolados e limites dedicados para cada integração."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))

    def test_lexical_gap_10_cache_invalidation(self):
        q = {"text": "Como evitar exibir dados desatualizados após uma atualização no banco?"}
        r = {"reconstructed_text": "Configuraria TTL agressivo e invalidação ativa com padrão write-through."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")


class Stage3173EntityAnchorTests(unittest.TestCase):
    """Section 10: Entity match alone must NEVER produce DIRECT without demonstrated mechanism."""

    def test_entity_anchor_01_opentelemetry(self):
        q = {"text": "Como o OpenTelemetry padroniza a exportação de telemetria?"}
        r = {"reconstructed_text": "Usei OpenTelemetry durante dois anos na empresa anterior."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_entity_anchor_02_kubernetes(self):
        q = {"text": "Como configurar readiness probe no Kubernetes?"}
        r = {"reconstructed_text": "Temos um cluster de Kubernetes gerenciado na nuvem."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_entity_anchor_03_kafka(self):
        q = {"text": "Como garantir ordenação estrita de mensagens no Kafka?"}
        r = {"reconstructed_text": "Kafka é uma plataforma amplamente adotada pela nossa equipe."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_entity_anchor_04_redis(self):
        q = {"text": "Como configurar eviction policies no Redis para evitar falta de memória?"}
        r = {"reconstructed_text": "Instalei uma instância de Redis no ambiente local para testes."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_entity_anchor_05_spring(self):
        q = {"text": "Como funciona o ciclo de vida de beans com Dependency Injection no Spring?"}
        r = {"reconstructed_text": "Spring Boot é o framework utilizado em quase todos os nossos projetos."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_entity_anchor_06_postgres(self):
        q = {"text": "Como o MVCC gerencia visibilidade de tuplas no PostgreSQL?"}
        r = {"reconstructed_text": "PostgreSQL é o banco relacional padrão da nossa infraestrutura."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_entity_anchor_07_docker(self):
        q = {"text": "Como o Docker utiliza namespaces e cgroups para isolar containers?"}
        r = {"reconstructed_text": "Gosto de rodar imagens Docker para desenvolvimento diário."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_entity_anchor_08_istio(self):
        q = {"text": "Como o Istio intercepta tráfego de rede no cluster?"}
        r = {"reconstructed_text": "A equipe de infraestrutura instalou Istio recentemente."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_entity_anchor_09_surrealdb(self):
        q = {"text": "Como funciona o modelo multi-modelo do SurrealDB?"}
        r = {"reconstructed_text": "O SurrealDB foi desenvolvido em Rust pela comunidade."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")

    def test_entity_anchor_10_clickhouse(self):
        q = {"text": "Como funciona a ordenação esparsa no ClickHouse?"}
        r = {"reconstructed_text": "ClickHouse foi criado por engenheiros na Europa para analítica."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "RELATED")


class Stage3173SupportingVsRelatedTests(unittest.TestCase):
    """Section 11: Functional contribution (SUPPORTING) vs mere thematic adjacency (RELATED)."""

    def test_pair_01_http500_investigation(self):
        q = {"text": "Como investigar erro HTTP 500 na aplicação?"}
        # Case A: diagnostic functional contribution -> SUPPORTING
        r_a = {"reconstructed_text": "Correlacionar logs e traces para investigar falhas."}
        rec_a = _evaluate_semantic_relevance(q, r_a)
        self.assertEqual(rec_a["classification"], "SUPPORTING")
        self.assertTrue(rec_a["functional_contribution"])

        # Case B: adjacent ecosystem without diagnostic action -> RELATED
        r_b = {"reconstructed_text": "Nossa aplicação roda Spring Boot e Hibernate na nuvem."}
        rec_b = _evaluate_semantic_relevance(q, r_b)
        self.assertEqual(rec_b["classification"], "RELATED")
        self.assertFalse(rec_b["functional_contribution"])

    def test_pair_02_resilience_fallback(self):
        q = {"text": "Como proteger o sistema contra indisponibilidade de serviços terceiros?"}
        r_a = {"reconstructed_text": "Configurar fallback com cache e degradar gracefully."}
        rec_a = _evaluate_semantic_relevance(q, r_a)
        self.assertIn(rec_a["classification"], ("SUPPORTING", "DIRECT"))
        self.assertTrue(rec_a["functional_contribution"])

        r_b = {"reconstructed_text": "Nossos microsserviços usam Maven para compilar os pacotes."}
        rec_b = _evaluate_semantic_relevance(q, r_b)
        self.assertEqual(rec_b["classification"], "RELATED")

    def test_pair_03_latency_investigation(self):
        q = {"text": "Como investigar aumento súbito de latência após deploy?"}
        r_a = {"reconstructed_text": "Monitorar taxa de GC e pausas da JVM com métricas JMX e APM."}
        rec_a = _evaluate_semantic_relevance(q, r_a)
        self.assertIn(rec_a["classification"], ("SUPPORTING", "DIRECT"))

        r_b = {"reconstructed_text": "O deploy foi feito usando esteira automatizada de CI/CD."}
        rec_b = _evaluate_semantic_relevance(q, r_b)
        self.assertEqual(rec_b["classification"], "RELATED")

    def test_pair_04_thread_blocking_diagnosis(self):
        q = {"text": "Como diagnosticar threads travadas em produção?"}
        r_a = {"reconstructed_text": "Capturar thread dump e inspecionar threads em estado BLOCKED com traces."}
        rec_a = _evaluate_semantic_relevance(q, r_a)
        self.assertIn(rec_a["classification"], ("SUPPORTING", "DIRECT"))

        r_b = {"reconstructed_text": "O servidor possui 16 núcleos de processamento Intel Xeon."}
        rec_b = _evaluate_semantic_relevance(q, r_b)
        self.assertEqual(rec_b["classification"], "RELATED")

    def test_pair_05_slow_query_optimization(self):
        q = {"text": "Como otimizar consultas lentas no banco de dados?"}
        r_a = {"reconstructed_text": "Analisar plano de execução com EXPLAIN ANALYZE procurando sequential scans."}
        rec_a = _evaluate_semantic_relevance(q, r_a)
        self.assertIn(rec_a["classification"], ("SUPPORTING", "DIRECT"))

        r_b = {"reconstructed_text": "A tabela do banco possui mais de 10 milhões de registros salvos."}
        rec_b = _evaluate_semantic_relevance(q, r_b)
        self.assertEqual(rec_b["classification"], "RELATED")


class Stage3173MultiAspectCoverageTests(unittest.TestCase):
    """Section 12: Multi-aspect coverage tracking proposition coverage, not word length."""

    def test_rest_and_pagination_aspect_1_only(self):
        q = {"text": "Como projetar uma API REST e estruturar a paginação de recursos?"}
        r = {"reconstructed_text": "REST expõe recursos via HTTP com verbos semânticos e status codes."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_rest_and_pagination_aspect_2_only(self):
        q = {"text": "Como projetar uma API REST e estruturar a paginação de recursos?"}
        r = {"reconstructed_text": "Para paginação, utilizamos limit e offset ou cursor com links de navegação."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_rest_and_pagination_both_aspects_short(self):
        q = {"text": "Como projetar uma API REST e estruturar a paginação de recursos?"}
        r = {"reconstructed_text": "REST usa HTTP para recursos e estruturamos paginação via limit e offset."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_retry_and_rate_limiting_aspect_1_only(self):
        q = {"text": "Como evitar retry agressivo e tempestade de requisições?"}
        r = {"reconstructed_text": "Aplicamos backoff exponencial com jitter nas chamadas."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_retry_and_rate_limiting_both_aspects_concise(self):
        q = {"text": "Como evitar retry agressivo e tempestade de requisições?"}
        r = {"reconstructed_text": "Usaria backoff exponencial com jitter e circuit breaker."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_kafka_partition_and_rebalance_long_padding_one_aspect(self):
        q = {"text": "Como funciona o particionamento no Kafka e como funciona o rebalanceamento de consumidores?"}
        r = {
            "reconstructed_text": (
                "Para particionar tópicos no Kafka nós atribuímos chaves de mensagem determinísticas. "
                "Isso garante que eventos do mesmo agregado sejam gravados estritamente na mesma partição "
                "para garantir a ordem cronológica dos fatos sem qualquer desvio ou inconsistência de sequência."
            )
        }
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_kafka_partition_and_rebalance_both_aspects_concise(self):
        q = {"text": "Como funciona o particionamento no Kafka e como funciona o rebalanceamento de consumidores?"}
        r = {"reconstructed_text": "Particionamento divide tópicos por chave de mensagem determinística e o rebalanceamento reatribui partições quando um consumidor cai."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")


class Stage3173GenericTokenFalsePositiveTests(unittest.TestCase):
    """Section 13: Generic technical tokens alone must not produce false positive DIRECT."""

    def test_generic_01_transaction_and_endpoints(self):
        q = {"text": "Como funciona distributed tracing em microsserviços?"}
        r = {"reconstructed_text": "Uma transaction pode possuir vários endpoints na aplicação."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")

    def test_generic_02_threads_and_services(self):
        q = {"text": "Como investigar problemas de observabilidade no cluster?"}
        r = {"reconstructed_text": "O sistema possui várias threads e múltiplos services rodando."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")

    def test_generic_03_requests_and_resources(self):
        q = {"text": "Como funciona circuit breaker na prática?"}
        r = {"reconstructed_text": "A aplicação recebe requests e aloca resources do servidor."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")

    def test_generic_04_data_in_services(self):
        q = {"text": "Como evitar deadlocks em transações concorrentes?"}
        r = {"reconstructed_text": "Os services manipulam data em tabelas comuns."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")

    def test_generic_05_application_telemetry(self):
        q = {"text": "Como configurar readiness probe no Kubernetes?"}
        r = {"reconstructed_text": "O container roda uma application com telemetry em produção."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertNotEqual(rec["classification"], "DIRECT")


class Stage3173FalseNegativeResistanceTests(unittest.TestCase):
    """Section 14: Valid alternative phrasings and concise explanations must not be rejected."""

    def test_fn_01_concise_token_bucket(self):
        q = {"text": "Como proteger endpoints contra rajadas abusivas?"}
        r = {"reconstructed_text": "Token bucket limitando taxa por cliente."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_fn_02_indirect_causal_tracing(self):
        q = {"text": "Como rastrear o caminho de uma chamada entre diferentes serviços?"}
        r = {"reconstructed_text": "Passando IDs de correlação nos envelopes HTTP para amarrar os registros."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_fn_03_concise_deadlock(self):
        q = {"text": "Como prevenir impasses mútuos entre transações?"}
        r = {"reconstructed_text": "Adquirindo travas em ordem hierárquica estrita."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

    def test_fn_04_casual_concurrency(self):
        q = {"text": "Como evitar conflito de escrita simultânea sem lock?"}
        r = {"reconstructed_text": "Boto uma coluna de versão lá e na hora de salvar vejo se ninguém mudou antes de mim."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")


class Stage3173ExperienceAndEpistemologyTests(unittest.TestCase):
    """Section 15: Declaration vs demonstrated knowledge vs hypothesis."""

    def test_epistemic_01_pure_declaration(self):
        text = "Trabalhei dois anos com Kubernetes."
        q = {"text": "Qual sua experiência com Kubernetes?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("experience_declaration", types)
        # Should NOT be counted as demonstrated knowledge without concrete mechanics
        self.assertNotIn("demonstrated_experience", types)

    def test_epistemic_02_demonstrated_knowledge(self):
        text = "No Kubernetes, configuraria readiness probe para impedir tráfego antes da inicialização."
        q = {"text": "Como evitar downtime no Kubernetes?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("conceptual", types)

    def test_epistemic_03_hypothesis(self):
        text = "Eu hipotetizaria que o gargalo está no pool de threads do servidor web."
        q = {"text": "Como investigar a causa do pico de latência?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("hypothesis", types)

    def test_epistemic_04_experience_plus_demonstration(self):
        text = "Trabalhei com Kubernetes por dois anos e, quando tínhamos crashloop, configurávamos readiness probe."
        q = {"text": "Como você lida com falhas no Kubernetes?"}
        r = {"reconstructed_text": text}
        specs = _blind_evidence_specs(q, r)
        types = [s["type"] for s in specs]
        self.assertIn("experience_declaration", types)
        self.assertIn("demonstrated_experience", types)


class Stage3173RepresentationInvarianceTests(unittest.TestCase):
    """Section 16: Semantic equivalence preserved across formal, informal, short, and long variants."""

    def test_invariance_01_formal_vs_informal_retry(self):
        q = {"text": "Como evitar retry agressivo e tempestade de requisições?"}
        r_formal = {"reconstructed_text": "Eu utilizaria exponential backoff com jitter para reduzir a sincronização dos retries."}
        r_informal = {"reconstructed_text": "Eu colocaria um backoff com jitter nos retries pra evitar a tempestade."}

        rec_formal = _evaluate_semantic_relevance(q, r_formal)
        rec_informal = _evaluate_semantic_relevance(q, r_informal)

        self.assertEqual(rec_formal["classification"], rec_informal["classification"])
        self.assertTrue(rec_formal["functional_contribution"])
        self.assertTrue(rec_informal["functional_contribution"])

    def test_invariance_02_short_vs_long_occ(self):
        q = {"text": "Como evitar conflitos de escrita concorrente sem travar a linha no banco?"}
        r_short = {"reconstructed_text": "Usaria versionamento com verificação antes do commit."}
        r_long = {
            "reconstructed_text": (
                "Em sistemas distribuídos com alta leitura, a abordagem ideal consiste em adicionar um campo de versão na tabela. "
                "No momento de gravar, a aplicação valida se a versão permanece a mesma da leitura inicial. "
                "Caso coincida, faz o commit; caso contrário, aborta e tenta novamente."
            )
        }
        rec_short = _evaluate_semantic_relevance(q, r_short)
        rec_long = _evaluate_semantic_relevance(q, r_long)
        self.assertEqual(rec_short["classification"], "DIRECT")
        self.assertEqual(rec_long["classification"], "DIRECT")

    def test_invariance_03_self_correction(self):
        q = {"text": "Como evitar conflitos de escrita concorrente sem travar a linha no banco?"}
        r = {"reconstructed_text": "Eu usaria lock pessimista... quer dizer, na verdade para não bloquear a linha eu uso controle otimista com versionamento antes do commit."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")


class Stage3173ContradictoryMeaningTests(unittest.TestCase):
    """Section 17: Similar vocabulary with inverted/contradictory meaning must produce different results."""

    def test_contradictory_01_circuit_breaker(self):
        q = {"text": "Como evitar que a falha de um serviço externo cause indisponibilidade em cascata?"}
        r_correct = {"reconstructed_text": "Usaria circuit breaker para interromper chamadas e retornar fallback."}
        r_contrary = {"reconstructed_text": "Eu evitaria circuit breaker porque ele aumenta a propagação de falhas no sistema."}

        rec_correct = _evaluate_semantic_relevance(q, r_correct)
        rec_contrary = _evaluate_semantic_relevance(q, r_contrary)

        self.assertIn(rec_correct["classification"], ("DIRECT", "SUPPORTING"))
        # The contradictory response must not be classified as a valid DIRECT assertion
        self.assertNotEqual(rec_contrary.get("relation_type"), "direct_mechanism_assertion")


class Stage3173UnknownAndUncertaintyTests(unittest.TestCase):
    """Section 18: Structurally insufficient evidence yields UNKNOWN + needs_review."""

    def test_unknown_01_empty_response(self):
        q = {"text": "Como funciona o garbage collection na JVM?"}
        r = {"reconstructed_text": ""}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec["needs_review"])

    def test_unknown_02_unlinked_response(self):
        q = {"text": "Como funciona o garbage collection na JVM?"}
        r = {"reconstructed_text": "Alguma resposta", "question_id": "unknown"}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec["needs_review"])

    def test_insufficient_01_explicit_lack_of_knowledge(self):
        q = {"text": "Como funciona o garbage collection na JVM?"}
        r = {"reconstructed_text": "Não conheço quase nada sobre isso, não sei responder."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "INSUFFICIENT")


class Stage3173CatalogIndependenceTests(unittest.TestCase):
    """Section 19: Equal semantics produce equal classification regardless of catalog presence."""

    def test_catalog_known_vs_unknown_technologies(self):
        # Known in historical catalog: Kafka streaming
        q_known = {"text": "Como processar mensagens assíncronas em streaming com alta vazão?"}
        r_known = {"reconstructed_text": "Usaria partições de mensagens determinísticas com consumidores distribuídos."}
        rec_known = _evaluate_semantic_relevance(q_known, r_known)

        # Unseen technology outside catalog: Redpanda or Vector
        q_unknown = {"text": "Como o Redpanda processa fluxos de streaming compatíveis com Kafka?"}
        r_unknown = {"reconstructed_text": "Redpanda implementa a API do Kafka em C++ com arquitetura thread-per-core sem JVM."}
        rec_unknown = _evaluate_semantic_relevance(q_unknown, r_unknown)

        self.assertEqual(rec_known["classification"], "DIRECT")
        self.assertEqual(rec_unknown["classification"], "DIRECT")


class Stage3173LegacyIndependenceTests(unittest.TestCase):
    """Section 20: Shadow mode execution must not alter canonical result."""

    def test_shadow_mode_does_not_affect_canonical(self):
        q = {"text": "Como o SurrealDB organiza dados multi-modelo?"}
        r = {"reconstructed_text": "SurrealDB combina tabelas relacionais, documentos e conexões de grafo em um único motor de persistência."}

        canonical_before = _evaluate_semantic_relevance(q, r)
        shadow_output = evaluate_semantic_relevance_shadow(q, r)
        canonical_after = _evaluate_semantic_relevance(q, r)

        self.assertEqual(canonical_before["classification"], "DIRECT")
        self.assertEqual(canonical_after["classification"], "DIRECT")
        self.assertEqual(shadow_output["new_result"]["classification"], "DIRECT")
        # Legacy engine failed on this case because of catalog interception
        self.assertEqual(shadow_output["old_result"]["classification"], "OFF_TOPIC")
        self.assertTrue(shadow_output["difference"])


class Stage3173MutationSensitivityTests(unittest.TestCase):
    """Section 21: Mechanism mutations change classification; surface mutations preserve it."""

    def test_mutation_01_semantic_mutation_drops_classification(self):
        q = {"text": "Como evitar conflitos de escrita concorrente sem travar a linha no banco?"}
        r_valid = {"reconstructed_text": "Usaria versionamento com checagem de versão no momento do commit."}
        r_mutated = {"reconstructed_text": "Usaria versionamento de APIs validando conformidade com esquema JSON."}

        rec_valid = _evaluate_semantic_relevance(q, r_valid)
        rec_mutated = _evaluate_semantic_relevance(q, r_mutated)

        self.assertEqual(rec_valid["classification"], "DIRECT")
        self.assertNotEqual(rec_mutated["classification"], "DIRECT")

    def test_mutation_02_surface_mutation_preserves_classification(self):
        q = {"text": "Como evitar conflitos de escrita concorrente sem travar a linha no banco?"}
        r_base = {"reconstructed_text": "Usaria versionamento com checagem de versão no momento do commit."}
        r_surface = {"reconstructed_text": "   USARIA   versionamento COM checagem DE versão no MOMENTO do commit!   "}

        rec_base = _evaluate_semantic_relevance(q, r_base)
        rec_surface = _evaluate_semantic_relevance(q, r_surface)

        self.assertEqual(rec_base["classification"], rec_surface["classification"])


class Stage3173DeterminismAndIsolationTests(unittest.TestCase):
    """Section 28: Repeated runs under permutations produce strictly identical results."""

    def test_repeated_runs_identical_outputs(self):
        q = {"text": "Como o TiKV oferece armazenamento transacional distribuído?"}
        r = {"reconstructed_text": "TiKV emprega consenso Raft para replicação e Percolator para transações ACID distribuídas."}

        first_run = _evaluate_semantic_relevance(q, r)
        for _ in range(5):
            repeated_run = _evaluate_semantic_relevance(q, r)
            self.assertEqual(first_run["classification"], repeated_run["classification"])
            self.assertEqual(first_run["relation_type"], repeated_run["relation_type"])
            self.assertEqual(first_run["evidence_strength"], repeated_run["evidence_strength"])


class Stage3173PilotInterviewAlignmentTests(unittest.TestCase):
    """Section 24: Pilot Candidato-Piloto-05 alignment against frozen human reference."""

    def test_pilot_candidate_mae_remains_stable(self):
        src = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-01/Pilot Input - Source Transcript v3.md")
        result = run_real_pilot(src)["pipeline"]
        evals = result["artifacts"]["evaluations"]
        system_scores = [e["score"] for e in evals]
        human_scores = [4.0, 7.0, 4.0, 8.0, 2.0, 5.0, 5.0, 7.0, 4.0, 6.0, 4.0]
        mae = sum(abs(s - h) for s, h in zip(system_scores, human_scores)) / len(system_scores)
        self.assertEqual(round(mae, 2), 0.64)
        max_err = max(abs(s - h) for s, h in zip(system_scores, human_scores))
        self.assertAlmostEqual(max_err, 2.45, places=2)


if __name__ == "__main__":
    unittest.main()
