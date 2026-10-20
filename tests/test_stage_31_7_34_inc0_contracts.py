"""Stage 31.7.34 — INC-0 Contract & Unit Tests.

Validates the data foundation, typed dataclasses, Draft-07 schema compliance,
and causal traceability structures implemented in INC-0 (Cycle 6).
Ensures zero alteration to runtime semantic classification behavior.
"""

from __future__ import annotations

import json
import unittest
from datetime import datetime, timezone
from typing import Any

from reference_runtime.runtime import (
    DemandSpecification,
    QuestionProfile,
    DiscourseProposition,
    DiscourseProfile,
    ThematicAffinityEvaluation,
    ThematicEvaluation,
    EquivalenceEvaluation,
    AnalogyEvaluation,
    DemandNexusEvaluation,
    DemandNexusMatrix,
    CoverageEvaluation,
    EpistemicUncertaintyRecord,
    FinalDecisionRecord,
    EvidenceTraceabilityRecord,
    validate_evidence_traceability_record,
    _decoupled_evaluate_semantic_relevance,
    VALID_INTENT_MODES,
    VALID_DISCOURSE_ROLES,
    VALID_THEMATIC_STATUSES,
    VALID_REBUTTAL_REASONS,
    VALID_NEXUS_RELATIONS,
    VALID_CONFIDENCE_LEVELS,
    VALID_CLASSIFICATIONS,
)


class Stage31734Inc0ContractTests(unittest.TestCase):
    """Formal unit and contract tests for INC-0 (Data Foundation & Traceability)."""

    def setUp(self):
        self.valid_hash = "6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28"
        self.timestamp = datetime.now(timezone.utc).isoformat()

    def _create_sample_record(
        self,
        applied_contracts: list[str] | None = None,
        include_applied_contracts: bool = True
    ) -> EvidenceTraceabilityRecord:
        fd_kwargs: dict[str, Any] = {
            "classification": "DIRECT",
            "decision_rule_id": "RULE-SC-01-DIRECT",
            "formal_justification": "Critério semântico direto integralmente satisfeito.",
        }
        if include_applied_contracts:
            fd_kwargs["applied_contract_ids"] = applied_contracts if applied_contracts is not None else ["SC-01", "TRACE-01"]

        return EvidenceTraceabilityRecord(
            evaluation_id="EVAL-20261019-001",
            timestamp_utc=self.timestamp,
            runtime_version_hash=self.valid_hash,
            question_profile=QuestionProfile(
                raw_question="Como funciona o particionamento no Apache Kafka?",
                intent_mode="MECHANISM",
                primary_demand=DemandSpecification(
                    demand_id="D-KAFKA-01",
                    description="Mecanismo de particionamento e distribuição de mensagens",
                    is_mandatory=True,
                ),
                secondary_demands=[
                    DemandSpecification(
                        demand_id="D-KAFKA-02",
                        description="Ordenação por offset dentro de cada partição",
                        is_mandatory=False,
                    )
                ],
                target_entities=["Kafka", "particionamento", "offset"],
                context_qualifiers=["mensageria distribuída"],
            ),
            discourse_profile=DiscourseProfile(
                raw_response="O Kafka distribui mensagens em partições baseado na chave e garante a ordem dentro de cada partição por offset.",
                isolated_preambles=["Com certeza"],
                propositions=[
                    DiscourseProposition(
                        prop_id="P1",
                        text="O Kafka distribui mensagens em partições baseado na chave",
                        discourse_role="TECHNICAL_CORE",
                        is_negated=False,
                        is_conditional=False,
                    ),
                    DiscourseProposition(
                        prop_id="P2",
                        text="e garante a ordem dentro de cada partição por offset.",
                        discourse_role="TECHNICAL_CORE",
                        is_negated=False,
                        is_conditional=False,
                    ),
                ],
            ),
            thematic_affinity_evaluation=ThematicAffinityEvaluation(
                entity_overlap_tokens=["kafka", "particionamento", "offset"],
                thematic_presumption_status="CONFIRMED",
                rebuttal_detected=False,
                rebuttal_reason="NONE",
                disjoint_alien_domain_detected=False,
                alien_domain_category="",
            ),
            demand_nexus_evaluations=[
                DemandNexusEvaluation(
                    demand_id="D-KAFKA-01",
                    best_matching_prop_id="P1",
                    nexus_relation="FUNCTIONALLY_SOLVES",
                    semantic_rationale="Explica particionamento baseado em chave",
                    contradiction_detected=False,
                ),
                DemandNexusEvaluation(
                    demand_id="D-KAFKA-02",
                    best_matching_prop_id="P2",
                    nexus_relation="FUNCTIONALLY_SOLVES",
                    semantic_rationale="Explica ordenação por offset",
                    contradiction_detected=False,
                ),
            ],
            coverage_evaluation=CoverageEvaluation(
                coverage_ratio=1.0,
                mandatory_demands_count=1,
                fulfilled_mandatory_demands_count=1,
                unaddressed_demands=[],
            ),
            epistemic_uncertainty=EpistemicUncertaintyRecord(
                confidence_level="HIGH",
                unresolved_ambiguities_present=False,
                epistemic_limitations=[],
            ),
            final_decision=FinalDecisionRecord(**fd_kwargs),
        )

    def test_01_valid_complete_evidence_traceability_record(self):
        """TC-INC0-01: Valid complete record must pass schema validation and serialization."""
        rec = self._create_sample_record(applied_contracts=["SC-01", "SC-02"])
        data = rec.to_dict()
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertTrue(is_valid, f"Validation failed with errors: {errors}")
        self.assertEqual(len(errors), 0)
        self.assertEqual(data["evaluation_id"], "EVAL-20261019-001")
        self.assertEqual(data["final_decision"]["classification"], "DIRECT")
        self.assertEqual(data["final_decision"]["applied_contract_ids"], ["SC-01", "SC-02"])

    def test_02_valid_minimal_evidence_traceability_record(self):
        """TC-INC0-02: Valid minimal record with default/empty optionals must pass validation."""
        rec = EvidenceTraceabilityRecord(
            evaluation_id="EVAL-MINIMAL-01",
            timestamp_utc=self.timestamp,
            runtime_version_hash=self.valid_hash,
            question_profile=QuestionProfile(
                raw_question="O que é idempotência?",
                primary_demand=DemandSpecification(
                    demand_id="D1",
                    description="Definir conceito de idempotência",
                    is_mandatory=True,
                ),
                target_entities=["idempotência"],
            ),
            discourse_profile=DiscourseProfile(
                raw_response="Idempotência significa que múltiplas chamadas idênticas produzem o mesmo efeito que uma única chamada.",
                propositions=[
                    DiscourseProposition(
                        prop_id="P1",
                        text="Idempotência significa que múltiplas chamadas idênticas produzem o mesmo efeito",
                        discourse_role="TECHNICAL_CORE",
                    )
                ],
            ),
            thematic_affinity_evaluation=ThematicAffinityEvaluation(
                entity_overlap_tokens=["idempotencia"],
                thematic_presumption_status="CONFIRMED",
            ),
            demand_nexus_evaluations=[
                DemandNexusEvaluation(
                    demand_id="D1",
                    best_matching_prop_id="P1",
                    nexus_relation="FUNCTIONALLY_SOLVES",
                    semantic_rationale="Define conceito essencial",
                )
            ],
            coverage_evaluation=CoverageEvaluation(
                coverage_ratio=1.0,
                mandatory_demands_count=1,
                fulfilled_mandatory_demands_count=1,
            ),
            epistemic_uncertainty=EpistemicUncertaintyRecord(
                confidence_level="HIGH",
            ),
            final_decision=FinalDecisionRecord(
                classification="DIRECT",
                decision_rule_id="RULE-DEF-01",
                formal_justification="Conceito definido adequadamente.",
            ),
        )
        data = rec.to_dict()
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertTrue(is_valid, f"Validation failed with errors: {errors}")

    def test_03_finding_06_applied_contract_ids_populated(self):
        """TC-INC0-03 (FINDING-06): populated applied_contract_ids is preserved and validated."""
        contracts = ["SC-01", "SC-04", "ADV-02"]
        rec = self._create_sample_record(applied_contracts=contracts)
        data = rec.to_dict()
        self.assertIn("applied_contract_ids", data["final_decision"])
        self.assertEqual(data["final_decision"]["applied_contract_ids"], contracts)
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertTrue(is_valid)

    def test_04_finding_06_applied_contract_ids_empty(self):
        """TC-INC0-04 (FINDING-06): empty applied_contract_ids list validates correctly."""
        rec = self._create_sample_record(applied_contracts=[])
        data = rec.to_dict()
        self.assertNotIn("applied_contract_ids", data["final_decision"])  # omitted when empty or present
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertTrue(is_valid)

    def test_05_finding_06_applied_contract_ids_omitted_backward_compatibility(self):
        """TC-INC0-05 (FINDING-06): Record without applied_contract_ids remains 100% valid."""
        rec = self._create_sample_record(include_applied_contracts=False)
        data = rec.to_dict()
        self.assertNotIn("applied_contract_ids", data["final_decision"])
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertTrue(is_valid)

    def test_06_finding_06_applied_contract_ids_invalid_type(self):
        """TC-INC0-06 (FINDING-06): applied_contract_ids with non-strings must fail validation."""
        rec = self._create_sample_record()
        data = rec.to_dict()
        data["final_decision"]["applied_contract_ids"] = ["SC-01", 12345]  # invalid type
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("applied_contract_ids must contain only strings" in e for e in errors))

    def test_07_negative_missing_top_level_required_properties(self):
        """TC-INC0-07: Missing top-level required properties must fail validation."""
        rec = self._create_sample_record()
        data = rec.to_dict()
        del data["runtime_version_hash"]
        del data["final_decision"]
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("runtime_version_hash" in e for e in errors))
        self.assertTrue(any("final_decision" in e for e in errors))

    def test_08_negative_invalid_runtime_version_hash(self):
        """TC-INC0-08: Non-64 hex or lowercase hash must fail validation."""
        rec = self._create_sample_record()
        data = rec.to_dict()
        data["runtime_version_hash"] = "invalid_hash"
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("runtime_version_hash" in e for e in errors))

        # Test lowercase
        data["runtime_version_hash"] = self.valid_hash.lower()
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("runtime_version_hash" in e for e in errors))

    def test_09_negative_invalid_timestamp_format(self):
        """TC-INC0-09: Invalid ISO timestamp must fail validation."""
        rec = self._create_sample_record()
        data = rec.to_dict()
        data["timestamp_utc"] = "2026/10/19 22:00:00"
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("timestamp_utc" in e for e in errors))

    def test_10_negative_invalid_enum_intent_mode(self):
        """TC-INC0-10: Unknown intent_mode must fail validation."""
        rec = self._create_sample_record()
        data = rec.to_dict()
        data["question_profile"]["intent_mode"] = "FREEFORM_OPINION"
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("intent_mode" in e for e in errors))

    def test_11_negative_invalid_enum_discourse_role(self):
        """TC-INC0-11: Unknown discourse_role must fail validation."""
        rec = self._create_sample_record()
        data = rec.to_dict()
        data["discourse_profile"]["propositions"][0]["discourse_role"] = "GOSSIP"
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("discourse_role" in e for e in errors))

    def test_12_negative_invalid_enum_nexus_relation(self):
        """TC-INC0-12: Unknown nexus_relation must fail validation."""
        rec = self._create_sample_record()
        data = rec.to_dict()
        data["demand_nexus_evaluations"][0]["nexus_relation"] = "MAGICAL_MATCH"
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("nexus_relation" in e for e in errors))

    def test_13_negative_coverage_ratio_out_of_bounds(self):
        """TC-INC0-13: coverage_ratio < 0.0 or > 1.0 must fail validation."""
        rec = self._create_sample_record()
        data = rec.to_dict()
        data["coverage_evaluation"]["coverage_ratio"] = 1.5
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("coverage_ratio" in e for e in errors))

        data["coverage_evaluation"]["coverage_ratio"] = -0.1
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("coverage_ratio" in e for e in errors))

    def test_14_negative_invalid_classification_enum(self):
        """TC-INC0-14: Unknown final classification must fail validation."""
        rec = self._create_sample_record()
        data = rec.to_dict()
        data["final_decision"]["classification"] = "PERFECT_SCORE"
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("classification" in e for e in errors))

    def test_15_lossless_serialization_and_deserialization(self):
        """TC-INC0-15: Lossless JSON roundtrip serialization and structure preservation."""
        rec = self._create_sample_record(applied_contracts=["SC-01", "TRACE-01", "ADV-02"])
        data = rec.to_dict()
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        parsed = json.loads(json_str)
        self.assertEqual(data, parsed)
        is_valid, errors = validate_evidence_traceability_record(parsed)
        self.assertTrue(is_valid, f"Roundtrip json failed schema validation: {errors}")

    def test_16_semantic_classification_invariance(self):
        """TC-INC0-16: Calling semantic relevance logic before and after INC-0 yields identical results."""
        from reference_runtime.runtime import OpenDomainPropositionEngine
        engine = OpenDomainPropositionEngine()
        cases = [
            (
                "Como garantir que um cluster mantenha um unico estado consistente durante particoes de rede?",
                "Os nos utilizam um quorum de maioria e um lider eleito para validar qualquer transicao de estado antes de persistir.",
                "DIRECT"
            ),
            (
                "Como funciona o roteamento de pacotes no protocolo BGP?",
                "Para cuidar de orquideas regamos duas vezes por semana com adubo foliar equilibrado e poda cuidadosa das folhas secas.",
                "OFF_TOPIC"
            ),
            (
                "Como o Kafka particiona as mensagens em um topico?",
                "O Apache Kafka pertence a categoria de solucoes modernas de computacao e foi desenvolvido pela fundacao de software livre com ampla popularidade de mercado.",
                "RELATED"
            ),
            (
                "Como evitar vazamento de memoria em processos concorrentes?",
                "Adicionamos metricas no Prometheus e criamos alertas no Grafana para acompanhar o uso de memoria no dashboard.",
                "SUPPORTING"
            ),
            (
                "Como solucionar problemas de concorrencia em transacoes de banco?",
                "Olha, isso vai depender exclusivamente do orcamento e de muitos fatores de negocio antes de qualquer coisa.",
                "INSUFFICIENT"
            ),
            (
                "Como devemos tratar falhas intermitentes de conexao na replicacao do banco de dados?",
                "A abordagem pode variar conforme a situacao de como a equipe resolver fazer na hora diante da replicacao.",
                "UNKNOWN"
            ),
        ]
        for q, r, expected_cls in cases:
            res = engine.evaluate(q, r)
            self.assertEqual(res["classification"], expected_cls, f"Mismatch for question '{q}': got {res['classification']}, expected {expected_cls}")

    def test_17_robustness_with_empty_propositions_and_unlinked_entities(self):
        """TC-INC0-17: Robust handling of empty propositions and edge case structures."""
        rec = EvidenceTraceabilityRecord(
            evaluation_id="EVAL-EMPTY-PROP-01",
            timestamp_utc=self.timestamp,
            runtime_version_hash=self.valid_hash,
            question_profile=QuestionProfile(
                raw_question="Explique circuit breaker.",
                primary_demand=DemandSpecification(
                    demand_id="D-CB",
                    description="Explicar padrão circuit breaker",
                    is_mandatory=True,
                ),
            ),
            discourse_profile=DiscourseProfile(
                raw_response="",
                propositions=[],
                isolated_preambles=[],
            ),
            thematic_affinity_evaluation=ThematicAffinityEvaluation(
                entity_overlap_tokens=[],
                thematic_presumption_status="NOT_ESTABLISHED",
            ),
            demand_nexus_evaluations=[],
            coverage_evaluation=CoverageEvaluation(
                coverage_ratio=0.0,
                mandatory_demands_count=1,
                fulfilled_mandatory_demands_count=0,
                unaddressed_demands=["D-CB"],
            ),
            epistemic_uncertainty=EpistemicUncertaintyRecord(
                confidence_level="LOW",
                unresolved_ambiguities_present=True,
                epistemic_limitations=["Resposta vazia"],
            ),
            final_decision=FinalDecisionRecord(
                classification="UNKNOWN",
                decision_rule_id="RULE-EMPTY-RESPONSE",
                formal_justification="Resposta vazia sem proposições técnicas.",
            ),
        )
        data = rec.to_dict()
        is_valid, errors = validate_evidence_traceability_record(data)
        self.assertTrue(is_valid, f"Validation failed on empty propositions record: {errors}")


if __name__ == "__main__":
    unittest.main()
