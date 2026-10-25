"""Controlled report review checks; explicit dependencies are not semantic inference."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import re
import unittest

from audit_claims import audit_claims

FOLDER=Path(__file__).resolve().parent
ROOT=FOLDER.parents[3]


def policy_record(scope='candidate_knowledge',text='Source-based claim',refs=None,score=None):
    refs=['P1@07:22'] if refs is None else refs
    return dict(source_states={'P1@07:22':'unrecoverable','P1@05:10':'usable'},
        claims=[dict(id='C1',scope=scope,source_ids=refs,text=text)],
        evaluations=[dict(id='Q9',source_ids=refs,score=score)])


class QualitativeUncertaintyRegressionTests(unittest.TestCase):
    def test_unscored_negative_knowledge_claim_is_rejected(self):
        self.assertFalse(audit_claims(policy_record(text='Limitação de conhecimento declarada.'))['passed'])

    def test_unscored_positive_knowledge_claim_is_rejected(self):
        self.assertFalse(audit_claims(policy_record(text='Domínio do serviço demonstrado.'))['passed'])

    def test_experience_claim_is_also_rejected(self):
        self.assertFalse(audit_claims(policy_record(scope='candidate_experience'))['passed'])

    def test_adding_a_reliable_source_does_not_launder_the_bad_source(self):
        self.assertFalse(audit_claims(policy_record(refs=['P1@05:10','P1@07:22']))['passed'])

    def test_zero_is_not_a_substitute_for_deferral(self):
        record=policy_record(scope='assessment_status',score=0)
        self.assertFalse(audit_claims(record)['passed'])

    def test_original_can_be_preserved_as_a_source_record(self):
        self.assertTrue(audit_claims(policy_record(scope='source_record'))['passed'])

    def test_deferral_can_be_explained_without_judging_the_candidate(self):
        self.assertTrue(audit_claims(policy_record(scope='assessment_status'))['passed'])

    def test_unaffected_evidence_keeps_its_own_evaluation(self):
        self.assertTrue(audit_claims(policy_record(refs=['P1@05:10'],score=4))['passed'])


def scoring_sections(text):
    return re.findall(r'### AV-[^\n]+\n.*?(?=\n### |\n## |\Z)',text,re.S)


def verify_review():
    decisions=json.loads((FOLDER/'review_decisions.json').read_text(encoding='utf-8'))
    snapshot=(FOLDER/'Relatório-Ingrid Mazoni.before-review.md').read_bytes()
    report_path=ROOT/decisions['report_path']
    report=report_path.read_text(encoding='utf-8')
    source=ROOT/decisions['source_path']
    before=json.loads((FOLDER/'regression_case.json').read_text(encoding='utf-8'))
    before_result=audit_claims(before)
    states={ref:'usable' for ref in ['P2@04:27','P1@04:34','P1@04:37','P1@05:04','P1@05:10',
        'P1@05:36','P1@05:53','P1@08:01','P1@08:16','P1@08:21','P1@08:26']}
    states['P2@04:27']='confirmed_wording';states['P1@07:22']='unrecoverable'
    refs={
        'AV-Q4':['P2@04:27','P1@04:34','P1@04:37'],
        'AV-Q5':['P1@05:04','P1@05:10'],
        'AV-Q6.1':['P1@05:36','P1@05:53'],
        'AV-Q10':['P1@08:01','P1@08:16','P1@08:21','P1@08:26']}
    scores=[float(s) for s in re.findall(r'\*\*Nota: ([0-9.]+)/10',report)]
    before_scores=[float(s) for s in re.findall(r'\*\*Nota: ([0-9.]+)/10',snapshot.decode('utf-8'))]
    record=dict(source_states=states,claims=[dict(id=q,scope='candidate_knowledge',source_ids=ids,
        text='Existing technical judgment preserved; evidence references manually audited.') for q,ids in refs.items()]+[
        dict(id='Q9-status',scope='assessment_status',source_ids=['P1@07:22'],text='Resposta adiada por transcrição irrecuperável; conhecimento não avaliado.')],
        evaluations=[dict(id=q,score=score,source_ids=ids) for (q,ids),score in zip(refs.items(),scores)]+
            [dict(id='Q9',score=None,source_ids=['P1@07:22'])])
    current=audit_claims(record)
    checks=dict(
        original_report_preserved=sha256(snapshot).hexdigest()==decisions['original_report_sha256'],
        received_source_unchanged=sha256(source.read_text(encoding='utf-8').encode()).hexdigest()==decisions['received_source_sha256_lf'],
        all_four_scoring_sections_unchanged=len(scoring_sections(report))==4 and scoring_sections(report)==scoring_sections(snapshot.decode('utf-8')),
        numeric_scores_unchanged=len(scores)==4 and scores==before_scores,
        scored_subset_mean_unchanged=len(scores)==4 and sum(scores)/len(scores)==decisions['expected_scored_subset_mean'],
        partial_report_label='# Relatório de análise parcial — Ingrid Mazoni' in report,
        E07_not_in_used_evidence_table='| E07 |' not in report,
        Q9_explicitly_deferred='ADIADA_POR_TRANSCRIÇÃO' in report,
        old_negative_Azure_judgment_removed='Q9: limitação declarada no recorte' not in report and 'candidata nega uso no recorte' not in report,
        F01_reconfirmed=decisions['F01']['status']=='USER_CONFIRMED' and 'Sim, confirmei essa formulação' in report,
        baseline_failure_reproduced=before_result['passed'] is False,
        current_explicit_dependencies_pass=current['passed'])
    return dict(status='CONTROLLED_REVIEW_VERIFIED' if all(checks.values()) else 'REVIEW_CHECK_FAILED',
        checks=checks,before_dependency_audit=before_result,after_dependency_audit=current,
        final_claim_dependencies=record,
        limitation='Dependencies and prose classifications are manually supplied. These checks do not detect all semantic claims in free text or validate score calibration.',
        final_report_sha256_lf=sha256(report.encode()).hexdigest())


if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(QualitativeUncertaintyRegressionTests)
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    review=verify_review()
    print(json.dumps(dict(policy_tests_run=result.testsRun,policy_tests_passed=result.wasSuccessful(),
        review_status=review['status'],checks=review['checks']),ensure_ascii=False,indent=2))
    raise SystemExit(0 if result.wasSuccessful() and review['status']=='CONTROLLED_REVIEW_VERIFIED' else 1)
