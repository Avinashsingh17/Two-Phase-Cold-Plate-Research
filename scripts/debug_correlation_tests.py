"""Diagnostic script for failing correlation tests.

Run: .venv/bin/python scripts/debug_correlation_tests.py

Purpose: verify hand-calculation reference values before fixing tests.
Do NOT change implementation code until root causes are identified here.
"""

import math

# ===================================================================
# 1. DITTUS-BOELTER — Incropera 7e Example 8.6 (air cooling in duct)
#    Re=20050, Pr=0.698, n=0.3 (cooling). Textbook states Nu_D = 56.4.
# ===================================================================
print("=" * 70)
print("1. DITTUS-BOELTER — Incropera 7e Ex 8.6 verification")
print("=" * 70)

Re = 20_050.0
Pr = 0.698

Re_08 = Re**0.8
Pr_03 = Pr**0.3
Pr_04 = Pr**0.4
Nu_cooling = 0.023 * Re_08 * Pr_03
Nu_heating = 0.023 * Re_08 * Pr_04

print(f"  Re          = {Re:.0f}")
print(f"  Pr          = {Pr}")
print(f"  Re^0.8      = {Re_08:.2f}")
print(f"  Pr^0.3      = {Pr_03:.6f}")
print(f"  Pr^0.4      = {Pr_04:.6f}")
print()
print(f"  Nu (n=0.3, cooling) = 0.023 * {Re_08:.2f} * {Pr_03:.6f} = {Nu_cooling:.2f}")
print(f"  Nu (n=0.4, heating) = 0.023 * {Re_08:.2f} * {Pr_04:.6f} = {Nu_heating:.2f}")
print(f"  Textbook states: Nu_D = 56.4")
print(f"  Exact formula:   Nu   = {Nu_cooling:.1f}")
print(f"  Gap = {abs(Nu_cooling - 56.4) / 56.4 * 100:.1f}% (intermediate rounding in textbook)")
print()
print(f"  n=0.3 vs n=0.4 difference: {abs(Nu_cooling - Nu_heating):.2f}")
print(f"  n=0.4 value ({Nu_heating:.1f}) within 2% of 56.4? "
      f"{'YES' if abs(Nu_heating - 56.4) / 56.4 < 0.02 else 'NO'}")
print(f"  -> n-branch IS load-bearing: wrong n yields {Nu_heating:.1f}, not {Nu_cooling:.1f}")

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
