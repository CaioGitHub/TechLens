"""Tests for Stage 31.6 — Controlled Correction of Semantic Relevance Model.

Validates the structural corrections implemented in Stage 31.6:
1. Removal of all word-count proxies (len <= 6, len <= 3, word_count, token_count)
   for multi-aspect coverage and evidence evaluation.
2. Aspect-by-aspect propositional coverage derivation for multi-aspect queries.
3. General morphological normalization and stemming layer for Portuguese and English loanwords
   without closed vocabulary dictionaries.
4. Word-boundary / whole-token matching preventing substring collisions
   (e.g., 'orm' in 'performance', 'bus' in 'business', 'api' in 'apicultura').
5. Domain-open robustness on unseen foreign technologies without hardcoded entries.
6. Technology-free concept demonstrations.
7. Supporting vs Related functional discrimination.
8. Epistemic separation of experience declarations vs demonstrations.
9. Mutation causality tests demonstrating structural integrity.
10. Strict determinism and execution isolation.
"""

from __future__ import annotations

import copy
import random
import unittest
from typing import Any

from reference_runtime import run_interview_pipeline
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
        "metadata": {"interview_id": f"INT-{case_id}", "candidate_id": "CAND-316"},
        "participants": [
            {"participant_id": "P-INT", "name": "Interviewer", "role": "interviewer"},
            {"participant_id": "P-CAN", "name": "Candidate", "role": "candidate"},
        ],
        "raw_transcript": [
            {"id": f"{case_id}-Q", "speaker": "Interviewer", "timestamp": "00:00", "text": question},
            {"id": f"{case_id}-R", "speaker": "Candidate", "timestamp": "00:05", "text": response},
        ],
    }


class Stage316MultiAspectCoverageTests(unittest.TestCase):
    """Section 19: Multi-aspect coverage without word-count proxies."""

    def test_01_short_answer_covering_all_aspects_is_direct(self):
        """Short answer (<= 7 words) covering all aspects must be DIRECT, never downgraded by length."""
        rec = _evaluate_semantic_relevance(
            {"text": "Como evitar retry agressivo e tempestade de requisições?"},
            {"reconstructed_text": "Usaria backoff exponencial com jitter e circuit breaker."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

        # Also test on open domain multi-aspect
        rec2 = _evaluate_semantic_relevance(
            {"text": "O que é ScyllaDB e qual seu modelo de dados?"},
            {"reconstructed_text": "ScyllaDB é banco NoSQL cujo modelo de dados é wide-column distribuído."},
        )
        self.assertEqual(rec2["classification"], "DIRECT")
        self.assertTrue(rec2["functional_contribution"])

    def test_02_long_answer_covering_only_one_aspect_remains_partial(self):
        """Long answer (>30 words) covering only one aspect must remain PARTIAL, never promoted by length."""
        long_one_aspect = (
            "Para particionar tópicos no Kafka, nós definimos a chave de mensagem de forma "
            "consistente garantindo que todos os eventos do mesmo agregado caiam rigorosamente "
            "na mesma partição para preservar a ordem sequencial dos registros sem desvios operacionais."
        )
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o particionamento no Kafka e como funciona o rebalanceamento de consumidores?"},
            {"reconstructed_text": long_one_aspect},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertEqual(rec.get("relation_type"), "partial_aspect_coverage")

    def test_03_medium_answer_covering_initial_aspect_omitting_secondary(self):
        """Answer covering initial aspect but omitting secondary must be PARTIAL."""
        rec = _evaluate_semantic_relevance(
            {"text": "Explique REST e como funciona uma requisição HTTP."},
            {"reconstructed_text": "REST usa HTTP."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertEqual(rec.get("relation_type"), "partial_aspect_coverage")

    def test_04_long_answer_irrelevant_is_off_topic(self):
        """Long padding describing unrelated mechanisms must remain OFF_TOPIC."""
        long_off_topic = (
            "No ambiente de desenvolvimento nós configuramos pipelines completos de integração contínua "
            "usando Jenkins e Docker para gerar imagens, executar testes automatizados e publicar "
            "artefatos no repositório corporativo com aprovação em múltiplos estágios de validação."
        )
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona o isolamento de transações com lock otimista no banco de dados?"},
            {"reconstructed_text": long_off_topic},
        )
        self.assertEqual(rec["classification"], "OFF_TOPIC")
        self.assertFalse(rec["functional_contribution"])

    def test_05_multiple_propositions_covering_multiple_demands(self):
        """Response with multiple distinct technical propositions covering multi-aspect question."""
        rec = _evaluate_semantic_relevance(
            {"text": "O que é Cilium e como protege a rede?"},
            {"reconstructed_text": "Cilium utiliza programas eBPF carregados no kernel Linux para filtragem de pacotes e políticas de segurança."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_06_oauth_refresh_token_omission_is_partial(self):
        """Omitting refresh token explanation in OAuth query must be PARTIAL."""
        rec = _evaluate_semantic_relevance(
            {"text": "Explique OAuth2 e como funciona o refresh token."},
            {"reconstructed_text": "OAuth2 emite token de acesso."},
        )
        self.assertEqual(rec["classification"], "PARTIAL")
        self.assertEqual(rec.get("relation_type"), "partial_aspect_coverage")


class Stage316LinguisticInvarianceTests(unittest.TestCase):
    """Section 20: General morphological normalization and stemming."""

    def test_correlation_verb_noun_inflections_preserve_relevance(self):
        """correlacionar, correlação, correlacionando, correlacionou must normalize consistently."""
        forms = [
            "correlacionar logs e traces para identificar causa raiz",
            "fazer a correlação entre logs e traces para identificar causa raiz",
            "estamos correlacionando logs e traces para identificar causa raiz",
            "a equipe correlacionou logs e traces para identificar causa raiz",
        ]
        q = {"text": "Como você investigaria a causa raiz de um erro 500?"}
        results = [_evaluate_semantic_relevance(q, {"reconstructed_text": form}) for form in forms]
        for res in results:
            self.assertEqual(res["classification"], "SUPPORTING")
            self.assertTrue(res["functional_contribution"])

    def test_retry_repeticao_plural_inflections(self):
        """Plural and singular forms of technical loanwords and Portuguese nouns."""
        stems_retries = _extract_stemmed_tokens("retries e repetições")
        stems_retry = _extract_stemmed_tokens("retry e repetição")
        self.assertIn("retry", stems_retries)
        self.assertIn("retry", stems_retry)
        self.assertIn("repet", stems_retries)
        self.assertIn("repet", stems_retry)

    def test_general_portuguese_conjugations(self):
        """Verify general Portuguese verbal and noun suffixes normalize correctly."""
        self.assertEqual(_stem_word("atualizações"), "atualiz")
        self.assertEqual(_stem_word("atualização"), "atualiz")
        self.assertEqual(_stem_word("atualizar"), "atualiz")
        self.assertEqual(_stem_word("atualizamos"), "atualiz")
        self.assertEqual(_stem_word("configurações"), "configur")
        self.assertEqual(_stem_word("configuração"), "configur")
        self.assertEqual(_stem_word("configurar"), "configur")


class Stage316LexicalCollisionTests(unittest.TestCase):
    """Section 21: Token boundary & lexical collision prevention."""

    def test_orm_does_not_collide_with_performance(self):
        """'orm' must not match inside 'performance'."""
        self.assertFalse(_lexical_contains("otimizamos a performance da consulta", "orm"))
        self.assertTrue(_lexical_contains("usamos um framework de ORM no projeto", "orm"))

    def test_api_does_not_collide_with_apicultura(self):
        """'api' must not match inside 'apicultura' or other compound words."""
        self.assertFalse(_lexical_contains("o sistema trata sobre apicultura moderna", "api"))
        self.assertTrue(_lexical_contains("construímos uma API REST para o cliente", "api"))

    def test_bus_does_not_collide_with_business(self):
        """'bus' must not match inside 'business'."""
        self.assertFalse(_lexical_contains("regras de business logic no domínio", "bus"))
        self.assertTrue(_lexical_contains("usamos um service bus para eventos", "bus"))

    def test_log_does_not_collide_with_login(self):
        """'log' must not match inside 'login'."""
        self.assertFalse(_lexical_contains("a tela de login do usuário falhou", "log"))
        self.assertTrue(_lexical_contains("coletamos o log da aplicação no servidor", "log"))

    def test_trace_does_not_collide_with_traceroute(self):
        """'trace' must match word trace/traces, not arbitrary substring."""
        self.assertTrue(_lexical_contains("coletamos traces distribuídos", "trace"))
        self.assertFalse(_lexical_contains("executamos um traceroute na rede", "trace"))

    def test_sincrono_does_not_collide_with_assincrono(self):
        """'síncrono' must not collide with 'assíncrono'."""
        self.assertFalse(_lexical_contains("comunicação totalmente assíncrona", "síncrono"))
        self.assertFalse(_lexical_contains("comunicacao totalmente assincrona", "sincrono"))
        self.assertTrue(_lexical_contains("chamada totalmente síncrona bloqueante", "síncrono"))


class Stage316UnknownTechnologiesTests(unittest.TestCase):
    """Section 22: Unknown technologies foreign to internal capability dictionaries."""

    def test_unknown_tech_temporal_workflows(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Temporal garante a execução confiável de workflows de longa duração?"},
            {"reconstructed_text": "Temporal persiste o histórico de eventos de execução e usa event sourcing para replay determinístico em caso de falhas."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_unknown_tech_nats_jetstream(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é NATS JetStream e como gerencia persistência de mensagens?"},
            {"reconstructed_text": "JetStream adiciona streaming persistente ao NATS com retenção baseada em logs distribuídos e confirmação de entrega ack."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_unknown_tech_clickhouse_vectorized(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o ClickHouse processa consultas analíticas em alta velocidade?"},
            {"reconstructed_text": "ClickHouse armazena dados em colunas e utiliza execução vetorizada em lotes de dados com compactação agressiva."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_unknown_tech_keycloak_identity(self):
        rec = _evaluate_semantic_relevance(
            {"text": "O que é Keycloak e qual seu papel em SSO corporativo?"},
            {"reconstructed_text": "Keycloak atua como identity provider centralizado gerenciando autenticação federada via OpenID Connect e SAML."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_unknown_tech_traefik_reverse_proxy(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como o Traefik realiza roteamento dinâmico em ambientes conteinerizados?"},
            {"reconstructed_text": "Traefik escuta eventos da API do orquestrador e atualiza rotas e certificados TLS automaticamente sem reinicialização."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])


class Stage316TechnologyFreeConceptsTests(unittest.TestCase):
    """Section 23: Technical concepts articulated without naming specific products."""

    def test_in_memory_caching_without_redis_name(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como acelerar leituras de dados frequentemente acessados?"},
            {"reconstructed_text": "Armazenaria os resultados em memória temporariamente com política de expiração TTL para evitar consultas repetidas ao banco."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])

    def test_circuit_breaking_without_product_name(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como evitar falha em cascata quando um serviço parceiro fica lento?"},
            {"reconstructed_text": "Interromperia temporariamente as chamadas abrindo o circuito após uma taxa de erros e retornaria fallback degradado."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_eventual_consistency_without_product_name(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como garantir a consistência de dados entre serviços desacoplados?"},
            {"reconstructed_text": "Adotaria consistência eventual publicando eventos com chave de idempotência e reconciliação periódica assíncrona."},
        )
        self.assertEqual(rec["classification"], "DIRECT")
        self.assertTrue(rec["functional_contribution"])


class Stage316SupportingVsRelatedTests(unittest.TestCase):
    """Section 24: Discrimination between SUPPORTING and RELATED."""

    def test_troubleshooting_diagnostic_action_is_supporting(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como você investigaria alto consumo de CPU em processos concorrentes?"},
            {"reconstructed_text": "Coletaria thread dumps no debug para verificar contenção de locks e threads bloqueadas em I/O."},
        )
        self.assertEqual(rec["classification"], "SUPPORTING")
        self.assertTrue(rec["functional_contribution"])

    def test_ecosystem_adjacency_without_mechanism_is_related(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona Dependency Injection no Spring?"},
            {"reconstructed_text": "Spring Data fornece repositórios e abstrações para persistência com JPA e bancos relacionais."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])

    def test_adjacent_tools_without_diagnostic_action_is_related(self):
        rec = _evaluate_semantic_relevance(
            {"text": "Como funciona a arquitetura REST?"},
            {"reconstructed_text": "O ecossistema possui ferramentas como Swagger para documentar endpoints e OpenAPI para contratos de API."},
        )
        self.assertEqual(rec["classification"], "RELATED")
        self.assertFalse(rec["functional_contribution"])


class Stage316ExperienceHierarchyTests(unittest.TestCase):
    """Section 25: Epistemic separation of declaration, hypothesis, and demonstration."""

    def test_declaration_only_produces_insufficient_qualification(self):
        res = run_interview_pipeline(_case_fixture(
            "EXP-DECL",
            "Você tem experiência com Kubernetes?",
            "Já trabalhei com Kubernetes.",
        ))
        ev_types = [item["type"] for item in res["artifacts"]["evidence"]["evidence_set"]]
        self.assertEqual(ev_types, ["experience_declaration"])
        eval_item = res["artifacts"]["evaluations"][0]
        self.assertEqual(eval_item["dimensions"]["correctness"]["assessment"], "Insufficient")
        self.assertEqual(eval_item["score"], 4.0)

    def test_hypothesis_is_epistemically_separated_from_demonstration(self):
        res = run_interview_pipeline(_case_fixture(
            "EXP-HYPO",
            "Como você lidaria com concorrência alta em pagamentos?",
            "Eu usaria locks otimistas com versionamento e retry controlado se houvesse essa demanda.",
        ))
        ev_types = [item["type"] for item in res["artifacts"]["evidence"]["evidence_set"]]
        self.assertIn("hypothesis", ev_types)
        self.assertNotIn("demonstrated_experience", ev_types)

    def test_demonstrated_experience_requires_concrete_production_action(self):
        res = run_interview_pipeline(_case_fixture(
            "EXP-DEMO",
            "Você tem experiência com Kubernetes?",
            "Em produção configurei deployments e probes, investiguei restart loops e corrigi a configuração de memória dos pods.",
        ))
        ev_types = [item["type"] for item in res["artifacts"]["evidence"]["evidence_set"]]
        self.assertIn("demonstrated_experience", ev_types)
        eval_item = res["artifacts"]["evaluations"][0]
        self.assertEqual(eval_item["dimensions"]["practical_application"]["assessment"], "Strong")
        self.assertGreaterEqual(eval_item["score"], 7.0)


class Stage316MutationTests(unittest.TestCase):
    """Section 29: Deliberate mutation tests demonstrating causal validity."""

    def test_mutation_1_removing_covering_proposition_decreases_coverage(self):
        """Removing the proposition covering Aspect 2 turns DIRECT into PARTIAL."""
        full_text = "Envoy é um proxy de borda e sidecar que intercepta tráfego de rede provendo roteamento L7 e observabilidade."
        mutated_text = "Envoy é um proxy de borda."
        q = {"text": "O que é o Envoy proxy e qual seu papel em service mesh?"}

        full_rel = _evaluate_semantic_relevance(q, {"reconstructed_text": full_text})
        mutated_rel = _evaluate_semantic_relevance(q, {"reconstructed_text": mutated_text})

        self.assertEqual(full_rel["classification"], "DIRECT")
        self.assertEqual(mutated_rel["classification"], "PARTIAL")

    def test_mutation_2_adding_irrelevant_proposition_does_not_increase_coverage(self):
        """Adding irrelevant padding to a partial response must not promote it to DIRECT."""
        partial_base = "Kafka divide tópicos em partições."
        padded_text = (
            "Kafka divide tópicos em partições. Além disso, nós usamos git com feature branches, "
            "fazemos pull requests com code review diário e deployamos no ambiente de homologação."
        )
        q = {"text": "Como funciona o particionamento no Kafka e como funciona o rebalanceamento de consumidores?"}

        base_rel = _evaluate_semantic_relevance(q, {"reconstructed_text": partial_base})
        padded_rel = _evaluate_semantic_relevance(q, {"reconstructed_text": padded_text})

        self.assertEqual(base_rel["classification"], "PARTIAL")
        self.assertEqual(padded_rel["classification"], "PARTIAL")

    def test_mutation_3_substituting_term_with_inflection_preserves_semantics(self):
        """Inflection variants of equivalent root retain semantic classification."""
        base_text = "correlacionar logs e traces para investigar falhas"
        inflected_text = "fizemos a correlação de logs e traces para investigar falhas"
        q = {"text": "Como investigar erro HTTP 500?"}

        base_rel = _evaluate_semantic_relevance(q, {"reconstructed_text": base_text})
        inflected_rel = _evaluate_semantic_relevance(q, {"reconstructed_text": inflected_text})

        self.assertEqual(base_rel["classification"], inflected_rel["classification"])
        self.assertEqual(base_rel["functional_contribution"], inflected_rel["functional_contribution"])

    def test_mutation_4_lexically_similar_word_with_distinct_meaning_preserves_discrimination(self):
        """Words sharing prefix but differing in meaning must not cause false equivalence."""
        valid_orm = "Usamos o ORM do Hibernate para mapear entidades relacionais."
        collision_text = "Otimizamos a performance da aplicação reduzindo tempos de resposta."
        q = {"text": "Como funciona um framework de ORM?"}

        valid_rel = _evaluate_semantic_relevance(q, {"reconstructed_text": valid_orm})
        collision_rel = _evaluate_semantic_relevance(q, {"reconstructed_text": collision_text})

        self.assertEqual(valid_rel["classification"], "DIRECT")
        self.assertNotEqual(collision_rel["classification"], "DIRECT")


class Stage316DeterminismAndIsolationTests(unittest.TestCase):
    """Sections 30 & 31: Strict determinism and permutation isolation."""

    def test_strict_determinism_across_multiple_runs(self):
        fixture = _case_fixture(
            "DET-01",
            "Como funciona a virtual thread no Java 21?",
            "Virtual threads são threads leves gerenciadas pela JVM montadas em carrier threads do sistema operacional.",
        )
        res1 = run_interview_pipeline(fixture)
        res2 = run_interview_pipeline(fixture)
        res3 = run_interview_pipeline(fixture)

        score1 = res1["artifacts"]["evaluations"][0]["score"]
        score2 = res2["artifacts"]["evaluations"][0]["score"]
        score3 = res3["artifacts"]["evaluations"][0]["score"]

        self.assertEqual(score1, score2)
        self.assertEqual(score2, score3)
        self.assertEqual(
            res1["artifacts"]["evaluations"][0]["dimensions"],
            res2["artifacts"]["evaluations"][0]["dimensions"],
        )

    def test_execution_isolation_under_shuffling(self):
        cases = [
            ("ISO-01", "Explique REST.", "REST usa HTTP para expor recursos via endpoints."),
            ("ISO-02", "O que é SQL?", "SQL é linguagem para consultar tabelas em bancos relacionais."),
            ("ISO-03", "Como funciona Docker?", "Docker isola containers usando namespaces e cgroups."),
        ]
        base_scores = [
            run_interview_pipeline(_case_fixture(cid, q, a))["artifacts"]["evaluations"][0]["score"]
            for cid, q, a in cases
        ]
        shuffled = list(cases)
        random.seed(42)
        random.shuffle(shuffled)
        shuffled_scores = {
            cid: run_interview_pipeline(_case_fixture(cid, q, a))["artifacts"]["evaluations"][0]["score"]
            for cid, q, a in shuffled
        }
        for (cid, _, _), base_score in zip(cases, base_scores):
            self.assertEqual(base_score, shuffled_scores[cid])


if __name__ == "__main__":
    unittest.main()
