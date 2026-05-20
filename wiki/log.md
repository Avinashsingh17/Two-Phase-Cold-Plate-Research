---
title: Wiki Log
---

# Wiki Log

_Append-only chronological record of all wiki operations._

## [2026-05-07] ingest | Hall & Mudawar 2000 — Subcooled CHF Correlations
Created `wiki/papers/HallMudawar2000_subcooled_CHF.md` — equations-heavy summary of the inlet- and outlet-conditions subcooled CHF correlations (5 constants each), parametric ranges, error bands (MAE 10.3%), and comparison to Groeneveld 1995 LUT. Created `wiki/concepts/CHF_correlations.md` as anchor page for all CHF correlations. Created `wiki/entities/mudawar_group.md` for Purdue PUREES Lab. Updated paper template to include standard "Applicability to This Project" section.

## [2026-05-08] ingest | Krepper & Rzehak 2011 — DEBORA Subcooled Flow Boiling
Created `wiki/papers/KrepperRzehak2011_DEBORA.md` — setup-recipe table (14 closures × 5 columns incl. sensitivity tags and Fluent-TBD column), N_ref calibration procedure, DEBORA test matrix with DEBORA 3 recommended as Stage 1 primary target, and model limitations (wall-peak→core-peak failure, monodisperse assumption). Created `wiki/concepts/RPI_wall_boiling_model.md` — conceptual home for heat flux partitioning framework with closure catalog and known failure modes. Created `wiki/concepts/RPI_model_implementation.md` — sparse CFX→Fluent translation checklist with risk items (Tomiyama lift sign reversal, boiling wall function likely need UDFs). Skipped HZDR entity page (only one paper so far).

## [2026-05-20] ingest | Qu & Mudawar 2003 — Flow Boiling in Microchannel Heat Sinks (Part I)
Created `wiki/papers/QuMudawar2003_microchannel_boiling_I.md` — Fluent-reproduction-ready geometry tables (unit cell, planform, TC instrumentation with missing-dimension flags), 11-row correlation assessment table (MAE + trend columns; 0/11 capture correct h_tp vs x_e trend), publication cluster cross-referencing Parts I–III, experimental conditions, and applicability notes (saturated-only coverage, low-G range). Created `wiki/synthesis/motivation_for_CFD_approach.md` — first synthesis page arguing correlation-based design is unreliable for water microchannels, motivating CFD. Created `wiki/communication/plain_language_explanation.md` — canonical long-form physics-first project explanation. Updated `wiki/entities/mudawar_group.md` with second publication. Updated CLAUDE.md to add `communication/` directory. Two schema_evolution entries added (experimental vs CFD paper distinction, communication/ directory).
