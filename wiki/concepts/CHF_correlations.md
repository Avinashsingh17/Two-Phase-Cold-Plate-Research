---
title: "Critical Heat Flux (CHF) Correlations"
type: concept
tags: [CHF, boiling, safety-margin, design-constraint]
---

## Definition

Critical heat flux (CHF) is the maximum heat flux at which the boiling heat transfer mechanism sustains efficient cooling. Beyond CHF, a vapor film blankets the heated surface, causing a sudden spike in surface temperature that can lead to burnout. CHF correlations predict this limit as a function of flow conditions, geometry, and fluid properties.

## Physical Description

In subcooled flow boiling, CHF occurs when bubble generation at the wall becomes vigorous enough that the liquid supply to the surface is disrupted. The dominant parameters are mass velocity (G), subcooling or quality (x), pressure (P), tube diameter (D), and heated length (L). CHF generally increases with G and subcooling, and decreases with increasing quality and L/D.

Two correlation types exist:
- **Inlet-conditions** correlations: CHF = f(D, L, G, P, x_i). Use upstream (independent) variables. Preferred for uniform heat flux.
- **Outlet-conditions** correlations: CHF = f(D, G, P, x_o). Use local (dependent) variables at the CHF location. Required for nonuniform heat flux profiles.

## Key Correlations and Models

| Correlation | Author(s) | Form | Applicability | Accuracy |
|-------------|-----------|------|---------------|----------|
| Inlet-conditions (recommended) | [Hall & Mudawar 2000] | Nondimensional, 5 constants, Bo = f(We_D, ρ_f/ρ_g, x_i', L/D) | Water, round tube, D = 0.25–15 mm, G = 300–30,000 kg/m²s, P = 1–200 bar | MAE 10.3%, RMS 14.3% (4860 pts) |

_This table will grow as additional CHF correlations are ingested (Bowring, Katto-Ohno, Mudawar inlet-condition variants, etc.)._

## Role in This Project

CHF defines the hard safety constraint in the cold plate optimization: operating heat flux must remain below q″_CHF / 1.5 (safety factor ≥ 1.5). The Hall & Mudawar inlet-conditions correlation is the primary tool for evaluating this constraint across the design space. It will be implemented in `src/two_phase_cp/correlations/` and used in both the 1D analytical model and as a post-processing check on CFD results.

## CHF Data Points from Experimental Papers

| Source | Fluid | Geometry | d_h (um) | G (kg/m^2 s) | CHF (W/cm^2) | x_out at CHF | Notes |
|--------|-------|----------|----------|-------------|--------------|--------------|-------|
| [Drummond 2018] | HFE-7100 | Manifold MMC, Si, 15 x 35 um | 19.6 | 1300–2900 | 68.5–142 | 0.18–0.28 | CHF reached |
| [Drummond 2018] | HFE-7100 | Manifold MMC, Si, 15 x 150 um | 28.8 | 1300–2900 | 411–705 | 0.18–0.28 | CHF reached |
| [Drummond 2018] | HFE-7100 | Manifold MMC, Si, 15 x 300 um | 31.7 | 1300–2900 | 761–910 | — | **No CHF** — terminated at T_chip safety limit |

## Open Questions

- How much additional uncertainty does the hydraulic-diameter substitution (D → D_h) introduce for rectangular microchannels? Needs cross-validation against rectangular channel data (see [[QuMudawar2003_microchannel_boiling_I]]).
- Does the correlation remain accurate for dielectric fluids (HFE-7100, Novec 649)? Hall & Mudawar is water-only; a separate CHF correlation or scaling law will be needed for Phase 2. Drummond 2018 provides CHF data points for HFE-7100 in manifold microchannels (see table above) but no correlation.
- Behavior near saturation (x_o > −0.05) is less reliable — relevant if cold plate channels approach saturated exit conditions.

## Cross-References

- [[HallMudawar2000_subcooled_CHF]]
- [[mudawar_group]]
- [[QuMudawar2003_microchannel_boiling_I]]
- [[Drummond2018_manifold_microchannel]]
- [[garimella_group]]