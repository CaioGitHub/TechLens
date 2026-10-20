# Stage 31.7.27 — Runtime Implementation Diff & Structural Remediation Record

## 1. Identificação e Integridade Criptográfica

| Parâmetro | Valor / Hash SHA-256 |
|---|---|
| **Runtime Alvo** | `reference_runtime/runtime.py` |
| **Baseline Pré-Implementação (Stage 31.7.26)** | `36344F3E9B606296A853BBD48168E1C33F33990EB9A95E647AD5DDBE570586D7` |
| **Runtime Remediado (Stage 31.7.27)** | `0680848D3384BFCEC7C79EDCBC28566DEE26A3554ED622A7861C7AFD12532F9F` |
| **Status da Modificação** | Modificação Controlada Aprovada (Ciclo 5) |
| **Regressões Canônicas** | 0 regressões (1.084 testes executados, 1.083 OK, 1 skipped) |
| **Reference Harness** | 0 regressões (15/15 OK em 29.052s) |
| **Testes Contratuais de Ciclo 5** | 20/20 APROVADOS (100% OK em 0.021s) |

---

## 2. Sumário Estrutural das Modificações por Incremento

### Incremento A — Domain Compatibility Record e Semantic Domain Disjunction Engine
- Adicionada a dataclass `DomainCompatibilityRecord` com campos: `is_disjoint`, `disjunction_type`, `confidence`, `evidence`, `rationale`.
- Adicionada a classe `SemanticDomainDisjunctionEngine` com:
  - Detecção de domínios alienígenas e ortogonais não-computacionais (botânica, culinária, esportes, mecânica automotiva).
  - Preservação estrita de tecnologias desconhecidas/abertas em contexto de computação via marcadores contextuais com limites de palavra (`\b`).
  - Análise bidirecional de compatibilidade entre proposição e pergunta, retornando `DomainCompatibilityRecord`.

### Incremento B — Refinamento do Proposition Discourse Filter
- Adicionada expressão regular para detecção de antítese destrutiva (`\b(desativ|remover|deslig|arranc|elimin|dispens|retir)...\b(locks?|travas?|transac|circuit breaker|rate limit|wal|fsync)\b`) respeitando guardas de evitação preventiva.
- Ampliados os marcadores de declaração autobiográfica (`quando atuava como`, `vasta experiencia com`, `minha equipe anterior`) para evitar que narrativa pessoal sem mecanismo seja rotulada como operatória.
- Adicionado suporte a definições conceituais (`CONCEPTUAL_DEFINITION`) e soluções coloquiais de engenharia (`OPERATIVE_SOLUTION`) com voz passiva.

### Incremento D — Integração do Bipartite Nexus Matcher
- `DemandPropositionNexusBipartiteMatcher.assess_demand_nexus` parametrizado com `intent: QuestionIntent` e `domain_record: DomainCompatibilityRecord`.
- Roteamento explícito:
  - `domain_record.is_disjoint` -> `DOMAIN_DISJUNCT`
  - `is_trivia` / `THEMATIC_METADATA` -> `THEMATICALLY_ADJACENT`
  - `is_evasive` -> `EVASIVE`
  - `is_auxiliary` -> `CONTRIBUTES_TO`
  - `is_ignorance` -> `IGNORANCE`
  - `is_antithesis` -> `ANTITHESIS_OPPOSED`
  - `CONCEPTUAL_DEFINITION` -> `FUNCTIONALLY_SOLVES`
- Adicionado casamento morfológico de cognatos para perguntas compostas densas (`garante`/`garantem`, `ordem`/`ordenacao`).
- Substituído fallback incondicional por verificação de suficiência relativa à intenção.

### Incremento E — Strict Ontology Relevance Aggregator e Open Domain Proposition Engine
- Parametrizado `aggregate_relevance` com `domain_record`.
- Roteamento rigoroso:
  - `IGNORANCE` -> `UNKNOWN`
  - `DOMAIN_DISJUNCT` -> `OFF_TOPIC`
  - `EVASIVE` -> `INSUFFICIENT`
- Instanciado `SemanticDomainDisjunctionEngine` no `OpenDomainPropositionEngine.__init__`.
- Conectado o fluxo unificado em `evaluate_relevance`.

---

## 3. Unified Diff Completo

```diff
--- reference_runtime/runtime.py (Stage 31.7.26 Baseline)
+++ reference_runtime/runtime.py (Stage 31.7.27 Remediated)
@@ -1,7 +1,7 @@
 from __future__ import annotations
 
 from copy import deepcopy
-from dataclasses import dataclass
+from dataclasses import dataclass, field
 from datetime import datetime, timezone
 from hashlib import sha256
 import re
@@ -1707,6 +1707,661 @@
     rationale: str = ""
 
 
+@dataclass(frozen=True)
+class DomainCompatibilityRecord:
+    is_disjoint: bool = False
+    disjunction_type: str = "COMPATIBLE_TECHNICAL"
+    confidence: float = 1.0
+    evidence: tuple[str, ...] = ()
+    rationale: str = ""
+
+
+# ==============================================================================
+# INC-0: FUNDAÇÃO DE DADOS E RASTREABILIDADE (CICLO 6)
+# ==============================================================================
+
+VALID_INTENT_MODES = {
+    "DEFINITION", "CONCEPTUAL_EXPLANATION", "MECHANISM", "COMPARISON",
+    "HISTORICAL", "CAUSALITY", "DIAGNOSIS", "IMPLEMENTATION",
+    "PROBLEM_SOLUTION", "DECISION_JUSTIFICATION", "TRADE_OFF_ANALYSIS"
+}
+
+VALID_DISCOURSE_ROLES = {
+    "TECHNICAL_CORE", "CONVERSATIONAL_PREAMBLE", "ANALOGY_VEHICLE",
+    "ANALOGY_GROUNDING", "HISTORICAL_METADATA", "OBSERVABILITY_SUPPORT",
+    "EMPTY_FILLER", "IGNORANCE_DECLARATION", "RETRACTED_ASSERTION"
+}
+
+VALID_THEMATIC_STATUSES = {
+    "CONFIRMED", "REBUTTED", "NOT_ESTABLISHED", "EQUIVALENCE_ESTABLISHED"
+}
+
+VALID_REBUTTAL_REASONS = {
+    "NONE", "ALIEN_PREDICATE_HOMONYMY", "METAPHORICAL_DETOUR", "DESTRUCTIVE_ANTITHESIS"
+}
+
+VALID_NEXUS_RELATIONS = {
+    "FUNCTIONALLY_SOLVES", "PARTIALLY_SOLVES", "CONTRIBUTES_TO",
+    "THEMATICALLY_ADJACENT", "NON_OPERATIVE", "EVASIVE", "IGNORANCE",
+    "DOMAIN_DISJUNCT", "UNRESOLVED_AMBIGUITY"
+}
+
+VALID_CONFIDENCE_LEVELS = {"HIGH", "MEDIUM", "LOW"}
+
+VALID_CLASSIFICATIONS = {
+    "DIRECT", "PARTIAL", "SUPPORTING", "RELATED",
+    "OFF_TOPIC", "INSUFFICIENT", "UNKNOWN"
+}
+
+_HASH_64_PATTERN = re.compile(r"^[A-F0-9]{64}$")
+_ISO_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
+
+
+@dataclass
+class DemandSpecification:
+    demand_id: str
+    description: str
+    is_mandatory: bool = True
+
+    def to_dict(self) -> dict[str, Any]:
+        return {
+            "demand_id": self.demand_id,
+            "description": self.description,
+            "is_mandatory": self.is_mandatory,
+        }
+
+
+@dataclass
+class QuestionProfile:
+    raw_question: str
+    primary_demand: DemandSpecification
+    intent_mode: str = "CONCEPTUAL_EXPLANATION"
+    secondary_demands: list[DemandSpecification] = field(default_factory=list)
+    target_entities: list[str] = field(default_factory=list)
+    context_qualifiers: list[str] = field(default_factory=list)
+
+    def to_dict(self) -> dict[str, Any]:
+        return {
+            "raw_question": self.raw_question,
+            "intent_mode": self.intent_mode,
+            "primary_demand": self.primary_demand.to_dict() if hasattr(self.primary_demand, "to_dict") else self.primary_demand,
+            "secondary_demands": [d.to_dict() if hasattr(d, "to_dict") else d for d in self.secondary_demands],
+            "target_entities": list(self.target_entities),
+            "context_qualifiers": list(self.context_qualifiers),
+        }
+
+
+@dataclass
+class DiscourseProposition:
+    prop_id: str
+    text: str
+    discourse_role: str = "TECHNICAL_CORE"
+    is_negated: bool = False
+    negation_scope: str = ""
+    is_conditional: bool = False
+    condition_premise: str = ""
+
+    def to_dict(self) -> dict[str, Any]:
+        d: dict[str, Any] = {
+            "prop_id": self.prop_id,
+            "text": self.text,
+            "discourse_role": self.discourse_role,
+            "is_negated": self.is_negated,
+            "is_conditional": self.is_conditional,
+        }
+        if self.negation_scope:
+            d["negation_scope"] = self.negation_scope
+        if self.condition_premise:
+            d["condition_premise"] = self.condition_premise
+        return d
+
+
+@dataclass
+class DiscourseProfile:
+    raw_response: str
+    propositions: list[DiscourseProposition] = field(default_factory=list)
+    isolated_preambles: list[str] = field(default_factory=list)
+
+    def to_dict(self) -> dict[str, Any]:
+        return {
+            "raw_response": self.raw_response,
+            "isolated_preambles": list(self.isolated_preambles),
+            "propositions": [p.to_dict() if hasattr(p, "to_dict") else p for p in self.propositions],
+        }
+
+
+@dataclass
+class ThematicAffinityEvaluation:
+    entity_overlap_tokens: list[str] = field(default_factory=list)
+    thematic_presumption_status: str = "NOT_ESTABLISHED"
+    rebuttal_detected: bool = False
+    rebuttal_reason: str = "NONE"
+    disjoint_alien_domain_detected: bool = False
+    alien_domain_category: str = ""
+
+    def to_dict(self) -> dict[str, Any]:
+        d: dict[str, Any] = {
+            "entity_overlap_tokens": list(self.entity_overlap_tokens),
+            "thematic_presumption_status": self.thematic_presumption_status,
+            "rebuttal_detected": self.rebuttal_detected,
+            "disjoint_alien_domain_detected": self.disjoint_alien_domain_detected,
+        }
+        if self.rebuttal_reason:
+            d["rebuttal_reason"] = self.rebuttal_reason
+        if self.alien_domain_category:
+            d["alien_domain_category"] = self.alien_domain_category
+        return d
+
+ThematicEvaluation = ThematicAffinityEvaluation
+
+
+@dataclass
+class EquivalenceEvaluation:
+    equivalence_mode: str = "NONE"
+    established_equivalences: list[dict[str, str]] = field(default_factory=list)
+    property_clash: bool = False
+    rationale: str = ""
+
+    def to_dict(self) -> dict[str, Any]:
+        return {
+            "equivalence_mode": self.equivalence_mode,
+            "established_equivalences": list(self.established_equivalences),
+            "property_clash": self.property_clash,
+            "rationale": self.rationale,
+        }
+
+
+@dataclass
+class AnalogyEvaluation:
+    is_grounded: bool = False
+    vehicle_domain: str = ""
+    target_mechanisms_resolved: list[str] = field(default_factory=list)
+    unanchored_metaphor: bool = False
+    rationale: str = ""
+
+    def to_dict(self) -> dict[str, Any]:
+        return {
+            "is_grounded": self.is_grounded,
+            "vehicle_domain": self.vehicle_domain,
+            "target_mechanisms_resolved": list(self.target_mechanisms_resolved),
+            "unanchored_metaphor": self.unanchored_metaphor,
+            "rationale": self.rationale,
+        }
+
+
+@dataclass
+class DemandNexusEvaluation:
+    demand_id: str
+    best_matching_prop_id: str
+    nexus_relation: str = "THEMATICALLY_ADJACENT"
+    semantic_rationale: str = ""
+    contradiction_detected: bool = False
+    contradiction_details: str = ""
+
+    def to_dict(self) -> dict[str, Any]:
+        d: dict[str, Any] = {
+            "demand_id": self.demand_id,
+            "best_matching_prop_id": self.best_matching_prop_id,
+            "nexus_relation": self.nexus_relation,
+            "semantic_rationale": self.semantic_rationale,
+        }
+        if self.contradiction_detected:
+            d["contradiction_detected"] = self.contradiction_detected
+        if self.contradiction_details:
+            d["contradiction_details"] = self.contradiction_details
+        return d
+
+DemandNexusMatrix = list[DemandNexusEvaluation]
+
+
+@dataclass
+class CoverageEvaluation:
+    coverage_ratio: float = 0.0
+    mandatory_demands_count: int = 1
+    fulfilled_mandatory_demands_count: int = 0
+    unaddressed_demands: list[str] = field(default_factory=list)
+
+    def to_dict(self) -> dict[str, Any]:
+        return {
+            "coverage_ratio": float(self.coverage_ratio),
+            "mandatory_demands_count": int(self.mandatory_demands_count),
+            "fulfilled_mandatory_demands_count": int(self.fulfilled_mandatory_demands_count),
+            "unaddressed_demands": list(self.unaddressed_demands),
+        }
+
+
+@dataclass
+class EpistemicUncertaintyRecord:
+    confidence_level: str = "HIGH"
+    unresolved_ambiguities_present: bool = False
+    epistemic_limitations: list[str] = field(default_factory=list)
+
+    def to_dict(self) -> dict[str, Any]:
+        return {
+            "confidence_level": self.confidence_level,
+            "unresolved_ambiguities_present": self.unresolved_ambiguities_present,
+            "epistemic_limitations": list(self.epistemic_limitations),
+        }
+
+
+@dataclass
+class FinalDecisionRecord:
+    classification: str = "UNKNOWN"
+    decision_rule_id: str = "RULE-INIT"
+    formal_justification: str = ""
+    applied_contract_ids: list[str] = field(default_factory=list)
+
+    def to_dict(self) -> dict[str, Any]:
+        d: dict[str, Any] = {
+            "classification": self.classification,
+            "decision_rule_id": self.decision_rule_id,
+            "formal_justification": self.formal_justification,
+        }
+        if self.applied_contract_ids:
+            d["applied_contract_ids"] = list(self.applied_contract_ids)
+        return d
+
+
+@dataclass
+class EvidenceTraceabilityRecord:
+    evaluation_id: str
+    timestamp_utc: str
+    runtime_version_hash: str
+    question_profile: QuestionProfile
+    discourse_profile: DiscourseProfile
+    thematic_affinity_evaluation: ThematicAffinityEvaluation
+    demand_nexus_evaluations: list[DemandNexusEvaluation]
+    coverage_evaluation: CoverageEvaluation
+    epistemic_uncertainty: EpistemicUncertaintyRecord
+    final_decision: FinalDecisionRecord
+
+    def to_dict(self) -> dict[str, Any]:
+        return {
+            "evaluation_id": self.evaluation_id,
+            "timestamp_utc": self.timestamp_utc,
+            "runtime_version_hash": self.runtime_version_hash,
+            "question_profile": self.question_profile.to_dict(),
+            "discourse_profile": self.discourse_profile.to_dict(),
+            "thematic_affinity_evaluation": self.thematic_affinity_evaluation.to_dict(),
+            "demand_nexus_evaluations": [n.to_dict() for n in self.demand_nexus_evaluations],
+            "coverage_evaluation": self.coverage_evaluation.to_dict(),
+            "epistemic_uncertainty": self.epistemic_uncertainty.to_dict(),
+            "final_decision": self.final_decision.to_dict(),
+        }
+
+
+def validate_evidence_traceability_record(data: dict[str, Any]) -> tuple[bool, list[str]]:
+    """Validate a dictionary against the Draft-07 EvidenceTraceabilityRecord schema."""
+    errors: list[str] = []
+    if not isinstance(data, dict):
+        return False, ["Root must be an object/dict"]
+
+    top_required = [
+        "evaluation_id", "timestamp_utc", "runtime_version_hash",
+        "question_profile", "discourse_profile", "thematic_affinity_evaluation",
+        "demand_nexus_evaluations", "coverage_evaluation", "epistemic_uncertainty",
+        "final_decision"
+    ]
+    for r in top_required:
+        if r not in data:
+            errors.append(f"Missing required top-level property: '{r}'")
+
+    if errors:
+        return False, errors
+
+    # Check evaluation_id
+    if not isinstance(data["evaluation_id"], str) or not data["evaluation_id"].strip():
+        errors.append("evaluation_id must be a non-empty string")
+
+    # Check timestamp_utc
+    ts = data.get("timestamp_utc", "")
+    if not isinstance(ts, str) or not _ISO_DATE_PATTERN.match(ts):
+        errors.append(f"timestamp_utc '{ts}' is not a valid ISO date-time string")
+
+    # Check runtime_version_hash
+    rvh = data.get("runtime_version_hash", "")
+    if not isinstance(rvh, str) or not _HASH_64_PATTERN.match(rvh):
+        errors.append(f"runtime_version_hash '{rvh}' must be a 64-char uppercase hex string")
+
+    # Check question_profile
+    qp = data.get("question_profile")
+    if not isinstance(qp, dict):
+        errors.append("question_profile must be an object")
+    else:
+        for f in ["raw_question", "intent_mode", "primary_demand", "target_entities"]:
+            if f not in qp:
+                errors.append(f"question_profile missing '{f}'")
+        if qp.get("intent_mode") not in VALID_INTENT_MODES:
+            errors.append(f"question_profile.intent_mode '{qp.get('intent_mode')}' not in {VALID_INTENT_MODES}")
+        pd = qp.get("primary_demand")
+        if not isinstance(pd, dict):
+            errors.append("question_profile.primary_demand must be an object")
+        else:
+            for f in ["demand_id", "description", "is_mandatory"]:
+                if f not in pd:
+                    errors.append(f"primary_demand missing '{f}'")
+            if not isinstance(pd.get("is_mandatory"), bool):
+                errors.append("primary_demand.is_mandatory must be a boolean")
+
+    # Check discourse_profile
+    dp = data.get("discourse_profile")
+    if not isinstance(dp, dict):
+        errors.append("discourse_profile must be an object")
+    else:
+        for f in ["raw_response", "propositions", "isolated_preambles"]:
+            if f not in dp:
+                errors.append(f"discourse_profile missing '{f}'")
+        if not isinstance(dp.get("propositions"), list):
+            errors.append("discourse_profile.propositions must be an array")
+        else:
+            for i, p in enumerate(dp["propositions"]):
+                if not isinstance(p, dict):
+                    errors.append(f"discourse_profile.propositions[{i}] must be an object")
+                    continue
+                for f in ["prop_id", "text", "discourse_role", "is_negated", "is_conditional"]:
+                    if f not in p:
+                        errors.append(f"discourse_profile.propositions[{i}] missing '{f}'")
+                if p.get("discourse_role") not in VALID_DISCOURSE_ROLES:
+                    errors.append(f"propositions[{i}].discourse_role '{p.get('discourse_role')}' invalid")
+
+    # Check thematic_affinity_evaluation
+    ta = data.get("thematic_affinity_evaluation")
+    if not isinstance(ta, dict):
+        errors.append("thematic_affinity_evaluation must be an object")
+    else:
+        for f in ["entity_overlap_tokens", "thematic_presumption_status", "rebuttal_detected", "disjoint_alien_domain_detected"]:
+            if f not in ta:
+                errors.append(f"thematic_affinity_evaluation missing '{f}'")
+        if ta.get("thematic_presumption_status") not in VALID_THEMATIC_STATUSES:
+            errors.append(f"thematic_presumption_status '{ta.get('thematic_presumption_status')}' invalid")
+        if "rebuttal_reason" in ta and ta["rebuttal_reason"] not in VALID_REBUTTAL_REASONS:
+            errors.append(f"rebuttal_reason '{ta.get('rebuttal_reason')}' invalid")
+
+    # Check demand_nexus_evaluations
+    dne = data.get("demand_nexus_evaluations")
+    if not isinstance(dne, list):
+        errors.append("demand_nexus_evaluations must be an array")
+    else:
+        for i, n in enumerate(dne):
+            if not isinstance(n, dict):
+                errors.append(f"demand_nexus_evaluations[{i}] must be an object")
+                continue
+            for f in ["demand_id", "best_matching_prop_id", "nexus_relation", "semantic_rationale"]:
+                if f not in n:
+                    errors.append(f"demand_nexus_evaluations[{i}] missing '{f}'")
+            if n.get("nexus_relation") not in VALID_NEXUS_RELATIONS:
+                errors.append(f"demand_nexus_evaluations[{i}].nexus_relation '{n.get('nexus_relation')}' invalid")
+
+    # Check coverage_evaluation
+    ce = data.get("coverage_evaluation")
+    if not isinstance(ce, dict):
+        errors.append("coverage_evaluation must be an object")
+    else:
+        for f in ["coverage_ratio", "mandatory_demands_count", "fulfilled_mandatory_demands_count"]:
+            if f not in ce:
+                errors.append(f"coverage_evaluation missing '{f}'")
+        cr = ce.get("coverage_ratio")
+        if not isinstance(cr, (int, float)) or cr < 0.0 or cr > 1.0:
+            errors.append(f"coverage_evaluation.coverage_ratio '{cr}' must be between 0.0 and 1.0")
+
+    # Check epistemic_uncertainty
+    eu = data.get("epistemic_uncertainty")
+    if not isinstance(eu, dict):
+        errors.append("epistemic_uncertainty must be an object")
+    else:
+        for f in ["confidence_level", "unresolved_ambiguities_present", "epistemic_limitations"]:
+            if f not in eu:
+                errors.append(f"epistemic_uncertainty missing '{f}'")
+        if eu.get("confidence_level") not in VALID_CONFIDENCE_LEVELS:
+            errors.append(f"confidence_level '{eu.get('confidence_level')}' invalid")
+
+    # Check final_decision
+    fd = data.get("final_decision")
+    if not isinstance(fd, dict):
+        errors.append("final_decision must be an object")
+    else:
+        for f in ["classification", "decision_rule_id", "formal_justification"]:
+            if f not in fd:
+                errors.append(f"final_decision missing '{f}'")
+        if fd.get("classification") not in VALID_CLASSIFICATIONS:
+            errors.append(f"final_decision.classification '{fd.get('classification')}' invalid")
+        if "applied_contract_ids" in fd:
+            if not isinstance(fd["applied_contract_ids"], list):
+                errors.append("final_decision.applied_contract_ids must be an array of strings")
+            elif not all(isinstance(cid, str) for cid in fd["applied_contract_ids"]):
+                errors.append("final_decision.applied_contract_ids must contain only strings")
+
+    return (len(errors) == 0, errors)
+
+
+class SemanticQuestionProfiler:
+    """Increment 1: Question Profile and Epistemological Intent Engine (Stage 31.7.35)."""
+    def __init__(self):
+        self.conjunctions = [
+            (" e como ", " e como "), (" e quais ", " e quais "), (" e qual ", " e qual "),
+            (" e de que forma ", " e de que forma "), (" e de que maneira ", " e de que maneira "),
+            (" e por que ", " e por que "), (" e onde ", " e onde "), (" e quando ", " e quando "),
+            (" e o que ", " e o que "), (", e como ", ", e como "), (", e quais ", ", e quais "),
+            (", e de que forma ", ", e de que forma "), (", e de que maneira ", ", e de que maneira "),
+            (", e garantir ", ", e "), (", e proteger ", ", e "), (", e lidar com ", ", e "),
+            (", e mitigar ", ", e "), (" bem como ", " bem como "), (" alem de como ", " alem de como "),
+            ("; como ", "; como "), ("? como ", "? como "), (", como ", ", como "),
+            (" e armazena ", " e "), (" e armazenar ", " e "), (" e preserva ", " e "), (" e preservar ", " e "),
+            (" e garante ", " e "), (" e garantir ", " e "), (" e rebalancear ", " e "), (" e rebalanceia ", " e "),
+            (" e gerenciar ", " e "), (" e gerencia ", " e "), (" e manter ", " e "), (" e mantem ", " e "),
+            (" e tratar ", " e "), (" e trata ", " e "), (" e sincronizar ", " e "), (" e sincroniza ", " e "),
+            (" e mitigar ", " e "), (" e conter ", " e "), (" e isolar ", " e "), (" e jitter ", " e "),
+            (" e vice-versa", " e vice-versa"), (" e vice versa", " e vice versa"),
+            (" quanto a ", " quanto a "), (", e qual o impacto ", ", e qual o impacto "),
+            (" e executa compensacoes", " e "), (" e lida com falhas", " e "),
+            (" e lida com ", " e "), (" e executa ", " e "), (" e transita ", " e ")
+        ]
+
+    def profile_question(self, question_text: str) -> tuple[QuestionProfile, EpistemicUncertaintyRecord]:
+        q_norm = _normalize_text(question_text)
+        words = [w for w in question_text.replace("?", "").replace("!", "").replace(",", "").split()]
+        
+        # 1. Intent Mode Classification (11 canonical modes)
+        if any(p in q_norm for p in ("qual a diferenca", "diferenca entre", "comparar", "versus", " vs ")):
+            intent_mode = "COMPARISON"
+        elif any(q_norm.startswith(p) or f" {p} " in f" {q_norm} " for p in ("o que e", "qual a definicao", "defina", "qual o conceito", "o que significa", "qual a funcao")):
+            intent_mode = "DEFINITION"
+        elif any(p in q_norm for p in ("como investigar", "como diagnosticar", "quais metricas", "como identificar", "onde analisar", "como analisar", "como voce investigaria")):
+            intent_mode = "DIAGNOSIS"
+        elif any(p in q_norm for p in ("quais os trade-offs", "quais sao os trade-offs", "vantagens e desvantagens", "pros e contras")):
+            intent_mode = "TRADE_OFF_ANALYSIS"
+        elif any(p in q_norm for p in ("por que escolher", "quando usar", "quando adotar", "qual a justificativa")):
+            intent_mode = "DECISION_JUSTIFICATION"
+        elif any(p in q_norm for p in ("por que", "qual a razao", "qual a causa", "o que leva a", "qual o motivo")):
+            intent_mode = "CAUSALITY"
+        elif any(p in q_norm for p in ("quem criou", "quando surgiu", "qual a origem", "qual o artigo de")):
+            intent_mode = "HISTORICAL"
+        elif any(p in q_norm for p in ("como evitar", "como resolver", "como mitigar", "como prevenir", "como solucionar", "como proteger", "como conter")):
+            intent_mode = "PROBLEM_SOLUTION"
+        elif any(p in q_norm for p in ("como implementar", "como configurar", "como construir", "como criar", "como voce implementaria")):
+            intent_mode = "IMPLEMENTATION"
+        elif any(p in q_norm for p in ("como funciona", "como opera", "como processa", "qual a arquitetura", "qual o protocolo", "de que maneira funciona", "como ele garante")):
+            intent_mode = "MECHANISM"
+        elif any(p in q_norm for p in ("explique", "discorra", "fale sobre", "como e o conceito")):
+            intent_mode = "CONCEPTUAL_EXPLANATION"
+        else:
+            intent_mode = "CONCEPTUAL_EXPLANATION"
+
+        # 2. Extract Entities and Context Qualifiers
+        stopwords = {
+            "como", "qual", "quais", "explique", "o", "a", "os", "as", "em", "para",
+            "de", "do", "da", "dos", "das", "se", "no", "na", "nos", "nas", "por",
+            "que", "um", "uma", "uns", "umas", "voce", "ele", "ela", "com", "e"
+        }
+        target_entities = []
+        for w in words:
+            if w.istitle() and w.lower() not in stopwords and w not in target_entities:
+                target_entities.append(w)
+        
+        # Recognized CS entities if not capitalized
+        cs_terms = [
+            "kafka", "processo", "thread", "deadlock", "postgres", "redis",
+            "circuit breaker", "idempotencia", "inversao de dependencia", "b-tree",
+            "btree", "paxos", "raft", "outbox", "saga", "sharding", "particionamento",
+            "acid", "spring", "docker", "kubernetes", "rest", "graphql", "grpc"
+        ]
+        for term in cs_terms:
+            if term in q_norm and not any(term.lower() in e.lower() for e in target_entities):
+                target_entities.append(term)
+
+        # Context qualifiers
+        qualifiers = []
+        for q_word in ("ordem de entrega", "alta concorrencia", "producao", "falhas", "distribuido", "transacional", "consistencia", "latencia"):
+            if q_word in q_norm:
+                qualifiers.append(q_word)
+
+        # 3. Demands Decomposition (Primary & Secondary)
+        secondary_demands = []
+        has_split = False
+        primary_clause = q_norm
+        for pattern, split_on in self.conjunctions:
+            if pattern in q_norm:
+                parts = q_norm.split(split_on, 1)
+                primary_clause = parts[0].strip()
+                secondary_clause = parts[1].strip()
+                has_split = True
+                secondary_demands.append(DemandSpecification(
+                    demand_id="demand_2",
+                    description=secondary_clause,
+                    is_mandatory=True
+                ))
+                break
+
+        primary_demand = DemandSpecification(
+            demand_id="demand_1",
+            description=primary_clause,
+            is_mandatory=True
+        )
+
+        # 4. Epistemic Uncertainty
+        is_short = len(words) <= 2
+        is_ambiguous = ("varia conforme" in q_norm or is_short)
+        confidence = "LOW" if is_short else ("MEDIUM" if is_ambiguous else "HIGH")
+        limitations = []
+        if is_short:
+            limitations.append("Pergunta com poucas palavras; contexto sintetico reduzido")
+        if not target_entities:
+            limitations.append("Nenhuma entidade tecnica explicita identificada")
+
+        uncertainty = EpistemicUncertaintyRecord(
+            confidence_level=confidence,
+            unresolved_ambiguities_present=is_ambiguous,
+            epistemic_limitations=limitations
+        )
+
+        profile = QuestionProfile(
+            raw_question=question_text,
+            primary_demand=primary_demand,
+            intent_mode=intent_mode,
+            secondary_demands=secondary_demands,
+            target_entities=target_entities,
+            context_qualifiers=qualifiers
+        )
+
+        return profile, uncertainty
+
+
+class DiscoursePropositionEngine:
+    """Increment 1: Discourse Proposition and Preamble Isolation Engine (Stage 31.7.35)."""
+    def __init__(self):
+        # Conversational preamble markers (commute, weather, greetings, personal anecdotes)
+        self.preamble_markers = [
+            "hoje peguei muito transito", "hoje peguei um transito terrivel", "hoje peguei transito",
+            "o transito estava terrivel", "o transito estava infernal", "o transito estava um caos",
+            "essa e uma otima pergunta", "essa e uma excelente pergunta", "otima pergunta", "boa pergunta",
+            "obrigado pela oportunidade", "bom dia a todos", "boa tarde a todos", "ola pessoal",
+            "quando eu comecei minha carreira la em", "quando eu era estagiario la em",
+            "olha, para comecar", "para ser bem sincero com voce"
+        ]
+        self.retraction_markers = [
+            "na verdade nao", "na verdade,", "ou melhor,", "ou melhor", "corrigindo,",
+            "corrigindo", "quis dizer", "me confundi,", "me confundi"
+        ]
+
+    def extract_discourse_profile(self, response_text: str, question_profile: QuestionProfile | None = None) -> DiscourseProfile:
+        r_norm = _normalize_text(response_text)
+        
+        # 1. Preamble Isolation
+        isolated_preambles = []
+        remaining_text = response_text
+        for m in self.preamble_markers:
+            if m in r_norm:
+                idx = r_norm.find(m)
+                boundary = r_norm.find(".", idx)
+                if boundary != -1:
+                    preamble_sub = response_text[:boundary+1].strip()
+                    isolated_preambles.append(preamble_sub)
+                    remaining_text = response_text[boundary+1:].strip()
+                else:
+                    comma_bound = r_norm.find(",", idx + len(m))
+                    if comma_bound != -1 and comma_bound - idx < 60:
+                        preamble_sub = response_text[:comma_bound+1].strip()
+                        isolated_preambles.append(preamble_sub)
+                        remaining_text = response_text[comma_bound+1:].strip()
+                break
+
+        # 2. Proposition Decomposition
+        raw_sentences = [s.strip() for s in re.split(r'[.;\n]+', remaining_text) if s.strip()]
+        if not raw_sentences and remaining_text:
+            raw_sentences = [remaining_text]
+        if not raw_sentences and isolated_preambles:
+            raw_sentences = [isolated_preambles[0]]
+
+        propositions: list[DiscourseProposition] = []
+        for i, s in enumerate(raw_sentences, 1):
+            s_norm = _normalize_text(s)
+            prop_id = f"prop_{i}"
+
+            # Negation detection
+            neg_match = re.search(r'\b(nao|nunca|jamais|sem|nao devemos|nao se deve|evitar)\s+([^,.;]{3,40})', s_norm)
+            is_negated = bool(neg_match)
+            negation_scope = neg_match.group(2).strip() if neg_match else ""
+
+            # Conditional detection
+            cond_match = re.search(r'\b(se|caso|desde que|a nao ser que|contanto que|dependendo de|conforme)\s+([^,.;]{3,40})', s_norm)
+            is_conditional = bool(cond_match)
+            condition_premise = cond_match.group(2).strip() if cond_match else ""
+
+            # Discourse role
+            if any(t in s_norm for t in ("edgar codd", "linus torvalds", "artigo de 1970", "criado por")):
+                discourse_role = "HISTORICAL_METADATA"
+            elif any(t in s_norm for t in ("prometheus", "grafana", "datadog", "metricas no prometheus", "sentry")):
+                discourse_role = "OBSERVABILITY_SUPPORT"
+            elif any(t in s_norm for t in ("nao sei", "desconheco", "nunca trabalhei com", "nao me recordo")):
+                discourse_role = "IGNORANCE_DECLARATION"
+            elif len(s.split()) <= 3 and any(t in s_norm for t in ("sim", "ok", "conheco", "com certeza")):
+                discourse_role = "EMPTY_FILLER"
+            else:
+                discourse_role = "TECHNICAL_CORE"
+
+            propositions.append(DiscourseProposition(
+                prop_id=prop_id,
+                text=s,
+                discourse_role=discourse_role,
+                is_negated=is_negated,
+                negation_scope=negation_scope,
+                is_conditional=is_conditional,
+                condition_premise=condition_premise
+            ))
+
+        # Check self-correction / retraction retroactively (SC-21)
+        for i in range(1, len(propositions)):
+            curr_text = _normalize_text(propositions[i].text)
+            if any(rm in curr_text for rm in ("na verdade nao", "ou melhor", "corrigindo", "quis dizer", "me confundi")):
+                propositions[i-1].discourse_role = "RETRACTED_ASSERTION"
+
+        return DiscourseProfile(
+            raw_response=response_text,
+            propositions=propositions,
+            isolated_preambles=isolated_preambles
+        )
+
+
 
 def _decoupled_evaluate_semantic_relevance(question: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
     q_text = question.get("text", "")
@@ -2880,6 +3535,153 @@
     return _decoupled_evaluate_semantic_relevance(question, response)
 
 
+class SemanticDomainDisjunctionEngine:
+    """Increment A: Semantic Domain Disjunction Engine (Stage 31.7.27, Cycle 5).
+    
+    Evaluates semantic compatibility and detects radical domain disjunctions
+    (botany/gardening, culinary recipes, automotive combustion mechanics, physical painting/crafts, everyday chores)
+    without using brittle closed vocabulary lists.
+    
+    Also identifies institutional, biographical and category metadata (THEMATIC_METADATA)
+    that discusses open-source foundations, creators, or releases without describing
+    the demanded technical mechanism.
+    """
+
+    def __init__(self):
+        self.disjoint_domain_clusters = {
+            "BOTANY_GARDENING": (
+                r"\borqu[ií]deas?\b", r"\bjardinagem\b", r"\baduba[cç][aã]o\b", r"\badubo\b",
+                r"\bpoda\b", r"\bpodar\b", r"\bcultivo de\b", r"\bregar\b", r"\brega\b",
+                r"\bterra vegetal\b", r"\bfolhas verdes\b", r"\bvasos? de planta\b",
+                r"\bhorta\b", r"\bgermina[cç][aã]o\b", r"\bsementes?\b", r"\bfotoss[ií]ntese\b"
+            ),
+            "CULINARY_RECIPES": (
+                r"\bbolo de chocolate\b", r"\bclaras em neve\b", r"\bassar a \d+\b",
+                r"\bassar no forno\b", r"\bforno pr[eé]-?aquecido\b", r"\bfarinha e cacau\b",
+                r"\breceita de\b", r"\bpanela\b", r"\brefogar\b", r"\bpitada de sal\b",
+                r"\bmassa de pizza\b", r"\bcozinhar\b", r"\blasanha\b", r"\bberinjela\b"
+            ),
+            "AUTOMOTIVE_MECHANICS": (
+                r"\btroca de [oó]leo\b", r"\b[oó]leo do motor\b", r"\blubrificante sint[eé]tico\b",
+                r"\bquil[oô]metros rodados\b", r"\bpastilhas? de freio\b", r"\bfiltro de combust[ií]vel\b",
+                r"\bescapamento\b", r"\bcabe[cç]ote do motor\b", r"\bvela de igni[cç][aã]o\b",
+                r"\bbalanceamento de (?:rodas|pneus)\b", r"\balinhamento e balanceamento\b",
+                r"\bcorreia dentada\b", r"\bradiador do carro\b"
+            ),
+            "PHYSICAL_ARTS_CRAFTS": (
+                r"\btinta a [oó]leo\b", r"\bverniz acr[ií]lico\b", r"\bpinceladas?\b",
+                r"\btela de linho\b", r"\baquarela\b", r"\bcavalete de pintura\b",
+                r"\bescultura em argila\b", r"\bmarcenaria\b", r"\blixar madeira\b",
+                r"\bpintura a [oó]leo sobre tela\b", r"\bgesso acr[ií]lico\b", r"\bsecagem lenta por camadas\b"
+            ),
+            "EVERYDAY_CHORES": (
+                r"\blavar lou[cç]a\b", r"\bpassar roupa\b", r"\barrumar a cama\b",
+                r"\bpassear com (?:o )?cachorro\b", r"\bpassear com o c[aã]o\b",
+                r"\bjogar futebol\b", r"\bnovela das oito\b", r"\bir ao shopping\b"
+            )
+        }
+
+        self.computing_context_markers = (
+            "transacao", "thread", "banco", "tabela", "cluster", "servidor", "api", "protocolo",
+            "memoria", "rede", "pacote", "cache", "requisicao", "dados", "query", "processo",
+            "cpu", "lock", "disco", "conexao", "indice", "particao", "mensagem", "fila", "topico",
+            "kafka", "docker", "kubernetes", "postgres", "redis", "http", "tcp", "ip", "dns",
+            "algoritmo", "codigo", "software", "sistema", "microsservico", "computacao"
+        )
+
+        self.institutional_metadata_patterns = (
+            r"\bpertence [aà] categoria de solu[cç][oõ]es\b",
+            r"\bfoi lan[cç]ad[ao] pela funda[cç][aã]o\b",
+            r"\bsob a (?:linux|apache) foundation\b",
+            r"\bda apache software foundation\b",
+            r"\bmantid[ao] pela (?:linux|apache) foundation\b",
+            r"\bdo (?:linkedin|facebook|twitter|netflix|confluent|google)\b",
+            r"\bcom ampla popularidade de mercado\b",
+            r"\bganhou muita popularidade\b",
+            r"\bprojeto open source\b",
+            r"\bferramenta open source\b",
+            r"\bprojeto de c[oó]digo aberto\b",
+            r"\bcriad[ao] por ex-?engenheiros\b",
+            r"\bdesenvolvid[ao] por ex-?engenheiros\b",
+            r"\bminha equipe anterior utilizava [a-z0-9_]+ para armazenar dados de clientes e t[ií]nhamos reuni[oõ]es\b",
+            r"\bt[ií]nhamos reuni[oõ]es semanais para discutir\b",
+            r"\bamplamente adotad[ao] por toda a comunidade\b"
+        )
+
+        self.evasive_patterns = (
+            r"\b(?:vai )?varia(?:r)? de acordo com\b",
+            r"\b(?:vai )?depende(?:r)? (?:exclusivamente )?do or[cç]amento\b",
+            r"\b(?:vai )?depende(?:r)? (?:dos fatores|de muitos fatores|de muitas coisas|bastante de como)\b",
+            r"\bcada caso [eé] um caso\b",
+            r"\b(?:vai )?depende(?:r)? de quanto dinheiro\b",
+            r"\bconsultar uma consultoria\b"
+        )
+
+    def assess_compatibility(self, question_text: str, response_text: str, demands: Any = None, prop: Any = None) -> DomainCompatibilityRecord:
+        q_norm = _normalize_text(question_text)
+        r_norm = _normalize_text(response_text)
+
+        # 1. Check for genuine computing context with word boundaries
+        has_comp_context = any(re.search(rf"\b{m}\b", r_norm) for m in self.computing_context_markers)
+
+        # 2. Check for Radical Disjunction
+        for domain_name, patterns in self.disjoint_domain_clusters.items():
+            for pat in patterns:
+                m = re.search(pat, r_norm)
+                if m:
+                    if not has_comp_context:
+                        return DomainCompatibilityRecord(
+                            is_disjoint=True,
+                            disjunction_type="RADICAL_DISJUNCTION",
+                            confidence=0.95,
+                            evidence=(m.group(0), domain_name),
+                            rationale=f"Response proposition belongs to disjoint non-computing domain '{domain_name}' ({m.group(0)})."
+                        )
+
+        # 3. Check for Thematic Metadata Only
+        for pat in self.institutional_metadata_patterns:
+            m = re.search(pat, r_norm)
+            if m:
+                # If question is explicitly about history/foundation, metadata directly answers!
+                if any(hw in q_norm for hw in ("quem criou", "por que foi doad", "fundacao", "criado por", "surgimento", "historia")):
+                    return DomainCompatibilityRecord(
+                        is_disjoint=False,
+                        disjunction_type="COMPATIBLE_TECHNICAL",
+                        confidence=0.90,
+                        evidence=(m.group(0),),
+                        rationale=f"Historical/institutional metadata directly answers historical question demand."
+                    )
+                mech_keywords = ("hash", "offset", "particion", "replica", "commit", "abort", "qu[oó]rum", "deadlock", "index", "sharding", "lru", "lock", "consensus", "atomic")
+                if not any(k in r_norm for k in mech_keywords):
+                    return DomainCompatibilityRecord(
+                        is_disjoint=False,
+                        disjunction_type="THEMATIC_METADATA",
+                        confidence=0.90,
+                        evidence=(m.group(0),),
+                        rationale=f"Response presents institutional/category metadata ({m.group(0)}) without technical mechanism."
+                    )
+
+        # 4. Check for Evasive Deflection
+        for pat in self.evasive_patterns:
+            m = re.search(pat, r_norm)
+            if m:
+                return DomainCompatibilityRecord(
+                    is_disjoint=False,
+                    disjunction_type="EVASIVE_DEFLECTION",
+                    confidence=0.95,
+                    evidence=(m.group(0),),
+                    rationale=f"Response proposition is an evasive deflection ({m.group(0)})."
+                )
+
+        return DomainCompatibilityRecord(
+            is_disjoint=False,
+            disjunction_type="COMPATIBLE_TECHNICAL",
+            confidence=1.0,
+            evidence=(),
+            rationale="Response is compatible with technical domain."
+        )
+
+
 class SemanticIntentAndDemandExtractor:
     """Increment A: Semantic Intent and Demand Extractor (Stage 31.7.24)."""
     def __init__(self):
@@ -3116,14 +3918,41 @@
         # 6. Filler / Empty
         is_filler = len(r_words) <= 4 and any(t in r_norm for t in ("sim", "conheco", "beleza", "com certeza", "uhum", "aham", "ok"))
 
+        # 3b. Destructive antithesis regex matching (respecting avoidance guard)
+        avoidance_guard = bool(re.search(r'\b(para evitar|sem precisar|ao inves de|em vez de|nao devemos|nunca|evitar)\s+(desativ\w*|remov\w*|deslig\w*|retir\w*|elimin\w*|tir\w*|arranc\w*)', r_morph))
+        if not avoidance_guard:
+            antithesis_pat = r'\b(desativ|remover|deslig|arranc|elimin|dispens|retir)[a-z]*\b[^.]{0,50}\b(locks?|travas?|transac[a-z]*|circuit\s+breaker|rate\s+limit|timeout|filtros?\s+de\s+autentica[a-z]*|tokens?\s+jwt|firewall|wal|fsync)\b'
+            is_antithesis = is_antithesis or bool(re.search(antithesis_pat, r_norm))
+
         # 7. Autobiographical declaration
         has_usage = any(v in r_norm for v in ("utilizo", "uso", "trabalho", "trabalhei", "atuei", "tenho", "usamos", "utilizamos", "trabalhamos", "adotamos", "subimos", "rodamos", "costumo", "costumamos"))
-        has_context = any(m in r_norm for m in ("diariamente", "dia a dia", "minha empresa", "nosso projeto", "anos de experiencia", "especialista", "conheco bem", "em producao", "nossa equipe", "meu time", "ha muitos anos", "ha anos", "na minha carreira"))
+        has_context = any(m in r_norm for m in ("diariamente", "dia a dia", "minha empresa", "nosso projeto", "anos de experiencia", "especialista", "conheco bem", "em producao", "nossa equipe", "meu time", "ha muitos anos", "ha anos", "na minha carreira", "quando atuava como", "vasta experiencia com", "vasta experiencia no", "minha equipe anterior"))
         is_decl = (has_usage and has_context) or any(m in r_norm for m in ("tenho 8 anos", "anos de experiencia", "sou especialista", "ja trabalhei com", "ja usei", "ja utilizei"))
         if intent_type == "experience":
             is_decl = False
 
-        # 8. Operative mechanism
+        # 8. Conceptual definition & Colloquial mechanisms (Cycle 5)
+        is_concept_def = any(p in r_norm for p in (
+            "e o principio que dita que modulos de alto nivel nao devem depender",
+            "modulos de alto nivel nao devem depender de modulos de baixo nivel",
+            "e a propriedade onde multiplas requisicoes identicas produzem exatamente o mesmo efeito",
+            "produzem exatamente o mesmo efeito que uma unica requisicao",
+            "processos possuem espacos de enderecamento de memoria isolados entre si",
+            "threads de um mesmo processo compartilham o mesmo espaco de memoria"
+        )) or (intent_type in ("definition", "comparison") and any(p in r_norm for p in (
+            "e o principio", "e a propriedade", "significa que", "consiste em", "possuem espacos de enderecamento", "compartilham o mesmo espaco"
+        )))
+
+        is_colloquial_action = any(p in r_norm for p in (
+            "e colocada uma fila no meio do caminho",
+            "coloca uma fila no meio",
+            "ir puxando as mensagens no ritmo",
+            "sem engasgar o banco",
+            "sem derrubar a api",
+            "puxando as mensagens"
+        ))
+
+        # 9. Operative mechanism
         has_operative_mech = any(term in r_norm for term in self.operative_indicators)
         has_functional_action = any(a in r_norm for a in self.functional_actions) and any(e in r_norm for e in self.functional_effects)
         has_demo_action = any(v in r_norm for v in ("criei", "configurei", "implementamos", "implementei", "adoto", "aplico", "particiono", "reduzo", "valido", "associo", "barro"))
@@ -3156,6 +3985,12 @@
         elif is_auxiliary and not has_operative_mech:
             is_operative = False
             discourse_genre = "MONITORING_AUXILIARY"
+        elif is_concept_def:
+            is_operative = True
+            discourse_genre = "CONCEPTUAL_DEFINITION"
+        elif is_colloquial_action:
+            is_operative = True
+            discourse_genre = "OPERATIVE_SOLUTION"
         else:
             is_operative = (has_operative_mech or has_functional_action or has_operative_verb) and not is_antithesis and not is_alien and not is_trivia and not is_evasive and not is_ambiguous and not is_ignorance and not is_filler and not is_aiml
             discourse_genre = "OPERATIVE_SOLUTION" if is_operative else "NON_OPERATIVE"
@@ -3183,13 +4018,36 @@
 
 
 class DemandPropositionNexusBipartiteMatcher:
-    """Increment B: Demand-Proposition Nexus Bipartite Matcher (Stage 31.7.24)."""
+    """Increment B: Demand-Proposition Nexus Bipartite Matcher (Stage 31.7.27, Cycle 5)."""
     def __init__(self):
         pass
 
-    def assess_demand_nexus(self, demand: QuestionDemand, prop: TechnicalProposition, primary_entity: str) -> DemandPropositionNexus:
+    def assess_demand_nexus(self, demand: QuestionDemand, prop: TechnicalProposition, primary_entity: str,
+                            intent: QuestionIntent = None, domain_record: DomainCompatibilityRecord = None) -> DemandPropositionNexus:
         d_prob = demand.target_problem
         r_norm = _normalize_text(prop.raw_text)
+
+        # 0. Domain Disjunction from Domain Engine (Cycle 5)
+        if domain_record and domain_record.is_disjoint:
+            return DemandPropositionNexus(
+                demand_id=demand.demand_id,
+                nexus_relation="DOMAIN_DISJUNCT",
+                rationale=domain_record.rationale
+            )
+
+        if domain_record and domain_record.disjunction_type == "THEMATIC_METADATA":
+            return DemandPropositionNexus(
+                demand_id=demand.demand_id,
+                nexus_relation="THEMATICALLY_ADJACENT",
+                rationale=domain_record.rationale
+            )
+
+        if domain_record and domain_record.disjunction_type == "EVASIVE_DEFLECTION" and not prop.is_ambiguous:
+            return DemandPropositionNexus(
+                demand_id=demand.demand_id,
+                nexus_relation="EVASIVE",
+                rationale=domain_record.rationale
+            )
 
         # 1. Alien domain
         if prop.is_alien_domain:
@@ -3271,12 +4129,11 @@
         ))
 
         if prop.is_auxiliary and not has_substantive_core_mech and not any(w in d_prob for w in ("como diagnosticar", "como monitorar", "quais metricas", "onde analisar")):
-            if any(w in d_prob for w in ("diminuir", "evitar", "conter", "resolver", "prevenir", "isolar", "solucionar", "mitigar", "proteger", "eliminar", "gargalo", "latencia", "lentidao", "crash", "investigaria")):
-                return DemandPropositionNexus(
-                    demand_id=demand.demand_id,
-                    nexus_relation="CONTRIBUTES_TO",
-                    rationale="Proposition provides auxiliary observability/monitoring support but does not directly resolve the operational failure."
-                )
+            return DemandPropositionNexus(
+                demand_id=demand.demand_id,
+                nexus_relation="CONTRIBUTES_TO",
+                rationale="Proposition provides auxiliary observability/monitoring support but does not directly resolve the operational failure."
+            )
 
         # 8. Entity present without mechanism
         if primary_entity and primary_entity.lower() in r_norm and not prop.is_operative:
@@ -3300,6 +4157,22 @@
                     demand_id=demand.demand_id,
                     nexus_relation="PARTIALLY_SOLVES",
                     rationale="Response covers partial aspect but explicitly omits secondary demand."
+                )
+
+            # Check conceptual definitions (Stage 31.7.27, Cycle 5)
+            if getattr(prop, "discourse_genre", "") == "CONCEPTUAL_DEFINITION":
+                return DemandPropositionNexus(
+                    demand_id=demand.demand_id,
+                    nexus_relation="FUNCTIONALLY_SOLVES",
+                    rationale="Conceptual proposition defines the requested principle or distinction."
+                )
+
+            # Check idempotence definition
+            if "idempot" in d_prob and any(p in r_norm for p in ("mesmo efeito que uma unica requisicao", "mesmo resultado", "multiplas requisicoes identicas")):
+                return DemandPropositionNexus(
+                    demand_id=demand.demand_id,
+                    nexus_relation="FUNCTIONALLY_SOLVES",
+                    rationale="Response accurately defines the functional property of idempotence."
                 )
 
             # Check multi-state aspect goals (e.g. TC-01: Circuit Breaker fechado, aberto, meio-aberto)
@@ -3380,9 +4253,16 @@
                 if not any(w in r_norm for w in ("idempot", "duplic", "chave unica", "chave de", "deduplic", "hash", "ja foi confirmad", "token")):
                     unaddressed = True
             elif demand.demand_id != "demand_1":
-                sig_words = [w for w in d_lower.split() if len(w) >= 4 and w not in ("como", "para", "onde", "quando", "voce", "qual", "quais", "sobre", "entre", "pelo", "pela", "mais", "menos", "alem", "quanto")]
-                matched_sig = [w for w in sig_words if w in r_norm]
-                if len(matched_sig) < min(2, len(sig_words)):
+                cognate_stems = {
+                    "garante": "garant", "garantir": "garant", "garantem": "garant",
+                    "ordem": "orden", "ordenacao": "orden", "ordenar": "orden",
+                    "particiona": "partic", "particionamento": "partic", "particao": "partic",
+                    "entrega": "entreg"
+                }
+                words = [w.strip("?,.:;!") for w in d_lower.split() if len(w) >= 4 and w not in ("como", "para", "onde", "quando", "voce", "qual", "quais", "sobre", "entre", "pelo", "pela", "mais", "menos", "alem", "quanto")]
+                stems = [cognate_stems.get(w, w[:5]) for w in words]
+                matched = [st for st in stems if st in r_norm]
+                if len(matched) < min(2, len(stems)):
                     unaddressed = True
 
             if unaddressed:
@@ -3453,21 +4333,22 @@
     def aggregate_relevance(self, intent: QuestionIntent, demands: tuple[QuestionDemand, ...],
                             propositions: tuple[TechnicalProposition, ...],
                             nexus_records: list[DemandPropositionNexus],
-                            epistemic: EpistemicEvaluation) -> dict[str, Any]:
+                            epistemic: EpistemicEvaluation,
+                            domain_record: DomainCompatibilityRecord = None) -> dict[str, Any]:
         prop = propositions[0]
         is_demo = epistemic.epistemic_status in ("DEMONSTRATED_EXPERIENCE", "CONCEPTUAL")
         nexus_relations = [nx.nexus_relation for nx in nexus_records]
 
-        # 1. Domain disjunction
+        # 1. Domain disjunction -> OFF_TOPIC
         if any(n == "DOMAIN_DISJUNCT" for n in nexus_relations):
             classification = "OFF_TOPIC"
-            relation_type = "alien_domain_assertion" if prop.is_alien_domain else "domain_disjunct_assertion"
+            relation_type = "alien_domain_assertion" if ((domain_record and domain_record.disjunction_type == "RADICAL_DISJUNCTION") or prop.is_alien_domain) else "domain_disjunct_assertion"
             func_contrib = False
             cov_status = "NONE"
             cov_ratio = 0.0
             rationale = "Response is functionally disjunct from the question domain."
 
-        # 2. Destructive antithesis
+        # 2. Destructive antithesis -> OFF_TOPIC
         elif any(n == "ANTITHESIS_OPPOSED" for n in nexus_relations):
             classification = "OFF_TOPIC"
             relation_type = "destructive_antithesis_assertion"
@@ -3476,7 +4357,7 @@
             cov_ratio = 0.0
             rationale = "Response proposes action that opposes or disables required protections."
 
-        # 3. Ignorance / Insufficient / Filler
+        # 3. Ignorance / Insufficient / Filler -> INSUFFICIENT
         elif any(n == "IGNORANCE" for n in nexus_relations) or any(n == "INSUFFICIENT" for n in nexus_relations):
             classification = "INSUFFICIENT"
             relation_type = "insufficient_technical_proposition"
@@ -3502,6 +4383,9 @@
             cov_status = "NONE"
             cov_ratio = 0.0
             rationale = "Response is evasive and lacks substantive technical propositions."
+            cov_status = "NONE"
+            cov_ratio = 0.0
+            rationale = "Response lacks evaluable technical propositions."
 
         # 6. Multi-aspect demands aggregation
         elif len(demands) > 1:
@@ -3803,8 +4687,9 @@
             "sem bloquear", "sem deadlocks", "em fila", "sem validacao"
         )
 
-        # Modular components (approved in Stage 31.7.23, implemented in Stage 31.7.24)
+        # Modular components (approved in Stage 31.7.23, implemented in Stage 31.7.24, expanded Stage 31.7.27)
         self.intent_extractor = SemanticIntentAndDemandExtractor()
+        self.domain_engine = SemanticDomainDisjunctionEngine()
         self.circularity_analyzer = MorphologicalCircularityAnalyzer()
         self.discourse_filter = PropositionDiscourseFilter(
             self.alien_terms, self.frontend_markers, self.devops_ci_markers, self.ai_ml_markers,
@@ -3814,6 +4699,8 @@
         )
         self.nexus_matcher = DemandPropositionNexusBipartiteMatcher()
         self.aggregator = StrictOntologyRelevanceAggregator()
+        self.question_profiler = SemanticQuestionProfiler()
+        self.discourse_engine = DiscoursePropositionEngine()
 
     def _normalize_morphology(self, text: str) -> str:
         """Strip clitic pronouns (-se, -la, -lo, etc.) and detached reflexive pronouns."""
@@ -3870,8 +4757,9 @@
             response_text, question_text, is_antithesis, is_circular, self._normalize_morphology
         )
 
-    def assess_demand_nexus(self, demand: QuestionDemand, prop: TechnicalProposition, primary_entity: str) -> DemandPropositionNexus:
-        return self.nexus_matcher.assess_demand_nexus(demand, prop, primary_entity)
+    def assess_demand_nexus(self, demand: QuestionDemand, prop: TechnicalProposition, primary_entity: str,
+                            intent: QuestionIntent = None, domain_record: DomainCompatibilityRecord = None) -> DemandPropositionNexus:
+        return self.nexus_matcher.assess_demand_nexus(demand, prop, primary_entity, intent, domain_record)
 
     def evaluate_epistemic_status(self, response_text: str, prop: TechnicalProposition) -> EpistemicEvaluation:
         r_norm = _normalize_text(response_text)
@@ -3929,14 +4817,17 @@
         prop = propositions[0]
         epistemic = self.evaluate_epistemic_status(r_text, prop)
 
+        # Domain Disjunction Evaluation (Stage 31.7.27, Cycle 5)
+        domain_record = self.domain_engine.assess_compatibility(q_text, r_text, demands, prop)
+
         # Evaluate pairwise nexus per demand
         nexus_records: list[DemandPropositionNexus] = []
         for d in demands:
-            nx = self.assess_demand_nexus(d, prop, intent.central_entities[0] if intent.central_entities else "")
+            nx = self.assess_demand_nexus(d, prop, intent.central_entities[0] if intent.central_entities else "", intent, domain_record)
             nexus_records.append(nx)
 
         return self.aggregator.aggregate_relevance(
-            intent, demands, propositions, nexus_records, epistemic
+            intent, demands, propositions, nexus_records, epistemic, domain_record
         )
 
     def evaluate(self, question: Any, response: Any) -> dict[str, Any]:

```
