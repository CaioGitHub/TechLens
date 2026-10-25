"""Build a review-artifact-free reference snapshot for a user-owned agent."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import zipfile


def build(repo, output, git):
    spec_path=repo/'11 - Interview Evaluation/09 - Real Interview Pilot/Agent Retest 2026-10-25/build_spec.json'
    spec=json.loads(spec_path.read_text(encoding='utf-8'))
    metadata=spec_path.parent
    def source(path):
        return subprocess.check_output([git,'-C',str(repo),'show',spec['source_commit']+':'+path]).decode('utf-8').replace('\r\n','\n')
    assert not output.exists(),'Do not overwrite an existing package.'
    output.mkdir(parents=True)
    transforms=[]
    for path in spec['method_sources']:
        text=source(path)
        if path=='TRANSCRIPTION_AGENT_WORKFLOW.md':
            text=text.split('\n## Primeira validação diagnóstica do roteiro',1)[0].rstrip()+'\n'
            transforms.append(dict(path=path,action='Excluded execution-history appendix; method steps retained.'))
        if path.endswith('/Transcription Processing Model.md'):
            text=text.replace('Ingrid Mazoni','Candidata Exemplo').replace('Ingrid','Candidata Exemplo')
            transforms.append(dict(path=path,action='Replaced illustrative participant names only, not method rules.'))
        target=output/path;target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(text,encoding='utf-8',newline='\n')
    transcript=source(spec['transcript_source'])
    match=re.search(r'```text\r?\n(.*?)\r?\n```',transcript,re.S)
    assert match
    raw=match.group(1)
    turns=re.findall(r'^.+?\s+—\s+\d{2}:\d{2}$',raw,re.M)
    assert len(turns)==164
    (output/'TRANSCRICAO_ORIGINAL.md').write_text('# Transcrição original para análise\n\nTexto recebido, sem correções lexicais aplicadas. Timestamps indicam início de turno. As condições da fonte estão em CONDICOES_DA_FONTE.md.\n\n```text\n'+raw+'\n```\n',encoding='utf-8',newline='\n')
    for name in ['CONDICOES_DA_FONTE.md','TAREFA_PARA_O_AGENTE.md']:
        (output/name).write_text((metadata/name).read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
    (output/'START_HERE.md').write_text('''# Início desta análise

Este é um snapshot limitado do método do projeto, não o repositório completo de desenvolvimento. Execute TAREFA_PARA_O_AGENTE.md com TRANSCRICAO_ORIGINAL.md e CONDICOES_DA_FONTE.md. Consulte TRANSCRIPTION_AGENT_WORKFLOW.md e os documentos de método presentes. Não procure avaliações anteriores da entrevista nem outras pastas/repositórios.

As referências ausentes a histórico, runtime ou desenvolvimento não são necessárias para analisar a transcrição. Registre qualquer outra fonte metodológica essencial que esteja indisponível; não afirme tê-la consultado. Grave ou apresente a entrega como uma nova análise desta entrada, sem sobrescrever relatórios fora deste pacote.
''',encoding='utf-8',newline='\n')
    (output/'GEMINI_HANDOFF.md').write_text('''# Continuidade disponibilizada para este reteste

O fluxo de uso é: o usuário envia a transcrição ao seu próprio agente, que consulta os documentos do projeto como método. Este snapshot não contém resultados de execuções anteriores, notas ou decisões sobre a candidata. Os gates históricos de desenvolvimento e validação semântica do projeto não são promovidos por esta análise; a metodologia não é apresentada como homologada de forma geral.

Não é necessário desenvolver código, executar testes de runtime ou conectar modelos para realizar a análise. Siga o método e exponha os limites da fonte. Consulte START_HERE.md para o escopo desta pasta.
''',encoding='utf-8',newline='\n')
    (output/'LEIA_PRIMEIRO.md').write_text('''# Pacote de reteste

Abra esta pasta como uma área separada em uma conversa nova do agente escolhido. Envie ou indique TAREFA_PARA_O_AGENTE.md. O agente precisa ter acesso aos arquivos desta pasta; anexar somente o ZIP não garante que sua ferramenta consiga lê-lo.

Não adicione relatórios, notas, revisões ou histórico de conversas anteriores. A entrega deve ser guardada antes da comparação. Este pacote separa as entradas; ele não restringe tecnicamente o acesso do agente ao restante do computador ou a outras conversas.

O conteúdo é uma entrevista real, com condições de fidelidade já conhecidas. Este é um teste de aplicação do método com essas condições explícitas, não de adivinhação do trecho perdido nem de detecção cega de todos os erros.
''',encoding='utf-8',newline='\n')
    forbidden=['Relatório-Ingrid','before-review','verification_results','expected_scores','scored_subset_mean','AV-Q4 =','0/4/8/4','média 4,0']
    leaks=[]
    for path in output.rglob('*'):
        if path.is_file():
            text=path.read_text(encoding='utf-8')
            leaks.extend(dict(path=path.relative_to(output).as_posix(),token=token) for token in forbidden if token in text)
    assert not leaks,leaks
    files={p.relative_to(output).as_posix():sha256(p.read_bytes()).hexdigest() for p in output.rglob('*') if p.is_file()}
    manifest=dict(status='READY_AWAITING_USER_AGENT_EXECUTION',source_commit=spec['source_commit'],
        transcript_turn_count=164,transcript_sha256_lf=sha256(raw.encode()).hexdigest(),
        transforms=transforms,file_sha256=files,contains_prior_candidate_scores=False,
        technical_access_isolation=False,blind_execution_proven=False)
    (output/'package_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    archive=output.with_suffix('.zip');assert not archive.exists()
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(output.rglob('*')):
            if path.is_file():z.write(path,path.relative_to(output))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert set(z.namelist())==set(files)|{'package_manifest.json'}
        for path,digest in files.items():assert sha256(z.read(path)).hexdigest()==digest
        assert not any('Reports/' in name or 'Real Interview Pilot/' in name or name.startswith('.git/') for name in z.namelist())
    return dict(status=manifest['status'],folder=str(output),zip=str(archive),zip_sha256=sha256(archive.read_bytes()).hexdigest(),
        method_source_count=len(spec['method_sources']),file_count=len(files)+1,transcript_turn_count=164,
        package_checks=dict(prior_score_markers_absent=True,source_turn_count_preserved=True,archive_integrity=True,
            file_hashes_verified=True,prior_report_directories_absent=True),execution_performed=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--git',default=shutil.which('git'))
    args=parser.parse_args()
    if not args.git:parser.error('Specify --git or install Git to build the snapshot.')
    print(json.dumps(build(args.repo,args.output,args.git),ensure_ascii=True,indent=2))
