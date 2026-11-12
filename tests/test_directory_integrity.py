"""Tests for schema validation, cross-file referential integrity, and source diversity invariants."""

from __future__ import annotations

import unittest

from osint_agent.loader import DirectoryRepository
from osint_agent.validator import validate_repository


class TestDirectoryIntegrity(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = DirectoryRepository()

    def test_full_repository_schema_and_referential_validation(self) -> None:
        report = validate_repository(self.repo.repo_root)
        self.assertTrue(report.is_valid, f"Validation errors: {report.errors}")
        self.assertEqual(report.warnings, [], f"Unexpected warnings: {report.warnings}")
        self.assertGreaterEqual(report.stats["media_and_primary_sources"], 40)
        self.assertGreaterEqual(report.stats["academic_and_concept_sources"], 20)
        self.assertEqual(report.stats["domains"], 8)

    def test_every_non_global_region_has_regional_record_sources(self) -> None:
        regions = [
            r["id"]
            for r in self.repo.taxonomy["geographic_regions"]
            if r["id"] != "global"
        ]
        for reg_id in regions:
            regional_sources = [
                s
                for s in self.repo.media_sources_by_id.values()
                if s["tier"] == "tier_2_regional_record" and reg_id in s["regions"]
            ]
            self.assertGreaterEqual(
                len(regional_sources),
                1,
                f"Region '{reg_id}' lacks a dedicated tier_2_regional_record media source",
            )

    def test_all_three_bias_layers_are_populated(self) -> None:
        categories = {e["category"] for e in self.repo.biases_catalog["entries"]}
        self.assertEqual(categories, {"analyst_ai", "media_source", "data_sampling"})

    def test_academic_evidence_hierarchy_covers_all_five_tiers(self) -> None:
        hierarchy_tiers = [
            item["tier_id"] for item in self.repo.concept_taxonomy["evidence_hierarchy"]
        ]
        self.assertEqual(
            hierarchy_tiers,
            [
                "meta_analysis_and_systematic_review",
                "peer_reviewed_primary_literature",
                "technical_standard_and_reference",
                "working_paper_and_policy_analysis",
                "unrefereed_preprint",
            ],
        )

    def test_query_filters_media_and_academic_sources(self) -> None:
        open_cyber = self.repo.query_media_sources(
            domain="technology_cyber_ai",
            open_access_only=True,
        )
        ids = {s["id"] for s in open_cyber}
        self.assertIn("krebs_on_security", ids)
        self.assertIn("cisa_nvd", ids)

        peer_health = self.repo.query_academic_sources(
            domain="science_medicine_public_health",
            peer_reviewed_only=True,
        )
        ac_ids = {s["id"] for s in peer_health}
        self.assertIn("cochrane_library", ac_ids)
        self.assertIn("pubmed_pmc", ac_ids)
        self.assertNotIn("biorxiv_medrxiv", ac_ids)


if __name__ == "__main__":
    unittest.main()
