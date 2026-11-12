# Critical Thinking & Hypothesis Stress-Testing Protocol (ACH)

When an Agentic AI moves beyond reporting raw facts ("What happened?") to analytical explanation ("Why did it happen, who is responsible, or what does it mean?"), its single greatest failure mode is **building a brief for its first plausible theory**. This protocol mandates structured falsification using **Analysis of Competing Hypotheses (ACH)** and adversarial critique.

---

## 1. Formulating Mutually Distinct Competing Hypotheses

For any non-trivial causal, attribution, or impact question, the agent MUST formulate **at least 2 to 4 competing hypotheses** before drafting conclusions:

- **$H_1$ (Primary/Prominent Explanation)**: Often the dominant framing in initial media coverage.
- **$H_2$ (Rival Strategic or Structural Explanation)**: An alternative mechanism grounded in economic incentives, domestic politics, or rival actor constraints.
- **$H_0$ (Mundane / Friction / Null Hypothesis)**: Technical failure, bureaucratic miscoordination, statistical noise, reporting lag, or coincidence rather than deliberate grand design.

> **Anti-Bifurcation Rule**: Avoid setting up a straw-man extreme solely to make $H_1$ look reasonable (`false_dilemma`). Every alternative hypothesis must be **steel-manned** using its strongest primary or scholarly formulation.

---

## 2. Diagnosticity & Disconfirmation Scoring

Human and AI analysts naturally accumulate *confirming* evidence—facts consistent with their favored hypothesis. However, if Evidence $E_1$ is equally consistent with $H_1$, $H_2$, and $H_0$, **$E_1$ has zero diagnostic value**.

1. **Work Across the Matrix (Evidence $\rightarrow$ Hypotheses), Not Down Columns**:
   For each verified item in the Evidence Ledger, ask: *"If $H_k$ were true, how probable would it be to observe $E_i$?"*
2. **Prioritize Disconfirming Anomalies**:
   - The winning hypothesis is **not** the one with the longest list of compatible anecdotes; it is the hypothesis with the **fewest credible disconfirming anomalies**.
   - Record both `supporting_evidence_ids` AND `disconfirming_evidence_ids` in the dossier's `competing_hypotheses` array.
3. **Symmetric Falsification Searches**:
   Before closing collection, execute at least one search query explicitly designed to *refute* the leading hypothesis (e.g., searching for counterfactual baseline frequencies, technical impossibility critiques, or rival econometric estimates).

---

## 3. Key Assumptions Check (KAC)

Every analytical synthesis rests on unstated background premises. Surface at least 2–3 key assumptions explicitly by asking:

- *What must remain true about physical infrastructure, legal jurisdiction, coalition stability, or data accuracy for my conclusion to hold?*
- *Which assumption is least well-supported by primary evidence, and what observable indicator would show it breaking?*

---

## 4. Fallacy & Bias Cross-Scan

Before transitioning to the Introspection Gate, cross-check the draft reasoning against:
- `guardrails/logical_fallacies.json` (especially `post_hoc_ergo_propter_hoc`, `base_rate_neglect`, `motte_and_bailey`, `fallacy_of_composition_division`, and `circular_reporting_petitio_principii`).
- `guardrails/biases_catalog.json` across all three layers:
  1. **Analyst/AI Layer**: Did I mirror-image a foreign actor? Did I anchor on the first search snippet? Did I succumb to sycophancy toward the user's prompt? Did I rely on stale parametric training memory?
  2. **Media Layer**: Do my citations rely exclusively on anonymous officials from a single capital?
  3. **Data Layer**: Are my numbers skewed by testing/ascertainment shifts, survivorship visibility in connected cities, or Goodhart's Law metric gaming?
