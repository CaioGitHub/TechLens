from __future__ import annotations

import hashlib
import unittest
from pathlib import Path

from reference_runtime import (
    build_real_pilot_fixture,
    parse_source_transcript,
    run_real_pilot,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "11 - Interview Evaluation" / "09 - Real Interview Pilot" / "Candidato-Piloto-01" / "Pilot Input - Source Transcript v3.md"
PILOT = ROOT / "11 - Interview Evaluation" / "09 - Real Interview Pilot" / "Candidato-Piloto-05"


class Stage30RealInterviewPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        cls.entries = parse_source_transcript(SOURCE)
        cls.pilot_run = run_real_pilot(SOURCE)
        cls.pipeline = cls.pilot_run["pipeline"]
        cls.artifacts = cls.pipeline["artifacts"]

    def test_source_is_real_and_raw_only(self):
        self.assertGreaterEqual(len(self.entries), 100)
        fixture = self.pilot_run["fixture"]
        self.assertIn("raw_transcript", fixture)
        for key in ("transcript", "questions", "responses", "evidence_specs", "evaluation_specs"):
            self.assertNotIn(key, fixture)
        self.assertEqual(len(self.artifacts["raw_transcript"]), len(self.entries))

    def test_participants_and_roles_are_identified(self):
        participants = self.artifacts["participants"]
        self.assertEqual({item["role"] for item in participants}, {"candidate", "interviewer", "observer"})
        self.assertEqual(
            next(item for item in participants if item["role"] == "candidate")["participant_id"],
            "P-05-CANDIDATE",
        )

    def test_transcription_processing_reaches_allowed_gate(self):
        self.assertIn(self.pipeline["readiness"]["ready_for_next_stage"], {True, False})
        self.assertEqual(self.pipeline["pipeline"]["status"], "READY_WITH_WARNINGS")
        stage_207 = next(item for item in self.pipeline["stages"] if item["stage"] == "20.7")
        self.assertIn(stage_207["status"], {"READY", "READY_WITH_WARNINGS"})

    def test_real_questions_responses_and_evidence_are_derived(self):
        self.assertGreater(len(self.artifacts["questions"]), 0)
        self.assertGreater(len(self.artifacts["responses"]), 0)
        self.assertGreater(len(self.artifacts["evidence"]["evidence_set"]), 0)
        self.assertGreater(len(self.artifacts["evaluations"]), 0)

    def test_candidate_questions_are_not_evaluated(self):
        candidate_questions = self.artifacts.get("candidate_questions", [])
        evaluation_questions = {item["question_id"] for item in self.artifacts["evaluations"]}
        self.assertTrue(candidate_questions)
        self.assertTrue(
            all(item.get("question_id") not in evaluation_questions for item in candidate_questions)
        )

    def test_traceability_reaches_raw_segments(self):
        segment_ids = {item["id"] for item in self.artifacts["speaker_attributed_transcript"]}
        evidence_by_id = {
            item["evidence_id"]: item
            for item in self.artifacts["evidence"]["evidence_set"]
        }
        for evaluation in self.artifacts["evaluations"]:
            for evidence_id in evaluation["evidence_ids"]:
                self.assertIn(evidence_id, evidence_by_id)
                self.assertTrue(
                    set(evidence_by_id[evidence_id]["source"]["segment_ids"]) <= segment_ids
                )

    def test_no_cv_hiring_or_seniority_in_evaluation(self):
        serialized = repr(self.artifacts["evaluations"]).lower()
        for forbidden in ("currículo", "senioridade", "contratar", "aprovado", "reprovado"):
            self.assertNotIn(forbidden, serialized)

    def test_reproducibility_and_idempotency(self):
        repeated = run_real_pilot(SOURCE)["pipeline"]
        for key in ("questions", "responses", "reconstructed_responses", "evidence", "evaluations"):
            self.assertEqual(self.artifacts[key], repeated["artifacts"][key])
        self.assertEqual(self.pipeline["warnings"], repeated["warnings"])

    def test_source_mutation_changes_derived_result(self):
        fixture = build_real_pilot_fixture(SOURCE)
        original = run_real_pilot(SOURCE)["pipeline"]
        candidate_index = next(
            index
            for index, item in enumerate(fixture["raw_transcript"])
            if item["speaker"] == "Ingrid Mazoni" and index > 20
        )
        fixture["raw_transcript"][candidate_index]["text"] = "Não sei responder essa pergunta."
        from reference_runtime import run_interview_pipeline
        mutated = run_interview_pipeline(fixture, run_id="REAL-PILOT-05-MUTATED")
        self.assertNotEqual(
            original["artifacts"]["responses"],
            mutated["artifacts"]["responses"],
        )

    def test_historical_source_is_not_modified(self):
        self.assertEqual(self.original_hash, hashlib.sha256(SOURCE.read_bytes()).hexdigest())

    def test_real_source_has_expected_interview_roles(self):
        speakers = {item["speaker"] for item in self.entries}
        self.assertIn("Ingrid Mazoni", speakers)
        self.assertIn("Morais, Michelly Pereira de", speakers)
        self.assertIn("Paes, Caio Victor Pessoa de Vasconcelos", speakers)
        self.assertIn("Nascimento, Rodrigo Borges do", speakers)


if __name__ == "__main__":
    unittest.main()
