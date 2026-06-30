"""06 — Lord's Paradox.

Two diets, students weighed at the start and end of term. One analyst compares the
average weight GAINED (the change score) and finds the diets identical. Another
ADJUSTS for starting weight (ANCOVA) and finds a clear difference. Same data,
opposite conclusions — Lord (1967).
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

RNG = np.random.default_rng(31)
# Each diet: end weight regresses toward the diet's own mean (slope < 1), and the
# average gain is ~0. Diet B students simply start (and end) heavier.
GROUPS = ["Diet A", "Diet B"]
start_mean = [58.0, 68.0]
BETA = 0.70                      # within-group regression of end on start (<1)
rows, means = [], []
for i, sm in enumerate(start_mean):
    x = RNG.normal(sm, 6.0, 90)
    y = BETA * x + (1 - BETA) * sm + RNG.normal(0, 2.6, x.size)   # mean gain ≈ 0
    rows += [(float(a), float(b), i) for a, b in zip(x, y)]
    means.append((float(x.mean()), float(y.mean())))

xs = np.array([r[0] for r in rows]); ys = np.array([r[1] for r in rows])
g = np.array([r[2] for r in rows])
fits = [pieces.fit(xs[g == i], ys[g == i]) for i in (0, 1)]
adjust_x = float(xs.mean())
gain = [means[i][1] - means[i][0] for i in (0, 1)]
adj_gap = abs((fits[1][0] * adjust_x + fits[1][1]) - (fits[0][0] * adjust_x + fits[0][1]))
print("Lord's: mean gain A=%.2f B=%.2f (≈equal) | within slope %.2f | ANCOVA gap=%.1f kg" %
      (gain[0], gain[1], fits[0][0], adj_gap))

payload = {
    "points": [{"x": round(a, 2), "y": round(b, 2), "g": int(c)} for a, b, c in rows],
    "groups": GROUPS, "groupColors": [style.AMBER, style.TEAL],
    "groupMeans": [{"x": round(m[0], 2), "y": round(m[1], 2)} for m in means],
    "fits": [{"m": m, "b": b} for m, b in fits],
    "adjustX": round(adjust_x, 2), "unit": "kg",
    "xLabel": "Weight at start of term (kg)", "yLabel": "Weight at end of term (kg)",
    "title": "Did the diet make a difference?",
    "lede": "Same students, two analysts. Drag from <strong>Compare the gain</strong> to "
            "<strong>Adjust for the start</strong> — and watch the conclusion flip.",
    "left": "Compare the gain", "right": "Adjust for the start",
    "calloutGain": "↔ same average gain — no effect?", "calloutAdj": "↕ at equal start, Diet B ends higher",
    "stateGain": "change-score view", "stateAdj": "baseline-adjusted view",
    "hint": "Synthetic data, in the shape of Lord's 1967 example. Neither analyst miscalculated.",
    "footer": "Data Curiosities · 06 — Lord's paradox · williamcatt.dev",
    "domain": {"x": [float(xs.min()) - 3, float(xs.max()) + 3],
               "y": [float(ys.min()) - 3, float(ys.max()) + 3]},
}
pieces.write_lord_toy(HERE / "toy.html", payload)

# static figure
style.apply_rcParams()
fig, ax = plt.subplots(figsize=(7.2, 4.8))
for i, lbl in enumerate(GROUPS):
    mask = g == i
    ax.scatter(xs[mask], ys[mask], s=24, color=payload["groupColors"][i], alpha=0.6,
               edgecolor="none", label=lbl)
    xb = np.array([xs[mask].min(), xs[mask].max()])
    ax.plot(xb, fits[i][0] * xb + fits[i][1], color=payload["groupColors"][i], lw=3)
lo = max(xs.min(), ys.min()); hi = min(xs.max(), ys.max())
ax.plot([lo, hi], [lo, hi], color=style.INK, lw=1.3, ls="--", alpha=0.45)
yA = fits[0][0] * adjust_x + fits[0][1]; yB = fits[1][0] * adjust_x + fits[1][1]
ax.plot([adjust_x, adjust_x], [yA, yB], color=style.INK, lw=4)
ax.annotate(f"adjusted gap ≈ {adj_gap:.1f} kg", xy=(adjust_x + 0.6, (yA + yB) / 2),
            fontsize=10, fontweight="bold", color=style.INK, va="center")
style.despine(ax); style.title_left(ax, "Equal gains, yet a gap once you adjust for the start")
ax.set_xlabel(payload["xLabel"]); ax.set_ylabel(payload["yLabel"])
ax.legend(frameon=False, loc="upper left", fontsize=10)
style.save(fig, str(FIG / "fig_split.png")); plt.close(fig)
print("wrote toy.html, fig_split.png")
