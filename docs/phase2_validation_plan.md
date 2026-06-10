---
title: "CFD Validation Plan (phase2_validation_plan)"
last_updated: 2026-06-09
status: skeleton — §2 envelope filled; §1 success criterion still EXTRACT
gates: no design exploration until both stages below pass and are documented in wiki/synthesis/validation_status.md
---

# CFD Validation Plan

Filename retained per PROJECT_CONTEXT Task 6. Despite the "phase2" name, this
is the Phase 3 CFD validation plan (PROJECT_CONTEXT phase numbering: Phase 2 =
1D analytical baseline, Phase 3 = CFD validation). It is the gate before any
Fluent work and before any design exploration.

---

## 0. Benchmark reconciliation (read this first)

PROJECT_CONTEXT Task 6 names a "Mudawar 2009" benchmark. That reference is
stale and ambiguous — flagged in literature_review.md (the Mudawar group's
2008–09 microchannel work used HFE-7100, not water). The authoritative
benchmark set is the two-stage registry in CLAUDE.md, which supersedes
"Mudawar 2009":

* **Stage 1 — RPI shakedown:** Krepper & Rzehak 2011, DEBORA case.
* **Stage 2 — Cold-plate geometry:** Qu & Mudawar 2003, saturated water
  microchannel heat sink.

**Why two stages, in this order.** You validate the machinery
(Eulerian-Eulerian + RPI wall-boiling) in a simple, exceptionally
well-instrumented geometry first — DEBORA measured radial
void/velocity/temperature profiles that water experiments rarely capture —
then carry the validated setup to the geometry class that matters (parallel
microchannels, water). Reversing the order would conflate "is my RPI setup
correct?" with "does RPI work at this scale?" — two failures that look
identical in the output.

---

## 1. Stage 1 — Krepper & Rzehak 2011 (DEBORA): RPI shakedown

**What to reproduce:** wall-superheat vs. heat-flux curve and the axial (and
radial, if attempted) void-fraction profile.

**Working fluid:** R-12. **Solver in paper:** CFX. **Our solver:** Fluent — so
this is also a solver-translation check, not a pure replication.

**Geometry (resolved):** vertical heated tube, ID 19.2 mm, heated length
3.5 m, R-12, G = 2000–3000 kg/m²·s, system pressure 1.46–2.62 MPa. Radial
profiles (void fraction, velocity, temperature) measured at end of heated
length. CLAUDE.md previously said "vertical annulus" — corrected to "vertical
tube" in this commit.

**Mesh approach:** quasi-2D axisymmetric sector (azimuthal symmetry of the
round tube). This is the simplest geometry that exercises the full RPI closure
set, which is the point of Stage 1.

**EXTRACT:** confirm RPI sub-model correspondence between CFX and Fluent
(wall-partitioning, bubble departure diameter, nucleation site density model) —
this is where D3 (IMECE 2024, VOF-vs-RPI in Fluent) becomes required reading.

**Key tuning knob:** nucleation site density. Krepper & Rzehak's central
finding is that this parameter dominates the wall-temperature match and must be
calibrated per pressure level. Treat it as the one legitimate calibration lever;
everything else should fall out of the physics. (This is the same discipline as
exposing correlation calibration coefficients as kwargs — calibrate openly
against data, don't bury fitted constants.)

**Success criterion:** EXTRACT from paper — match wall-superheat curve and
void-fraction profile within the experimental uncertainty Krepper & Rzehak
themselves quote. State the number here once read.

**Gates:** RPI model setup. No move to Stage 2 until this passes and is logged
in validation_status.md.

---

## 2. Stage 2 — Qu & Mudawar 2003: cold-plate geometry

**Geometry (locked, from wiki):** 21 parallel rectangular channels, 231 µm
wide × 713 µm deep, copper block 1 cm × 4.48 cm, DI water, saturated flow
boiling. Channel depth: 713 µm per abstract and Table 3; body text p. 2757
states 712 µm — 1 µm internal inconsistency in the paper, noted but
non-material. We use 713 µm (abstract value).

**Operating envelope:**

| Parameter | Value | Source |
|-----------|-------|--------|
| Mass flux G | 135–402 kg/m²·s | Qu & Mudawar 2003, abstract + Table 2 |
| Inlet temperature T_in | 30 and 60 °C | Qu & Mudawar 2003, test matrix |
| Outlet pressure P_out | 1.17 bar | Qu & Mudawar 2003, test conditions |
| Heat flux q″_eff | ~30–120 W/cm² (approximate, figure-read from Fig. 5) | Qu & Mudawar 2003, Fig. 5 (T_in=60 °C, G=255 kg/m²·s series) |
| Exit quality x_e | 0–0.20 | Qu & Mudawar 2003, p. 2761 (tests terminated at x_e ≈ 0.2); Fig. 6 axes confirm |
| h_tp range | 20–45 kW/m²·K | Qu & Mudawar 2003, p. 2763 (stated) |

**Heat-flux basis (important).** q″_eff = P_W / A_t, where A_t is the top
planform area 1.0 × 4.48 cm² (Eq. 1, p. 2761). This equals device heat flux
per our wiki convention — no conversion needed. The paper also defines q″_ch
(channel-perimeter basis, Eq. 9), used only for their boiling number; do not
conflate with q″_eff.

**Upper q″ bound.** The paper states no tabulated peak q″_eff. The ~120 W/cm²
upper bound is set by the x_e ≈ 0.2 test-termination criterion (p. 2761), not
a stated flux ceiling. Mark as approximate in any comparison.

**Inlet state.** Subcooled: T_in = 30 and 60 °C vs. T_sat ≈ 105 °C at P_out =
1.17 bar. Regime span across a single test run: subcooled inlet → x_e = 0
(saturation) → saturated flow boiling to x_e ≈ 0.2.

**Quality regime scoping.** x_e max ≈ 0.2 means Stage 2 stays in the
low-quality saturated/annular regime and never approaches dryout — consistent
with the finding (§3 below) that saturated-CHF (Katto-Ohno) is flag-only for
Stage 2.

**What to reproduce:** Nu and pressure drop vs. Re, and the two-phase
performance map — including the HTC-decreases-with-quality trend that every
correlation misses (this trend is the whole point; if CFD reproduces it where
correlations cannot, that is the validation win).

**Success criterion:** EXTRACT — reproduce within Qu & Mudawar's stated
experimental uncertainty.

**Gates:** cold-plate design exploration. This is the hard gate in
PROJECT_CONTEXT and CLAUDE.md.

---

## 3. Why this plan comes before filling the 1D-model correlation gaps

This is the scoping dependency, made explicit. The two stacked gaps in the
Phase-2 1D model — saturated CHF (Katto-Ohno, unfilled) and the FDB asymptote
(BR incipience curve standing in, wrong at high superheat) — both live in the
saturated / high-flux region. Qu & Mudawar 2003 is a saturated benchmark. So
Stage 2's operating envelope lands directly in the 1D model's two gap regions.

Therefore the envelope extraction above is what scopes the gap-filling:

* If the Qu & Mudawar envelope approaches CHF, Katto-Ohno must be accurate
  there → higher priority, tighter validation.
* If it sits well below CHF, the saturated-CHF gap is a flag-only safety
  boundary for now, not a precision requirement.
* The exit-quality range tells you how far into developed boiling the FDB
  asymptote is actually exercised — i.e. how wrong the BR stand-in is allowed
  to be before it corrupts the sanity-check.

**Sharpened result (2026-06-05).** With the envelope partially filled, neither
logged gap binds Stage 2:

* **Saturated CHF (Katto-Ohno):** Qu & Mudawar's experiments do not approach
  CHF — they terminate at moderate exit qualities well below burnout. The
  saturated-CHF gap remains a flag-only safety boundary, not a precision
  requirement for the benchmark comparison.
* **FDB asymptote (BR stand-in):** The Qu & Mudawar operating envelope is
  saturated convective-dominant, not nucleate-dominant — the regime where the
  FDB curve matters least.
* **Structural limit:** The 1D model cannot reproduce the h_tp-decreases-with-
  quality trend by construction, because it is built from the superposition
  correlations that Qu & Mudawar 2003 invalidated (see correlation_anatomy §4b).
  The 1D model's role at Stage 2 conditions is pre-flight sanity check
  (magnitude, regime transitions, CHF margin), not trend reproduction — that is
  CFD's job.

The 1D model is not gated to reproduce the benchmark within experimental
uncertainty — that is CFD's job. The 1D model's job is to run cleanly at the
benchmark conditions as a cheap pre-flight sanity check before expensive CFD,
and to do so it must at minimum not be grossly wrong in the regimes the
benchmark exercises.

---

## 4. Open items to resolve before touching Fluent

1. **EXTRACT** remaining operating-envelope numbers: §1 success criterion
   (experimental uncertainty). §2 envelope now fully filled (G, T_in, P_out,
   q″_eff, x_e, h_tp, channel depth, heat-flux basis); DEBORA geometry
   now filled.
2. ~~**Resolve** the DEBORA tube/annulus CONFLICT (§1).~~ **RESOLVED** —
   vertical tube, ID 19.2 mm. CLAUDE.md corrected in this commit.
3. **ANSYS license check** — confirm Fluent multiphase + RPI wall-boiling are
   in the OU academic license before committing to the E-E path.
   PROJECT_CONTEXT flags this as unconfirmed. If unavailable, the
   empirical-HTC-via-UDF fallback (the ITER-APDL approach) is the
   contingency — which is partly why C3/D3 stay on the reading list.
4. **Ingest D3** (IMECE 2024, VOF-vs-RPI in Fluent) — gated to this plan per
   literature_review.md's own note ("required reading before we commit to the
   high-fidelity model"). This is the next genuine paper pull.
5. **Confirm** what data in each paper is actually digitizable (published curves
   vs. tabulated points) — determines whether validation is point-wise or
   trend-wise.

---

## 5. Gate summary

| Stage | Benchmark | Reproduce | Gates | Status |
|-------|-----------|-----------|-------|--------|
| 1 | Krepper & Rzehak 2011 (DEBORA) | wall-superheat vs q″; void profile | RPI model setup | not started |
| 2 | Qu & Mudawar 2003 | Nu, Δp vs Re; two-phase map | design exploration | not started |

**No design exploration until both gates pass and are documented in
wiki/synthesis/validation_status.md (CLAUDE.md, non-negotiable).**
