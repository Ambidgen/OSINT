# Heuristic Question Refinement & Source Routing Protocol

Raw research questions posed by human users—or generated mid-workflow by upstream orchestrator agents—are frequently **underspecified**, **broad**, **temporally ambiguous**, or **loaded with presuppositions**. Before executing web searches or fetching documents, an Agentic AI must pass the query through a four-step categorical refinement pipeline (`python3 -m osint_agent route "<question>"`).

---

## Step 1: Prompt Neutralization & De-Biasing

Search engines and RAG pipelines reflect the framing of the query string. Searching *"Why did Policy X fail catastrophically?"* retrieves polemical commentary confirming failure while missing empirical evaluations showing mixed or lagged effects.

1. **Scan for Framing Markers** (cataloged in `heuristics/taxonomy.json` under `framing_neutralization_markers`):
   - *Loaded Presuppositions*: `"why did X fail"`, `"why is X corrupt"`, `"how did X rig"`, `"inevitable collapse"`
   - *Emotional/Absolutist Intensifiers*: `"catastrophic"`, `"disaster"`, `"hoax"`, `"miracle"`, `"total failure"`, `"undeniably"`
   - *Conspiratorial Premise*: `"secret plot"`, `"cover-up"`, `"deliberately crashing"`
2. **Reformulate Neutrally**:
   Convert value-laden assertions into measurable empirical questions:
   - *Raw*: `"Why are semiconductor export controls completely failing to stop AI chips?"`
   - *Neutralized*: `"What are the documented enforcement outcomes, compliance mechanisms, supply-chain adaptations, and smuggling/cloud-access workarounds associated with current semiconductor export controls?"`

---

## Step 2: Dual-Track Decomposition (Journalist vs. Academic)

Split every neutralized research question into two complementary sub-question sets:

### Track A — Journalist Sub-Questions (*Facts on the Ground*)
Focus on empirical, timestamped events, actor actions, and primary records:
- **What** concrete action, incident, filing, or announcement occurred?
- **Who** are the named institutional, state, corporate, or judicial actors?
- **When and Where** did the events take place, and what is the verification status (`confirmed_fact` vs. `attributed_reporting`)?
- **What primary artifact** anchors the story (court order, sanctions designation, satellite pass, statistical release, 8-K filing)?

### Track B — Academic Sub-Questions (*Concept Understanding*)
Focus on esoteric, technical, legal, or scientific mechanisms required for genuine reader comprehension:
- **What specialized terms or physical/institutional mechanisms** appear in the story (e.g., *High-NA EUV lithography*, *ICJ provisional measures plausibility threshold*, *FX swap basis*, *antigenic shift vs. drift*, *grid synchronous inertia*)?
- **How does the mechanism work** according to peer-reviewed literature or formal engineering/legal standards?
- **Where does scholarly consensus stand**, and what common media misconceptions distort public understanding?

---

## Step 3: Categorical Matrix Classification

Classify the decomposed query along three routing axes (`heuristics/taxonomy.json`):

1. **Domain Classification** (Primary + Secondary Domains):
   - `geopolitics_diplomacy`
   - `conflict_defense_security`
   - `economics_markets_trade`
   - `technology_cyber_ai`
   - `science_medicine_public_health`
   - `climate_energy_environment`
   - `law_governance_human_rights`
   - `society_demographics_labor`
2. **Geographic Scope**:
   - `global`, `north_america`, `europe`, `east_asia_pacific`, `south_central_asia`, `middle_east_north_africa`, `sub_saharan_africa`, `latin_america_caribbean`
3. **Temporal Horizon**:
   - `breaking_sub_24h`: Prioritize multi-wire confirmation (`reuters`, `associated_press`, `afp`), official alerts, and strict fog-of-war restraint.
   - `developing_days_weeks`: Add specialist beat press, regional record newspapers, and forensic OSINT collectives (`bellingcat`, `cir_info_resilience`).
   - `ongoing_structural_months`: Integrate investigative journalism (`propublica`, `icij`, `occrp`), full official statistical series, and working papers (`nber`, `bis_central_bank_research`).
   - `historical_settled`: Anchor primarily in peer-reviewed scholarship, systematic reviews, archival court judgments, and harmonized long-run series (`our_world_in_data`).

---

## Step 4: Diverse Multi-Tier Source Bundle Construction

Never route an inquiry to a single media tier or single national vantage point. Every routed query dispatches a **4-part Journalist Bundle + Academic Concept Bundle**:

1. **Global Wire / Record Anchor** (>= 2 independent global wires/records, e.g., `reuters` + `afp` or `financial_times`)
2. **Specialist Beat OR Forensic Verification Desk** (domain-literate reporting, e.g., `stat_news`, `lawfare`, `carbon_brief`, `krebs_on_security`, `bellingcat`)
3. **Regional Record Counterweight** (local ground truth from the affected region, e.g., `nikkei_asia`, `the_hindu`, `al_monitor`, `le_monde`, `daily_maverick`, `folha_de_spaulo`)
4. **Primary Official / Sensor Registry** (hard documentary/physical anchor, e.g., `sec_edgar`, `icj_icc_filings`, `imf_world_bank_fred`, `who_cdc_ecdc`, `cisa_nvd`, `usgs_copernicus_noaa`)
5. **Academic Concept Sources** (peer-reviewed discovery + standards/synthesis, e.g., `openalex`, `semantic_scholar`, `cochrane_library`, `nist_ietf_ieee`, `stanford_encyclopedia`)
