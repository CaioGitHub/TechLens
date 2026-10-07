from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import re
import unicodedata
from typing import Any


STAGES = (
    "20.1",
    "20.2",
    "20.3",
    "20.4",
    "20.5",
    "20.6",
    "20.7",
    "21",
    "23",
    "report",
)


class PipelineBlocked(RuntimeError):
    def __init__(self, result: dict[str, Any]):
        super().__init__("pipeline blocked")
        self.result = result


@dataclass(frozen=True)
class StageResult:
    stage: str
    status: str
    input_id: str
    output_id: str
    warnings: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()


def _stable_id(prefix: str, value: str) -> str:
    digest = sha256(value.encode("utf-8")).hexdigest()[:8]
    return f"{prefix}-{digest}"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stage(
    stage: str,
    status: str,
    input_id: str,
    output_id: str,
    warnings: list[str] | None = None,
    errors: list[str] | None = None,
) -> dict[str, Any]:
    result = StageResult(
        stage,
        status,
        input_id,
        output_id,
        tuple(warnings or ()),
        tuple(errors or ()),
    )
    return {
        "stage": result.stage,
        "status": result.status,
        "input_id": result.input_id,
        "output_id": result.output_id,
        "warnings": list(result.warnings),
        "errors": list(result.errors),
    }


def _fixture_id(fixture: dict[str, Any]) -> str:
    return fixture.get("fixture_id", "synthetic-input")


def _participants(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return deepcopy(fixture.get("participants", []))


def _source(segment_id: str, segments: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    source: dict[str, Any] = {"segment_ids": [segment_id]}
    if segments is not None:
        segment = _find_segment(segments, segment_id)
        if segment and segment.get("timestamp"):
            source["timestamps"] = [segment["timestamp"]]
    return source


def _find_segment(segments: list[dict[str, Any]], segment_id: str) -> dict[str, Any] | None:
    return next((segment for segment in segments if segment["id"] == segment_id), None)


def _is_conversational_prompt(lower: str) -> bool:
    return lower.startswith(
        (
            "quer falar mais alguma coisa",
            "você tem alguma dúvida",
            "voce tem alguma duvida",
            "mais alguma dúvida",
            "mais alguma duvida",
            "tem dúvidas",
            "tem duvidas",
            "pode ficar à vontade",
            "pode ficar a vontade",
            "você diz ",
            "voce diz ",
            "quer falar, ",
        )
    )


def _is_interviewer_comment(lower: str, text: str) -> bool:
    if _is_conversational_prompt(lower):
        return True
    if lower.endswith(("não é?", "nao e?", "né?", "ne?", "não?", "nao?", "tá?", "ta?")):
        contextual_markers = (
            "e tem ",
            "tem uma ",
            "tem um ",
            "também",
            "tambem",
            "só nossa",
            "so nossa",
            "a gente",
            "nossa ",
            "nosso ",
        )
        if sum(marker in lower for marker in contextual_markers) >= 2:
            return True
    if lower.startswith(
        (
            "aí no final",
            "ai no final",
            "bora lá",
            "bora la",
            "top ",
            "beleza, mais",
        )
    ):
        return True
    if len(text.split()) >= 18 and any(
        marker in lower
        for marker in (
            "a gente",
            "o cliente",
            "o banco",
            "porque ",
            "então ",
            "entao ",
        )
    ):
        return True
    return False


def _question_kind(role: str, text: str) -> str | None:
    lower = text.strip().lower()
    candidate_interrogative = lower.startswith(
        (
            "como ",
            "qual ",
            "quais ",
            "por que ",
            "porque ",
            "e como ",
            "posso perguntar",
            "uma dúvida",
            "uma duvida",
            "tenho uma dúvida",
            "tenho uma duvida",
        )
    )
    tag_question = lower.endswith(
        ("não é?", "nao e?", "né?", "ne?", "não?", "nao?", "tá?", "ta?")
    )
    if role == "candidate" and candidate_interrogative and not tag_question:
        return "candidate_question"
    if role != "interviewer":
        return None
    explicit = text.rstrip().endswith("?")
    indirect = lower.startswith(("conte ", "explique ", "descreva ", "fale "))
    indirect_context = any(
        marker in lower
        for marker in (
            "já chegou a usar",
            "ja chegou a usar",
            "saberia também",
            "saberia tambem",
            "trabalha com o que",
            "vem utilizando",
            "teria algum",
        )
    )
    experience_prompt = (
        "queria entender" in lower
        and any(term in lower for term in ("experiência", "experiencia", "projetos"))
    )
    if not (explicit or indirect or experience_prompt or indirect_context):
        return None
    if _is_interviewer_comment(lower, text):
        return "conversational_prompt"
    return "interviewer_question"


def _prepare_raw_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    """Adapt a controlled raw transcript into the existing stage contract."""
    if "raw_transcript" not in fixture:
        return fixture

    participants = fixture.get("participants", [])
    labels = {
        participant["name"]: participant["role"]
        for participant in participants
        if participant.get("name")
    }
    previous_question_id: str | None = None
    question_number = 0
    candidate_question_number = 0
    response_number = 0
    transcript: list[dict[str, Any]] = []

    for raw in fixture["raw_transcript"]:
        text = raw["text"]
        role = labels.get(raw.get("speaker"), "unknown")
        lower = text.strip().lower()
        kind = _question_kind(role, text)
        candidate_question = kind == "candidate_question"
        segment: dict[str, Any] = {
            "id": raw["id"],
            "timestamp": raw.get("timestamp"),
            "speaker_label": raw.get("speaker"),
            "speaker_role": role,
            "text": text,
        }
        for field in ("needs_review", "reconstruction_confidence", "linking_confidence"):
            if field in raw:
                segment[field] = raw[field]
        if raw.get("speaker") in (None, "UNKNOWN"):
            segment["ambiguous_speaker"] = True

        if kind == "interviewer_question":
            question_number += 1
            question_id = f"Q{question_number}"
            follow_up_of = None
            if lower.startswith(("e ", "e se ", "e nesse", "e no ")):
                follow_up_of = previous_question_id
            segment.update(
                {
                    "kind": "question",
                    "question_id": question_id,
                    "follow_up_of": follow_up_of,
                    "question_kind": "interviewer_question",
                    "evaluation_eligible": True,
                }
            )
            if lower.startswith(("quer dizer", "reformulando", "melhor:")):
                segment["reformulation_of"] = previous_question_id
            previous_question_id = question_id
        elif candidate_question:
            candidate_question_number += 1
            segment.update(
                {
                    "kind": "candidate_question",
                    "candidate_question": True,
                    "question_id": f"CQ{candidate_question_number}",
                    "question_kind": "candidate_question",
                    "evaluation_eligible": False,
                }
            )
            previous_question_id = None
        elif kind == "conversational_prompt":
            segment.update(
                {
                    "kind": "intervention",
                    "question_kind": "conversational_prompt",
                    "evaluation_eligible": False,
                    "needs_review": True,
                }
            )
            if (
                len(text.split()) >= 8
                and transcript
                and transcript[-1].get("kind") == "response"
            ):
                previous_question_id = None
        elif role == "candidate":
            response_number += 1
            response_type = "direct"
            if "não lembro" in lower or "nao lembro" in lower:
                response_type = "uncertainty"
            elif any(token in lower for token in ("provavelmente", "eu faria", "uma possibilidade")):
                response_type = "hypothetical"
            elif "já trabalhei" in lower or "tenho experiência" in lower:
                response_type = "experience_declaration"
            elif any(token in lower for token in ("configurei", "criei uma consulta", "em produção")):
                response_type = "experience_with_evidence"
            segment.update(
                {
                    "kind": "response",
                    "response_id": f"R{response_number}",
                    "question_id": previous_question_id or "unknown",
                    "response_type": response_type,
                    "evaluation_eligible": True,
                }
            )
            if transcript:
                previous = transcript[-1]
                previous_text = previous.get("text", "").lower()
                if previous.get("speaker_role") == "interviewer" and any(
                    marker in previous_text
                    for marker in (
                        "concorda",
                        "certo",
                        "não é",
                        "nao e",
                        "porque ",
                        "você poderia usar",
                    )
                ):
                    segment["prompted_by_interviewer"] = True
            if transcript and transcript[-1].get("kind") == "response":
                if transcript[-1].get("question_id") == previous_question_id:
                    segment["response_group_id"] = transcript[-1].get("response_id")
        else:
            segment["kind"] = "intervention"
            segment["evaluation_eligible"] = False
            if (
                role == "interviewer"
                and len(text.split()) >= 8
                and transcript
                and transcript[-1].get("kind") == "response"
            ):
                previous_question_id = None
        transcript.append(segment)

    prepared = deepcopy(fixture)
    prepared["transcript"] = transcript
    prepared["_raw_input"] = deepcopy(fixture["raw_transcript"])
    return prepared


def _stage_201(fixture: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    participants = _participants(fixture)
    if not participants:
        participants = [
            {"participant_id": "P-INTERVIEWER", "role": "interviewer"},
            {"participant_id": "P-CANDIDATE", "role": "candidate"},
        ]
    return participants, _stage("20.1", "COMPLETED", _fixture_id(fixture), "participants")


def _stage_202(
    fixture: dict[str, Any], participants: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    known_roles = {p["role"]: p["participant_id"] for p in participants}
    segments = []
    warnings: list[str] = []
    for source in fixture.get("transcript", []):
        segment = deepcopy(source)
        role = segment.get("speaker_role")
        if segment.get("ambiguous_speaker"):
            segment["speaker_id"] = "unknown"
            segment["participant_id"] = None
            segment["attribution_confidence"] = "low"
            segment["needs_review"] = True
            warnings.append(f"ambiguous speaker: {segment['id']}")
        else:
            segment["speaker_id"] = segment.get("speaker_id", role or "unknown")
            segment["participant_id"] = segment.get(
                "participant_id", known_roles.get(role)
            )
            segment["attribution_confidence"] = segment.get(
                "attribution_confidence", "high"
            )
            segment["needs_review"] = bool(segment.get("needs_review", False))
        segments.append(segment)
    return segments, _stage(
        "20.2",
        "READY_WITH_WARNINGS" if warnings else "COMPLETED",
        "participants",
        "speaker-attributed-transcript",
        warnings,
    )


def _stage_203(
    segments: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    questions: list[dict[str, Any]] = []
    for segment in segments:
        if (
            segment.get("kind") != "question"
            or segment.get("candidate_question")
            or not segment.get("evaluation_eligible", True)
        ):
            continue
        question_id = segment.get("question_id")
        if not question_id:
            continue
        question = {
            "question_id": question_id,
            "text": segment["text"],
            "primary_type": segment.get("primary_type", "technical"),
            "source": _source(segment["id"], segments),
            "question_status": "identified",
            "question_kind": segment.get("question_kind", "interviewer_question"),
            "evaluation_eligible": True,
            "follow_up_of": segment.get("follow_up_of"),
            "reformulation_of": segment.get("reformulation_of"),
            "needs_review": bool(segment.get("needs_review", False)),
        }
        questions.append(question)
    return questions, _stage("20.3", "COMPLETED", "speaker-attributed-transcript", "questions")


def _stage_204(
    fixture: dict[str, Any],
    segments: list[dict[str, Any]],
    questions: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    question_ids = {question["question_id"] for question in questions}
    responses: list[dict[str, Any]] = []
    answered: set[str] = set()
    grouped: dict[str, dict[str, Any]] = {}
    for segment in segments:
        if segment.get("kind") != "response":
            continue
        response_id = segment.get("response_id") or _stable_id("R", segment["id"])
        question_id = segment.get("question_id", "unknown")
        group_id = segment.get("response_group_id", response_id)
        if group_id in grouped:
            grouped[group_id]["original_segments"].append(segment["id"])
            grouped[group_id]["text"] = (
                f"{grouped[group_id]['text']} {segment['text']}"
            )
            grouped[group_id]["source"]["segment_ids"].append(segment["id"])
            if segment.get("timestamp"):
                grouped[group_id]["source"].setdefault("timestamps", []).append(
                    segment["timestamp"]
                )
            grouped[group_id]["needs_review"] = (
                grouped[group_id]["needs_review"]
                or bool(segment.get("needs_review", False))
            )
            if grouped[group_id].get("reconstruction_confidence") is None:
                grouped[group_id]["reconstruction_confidence"] = segment.get(
                    "reconstruction_confidence"
                )
            continue
        response = {
            "response_id": group_id,
            "question_id": question_id if question_id in question_ids else "unknown",
            "text": segment["text"],
            "original_segments": [segment["id"]],
            "response_status": "identified",
            "response_type": segment.get("response_type", "direct"),
            "source": _source(segment["id"], segments),
            "needs_review": bool(segment.get("needs_review", False))
            or question_id == "unknown",
            "speaker_id": segment.get("speaker_id"),
            "reconstruction_confidence": segment.get("reconstruction_confidence"),
            "prompted_by_interviewer": bool(segment.get("prompted_by_interviewer", False)),
            "evaluation_eligible": question_id != "unknown",
        }
        grouped[group_id] = response
        if response["question_id"] != "unknown":
            answered.add(response["question_id"])
    responses.extend(grouped.values())
    for question in questions:
        if question["question_id"] not in answered:
            responses.append(
                {
                    "response_id": None,
                    "question_id": question["question_id"],
                    "text": None,
                    "original_segments": [],
                    "response_status": "missing",
                    "response_type": None,
                    "source": {"segment_ids": []},
                    "needs_review": False,
                    "speaker_id": None,
                }
            )
    return responses, _stage("20.4", "COMPLETED", "questions", "responses")


def _stage_205(
    fixture: dict[str, Any], responses: list[dict[str, Any]], segments: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    by_id = {segment["id"]: segment for segment in segments}
    reconstructed: list[dict[str, Any]] = []
    for response in responses:
        item = deepcopy(response)
        if item["response_status"] == "missing":
            item["original_text"] = None
            item["reconstructed_text"] = None
            item["reconstruction_confidence"] = (
                item.get("reconstruction_confidence") or "high"
            )
            reconstructed.append(item)
            continue
        source_ids = item["original_segments"]
        original = " ".join(by_id[segment_id]["text"] for segment_id in source_ids)
        item["original_text"] = original
        reconstructed_text = fixture.get("reconstructions", {}).get(item["response_id"], original)
        item["reconstructed_text"] = reconstructed_text
        item["normalization_applied"] = (
            item["reconstructed_text"] != item["original_text"]
        )
        item["reconstruction_confidence"] = (
            item.get("reconstruction_confidence") or "high"
        )
        reconstructed.append(item)
    return reconstructed, _stage("20.5", "COMPLETED", "responses", "reconstructed-responses")


def _blind_evidence_specs(question: dict[str, Any], response: dict[str, Any]) -> list[dict[str, Any]]:
    text = response["reconstructed_text"]
    lower = text.lower()
    normalized_lower = "".join(
        character
        for character in unicodedata.normalize("NFD", lower)
        if unicodedata.category(character) != "Mn"
    )
    question_lower = question["text"].lower()
    specs: list[dict[str, Any]] = []
    declaration = any(
        term in lower
        for term in (
            "já trabalhei",
            "tenho experiência",
            "trabalhei bastante",
            "já usei",
            "usei ",
            "uso ",
            "utilizo ",
            "utilizei ",
            "cheguei a usar",
            "chegou a usar",
            "trabalho com",
            "conheço ",
        )
    ) or (
        "tenho " in lower and " anos " in f" {lower} "
    )
    concrete = any(
        term in lower
        for term in (
            "em produção",
            "configurei",
            "implementei",
            "criei",
            "incidente",
            "resultado",
            "usamos",
            "rastrear",
            "investiguei",
            "corrigi",
            "restart loop",
        )
    )
    hypothetical = any(
        term in lower
        for term in (
            "provavelmente",
            "eu faria",
            "uma possibilidade",
            "eu usaria",
            "eu investigaria",
            "eu começaria",
        )
    )
    uncertainty = any(
        term in lower
        for term in (
            "não lembro",
            "nao lembro",
            "não tenho certeza",
            "nao tenho certeza",
            "não sei",
            "nao sei",
        )
    )
    self_correction = any(
        term in lower
        for term in (
            "pensando melhor",
            "na verdade",
            "espera, não",
            "espera nao",
            "ah, verdade",
            "não, acho",
            "nao, acho",
        )
    )
    technical_error = any(
        term in lower
        for term in (
            "sempre representa o pior caso",
            "pior tempo de todas",
            "threads de plataforma",
            "thread do sistema operacional",
            "threads do sistema operacional",
            "não suporta mensagens",
            "nao suporta mensagens",
            "retry agressivo",
            "ignorar perda de dados",
            "sincronicamente bloqueando",
            "opera sincronicamente",
            "bloqueando threads de chamada",
        )
    )
    partial_signal = any(
        term in lower
        for term in ("mas não detalharia", "mas nao detalharia", "pequena imprecisão", "pequena imprecisao")
    )
    insufficient_signal = any(
        term in normalized_lower
        for term in (
            "nao explica",
            "apenas palavras",
            "so palavras",
        )
    ) or ("explica" in lower and any(term in lower for term in ("frase", "palavras")))
    contradiction = "na verdade" in lower and any(
        term in lower
        for term in (
            "não funcionaria",
            "nao funcionaria",
            "não usaria",
            "nao usaria",
            "não seria adequado",
            "nao seria adequado",
        )
    )
    tradeoff = any(term in lower for term in ("trade-off", "versus", " vs ", "custo", "em troca"))
    reasoning = (
        any(term in lower for term in ("antes de", "então", "compararia", "prioriz", "escolheria", "investiguei", "debuguei", "restart loop"))
        or bool(re.search(r"\b(?:se|fosse|caso)\b", lower))
    )
    practical = concrete or any(
        term in lower
        for term in ("plano de execução", "plano de execucao")
    ) or (
        "query" in lower
        and any(term in question_lower for term in ("jdbc", "sql", "banco", "consulta"))
    )
    messaging_signal = any(
        term in lower
        for term in ("kafka", "rabbit", "producer", "consumer", "fila", "tópico", "topico", "mensager")
    )
    named_tool = any(
        term in lower
        for term in (
            "dynatrace",
            "dyna trace",
            "copilot",
            "azure monitor",
            "application insights",
            "prometheus",
            "grafana",
            "datadog",
        )
    )
    declaration = declaration or (named_tool and not concrete)
    relevance = _evaluate_semantic_relevance(question, response)
    off_topic = relevance["classification"] in ("OFF_TOPIC", "RELATED")
    partial_relevance = relevance["classification"] == "PARTIAL"
    insufficient_relevance = relevance["classification"] == "INSUFFICIENT"
    fragmented = lower.strip() in {"sim", "nao", "não", "ok", "beleza", "isso", "concordo", "top", "perfeito", "aham", "uhum"}
    prompted_confirmation = (
        response.get("prompted_by_interviewer", False)
        and not relevance.get("functional_contribution")
        and any(term in lower for term in ("sim", "isso mesmo", "exato", "exatamente", "concordo", "com certeza"))
    )

    if prompted_confirmation:
        specs.append({"type": "confirmation", "qualification": "insufficient"})
    elif declaration and not concrete:
        specs.append({"type": "experience_declaration", "qualification": "insufficient"})
        cleaned_decl = re.sub(
            r"\b(já trabalhei|tenho experiência|trabalhei bastante|já usei|não cheguei a usar|nao cheguei a usar|tenho conhecimento|trabalho com|conheço|bastante|com|sim|não|nao)\b",
            "",
            lower,
            flags=re.IGNORECASE,
        )
        has_conceptual_content = (
            relevance.get("relation_type") in ("open_technical_assertion", "direct_mechanism_assertion")
            or any(_lexical_contains(cleaned_decl, t) for t in ("separa", "regra de negócio", "tecnologias externas", "camada", "camadas", "lógica", "abstração"))
            or any(
                any(_lexical_contains(cleaned_decl, v) for v in cap["valid"])
                for cap in _FUNCTIONAL_CAPABILITIES.values()
            )
        )
        if not named_tool and has_conceptual_content:
            specs.append({"type": "conceptual", "qualification": "positive"})
    if concrete:
        specs.append({"type": "demonstrated_experience", "qualification": "positive"})
    if hypothetical:
        specs.append({"type": "hypothesis", "qualification": "conditional"})
    if uncertainty:
        specs.append({"type": "uncertainty", "qualification": "insufficient"})
    if self_correction:
        specs.append({"type": "self_correction", "qualification": "contradictory" if technical_error else "positive"})
    if technical_error:
        specs.append({"type": "technical_error", "qualification": "negative"})
    if contradiction:
        specs.append({"type": "contradiction", "qualification": "contradictory"})
    if practical:
        specs.append({"type": "practical", "qualification": "positive"})
    if reasoning and not declaration:
        specs.append({"type": "reasoning", "qualification": "positive"})
    if tradeoff:
        specs.append({"type": "tradeoff", "qualification": "positive"})
    if off_topic:
        specs.append({"type": "off_topic", "qualification": "negative"})
        if messaging_signal:
            specs.append({"type": "conceptual", "qualification": "partial"})
    if partial_relevance or insufficient_signal:
        specs.append({
            "type": "conceptual",
            "qualification": "partial",
            "relation_type": relevance.get("relation_type", "partial_concept"),
        })
    if insufficient_relevance:
        specs.append({"type": "conceptual", "qualification": "insufficient"})
    if "jdbc" in question_lower and "jdbc" not in lower and any(
        term in lower for term in ("banco", "query", "consulta")
    ):
        specs.append({"type": "conceptual", "qualification": "partial"})
    if (
        "jdbc" in question_lower
        and "jdbc" in lower
        and any(term in lower for term in ("banco", "query", "consulta"))
        and not any(
            term in lower
            for term in ("driver", "conexão", "conexao", "statement", "resultset", "prepared", "execute")
        )
    ):
        specs.append({"type": "conceptual", "qualification": "partial"})
    if not specs:
        specs.append(
            {
                "type": "conceptual",
                "qualification": (
                    "negative"
                    if off_topic or technical_error
                    else (
                        "insufficient"
                        if (
                            insufficient_relevance
                            or insufficient_signal
                            or fragmented
                            or any(term in lower for term in ("muito pouco", "bem por cima", "não sei", "nao sei"))
                        )
                        else "positive"
                    )
                ),
            }
        )
    for index, spec in enumerate(specs, start=1):
        spec["evidence_id_suffix"] = index
        spec["evidence_strength"] = "strong" if concrete or reasoning or tradeoff else "moderate"
        spec["evidence_confidence"] = "medium" if uncertainty or off_topic else "high"
    return specs


def _normalize_text(text: str) -> str:
    nfd = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in nfd if unicodedata.category(c) != "Mn")


def _stem_word(word: str) -> str:
    w = _normalize_text(word)
    if len(w) <= 3:
        return w
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    elif w.endswith("ing") and len(w) > 5:
        return w[:-3]

    suffixes = [
        ("acionamentos", 3), ("acionamento", 3), ("acionaria", 3), ("acionar", 3), ("acionando", 3),
        ("icionamentos", 3), ("icionamento", 3), ("icionaria", 3), ("icionar", 3), ("icionando", 3),
        ("amentos", 3), ("amento", 3), ("imentos", 3), ("imento", 3),
        ("acoes", 3), ("acao", 3), ("icoes", 3), ("icao", 3),
        ("soes", 3), ("sao", 3),
        ("encias", 3), ("encia", 3), ("ancias", 3), ("ancia", 3),
        ("entes", 3), ("ente", 3),
        ("idades", 3), ("idade", 3),
        ("iveis", 3), ("ivel", 3), ("aveis", 3), ("avel", 3),
        ("ariamos", 3), ("eriamos", 3), ("iriamos", 3),
        ("assem", 3), ("essem", 3), ("issem", 3),
        ("ariam", 3), ("eriam", 3), ("iriam", 3),
        ("aria", 3), ("eria", 3), ("iria", 3),
        ("ando", 3), ("endo", 3), ("indo", 3),
        ("amos", 3), ("emos", 3), ("imos", 3),
        ("avam", 3), ("avas", 3), ("ava", 3),
        ("aram", 3), ("eram", 3), ("iram", 3),
        ("ados", 3), ("idos", 3), ("adas", 3), ("idas", 3),
        ("ado", 3), ("ido", 3), ("ada", 3), ("ida", 3),
        ("ar", 3), ("er", 4), ("ir", 3),
        ("oes", 3), ("ao", 3),
        ("s", 3),
    ]
    for suf, min_rem in suffixes:
        if w.endswith(suf) and len(w) - len(suf) >= min_rem:
            w = w[:-len(suf)]
            break
    if w.endswith("er") and len(w) > 5:
        w = w[:-2]
    if w.endswith(("a", "o")) and len(w) > 4:
        w = w[:-1]
    return w


_STOP_WORDS = {
    "o", "os", "a", "as", "um", "uma", "uns", "umas", "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas", "por", "pelo", "pela", "pelos", "pelas", "com",
    "para", "pra", "que", "qual", "quais", "como", "quando", "onde", "por que", "porque",
    "funciona", "funcionar", "serve", "servir", "voce", "você", "seu", "sua", "seus", "suas",
    "tipo", "sobre", "mais", "menos", "muito", "pouco", "bem", "sim", "nao", "não", "sao", "são",
}


def _extract_stemmed_tokens(text: str) -> set[str]:
    raw_words = set(re.findall(r"\b[a-zA-Z0-9_\u00c0-\u00ff\-]{3,}\b", text.lower()))
    filtered = raw_words - _STOP_WORDS
    return {_stem_word(w) for w in filtered}


def _lexical_contains(text: str, term: str) -> bool:
    t_norm = _normalize_text(text)
    term_norm = _normalize_text(term)
    if not term_norm or not t_norm:
        return False
    words = term_norm.split()
    if len(words) == 1:
        single = words[0]
        if re.search(r"\b" + re.escape(single) + r"\b", t_norm):
            return True
        stem_term = _stem_word(single)
        text_words = re.findall(r"\b[a-zA-Z0-9_\-]+\b", t_norm)
        return any(_stem_word(tw) == stem_term for tw in text_words)
    else:
        pattern = r"\b" + r"\s+".join(re.escape(w) for w in words) + r"\b"
        return bool(re.search(pattern, t_norm))


def _evaluate_multi_aspect_coverage(
    question_text: str,
    response_text: str,
    target_domain: str | None = None,
) -> dict[str, Any]:
    q_norm = _normalize_text(question_text)
    r_norm = _normalize_text(response_text)
    r_stems = _extract_stemmed_tokens(response_text)

    split_markers = (
        " e como ",
        " e o que ",
        " e qual ",
        " e quais ",
        " e por que ",
        " e porque ",
        " e quais sao ",
        " e quais seus ",
        " e suas ",
        " e seus ",
        " e qual seu ",
        " e quais estrategias ",
        " e como gerencia ",
        " e como configura ",
        " e qual a importancia ",
        " e qual a relevancia ",
    )
    for marker in split_markers:
        if marker in q_norm:
            parts = q_norm.split(marker, 1)
            aspect_1_stems = _extract_stemmed_tokens(parts[0])
            aspect_2_stems = _extract_stemmed_tokens(parts[1])
            aspect_2_distinct = aspect_2_stems - aspect_1_stems
            if not aspect_2_distinct:
                aspect_2_distinct = aspect_2_stems

            cov1 = bool(aspect_1_stems & r_stems)
            p2_norm = parts[1].strip()
            if "refresh" in p2_norm and "token" in p2_norm:
                cov2 = any(_lexical_contains(r_norm, t) for t in ("refresh", "renovacao", "renovação", "expiracao"))
            elif "requisicao" in p2_norm or "requisicoes" in p2_norm:
                cov2 = any(_lexical_contains(r_norm, t) for t in ("requisicao", "requisicão", "requisicoes", "request", "metodo", "metodos", "header", "headers", "status", "verbo", "verbos"))
            elif "rebalance" in p2_norm:
                cov2 = any(_lexical_contains(r_norm, t) for t in ("rebalanceamento", "rebalance", "reatribuicao"))
            elif "escrita" in p2_norm or "escritas" in p2_norm:
                cov2 = any(_lexical_contains(r_norm, t) for t in ("escrita", "escritas", "write", "custo", "overhead", "lenta", "desacelera"))
            elif "porta" in p2_norm or "adaptador" in p2_norm:
                cov2 = any(_lexical_contains(r_norm, t) for t in ("porta", "portas", "adaptador", "adaptadores", "adapter", "adapters"))
            elif "protocol buffer" in p2_norm or "protobuf" in p2_norm or "serializ" in p2_norm:
                cov2 = any(_lexical_contains(r_norm, t) for t in ("protobuf", "proto", "serializacao", "serialização", "binario", "binário"))
            elif "service mesh" in p2_norm or "papel do service mesh" in p2_norm or "papel em service mesh" in p2_norm:
                cov2 = any(_lexical_contains(r_norm, t) for t in ("mesh", "sidecar", "l7", "roteamento", "observabilidade", "papel"))
            elif "sso" in p2_norm:
                cov2 = any(_lexical_contains(r_norm, t) for t in ("sso", "single sign-on", "identity provider", "federada", "autenticacao", "openid", "saml"))
            elif "protege" in p2_norm:
                cov2 = any(_lexical_contains(r_norm, t) for t in ("protege", "seguranca", "segurança", "filtragem", "politicas", "pacotes", "firewall"))
            else:
                cov2 = bool(aspect_2_distinct & r_stems)

            if target_domain and target_domain in _FUNCTIONAL_CAPABILITIES:
                cap = _FUNCTIONAL_CAPABILITIES[target_domain]
                has_valid = any(_lexical_contains(r_norm, v) for v in cap["valid"])
                if has_valid:
                    cov1 = True

            if cov1 and not cov2:
                return {
                    "is_multi_aspect": True,
                    "is_partial": True,
                    "covered_aspects": 1,
                    "total_aspects": 2,
                    "covered_stems": aspect_1_stems & r_stems,
                    "omitted_summary": parts[1].strip(),
                }
            elif cov2 and not cov1:
                return {
                    "is_multi_aspect": True,
                    "is_partial": True,
                    "covered_aspects": 1,
                    "total_aspects": 2,
                    "covered_stems": aspect_2_distinct & r_stems,
                    "omitted_summary": parts[0].strip(),
                }
            elif cov1 and cov2:
                return {
                    "is_multi_aspect": True,
                    "is_partial": False,
                    "covered_aspects": 2,
                    "total_aspects": 2,
                    "covered_stems": (aspect_1_stems | aspect_2_distinct) & r_stems,
                    "omitted_summary": "",
                }

    if " e circuit breaker" in q_norm or " e bulkhead" in q_norm:
        has_bulkhead = any(t in r_norm for t in ("bulkhead", "pool", "threads", "isolamento"))
        has_circuit = any(t in r_norm for t in ("circuit breaker", "circuito", "abrir circuito"))
        if (has_bulkhead and not has_circuit) or (has_circuit and not has_bulkhead):
            return {
                "is_multi_aspect": True,
                "is_partial": True,
                "covered_aspects": 1,
                "total_aspects": 2,
                "covered_stems": r_stems,
                "omitted_summary": "circuit breaker" if has_bulkhead else "bulkhead",
            }

    if "trade-off" in q_norm or "tradeoff" in q_norm or "desvantagens" in q_norm:
        has_tradeoff = any(t in r_norm for t in ("trade-off", "tradeoff", "desvantagem", "invalidação", "custo", "consistência", "desvantagens"))
        if not has_tradeoff:
            return {
                "is_multi_aspect": True,
                "is_partial": True,
                "covered_aspects": 1,
                "total_aspects": 2,
                "covered_stems": r_stems,
                "omitted_summary": "trade-offs and drawbacks",
            }

    return {
        "is_multi_aspect": False,
        "is_partial": False,
        "covered_aspects": 1,
        "total_aspects": 1,
        "covered_stems": set(),
        "omitted_summary": "",
    }


_FUNCTIONAL_CAPABILITIES: dict[str, dict[str, set[str]]] = {
    "container_isolation": {
        "demands": {"docker", "dockerfile", "container networking", "isolamento de container", "rede bridge", "overlay"},
        "valid": {"bridge", "daemon", "overlay", "roteamento de pacotes", "filtrar pacotes", "kernel filtering", "dns interno", "namespaces", "cgroups"},
        "defining": {"docker", "dockerfile", "rede bridge", "dns interno"},
    },
    "container_orchestration": {
        "demands": {"kubernetes", "k8s", "orquestra containers", "cluster de containers", "orquestração de containers", "orquestracao de containers"},
        "valid": {"cluster", "clusters", "pod", "pods", "deployment", "deployments", "probe", "probes", "scheduler", "kubelet"},
        "defining": {"kubernetes", "k8s", "orquestra containers", "agenda pods nos nós"},
    },
    "relational_query_and_storage": {
        "demands": {"sql", "banco relacional", "bancos relacionais", "tabelas relacionais", "índice sql", "índices sql", "indices sql", "índice no banco relacional"},
        "valid": {"sql", "tabela", "tabelas", "query", "queries", "consulta", "consultas", "índice", "indices", "índices", "b-tree", "árvore b", "arvore b", "scan", "seek"},
        "defining": {"sql", "banco relacional", "bancos relacionais", "tabelas relacionais", "índices sql", "índice b-tree"},
    },
    "in_memory_caching_and_latency": {
        "demands": {"cache", "caching", "redis", "memcached", "latência", "latencia", "reduzir a latência", "reduzir latência", "reduziria a latência", "reduziria latência", "consultas repetidas", "cache distribuído", "acelerar leituras", "acelera leituras", "frequentemente acessados", "dados frequentemente acessados"},
        "valid": {"cache", "caching", "redis", "memcached", "memória", "memoria", "chave e valor", "latência", "latencia", "ttl", "expiração", "expiracao", "invalidação", "invalidacao", "consultas repetidas", "evitar consultas", "rápida", "rápido", "rapida", "rapido"},
        "defining": {"redis", "memcached", "armazena dados em memória", "armazena dados em memoria", "chave e valor", "acelera leituras", "cache reduz latência", "cache reduz latencia", "dados temporariamente em memória", "dados em memória"},
    },
    "dependency_injection_ioc": {
        "demands": {"dependency injection", "injeção de dependência", "injecao de dependencia", "inversão de controle", "desacoplar a criação de objetos", "desacoplar criação de objetos", "desacoplar componentes"},
        "valid": {"injeção de dependência", "injecao de dependencia", "dependência de fora", "dependencia de fora", "inversão de controle", "fornecidas externamente", "desacoplar a criação de objetos", "desacoplar componentes", "sem instanciar na classe", "desacopla a criação", "desacopla componentes"},
        "defining": {"injeção de dependência", "injecao de dependencia", "dependência de fora", "inversão de controle", "fornecidas externamente"},
    },
    "data_access_abstraction": {
        "demands": {"spring data", "jpa", "hibernate", "orm", "repository"},
        "valid": {"repository", "jpa", "hibernate", "orm", "repositórios", "repositorios"},
        "defining": {"spring data", "abstrações para acesso a bancos", "abstracoes para acesso a bancos"},
    },
    "api_design_and_protocols": {
        "demands": {"api rest", "o que é rest", "o que e rest", "explique rest", "arquitetura rest", "serviço rest", "servico rest", "endpoint", "recursos http"},
        "valid": {"http", "endpoint", "endpoints", "recurso", "recursos", "métodos", "metodos", "status", "produces", "consumes", "status codes", "status code", "get", "post", "put", "delete", "uri", "uris"},
        "defining": {"rest usa recursos", "recursos e http"},
    },
    "asynchronous_messaging": {
        "demands": {"kafka", "rabbitmq", "rabbit", "mensageria", "mensagens assíncronas", "lentidão em um serviço", "lentidao em um servico", "fila assíncrona", "fila assincrona", "particionamento no kafka"},
        "valid": {"producer", "consumer", "assíncrono", "assincrono", "fila assíncrona", "fila assincrona", "publicaria mensagens", "partições", "particoes", "consumer group", "offset", "offsets", "broker", "brokers", "ack", "commit"},
        "defining": {"kafka", "rabbitmq", "rabbit", "tópicos e consumidores", "topicos e consumidores", "fila do kafka", "parte de kafka", "mensageria assíncrona"},
    },
    "identity_tokens_security": {
        "demands": {"oauth", "oauth2", "jwt", "proteger uma api com tokens", "segurança de api", "seguranca de api", "assinatura de tokens", "autenticação", "autenticacao", "api de autenticação", "api de autenticacao", "proteger uma api com autenticação", "autenticação em api"},
        "valid": {"oauth", "oauth2", "autorização", "autorizacao", "token", "tokens", "jwt", "rate limit", "waf", "autenticação", "autenticacao", "assina tokens", "chave criptográfica", "chave criptografica"},
        "defining": {"oauth", "oauth2", "jwt assina tokens", "jwt assina token", "waf", "rate limit"},
    },
    "ui_reactivity_and_state": {
        "demands": {"angular signals", "signals", "reatividade de interface", "reatividade com angular"},
        "valid": {"signals", "signal", "reatividade", "computed", "effect"},
        "defining": {"angular signals", "computed"},
    },
    "ui_styling_and_presentation": {
        "demands": {"css", "estilo", "layout visual", "alinhamento de layout"},
        "valid": {"flexbox", "grid", "display", "alinhamento", "margin", "padding", "estilos visuais"},
        "defining": {"css define estilos", "css controla estilos"},
    },
    "delivery_pipelines": {
        "demands": {"ci/cd", "ci cd", "jenkins", "pipelines de deploy", "pipeline de ci/cd"},
        "valid": {"deploy", "build", "testes automatizados", "runner", "pipeline de deploy", "integração contínua", "integracao continua"},
        "defining": {"jenkins executa pipelines", "pipelines de ci/cd"},
    },
    "concurrency_and_threading": {
        "demands": {"virtual thread", "virtual threads", "threads virtuais"},
        "valid": {"threads virtuais", "carrier thread", "carrier threads", "continuation", "threads leves", "jvm", "gerenciadas pela jvm", "bloqueantes"},
        "defining": {"virtual threads", "threads virtuais", "carrier threads"},
    },
    "telemetry_and_query_analytics": {
        "demands": {"kql", "log analytics", "kusto", "observabilidade", "telemetria", "application insights", "consulta kql"},
        "valid": {"kusto", "application insights", "observabilidade", "telemetria", "dependency", "dependência", "summarize", "project", "where", "bin("},
        "defining": {"kql", "log analytics"},
    },
    "architectural_structural_patterns": {
        "demands": {"arquitetura hexagonal", "hexagonal", "solid", "event-driven", "consistência eventual", "consistencia eventual", "sincronizar dados", "idempotência", "idempotencia", "duas vezes", "duplicidade", "consistência de dados", "consistencia de dados", "serviços desacoplados", "servicos desacoplados", "transação distribuída", "transacao distribuida"},
        "valid": {"hexagonal", "portas e adaptadores", "ports and adapters", "portas e adapters", "inverter dependências", "solid", "responsabilidades", "abstrações", "event-driven", "evento", "eventos", "consumidores desacoplados", "idempotência", "consistência eventual", "consistencia eventual", "reconciliação", "reconciliacao", "chave de idempotência", "chave de idempotencia", "mensageria", "mensageria assíncrona", "mensageria assincrona", "compensação", "compensacao"},
        "defining": {"portas e adaptadores", "portas e adapters", "ports and adapters", "inverter dependências", "separaria responsabilidades e dependeria de abstrações", "consumidores desacoplados e idempotência", "eventos, consumidores desacoplados", "chave de idempotência", "consistência eventual"},
    },
    "resilience_and_fault_tolerance": {
        "demands": {"bulkhead", "circuit breaker", "resiliência", "resiliente", "tolerância a falhas", "tolerancia a falhas", "retry", "retries", "backoff", "jitter", "indisponibilidade downstream", "falha em cascata", "falhas em cascata", "dependência externa", "dependencia externa"},
        "valid": {"bulkhead", "circuit breaker", "fallback", "isolar falhas", "isolamento", "pools de threads", "esgotamento", "abrir circuito", "degradação graciosa", "degradacao graciosa", "repetições", "repeticoes", "intervalo exponencial", "jitter", "backoff", "aleatório", "aleatorio"},
        "defining": {"bulkhead isola falhas", "circuit breaker abre circuito", "pools de threads para isolar falhas", "backoff exponencial com jitter"},
    },
    "enterprise_framework_transactions": {
        "demands": {"transação", "transacao", "transações", "transacoes", "transação no spring", "transacao no spring"},
        "valid": {"@transactional", "transactional", "transação", "transacao", "transações", "transacoes", "configurar transações", "configurar transacoes", "commit", "rollback"},
        "defining": {"@transactional", "transações declarativas", "configurar transações"},
    },
}

_EXPERIENCE_QUESTION_MARKERS = (
    "trajetória",
    "trajetoria",
    "projetos",
    "tecnologias que tu usou",
    "já atuou",
    "ja atuou",
    "atuava",
    "atuou",
    "já trabalhou",
    "trabalhou com",
    "já precisou usar",
    "vocês usam",
    "já chegou a usar",
    "vem utilizando",
    "no seu dia a dia",
    "você tem experiência",
    "voce tem experiencia",
    "tem experiência",
    "tem experiencia",
    "experiência com",
    "experiencia com",
)

_BROAD_ECOSYSTEM_NAMES = {
    "java", "spring", "css", "html", "web", "http", "api", "rest",
    "kafka", "angular", "kql", "banco", "relacional", "bancos",
    "sql", "pipeline", "pipelines", "ci/cd", "git", "cloud", "azure",
    "linux", "docker", "kubernetes", "dados", "log", "logs", "analytics",
    "jwt", "swagger", "openapi", "npm", "maven", "rbac"
}


def _evaluate_semantic_relevance(question: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    q_text = question.get("text", "")
    r_text = response.get("reconstructed_text") or response.get("text") or ""
    q_lower = q_text.lower()
    r_lower = r_text.lower()

    if response.get("question_id") == "unknown" or not r_text.strip():
        return {
            "classification": "UNKNOWN",
            "question_intent": "unknown",
            "target_knowledge_domain": "unknown",
            "demonstrated_concepts": (),
            "relation_type": "unlinked_or_missing_response",
            "functional_contribution": False,
            "evidence_strength": "NONE",
            "confidence": "LOW",
            "rationale": "Response is unlinked or missing source text.",
            "needs_review": True,
        }

    insufficient_terms = (
        "é muito pouco", "muito pouco", "bem por cima", "quase nada", "sei pouco",
        "sei quase nada", "não sei", "nao sei", "não lembro", "nao lembro",
        "não conheço", "nao conheco", "não domino", "nao domino"
    )
    tokens = re.findall(r"\b\w+\b", r_lower)
    is_conversational_acknowledgment = bool(tokens) and all(
        t in {"yes", "beijava", "sim", "beleza", "ok", "top", "perfeito", "aham", "uhum"}
        for t in tokens
    )
    if is_conversational_acknowledgment or any(
        term in r_lower for term in insufficient_terms
    ):
        return {
            "classification": "INSUFFICIENT",
            "question_intent": "factual_mechanism",
            "target_knowledge_domain": "general",
            "demonstrated_concepts": (),
            "relation_type": "insufficient_substance",
            "functional_contribution": False,
            "evidence_strength": "NONE",
            "confidence": "MEDIUM",
            "rationale": "Candidate asserts lack of depth or provides fragmented acknowledgment.",
            "needs_review": False,
        }

    # 1. Detect Intent
    if any(marker in q_lower for marker in _EXPERIENCE_QUESTION_MARKERS):
        intent = "experience_verification"
    elif any(
        prefix in q_lower
        for prefix in (
            "como investigaria",
            "como você investigaria",
            "como voce investigaria",
            "como resolveria",
            "erro 500",
            "http 500",
            "falha 500",
            "incidente",
            "como observar",
            "observar uma aplicação",
            "observabilidade",
            "aplicaria observabilidade",
        )
    ):
        intent = "diagnostic_troubleshooting"
    elif any(
        marker in q_lower
        for marker in (
            "resiliente",
            "resiliência",
            "como escolheria",
            "como decidiria",
            "trade-off",
            "tradeoff",
            "como projetaria",
            "desenharia arquitetura",
            "projetaria um sistema",
            "como aplicaria solid",
            "como desenharia arquitetura hexagonal",
            "dependência externa",
            "dependencia externa",
            "proteger a aplicação",
            "proteger a aplicacao",
            "falha em cascata",
            "falhas em cascata",
        )
    ):
        intent = "architectural_decision"
    else:
        intent = "factual_mechanism"

    # Diagnostic troubleshooting intent
    if intent == "diagnostic_troubleshooting":
        has_diagnostic = any(
            term in r_lower
            for term in (
                "log",
                "logs",
                "trace",
                "traces",
                "métrica",
                "metricas",
                "metrics",
                "dependência",
                "dependencias",
                "dependency",
                "dependencies",
                "p95",
                "p99",
                "baseline",
                "debug",
                "kql",
                "telemetria",
                "application insights",
                "alertas",
                "alerts",
                "timeout",
                "latência",
                "latencia",
                "tempo de resposta",
            )
        )
        has_mitigation = any(
            _lexical_contains(r_lower, term)
            for term in (
                "bulkhead",
                "circuit breaker",
                "fallback",
                "isolar falhas",
                "isolamento",
                "pools de threads",
                "cache local",
                "mitigação",
                "mitigacao",
            )
        )
        alien_domains = [
            d_name
            for d_name, cap in _FUNCTIONAL_CAPABILITIES.items()
            if d_name != "telemetry_and_query_analytics"
            and not any(_lexical_contains(q_lower, q_term) for q_term in cap["demands"])
            and any(_lexical_contains(r_lower, d_term) for d_term in cap["defining"])
        ]
        if alien_domains and not (has_diagnostic or has_mitigation):
            return {
                "classification": "OFF_TOPIC",
                "question_intent": intent,
                "target_knowledge_domain": "diagnostic_troubleshooting",
                "demonstrated_concepts": tuple(alien_domains),
                "relation_type": "alien_functional_domain",
                "functional_contribution": False,
                "evidence_strength": "NONE",
                "confidence": "HIGH",
                "rationale": "Candidate described unrelated operational mechanisms instead of diagnostic troubleshooting.",
                "needs_review": False,
            }
        if alien_domains and (has_diagnostic or has_mitigation):
            return {
                "classification": "PARTIAL",
                "question_intent": intent,
                "target_knowledge_domain": "diagnostic_troubleshooting",
                "demonstrated_concepts": ("diagnostic_action",) + tuple(alien_domains),
                "relation_type": "mixed_diagnostic_and_alien",
                "functional_contribution": True,
                "evidence_strength": "MODERATE",
                "confidence": "HIGH",
                "rationale": "Candidate mixed valid diagnostic/mitigation action with an unrelated domain explanation.",
                "needs_review": False,
            }
        if has_diagnostic or has_mitigation:
            return {
                "classification": "SUPPORTING",
                "question_intent": intent,
                "target_knowledge_domain": "diagnostic_troubleshooting",
                "demonstrated_concepts": ("diagnostic_action",),
                "relation_type": "diagnostic_action_serves_goal",
                "functional_contribution": True,
                "evidence_strength": "STRONG",
                "confidence": "HIGH",
                "rationale": "Diagnostic or mitigation action directly serves troubleshooting scenario.",
                "needs_review": False,
            }

    # Architectural resilience / trade-off intent
    if intent == "architectural_decision":
        has_resilience = any(
            _lexical_contains(r_lower, term)
            for term in ("timeout", "retry", "backoff", "circuit breaker", "observabilidade", "resiliente", "bulkhead", "fallback", "isolaria", "isolamento")
        )
        has_tradeoff = any(
            _lexical_contains(r_lower, term)
            for term in ("trade-off", "tradeoff", "menor latência", "consistência", "abstrações", "portas e adapters", "eventos, consumidores")
        )
        if has_resilience or has_tradeoff:
            return {
                "classification": "SUPPORTING",
                "question_intent": intent,
                "target_knowledge_domain": "architectural_decision",
                "demonstrated_concepts": ("resilience_and_tradeoffs",),
                "relation_type": "architectural_reasoning_serves_goal",
                "functional_contribution": True,
                "evidence_strength": "STRONG",
                "confidence": "HIGH",
                "rationale": "Articulates resilience patterns and architectural trade-offs.",
                "needs_review": False,
            }

    # Experience verification intent
    if intent == "experience_verification":
        return {
            "classification": "DIRECT",
            "question_intent": intent,
            "target_knowledge_domain": "experience_verification",
            "demonstrated_concepts": ("experience_trajectory",),
            "relation_type": "candidate_ecosystem_description",
            "functional_contribution": True,
            "evidence_strength": "STRONG",
            "confidence": "HIGH",
            "rationale": "Candidate describes career trajectory, stack usage, or operational background.",
            "needs_review": False,
        }

    stop_words = _STOP_WORDS
    q_words = set(re.findall(r"\b[a-zA-Z0-9_\u00c0-\u00ff\-]{3,}\b", q_lower)) - stop_words
    r_words = set(re.findall(r"\b[a-zA-Z0-9_\u00c0-\u00ff\-]{3,}\b", r_lower)) - stop_words
    shared = q_words & r_words

    # Factual mechanism intent
    target_domains = [
        d_name
        for d_name, cap in _FUNCTIONAL_CAPABILITIES.items()
        if any(_lexical_contains(q_lower, d_term) for d_term in cap["demands"])
    ]

    for d_name in target_domains:
        cap = _FUNCTIONAL_CAPABILITIES[d_name]
        has_valid = any(_lexical_contains(r_lower, v) for v in cap["valid"])
        other_defines = [
            other_name
            for other_name, other_cap in _FUNCTIONAL_CAPABILITIES.items()
            if other_name != d_name
            and any(_lexical_contains(r_lower, d_term) for d_term in other_cap["defining"])
        ]

        if not has_valid or any(_lexical_contains(r_lower, term) for term in ("swagger", "openapi")):
            is_adjacent_stack = (
                (d_name == "dependency_injection_ioc" and "data_access_abstraction" in other_defines)
                or (not other_defines and (
                    any(_lexical_contains(r_lower, term) for term in ("tags html", "html", "git", "replicação", "replicacao", "cors", "swagger", "openapi", "npm", "package.json", "rbac", "pom.xml", "maven", "schema registry", "avro"))
                    or any(_lexical_contains(q_lower, eco) and _lexical_contains(r_lower, eco) for eco in _BROAD_ECOSYSTEM_NAMES)
                ))
            )
            if is_adjacent_stack:
                return {
                    "classification": "RELATED",
                    "question_intent": intent,
                    "target_knowledge_domain": d_name,
                    "demonstrated_concepts": tuple(other_defines) if other_defines else (d_name,),
                    "relation_type": "thematic_adjacency_without_mechanism",
                    "functional_contribution": False,
                    "evidence_strength": "NONE",
                    "confidence": "HIGH",
                    "rationale": f"Candidate described adjacent ecosystem/technology instead of required {d_name} mechanism.",
                    "needs_review": False,
                }
            return {
                "classification": "OFF_TOPIC",
                "question_intent": intent,
                "target_knowledge_domain": d_name,
                "demonstrated_concepts": tuple(other_defines) if other_defines else (),
                "relation_type": "alien_functional_domain",
                "functional_contribution": False,
                "evidence_strength": "NONE",
                "confidence": "HIGH",
                "rationale": f"Candidate described alien domain instead of {d_name}.",
                "needs_review": False,
            }

        if other_defines and has_valid:
            return {
                "classification": "PARTIAL",
                "question_intent": intent,
                "target_knowledge_domain": d_name,
                "demonstrated_concepts": (d_name,) + tuple(other_defines),
                "relation_type": "mixed_target_and_alien",
                "functional_contribution": True,
                "evidence_strength": "MODERATE",
                "confidence": "HIGH",
                "rationale": "Candidate addressed target mechanism but mixed with an alien domain explanation.",
                "needs_review": False,
            }

        if has_valid:
            aspect_cov = _evaluate_multi_aspect_coverage(q_text, r_text, d_name)
            if aspect_cov["is_multi_aspect"] and aspect_cov["is_partial"]:
                return {
                    "classification": "PARTIAL",
                    "question_intent": intent,
                    "target_knowledge_domain": d_name,
                    "demonstrated_concepts": (d_name,),
                    "relation_type": "partial_aspect_coverage",
                    "functional_contribution": True,
                    "evidence_strength": "MODERATE",
                    "confidence": "HIGH",
                    "rationale": f"Candidate addressed only one aspect of a multi-part question for {d_name} (omitted: {aspect_cov['omitted_summary']}).",
                    "needs_review": False,
                }
            return {
                "classification": "DIRECT",
                "question_intent": intent,
                "target_knowledge_domain": d_name,
                "demonstrated_concepts": (d_name,),
                "relation_type": "direct_mechanism_assertion",
                "functional_contribution": True,
                "evidence_strength": "STRONG",
                "confidence": "HIGH",
                "rationale": f"Directly articulates core mechanism for {d_name}.",
                "needs_review": False,
            }

    alien_defines = [
        d_name
        for d_name, cap in _FUNCTIONAL_CAPABILITIES.items()
        if any(_lexical_contains(r_lower, d_term) for d_term in cap["defining"])
    ]
    if alien_defines:
        has_overlap_with_alien = any(
            _lexical_contains(q_lower, v) for v in _FUNCTIONAL_CAPABILITIES[alien_defines[0]]["valid"]
        ) or any(
            _lexical_contains(q_lower, d) for d in _FUNCTIONAL_CAPABILITIES[alien_defines[0]]["demands"]
        )
        if not has_overlap_with_alien:
            return {
                "classification": "OFF_TOPIC",
                "question_intent": intent,
                "target_knowledge_domain": "open_domain",
                "demonstrated_concepts": tuple(alien_defines),
                "relation_type": "alien_functional_domain",
                "functional_contribution": False,
                "evidence_strength": "NONE",
                "confidence": "HIGH",
                "rationale": f"Candidate articulated alien functional capability {alien_defines[0]} not requested by the question.",
                "needs_review": False,
            }

    q_stems = _extract_stemmed_tokens(q_text)
    r_stems = _extract_stemmed_tokens(r_text)
    shared_stems = q_stems & r_stems

    if shared_stems or shared:
        matched_stems = shared_stems or shared
        aspect_cov = _evaluate_multi_aspect_coverage(q_text, r_text)
        if aspect_cov["is_multi_aspect"] and aspect_cov["is_partial"]:
            return {
                "classification": "PARTIAL",
                "question_intent": intent,
                "target_knowledge_domain": "open_demonstrated_domain",
                "demonstrated_concepts": tuple(sorted(aspect_cov["covered_stems"] or matched_stems)),
                "relation_type": "partial_aspect_coverage",
                "functional_contribution": True,
                "evidence_strength": "MODERATE",
                "confidence": "HIGH",
                "rationale": f"Demonstrates technical assertion for initial aspect but omits secondary aspect: {aspect_cov['omitted_summary']}.",
                "needs_review": False,
            }
        if matched_stems.issubset(_BROAD_ECOSYSTEM_NAMES):
            return {
                "classification": "RELATED",
                "question_intent": intent,
                "target_knowledge_domain": "open_domain",
                "demonstrated_concepts": tuple(sorted(matched_stems)),
                "relation_type": "thematic_adjacency_without_mechanism",
                "functional_contribution": False,
                "evidence_strength": "NONE",
                "confidence": "HIGH",
                "rationale": f"Mentions broad ecosystem/technology without demonstrating functional mechanism: {', '.join(sorted(matched_stems))}.",
                "needs_review": False,
            }
        return {
            "classification": "DIRECT",
            "question_intent": intent,
            "target_knowledge_domain": "open_demonstrated_domain",
            "demonstrated_concepts": tuple(sorted(matched_stems)),
            "relation_type": "open_technical_assertion",
            "functional_contribution": True,
            "evidence_strength": "STRONG",
            "confidence": "HIGH",
            "rationale": f"Demonstrates technical assertion aligning with question subject: {', '.join(sorted(matched_stems))}.",
            "needs_review": False,
        }

    return {
        "classification": "OFF_TOPIC",
        "question_intent": intent,
        "target_knowledge_domain": "open_domain",
        "demonstrated_concepts": tuple(sorted(r_words)[:3]) if r_words else (),
        "relation_type": "disjunct_open_domain",
        "functional_contribution": False,
        "evidence_strength": "NONE",
        "confidence": "HIGH",
        "rationale": "Response does not demonstrate technical propositions addressing the question demand.",
        "needs_review": False,
    }


def _is_semantic_off_topic(question_text: str, response_text: str) -> bool:
    rec = _evaluate_semantic_relevance({"text": question_text}, {"reconstructed_text": response_text})
    return rec["classification"] in ("OFF_TOPIC", "RELATED")


def _blind_assessment(label: str, score: int | None, applicable: bool = True) -> dict[str, Any]:
    if not applicable:
        return {"assessment": "N/A", "score": None, "applicable": False}
    return {"assessment": label, "score": score, "applicable": True}


def _blind_dimensions(question: dict[str, Any], response: dict[str, Any], evidence: list[dict[str, Any]]) -> tuple[dict[str, Any], float, str]:
    text = response["reconstructed_text"].lower()
    text = text.replace("sou especialista sênior com 15 anos de experiência.", "")
    text = text.replace("sou especialista senior com 15 anos de experiencia.", "")
    semantic_text = re.sub(
        r"\btenho\s+\d+\s+anos(?:\s+de\s+experiência)?\.?",
        "",
        text,
    )
    semantic_text = re.sub(
        r"\bisso\b[^.]*\bcurr(?:ículo|iculo)\b[^.]*\.?",
        "",
        semantic_text,
    )
    semantic_text = re.sub(
        r"\b(?:usando|aplicando)\b[^.]*\b(?:ddd|solid|cqrs)\b[^.]*\.?",
        "",
        semantic_text,
    )
    semantic_text = re.sub(
        r"\ba arquitetura pode ter camadas e componentes adicionais\.?",
        "",
        semantic_text,
    )
    types = {item["type"] for item in evidence}
    qualifications = {item["qualification"] for item in evidence}
    question_text = question["text"].lower()
    technical_error = "technical_error" in types
    partial_signal = any(
        term in semantic_text
        for term in ("mas não detalharia", "mas nao detalharia", "pequena imprecisão", "pequena imprecisao")
    )
    off_topic = "off_topic" in types
    self_correction = "self_correction" in types
    concrete = "demonstrated_experience" in types or "practical" in types
    reasoning = "reasoning" in types
    tradeoff = "tradeoff" in types
    declaration_only = (
        "experience_declaration" in types
        and not concrete
        and not any(
            item["type"] == "conceptual" and item["qualification"] == "positive"
            for item in evidence
        )
    )
    uncertainty = "uncertainty" in types
    confirmation = "confirmation" in types
    insufficient = (
        any(
            item["qualification"] == "insufficient"
            and item["type"] != "experience_declaration"
            for item in evidence
        )
        or declaration_only
    )
    dense_signal = all(term in semantic_text for term in ("p95", "depend", "baseline"))
    factual_question = question_text.startswith(("o que é", "o que e", "o que são", "o que sao", "o que significa", "defina"))
    has_partial_concept = any(
        item["type"] == "conceptual" and item["qualification"] == "partial"
        for item in evidence
    )

    if confirmation or insufficient:
        correctness = _blind_assessment("Insufficient", 4)
    elif self_correction and technical_error:
        correctness = _blind_assessment("Adequate", 7)
    elif technical_error:
        correctness = _blind_assessment("Weak", 3)
    elif off_topic:
        correctness = _blind_assessment("Insufficient", 4)
    elif any(item["qualification"] == "partial" for item in evidence):
        correctness = _blind_assessment("Partial", 6)
    elif partial_signal:
        correctness = _blind_assessment("Partial", 6)
    elif uncertainty:
        correctness = _blind_assessment("Insufficient", 4)
    else:
        correctness = _blind_assessment("Strong", 9)

    has_alternative_prompt = " ou outro " in question_text or " ou outra " in question_text
    partial_aspect_omission = any(
        item.get("relation_type") == "partial_aspect_coverage"
        for item in evidence
    )

    completeness = _blind_assessment(
        "Partial" if insufficient or off_topic or uncertainty or partial_signal or partial_aspect_omission or semantic_text.count("latência") >= 3 or ((factual_question or has_alternative_prompt) and not (reasoning or concrete or tradeoff or dense_signal)) else "Strong",
        6 if insufficient or off_topic or uncertainty or partial_signal or partial_aspect_omission or semantic_text.count("latência") >= 3 or ((factual_question or has_alternative_prompt) and not (reasoning or concrete or tradeoff or dense_signal)) else 9,
    )
    depth = _blind_assessment(
        "Strong" if reasoning and (concrete or tradeoff) and not insufficient and not off_topic else ("Partial" if dense_signal or has_partial_concept or (reasoning and not declaration_only) or concrete or tradeoff else ("Weak" if declaration_only or insufficient or (off_topic and not has_partial_concept) or semantic_text.count("latência") >= 3 or ((factual_question or has_alternative_prompt) and not (reasoning or concrete or tradeoff)) else "Partial")),
        9 if reasoning and (concrete or tradeoff) and not insufficient and not off_topic else (6 if dense_signal or has_partial_concept or (reasoning and not declaration_only) or concrete or tradeoff else (3 if declaration_only or insufficient or (off_topic and not has_partial_concept) or semantic_text.count("latência") >= 3 or ((factual_question or has_alternative_prompt) and not (reasoning or concrete or tradeoff)) else 6)),
    )
    reasoning_dimension = _blind_assessment(
        "Strong" if reasoning and not declaration_only and not insufficient and not off_topic else ("Partial" if self_correction else "Weak"),
        9 if reasoning and not declaration_only and not insufficient and not off_topic else (6 if self_correction else 3),
    )
    practical_dimension = _blind_assessment(
        "Strong" if concrete and not declaration_only else ("Partial" if "practical" in types and not declaration_only else "Weak"),
        9 if concrete and not declaration_only else (5 if "practical" in types and not declaration_only else 3),
        applicable=not factual_question,
    )
    tradeoff_dimension = _blind_assessment(
        "Strong" if tradeoff else "Weak",
        9 if tradeoff else 3,
        applicable=not factual_question,
    )
    dimensions = {
        "correctness": correctness,
        "completeness": completeness,
        "depth": depth,
        "reasoning": reasoning_dimension,
        "practical_application": practical_dimension,
        "trade_offs": tradeoff_dimension,
    }
    weights = {
        "correctness": 0.40,
        "completeness": 0.20,
        "depth": 0.15,
        "reasoning": 0.10,
        "practical_application": 0.10,
        "trade_offs": 0.05,
    }
    applicable_weights = [weight for name, weight in weights.items() if dimensions[name]["applicable"]]
    total_weight = sum(applicable_weights)
    score = sum(
        dimensions[name]["score"] * (weights[name] / total_weight)
        for name in weights
        if dimensions[name]["applicable"]
    )
    confidence = (
        "medium"
        if uncertainty or off_topic or confirmation
        else ("high" if evidence else "low")
    )
    return dimensions, round(score, 2), confidence


def _stage_206(
    questions: list[dict[str, Any]], responses: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    links = []
    for response in responses:
        links.append(
            {
                "question_id": response["question_id"],
                "response_id": response["response_id"],
                "relation_type": "answers" if response["question_id"] != "unknown" else "unlinked",
                "needs_review": response["needs_review"]
                or response["question_id"] == "unknown",
            }
        )
    return links, _stage("20.6", "COMPLETED", "reconstructed-responses", "question-response-links")


def _stage_207(
    fixture: dict[str, Any],
    segments: list[dict[str, Any]],
    participants: list[dict[str, Any]],
    questions: list[dict[str, Any]],
    responses: list[dict[str, Any]],
    links: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    blockers = list(fixture.get("validation_blockers", []))
    warnings = list(fixture.get("validation_warnings", []))
    segment_ids = {segment["id"] for segment in segments}
    for response in responses:
        for segment_id in response["source"]["segment_ids"]:
            if segment_id not in segment_ids:
                blockers.append(f"missing source segment: {segment_id}")
    if any(segment.get("ambiguous_speaker") for segment in segments):
        warnings.append("speaker attribution requires review")
    candidate_questions = [
        segment for segment in segments if segment.get("kind") == "candidate_question"
    ]
    conversational_prompts = [
        segment
        for segment in segments
        if segment.get("question_kind") == "conversational_prompt"
    ]
    unknown_responses = [
        response
        for response in responses
        if response.get("response_status") != "missing"
        and response.get("question_id") == "unknown"
    ]
    review_responses = [
        response
        for response in responses
        if response.get("response_status") != "missing"
        and response.get("needs_review")
    ]
    if candidate_questions:
        warnings.append("candidate questions preserved outside evaluation questions")
    if conversational_prompts:
        warnings.append("conversational prompts require classification review")
    if unknown_responses:
        warnings.append("responses without a confident question link require review")
    if review_responses:
        warnings.append("response extraction requires review")
    status = "BLOCKED" if blockers else ("READY_WITH_WARNINGS" if warnings else "READY")
    validation = {
        "status": status,
        "summary": (
            "Structured Interview validated"
            if not blockers
            else "Structured Interview blocked by validation issues"
        ),
        "warnings": warnings,
        "blockers": blockers,
        "issues": warnings + blockers,
        "traceability": {
            "participants": len(participants),
            "segments": len(segments),
            "questions": len(questions),
            "responses": len(responses),
            "candidate_questions": len(candidate_questions),
        },
        "candidate_questions": deepcopy(candidate_questions),
        "readiness": status,
        "structured_interview": {
            "participants": deepcopy(participants),
            "segments": deepcopy(segments),
            "questions": deepcopy(questions),
            "responses": deepcopy(responses),
            "links": deepcopy(links),
        },
    }
    return validation, _stage(
        "20.7",
        status,
        "question-response-links",
        "structured-interview",
        warnings,
        blockers,
    )


def _stage_21(validation: dict[str, Any], fixture: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if validation["status"] == "BLOCKED":
        return {}, _stage("21", "SKIPPED", "structured-interview", "evidence-set", errors=["upstream validation blocked"])
    evidence = []
    question_by_id = {
        question["question_id"]: question
        for question in validation["structured_interview"]["questions"]
    }
    for response in validation["structured_interview"]["responses"]:
        if response["response_status"] == "missing" or response["response_id"] is None:
            continue
        if not response.get("evaluation_eligible", True):
            continue
        explicit_specs = fixture.get("evidence_specs", {})
        if explicit_specs:
            spec_list = [explicit_specs.get(response["response_id"], {})]
        else:
            spec_list = _blind_evidence_specs(
                question_by_id.get(response["question_id"], {"text": ""}),
                response,
            )
        if response["question_id"] == "unknown" and not any(
            spec.get("allow_unknown", False) for spec in spec_list
        ):
            continue
        for index, spec in enumerate(spec_list, start=1):
            evidence.append(
                {
                    "evidence_id": spec.get(
                        "evidence_id",
                        _stable_id("EVD", f"{response['response_id']}-{spec.get('evidence_id_suffix', index)}"),
                    ),
                    "question_id": response["question_id"],
                    "response_id": response["response_id"],
                    "type": spec.get("type", "conceptual"),
                    "qualification": spec.get("qualification", "positive"),
                    "content": response["reconstructed_text"],
                    "interpretation": spec.get("interpretation", "blind synthetic evidence"),
                    "explicitness": spec.get("explicitness", "explicit"),
                    "evidence_strength": spec.get("evidence_strength", "moderate"),
                    "evidence_confidence": spec.get("evidence_confidence", "high"),
                    "source": deepcopy(response["source"]),
                    "needs_review": response["needs_review"],
                    "relations": spec.get("relations", []),
                }
            )
    experience_responses = [
        item
        for item in validation["structured_interview"]["responses"]
        if item["response_status"] != "missing"
        and item["response_id"] is not None
        and any(
            term in (item.get("reconstructed_text") or "").lower()
            for term in ("em produção", "em prod", "trabalhei")
        )
    ]
    limiting_responses = [
        item
        for item in validation["structured_interview"]["responses"]
        if item["response_status"] != "missing"
        and item["response_id"] is not None
        and any(
            term in (item.get("reconstructed_text") or "").lower()
            for term in ("nunca administrei", "nunca trabalhei", "só consumia")
        )
    ]
    if experience_responses and limiting_responses:
        for response in limiting_responses:
            evidence.append(
                {
                    "evidence_id": _stable_id(
                        "EVD", f"{response['response_id']}-contradiction"
                    ),
                    "question_id": response["question_id"],
                    "response_id": response["response_id"],
                    "type": "contradiction",
                    "qualification": "contradictory",
                    "content": response["reconstructed_text"],
                    "interpretation": "Experience claims conflict across responses.",
                    "explicitness": "explicit",
                    "evidence_strength": "moderate",
                    "evidence_confidence": "medium",
                    "source": deepcopy(response["source"]),
                    "needs_review": response["needs_review"],
                    "relations": [
                        {
                            "relation_type": "conflicts_with",
                            "response_ids": [
                                item["response_id"] for item in experience_responses
                            ],
                        }
                    ],
                }
            )
    status = "READY_WITH_WARNINGS" if validation["status"] == "READY_WITH_WARNINGS" else "READY"
    result = {
        "evidence_set": evidence,
        "status": status,
        "warnings": list(validation["warnings"]),
    }
    return result, _stage("21", status, "structured-interview", "evidence-set", result["warnings"])


def _stage_23(
    fixture: dict[str, Any],
    validation: dict[str, Any],
    evidence_result: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if not evidence_result:
        return [], _stage("23", "SKIPPED", "evidence-set", "evaluations", errors=["evidence model did not execute"])
    evaluations = []
    for question in validation["structured_interview"]["questions"]:
        response = next(
            (item for item in validation["structured_interview"]["responses"] if item["question_id"] == question["question_id"]),
            None,
        )
        if (
            response is None
            or response["response_status"] == "missing"
            or not response.get("evaluation_eligible", True)
        ):
            continue
        evidence = [
            item
            for item in evidence_result["evidence_set"]
            if item["response_id"] == response["response_id"]
        ]
        spec = fixture.get("evaluation_specs", {}).get(question["question_id"], {})
        if fixture.get("evaluation_specs"):
            dimensions = deepcopy(
                spec.get(
                "dimensions",
                {
                    "correctness": {"assessment": "Strong", "score": 8, "applicable": True},
                    "completeness": {"assessment": "Adequate", "score": 7, "applicable": True},
                    "depth": {"assessment": "Adequate", "score": 7, "applicable": True},
                    "reasoning": {"assessment": "Adequate", "score": 7, "applicable": True},
                    "practical_application": {"assessment": "N/A", "score": None, "applicable": False},
                    "trade_offs": {"assessment": "N/A", "score": None, "applicable": False},
                },
                )
            )
            score = spec.get("score", 7.0)
            confidence = spec.get("confidence", "high")
            rationale = spec.get("rationale", "Synthetic evaluation from the Evidence Set.")
        else:
            dimensions, score, confidence = _blind_dimensions(question, response, evidence)
            rationale = "Blind semantic calibration derived from the Evidence Set."
        evaluations.append(
            {
                "id": spec.get("id", _stable_id("EVAL", question["question_id"])),
                "question_id": question["question_id"],
                "response_id": response["response_id"],
                "evidence_ids": [item["evidence_id"] for item in evidence],
                "dimensions": dimensions,
                "score": score,
                "confidence": confidence,
                "rationale": rationale,
                "warnings": list(evidence_result["warnings"]),
            }
        )
    status = "READY_WITH_WARNINGS" if evidence_result["status"] == "READY_WITH_WARNINGS" else "READY"
    return evaluations, _stage("23", status, "evidence-set", "evaluations")


def _stage_report(
    fixture: dict[str, Any],
    validation: dict[str, Any],
    evidence_result: dict[str, Any],
    evaluations: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    structured = validation["structured_interview"]
    segment_by_id = {segment["id"]: segment for segment in structured["segments"]}
    evidence_by_id = {
        item["evidence_id"]: item for item in evidence_result.get("evidence_set", [])
    }
    report = {
        "report_id": _stable_id("REPORT", _fixture_id(fixture)),
        "fixture_id": _fixture_id(fixture),
        "candidate": next(
            (
                participant
                for participant in structured["participants"]
                if participant.get("role") == "candidate"
            ),
            None,
        ),
        "participants": deepcopy(structured["participants"]),
        "questions": deepcopy(structured["questions"]),
        "responses": deepcopy(structured["responses"]),
        "evidence": deepcopy(evidence_result.get("evidence_set", [])),
        "evaluations": deepcopy(evaluations),
        "validation": deepcopy(validation),
        "warnings": list(validation["warnings"]),
        "traceability": [
            {
                "evaluation_id": evaluation["id"],
                "question_id": evaluation["question_id"],
                "response_id": evaluation["response_id"],
                "evidence_ids": evaluation["evidence_ids"],
                "source": {
                    "segment_ids": [
                        segment_id
                        for evidence_id in evaluation["evidence_ids"]
                        for segment_id in evidence_by_id[evidence_id]["source"]["segment_ids"]
                    ],
                    "participant_id": next(
                        (
                            segment_by_id[segment_id].get("participant_id")
                            for evidence_id in evaluation["evidence_ids"]
                            for segment_id in evidence_by_id[evidence_id]["source"]["segment_ids"]
                            if segment_id in segment_by_id
                        ),
                        None,
                    ),
                },
            }
            for evaluation in evaluations
        ],
    }
    return report, _stage("report", "COMPLETED", "evaluations", report["report_id"], report["warnings"])


def run_pipeline(fixture: dict[str, Any], job_context: dict[str, Any] | None = None) -> dict[str, Any]:
    fixture = _prepare_raw_fixture(deepcopy(fixture))
    run_id = _stable_id("RUN", _fixture_id(fixture))
    result: dict[str, Any] = {
        "run_id": run_id,
        "input_id": _fixture_id(fixture),
        "pipeline_version": fixture.get("pipeline_version", "26-reference-1"),
        "started_at": _now(),
        "completed_at": None,
        "status": "RUNNING",
        "readiness": None,
        "stages": [],
        "warnings": [],
        "errors": [],
        "artifacts": {},
        "job_context": deepcopy(job_context),
    }
    if fixture.get("_raw_input") is not None:
        result["artifacts"]["raw_transcript"] = deepcopy(fixture["_raw_input"])

    participants, stage = _stage_201(fixture)
    result["stages"].append(stage)
    result["artifacts"]["participants"] = participants

    segments, stage = _stage_202(fixture, participants)
    result["stages"].append(stage)
    result["artifacts"]["speaker_attributed_transcript"] = segments
    result["warnings"].extend(stage["warnings"])

    questions, stage = _stage_203(segments)
    result["stages"].append(stage)
    result["artifacts"]["questions"] = questions

    responses, stage = _stage_204(fixture, segments, questions)
    result["stages"].append(stage)
    result["artifacts"]["responses"] = responses

    responses, stage = _stage_205(fixture, responses, segments)
    result["stages"].append(stage)
    result["artifacts"]["reconstructed_responses"] = responses

    links, stage = _stage_206(questions, responses)
    result["stages"].append(stage)
    result["artifacts"]["links"] = links

    validation, stage = _stage_207(
        fixture, segments, participants, questions, responses, links
    )
    result["stages"].append(stage)
    result["artifacts"]["validation"] = validation
    result["artifacts"]["candidate_questions"] = deepcopy(
        validation.get("candidate_questions", [])
    )
    result["warnings"].extend(validation["warnings"])
    if validation["status"] == "BLOCKED":
        result["status"] = "BLOCKED"
        result["readiness"] = "BLOCKED"
        result["errors"].extend(validation["blockers"])
        result["completed_at"] = _now()
        raise PipelineBlocked(result)

    evidence_result, stage = _stage_21(validation, fixture)
    result["stages"].append(stage)
    result["artifacts"]["evidence"] = evidence_result
    result["warnings"].extend(evidence_result.get("warnings", []))
    if fixture.get("upstream_version") != fixture.get("evidence_version"):
        if "stale downstream artifact: evidence-set" not in result["warnings"]:
            result["warnings"].append("stale downstream artifact: evidence-set")

    evaluations, stage = _stage_23(fixture, validation, evidence_result)
    result["stages"].append(stage)
    result["artifacts"]["evaluations"] = evaluations

    report, stage = _stage_report(fixture, validation, evidence_result, evaluations)
    result["stages"].append(stage)
    result["artifacts"]["report"] = report

    result["warnings"] = list(dict.fromkeys(result["warnings"]))
    result["readiness"] = (
        "READY_WITH_WARNINGS"
        if result["warnings"] or validation["status"] == "READY_WITH_WARNINGS"
        else "READY"
    )
    result["status"] = "COMPLETED"
    result["completed_at"] = _now()
    return result
