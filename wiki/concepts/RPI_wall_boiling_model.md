---
title: "RPI Wall Boiling Model (Heat Flux Partitioning)"
type: concept
tags: [RPI, wall-boiling, Euler-Euler, subcooled-boiling, closure-models, CFD]
---

## Definition

The RPI (Rensselaer Polytechnic Institute) wall boiling model is a heat flux partitioning framework for CFD simulation of subcooled flow boiling. It decomposes the total wall heat flux into three components — single-phase convection, quenching (transient conduction), and evaporation — and uses empirical closure relations to compute each as a function of wall temperature and local flow conditions.

## Physical Description

In subcooled flow boiling, the heated wall surface is partially covered by growing vapor bubbles and partially wetted by liquid. The RPI model partitions the wall heat flux as:

**Q_tot = Q_C + Q_Q + Q_E**

- **Q_C (convection):** Single-phase turbulent heat transfer on the bubble-free wall fraction (1 − A_W). Uses standard wall functions (e.g., Kader 1981).
- **Q_Q (quenching):** Transient conduction to cold liquid that rushes in after a bubble departs. Modeled via Mikic & Rohsenow (1969) analytical solution. Acts on the bubble-influenced wall fraction A_W.
- **Q_E (evaporation):** Latent heat carried away by departing bubbles. Computed from bubble departure diameter d_W, frequency f, and nucleation site density N.

Given Q_tot as a boundary condition, the model iteratively solves for T_W that satisfies the partition. The closure relations for d_W, f, N, and A_W are the heart of the model and the primary source of uncertainty.

### Closure Relations Catalog

| Closure | Common choices | Role |
|---------|---------------|------|
| Bubble detachment diameter d_W | Tolubinsky & Kostanchuk (1970), Unal (1976) | Sets evaporation mass flux and bubble forces |
| Nucleation site density N | Lemmert & Chawla (1977) power law | **Primary tuning knob** — calibrated against wall superheat |
| Bubble detachment frequency f | Cole (1960) | Couples with d_W for evaporation rate |
| Bubble influence factor a | Kurul & Podowski (1990): a = 2 | Sets A_W = π(a·d_W/2)²·N |
| Quenching HTC h_Q | Mikic & Rohsenow (1969) with t_wait = 0.8/f | Transient conduction model |
| Bulk bubble diameter d_B | Anglart et al. (1997) linear interpolation in subcooling | Sets interfacial area for bulk condensation |
| Interfacial heat transfer | Ranz & Marshall (1952) | Drives bulk condensation/evaporation |

See [[KrepperRzehak2011_DEBORA]] for a complete calibration of all closures against the DEBORA R12 experiments, including per-pressure constant values.

## Assumptions and Limitations

1. **Monodispersed bubble population.** All bubbles at a given location have the same diameter. Cannot capture polydisperse effects like size-dependent lift force reversal (wall-peak → core-peak transition). Polydisperse population balance extensions exist but are significantly more complex [Krepper & Rzehak 2011].

2. **All vapor generated in wall-adjacent cell.** The Kurul-Podowski formulation generates all vapor mass in the first cell off the wall. This creates a mesh sensitivity: y+ must remain above ~70 for convergence [Krepper & Rzehak 2011]. Excessively fine near-wall meshes cause divergence.

3. **Nucleation site density is surface-dependent.** N_ref varies by orders of magnitude across surface finishes and cannot be predicted a priori. Must be calibrated against wall temperature data for each new surface/fluid/pressure combination.

4. **Sub-CHF only.** The model assumes liquid supply to nucleation sites is maintained. It does not predict CHF or post-CHF behavior. CHF margins must be evaluated separately (see [[CHF_correlations]]).

5. **Bubble influence factor poorly constrained.** The value a = 2 comes from a single rough experiment (Han & Griffith 1965). No systematic validation exists.

## Role in This Project

The RPI model is the primary CFD approach for Phase 3 validation and Phase 4 parametric study. It will be implemented in ANSYS Fluent within the Euler/Euler multiphase framework. The Stage 1 validation target is DEBORA 3 (R12, vertical pipe) to prove the model setup; Stage 2 transitions to Qu & Mudawar 2003 (water, rectangular microchannels).

For implementation details and CFX-vs-Fluent translation, see [[RPI_model_implementation]].

## Open Questions

- Can the monodispersed model produce reliable results for microchannel geometries where bubble confinement may force different size distributions?
- What N_ref value is appropriate for water at ~1 atm on a copper surface? No direct data in the ingested literature yet.
- Is the Anglart (1997) bulk bubble size parameterization valid for microchannels, or does confinement invalidate the linear subcooling assumption?
- Kurul & Podowski (1990, 1991) — the original RPI source — is on the reading list as low-priority background, ahead of paper drafting. Not a Phase 3 prerequisite; Krepper & Rzehak 2011 documents the model thoroughly enough to set up the validation case.

## Cross-References

- [[KrepperRzehak2011_DEBORA]]
- [[RPI_model_implementation]]
- [[CHF_correlations]]
- [[QuMudawar2003_microchannel_boiling_I]]
- [[two_phase_fundamentals]]
