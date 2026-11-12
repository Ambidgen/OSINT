# Curated Source Directory Governance & Architecture

This directory contains the machine-readable catalogs of journalistic, primary-telemetry, and academic sources used by Agentic AI operating within this repository.

## Dual-Track Organization

1. **`sources/media/` — The Journalist Track (Facts on the Ground)**
   - **`wire_services_and_global_record.json`** (`tier_1_global_wire_and_record`): Global wire agencies and international newspapers/broadcasters of record with multi-layer editorial fact-checking, formal corrections policies, and global bureau footprints.
   - **`investigative_and_verification.json`** (`tier_2_investigative_and_verification`): Non-profit investigative newsrooms and open-source forensic collectives (geolocation, chronolocation, leaked-document cross-verification).
   - **`specialist_and_sector_press.json`** (`tier_2_specialist_beat`): Domain-dedicated publications whose beat reporters possess technical literacy superior to generalist outlets (epidemiology, cybersecurity, national security law, climate science, defense posture).
   - **`regional_established.json`** (`tier_2_regional_record`): Editorially independent newspapers and news agencies rooted in specific geographies, indispensable for local context, language access, and countering distant-capital blind spots.
   - **`primary_and_institutional_osint.json`** (`primary_official_and_sensor`): Primary documents, court dockets, securities filings, macroeconomic statistical bureaus, vulnerability databases, sanctions registries, and open physical sensor networks (ADS-B, AIS, satellite imagery).

2. **`sources/academic/` — The Academic Track (Concept Understanding)**
   - **`scholarly_indexes_and_open_apis.json`**: Programmatic scholarly discovery graphs (OpenAlex, Semantic Scholar, Crossref, PubMed) and scientific-integrity verification tools (Retraction Watch).
   - **`discipline_repositories_and_preprints.json`**: Discipline-specific working-paper archives and preprint servers (arXiv, NBER, RePEc, SSRN, bioRxiv/medRxiv, PhilPapers, WorldLII) with explicit peer-review status tags and clinical/policy hygiene rules.
   - **`reference_standards_and_think_tanks.json`**: Living peer-reviewed encyclopedias, systematic-review clearinghouses (Cochrane, IPCC), technical standards bodies (NIST, IETF, IEEE, BIS), and established research institutes (SIPRI, Chatham House, Carnegie) annotated with governance and funding disclosures.

## Inclusion & Epistemic Hygiene Principles

- **No Infallible Source**: Even `tier_1_global_wire_and_record` outlets carry a *baseline* Admiralty source reliability (`A` or `B`), never an automatic `1` on information credibility. Every factual claim still requires independent multi-source corroboration (`1`–`6`) and provenance tracing.
- **Explicit Limitations Required**: Every source entry must document `known_limitations_and_biases` (e.g., paywalls, geopolitical framing, donor ecosystems, breaking-news speed risk, unrefereed preprint status) and a concrete `corroboration_pairing_rule`.
- **Schema Validation**: All files in `sources/media/` validate against `schemas/media_source.schema.json`; all files in `sources/academic/` validate against `schemas/academic_source.schema.json`. Run `python3 -m osint_agent validate` after any edit.
