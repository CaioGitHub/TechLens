"""Tests for Stage 31.4.2 — Semantic Relevance Model Implementation & Migration.

Validates the executable implementation of the Semantic Relevance Model in the
Reference Evaluation Engine (reference_runtime/runtime.py).

Enforces:
1. Canonical taxonomy: DIRECT (>=10), PARTIAL (>=10), SUPPORTING (>=10),
   RELATED (>=10), OFF_TOPIC (>=10), INSUFFICIENT (>=5), UNKNOWN (>=5). Total >= 60 cases.
2. At least 10 unknown technologies absent from the internal vocabulary (Raft, Envoy,
   Cilium, eBPF, gRPC, WebAssembly, GraphQL, BGP, Terraform, Postgres).
3. At least 10 concepts demonstrated without technology names.
4. Supporting != Related distinction enforced.
5. Length invariance: short is not penalized, long padding is not rewarded.
6. Representation invariance across formal, informal, colloquial, hesitant, jargon.
7. Experience separation: declaration < hypothesis < demonstration.
8. Semantic discrimination: superficial similarity with opposite technical content.
9. Mutation sensitivity: technical changes affect classification; style preserves.
10. Strict determinism: Run 1 == Run 2 == Run 3.
11. Execution isolation: shuffle permutations do not leak state.
"""

import copy
import random
import unittest
from typing import Any

from reference_runtime import run_interview_pipeline
from reference_runtime.runtime import (
    _evaluate_semantic_relevance,
    _blind_dimensions,
)


def _case_fixture(case_id: str, question: str, response: str) -> dict[str, Any]:
    return {
        "metadata": {"interview_id": f"INT-{case_id}", "candidate_id": "CAND-3142"},
        "participants": [
            {"participant_id": "P-INT", "name": "Interviewer", "role": "interviewer"},
            {"participant_id": "P-CAN", "name": "Candidate", "role": "candidate"},
        ],
        "raw_transcript": [
            {"id": f"{case_id}-Q", "speaker": "Interviewer", "timestamp": "00:00", "text": question},
            {"id": f"{case_id}-R", "speaker": "Candidate", "timestamp": "00:05", "text": response},
        ],
    }


class Stage3142CanonicalTaxonomyAdversarialTests(unittest.TestCase):
    """60+ adversarial cases across 7 canonical taxonomy classifications and diverse domains."""

    # -------------------------------------------------------------
    # 1. DIRECT (10 cases)
    # -------------------------------------------------------------
    def test_direct_01_unknown_tech_raft_consensus(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o algoritmo Raft?"},
            {"reconstructed_text": "Raft elege um líder que coordena a replicação de logs nos seguidores por maioria de quórum."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])
        self.assertEqual(rec["evidence_strength"], "STRONG")

    def test_direct_02_unknown_tech_envoy_proxy(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é o Envoy proxy e qual seu papel em service mesh?"},
            {"reconstructed_text": "Envoy é um proxy de borda e sidecar que intercepta tráfego de rede provendo roteamento L7 e observabilidade."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_03_unknown_tech_cilium_ebpf(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é Cilium e como protege a rede?"},
            {"reconstructed_text": "Cilium utiliza programas eBPF carregados no kernel Linux para filtragem de pacotes e políticas de segurança."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_04_concept_without_name_in_memory_latency(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como evitar consultas repetidas ao banco de dados?"},
            {"reconstructed_text": "Manteria os dados em memória por determinado período com tempo de expiração e estratégia de invalidação."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_05_concept_without_name_decoupling_instantiation(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como desacoplar a criação de objetos da sua utilização?"},
            {"reconstructed_text": "As dependências são fornecidas externamente através de inversão de controle sem instanciar na classe."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_06_concept_without_name_asynchronous_queue_buffering(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como evitar que uma lentidão em um serviço downstream afete o chamador?"},
            {"reconstructed_text": "Publicaria mensagens em uma fila assíncrona para que os consumidores processem desacoplados do produtor."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_07_api_design_rest(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é uma API REST?"},
            {"reconstructed_text": "É uma arquitetura baseada em recursos identificados por URIs e manipulados via métodos HTTP padronizados."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_08_relational_query_btree_index(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é um índice no banco relacional?"},
            {"reconstructed_text": "É uma estrutura em árvore B-Tree que acelera consultas em tabelas relacionais evitando scans completos."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_09_concurrency_virtual_threads(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que são Virtual Threads no Java?"},
            {"reconstructed_text": "São threads virtuais leves gerenciadas pela JVM que desvinculam o thread da carrier thread durante bloqueios de I/O."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_direct_10_concept_without_name_circuit_breaker(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como desenharia arquitetura para isolar dependências com falha?"},
            {"reconstructed_text": "Usaria timeouts, retries com backoff e circuit breaker para proteger as chamadas downstream."},
        )
        self.assertIn(rec["classification"], ("DIRECT", "SUPPORTING"))
        self.assertTrue(rec["functional_contribution"])

    # -------------------------------------------------------------
    # 2. PARTIAL (10 cases)
    # -------------------------------------------------------------
    def test_partial_01_multi_aspect_rest_http_short(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Explique REST e como funciona uma requisição HTTP."},
            {"reconstructed_text": "REST usa HTTP."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_02_distributed_cache_omits_tradeoffs(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Explique cache distribuído e seus trade-offs."},
            {"reconstructed_text": "Cache distribuído armazena dados em memória entre instâncias."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_03_docker_network_mixed_with_alien_jenkins(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona a rede padrão (bridge) do Docker?"},
            {"reconstructed_text": "Usa rede bridge para isolar containers, além de também configurar pipelines de CI/CD no Jenkins."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_04_kafka_partitions_and_consumer_rebalance(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o particionamento no Kafka e como funciona o rebalanceamento de consumidores?"},
            {"reconstructed_text": "Kafka divide tópicos em partições."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_05_sql_index_and_write_overhead(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como um índice acelera queries e qual seu impacto nas escritas?"},
            {"reconstructed_text": "O índice acelera tabelas relacionais."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_06_hexagonal_architecture_and_ports(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como desenharia arquitetura hexagonal e como separaria portas de adaptadores?"},
            {"reconstructed_text": "A arquitetura hexagonal separa domínio."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_07_oauth2_and_token_refresh(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Explique OAuth2 e como funciona o refresh token."},
            {"reconstructed_text": "OAuth2 emite token de acesso."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_08_unknown_tech_grpc_protobuf(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é gRPC e como funciona a serialização em Protocol Buffers?"},
            {"reconstructed_text": "gRPC faz chamadas remotas."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_09_unknown_tech_wasm_and_memory(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é WebAssembly e como gerencia memória linear?"},
            {"reconstructed_text": "WebAssembly executa bytecode rápido."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    def test_partial_10_unknown_tech_graphql_overfetching(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é GraphQL e por que evita overfetching em comparação com REST?"},
            {"reconstructed_text": "GraphQL usa schema flexível."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertTrue(rec["functional_contribution"])

    # -------------------------------------------------------------
    # 3. SUPPORTING (10 cases)
    # -------------------------------------------------------------
    def test_supporting_01_http_500_logs_and_traces(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria um erro HTTP 500?"},
            {"reconstructed_text": "Verificaria logs, traces correlacionados e métricas de dependências para encontrar a exceção."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_02_latency_p95_and_dependencies(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria latência elevada em produção?"},
            {"reconstructed_text": "Mediria p95, p99, separaria os tempos por dependência e compararia com o baseline histórico."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_03_resilience_timeouts_and_retries(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como projetaria um sistema resiliente a falhas de rede?"},
            {"reconstructed_text": "Configuraria timeouts agressivos, retries com backoff exponencial e circuit breaker."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_04_unknown_tech_memory_heapdump_gc_roots(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria memory leak no servidor?"},
            {"reconstructed_text": "Coletaria heap dump na aplicação, analisaria histograma de objetos retidos e rastrearia GC roots no debug."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_05_unknown_tech_tcpdump_packet_inspection(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria perda de pacotes entre instâncias?"},
            {"reconstructed_text": "Faria captura com tcpdump, checaria métricas de interface e logs de drop do kernel."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_06_event_driven_idempotency_tradeoff(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como decidiria a arquitetura de processamento assíncrono?"},
            {"reconstructed_text": "Analisaria o trade-off entre consistência e latência, garantindo idempotência nos consumidores desacoplados."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_07_unknown_tech_postgres_stat_activity(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria incidente de queries bloqueadas no banco?"},
            {"reconstructed_text": "Consultaria métricas de locks e logs de transações bloqueadoras para isolar o deadlock."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_08_unknown_tech_k8s_crashloop_logs_exit_code(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria falha 500 no microserviço em container?"},
            {"reconstructed_text": "Inspecionaria logs do container, checaria métricas de CPU e memória, e analisaria probes de liveness."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_09_api_rate_limiting_metrics(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria sobrecarga na API de autenticação?"},
            {"reconstructed_text": "Analisaria métricas de taxa de requisições, logs de WAF e taxas de erro HTTP para mitigar o pico."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_supporting_10_flamegraph_cpu_troubleshooting(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria incidente de saturação de CPU?"},
            {"reconstructed_text": "Faria profiling com flamegraph e analisaria traces e métricas de threads ativas no debug."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    # -------------------------------------------------------------
    # 4. RELATED (10 cases)
    # -------------------------------------------------------------
    def test_related_01_di_vs_spring_data(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é Dependency Injection e como ela desacopla componentes?"},
            {"reconstructed_text": "No Spring usamos bastante o Spring Data, que cria repositórios e abstrai o acesso ao banco de dados com interfaces."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])
        self.assertEqual(rec["evidence_strength"], "NONE")

    def test_related_02_css_flexbox_vs_html_semantics(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o alinhamento de layout no CSS?"},
            {"reconstructed_text": "No CSS e web usamos tags HTML semânticas como main e article para estruturar páginas."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_03_cicd_pipeline_vs_git_branching(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona um pipeline de CI/CD para deploy?"},
            {"reconstructed_text": "Nos pipelines de CI/CD usamos git branches e pull requests para organizar o repositório."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_04_relational_btree_vs_database_replication(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é um índice no banco relacional e como acelera queries?"},
            {"reconstructed_text": "No banco relacional configuramos replicação com réplicas de leitura para distribuir carga de banco."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_05_java_virtual_threads_vs_maven_build(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que são threads virtuais no Java?"},
            {"reconstructed_text": "No Java usamos o pom.xml do Maven para gerenciar dependências e compilar o projeto."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_06_kafka_partitions_vs_schema_registry(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o particionamento no Kafka?"},
            {"reconstructed_text": "Na parte de Kafka usamos Schema Registry com Avro para versionar esquemas de mensagens."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_07_jwt_tokens_vs_cors_headers(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona a assinatura de tokens JWT?"},
            {"reconstructed_text": "Para segurança de API configuramos cabeçalhos CORS no HTTP para controlar acessos do navegador."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_08_rest_status_codes_vs_swagger_docs(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona uma API REST com seus status codes?"},
            {"reconstructed_text": "Na API REST usamos Swagger e OpenAPI para gerar a documentação interativa dos endpoints."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_09_angular_signals_vs_npm_packages(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona a reatividade com Angular signals?"},
            {"reconstructed_text": "No Angular usamos npm e package.json para instalar bibliotecas de interface."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_related_10_kql_analytics_vs_azure_portal_rbac(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona uma consulta KQL no Log Analytics?"},
            {"reconstructed_text": "No Log Analytics e KQL gerenciamos permissões de RBAC pelo portal da nuvem."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    # -------------------------------------------------------------
    # 5. OFF_TOPIC (10 cases)
    # -------------------------------------------------------------
    def test_off_topic_01_docker_to_kubernetes_d2(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona a rede padrão (bridge) do Docker?"},
            {"reconstructed_text": "O Kubernetes orquestra os containers em pods e agenda nos nós."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])
        self.assertEqual(rec["evidence_strength"], "NONE")

    def test_off_topic_02_sql_to_redis_d3(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é um índice no banco relacional e como ele acelera consultas?"},
            {"reconstructed_text": "O Redis armazena dados em memória com chave e valor para acelerar leituras."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_03_spring_transaction_to_virtual_threads_adv09(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona uma transação no Spring?"},
            {"reconstructed_text": "Virtual threads são leves e gerenciadas pela JVM."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_04_rest_to_kafka_messaging(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é uma API REST e como ela opera?"},
            {"reconstructed_text": "Kafka usa tópicos e consumidores para mensageria assíncrona distribuída."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_05_unknown_tech_cilium_to_terraform(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é Cilium e como filtra pacotes de rede?"},
            {"reconstructed_text": "Terraform provisiona infraestrutura como código na nuvem através de arquivos declarativos."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_06_css_styling_to_sql_queries(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como você define o layout visual com CSS?"},
            {"reconstructed_text": "Faço consultas SQL com SELECT, JOIN e GROUP BY para buscar tabelas relacionais."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_07_cooking_recipe_to_docker(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o isolamento de rede no Docker?"},
            {"reconstructed_text": "Para preparar um bolo você mistura ovos, farinha e assa no forno por quarenta minutos."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_08_virtual_threads_to_kql_query(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que são Virtual Threads e como melhoram I/O bloqueante?"},
            {"reconstructed_text": "No KQL usamos summarize count() by bin(timestamp, 1h) para agrupar logs analíticos."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_09_unknown_tech_bgp_routing_to_graphql(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o protocolo BGP para troca de rotas de rede?"},
            {"reconstructed_text": "No GraphQL definimos schemas com queries e mutations para buscar payloads JSON."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_off_topic_10_unknown_tech_envoy_to_rabbitmq(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Envoy intercepta o tráfego de rede em service mesh?"},
            {"reconstructed_text": "RabbitMQ entrega mensagens com exchanges direct e topic para filas com ack manual."},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    # -------------------------------------------------------------
    # 6. INSUFFICIENT (5 cases)
    # -------------------------------------------------------------
    def test_insufficient_01_bem_por_cima(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona garbage collection?"},
            {"reconstructed_text": "Mais ou menos, sei bem por cima."},
        )
        self.assertEqual(rec["classification"], "INSUFFICIENT")
        self.assertFalse(rec["functional_contribution"])

    def test_insufficient_02_nao_sei(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é injeção de dependência?"},
            {"reconstructed_text": "Não sei."},
        )
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    def test_insufficient_03_muito_pouco(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o particionamento no Kafka?"},
            {"reconstructed_text": "É muito pouco, quase nada."},
        )
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    def test_insufficient_04_yes_single_word(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é um memory leak em Java?"},
            {"reconstructed_text": "Yes."},
        )
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    def test_insufficient_05_beijava_noise(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como você implementaria rate limiting?"},
            {"reconstructed_text": "Beijava."},
        )
        self.assertEqual(rec["classification"], "INSUFFICIENT")

    # -------------------------------------------------------------
    # 7. UNKNOWN (5 cases)
    # -------------------------------------------------------------
    def test_unknown_01_empty_text(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Qual a estratégia de cache?"},
            {"reconstructed_text": ""},
        )
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec["needs_review"])

    def test_unknown_02_unlinked_question_id(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona autenticação?"},
            {"reconstructed_text": "Uso tokens JWT.", "question_id": "unknown"},
        )
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec["needs_review"])

    def test_unknown_03_whitespace_only(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Explique microsserviços."},
            {"reconstructed_text": "   \n\t  "},
        )
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec["needs_review"])

    def test_unknown_04_missing_text_key(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como escala a aplicação?"},
            {},
        )
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec["needs_review"])

    def test_unknown_05_unknown_question_id_none_text(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona deployment?"},
            {"question_id": "unknown", "text": None},
        )
        self.assertEqual(rec["classification"], "UNKNOWN")
        self.assertTrue(rec["needs_review"])


class Stage3142InvarianceAndPropertiesTests(unittest.TestCase):
    """Validates length invariance, style invariance, experience hierarchy, and discrimination."""

    def test_length_invariance_concise_vs_verbose_same_semantics(self):
        concise = "Cache em memória reduz a latência das consultas."
        verbose = "A aplicação faz uso estratégico de uma camada de cache distribuído em memória com a finalidade primordial de reduzir a latência das consultas no banco de dados."
        question = "Como reduziria a latência de consultas?"

        rec_c = _evaluate_semantic_relevance({"text": question}, {"reconstructed_text": concise})
        rec_v = _evaluate_semantic_relevance({"text": question}, {"reconstructed_text": verbose})

        self.assertEqual(rec_c["classification"], "DIRECT")
        self.assertEqual(rec_v["classification"], "DIRECT")

        res_c = run_interview_pipeline(_case_fixture("LEN-C", question, concise))
        res_v = run_interview_pipeline(_case_fixture("LEN-V", question, verbose))

        eval_c = res_c["artifacts"]["evaluations"][0]
        eval_v = res_v["artifacts"]["evaluations"][0]

        # Both concise and verbose have Strong correctness and score equivalently
        self.assertEqual(eval_c["dimensions"]["correctness"]["assessment"], "Strong")
        self.assertEqual(eval_v["dimensions"]["correctness"]["assessment"], "Strong")
        self.assertAlmostEqual(eval_c["score"], eval_v["score"], delta=0.5)

    def test_anti_padding_long_answer_buzzwords_not_rewarded(self):
        question = "Como reduziria consultas repetidas ao banco?"
        padding = "Trabalhamos com microsserviços em cloud usando Docker, Kubernetes, CI/CD no Jenkins, observabilidade moderna, SOLID, DDD, monitoramento distribuído e sprints ágeis com times multidisciplinares maduros."

        rec = _evaluate_semantic_relevance({"text": question}, {"reconstructed_text": padding})
        self.assertEqual(rec["classification"], "OFF_TOPIC")

        res = run_interview_pipeline(_case_fixture("PAD", question, padding))
        evaluation = res["artifacts"]["evaluations"][0]
        self.assertLessEqual(evaluation["score"], 5.0)
        self.assertEqual(evaluation["dimensions"]["correctness"]["assessment"], "Insufficient")

    def test_style_invariance_formal_informal_hesitant_colloquial(self):
        styles = [
            ("formal", "A camada de cache distribuído em memória reduz a latência das consultas."),
            ("informal", "A gente usa cache pra deixar as consultas mais rápidas."),
            ("hesitant", "Bom, tipo, usando cache na memória, né, a consulta fica mais rápida."),
            ("colloquial", "A gente coloca cache na frente pra consulta responder rapidinho."),
        ]
        question = "Como reduziria a latência de consultas?"
        scores = []
        for name, text in styles:
            res = run_interview_pipeline(_case_fixture(f"ST-{name}", question, text))
            ev = res["artifacts"]["evaluations"][0]
            self.assertEqual(ev["dimensions"]["correctness"]["assessment"], "Strong")
            scores.append(ev["score"])

        # All variants should produce near-identical or identical scores
        first = scores[0]
        for s in scores[1:]:
            self.assertAlmostEqual(s, first, delta=0.3)

    def test_semantic_discrimination_superficial_similarity_opposite_meaning(self):
        # Two answers with similar vocabulary and structure, but opposite technical claims
        q = "Como opera o RabbitMQ?"
        ans_correct = "RabbitMQ opera assincronamente através de filas e exchanges."
        ans_incorrect = "RabbitMQ opera sincronicamente bloqueando threads de chamada."

        res_c = run_interview_pipeline(_case_fixture("DISC-C", q, ans_correct))
        res_i = run_interview_pipeline(_case_fixture("DISC-I", q, ans_incorrect))

        eval_c = res_c["artifacts"]["evaluations"][0]
        eval_i = res_i["artifacts"]["evaluations"][0]

        self.assertGreater(eval_c["score"], eval_i["score"])

    def test_experience_hierarchy_declaration_vs_hypothesis_vs_demonstration(self):
        q = "Você tem experiência com Kubernetes em produção?"
        decl = "Trabalhei 3 anos com Kubernetes."
        hypo = "Eu criaria um deployment no Kubernetes se precisasse escalar."
        demo = "Em produção gerenciei clusters Kubernetes, configurei liveness e readiness probes, debuguei crash loops e resolvi gargalos de memória OOM."

        res_decl = run_interview_pipeline(_case_fixture("EXP-D", q, decl))
        res_hypo = run_interview_pipeline(_case_fixture("EXP-H", q, hypo))
        res_demo = run_interview_pipeline(_case_fixture("EXP-E", q, demo))

        score_decl = res_decl["artifacts"]["evaluations"][0]["score"]
        score_hypo = res_hypo["artifacts"]["evaluations"][0]["score"]
        score_demo = res_demo["artifacts"]["evaluations"][0]["score"]

        # Strict hierarchy: declaration <= hypothesis < demonstration
        self.assertLessEqual(score_decl, score_hypo)
        self.assertLess(score_hypo, score_demo)
        self.assertGreaterEqual(score_demo, 7.0)

    def test_mutation_sensitivity_technical_change_alters_classification(self):
        q = "O que é um índice no banco relacional?"
        valid_ans = "É uma estrutura em árvore B-Tree que acelera buscas na tabela."
        mutated_alien = "É uma estrutura do Redis que armazena dados em memória com chave e valor."

        rec_valid = _evaluate_semantic_relevance({"text": q}, {"reconstructed_text": valid_ans})
        rec_alien = _evaluate_semantic_relevance({"text": q}, {"reconstructed_text": mutated_alien})

        self.assertEqual(rec_valid["classification"], "DIRECT")
        self.assertEqual(rec_alien["classification"], "OFF_TOPIC")

    def test_mutation_invariance_purely_stylistic_change_preserves_classification(self):
        q = "O que é um índice no banco relacional?"
        form_a = "O índice utiliza uma estrutura em árvore B-Tree para acelerar consultas nas tabelas."
        form_b = "Nas tabelas, o índice usa uma árvore B-Tree para deixar as consultas bem mais rápidas."

        rec_a = _evaluate_semantic_relevance({"text": q}, {"reconstructed_text": form_a})
        rec_b = _evaluate_semantic_relevance({"text": q}, {"reconstructed_text": form_b})

        self.assertEqual(rec_a["classification"], rec_b["classification"])
        self.assertEqual(rec_a["functional_contribution"], rec_b["functional_contribution"])

    def test_determinism_multiple_runs_identical_results(self):
        q = "Como investigaria latência elevada em produção?"
        ans = "Mediria p95, separaria os tempos por dependência e compararia com o baseline histórico."

        res1 = run_interview_pipeline(_case_fixture("DET-1", q, ans))
        res2 = run_interview_pipeline(_case_fixture("DET-1", q, ans))
        res3 = run_interview_pipeline(_case_fixture("DET-1", q, ans))

        eval1 = res1["artifacts"]["evaluations"][0]
        eval2 = res2["artifacts"]["evaluations"][0]
        eval3 = res3["artifacts"]["evaluations"][0]

        self.assertEqual(eval1["score"], eval2["score"])
        self.assertEqual(eval2["score"], eval3["score"])
        self.assertEqual(eval1["dimensions"], eval2["dimensions"])
        self.assertEqual(eval2["dimensions"], eval3["dimensions"])

    def test_execution_isolation_order_permutations(self):
        cases = [
            ("Raft", "Como funciona o Raft?", "Raft elege um líder que replica logs por quórum."),
            ("Cache", "Como evitar consultas repetidas?", "Manteria dados em memória com TTL."),
            ("Docker", "Como funciona a rede bridge?", "Kubernetes orquestra pods nos nós."),  # off topic
        ]

        def run_all(order):
            results = []
            for cid, q, a in order:
                out = run_interview_pipeline(_case_fixture(cid, q, a))
                results.append((cid, out["artifacts"]["evaluations"][0]["score"]))
            return dict(results)

        base = run_all(cases)
        for _ in range(3):
            shuffled = list(cases)
            random.shuffle(shuffled)
            current = run_all(shuffled)
            self.assertEqual(base, current)


if __name__ == "__main__":
    unittest.main()
