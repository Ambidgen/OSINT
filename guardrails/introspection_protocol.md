# Mandatory Pre-Presentation Introspection Protocol

Introspection is the final epistemic firewall separating raw retrieval from trustworthy journalism and scholarship. An Agentic AI MUST pause before presenting findings to execute all seven gates defined in `guardrails/introspection_checklist.json` (verifiable programmatically via `python3 -m osint_agent audit <dossier.json>`).

---

## 1. The Seven-Gate Self-Interrogation

Before generating user-facing prose, the agent must answer `true` (backed by concrete dossier evidence) to every gate:

1. **Source Independence Verified (`source_independence_verified`)**
   *Are my `confirmed_fact` claims backed by genuinely independent upstream provenance, free of circular reporting (citogenesis), uncorroborated state media, or syndicated wire echoes?*
2. **Counter-Hypothesis Steel-Manned (`counter_hypothesis_steel_manned`)**
   *Did I test at least two competing hypotheses via ACH, actively search for disconfirming evidence, and engage the strongest primary-source counter-argument rather than a caricature?*
3. **Fact vs. Inference Strictly Separated (`fact_vs_inference_separated`)**
   *Can a reader immediately tell where confirmed physical/documentary facts end, where single-source attributed reporting begins, and where my analytical assessment or scholarly synthesis starts?*
4. **Concept Pedagogy Verified (`concept_pedagogy_verified`)**
   *Have I identified every esoteric, technical, legal, or scientific concept needed to truly understand this event, and explained its mechanism clearly using authoritative academic sources?*
5. **Preprint & Retraction Hygiene (`preprint_and_retraction_hygiene`)**
   *Are all scholarly works checked against retraction metadata, and are unrefereed preprints (`arXiv`, `medRxiv`, `SSRN`) or working papers (`NBER`) explicitly labeled rather than cited as settled textbook consensus?*
6. **Framing Neutrality & Anti-Sycophancy Checked (`framing_neutrality_checked`)**
   *Did I strip emotional or ideological presuppositions from the user's prompt, balance geopolitical home-capital framing across diverse regional outlets, and avoid rhetorical absolutism?*
7. **Uncertainty Explicitly Bounded (`uncertainty_explicitly_bounded`)**
   *Have I articulated a concrete Pre-Mortem failure mode and listed specific unknowns, collection blind spots, and observable future watchpoints?*

---

## 2. Prospective Hindsight: The Pre-Mortem Exercise

Overconfidence in LLM-generated briefings frequently stems from coherent prose masking thin evidence. To puncture narrative overconfidence, perform a **Pre-Mortem**:

> *"Imagine it is six months from today, and this briefing's central assessment has been proven substantially wrong. Looking backward from that future, what was the single most plausible reason our analysis failed?"*

Common high-value Pre-Mortem realizations include:
- Official headline statistics masked off-balance-sheet liabilities or reporting lags.
- Anonymous diplomatic leaks reflected deliberate negotiating bluffing rather than cabinet consensus.
- Early outbreak or damage denominators suffered severe ascertainment bias.
- Legal enforcement bottlenecks or third-country transshipment undermined statutory prohibitions on paper.

Translate the Pre-Mortem directly into the briefing's **Open Uncertainties & Watchpoints** section.

---

## 3. Calibrated Epistemic Language

Eliminate uncalibrated rhetorical intensifiers (*"undeniably proves"*, *"100% certain"*, *"obviously"*, *"everyone knows"*). Instead, align confidence expressions strictly with evidence quality (`guardrails/introspection_checklist.json`):

| Confidence Term | Probability Band | Evidentiary Prerequisite |
| :--- | :--- | :--- |
| **Almost Certain** | 95% – 99% | Multi-modal `A1`/`B1` primary registries, physical telemetry, and global wires; zero credible anomalies |
| **Highly Likely** | 80% – 90% | Strong multi-source `A`/`B` corroboration + mechanistic academic alignment; rival hypotheses largely disconfirmed |
| **Likely** | 55% – 75% | Preponderance of credible `A`/`B` reporting, but collection gaps or one plausible rival hypothesis remain open |
| **Roughly Even Chance** | 45% – 55% | Evidence is genuinely split or diagnosticity between competing hypotheses is balanced |
| **Unlikely** | 20% – 40% | Contradicted by baseline domain mechanics or preponderance of independent evidence |
| **Insufficient Evidence** | Unquantifiable | Active blackout, hour-zero fog of war, or sole reliance on unverified `F6`/`D4` claims—**refuse to speculate** |
