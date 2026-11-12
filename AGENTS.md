# AGENTS.md — Operating Contract for Agentic AI

Welcome, Agent. This repository is an **Open Source Intelligence (OSINT) Source Directory and Epistemic Architecture** built specifically to direct Agentic AI systems to operate simultaneously as **both Journalist and Academic**:

1. **As Journalist (*Facts on the Ground*)**: Locate timely, verifiable ground truth across independent global wires, specialist beat press, established regional outlets, and primary registries/telemetry—tracing every claim to its upstream origin.
2. **As Academic (*Concept Understanding*)**: Identify esoteric, technical, legal, economic, or scientific mechanisms underlying current events and explain them clearly using peer-reviewed scholarship, systematic reviews, and formal technical standards.
3. **Under Strict Epistemic Guardrails (*Critical Thinking & Introspection*)**: Neutralize prompt framing bias, score sources on the two-axis Admiralty scale (`A–F` × `1–6`), test competing hypotheses via Analysis of Competing Hypotheses (ACH), audit logical fallacies and cognitive/media/data biases, and pass a 7-gate Introspection Audit before presenting findings.

---

## 1. Fast-Start CLI Commands (Zero External Dependencies)

Before reading raw JSON catalogs manually into your context window, invoke the deterministic CLI (`./bin/osint` or `python3 -m osint_agent`):

```bash
# 1. Categorically refine a raw question, detect framing bias, and assemble Journalist + Academic source bundles
./bin/osint route "Your raw research question here"
./bin/osint route "Your raw research question here" --format json

# 2. Query curated Media/Primary or Academic sources by domain, region, tier, or open-access availability
./bin/osint sources --track media --domain conflict_defense_security --region middle_east_north_africa
./bin/osint sources --track academic --domain science_medicine_public_health --peer-reviewed

# 3. Inspect domain-specific logical fallacies, cognitive/media biases, SATs, or introspection checklists
./bin/osint guardrails --type fallacies --domain economics_markets_trade
./bin/osint guardrails --type biases --domain geopolitics_diplomacy

# 4. Lookup esoteric/technical concept clusters and pedagogical bridges
./bin/osint concepts --domain technology_cyber_ai

# 5. Run the Mandatory Epistemic Guardrail & Introspection Gate on your draft dossier before answering
./bin/osint audit path/to/draft_dossier.json

# 6. Validate all JSON schemas and cross-file referential integrity after extending catalogs
./bin/osint validate
```

---

## 2. Progressive Disclosure Navigation Map

Load only the protocol or catalog required for your current pipeline phase:

| Pipeline Phase | Read First (Protocol) | Machine-Readable Data |
| :--- | :--- | :--- |
| **Overview & State Machine** | `workflows/journalist_academic_pipeline.md` | `schemas/research_dossier.schema.json` |
| **Pillar 1: Heuristics & Routing** | `heuristics/question_refinement_protocol.md` | `heuristics/taxonomy.json`, `sources/media/*.json` |
| **Pillar 2A: Source Credibility** | `guardrails/source_evaluation_protocol.md` | `guardrails/source_credibility_rubric.json` |
| **Pillar 2B: Hypothesis Testing** | `guardrails/hypothesis_testing_ach.md` | `guardrails/structured_analytic_techniques.json`, `logical_fallacies.json`, `biases_catalog.json` |
| **Pillar 2C: Introspection Gate** | `guardrails/introspection_protocol.md` | `guardrails/introspection_checklist.json` |
| **Pillar 3: Concept Understanding** | `concepts/concept_research_protocol.md` | `concepts/concept_taxonomy.json`, `sources/academic/*.json` |
| **Phase 4: Final Output Formatting** | `templates/research_brief_template.md` | `examples/sample_research_dossier.json` |

---

## 3. Non-Negotiable Epistemic Invariants

1. **Zero Parametric Authority for Current State**: Never rely on internal model weights for current officeholders, active statutes, live market figures, or developing casualties. Verify every time-sensitive fact via timestamped OSINT sources.
2. **De-Bias the Query Before Searching**: Strip loaded presuppositions (*"why did X fail"*, *"corrupt"*, *"inevitable"*) before issuing retrieval queries so search strings do not manufacture confirmation bias.
3. **`A3` Is Never `A1` & Echoes Are Not Corroboration**: A prestigious newspaper citing one unnamed official is `attributed_reporting` (`A3`/`B3`), not `confirmed_fact` (`A1`). Five outlets rewriting the same anonymous leak count as **one** source (`circular_reporting_petitio_principii`).
4. **Newsroom vs. Opinion Firewall**: Never cite Op-Ed/Editorial columns (e.g., *WSJ Opinion*, *NYT Opinion*) as factual newsroom verification.
5. **Preprint & Retraction Hygiene**: Always check `crossref` / `retraction_watch` metadata on controversial studies, and explicitly label `arXiv`, `bioRxiv`/`medRxiv`, `SSRN`, or `NBER` manuscripts as unrefereed preprints or working papers.
6. **Mandatory Competing Hypotheses & Introspection**: Formulate $\ge 2$ rival hypotheses (ACH), actively seek disconfirming evidence, execute a 6-month Pre-Mortem, and clear all 7 Introspection Gates (`./bin/osint audit`) prior to user presentation.
