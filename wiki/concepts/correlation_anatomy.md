---
title: "Correlation Anatomy"
type: concept
last_updated: 2026-06-01
prerequisites: [two_phase_fundamentals]
tags: [concept, correlations, dimensionless-groups, superposition, envelope, failure-modes]
---

## Correlation Anatomy

What a heat-transfer correlation actually is, the dimensionless vocabulary it is written in, how multi-mechanism correlations are assembled, and the two distinct ways they fail. Companion to [[two_phase_fundamentals]] (which covers the boiling curve and regimes) — this page is about the equations that predict points on that curve, not the curve itself.

### 1. A correlation is a bounded curve fit, not a law

A heat-transfer correlation is an empirical formula fitted to a specific experimental database. It is not a physical law — it is interpolation within the conditions that produced it. Every correlation carries an implicit envelope: the fluid(s), hydraulic-diameter range, pressure range, mass-flux range, quality range, and Reynolds range of the data it was fitted to. Inside that envelope the correlation interpolates; outside it, it extrapolates, and extrapolation error is unbounded and silent unless you check for it.

This is why each correlation in `correlations/` is wrapped in a `CorrelationEnvelope`. The envelope is not bookkeeping — it is the structural defense against the dominant failure mode in this field (§4). A correlation with no stated envelope is a correlation you cannot trust off-paper.

The single most important habit this page is trying to instill: **before reading a correlation's value, read its envelope.** A confidently-returned number from an out-of-envelope correlation is the most dangerous output the model can produce, because nothing about the number itself signals that it is wrong.

### 2. The dimensionless vocabulary

Correlations are written in dimensionless groups so that a fit from one fluid/scale can (in principle) transfer to another. Three groups carry single-phase convection; three more carry the boiling and small-channel physics.

#### Single-phase trio

| Group | Definition | Physical meaning | Role |
|-------|-----------|-----------------|------|
| Re (Reynolds) | $Re = G D_h / \mu = \rho u D_h / \mu$ | inertial / viscous forces | sets laminar/turbulent; input |
| Pr (Prandtl) | $Pr = \mu c_p / k = \nu / \alpha$ | momentum / thermal diffusivity | fluid property (not flow); water ~ 5.4 at 25 C, ~ 1.75 at 100 C |
| Nu (Nusselt) | $Nu = h D_h / k$ | convective / conductive transfer at wall | output — back out $h = Nu \cdot k / D_h$ |

The standard single-phase form is Dittus-Boelter, $Nu = 0.023\,Re^{0.8}Pr^{n}$ ($n=0.4$ heating, $0.3$ cooling) [Incropera]. It is valid only for fully turbulent flow — the model flags $Re < 10^4$ as outside the DB envelope (use Gnielinski in the transition band).

#### Two-phase / small-channel trio

| Group | Definition | Physical meaning |
|-------|-----------|-----------------|
| Bo (Boiling number) | $Bo = q'' / (G\, h_{fg})$ | evaporative mass flux / total mass flux — a dimensionless wall heat flux. High Bo -> nucleate-boiling-dominated |
| Co (Convection number) | $Co = \left(\tfrac{1-x}{x}\right)^{0.8}\!\left(\tfrac{\rho_g}{\rho_f}\right)^{0.5}$ | Kandlikar's modified Martinelli parameter [Kandlikar 1990]; low Co (high quality) -> convective-dominant, high Co -> nucleate-dominant |
| $N_{conf}$ (Confinement) | $N_{conf} = \tfrac{1}{D_h}\left[\tfrac{\sigma}{g(\rho_f-\rho_g)}\right]^{0.5} = Bd^{-1/2}$ | surface tension / buoyancy; the dimensionless marker of the macro->micro transition. $N_{conf} \gtrsim 0.5$ -> bubbles confined -> microchannel physics. See [[two_phase_fundamentals]] |

**Naming-collision warning.** Two different groups are written "Co" in the literature: Kandlikar's Convection number (above) and the Confinement number (here written $N_{conf}$ to disambiguate; also appears as $Co$, $Bd^{-1/2}$, or $\sqrt{Co_{conf}}$). They are unrelated. When reading a correlation, confirm which one a "Co" denotes from its definition, not its symbol.

A convention note that matters for this project: the $q''$ in $Bo$ is the local wall heat flux, not the device heat flux used as the wiki's default reporting basis ([[Drummond2018_manifold_microchannel]]). Correlations live in wall-heat-flux space; the device-heat-flux convention is a reporting layer on top.

### 3. How multi-mechanism correlations are assembled: superposition

Flow-boiling HTC correlations almost all assume that nucleate boiling and convective boiling are two separable, coexisting mechanisms whose contributions combine. This is the **superposition premise**. Three assembly forms:

1. **Additive** (the prototype, [Chen 1966]): $h_{tp} = S\,h_{nb} + F\,h_{l}$, with a convective enhancement factor $F \geq 1$ and a nucleate suppression factor $S \leq 1$.
2. **Asymptotic / power-additive:** $h_{tp} = \left(h_{nb}^{\,n} + h_{cb}^{\,n}\right)^{1/n}$ (e.g. Liu-Winterton, $n=2$). The 1D model's subcooled partial-boiling interpolation is power-additive in this family [Bergles & Rohsenow 1964].
3. **Larger-of:** $h_{tp} = \max(h_{NBD}, h_{CBD})$, switching on Co (Kandlikar's NBD/CBD branches [Kandlikar 1990]).

All three are built on macroscale data, where the HTC rises with vapor quality — as the liquid film thins and velocity climbs, the convective term grows. That rising-with-quality behavior is baked into the functional form.

### 4. The two failure modes

#### 4a. Out-of-envelope extrapolation (a usage failure)

The correlation is sound; it is being applied outside its fitted database. Error is unbounded and unsignaled. This is what the `CorrelationEnvelope` guards against. [Qu & Mudawar 2003] is the canonical demonstration: 11 published correlations tested against water boiling in a microchannel heat sink, all 11 failed — the best captured magnitude but missed the trend, the worst was off by 272%. Fixable by staying in-envelope (or by choosing a correlation whose envelope contains your operating point).

#### 4b. Structural trend reversal (a functional-form failure)

This one is not fixable by refitting. In microchannels the HTC decreases with quality — the opposite of the macroscale behavior that superposition is built on [Qu & Mudawar 2003; Kim & Mudawar 2013]. A superposition correlation whose convective term increases in $x$ therefore has the slope backwards. No re-tuning of constants repairs a form whose derivative points the wrong way. Kim & Mudawar 2013 — the most comprehensive small-channel correlation available (10,805 pre-dryout points, 18 fluids, $D_h = 0.19$–$6.5$ mm) — still mispredicts the water-in-microchannel trend, which establishes the failure as structural rather than a matter of insufficient data.

**This distinction is the project's core defensibility argument:** 4a motivates the envelope; 4b motivates CFD. Correlation-based design optimization is unreliable in the microchannel regime not because we lack a good enough correlation, but because the superposition family is the wrong functional form there.

### 5. Validity is role-dependent, not equation-intrinsic (the BR case)

A correlation's validity is a property of the triple (equation, role, regime) — not of the equation alone. The same expression can be correct in one slot and wrong in another. The Phase-2 1D model contains a clean live example.

The subcooled partial-boiling interpolation [Bergles & Rohsenow 1964] interpolates wall superheat between single-phase forced convection and fully-developed boiling (FDB), anchored at incipience (ONB) by the BR incipience correlation ($q'' = 1082\,P^{1.156}(1.8\,\Delta T_{sat})^{2.16/P^{0.0234}}$, as implemented).

That single incipience expression currently appears in two roles:

* **Role A — incipience anchor (valid).** As the ONB anchor for the interpolation, in the subcooled near-ONB region. This is exactly what the curve is for. Verified: $T_w$ continuous through ONB (0.01–0.06% jump across the transition).
* **Role B — FDB asymptote (invalid).** The same incipience expression is reused as the fully-developed-boiling asymptote at high superheat. The incipience curve is not the developed-boiling curve: correct near onset, wrong asymptotically. <!-- TODO: verify — replace FDB stand-in with Rohsenow pool boiling or an FC-boiling fit; logged in model.py module docstring -->

The lesson generalizes past this one case: an envelope check that only asks "is this fluid/D_h/pressure in range?" is necessary but not sufficient — the correlation also has to be in the role it was fitted for. The BR incipience curve passes every envelope bound in Role B and is still wrong, because incipience and developed boiling are different physics wearing the same algebra.

## Cross-references

- [[two_phase_fundamentals]] — boiling curve, regimes, macro/micro transition (prerequisite)
- [[QuMudawar2003_microchannel_boiling_I]] — source for the 11-correlation failure and the trend-reversal finding
- [[KimMudawar2013_universal_boiling_II]] — structural-failure-persists-with-more-data evidence
- [[motivation_for_CFD_approach]] — consumes §4b as the why-CFD argument
- [[Drummond2018_manifold_microchannel]] — device- vs wall-heat-flux convention referenced in §2

## Notes

- Symbols follow [[two_phase_fundamentals]]; $G$ = mass flux, $x$ = thermodynamic quality, $D_h$ = hydraulic diameter.
- The FDB-asymptote gap (§5, Role B) and the saturated-CHF gap are both logged in `src/two_phase_cp/analytical/model.py` module docstring so a reviewer sees them, not just the cell logs.
