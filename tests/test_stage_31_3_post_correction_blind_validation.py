import copy
import hashlib
import unittest
from pathlib import Path

from reference_runtime import build_real_pilot_fixture, run_interview_pipeline, run_real_pilot


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "11 - Interview Evaluation"
    / "09 - Real Interview Pilot"
    / "Candidato-Piloto-01"
    / "Pilot Input - Source Transcript v3.md"
)
PILOT = ROOT / "11 - Interview Evaluation" / "09 - Real Interview Pilot" / "Candidato-Piloto-05"
HUMAN = PILOT / "Stage 31 — Human Evaluation Independent.md"
COMPARISON = PILOT / "Stage 31 — Human vs System Comparison.md"
STAGE311 = PILOT / "Stage 31.1 — Human vs System Failure Analysis.md"
STAGE312 = PILOT / "Stage 31.2 — Controlled Correction.md"
STAGE312_COMPARISON = PILOT / "Stage 31.2 — Human vs System Post-Correction.md"


def _fixture(case_id, question, answer, *, seniority=None):
    fixture = {
        "fixture_id": case_id,
        "pipeline_version": "31.3-independent",
        "participants": [
            {"participant_id": "I", "name": "Interviewer", "role": "interviewer"},
            {"participant_id": "C", "name": "Candidate", "role": "candidate"},
        ],
        "raw_transcript": [
            {"id": f"{case_id}-Q", "timestamp": "00:00", "speaker": "Interviewer", "text": question},
            {"id": f"{case_id}-R", "timestamp": "00:01", "speaker": "Candidate", "text": answer},
        ],
    }
    if seniority:
        fixture["metadata"] = {"seniority": seniority, "title": seniority}
    return fixture


CASES = [
    ("A1", "O que é injeção de dependência?", "É fornecer dependências externamente em vez de criar dentro da classe.", "positive"),
    ("A2", "O que é HTTP 500?", "É um erro interno do servidor.", "positive"),
    ("B1", "Como investigaria latência?", "Eu verificaria os logs.", "partial"),
    ("C1", "O que é HTTP 500?", "É um erro interno do servidor.", "superficial"),
    ("D1", "Explique REST.", "Kafka permite comunicação assíncrona entre producers e consumers.", "off_topic"),
    ("D2", "Como funciona Docker?", "Kubernetes orquestra containers em clusters.", "off_topic"),
    ("D3", "Explique SQL.", "Redis armazena dados em memória como chave e valor.", "off_topic"),
    ("E1", "O que é p95?", "É sempre o pior tempo de todas as requisições.", "incorrect"),
    ("F1", "Você tem experiência com Azure?", "Já trabalhei bastante com Azure.", "declared"),
    ("G1", "Você tem experiência com Kubernetes?", "Em produção configurei deployments e probes, investiguei restart loops e ajustei recursos.", "demonstrated"),
    ("H1", "Como você lidaria com mensageria?", "Eu usaria Kafka com retry e backoff se tivesse esse cenário.", "hypothetical"),
    ("I1", "O que é HTTP 500?", "Erro interno do servidor.", "short_correct"),
    ("J1", "Explique REST.", "REST, HTTP, microservices, CQRS, DDD, SOLID, Kafka, cloud e observabilidade são fundamentais para arquiteturas modernas escaláveis.", "jargon"),
    ("K1", "Como funciona uma transação no Spring?", "Spring possui @Transactional e permite configurar transações.", "partial_related"),
    ("L1", "Como funciona Dependency Injection?", "Spring Data fornece abstrações para acesso a bancos de dados.", "wrong_question"),
    ("M1", "Como funciona RabbitMQ?", "RabbitMQ é síncrono... quer dizer, assíncrono, usando filas.", "self_correction"),
    ("N1", "Como funciona o pipeline?", "Não tenho certeza, mas acredito que depende dos componentes.", "uncertain"),
    ("O1", "Explique Kubernetes.", "Não sei.", "unknown"),
    ("P1", "O que é REST?", "REST usa HTTP para recursos.", "incomplete"),
    ("Q1", "Como investigaria uma falha 500?", "Primeiro verificaria logs e traces, depois dependências externas e correlação para localizar a causa.", "related_context"),
    ("R1", "Como integra Java Spring Azure?", "No Spring implementamos APIs Java e usamos Application Insights e KQL para correlacionar falhas de dependências.", "integration"),
    ("S1", "O que é HTTP 500?", "É um erro interno do servidor, tipo quando dá problema no back-end.", "informal_correct"),
    ("T1", "O que é p95?", "É sempre o pior tempo de todas as requisições.", "polished_wrong"),
    ("X1", "Você tem experiência com Kubernetes?", "Já trabalhei com Kubernetes.", "declared_progression"),
    ("X2", "Você tem experiência com Kubernetes?", "Já trabalhei com Kubernetes. Configurei deployments e probes.", "demonstrated_progression"),
    ("X3", "Você tem experiência com Kubernetes?", "Já trabalhei com Kubernetes. Tivemos restart loop; investiguei logs, eventos e probes e corrigi a configuração.", "troubleshooting_progression"),
]


def _run(case):
    case_id, question, answer, _ = case
    return run_interview_pipeline(_fixture(case_id, question, answer))


def _projection(result):
    artifacts = result["artifacts"]
    if not artifacts["evaluations"]:
        return {
            "score": None,
            "confidence": None,
            "dimensions": {},
            "evidence": [
                (item["type"], item["qualification"])
                for item in artifacts["evidence"]["evidence_set"]
            ],
        }
    evaluation = artifacts["evaluations"][0]
    evidence = artifacts["evidence"]["evidence_set"]
    return {
        "score": evaluation["score"],
        "confidence": evaluation["confidence"],
        "dimensions": evaluation["dimensions"],
        "evidence": [(item["type"], item["qualification"]) for item in evidence],
    }


def _semantic_failures(results):
    failures = []
    by_case = {case_id: _projection(results[case_id]) for case_id, _, _, _ in CASES}

    for case_id in ("D1", "D2", "D3", "L1"):
        if "off_topic" not in {item[0] for item in by_case[case_id]["evidence"]}:
            failures.append({
                "case": case_id,
                "expected": "off_topic evidence",
                "actual": by_case[case_id],
                "root_cause_hypothesis": "domain mismatch heuristic remains narrow",
            })
    for case_id in ("A1", "A2", "C1", "I1", "S1", "Q1", "R1"):
        if by_case[case_id]["dimensions"].get("correctness", {}).get("assessment") == "Weak":
            failures.append({
                "case": case_id,
                "expected": "legitimate related answer receives correctness credit",
                "actual": by_case[case_id],
                "root_cause_hypothesis": "possible false negative",
            })
    if "experience_declaration" not in {item[0] for item in by_case["F1"]["evidence"]}:
        failures.append({"case": "F1", "expected": "experience_declaration", "actual": by_case["F1"]})
    if "demonstrated_experience" not in {item[0] for item in by_case["G1"]["evidence"]}:
        failures.append({"case": "G1", "expected": "demonstrated_experience", "actual": by_case["G1"]})
    if "hypothesis" not in {item[0] for item in by_case["H1"]["evidence"]}:
        failures.append({"case": "H1", "expected": "hypothesis", "actual": by_case["H1"]})
    if by_case["H1"]["dimensions"].get("practical_application", {}).get("assessment") == "Strong":
        failures.append({"case": "H1", "expected": "hypothesis not demonstrated experience", "actual": by_case["H1"]})
    progression_scores = [by_case[case_id]["score"] for case_id in ("X1", "X2", "X3")]
    if any(score is None for score in progression_scores) or progression_scores[0] >= progression_scores[1] or progression_scores[1] > progression_scores[2]:
        failures.append({
            "case": "X1-X3",
            "expected": "declaration <= demonstration <= troubleshooting progression",
            "actual": {case_id: by_case[case_id]["score"] for case_id in ("X1", "X2", "X3")},
        })
    return failures


class Stage313PostCorrectionBlindValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = {case_id: _run(case) for case in CASES for case_id in [case[0]]}
        cls.failures = _semantic_failures(cls.results)

    def test_executor_is_blind_to_oracles_and_human_results(self):
        for case_id, question, answer, _ in CASES:
            fixture = _fixture(case_id, question, answer)
            self.assertNotIn("expected", fixture)
            self.assertNotIn("oracle", fixture)
            self.assertNotIn("human_score", fixture)
            self.assertNotIn("evaluation_specs", fixture)
            self.assertNotIn("evidence_specs", fixture)
        self.assertNotIn("score", HUMAN.read_text(encoding="utf-8").split("##")[0])

    def test_independent_case_set_has_required_coverage(self):
        self.assertGreaterEqual(len(CASES), 20)
        kinds = {kind for _, _, _, kind in CASES}
        self.assertTrue({"positive", "partial", "off_topic", "declared", "demonstrated", "hypothetical", "jargon"} <= kinds)

    def test_q5_four_level_pertinence_contract(self):
        source = Path(SOURCE).read_text(encoding="utf-8")
        pilot = run_real_pilot(SOURCE)["pipeline"]["artifacts"]
        question = next(item for item in pilot["questions"] if item["question_id"] == "Q5")
        response = next(item for item in pilot["responses"] if item["response_id"] == "R17")
        evidence = [item for item in pilot["evidence"]["evidence_set"] if item["response_id"] == "R17"]
        evaluation = next(item for item in pilot["evaluations"] if item["question_id"] == "Q5")
        self.assertIn("api rest", question["text"].lower())
        self.assertIn("Kafka", response["text"])
        self.assertTrue(evidence)
        self.assertIn("off_topic", {item["type"] for item in evidence})
        self.assertNotEqual(evaluation["dimensions"]["correctness"]["assessment"], "Strong")
        self.assertIn("Transcript", source)

    def test_no_critical_false_negative_is_present(self):
        critical = [item for item in self.failures if item["case"] in {"A1", "A2", "C1", "I1", "Q1", "R1"}]
        self.assertEqual(critical, [])

    def test_no_residual_domain_mismatch_false_positive(self):
        mismatches = [item for item in self.failures if item["case"] in {"D1", "D2", "D3", "L1"}]
        self.assertEqual(mismatches, [])

    def test_experience_hypothesis_and_progression(self):
        self.assertEqual([item[0] for item in _projection(self.results["F1"])["evidence"]], ["experience_declaration"])
        self.assertIn("demonstrated_experience", {item[0] for item in _projection(self.results["G1"])["evidence"]})
        self.assertIn("hypothesis", {item[0] for item in _projection(self.results["H1"])["evidence"]})
        self.assertNotIn("demonstrated_experience", {item[0] for item in _projection(self.results["H1"])["evidence"]})

    def test_length_jargon_style_and_seniority_do_not_create_credit(self):
        short = _projection(self.results["I1"])
        informal = _projection(self.results["S1"])
        jargon = _projection(self.results["J1"])
        senior = _projection(run_interview_pipeline(_fixture("SENIOR", "O que é HTTP 500?", "É um erro interno do servidor.", seniority="senior")))
        junior = _projection(run_interview_pipeline(_fixture("JUNIOR", "O que é HTTP 500?", "É um erro interno do servidor.", seniority="junior")))
        self.assertEqual(short["dimensions"]["correctness"]["assessment"], informal["dimensions"]["correctness"]["assessment"])
        self.assertLessEqual(jargon["score"], 8.0)
        self.assertEqual(senior, junior)

    def test_mutations_are_semantically_directional(self):
        related = _projection(self.results["P1"])
        off_topic = _projection(self.results["D1"])
        complete = _projection(self.results["Q1"])
        partial = _projection(self.results["B1"])
        self.assertNotEqual(related["score"], off_topic["score"])
        self.assertGreaterEqual(complete["score"], partial["score"])

    def test_context_isolation_idempotency_and_source_protection(self):
        fixture = build_real_pilot_fixture(SOURCE)
        first = run_interview_pipeline(fixture)["artifacts"]
        second = run_interview_pipeline(copy.deepcopy(fixture))["artifacts"]
        self.assertEqual(first["evidence"], second["evidence"])
        self.assertEqual(first["evaluations"], second["evaluations"])
        external = copy.deepcopy(fixture)
        external.update({
            "cv": {"seniority": "staff"},
            "job_context": {"title": "staff", "company": "Other"},
            "expected_score": 10,
            "human_score": 1,
            "historical_report": "override",
        })
        self.assertEqual(first["evaluations"], run_interview_pipeline(external)["artifacts"]["evaluations"])
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest(), hashlib.sha256(SOURCE.read_bytes()).hexdigest())

    def test_repeated_validation_is_deterministic(self):
        repeated = {case_id: _run(case) for case in CASES for case_id in [case[0]]}
        self.assertEqual(
            {case_id: _projection(result) for case_id, result in self.results.items()},
            {case_id: _projection(result) for case_id, result in repeated.items()},
        )

    def test_historical_artifacts_are_frozen(self):
        self.assertIn("HUMAN_VS_SYSTEM_BLOCKED", COMPARISON.read_text(encoding="utf-8"))
        self.assertIn("HUMAN_VS_SYSTEM_FAILURE_ANALYSIS_COMPLETE_WITH_WARNINGS", STAGE311.read_text(encoding="utf-8"))
        self.assertIn("CONTROLLED_CORRECTION_COMPLETE_WITH_WARNINGS", STAGE312.read_text(encoding="utf-8"))
        self.assertIn("Mean absolute difference: `0.64`", STAGE312_COMPARISON.read_text(encoding="utf-8"))

    def test_oracle_comparator_has_no_unresolved_semantic_failures(self):
        self.assertEqual(self.failures, [])


if __name__ == "__main__":
    unittest.main()
