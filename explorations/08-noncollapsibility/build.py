"""08 — Noncollapsibility.

A randomised treatment (no confounding), with a constant conditional odds ratio of
2.0 in two risk strata. Combine the strata and the marginal odds ratio falls below
2.0 — the OR changes on adjustment even though nothing is confounded. The risk
difference and risk ratio don't do this. A property of the odds ratio, not a bias.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "lib"))
import style, pieces  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)

OR = 2.0
BASE = 0.30
GMAX = 0.26


def odds(p): return p / (1 - p)
def risk(o): return o / (1 + o)
def treated(p0): return risk(OR * odds(p0))


def marginal_or(gap):
    p0L, p0H = BASE - gap, BASE + gap
    p1L, p1H = treated(p0L), treated(p0H)
    P0, P1 = (p0L + p0H) / 2, (p1L + p1H) / 2
    return odds(P1) / odds(P0)


# sanity check the maths the toy will reproduce
for gp in (0.0, 0.13, 0.26):
    print("gap %.2f -> marginal OR %.3f (conditional 2.0)" % (gp, marginal_or(gp)))

payload = {
    "conditionalOR": OR, "baseRisk": BASE, "gapMax": GMAX,
    "lowLabel": "Low-risk patients", "highLabel": "High-risk patients",
    "combinedLabel": "Everyone combined",
    "title": "An effect that shrinks when you combine groups",
    "lede": "A drug with the <strong>same odds ratio (2.0)</strong> in low-risk and high-risk patients, "
            "assigned at random so there's no confounding. Drag to spread the two groups apart.",
    "left": "Identical patients", "right": "Very different patients",
    "hint": "The combined odds ratio sits below 2.0 with no confounding present. The risk difference "
            "and risk ratio stay collapsible — it's the odds ratio that misbehaves.",
    "footer": "Data Curiosities · 08 — Noncollapsibility · williamcatt.dev",
}
pieces.write_noncollapse_toy(HERE / "toy.html", payload)

# static figure: conditional OR (flat) vs marginal OR (falls) as the risk gap widens
style.apply_rcParams()
gaps = np.linspace(0, GMAX, 60)
marg = np.array([marginal_or(g) for g in gaps])
fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.axhline(OR, color=style.AMBER, lw=3, label="within each group (conditional OR)")
ax.plot(gaps, marg, color=style.TEAL, lw=3, label="combined (marginal OR)")
ax.fill_between(gaps, marg, OR, color=style.TEAL, alpha=0.08)
style.despine(ax)
style.title_left(ax, "Same odds ratio in each group, smaller once combined")
ax.set_xlabel("How different the two patient groups are (baseline-risk gap)")
ax.set_ylabel("Odds ratio for the treatment")
ax.set_ylim(1.4, 2.1)
ax.legend(frameon=False, loc="lower left", fontsize=10)
ax.annotate("no confounding anywhere here", xy=(0.97, 0.95), xycoords="axes fraction",
            ha="right", va="top", color=style.MUTED, fontsize=10)
style.save(fig, str(FIG / "fig_split.png")); plt.close(fig)
print("wrote toy.html, fig_split.png")
