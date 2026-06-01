---
title: "CFD Validation Plan (phase2_validation_plan)"
last_updated: 2026-06-01
status: skeleton — open items marked EXTRACT must be filled from the source papers before Fluent setup begins
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

**EXTRACT:** confirm RPI sub-model correspondence between CFX and Fluent
(wall-partitioning, bubble departure diameter, nucleation site density model) —
this is where D3 (IMECE 2024, VOF-vs-RPI in Fluent) becomes required reading.

**Key tuning knob:** nucleation site density. Krepper & Rzehak's central
finding is that this parameter dominates the wall-temperature match and must be
calibrated per pressure level. Treat it as the one legitimate calibration lever;
everything else should fall out of the physics. (This is the same discipline as
exposing correlation calibration coefficients as kwargs — calibrate openly
against data, don't bury fitted constants.)

> **CONFLICT (resolve from the paper):** Your own docs disagree on DEBORA's
> geometry. CLAUDE.md registry says *vertical annulus*; plain_language_explanation.md
> says *vertical tube*. Published DEBORA is, to my knowledge, a vertical heated
> tube — but I am not certain enough to overwrite your registry. Resolve by
> reading Krepper & Rzehak 2011 §experimental setup and correct whichever doc is
> wrong. This matters: the mesh and boundary-condition topology differ between
> the two.

**Success criterion:** EXTRACT from paper — match wall-superheat curve and
void-fraction profile within the experimental uncertainty Krepper & Rzehak
themselves quote. State the number here once read.

**Gates:** RPI model setup. No move to Stage 2 until this passes and is logged
in validation_status.md.

---

## 2. Stage 2 — Qu & Mudawar 2003: cold-plate geometry

**Geometry (locked, from wiki):** 21 parallel rectangular channels, 231 µm
wide × 713 µm deep, copper block 1 cm × 4.48 cm, DI water, saturated flow
boiling.

**Operating envelope (EXTRACT — do not invent):**

| Parameter | Value | Source |
|-----------|-------|--------|
| Mass flux G | EXTRACT range | Qu & Mudawar 2003 Table __ |
| Inlet subcooling / inlet temperature | EXTRACT | Qu & Mudawar 2003 Table __ |
| System pressure | EXTRACT | Qu & Mudawar 2003 §__ |
| Heat flux q″ range and basis (channel-base vs. footprint — reconcile to the wiki's device-heat-flux convention) | EXTRACT | Qu & Mudawar 2003 Table __ |
| Exit quality x_eq range | EXTRACT | Qu & Mudawar 2003 Table __ |

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

The 1D model is not gated to reproduce the benchmark within experimental
uncertainty — that is CFD's job. The 1D model's job is to run cleanly at the
benchmark conditions as a cheap pre-flight sanity check before expensive CFD,
and to do so it must at minimum not be grossly wrong in the regimes the
benchmark exercises. Extracting the envelope is what turns "the gaps are bad in
the abstract" into "the gaps must be this good, at these conditions."

---

## 4. Open items to resolve before touching Fluent

1. **EXTRACT** all operating-envelope numbers (§1, §2) from the source papers.
2. **Resolve** the DEBORA tube/annulus CONFLICT (§1).
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
