---
title: "Hall & Mudawar 2000 — Subcooled CHF Correlations for Water in Tubes"
type: paper
source: "D.D. Hall, I. Mudawar, 'Critical heat flux (CHF) for water flow in tubes — II. Subcooled CHF correlations,' International Journal of Heat and Mass Transfer, vol. 43, pp. 2605–2640, 2000."
date_ingested: 2026-05-07
tags: [CHF, correlation, subcooled-boiling, water, round-tube, validation]
---

## Summary

Exhaustive compilation and assessment of 100+ subcooled CHF correlations for water flow in uniformly heated round tubes, evaluated against the PU-BTPFL database containing 5544 subcooled CHF data points — the largest such database in the open literature. The authors develop two new nondimensional correlations (inlet- and outlet-conditions forms) with only 5 adjustable constants each, whose functional forms were derived from observed parametric trends rather than statistical curve-fitting. The inlet-conditions correlation is recommended as the most accurate subcooled CHF prediction method available for uniformly heated tubes.

## Key Findings

- The optimized inlet-conditions correlation achieves MAE = 10.3% and RMS = 14.3% against the full subcooled CHF database — errors *below* the estimated ~18% total experimental uncertainty in CHF measurement [Hall & Mudawar 2000]. This means the correlation is as accurate as the underlying data permits; re-optimization with additional data is unlikely to improve accuracy.
- The inlet-conditions correlation is 41% more accurate (by MAE) than the next-best correlation in the literature [Hall & Mudawar 2000].
- The Groeneveld et al. 1995 CHF look-up table (used in nuclear reactor thermal-hydraulic codes) has MAE = 37.5% and RMS = 72.5% within the subcooled region, and *cannot predict* 30% of the database because data fall outside its tabulated range [Hall & Mudawar 2000]. The inlet-conditions correlation is superior to the look-up table under all conditions tested.
- Functional forms were determined from parametric trends in <10% of the database (high-G, small-D data from Mudawar & Bowers and Ornatskii & Kichigin), then constants were optimized against the full database. The fact that pre-optimization constants already yielded near-optimal accuracy confirms the physical basis of the functional form [Hall & Mudawar 2000].
- CHF is approximately proportional to G^0.5 (Weber number exponent C₂ = −0.312) and decreases linearly with increasing outlet quality [Hall & Mudawar 2000].

## Correlation Equations

### Inlet-conditions correlation (recommended for uniform heat flux)

$$
\text{Bo} = \frac{C_1 \, \text{We}_D^{C_2} \, (\rho_f/\rho_g)^{C_3} \left[1 - C_4 \, (\rho_f/\rho_g)^{C_5} \, x_{i}'\right]}{1 + 4 \, C_1 \, C_4 \, \text{We}_D^{C_2} \, (\rho_f/\rho_g)^{C_3+C_5} \, (L/D)}
$$

where Bo = q″_CHF / (G·h_fg), We_D = G²D/(ρ_f·σ), and x_i' is the pseudo-inlet quality (saturated properties evaluated at outlet pressure).

### Outlet-conditions correlation (for nonuniform heat flux)

$$
\text{Bo} = C_1 \, \text{We}_D^{C_2} \, (\rho_f/\rho_g)^{C_3} \left[1 - C_4 \, (\rho_f/\rho_g)^{C_5} \, x_o\right]
$$

### Optimized constants (same for both correlations)

| Constant | Value |
|----------|-------|
| C₁ | 0.0722 |
| C₂ | −0.312 |
| C₃ | −0.644 |
| C₄ | 0.900 |
| C₅ | 0.724 |

## Parametric Range

| Parameter | Inlet correlation | Outlet correlation |
|-----------|------------------|--------------------|
| D (mm) | 0.25–15 | 0.25–15 |
| L/D | 2–200 | — |
| G (kg/m²s) | 300–30,000 | 300–30,000 |
| P (bar) | 1–200 | 1–200 |
| x_i | −2.0 to 0.0 | — |
| x_o | −1.0 to 0.0 | −1.0 to −0.05 |

The inlet correlation parametric range was chosen to contain ~85% of the subcooled CHF database, concentrated in data-rich regions.

## Error Bands

| Correlation | Database | MAE (%) | RMS (%) | Mean error (%) |
|-------------|----------|---------|---------|----------------|
| Inlet (recommended) | Full (4860 pts) | 10.3 | 14.3 | −2.0 |
| Outlet | Full (4860 pts) | 22.3 | 31.6 | −2.1 |
| Outlet | x_o < −0.05 (3202 pts) | 18.5 | 27.7 | — |
| Groeneveld 1995 LUT | Within LUT range (3405 pts) | 37.5 | 72.5 | 23.6 |

## Experimental / Computational Setup

| Parameter | Value |
|-----------|-------|
| Geometry | Round tubes, uniformly heated |
| Fluid | Water |
| D range | 0.25–44.7 mm (database); 0.25–15 mm (correlation range) |
| G range | 300–134,000 kg/m²s (database); 300–30,000 (correlation range) |
| P range | 1–218 bar (database); 1–200 bar (correlation range) |
| CHF range | 0.5–276 MW/m² |
| Flow orientation | Primarily vertical upflow (4227 pts); horizontal (633 pts) |

## Data Available for Validation

- Table 4: Final correlation equations and constants — directly implementable.
- Table 5: MAE, RMS, and mean error for all 77+ correlations — useful for benchmarking any CHF correlation we implement.
- Table 6: Head-to-head comparison of inlet/outlet correlations vs. Groeneveld LUT across multiple parametric subsets.
- Figs. 3(a–i): Error distribution by parameter bin — shows where correlation accuracy degrades.
- Fig. 5: Predicted vs. measured CHF scatter plot and error histogram.

## Applicability to This Project

This paper provides the primary CHF correlation for computing critical heat flux safety margins in the cold plate optimization. The CHF constraint (operating heat flux ≤ q″_CHF / 1.5) is one of the four optimization objectives. The inlet-conditions correlation is the recommended tool for this: 5 constants, single equation, physically-grounded functional form, and accuracy below experimental uncertainty. The comparison to the Groeneveld look-up table (MAE 37.5%, 30% of data unpredictable) provides direct justification for using a correlation-based approach rather than a look-up table in our framework.

**Geometry mismatch — round tube vs. rectangular microchannel.** All data and correlations in this paper are for uniformly heated round tubes. Our cold plate uses rectangular microchannels (aspect ratios 0.5–5, D_h = 0.5–3 mm). The standard approach is to substitute hydraulic diameter D_h = 4A/P_w for the tube diameter D in the correlation. This is common practice but introduces additional uncertainty not quantified in the paper's error bands. The degree of extra error depends on aspect ratio and confinement effects.

**Partially mitigated by parametric range.** The correlation covers D down to 0.25 mm and L/D down to 2, which overlaps well with microchannel dimensions. The small-diameter, high-mass-velocity regime (where the correlation was developed) aligns with cold plate operating conditions.

**Rectangular channel validation needed.** The hydraulic-diameter substitution should be checked against rectangular-channel CHF data. [[QuMudawar2003_microchannel_heat_sink]] provides saturated boiling data in 231 µm × 713 µm rectangular channels that can serve as a cross-check. <!-- TODO: verify --> Whether Hall & Mudawar inlet correlation with D_h substitution predicts Qu & Mudawar CHF data within acceptable error has not yet been assessed.

**Fluid match.** Water — matches our Phase 1 validation fluid. Not applicable to dielectric fluids (Phase 2) without separate validation.

## Cross-References

- [[CHF_correlations]]
- [[mudawar_group]]
- [[QuMudawar2003_microchannel_heat_sink]]
## Notes

- The outlet-conditions correlation degrades for near-saturated conditions (x_o > −0.05), suggesting a possible transition in the CHF trigger mechanism near saturation [Hall & Mudawar 2000].
- Part I of this study [Hall & Mudawar 2000, ref. 1] describes the PU-BTPFL database compilation and data screening methodology. Not ingested separately but referenced here.
- The 110 data points from Mayinger et al. were excluded from optimization due to suspected measurement quality issues (MAE = 41.4% vs. correlation).
