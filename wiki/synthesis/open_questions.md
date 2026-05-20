---
title: "Open Questions — Consolidated TODO Tracker"
type: synthesis
last_updated: 2026-05-20
tags: [meta, open-questions, TODO, lint]
---

## Purpose

Consolidated list of all open `<!-- TODO -->` items and unresolved questions across the wiki. Maintained during each lint pass. Inline TODOs remain on their source pages (close to context); this page provides a single view for prioritization.

---

## Open TODOs

| # | Source page | Description | Status | What would resolve it |
|---|-----------|-------------|--------|----------------------|
| 1 | [[HallMudawar2000_subcooled_CHF]] (line 97) | Verify whether Hall & Mudawar inlet-conditions CHF correlation with D_h substitution predicts Qu & Mudawar microchannel conditions within acceptable error | Open | Qu & Mudawar 2003 does not report CHF data (tests terminated at x_e ≈ 0.2). May require a separate rectangular-channel CHF dataset, or the Kim & Mudawar 2013 review may address this |
| 2 | [[QuMudawar2003_microchannel_boiling_I]] (line 68) | Extract thermocouple axial coordinates z_tc1–z_tc4 from Fig. 2 schematic | Open | Read Fig. 2 from the PDF (image extraction), or check companion papers (B2, B3) for numerical values |
| 3 | [[QuMudawar2003_microchannel_boiling_I]] (line 73) | Determine total copper height below channels to heater surface (only H_w2 to TC plane is given) | Open | Read Fig. 3 cross-section from PDF, or check companion paper B2 (pressure drop) which may describe the full geometry |

## Open Questions (from wiki page content)

| # | Source page | Question | Context |
|---|-----------|----------|---------|
| 4 | [[motivation_for_CFD_approach]] | Does the Qu & Mudawar Part II annular flow model perform better than the 11 empirical correlations? | If yes, useful as 1D analytical baseline before CFD. Requires ingesting B3 |
| 5 | [[motivation_for_CFD_approach]] | Are newer correlations (e.g., Kim & Mudawar 2013) any better at capturing the decreasing-h_tp-with-quality trend? | Kim & Mudawar 2013 is on the priority ingest list |
| 6 | [[CHF_correlations]] | How much additional uncertainty does D → D_h substitution introduce for rectangular microchannels? | Cross-validation against rectangular channel CHF data needed |
| 7 | [[CHF_correlations]] | Does the Hall & Mudawar correlation remain accurate for dielectric fluids? | Water-only correlation; Phase 2 will need a separate CHF tool |
| 8 | [[RPI_wall_boiling_model]] | Can the monodispersed RPI model produce reliable results for microchannel geometries with bubble confinement? | Stage 2 validation (Qu & Mudawar) will answer this directly |
| 9 | [[RPI_wall_boiling_model]] | What N_ref value is appropriate for water at ~1 atm on a copper surface? | No direct data in current corpus. May need literature search or calibration during Stage 2 |

---

_Last lint pass: 2026-05-20. Next pass recommended after the next ingest._
