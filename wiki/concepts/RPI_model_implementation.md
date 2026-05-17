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
- IMECE 2024 ANSYS Fluent paper (pending ingest — may contain Fluent-specific guidance)
- Our own Phase 3 experience

## Cross-References

- [[RPI_wall_boiling_model]]
- [[KrepperRzehak2011_DEBORA]]
