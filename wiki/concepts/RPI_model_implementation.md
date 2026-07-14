---
title: "RPI Model Implementation — CFX vs. Fluent Translation"
type: concept
tags: [RPI, Fluent, CFX, implementation, UDF, setup]
---

## Definition

This page tracks the practical differences between ANSYS CFX and ANSYS Fluent implementations of the RPI wall boiling model, and serves as the master checklist for translating published CFX-based setups (primarily [[KrepperRzehak2011_DEBORA]]) into our Fluent workflow.

## Translation Checklist

_Status: sparse — to be populated during Phase 3 when Fluent is opened._

| Sub-model | CFX (Krepper & Rzehak) | Fluent status | UDF needed? | Notes |
|-----------|----------------------|---------------|-------------|-------|
| RPI heat flux partitioning | Built-in | TBD — verify available under Eulerian multiphase → wall boiling | Unlikely | |
| Tolubinsky-Kostanchuk d_W | Built-in, constants settable | TBD | TBD | Check if Fluent default is Tolubinsky or Unal |
| Lemmert-Chawla N | Built-in, N_ref settable | TBD | TBD | |
| Cole frequency | Built-in | TBD | TBD | |
| Tomiyama lift (full, with sign reversal) | Built-in | TBD | **Likely UDF** | Critical: must include Eo_⊥-dependent sign reversal per Eq. 26 in Krepper & Rzehak. If Fluent only provides constant-C_L lift, UDF is mandatory |
| Burns turbulent dispersion (Favre-averaged) | Built-in, C_TD settable | TBD | TBD | |
| Boiling wall function (Ramstorfer 2005) | Built-in | TBD | **Likely UDF** | Roughness analogy s ∝ N·d_W³; non-standard |
| Sato bubble-induced turbulence | Built-in, C_B = 0.6 | TBD | TBD | |
| Anglart bulk bubble size | Built-in | TBD | TBD | |

## Known Risk Items

1. **Tomiyama lift sign reversal.** If Fluent does not implement the full Tomiyama (2002) correlation — specifically the Eo_⊥-dependent branch that produces negative C_L for large deformed bubbles — a UDF is required. This is the mechanism responsible for the wall-peak → core-peak transition and for correct radial void fraction distribution.

2. **Boiling wall function.** The Ramstorfer et al. (2005) two-phase wall function is likely not available in Fluent out of the box. The standard single-phase wall function is a usable fallback (velocity profiles will be less accurate but void fraction and temperature are minimally affected per Krepper & Rzehak 2011 Section 7.1).

3. **y+ constraint.** The RPI model requires y+ ≥ 70 in the wall-adjacent cell. Meshes finer than this cause convergence failure because the model concentrates all vapor generation in one cell. This constrains near-wall mesh sizing.

## Resources to Populate This Page

- ANSYS Fluent Theory Guide: Multiphase → Eulerian Model → Wall Boiling
- ANSYS Fluent User's Guide: Setting Up Multiphase → Wall Boiling Model
- IMECE 2024 ANSYS Fluent paper — **ingested 2026-07-14; NOT an RPI source.**
  [[Viyyuri2024_fluent_microchannel_boiling]] turned out to use VOF and a
  semi-mechanistic boiling (SMB) model under the *mixture* multiphase framework —
  it contains **no** RPI heat-flux-partitioning / Euler-Euler content and does
  **not** populate this checklist. The CFX↔Fluent RPI correspondence therefore
  remains unsourced and must come from the Fluent Theory Guide RPI chapter + the
  GUI Boiling-tab default inventory checked against Krepper & Rzehak's reported
  closures (re-scoped validation-plan item 4). See [[open_questions]] #16. The D3
  page is retained for precedent / model-form value only (industry-source rule).
- Our own Phase 3 experience

## Cross-References

- [[RPI_wall_boiling_model]]
- [[KrepperRzehak2011_DEBORA]]
- [[Viyyuri2024_fluent_microchannel_boiling]] (precedent, **not** an RPI source)
