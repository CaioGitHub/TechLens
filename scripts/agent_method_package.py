"""Versioned method-only ZIPs. No transcript input, model API or scoring logic."""
import argparse
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

METHOD_SOURCES = (
    'AGENTS.md',
    'SECOND_BRAIN.md',
    'GEMINI_GUARDRAILS.md',
    'TRANSCRIPTION_AGENT_WORKFLOW.md',
    'TRANSCRIPTION_CORRECTION_FIDELITY.md',
    'TRANSCRIPTION_UNCERTAINTY.md',
    '11 - Interview Evaluation/01 - Evaluation Framework/Interview Evaluation Model.md',
    '11 - Interview Evaluation/01 - Evaluation Framework/Transcription Processing Model.md',
    '11 - Interview Evaluation/01 - Evaluation Framework/Evaluation Engine.md',
    '11 - Interview Evaluation/08 - Evidence Model/21 - Evidence Model.md',
    '11 - Interview Evaluation/02 - Question Types/Question Taxonomy.md',
    '11 - Interview Evaluation/04 - Rubrics/Scoring Rubric.md',
    '03 - Architecture/Hexagonal Architecture/Hexagonal Architecture.md',
    '03 - Architecture/Hexagonal Architecture/Ports.md',
    '03 - Architecture/Hexagonal Architecture/Adapters.md',
    '02 - Technologies/Spring Boot/Spring REST.md',
    '02 - Technologies/Spring Boot/Spring Data.md',
    '07 - Troubleshooting/End-to-End Troubleshooting Playbook.md',
    '11 - Interview Evaluation/07 - Transcription Processing/20.1 - Participant Identification.md',
    '11 - Interview Evaluation/07 - Transcription Processing/20.2 - Speaker Attribution.md',
    '11 - Interview Evaluation/07 - Transcription Processing/20.3 - Question Extraction.md',
    '11 - Interview Evaluation/07 - Transcription Processing/20.4 - Response Extraction.md',
    '11 - Interview Evaluation/07 - Transcription Processing/20.5 - Reconstruction & Normalization.md',
    '11 - Interview Evaluation/07 - Transcription Processing/20.6 - Question-Response Linking.md',
    '11 - Interview Evaluation/07 - Transcription Processing/20.7 - Validation.md',
    'ANALISAR_ENTREVISTA.md',
    'TRANSCRIPTION_EVALUATION_CHECK.md',
)

FORMAT_V1 = "techlens.method.v1"
FORMAT = "techlens.method.v2"
DEFAULT_RELEASE = "0.1.0-piloto.2"
V2_SOURCES = METHOD_SOURCES + (
    "PROTOCOLO_VALIDACAO.md",
    "99 - Templates/Interview Validation/FICHA_REVISAO_PREVIA.md",
    "99 - Templates/Interview Validation/MATRIZ_DIVERGENCIAS.md",
    "99 - Templates/Interview Validation/DECISAO_VALIDACAO.md",
    "GUIA_DO_PILOTO.md",
    "99 - Templates/Interview Validation/REGISTRO_DO_PILOTO.md",
)


def sources_for_format(package_format):
    if package_format == FORMAT_V1:
        return METHOD_SOURCES
    if package_format == FORMAT:
        return V2_SOURCES
    raise ValueError("Unsupported package format")


def member_names(package_format):
    return set(sources_for_format(package_format)) | set(GENERATED) | {"package_manifest.json"}


def _release_valid(value):
    return isinstance(value, str) and re.fullmatch(
        r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?", value) is not None

MAX_TOTAL_BYTES = 20 * 1024 * 1024
GENERATED = {
    "README.md": "# TechLens — pacote de método\n\nComece por LEIA_PRIMEIRO.md, depois ANALISAR_ENTREVISTA.md. Este ZIP contém somente referências de método e exemplos metodológicos, sem entrevista de entrada ou relatório de candidato. Extraia em uma pasta nova. Use seu próprio agente com acesso aos arquivos. Não é necessário executar Python para analisar.\n\nO manifesto identifica a revisão Git usada. Integridade de bytes não comprova fidelidade de uma transcrição, autoria do pacote ou qualidade semântica do agente. Não há fonte real neste pacote: aguardar uma transcrição fornecida pelo usuário. Não reutilizar relatórios anteriores como gabarito.\n",
    "LEIA_PRIMEIRO.md": "# Início\n\nAbra ANALISAR_ENTREVISTA.md e siga o pedido copiável com sua transcrição. GUIA_DO_PILOTO.md orienta o acompanhamento quando estiver incluído. Use uma conversa sem relatórios anteriores e declare seu contexto real. Preserve o ZIP original; a verificação se aplica ao ZIP antes de adicionar transcrição e saídas à pasta extraída. Registre o contexto e as limitações reais; uma pasta separada não garante cegamento.\n",
    "START_HERE.md": "# Entrada do snapshot\n\nEste é um pacote limitado do método, não o checkout de desenvolvimento. Siga ANALISAR_ENTREVISTA.md e TRANSCRIPTION_AGENT_WORKFLOW.md. Referências ausentes de histórico/runtime não são necessárias à análise textual. Declare fonte técnica essencial que esteja indisponível. Não afirmar consulta inexistente.\n",
    "GEMINI_HANDOFF.md": "# Escopo deste pacote\n\nO agente do usuário consulta o projeto como método. Este snapshot não contém relatórios ou resultados de entrevistas anteriores. Há exemplos legítimos na rubrica. Gates históricos não são promovidos por uma nova análise. Não implementar integrações ou executar runtime para analisar.\n",
    "CONTINUIDADE_2026-10-28.md": "# Continuidade no pacote distribuído\n\nDocumento de orientação gerado, não reprodução do histórico do repositório. Use ANALISAR_ENTREVISTA.md. A metodologia tem validações diagnósticas com limitações; uso supervisionado. Não há independência comprovada ou homologação semântica geral. A revisão de origem consta do manifesto.\n",
    "TRANSCRIPTION_PROJECT_STATUS_2026-10-26.md": "# Limites de validação no pacote\n\nResumo gerado para distribuição, sem resultados ou dados de candidatos. Verificar integridade do pacote não valida a análise semântica nem qualquer transcrição. Aplicar o método com supervisão, guardar a primeira saída e limitar conclusões às evidências. O histórico de desenvolvimento completo não acompanha este snapshot.\n",
}


def _canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _git(repo, git, *args):
    try:
        return subprocess.check_output([git, "-C", str(repo), *args], stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exc:
        raise ValueError("Required Git revision or method source is unavailable") from exc


def _transform(name, raw):
    text = raw.decode("utf-8").replace("\r\n", "\n")
    changes = []
    if name == "TRANSCRIPTION_AGENT_WORKFLOW.md":
        marker = "\n## Primeira validação diagnóstica do roteiro"
        if marker in text:
            text = text.split(marker, 1)[0].rstrip() + "\n"
            changes.append("Execution-history appendix omitted; method retained")
    if name.endswith("/Transcription Processing Model.md"):
        normalized = text.replace("Ingrid Mazoni", "Candidata Exemplo").replace("Ingrid", "Candidata Exemplo")
        if normalized != text:
            changes.append("Illustrative participant name generalized")
            text = normalized
    return text.encode("utf-8"), changes


def build_package(repo, output, ref="HEAD", git=None, release_version=DEFAULT_RELEASE, package_format=FORMAT):
    repo, output = Path(repo), Path(output)
    if output.exists():
        raise FileExistsError(output)
    sources = sources_for_format(package_format)
    if package_format == FORMAT and not _release_valid(release_version):
        raise ValueError("Invalid release version")
    git = git or shutil.which("git")
    if not git:
        raise ValueError("Git is required to read a fixed source revision")
    commit = _git(repo, git, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}").decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
        raise ValueError("Invalid resolved source commit")
    files, source_hashes, transforms = {}, {}, []
    for name in sources:
        raw = _git(repo, git, "show", commit + ":" + name)
        source_hashes[name] = sha256(raw).hexdigest()
        files[name], changes = _transform(name, raw)
        if changes:
            transforms.append({"path": name, "changes": changes})
    files.update({name: body.encode("utf-8") for name, body in GENERATED.items()})
    manifest = {
        "package_format": package_format,
        "source_commit": commit,
        "source_file_sha256": source_hashes,
        "file_sha256": {name: sha256(raw).hexdigest() for name, raw in files.items()},
        "transforms": transforms,
        "generated_files": sorted(GENERATED),
        "selection": "Explicit method-document allowlist; no interview or report directories",
        "transcript_included": False,
        "candidate_report_included": False,
        "independent_semantic_validation": False,
        "integrity_is_authenticity_proof": False,
    }
    if package_format == FORMAT:
        manifest["release_version"] = release_version
        manifest["distribution"] = "CONTROLLED_SUPERVISED_PILOT"
    files["package_manifest.json"] = _canonical(manifest)
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, raw in sorted(files.items()):
            item = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            item.create_system = 3
            item.external_attr = 0o100644 << 16
            item.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(item, raw, compresslevel=9)
    data = stream.getvalue()
    # Validate the complete archive before touching the destination.
    _verify(io.BytesIO(data))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as handle:
        handle.write(data)
    return {"status": "PACKAGE_BUILT", "source_commit": commit, "zip": str(output),
            "zip_sha256": sha256(data).hexdigest(), "file_count": len(files),
            "package_format": package_format, "release_version": manifest.get("release_version")}


def read_verified_package(source):
    """Return metadata and exactly the validated members from one archive read."""
    try:
        with zipfile.ZipFile(source) as z:
            names = z.namelist()
            if len(names) != len(set(names)) or "package_manifest.json" not in names:
                raise ValueError("Duplicate members or missing manifest")
            if sum(i.file_size for i in z.infolist()) > MAX_TOTAL_BYTES:
                raise ValueError("Method package exceeds size limit")
            if any(i.flag_bits & 1 or i.is_dir() or (i.external_attr >> 16) & 0o170000 == 0o120000 for i in z.infolist()):
                raise ValueError("Unsupported encrypted, directory or symbolic-link member")
            manifest = json.loads(z.read("package_manifest.json"))
            package_format = manifest.get("package_format")
            expected = member_names(package_format)
            if set(names) != expected:
                raise ValueError("Archive members do not match the method-only allowlist")
            if package_format == FORMAT and not _release_valid(manifest.get("release_version")):
                raise ValueError("Missing or invalid release version")
            if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", manifest.get("source_commit", "")):
                raise ValueError("Missing source revision")
            hashes = manifest.get("file_sha256", {})
            if not isinstance(hashes, dict) or set(hashes) != expected - {"package_manifest.json"}:
                raise ValueError("Manifest members do not match archive")
            files = {name: z.read(name) for name in sorted(expected)}
            for name, digest in hashes.items():
                if not isinstance(digest, str) or sha256(files[name]).hexdigest() != digest:
                    raise ValueError("Hash mismatch: " + name)
            if manifest.get("transcript_included") is not False or manifest.get("candidate_report_included") is not False:
                raise ValueError("Not a method-only package")
    except (zipfile.BadZipFile, json.JSONDecodeError, UnicodeDecodeError, KeyError, TypeError, AttributeError, RuntimeError) as exc:
        raise ValueError("Invalid method archive or manifest") from exc
    return {"status": "INTEGRITY_VERIFIED", "source_commit": manifest["source_commit"],
            "package_format": package_format, "release_version": manifest.get("release_version"),
            "file_count": len(expected), "authenticity_verified": False, "semantic_validation": False}, files


def _verify(source):
    return read_verified_package(source)[0]


def verify_package(archive):
    raw = Path(archive).read_bytes()
    result = _verify(io.BytesIO(raw))
    result["zip_sha256"] = sha256(raw).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("--repo", type=Path, default=Path.cwd())
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--ref", default="HEAD")
    build.add_argument("--git")
    build.add_argument("--release-version", default=DEFAULT_RELEASE)
    build.add_argument("--package-format", choices=(FORMAT_V1, FORMAT), default=FORMAT)
    verify = sub.add_parser("verify")
    verify.add_argument("archive", type=Path)
    args = parser.parse_args()
    try:
        result = build_package(args.repo, args.output, args.ref, args.git, args.release_version, args.package_format) if args.command == "build" else verify_package(args.archive)
    except (ValueError, FileExistsError, OSError) as exc:
        parser.exit(1, str(exc) + "\n")
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
