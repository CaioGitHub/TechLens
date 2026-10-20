import json
from pathlib import Path

pilot_dir = Path("11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05")

findings = [
    {
        "finding_id": "FINDING-01",
        "severity": "MAJOR",
        "title": "Mecanismo de Determinação de Predicados Alienígenas no Estágio 3",
        "artifact_reference": "stage_31_7_31_thematic_connection_contract.md, Seção 3 e stage_31_7_31_open_questions.md, Questão 1",
        "evidence": "A especificação define que a presunção temática é refutada quando os predicados atuam sobre domínio alienígena, mas não detalha como o motor infere essa incompatibilidade sem recorrer a listas lexicais fechadas.",
        "impact": "Risco de reintroduzir heurísticas duras de palavras proibidas ou listas estáticas durante a fase de codificação.",
        "recommendation": "No planejamento de implementação (Stage 31.7.33), delimitar formalmente que a refutação de predicados deve operar sobre análise sintática de papéis semânticos (SRL) ou casamento de substantivos nucleares concretos do mundo físico, evitando listas ad-hoc.",
        "status": "OPEN_FOR_IMPLEMENTATION_PLANNING"
    },
    {
        "finding_id": "FINDING-02",
        "severity": "MAJOR",
        "title": "Limites Operacionais da Equivalência Conceitual e Hiperônimos Abertos no Estágio 4",
        "artifact_reference": "stage_31_7_31_conceptual_equivalence_contract.md, Seção 4 e stage_31_7_31_open_questions.md, Questão 1",
        "evidence": "O reconhecimento de equivalência aberta sem repetição de tokens literais (Caso D: árvore balanceada para B-tree) é formalmente correto, mas a especificação reconhece em Questões em Aberto que sua generalização pode exigir oráculos vetoriais.",
        "impact": "Tentativa de implementar cobertura universal em analisador determinístico simbólico puro pode resultar em lacunas ou complexidade descontrolada.",
        "recommendation": "No plano de implementação, focar a equivalência funcional nos invariantes essenciais bem documentados da ciência da computação (árvores, tabelas hash, locks, réplicas, consenso), delimitando o escopo simbólico e tratando casos fora do escopo com incerteza calibrada (UNKNOWN).",
        "status": "OPEN_FOR_IMPLEMENTATION_PLANNING"
    },
    {
        "finding_id": "FINDING-03",
        "severity": "MODERATE",
        "title": "Risco de Rigidez Lexical na Detecção de Aterrissagem de Analogias no Estágio 5",
        "artifact_reference": "stage_31_7_31_analogy_handling_contract.md, Seção 2 e 3",
        "evidence": "A exigência de comprovação de aterrissagem no domínio-alvo (software) pode induzir a implementação a procurar expressões literais como 'no software', 'na aplicação' ou 'em microsserviços'.",
        "impact": "Analogias válidas formuladas em linguagem natural com aterrissagem sutil ou elíptica correm risco de serem rebaixadas indevidamente para INSUFFICIENT.",
        "recommendation": "O motor deve verificar a presença de termos, entidades e predicados do domínio computacional no agregado oracional da resposta como evidência de aterrissagem, sem depender de expressões fixas de transposição.",
        "status": "OPEN_FOR_IMPLEMENTATION_PLANNING"
    },
    {
        "finding_id": "FINDING-04",
        "severity": "MODERATE",
        "title": "Interdependência Causal entre Afinidade Temática (Estágio 3) e Equivalência Funcional (Estágio 4)",
        "artifact_reference": "stage_31_7_31_refined_architecture.md, Seção 2.3 e 2.4",
        "evidence": "Se a resposta omitir o nome da tecnologia da pergunta e usar apenas a descrição funcional (Caso D), o Estágio 3 não encontra tokens compartilhados (Er ∩ Eq = ∅).",
        "impact": "Se o Estágio 3 emitir um veredito sumário de disjunção alienígena prematuro, o Estágio 4 pode ser bypassado ou neutralizado.",
        "recommendation": "O Estágio 3 deve emitir status EQUIVALENCE_PENDING quando Er ∩ Eq = ∅, delegando ao Estágio 4 a responsabilidade de confirmar a equivalência funcional antes de qualquer conclusão sobre afinidade temática.",
        "status": "OPEN_FOR_IMPLEMENTATION_PLANNING"
    },
    {
        "finding_id": "FINDING-05",
        "severity": "MODERATE",
        "title": "Demarcação entre Contradições Reais e Contradições Aparentes no Discurso",
        "artifact_reference": "stage_31_7_31_proposition_composition_contract.md, Seção 3 e stage_31_7_32_adversarial_counterexamples.json, ADV-12 e ADV-13",
        "evidence": "Respostas dialéticas maduras frequentemente contrapõem propriedades (e.g. leitura estrita no primário vs leitura eventual nas réplicas).",
        "impact": "Detectores simplistas de contradição por operadores de negação podem punir respostas técnicas sofisticadas como se fossem inconsistentes.",
        "recommendation": "Exigir que o detector de contradição analise se as proposições com polaridades opostas compartilham o mesmo escopo condicional; havendo condições arquiteturais distintas, a resposta deve ser aceita como contextualizada.",
        "status": "OPEN_FOR_IMPLEMENTATION_PLANNING"
    },
    {
        "finding_id": "FINDING-06",
        "severity": "MINOR",
        "title": "Omissão de Campo para Registro de Contratos no Schema de Rastreabilidade",
        "artifact_reference": "stage_31_7_31_evidence_traceability_schema.json, nó final_decision",
        "evidence": "O schema JSON atual não possui um atributo explícito para listar os IDs dos contratos semânticos (e.g. SC-30) que foram validados na avaliação.",
        "impact": "Dificulta a auditoria automática de cobertura de contratos semânticos por arquivo de saída.",
        "recommendation": "Adicionar o campo opcional 'applied_contract_ids': list[str] no nó final_decision no planejamento de implementação.",
        "status": "OPEN_FOR_IMPLEMENTATION_PLANNING"
    },
    {
        "finding_id": "FINDING-07",
        "severity": "MODERATE",
        "title": "Manutenção Obrigatória da Ressalva Metodológica REFERENCE_INDEPENDENCE_UNRESOLVED",
        "artifact_reference": "GEMINI_HANDOFF.md, Seções 75 a 82; stage_31_7_31_open_questions.md, Questão 4",
        "evidence": "O benchmark de 250 casos foi desenvolvido internamente e não constitui validação independente duplo-cega.",
        "impact": "Risco de declarar sucesso definitivo com base em alinhamento a um gabarito construído no próprio ciclo de desenvolvimento.",
        "recommendation": "Preservar a ressalva REFERENCE_INDEPENDENCE_UNRESOLVED em todos os gates até a realização de validação externa independente com transcrições reais.",
        "status": "OPEN_GOVERNANCE_REQUIREMENT"
    }
]

doc = {
    "stage": "31.7.32",
    "title": "Stage 31.7.32 Independent Architecture Findings Register",
    "total_findings": len(findings),
    "summary_by_severity": {
        "BLOCKER": sum(1 for f in findings if f["severity"] == "BLOCKER"),
        "CRITICAL": sum(1 for f in findings if f["severity"] == "CRITICAL"),
        "MAJOR": sum(1 for f in findings if f["severity"] == "MAJOR"),
        "MODERATE": sum(1 for f in findings if f["severity"] == "MODERATE"),
        "MINOR": sum(1 for f in findings if f["severity"] == "MINOR")
    },
    "findings": findings,
    "audit_declaration": "Não foram encontrados BLOCKERS nem falhas CRITICAL que inviabilizem a arquitetura ou exijam rejeição da especificação. Os 2 achados MAJOR e 4 MODERATE representam decisões de design e diretrizes obrigatórias que devem ser endereçadas formalmente no plano de implementação (Stage 31.7.33) antes da modificação do runtime."
}

with open(pilot_dir / "stage_31_7_32_architecture_findings.json", "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

print(f"Generated stage_31_7_32_architecture_findings.json with {len(findings)} formal findings.")
