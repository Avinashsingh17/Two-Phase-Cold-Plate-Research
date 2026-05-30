---
title: "Kim & Mudawar 2013 — Universal Saturated Flow Boiling HTC Correlation for Mini/Micro-Channels (Part II)"
type: paper
source: "S.-M. Kim, I. Mudawar, 'Universal approach to predicting saturated flow boiling heat transfer in mini/micro-channels – Part II. Two-phase heat transfer coefficient,' International Journal of Heat and Mass Transfer, vol. 64, pp. 1239–1256, 2013."
date_ingested: 2026-05-20
tags: [correlation, flow-boiling, microchannel, HTC, universal, dryout, annular-flow, nucleate-boiling, convective-boiling, water, refrigerant]
---

## Summary

Consolidates the largest published database for saturated flow boiling heat transfer in mini/micro-channels (10,805 pre-dryout data points, 31 sources, 18 working fluids, D_h = 0.19–6.5 mm) and develops a new "universal" correlation by superpositioning nucleate boiling and convective boiling contributions. Achieves MAE = 20.3% overall — the best available correlation for mini/micro-channels. However, for the water microchannel subset (Qu & Mudawar 2003), the correlation reproduces the magnitude (MAE = 20.5%) but **not the trend**: it predicts h_tp increasing with quality (standard convective boiling), while the data shows h_tp decreasing — the same qualitative failure as all 11 correlations tested in Qu & Mudawar 2003. This strengthens the project's motivation for CFD-based design. See [[motivation_for_CFD_approach]].

## Key Findings

- **10,805-point pre-dryout consolidated database.** 18 fluids (FC72, R11, R113, R123, R1234yf, R1234ze, R134a, R152a, R22, R236fa, R245fa, R32, R404A, R407C, R410A, R417A, CO2, water), D_h = 0.19–6.5 mm, G = 19–1608 kg/m²s, Re_fo = 57–49,820, x = 0–1, P_R = 0.005–0.69. Pre-dryout subset identified using Part I's dryout incipience quality correlation [Kim & Mudawar 2013].
- **13 prior correlations assessed** (4 macro-channel: [[Shah_1982]], [[Cooper_1984]], [[GungorWinterton_1986]], [[LiuWinterton_1991]]; 9 mini/micro-channel: [[LazarekBlack_1982]], [[Tran_1996]], [[Warrier_2002]], [[Yu_2002]], [[AgostiniBontemps_2005]], [[Bertsch_2009]], [[LiWu_2010]], [[Ducoulombier_2011]], [[OhSon_2011]]). Best of the old guard: Lazarek & Black (MAE 28.2%), Liu & Winterton (28.1%). All degrade for D_h < 0.5 mm or convective-boiling-dominant data [Kim & Mudawar 2013].
- **New correlation achieves MAE = 20.3%** overall, 79.9% within ±30%, 95.5% within ±50%. Evenly good across all fluids and parameter ranges. Best performance among all tested for 23 of 37 individual source databases [Kim & Mudawar 2013].
- **Two distinct heat transfer regimes identified.** Nucleate Boiling Dominant (h_nb/h_cb > 1): h_tp decreases with x due to gradual nucleation suppression. Convective Boiling Dominant (h_nb/h_cb < 1): h_tp increases with x due to annular film thinning. The correlation captures both regimes via the superposition form [Kim & Mudawar 2013].
- **Water at ~1 atm in microchannels is strongly convective-boiling-dominant.** Fig. 12(a) shows (h_nb/h_cb)_avg ≪ 1 for water at P_sat = 1 bar, D_h = 0.5 mm — nucleate boiling is "virtually nonexistent" [Kim & Mudawar 2013]. The correlation predicts h_tp increasing with x for this case.
- **Qu & Mudawar 2003 water data:** (h_nb/h_cb)_avg = 0.26 for this 335-point subset (averaged over the full quality range of that dataset), confirming convective boiling dominance. New correlation MAE = 20.5%, vs. Shah 61.8%, Lazarek & Black 41.0%, Liu & Winterton 41.8%, Bertsch 19.5% [Kim & Mudawar 2013, Table 5].
- **The correlation does NOT capture the h_tp-decreasing-with-quality trend in the Qu & Mudawar water microchannel data.** The correlation's convective boiling term (h_cb) inherently increases with x via the Martinelli parameter (thinner annular film → higher HTC). The unique droplet entrainment/deposition mechanism identified by Qu & Mudawar 2003 — which thickens the film downstream, reversing the trend — is not in any superposition-type correlation's physics. The 20.5% MAE is achieved by averaging opposing errors across quality bins, not by matching the trend. **This is the load-bearing finding for the project motivation.** See [[motivation_for_CFD_approach]].

## Publication Cluster

This paper is Part II of a two-part study:

| Paper | Topic | File in raw/ | Ingested? |
|-------|-------|-------------|-----------|
| **Part I** | Dryout incipience quality correlation (x_di) | Not in raw/ | No |
| **Part II** (this page) | Pre-dryout two-phase HTC correlation | A4 | Yes |

Cross-reference: [[KimMudawar2013_dryout_incipience_I]]

## Correlation Equations

### Pre-dryout two-phase heat transfer coefficient (Table 4)

$$
h_{tp} = \left(h_{nb}^2 + h_{cb}^2\right)^{0.5}
$$

**Nucleate boiling contribution:**

$$
h_{nb} = \left[2345 \left(\text{Bo} \frac{P_H}{P_F}\right)^{0.70} P_R^{0.38} (1-x)^{-0.51}\right] \left(0.023 \, Re_f^{0.8} \, Pr_f^{0.4} \frac{k_f}{D_h}\right)
$$

**Convective boiling contribution:**

$$
h_{cb} = \left[5.2 \left(\text{Bo} \frac{P_H}{P_F}\right)^{0.08} We_{fo}^{-0.54} \left(\frac{\rho_g}{\rho_f}\right)^{0.94} + 3.5 \left(\frac{1}{X_{tt}}\right)^{0.25}\right] \left(0.023 \, Re_f^{0.8} \, Pr_f^{0.4} \frac{k_f}{D_h}\right)
$$

where:

| Symbol | Definition |
|--------|-----------|
| Bo | q″_H / (G·h_fg) — Boiling number based on heated perimeter heat flux |
| P_H / P_F | Heated perimeter / wetted perimeter (= 1 for uniform circumferential; < 1 for three-sided heating) |
| P_R | P / P_crit — Reduced pressure |
| Re_f | G(1−x)D_h / µ_f — Superficial liquid Reynolds number |
| We_fo | G²D_h / (ρ_f·σ) — Liquid-only Weber number |
| X_tt | (µ_f/µ_g)^0.1 · ((1−x)/x)^0.9 · (ρ_g/ρ_f)^0.5 — Lockhart-Martinelli parameter (turbulent-turbulent) |

### Dryout incipience quality (Part I, Table 1)

$$
x_{di} = 1.4 \, We_{fo}^{0.03} \, P_R^{0.08} \, Ca^{-0.35} \left(\frac{\rho_g}{\rho_f}\right)^{-0.06} - 15.0 \, \text{Bo} \frac{P_H}{P_F}
$$

where Ca = µ_f·G / (ρ_f²·σ) = We_fo / Re_fo (Capillary number).

**Note:** Part I is not ingested. This equation is reproduced from Table 1 of the present paper for completeness. x_di marks the quality at which annular film dryout begins and h_tp starts to collapse.

### Three-sided heating correction (Eqs. 3a, 3b)

For rectangular channels with three-sided heating (e.g., Qu & Mudawar geometry), the PH/PF ratio in the correlation handles the asymmetry directly. The older Nu₃/Nu₄ correction used in Qu & Mudawar 2003 is not needed when using this correlation.

Nu₃ and Nu₄ polynomials (Shah & London 1978) are given for reference:

- Nu₃ = 8.235(1 − 1.833β + 3.767β² − 5.814β³ + 5.361β⁴ − 2.0β⁵)
- Nu₄ = 8.235(1 − 2.042β + 3.085β² − 2.477β³ + 1.058β⁴ − 0.186β⁵)

where β < 1 is the channel aspect ratio (short side / long side).

## Prior Correlation Assessment (against 10,805-point database)

### Macro-channel correlations

| Correlation | MAE (%) | θ (±30%) | ξ (±50%) | Notes |
|-------------|---------|----------|----------|-------|
| [[Shah_1982]] | 32.0 | 57.0 | 85.7 | Underpredicts high-pressure data |
| [[Cooper_1984]] (pool boiling) | 33.2 | 46.2 | 83.1 | Generally underpredicts |
| [[GungorWinterton_1986]] | 28.1 | 63.4 | 90.4 | Generally overpredicts |
| [[LiuWinterton_1991]] | 55.9 | 41.6 | 59.3 | Poor for D_h < 2 mm |

### Mini/micro-channel correlations

| Correlation | MAE (%) | θ (±30%) | ξ (±50%) | Notes |
|-------------|---------|----------|----------|-------|
| [[LazarekBlack_1982]] | 28.2 | — | — | Best of the old mini/micro; poor for CB-dominant |
| [[Bertsch_2009]] | 30.5 | — | — | Underpredicts most data |
| Other 7 correlations | 34–1673% | — | — | Wide scatter; see Table 3 in paper |

### By fluid category (Table 6)

| Fluid category | N_pts | New correlation MAE (%) | Best prior MAE (%) |
|----------------|-------|------------------------|--------------------|
| Refrigerants | 8222 | 21.0 | 26.5 (Lazarek & Black) |
| Water | 485 | 21.2 | 23.9 (Bertsch) |
| CO₂ | 1758 | 16.3 | 22.9 (Liu & Winterton) |
| FC72 | 340 | 21.9 | 19.5 (Lazarek & Black) |

### By dominant regime (Table 7)

| Regime | N_pts | New correlation MAE (%) | Best prior MAE (%) |
|--------|-------|------------------------|--------------------|
| Nucleate boiling dominant (h_nb/h_cb > 1) | 8264 | 20.7 | 24.3 (Lazarek & Black) |
| Convective boiling dominant (h_nb/h_cb ≤ 1) | 2541 | 19.0 | 25.8 (Liu & Winterton) |

## Data Available for Validation

- Table 4: Complete correlation equations (reproduced above) — directly implementable.
- Table 1: Dryout incipience quality correlation from Part I (reproduced above).
- Table 5: MAE for each of 37 individual databases against 5 correlations — comprehensive benchmarking reference.
- Table 6: MAE by fluid category (refrigerants, water, CO₂, FC72).
- Table 7: MAE by dominant regime (NB vs. CB).
- Figs. 9–10: Predicted vs. measured h_tp as function of x for selected datasets — trend validation.
- Fig. 12: Parametric trend predictions for water, CO₂, R134a, FC72 at representative conditions.

## Applicability to This Project

**Best available correlation for our parameter range.** D_h = 0.19–6.5 mm covers our cold plate channels. Water is included in the database (485 points). The correlation handles three-sided heating via PH/PF without external correction. It is directly implementable for 1D analytical screening before CFD.

**Does not replace CFD for design optimization.** Despite 20.5% MAE on the Qu & Mudawar data by magnitude, the correlation predicts the wrong qualitative trend (h_tp increasing with x for water microchannels, whereas data shows decreasing). This means it cannot reliably predict *where* in the quality range h_tp is highest — which is exactly what a design optimizer needs. The correlation is useful for order-of-magnitude screening but not for trend-sensitive optimization.

**x_di and subcooled CHF are different physical constraints.** The dryout incipience quality x_di (Part I) marks annular film dryout onset in the *saturated* regime (x > 0). The Hall & Mudawar CHF correlation constrains the *subcooled* regime (x < 0). These are not redundant safeguards — they are constraints in different operating regimes. If our cold plate design crosses into saturated operation (x_e > 0), x_di becomes the binding thermal limit; if it stays subcooled, Hall & Mudawar CHF governs. Both constraints must be evaluated.

**Three-sided heating.** The PH/PF ratio in the correlation handles asymmetric heating directly, avoiding the Nu₃/Nu₄ multiplier needed by older correlations. For the Qu & Mudawar geometry (β ≈ 0.324), PH/PF = (W_ch + 2·H_ch) / (W_ch + 2·H_ch + W_ch) = (231 + 1426) / (231 + 1426 + 231) ≈ 0.878.

**Part I (dryout incipience) not in raw/.** The x_di correlation is reproduced from Table 1 of this paper but the full Part I derivation and validation are not available for detailed ingest. Consider sourcing if x_di becomes a binding constraint.

## Cross-References

- [[motivation_for_CFD_approach]]
- [[QuMudawar2003_microchannel_boiling_I]]
- [[HallMudawar2000_subcooled_CHF]]
- [[CHF_correlations]]
- [[mudawar_group]]
- [[KimMudawar2013_dryout_incipience_I]]

### Concepts

- [[two_phase_fundamentals]]

## Notes

- The correlation is optimized against pre-dryout data only. Post-dryout (x > x_di) heat transfer is not addressed; the mist flow regime requires separate treatment.
- Re_fo < 50,000 and P_R < 0.7 are recommended applicability limits; data are too sparse outside these ranges.
- The paper includes Qu & Mudawar 2003 data as source [26] in the consolidated database. The (h_nb/h_cb)_avg = 0.26 value is for the Qu & Mudawar 335-point subset only — not the full 10,805-point database. Convective boiling dominates across the full quality range of that subset.
- The superposition form h_tp = (h_nb² + h_cb²)^0.5 follows Churchill & Usagi (1972) asymptotic blending. The exponent of 2 was selected over linear or cubic superposition based on best fit to the database [Kim & Mudawar 2013].
- This paper explicitly cites and includes the Qu & Mudawar 2003 data. Reference [26] in their paper = our [[QuMudawar2003_microchannel_boiling_I]].
