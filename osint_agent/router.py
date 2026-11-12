"""Heuristic question refinement, framing neutralization, and dual-track source routing."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from .loader import DirectoryRepository


def _term_matches(text_lower: str, term: str) -> bool:
    """Match keywords accurately using word boundaries so short acronyms never false-trigger."""
    escaped = re.escape(term.lower().strip())
    if len(term) <= 4 or " " in term or "." in term:
        pattern = rf"(?<![a-z0-9]){escaped}(?![a-z0-9])"
    else:
        # Allow plural/inflection suffixes on longer stems (e.g. 'tariff' -> 'tariffs')
        stem = escaped[:-1] if escaped.endswith("y") and len(escaped) > 5 else escaped
        pattern = rf"(?<![a-z0-9]){stem}[a-z]*"
    return re.search(pattern, text_lower) is not None


@dataclass
class RoutingPlan:
    """Structured heuristic triage output directing an Agentic AI across Journalist + Academic tracks."""

    raw_question: str
    framing_alerts: list[dict[str, Any]]
    suggested_neutral_framing: str
    primary_domain: dict[str, Any]
    secondary_domains: list[dict[str, Any]]
    geographic_scope: dict[str, Any]
    temporal_horizon: dict[str, Any]
    journalist_subquestions: list[str]
    academic_subquestions: list[str]
    matched_concept_clusters: list[dict[str, Any]]
    journalist_source_bundle: dict[str, list[dict[str, Any]]]
    academic_source_bundle: list[dict[str, Any]]
    guardrail_watch_list: dict[str, list[dict[str, Any]]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw_question": self.raw_question,
            "framing_alerts": self.framing_alerts,
            "suggested_neutral_framing": self.suggested_neutral_framing,
            "classification": {
                "primary_domain": {
                    "id": self.primary_domain["id"],
                    "label": self.primary_domain["label"],
                    "matched_signals": self.primary_domain["matched_signals"],
                },
                "secondary_domains": [
                    {"id": d["id"], "label": d["label"], "matched_signals": d["matched_signals"]}
                    for d in self.secondary_domains
                ],
                "geographic_scope": self.geographic_scope,
                "temporal_horizon": self.temporal_horizon,
            },
            "refinement_questions": {
                "journalist_track": self.journalist_subquestions,
                "academic_track": self.academic_subquestions,
            },
            "matched_concept_clusters": [
                {
                    "id": c["id"],
                    "title": c["title"],
                    "academic_disciplines": c["academic_disciplines"],
                    "foundational_mechanisms": c["foundational_mechanisms"],
                    "common_media_misconceptions": c["common_media_misconceptions"],
                    "pedagogical_bridge_prompt": c["pedagogical_bridge_prompt"],
                }
                for c in self.matched_concept_clusters
            ],
            "recommended_sources": {
                "journalist_track": self.journalist_source_bundle,
                "academic_track": self.academic_source_bundle,
            },
            "guardrail_watch_list": self.guardrail_watch_list,
        }


class HeuristicRouter:
    """Refines raw research questions categorically and assembles diverse OSINT + Academic source bundles."""

    def __init__(self, repo: DirectoryRepository | None = None) -> None:
        self.repo = repo or DirectoryRepository()

    def detect_framing_bias(self, question: str) -> tuple[list[dict[str, Any]], str]:
        """Detect loaded presuppositions or emotional intensifiers and propose neutral phrasing."""
        q_lower = question.lower().strip()
        alerts: list[dict[str, Any]] = []
        matched_terms_all: list[str] = []

        for marker in self.repo.taxonomy["framing_neutralization_markers"]:
            hits = [t for t in marker["trigger_terms"] if _term_matches(q_lower, t)]
            if hits:
                matched_terms_all.extend(hits)
                alerts.append(
                    {
                        "pattern_id": marker["pattern_id"],
                        "category": marker["category"],
                        "matched_terms": hits,
                        "remediation_guidance": marker["remediation_guidance"],
                    }
                )

        if not alerts:
            return [], question.strip()

        cleaned = question.strip().rstrip("!").strip()
        # Strip leading loaded openers to construct an actionable neutral research query
        neutral_core = re.sub(
            r"^(why\s+(did|do|does|is|are|has|have)|prove\s+that|reasons\s+why|list\s+the\s+failures\s+of)\s+",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )
        for term in sorted(matched_terms_all, key=len, reverse=True):
            if term.lower() not in ("why did", "prove that", "reasons why", "list the failures"):
                neutral_core = re.sub(re.escape(term), "", neutral_core, flags=re.IGNORECASE)
        neutral_core = re.sub(r"\b100%\b|\bcompletely\b|\btotally\b", "", neutral_core, flags=re.IGNORECASE)
        neutral_core = re.sub(r"\s+", " ", neutral_core).strip(" ?!.,")
        neutral_core = re.sub(
            r"\s+\b(is|are|was|were|has|have|did|do|does|being)\b$",
            "",
            neutral_core,
            flags=re.IGNORECASE,
        ).strip(" ?!.,")
        suggested = (
            f"What are the verified empirical facts, competing explanations, and underlying mechanisms regarding: "
            f"{neutral_core}?"
        )
        return alerts, suggested

    def route(
        self,
        question: str,
        *,
        region_override: str | None = None,
        horizon_override: str | None = None,
    ) -> RoutingPlan:
        q_lower = question.lower()
        framing_alerts, neutral_framing = self.detect_framing_bias(question)

        # Score concept clusters first so technical jargon also enriches domain scoring
        scored_clusters: list[tuple[int, dict[str, Any]]] = []
        domain_concept_bonus: dict[str, list[str]] = {}
        for cluster in self.repo.concept_taxonomy["concept_clusters"]:
            c_hits = [t for t in cluster["trigger_terms"] if _term_matches(q_lower, t)]
            if c_hits:
                scored_clusters.append((len(c_hits), cluster))
                domain_concept_bonus.setdefault(cluster["domain"], []).extend(c_hits)

        scored_clusters.sort(key=lambda pair: pair[0], reverse=True)

        # Score domains
        scored_domains: list[tuple[int, dict[str, Any], list[str]]] = []
        for dom in self.repo.taxonomy["domains"]:
            kw_hits = [kw for kw in dom["signal_keywords"] if _term_matches(q_lower, kw)]
            bonus_hits = [
                h for h in domain_concept_bonus.get(dom["id"], []) if h not in kw_hits
            ]
            all_hits = kw_hits + bonus_hits
            score = len(kw_hits) * 2 + len(bonus_hits) * 3
            scored_domains.append((score, dom, all_hits))

        scored_domains.sort(key=lambda item: item[0], reverse=True)

        top_score, top_dom, top_hits = scored_domains[0]
        if top_score == 0:
            # Default broad geopolitical/current-events fallback
            top_dom = self.repo.domains_by_id["geopolitics_diplomacy"]
            top_hits = ["default_broad_osint_fallback"]

        primary_domain_info = {
            **top_dom,
            "matched_signals": top_hits,
        }
        secondary_domains_info = [
            {**dom, "matched_signals": hits}
            for score, dom, hits in scored_domains[1:3]
            if score > 0 and dom["id"] != top_dom["id"]
        ]

        # Geographic scope
        selected_region: dict[str, Any] | None = None
        if region_override:
            for reg in self.repo.taxonomy["geographic_regions"]:
                if reg["id"] == region_override:
                    selected_region = {**reg, "matched_signals": ["explicit_override"]}
                    break
            if selected_region is None:
                raise ValueError(f"Unknown region_override: {region_override}")
        else:
            best_reg_score = 0
            for reg in self.repo.taxonomy["geographic_regions"]:
                if reg["id"] == "global":
                    continue
                r_hits = [rk for rk in reg["signal_keywords"] if _term_matches(q_lower, rk)]
                if len(r_hits) > best_reg_score:
                    best_reg_score = len(r_hits)
                    selected_region = {**reg, "matched_signals": r_hits}
            if selected_region is None:
                global_reg = next(
                    r for r in self.repo.taxonomy["geographic_regions"] if r["id"] == "global"
                )
                selected_region = {**global_reg, "matched_signals": ["default_global_scope"]}

        # Temporal horizon
        selected_horizon: dict[str, Any] | None = None
        if horizon_override:
            for hor in self.repo.taxonomy["temporal_horizons"]:
                if hor["id"] == horizon_override:
                    selected_horizon = {**hor, "matched_signals": ["explicit_override"]}
                    break
            if selected_horizon is None:
                raise ValueError(f"Unknown horizon_override: {horizon_override}")
        else:
            best_h_score = 0
            for hor in self.repo.taxonomy["temporal_horizons"]:
                h_hits = [hk for hk in hor["signal_keywords"] if _term_matches(q_lower, hk)]
                if len(h_hits) > best_h_score:
                    best_h_score = len(h_hits)
                    selected_horizon = {**hor, "matched_signals": h_hits}
            if selected_horizon is None:
                dev_hor = next(
                    h
                    for h in self.repo.taxonomy["temporal_horizons"]
                    if h["id"] == "developing_days_weeks"
                )
                selected_horizon = {**dev_hor, "matched_signals": ["default_developing_horizon"]}

        # Concept clusters (include domain cluster if no direct lexical hit)
        matched_clusters = [cluster for _, cluster in scored_clusters[:3]]
        if not matched_clusters:
            matched_clusters = [
                c
                for c in self.repo.concept_taxonomy["concept_clusters"]
                if c["domain"] == primary_domain_info["id"]
            ][:2]

        # Build Journalist Track Source Bundle across distinct tiers
        candidate_media_ids: list[str] = list(primary_domain_info["priority_media_sources"])
        for sec_dom in secondary_domains_info:
            for mid in sec_dom["priority_media_sources"][:3]:
                if mid not in candidate_media_ids:
                    candidate_media_ids.append(mid)

        # Add regional record outlets specifically matching the detected region
        reg_id = selected_region["id"]
        if reg_id != "global":
            for src in self.repo.media_sources_by_id.values():
                if (
                    src["tier"] == "tier_2_regional_record"
                    and reg_id in src["regions"]
                    and src["id"] not in candidate_media_ids
                ):
                    candidate_media_ids.append(src["id"])

        wire_and_record: list[dict[str, Any]] = []
        specialist_and_investigative: list[dict[str, Any]] = []
        regional_counterweights: list[dict[str, Any]] = []

        for mid in candidate_media_ids:
            src = self.repo.media_sources_by_id[mid]
            summary = self._summarize_media_source(src)
            if src["tier"] == "tier_1_global_wire_and_record":
                wire_and_record.append(summary)
            elif src["tier"] in (
                "tier_2_specialist_beat",
                "tier_2_investigative_and_verification",
            ):
                specialist_and_investigative.append(summary)
            elif src["tier"] == "tier_2_regional_record":
                regional_counterweights.append(summary)

        primary_ids: list[str] = list(primary_domain_info["priority_primary_sources"])
        for sec_dom in secondary_domains_info:
            for pid in sec_dom["priority_primary_sources"]:
                if pid not in primary_ids:
                    primary_ids.append(pid)
        primary_registries = [
            self._summarize_media_source(self.repo.media_sources_by_id[pid])
            for pid in primary_ids
        ]

        journalist_bundle = {
            "global_wires_and_record": wire_and_record[:5],
            "specialist_and_verification": specialist_and_investigative[:4],
            "regional_record_counterweights": regional_counterweights[:4],
            "primary_official_and_telemetry": primary_registries[:4],
        }

        # Build Academic Track Source Bundle
        academic_ids: list[str] = list(primary_domain_info["priority_academic_sources"])
        for cluster in matched_clusters:
            for aid in cluster["recommended_academic_sources"]:
                if aid not in academic_ids:
                    academic_ids.append(aid)
        if "retraction_watch" not in academic_ids and primary_domain_info["id"] in (
            "science_medicine_public_health",
            "technology_cyber_ai",
        ):
            academic_ids.append("retraction_watch")

        academic_bundle = [
            self._summarize_academic_source(self.repo.academic_sources_by_id[aid])
            for aid in academic_ids[:6]
        ]

        # Build Guardrail Watch List
        fallacy_ids: list[str] = list(primary_domain_info["high_risk_fallacies"])
        bias_ids: list[str] = list(primary_domain_info["high_risk_biases"])
        if framing_alerts and "sycophancy_prompt_framing_bias" not in bias_ids:
            bias_ids.insert(0, "sycophancy_prompt_framing_bias")
        if selected_horizon["id"] == "breaking_sub_24h" and "breaking_news_speed_bias" not in bias_ids:
            bias_ids.insert(0, "breaking_news_speed_bias")

        guardrail_watch = {
            "fallacies_to_monitor": [
                {
                    "id": fid,
                    "name": self.repo.fallacies_by_id[fid]["name"],
                    "remediation_protocol": self.repo.fallacies_by_id[fid]["remediation_protocol"],
                }
                for fid in fallacy_ids
            ],
            "biases_to_monitor": [
                {
                    "id": bid,
                    "name": self.repo.biases_by_id[bid]["name"],
                    "category": self.repo.biases_by_id[bid]["category"],
                    "remediation_protocol": self.repo.biases_by_id[bid]["remediation_protocol"],
                }
                for bid in bias_ids
            ],
        }

        return RoutingPlan(
            raw_question=question,
            framing_alerts=framing_alerts,
            suggested_neutral_framing=neutral_framing,
            primary_domain=primary_domain_info,
            secondary_domains=secondary_domains_info,
            geographic_scope={
                "id": selected_region["id"],
                "label": selected_region["label"],
                "routing_guidance": selected_region["routing_guidance"],
                "matched_signals": selected_region["matched_signals"],
            },
            temporal_horizon={
                "id": selected_horizon["id"],
                "label": selected_horizon["label"],
                "journalist_routing_rule": selected_horizon["journalist_routing_rule"],
                "academic_routing_rule": selected_horizon["academic_routing_rule"],
                "primary_risk": selected_horizon["primary_risk"],
            },
            journalist_subquestions=list(primary_domain_info["refinement_questions_journalist"]),
            academic_subquestions=list(primary_domain_info["refinement_questions_academic"]),
            matched_concept_clusters=matched_clusters,
            journalist_source_bundle=journalist_bundle,
            academic_source_bundle=academic_bundle,
            guardrail_watch_list=guardrail_watch,
        )

    @staticmethod
    def _summarize_media_source(src: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": src["id"],
            "name": src["name"],
            "url": src["url"],
            "tier": src["tier"],
            "access_model": src["access_model"],
            "baseline_admiralty_reliability": src["baseline_admiralty_reliability"],
            "corroboration_pairing_rule": src["corroboration_pairing_rule"],
        }

    @staticmethod
    def _summarize_academic_source(src: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": src["id"],
            "name": src["name"],
            "url": src["url"],
            "category": src["category"],
            "peer_review_status": src["peer_review_status"],
            "evidence_tier": src["evidence_tier"],
            "citation_and_hygiene_rules": src["citation_and_hygiene_rules"],
        }
