"""Generate a schematic Nukiyama boiling curve (q" vs ΔT_sat) as SVG.

Output: wiki/concepts/boiling_curve.svg

This is a *schematic* (not computed from any correlation) illustrating the
four regimes: natural convection, nucleate boiling, transition boiling, and
film boiling. Key transition points (ONB, CHF, Leidenfrost) are annotated.

Run: .venv/bin/python scripts/generate_boiling_curve.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# --- Schematic boiling curve data (log-log) ---
# These are representative shapes, not computed from a physical model.
# x-axis: ΔT_sat = T_wall - T_sat [K], log scale
# y-axis: q" [W/m²], log scale

# Region A: Natural convection (ΔT ~ 1–5 K)
dT_A = np.linspace(1, 5, 30)
q_A = 500 * dT_A**1.25  # gentle power law

# Region B: Nucleate boiling (ΔT ~ 5–30 K), steep rise
dT_B = np.linspace(5, 30, 50)
q_B = q_A[-1] * (dT_B / 5) ** 3.0  # ~cubic rise (Rohsenow-like)

# CHF point
dT_CHF = 30.0
q_CHF = q_B[-1]

# Region C: Transition boiling (ΔT ~ 30–120 K), decreasing q"
dT_C = np.linspace(30, 120, 40)
q_Leidenfrost = q_CHF * 0.08  # Leidenfrost minimum ~ 8% of CHF
log_q_C = np.log10(q_CHF) + (np.log10(q_Leidenfrost) - np.log10(q_CHF)) * (
    (dT_C - 30) / (120 - 30)
) ** 0.8
q_C = 10**log_q_C

# Leidenfrost point
dT_Leid = 120.0
q_Leid = q_C[-1]

# Region D: Film boiling (ΔT ~ 120–1000 K), gradual rise (radiation)
dT_D = np.linspace(120, 1000, 50)
q_D = q_Leid * (dT_D / 120) ** 1.1

# --- Plot ---
fig, ax = plt.subplots(figsize=(8, 5.5))

# Plot each region with the same color but distinct labels
color = "#2563EB"
ax.loglog(dT_A, q_A, color=color, linewidth=2.2, solid_capstyle="round")
ax.loglog(dT_B, q_B, color=color, linewidth=2.2, solid_capstyle="round")
ax.loglog(dT_C, q_C, color=color, linewidth=2.2, linestyle="--",
          solid_capstyle="round")
ax.loglog(dT_D, q_D, color=color, linewidth=2.2, solid_capstyle="round")

# Transition points
marker_kw = dict(markersize=8, zorder=5)
ax.plot(dT_A[-1], q_A[-1], "o", color="#16A34A", label="ONB", **marker_kw)
ax.plot(dT_CHF, q_CHF, "s", color="#DC2626", label="CHF (burnout)",
        **marker_kw)
ax.plot(dT_Leid, q_Leid, "D", color="#D97706", label="Leidenfrost point",
        **marker_kw)

# Region labels
ax.annotate("Natural\nconvection", xy=(2, q_A[10]),
            fontsize=9, ha="center", color="#555")
ax.annotate("Nucleate\nboiling", xy=(12, q_B[20] * 0.4),
            fontsize=9, ha="center", color="#555")
ax.annotate("Transition\nboiling", xy=(60, q_C[15] * 2.5),
            fontsize=9, ha="center", color="#555")
ax.annotate("Film\nboiling", xy=(500, q_D[30] * 0.35),
            fontsize=9, ha="center", color="#555")

# Annotations for key points
ax.annotate("ONB", xy=(dT_A[-1], q_A[-1]),
            xytext=(2.5, q_A[-1] * 3),
            fontsize=8.5, fontweight="bold", color="#16A34A",
            arrowprops=dict(arrowstyle="->", color="#16A34A", lw=1.2))
ax.annotate("CHF\n(q″$_{max}$)", xy=(dT_CHF, q_CHF),
            xytext=(dT_CHF * 2.2, q_CHF * 2.5),
            fontsize=8.5, fontweight="bold", color="#DC2626",
            arrowprops=dict(arrowstyle="->", color="#DC2626", lw=1.2))
ax.annotate("Leidenfrost\n(q″$_{min}$)", xy=(dT_Leid, q_Leid),
            xytext=(dT_Leid * 2.5, q_Leid * 0.15),
            fontsize=8.5, fontweight="bold", color="#D97706",
            arrowprops=dict(arrowstyle="->", color="#D97706", lw=1.2))

# Axes
ax.set_xlabel("Wall superheat  ΔT$_{sat}$ = T$_w$ − T$_{sat}$  [K]",
              fontsize=11)
ax.set_ylabel("Heat flux  q″  [W/m²]", fontsize=11)
ax.set_title("Boiling Curve (Nukiyama, schematic — water at 1 atm)",
             fontsize=12, fontweight="bold")
ax.set_xlim(1, 1200)
ax.set_ylim(300, 5e6)

ax.legend(loc="upper left", fontsize=8.5, framealpha=0.9)
ax.grid(True, which="both", alpha=0.3)
ax.tick_params(labelsize=9)

fig.tight_layout()

# Save
out_path = Path(__file__).resolve().parent.parent / "wiki" / "concepts" / "boiling_curve.svg"
fig.savefig(out_path, format="svg", bbox_inches="tight")
print(f"Saved: {out_path}")
plt.close(fig)
