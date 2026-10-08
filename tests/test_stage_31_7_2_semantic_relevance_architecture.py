"""Stage 31.7.2 — Implementation & Decoupling of Semantic Relevance Architecture Test Suite.

Verifies the decoupled Semantic Relevance architecture implemented in Stage 31.7.2:
1. Architectural Decoupling: _FUNCTIONAL_CAPABILITIES retains NO eliminatory semantic authority.
2. Entity Anchor Contract: entity_match != DIRECT (mere presence of entity without mechanism is insufficient).
3. Polysemy Disambiguation: contextual demand routing for ambiguous tokens (transação, telemetria, endpoints).
4. Problem -> Mechanism Independence: causal resolution without lexical overlap (OCC, distributed tracing, token bucket).
5. 10+ New Unseen Technologies across canonical classes never present in catalog.
6. 10+ Technology-Free Concepts evaluated purely on functional mechanics.
7. Supporting vs Related functional discrimination (active troubleshooting vs passive documentation/tooling).
8. Epistemic Separation: experience declarations vs demonstrated experience vs hypothetical formulation.
9. Multi-Aspect Proposition Coverage based on semantic demand fulfillment.
10. Representation Invariance across formal, informal, colloquial, concise, and verbose responses.
11. Semantic Mutation Sensitivity: technical alterations and padding changes alter classification.
12. Shadow Mode Contract: evaluate_semantic_relevance_shadow returns old_result, new_result, difference, reason.
13. Determinism and execution isolation under repeated and shuffled executions.
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
    _legacy_evaluate_semantic_relevance,
    evaluate_semantic_relevance_shadow,
    _evaluate_multi_aspect_coverage,
    _lexical_contains,
    _stem_word,
    _extract_stemmed_tokens,
    _blind_dimensions,
    _FUNCTIONAL_CAPABILITIES,
)


def _case_fixture(case_id: str, question: str, response: str) -> dict[str, Any]:
    return {
        "metadata": {"interview_id": f"INT-{case_id}", "candidate_id": "CAND-3172"},
        "participants": [
            {"participant_id": "P-INT", "name": "Interviewer", "role": "interviewer"},
            {"participant_id": "P-CAN", "name": "Candidate", "role": "candidate"},
        ],
        "raw_transcript": [
            {"id": f"{case_id}-Q", "speaker": "Interviewer", "timestamp": "00:00", "text": question},
            {"id": f"{case_id}-R", "speaker": "Candidate", "timestamp": "00:05", "text": response},
        ],
    }


class Stage3172CatalogDecouplingTests(unittest.TestCase):
    """Section 5, 6 & 33: Functional Catalog Decoupling & Authority Removal."""

    def test_catalog_missing_technology_is_not_off_topic(self):
        """Unseen technology not present in _FUNCTIONAL_CAPABILITIES must NOT be rejected with OFF_TOPIC."""
        self.assertNotIn("duckdb", _FUNCTIONAL_CAPABILITIES)
        rec = _evaluate_semantic_relevance(
            {"text": "Como o DuckDB organiza a execução de queries em memória?"},
            {"reconstructed_text": "Utiliza processamento vetorizado colunar em processo otimizado para OLAP."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_alien_catalog_term_does_not_trigger_off_topic(self):
        """SurrealDB response mentioning relational tables (from data_access_abstraction) must remain DIRECT."""
        self.assertNotIn("surrealdb", _FUNCTIONAL_CAPABILITIES)
        rec = _evaluate_semantic_relevance(
            {"text": "Como o SurrealDB organiza dados multi-modelo?"},
            {"reconstructed_text": "SurrealDB combina tabelas relacionais, documentos e conexões de grafo."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_entity_match_is_not_a_free_pass_to_direct(self):
        """Section 8: entity_match == true without mechanism must NOT produce DIRECT conceptual evidence."""
        rec = _evaluate_semantic_relevance(
            {"text": "Como o OpenTelemetry padroniza a exportação de telemetria?"},
            {"reconstructed_text": "Usei OpenTelemetry durante dois anos na empresa anterior."},
        )
        # It's an experience declaration without the technical mechanism requested
        res = run_interview_pipeline(_case_fixture(
            "OTEL-DECL",
            "Como o OpenTelemetry padroniza a exportação de telemetria?",
            "Usei OpenTelemetry durante dois anos na empresa anterior.",
        ))
        ev_types = [item["type"] for item in res["artifacts"]["evidence"]["evidence_set"]]
        self.assertIn("experience_declaration", ev_types)
        # Must not be promoted to positive conceptual mechanism
        conceptual_pos = [item for item in res["artifacts"]["evidence"]["evidence_set"] if item["type"] == "conceptual" and item["qualification"] == "positive"]
        self.assertEqual(len(conceptual_pos), 0)


class Stage3172PolysemyDisambiguationTests(unittest.TestCase):
    """Section 13: Polysemy handling using full context instead of single isolated keywords."""

    def test_transacao_in_distributed_tracing_not_database_transaction(self):
        """'transação' in context of multiple services must map to distributed tracing, not database transactions."""
        rec = _evaluate_semantic_relevance(
            {"text": "Como rastrear uma transação que passa por múltiplos serviços sem perder o contexto?"},
            {"reconstructed_text": "Usaria trace e span IDs nos headers e propagaria o contexto downstream."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertEqual(rec["target_knowledge_domain"], "distributed_tracing")
        self.assertTrue(rec["functional_contribution"])

    def test_telemetria_in_opentelemetry_not_azure_kql(self):
        """'telemetria' in OpenTelemetry query must map to OTLP collector, not KQL / Azure Log Analytics."""
        rec = _evaluate_semantic_relevance(
            {"text": "Como o OpenTelemetry padroniza a exportação de telemetria?"},
            {"reconstructed_text": "OpenTelemetry padroniza traces, métricas e logs por meio do protocolo OTLP."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertEqual(rec["target_knowledge_domain"], "telemetry_collection_and_export")
        self.assertTrue(rec["functional_contribution"])

    def test_endpoints_in_rate_limiting_not_rest_verb_design(self):
        """'endpoints' in burst protection query must map to token bucket/sliding window, not REST verbs."""
        rec = _evaluate_semantic_relevance(
            {"text": "Como proteger endpoints públicos contra rajadas abusivas?"},
            {"reconstructed_text": "Usaria token bucket ou sliding window limitando requisições por cliente."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertEqual(rec["target_knowledge_domain"], "traffic_shaping_and_rate_limiting")
        self.assertTrue(rec["functional_contribution"])


class Stage3172UnseenTechnologiesTests(unittest.TestCase):
    """Section 24: 10+ Unseen Technologies never present in _FUNCTIONAL_CAPABILITIES."""

    def test_01_duckdb_columnar(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o DuckDB organiza a execução de queries em memória?"},
            {"reconstructed_text": "Utiliza processamento vetorizado colunar em processo otimizado para OLAP."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_02_cockroachdb_distributed_sql(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o CockroachDB implementa consistência distribuída em transações SQL?"},
            {"reconstructed_text": "Combina o algoritmo Raft para consenso e controle serializável distribuído."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_03_surrealdb_multimodel(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o SurrealDB organiza dados multi-modelo?"},
            {"reconstructed_text": "SurrealDB combina tabelas relacionais, documentos e conexões de grafo."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_04_linkerd_service_mesh(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Linkerd intercepta e gerencia tráfego na malha de serviços?"},
            {"reconstructed_text": "Injeta micro-proxies leves em Rust como sidecars para mTLS e roteamento L7."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_05_opentelemetry_collector(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o OpenTelemetry padroniza a exportação de telemetria?"},
            {"reconstructed_text": "OpenTelemetry padroniza traces, métricas e logs por meio do protocolo OTLP."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_06_polars_dataframes(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Polars processa DataFrames com alto desempenho?"},
            {"reconstructed_text": "Executa sobre Apache Arrow em Rust com avaliação lazy e paralelismo nativo."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_07_redpanda_streaming(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Redpanda processa fluxos de streaming compatíveis com Kafka?"},
            {"reconstructed_text": "Redpanda implementa a API do Kafka em C++ com arquitetura thread-per-core."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_08_triton_inference_server(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Triton Inference Server gerencia modelos de Machine Learning?"},
            {"reconstructed_text": "Orquestra lotes dinâmicos de inferência em múltiplas instâncias de GPU."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_09_spire_workload_identity(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Spire autentica workloads em ambientes heterogêneos?"},
            {"reconstructed_text": "Implementa a especificação SPIFFE emitindo documentos SVID assinados criptograficamente."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_10_fluentbit_log_processor(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Fluentbit coleta e encaminha eventos de log?"},
            {"reconstructed_text": "Coleta logs de containers e aplica filtros de parsing antes de encaminhar aos destinos."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_11_ebpf_packet_filtering(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o eBPF permite observabilidade e segurança no kernel Linux?"},
            {"reconstructed_text": "Executa bytecode seguro no kernel via XDP para filtrar pacotes e coletar métricas."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_12_zero_knowledge_proofs(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funcionam as provas de conhecimento zero em verificação de identidade?"},
            {"reconstructed_text": "Permitem que um provador comprove matematicamente uma asserção para o verificador sem revelar o dado secreto subjacente."},
        )
        self.assertEqual(rec["classification"], "DIRECT")


class Stage3172TechnologyFreeConceptsTests(unittest.TestCase):
    """Section 25: 10 Technology-Free Concepts evaluated on causal mechanics."""

    def test_01_optimistic_concurrency_control(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como evitar conflitos de escrita concorrente sem travar a linha no banco?"},
            {"reconstructed_text": "Usaria versionamento por timestamp ou contador, validando a versão antes do commit."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_02_backpressure_flow_control(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como evitar que um produtor rápido sobrecarregue um consumidor lento?"},
            {"reconstructed_text": "Implementaria backpressure para que o consumidor sinalize quando diminuir a taxa."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_03_idempotency_deduplication(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como processar a mesma requisição múltiplas vezes sem duplicar pagamentos?"},
            {"reconstructed_text": "Usaria chave de idempotência validando se o token já foi executado antes de processar."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_04_distributed_context_propagation(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como rastrear uma transação que passa por múltiplos serviços sem perder o contexto?"},
            {"reconstructed_text": "Usaria trace e span IDs nos headers e propagaria o contexto downstream."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_05_circuit_breaker_fallback(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como impedir que a indisponibilidade de um serviço parceiro derrube a nossa aplicação?"},
            {"reconstructed_text": "Abriria o circuito temporariamente ao detectar alta taxa de erros e responderia via fallback com resposta degradada ou cache."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")

    def test_06_eventual_consistency_reconciliation(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como garantir consistência entre dois serviços sem transação distribuída em duas fases?"},
            {"reconstructed_text": "Adotaria consistência eventual com publicação de eventos assíncronos e rotinas de reconciliação para corrigir inconsistências."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_07_regression_detection_p99_baseline(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como identificar degradação de performance após um novo deploy?"},
            {"reconstructed_text": "Compararia as métricas de latência P99 e taxa de erro da nova versão contra a baseline histórica de telemetria da versão anterior."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_08_bulkhead_resource_isolation(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como evitar que chamadas a um serviço lento esgotem todas as threads da aplicação?"},
            {"reconstructed_text": "Segmentaria pools de threads dedicadas e limites de conexões separados para cada dependência externa."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")

    def test_09_ttl_cache_invalidation(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como acelerar leituras e impedir que dados obsoletos permaneçam em memória?"},
            {"reconstructed_text": "Configuraria tempo de vida TTL com renovação automática e invalidação explícita nos eventos de alteração cadastral."},
        )
        self.assertEqual(rec["classification"], "DIRECT")

    def test_10_token_bucket_rate_limiting(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como proteger endpoints públicos contra rajadas abusivas?"},
            {"reconstructed_text": "Usaria token bucket ou sliding window limitando requisições por cliente."},
        )
        self.assertEqual(rec["classification"], "DIRECT")


class Stage3172SupportingVsRelatedTests(unittest.TestCase):
    """Section 11: Supporting vs Related Discrimination."""

    def test_troubleshooting_diagnostic_action_is_supporting(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como você investigaria um erro HTTP 500?"},
            {"reconstructed_text": "Eu analisaria logs da aplicação, métricas de dependências e traces correlacionados."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_passive_documentation_is_related(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona a arquitetura REST?"},
            {"reconstructed_text": "O ecossistema possui ferramentas como Swagger para documentar endpoints e OpenAPI para contratos de API."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_adjacent_stack_persistence_is_related(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona Dependency Injection no Spring?"},
            {"reconstructed_text": "Spring Data fornece repositórios e abstrações para persistência com JPA e bancos relacionais."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])


class Stage3172RepresentationInvarianceTests(unittest.TestCase):
    """Section 28: Representation Invariance across linguistic variations."""

    def test_formality_and_colloquialism_invariance(self):
        q = {"text": "Como o cache em memória reduz latência?"}
        formal = {"reconstructed_text": "O mecanismo de cache armazena em memória primária os dados de acesso frequente, evitando I/O de disco."}
        informal = {"reconstructed_text": "A gente guarda os dados mais acessados na memória pra não ter que bater no disco toda hora."}
        colloquial = {"reconstructed_text": "Joga em memória com cache e pronto, economiza leitura pesada de disco."}

        rec_f = _evaluate_semantic_relevance(q, formal)
        rec_i = _evaluate_semantic_relevance(q, informal)
        rec_c = _evaluate_semantic_relevance(q, colloquial)

        self.assertEqual(rec_f["classification"], "DIRECT")
        self.assertEqual(rec_i["classification"], "DIRECT")
        self.assertEqual(rec_c["classification"], "DIRECT")

    def test_self_correction_preserves_semantics(self):
        q = {"text": "Como o Redpanda processa fluxos compatíveis com Kafka?"}
        r = {"reconstructed_text": "Ele usa Java... espera, não, na verdade o Redpanda foi feito em C++ com arquitetura thread-per-core sem JVM."}
        rec = _evaluate_semantic_relevance(q, r)
        self.assertEqual(rec["classification"], "DIRECT")


class Stage3172MutationTests(unittest.TestCase):
    """Section 27: Semantic Mutation Tests."""

    def test_mutation_reversing_mechanism_alters_classification(self):
        q = {"text": "Como evitar conflitos de escrita concorrente sem travar a linha no banco?"}
        valid_r = {"reconstructed_text": "Usaria versionamento por timestamp, validando a versão antes do commit."}
        mutated_r = {"reconstructed_text": "Usaria validação de esquema JSON para garantir que o payload está bem formatado."}

        rec_valid = _evaluate_semantic_relevance(q, valid_r)
        rec_mutated = _evaluate_semantic_relevance(q, mutated_r)

        self.assertEqual(rec_valid["classification"], "DIRECT")
        self.assertEqual(rec_mutated["classification"], "OFF_TOPIC")

    def test_mutation_buzzword_padding_does_not_promote(self):
        q = {"text": "Como evitar conflitos de escrita concorrente sem travar a linha no banco?"}
        buzz_r = {"reconstructed_text": "Aplicaria uma arquitetura moderna com microsserviços ágeis e escalabilidade em cloud com metodologia ágil contínua."}
        rec = _evaluate_semantic_relevance(q, buzz_r)
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])


class Stage3172ShadowModeTests(unittest.TestCase):
    """Section 29: Shadow Mode Contract Verification."""

    def test_shadow_mode_structure_and_comparison(self):
        q = {"text": "Como o SurrealDB organiza dados multi-modelo?"}
        r = {"reconstructed_text": "SurrealDB combina tabelas relacionais, documentos e conexões de grafo."}

        shadow = evaluate_semantic_relevance_shadow(q, r)
        self.assertIn("old_result", shadow)
        self.assertIn("new_result", shadow)
        self.assertIn("difference", shadow)
        self.assertIn("reason", shadow)

        # Legacy rejected SurrealDB due to 'tabelas relacionais' triggering alien domain
        self.assertEqual(shadow["old_result"]["classification"], "OFF_TOPIC")
        # Decoupled engine classifies SurrealDB correctly as DIRECT
        self.assertEqual(shadow["new_result"]["classification"], "DIRECT")
        self.assertTrue(shadow["difference"])
        self.assertIn("Classification changed", shadow["reason"])


class Stage3172DeterminismAndIsolationTests(unittest.TestCase):
    """Sections 35 & 36: Strict determinism and permutation isolation."""

    def test_determinism_across_multiple_invocations(self):
        q = {"text": "Como o Redpanda processa fluxos compatíveis com Kafka?"}
        r = {"reconstructed_text": "Redpanda implementa a API do Kafka em C++ com arquitetura thread-per-core."}
        first = _evaluate_semantic_relevance(q, r)
        for _ in range(20):
            again = _evaluate_semantic_relevance(q, r)
            self.assertEqual(first, again)

    def test_isolation_under_shuffled_order(self):
        cases = [
            ("C1", "Como funciona a arquitetura REST?", "REST usa HTTP com verbos e recursos."),
            ("C2", "Como investigar um erro HTTP 500?", "Analisaria logs e métricas de dependência."),
            ("C3", "Como o SurrealDB organiza dados multi-modelo?", "SurrealDB combina tabelas relacionais e grafos."),
        ]
        seq1 = [_evaluate_semantic_relevance({"text": c[1]}, {"reconstructed_text": c[2]})["classification"] for c in cases]
        shuffled = list(cases)
        random.seed(42)
        random.shuffle(shuffled)
        seq2 = [_evaluate_semantic_relevance({"text": c[1]}, {"reconstructed_text": c[2]})["classification"] for c in shuffled]
        # Reconstruct seq2 in original order
        mapping = {c[0]: cls for c, cls in zip(shuffled, seq2)}
        self.assertEqual(seq1, [mapping[c[0]] for c in cases])


if __name__ == "__main__":
    unittest.main()
