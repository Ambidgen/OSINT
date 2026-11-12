# Source Credibility & Provenance Evaluation Protocol

Agentic AI systems frequently fail OSINT tasks not because they lack retrieval access, but because they flatten **source prestige**, **claim corroboration**, and **upstream provenance** into a single binary judgment ("credible website = true fact"). This protocol enforces strict separation across all three dimensions.

---

## 1. The Two-Axis Admiralty Evaluation (`A–F` × `1–6`)

Every citation recorded in an Agentic AI's Evidence Ledger must be scored on **two orthogonal axes** (defined in `guardrails/source_credibility_rubric.json`):

| Source Reliability (`A`–`F`) | Information Credibility (`1`–`6`) |
| :--- | :--- |
| **A**: Completely reliable (audited primary registry, calibrated physical telemetry, Tier-1 wire/investigative desk) | **1**: Confirmed by genuinely independent sources + primary/physical consistency |
| **B**: Usually reliable (specialist beat press, regional newspaper of record, vetted OSINT collective) | **2**: Probably true; logical and consistent with domain mechanics, firsthand reporting |
| **C**: Fairly reliable (advocacy/think-tank brief, single-vendor commercial report, working paper) | **3**: Possibly true; plausible but single-source anonymous or uncorroborated |
| **D**: Not usually reliable (state-controlled propaganda organ, sensationalist tabloid) | **4**: Doubtful; contradicts baseline constraints or exhibits obvious self-serving incentive |
| **E**: Unreliable (known disinformation mill, synthetic slop farm, forged document) | **5**: Improbable; directly refuted by verified telemetry or primary records |
| **F**: Reliability cannot be judged (unfamiliar/first-time eyewitness account) | **6**: Truth cannot be judged (collection blackout, zero independent open-source visibility) |

### Critical Operational Rules
1. **`A3` Is Not `A1`**: When *Reuters* or *The New York Times* reports *"a senior official speaking on condition of anonymity said X"*, the rating is **`A3` or `B3`** (`attributed_reporting`), **never `A1`** (`confirmed_fact`).
2. **`F1` Is Valid Ground Truth**: When an unknown local bystander (`F`) uploads smartphone footage of an industrial explosion whose timestamp, shadow geometry, building skyline, and Sentinel-2 SAR burn scar are independently geo-verified (`1`), the artifact achieves **`F1`** confirmation.
3. **News vs. Opinion Firewall**: Major newspapers of record (*WSJ*, *NYT*, *FT*, *The Hindu*, *Le Monde*) publish Op-Eds alongside straight news. Op-Eds represent normative advocacy and must never be cited as newsroom factual verification.

---

## 2. Lateral Reading (SIFT) & Anti-Citogenesis Tracing

Before treating two URLs as "corroboration," the agent must execute the **SIFT** sequence:

1. **S — Stop**: Do not accept headline framing or snippet summaries at face value.
2. **I — Investigate the Source**: Check ownership, state affiliation, funding model, and editorial corrections apparatus (query `python3 -m osint_agent sources`).
3. **F — Find Better Coverage**: If a claim originates in a partisan aggregator or social post, pivot horizontally to Tier-1 wires, specialist beat press, and primary dockets.
4. **T — Trace to Upstream Provenance**: Identify the **root origin** (`upstream_provenance`) of the specific number, quote, or allegation:
   - *Echo Corroboration (Citogenesis Trap)*: Outlet B cites Outlet A, Outlet C aggregates Outlet B, and Wikipedia cites Outlet C. **True independent source count = 1.**
   - *True Triangulation*: A Reuters correspondent interviews dockworkers on site + Marine AIS shows vessel draft/course shift + Lloyd's/port authority notice confirms berth closure. **True independent source count = 3 across distinct evidentiary modalities.**

---

## 3. Disqualification & Quarantine Triggers

- **State-Controlled Media**: May be cited *only* to establish official state posture (*"State broadcaster X stated..."*), never as uncorroborated evidence of ground facts.
- **Unverified Kinetic OSINT Accounts**: High-engagement social-media "OSINT aggregator" accounts that repost unattributed combat footage without coordinates or timestamps are quarantined (`F6`/`D4`) unless traced to reproducible geolocation collectives (e.g., Bellingcat, CIR, BBC Verify).
- **Retracted or Predatory Papers**: Any academic work flagged `is_retracted: true` in Crossref/OpenAlex/Retraction Watch is disqualified from supporting empirical claims.
