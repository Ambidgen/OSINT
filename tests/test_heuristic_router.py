"""Tests for heuristic question refinement, framing neutralization, and dual-track routing."""

from __future__ import annotations

import unittest

from osint_agent.loader import DirectoryRepository
from osint_agent.router import HeuristicRouter


class TestHeuristicRouter(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = DirectoryRepository()
        self.router = HeuristicRouter(self.repo)

    def test_loaded_prompt_triggers_neutralization_and_sycophancy_guardrail(self) -> None:
        plan = self.router.route(
            "Why did export bans on EUV lithography chips to China completely fail?"
        )
        self.assertGreaterEqual(len(plan.framing_alerts), 1)
        self.assertNotIn("completely fail", plan.suggested_neutral_framing.lower())
        self.assertEqual(plan.primary_domain["id"], "technology_cyber_ai")
        self.assertEqual(plan.geographic_scope["id"], "east_asia_pacific")
        cluster_ids = [c["id"] for c in plan.matched_concept_clusters]
        self.assertIn("semiconductor_lithography_and_export_chokepoints", cluster_ids)
        bias_ids = [b["id"] for b in plan.guardrail_watch_list["biases_to_monitor"]]
        self.assertIn("sycophancy_prompt_framing_bias", bias_ids)

    def test_neutral_question_does_not_false_trigger_framing_alerts(self) -> None:
        plan = self.router.route(
            "What did the ICJ provisional measures order state regarding treaty jurisdiction?"
        )
        self.assertEqual(plan.framing_alerts, [])
        self.assertEqual(plan.primary_domain["id"], "law_governance_human_rights")
        cluster_ids = [c["id"] for c in plan.matched_concept_clusters]
        self.assertIn("international_law_icj_ihl_and_maritime_treaties", cluster_ids)

    def test_short_acronyms_do_not_false_match_inside_longer_words(self) -> None:
        # 'unemployment' begins with 'un' and 'poll' should not match 'apollo'
        plan = self.router.route(
            "How have unemployment and real wages evolved in Brazil this year?"
        )
        self.assertEqual(plan.geographic_scope["id"], "latin_america_caribbean")
        self.assertIn(
            plan.primary_domain["id"],
            ("society_demographics_labor", "economics_markets_trade"),
        )
        reg_ids = [
            s["id"]
            for s in plan.journalist_source_bundle["regional_record_counterweights"]
        ]
        self.assertIn("folha_de_spaulo", reg_ids)

    def test_breaking_horizon_detection_attaches_fog_of_war_bias(self) -> None:
        plan = self.router.route(
            "Breaking: explosion reported near Red Sea naval strait hours ago"
        )
        self.assertEqual(plan.temporal_horizon["id"], "breaking_sub_24h")
        self.assertEqual(plan.primary_domain["id"], "conflict_defense_security")
        self.assertEqual(plan.geographic_scope["id"], "middle_east_north_africa")
        bias_ids = [b["id"] for b in plan.guardrail_watch_list["biases_to_monitor"]]
        self.assertIn("breaking_news_speed_bias", bias_ids)

    def test_epidemiology_routing_pairs_medical_journalism_and_systematic_reviews(self) -> None:
        plan = self.router.route(
            "What is the true case fatality ratio and spillover risk in the latest H5N1 outbreak?"
        )
        self.assertEqual(plan.primary_domain["id"], "science_medicine_public_health")
        specialist_ids = [
            s["id"] for s in plan.journalist_source_bundle["specialist_and_verification"]
        ]
        self.assertIn("stat_news", specialist_ids)
        academic_ids = [s["id"] for s in plan.academic_source_bundle]
        self.assertIn("cochrane_library", academic_ids)
        self.assertIn("retraction_watch", academic_ids)


if __name__ == "__main__":
    unittest.main()
