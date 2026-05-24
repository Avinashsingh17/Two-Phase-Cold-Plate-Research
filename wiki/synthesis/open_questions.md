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
| 5 | [[motivation_for_CFD_approach]] | Are newer correlations (e.g., Kim & Mudawar 2013) any better at capturing the decreasing-h_tp-with-quality trend? | **Resolved (2026-05-20):** No. Kim & Mudawar 2013 still predicts wrong trend for water microchannels. See [[KimMudawar2013_universal_boiling_II]] |
| 6 | [[CHF_correlations]] | How much additional uncertainty does D → D_h substitution introduce for rectangular microchannels? | Cross-validation against rectangular channel CHF data needed |
| 7 | [[CHF_correlations]] | Does the Hall & Mudawar correlation remain accurate for dielectric fluids? | Water-only correlation; Phase 2 will need a separate CHF tool |
| 8 | [[RPI_wall_boiling_model]] | Can the monodispersed RPI model produce reliable results for microchannel geometries with bubble confinement? | Stage 2 validation (Qu & Mudawar) will answer this directly |
| 9 | [[RPI_wall_boiling_model]] | What N_ref value is appropriate for water at ~1 atm on a copper surface? | No direct data in current corpus. May need literature search or calibration during Stage 2 |
| 10 | [[KimMudawar2013_universal_boiling_II]] | Does our cold plate design envelope cross into saturated operation (x_e > 0) where dryout incipience quality x_di becomes the binding thermal constraint instead of subcooled CHF? | x_di (saturated annular film dryout) and subcooled CHF (Hall & Mudawar) are different physical events in different regimes. Need to evaluate which constraint binds for our operating conditions. If x_e > 0 at channel exit, source Kim & Mudawar 2013 Part I for x_di correlation |

| 11 | [[Drummond2018_manifold_microchannel]] | In the low-quality regime (x_out < 0.1), HTC is roughly independent of channel cross-section for all three geometries tested. If HTC doesn't strongly depend on cross-section in the confined regime, the dominant design levers are (a) wall area per unit footprint via fin density/efficiency and (b) staying below dryout quality — not channel aspect ratio per se. Does this hold for water and for our cold plate scale? | May warrant a design-philosophy update: optimize fin density + dryout margin rather than aspect ratio. Verify with water microchannel data (Qu & Mudawar shows similar trend). |
| 12 | [[Drummond2018_manifold_microchannel]] | Identify HFE-7100 RPI closure source for Phase 2 optimization. Need nucleation site density (N_ref), bubble departure diameter, contact angle, and other closure parameters for HFE-7100 on silicon. | Garimella group (same lab as Drummond) has published HFE-7100 boiling work — targeted literature search likely turns up usable closures. This is the first project dependency where validation fluid ≠ optimization fluid has methodological consequences beyond property tables. |

## Methodological Note: Validation Fluid ≠ Optimization Fluid

The project's CFD validation pipeline uses water (Stage 2, Qu & Mudawar 2003) and R12 (Stage 1, Krepper & Rzehak 2011), but the optimization baseline target (Drummond 2018) uses HFE-7100. This is methodologically acceptable — the RPI framework and Eulerian solver are fluid-agnostic; only property tables and closure constants change. However, **closure recalibration for HFE-7100 is a separate workstream** that needs its own data source, not just a property table swap. This is distinct from prior fluid mismatches in the pipeline (R12 → water was a validation-stage concern handled by re-running Stage 2). The HFE-7100 gap requires identifying a boiling closure source with local measurements (void fraction, bubble parameters) for this specific fluid. Flag now so it doesn't surprise us — or a reviewer — later.

---

_Last lint pass: 2026-05-24. Next pass recommended after the next ingest._
