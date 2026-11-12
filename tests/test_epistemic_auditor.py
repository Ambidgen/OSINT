"""Tests for the Epistemic Guardrail & Introspection Gate and CLI subcommands."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from osint_agent.auditor import EpistemicAuditor
from osint_agent.loader import DirectoryRepository


class TestEpistemicAuditor(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = DirectoryRepository()
        self.auditor = EpistemicAuditor(self.repo)
        self.sample_path = self.repo.repo_root / "examples" / "sample_research_dossier.json"
        self.flawed_path = self.repo.repo_root / "examples" / "flawed_research_dossier.json"
        with self.sample_path.open("r", encoding="utf-8") as fh:
            self.valid_dossier = json.load(fh)
        with self.flawed_path.open("r", encoding="utf-8") as fh:
            self.flawed_dossier = json.load(fh)

    def test_sample_dossier_passes_all_gates_with_perfect_score(self) -> None:
        result = self.auditor.audit_dossier(self.valid_dossier)
        self.assertEqual(result.status, "PASS", f"Unexpected findings: {result.findings}")
        self.assertTrue(result.passed_gate)
        self.assertEqual(result.epistemic_score, 100)

    def test_flawed_dossier_fails_multiple_epistemic_gates(self) -> None:
        result = self.auditor.audit_dossier(self.flawed_dossier)
        self.assertEqual(result.status, "FAIL")
        self.assertFalse(result.passed_gate)
        codes = {f.code for f in result.findings}
        self.assertIn("unneutralized_loaded_prompt", codes)
        self.assertIn("uncorroborated_or_echo_confirmed_fact", codes)
        self.assertIn("preprint_cited_as_settled_consensus", codes)
        self.assertIn("unflagged_preprint_risk", codes)
        self.assertIn("single_hypothesis_tunnel_vision", codes)
        self.assertIn("missing_fallacy_or_bias_audit", codes)
        self.assertIn("rhetorical_overconfidence_detected", codes)
        self.assertIn("uncalibrated_high_confidence", codes)

    def test_citogenesis_shared_upstream_provenance_is_caught(self) -> None:
        mutated = copy.deepcopy(self.valid_dossier)
        # Force both A1/A2 citations on claim_02 to share the exact same upstream provenance
        shared_root = "Single anonymous official briefing in Capital X"
        for cit in mutated["journalist_track"]["evidence_ledger"][1]["citations"]:
            cit["upstream_provenance"] = shared_root
            cit["source_id"] = "reuters"
        result = self.auditor.audit_dossier(mutated)
        self.assertEqual(result.status, "FAIL")
        codes = {f.code for f in result.findings}
        self.assertIn("uncorroborated_or_echo_confirmed_fact", codes)

    def test_missing_academic_concepts_triggers_failure(self) -> None:
        mutated = copy.deepcopy(self.valid_dossier)
        mutated["academic_track"]["concepts_explained"] = []
        result = self.auditor.audit_dossier(mutated)
        self.assertEqual(result.status, "FAIL")
        codes = {f.code for f in result.findings}
        self.assertIn("missing_academic_concept_buttressing", codes)

    def test_cli_json_outputs_and_exit_codes(self) -> None:
        cmd_base = [sys.executable, "-m", "osint_agent"]

        val_proc = subprocess.run(
            [*cmd_base, "validate", "--format", "json"],
            cwd=self.repo.repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(val_proc.returncode, 0, val_proc.stderr)
        val_json = json.loads(val_proc.stdout)
        self.assertTrue(val_json["valid"])

        route_proc = subprocess.run(
            [*cmd_base, "route", "What caused the FX swap basis spike?", "--format", "json"],
            cwd=self.repo.repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(route_proc.returncode, 0, route_proc.stderr)
        route_json = json.loads(route_proc.stdout)
        self.assertEqual(
            route_json["classification"]["primary_domain"]["id"],
            "economics_markets_trade",
        )

        pass_audit = subprocess.run(
            [*cmd_base, "audit", str(self.sample_path), "--format", "json"],
            cwd=self.repo.repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(pass_audit.returncode, 0)
        self.assertEqual(json.loads(pass_audit.stdout)["status"], "PASS")

        fail_audit = subprocess.run(
            [*cmd_base, "audit", str(self.flawed_path), "--format", "json"],
            cwd=self.repo.repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(fail_audit.returncode, 1)
        self.assertEqual(json.loads(fail_audit.stdout)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
