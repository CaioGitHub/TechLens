from __future__ import annotations
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

# Allowed enum sets per Schema Draft-07
VALID_INTENT_MODES = {
    "DEFINITION", "CONCEPTUAL_EXPLANATION", "MECHANISM", "COMPARISON",
    "HISTORICAL", "CAUSALITY", "DIAGNOSIS", "IMPLEMENTATION",
    "PROBLEM_SOLUTION", "DECISION_JUSTIFICATION", "TRADE_OFF_ANALYSIS"
}

VALID_DISCOURSE_ROLES = {
    "TECHNICAL_CORE", "CONVERSATIONAL_PREAMBLE", "ANALOGY_VEHICLE",
    "ANALOGY_GROUNDING", "HISTORICAL_METADATA", "OBSERVABILITY_SUPPORT",
    "EMPTY_FILLER", "IGNORANCE_DECLARATION", "RETRACTED_ASSERTION"
}

VALID_THEMATIC_STATUSES = {
    "CONFIRMED", "REBUTTED", "NOT_ESTABLISHED", "EQUIVALENCE_ESTABLISHED"
}

VALID_REBUTTAL_REASONS = {
    "NONE", "ALIEN_PREDICATE_HOMONYMY", "METAPHORICAL_DETOUR", "DESTRUCTIVE_ANTITHESIS"
}

VALID_NEXUS_RELATIONS = {
    "FUNCTIONALLY_SOLVES", "PARTIALLY_SOLVES", "CONTRIBUTES_TO",
    "THEMATICALLY_ADJACENT", "NON_OPERATIVE", "EVASIVE", "IGNORANCE",
    "DOMAIN_DISJUNCT", "UNRESOLVED_AMBIGUITY"
}

VALID_CONFIDENCE_LEVELS = {"HIGH", "MEDIUM", "LOW"}

VALID_CLASSIFICATIONS = {
    "DIRECT", "PARTIAL", "SUPPORTING", "RELATED",
    "OFF_TOPIC", "INSUFFICIENT", "UNKNOWN"
}

HASH_PATTERN = re.compile(r"^[A-F0-9]{64}$")
ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")


@dataclass
class DemandSpecification:
    demand_id: str
    description: str
    is_mandatory: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "demand_id": self.demand_id,
            "description": self.description,
            "is_mandatory": self.is_mandatory,
        }


@dataclass
class QuestionProfile:
    raw_question: str
    primary_demand: DemandSpecification
    intent_mode: str = "CONCEPTUAL_EXPLANATION"
    secondary_demands: list[DemandSpecification] = field(default_factory=list)
    target_entities: list[str] = field(default_factory=list)
    context_qualifiers: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw_question": self.raw_question,
            "intent_mode": self.intent_mode,
            "primary_demand": self.primary_demand.to_dict() if hasattr(self.primary_demand, "to_dict") else self.primary_demand,
            "secondary_demands": [d.to_dict() if hasattr(d, "to_dict") else d for d in self.secondary_demands],
            "target_entities": list(self.target_entities),
            "context_qualifiers": list(self.context_qualifiers),
        }


@dataclass
class DiscourseProposition:
    prop_id: str
    text: str
    discourse_role: str = "TECHNICAL_CORE"
    is_negated: bool = False
    negation_scope: str = ""
    is_conditional: bool = False
    condition_premise: str = ""

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "prop_id": self.prop_id,
            "text": self.text,
            "discourse_role": self.discourse_role,
            "is_negated": self.is_negated,
            "is_conditional": self.is_conditional,
        }
        if self.negation_scope:
            d["negation_scope"] = self.negation_scope
        if self.condition_premise:
            d["condition_premise"] = self.condition_premise
        return d


@dataclass
class DiscourseProfile:
    raw_response: str
    propositions: list[DiscourseProposition] = field(default_factory=list)
    isolated_preambles: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw_response": self.raw_response,
            "isolated_preambles": list(self.isolated_preambles),
            "propositions": [p.to_dict() if hasattr(p, "to_dict") else p for p in self.propositions],
        }


@dataclass
class ThematicAffinityEvaluation:
    entity_overlap_tokens: list[str] = field(default_factory=list)
    thematic_presumption_status: str = "NOT_ESTABLISHED"
    rebuttal_detected: bool = False
    rebuttal_reason: str = "NONE"
    disjoint_alien_domain_detected: bool = False
    alien_domain_category: str = ""

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "entity_overlap_tokens": list(self.entity_overlap_tokens),
            "thematic_presumption_status": self.thematic_presumption_status,
            "rebuttal_detected": self.rebuttal_detected,
            "disjoint_alien_domain_detected": self.disjoint_alien_domain_detected,
        }
        if self.rebuttal_reason:
            d["rebuttal_reason"] = self.rebuttal_reason
        if self.alien_domain_category:
            d["alien_domain_category"] = self.alien_domain_category
        return d

ThematicEvaluation = ThematicAffinityEvaluation


@dataclass
class EquivalenceEvaluation:
    equivalence_mode: str = "NONE"
    established_equivalences: list[dict[str, str]] = field(default_factory=list)
    property_clash: bool = False
    rationale: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "equivalence_mode": self.equivalence_mode,
            "established_equivalences": list(self.established_equivalences),
            "property_clash": self.property_clash,
            "rationale": self.rationale,
        }


@dataclass
class AnalogyEvaluation:
    is_grounded: bool = False
    vehicle_domain: str = ""
    target_mechanisms_resolved: list[str] = field(default_factory=list)
    unanchored_metaphor: bool = False
    rationale: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_grounded": self.is_grounded,
            "vehicle_domain": self.vehicle_domain,
            "target_mechanisms_resolved": list(self.target_mechanisms_resolved),
            "unanchored_metaphor": self.unanchored_metaphor,
            "rationale": self.rationale,
        }


@dataclass
class DemandNexusEvaluation:
    demand_id: str
    best_matching_prop_id: str
    nexus_relation: str = "THEMATICALLY_ADJACENT"
    semantic_rationale: str = ""
    contradiction_detected: bool = False
    contradiction_details: str = ""

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "demand_id": self.demand_id,
            "best_matching_prop_id": self.best_matching_prop_id,
            "nexus_relation": self.nexus_relation,
            "semantic_rationale": self.semantic_rationale,
        }
        if self.contradiction_detected:
            d["contradiction_detected"] = self.contradiction_detected
        if self.contradiction_details:
            d["contradiction_details"] = self.contradiction_details
        return d

DemandNexusMatrix = list[DemandNexusEvaluation]


@dataclass
class CoverageEvaluation:
    coverage_ratio: float = 0.0
    mandatory_demands_count: int = 1
    fulfilled_mandatory_demands_count: int = 0
    unaddressed_demands: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "coverage_ratio": float(self.coverage_ratio),
            "mandatory_demands_count": int(self.mandatory_demands_count),
            "fulfilled_mandatory_demands_count": int(self.fulfilled_mandatory_demands_count),
            "unaddressed_demands": list(self.unaddressed_demands),
        }


@dataclass
class EpistemicUncertaintyRecord:
    confidence_level: str = "HIGH"
    unresolved_ambiguities_present: bool = False
    epistemic_limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "confidence_level": self.confidence_level,
            "unresolved_ambiguities_present": self.unresolved_ambiguities_present,
            "epistemic_limitations": list(self.epistemic_limitations),
        }


@dataclass
class FinalDecisionRecord:
    classification: str = "UNKNOWN"
    decision_rule_id: str = "RULE-INIT"
    formal_justification: str = ""
    applied_contract_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "classification": self.classification,
            "decision_rule_id": self.decision_rule_id,
            "formal_justification": self.formal_justification,
        }
        if self.applied_contract_ids:
            d["applied_contract_ids"] = list(self.applied_contract_ids)
        return d


@dataclass
class EvidenceTraceabilityRecord:
    evaluation_id: str
    timestamp_utc: str
    runtime_version_hash: str
    question_profile: QuestionProfile
    discourse_profile: DiscourseProfile
    thematic_affinity_evaluation: ThematicAffinityEvaluation
    demand_nexus_evaluations: list[DemandNexusEvaluation]
    coverage_evaluation: CoverageEvaluation
    epistemic_uncertainty: EpistemicUncertaintyRecord
    final_decision: FinalDecisionRecord

    def to_dict(self) -> dict[str, Any]:
        return {
            "evaluation_id": self.evaluation_id,
            "timestamp_utc": self.timestamp_utc,
            "runtime_version_hash": self.runtime_version_hash,
            "question_profile": self.question_profile.to_dict(),
            "discourse_profile": self.discourse_profile.to_dict(),
            "thematic_affinity_evaluation": self.thematic_affinity_evaluation.to_dict(),
            "demand_nexus_evaluations": [n.to_dict() for n in self.demand_nexus_evaluations],
            "coverage_evaluation": self.coverage_evaluation.to_dict(),
            "epistemic_uncertainty": self.epistemic_uncertainty.to_dict(),
            "final_decision": self.final_decision.to_dict(),
        }


def validate_evidence_traceability_record(data: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate a dictionary against the Draft-07 EvidenceTraceabilityRecord schema."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return False, ["Root must be an object/dict"]

    top_required = [
        "evaluation_id", "timestamp_utc", "runtime_version_hash",
        "question_profile", "discourse_profile", "thematic_affinity_evaluation",
        "demand_nexus_evaluations", "coverage_evaluation", "epistemic_uncertainty",
        "final_decision"
    ]
    for r in top_required:
        if r not in data:
            errors.append(f"Missing required top-level property: '{r}'")

    if errors:
        return False, errors

    # Check evaluation_id
    if not isinstance(data["evaluation_id"], str) or not data["evaluation_id"].strip():
        errors.append("evaluation_id must be a non-empty string")

    # Check timestamp_utc
    ts = data.get("timestamp_utc", "")
    if not isinstance(ts, str) or not ISO_DATE_PATTERN.match(ts):
        errors.append(f"timestamp_utc '{ts}' is not a valid ISO date-time string")

    # Check runtime_version_hash
    rvh = data.get("runtime_version_hash", "")
    if not isinstance(rvh, str) or not HASH_PATTERN.match(rvh):
        errors.append(f"runtime_version_hash '{rvh}' must be a 64-char uppercase hex string")

    # Check question_profile
    qp = data.get("question_profile")
    if not isinstance(qp, dict):
        errors.append("question_profile must be an object")
    else:
        for f in ["raw_question", "intent_mode", "primary_demand", "target_entities"]:
            if f not in qp:
                errors.append(f"question_profile missing '{f}'")
        if qp.get("intent_mode") not in VALID_INTENT_MODES:
            errors.append(f"question_profile.intent_mode '{qp.get('intent_mode')}' not in {VALID_INTENT_MODES}")
        pd = qp.get("primary_demand")
        if not isinstance(pd, dict):
            errors.append("question_profile.primary_demand must be an object")
        else:
            for f in ["demand_id", "description", "is_mandatory"]:
                if f not in pd:
                    errors.append(f"primary_demand missing '{f}'")
            if not isinstance(pd.get("is_mandatory"), bool):
                errors.append("primary_demand.is_mandatory must be a boolean")

    # Check discourse_profile
    dp = data.get("discourse_profile")
    if not isinstance(dp, dict):
        errors.append("discourse_profile must be an object")
    else:
        for f in ["raw_response", "propositions", "isolated_preambles"]:
            if f not in dp:
                errors.append(f"discourse_profile missing '{f}'")
        if not isinstance(dp.get("propositions"), list):
            errors.append("discourse_profile.propositions must be an array")
        else:
            for i, p in enumerate(dp["propositions"]):
                if not isinstance(p, dict):
                    errors.append(f"discourse_profile.propositions[{i}] must be an object")
                    continue
                for f in ["prop_id", "text", "discourse_role", "is_negated", "is_conditional"]:
                    if f not in p:
                        errors.append(f"discourse_profile.propositions[{i}] missing '{f}'")
                if p.get("discourse_role") not in VALID_DISCOURSE_ROLES:
                    errors.append(f"propositions[{i}].discourse_role '{p.get('discourse_role')}' invalid")

    # Check thematic_affinity_evaluation
    ta = data.get("thematic_affinity_evaluation")
    if not isinstance(ta, dict):
        errors.append("thematic_affinity_evaluation must be an object")
    else:
        for f in ["entity_overlap_tokens", "thematic_presumption_status", "rebuttal_detected", "disjoint_alien_domain_detected"]:
            if f not in ta:
                errors.append(f"thematic_affinity_evaluation missing '{f}'")
        if ta.get("thematic_presumption_status") not in VALID_THEMATIC_STATUSES:
            errors.append(f"thematic_presumption_status '{ta.get('thematic_presumption_status')}' invalid")
        if "rebuttal_reason" in ta and ta["rebuttal_reason"] not in VALID_REBUTTAL_REASONS:
            errors.append(f"rebuttal_reason '{ta.get('rebuttal_reason')}' invalid")

    # Check demand_nexus_evaluations
    dne = data.get("demand_nexus_evaluations")
    if not isinstance(dne, list):
        errors.append("demand_nexus_evaluations must be an array")
    else:
        for i, n in enumerate(dne):
            if not isinstance(n, dict):
                errors.append(f"demand_nexus_evaluations[{i}] must be an object")
                continue
            for f in ["demand_id", "best_matching_prop_id", "nexus_relation", "semantic_rationale"]:
                if f not in n:
                    errors.append(f"demand_nexus_evaluations[{i}] missing '{f}'")
            if n.get("nexus_relation") not in VALID_NEXUS_RELATIONS:
                errors.append(f"demand_nexus_evaluations[{i}].nexus_relation '{n.get('nexus_relation')}' invalid")

    # Check coverage_evaluation
    ce = data.get("coverage_evaluation")
    if not isinstance(ce, dict):
        errors.append("coverage_evaluation must be an object")
    else:
        for f in ["coverage_ratio", "mandatory_demands_count", "fulfilled_mandatory_demands_count"]:
            if f not in ce:
                errors.append(f"coverage_evaluation missing '{f}'")
        cr = ce.get("coverage_ratio")
        if not isinstance(cr, (int, float)) or cr < 0.0 or cr > 1.0:
            errors.append(f"coverage_evaluation.coverage_ratio '{cr}' must be between 0.0 and 1.0")

    # Check epistemic_uncertainty
    eu = data.get("epistemic_uncertainty")
    if not isinstance(eu, dict):
        errors.append("epistemic_uncertainty must be an object")
    else:
        for f in ["confidence_level", "unresolved_ambiguities_present", "epistemic_limitations"]:
            if f not in eu:
                errors.append(f"epistemic_uncertainty missing '{f}'")
        if eu.get("confidence_level") not in VALID_CONFIDENCE_LEVELS:
            errors.append(f"confidence_level '{eu.get('confidence_level')}' invalid")

    # Check final_decision
    fd = data.get("final_decision")
    if not isinstance(fd, dict):
        errors.append("final_decision must be an object")
    else:
        for f in ["classification", "decision_rule_id", "formal_justification"]:
            if f not in fd:
                errors.append(f"final_decision missing '{f}'")
        if fd.get("classification") not in VALID_CLASSIFICATIONS:
            errors.append(f"final_decision.classification '{fd.get('classification')}' invalid")
        if "applied_contract_ids" in fd:
            if not isinstance(fd["applied_contract_ids"], list):
                errors.append("final_decision.applied_contract_ids must be an array of strings")
            elif not all(isinstance(cid, str) for cid in fd["applied_contract_ids"]):
                errors.append("final_decision.applied_contract_ids must contain only strings")

    return (len(errors) == 0, errors)


if __name__ == "__main__":
    # Test valid record creation
    rec = EvidenceTraceabilityRecord(
        evaluation_id="EVAL-20261019-001",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        runtime_version_hash="6C44B7A8FBDABC1CBB111666DD543489FBC152B19A27AA3FF8B67B82B0CA4F28",
        question_profile=QuestionProfile(
            raw_question="Como o Kafka garante a ordem das mensagens?",
            intent_mode="MECHANISM",
            primary_demand=DemandSpecification(
                demand_id="D1",
                description="Explicar o mecanismo de garantia de ordem por partição",
                is_mandatory=True
            ),
            target_entities=["Kafka", "ordem", "partições"]
        ),
        discourse_profile=DiscourseProfile(
            raw_response="O Kafka garante a ordem estritamente dentro da mesma partição por meio de offsets sequenciais.",
            propositions=[
                DiscourseProposition(
                    prop_id="P1",
                    text="O Kafka garante a ordem estritamente dentro da mesma partição por meio de offsets sequenciais.",
                    discourse_role="TECHNICAL_CORE",
                    is_negated=False,
                    is_conditional=False
                )
            ]
        ),
        thematic_affinity_evaluation=ThematicAffinityEvaluation(
            entity_overlap_tokens=["kafka", "ordem", "particao"],
            thematic_presumption_status="CONFIRMED",
            rebuttal_detected=False,
            rebuttal_reason="NONE",
            disjoint_alien_domain_detected=False
        ),
        demand_nexus_evaluations=[
            DemandNexusEvaluation(
                demand_id="D1",
                best_matching_prop_id="P1",
                nexus_relation="FUNCTIONALLY_SOLVES",
                semantic_rationale="Explica offsets sequenciais por partição"
            )
        ],
        coverage_evaluation=CoverageEvaluation(
            coverage_ratio=1.0,
            mandatory_demands_count=1,
            fulfilled_mandatory_demands_count=1,
            unaddressed_demands=[]
        ),
        epistemic_uncertainty=EpistemicUncertaintyRecord(
            confidence_level="HIGH",
            unresolved_ambiguities_present=False,
            epistemic_limitations=[]
        ),
        final_decision=FinalDecisionRecord(
            classification="DIRECT",
            decision_rule_id="RULE-FULL-DIRECT",
            formal_justification="Todas as demandas obrigatórias foram resolvidas funcionalmente sem disjunção alienígena.",
            applied_contract_ids=["SC-01", "SC-02"]
        )
    )

    d = rec.to_dict()
    valid, errors = validate_evidence_traceability_record(d)
    print("Valid record test:", valid, errors)
    assert valid, f"Expected valid, got: {errors}"

    # Test invalid record (missing required property and invalid enum)
    bad_dict = json.loads(json.dumps(d))
    del bad_dict["final_decision"]["classification"]
    bad_dict["question_profile"]["intent_mode"] = "INVALID_MODE"
    valid_bad, errors_bad = validate_evidence_traceability_record(bad_dict)
    print("Invalid record test caught errors correctly:", not valid_bad, len(errors_bad), errors_bad)
    assert not valid_bad and len(errors_bad) >= 2
    print("All prototype tests passed successfully!")
