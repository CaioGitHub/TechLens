import copy
import unittest

from reference_runtime import run_interview_pipeline


def _fixture(case_id, question, answer, **metadata):
    fixture = {
        "fixture_id": case_id,
        "pipeline_version": "31.4-reference-1",
        "participants": [
            {"participant_id": "I", "name": "Interviewer", "role": "interviewer"},
            {"participant_id": "C", "name": "Candidate", "role": "candidate"},
        ],
        "raw_transcript": [
            {"id": f"{case_id}-Q", "timestamp": "00:00", "speaker": "Interviewer", "text": question},
            {"id": f"{case_id}-R", "timestamp": "00:01", "speaker": "Candidate", "text": answer},
        ],
    }
    fixture.update(metadata)
    return fixture


def _run(case_id, question, answer, **metadata):
    return run_interview_pipeline(_fixture(case_id, question, answer, **metadata))["artifacts"]


def _projection(artifacts):
    evaluation = artifacts["evaluations"][0]
    return {
        "score": evaluation["score"],
        "dimensions": evaluation["dimensions"],
        "evidence": [(item["type"], item["qualification"]) for item in artifacts["evidence"]["evidence_set"]],
    }


class Stage314SemanticRelevanceInvarianceTests(unittest.TestCase):
    def test_original_findings_are_resolved_without_pair_rules(self):
        cases = [
            ("D2", "Como funciona Docker?", "Kubernetes orquestra containers em clusters."),
            ("D3", "Explique SQL.", "Redis armazena dados em memória como chave e valor."),
            ("L1", "Como funciona Dependency Injection?", "Spring Data fornece abstrações para acesso a bancos de dados."),
        ]
        for case_id, question, answer in cases:
            artifacts = _run(case_id, question, answer)
            self.assertIn("off_topic", {item["type"] for item in artifacts["evidence"]["evidence_set"]})
            self.assertNotEqual(
                artifacts["evaluations"][0]["dimensions"]["correctness"]["assessment"],
                "Strong",
            )

    def test_generalizes_to_new_domain_mismatches(self):
        cases = [
            ("N1", "Como funciona autenticação OAuth?", "Cache reduz latência e evita consultas repetidas."),
            ("N2", "Como criar índices SQL?", "Kafka usa tópicos e consumidores."),
            ("N3", "Como funciona Docker networking?", "Jenkins executa pipelines de CI/CD."),
            ("N4", "Como funcionam Angular Signals?", "CSS define estilos e layout."),
            ("N5", "Como proteger uma API?", "Redis acelera leituras com cache."),
            ("N6", "Como funciona arquitetura hexagonal?", "JWT assina tokens para autenticação."),
            ("N7", "Como funciona event-driven?", "JWT assina tokens para autenticação."),
            ("N8", "Como testar um endpoint?", "Kubernetes orquestra containers."),
            ("N9", "Como escolher banco relacional?", "Redis armazena dados em memória."),
            ("N10", "Como funciona Docker networking?", "Jenkins executa pipelines de CI/CD."),
        ]
        for case_id, question, answer in cases:
            artifacts = _run(case_id, question, answer)
            self.assertIn("off_topic", {item["type"] for item in artifacts["evidence"]["evidence_set"]}, case_id)

    def test_legitimate_related_concepts_are_not_off_topic(self):
        cases = [
            ("R1", "Como investigaria uma falha 500?", "Verificaria logs, traces, dependências e métricas."),
            ("R2", "Como projetaria uma API resiliente?", "Usaria timeout, retry com backoff, circuit breaker e observabilidade."),
            ("R3", "Como funciona uma transação no Spring?", "Spring possui @Transactional e permite configurar transações."),
            ("R4", "Como observar uma aplicação?", "Usaria métricas, logs e traces para correlacionar falhas."),
            ("R5", "Como funciona Docker networking?", "Containers usam redes bridge e DNS interno para se comunicar."),
        ]
        for case_id, question, answer in cases:
            artifacts = _run(case_id, question, answer)
            self.assertNotIn("off_topic", {item["type"] for item in artifacts["evidence"]["evidence_set"]}, case_id)

    def test_partial_relevance_preserves_positive_and_limits_strength(self):
        artifacts = _run(
            "PARTIAL",
            "Como investigaria uma falha 500?",
            "Primeiro verificaria logs. Também explicaria como Kafka funciona e como configurar consumidores.",
        )
        types = {item["type"] for item in artifacts["evidence"]["evidence_set"]}
        self.assertIn("conceptual", types)
        self.assertNotEqual(artifacts["evaluations"][0]["dimensions"]["correctness"]["assessment"], "Strong")

    def test_formal_informal_short_and_hesitant_equivalence(self):
        answers = [
            "A aplicação utiliza cache para reduzir a latência das consultas.",
            "A gente usa cache pra deixar as consultas mais rápidas.",
            "Cache reduz a latência das consultas.",
            "Bom, a gente usa cache, né, pra consulta ficar mais rápida.",
        ]
        projections = [
            _projection(_run(f"EQ{i}", "Como reduziria a latência de consultas?", answer))
            for i, answer in enumerate(answers)
        ]
        correctness = {item["dimensions"]["correctness"]["assessment"] for item in projections}
        self.assertEqual(correctness, {"Strong"})

    def test_equivalent_autocorrection_and_direct_answer(self):
        direct = _projection(_run("AUTO-A", "Como funciona RabbitMQ?", "RabbitMQ é assíncrono e usa filas."))
        corrected = _projection(_run("AUTO-B", "Como funciona RabbitMQ?", "RabbitMQ é síncrono... quer dizer, assíncrono e usa filas."))
        self.assertEqual(
            direct["dimensions"]["correctness"]["assessment"],
            corrected["dimensions"]["correctness"]["assessment"],
        )

    def test_length_and_jargon_do_not_replace_evidence(self):
        simple = _projection(_run("JARGON-A", "Explique REST.", "REST usa recursos e HTTP."))
        verbose = _projection(_run(
            "JARGON-B",
            "Explique REST.",
            "REST, HTTP, microservices, CQRS, DDD, SOLID, cloud e observabilidade são palavras importantes, "
            "mas esta frase não explica como recursos, métodos ou representações são utilizados.",
        ))
        self.assertLessEqual(verbose["score"], simple["score"])

    def test_experience_progression_remains_distinct(self):
        declaration = _projection(_run("EXP-A", "Você tem experiência com Kubernetes?", "Já trabalhei com Kubernetes."))
        demonstrated = _projection(_run("EXP-B", "Você tem experiência com Kubernetes?", "Já trabalhei com Kubernetes. Configurei deployments e probes."))
        troubleshooting = _projection(_run(
            "EXP-C",
            "Você tem experiência com Kubernetes?",
            "Já trabalhei com Kubernetes. Tivemos restart loop; investiguei logs, eventos e probes e corrigi a configuração.",
        ))
        self.assertIn(("experience_declaration", "insufficient"), declaration["evidence"])
        self.assertIn("demonstrated_experience", {item[0] for item in demonstrated["evidence"]})
        self.assertGreaterEqual(troubleshooting["score"], demonstrated["score"])

    def test_troubleshooting_and_architecture_pairs(self):
        pairs = [
            ("Como investigaria erro 500?", "Verificaria logs, traces e dependências.", "Eu usaria Kubernetes porque ele gerencia containers."),
            ("Como aplicaria SOLID?", "Separaria responsabilidades e dependeria de abstrações.", "Redis acelera leituras em memória."),
            ("Como desenharia arquitetura hexagonal?", "Usaria portas e adapters para inverter dependências.", "CSS controla estilos da interface."),
            ("Como projetaria um sistema event-driven?", "Usaria eventos, consumidores desacoplados e idempotência.", "JWT assina tokens."),
        ]
        for index, (question, related, unrelated) in enumerate(pairs):
            good = _projection(_run(f"PAIR-G{index}", question, related))
            bad = _projection(_run(f"PAIR-B{index}", question, unrelated))
            self.assertGreater(good["score"], bad["score"])

    def test_context_seniority_cv_and_order_invariance(self):
        base = _run("CTX-A", "O que é HTTP 500?", "É um erro interno do servidor.")
        variants = [
            _run("CTX-B", "O que é HTTP 500?", "É um erro interno do servidor.", metadata={"seniority": "junior", "cv": "irrelevant"}),
            _run("CTX-C", "O que é HTTP 500?", "É um erro interno do servidor.", metadata={"seniority": "senior", "job_context": {"title": "staff"}}),
        ]
        expected = _projection(base)
        for variant in variants:
            self.assertEqual(expected, _projection(variant))

    def test_mutations_are_directional_and_idempotent(self):
        related = _run("M-A", "Explique REST.", "REST usa recursos e HTTP.")
        unrelated = _run("M-B", "Explique REST.", "Kubernetes orquestra containers.")
        enriched = _run("M-C", "Explique REST.", "REST usa recursos, HTTP, métodos, status e representações.")
        self.assertGreater(_projection(related)["score"], _projection(unrelated)["score"])
        self.assertGreaterEqual(_projection(enriched)["score"], _projection(related)["score"])
        repeated = _run("M-C", "Explique REST.", "REST usa recursos, HTTP, métodos, status e representações.")
        self.assertEqual(_projection(enriched), _projection(repeated))


if __name__ == "__main__":
    unittest.main()
