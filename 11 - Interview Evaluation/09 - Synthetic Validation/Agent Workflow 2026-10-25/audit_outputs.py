"""Reproducible structural checks; does not judge semantic correctness or score quality."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

FOLDER=Path(__file__).resolve().parent
ROOT=FOLDER.parents[2]
DIMENSIONS={'correctness','completeness','depth','reasoning','practical_application','trade_offs'}


def audit_case(case,report,manifest):
    turns={t['id']:t for t in case['turns']}
    coverage=report['turn_disposition']
    evaluations=report['evaluations']
    references_valid=all(all(s in turns for s in e['prompt_turns']+e['response_turns']) for e in evaluations)
    return dict(
        frozen_inputs_and_expectations=(
            sha256((FOLDER/'cases'/(case['id']+'.json')).read_bytes()).hexdigest()==manifest['input_sha256'] and
            sha256((FOLDER/'reference'/(case['id']+'.json')).read_bytes()).hexdigest()==manifest['expectations_sha256']),
        exact_original_preserved=report['original_transcript']==case['turns'],
        every_turn_accounted_once=len(coverage)==len(turns) and {t['source_id'] for t in coverage}==set(turns),
        evidence_quotes_and_authors_match_source=all(
            e['source_id'] in turns and e['quote']==turns[e['source_id']]['text'] and
            e['author']==turns[e['source_id']]['speaker'] and turns[e['source_id']]['role']=='candidate'
            for e in report['evidence']),
        question_and_response_references_exist=references_valid,
        dimension_contract=all(set(e['dimensions'])==DIMENSIONS and all(
            type(d['applicable']) is bool and (d['applicable'] or d['assessment']=='N/A')
            for d in e['dimensions'].values()) for e in evaluations),
        uncertainty_not_scored_as_zero=all(e['score'] is None for e in evaluations if e['status']=='DEFERRED_TRANSCRIPTION_UNCERTAINTY') and
            (not any(e['status']=='DEFERRED_TRANSCRIPTION_UNCERTAINTY' for e in evaluations) or report['assessment_complete'] is False),
        cited_project_sources_exist=all((ROOT/p).is_file() for p in report['consulted_project_sources']),
        synthetic_nonblind_limit_visible=report['synthetic'] is True and report['blind'] is False and report['independent'] is False,
        no_global_score_or_applied_lexical_changes=report['global_score'] is None and all(
            p['status']=='UNCONFIRMED_HYPOTHESIS_NOT_APPLIED' for p in report['transcript_proposals']))


def audit_run():
    manifest=json.loads((FOLDER/'manifest.json').read_text(encoding='utf-8'))
    cases=[];controls=[]
    for entry in manifest['cases']:
        cid=entry['case_id']
        case=json.loads((FOLDER/'cases'/(cid+'.json')).read_text(encoding='utf-8'))
        report=json.loads((FOLDER/'analyses'/(cid+'.json')).read_text(encoding='utf-8'))
        checks=audit_case(case,report,entry)
        cases.append(dict(case_id=cid,checks=checks,all_structural_checks_passed=all(checks.values())))
        if cid=='SYN-AGENT-01':
            corrupted=deepcopy(report);corrupted['evidence'][0]['quote']+=' invented content'
            controls.append(dict(name='invented_quote_is_detected',detected=not audit_case(case,corrupted,entry)['evidence_quotes_and_authors_match_source']))
        if cid=='SYN-AGENT-02':
            corrupted=deepcopy(report);corrupted['evaluations'][0]['score']=0
            controls.append(dict(name='zero_for_transcription_loss_is_detected',detected=not audit_case(case,corrupted,entry)['uncertainty_not_scored_as_zero']))
    return dict(scope='STRUCTURAL_CHECKS_ONLY',blind=False,independent=False,cases=cases,negative_controls=controls,
        structural_check_count=sum(len(c['checks']) for c in cases),
        all_structural_checks_passed=all(c['all_structural_checks_passed'] for c in cases),
        all_negative_controls_detected=all(c['detected'] for c in controls))


if __name__=='__main__':
    result=audit_run()
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['all_structural_checks_passed'] and result['all_negative_controls_detected'] else 1)
