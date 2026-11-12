"""Epistemic guardrail and introspection gate evaluator for Agentic AI research dossiers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .loader import DirectoryRepository
from .router import HeuristicRouter
from .validator import validate_against_schema


@dataclass
class AuditFinding:
    """Single finding emitted by the epistemic auditor."""

    severity: str  # "FAIL" | "WARN"
    code: str
    message: str
    remediation: str

    def to_dict(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "code": self.code,
            "message": self.message,
            "remediation": self.remediation,
        }


@dataclass
class AuditResult:
    """Aggregate report produced by auditing a research dossier against repository guardrails."""

    dossier_id: str
    status: str  # "PASS" | "WARN" | "FAIL"
    epistemic_score: int
    passed_checks: list[str] = field(default_factory=list)
    findings: list[AuditFinding] = field(default_factory=list)

    @property
    def passed_gate(self) -> bool:
        return self.status in ("PASS", "WARN")

    def to_dict(self) -> dict[str, Any]:
        return {
            "dossier_id": self.dossier_id,
            "status": self.status,
            "passed_gate": self.passed_gate,
            "epistemic_score": self.epistemic_score,
            "passed_checks": self.passed_checks,
            "fail_count": sum(1 for f in self.findings if f.severity == "FAIL"),
            "warn_count": sum(1 for f in self.findings if f.severity == "WARN"),
            "findings": [f.to_dict() for f in self.findings],
        }


class EpistemicAuditor:
    """Enforces source credibility, ACH, fallacy/bias tracking, preprint hygiene, and introspection."""

    def __init__(self, repo: DirectoryRepository | None = None) -> None:
        self.repo = repo or DirectoryRepository()
        self.router = HeuristicRouter(self.repo)
        self.dossier_schema = self.repo.load_schema("research_dossier.schema.json")

    def audit_dossier(self, dossier: dict[str, Any]) -> AuditResult:
        dossier_id = str(dossier.get("dossier_id", "unknown_dossier"))
        findings: list[AuditFinding] = []
        passed: list[str] = []

        # 0. Structural Schema Check
        schema_errors = validate_against_schema(dossier, self.dossier_schema, path="dossier")
        if schema_errors:
            for err in schema_errors:
                findings.append(
                    AuditFinding(
                        severity="FAIL",
                        code="dossier_schema_violation",
                        message=err,
                        remediation="Conform the dossier JSON strictly to schemas/research_dossier.schema.json.",
                    )
                )
            return AuditResult(
                dossier_id=dossier_id,
                status="FAIL",
                epistemic_score=0,
                passed_checks=[],
                findings=findings,
            )
        passed.append("dossier_schema_valid")

        # 1. Prompt Framing & Anti-Sycophancy Check
        intake = dossier["query_intake"]
        framing_alerts, suggested_neutral = self.router.detect_framing_bias(intake["raw_question"])
        if framing_alerts and (
            intake["neutralized_question"].strip().lower()
            == intake["raw_question"].strip().lower()
        ):
            findings.append(
                AuditFinding(
                    severity="FAIL",
                    code="unneutralized_loaded_prompt",
                    message=(
                        "Raw question triggered framing-bias markers "
                        f"({[a['pattern_id'] for a in framing_alerts]}), "
                        "but `neutralized_question` was left identical to `raw_question`."
                    ),
                    remediation=f"Rewrite `neutralized_question` neutrally, e.g.: '{suggested_neutral}'",
                )
            )
        else:
            passed.append("prompt_framing_neutralized")

        # 2. Journalist Track: Admiralty Credibility & Anti-Citogenesis Check
        ledger = dossier["journalist_track"]["evidence_ledger"]
        valid_confirmed_facts = 0
        corroboration_failed = False

        for claim in ledger:
            cid = claim["claim_id"]
            status = claim["claim_status"]
            citations = claim["citations"]

            if status == "confirmed_fact":
                independent_high_grade_provenance: set[str] = set()
                has_primary_registry_a1 = False

                for cit in citations:
                    rel = cit["admiralty_reliability"]
                    cred = cit["admiralty_credibility"]
                    state_aff = bool(cit.get("state_affiliated_media", False))
                    prov = cit["upstream_provenance"].strip().lower()
                    sid = cit["source_id"]

                    if rel in ("A", "B") and cred in ("1", "2") and not state_aff:
                        independent_high_grade_provenance.add(prov)
                        known_media = self.repo.media_sources_by_id.get(sid)
                        if (
                            known_media
                            and known_media["tier"] == "primary_official_and_sensor"
                            and rel == "A"
                            and cred == "1"
                        ):
                            has_primary_registry_a1 = True

                if len(independent_high_grade_provenance) >= 2 or has_primary_registry_a1:
                    valid_confirmed_facts += 1
                else:
                    corroboration_failed = True
                    findings.append(
                        AuditFinding(
                            severity="FAIL",
                            code="uncorroborated_or_echo_confirmed_fact",
                            message=(
                                f"Claim '{cid}' is marked `confirmed_fact` with only "
                                f"{len(independent_high_grade_provenance)} independent A/B+1/2 upstream provenance root(s). "
                                "Multiple outlets repeating one upstream leak or D/E source cannot establish confirmed_fact."
                            ),
                            remediation=(
                                f"Either corroborate '{cid}' via an independent Tier-1/primary source with distinct "
                                "`upstream_provenance`, or downgrade `claim_status` to `attributed_reporting` / `contested_claim`."
                            ),
                        )
                    )

        if not corroboration_failed:
            passed.append("source_credibility_and_anti_citogenesis_verified")

        # 3. Academic Track: Concept Buttressing & Preprint Hygiene
        concepts = dossier["academic_track"]["concepts_explained"]
        concept_narrative_lower = dossier["final_synthesis"][
            "conceptual_background_narrative"
        ].lower()

        if not concepts:
            findings.append(
                AuditFinding(
                    severity="FAIL",
                    code="missing_academic_concept_buttressing",
                    message="`academic_track.concepts_explained` is empty; the Academic half of the dual persona was skipped.",
                    remediation="Identify at least one underlying technical, legal, economic, or scientific concept and ground it via sources/academic/.",
                )
            )
        else:
            preprint_ok = True
            for concept in concepts:
                cname = concept["concept_name"]
                consensus = concept["scholarly_consensus_status"]
                ac_cits = concept["academic_citations"]

                all_unrefereed = all(
                    (not c["peer_reviewed"]) or c["evidence_tier"] == "unrefereed_preprint"
                    for c in ac_cits
                )
                if consensus == "settled_consensus" and all_unrefereed:
                    preprint_ok = False
                    findings.append(
                        AuditFinding(
                            severity="FAIL",
                            code="preprint_cited_as_settled_consensus",
                            message=(
                                f"Concept '{cname}' claims `settled_consensus` while citing exclusively "
                                "non-peer-reviewed preprints or working papers."
                            ),
                            remediation=(
                                "Add peer-reviewed systematic reviews/standards (OpenAlex, Cochrane, IPCC, NIST, SEP), "
                                "or change `scholarly_consensus_status` to `emerging_frontier` / `active_scholarly_debate`."
                            ),
                        )
                    )

                for ac in ac_cits:
                    if ac["evidence_tier"] == "unrefereed_preprint":
                        has_caveat = bool(ac.get("caveats", "").strip()) or any(
                            token in concept_narrative_lower
                            for token in ("preprint", "unrefereed", "not peer-reviewed", "non-peer-reviewed")
                        )
                        if not has_caveat:
                            preprint_ok = False
                            findings.append(
                                AuditFinding(
                                    severity="FAIL",
                                    code="unflagged_preprint_risk",
                                    message=(
                                        f"Concept '{cname}' cites unrefereed preprint '{ac['work_title']}' "
                                        "without explicit preprint caveats."
                                    ),
                                    remediation="Add a `caveats` disclosure on the citation and explicitly label it as a non-peer-reviewed preprint in prose.",
                                )
                            )
            if preprint_ok:
                passed.append("academic_concepts_and_preprint_hygiene_verified")

        # 4. Critical Thinking: Analysis of Competing Hypotheses (ACH)
        eval_block = dossier["guardrail_evaluation"]
        hypotheses = eval_block["competing_hypotheses"]
        if len(hypotheses) < 2:
            findings.append(
                AuditFinding(
                    severity="FAIL",
                    code="single_hypothesis_tunnel_vision",
                    message=f"Only {len(hypotheses)} hypothesis evaluated in `competing_hypotheses`; ACH requires >= 2 rival hypotheses.",
                    remediation="Formulate at least one steel-manned rival or null/friction hypothesis and test evidence diagnosticity across both.",
                )
            )
        else:
            total_disconfirming = sum(
                len(h["disconfirming_evidence_ids"]) for h in hypotheses
            )
            if total_disconfirming == 0:
                findings.append(
                    AuditFinding(
                        severity="WARN",
                        code="missing_disconfirming_evidence",
                        message="Multiple hypotheses listed, but zero `disconfirming_evidence_ids` recorded across the ACH matrix.",
                        remediation="Execute symmetric falsification searches and record anomalies that disconfirm or qualify rival hypotheses.",
                    )
                )
            else:
                passed.append("ach_competing_hypotheses_tested")

        # 5. Logical Fallacies & Biases Stock-Taking
        fallacies_checked = eval_block["fallacies_checked"]
        biases_checked = eval_block["biases_checked"]
        if not fallacies_checked or not biases_checked:
            findings.append(
                AuditFinding(
                    severity="FAIL",
                    code="missing_fallacy_or_bias_audit",
                    message=(
                        f"Dossier logged {len(fallacies_checked)} fallacies and {len(biases_checked)} biases; "
                        "both must be actively audited before presentation."
                    ),
                    remediation="Cross-scan reasoning against guardrails/logical_fallacies.json and guardrails/biases_catalog.json.",
                )
            )
        else:
            passed.append("fallacies_and_biases_audited")
            for fc in fallacies_checked:
                if fc["fallacy_id"] not in self.repo.fallacies_by_id:
                    findings.append(
                        AuditFinding(
                            severity="WARN",
                            code="unregistered_fallacy_id",
                            message=f"Fallacy ID '{fc['fallacy_id']}' is not in guardrails/logical_fallacies.json.",
                            remediation="Use a canonical fallacy ID from `python3 -m osint_agent guardrails --type fallacies`.",
                        )
                    )
            for bc in biases_checked:
                if bc["bias_id"] not in self.repo.biases_by_id:
                    findings.append(
                        AuditFinding(
                            severity="WARN",
                            code="unregistered_bias_id",
                            message=f"Bias ID '{bc['bias_id']}' is not in guardrails/biases_catalog.json.",
                            remediation="Use a canonical bias ID from `python3 -m osint_agent guardrails --type biases`.",
                        )
                    )

        # 6. Mandatory 7-Gate Introspection & Pre-Mortem Check
        intro = dossier["introspection_audit"]
        gates = intro["gates"]
        failed_gates = [g_name for g_name, g_val in gates.items() if not g_val]
        if failed_gates:
            for fg in failed_gates:
                findings.append(
                    AuditFinding(
                        severity="FAIL",
                        code=f"introspection_gate_failed:{fg}",
                        message=f"Mandatory introspection gate '{fg}' is marked false.",
                        remediation="Complete the underlying verification step in guardrails/introspection_protocol.md before unlocking synthesis.",
                    )
                )
        else:
            passed.append("seven_introspection_gates_completed")

        if len(intro["pre_mortem_failure_mode"].strip()) < 45:
            findings.append(
                AuditFinding(
                    severity="WARN",
                    code="shallow_pre_mortem",
                    message="`pre_mortem_failure_mode` is overly brief (< 45 chars) and lacks concrete failure analysis.",
                    remediation="Articulate a specific structural, measurement, or deception failure mode that could invalidate the assessment in 6 months.",
                )
            )
        else:
            passed.append("substantive_pre_mortem_recorded")

        # 7. Confidence Calibration & Rhetorical Overconfidence Scan
        synth = dossier["final_synthesis"]
        combined_prose = " ".join(
            [
                synth["executive_summary"],
                synth["facts_on_the_ground_narrative"],
                synth["conceptual_background_narrative"],
            ]
        ).lower()

        red_flags = self.repo.introspection_checklist.get("overconfidence_red_flag_phrases", [])
        triggered_phrases = [p for p in red_flags if p.lower() in combined_prose]
        if triggered_phrases:
            findings.append(
                AuditFinding(
                    severity="FAIL",
                    code="rhetorical_overconfidence_detected",
                    message=f"Final synthesis prose contains uncalibrated absolutist phrases: {triggered_phrases}",
                    remediation="Replace absolutist rhetoric with calibrated ICD-203 epistemic phrasing tied to specific evidence ratings.",
                )
            )
        else:
            passed.append("calibrated_prose_verified")

        conf = intro["overall_confidence"]
        if conf in ("almost_certain", "highly_likely") and valid_confirmed_facts == 0:
            findings.append(
                AuditFinding(
                    severity="FAIL",
                    code="uncalibrated_high_confidence",
                    message=(
                        f"Overall confidence is set to '{conf}', but zero `confirmed_fact` entries "
                        "passed independent A/B corroboration."
                    ),
                    remediation="Downgrade `overall_confidence` to `likely`, `roughly_even_chance`, or `insufficient_evidence`.",
                )
            )

        # Compute overall status and 0-100 epistemic readiness score
        fail_count = sum(1 for f in findings if f.severity == "FAIL")
        warn_count = sum(1 for f in findings if f.severity == "WARN")
        raw_score = 100 - (fail_count * 18) - (warn_count * 6)
        score = max(0, min(100, raw_score))

        if fail_count > 0:
            overall_status = "FAIL"
        elif warn_count > 0:
            overall_status = "WARN"
        else:
            overall_status = "PASS"

        return AuditResult(
            dossier_id=dossier_id,
            status=overall_status,
            epistemic_score=score,
            passed_checks=passed,
            findings=findings,
        )
