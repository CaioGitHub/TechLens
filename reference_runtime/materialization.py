from __future__ import annotations

from pathlib import Path
from typing import Any

from .evaluation_engine import EvaluationInput, load_pilot_input, run_evaluation_engine
from .global_audit import audit_global_output


def _fmt(value: Any) -> str:
    return str(value).replace("\n", " ").strip()


def _list(items: list[str]) -> str:
    return ", ".join(items) if items else "Nenhuma"


def _render_domains(domains: dict[str, dict[str, Any]]) -> str:
    lines = [
        "| Domínio | Avaliação | Evidência/Cobertura |",
        "|---|---|---|",
    ]
    for name, item in domains.items():
        label = name.replace("_", " ").title()
        evaluation = (
            f"{item['average_score']:.1f} / 10 "
            f"({item['question_count']} pergunta(s))"
        )
        coverage = (
            f"{item['coverage']}; "
            f"evidências: {_list(item.get('evidence_summary', []))}"
        )
        lines.append(f"| {label} | {evaluation} | {coverage} |")
    return "\n".join(lines)


def _render_complexity(complexity: dict[str, dict[str, Any]]) -> str:
    labels = {
        "basic": "Básica",
        "intermediate": "Intermediária",
        "advanced": "Avançada",
    }
    lines = [
        "| Complexidade | Avaliação |",
        "|---|---|",
    ]
    for key in ("basic", "intermediate", "advanced"):
        item = complexity[key]
        if item["coverage"] == "Not evaluated":
            assessment = "Não avaliada"
        else:
            assessment = (
                f"{item['average_score']:.1f} / 10; "
                f"{item['question_count']} pergunta(s); {item['assessment']}"
            )
        lines.append(f"| {labels[key]} | {assessment} |")
    return "\n".join(lines)


def _render_dimensions(dimensions: dict[str, dict[str, Any]]) -> str:
    headings = {
        "correctness": "Conhecimento conceitual",
        "completeness": "Completude",
        "depth": "Profundidade",
        "reasoning": "Raciocínio",
        "practical_application": "Aplicação prática",
        "trade_offs": "Trade-offs",
    }
    sections: list[str] = []
    for key, heading in headings.items():
        item = dimensions[key]
        sections.append(f"### {heading}")
        sections.append(
            f"Cobertura: {item['coverage']}; "
            f"avaliadas: {item['evaluated_count']}; "
            f"N/A: {item['not_applicable_count']}."
        )
        if item["assessments"]:
            sections.extend(f"- {_fmt(value)}" for value in item["assessments"])
        else:
            sections.append("- Não avaliada.")
        sections.append("")
    return "\n".join(sections).rstrip()


def _render_findings(items: list[dict[str, Any]], kind: str) -> str:
    lines: list[str] = []
    for item in items:
        refs = (
            f"avaliações: {_list(item.get('evaluation_ids', []))}; "
            f"perguntas: {_list(item.get('question_ids', []))}"
        )
        lines.append(f"- {item['text']} ({refs})")
    return "\n".join(lines) if lines else f"Nenhum {kind} consolidado."


def _render_traceability(traceability: dict[str, Any]) -> str:
    lines = [
        "```text",
        "Interview Evaluation v2",
        "        ↓",
        "Reference Evaluation Engine Runtime",
        "        ↓",
        "Individual Evaluations v2",
        "        ↓",
        "Evidence Set v1",
        "        ↓",
        "Structured Interview - Controlled Correction v6",
        "        ↓",
        "Transcript source",
        "```",
        "",
        f"Evaluation IDs: {_list(traceability['evaluation_ids'])}",
        f"Question IDs: {_list(traceability['question_ids'])}",
        f"Evidence IDs: {_list(traceability['evidence_ids'])}",
        "",
        "Source segments by evidence:",
    ]
    for evidence_id in traceability["evidence_ids"]:
        segments = traceability["evidence_sources"][evidence_id]
        lines.append(f"- {evidence_id}: {_list(segments)}")
    return "\n".join(lines)


def render_interview_evaluation_v2(
    output: dict[str, Any],
    *,
    audit: dict[str, Any],
    candidate: str,
    interview_date: str,
    structured_interview_source: str,
    audit_source: str,
) -> str:
    summary = output["summary"]
    confidence_label = {
        "low": "Baixa",
        "medium": "Média",
        "high": "Alta",
    }[summary["confidence"]]
    gate = (
        "AUDITED_WITH_WARNINGS"
        if output["warnings"]
        else "AUDITED"
    )
    status_line = "Audited with warnings" if output["warnings"] else "Audited"
    distribution = output["distribution"]
    errors = output["errors"]
    not_evaluated = output["not_evaluated"]
    traceability = output["traceability"]
    summary_strengths = output["strengths"][:3]
    summary_gaps = output["gaps"][:3]
    excluded = (
        "Q8, Q12, CQ1–CQ7, R24, R26, R41, R52 e "
        'R31 / "Scroll." não foram considerados avaliações ou evidências válidas.'
    )

    lines = [
        "---",
        "type: reference",
        "status: understood",
        "confidence: 100",
        "created: 2026-10-05",
        "updated: 2026-10-05",
        "tags:",
        "  - interview-evaluation",
        "  - materialized-evaluation",
        "  - stage-23-2",
        "---",
        "",
        "# Avaliação Técnica da Entrevista",
        "",
        "## Identificação",
        "",
        f"Candidato: {candidate}",
        f"Data da entrevista: {interview_date}",
        "",
        "## Proveniência",
        "",
        "Evaluation Engine: Reference Evaluation Engine Runtime",
        "Individual Evaluations: Individual Evaluations v2",
        "Evidence: Evidence Set v1",
        "Global Audit: Stage 23.1 — Global Evaluation Semantic Audit",
        f"Status: {status_line}",
        "",
        "```yaml",
        "stage: 23.2",
        "artifact_type: interview_evaluation",
        "version: 2",
        'evaluation_source: "Reference Evaluation Engine Runtime"',
        'individual_evaluations_source: "Individual Evaluations v2.md"',
        'evidence_source: "Evidence Set v1.md"',
        f'structured_interview_source: "{structured_interview_source}"',
        f'audit_source: "{audit_source}"',
        f'global_confidence: "{summary["confidence"]}"',
        f'status: "{gate}"',
        "```",
        "",
        "## Resumo",
        "",
        output["global_assessment"],
        "",
        "A consolidação registra forças, limitações e gaps somente nas perguntas e evidências avaliadas. "
        f"A cobertura compreende {summary['questions_evaluated']} perguntas e "
        f"{audit['evidence_count']} evidências, com confiança global {confidence_label.lower()}.",
        "",
        "Principais forças consolidadas:",
        *[f"- {item['text']}" for item in summary_strengths],
        "Principais gaps consolidados:",
        *[f"- {item['text']}" for item in summary_gaps],
        "Limitações principais:",
        *[f"- {item}" for item in output["limitations"]],
        "",
        "## Indicadores",
        "",
        f"Perguntas avaliadas: {summary['questions_evaluated']}",
        f"Média: {summary['average_score']:.1f} / 10",
        f"Mediana: {summary['median_score']:.1f} / 10",
        f"Mínimo: {summary['minimum_score']:.1f} / 10",
        f"Máximo: {summary['maximum_score']:.1f} / 10",
        f"Confiança global: {confidence_label}",
        f"Evidências utilizadas: {audit['evidence_count']}",
        "",
        "## Distribuição das notas",
        "",
        "| Faixa | Quantidade |",
        "|---|---:|",
        *[f"| {label} | {distribution[label]} |" for label in distribution],
        "",
        "## Desempenho por domínio",
        "",
        _render_domains(output["domains"]),
        "",
        "## Desempenho por complexidade",
        "",
        _render_complexity(output["complexity"]),
        "",
        "## Dimensões observadas",
        "",
        _render_dimensions(output["dimensions"]),
        "",
        "## Pontos fortes",
        "",
        _render_findings(output["strengths"], "ponto forte"),
        "",
        "## Gaps",
        "",
        _render_findings(output["gaps"], "gap"),
        "",
        "## Erros relevantes",
        "",
    ]
    if errors:
        for error in errors:
            lines.append(
                f"- {error['question_id']}: severidade `{error['severity']}`; "
                f"{error['description']} "
                f"(evidências: {_list(error['evidence_ids'])})"
            )
    else:
        lines.append("Nenhum erro relevante consolidado.")
    lines.extend(
        [
            "",
            "## Áreas não avaliadas",
            "",
            *[
                f"- {item['question_id']}: {item['reason']}"
                for item in not_evaluated
            ],
            "- Complexidade avançada: não avaliada.",
            "",
            "## Respostas e perguntas excluídas",
            "",
            excluded,
            "",
            "## Avaliação global",
            "",
            output["global_assessment"],
            "",
            "## Confiança da avaliação",
            "",
            f"Confiança global: {confidence_label}",
            "",
            "A confiança permanece limitada pelas advertências do Runtime: "
            + _list(output["warnings"])
            + ".",
            "",
            "## Limitações",
            "",
            *[f"- {limitation}" for limitation in output["limitations"]],
            "- A avaliação é baseada exclusivamente nas evidências estruturadas da entrevista.",
            "- O Reference Runtime é determinístico e consolida julgamentos individuais existentes; não reavalia respostas.",
            "- Ausência de evidência não foi convertida em ausência de conhecimento.",
            "",
            "## Rastreabilidade",
            "",
            _render_traceability(traceability),
            "",
            "## Gate",
            "",
            f"`INTERVIEW_EVALUATION_V2_MATERIALIZED{'_WITH_WARNINGS' if output['warnings'] else ''}`",
            "",
            "Este artefato materializa a saída auditada do Runtime. O Interview Evaluation v1 permanece preservado como histórico.",
            "",
        ]
    )
    return "\n".join(lines)


def materialize_interview_evaluation_v2(
    evaluations_path: str | Path,
    evidence_path: str | Path,
    output_path: str | Path,
    *,
    candidate: str = "Candidato-Piloto-01",
    interview_date: str = "2026-09-14",
    structured_interview_source: str = "Structured Interview - Controlled Correction v6.md",
    audit_source: str = "Stage 23.1 — Global Evaluation Semantic Audit.md",
) -> dict[str, Any]:
    input_data: EvaluationInput = load_pilot_input(evaluations_path, evidence_path)
    runtime = run_evaluation_engine(input_data)["interview_evaluation"]
    audit = audit_global_output(input_data, runtime)
    content = render_interview_evaluation_v2(
        runtime,
        audit=audit,
        candidate=candidate,
        interview_date=interview_date,
        structured_interview_source=structured_interview_source,
        audit_source=audit_source,
    )
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    temporary.replace(destination)
    return {
        "runtime": runtime,
        "audit": audit,
        "gate": (
            "INTERVIEW_EVALUATION_V2_MATERIALIZED_WITH_WARNINGS"
            if runtime["warnings"]
            else "INTERVIEW_EVALUATION_V2_MATERIALIZED"
        ),
        "content": content,
        "output_path": str(destination),
    }


__all__ = [
    "materialize_interview_evaluation_v2",
    "render_interview_evaluation_v2",
]
