# Unified Operational Workflow: The Journalist-Academic Agentic Pipeline

This workflow defines the mandatory execution state machine for any Agentic AI operating within this repository. Its objective is to unite two distinct epistemic modes into one coherent synthesis:

- **The Journalist**: Rapid, ground-truth empirical verification of *what is happening right now*, anchored in multi-wire corroboration, specialist beat reporting, regional voices, and primary registries.
- **The Academic**: Deliberate, structured theoretical and empirical research explaining *how the underlying technical, legal, economic, or scientific concepts work*, anchored in peer-reviewed scholarship and formal standards.

```text
[Raw User Question]
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│ PHASE 0 & 1: HEURISTIC INTAKE & CATEGORICAL ROUTING      │
│  • Strip framing bias & sycophantic presuppositions      │
│  • Classify Domain + Region + Temporal Horizon           │
│  • Decompose into Journalist vs. Academic Sub-Questions  │
│  (`python3 -m osint_agent route "<question>"`)           │
└───────────────┬──────────────────────────┬───────────────┘
                │                          │
                ▼                          ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐
│ PHASE 2A: JOURNALIST TRACK   │ │ PHASE 2B: ACADEMIC TRACK     │
│  • Tier-1 Wires + Specialist │ │  • Extract esoteric/tech     │
│    + Regional + Primary Data │ │    concepts needing clarity  │
│  • Score Admiralty (A-F/1-6) │ │  • Query OpenAlex / PubMed / │
│  • Trace upstream provenance │ │    SEP / NIST / BIS / NBER   │
│    to block citogenesis      │ │  • Flag preprints/retractions│
└───────────────┬──────────────┘ └──────────────┬───────────────┘
                └──────────────┬────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────┐
│ PHASE 3: GUARDRAILS, ACH & INTROSPECTION GATE            │
│  • Formulate >= 2-4 Competing Hypotheses (ACH)           │
│  • Run Symmetric Falsification Search (disconfirm H1)    │
│  • Audit Logical Fallacies & Analyst/Media/Data Biases   │
│  • Execute 7-Gate Introspection + Pre-Mortem             │
│  (`python3 -m osint_agent audit <dossier.json>`)         │
└───────────────┬──────────────────────────┬───────────────┘
                │ FAIL / WARN              │ PASS
                └──────► Loop to Phase 2   ▼
                               ┌───────────────────────────┐
                               │ PHASE 4: PRESENTATION     │
                               │  • Executive Summary      │
                               │  • Facts on the Ground    │
                               │  • Concept Deep-Dive      │
                               │  • Competing Views &      │
                               │    Epistemic Box          │
                               └───────────────────────────┘
```

---

## Phase-by-Phase Execution Contract

### Phase 0 & 1: Heuristic Intake & Categorical Refinement
1. Run `python3 -m osint_agent route "<raw_question>"` (or apply `heuristics/question_refinement_protocol.md`).
2. If framing markers trigger, rewrite the query into `neutralized_question` before running any external retrieval.
3. Populate at least two `journalist_subquestions` (who/what/where/when/primary record) and at least one `academic_subquestions` (mechanism/theory/standard).

### Phase 2A: Journalist Track (Facts on the Ground)
1. Retrieve coverage across **at least three distinct source tiers** where available:
   - Global Wire / Newspaper of Record (`sources/media/wire_services_and_global_record.json`)
   - Specialist Beat OR Forensic Verification (`specialist_and_sector_press.json` / `investigative_and_verification.json`)
   - Regional Established Press (`regional_established.json`)
   - Primary Official / Sensor Registry (`primary_and_institutional_osint.json`)
2. Log every claim in `journalist_track.evidence_ledger` with:
   - `claim_status`: `confirmed_fact`, `attributed_reporting`, `contested_claim`, or `unverified_signal`
   - Explicit Admiralty code (`A1`–`F6`) and `upstream_provenance` string to verify independence.

### Phase 2B: Academic Track (Concept Understanding)
1. Identify esoteric, technical, statutory, statistical, or physical concepts encountered in Phase 2A.
2. Retrieve authoritative explanations from `sources/academic/` following the 5-rung evidence hierarchy (`concepts/concept_research_protocol.md`).
3. Verify bibliographic accuracy and non-retraction (`crossref` / `retraction_watch`), and explicitly flag `peer_reviewed: false` for preprints or working papers.
4. Structure each explanation using the **Four-Part Pedagogical Bridge**: Definition $\rightarrow$ Mechanism $\rightarrow$ Relevance to Today's Event $\rightarrow$ Scholarly Consensus Status.

### Phase 3: Guardrails, ACH & Mandatory Introspection Gate
1. Populate `guardrail_evaluation.competing_hypotheses` with $\ge 2$ distinct hypotheses (including rival structural or null/friction explanations) and record disconfirming evidence.
2. Surface `key_assumptions` and scan reasoning against `guardrails/logical_fallacies.json` and `guardrails/biases_catalog.json`.
3. Complete all seven boolean gates in `introspection_audit.gates`, write a concrete `pre_mortem_failure_mode`, and calibrate `overall_confidence`.
4. Run `python3 -m osint_agent audit <dossier.json>`. **Do not present findings as settled if the audit returns `FAIL`.** Resolve flagged single-source claims, circular provenance, unflagged preprints, or overconfident language first.

### Phase 4: User-Facing Synthesis
Render the final response following `templates/research_brief_template.md` so the human reader receives both crisp, well-attributed journalism and clear, illuminating academic context.
