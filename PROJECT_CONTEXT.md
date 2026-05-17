# Two-Phase Cold Plate Optimization — Project Context

> Save this file as `PROJECT_CONTEXT.md` at the root of your Claude Code project. Reference it explicitly in your first session ("Read PROJECT_CONTEXT.md and confirm understanding before we start"). Update it as the project evolves.

---

## Researcher Profile

I am Avinash Nayal, PhD candidate in Mechanical Engineering at the University of Oklahoma (finishing 2026). My research focuses on thermal management of high-heat-flux systems. Background directly relevant to this project:

- **B.Tech thesis at Institute for Plasma Research (IPR), 2017** — Built an FEM model in ANSYS APDL for subcooled flow boiling in the ITER divertor at 10+ MW/m² one-sided heat flux. Implemented a piecewise boiling curve using Sieder-Tate (single-phase), Bergles-Rohsenow (ONB), Araki, Tong-75, and Marshall-98 (CHF) correlations as temperature-dependent surface conditions. Validated against electron-beam calorimetry within ~10%. Developed original linear-regression peaking-factor correlations for swirl-tube and straight-flow geometries.
- **PhD at OU** — Designed and tested air, liquid, PCM, and hybrid cooling rigs for high-power battery cell arrays at <2 °C non-uniformity. Built Python data-reduction pipelines that cut analysis time 40%+.
- **ORNL GRO Internship (Jan–May 2025)** — Python-based thermal resistance modeling framework using first-principles phonon transport (Quantum ESPRESSO + Boltzmann transport equation) for GaN under mechanical strain.

**Strengths to lean on**: ANSYS Fluent and APDL, subcooled flow boiling correlation libraries, validation discipline, parametric simulation workflows, Python automation, conjugate heat transfer modeling.

**Areas where I have less depth and want Claude Code's support**: Eulerian-Eulerian multiphase setup at production scale in Fluent, microchannel-specific boiling regimes (vs. macrochannel), Bayesian optimization frameworks, ML surrogate modeling.

---

## Project Goal

Develop a fully validated, open-source computational framework for design optimization of **two-phase cold plates targeting AI accelerator and data center cooling**. Target heat flux range 200–500 W/cm², matching NVIDIA H100 (~700 W TDP), B200 (~1000 W TDP), and ACT's recently launched 7.5 kW / 300 W/cm² two-phase cold plate.

**Deliverables**:
1. A reusable Python+Fluent design optimization codebase, version-controlled and tested.
2. A first-author research paper (target venue: *International Journal of Heat and Mass Transfer*, *Applied Thermal Engineering*, or *International Journal of Multiphase Flow*).
3. A demonstrated Pareto-optimal cold plate design that improves on a published baseline by a meaningful margin.

**Industry alignment**: Direct relevance to Advanced Cooling Technologies (ACT), Cooler Master, JetCool, and in-house thermal teams at NVIDIA, AMD, Microsoft, Meta, Google.

---

## Technical Scope

### Physics
- Subcooled flow boiling in mini- and micro-channels (D_h = 0.5–3 mm)
- Single-phase forced convection through ONB → fully-developed nucleate boiling, with explicit attention to approach-to-CHF margin
- Conjugate heat transfer (Cu or Al cold plate body + working fluid)
- Pressure drop and pumping-power accounting

### Working Fluids
- **Phase 1 (validation)**: deionized water — best-documented benchmark data
- **Phase 2 (industry application)**: dielectric fluid (HFE-7100 or Novec 649) — what real data center two-phase cold plates use due to electrical-isolation requirements

### Modeling Approach
- **Primary solver**: ANSYS Fluent (2024 R1 or later). Confirm multiphase + RPI wall-boiling availability with my OU academic license before assuming.
- **High-fidelity model**: Eulerian-Eulerian multiphase with RPI wall-boiling model.
- **Mid-fidelity option**: empirical heat-transfer-coefficient boundary condition driven by a Python correlation library through a UDF — this is the same approach I used in APDL on ITER, scaled to 3D Fluent. Useful for fast design sweeps.
- **Lowest-fidelity baseline**: 1D segmented analytical model in pure Python — built first, used as the sanity-checker for all higher-fidelity work.
- **Driver**: Python through `pyfluent` (Ansys' official Python API). Geometry parameterized via SpaceClaim or Workbench parameters.

### Validation Targets (priority order)
1. **Mudawar group subcooled flow boiling channel data** (Purdue PUREES Lab) — extensive published water-in-rectangular-channel data with broad parameter range. Best-documented benchmark.
2. **Kandlikar microchannel flow boiling correlations** and underlying experimental data.
3. **Mandel & Garimella (Purdue) manifold-microchannel two-phase cold plate data** — closest to industrial cold-plate geometry.
4. Recent (2022–2025) two-phase cold plate publications from Cooler Master, JetCool, ACT — for industry-realistic operating conditions.

**Validation philosophy is non-negotiable**: every model must reproduce a published benchmark within stated experimental uncertainty before being used for design exploration. This is how I learned to do simulation at IPR (calorimetry-validated boiling model) and it is how this paper will pass review.

### Design Variables (optimization)
- Channel hydraulic diameter (0.5–3 mm)
- Channel aspect ratio (0.5–5)
- Fin density / pitch
- Manifold configuration (single-pass, U-flow, manifold-microchannel)
- Mass flux
- Inlet subcooling

### Objectives (multi-objective)
- Maximize heat removal (W/cm²) at fixed wall superheat
- Minimize junction-to-fluid thermal resistance
- Minimize pumping power
- Maintain CHF safety margin (≥1.5× operating heat flux)

Pareto front analysis is the desired output, not a single "optimal" design.

---

## Code Architecture

```
two-phase-cold-plate/
├── README.md
├── PROJECT_CONTEXT.md       # this document
├── pyproject.toml
├── src/two_phase_cp/
│   ├── correlations/        # boiling correlations, type-hinted, unit-tested
│   ├── analytical/          # 1D segmented model
│   ├── geometry/            # parametric cold plate definitions
│   ├── solver/              # pyfluent wrappers, BC setup, models
│   ├── postproc/            # results extraction
│   ├── optimization/        # Bayesian optimization loop
│   └── surrogate/           # ML surrogate (Phase 5)
├── benchmarks/
│   ├── mudawar_2009/
│   ├── kandlikar_2005/
│   └── mandel_2024/
├── designs/                 # JSON specs for parametric runs
├── results/
├── notebooks/               # exploratory analysis, paper figures
├── tests/                   # pytest, esp. for correlations module
└── docs/
```

### Tooling
- Environment: `uv` or Poetry
- Python 3.11+
- Core: `numpy`, `scipy`, `pandas`, `matplotlib`
- Ansys: `ansys-fluent-core` (pyfluent)
- Optimization: `BoTorch` (preferred for multi-objective) or `Optuna`
- ML (Phase 5): `scikit-learn` for GP surrogates, `PyTorch` for NN surrogates
- Testing: `pytest`
- Version control: `git` from day one, conventional commits

---

## Execution Phases

### Phase 1 — Foundation (Weeks 1–2)
- Initialize repo with the structure above
- Set up environment, pyfluent install, confirm ANSYS license + multiphase capability
- Implement and unit-test the **correlation library**:
  - Single-phase: Dittus-Boelter, Sieder-Tate, Gnielinski
  - ONB: Bergles-Rohsenow, Hsu, Davis-Anderson
  - Subcooled boiling: Chen, Liu-Winterton, Kandlikar
  - Pool boiling: Cooper, Rohsenow
  - CHF: Bowring, Katto-Ohno, Mudawar inlet condition correlation
  - Pressure drop: Friedel, Lockhart-Martinelli, Mishima-Hibiki
- I will provide my ITER APDL correlation implementations as a starting point where they overlap

### Phase 2 — 1D Analytical Baseline (Week 2–3)
- Build segmented 1D model: input (geometry, mass flux, inlet conditions, heat flux profile) → output (channel-wise wall temperature, HTC, vapor quality, pressure drop)
- This is the sanity-checker for all CFD work that follows
- Includes regime-detection logic (single-phase, ONB, partial boiling, fully developed nucleate boiling, CHF approach)

### Phase 3 — CFD Validation (Weeks 3–5)
- Pick **Mudawar 2009 subcooled water channel** as the first benchmark
- Build parametric Fluent model with Eulerian-Eulerian + RPI wall-boiling
- Reproduce published heat-flux vs. wall-superheat curve within experimental uncertainty
- Mesh independence study with documented convergence
- **Gate**: no design exploration until validation is locked in

### Phase 4 — Parametric Study (Weeks 6–7)
- Define base cold plate geometry (manifold-microchannel, copper, ~50 mm × 50 mm footprint matching GPU die size)
- Latin hypercube sample of 30–50 design points
- Python-orchestrated batch runs through pyfluent
- Manual response-surface analysis first — to build physical intuition before handing it to an optimizer

### Phase 5 — Bayesian Optimization (Weeks 8–10)
- Multi-objective Bayesian optimization with BoTorch
- 50–100 simulation evaluations
- Pareto front analysis
- Verification of Pareto-optimal designs at finer mesh

### Phase 6 — Surrogate + Paper (Weeks 11–14)
- Train Gaussian Process and a small NN surrogate on the simulation dataset
- Compare optimization speed and accuracy with/without surrogate
- Draft paper, generate publication-quality figures

---

## Success Criteria
- Correlation library passes unit tests against textbook values
- 1D analytical model matches CFD within ~15% in single-phase regime
- CFD validation case reproduces Mudawar benchmark within experimental uncertainty
- Pareto-optimal design improves on a published baseline by ≥15% in at least one objective
- Reusable, documented, version-controlled codebase
- First-author manuscript draft by Week 14

---

## Constraints and Watchouts

- **Solo computational work** — no experimental resources. Validation comes from published benchmarks only.
- **Compute budget** — workstation-class machine, parallel runs but not HPC. Each Fluent run scoped to 2–12 hours wall time. Optimize aggressively before launching 100-point campaigns.
- **License** — ANSYS Academic through OU. Confirm Fluent multiphase + RPI wall-boiling are included before committing to that approach.
- **Don't fabricate physics**. Every correlation cited to source paper. Every model setting justified from Fluent documentation or peer-reviewed literature.
- **Don't skip validation**. The model is not "done" until it reproduces a benchmark within stated uncertainty.
- **Don't over-engineer the optimization framework** before the physics is right. Phases are sequential for a reason.

---

## What I Need From Claude Code Right Now (Session 1)

1. Read this document and confirm understanding. Flag anything unclear or that you'd push back on.
2. Initialize the repo with the structure above. Use `uv` for environment management.
3. Set up `pyproject.toml` with the dependency list above.
4. Stub out `src/two_phase_cp/correlations/` with each correlation as a separate, type-hinted, docstring-cited function. Start with: Dittus-Boelter, Sieder-Tate, Gnielinski, Chen, Kandlikar, Bergles-Rohsenow ONB. Each function gets a `pytest` unit test against a textbook reference value.
5. Write the **1D segmented analytical model** as the first usable artifact. Input: geometry + operating conditions. Output: channel-wise wall temperature, HTC, vapor quality, pressure drop. This becomes my sanity-checker for everything that follows.
6. Provide a brief written plan (markdown, in `docs/phase2_validation_plan.md`) for the Mudawar 2009 benchmark setup before we touch Fluent.

When you don't know something specific (e.g. exact form of a correlation, a Fluent model setting), **say so and ask**. I will provide my ITER APDL files, correlation references, or specific paper PDFs as needed. Don't guess.

---

## Working Style Preferences

- Test-driven where it matters (correlation library, analytical model)
- Conventional commits, small focused PRs
- Docstrings cite source papers
- Paper-quality figures from day one (matplotlib with consistent style)
- I will review code before merging — explain non-obvious choices in the commit message
- Ask before installing new dependencies beyond what's listed