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
| 12 | [[Drummond2018_manifold_microchannel]] | HFE-7100 RPI closure source for Phase 2 optimization — **scoped, outcome (a) with significant caveats** | See detailed entry below |

## #12 Detail: HFE-7100 RPI Closure Source (Resolved to Scoped Workstream)

**Status:** Converted from "unknown gap" to "scoped task with known remediation path" (2026-05-24).

### Primary source — direct HFE-7100 closure measurements

**Al-Zaidi, Mahmoud, Ivanov & Karayiannis (2025)** — "Bubble nucleation site density, generation frequency and departure diameter in flow boiling of HFE-7100," *IJHMT* 242, 126830. Experimental measurements of all three key RPI closure parameters (N, D_d, f) for HFE-7100 flow boiling in a 1 mm microgap heat exchanger. Existing models compared — Hibiki-Ishii was best performer for N but still ~62% MAE. **New correlations proposed** for N, D_d, f based on the experimental data.

- Conditions: P = 1–2 bar, G = 100–200 kg/m²s, q″ up to 8.4 W/cm², inlet subcooling 5 K
- Key dependencies on operating conditions: N increases with q″ and P (weak G dependence); D_d increases with q″, decreases with G and P; f increases with q″, G, and P

**Critical caveat — extrapolation required.** Our target envelope is q″ = 200–500 W/cm² and Drummond's baseline operates at G = 1300–2900 kg/m²s. Al-Zaidi measured at q″ ≤ 8.4 W/cm² and G = 100–200 kg/m²s — a 24–60× gap in heat flux and an order of magnitude in mass flux. Since N, D_d, and f are all strongly heat-flux-dependent per Al-Zaidi's own findings, direct application of these correlations at our conditions is an extrapolation, not an interpolation. Al-Zaidi is the best available starting point, but closure setup is a workstream requiring explicit uncertainty bounds, not a plug-and-play operation.

### Companion reference — same group, microchannel geometry

**Al-Zaidi, Mahmoud & Karayiannis (2019)** — "Flow boiling of HFE-7100 in microchannels," *IJHMT* 140, 100–128. Flow boiling HTC data and correlation comparison for HFE-7100 in microchannels — closer to our geometry class than the 2025 microgap paper, even though it does not report N/D_d/f directly. Useful for verifying that the 2025 closure correlations produce reasonable HTC predictions in a microchannel geometry.

### Secondary source — HFE-7100 Eulerian CFD precedent

**Lioger-Arago, Coste & Caney (2022)** — "Experimental and Numerical Study of Boiling HFE-7100 in a Vertical Mini-channel," *JFFHMT* 9, 92–100. Eulerian multiphase with CHF wall-boiling model for HFE-7100, 1 mm × 30 mm × 120 mm rectangular channel, G = 140–648 kg/m²s, validated from onset of boiling to dryout. From CEA/Grenoble. Provides a worked CFD implementation precedent for the fluid. Specific closure constants to be verified at ingest time.

### Adjacent-fluid references (FC-72, Novec 649)

- **Bansode & Saini (2020)** — ASME InterPACK 2020. Eulerian + RPI in Fluent for FC-72 immersion cooling. Fluent built-in defaults (Lemmert-Chawla for N, Unal for D_d, Cole for f) gave acceptable results for FC-72. Useful as a "dielectric RPI is tractable in Fluent with default closures" precedent; specific constant values are not transferable to HFE-7100 without recalibration.
- **Nguyen (2015)** — Auburn MS thesis. Novec 649 **pool** boiling (not flow boiling) in Fluent. Tested 6 D_d × 12 N function combinations. Departure mechanics differ between pool (buoyancy-driven) and flow (drag-driven) boiling. Useful only as a "dielectric RPI is tractable in Fluent" precedent; not a closure source.

### HFE-7100 contact angle

HFE-7100 is nearly fully wetting on silicon and copper surfaces (σ = 11.11 mN/m at room temperature; static contact angle < 10° on most metal/silica surfaces, often effectively zero). Standard RPI contact angle closures assume moderate wetting. This requires explicit treatment in the closure setup — either a fixed near-zero contact angle or a modified nucleation model that accounts for the difficulty of vapor trapping in surface cavities for highly wetting fluids.

### Remediation path (Phase 2 closure setup workstream)

1. Start from Al-Zaidi et al. 2025 correlations for N, D_d, f as initial closure inputs
2. Verify functional forms against Al-Zaidi et al. 2019 microchannel HTC data for geometry-class consistency
3. Extrapolate to our operating envelope (200–500 W/cm², G = 1300–2900 kg/m²s) with explicit uncertainty bounds
4. Calibrate extrapolation against Drummond 2018 system-level data (R_eff, ΔT) as the high-flux/high-G anchor
5. Document contact-angle treatment (HFE-7100 nearly fully wetting; standard RPI assumes moderate wetting)
6. Sensitivity analysis on the extrapolation — quantify how much R_eff prediction changes with ±50% variation in N, D_d, f at our operating conditions

**Lioger-Arago et al. 2022** provides a worked Eulerian-CFD precedent for HFE-7100 in a vertical mini-channel (closure constants in that paper to be verified at ingest time). **Al-Zaidi et al. 2025** warrants full wiki ingest when Phase 2 closure setup begins.

## Methodological Note: Validation Fluid ≠ Optimization Fluid

The project's CFD validation pipeline uses water (Stage 2, Qu & Mudawar 2003) and R12 (Stage 1, Krepper & Rzehak 2011), but the optimization baseline target (Drummond 2018) uses HFE-7100. This is methodologically acceptable — the RPI framework and Eulerian solver are fluid-agnostic; only property tables and closure constants change. However, **closure recalibration for HFE-7100 is a separate workstream** that needs its own data source, not just a property table swap. This is distinct from prior fluid mismatches in the pipeline (R12 → water was a validation-stage concern handled by re-running Stage 2). The HFE-7100 gap requires identifying a boiling closure source with local measurements (void fraction, bubble parameters) for this specific fluid — now scoped via Al-Zaidi et al. 2025, with the critical caveat that a 24–60× heat flux extrapolation and order-of-magnitude mass flux extrapolation are required. Flag now so it doesn't surprise us — or a reviewer — later.

---

_Last lint pass: 2026-05-24. Next pass recommended after the next ingest._
