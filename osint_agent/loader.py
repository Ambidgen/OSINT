"""Loader and unified index for OSINT source catalogs, heuristics, concepts, and guardrails."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def get_default_repo_root() -> Path:
    """Resolve the repository root directory relative to this package."""
    return Path(__file__).resolve().parent.parent


class DirectoryRepository:
    """In-memory index over all structured JSON catalogs in the OSINT directory."""

    def __init__(self, repo_root: Path | str | None = None) -> None:
        self.repo_root = Path(repo_root).resolve() if repo_root else get_default_repo_root()
        self.schemas_dir = self.repo_root / "schemas"
        self.sources_media_dir = self.repo_root / "sources" / "media"
        self.sources_academic_dir = self.repo_root / "sources" / "academic"
        self.heuristics_dir = self.repo_root / "heuristics"
        self.guardrails_dir = self.repo_root / "guardrails"
        self.concepts_dir = self.repo_root / "concepts"

        self.media_catalogs: list[dict[str, Any]] = self._load_dir_json(self.sources_media_dir)
        self.academic_catalogs: list[dict[str, Any]] = self._load_dir_json(self.sources_academic_dir)

        self.media_sources_by_id: dict[str, dict[str, Any]] = {}
        for cat in self.media_catalogs:
            for src in cat.get("sources", []):
                enriched = dict(src)
                enriched["catalog_id"] = cat["catalog_id"]
                self.media_sources_by_id[src["id"]] = enriched

        self.academic_sources_by_id: dict[str, dict[str, Any]] = {}
        for cat in self.academic_catalogs:
            for src in cat.get("sources", []):
                enriched = dict(src)
                enriched["catalog_id"] = cat["catalog_id"]
                self.academic_sources_by_id[src["id"]] = enriched

        self.taxonomy: dict[str, Any] = self._load_json(self.heuristics_dir / "taxonomy.json")
        self.concept_taxonomy: dict[str, Any] = self._load_json(self.concepts_dir / "concept_taxonomy.json")

        self.fallacies_catalog: dict[str, Any] = self._load_json(self.guardrails_dir / "logical_fallacies.json")
        self.biases_catalog: dict[str, Any] = self._load_json(self.guardrails_dir / "biases_catalog.json")
        self.sats_catalog: dict[str, Any] = self._load_json(
            self.guardrails_dir / "structured_analytic_techniques.json"
        )
        self.credibility_rubric: dict[str, Any] = self._load_json(
            self.guardrails_dir / "source_credibility_rubric.json"
        )
        self.introspection_checklist: dict[str, Any] = self._load_json(
            self.guardrails_dir / "introspection_checklist.json"
        )

        self.domains_by_id: dict[str, dict[str, Any]] = {
            d["id"]: d for d in self.taxonomy.get("domains", [])
        }
        self.fallacies_by_id: dict[str, dict[str, Any]] = {
            e["id"]: e for e in self.fallacies_catalog.get("entries", [])
        }
        self.biases_by_id: dict[str, dict[str, Any]] = {
            e["id"]: e for e in self.biases_catalog.get("entries", [])
        }
        self.sats_by_id: dict[str, dict[str, Any]] = {
            e["id"]: e for e in self.sats_catalog.get("entries", [])
        }

    @staticmethod
    def _load_json(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError(f"Expected JSON object in {path}")
        return data

    def _load_dir_json(self, directory: Path) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for path in sorted(directory.glob("*.json")):
            obj = self._load_json(path)
            obj["_file_path"] = str(path.relative_to(self.repo_root))
            results.append(obj)
        return results

    def load_schema(self, schema_filename: str) -> dict[str, Any]:
        return self._load_json(self.schemas_dir / schema_filename)

    def query_media_sources(
        self,
        *,
        domain: str | None = None,
        region: str | None = None,
        tier: str | None = None,
        open_access_only: bool = False,
        search: str | None = None,
    ) -> list[dict[str, Any]]:
        """Filter media and primary OSINT sources."""
        results: list[dict[str, Any]] = []
        needle = search.lower().strip() if search else None

        for src in self.media_sources_by_id.values():
            if domain and domain not in src["domains"]:
                continue
            if region and region not in src["regions"] and "global" not in src["regions"]:
                continue
            if tier and src["tier"] != tier:
                continue
            if open_access_only and src["access_model"] not in ("open_access", "open_api_available"):
                continue
            if needle:
                haystack = " ".join(
                    [
                        src["id"],
                        src["name"],
                        src["ownership_and_funding"],
                        src["editorial_standards"],
                        " ".join(src["strengths"]),
                    ]
                ).lower()
                if needle not in haystack:
                    continue
            results.append(src)
        return results

    def query_academic_sources(
        self,
        *,
        domain: str | None = None,
        category: str | None = None,
        peer_reviewed_only: bool = False,
        open_access_only: bool = False,
        search: str | None = None,
    ) -> list[dict[str, Any]]:
        """Filter academic and concept-understanding sources."""
        results: list[dict[str, Any]] = []
        needle = search.lower().strip() if search else None

        for src in self.academic_sources_by_id.values():
            if domain and domain not in src["domains"]:
                continue
            if category and src["category"] != category:
                continue
            if peer_reviewed_only and src["peer_review_status"] not in (
                "peer_reviewed",
                "consensus_standard",
            ):
                continue
            if open_access_only and src["access_model"] not in ("open_access", "open_api_available"):
                continue
            if needle:
                haystack = " ".join(
                    [
                        src["id"],
                        src["name"],
                        " ".join(src["disciplines"]),
                        " ".join(src["concept_use_cases"]),
                    ]
                ).lower()
                if needle not in haystack:
                    continue
            results.append(src)
        return results

    def query_guardrails(
        self,
        *,
        guardrail_type: str = "all",
        domain: str | None = None,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Query fallacies, biases, SATs, credibility rubric, or introspection gates."""
        needle = search.lower().strip() if search else None

        def _filter_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
            matched: list[dict[str, Any]] = []
            for entry in entries:
                if domain and domain not in entry.get("high_prevalence_domains", []):
                    continue
                if needle:
                    haystack = " ".join(
                        [
                            entry["id"],
                            entry["name"],
                            entry["category"],
                            entry["definition"],
                            entry["osint_manifestation"],
                            entry["remediation_protocol"],
                        ]
                    ).lower()
                    if needle not in haystack:
                        continue
                matched.append(entry)
            return matched

        payload: dict[str, Any] = {}
        if guardrail_type in ("all", "fallacies"):
            payload["logical_fallacies"] = _filter_entries(self.fallacies_catalog["entries"])
        if guardrail_type in ("all", "biases"):
            payload["cognitive_and_media_biases"] = _filter_entries(self.biases_catalog["entries"])
        if guardrail_type in ("all", "sats"):
            payload["structured_analytic_techniques"] = _filter_entries(self.sats_catalog["entries"])
        if guardrail_type in ("all", "credibility"):
            payload["source_credibility_rubric"] = self.credibility_rubric
        if guardrail_type in ("all", "checklist"):
            payload["introspection_checklist"] = self.introspection_checklist
        return payload

    def query_concepts(
        self,
        *,
        domain: str | None = None,
        search: str | None = None,
    ) -> list[dict[str, Any]]:
        """Query concept-to-discipline academic clusters."""
        needle = search.lower().strip() if search else None
        clusters: list[dict[str, Any]] = []
        for cluster in self.concept_taxonomy.get("concept_clusters", []):
            if domain and cluster["domain"] != domain:
                continue
            if needle:
                haystack = " ".join(
                    [
                        cluster["id"],
                        cluster["title"],
                        " ".join(cluster["trigger_terms"]),
                        " ".join(cluster["academic_disciplines"]),
                        " ".join(cluster["foundational_mechanisms"]),
                    ]
                ).lower()
                if needle not in haystack:
                    continue
            clusters.append(cluster)
        return clusters
