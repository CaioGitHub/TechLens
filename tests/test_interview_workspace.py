from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from scripts.agent_method_package import FORMAT as METHOD_FORMAT
from scripts.interview_workspace import METHOD_FILES, prepare_analysis, prepare_review


class InterviewWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.method = self.root / 'method.zip'
        files = {n: b'# Fictitious method fixture\n' for n in METHOD_FILES if n != 'package_manifest.json'}
        files['package_manifest.json'] = json.dumps({
            'package_format': METHOD_FORMAT, 'source_commit': 'a'*40,
            'file_sha256': {n: sha256(b).hexdigest() for n, b in files.items()},
            'transcript_included': False, 'candidate_report_included': False,
        }).encode()
        with zipfile.ZipFile(self.method, 'w') as z:
            for name, raw in files.items():
                z.writestr(name, raw)
        self.transcript = self.root / 'source.md'
        self.transcript.write_bytes('Pessoa — 00:03\r\nEu não implementei.\r\n'.encode('utf-8'))
        self.workspace = self.root / 'analysis'
        self.review = self.root / 'review'
        self.analysis = self.root / 'delivery.md'
        self.analysis.write_bytes(b'# First delivery\r\n')
        self.record = self.root / 'record.md'
        self.record.write_bytes(b'# Actual consultations\r\n')

    def prepare(self, **kwargs):
        return prepare_analysis(self.method, self.transcript, self.workspace, **kwargs)

    def test_analysis_preserves_exact_source_and_conditions_with_method(self):
        conditions = self.root / 'conditions.md'
        conditions.write_bytes(b'\xef\xbb\xbf# Conditions\r\nAudio unknown.\r\n')
        result = self.prepare(conditions=conditions)
        self.assertEqual(result['status'], 'PREPARED_NOT_EXECUTED')
        self.assertEqual((self.workspace/'TRANSCRICAO_ORIGINAL.md').read_bytes(), self.transcript.read_bytes())
        self.assertEqual((self.workspace/'CONDICOES_DA_FONTE.md').read_bytes(), conditions.read_bytes())
        for name in METHOD_FILES:
            self.assertTrue((self.workspace/'METODO'/name).is_file())
        self.assertFalse((self.workspace/'ENTREGA_DA_ANALISE.md').exists())

    def test_missing_conditions_are_unknown_not_confirmed(self):
        self.prepare()
        body = (self.workspace/'CONDICOES_DA_FONTE.md').read_text(encoding='utf-8')
        self.assertIn('não informados', body)
        self.assertFalse(json.loads((self.workspace/'workspace_manifest.json').read_bytes())['conditions_supplied'])

    def test_review_is_self_contained_preserves_outputs_and_excludes_unselected_files(self):
        self.prepare()
        (self.workspace/'unrelated-private.md').write_text('DO NOT COPY')
        feedback = self.root/'feedback.md'
        feedback.write_bytes(b'# A later comment\r\n')
        before = {p.relative_to(self.workspace): p.read_bytes() for p in self.workspace.rglob('*') if p.is_file()}
        prepare_review(self.workspace, self.analysis, self.record, self.review, feedback)
        for name in METHOD_FILES:
            self.assertEqual((self.review/'METODO'/name).read_bytes(), (self.workspace/'METODO'/name).read_bytes())
        self.assertEqual((self.review/'TRANSCRICAO_ORIGINAL.md').read_bytes(), self.transcript.read_bytes())
        self.assertEqual((self.review/'ENTREGA_RECEBIDA.md').read_bytes(), self.analysis.read_bytes())
        self.assertEqual((self.review/'REGISTRO_RECEBIDO.md').read_bytes(), self.record.read_bytes())
        self.assertEqual((self.review/'FEEDBACK_RECEBIDO.md').read_bytes(), feedback.read_bytes())
        self.assertFalse((self.review/'unrelated-private.md').exists())
        self.assertEqual(before, {p.relative_to(self.workspace): p.read_bytes() for p in self.workspace.rglob('*') if p.is_file()})
        self.assertEqual(json.loads((self.review/'workspace_manifest.json').read_bytes())['phase'], 'assisted_review')

    def test_review_without_feedback_is_not_marked_blind_or_assisted(self):
        self.prepare()
        prepare_review(self.workspace, self.analysis, self.record, self.review)
        self.assertEqual(json.loads((self.review/'workspace_manifest.json').read_bytes())['phase'], 'exposed_review')
        self.assertFalse((self.review/'FEEDBACK_RECEBIDO.md').exists())

    def test_corrupt_method_and_invalid_text_leave_no_workspace(self):
        self.method.write_bytes(b'not a zip')
        with self.assertRaises((ValueError, zipfile.BadZipFile)):
            self.prepare()
        self.assertFalse(self.workspace.exists())

    def test_non_utf8_source_is_rejected_without_output(self):
        self.transcript.write_bytes(b'\xff\xfe\xff')
        with self.assertRaises(ValueError):
            self.prepare()
        self.assertFalse(self.workspace.exists())

    def test_changed_input_blocks_review_before_writing(self):
        self.prepare()
        (self.workspace/'TRANSCRICAO_ORIGINAL.md').write_text('Changed')
        with self.assertRaisesRegex(ValueError, 'changed'):
            prepare_review(self.workspace, self.analysis, self.record, self.review)
        self.assertFalse(self.review.exists())

    def test_extra_manifest_path_cannot_copy_arbitrary_file(self):
        self.prepare()
        p = self.workspace/'workspace_manifest.json'
        manifest = json.loads(p.read_bytes())
        manifest['file_sha256']['../delivery.md'] = sha256(self.analysis.read_bytes()).hexdigest()
        p.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            prepare_review(self.workspace, self.analysis, self.record, self.review)
        self.assertFalse(self.review.exists())

    def test_invalid_manifest_schema_is_rejected_before_review(self):
        self.prepare()
        p = self.workspace/'workspace_manifest.json'
        valid = json.loads(p.read_bytes())
        for invalid in ([], dict(valid, file_sha256=None)):
            with self.subTest(invalid=invalid):
                p.write_text(json.dumps(invalid))
                with self.assertRaises(ValueError):
                    prepare_review(self.workspace, self.analysis, self.record, self.review)
                self.assertFalse(self.review.exists())

    def test_existing_folders_and_nested_review_are_preserved(self):
        self.prepare()
        with self.assertRaises(FileExistsError):
            self.prepare()
        nested = self.workspace/'nested'
        with self.assertRaises(ValueError):
            prepare_review(self.workspace, self.analysis, self.record, nested)
        self.assertFalse(nested.exists())
        self.review.mkdir()
        marker = self.review/'keep.md'
        marker.write_bytes(b'keep')
        with self.assertRaises(FileExistsError):
            prepare_review(self.workspace, self.analysis, self.record, self.review)
        self.assertEqual(marker.read_bytes(), b'keep')


if __name__ == '__main__':
    unittest.main()
