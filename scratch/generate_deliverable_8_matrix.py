import json
from pathlib import Path

pilot_dir = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05")
c29_file = pilot_dir / "stage_31_7_29_semantic_contracts.json"
c29_data = json.load(open(c29_file, encoding="utf-8"))

evaluated_contracts = []
for c in c29_data["contracts"]:
    cid = c["id"]
    scenario = c["scenario"]
    ref_class = c["reference_class"]
    
    # Assess overfitting risk and collisions
    if cid in ("SC-02", "SC-19"):
        overfitting_risk = "MODERATE: O cenário usa artesanato/antítese. Risco de codificação de regras ad-hoc se o desenvolvedor apenas adicionar esses termos a regexes em vez de generalizar a análise de predicados."
    elif cid in ("SC-03", "SC-04"):
        overfitting_risk = "LOW_TO_MODERATE: Testa metadados históricos. Risco de fixar apenas a palavra 'Berkeley' ou 'origem'."
    elif cid in ("SC-07", "SC-08"):
        overfitting_risk = "LOW: Testa decomposição composta clássica de Kafka/Circuit Breaker."
    else:
        overfitting_risk = "LOW: Representa propriedades ontológicas gerais da engenharia de software."
        
    evaluated_contracts.append({
        "contract_id": cid,
        "scenario": scenario,
        "expected_class": ref_class,
        "semantic_objective": c["justifying_evidence"],
        "architectural_rule_covered": "Cycle 6 Entity-Domain Binding & Nexus Bipartite Matching",
        "overfitting_risk": overfitting_risk,
        "potential_collision": f"Colisão potencial com {('RELATED' if ref_class == 'OFF_TOPIC' else 'INSUFFICIENT' if ref_class == 'UNKNOWN' else 'PARTIAL')} em fronteiras semânticas imprecisas.",
        "stress_verdict": "ADEQUATE_AS_SPECIFICATION"
    })

# Add 6 new adversarial review contracts exclusive to Stage 31.7.30
additional_review_contracts = [
    {
        "contract_id": "SC-23-REV",
        "scenario": "Metaphorical / Pedagogical Analogy from Another Domain",
        "expected_class": "DIRECT",
        "semantic_objective": "Validar se analogias que comparam conceitos técnicos a objetos do mundo real (disjuntor elétrico residencial) preservam a classificação DIRECT pela oração principal de software.",
        "architectural_rule_covered": "Clausal Dependency Disjunction Exemption for Metaphorical Explanations",
        "overfitting_risk": "Alto se o motor punir qualquer substantivo físico residencial.",
        "potential_collision": "Colisão com OFF_TOPIC se analisado puramente no nível léxico de substantivos.",
        "stress_verdict": "CRITICAL_ADVERSARIAL_CONTRACT"
    },
    {
        "contract_id": "SC-24-REV",
        "scenario": "Conversational Chitchat Preamble followed by Complete Direct Mechanism",
        "expected_class": "DIRECT",
        "semantic_objective": "Garantir que desabafos sobre trânsito ou café antes de responder ao algoritmo Paxos não rebaixem a resposta para OFF_TOPIC.",
        "architectural_rule_covered": "Discourse Segment Isolation & Substantive Proposition Extraction",
        "overfitting_risk": "Médio se o pré-processador não separar orações independentes.",
        "potential_collision": "Colisão com INSUFFICIENT ou OFF_TOPIC por contaminação de preâmbulo.",
        "stress_verdict": "CRITICAL_ADVERSARIAL_CONTRACT"
    },
    {
        "contract_id": "SC-25-REV",
        "scenario": "Legitimate Infrastructure Prerequisite as Response",
        "expected_class": "SUPPORTING",
        "semantic_objective": "Reconhecer que liberar portas de rede no security group e pg_hba.conf é suporte instrumental válido para replicação de banco de dados.",
        "architectural_rule_covered": "Prerequisite Technical Anchoring to Target Infrastructure",
        "overfitting_risk": "Baixo.",
        "potential_collision": "Colisão com OFF_TOPIC por ausência de parâmetros do postgresql.conf.",
        "stress_verdict": "CRITICAL_ADVERSARIAL_CONTRACT"
    },
    {
        "contract_id": "SC-26-REV",
        "scenario": "Lexical Homonymy with Non-Computing Metaphor (Shared Word, Alien Predicate)",
        "expected_class": "OFF_TOPIC",
        "semantic_objective": "Demonstrar que usar a palavra 'dependência' para divagar sobre importações e geopolítica deve ser classificado como OFF_TOPIC a despeito do match de palavra.",
        "architectural_rule_covered": "Rebuttal of Shared Entity Presumption via Alien Predicate Verification",
        "overfitting_risk": "Crítico se o sistema adotar veto absoluto cego de OFF_TOPIC.",
        "potential_collision": "Colisão direta com a regra ingênua de veto de entidade do Stage 31.7.29.",
        "stress_verdict": "DECISIVE_ADVERSARIAL_COUNTEREXAMPLE"
    },
    {
        "contract_id": "SC-27-REV",
        "scenario": "Pure Praise / Buzzword Triviality Citing Target Entity",
        "expected_class": "INSUFFICIENT",
        "semantic_objective": "Confirmar que dizer apenas 'O PostgreSQL é ótimo e muito popular' é INSUFFICIENT e não RELATED.",
        "architectural_rule_covered": "Distinction between Thematic Substantive Metadata and Conversational Filler",
        "overfitting_risk": "Médio se qualquer frase com a entidade for forçada para RELATED.",
        "potential_collision": "Colisão entre RELATED e INSUFFICIENT.",
        "stress_verdict": "CRITICAL_ADVERSARIAL_CONTRACT"
    },
    {
        "contract_id": "SC-28-REV",
        "scenario": "Fictional Technology with Rigorous Distributed Computing Mechanics",
        "expected_class": "DIRECT",
        "semantic_objective": "Provar que uma ferramenta inédita (VulcanDB) respondida com relógios vetoriais é DIRECT sem necessidade de catálogo.",
        "architectural_rule_covered": "Open Domain Conceptual Soundness without Closed Software Inventories",
        "overfitting_risk": "Baixo.",
        "potential_collision": "Colisão com OFF_TOPIC ou UNKNOWN por tecnologia não catalogada.",
        "stress_verdict": "CRITICAL_ADVERSARIAL_CONTRACT"
    }
]

matrix = {
    "stage": "31.7.30",
    "matrix_name": "Stage 31.7.30 Adversarial Contract Coverage Matrix",
    "total_cycle_5_contracts_reviewed": len(evaluated_contracts),
    "total_additional_review_contracts": len(additional_review_contracts),
    "total_combined_contracts": len(evaluated_contracts) + len(additional_review_contracts),
    "cycle_5_contract_reviews": evaluated_contracts,
    "stage_31_7_30_adversarial_stress_contracts": additional_review_contracts,
    "audit_conclusion": "Os 22 contratos do Stage 31.7.29 cobrem as falhas pontuais do benchmark, mas continham lacunas severas em metáforas analógicas (SC-23), preâmbulos ruidosos (SC-24), pré-requisitos (SC-25) e homonímia com divagação (SC-26). Os 6 novos contratos adversariais preenchem essas lacunas e estabelecem o padrão exigido para a revisão arquitetural."
}

with open(pilot_dir / "stage_31_7_30_contract_coverage_matrix.json", "w", encoding="utf-8") as f:
    json.dump(matrix, f, indent=2, ensure_ascii=False)

print(f"Generated stage_31_7_30_contract_coverage_matrix.json with {matrix['total_combined_contracts']} total contracts.")
