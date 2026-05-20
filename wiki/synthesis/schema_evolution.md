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

## [2026-05-20] Added wiki/synthesis/open_questions.md

**What:** Created a consolidated open-questions tracker that mirrors all `<!-- TODO -->` items and unresolved questions from across the wiki. Inline TODOs stay on source pages (close to context); the tracker provides a single view for prioritization. Updated during each lint pass.

**Why:** With 3 papers ingested, open questions are scattered across 5+ pages. A consolidated view makes it easier to decide which gaps to fill next and to track resolution over time.
