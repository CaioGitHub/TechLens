from pathlib import Path
import ast
import hashlib
import io
import json
import os
import sys
import time
import unittest

root = Path(__file__).resolve().parents[1]
os.chdir(root)
sys.path.insert(0, str(root))
folder = root / '11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05'
runtime = root / 'reference_runtime/runtime.py'
entry = root / 'reference_runtime/runtime.py.inc1_contracts_question_entry'
exclude = {'SemanticQuestionProfiler', 'DiscoursePropositionEngine'}
def structure(p):
    return [ast.dump(n, include_attributes=False) for n in ast.parse(p.read_text(encoding='utf-8-sig')).body
            if getattr(n, 'name', None) not in exclude]
assert structure(entry) == structure(runtime), 'Changes outside authorized extraction classes'
before = hashlib.sha256(runtime.read_bytes()).hexdigest().upper()
mode = sys.argv[1]
suite = (unittest.defaultTestLoader.discover('tests', pattern='test_*.py') if mode == 'canonical'
         else unittest.defaultTestLoader.loadTestsFromName('tests.test_stage_26_reference_harness'))
stream = io.StringIO()
start = time.perf_counter()
result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
after = hashlib.sha256(runtime.read_bytes()).hexdigest().upper()
record = {'suite': mode, 'run': result.testsRun, 'failures': len(result.failures),
          'errors': len(result.errors), 'skipped': len(result.skipped),
          'passed': result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped),
          'seconds': round(time.perf_counter() - start, 3), 'successful': result.wasSuccessful(),
          'hash_before': before, 'hash_after': after, 'runtime_unchanged_during_tests': before == after,
          'ast_unchanged_outside_extraction_classes': True, 'output': stream.getvalue()}
(folder / f'stage_31_7_35_contracts_{mode}.json').write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k:v for k,v in record.items() if k != 'output'}, indent=2), flush=True)
if not result.wasSuccessful():
    print(stream.getvalue())
raise SystemExit(0 if result.wasSuccessful() and before == after else 1)
