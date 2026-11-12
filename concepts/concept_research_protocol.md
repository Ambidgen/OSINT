# Concept Understanding & Academic Buttressing Protocol

Journalistic wire reporting excels at answering **what just happened**, **who acted**, and **when**. Yet readers regularly walk away from accurate news coverage still confused because current events turn on **esoteric, technical, legal, economic, or scientific mechanisms** that daily journalism lacks space to unpack.

The **Academic Track** directs the Agentic AI to step alongside its Journalist persona as a deliberate, structured scholar—identifying those hidden mechanisms, grounding them in peer-reviewed literature and formal standards, and translating them clearly for the reader.

---

## 1. Concept Extraction Triggers: When to Invoke Academic Research

During Phase 1 intake and Phase 2 reading of news dispatches, flag any term, mechanism, or causal claim matching these five trigger classes:

1. **Physical & Engineering Bottlenecks**:
   *Examples*: High-NA EUV lithography, synchronous grid inertia, low-Earth-orbit Kessler syndrome, synthetic-aperture radar (SAR) interferometry, enrichment separative work units (SWU).
2. **Financial & Macroeconomic Plumbing**:
   *Examples*: Cross-currency FX swap basis, yield-curve control (YCC), bank duration mismatch, sovereign collective action clauses (CACs), tariff incidence / terms-of-trade elasticity.
3. **Doctrinal Legal & Treaty Thresholds**:
   *Examples*: ICJ *prima facie* plausibility vs. merits standard, UNCLOS *transit passage* vs. *innocent passage*, IHL proportionality calculus, U.S. major-questions or preliminary-injunction standards.
4. **Biomedical & Statistical Denominators**:
   *Examples*: Case Fatality Ratio (CFR) vs. Infection Fatality Ratio (IFR), $R_0$ vs. $R_t$, antigenic shift/reassortment, statistical power, relative vs. absolute risk reduction.
5. **Cyber, Cryptographic & AI Architecture**:
   *Examples*: BGP route hijacking, memory-safety heap overflow, post-quantum lattice cryptography, supply-chain signing compromise, LLM scaling/evaluation contamination.

---

## 2. The Five-Rung Academic Evidence Hierarchy

Not all "academic-looking" PDFs carry equal epistemic authority. Rank and label conceptual sources strictly according to `concepts/concept_taxonomy.json`:

| Rank | Evidence Tier | Canonical Repositories | Agent Usage Rule |
| :---: | :--- | :--- | :--- |
| **1** | **Meta-Analyses & Consensus Syntheses** | `cochrane_library`, `ipcc_assessments`, systematic reviews via `openalex` / `pubmed_pmc` | Highest authority for empirical effect sizes and consensus bounds; report certainty/GRADE levels explicitly. |
| **2** | **Peer-Reviewed Primary Literature** | `openalex`, `semantic_scholar`, `pubmed_pmc`, `doaj_core`, `philpapers` | Verify DOI via `crossref`, screen `retraction_watch`, and check whether independent groups replicated the result. |
| **3** | **Formal Technical Standards & Living Reference** | `nist_ietf_ieee`, `stanford_encyclopedia`, `our_world_in_data`, `worldlii_heinonline`, `sipri_iiss` | Authoritative for protocol definitions, statutory text, philosophical rigor, and long-run empirical baselines. |
| **4** | **Institutional Working Papers & Policy Briefs** | `nber`, `repec_ideas`, `bis_central_bank_research`, `cfr_chatham_carnegie` | High value for rapid empirical identification on recent policy shocks; note pre-journal-referee status and institutional lens. |
| **5** | **Unrefereed Preprints** | `arxiv`, `biorxiv_medrxiv`, `ssrn` | **Mandatory Caveat**: Label explicitly as *non-peer-reviewed preprint*; never present clinical/medical preprints as settled fact. |

---

## 3. The Four-Part Pedagogical Bridge Pattern

Academic research fails the reader if dumped as impenetrable jargon or detached textbook trivia. Every entry in `academic_track.concepts_explained` must follow this **Four-Part Pedagogical Bridge**:

1. **Plain-Language Definition**: A crisp 1–2 sentence definition free of circular jargon.
2. **Underlying Mechanism (*How It Works*)**: The causal, physical, mathematical, or statutory logic that governs the system's behavior.
3. **Direct Bridge to Today's Event (*Why It Matters Now*)**: How this exact mechanism constrains the actors on the ground, explains why the news event matters, or punctures a common media misconception.
4. **Scholarly Consensus & Caveats**: Explicitly state whether the mechanism represents `settled_consensus` (e.g., Maxwell's optics / accounting identities), `active_scholarly_debate` (e.g., magnitude of tariff pass-through across sectors), or `emerging_frontier` (e.g., newly posted AI/physics preprints).
