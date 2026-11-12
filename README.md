# OSINT: Agentic AI Source Directory & Epistemic Architecture

An Open Source Intelligence (OSINT) source directory, heuristic routing engine, and epistemic guardrail architecture designed specifically to be consumed and operated by **Agentic AI**.

The overarching mission of this repository is to direct autonomous and tool-using AI agents to serve simultaneously as **both Journalist and Academic**:

- **As Journalist (*Facts on the Ground*)**: Rapidly triangulating current events across credible global wire services, specialist beat press, independent regional outlets, forensic verification collectives, and primary official/sensor registries.
- **As Academic (*Concept Understanding*)**: Performing deliberate, structured scholarly research to unpack the esoteric, technical, legal, economic, or scientific mechanisms that allow a reader to genuinely understand *why* current events unfold as they do.

---

## Core Architectural Pillars

### 1. Heuristics (`heuristics/` & `sources/media/`)
Transforms raw, underspecified, or emotionally loaded research questions into structured, multi-tier retrieval plans:
- **Prompt Neutralization & Anti-Sycophancy**: Detects presuppositions (*"why did Policy X backfire?"*, *"prove that..."*) and reformulates them into neutral empirical inquiries before search strings are constructed.
- **Categorical Matrix Classification**: Routes queries across **8 primary domains**, **8 global regions**, and **4 temporal horizons** (`breaking_sub_24h` through `historical_settled`).
- **Multi-Tier Credible Media Directory (`47` curated media & primary sources)**:
  - `tier_1_global_wire_and_record`: Reuters, AP, AFP, Financial Times, BBC News, WSJ News, NYT, The Economist, Bloomberg, Nikkei Asia.
  - `tier_2_investigative_and_verification`: Bellingcat, ProPublica, ICIJ, OCCRP, Centre for Information Resilience, PBS FRONTLINE.
  - `tier_2_specialist_beat`: STAT News, Nature News, Ars Technica, KrebsOnSecurity, The Record, Lawfare, SCOTUSblog, Carbon Brief, War on the Rocks, Foreign Affairs.
  - `tier_2_regional_record`: Le Monde, Der Spiegel, El País, The Hindu, The Straits Times, Yonhap, Kyodo News, Al-Monitor, Daily Maverick, The Globe and Mail, Folha de S.Paulo, The Kyiv Independent.
  - `primary_official_and_sensor`: UN OCHA ReliefWeb, ICJ/ICC Court Dockets, SEC EDGAR, IMF/World Bank/FRED, WHO/CDC/ECDC, CISA KEV/NIST NVD, USGS/Copernicus/NOAA, OFAC/EU/UN Sanctions, Open ADS-B & Marine AIS Telemetry.

### 2. Guardrails (`guardrails/`)
Prevents hallucinated consensus, single-source echo chambers, tunnel vision, and rhetorical overconfidence:
- **Two-Axis Admiralty Credibility Rubric (`A–F` × `1–6`)**: Decouples *source reliability* (`A`–`F`) from *claim corroboration* (`1`–`6`), enforcing lateral reading (SIFT) and `upstream_provenance` tracing to block **citogenesis / circular reporting**.
- **Critical Thinking & Hypothesis Stress-Testing**: Operationalizes **Analysis of Competing Hypotheses (ACH)**, **Key Assumptions Check (KAC)**, **Devil's Advocacy / Steel-Manning**, and **Red-Team Deception Checks**.
- **Logical Fallacies & Multi-Layer Biases Stock-Taking**:
  - `14` formal and informal logical fallacies (`post_hoc_ergo_propter_hoc`, `base_rate_neglect`, `motte_and_bailey`, `circular_reporting_petitio_principii`, `ecological_fallacy`, `texas_sharpshooter`, `nirvana_perfect_solution`, etc.) with detection signals and remediation prompts.
  - `14` biases across three distinct layers: **Analyst/AI Biases** (confirmation, sycophancy, anchoring, mirror-imaging, parametric training-cutoff drift), **Media Structural Biases** (anonymous-official access bias, false balance, breaking-news speed bias, home-capital framing), and **Data/Sampling Biases** (conflict-zone digital visibility bias, ascertainment lag, Goodhart's Law).
- **Mandatory 7-Gate Introspection & Pre-Mortem Audit**: Requires every draft dossier to pass seven self-interrogation checks, articulate a concrete 6-month **Pre-Mortem** failure mode, and calibrate confidence using ICD-203 probability bands before user presentation.

### 3. Concept Understanding (`concepts/` & `sources/academic/`)
Equips the AI agent to buttress current-events reporting with rigorous academic explanation:
- **5-Rung Evidence Hierarchy**: Ranks evidence from Systematic Reviews/Meta-Analyses (`cochrane_library`, `ipcc_assessments`) $\rightarrow$ Peer-Reviewed Literature (`openalex`, `semantic_scholar`, `pubmed_pmc`, `doaj_core`, `philpapers`) $\rightarrow$ Technical/Legal Standards & Living Reference (`nist_ietf_ieee`, `stanford_encyclopedia`, `our_world_in_data`, `worldlii_heinonline`, `sipri_iiss`) $\rightarrow$ Institutional Working Papers (`nber`, `repec_ideas`, `bis_central_bank_research`, `cfr_chatham_carnegie`) $\rightarrow$ Unrefereed Preprints (`arxiv`, `biorxiv_medrxiv`, `ssrn`) plus mandatory retraction screening (`crossref` / `retraction_watch`).
- **Concept-to-Discipline Taxonomy**: Maps `11` esoteric current-events concept clusters (e.g., *EUV lithography & Rayleigh optics*, *FX swap/repo monetary plumbing*, *ICJ provisional-measures law & UNCLOS straits*, *CFR vs. IFR outbreak epidemiology*, *AC grid synchronous inertia*) to exact academic disciplines, foundational mechanisms, and common media misconceptions.
- **Four-Part Pedagogical Bridge**: *Plain-Language Definition* $\rightarrow$ *Underlying Mechanism* $\rightarrow$ *Relevance to Today's Event* $\rightarrow$ *Scholarly Consensus & Caveats*.

---

## Repository Structure

```text
OSINT/
├── AGENTS.md                         # Entry-point operating manual & progressive-disclosure map for Agentic AI
├── README.md                         # Architectural documentation, quickstart & extension guide
├── pyproject.toml                    # Zero-dependency Python package configuration
├── bin/
│   └── osint                         # Executable CLI entrypoint for shell-equipped AI agents
├── schemas/                          # Draft 2020-12 JSON Schemas enforcing strict catalog & dossier contracts
│   ├── media_source.schema.json
│   ├── academic_source.schema.json
│   ├── taxonomy.schema.json
│   ├── guardrail_catalog.schema.json
│   ├── concept_taxonomy.schema.json
│   └── research_dossier.schema.json
├── heuristics/                       # Pillar 1: Question de-biasing, decomposition & categorical routing
│   ├── question_refinement_protocol.md
│   └── taxonomy.json
├── sources/                          # 68 richly annotated journalistic, primary & academic sources
│   ├── README.md
│   ├── media/                        # Wire/record, investigative, specialist beat, regional & primary OSINT
│   └── academic/                     # Scholarly APIs, working-paper/preprint archives, standards & institutes
├── guardrails/                       # Pillar 2: Admiralty 6x6, ACH, fallacies, biases & 7-gate introspection
│   ├── source_evaluation_protocol.md
│   ├── source_credibility_rubric.json
│   ├── hypothesis_testing_ach.md
│   ├── structured_analytic_techniques.json
│   ├── logical_fallacies.json
│   ├── biases_catalog.json
│   ├── introspection_protocol.md
│   └── introspection_checklist.json
├── concepts/                         # Pillar 3: Academic concept buttressing & pedagogical synthesis
│   ├── concept_research_protocol.md
│   └── concept_taxonomy.json
├── workflows/
│   └── journalist_academic_pipeline.md
├── templates/
│   └── research_brief_template.md
├── examples/
│   ├── sample_research_dossier.json  # Passing end-to-end Journalist + Academic dossier (100/100 score)
│   └── flawed_research_dossier.json  # Negative example catching echo provenance, preprint & bias violations
├── osint_agent/                      # Pure-stdlib Python 3.10+ engine (loader, validator, router, auditor, CLI)
└── tests/                            # Automated unit & integration test suite (`unittest`)
```

---

## Quickstart (Zero External Dependencies)

Requires only **Python 3.10+** standard library—no `pip install` or network setup needed to run routing, querying, validation, or dossier auditing.

### 1. Validate Schema & Cross-Reference Integrity
```bash
./bin/osint validate
```

### 2. Refine & Route a Raw Research Question
```bash
./bin/osint route "Why did export bans on EUV lithography chips to China backfire?"
# Or emit structured JSON for programmatic agent consumption:
./bin/osint route "Is the ICJ provisional measures order legally binding?" --format json
```

### 3. Query Curated Media & Academic Directories
```bash
./bin/osint sources --track media --domain conflict_defense_security --open-access
./bin/osint sources --track academic --domain economics_markets_trade
./bin/osint concepts --domain climate_energy_environment
./bin/osint guardrails --type biases --domain geopolitics_diplomacy
```

### 4. Run the Epistemic Guardrail & Introspection Gate on a Draft Dossier
```bash
# Passes all 7 introspection gates, Admiralty corroboration, ACH, and preprint hygiene:
./bin/osint audit examples/sample_research_dossier.json

# Rejects circular reporting, unneutralized prompt bias, unflagged preprints, and overconfidence:
./bin/osint audit examples/flawed_research_dossier.json
```

### 5. Python Library API for Orchestrator Agents
```python
from osint_agent import DirectoryRepository, EpistemicAuditor, HeuristicRouter

repo = DirectoryRepository()
router = HeuristicRouter(repo)

plan = router.route("What caused the recent sovereign bond yield spike and FX swap basis blowout?")
print(plan.primary_domain["id"])          # 'economics_markets_trade'
print(plan.matched_concept_clusters[0]["id"])  # 'monetary_plumbing_liquidity_and_yield_curves'
```

---

## Running the Test Suite

```bash
python3 -m unittest discover -s tests -v
```

---

## Extending the Directory

1. **Adding a Media or Primary OSINT Source**: Append an entry to the appropriate catalog in `sources/media/` including ownership/funding disclosure, editorial standards, baseline Admiralty reliability (`A`–`C`), strengths, known limitations/biases, and a concrete `corroboration_pairing_rule`.
2. **Adding an Academic Repository or Concept Cluster**: Add repositories to `sources/academic/` (with explicit `peer_review_status` and `evidence_tier`) and map technical trigger terms in `concepts/concept_taxonomy.json`.
3. **Verify Integrity**: Run `./bin/osint validate && python3 -m unittest discover -s tests -v` to verify JSON Schema compliance and cross-file referential integrity.
