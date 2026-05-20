---
title: "Plain-Language Explanation of the Project"
type: communication
last_updated: 2026-05-20
tags: [communication, explanation, audience-facing, physics-first]
---

# Plain-Language Explanation of the Project

*Last updated: after 3 ingests (Hall & Mudawar 2000, Krepper & Rzehak 2011, Qu & Mudawar 2003)*

*Purpose: This is the canonical long-form physics-first explanation of the project. Used for explaining the work to non-specialists, reviewers, interviewers, and audiences. Shorter audience-specific versions (elevator pitch, interview answer, poster abstract) derive from this.*

---

## The fundamental problem

A modern AI chip — an NVIDIA H100, a B200 — dissipates somewhere between 700 and 1000 watts of heat. That heat comes from billions of transistors switching billions of times per second; every switch loses a tiny bit of energy as heat. Now look at the chip: it's roughly the size of a postage stamp, maybe 4 cm². So you're trying to dump 700–1000 watts out of an area smaller than your thumbnail. That's a heat flux of around 200–500 watts per square centimeter.

For comparison: the surface of a stovetop burner on high is about 10 W/cm². The skin of a spacecraft re-entering the atmosphere experiences around 100 W/cm². You're trying to cool something that, locally, generates more heat per unit area than a spacecraft heat shield encounters. And unlike the heat shield, the chip has to stay below about 85°C or it dies.

So the question is: **how do you move that much heat away, that fast, without letting the chip overheat?**

## Why air isn't enough anymore

Air is a lousy coolant. Its density is low, its specific heat is low, its thermal conductivity is low. To move 1000 watts using air at reasonable temperature differences, you'd need fans the size of dinner plates moving hurricane-force winds across the chip. Server racks today are already at the limit of what air can do — that's why data centers sound like jet engines.

The thermal physics here is captured by Newton's law of cooling:

**q = h × A × ΔT**

You're trying to move heat q out of an area A with some temperature difference ΔT between the chip and the coolant. The heat transfer coefficient h tells you how good your coolant is. For forced air convection, h is maybe 100 W/m²·K. To remove 1000 W from 4 cm² with that h, you'd need a temperature difference of 25,000 K. Which is, obviously, impossible.

So you switch to liquid. Water has h values around 5,000–20,000 W/m²·K in forced convection. Suddenly the same job needs only a 25–100 K temperature difference. Possible, but still not great when your chip is already running at 65°C and the failure threshold is 85°C — you only have 20 K of headroom.

## Why two-phase cooling

Here's where the physics gets interesting. When a liquid *boils* — actually changes phase from liquid to vapor — it absorbs a huge amount of energy without changing temperature. That's latent heat. For water, vaporizing 1 gram absorbs about 2,260 joules. Heating that same 1 gram of liquid water by 1°C absorbs only 4.18 joules. The latent heat is 540 times larger than the sensible heat per degree.

So if you can get your coolant to *boil* at the chip surface — not flow over it, but actually nucleate vapor bubbles right there at the hot wall — you tap into latent heat. The heat transfer coefficients for boiling are enormous: 50,000 to 200,000 W/m²·K, sometimes higher. Your 1000-watt chip can now be cooled with a temperature difference of just 5–10 K. You have headroom again.

This is what "two-phase cooling" means. The fluid enters as liquid, partially boils at the chip surface, and leaves as a mixture of liquid and vapor.

## But boiling is wild

Here's the problem: boiling is one of the most physically complex processes in fluid mechanics. Look at the wall of a heated channel with water flowing past it, and you see a chaos of things happening simultaneously:

A bubble nucleates at a microscopic cavity on the surface, grows by absorbing latent heat from the wall, departs into the flow, gets pushed around by the moving liquid, possibly condenses if the bulk liquid is still cool, or possibly grows further if the liquid is near saturation. Meanwhile other bubbles are doing their own thing at neighboring sites. The liquid near the wall is hotter than the bulk; the bulk might be subcooled (below boiling point) while the wall is superheated (above boiling point). The vapor and liquid have wildly different densities and viscosities. At high heat fluxes, bubbles can merge into a continuous vapor film that *insulates* the wall from the liquid — and the chip immediately overheats and fails. This catastrophic event is called the **critical heat flux**, or CHF, and avoiding it is a design constraint that has killed nuclear reactors and burned out electronics for decades.

So boiling gives you enormous heat transfer, but only if you stay in the right regime. Push too hard and the surface dries out. Operate at the wrong pressure, geometry, or flow rate and you lose efficiency. Use a dirty surface and your nucleation behavior changes.

## Why this is hard to predict

For 80 years, engineers have been trying to write down equations that predict how all of this works. The equations are called **correlations** — empirical formulas derived from experimental data that relate heat transfer coefficient, wall temperature, flow rate, fluid properties, and geometry to each other. Names like Chen, Kandlikar, Liu-Winterton, Cooper. Each one was developed by fitting curves to experimental data from specific setups.

The problem is that no two boiling setups are quite the same. A correlation developed for a 25 mm copper tube with water at atmospheric pressure does not necessarily work for a 300 µm rectangular channel with HFE-7100 at 2 bar. As channels get smaller (microchannels, hydraulic diameter under 1 mm), the physics shifts. Surface tension becomes more important than gravity. Bubbles fill the channel cross-section. Flow patterns change. The macro-scale correlations stop working.

This is exactly what Qu & Mudawar showed in their 2003 paper: they tested **11 different correlations** against water boiling in a microchannel heat sink, and **all 11 failed**. The best one got the magnitude roughly right but missed the trend entirely; the worst was off by 272%. That's not a small calibration issue — that's the physics being fundamentally different from what the correlations were built for.

## So where does CFD come in

If correlations can't predict it, you need to simulate the physics directly. **Computational fluid dynamics** with a **two-phase boiling model** means: solve the conservation equations (mass, momentum, energy) for the liquid and the vapor as two interacting fluids, with sub-models for what's happening at the wall (bubble nucleation, departure, frequency) and at the interface between phases (drag, lift, heat transfer between bubbles and liquid).

The most widely-used framework is called the **RPI wall-boiling model**, developed at Rensselaer Polytechnic Institute. It splits the heat flux leaving the wall into three parts:

- Heat that goes into making vapor (evaporative flux)
- Heat that goes into the liquid touching the wall (single-phase convective flux)
- Heat that goes into the cooler liquid that rushes in to replace a departed bubble (quenching flux)

That's a clever physical decomposition: you're saying the wall does three different things at once, and the total heat removed is the sum. Each piece has its own sub-model based on bubble physics — how often bubbles depart, how big they are when they leave, how many nucleation sites are active per unit area.

This is what Krepper & Rzehak 2011 validated. They took the full RPI model framework, applied it in a CFD solver (CFX), simulated boiling in a vertical tube with refrigerant R12 (a chemical chosen because its experimental data are exceptionally detailed — they measured radial profiles of vapor fraction, velocity, temperature, and bubble size, which water experiments rarely capture), and tested whether the model could reproduce reality. It mostly could, with one important tuning knob: the nucleation site density. That parameter — how many bubble-generating spots per square meter — is the dominant lever for matching experimental wall temperature, and it has to be calibrated against data for each pressure level.

## What Hall & Mudawar gives us

Now, two-phase boiling has a death zone we mentioned: critical heat flux. At some point, vapor production outpaces liquid resupply, the wall dries out, temperature spikes, the chip is dead. So any cold plate design has to operate safely below CHF.

Hall & Mudawar 2000 is the most accurate correlation in existence for predicting CHF in subcooled water flow boiling in round tubes. They compiled 5,544 data points from across the world's literature — the largest such database ever assembled — and derived a correlation that predicts CHF within about 10% accuracy. That's actually *better* than the experimental measurement uncertainty itself. For our project, this is the safety constraint: whatever cold plate geometry we end up designing, the operating heat flux has to stay safely below the CHF predicted by this correlation, with margin.

## What Qu & Mudawar gives us

This paper is the bridge from "boiling in tubes" to "boiling in microchannel cold plates." They built an actual heat sink — 21 parallel rectangular channels, each 231 µm wide and 713 µm deep, in a copper block 1 cm by 4.48 cm — and characterized water boiling through it across a range of flow rates. Their data are what we'll use to validate that our CFD model works for the **geometry class that matters** for our paper, after we first validate it works in principle using Krepper & Rzehak's simpler tube case.

It also gave us the killer motivational finding I mentioned: existing correlations are not just inaccurate for microchannel water boiling, they get the *trend* wrong. The heat transfer coefficient *decreases* with quality in microchannels (the opposite of macroscale behavior), and no existing correlation captures that. This means design optimization based on correlations is fundamentally unreliable in this regime, and CFD is the only credible path.

## Putting it all together: what we're trying to do

You're building a computational framework that does three things:

**First**, simulate two-phase boiling flow inside a cold plate geometry using CFD with the RPI wall-boiling model. This means solving the conservation equations for liquid and vapor phases simultaneously, with sub-models capturing what happens at the bubble scale near the heated wall.

**Second**, validate that the model is trustworthy. We do this in two stages: against Krepper & Rzehak's DEBORA case (which proves the RPI model setup is correct in a simple, well-instrumented geometry), and against Qu & Mudawar's microchannel heat sink data (which proves the model works for the geometry type we actually care about). The Hall & Mudawar correlation gives us the safety boundary — operate below CHF, always, with margin.

**Third**, once the model is validated and trustworthy, use it to *optimize* the cold plate design. Sweep through different channel widths, depths, manifold geometries, flow rates, working fluids — find combinations that move heat better with less pumping power, while staying away from CHF. This is where machine learning comes in eventually: train a surrogate model on the CFD results so you can explore the design space orders of magnitude faster than running full simulations.

The end goal is a cold plate design — a specific geometry, with specific operating conditions — that beats published baselines for cooling AI chips. That's the paper. And along the way you build a reusable computational pipeline that companies like ACT, JetCool, and the hyperscalers actually need but rarely have built rigorously, because most of this work in industry happens with correlations that we now know don't work for this regime.

## The one-paragraph version

Modern AI chips dump so much heat into so small an area that conventional cooling fails. The only physics that can handle the load is **boiling**, because phase change absorbs enormous energy without raising temperature. But boiling in the tiny channels needed for cold plates is poorly predicted by existing equations — they were developed for larger tubes and different fluids, and they get the answer wrong, sometimes catastrophically wrong. You're building a CFD-based framework that simulates the boiling physics directly, validates against benchmark experiments to prove it's trustworthy, and then uses that validated model to design better cold plates than anyone has published. The papers you've read so far establish the safety boundary (Hall & Mudawar — CHF limits), the validation method (Krepper & Rzehak — RPI model in a benchmark geometry), and the application case (Qu & Mudawar — water boiling in the microchannel geometry class that matters). The rest of the project builds the framework, runs the optimization, and writes the paper.
