---
title: "Viyyuri 2024 — CFD Modeling of Flow Boiling in Microchannels (ANSYS Fluent: VOF & SMB-Mixture)"
type: paper
source: "Viyyuri, S. (2024). Computational Fluid Dynamics (CFD) Modeling of Flow Boiling Heat Transfer in Microchannels: Modeling Approaches Using ANSYS Fluent and Validation Studies. Proceedings of the ASME 2024 International Mechanical Engineering Congress and Exposition (IMECE), Nov 17–21 2024, Portland, OR. Paper IMECE2024-146631. ANSYS, Inc."
date_ingested: 2026-07-14
tags: [ANSYS-Fluent, VOF, semi-mechanistic-boiling, mixture-model, microchannel, flow-boiling, vendor-source, precedent]
---

## Nomenclature

This page is self-contained: every symbol, abbreviation, and named correlation
used below is defined here (and spelled out on first use in the text).

| Term | Meaning |
|------|---------|
| CFD | Computational fluid dynamics |
| VOF | Volume of Fluid — interface-resolving multiphase model; tracks the liquid–vapor interface via a volume-fraction field, no empirical boiling closures |
| SMB | Semi-mechanistic boiling — an empirical wall-boiling model combining nucleate-boiling and convective HTC correlations; run here under the mixture framework |
| Mixture model | Simplified multiphase model solving mixture continuity/momentum/energy with algebraic slip between phases (not two full phase sets) |
| Euler-Euler (E-E) | Two-fluid model solving separate continuity/momentum/energy for each phase; the framework RPI uses (contrast, not used in D3) |
| RPI | Rensselaer Polytechnic Institute wall-boiling model — heat-flux **partitioning** closure under Euler-Euler; **not used in D3** (see Applicability) |
| CSF | Continuum Surface Force — models surface tension as a body force at the interface (Brackbill et al. 1992) |
| Hertz-Knudsen | Kinetic-theory interfacial mass-transfer model for phase change (Schrage 1953); used for evaporation/condensation in the VOF path |
| Foster-Zuber | Nucleate pool-boiling HTC correlation; the nucleate term in the SMB path |
| Chen | Chen (1966) saturated flow-boiling correlation providing the convective-augmentation factor |
| Chen-Steiner | Boiling-suppression factor (Steiner et al. 2005) applied in the SMB path |
| PRESTO! | PREssure STaggering Option — Fluent face-pressure interpolation scheme |
| SIMPLEC | Semi-Implicit Method for Pressure-Linked Equations-Consistent — pressure–velocity coupling |
| ONB | Onset of nucleate boiling |
| CHF | Critical heat flux |
| HTC | Heat transfer coefficient |
| y⁺ | Non-dimensional wall distance of the first cell centroid |
| ΔT_sat | Wall superheat, T_wall − T_sat |
| T_sat | Saturation temperature |
| D_h | Hydraulic diameter |
| G | Mass flux (kg·m⁻²·s⁻¹) |
| AR | Aspect ratio (channel depth / width) |
| P_out | Outlet pressure |
| α | Volume fraction (VOF field: 0 = vapor, 1 = liquid) |

## Summary

Vendor (ANSYS) demonstration paper presenting **two ANSYS Fluent modeling paths
for microchannel flow boiling**: (1) a transient **Volume of Fluid (VOF)**
interface-resolving simulation with kinetic-theory (Hertz-Knudsen) phase change
and Continuum Surface Force (CSF) surface tension, and (2) a steady
**semi-mechanistic boiling (SMB)** model run under the **mixture** multiphase
framework, using empirical HTC correlations (Foster-Zuber nucleate + Chen
convective augmentation + Chen-Steiner suppression). The headline result is a
**~60× runtime advantage** for SMB (≈0.4 h on 4 cores) over VOF (≈24 h on 56
cores) at comparable heat-flux-vs-wall-superheat predictions. Two demonstration
cases are shown: water in a single microchannel, and R134a in a 17-channel cold
plate. **This is a precedent / model-form source, not validation evidence** —
see Applicability.

## Key Findings

- SMB-on-mixture reproduces the VOF and Bertsch-correlation wall-superheat trends
  at a fraction of the cost (~60× faster), making it a candidate fast screening
  path [Viyyuri 2024].
- VOF and correlation agree well at low heat flux (< 70 W/cm²); at high flux,
  bubble-confinement effects can push the two-phase regime outside the range of
  regime-independent correlations [Viyyuri 2024].
- SMB requires a **coarse** near-wall mesh (y⁺ > 5) and a modelled **solid zone**
  (heat-flux BCs are not allowed directly on fluid-adjacent walls); a finer mesh
  drives wall-superheat over-prediction [Viyyuri 2024].
- Case 2 pre-ONB: the single-phase heat-flux multiplier needs tuning (SMB
  under-predicts wall superheat before boiling onset); post-ONB agreement with
  experiment is good [Viyyuri 2024].

## Experimental / Computational Setup

Two demonstration cases. All geometry/property values transcribed for
Fluent-reproduction; computed or missing items flagged.

### Case 1 — Water, single microchannel (VOF + SMB)

| Parameter | Value |
|-----------|-------|
| Channel cross-section | 300 µm wide × 150 µm high, rectangular |
| Length | 0.5 mm adiabatic entrance + 4.5 mm heated |
| Hydraulic diameter D_h | 200 µm (computed 2WH/(W+H); **not stated in paper**) |
| Heated-wall configuration | Heated section 4.5 mm; "zero-thickness walls" — **which walls heated not explicitly stated** <!-- TODO: verify --> |
| Fluid | Water (liquid) / water vapor |
| Mass flux G | 500 kg/m²·s (inlet) |
| Outlet BC | Pressure outlet, 0 gauge (≈ saturation pressure) |
| T_sat | 100 °C |
| Mesh | 10 µm uniform (225,000 hex) and 5 µm near-wall refined (402,400); no result difference → 10 µm adequate (VOF) |

Fluid properties (D3 Table 1):

| Property | Water (liquid) | Vapor |
|----------|----------------|-------|
| Density (kg/m³) | 958.5 | 0.595 |
| Thermal conductivity (W/m·K) | 0.665 | 0.025 |
| Specific heat (J/kg·K) | 4217 | 2043 |
| Dynamic viscosity (Pa·s) | 2.82×10⁻⁴ | 1.23×10⁻⁵ |
| Surface tension (N/m) | 0.0589 | — |
| Latent heat (J/kmol) | 4.07×10⁷ | — |
| Wall contact angle (deg) | 140 | — |

### Case 2 — R134a, 17-channel cold plate (VOF single-channel + SMB single & full)

| Parameter | Value |
|-----------|-------|
| Number of channels | 17 |
| Hydraulic diameter D_h | 1089 µm |
| Channel depth | 1905 µm |
| Channel width | 762 µm |
| Fin width | 762 µm |
| Aspect ratio (depth/width) | 2.5 |
| Test-piece length | 9.53 mm (pre/post-evaporator 30.16 mm each, **not** in CFD) |
| Fluid | R134a |
| Operating pressure | 750 kPa |
| Mass flux G | 42 and 334 kg/m²·s |
| Heated-wall configuration | Bottom wall heat flux; other walls adiabatic |
| Mesh (VOF, single channel) | 20 µm fluid / 50 µm solid, ~508,000 hex |
| Mesh (SMB, single channel) | ~150 µm, ~11,000 cells (y⁺ > 5) |
| Mesh (SMB, full 17-channel) | ~150 µm, ~179,000 hex |

Fluid properties (D3 Table 3):

| Property | R134a (liquid) | R134a (vapor) |
|----------|----------------|----------------|
| Density (kg/m³) | 1191.2 | 36.5 |
| Thermal conductivity (W/m·K) | 0.0807 | 0.0149 |
| Specific heat (J/kg·K) | 1442 | 1058.6 |
| Dynamic viscosity (Pa·s) | 1.87×10⁻⁴ | 1.23×10⁻⁵ <!-- TODO: verify — printed identical to water-vapor value in Table 1; possible source transcription artifact --> |
| Surface tension (N/m) | 0.0083 | — |
| T_sat at 750 kPa (°C) | 29.03 | — |
| Latent heat (J/kmol) | 1.86×10⁷ | — |
| Wall contact angle (deg) | 90 | — |

### Solver settings (transferable, both cases)

- Transient laminar VOF: SIMPLEC pressure–velocity coupling; PRESTO! face
  pressure; second-order upwind on momentum/transport; compressive scheme
  (second-order reconstruction + slope limiters) at the interface.
- Steady SMB: coupled solver in pseudo-transient mode; PRESTO! + second-order
  schemes; secondary-phase (vapor) bubble diameter set to channel width (0.1 mm,
  Case 1); Chen convective augmentation with heat-flux multiplier = 5.
- Convergence: residuals below 1×10⁻³ (continuity), 1×10⁻⁶ (energy), 1×10⁻⁴
  (others); plus wall-superheat and inlet-pressure monitors.

## Models / Correlations Used

- **VOF path:** Hertz-Knudsen interfacial mass transfer (Eqs. 1–2, kinetic theory
  / Schrage 1953); CSF surface tension (Brackbill et al. 1992); wall adhesion via
  contact angle; compressive interface scheme.
- **SMB path (mixture framework):** Foster-Zuber nucleate-boiling HTC + Chen
  (1966) convective augmentation + Chen-Steiner (Steiner et al. 2005)
  suppression factor; semi-mechanistic wall-boiling formulation of Das & Punekar
  (2016). Liquid water/R134a = primary phase, vapor = secondary phase.

## Data Available for Validation

- **All comparison data are figure-only** (Figs. 5, 8, 16, 19 — heat flux vs.
  average wall superheat); the paper tabulates no profile data.
- Case 1 comparison is against the **Bertsch correlation**, not experiment.
- Case 2 has a **single experimental point** (transient VOF ΔT_sat 14.1 °C vs.
  14.3 °C measured; Table 4), plus figure comparisons vs. Bertsch et al. (2009)
  experimental data at two mass fluxes.
- **Not usable as validation evidence** for this project (see Applicability).

## Applicability to This Project

**(1) Value.** D3 is useful as **precedent and model-form reference**, not data:
- Demonstrates that ANSYS Fluent handles microchannel flow boiling end-to-end.
- Provides a concrete **SMB-on-mixture fast-path recipe** with a headline runtime
  contrast (VOF ≈24 h / 56 cores vs. SMB ≈0.4 h / 4 cores) — relevant to Phase-4
  screening pragmatics.
- Supplies a transferable **solver-settings reference** (SIMPLEC, PRESTO!, coupled
  pseudo-transient; y⁺ > 5 coarse mesh + solid zone required for SMB; convergence
  targets and monitors above).

**(2) Limits, stated explicitly.** D3 is **vendor-authored (ANSYS, Inc.)** and its
validation is thin: Case 1 is checked against the **Bertsch correlation, not
experiment**, and Case 2 is a **single-point** experimental comparison. Per the
CLAUDE.md industry-source rule, **D3 is cited for model-form / precedent only and
must never be used as validation evidence in the manuscript.**

**(3) Gate note — why D3 does NOT close pre-Fluent item 4.** D3 was originally
gated (phase2_validation_plan.md item 4, and literature_review.md) as the source
that would confirm **RPI wall-boiling sub-model correspondence between CFX**
(Krepper & Rzehak's solver) **and Fluent**. On reading, **it is not that**: D3's
fast path is a semi-mechanistic boiling model under the **mixture** framework
(empirical HTC superposition), and its detailed path is VOF — **neither exercises
RPI heat-flux partitioning under Euler-Euler.** The abstract's phrase "Eulerian
multiphase framework" is contradicted by the body (secs 2.1.1, 2.2.2; Fig. 6/15/17
captions; conclusion), which uniformly say *mixture*. D3 therefore contains **zero
RPI/Euler-Euler wall-boiling content** and does **not** close the correspondence
gate. That check **remains open** and is now sourced from the Fluent Theory Guide
RPI chapter + the GUI Boiling-tab default inventory vs. Krepper & Rzehak's reported
closures (re-scoped validation-plan item 4). See [[open_questions]] #16 and
[[RPI_model_implementation]].

## Cross-References

- [[semi_mechanistic_boiling_model]]
- [[RPI_model_implementation]]
- [[RPI_wall_boiling_model]]
- [[KrepperRzehak2011_DEBORA]]
- [[two_phase_fundamentals]]
- Bertsch, Groll & Garimella (2009), *Int. J. Heat Mass Transfer* 52(7–8),
  2110–2118 (external; D3's primary validation reference; corpus item B3, not yet
  ingested)

## Notes

- <!-- TODO: verify --> Case 1 heated-wall configuration and D_h are not stated in
  D3; D_h computed here. R134a vapor viscosity printed identical to the water-vapor
  value — possible source transcription artifact.
- Vendor-authored; precedent/model-form only, never validation evidence
  (CLAUDE.md industry-source rule).
