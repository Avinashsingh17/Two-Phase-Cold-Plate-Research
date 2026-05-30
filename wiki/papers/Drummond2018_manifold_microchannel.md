---
title: "Drummond et al. 2018 — A Hierarchical Manifold Microchannel Heat Sink Array for High-Heat-Flux Two-Phase Cooling of Electronics"
type: paper
source: "K.P. Drummond, D. Back, M.D. Sinanis, D.B. Janes, D. Peroulis, J.A. Weibel, S.V. Garimella, 'A hierarchical manifold microchannel heat sink array for high-heat-flux two-phase cooling of electronics,' International Journal of Heat and Mass Transfer, vol. 117, pp. 319–330, 2018."
date_ingested: 2026-05-24
tags: [microchannel, manifold, two-phase, HFE-7100, dielectric, intrachip, embedded-cooling, experimental, baseline]
---

## Summary

First demonstration of two-phase evaporative cooling in a hierarchical manifold microchannel (MMC) heat sink array using a dielectric fluid (HFE-7100). A 3 x 3 array of silicon microchannel heat sinks — each containing 50 high-aspect-ratio channels etched directly into the heated substrate — is fed by a hierarchical manifold that decouples effective flow length from chip area. Three channel depths (35, 150, 300 um at fixed 15 um width) are tested parametrically across three mass fluxes (1300, 2100, 2900 kg/m^2 s). The deepest channels dissipate base heat fluxes up to 910 W/cm^2 at pressure drops below 162 kPa and chip-to-fluid temperature rises under 47 C. This paper is the **baseline design target** for the optimization phase of this project. See [[baseline_decision]].

## Key Findings

### Extreme heat flux performance with dielectric fluid

Base heat fluxes up to 910 W/cm^2 (Sample C, G = 2900 kg/m^2 s) are demonstrated with HFE-7100, at pressure drops < 162 kPa and chip-to-fluid DT < 47 C [Drummond 2018]. This is a record-level result for dielectric-fluid two-phase cooling. Minimum effective thermal resistance of 5.6 x 10^-6 m^2 K/W (Sample C, G = 2900) — comparable to a single layer of high-performance thermal interface material [Drummond 2018].

### Heat transfer coefficient is approximately geometry-independent in the low-quality regime

For all three channel geometries at all mass fluxes, **h_wall values converge in the low-quality regime** (0 < x_out < 0.1). In this range, all samples show similar heat transfer coefficients that increase steadily with exit quality, independent of channel cross-section [Drummond 2018, Fig. 10]. This is attributed to highly confined two-phase flow in small hydraulic diameter channels (d_h = 19.6–31.7 um), where bubble confinement dominates and the flow regime is insensitive to channel geometry.

**Implication for design:** If HTC does not strongly depend on channel cross-section in the confined regime, then the dominant design levers are: (a) total wetted area per unit footprint (fin density and fin efficiency), and (b) staying below dryout quality — not channel aspect ratio per se. This potentially simplifies the design optimization problem. See [[open_questions]] #11.

### Deeper channels increase maximum heat flux but with diminishing returns

| Sample | w_c x d_c (um) | AR | Max q"_base (W/cm^2) | Min R_eff (m^2 K/W) | Fin efficiency (%) |
|--------|----------------|-----|----------------------|---------------------|--------------------|
| A | 15 x 35 | 2.7 | 142 | 19.9 x 10^-6 | High (not reported) |
| B | 15 x 150 | 10.4 | 705 | 7.66 x 10^-6 | ~70–80 (estimated) |
| C | 15 x 300 | 19.1 | 910 | 5.60 x 10^-6 | ~58 |

Deeper channels provide more wetted area, reducing thermal resistance. But fin efficiency drops to ~58% for the deepest channels (Sample C), meaning nearly half the added fin area is thermally inactive [Drummond 2018]. The design tradeoff between wetted area and fin efficiency is the central geometric optimization lever.

### CHF and dryout behavior

CHF occurred at exit qualities between 0.18 and 0.28 for Samples A and B. Sample C did not reach CHF — experiments were terminated at the temperature safety limit (~125 C chip temperature) [Drummond 2018, Table 4]. CHF increases with mass flux and wetted area, consistent with straight-channel literature. Boiling incipience observed at 8–10 C superheat (G = 1300) to 14–22 C (G = 2900).

### Manifold architecture decouples flow length from device area

The hierarchical manifold delivers fluid to the center of each microchannel and collects it from both ends, setting the effective flow length to **750 um regardless of chip area** [Drummond 2018]. This directly addresses the pressure-drop scaling problem (DP ~ L/d_h^2) that limits conventional straight-channel heat sinks. See "Architectural template" under Applicability.

### Manifold pressure drop dominates at high flow rates

At the highest flow rates for Sample A (19–42 mL/min), up to 70% of the total single-phase pressure drop is estimated to come from manifold losses (sudden expansions, contractions, flow splitting) rather than channel friction [Drummond 2018]. At low flow rates, manifold contribution is negligible (< 3%). This means manifold design becomes the critical pressure-drop bottleneck at high mass fluxes — optimizing only channel geometry is insufficient.

## Test Vehicle Architecture

### Hierarchical manifold microchannel concept

- 3 x 3 array of microchannel heat sinks covering a 5 x 5 mm silicon chip
- Each heat sink: 50 parallel channels in a 1667 x 1667 um footprint
- Microchannels etched directly into silicon substrate (intrachip / embedded cooling)
- Fluid enters at channel center via manifold, exits both ends → effective flow length = 750 um
- Manifold uses self-similar hierarchical bifurcation to distribute flow uniformly
- Plenum interface plate between manifold and microchannel plate provides 1:1 inlet-to-outlet area ratio

### Component stack (bottom to top)

| Layer | Material | Function |
|-------|----------|----------|
| Manifold base | Acrylic (laser-cut, 4 layers) | Flow distribution network |
| Plenum interface plate | Silicon | Defines individual inlet/outlet per heat sink |
| Microchannel plate | Silicon | Contains channels + heaters/sensors |
| PCB | Custom | Electrical interface to heaters and RTDs |

### Fabrication

- Microchannel plate: 4-inch double-side polished Si wafer, 350 nm SiO2 thermal oxide, channels etched by DRIE (Bosch process)
- Wafer thicknesses: 220 um (Sample A), 300 um (Sample B), 385 um (Sample C)
- Heaters: Pt serpentine heaters (9 in parallel, covering 5 x 5 mm)
- Temperature sensors: 9 x 4-wire Pt RTDs (calibrated, +/- 1.0 C)
- Microchannel-plenum bonding: thermo-compression Au-Au bonding at 450 C

## Heat Sink Geometry

### Channel dimensions (from Table 1, measured by SEM)

| Parameter | Sample A | Sample B | Sample C | Notes |
|-----------|----------|----------|----------|-------|
| Channel width, w_c (um) | 12.0 | 14.7 | 16.2 | Nominal 15 um; actual varies due to DRIE taper |
| Channel depth, d_c (um) | 34 | 153 | 310 | Nominal 35, 150, 300 um |
| Hydraulic diameter, d_h (um) | 19.6 | 28.8 | 31.7 | d_h = 2 w_c d_c / (w_c + d_c) |
| Aspect ratio, AR | 2.7 | 10.4 | 19.1 | |
| Channel cross-section area, A_c (um^2) | 360 | 2275 | 5000 | |
| Channel wetted area per channel, A_wet (um^2) | 5.59 x 10^4 | 2.41 x 10^5 | 4.83 x 10^5 | Rectangular perimeter x L_flow |
| Fin width (wall between channels) | 30 um pitch - w_c | 30 um pitch - w_c | 30 um pitch - w_c | Fin pitch is constant at 30 um |

### Heat sink planform

| Parameter | Value |
|-----------|-------|
| Heat sink footprint per element | 1667 x 1667 um |
| Array | 3 x 3 = 9 heat sinks |
| Total cooled area | 5 x 5 mm = 25 mm^2 = 0.25 cm^2 |
| Channels per heat sink | 50 |
| Total channels | 450 |
| Effective flow length, L_flow | 750 um |
| Channel material | Silicon |
| Heating configuration | Bottom wall heated (opposite face from channels) |
| Wafer thickness (base, d_b) | 220 / 300 / 385 um for A / B / C |

### Dimensions not explicitly reported (flag for any future Fluent modeling)

- **Manifold channel dimensions:** Internal manifold bifurcation widths and depths not fully specified. Would need to be reverse-engineered from Fig. 2 or obtained from authors for full manifold CFD.
- **Plenum feature dimensions:** Inlet/outlet port sizes on the plenum interface plate are described qualitatively (1:1 inlet-to-outlet ratio) but not dimensioned.
- **DRIE channel sidewall taper angle:** SEM images (Fig. 4) show tapered sidewalls and curved bottoms; actual cross-section is not perfectly rectangular. The reported A_wet accounts for the measured perimeter boundary, but a Fluent model would need to approximate this as rectangular or import the SEM profile.

## Experimental Conditions

| Parameter | Value |
|-----------|-------|
| Fluid | HFE-7100 (3M Novec engineered fluid) |
| T_in | T_sat - 7 C (7 C subcooling at inlet) |
| Outlet pressure | 123 kPa |
| G (channel mass flux) | 1300, 2100, 2900 kg/m^2 s |
| Flow rate range | 19–540 mL/min (across all samples) |
| Re range | 71–238 (laminar) |
| q"_base range | 0–910 W/cm^2 |
| x_out range | < 0 (single-phase) to ~0.3 |
| Max chip temperature | ~125 C (safety cutoff) |
| Dissolved gas management | Vigorous pre-boiling to remove noncondensable gases |

### Flow loop

Gear pump (magnetically coupled), Coriolis mass flow meter, inline preheater, liquid-liquid heat exchanger for condenser, adjustable-volume reservoir for pressure control.

### Uncertainty (Table 3)

| Measured value | Instrument | Uncertainty |
|----------------|------------|-------------|
| Chip temperature | Calibrated Pt RTDs | +/- 1.0 C |
| Fluid inlet/outlet temperature | T-type thermocouples (calibrated) | +/- 0.25 C |
| Pressure drop | Differential pressure transducer | +/- 0.17 kPa |
| Mass flow rate | Coriolis flow meter | +/- 0.1% |
| Heater voltage | Voltage divider circuit | +/- 1.0% |
| Heater current | Shunt resistor | +/- 0.1% |
| **Heat flux** | **Calculated** | **+/- 0.6 to 2%** |
| **R_eff** | **Calculated** | **+/- 5 to 10%** |
| **h_wall** | **Calculated** | **+/- 7 to 15%** |

## Data Reduction

Effective thermal resistance [Drummond 2018, Eq. 1]:

R_eff = A_b (T_chip,avg - T_fl,in) / Q_net

where A_b is the base footprint area (= chip area = 25 mm^2 in this experiment).

Wall heat transfer coefficient [Drummond 2018, Eq. 2]:

h_wall = Q_net / (eta_o A_wet (T_base,avg - T_fl,ref))

where eta_o = overall surface efficiency (Eq. 6), T_fl,ref = length-weighted reference temperature (Eq. 4), T_base,avg = chip temperature corrected for conduction through silicon base and SiO2 layer (Eq. 5).

Fin efficiency [Drummond 2018, Eq. 7]:

eta_f = tanh(m d_c) / (m d_c), where m = sqrt(2 h_wall / (k_Si w_f))

Iterative solution: h_wall → eta_f → eta_o → h_wall until converged.

Exit quality [Drummond 2018, Eq. 3]:

x_out = (Q_in - m_dot c_p (T_fl,out - T_fl,in)) / (m_dot h_fg)

## Thermal Performance Summary (Table 4)

| Sample | G (kg/m^2 s) | Max q"_base (W/cm^2) | Max h_wall (W/m^2 K) | Min R_eff (m^2 K/W) | Notes |
|--------|-------------|----------------------|----------------------|---------------------|-------|
| A (15 x 35) | 1300 | 68.5 | 33.7 x 10^3 | 27.4 x 10^-6 | |
| | 2100 | 104 | 35.9 x 10^3 | 24.2 x 10^-6 | |
| | 2900 | 142 | 43.3 x 10^3 | 19.9 x 10^-6 | |
| B (15 x 150) | 1300 | 411 | 26.9 x 10^3 | 9.22 x 10^-6 | |
| | 2100 | 641 | 31.0 x 10^3 | 7.73 x 10^-6 | |
| | 2900 | 705 | 30.7 x 10^3 | 7.66 x 10^-6 | |
| C (15 x 300) | 1300 | 761* | 28.7 x 10^3 | 5.90 x 10^-6 | |
| | 2100 | 873* | 27.0 x 10^3 | 5.83 x 10^-6 | |
| | 2900 | 910* | 28.2 x 10^3 | 5.60 x 10^-6 | |

*Experiment stopped due to high steady-state temperature rather than CHF.

## Data Available

- **Fig. 9(a–c):** Boiling curves — q"_base vs (T_base,avg - T_fl,ref) for all samples at all three mass fluxes. Primary baseline comparison data.
- **Fig. 10(a–c):** h_wall vs x_out for all samples at all three mass fluxes. Shows HTC geometry-independence in low-quality regime.
- **Fig. 11(a–c):** R_eff vs x_out for all samples at all three mass fluxes. **Primary target for the 15% improvement criterion.**
- **Fig. 12(a–c):** Pressure drop vs q"_base for all samples at all mass fluxes.
- **Fig. 8:** Spatial temperature distribution across 3 x 3 array (9 RTDs) — shows temperature non-uniformity increasing with heat flux.
- **Table 4:** Summary performance metrics (reproduced above).

## Heat Flux Convention

> **Project-wide convention (established with this ingest):** All heat fluxes in the wiki refer to **chip-level device heat flux** (q"_device = Q_net / A_chip) unless explicitly annotated as base heat flux. See [[schema_evolution]] entry 2026-05-24.

In this specific experiment, q"_base = q"_device because the 3 x 3 heat sink array covers the full 5 x 5 mm chip (A_b = A_chip = 25 mm^2 = 0.25 cm^2). The two metrics diverge when:
- The cold plate footprint differs from the chip area (common in remote/attached cold plates)
- The heat sink only partially covers the heated surface

For the **>= 15% improvement criterion**, we compare R_eff at matched pumping power. R_eff is geometry-invariant (it normalizes by chip footprint area); heat flux targets are ambiguous because they depend on reference surface. This ensures an apples-to-apples comparison regardless of how different papers define their reference area.

## Applicability to This Project

**This is the baseline design target for the optimization phase.** Drummond 2018 defines what "state of the art" looks like for two-phase manifold microchannel cooling of electronics. The optimization goal is to demonstrate >= 15% improvement in R_eff (or equivalent DT reduction at matched pumping power) over Drummond's best result via geometry optimization guided by validated CFD. See [[baseline_decision]].

### Architectural template

The **manifold-fed microchannel architecture** is the single most important design concept from this paper for our project. By delivering fluid to the channel center and collecting from both ends, the effective flow length is fixed at 750 um regardless of chip area. This directly solves the pressure-drop scaling problem:

- Conventional straight-channel heat sinks: DP ~ L_channel / d_h^2. For a 50 x 50 mm cold plate with 200 um channels, L/d_h ~ 250, producing prohibitive DP at high G.
- Manifold microchannel: L_flow = 750 um independent of device size. DP is governed by channel length (~750 um) + manifold losses, not device dimension.

This makes the manifold architecture a candidate template for our cold plate geometry, not just a data point. The optimization explores channel geometry (width, depth, fin pitch) and manifold parameters (bifurcation topology, port sizing) within this architectural framework.

**Key insight for manifold optimization:** At high mass fluxes, manifold losses dominate (up to 70% of total DP). Optimizing channel geometry alone is insufficient — the manifold must be co-optimized. This is a 3D design problem.

### What beating Drummond by 15% looks like

| Metric | Drummond best | 15% improvement target | Notes |
|--------|--------------|----------------------|-------|
| **R_eff** (primary) | 5.6 x 10^-6 m^2 K/W | < 4.8 x 10^-6 m^2 K/W | Geometry-invariant; this is the binding criterion |
| DP at matched R_eff | 162 kPa | < 138 kPa | Or: equivalent R_eff at >= 15% lower DP |

Candidate improvement levers:
- **Fin density optimization:** Drummond uses 30 um pitch (15 um channel + 15 um fin). Is this optimal? Fin efficiency drops to 58% for Sample C — there may be a better pitch that trades fin count for efficiency.
- **Channel depth optimization:** Sample C's diminishing returns (58% fin efficiency) suggest a depth optimum exists. Parametric CFD can locate it.
- **Manifold co-optimization:** Reducing manifold losses (70% of DP at high G) is potentially a larger lever than channel geometry changes.
- **Fluid property exploitation:** If Phase 2 uses HFE-7100 at different saturation pressures, latent heat and surface tension change — opening another design axis.

### Geometry and fluid mismatches vs. our cold plate

| Attribute | Drummond 2018 | Our project (Phase 1–2) | Mismatch severity |
|-----------|---------------|------------------------|-------------------|
| Fluid | HFE-7100 (dielectric) | Water (validation) → HFE-7100 (optimization) | Resolved by option (a): optimize with HFE-7100 |
| Substrate | Silicon | Copper (likely) | Moderate — k_Si = 148 W/mK vs k_Cu = 385 W/mK; affects fin efficiency and conduction resistance |
| Architecture | Intrachip (embedded) | Remote cold plate (attached) | Significant — embedded eliminates TIM + spreader resistance; our R_eff will include these |
| Channel scale | d_h = 19.6–31.7 um | d_h ~ 100–500 um (TBD) | Moderate — our channels will be larger; different confinement regime |
| Chip area | 5 x 5 mm | 50 x 50 mm (notional) | Manifold architecture handles the scaling; not a fundamental mismatch |
| Fabrication | DRIE in silicon | CNC / EDM in copper (likely) | Constrains minimum feature size in our design (~50 um vs ~15 um) |

### Fluid mismatch resolution

Decision recorded in [[baseline_decision]]: adopt option (a). Phase 1–2 validation uses water/R12 to prove the CFD framework. Phase 3 optimization uses HFE-7100 for direct comparison against Drummond. Closure recalibration for HFE-7100 is a separate workstream — see [[open_questions]] #12.

## Cross-References

- [[baseline_decision]]
- [[garimella_group]]
- [[CHF_correlations]]
- [[motivation_for_CFD_approach]]
- [[QuMudawar2003_microchannel_boiling_I]]
- [[open_questions]]

### Concepts

- [[two_phase_fundamentals]]

## Notes

- Drummond 2018 is funded by DARPA ICECool (Intrachip/Interchip Enhanced Cooling). This program drove much of the manifold microchannel work at Purdue in 2013–2018.
- The paper does not report local boiling data (void fraction profiles, local HTC along channel length). Only system-level metrics (T_chip, R_eff, DP, h_wall averaged over heat sink). This means Drummond cannot serve as a CFD validation case — it serves as a baseline design target only.
- Boiling number for this study: Bl = q"_base / (G h_fg) ranges from ~10^-4 to ~10^-3, overlapping with the Qu & Mudawar 2003 range. The same convective-boiling-dominant regime is likely operative, though the fluid is different.
- The paper cites Bertsch et al. [44] (2009) for a composite HTC correlation for saturated flow boiling in small channels — this is paper B3 in our raw/ folder.
