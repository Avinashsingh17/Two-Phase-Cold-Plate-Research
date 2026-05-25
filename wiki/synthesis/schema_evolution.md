---
title: "Schema Evolution Log"
type: synthesis
last_updated: 2026-05-20
tags: [meta, schema, wiki-structure]
---

## Purpose

Append-only log of structural decisions about the wiki schema. Records what changed, when, and why — so that 20 papers from now we remember the reasoning behind current conventions.

---

## [2026-05-07] Initial schema established

Created CLAUDE.md (wiki schema), directory structure, all 5 page templates (paper, concept, entity, comparison, synthesis), wiki/index.md, wiki/log.md. Paper template included both "Relevance to This Project" and "Applicability to This Project" as separate sections.

## [2026-05-08] Added "Applicability to This Project" to paper template

After first ingest (Hall & Mudawar 2000): user requested an explicit section on every paper page that flags geometry/fluid/solver mismatches, standard workarounds, and cross-references to gap-filling papers. Added as a section below "Relevance."

Added sensitivity/criticality column to the setup-recipe table convention for CFD papers. Established convention: paper-specific sections (Correlation Equations, Setup Recipe, Test Matrix, etc.) are added beyond the template skeleton as needed — template is a floor, not a ceiling.

## [2026-05-17] Collapsed Relevance + Applicability; dropped (pending ingest) annotations

**What:** Merged "Relevance to This Project" and "Applicability to This Project" into a single "Applicability to This Project" section in the template and all existing paper pages.

**Why:** In practice, "Relevance" was always just the first paragraph of "Applicability" — keeping them separate created redundant structure and ambiguity about where to put content. One section that covers both "why this matters" and "where the gaps are" is cleaner.

**What:** Removed all `(pending ingest)` annotations from `[[wikilinks]]`.

**Why:** Broken links are self-evidently pending. The annotations created stale state that required maintenance on every future ingest. Option (a) — just drop them — minimizes bookkeeping.

**Lint finding:** Template-vs-actual drift on both paper pages is intentional. Paper-specific sections (Correlation Equations, Setup Recipe, Test Matrix, N_ref Calibration, etc.) extend beyond the template skeleton. No reconciliation needed — the template defines the minimum required sections, not the maximum.

## [2026-05-20] Experimental vs CFD paper distinction clarified

**What:** After 3 ingests, the paper template now implicitly distinguishes two sub-types of paper pages. Experimental papers (Hall & Mudawar 2000, Qu & Mudawar 2003) feature Geometry tables and Data Available sections but no Model Setup Recipe. CFD methodology papers (Krepper & Rzehak 2011) feature a Model Setup Recipe table with sensitivity/criticality tags and a Fluent-equivalent column. Both share the same outer structure (Summary, Key Findings, Applicability, Cross-References, Notes); the middle sections differ by paper type.

**Why:** The template skeleton is intentionally a floor, not a ceiling. No formal sub-template is needed — the existing convention of extending beyond the template naturally accommodates this. Documenting the pattern here so future ingests follow the established precedent.

## [2026-05-20] Added wiki/communication/ directory

**What:** Created `wiki/communication/` for audience-facing artifacts (plain-language explanations, elevator pitches, poster abstracts). First file: `plain_language_explanation.md`. Updated CLAUDE.md directory structure and added a "Communication artifacts" section describing purpose and maintenance expectations.

**Why:** Communication artifacts derive from synthesis but serve a different audience and purpose. They are living documents that should be flagged for update when new ingests materially change the project narrative. Keeping them in `wiki/` (rather than a separate top-level directory) maintains the single-knowledge-base principle.

## [2026-05-20] Entity pages track strict authorship only

**What:** After 3 ingests + first lint pass — entity pages track strict authorship only, not citation chains. Future ingests should only link entity pages from papers authored by that entity. Removed `[[mudawar_group]]` from Krepper & Rzehak 2011 cross-references (Krepper is Helmholtz-Zentrum, not Mudawar group). Paper-to-paper citation links (e.g., Krepper → Hall & Mudawar 2000) remain on the paper page and are the correct mechanism for tracking citation context.

**Why:** Conflating authorship and citation chains in entity pages muddies what entity pages mean. If every paper that *cites* a Mudawar paper links to `[[mudawar_group]]`, the entity page becomes a citation index rather than an authorship registry. Citation chains are already captured by paper-to-paper cross-references.

## [2026-05-24] Correlation-development papers — no new sub-type

**What:** Kim & Mudawar 2013 (universal saturated-boiling HTC correlation) is the first "correlation-development" paper ingested. Its page extends the template with Correlation Equations, Applicability Map, and Calibration Data sections — handled entirely by the existing "template is a floor, not a ceiling" precedent. No formal sub-type or sub-template created.

**Why:** The pattern already accommodates this naturally, just as it did for experimental vs. CFD papers. Formalizing sub-types would add schema weight without actionable benefit. Documented here so future correlation-paper ingests follow suit without re-litigating.

## [2026-05-24] Experimental papers split into two sub-roles

**What:** With Drummond et al. 2018, experimental papers now serve two distinct functional roles: (1) **validation benchmarks** (Qu & Mudawar 2003) — Applicability section foregrounds "can we reproduce this in CFD?" with geometry tables optimized for Fluent setup; (2) **baseline design sheets** (Drummond 2018) — Applicability section foregrounds "what would beating this by 15% look like?" with baseline-comparison logic and performance ceilings. Both share the same outer structure and Geometry/Data Available sections.

**Why:** The distinction is in how the Applicability section is framed, not in the template skeleton. Validation benchmarks define gates in the validation pipeline (CLAUDE.md registry). Baseline design sheets define optimization targets. The pattern will recur (e.g., Mandel & Garimella when ingested). No sub-template needed — handled by the floor-not-ceiling convention.

## [2026-05-24] Heat flux reporting convention adopted

**What:** All heat fluxes reported in the wiki refer to **chip-level device heat flux** (q″_device = Q_net / A_chip) unless explicitly noted as base heat flux (q″_base = Q_net / A_channel_base). Convention defined on [[Drummond2018_manifold_microchannel]] and referenced from any future comparison page.

**Why:** Different papers reference heat flux to different areas (channel base area, heat sink footprint, chip footprint). For cross-study comparisons and the ≥15% improvement criterion, a consistent convention is essential. Device heat flux is chosen because it represents the system-level constraint (watts per unit chip area that must be dissipated), which is what end users care about.

## [2026-05-24] Paired-paper convention for multi-part studies

**What:** Ozguc, Pan & Weibel 2024 Parts 1 and 2 are ingested on a single wiki page (`Ozguc2024_topology_optimization.md`) rather than two separate pages. The page covers both papers with sections clearly attributing findings to Part 1 or Part 2.

**Why:** Parts 1 and 2 form a single intellectual unit (framework + calibration/validation). Splitting them would fragment the narrative and require constant cross-referencing between two pages for a workflow that only makes sense as a whole. This is a convention for multi-part companion papers, not a new sub-type. Single-page treatment applies when the parts are published together and share authorship; independently published follow-ups from different groups would still get separate pages.

## [2026-05-20] Added wiki/synthesis/open_questions.md

**What:** Created a consolidated open-questions tracker that mirrors all `<!-- TODO -->` items and unresolved questions from across the wiki. Inline TODOs stay on source pages (close to context); the tracker provides a single view for prioritization. Updated during each lint pass.

**Why:** With 3 papers ingested, open questions are scattered across 5+ pages. A consolidated view makes it easier to decide which gaps to fill next and to track resolution over time.
