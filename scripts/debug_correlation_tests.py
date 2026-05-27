"""Diagnostic script for failing correlation tests.

Run: .venv/bin/python scripts/debug_correlation_tests.py

Purpose: verify hand-calculation reference values before fixing tests.
Do NOT change implementation code until root causes are identified here.
"""

import math

# ===================================================================
# 1. DITTUS-BOELTER — Re=14050, Pr=4.85, n=0.4
#    Test expects Nu ≈ 115.5 (claimed Incropera 8e Ex 8.4)
#    Code returns ~90.0
# ===================================================================
print("=" * 70)
print("1. DITTUS-BOELTER DIAGNOSTIC")
print("=" * 70)

Re = 14_050.0
Pr = 4.85

Re_08 = Re**0.8
Pr_04 = Pr**0.4
Nu_DB = 0.023 * Re_08 * Pr_04

print(f"  Re        = {Re:.0f}")
print(f"  Pr        = {Pr}")
print(f"  Re^0.8    = {Re_08:.2f}   (test comment claims 2637)")
print(f"  Pr^0.4    = {Pr_04:.4f}   (test comment claims 1.905)")
print(f"  Nu (D-B)  = 0.023 * {Re_08:.2f} * {Pr_04:.4f} = {Nu_DB:.2f}")
print(f"  Test expected: 115.5")
print()

# What Re^0.8 is needed for Nu=115.5?
Re_08_needed = 115.5 / (0.023 * Pr_04)
Re_needed = Re_08_needed ** (1.0 / 0.8)
print(f"  To get Nu=115.5, need Re^0.8 = {Re_08_needed:.1f}")
print(f"  That corresponds to Re = {Re_needed:.0f}")
print()

# Verify Gnielinski at same conditions (this test PASSES)
f = (0.790 * math.log(Re) - 1.64) ** (-2)
f8 = f / 8.0
Nu_G = f8 * (Re - 1000) * Pr / (1.0 + 12.7 * f8**0.5 * (Pr ** (2.0 / 3.0) - 1.0))
print(f"  Gnielinski at same Re,Pr: Nu = {Nu_G:.2f}  (test expects 93.6 — PASSES)")
print()
print("  DIAGNOSIS: Re^0.8 = 14050^0.8 = {:.2f}, NOT 2637.".format(Re_08))
print("  The test reference value Nu=115.5 was computed from the wrong Re^0.8.")
print("  Implementation is correct. Test expected value is fabricated.")

# ===================================================================
# 2. BERGLES-ROHSENOW — sweep delta_T_sat at several pressures
#    Test at P=70 bar, dT=10 K returns 2.4e62 (pathological)
# ===================================================================
print()
print("=" * 70)
print("2. BERGLES-ROHSENOW ONB DIAGNOSTIC")
print("=" * 70)


def bergles_rohsenow_BUGGY(P, dT):
    """BUGGY form: exponent = P^0.0234 / 0.0234 (~42). Pathological."""
    exponent = P**0.0234 / 0.0234
    return 1082.0 * P**1.156 * (1.8 * dT / P**0.0234) ** exponent


def bergles_rohsenow_FIXED(P, dT):
    """FIXED form: exponent = 2.16 / P^0.0234 (~2). Well-behaved."""
    exponent = 2.16 / P**0.0234
    return 1082.0 * P**1.156 * (1.8 * dT) ** exponent


# Show the exponent at various pressures — BUGGY vs FIXED
print("\n  Exponent comparison at various pressures:")
print(f"    {'P (bar)':>10}  {'BUGGY (P^0.0234/0.0234)':>25}  {'FIXED (2.16/P^0.0234)':>25}")
for P in [1.0, 10.0, 50.0, 70.0, 100.0, 138.0]:
    buggy = P**0.0234 / 0.0234
    fixed = 2.16 / P**0.0234
    print(f"    {P:10.1f}  {buggy:25.2f}  {fixed:25.4f}")

# Sweep dT at P=1 bar — FIXED
print("\n  q_ONB sweep at P = 1 bar (FIXED form):")
for dT in [0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]:
    q = bergles_rohsenow_FIXED(1.0, dT)
    print(f"    dT = {dT:5.1f} K  ->  q = {q:.3e} W/m2")

# Sweep dT at P=10 bar — FIXED
print("\n  q_ONB sweep at P = 10 bar (FIXED form):")
for dT in [0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]:
    q = bergles_rohsenow_FIXED(10.0, dT)
    print(f"    dT = {dT:5.1f} K  ->  q = {q:.3e} W/m2")

# Sweep dT at P=70 bar — FIXED
print("\n  q_ONB sweep at P = 70 bar (FIXED form):")
for dT in [0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]:
    q = bergles_rohsenow_FIXED(70.0, dT)
    print(f"    dT = {dT:5.1f} K  ->  q = {q:.3e} W/m2")

# Sweep dT at P=138 bar — FIXED
print("\n  q_ONB sweep at P = 138 bar (FIXED form):")
for dT in [0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]:
    q = bergles_rohsenow_FIXED(138.0, dT)
    print(f"    dT = {dT:5.1f} K  ->  q = {q:.3e} W/m2")

print()
print("  DIAGNOSIS: Exponent was P^0.0234/0.0234 (~42) — should be 2.16/P^0.0234 (~2).")
print("  Fixed form: q rises smoothly with dT as a ~square-law, physically correct.")
print("  Pressure range (1-138 bar) matches original Bergles & Rohsenow (1964).")

# ===================================================================
# 3. HALL-MUDAWAR 2000 — G=5000, D=3mm, L=100mm, x_i'=-0.3, P=10bar
#    Test expects ~11 MW/m2, code returns 13.56 MW/m2
# ===================================================================
print()
print("=" * 70)
print("3. HALL-MUDAWAR 2000 CHF DIAGNOSTIC")
print("=" * 70)

import CoolProp.CoolProp as CP

P_pa = 1_000_000.0  # 10 bar
rho_f = CP.PropsSI("D", "P", P_pa, "Q", 0, "Water")
rho_g = CP.PropsSI("D", "P", P_pa, "Q", 1, "Water")
h_f = CP.PropsSI("H", "P", P_pa, "Q", 0, "Water")
h_g = CP.PropsSI("H", "P", P_pa, "Q", 1, "Water")
h_fg = h_g - h_f
sigma = CP.PropsSI("I", "P", P_pa, "Q", 0, "Water")

print(f"  CoolProp properties at P = 10 bar:")
print(f"    rho_f  = {rho_f:.2f}  kg/m3   (test comment assumed 887)")
print(f"    rho_g  = {rho_g:.4f}  kg/m3   (test comment assumed 5.15)")
print(f"    h_fg   = {h_fg:.0f}  J/kg     (test comment assumed 2.015e6)")
print(f"    sigma  = {sigma:.6f}  N/m     (test comment assumed 0.0422)")
print()

G, D, L = 5000.0, 0.003, 0.100
x_i = -0.3
C1, C2, C3, C4, C5 = 0.0722, -0.312, -0.644, 0.900, 0.724

We_D = G**2 * D / (rho_f * sigma)
dr = rho_f / rho_g

print(f"  Derived quantities:")
print(f"    We_D   = G^2*D/(rho_f*sigma) = {We_D:.2f}   (test comment assumed 2005)")
print(f"    dr     = rho_f/rho_g = {dr:.2f}              (test comment assumed 172.2)")
print()

# Step-by-step numerator
We_C2 = We_D**C2
dr_C3 = dr**C3
dr_C5 = dr**C5
bracket = 1.0 - C4 * dr_C5 * x_i
numerator = C1 * We_C2 * dr_C3 * bracket

print(f"  Numerator breakdown:")
print(f"    We_D^C2        = {We_D}^{C2} = {We_C2:.6f}   (test assumed 0.0908)")
print(f"    dr^C3          = {dr:.2f}^{C3} = {dr_C3:.6f}   (test assumed 0.0254)")
print(f"    dr^C5          = {dr:.2f}^{C5} = {dr_C5:.4f}     (test assumed 48.5)")
print(f"    bracket        = 1 - {C4}*{dr_C5:.4f}*({x_i}) = {bracket:.4f}")
print(f"    numerator      = {C1}*{We_C2:.6f}*{dr_C3:.6f}*{bracket:.4f} = {numerator:.6f}")
print()

# Step-by-step denominator
dr_C3C5 = dr ** (C3 + C5)
denominator = 1.0 + 4.0 * C1 * C4 * We_C2 * dr_C3C5 * (L / D)

print(f"  Denominator breakdown:")
print(f"    dr^(C3+C5)     = {dr:.2f}^{C3+C5:.3f} = {dr_C3C5:.6f}")
print(f"    4*C1*C4*We^C2*dr^(C3+C5)*(L/D)")
print(f"      = 4*{C1}*{C4}*{We_C2:.6f}*{dr_C3C5:.6f}*{L/D:.2f}")
print(f"      = {4*C1*C4*We_C2*dr_C3C5*(L/D):.6f}")
print(f"    denominator    = {denominator:.6f}")
print()

Bo = numerator / denominator
q_chf = Bo * G * h_fg

print(f"  Result:")
print(f"    Bo_CHF = {Bo:.6f}")
print(f"    q_CHF  = Bo * G * h_fg = {Bo:.6f} * {G:.0f} * {h_fg:.0f}")
print(f"           = {q_chf:.0f} W/m2 = {q_chf/1e6:.2f} MW/m2")
print(f"    Test expected: ~11 MW/m2")
print(f"    Deviation: {(q_chf - 11e6) / 11e6 * 100:.1f}%")
print()

# Compare hand-calc assumptions vs CoolProp actuals
print("  Property comparison (hand-calc assumptions vs CoolProp):")
print(f"    rho_f:  887    vs {rho_f:.2f}  -> delta = {(rho_f-887)/887*100:.1f}%")
print(f"    rho_g:  5.15   vs {rho_g:.4f}  -> delta = {(rho_g-5.15)/5.15*100:.1f}%")
print(f"    h_fg:   2.015e6 vs {h_fg:.0f}  -> delta = {(h_fg-2.015e6)/2.015e6*100:.1f}%")
print(f"    sigma:  0.0422 vs {sigma:.6f}  -> delta = {(sigma-0.0422)/0.0422*100:.1f}%")
print()
print("  DIAGNOSIS: Compare code q_CHF vs hand-calc to determine if the")
print("  discrepancy is from (a) wrong property assumptions in the hand calc,")
print("  (b) arithmetic errors in the hand calc, or (c) implementation bug.")
