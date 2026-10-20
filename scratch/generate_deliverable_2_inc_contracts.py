import json
from pathlib import Path

pilot_dir = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05")

increments = [
    {
        "increment_id": "INC-0",
        "name": "Fundação de Rastreabilidade e Estruturas de Dados Tipadas",
        "description": "Definição formal das dataclasses tipadas e do schema JSON Draft-07 atualizado com o campo applied_contract_ids, estabelecendo a infraestrutura imutável de rastreabilidade causal.",
        "inputs": ["raw_question: str", "raw_response: str"],
        "outputs": [
            "QuestionProfile", "DiscourseProfile", "ThematicEvaluation",
            "EquivalenceEvaluation", "AnalogyEvaluation", "DemandNexusMatrix",
            "CoverageEvaluation", "EvidenceTraceabilityRecord"
        ],
        "satisfied_contracts": ["TRACEABILITY-SCHEMA-DRAFT-07", "FINDING-06-DISPOSITION"],
        "acceptance_criteria": "Validação estrutural 100% conforme no JSON Schema Draft-07 com serialização e desserialização sem perda de informação.",
        "dependencies": [],
        "rollback_target": "reference_runtime/runtime.py.stage_31_7_32_freeze"
    },
    {
        "increment_id": "INC-1",
        "name": "Perfil da Pergunta e Suficiência por Intenção",
        "description": "Implementação do QuestionProfileExtractor e do SufficiencyAssessmentEngine para os 10 modos de intenção epistemológica, com decomposição estrita de demandas compostas (Dp e Ds) e critérios de suficiência específicos por modo.",
        "inputs": ["raw_question: str"],
        "outputs": ["QuestionProfile (intent_mode, Dp, Ds, Eq, context)"],
        "satisfied_contracts": [
            "SC-01", "SC-02", "SC-05", "SC-06", "SC-07", "SC-08", "SC-11", "SC-12", "ADV-06"
        ],
        "acceptance_criteria": "Decomposição correta em 100% das perguntas com demandas compostas (e.g. particionamento + ordenação no Kafka) e classificação precisa dos 10 modos de intenção.",
        "dependencies": ["INC-0"],
        "rollback_target": "reference_runtime/runtime.py.stage_31_7_33_inc_0"
    },
    {
        "increment_id": "INC-2",
        "name": "Segmentação Discursiva, Modificadores, Preâmbulos e Autocorreção",
        "description": "Implementação do DiscourseSegmentationEngine com isolamento de preâmbulos fáticos ruidosos, vinculação de escopos de negações e condicionais, resolução de autocorreções explícitas e demarcação de contradições reais vs aparentes.",
        "inputs": ["raw_response: str"],
        "outputs": ["DiscourseProfile (propositions, isolated_preambles, scopes, contradictions)"],
        "satisfied_contracts": [
            "SC-17", "SC-18", "SC-20", "SC-21", "SC-22", "SC-32", "SC-33", "SC-34",
            "ADV-05", "ADV-09", "ADV-10", "ADV-11", "ADV-12", "ADV-13", "ADV-14", "FINDING-05-DISPOSITION"
        ],
        "acceptance_criteria": "Isolamento de 100% dos preâmbulos fáticos sem contaminar o núcleo técnico; preservação de escopo de negações preventivas e condicionais; prevalência de conclusões em autocorreções; conciliação de contradições sob escopos distintos.",
        "dependencies": ["INC-0"],
        "rollback_target": "reference_runtime/runtime.py.stage_31_7_33_inc_1"
    },
    {
        "increment_id": "INC-3",
        "name": "Afinidade Temática Refutável e Resolução de Homonímia",
        "description": "Implementação do ThematicAffinityEngine com presunção H_tema e teste de refutação por predicados alienígenas sobre papéis semânticos (SRL) e categorias de substantivos físicos, com emissão do status transitório EQUIVALENCE_PENDING.",
        "inputs": ["QuestionProfile", "DiscourseProfile"],
        "outputs": ["ThematicEvaluation (presumption_status, rebuttal_reason, is_alien)"],
        "satisfied_contracts": [
            "SC-29", "SC-23-REV", "ADV-01", "FINDING-01-DISPOSITION", "FINDING-04-DISPOSITION"
        ],
        "acceptance_criteria": "Refutação categórica de homônimos com divagação alienígena (Spring DI vs petróleo bruto -> OFF_TOPIC); emissão de EQUIVALENCE_PENDING quando Er ∩ Eq = ∅ sem disparar disjunção prematura.",
        "dependencies": ["INC-0", "INC-1", "INC-2"],
        "rollback_target": "reference_runtime/runtime.py.stage_31_7_33_inc_2"
    },
    {
        "increment_id": "INC-4",
        "name": "Equivalência Conceitual, Invariantes de CS e Analogias Ancoradas",
        "description": "Implementação do ConceptualEquivalenceEngine e do AnalogyResolutionEngine, reconhecendo propriedades invariantes formais de estruturas de dados e concorrência sem nomes literais e verificando aterrissagem substantiva de analogias pedagógicas.",
        "inputs": ["QuestionProfile", "DiscourseProfile", "ThematicEvaluation"],
        "outputs": [
            "EquivalenceEvaluation (established_equivalences, property_clash)",
            "AnalogyEvaluation (is_grounded, target_mechanisms_resolved)"
        ],
        "satisfied_contracts": [
            "SC-24-REV", "SC-25-REV", "SC-26-REV", "SC-27-REV", "SC-28-REV", "SC-30", "SC-31",
            "ADV-02", "ADV-04", "ADV-07", "ADV-08", "FINDING-02-DISPOSITION", "FINDING-03-DISPOSITION"
        ],
        "acceptance_criteria": "Reconhecimento de DIRECT para B-tree explicada como árvore balanceada e ChronoMesh com relógios vetoriais; aceitação de analogias com aterrissagem técnica (Circuit Breaker com disjuntor) e rebaixamento de analogias sem transposição para INSUFFICIENT.",
        "dependencies": ["INC-0", "INC-1", "INC-2", "INC-3"],
        "rollback_target": "reference_runtime/runtime.py.stage_31_7_33_inc_3"
    },
    {
        "increment_id": "INC-5",
        "name": "Agregação Estrita das Sete Classes e Roteamento Ontológico",
        "description": "Implementação do StrictRelevanceAggregator com consolidação na tabela de decisão determinística fechada das 7 classes, eliminação definitiva do sumidouro else: OFF_TOPIC, roteamento explícito de metadados para RELATED e chavões para INSUFFICIENT, e emissão do schema JSON de rastreabilidade.",
        "inputs": ["Todas as saídas dos estágios INC-0 a INC-4"],
        "outputs": ["Final Canonical Classification (7 classes)", "EvidenceTraceabilityRecord JSON"],
        "satisfied_contracts": [
            "SC-03", "SC-04", "SC-09", "SC-10", "SC-13", "SC-14", "SC-15", "SC-16", "SC-19", "SC-35",
            "ADV-03", "ADV-15", "21-CLASS-BOUNDARIES-MATRIX"
        ],
        "acceptance_criteria": "0 falsos DIRECT em elogios vazios; roteamento de 100% dos metadados históricos/institucionais legítimos para RELATED; emissão de JSON de rastreabilidade para 100% das predições; zero regressões canônicas.",
        "dependencies": ["INC-0", "INC-1", "INC-2", "INC-3", "INC-4"],
        "rollback_target": "reference_runtime/runtime.py.stage_31_7_33_inc_4"
    }
]

doc = {
    "stage": "31.7.33",
    "title": "Stage 31.7.33 Controlled Increment Contracts Specification",
    "total_increments": len(increments),
    "increments": increments,
    "audit_declaration": "Os seis incrementos decompõem exaustivamente o pipeline em unidades autônomas, verificáveis e reversíveis, garantindo que cada contrato semântico possua atribuição inequívoca e que todo rollback aponte para um snapshot imutável pré-existente."
}

with open(pilot_dir / "stage_31_7_33_increment_contracts.json", "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Generated stage_31_7_33_increment_contracts.json with {len(increments)} increments.")
