---
title: "Krepper & Rzehak 2011 — CFD for Subcooled Flow Boiling: Simulation of DEBORA Experiments"
type: paper
source: "E. Krepper, R. Rzehak, 'CFD for subcooled flow boiling: Simulation of DEBORA experiments,' Nuclear Engineering and Design, vol. 241, pp. 3851–3866, 2011."
date_ingested: 2026-05-08
tags: [RPI, wall-boiling, Euler-Euler, DEBORA, R12, CFD, validation, subcooled-boiling, closure-models]
---

## Summary

Systematic validation of the Euler/Euler two-phase framework with Kurul-Podowski (RPI) heat flux partitioning against the DEBORA subcooled flow boiling experiments (R12 refrigerant, 19.2 mm vertical pipe, 1.46–2.62 MPa). The paper catalogs every closure relation in the RPI model, recalibrates each from water/high-pressure conditions to R12, and identifies which parameters require per-experiment tuning vs. which transfer across cases at a given pressure. The result is the most complete published recipe for setting up an Euler/Euler wall boiling simulation, with clearly identified failure modes.

## Key Findings

- A single set of calibrated model parameters reproduces multiple DEBORA test cases at the same pressure level within ~20–30% for radial void fraction and velocity profiles, and with good accuracy for cross-sectionally averaged void fraction [Krepper & Rzehak 2011].
- **Nucleation site density N_ref is the dominant tuning knob** — strong influence on wall superheat, weak influence on void fraction. Calibrated against measured wall temperature profiles; a single N_ref per pressure level suffices [Krepper & Rzehak 2011].
- The model **cannot capture the wall-peak → core-peak transition** in void fraction as subcooling decreases (DEBORA 3→7), because the monodispersed bubble size assumption prevents size-dependent lift force reversal from transporting large bubbles to the pipe center [Krepper & Rzehak 2011].
- A two-phase boiling wall function (roughness analogy, s ∝ N·d_W³) significantly improves velocity profile predictions over the standard single-phase wall function [Krepper & Rzehak 2011].
- Reducing the turbulent dispersion force to 50% of its reference value improved the void fraction profile shape, suggesting the Burns et al. (2004) Favre-averaged formulation may overpredict dispersion [Krepper & Rzehak 2011].

## DEBORA Test Matrix

| Test | P (MPa) | G (kg/m²s) | q″_w (kW/m²) | T_in (°C) | x_out,eq | Role in our validation |
|------|---------|------------|---------------|-----------|----------|------------------------|
| DEBORA 1 | 2.62 | 1996 | 73.89 | 68.52 | 0.058 | Secondary — higher pressure, less data reuse in literature |
| DEBORA 2 | 2.62 | 1985 | 73.89 | 70.53 | 0.085 | Secondary |
| DEBORA 3 | 1.46 | 2028 | 76.2 | 28.52 | −0.028 | **PRIMARY** ★ (confirmed) |
| DEBORA 4 | 1.46 | 2030 | 76.24 | 31.16 | −0.007 | **SECONDARY** — transferability check, zero parameter changes (confirmed) |
| DEBORA 5 | 1.46 | 2028 | 76.19 | 35.60 | 0.032 | Diagnostic only — onset of core-peak transition |
| DEBORA 6 | 1.46 | 2023 | 76.26 | 39.67 | 0.069 | Diagnostic only — core-peak regime |
| DEBORA 7 | 1.46 | 2024 | 76.26 | 44.21 | 0.109 | Avoid — known model failure (core-peak) |

**★ CONFIRMED Stage 1 primary target: DEBORA 3.** Rationale: (1) cleanest wall-peaked void fraction profile — well within the regime where the monodispersed model works; (2) subcooled outlet (x_out = −0.028) avoids the wall-peak → core-peak transition that breaks the model at DEBORA 5–7; (3) most heavily subcooled of the 1.46 MPa series, giving the largest safety margin from the failure mode; (4) 1.46 MPa pressure level has better-separated density ratio (ρ_f/ρ_g = 13.9) and larger bubbles, providing more demanding validation than the 2.62 MPa cases.

After reproducing DEBORA 3, DEBORA 4 should be run with **zero parameter changes** to confirm transferability — this is the key test of whether the model generalizes within a pressure level.

## Nucleation Site Density Calibration

The nucleation site density N is parameterized as a power law of wall superheat [Lemmert & Chawla 1977]:

$$
N = N_\text{ref} \left(\frac{T_W - T_\text{sat}}{T_\text{ref}^N}\right)^p
$$

with p = 1.805 and T_ref^N = 10 K (standard). **N_ref is the only free parameter** and is calibrated by matching the axial wall superheat profile.

| Experiment set | P (MPa) | Calibrated N_ref (m⁻²) | Source |
|----------------|---------|------------------------|--------|
| Bartolomej & Chanturiya (water) | 4.7 | 0.8 × 10⁶ | [Krepper et al. 2007] |
| DEBORA 1–2 (R12) | 2.62 | 3.0 × 10⁷ | [Krepper & Rzehak 2011] |
| DEBORA 3–7 (R12) | 1.46 | 5.0 × 10⁶ | [Krepper & Rzehak 2011] |

**Why this matters for Phase 3:** N_ref varies by ~40× across these three cases. It cannot be predicted a priori — it depends on surface finish, fluid, and pressure. Our procedure will be: (1) run an initial simulation with a literature estimate of N_ref; (2) compare predicted wall superheat to data; (3) adjust N_ref to match. Wall superheat is the calibration target; void fraction and other quantities are then predictions (not fits). This single-knob calibration procedure is what makes the RPI model usable as a predictive tool rather than an N-parameter curve fit.

**Sensitivity:** N_ref has almost no influence on liquid temperature, small influence on void fraction, but **strong influence on wall superheat** (Fig. 4 in paper). Changing N_ref by an order of magnitude shifts wall superheat by ~5–10 K.

## Model Setup Recipe

| Sub-model | Krepper & Rzehak choice | Calibrated constants | Sensitivity / criticality | Fluent equivalent (TBD) |
|-----------|------------------------|---------------------|--------------------------|------------------------|
| **Heat flux partitioning** | Kurul & Podowski (1990, 1991). Q_tot = Q_C + Q_Q + Q_E | — (framework, not tunable) | HIGH — defines the entire wall boiling structure | RPI wall boiling model (TBD: verify available in Fluent multiphase) |
| **Single-phase convection (Q_C)** | Kader (1981) temperature wall function. Q_C = (1−A_W)·h_C·(T_W−T_L) | Standard wall function constants | LOW | TBD |
| **Quenching heat flux (Q_Q)** | Mikic & Rohsenow (1969) transient conduction. h_Q = (2/√π)·√(f·t_wait·k_L·ρ_L·C_pL) | t_wait = 0.8/f (Kurul & Podowski) | LOW — quenching is minor contributor for DEBORA conditions (inferred) | TBD |
| **Evaporation heat flux (Q_E)** | Q_E = ṁ_W · H_LG; ṁ_W = (ρ_G·π/6)·d_W³·f·N | Computed from d_W, f, N closures below | HIGH — couples three sub-models | TBD |
| **Bubble detachment diameter (d_W)** | Tolubinsky & Kostanchuk (1970). d_W = d_ref · exp(−(T_sat−T_L)/T_ref^d) | P = 2.62 MPa: d_ref = 0.24 mm, T_ref^d = 45 K. P = 1.46 MPa: d_ref = 0.35 mm, T_ref^d = 45 K | MEDIUM — calibrated per pressure; feeds into evaporation mass flux and bubble forces | TBD — Fluent default may use Tolubinsky or Unal; check which and whether constants are user-settable |
| **Nucleation site density (N)** | Lemmert & Chawla (1977). N = N_ref·((T_W−T_sat)/T_ref^N)^p | p = 1.805, T_ref^N = 10 K. N_ref: see calibration section above | **HIGH — primary tuning knob** | TBD |
| **Bubble detachment frequency (f)** | Cole (1960). f = √(4g(ρ_L−ρ_G)/(3·C_D·d_W·ρ_L)) | Standard; depends on d_W | LOW (inferred) | TBD |
| **Bubble influence factor (a)** | Kurul & Podowski (1990). A_W = π·(a·d_W/2)²·N, capped at A_W < 1 | a = 2 (standard) | LOW — limited experimental basis but standard value used universally (inferred) | TBD |
| **Bulk bubble diameter (d_B)** | Linear interpolation in subcooling (Anglart et al. 1997). d_B = f(T_sub) between (d_B1, T_sub1) and (d_B2, T_sub2) | P = 2.62 MPa: d_B1 = 0.035 mm, d_B2 = 0.7 mm. P = 1.46 MPa: d_B1 = 0.066 mm, d_B2 = 1.2 mm. Subcooling bounds: T_sub1 = −13.5 K, T_sub2 = 5 K | MEDIUM — affects interfacial area density for bulk condensation; calibrated per pressure | TBD — Fluent may use Anglart or other; check |
| **Bulk condensation/evaporation** | Ranz & Marshall (1952) interfacial HTC. Nu = 2 + 0.6·Re^0.5·Pr^(1/3). A_I = 6·α_G/d_B | Standard | LOW (inferred) | TBD |
| **Turbulence model** | SST (Menter 1994) — k-ω near walls, k-ε far field | Standard SST constants | LOW — standard choice | SST k-ω (available) |
| **Bubble-induced turbulence** | Sato et al. (1981). μ_bub = C_B·ρ_L·α_G·d_B·\|u_G−u_L\| | C_B = 0.6 | LOW (inferred) | TBD — Fluent has Sato model; verify C_B settable |
| **Drag** | Ishii & Zuber (1979). C_D = (24/Re)·(1+0.1·Re^0.75) | Standard | LOW | Ishii-Zuber (likely available) |
| **Lift** | Tomiyama et al. (2002) with **sign reversal**. C_L > 0 for small bubbles (toward wall), C_L < 0 for large bubbles (toward center). Reversal at d_B ≈ 1.5 mm for R12 at 1.46 MPa, ≈ 1.0 mm at 2.62 MPa | C_L = f(Re, Eo_⊥) per Eq. 26. Eo_⊥ uses d_⊥ from Wellek et al. (1966) aspect ratio correlation | **WATCHOUT — sign convention varies between codes.** The sign reversal is physical (large deformed bubbles migrate to pipe center) and is the mechanism that drives wall-peak → core-peak transition. If Fluent's Tomiyama lift model does not include the sign reversal branch, a UDF is required. | TBD — **verify Fluent implements the full Tomiyama (2002) correlation including Eo_⊥-dependent sign reversal, not just the positive-C_L branch** |
| **Turbulent dispersion** | Burns et al. (2004) Favre-averaged drag. F_disp ∝ C_TD · ∇α_G | C_TD = 0.9 (but 50% reduction improved results — see Limitations) | MEDIUM — overprediction suspected; may need reduction (inferred) | TBD — Fluent has Burns/FAD model; check C_TD settable |
| **Wall function** | Two-phase boiling wall function (Ramstorfer et al. 2005). Roughness analogy: s ∝ N·d_W³. B* = 8.5 (fully rough limit). Proportionality constant = 1 | See above | MEDIUM — significantly improves velocity profiles; standard single-phase wall function usable as fallback | TBD — **likely requires UDF in Fluent; this is a non-standard wall function** |

## Model Limitations

**1. Wall-peak → core-peak transition (critical failure mode).** As inlet subcooling decreases (DEBORA 3 → 7), the measured void fraction profile transitions from wall-peaked to core-peaked. The model cannot reproduce this. Root cause: the monodispersed bubble size assumption assigns all bubbles the same diameter and the same lift force direction. In reality, larger bubbles (Eo_⊥ > 4) experience negative lift and migrate to the pipe center, while smaller bubbles remain near the wall. **Fix requires a polydispersed population balance model** that tracks bubble size classes with size-dependent velocities and forces, plus explicit coalescence/fragmentation models. This is a known open research problem.

**Implication for our work:** We must select validation cases that remain in the wall-peaked regime (DEBORA 3, 4). If our cold plate channels operate near saturated exit conditions (x_out approaching 0), we are near or inside this failure mode. This limitation must be disclosed in the paper's methods section.

**2. Bubble size near the wall.** The linear subcooling-based bulk bubble model (Anglart et al. 1997) matches the pipe center but underpredicts bubble size near the wall. The growing near-wall bubbles are likely controlled by coalescence, which is not modeled. Imposing measured bubble size profiles as boundary conditions showed negligible effect on void fraction and velocity — suggesting bubble size errors are not the root cause of void fraction discrepancies.

**3. Velocity profiles.** Calculated velocity profiles are too flat: overestimated near the wall, underestimated in the center. The boiling wall function (Ramstorfer et al. 2005) significantly improves this but does not fully resolve it. Full resolution likely requires two-phase k-ε/k-ω source terms beyond the Sato additive viscosity model.

**4. Turbulent dispersion force magnitude.** The Burns et al. (2004) Favre-averaged formulation with C_TD = 0.9 may overpredict radial dispersion. Reducing to 50% improved void fraction profile shape for DEBORA 2, suggesting this coefficient needs re-examination.

## Applicability to This Project

**This is our Stage 1 validation benchmark** (per CLAUDE.md validation registry). DEBORA 3 is the recommended primary target case: subcooled R12 in a vertical pipe, wall-peaked void fraction, rich radial profile data for void fraction, velocity, temperature, and bubble size. The purpose is to prove we can set up and run the RPI wall boiling model correctly before moving to the Stage 2 cold plate geometry (Qu & Mudawar 2003).

**Fluid mismatch: R12 vs. water.** The DEBORA tests use R12, not water. However, the dimensionless groups (Re, density ratio, We, Bo) at DEBORA conditions overlap with water at PWR-typical pressures (Table 2 in paper). For our cold plate (water at ~1 atm), the Jakob number is ~30× higher than DEBORA, meaning bubble dynamics will differ significantly. The Stage 1 validation proves the model framework works; Stage 2 re-validates with water in the actual geometry.

**Solver mismatch: CFX → Fluent.** Krepper & Rzehak used ANSYS CFX. Our project uses ANSYS Fluent. Both implement Euler/Euler + RPI wall boiling, but the specific sub-model options, default constants, and wall function implementations differ. See [[RPI_model_implementation]] for the translation checklist. Key risk items: (1) Tomiyama lift sign-reversal availability, (2) boiling wall function (likely UDF), (3) nucleation site density and bubble detachment diameter parameterizations.

**Geometry mismatch: 19.2 mm pipe vs. microchannels.** The DEBORA pipe is ~40× larger than our cold plate channels (D_h ~ 0.5 mm). This is intentional for Stage 1 — we validate the model physics in a well-instrumented geometry before transferring to an uninstrumented microchannel.

## Cross-References

- [[RPI_wall_boiling_model]]
- [[RPI_model_implementation]]
- [[CHF_correlations]]
- [[HallMudawar2000_subcooled_CHF]]
- [[QuMudawar2003_microchannel_boiling_I]]

### Concepts

- [[two_phase_fundamentals]]

## Notes

- The original RPI model source is Kurul & Podowski (1990, 1991) — on reading list as low-priority background for paper drafting. Not a Phase 3 prerequisite.
- Bartolomej & Chanturiya (1967) is cited as the prior water-based validation for this model framework. Cross-sectional averaged void fraction data only (no radial profiles). Not ingested but referenced.
- Grid resolution: simulations used y+ ≈ 200; grid independence held down to y+ ≈ 70; below y+ ≈ 70, convergence failed due to the Kurul-Podowski model's assumption that all vapor generation occurs in the wall-adjacent cell. This y+ constraint is a practical setup requirement.
- The paper does not report CHF predictions — the model operates well below CHF. CHF safety margins must be evaluated separately using correlations (see [[HallMudawar2000_subcooled_CHF]]).
