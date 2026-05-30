---
title: "Qu & Mudawar 2003 — Flow Boiling Heat Transfer in Micro-Channel Heat Sinks (Part I)"
type: paper
source: "W. Qu, I. Mudawar, 'Flow boiling heat transfer in two-phase micro-channel heat sinks — I. Experimental investigation and assessment of correlation methods,' International Journal of Heat and Mass Transfer, vol. 46, pp. 2755–2771, 2003."
date_ingested: 2026-05-20
tags: [microchannel, flow-boiling, water, HTC, annular-flow, correlation-assessment, validation, experimental]
---

## Summary

First comprehensive experimental study of saturated flow boiling heat transfer for water in a copper microchannel heat sink (21 parallel channels, 231 × 713 µm, D_h ≈ 349 µm). Demonstrates that the dominant heat transfer mechanism is forced convective boiling (annular flow), not nucleate boiling — a fundamental departure from both macro-channel behavior and refrigerant-based microchannel studies. Tests 11 existing correlations (6 macro-channel, 5 mini/micro-channel) against the data; none capture the correct trend of h_tp decreasing with increasing quality. This paper is the Stage 2 validation benchmark for this project.

## Key Findings

- **Forced convective boiling (annular flow) is the dominant mechanism** in water microchannels at moderate-to-high heat fluxes. h_tp is a strong function of mass velocity G and weak function of heat flux q″ — the signature of convective boiling, not nucleate boiling [Qu & Mudawar 2003].
- **h_tp decreases with increasing thermodynamic equilibrium quality x_e** — opposite to macro-channel trends. Attributed to appreciable liquid droplet entrainment at annular flow onset (near x_e = 0), followed by droplet deposition increasing the annular liquid film thickness downstream [Qu & Mudawar 2003]. This is unique to water microchannels.
- **All 11 existing correlations fail to predict the correct trend.** Six macro-channel correlations (Chen, Shah, Gungor-Winterton, Kandlikar, Liu-Winterton, Steiner-Taborek) predict h_tp *increasing* with x_e — the opposite of measured behavior. Five mini/micro-channel correlations fare no better at capturing the trend. Best MAE is 19.3% (Yu et al.) but even that correlation gets the trend wrong [Qu & Mudawar 2003]. **This result is load-bearing for our paper's motivation: if correlation-based design is fundamentally limited for water microchannels, CFD validation is the only credible path to design optimization.** See [[motivation_for_CFD_approach]].
- Abrupt transition to annular flow occurs near x_e = 0, with no sustained bubbly or slug flow regime at moderate-to-high heat fluxes [Qu & Mudawar 2003]. This contrasts with refrigerants (e.g., R-113, FC-84) where lower surface tension produces much smaller bubble departure diameters that sustain nucleate boiling over a larger quality range.
- Boiling number for the present study (Bo = 2.2 × 10⁻⁴ to 7.8 × 10⁻⁴) is significantly lower than studies that reported nucleate boiling dominance (Bo > 10⁻³) [Qu & Mudawar 2003].

## Publication Cluster

This paper is Part I of a 3-paper cluster published in the same volume of IJHMT (vol. 46, 2003). Treat as a unit for future ingest planning:

| Paper | Topic | File in raw/ | Ingested? |
|-------|-------|-------------|-----------|
| **Part I** (this page) | Experimental HTC data + correlation assessment | B1 | Yes |
| **Pressure drop companion** | Subcooled flow boiling pressure drop in same heat sink | B2 | No |
| **Part II** | Annular two-phase flow model for HTC prediction | B3 | No |

Cross-references: [[QuMudawar2003_pressure_drop]], [[QuMudawar2003_annular_model_II]]

## Heat Sink Geometry

This is the Stage 2 validation geometry. Dimensions must be reproduced exactly in Fluent. All values from Table 3 and Section 2.2 of [Qu & Mudawar 2003] unless noted.

### Unit cell dimensions (Table 3)

| Parameter | Symbol | Value | Notes |
|-----------|--------|-------|-------|
| Half-wall width | W_w | 118 µm | Half the copper wall between adjacent channels |
| Channel width | W_ch | 231 µm | |
| Unit cell width | W_cell | W_ch + 2·W_w = 467 µm | Symmetry model: one channel + one wall on each side |
| Lexan cover plate thickness | H_w1 | 12,700 µm (12.7 mm) | Polycarbonate; adiabatic top boundary |
| Channel depth | H_ch | 713 µm | Aspect ratio β = H_ch/W_ch ≈ 3.09 |
| Copper: channel bottom to TC plane | H_w2 | 2,462 µm | 1D conduction correction applied in data reduction (Eq. 7) |
| Hydraulic diameter | D_h | ~349 µm | D_h = 2·W_ch·H_ch / (W_ch + H_ch) |

### Heat sink planform and channel array

| Parameter | Value |
|-----------|-------|
| Heat sink material | Oxygen-free copper |
| Planform (top surface) | W = 1.0 cm × L = 4.48 cm |
| Top planform area (A_t) | 4.48 cm² |
| Number of channels | 21 parallel rectangular |
| Heating configuration | **Three-sided** — bottom + two side walls heated; top wall (Lexan) adiabatic |
| Heaters | 12 cartridge heaters inserted into holes drilled in bottom surface |
| Anti-conduction slots | 3 narrow deep slots cut from bottom surface upward to reduce axial conduction |

### Thermocouple instrumentation

| Parameter | Value |
|-----------|-------|
| Type | 4 × Type-K (tc1–tc4) |
| Placement | Along center plane of heat sink, stream-wise (tc1 = upstream, tc4 = downstream) |
| Depth | H_w2 = 2,462 µm below channel bottom wall |
| Axial coordinates (z_tc1–z_tc4) | **Not reported numerically** — shown only in Fig. 2 schematic. <!-- TODO: extract z_tc values from Fig. 2 or companion paper --> |
| Data reduction note | Only tc3 and tc4 reliably in the saturated region for most test conditions; tc1 and tc2 are mostly subcooled [Qu & Mudawar 2003] |

### Dimensions not explicitly reported (flag for Fluent setup)

- **Total copper height below channels to heater surface:** Only H_w2 (channel bottom → TC plane) is given. Distance from TC plane to bottom surface (heater plane) is not stated. <!-- TODO: check Fig. 3 cross-section or companion paper for total copper height -->
- **Anti-conduction slot dimensions:** Described as "three narrow deep slots" but width, depth, and axial positions are not specified. For a unit-cell CFD model these may be ignorable (they affect only axial conduction in the solid, which is secondary).
- **Inlet/outlet plenum geometry:** Plenums exist upstream and downstream but dimensions are not given. Relevant only if modeling the full heat sink (not the unit cell).

**Three-sided heating correction:** Because the top wall is adiabatic, correlations developed for uniformly heated tubes require a correction factor Nu₃/Nu₄, where Nu₃ and Nu₄ are fully developed laminar Nusselt numbers for 3-wall and 4-wall heating, respectively [Qu & Mudawar 2003, Eqs. 11–12]. This correction must also be applied in CFD post-processing when comparing to the data.

## Experimental Conditions

| Parameter | Value |
|-----------|-------|
| Fluid | Deionized water (deaerated) |
| T_in | 30 °C, 60 °C |
| G | 135–402 kg/m²s |
| P_out | 1.17 bar |
| P_pump_exit | 2.0 bar (elevated to suppress flow oscillations) |
| x_e range | 0 to ~0.2 (tests terminated at x_e ≈ 0.2) |
| h_tp range | 20–45 kW/m²K |
| Heat loss | < 4% (verified by single-phase energy balance) |
| Measurement uncertainty | Wattmeter ±0.5%, thermocouples ±0.3 °C, pressure ±3.5%, flow rate ±4% |

**Data reduction method:** Fin analysis applied to a 2D unit cell (single channel + surrounding solid). Side walls modeled as thin fins with efficiency η. Mean h_tp averaged over heated perimeter. Wall temperature T_w obtained from thermocouple readings corrected for 1D conduction through copper between TC plane and channel bottom.

## Correlation Assessment

| # | Correlation | Type | MAE (%) | Captures h_tp vs x_e trend? |
|---|-------------|------|---------|----------------------------|
| 1 | Chen (1966) | Macro | 43.9 | No — predicts increasing h_tp |
| 2 | Shah (1976, 1982) | Macro | 53.7 | No |
| 3 | Gungor & Winterton (1986) | Macro | 50.1 | No |
| 4 | Kandlikar (1990) | Macro | 49.4 | No |
| 5 | Liu & Winterton (1991) | Macro | 35.1 | No |
| 6 | Steiner & Taborek (1992) | Macro | 46.2 | No |
| 7 | Lazarek & Black (1982) | Mini/micro | 36.2 | No |
| 8 | Tran et al. (1996) | Mini/micro | 98.8 | No |
| 9 | Lee & Lee (2001) | Mini/micro | 272.1 | No |
| 10 | Yu et al. (2002) | Mini/micro | 19.3 | No (best MAE, wrong trend) |
| 11 | Warrier et al. (2002) | Mini/micro | 25.4 | Closest to correct trend |

**Bottom line:** No existing correlation is suitable for water microchannel heat sink design. Even the best performer gets the qualitative trend wrong. This motivates CFD-based and mechanistic-model-based approaches.

## Data Available for Validation

- Fig. 6(a, b): h_tp vs x_e at tc4 for T_in = 30 °C and 60 °C, five mass velocities each — **primary validation target for Stage 2**.
- Fig. 5: Boiling curves (q″_eff vs T_w − T_in) at all four TC locations for one operating condition.
- Figs. 8(a–f), 10(a–e): Predicted-to-measured h_tp ratio vs x_e for all 11 correlations — useful for benchmarking our correlation library.
- Table 3: Unit cell dimensions for geometry reproduction.
- Table 4: All 11 correlation equations in closed form — directly implementable.

## Applicability to This Project

**This is the Stage 2 validation benchmark** (per CLAUDE.md validation registry). It provides the closest published match to our cold plate design: rectangular copper microchannels, water, heat-sink-scale geometry with parallel channels and three-sided heating. The experimental conditions (G = 135–402 kg/m²s, P ≈ 1 atm, D_h ≈ 349 µm) fall within our design variable space.

> **Validation data covers saturated flow boiling only (x_e ≥ 0).** Subcooled regime data must come from other sources: [[HallMudawar2000_subcooled_CHF]] for CHF safety margins, [[KrepperRzehak2011_DEBORA]] for subcooled void fraction and temperature profiles. Together, these three papers form a coverage map across regimes — do not rely on Qu & Mudawar 2003 alone for subcooled validation.

**Mass velocity range is low.** G = 135–402 kg/m²s is at the lower end of our design space (PROJECT_CONTEXT.md targets up to high-mass-velocity conditions). Higher-G validation may require additional data sources.

**Three-sided heating vs. uniform heating.** The adiabatic top wall creates a non-uniform heat flux distribution around the channel perimeter. CFD models must reproduce this boundary condition exactly (heated bottom + side walls, adiabatic top) — not assume uniform heating.

**Pressure drop data are in the companion paper** ([[QuMudawar2003_pressure_drop]]), which must be ingested separately for a complete validation (thermal + hydraulic).

**Flow oscillation suppression.** The pump exit pressure was elevated to 2.0 bar to suppress two-phase instabilities. Our CFD model assumes steady-state flow — this experimental precaution ensures the data are compatible with that assumption.

## Cross-References

- [[motivation_for_CFD_approach]]
- [[CHF_correlations]]
- [[mudawar_group]]
- [[HallMudawar2000_subcooled_CHF]]
- [[KrepperRzehak2011_DEBORA]]
- [[QuMudawar2003_pressure_drop]]
- [[QuMudawar2003_annular_model_II]]

### Concepts

- [[two_phase_fundamentals]]

## Notes

- Inlet Reynolds number range is 60–300 (laminar). Macro-channel correlations assume turbulent flow (Dittus-Boelter base) — a fundamental mismatch explaining part of the correlation failure.
- The paper does not report CHF data. Tests were terminated at x_e ≈ 0.2, well below CHF. CHF safety margins must be evaluated separately.
- The companion Part II paper [Qu & Mudawar 2003, ref. 21] develops an annular flow model incorporating the droplet entrainment/deposition mechanism — this may be more useful than any of the 11 correlations for our 1D analytical model.
