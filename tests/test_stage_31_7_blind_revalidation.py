"""Stage 31.7 — Post-Correction Human vs System Blind Revalidation Test Suite.

Executes an independent, non-optimizing blind validation of the Reference
Evaluation Engine following the structural corrections in Stage 31.6.

Tests:
1. Revalidation of Stage 31.5 root causes (word-count proxy, morphology, substring collisions).
2. Functional capability open-domain generalizability (concepts not in _FUNCTIONAL_CAPABILITIES).
3. Stemmer false grouping prevention (distinct words with shared roots/prefixes).
4. 10 new unseen technologies across canonical classes.
5. 10 new technology-free concepts.
6. 10 new multi-aspect questions with proposition coverage tracking.
7. Supporting vs Related functional discrimination.
8. Semantic Relevance vs Evidence Strength independence.
9. Experience epistemic separation (declaration, hypothesis, demonstration).
10. Representation invariance (formality, verbosity, colloquialism, minor errors).
11. False positive resistance (buzzword padding) and False negative resistance (concise alternative).
12. Semantic mutations (polarity reversal, padding, omission).
13. Determinism and execution isolation under permutations.
14. Audit of real pilot interview (Candidato-Piloto-05) against frozen human reference.
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
    _lexical_contains,
    _stem_word,
    _extract_stemmed_tokens,
    _blind_dimensions,
)


def _case_fixture(case_id: str, question: str, response: str) -> dict[str, Any]:
    return {
        "metadata": {"interview_id": f"INT-{case_id}", "candidate_id": "CAND-317"},
        "participants": [
            {"participant_id": "P-INT", "name": "Interviewer", "role": "interviewer"},
            {"participant_id": "P-CAN", "name": "Candidate", "role": "candidate"},
        ],
        "raw_transcript": [
            {"id": f"{case_id}-Q", "speaker": "Interviewer", "timestamp": "00:00", "text": question},
            {"id": f"{case_id}-R", "speaker": "Candidate", "timestamp": "00:05", "text": response},
        ],
    }


class Stage317RootCausesRevalidationTests(unittest.TestCase):
    """Section 8: Revalidate Causa A, B, and C from Stage 31.5."""

    def test_causa_a_short_multi_aspect_answer_is_not_penalized(self):
        """Short answer (8 words) covering both demands must be DIRECT, not PARTIAL."""
        q = {"text": "Como evitar retry agressivo e tempestade de requisições?"}
        r = {"reconstructed_text": "Usaria backoff exponencial com jitter e circuit breaker."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_causa_a_long_padding_with_one_aspect_remains_partial(self):
        """Long response (>40 words) with padding covering only 1 aspect must remain PARTIAL."""
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
        self.assertEqual(rec["relation_type"], "partial_aspect_coverage")

    def test_causa_b_morphological_variants_correlacionar(self):
        """All morphological variants of 'correlacionar' yield equivalent SUPPORTING classification."""
        q = {"text": "Como investigar erro HTTP 500 na aplicação?"}
        variants = [
            "correlacionar logs e traces para investigar falhas",
            "fazer a correlação de logs e traces para investigar falhas",
            "correlacionando logs e traces para investigar falhas",
            "correlacionou logs e traces para investigar falhas",
        ]
        results = [_evaluate_semantic_relevance(q, {"reconstructed_text": v}) for v in variants]
        for res in results:
            self.assertEqual(res["classification"], "SUPPORTING")
            self.assertTrue(res["functional_contribution"])

    def test_causa_b_plural_and_loanword_inflections(self):
        """Plural/singular forms of technical loanwords and Portuguese nouns normalize to same root."""
        self.assertEqual(_stem_word("retries"), _stem_word("retry"))
        self.assertEqual(_stem_word("repetições"), _stem_word("repetição"))
        self.assertEqual(_stem_word("atualizações"), _stem_word("atualização"))

    def test_causa_c_substring_collisions_prevented(self):
        """Word boundaries prevent collisions in substring patterns."""
        self.assertFalse(_lexical_contains("otimizamos a performance da aplicação", "orm"))
        self.assertFalse(_lexical_contains("regras de negócio do business", "bus"))
        self.assertFalse(_lexical_contains("produção de mel na apicultura", "api"))
        self.assertFalse(_lexical_contains("tela de login do sistema", "log"))
        self.assertFalse(_lexical_contains("discurso com cacofonia", "cache"))
        self.assertFalse(_lexical_contains("executamos comando traceroute", "trace"))
        self.assertFalse(_lexical_contains("exatamente o mesmo resultado", "mesh"))
        self.assertFalse(_lexical_contains("chamada totalmente assíncrona", "síncrono"))
        self.assertTrue(_lexical_contains("chamada totalmente síncrona bloqueante", "síncrono"))


class Stage317FunctionalCapabilityCatalogAuditTests(unittest.TestCase):
    """Section 9: Functional capability audit on concepts NOT in _FUNCTIONAL_CAPABILITIES."""

    def test_ebpf_kernel_packet_filtering_open_domain(self):
        """Open-domain concept: eBPF packet filtering without entry in catalog."""
        q = {"text": "Como o eBPF filtra pacotes de rede no kernel Linux?"}
        r = {"reconstructed_text": "eBPF executa bytecode seguro verificado dentro do kernel anexado a hooks de rede XDP para filtrar pacotes em tempo real."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_vector_similarity_search_open_domain(self):
        """Open-domain concept: Vector similarity search."""
        q = {"text": "Como funciona a busca por similaridade de embeddings em bancos vetoriais?"}
        r = {"reconstructed_text": "Bancos vetoriais utilizam índices HNSW e distância de cosseno para recuperar os vetores mais próximos em alta dimensionalidade."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_crdt_conflict_free_replication_open_domain(self):
        """Open-domain concept: CRDT for collaborative editing."""
        q = {"text": "Como o CRDT resolve conflitos de edição concorrente sem coordenação central?"}
        r = {"reconstructed_text": "CRDTs utilizam estruturas de dados comutativas e associativas que garantem convergência matemática automática entre réplicas."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_zero_knowledge_proofs_open_domain(self):
        """Open-domain concept: Zero-knowledge proofs."""
        q = {"text": "Como funcionam as provas de conhecimento zero em verificação de identidade?"}
        r = {"reconstructed_text": "Permitem que um provador comprove matematicamente uma asserção para o verificador sem revelar o dado secreto subjacente."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])


class Stage317StemmerFalseGroupingTests(unittest.TestCase):
    """Sections 10 & 11: Stemmer audit verifying preservation of technical discrimination."""

    def test_log_and_login_remain_distinct(self):
        stem_log = _stem_word("log")
        stem_login = _stem_word("login")
        self.assertNotEqual(stem_log, stem_login)
        self.assertFalse(_lexical_contains("acesso via tela de login", "log"))

    def test_sincrono_and_assincrono_remain_distinct(self):
        stem_sincrono = _stem_word("sincrono")
        stem_assincrono = _stem_word("assincrono")
        self.assertNotEqual(stem_sincrono, stem_assincrono)
        self.assertFalse(_lexical_contains("comunicação assíncrona por eventos", "síncrono"))

    def test_porta_and_portanto_remain_distinct(self):
        stem_porta = _stem_word("porta")
        stem_portanto = _stem_word("portanto")
        self.assertNotEqual(stem_porta, stem_portanto)

    def test_teste_and_testemunha_remain_distinct(self):
        self.assertNotEqual(_stem_word("teste"), _stem_word("testemunha"))


class Stage317NewUnseenTechnologiesTests(unittest.TestCase):
    """Section 12: 10 new unseen technologies across canonical classes."""

    def test_01_unseen_duckdb_columnar(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o DuckDB processa consultas analíticas diretamente na aplicação?"},
            {"reconstructed_text": "DuckDB processa queries analíticas colunares diretamente no processo da aplicação usando execução vetorizada."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_02_unseen_cockroachdb_distributed_sql(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o CockroachDB garante consenso e transações distribuídas?"},
            {"reconstructed_text": "CockroachDB utiliza o consenso Raft para coordenar réplicas e prover transações ACID distribuídas serializáveis."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_03_unseen_surrealdb_multimodel(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o SurrealDB organiza dados multi-modelo?"},
            {"reconstructed_text": "SurrealDB combina tabelas relacionais, documentos e conexões de grafo em um único motor de persistência."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_04_unseen_linkerd_service_mesh(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Linkerd gerencia tráfego L7 em pods?"},
            {"reconstructed_text": "Linkerd utiliza micro-proxies sidecars em Rust nos pods para gerenciar mTLS e métricas de tráfego L7."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_05_unseen_opentelemetry_collector(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o OpenTelemetry padroniza a exportação de telemetria?"},
            {"reconstructed_text": "OpenTelemetry padroniza a coleta de traces, métricas e logs exportando para backends analíticos via protocolo OTLP."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_06_unseen_polars_dataframes(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Polars processa grandes volumes de dados em memória?"},
            {"reconstructed_text": "Polars executa consultas sobre dados em memória usando Rust e Apache Arrow com avaliação lazy e paralelismo."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_07_unseen_redpanda_streaming(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Redpanda processa fluxos de streaming compatíveis com Kafka?"},
            {"reconstructed_text": "Redpanda implementa a API do Kafka em C++ com arquitetura thread-per-core sem depender de JVM ou Zookeeper."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_08_unseen_triton_inference_server(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Triton Server orquestra modelos de IA em GPUs?"},
            {"reconstructed_text": "Triton gerencia inferência de múltiplos modelos de machine learning com suporte a lotes dinâmicos e aceleração em GPU."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_09_unseen_spire_workload_identity(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Spire atesta e emite identidades para workloads?"},
            {"reconstructed_text": "SPIFFE define identidades criptográficas para workloads emitindo documentos SVID temporários assinados."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_10_unseen_fluentbit_log_processor(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Fluentbit coleta e encaminha logs de containers?"},
            {"reconstructed_text": "Fluentbit coleta logs de containers, processa filtros de parsing e encaminha eventos para armazenamento central."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_unseen_tech_partial_omission(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é Polars e como funciona sua execução lazy?"},
            {"reconstructed_text": "Polars é uma biblioteca de dataframes escrita em Rust para processamento tabular."}
        )
        self.assertEqual(rec["classification"], "PARTIAL")

    def test_unseen_tech_alien_off_topic(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Spire atesta identidades criptográficas?"},
            {"reconstructed_text": "DuckDB executa queries SQL colunares vetorizadas em memória."}
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")


class Stage317TechnologyFreeConceptsTests(unittest.TestCase):
    """Section 13: 10 new technology-free concepts without naming specific products."""

    def test_01_optimistic_concurrency_control(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como evitar conflitos de escrita concorrente sem travar a linha no banco?"},
            {"reconstructed_text": "Utilizaria versionamento por timestamp ou contador de versão onde o update valida se o registro não foi alterado antes de commitar."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_02_backpressure_flow_control(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como evitar que um consumidor seja sobrecarregado por um produtor rápido?"},
            {"reconstructed_text": "Implementaria controle de fluxo por backpressure sinalizando a taxa de consumo para diminuir a taxa de envio do produtor."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_03_idempotency_deduplication(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como processar a mesma requisição múltiplas vezes sem duplicar pagamentos?"},
            {"reconstructed_text": "Registraria um token único de idempotência na primeira execução e rejeitaria ou retornaria o resultado salvo para requisições repetidas."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_04_distributed_context_propagation(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como rastrear uma transação que passa por múltiplos serviços sem perder o contexto?"},
            {"reconstructed_text": "Injetaria identificadores de trace e span nos headers das requisições repassando o contexto em cada chamada downstream."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_05_circuit_breaker_graceful_fallback(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como impedir que a indisponibilidade de um serviço parceiro derrube a nossa aplicação?"},
            {"reconstructed_text": "Abriria o circuito temporariamente ao detectar alta taxa de erros e responderia via fallback com resposta degradada ou cache."}
        )
        self.assertEqual(rec["classification"], "SUPPORTING")

    def test_06_eventual_consistency_reconciliation(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como garantir consistência entre dois serviços sem transação distribuída em duas fases?"},
            {"reconstructed_text": "Adotaria consistência eventual com publicação de eventos assíncronos e rotinas de reconciliação para corrigir inconsistências."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_07_regression_detection_p99_baseline(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como identificar degradação de performance após um novo deploy?"},
            {"reconstructed_text": "Compararia as métricas de latência P99 e taxa de erro da nova versão contra a baseline histórica de telemetria da versão anterior."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_08_bulkhead_resource_isolation(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como evitar que chamadas a um serviço lento esgotem todas as threads da aplicação?"},
            {"reconstructed_text": "Segmentaria pools de threads dedicadas e limites de conexões separados para cada dependência externa."}
        )
        self.assertEqual(rec["classification"], "SUPPORTING")

    def test_09_ttl_cache_invalidation(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como acelerar leituras e impedir que dados obsoletos permaneçam em memória?"},
            {"reconstructed_text": "Configuraria tempo de vida TTL com renovação automática e invalidação explícita nos eventos de alteração cadastral."}
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_10_token_bucket_rate_limiting(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como proteger endpoints públicos contra rajadas abusivas de requisições?"},
            {"reconstructed_text": "Aplicaria controle de vazão por token bucket ou janela deslizante limitando requisições por IP ou token de cliente."}
        )
        self.assertEqual(rec["classification"], "DIRECT")


class Stage317MultiAspectCoverageTests(unittest.TestCase):
    """Section 14: 10 new multi-aspect questions tracking proposition coverage."""

    def test_01_rest_and_pagination(self):
        rec_full = _evaluate_semantic_relevance(
            {"text": "Como projetar uma API REST e como estruturar a paginação de recursos?"},
            {"reconstructed_text": "REST expõe recursos via endpoints HTTP e a paginação pode ser feita por cursor ou limit e offset nos headers."}
        )
        self.assertEqual(rec_full["classification"], "DIRECT")

        rec_part = _evaluate_semantic_relevance(
            {"text": "Como projetar uma API REST e como estruturar a paginação de recursos?"},
            {"reconstructed_text": "REST usa HTTP para expor endpoints de recursos."}
        )
        self.assertEqual(rec_part["classification"], "PARTIAL")

    def test_02_jwt_and_signature(self):
        rec_full = _evaluate_semantic_relevance(
            {"text": "O que é autenticação JWT e como funciona a validação da assinatura?"},
            {"reconstructed_text": "JWT é um token com header payload e a validação verifica a assinatura criptográfica usando chave pública ou segredo."}
        )
        self.assertEqual(rec_full["classification"], "DIRECT")

        rec_part = _evaluate_semantic_relevance(
            {"text": "O que é autenticação JWT e como funciona a validação da assinatura?"},
            {"reconstructed_text": "JWT é um token codificado em base64 com claims de autenticação."}
        )
        self.assertEqual(rec_part["classification"], "PARTIAL")

    def test_03_kafka_partitions_and_rebalance(self):
        rec_full = _evaluate_semantic_relevance(
            {"text": "Como funciona o particionamento no Kafka e o que causa rebalanceamento de consumidores?"},
            {"reconstructed_text": "Particionamento divide tópicos em lotes paralelos por chave e rebalanceamento ocorre quando consumidor cai sem enviar heartbeat."}
        )
        self.assertEqual(rec_full["classification"], "DIRECT")

        rec_part = _evaluate_semantic_relevance(
            {"text": "Como funciona o particionamento no Kafka e o que causa rebalanceamento de consumidores?"},
            {"reconstructed_text": "Kafka divide tópicos em partições para garantir paralelismo ordenado por chave."}
        )
        self.assertEqual(rec_part["classification"], "PARTIAL")

    def test_04_docker_dockerfile_and_namespaces(self):
        rec_full = _evaluate_semantic_relevance(
            {"text": "O que é Dockerfile e como funciona o isolamento por namespaces no container?"},
            {"reconstructed_text": "Dockerfile define instruções para construir a imagem e namespaces isolam processos e rede no kernel Linux."}
        )
        self.assertEqual(rec_full["classification"], "DIRECT")

    def test_05_relational_database_and_btree(self):
        rec_full = _evaluate_semantic_relevance(
            {"text": "Como funciona um banco relacional e como o índice B-Tree acelera buscas?"},
            {"reconstructed_text": "Bancos relacionais estruturam dados em tabelas com schema e o índice B-Tree permite buscas em tempo logarítmico evitando scan."}
        )
        self.assertEqual(rec_full["classification"], "DIRECT")

    def test_06_api_latency_and_cascading_failures(self):
        rec_full = _evaluate_semantic_relevance(
            {"text": "Como proteger uma API contra lentidão e como evitar falhas em cascata?"},
            {"reconstructed_text": "Configuraria timeout agressivo e circuit breaker para interromper chamadas e prevenir falha em cascata."}
        )
        self.assertEqual(rec_full["classification"], "SUPPORTING")

    def test_07_eventual_consistency_and_idempotency(self):
        rec_full = _evaluate_semantic_relevance(
            {"text": "Como implementar consistência eventual e como garantir a idempotência de eventos?"},
            {"reconstructed_text": "Adotaria mensageria assíncrona orientada a eventos e persistência com chave de idempotência para evitar duplicidade."}
        )
        self.assertEqual(rec_full["classification"], "DIRECT")

    def test_08_virtual_threads_and_carrier_threads(self):
        rec_full = _evaluate_semantic_relevance(
            {"text": "O que é virtual thread no Java 21 e como ela interage com a carrier thread da JVM?"},
            {"reconstructed_text": "Virtual threads são gerenciadas pela JVM e montadas dinamicamente em carrier threads do sistema operacional."}
        )
        self.assertEqual(rec_full["classification"], "DIRECT")

    def test_09_http_protocol_and_methods_short_answer(self):
        """Short answer (10 words) covering both aspects must be DIRECT."""
        rec_short = _evaluate_semantic_relevance(
            {"text": "Como funciona o protocolo HTTP e quais seus métodos principais?"},
            {"reconstructed_text": "HTTP é cliente-servidor e usa métodos GET, POST, PUT, DELETE."}
        )
        self.assertEqual(rec_short["classification"], "DIRECT")

    def test_10_ci_cd_definition_and_pipeline_stages(self):
        rec_full = _evaluate_semantic_relevance(
            {"text": "O que é CI/CD e quais etapas compõem um pipeline automatizado?"},
            {"reconstructed_text": "CI/CD automatiza entrega contínua com etapas de build, testes automatizados e deploy em ambientes."}
        )
        self.assertEqual(rec_full["classification"], "DIRECT")


class Stage317SupportingVsRelatedTests(unittest.TestCase):
    """Section 15: Functional discrimination between SUPPORTING and RELATED."""

    def test_active_telemetry_correlation_is_supporting(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como investigaria aumento de latência na aplicação?"},
            {"reconstructed_text": "Correlacionaria traces distribuídos, métricas de latência P99 e logs da operação."}
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_passive_documentation_tooling_is_related(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona a arquitetura REST?"},
            {"reconstructed_text": "A aplicação utiliza OpenAPI e Swagger para documentar endpoints."}
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])


class Stage317SemanticRelevanceVsEvidenceStrengthTests(unittest.TestCase):
    """Section 16: Independence between semantic relevance and evidence strength."""

    def test_direct_with_shallow_depth(self):
        """Candidate answers the right topic directly but only at high level."""
        q = {"text": "Como funciona a arquitetura REST?"}
        r = {"reconstructed_text": "REST é uma arquitetura que utiliza requisições HTTP para acessar recursos."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

        res = run_interview_pipeline(_case_fixture("DIR-SHALLOW", q["text"], r["reconstructed_text"]))
        eval_item = res["artifacts"]["evaluations"][0]
        self.assertIn(eval_item["dimensions"]["depth"]["assessment"], ["Weak", "Partial"])

    def test_direct_with_deep_demonstration(self):
        """Candidate provides deep, concrete technical mechanism."""
        q = {"text": "Como funciona o particionamento no Kafka?"}
        r = {"reconstructed_text": "Kafka particiona mensagens baseado no hash da chave do registro gravando sequencialmente no commit log do broker e distribuindo réplicas via ISR."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")

        res = run_interview_pipeline(_case_fixture("DIR-DEEP", q["text"], r["reconstructed_text"]))
        eval_item = res["artifacts"]["evaluations"][0]
        self.assertIn(eval_item["dimensions"]["correctness"]["assessment"], ["Moderate", "Strong"])


class Stage317ExperienceEpistemologyTests(unittest.TestCase):
    """Section 17: Separation of declaration, hypothesis, and demonstration."""

    def test_experience_declaration_without_mechanism(self):
        res = run_interview_pipeline(_case_fixture(
            "EXP-ONLY",
            "Você tem experiência com Kubernetes?",
            "Trabalhei dois anos com Kubernetes na empresa anterior.",
        ))
        ev_types = [item["type"] for item in res["artifacts"]["evidence"]["evidence_set"]]
        self.assertEqual(ev_types, ["experience_declaration"])
        eval_item = res["artifacts"]["evaluations"][0]
        self.assertEqual(eval_item["dimensions"]["completeness"]["assessment"], "Insufficient")

    def test_hypothesis_formulation_is_tagged_epistemically(self):
        res = run_interview_pipeline(_case_fixture(
            "EXP-HYPO",
            "Como você investigaria um erro HTTP 500?",
            "Eu hipotetizaria que o problema está na conexão com o banco e analisaria os logs da aplicação.",
        ))
        ev_types = [item["type"] for item in res["artifacts"]["evidence"]["evidence_set"]]
        self.assertIn("hypothesis_formulation", ev_types)

    def test_demonstrated_experience_concrete(self):
        res = run_interview_pipeline(_case_fixture(
            "EXP-DEMO",
            "Conte uma situação em que você otimizou uma consulta SQL.",
            "No projeto de pagamentos criei um índice composto B-Tree reduzindo o tempo de scan de 12 segundos para 40 milissegundos e eliminamos timeouts.",
        ))
        ev_types = [item["type"] for item in res["artifacts"]["evidence"]["evidence_set"]]
        self.assertIn("demonstrated_experience", ev_types)
        eval_item = res["artifacts"]["evaluations"][0]
        self.assertEqual(eval_item["dimensions"]["practical_application"]["assessment"], "Strong")


class Stage317RepresentationInvarianceTests(unittest.TestCase):
    """Section 18: Invariance across representation styles."""

    def test_formal_vs_informal_vs_colloquial(self):
        q = {"text": "Como funciona o isolamento no Docker?"}
        formal = "Docker provê isolamento de processos mediante namespaces e cgroups no kernel Linux."
        informal = "Ele meio que usa namespaces e cgroups lá do kernel do Linux pra isolar o container."
        with_errors = "docker usa namespace e cgroup do linux pra fazer o isolamento dos processo."

        rel_formal = _evaluate_semantic_relevance(q, {"reconstructed_text": formal})
        rel_informal = _evaluate_semantic_relevance(q, {"reconstructed_text": informal})
        rel_errors = _evaluate_semantic_relevance(q, {"reconstructed_text": with_errors})

        self.assertEqual(rel_formal["classification"], "DIRECT")
        self.assertEqual(rel_informal["classification"], "DIRECT")
        self.assertEqual(rel_errors["classification"], "DIRECT")

    def test_self_correction_preserves_semantics(self):
        q = {"text": "Como funciona a arquitetura REST?"}
        self_corrected = "Usamos SOAP, quer dizer, não, usamos HTTP com verbos GET e POST para expor recursos REST."
        rec = _evaluate_semantic_relevance(q, {"reconstructed_text": self_corrected})
        self.assertEqual(rec["classification"], "DIRECT")


class Stage317FalsePositivesAndNegativesTests(unittest.TestCase):
    """Sections 19 & 20: Resistance to buzzword soup and concise alternative expressions."""

    def test_buzzword_soup_without_mechanism_is_not_direct(self):
        q = {"text": "Como funciona o isolamento no Docker?"}
        buzzword_soup = "Trabalhamos com arquitetura moderna, escalabilidade em cloud, microsserviços ágeis, CI/CD, DevOps e alta disponibilidade corporativa."
        rec = _evaluate_semantic_relevance(q, {"reconstructed_text": buzzword_soup})
        self.assertNotEqual(rec["classification"], "DIRECT")
        self.assertFalse(rec["functional_contribution"])

    def test_concise_accurate_answer_is_not_false_negative(self):
        q = {"text": "Como acelerar leituras de dados frequentemente acessados?"}
        concise = "Guardaria em cache na memória com TTL."
        rec = _evaluate_semantic_relevance(q, {"reconstructed_text": concise})
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])


class Stage317SemanticMutationTests(unittest.TestCase):
    """Section 21: Semantic mutations validating sensitivity to meaning."""

    def test_mutation_omission_decreases_coverage(self):
        q = {"text": "O que é JWT e como funciona a validação da assinatura?"}
        full = "JWT é um token com claims e a validação confere a assinatura criptográfica usando chave privada ou pública."
        omitted = "JWT é um token com claims codificado em base64."

        rec_full = _evaluate_semantic_relevance(q, {"reconstructed_text": full})
        rec_omitted = _evaluate_semantic_relevance(q, {"reconstructed_text": omitted})

        self.assertEqual(rec_full["classification"], "DIRECT")
        self.assertEqual(rec_omitted["classification"], "PARTIAL")

    def test_mutation_irrelevant_padding_does_not_promote(self):
        q = {"text": "O que é JWT e como funciona a validação da assinatura?"}
        omitted_with_padding = (
            "JWT é um token com claims codificado em base64. Além disso nossa equipe realiza reuniões diárias, "
            "fazemos planejamento de sprint com Jira e entregamos valor com metodologia ágil contínua."
        )
        rec = _evaluate_semantic_relevance(q, {"reconstructed_text": omitted_with_padding})
        self.assertEqual(rec["classification"], "PARTIAL")


class Stage317DeterminismAndIsolationTests(unittest.TestCase):
    """Sections 22 & 23: Strict determinism and permutation isolation."""

    def test_strict_determinism_across_runs(self):
        fixture = _case_fixture(
            "DET-317",
            "Como funciona a virtual thread no Java 21?",
            "Virtual threads são threads leves gerenciadas pela JVM montadas em carrier threads do sistema operacional.",
        )
        res1 = run_interview_pipeline(fixture)
        res2 = run_interview_pipeline(fixture)
        self.assertEqual(
            res1["artifacts"]["evaluations"][0]["score"],
            res2["artifacts"]["evaluations"][0]["score"],
        )
        self.assertEqual(
            res1["artifacts"]["evaluations"][0]["dimensions"],
            res2["artifacts"]["evaluations"][0]["dimensions"],
        )

    def test_order_permutation_isolation(self):
        cases = [
            ("P1", "Explique REST.", "REST usa HTTP para expor recursos via endpoints."),
            ("P2", "O que é SQL?", "SQL é linguagem para consultar tabelas em bancos relacionais."),
            ("P3", "Como funciona Docker?", "Docker isola containers usando namespaces e cgroups."),
        ]
        seq1 = [run_interview_pipeline(_case_fixture(c[0], c[1], c[2]))["artifacts"]["evaluations"][0]["score"] for c in cases]
        shuffled_cases = list(reversed(cases))
        seq2_rev = [run_interview_pipeline(_case_fixture(c[0], c[1], c[2]))["artifacts"]["evaluations"][0]["score"] for c in shuffled_cases]
        self.assertEqual(seq1, list(reversed(seq2_rev)))


class Stage317RealPilotHumanAuditTests(unittest.TestCase):
    """Section 5 & 7: Audit of Candidato-Piloto-05 against frozen human reference."""

    @classmethod
    def setUpClass(cls):
        src = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-01/Pilot Input - Source Transcript v3.md")
        cls.pilot_res = run_real_pilot(src)["pipeline"]
        cls.evals = cls.pilot_res["artifacts"]["evaluations"]
        cls.system_scores = [e["score"] for e in cls.evals]
        cls.human_scores = [4.0, 7.0, 4.0, 8.0, 2.0, 5.0, 5.0, 7.0, 4.0, 6.0, 4.0]

    def test_pilot_question_count(self):
        self.assertEqual(len(self.system_scores), 11)

    def test_pilot_mean_absolute_error(self):
        mae = sum(abs(s - h) for s, h in zip(self.system_scores, self.human_scores)) / len(self.system_scores)
        self.assertAlmostEqual(mae, 7.0 / 11.0, places=3)
        self.assertEqual(round(mae, 2), 0.64)

    def test_pilot_exact_concordances(self):
        for q_idx in (0, 2, 8, 10):
            self.assertEqual(self.system_scores[q_idx], self.human_scores[q_idx])

    def test_pilot_material_divergence_q5(self):
        diff_q5 = abs(self.system_scores[4] - self.human_scores[4])
        self.assertEqual(round(diff_q5, 2), 2.45)

    def test_pilot_substantial_divergence_q10(self):
        diff_q10 = abs(self.system_scores[9] - self.human_scores[9])
        self.assertEqual(round(diff_q10, 2), 1.65)


if __name__ == "__main__":
    unittest.main()
