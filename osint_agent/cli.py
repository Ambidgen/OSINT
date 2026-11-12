"""Command-line interface enabling Agentic AI systems to query and operate the OSINT directory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .auditor import EpistemicAuditor
from .loader import DirectoryRepository
from .router import HeuristicRouter
from .validator import validate_repository


def _emit_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _cmd_validate(args: argparse.Namespace) -> int:
    report = validate_repository(args.repo_root)
    if args.format == "json":
        _emit_json(report.to_dict())
    else:
        status_str = "VALID" if report.is_valid else "INVALID"
        print(f"# OSINT Directory Validation Report: {status_str}")
        print(f"- **Files Checked**: {report.files_checked}")
        for k, v in report.stats.items():
            print(f"- **{k}**: {v}")
        if report.warnings:
            print("\n## Warnings")
            for w in report.warnings:
                print(f"- [WARN] {w}")
        if report.errors:
            print("\n## Errors")
            for e in report.errors:
                print(f"- [ERROR] {e}")
    return 0 if report.is_valid else 1


def _cmd_route(args: argparse.Namespace) -> int:
    repo = DirectoryRepository(args.repo_root)
    router = HeuristicRouter(repo)
    plan = router.route(
        args.question,
        region_override=args.region,
        horizon_override=args.horizon,
    )
    if args.format == "json":
        _emit_json(plan.to_dict())
        return 0

    data = plan.to_dict()
    print("# OSINT Dual-Track Heuristic Routing Plan\n")
    print(f"- **Raw Question**: {data['raw_question']}")
    if data["framing_alerts"]:
        print(f"- **Neutralized Framing**: {data['suggested_neutral_framing']}")
        print("\n## Framing & Anti-Sycophancy Alerts")
        for alert in data["framing_alerts"]:
            print(
                f"- **{alert['pattern_id']}** (matched: `{', '.join(alert['matched_terms'])}`): "
                f"{alert['remediation_guidance']}"
            )
    cls = data["classification"]
    print("\n## Categorical Classification")
    print(f"- **Primary Domain**: `{cls['primary_domain']['id']}` — {cls['primary_domain']['label']}")
    if cls["secondary_domains"]:
        sec = ", ".join(f"`{d['id']}`" for d in cls["secondary_domains"])
        print(f"- **Secondary Domains**: {sec}")
    print(f"- **Geographic Scope**: `{cls['geographic_scope']['id']}` ({cls['geographic_scope']['label']})")
    print(f"- **Temporal Horizon**: `{cls['temporal_horizon']['id']}` ({cls['temporal_horizon']['label']})")
    print(f"  - *Primary Risk*: {cls['temporal_horizon']['primary_risk']}")

    print("\n## Track A — Journalist Sub-Questions & Credible Media Bundle")
    for q in data["refinement_questions"]["journalist_track"]:
        print(f"- {q}")

    jb = data["recommended_sources"]["journalist_track"]
    for group_key, group_label in [
        ("global_wires_and_record", "Tier-1 Global Wires & Record"),
        ("specialist_and_verification", "Specialist Beat & Forensic Verification"),
        ("regional_record_counterweights", "Regional Record Counterweights"),
        ("primary_official_and_telemetry", "Primary Official & Telemetry Registries"),
    ]:
        items = jb.get(group_key, [])
        if items:
            print(f"\n### {group_label}")
            for s in items:
                print(
                    f"- **{s['name']}** (`{s['id']}`, baseline `{s['baseline_admiralty_reliability']}`, "
                    f"`{s['access_model']}`) — {s['url']}\n  *Pairing rule*: {s['corroboration_pairing_rule']}"
                )

    print("\n## Track B — Academic Concept Buttressing")
    for q in data["refinement_questions"]["academic_track"]:
        print(f"- {q}")
    for cluster in data["matched_concept_clusters"]:
        print(f"\n### Concept Cluster: {cluster['title']} (`{cluster['id']}`)")
        print(f"- **Disciplines**: {', '.join(cluster['academic_disciplines'])}")
        print(f"- **Pedagogical Bridge**: {cluster['pedagogical_bridge_prompt']}")
    print("\n### Recommended Academic & Reference Sources")
    for s in data["recommended_sources"]["academic_track"]:
        print(
            f"- **{s['name']}** (`{s['id']}`, `{s['evidence_tier']}`, `{s['peer_review_status']}`) — {s['url']}\n"
            f"  *Hygiene*: {s['citation_and_hygiene_rules']}"
        )

    print("\n## Domain Guardrail Watch List")
    for f in data["guardrail_watch_list"]["fallacies_to_monitor"]:
        print(f"- **Fallacy — {f['name']}** (`{f['id']}`): {f['remediation_protocol']}")
    for b in data["guardrail_watch_list"]["biases_to_monitor"]:
        print(f"- **Bias — {b['name']}** (`{b['id']}`, `{b['category']}`): {b['remediation_protocol']}")
    return 0


def _cmd_sources(args: argparse.Namespace) -> int:
    repo = DirectoryRepository(args.repo_root)
    payload: dict[str, Any] = {}
    if args.track in ("all", "media"):
        payload["media_sources"] = repo.query_media_sources(
            domain=args.domain,
            region=args.region,
            tier=args.tier,
            open_access_only=args.open_access,
            search=args.search,
        )
    if args.track in ("all", "academic"):
        payload["academic_sources"] = repo.query_academic_sources(
            domain=args.domain,
            category=args.category,
            peer_reviewed_only=args.peer_reviewed,
            open_access_only=args.open_access,
            search=args.search,
        )

    if args.format == "json":
        _emit_json(payload)
        return 0

    if "media_sources" in payload:
        ms = payload["media_sources"]
        print(f"# Media & Primary OSINT Sources ({len(ms)} matched)\n")
        for s in ms:
            print(
                f"- **{s['name']}** (`{s['id']}`) | Tier: `{s['tier']}` | "
                f"Baseline: `{s['baseline_admiralty_reliability']}` | Access: `{s['access_model']}` | {s['url']}"
            )
    if "academic_sources" in payload:
        acs = payload["academic_sources"]
        print(f"\n# Academic & Concept Research Sources ({len(acs)} matched)\n")
        for s in acs:
            print(
                f"- **{s['name']}** (`{s['id']}`) | Tier: `{s['evidence_tier']}` | "
                f"Review: `{s['peer_review_status']}` | Access: `{s['access_model']}` | {s['url']}"
            )
    return 0


def _cmd_guardrails(args: argparse.Namespace) -> int:
    repo = DirectoryRepository(args.repo_root)
    payload = repo.query_guardrails(
        guardrail_type=args.type,
        domain=args.domain,
        search=args.search,
    )
    if args.format == "json":
        _emit_json(payload)
        return 0

    print("# OSINT Epistemic Guardrails\n")
    for section_key in ("logical_fallacies", "cognitive_and_media_biases", "structured_analytic_techniques"):
        if section_key in payload:
            entries = payload[section_key]
            print(f"## {section_key} ({len(entries)} entries)")
            for e in entries:
                print(f"- **{e['name']}** (`{e['id']}`, `{e['category']}`): {e['definition']}")
                print(f"  - *Remediation*: {e['remediation_protocol']}")
            print()
    if "source_credibility_rubric" in payload:
        rubric = payload["source_credibility_rubric"]
        print(f"## {rubric['title']}")
        print(f"- {rubric['core_principle']}\n")
    if "introspection_checklist" in payload:
        chk = payload["introspection_checklist"]
        print(f"## {chk['title']}")
        for g in chk["gates"]:
            print(f"- **`{g['gate_id']}`**: {g['question']}")
    return 0


def _cmd_concepts(args: argparse.Namespace) -> int:
    repo = DirectoryRepository(args.repo_root)
    clusters = repo.query_concepts(domain=args.domain, search=args.search)
    if args.format == "json":
        _emit_json({"concept_clusters": clusters})
        return 0

    print(f"# Academic Concept Clusters ({len(clusters)} matched)\n")
    for c in clusters:
        print(f"## {c['title']} (`{c['id']}` — `{c['domain']}`)")
        print(f"- **Disciplines**: {', '.join(c['academic_disciplines'])}")
        print(f"- **Recommended Academic Sources**: `{', '.join(c['recommended_academic_sources'])}`")
        print("- **Foundational Mechanisms**:")
        for m in c["foundational_mechanisms"]:
            print(f"  - {m}")
        print("- **Common Media Misconceptions**:")
        for mc in c["common_media_misconceptions"]:
            print(f"  - {mc}")
        print(f"- **Pedagogical Bridge**: {c['pedagogical_bridge_prompt']}\n")
    return 0


def _cmd_audit(args: argparse.Namespace) -> int:
    repo = DirectoryRepository(args.repo_root)
    auditor = EpistemicAuditor(repo)
    dossier_path = Path(args.dossier_file)
    with dossier_path.open("r", encoding="utf-8") as fh:
        dossier = json.load(fh)

    result = auditor.audit_dossier(dossier)
    if args.format == "json":
        _emit_json(result.to_dict())
    else:
        print(f"# Epistemic Guardrail & Introspection Audit: {result.status}")
        print(f"- **Dossier ID**: `{result.dossier_id}`")
        print(f"- **Epistemic Readiness Score**: {result.epistemic_score}/100")
        print(f"- **Gate Cleared**: `{result.passed_gate}`")
        if result.passed_checks:
            print("\n## Passed Checks")
            for chk in result.passed_checks:
                print(f"- [PASS] `{chk}`")
        if result.findings:
            print("\n## Guardrail Findings & Required Remediation")
            for f in result.findings:
                print(f"- **[{f.severity}] `{f.code}`**: {f.message}")
                print(f"  - *Remediation*: {f.remediation}")
    return 0 if result.passed_gate else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="osint-agent",
        description="Agentic AI OSINT Source Directory, Heuristic Router, Guardrails & Concept Engine",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Optional override path to the OSINT repository root",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_val = sub.add_parser("validate", help="Validate all directory JSON schemas and cross-references")
    p_val.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p_val.set_defaults(func=_cmd_validate)

    p_route = sub.add_parser(
        "route",
        help="Categorically refine a research question and build Journalist + Academic source bundles",
    )
    p_route.add_argument("question", help="Raw user or orchestrator research question")
    p_route.add_argument("--region", default=None, help="Optional geographic scope override")
    p_route.add_argument("--horizon", default=None, help="Optional temporal horizon override")
    p_route.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p_route.set_defaults(func=_cmd_route)

    p_src = sub.add_parser("sources", help="Query curated media, primary, and academic source catalogs")
    p_src.add_argument("--track", choices=["all", "media", "academic"], default="all")
    p_src.add_argument("--domain", default=None, help="Filter by domain ID")
    p_src.add_argument("--region", default=None, help="Filter media sources by region ID")
    p_src.add_argument("--tier", default=None, help="Filter media sources by tier")
    p_src.add_argument("--category", default=None, help="Filter academic sources by category")
    p_src.add_argument("--peer-reviewed", action="store_true", help="Academic peer-reviewed/standard only")
    p_src.add_argument("--open-access", action="store_true", help="Open-access or open-API sources only")
    p_src.add_argument("--search", default=None, help="Keyword filter")
    p_src.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p_src.set_defaults(func=_cmd_sources)

    p_grd = sub.add_parser("guardrails", help="Query logical fallacies, biases, SATs, and introspection gates")
    p_grd.add_argument(
        "--type",
        choices=["all", "fallacies", "biases", "sats", "credibility", "checklist"],
        default="all",
    )
    p_grd.add_argument("--domain", default=None, help="Filter by high-prevalence domain ID")
    p_grd.add_argument("--search", default=None, help="Keyword filter")
    p_grd.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p_grd.set_defaults(func=_cmd_guardrails)

    p_con = sub.add_parser("concepts", help="Query esoteric/technical concept-to-academic-discipline clusters")
    p_con.add_argument("--domain", default=None, help="Filter by domain ID")
    p_con.add_argument("--search", default=None, help="Keyword filter")
    p_con.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p_con.set_defaults(func=_cmd_concepts)

    p_aud = sub.add_parser(
        "audit",
        help="Run the Epistemic Guardrail & Introspection Gate on a research dossier JSON file",
    )
    p_aud.add_argument("dossier_file", help="Path to draft research dossier JSON")
    p_aud.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p_aud.set_defaults(func=_cmd_audit)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
