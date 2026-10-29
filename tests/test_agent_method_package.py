import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile

from scripts.agent_method_package import METHOD_SOURCES, build_package, verify_package


class AgentMethodPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.git = shutil.which("git")
        if not cls.git:
            raise unittest.SkipTest("Git executable required")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        self.run_git("init", "-q")
        self.run_git("config", "user.name", "Package test")
        self.run_git("config", "user.email", "package@example.invalid")
        for name in METHOD_SOURCES:
            p = self.repo / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("# Method fixture\n\nStable method text.\n", encoding="utf-8")
        private = self.repo / "11 - Interview Evaluation/06 - Reports/private.md"
        private.parent.mkdir(parents=True, exist_ok=True)
        private.write_text("PRIVATE_INTERVIEW_SENTINEL", encoding="utf-8")
        self.run_git("add", ".")
        self.run_git("commit", "-qm", "fixture")
        self.output = Path(self.temp.name) / "method.zip"

    def run_git(self, *args):
        return subprocess.check_output([self.git, "-C", str(self.repo), *args], stderr=subprocess.PIPE)

    def build(self, destination=None):
        return build_package(self.repo, destination or self.output, git=self.git)

    def rewrite_zip(self, mutation):
        with zipfile.ZipFile(self.output) as z:
            entries = {n: z.read(n) for n in z.namelist()}
        mutation(entries)
        with zipfile.ZipFile(self.output, "w", zipfile.ZIP_DEFLATED) as z:
            for n, raw in entries.items():
                z.writestr(n, raw)

    def test_build_verifies_and_excludes_interview_and_git(self):
        self.build()
        result = verify_package(self.output)
        self.assertEqual(result["status"], "INTEGRITY_VERIFIED")
        with zipfile.ZipFile(self.output) as z:
            self.assertFalse(any("Reports/" in n or n.startswith(".git/") for n in z.namelist()))
            self.assertNotIn(b"PRIVATE_INTERVIEW_SENTINEL", b"".join(z.read(n) for n in z.namelist()))

    def test_same_revision_produces_same_zip(self):
        self.build()
        another = self.output.with_name("another.zip")
        self.build(another)
        self.assertEqual(self.output.read_bytes(), another.read_bytes())

    def test_working_tree_changes_are_not_exported(self):
        (self.repo / METHOD_SOURCES[0]).write_text("UNCOMMITTED_SENTINEL", encoding="utf-8")
        self.build()
        with zipfile.ZipFile(self.output) as z:
            self.assertNotIn(b"UNCOMMITTED_SENTINEL", z.read(METHOD_SOURCES[0]))

    def test_ref_selects_historical_revision(self):
        first = self.run_git("rev-parse", "HEAD").decode().strip()
        p = self.repo / METHOD_SOURCES[0]
        p.write_text("NEW_REVISION", encoding="utf-8")
        self.run_git("add", ".")
        self.run_git("commit", "-qm", "new")
        build_package(self.repo, self.output, ref=first, git=self.git)
        with zipfile.ZipFile(self.output) as z:
            self.assertNotIn(b"NEW_REVISION", z.read(METHOD_SOURCES[0]))
            self.assertEqual(json.loads(z.read("package_manifest.json"))["source_commit"], first)

    def test_existing_output_is_preserved(self):
        self.output.write_bytes(b"keep")
        with self.assertRaises(FileExistsError):
            self.build()
        self.assertEqual(self.output.read_bytes(), b"keep")

    def test_missing_required_source_leaves_no_output(self):
        self.run_git("rm", "--", METHOD_SOURCES[0])
        self.run_git("commit", "-qm", "missing")
        with self.assertRaises(ValueError):
            self.build()
        self.assertFalse(self.output.exists())

    def test_changed_member_is_rejected(self):
        self.build()
        self.rewrite_zip(lambda e: e.update({METHOD_SOURCES[0]: b"changed"}))
        with self.assertRaises(ValueError):
            verify_package(self.output)

    def test_extra_file_is_rejected_even_if_added_to_manifest(self):
        self.build()
        def mutation(entries):
            import hashlib
            name = "11 - Interview Evaluation/06 - Reports/private.md"
            entries[name] = b"private"
            manifest = json.loads(entries["package_manifest.json"])
            manifest["file_sha256"][name] = hashlib.sha256(b"private").hexdigest()
            entries["package_manifest.json"] = json.dumps(manifest).encode()
        self.rewrite_zip(mutation)
        with self.assertRaises(ValueError):
            verify_package(self.output)

    def test_duplicate_member_is_rejected(self):
        self.build()
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(self.output, "a") as z:
                z.writestr(METHOD_SOURCES[0], b"duplicate")
        with self.assertRaises(ValueError):
            verify_package(self.output)

    def test_traversal_name_is_rejected_without_extracting(self):
        self.build()
        self.rewrite_zip(lambda e: e.update({"../outside.md": b"outside"}))
        with self.assertRaises(ValueError):
            verify_package(self.output)
        self.assertFalse(self.output.parent.parent.joinpath("outside.md").exists())
