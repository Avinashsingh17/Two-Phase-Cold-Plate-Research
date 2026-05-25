---
title: "Baseline Design Target Decision — Drummond 2018 with HFE-7100"
type: synthesis
last_updated: 2026-05-24
tags: [baseline, optimization, HFE-7100, Drummond, design-target]
---

## Decision

**Drummond et al. 2018** is adopted as the baseline design target for the optimization phase. The "beat by 15%" criterion applies to effective thermal resistance (R_eff) at matched total pumping power, using HFE-7100 as the working fluid.

## Rationale

Two options were considered for how Drummond serves as baseline given the fluid mismatch (our validation pipeline uses water/R12; Drummond uses HFE-7100):

| Option | Description | Verdict |
|--------|-------------|---------|
| **(a) Target Drummond directly with HFE-7100** | Phase 1–2 validation uses water/R12. Phase 3 optimization switches to HFE-7100 for direct comparison against Drummond. | **Adopted** |
| (b) Find a water-MMC baseline | Use Drummond only as architectural reference; find a separate water-based manifold microchannel baseline for the 15% criterion. | Rejected — no comparably strong water-MMC anchor exists in the literature |

**Why (a):** Dielectric fluid is the industry-realistic choice for electronics cooling (non-corrosive, no shorting risk, compatible with direct-to-chip deployment). Drummond is the strongest available performance anchor for two-phase manifold microchannel cooling. The CFD framework (RPI + Eulerian) is fluid-agnostic — validation on water/R12 proves the framework; application to HFE-7100 requires only property tables and closure recalibration. Validation fluid and comparison fluid being different is methodologically standard.

## Baseline Performance Numbers (Drummond 2018)

| Metric | Best value | Sample | Conditions | Flux type |
|--------|-----------|--------|------------|-----------|
| Min R_eff | 5.6 x 10^-6 m^2 K/W | C (15 x 300 um) | G = 2900 kg/m^2 s, HFE-7100 | Device (= base in this experiment) |
| Max q"_base | 910 W/cm^2 | C (15 x 300 um) | G = 2900 kg/m^2 s | Device (= base) |
| Max h_wall | 43,300 W/m^2 K | A (15 x 35 um) | G = 2900 kg/m^2 s | — |
| Pressure drop at max q" | < 162 kPa | C | G = 2900 kg/m^2 s | — |
| Chip-to-fluid DT at max q" | < 47 C | C | G = 2900 kg/m^2 s | — |

**15% improvement target:** R_eff < 4.8 x 10^-6 m^2 K/W at equivalent or lower pumping power, or equivalent R_eff at >= 15% lower pumping power.

## Dependencies

- **Closure recalibration for HFE-7100:** RPI closure parameters (N_ref, bubble departure diameter, contact angle) are fluid-dependent. Need to identify an HFE-7100 boiling closure source with local measurements. The Garimella group has published HFE-7100 work — targeted search required. See [[open_questions]] #12.
- **Property tables:** HFE-7100 saturation properties at relevant pressures (1–2 bar). Available from 3M datasheets.

## Cross-References

- [[Drummond2018_manifold_microchannel]]
- [[Ozguc2024_topology_optimization]]
- [[open_questions]]
- [[motivation_for_CFD_approach]]
