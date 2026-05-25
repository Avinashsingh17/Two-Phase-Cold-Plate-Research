---
title: "Ozguc, Pan & Weibel 2024 — Topology Optimization of Heat Sinks for Two-Phase Flow Boiling (Parts 1 & 2)"
type: paper
source:
  - "S. Ozguc, L. Pan, J.A. Weibel, An approach for topology optimization of heat sinks for two-phase flow boiling: Part 1 — Model formulation and numerical implementation, Applied Thermal Engineering 249 (2024) 123337"
  - "S. Ozguc, L. Pan, J.A. Weibel, An approach for topology optimization of heat sinks for two-phase flow boiling: Part 2 — Model calibration and experimental validation, Applied Thermal Engineering 249 (2024) 123338"
date_ingested: 2026-05-24
tags: [topology-optimization, two-phase, mixture-model, HFE-7100, Pareto, additive-manufacturing, DMLS, homogenization, north-star-methodology]
---

## Summary

This two-part study is the **first topology optimization (TO) framework for two-phase flow boiling** heat sinks. Part 1 develops the algorithm: a homogenization-based TO approach coupled with a two-phase mixture model, using predefined square pin-fin microstructures so that empirical friction and HTC correlations always exist for the evolving geometry. Part 2 closes the loop: 14 free coefficients in the flow boiling correlations are experimentally calibrated against 214 DMLS pin-fin flow boiling tests with HFE-7100, and six Pareto-optimal TO designs are additively manufactured and tested — the experimental Pareto front closely overlaps the model-predicted front. This is the north star for our optimization methodology: the discipline of calibrating the underlying model against experiment and then validating that Pareto claims survive fabrication and testing.

## Key Findings

- **Two-phase TO beats single-phase TO by 39%** in thermal resistance at Q_in = 30 W (unconstrained, χ_max = 1.0). With a dryout-avoidance constraint of χ_max = 0.2, still 21% better than single-phase [Ozguc 2024 Part 1].
- **Optimal designs are heat-load-dependent** under two-phase operation. Higher heat loads produce thinner fins and larger flow channels to increase mass flow and heat capacity. Single-phase TO designs are load-independent. This is a fundamental difference introduced by the nonlinear, quality-dependent nature of two-phase transport [Ozguc 2024 Part 1].
- **The optimizer naturally generates manifold-like architectures**: large open channels at inlet/outlet acting as low-resistance distributors, with tightly packed pin fins in the heated region [Ozguc 2024 Part 1]. This emergent topology independently validates the manifold architecture adopted from [[Drummond2018_manifold_microchannel]].
- **14 model coefficients calibrated** (C₁–C₁₄) via gradient-based optimization against 214 experiments. Calibration reduced the average prediction error by 94% [Ozguc 2024 Part 2].
- **Post-calibration model accuracy:** ΔP MAE 45%, temperature rise MAE 21%. The model captures dryout onset and the sharp thermal resistance increase that follows [Ozguc 2024 Part 2].
- **Pareto optimality experimentally validated:** Six TO designs spanning the ΔP–R tradeoff, fabricated in DMLS AlSi10Mg, tested at Q_in ≈ 58.7 W, ṁ ≈ 1.28 g/s, T_in ≈ 59.6°C. Experimental measurements closely overlap the model-predicted Pareto front [Ozguc 2024 Part 2].
- **Non-uniform heating case:** 70 × 60 mm design space, two heated regions + hotspot (total 84.35 W), 1 kPa total pressure inlet (pump curve BC). TO achieved 53% lower thermal resistance than uniform pin-fin initialization. The optimizer intelligently routes coolant to avoid local dryout at hotspots without an explicit dryout constraint — the calibrated model captures dryout performance degradation directly [Ozguc 2024 Part 2].

## Design Space and Setup (Part 1)

| Parameter | Value |
|-----------|-------|
| Design space | 24 × 16 mm² (Part 1); 12 × 12 mm² heated region |
| Material | AlSi10Mg (k_s = 110 W/m·K in Part 1; 130 W/m·K in Part 2) |
| Fluid | HFE-7100 at saturation (T_in = T_sat) |
| Channel height H_t | 1 mm (Part 1); 2 mm (Part 2) |
| Base height H_b | 1 mm (Part 1); 3 mm (Part 2) |
| Total heat sink thickness | 2 mm (Part 1); 5 mm (Part 2) |
| Inlet BC | 5 kPa total gauge pressure (Part 1); velocity inlet (Part 2 calibration) |
| Outlet BC | 0 kPa gauge pressure |
| Grid size Δx | 0.5 mm (selected from convergence study: 0.25–2.0 mm) |
| Microstructure | Square pin fins; ε = w_c / Δx (0 = solid, 1 = open) |
| Manufacturing | DMLS; min pin fin thickness ≈ 0.25 mm (ε < 0.5) |
| Design initialization | ε₀ = 0.25 (uniform) |
| Convergence | 150–200 fixed iterations |

## Two-Phase Flow Model

### Mixture model approach

The flow model uses a **homogeneous two-phase mixture model** (single set of continuity, momentum, energy equations) — not an Eulerian two-fluid or RPI framework. Key simplifying assumptions [Ozguc 2024 Part 1]:

- Laminar, steady flow
- Homogeneous (liquid and vapor at same velocity)
- Properties evaluated at saturation temperature
- Fully developed flow in channels; separation of variables reduces 3D → 2D
- Solid temperature profiles 1D along base and fin heights

### Governing equations (Part 1 form)

| Equation | Expression | Notes |
|----------|------------|-------|
| Continuity | ∇·(v̄_m ρ_m) = 0 | Eq. 6 |
| Momentum | ρ_m v̄_m·∇v̄_m = −∇P + ∇·(τ̄) − S_M | S_M = frictional losses via Darcy permeability (Eq. 13–16) |
| Energy (flow) | ∇·(v̄_m ρ_m h_m) = S_E / (H_t Δx²) | S_E = convective coupling to base (Eq. 17) |
| Energy (base) | −∇·(k_s ∇T_b) = q̇ − S_E / (H_t Δx²) | Eq. 9; heat spreading in solid base |
| Quality | χ = (h_m − c_f T_sat) / h_fg | Eq. 10 |
| Mixture density | ρ_m = 1 / ((1−χ)/ρ_f + χ/ρ_g) | Eq. 11 |
| Mixture viscosity | μ_m = (C₇ χ μ_f + (1−C₇)(1−χ) μ_g) / (C₇ χ + (1−C₇)(1−χ)) | Eq. 11 Part 2; C₇ calibrated |

### Heat transfer coefficient — Bertsch et al. 2009 form

The HTC correlation adopts the **functional form** of Bertsch et al. 2009 [38 in Part 2], a composite correlation for saturated flow boiling in small channels. However, all constants are replaced by free coefficients C₈–C₁₄ for calibration [Ozguc 2024 Part 2]:

| Component | Expression | Ref |
|-----------|------------|-----|
| Total HTC | h = h_nb(1−χ) + h_tp [1 + C₈(χ² − χ^β) e^{−C₉ Co}] | Eq. 14 (Part 2) |
| Nucleate boiling | h_nb = C₁₀ (P/P_cr)^{0.12} · (−log(P/P_cr))^{−0.55} · M^{−0.5} · [h(T_w − T_f)]^{C₁₁} | Eq. 15 (Part 2); Cooper pool boiling form |
| Two-phase convective | h_tp = (1−χ) h_f + χ h_g | Eq. 16 (Part 2) |
| Single-phase (liq/vap) | h_{f/g} = C₁₂ · k_{f/g} / (2 Δx ε^{C₁₃} (1−ε)^{C₁₄}) | Eq. 17 (Part 2); Nusselt-form |
| Confinement number | Co = [g(ρ_f − ρ_g) D_h² / σ]^{−0.5} | Eq. 24 (Part 1) |

### Friction factor and permeability

Frictional losses via Darcy law (K₁ for fin sidewalls, K₂ for top/bottom channel surfaces), with free coefficients C₁–C₆ replacing the standard Darcy/Ergun constants [Ozguc 2024 Part 2, Eq. 8–9].

### Cost function

| Component | Expression | Notes |
|-----------|------------|-------|
| Thermal resistance | R = [1/n Σ(T_{b,i} − T_in)^m]^{1/m} / Q_in | Eq. 3 (Part 1); m = 10 weights hotspots |
| Cost (Part 1) | f_cost = R/R̄ + g_p(χ) | Single-objective + exterior penalty for χ_max |
| Cost (Part 2) | f_cost = α ΔP/P̄ + (1−α) R/R̄ | Multi-objective with weighting coefficient α |
| Dryout penalty (Part 1) | g_p(χ) = (P/n) Σ max(0, χ_i − χ_max)² | Eq. 5; P initialized at 10⁻⁷–10⁻⁶, multiplied ×10 every 50 iterations |

## Calibration Results (Part 2, Table 1)

| Coefficient | Initial | Final | Controls |
|-------------|---------|-------|----------|
| C₁ | 24.00 | 23.69 | Fin sidewall permeability |
| C₂ | 3.00 | 1.80 | Fin sidewall permeability exponent |
| C₃ | 0 | 0.06 | Fin sidewall permeability exponent |
| C₄ | 0.0063 | 0.0064 | Top/bottom permeability |
| C₅ | 3.00 | 2.99 | Top/bottom permeability exponent |
| C₆ | 0 | 0.13 | Top/bottom permeability exponent |
| C₇ | 0.50 | 0.97 | Mixture viscosity weighting |
| C₈ | 80 | 0 | Convection enhancement with quality |
| C₉ | 0.6 | — | Confinement number coefficient (C₈ = 0 → C₉ has no effect) |
| C₁₀ | 2.02 | 4.07 | Nucleate boiling magnitude |
| C₁₁ | 0.67 | 0.58 | Nucleate boiling wall-superheat exponent |
| C₁₂ | 7.54 | 12.03 | Single-phase convective Nusselt |
| C₁₃ | 1 | 0.42 | Nusselt ε-exponent |
| C₁₄ | 0 | −0.07 | Nusselt (1−ε)-exponent |

**Notable:** C₈ converges to 0, eliminating the quality-dependent convection enhancement term entirely. Post-calibration, the HTC is purely nucleate-boiling-dominant (h_nb) plus geometry-weighted single-phase convection (h_tp) — the Bertsch convection-enhancement term does not survive calibration for this geometry/fluid combination.

## Data Available for Validation

| Data type | Source | Conditions |
|-----------|--------|------------|
| Calibration ΔP, T₁–T₃, χ_exit | Part 2, Table S2 (Supplemental) | 8 uniform pin-fin samples (t_f = 0.25–0.45 mm), ṁ = 0.25–5.37 g/s, Q_in = 0–94.5 W |
| Model vs experiment (calibration) | Part 2, Fig. 8 (sample 8), Fig. 9 (all 8 samples) | ΔP parity ±25%, temperature parity ±25% |
| Pareto front (ΔP vs R_TC) | Part 2, Fig. 11a | 6 TO designs + 6 experimental measurements at Q_in ≈ 58.7 W, ṁ ≈ 1.28 g/s |
| TO design maps (ε, velocity, χ, T) | Part 1, Fig. 3, 5; Part 2, Fig. 10c, 11b, 12c | Various Q_in and χ_max values |
| Grid convergence | Part 1, Fig. 4a | R vs Δx (0.25–2.0 mm) |
| R vs Q_in at different χ_max | Part 1, Fig. 5a | Q_in = 10–50 W, χ_max = 0.2, 0.6, 1.0 |

## Applicability to This Project

### Dominant methodological caveat: Bertsch correlation dependence

The entire TO framework rests on the Bertsch et al. 2009 composite HTC correlation — or more precisely, a re-parameterized version of it with 14 experimentally fitted coefficients (C₁–C₁₄). This is the same class of small-channel superposition correlation that Qu & Mudawar 2003 and Kim & Mudawar 2013 have established gets the **qualitative trend wrong** for water microchannel boiling (see [[motivation_for_CFD_approach]]). The Pareto optimality claims in Part 1 are therefore measured in the model's own currency — they are only as credible as the underlying HTC correlation.

**What redeems this** is Part 2's experimental calibration loop. By fitting all 14 coefficients against 214 flow boiling experiments on their specific geometry class (DMLS AlSi10Mg square pin fins) and fluid (HFE-7100), Ozguc et al. convert a generic correlation with known failure modes into a locally calibrated surrogate. The subsequent Pareto validation (6 designs manufactured and tested, experimental front overlaps predicted front) confirms that the calibrated model produces genuinely Pareto-optimal designs for this geometry/fluid/operating envelope — not just model-optimal ones.

**Implication for our project:** The Ozguc workflow is the methodological template for Phase 5 (optimization). But their model is deliberately simplified for TO tractability (mixture model, homogeneous flow, laminar, 2D). It is **complementary to our Eulerian/RPI framework in fidelity, not redundant**. We inherit the discipline (calibrate → optimize → fabricate → validate Pareto claims), not the physics model. The Ozguc page should not be cited as a physics reference for boiling HTC or closure parameters.

### North star for optimization methodology

Ozguc Parts 1+2 establish the end-to-end workflow that our optimization phase should follow:

1. Define a physics-based model tractable enough for iterative optimization
2. Calibrate it experimentally over the relevant microstructure/fluid/operating envelope
3. Run the optimizer to generate Pareto-optimal designs
4. Fabricate and test designs to validate that Pareto optimality survives reality

We may replace their mixture model with our Eulerian/RPI, and their adjoint-based TO with Bayesian optimization — but the four-step discipline is the same.

### χ_max penalty as dryout constraint precedent

Part 1's exterior penalty function (Eq. 5) that constrains local vapor quality below χ_max is a **published precedent for encoding the dryout/CHF safety constraint inside the optimization objective**. This is directly relevant to Phase 5 of our project, where we need to ensure optimized designs stay below CHF with margin. Part 2 shows an alternative: with a well-calibrated model that captures the thermal resistance spike at dryout, the optimizer avoids dryout without an explicit penalty — the cost function itself penalizes dryout-degraded performance. Both approaches are available to us.

### Heat-load-dependent optimal designs

Part 1 shows that two-phase TO designs change with heat load — unlike single-phase designs, which are load-independent. This raises an unresolved question for our project: **should we optimize for a single operating point or across an envelope of heat loads?** See [[open_questions]] #13.

### Geometry/fluid alignment with baseline

| Parameter | Ozguc 2024 | Drummond 2018 | Our project |
|-----------|------------|---------------|-------------|
| Fluid | HFE-7100 | HFE-7100 | HFE-7100 (optimization) |
| Material | AlSi10Mg (DMLS) | Si (DRIE) | TBD (DMLS likely) |
| Channel type | Square pin fins (homogenization) | Rectangular parallel channels | TBD |
| Flow model | Mixture (homogeneous, laminar) | N/A (experimental) | Eulerian + RPI |
| Optimization method | Adjoint-based TO (gradient) | N/A | Bayesian (surrogate-based) |
| Validation | Self-calibrated + Pareto validation | N/A | Krepper & Rzehak → Qu & Mudawar pipeline |

Ozguc and Drummond are from the same group (Purdue CTRC/Weibel). Drummond is the performance baseline we aim to beat; Ozguc is the methodological template for how to conduct and validate the optimization.

## Cross-References

- [[Drummond2018_manifold_microchannel]]
- [[motivation_for_CFD_approach]]
- [[baseline_decision]]
- [[garimella_group]]
- [[CHF_correlations]]
- [[open_questions]]

## Notes

- Part 2 reference [38] is Bertsch, Groll & Garimella 2009 (same group) — the composite HTC correlation for saturated flow boiling in small channels. This is paper B3 in our `raw/papers/` folder. Not yet ingested as a standalone wiki page, but its functional form and limitations are documented above.
- The calibrated C₈ = 0 result (convection enhancement term eliminated) is noteworthy: it means that for HFE-7100 in DMLS pin fins, the Bertsch quality-dependent enhancement mechanism does not contribute. The HTC is nucleate-boiling-dominant. This is consistent with the low-quality regime behavior observed by [[Drummond2018_manifold_microchannel]] where HTC is roughly independent of channel cross-section.
- k_s differs between Part 1 (110 W/m·K, from EOS datasheet) and Part 2 (130 W/m·K, from Ref [41]). Part 2 value is used for all calibration and validation runs.
- Part 2 references Drummond 2018 as Ref [23], confirming both are from the same research program at Purdue CTRC.
