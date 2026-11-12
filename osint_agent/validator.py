"""Schema and cross-file referential integrity validator for the OSINT directory."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .loader import DirectoryRepository, get_default_repo_root


@dataclass
class ValidationReport:
    """Structured result of validating schemas and cross-references across the directory."""

    files_checked: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stats: dict[str, int] = field(default_factory=dict)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.is_valid,
            "files_checked": self.files_checked,
            "stats": self.stats,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
        }


def validate_against_schema(
    instance: Any,
    schema: dict[str, Any],
    path: str = "$",
) -> list[str]:
    """Validate a JSON value against a Draft 2020-12 JSON Schema subset using pure stdlib."""
    errors: list[str] = []

    expected_type = schema.get("type")
    if expected_type is not None:
        if not _matches_json_type(instance, expected_type):
            errors.append(
                f"{path}: expected type '{expected_type}', got {type(instance).__name__}"
            )
            return errors

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} not in allowed enum {schema['enum']}")

    if isinstance(instance, str):
        min_len = schema.get("minLength")
        if min_len is not None and len(instance) < min_len:
            errors.append(f"{path}: string length {len(instance)} < minLength {min_len}")
        max_len = schema.get("maxLength")
        if max_len is not None and len(instance) > max_len:
            errors.append(f"{path}: string length {len(instance)} > maxLength {max_len}")
        pattern = schema.get("pattern")
        if pattern is not None and re.search(pattern, instance) is None:
            errors.append(f"{path}: string {instance!r} does not match pattern {pattern!r}")

    elif isinstance(instance, (int, float)) and not isinstance(instance, bool):
        minimum = schema.get("minimum")
        if minimum is not None and instance < minimum:
            errors.append(f"{path}: value {instance} < minimum {minimum}")
        maximum = schema.get("maximum")
        if maximum is not None and instance > maximum:
            errors.append(f"{path}: value {instance} > maximum {maximum}")

    elif isinstance(instance, list):
        min_items = schema.get("minItems")
        if min_items is not None and len(instance) < min_items:
            errors.append(f"{path}: array length {len(instance)} < minItems {min_items}")
        max_items = schema.get("maxItems")
        if max_items is not None and len(instance) > max_items:
            errors.append(f"{path}: array length {len(instance)} > maxItems {max_items}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for idx, item in enumerate(instance):
                errors.extend(validate_against_schema(item, item_schema, f"{path}[{idx}]"))

    elif isinstance(instance, dict):
        required = schema.get("required", [])
        for req_key in required:
            if req_key not in instance:
                errors.append(f"{path}: missing required property '{req_key}'")

        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, value in instance.items():
            prop_path = f"{path}.{key}"
            if key in properties:
                errors.extend(validate_against_schema(value, properties[key], prop_path))
            elif additional is False:
                errors.append(f"{path}: unexpected property '{key}' (additionalProperties=false)")
            elif isinstance(additional, dict):
                errors.extend(validate_against_schema(value, additional, prop_path))

    return errors


def _matches_json_type(value: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return True


def validate_repository(repo_root: Path | str | None = None) -> ValidationReport:
    """Validate all schemas, catalogs, worked examples, and cross-file ID references."""
    root = Path(repo_root).resolve() if repo_root else get_default_repo_root()
    report = ValidationReport()

    def _load_raw(rel_path: Path) -> Any:
        with (root / rel_path).open("r", encoding="utf-8") as fh:
            return json.load(fh)

    def _check_file(rel_path: Path, schema_name: str) -> None:
        report.files_checked += 1
        try:
            data = _load_raw(rel_path)
            schema = _load_raw(Path("schemas") / schema_name)
        except Exception as exc:
            report.errors.append(f"{rel_path}: failed to load JSON ({exc})")
            return
        for err in validate_against_schema(data, schema, path=str(rel_path)):
            report.errors.append(err)

    for path in sorted((root / "sources" / "media").glob("*.json")):
        _check_file(path.relative_to(root), "media_source.schema.json")

    for path in sorted((root / "sources" / "academic").glob("*.json")):
        _check_file(path.relative_to(root), "academic_source.schema.json")

    _check_file(Path("heuristics/taxonomy.json"), "taxonomy.schema.json")
    _check_file(Path("concepts/concept_taxonomy.json"), "concept_taxonomy.schema.json")
    _check_file(Path("guardrails/logical_fallacies.json"), "guardrail_catalog.schema.json")
    _check_file(Path("guardrails/biases_catalog.json"), "guardrail_catalog.schema.json")
    _check_file(
        Path("guardrails/structured_analytic_techniques.json"),
        "guardrail_catalog.schema.json",
    )

    for path in sorted((root / "examples").glob("*.json")):
        _check_file(path.relative_to(root), "research_dossier.schema.json")

    # Cross-file referential integrity checks
    repo = DirectoryRepository(root)

    seen_source_ids: dict[str, str] = {}
    for cat in repo.media_catalogs:
        file_label = cat.get("_file_path", cat["catalog_id"])
        for src in cat["sources"]:
            sid = src["id"]
            if sid in seen_source_ids:
                report.errors.append(
                    f"Duplicate source ID '{sid}' in {file_label} and {seen_source_ids[sid]}"
                )
            seen_source_ids[sid] = file_label

    for cat in repo.academic_catalogs:
        file_label = cat.get("_file_path", cat["catalog_id"])
        for src in cat["sources"]:
            sid = src["id"]
            if sid in seen_source_ids:
                report.errors.append(
                    f"Duplicate source ID '{sid}' across media/academic catalogs ({file_label} vs {seen_source_ids[sid]})"
                )
            seen_source_ids[sid] = file_label

    for domain in repo.taxonomy["domains"]:
        did = domain["id"]
        for m_id in domain["priority_media_sources"]:
            if m_id not in repo.media_sources_by_id:
                report.errors.append(
                    f"heuristics/taxonomy.json domain '{did}' references unknown media source '{m_id}'"
                )
        for p_id in domain["priority_primary_sources"]:
            if p_id not in repo.media_sources_by_id:
                report.errors.append(
                    f"heuristics/taxonomy.json domain '{did}' references unknown primary source '{p_id}'"
                )
            elif repo.media_sources_by_id[p_id]["tier"] != "primary_official_and_sensor":
                report.errors.append(
                    f"heuristics/taxonomy.json domain '{did}' primary source '{p_id}' is not tier 'primary_official_and_sensor'"
                )
        for a_id in domain["priority_academic_sources"]:
            if a_id not in repo.academic_sources_by_id:
                report.errors.append(
                    f"heuristics/taxonomy.json domain '{did}' references unknown academic source '{a_id}'"
                )
        for f_id in domain["high_risk_fallacies"]:
            if f_id not in repo.fallacies_by_id:
                report.errors.append(
                    f"heuristics/taxonomy.json domain '{did}' references unknown fallacy '{f_id}'"
                )
        for b_id in domain["high_risk_biases"]:
            if b_id not in repo.biases_by_id:
                report.errors.append(
                    f"heuristics/taxonomy.json domain '{did}' references unknown bias '{b_id}'"
                )

    seen_cluster_ids: set[str] = set()
    covered_concept_domains: set[str] = set()
    for cluster in repo.concept_taxonomy["concept_clusters"]:
        cid = cluster["id"]
        if cid in seen_cluster_ids:
            report.errors.append(f"Duplicate concept cluster ID '{cid}' in concepts/concept_taxonomy.json")
        seen_cluster_ids.add(cid)
        covered_concept_domains.add(cluster["domain"])
        for a_id in cluster["recommended_academic_sources"]:
            if a_id not in repo.academic_sources_by_id:
                report.errors.append(
                    f"concepts/concept_taxonomy.json cluster '{cid}' references unknown academic source '{a_id}'"
                )

    for did in repo.domains_by_id:
        if did not in covered_concept_domains:
            report.warnings.append(
                f"Domain '{did}' has no dedicated concept cluster in concepts/concept_taxonomy.json"
            )

    report.stats = {
        "media_and_primary_sources": len(repo.media_sources_by_id),
        "academic_and_concept_sources": len(repo.academic_sources_by_id),
        "total_curated_sources": len(repo.media_sources_by_id) + len(repo.academic_sources_by_id),
        "domains": len(repo.domains_by_id),
        "concept_clusters": len(repo.concept_taxonomy["concept_clusters"]),
        "logical_fallacies": len(repo.fallacies_by_id),
        "cognitive_and_media_biases": len(repo.biases_by_id),
        "structured_analytic_techniques": len(repo.sats_by_id),
    }
    return report
