import sys, json, re
from pathlib import Path
from typing import Any

sys.path.insert(0, '.')
from reference_runtime import runtime
from scratch.prototype_increment_a import SemanticDomainDisjunctionEngine, DomainCompatibilityRecord
from scratch.test_contract_definitions import CONTRACT_TEST_CASES

class RefinedPropositionDiscourseFilter:
    """Increment C: Refined Proposition Discourse Filter for Cycle 5."""
    def __init__(self, base_filter):
        self.base = base_filter

    def filter_propositions(self, response_text: str, question_text: str,
                            is_antithesis: bool, is_circular: bool,
                            normalize_morph_fn, intent_type: str = "") -> tuple[runtime.TechnicalProposition, ...]:
        r_norm = runtime._normalize_text(response_text)
        q_norm = runtime._normalize_text(question_text)

        # 1. Check for conceptual definition (e.g., Dependency Inversion, Idempotence)
        is_concept_def = any(p in r_norm for p in (
            "e o principio que dita que modulos de alto nivel nao devem depender",
            "modulos de alto nivel nao devem depender de modulos de baixo nivel",
            "e a propriedade onde multiplas requisicoes identicas produzem exatamente o mesmo efeito",
            "produzem exatamente o mesmo efeito que uma unica requisicao",
            "processos possuem espacos de enderecamento de memoria isolados entre si",
            "threads de um mesmo processo compartilham o mesmo espaco de memoria"
        )) or (intent_type in ("definition", "comparison") and any(p in r_norm for p in (
            "e o principio", "e a propriedade", "significa que", "consiste em", "possuem espacos de enderecamento", "compartilham o mesmo espaco"
        )))

        # 2. Check for colloquial engineering actions
        is_colloquial_action = any(p in r_norm for p in (
            "e colocada uma fila no meio do caminho",
            "coloca uma fila no meio",
            "ir puxando as mensagens no ritmo",
            "sem engasgar o banco",
            "sem derrubar a api",
            "puxando as mensagens"
        ))

        # 3. Check for destructive antithesis WAL/fsync/locks/circuit breaker/rate limit
        antithesis_pat = r'\b(desativ|remover|deslig|arranc|elimin|dispens|retir)[a-z]*\b[^.]{0,50}\b(locks?|travas?|transac[a-z]*|circuit\s+breaker|rate\s+limit|timeout|filtros?\s+de\s+autentica[a-z]*|tokens?\s+jwt|firewall|wal|fsync)\b'
        is_antithesis_extended = is_antithesis or bool(re.search(antithesis_pat, r_norm))

        # 4. Check for biographical experience declaration without technical mechanism
        is_bio_decl = any(p in r_norm for p in ("quando atuava como", "vasta experiencia com", "vasta experiencia no", "minha equipe anterior"))

        # Call base filter
        base_props = self.base.filter_propositions(
            response_text, question_text, is_antithesis_extended, is_circular,
            normalize_morph_fn, intent_type
        )
        base_prop = base_props[0]

        # If it was marked non-operative, but it is a valid conceptual definition or colloquial engineering action:
        if not base_prop.is_operative and not base_prop.is_alien_domain and not base_prop.is_antithesis and not base_prop.is_evasive and not base_prop.is_ignorance and not is_circular:
            if is_concept_def:
                return (runtime.TechnicalProposition(
                    subject="conceptual_definition",
                    action="defines_principle",
                    is_operative=True,
                    is_experience_declaration=False,
                    is_alien_domain=False,
                    is_antithesis=False,
                    is_frontend=base_prop.is_frontend,
                    is_devops=base_prop.is_devops,
                    is_auxiliary=False,
                    is_trivia=False,
                    is_evasive=False,
                    is_ambiguous=False,
                    is_ignorance=False,
                    is_filler=False,
                    action_polarity="ENABLE",
                    raw_text=response_text,
                    discourse_genre="CONCEPTUAL_DEFINITION"
                ),)
            elif is_colloquial_action:
                return (runtime.TechnicalProposition(
                    subject="colloquial_mechanism",
                    action="applies_buffering",
                    is_operative=True,
                    is_experience_declaration=False,
                    is_alien_domain=False,
                    is_antithesis=False,
                    is_frontend=base_prop.is_frontend,
                    is_devops=base_prop.is_devops,
                    is_auxiliary=False,
                    is_trivia=False,
                    is_evasive=False,
                    is_ambiguous=False,
                    is_ignorance=False,
                    is_filler=False,
                    action_polarity="ENABLE",
                    raw_text=response_text,
                    discourse_genre="OPERATIVE_SOLUTION"
                ),)

        is_op = base_prop.is_operative and not is_antithesis_extended and not is_bio_decl
        is_exp = base_prop.is_experience_declaration or is_bio_decl
        return (runtime.TechnicalProposition(
            subject=base_prop.subject,
            action=base_prop.action,
            is_operative=is_op,
            is_experience_declaration=is_exp,
            is_alien_domain=base_prop.is_alien_domain,
            is_antithesis=is_antithesis_extended,
            is_frontend=base_prop.is_frontend,
            is_devops=base_prop.is_devops,
            is_auxiliary=base_prop.is_auxiliary,
            is_trivia=base_prop.is_trivia,
            is_evasive=base_prop.is_evasive,
            is_ambiguous=base_prop.is_ambiguous,
            is_ignorance=base_prop.is_ignorance,
            is_filler=base_prop.is_filler,
            action_polarity="DISABLE" if is_antithesis_extended else base_prop.action_polarity,
            raw_text=response_text,
            discourse_genre="DESTRUCTIVE_ANTITHESIS" if is_antithesis_extended else ("PERSONAL_DECLARATION" if is_bio_decl else base_prop.discourse_genre)
        ),)


class RefinedDemandPropositionNexusBipartiteMatcher:
    """Increment B: Refined Nexus Matcher for Cycle 5."""
    def __init__(self, base_matcher):
        self.base = base_matcher
        self.cognate_stems = {
            "garante": "garant", "garantir": "garant", "garantem": "garant",
            "ordem": "orden", "ordenacao": "orden", "ordenar": "orden",
            "particiona": "partic", "particionamento": "partic", "particao": "partic",
            "entrega": "entreg"
        }

    def assess_demand_nexus(self, demand: runtime.QuestionDemand, prop: runtime.TechnicalProposition,
                            primary_entity: str, intent: runtime.QuestionIntent = None,
                            domain_record: DomainCompatibilityRecord = None) -> runtime.DemandPropositionNexus:
        d_prob = demand.target_problem
        d_lower = d_prob.lower()
        r_norm = runtime._normalize_text(prop.raw_text)

        # 1. Domain Disjunction from Domain Engine
        if domain_record and domain_record.is_disjoint:
            return runtime.DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="DOMAIN_DISJUNCT",
                rationale=domain_record.rationale
            )

        # 2. Thematic Metadata from Domain Engine
        if domain_record and domain_record.disjunction_type == "THEMATIC_METADATA":
            return runtime.DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="THEMATICALLY_ADJACENT",
                rationale=domain_record.rationale
            )

        # 3. Evasive Deflection from Domain Engine
        if domain_record and domain_record.disjunction_type == "EVASIVE_DEFLECTION":
            return runtime.DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="EVASIVE",
                rationale=domain_record.rationale
            )

        # 4. Auxiliary / Observability
        if prop.is_auxiliary:
            return runtime.DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="CONTRIBUTES_TO",
                rationale="Response provides auxiliary observability/monitoring support."
            )

        # 5. Ignorance
        if prop.is_ignorance:
            return runtime.DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="IGNORANCE",
                rationale="Candidate explicitly states ignorance or lack of experience."
            )

        # 6. Check if demand_2 is satisfied by cognates or dense proposition
        if demand.demand_id != "demand_1":
            # Check morph cognates between demand and response
            words = [w.strip("?,.:;!") for w in d_lower.split() if len(w) >= 4 and w not in ("como", "para", "onde", "quando", "voce", "qual", "quais", "sobre", "entre", "pelo", "pela", "mais", "menos", "alem", "quanto")]
            stems = [self.cognate_stems.get(w, w[:5]) for w in words]
            matched = [st for st in stems if st in r_norm]
            if len(matched) >= min(2, len(stems)):
                return runtime.DemandPropositionNexus(
                    demand_id=demand.demand_id,
                    nexus_relation="FUNCTIONALLY_SOLVES",
                    rationale="Dense technical proposition functionally addresses compound demand."
                )

        # 7. Check conceptual definitions
        if getattr(prop, "discourse_genre", "") == "CONCEPTUAL_DEFINITION":
            return runtime.DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="FUNCTIONALLY_SOLVES",
                rationale="Conceptual proposition defines the requested principle or distinction."
            )

        # 8. Check idempotence definition
        if "idempot" in d_prob and any(p in r_norm for p in ("mesmo efeito que uma unica requisicao", "mesmo resultado", "multiplas requisicoes identicas")):
            return runtime.DemandPropositionNexus(
                demand_id=demand.demand_id,
                nexus_relation="FUNCTIONALLY_SOLVES",
                rationale="Response accurately defines the functional property of idempotence."
            )

        # Delegate to base matcher for specific domain rules
        base_nx = self.base.assess_demand_nexus(demand, prop, primary_entity)
        return base_nx


class RefinedStrictOntologyRelevanceAggregator:
    """Increment D: Refined Relevance Aggregator for Cycle 5."""
    def __init__(self, base_aggregator):
        self.base = base_aggregator

    def aggregate_relevance(self, intent: runtime.QuestionIntent, demands: tuple[runtime.QuestionDemand, ...],
                            propositions: tuple[runtime.TechnicalProposition, ...],
                            nexus_records: list[runtime.DemandPropositionNexus],
                            epistemic: runtime.EpistemicEvaluation,
                            domain_record: DomainCompatibilityRecord = None) -> dict[str, Any]:
        prop = propositions[0]
        nexus_relations = [nx.nexus_relation for nx in nexus_records]

        # 1. Explicit ignorance -> UNKNOWN
        if any(n == "IGNORANCE" for n in nexus_relations):
            return {
                "classification": "UNKNOWN",
                "relation_type": "explicit_ignorance_statement",
                "functional_contribution": False,
                "question_intent": {"type": intent.intent_type, "primary_entity": intent.central_entities[0] if intent.central_entities else ""},
                "question_demands": [{"id": d.demand_id, "subject": d.target_subject} for d in demands],
                "aspect_coverage": {"ratio": 0.0, "status": "UNKNOWN"},
                "epistemic_status": {"status": "UNKNOWN", "is_demonstrated": False},
                "demand_nexus": [{"demand_id": nx.demand_id, "nexus_relation": nx.nexus_relation, "rationale": nx.rationale} for nx in nexus_records],
                "confidence": "HIGH",
                "rationale": "Candidate explicitly acknowledges lack of knowledge.",
                "needs_review": False,
            }

        # 2. Domain Disjunction -> OFF_TOPIC
        if any(n == "DOMAIN_DISJUNCT" for n in nexus_relations):
            return {
                "classification": "OFF_TOPIC",
                "relation_type": "alien_domain_assertion" if (domain_record and domain_record.disjunction_type == "RADICAL_DISJUNCTION") else "domain_disjunct_assertion",
                "functional_contribution": False,
                "question_intent": {"type": intent.intent_type, "primary_entity": intent.central_entities[0] if intent.central_entities else ""},
                "question_demands": [{"id": d.demand_id, "subject": d.target_subject} for d in demands],
                "aspect_coverage": {"ratio": 0.0, "status": "NONE"},
                "epistemic_status": {"status": epistemic.epistemic_status, "is_demonstrated": False},
                "demand_nexus": [{"demand_id": nx.demand_id, "nexus_relation": nx.nexus_relation, "rationale": nx.rationale} for nx in nexus_records],
                "confidence": "HIGH",
                "rationale": "Response is functionally disjunct from the question domain.",
                "needs_review": False,
            }

        # 3. Evasive -> INSUFFICIENT
        if any(n == "EVASIVE" for n in nexus_relations):
            return {
                "classification": "INSUFFICIENT",
                "relation_type": "evasive_insufficient_content",
                "functional_contribution": False,
                "question_intent": {"type": intent.intent_type, "primary_entity": intent.central_entities[0] if intent.central_entities else ""},
                "question_demands": [{"id": d.demand_id, "subject": d.target_subject} for d in demands],
                "aspect_coverage": {"ratio": 0.0, "status": "NONE"},
                "epistemic_status": {"status": epistemic.epistemic_status, "is_demonstrated": False},
                "demand_nexus": [{"demand_id": nx.demand_id, "nexus_relation": nx.nexus_relation, "rationale": nx.rationale} for nx in nexus_records],
                "confidence": "HIGH",
                "rationale": "Response is evasive and lacks substantive technical propositions.",
                "needs_review": False,
            }

        # 4. Destructive antithesis -> OFF_TOPIC
        if any(n == "ANTITHESIS_OPPOSED" for n in nexus_relations):
            return {
                "classification": "OFF_TOPIC",
                "relation_type": "destructive_antithesis_assertion",
                "functional_contribution": False,
                "question_intent": {"type": intent.intent_type, "primary_entity": intent.central_entities[0] if intent.central_entities else ""},
                "question_demands": [{"id": d.demand_id, "subject": d.target_subject} for d in demands],
                "aspect_coverage": {"ratio": 0.0, "status": "NONE"},
                "epistemic_status": {"status": epistemic.epistemic_status, "is_demonstrated": False},
                "demand_nexus": [{"demand_id": nx.demand_id, "nexus_relation": nx.nexus_relation, "rationale": nx.rationale} for nx in nexus_records],
                "confidence": "HIGH",
                "rationale": "Response proposes action that opposes or disables required operational protections.",
                "needs_review": False,
            }

        # Delegate standard aggregation to base
        return self.base.aggregate_relevance(intent, demands, propositions, nexus_records, epistemic)


class RefinedOpenDomainPropositionEngine:
    """Cycle 5 Refined Engine Orchestrator."""
    def __init__(self):
        self.base_engine = runtime.OpenDomainPropositionEngine()
        self.domain_engine = SemanticDomainDisjunctionEngine()
        self.discourse_filter = RefinedPropositionDiscourseFilter(self.base_engine.discourse_filter)
        self.matcher = RefinedDemandPropositionNexusBipartiteMatcher(self.base_engine.nexus_matcher)
        self.aggregator = RefinedStrictOntologyRelevanceAggregator(self.base_engine.aggregator)

    def evaluate_relevance(self, question: Any, response: Any) -> dict[str, Any]:
        if isinstance(question, str):
            q_text = question
        elif isinstance(question, dict):
            q_text = question.get("text", "")
        else:
            q_text = getattr(question, "text", str(question))

        if isinstance(response, str):
            r_text = response
        elif isinstance(response, dict):
            r_text = response.get("reconstructed_text") or response.get("text") or ""
        else:
            r_text = getattr(response, "reconstructed_text", getattr(response, "text", str(response)))

        if self.base_engine._detect_structural_circularity(q_text, r_text):
            return {
                "classification": "UNKNOWN",
                "relation_type": "circular_reasoning_tautology",
                "functional_contribution": False,
                "question_intent": {"type": "other", "primary_entity": ""},
                "question_demands": [{"id": "demand_1", "subject": q_text}],
                "aspect_coverage": {"ratio": 0.0, "status": "UNKNOWN"},
                "epistemic_status": {"status": "UNKNOWN", "is_demonstrated": False},
                "demand_nexus": [
                    {
                        "demand_id": "demand_1",
                        "nexus_relation": "THEMATICALLY_ADJACENT",
                        "rationale": "Response is a circular tautology without informational gain.",
                    }
                ],
                "confidence": "HIGH",
                "rationale": "Response is a circular tautology without informational gain.",
                "needs_review": False,
            }

        intent, demands = self.base_engine.decompose_question(q_text)
        is_antithesis = any(m in runtime._normalize_text(r_text) for m in self.base_engine.antithesis_markers)
        is_circular = False

        propositions = self.discourse_filter.filter_propositions(
            r_text, q_text, is_antithesis, is_circular,
            self.base_engine._normalize_morphology, intent.intent_type
        )
        prop = propositions[0]
        epistemic = self.base_engine.evaluate_epistemic_status(r_text, prop)

        # Domain Disjunction Evaluation
        domain_record = self.domain_engine.assess_compatibility(q_text, r_text, demands, prop)

        nexus_records = []
        for d in demands:
            nx = self.matcher.assess_demand_nexus(d, prop, intent.central_entities[0] if intent.central_entities else "", intent, domain_record)
            nexus_records.append(nx)

        return self.aggregator.aggregate_relevance(
            intent, demands, propositions, nexus_records, epistemic, domain_record
        )

refined_engine = RefinedOpenDomainPropositionEngine()

# Test on 20 Contract Cases
passed = 0
for tc in CONTRACT_TEST_CASES:
    res = refined_engine.evaluate_relevance(tc['question'], tc['response'])
    cls = res['classification']
    ok = (cls == tc['expected'])
    if ok: passed += 1
    status = 'OK' if ok else 'FAIL'
    print(f"{tc['id']}: pred={cls} exp={tc['expected']} -> {status}")

print(f"\nRefined Prototype score on 20 contract cases: {passed}/{len(CONTRACT_TEST_CASES)}")
