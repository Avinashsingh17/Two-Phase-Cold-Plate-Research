---
title: "Schema Evolution Log"
type: synthesis
last_updated: 2026-05-17
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
