---
title: "Semi-Mechanistic Boiling (SMB) Model under the Mixture Multiphase Framework"
type: concept
tags: [SMB, mixture-model, flow-boiling, Fluent, wall-boiling, model-form, CFD]
---

## Nomenclature

Self-contained; every symbol, abbreviation, and named correlation used below is
defined here (and spelled out on first use in the text).

| Term | Meaning |
|------|---------|
| SMB | Semi-mechanistic boiling — empirical wall-boiling model combining a nucleate-boiling HTC term and a convective term, with a boiling-suppression factor |
| Mixture model | Simplified multiphase model solving mixture continuity/momentum/energy with algebraic (relative-velocity) slip between phases |
| Euler-Euler (E-E) | Two-fluid model solving separate continuity/momentum/energy sets per phase |
| RPI | Rensselaer Polytechnic Institute wall-boiling model — heat-flux **partitioning** closure (Q_C + Q_Q + Q_E) under Euler-Euler |
| HTC | Heat transfer coefficient |
| Foster-Zuber | Nucleate pool-boiling HTC correlation (nucleate term of SMB) |
| Chen | Chen (1966) saturated flow-boiling correlation (convective-augmentation factor) |
| Chen-Steiner | Boiling-suppression factor (Steiner et al. 2005) |
| ONB | Onset of nucleate boiling |
| CHF | Critical heat flux |
| y⁺ | Non-dimensional wall distance of the first cell centroid |
| ΔT_sat | Wall superheat, T_wall − T_sat |

## Definition

The **semi-mechanistic boiling (SMB)** model is an empirical wall-boiling closure
that predicts the boiling heat transfer coefficient (HTC) by combining a
nucleate-boiling term (Foster-Zuber), a convective-augmentation term (Chen 1966),
and a boiling-suppression factor (Chen-Steiner / Steiner et al. 2005). In ANSYS
Fluent it is run under the **mixture** multiphase framework, where a single set of
mixture continuity/momentum/energy equations is solved with algebraic slip between
liquid and vapor, rather than the two full phase sets of an Euler-Euler (E-E)
solution. It is the "fast path" demonstrated in [[Viyyuri2024_fluent_microchannel_boiling]].

## Physical Description

Unlike the [[RPI_wall_boiling_model]] — which **partitions** the wall heat flux
into single-phase-convective, quenching, and evaporative components under
Euler-Euler — SMB predicts an overall boiling HTC by **superposing** empirical
correlations. It combines fundamental principles (heat/mass transfer, bubble
dynamics) with empirical data, and can run at **steady state**, which is the
source of its speed advantage. In Fluent practice it requires a **coarse**
near-wall mesh (y⁺ > 5) and a modelled **solid zone** (a heat-flux boundary
condition cannot be applied directly to a fluid-adjacent wall).

### SMB (mixture) vs. RPI (Euler-Euler) — model-form contrast

| Axis | RPI / Euler-Euler | SMB / Mixture |
|------|-------------------|---------------|
| Multiphase framework | Eulerian-Eulerian (two full phase sets) | Mixture (algebraic slip) |
| Wall-boiling closure | heat-flux **partitioning** (Q_C + Q_Q + Q_E) | empirical **HTC superposition** (Foster-Zuber + Chen + Chen-Steiner) |
| Steady / transient | steady-capable | steady |
| Near-wall mesh | y⁺ ≥ ~70 to converge; run at y⁺ ≈ 200 [Krepper & Rzehak 2011] | y⁺ > 5 (coarse) [Viyyuri 2024] |
| Empiricism | closure catalog (d_W, f, N, A_W) | correlation-based HTC |
| Relative cost | moderate (transient/steady, finer near-wall) | low (fast path; ≈60× faster than VOF in [Viyyuri 2024]) |
| CHF | not predicted (sub-CHF only) | not predicted |

## Key Correlations and Models

| Correlation | Author(s) | Role |
|-------------|-----------|------|
| Foster-Zuber nucleate HTC | Foster & Zuber | Nucleate-boiling term |
| Convective augmentation | Chen [1966] | Convective term (heat-flux multiplier = 5 in [Viyyuri 2024] Case 1) |
| Chen-Steiner suppression | Steiner et al. [2005] | Boiling-suppression factor |
| Semi-mechanistic wall boiling | Das & Punekar [2016] | Underlying SMB formulation |

## Role in This Project

SMB-on-mixture is the candidate **fast screening path** for Phase 4/5 (much cheaper
than either VOF or a full RPI/Euler-Euler run), and is the reason D3 is retained as
a precedent. It is **distinct from the project's primary validation approach**,
which is RPI under Euler-Euler (Stage 1 DEBORA, Stage 2 Qu & Mudawar). Note that
mixture-model boiling closures also appear elsewhere in the corpus — the Ozguc 2024
topology-optimization framework uses a homogenization + mixture-model approach —
so this is a recurring model family, not a one-off. SMB is **not** validation-grade
here: its only appearance is in a vendor-authored precedent paper (see
[[Viyyuri2024_fluent_microchannel_boiling]], industry-source rule).

## Open Questions

- Does SMB-on-mixture recover the h_tp-decreases-with-quality trend that
  superposition correlations miss (see [[correlation_anatomy]]), or does it inherit
  the same structural failure? Untested for water microchannels in this corpus.
- Whether the fast path is accurate enough for Phase-4 screening, or only for
  qualitative ranking, is unresolved.

## Cross-References

- [[Viyyuri2024_fluent_microchannel_boiling]]
- [[RPI_wall_boiling_model]]
- [[RPI_model_implementation]]
- [[two_phase_fundamentals]]
- [[correlation_anatomy]]
