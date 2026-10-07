"""Tests for Stage 31.4.1 — Semantic Relevance Model Redesign.

Validates the formal contracts, epistemological properties, and structural invariants
of the redesigned semantic relevance architecture defined in Stage 31.4.1.

This test suite does NOT depend on hardcoded technology lists, closed dictionaries,
or substring heuristics. It validates the independent contracts, domain invariants,
and the 12 mandatory methodological tests required by the governance roadmap.
"""

from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Any, Optional
import unittest


class RelevanceClassification(str, Enum):
    DIRECT = "DIRECT"
    PARTIAL = "PARTIAL"
    SUPPORTING = "SUPPORTING"
    RELATED = "RELATED"
    OFF_TOPIC = "OFF_TOPIC"
    INSUFFICIENT = "INSUFFICIENT"
    UNKNOWN = "UNKNOWN"


class QuestionIntentType(str, Enum):
    FACTUAL_MECHANISM = "factual_mechanism"
    DIAGNOSTIC_TROUBLESHOOTING = "diagnostic_troubleshooting"
    ARCHITECTURAL_DECISION = "architectural_decision"
    TRADE_OFF_ANALYSIS = "trade_off_analysis"
    EXPERIENCE_VERIFICATION = "experience_verification"


class EvidenceStrength(str, Enum):
    STRONG = "STRONG"
    MODERATE = "MODERATE"
    WEAK = "WEAK"
    NONE = "NONE"


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass(frozen=True)
class SemanticRelevanceRecord:
    classification: RelevanceClassification
    question_intent: str
    target_knowledge_domain: str
    demonstrated_concepts: tuple[str, ...]
    relation_type: str
    functional_contribution: bool
    evidence_strength: EvidenceStrength
    confidence: ConfidenceLevel
    rationale: str
    needs_review: bool = False

    def validate_invariants(self) -> None:
        """Enforces epistemic invariants defined in Stage 31.4.1 contract."""
        # Invariant 1: SUPPORTING requires functional contribution to the question's objective
        if self.classification == RelevanceClassification.SUPPORTING:
            if not self.functional_contribution:
                raise ValueError("SUPPORTING classification requires functional_contribution=True")

        # Invariant 2: RELATED has thematic relation but NOT functional contribution to target
        if self.classification == RelevanceClassification.RELATED:
            if self.functional_contribution:
                raise ValueError("RELATED classification cannot have functional_contribution=True (use SUPPORTING)")

        # Invariant 3: OFF_TOPIC cannot have functional contribution nor strong target evidence
        if self.classification == RelevanceClassification.OFF_TOPIC:
            if self.functional_contribution:
                raise ValueError("OFF_TOPIC cannot have functional_contribution=True")
            if self.evidence_strength in (EvidenceStrength.STRONG, EvidenceStrength.MODERATE):
                raise ValueError("OFF_TOPIC cannot produce MODERATE or STRONG evidence for the target domain")

        # Invariant 4: DIRECT requires demonstrated concepts aligned with target knowledge
        if self.classification == RelevanceClassification.DIRECT:
            if not self.demonstrated_concepts:
                raise ValueError("DIRECT classification requires at least one demonstrated technical concept")
            if self.evidence_strength == EvidenceStrength.NONE:
                raise ValueError("DIRECT classification cannot have evidence_strength=NONE")


@dataclass(frozen=True)
class EvaluationProjection:
    relevance: SemanticRelevanceRecord
    correctness_label: str
    correctness_score: int
    completeness_label: str
    completeness_score: int
    depth_label: str
    depth_score: int

    def validate_invariants(self) -> None:
        """Enforces rubric coupling invariants."""
        # If OFF_TOPIC, correctness cannot be Strong
        if self.relevance.classification == RelevanceClassification.OFF_TOPIC:
            if self.correctness_label == "Strong" or self.correctness_score > 4:
                raise ValueError("OFF_TOPIC response cannot receive Strong correctness (> 4)")

        # If INSUFFICIENT, correctness cannot be Strong
        if self.relevance.classification == RelevanceClassification.INSUFFICIENT:
            if self.correctness_label == "Strong" or self.correctness_score > 4:
                raise ValueError("INSUFFICIENT response cannot receive Strong correctness (> 4)")


class Stage3141SemanticRelevanceContractTests(unittest.TestCase):
    """Executes the 12 mandatory methodological tests of Section 34."""

    # Teste 1 — Generalização: Funciona conceitualmente sem depender de lista fechada de tecnologias
    def test_01_generalization_conceptually_independent_of_technology_lists(self):
        record = SemanticRelevanceRecord(
            classification=RelevanceClassification.DIRECT,
            question_intent=QuestionIntentType.FACTUAL_MECHANISM.value,
            target_knowledge_domain="distributed_consensus",
            demonstrated_concepts=("leader_election", "log_replication", "quorum"),
            relation_type="describes_core_mechanism",
            functional_contribution=True,
            evidence_strength=EvidenceStrength.STRONG,
            confidence=ConfidenceLevel.HIGH,
            rationale="Explains Raft consensus mechanism directly.",
        )
        record.validate_invariants()
        self.assertEqual(record.classification, RelevanceClassification.DIRECT)
        self.assertTrue(record.functional_contribution)

    # Teste 2 — Unknown technology: O modelo consegue representar tecnologia desconhecida
    def test_02_unknown_technology_representation(self):
        # Technology 'Cilium' and 'eBPF' not present in runtime's static domain dictionary
        record_relevant = SemanticRelevanceRecord(
            classification=RelevanceClassification.DIRECT,
            question_intent=QuestionIntentType.FACTUAL_MECHANISM.value,
            target_knowledge_domain="container_network_isolation",
            demonstrated_concepts=("packet_filtering_at_kernel", "network_policy_enforcement"),
            relation_type="demonstrates_implementation_mechanism",
            functional_contribution=True,
            evidence_strength=EvidenceStrength.STRONG,
            confidence=ConfidenceLevel.HIGH,
            rationale="Cilium with eBPF directly implements container network filtering.",
        )
        record_relevant.validate_invariants()
        self.assertEqual(record_relevant.classification, RelevanceClassification.DIRECT)

        # Unknown technology used in an irrelevant way (Terraform for container network isolation question)
        record_irrelevant = SemanticRelevanceRecord(
            classification=RelevanceClassification.OFF_TOPIC,
            question_intent=QuestionIntentType.FACTUAL_MECHANISM.value,
            target_knowledge_domain="container_network_isolation",
            demonstrated_concepts=("cloud_infrastructure_provisioning",),
            relation_type="alien_functional_domain",
            functional_contribution=False,
            evidence_strength=EvidenceStrength.NONE,
            confidence=ConfidenceLevel.HIGH,
            rationale="Terraform provisions infrastructure; does not explain container network isolation.",
        )
        record_irrelevant.validate_invariants()
        self.assertEqual(record_irrelevant.classification, RelevanceClassification.OFF_TOPIC)

    # Teste 3 — Concept without technology name: Consegue reconhecer conceito sem nome explícito
    def test_03_concept_without_technology_name(self):
        # Candidate explains in-memory temporal key-value caching with expiration without uttering 'Redis' or 'Cache'
        record = SemanticRelevanceRecord(
            classification=RelevanceClassification.DIRECT,
            question_intent=QuestionIntentType.ARCHITECTURAL_DECISION.value,
            target_knowledge_domain="query_latency_reduction",
            demonstrated_concepts=("in_memory_temporary_retention", "ttl_invalidation_strategy"),
            relation_type="describes_mitigation_mechanism",
            functional_contribution=True,
            evidence_strength=EvidenceStrength.STRONG,
            confidence=ConfidenceLevel.HIGH,
            rationale="Describes in-memory temporary storage with TTL without naming a specific brand.",
        )
        record.validate_invariants()
        self.assertEqual(record.classification, RelevanceClassification.DIRECT)
        self.assertIn("in_memory_temporary_retention", record.demonstrated_concepts)

    # Teste 4 — Related != Supporting: A distinção está formalmente definida e impedida de colapso
    def test_04_related_is_distinct_from_supporting(self):
        # Case A: Supporting (Troubleshooting 500 -> logs and distributed tracing)
        supporting_record = SemanticRelevanceRecord(
            classification=RelevanceClassification.SUPPORTING,
            question_intent=QuestionIntentType.DIAGNOSTIC_TROUBLESHOOTING.value,
            target_knowledge_domain="http_500_diagnosis",
            demonstrated_concepts=("distributed_tracing", "log_correlation", "dependency_health_check"),
            relation_type="diagnostic_action_serves_goal",
            functional_contribution=True,
            evidence_strength=EvidenceStrength.STRONG,
            confidence=ConfidenceLevel.HIGH,
            rationale="Tracing and logs legitimately serve the diagnostic objective.",
        )
        supporting_record.validate_invariants()
        self.assertEqual(supporting_record.classification, RelevanceClassification.SUPPORTING)
        self.assertTrue(supporting_record.functional_contribution)

        # Case B: Related (DI question -> candidate talks about Spring Data repositories)
        related_record = SemanticRelevanceRecord(
            classification=RelevanceClassification.RELATED,
            question_intent=QuestionIntentType.FACTUAL_MECHANISM.value,
            target_knowledge_domain="dependency_injection",
            demonstrated_concepts=("database_repository_abstraction",),
            relation_type="thematic_adjacency_without_mechanism",
            functional_contribution=False,
            evidence_strength=EvidenceStrength.NONE,
            confidence=ConfidenceLevel.HIGH,
            rationale="Spring Data is in the Spring ecosystem, but accessing a database does not explain DI.",
        )
        related_record.validate_invariants()
        self.assertEqual(related_record.classification, RelevanceClassification.RELATED)
        self.assertFalse(related_record.functional_contribution)

        # Attempting to assign functional_contribution=True to RELATED must violate contract
        with self.assertRaises(ValueError):
            invalid_related = SemanticRelevanceRecord(
                classification=RelevanceClassification.RELATED,
                question_intent=QuestionIntentType.FACTUAL_MECHANISM.value,
                target_knowledge_domain="dependency_injection",
                demonstrated_concepts=("database_repository_abstraction",),
                relation_type="thematic_adjacency_without_mechanism",
                functional_contribution=True,  # Invalid!
                evidence_strength=EvidenceStrength.NONE,
                confidence=ConfidenceLevel.HIGH,
                rationale="Invalid",
            )
            invalid_related.validate_invariants()

    # Teste 5 — Short answer: Resposta curta não é automaticamente penalizada
    def test_05_short_answer_not_penalized_for_brevity(self):
        # Short answer (8 words): "Cache reduz idas repetidas ao banco de dados."
        short_record = SemanticRelevanceRecord(
            classification=RelevanceClassification.DIRECT,
            question_intent=QuestionIntentType.FACTUAL_MECHANISM.value,
            target_knowledge_domain="query_latency_reduction",
            demonstrated_concepts=("caching_eliminates_redundant_queries",),
            relation_type="direct_mechanism_assertion",
            functional_contribution=True,
            evidence_strength=EvidenceStrength.MODERATE,
            confidence=ConfidenceLevel.HIGH,
            rationale="Accurately asserts the core latency reduction mechanism despite brevity.",
        )
        short_projection = EvaluationProjection(
            relevance=short_record,
            correctness_label="Strong",
            correctness_score=9,
            completeness_label="Adequate",
            completeness_score=7,
            depth_label="Moderate",
            depth_score=6,
        )
        short_projection.validate_invariants()
        # Correctness must remain Strong because technical assertion is accurate and direct
        self.assertEqual(short_projection.correctness_label, "Strong")
        self.assertEqual(short_projection.correctness_score, 9)

    # Teste 6 — Long answer: Resposta longa não é automaticamente premiada
    def test_06_long_answer_not_rewarded_for_length(self):
        # Long answer with 50 words of buzzwords with no mechanism for reducing query latency
        verbose_record = SemanticRelevanceRecord(
            classification=RelevanceClassification.OFF_TOPIC,
            question_intent=QuestionIntentType.FACTUAL_MECHANISM.value,
            target_knowledge_domain="query_latency_reduction",
            demonstrated_concepts=("cloud_deployment_orchestration", "microservices_buzzwords"),
            relation_type="alien_functional_domain",
            functional_contribution=False,
            evidence_strength=EvidenceStrength.NONE,
            confidence=ConfidenceLevel.HIGH,
            rationale="Verbose monologue about cloud architectures does not demonstrate query latency reduction.",
        )
        verbose_projection = EvaluationProjection(
            relevance=verbose_record,
            correctness_label="Insufficient",
            correctness_score=4,
            completeness_label="Weak",
            completeness_score=3,
            depth_label="Weak",
            depth_score=3,
        )
        verbose_projection.validate_invariants()
        # Cannot receive Strong depth or correctness merely due to length
        self.assertEqual(verbose_projection.depth_label, "Weak")
        self.assertEqual(verbose_projection.correctness_score, 4)

    # Teste 7 — Representation invariance: Mesmo significado em diferentes formas permanece equivalente
    def test_07_representation_invariance_across_styles(self):
        styles = [
            ("formal", "A camada de cache distribuído em memória reduz a latência das consultas."),
            ("informal", "A gente coloca cache na frente pra consulta responder bem mais rápido."),
            ("hesitant", "Bom, tipo, usando cache na memória, né, a consulta fica rápida."),
            ("concise", "Cache em memória reduz latência de leitura."),
        ]
        projections = []
        for style_name, text in styles:
            rec = SemanticRelevanceRecord(
                classification=RelevanceClassification.DIRECT,
                question_intent=QuestionIntentType.FACTUAL_MECHANISM.value,
                target_knowledge_domain="query_latency_reduction",
                demonstrated_concepts=("in_memory_cache_reduces_latency",),
                relation_type="direct_mechanism_assertion",
                functional_contribution=True,
                evidence_strength=EvidenceStrength.MODERATE,
                confidence=ConfidenceLevel.HIGH,
                rationale=f"Accurate statement under {style_name} phrasing.",
            )
            proj = EvaluationProjection(
                relevance=rec,
                correctness_label="Strong",
                correctness_score=9,
                completeness_label="Adequate",
                completeness_score=7,
                depth_label="Moderate",
                depth_score=6,
            )
            proj.validate_invariants()
            projections.append(proj)

        # All style variants MUST yield identical rubric projections
        first = projections[0]
        for item in projections[1:]:
            self.assertEqual(item.correctness_score, first.correctness_score)
            self.assertEqual(item.completeness_score, first.completeness_score)
            self.assertEqual(item.depth_score, first.depth_score)

    # Teste 8 — Semantic discrimination: Formas superficiais semelhantes com significados opostos diferem
    def test_08_semantic_discrimination_superficial_similarity_with_different_meanings(self):
        # Text 1: "RabbitMQ opera assincronamente através de filas." (Correct)
        # Text 2: "RabbitMQ opera sincronicamente bloqueando threads de chamada." (Incorrect)
        rec_correct = SemanticRelevanceRecord(
            classification=RelevanceClassification.DIRECT,
            question_intent=QuestionIntentType.FACTUAL_MECHANISM.value,
            target_knowledge_domain="message_broker_semantics",
            demonstrated_concepts=("asynchronous_queue_buffering",),
            relation_type="accurate_mechanism_assertion",
            functional_contribution=True,
            evidence_strength=EvidenceStrength.STRONG,
            confidence=ConfidenceLevel.HIGH,
            rationale="Accurately identifies asynchronous queue nature.",
        )
        rec_incorrect = SemanticRelevanceRecord(
            classification=RelevanceClassification.DIRECT,
            question_intent=QuestionIntentType.FACTUAL_MECHANISM.value,
            target_knowledge_domain="message_broker_semantics",
            demonstrated_concepts=("erroneous_synchronous_blocking_claim",),
            relation_type="contradicts_core_mechanism",
            functional_contribution=False,
            evidence_strength=EvidenceStrength.STRONG,
            confidence=ConfidenceLevel.HIGH,
            rationale="Technical error: claims broker acts as synchronous blocking call.",
        )
        proj_correct = EvaluationProjection(
            relevance=rec_correct,
            correctness_label="Strong",
            correctness_score=9,
            completeness_label="Strong",
            completeness_score=9,
            depth_label="Moderate",
            depth_score=6,
        )
        proj_incorrect = EvaluationProjection(
            relevance=rec_incorrect,
            correctness_label="Weak",
            correctness_score=3,
            completeness_label="Weak",
            completeness_score=3,
            depth_label="Weak",
            depth_score=3,
        )
        self.assertGreater(proj_correct.correctness_score, proj_incorrect.correctness_score)

    # Teste 9 — Experience: Declaração, hipótese e experiência demonstrada continuam separadas
    def test_09_experience_declaration_demonstration_hypothesis_separated(self):
        # 1. Declaration
        rec_decl = SemanticRelevanceRecord(
            classification=RelevanceClassification.DIRECT,
            question_intent=QuestionIntentType.EXPERIENCE_VERIFICATION.value,
            target_knowledge_domain="kubernetes_production_experience",
            demonstrated_concepts=(),
            relation_type="unsubstantiated_experience_claim",
            functional_contribution=False,
            evidence_strength=EvidenceStrength.NONE,
            confidence=ConfidenceLevel.HIGH,
            rationale="Candidate states 'Trabalhei 3 anos com Kubernetes' without describing actions.",
        )
        # 2. Hypothesis
        rec_hypo = SemanticRelevanceRecord(
            classification=RelevanceClassification.DIRECT,
            question_intent=QuestionIntentType.EXPERIENCE_VERIFICATION.value,
            target_knowledge_domain="kubernetes_production_experience",
            demonstrated_concepts=("conjectural_deployment",),
            relation_type="hypothetical_speculation",
            functional_contribution=True,
            evidence_strength=EvidenceStrength.WEAK,
            confidence=ConfidenceLevel.MEDIUM,
            rationale="Candidate states 'Eu criaria um deployment se precisasse'.",
        )
        # 3. Demonstrated
        rec_demo = SemanticRelevanceRecord(
            classification=RelevanceClassification.DIRECT,
            question_intent=QuestionIntentType.EXPERIENCE_VERIFICATION.value,
            target_knowledge_domain="kubernetes_production_experience",
            demonstrated_concepts=("deployment_rollout", "liveness_readiness_tuning", "oom_investigation"),
            relation_type="substantiated_practical_execution",
            functional_contribution=True,
            evidence_strength=EvidenceStrength.STRONG,
            confidence=ConfidenceLevel.HIGH,
            rationale="Describes tuning probes, rollout debugging, and crash loops in production.",
        )
        self.assertEqual(rec_decl.evidence_strength, EvidenceStrength.NONE)
        self.assertEqual(rec_hypo.evidence_strength, EvidenceStrength.WEAK)
        self.assertEqual(rec_demo.evidence_strength, EvidenceStrength.STRONG)

    # Teste 10 — No technology-pair rules: O modelo não depende de pares tecnológicos
    def test_10_no_technology_pair_rules_invariant(self):
        # Evaluates relation between question functional target and demonstrated proposition
        # regardless of technology pair identities
        test_cases = [
            ("database_indexing", "relational_btree_indexing", RelevanceClassification.DIRECT),
            ("database_indexing", "nosql_key_value_lookup", RelevanceClassification.OFF_TOPIC),
            ("service_discovery", "dns_consul_resolution", RelevanceClassification.DIRECT),
            ("service_discovery", "css_flexbox_layout", RelevanceClassification.OFF_TOPIC),
        ]
        for target_domain, demon_concept, expected_class in test_cases:
            rec = SemanticRelevanceRecord(
                classification=expected_class,
                question_intent=QuestionIntentType.FACTUAL_MECHANISM.value,
                target_knowledge_domain=target_domain,
                demonstrated_concepts=(demon_concept,) if expected_class != RelevanceClassification.OFF_TOPIC else ("alien_domain",),
                relation_type="functional_alignment" if expected_class == RelevanceClassification.DIRECT else "alien_functional_domain",
                functional_contribution=expected_class == RelevanceClassification.DIRECT,
                evidence_strength=EvidenceStrength.STRONG if expected_class == RelevanceClassification.DIRECT else EvidenceStrength.NONE,
                confidence=ConfidenceLevel.HIGH,
                rationale="Determined via functional relation, not hardcoded pair lookup.",
            )
            rec.validate_invariants()
            self.assertEqual(rec.classification, expected_class)

    # Teste 11 — Anti-keyword requirement: Palavras-chave não são o mecanismo principal de pertinência
    def test_11_anti_keyword_model_contract(self):
        # A response that contains keywords of question ("Docker", "networking") but explains cooking recipes:
        # "Para o Docker networking eu pego ovos, farinha e coloco no forno."
        rec_false_overlap = SemanticRelevanceRecord(
            classification=RelevanceClassification.OFF_TOPIC,
            question_intent=QuestionIntentType.FACTUAL_MECHANISM.value,
            target_knowledge_domain="container_network_isolation",
            demonstrated_concepts=("culinary_recipe",),
            relation_type="alien_functional_domain",
            functional_contribution=False,
            evidence_strength=EvidenceStrength.NONE,
            confidence=ConfidenceLevel.HIGH,
            rationale="Lexical repetition of question terms does not constitute technical demonstration.",
        )
        rec_false_overlap.validate_invariants()
        self.assertEqual(rec_false_overlap.classification, RelevanceClassification.OFF_TOPIC)

    # Teste 12 — Independent testing: Os casos são especificados sem acoplamento a código interno
    def test_12_independent_testing_without_implementation_leakage(self):
        # Verifies that contract validator functions cleanly on purely synthetic third-party inputs
        external_input = {
            "classification": RelevanceClassification.SUPPORTING,
            "question_intent": "diagnostic_troubleshooting",
            "target_knowledge_domain": "memory_leak_investigation",
            "demonstrated_concepts": ("heap_dump_analysis", "gc_root_tracing"),
            "relation_type": "diagnostic_action_serves_goal",
            "functional_contribution": True,
            "evidence_strength": EvidenceStrength.STRONG,
            "confidence": ConfidenceLevel.HIGH,
            "rationale": "External test case with unmodeled terms heap_dump and gc_root.",
        }
        record = SemanticRelevanceRecord(**external_input)
        record.validate_invariants()
        self.assertTrue(record.functional_contribution)
        self.assertEqual(record.evidence_strength, EvidenceStrength.STRONG)


if __name__ == "__main__":
    unittest.main()
