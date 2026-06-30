"""04 — Berkson's paradox / collider bias.

Talent and looks are independent in the population. But select on their sum
(the famous need one or the other) and, among the selected, they trade off:
a spurious NEGATIVE correlation conjured purely by the filter.
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

RNG = np.random.default_rng(3)
N = 320
talent = RNG.normal(50, 15, N).clip(2, 98)
looks = RNG.normal(50, 15, N).clip(2, 98)   # independent of talent
r_pop = pieces.pearson(talent, looks)

payload = {
    "points": [{"x": round(float(a), 2), "y": round(float(b), 2)} for a, b in zip(talent, looks)],
    "xLabel": "Acting talent", "yLabel": "Good looks",
    "domain": {"x": [0, 100], "y": [0, 100]},
    "selectedName": "the famous",
    "title": "Are talented actors less good-looking?",
    "lede": "Talent and looks are <strong>unrelated</strong> in the crowd. Drag the bar from "
            "<strong>Everyone</strong> toward <strong>Only the famous</strong> — you need one or "
            "the other to make it — and watch a fake trade-off appear.",
    "left": "Everyone", "right": "Only the famous",
    "hint": "Synthetic, independent traits (population r ≈ %.02f). The negative link is the filter, not reality." % r_pop,
    "footer": "Data Curiosities · 04 — Berkson's paradox · williamcatt.dev",
}
pieces.write_selection_toy(HERE / "toy.html", payload)

# static figure: everyone (grey) vs a selected elite (amber) with its negative fit
cut = np.quantile(talent + looks, 0.72)
sel = (talent + looks) >= cut
m, b = pieces.fit(talent[sel], looks[sel])
r_sel = pieces.pearson(talent[sel], looks[sel])
print("Berkson: population r=%.2f | selected r=%.2f (n=%d)" % (r_pop, r_sel, sel.sum()))

style.apply_rcParams()
fig, ax = plt.subplots(figsize=(7.2, 4.8))
ax.scatter(talent[~sel], looks[~sel], s=22, color=style.GREY, alpha=0.5, edgecolor="none",
           label="everyone else")
ax.scatter(talent[sel], looks[sel], s=26, color=style.AMBER, alpha=0.9, edgecolor="none",
           label="the famous")
xl = np.array([talent[sel].min(), talent[sel].max()])
ax.plot(xl, m * xl + b, color=style.AMBER, lw=3)
ax.plot([cut - 100, 100], [100, cut - 100], color=style.INK, lw=1.3, ls="--", alpha=0.5)
style.despine(ax); style.title_left(ax, "A trade-off that only exists among the selected")
ax.set_xlabel("Acting talent"); ax.set_ylabel("Good looks")
ax.set_xlim(0, 100); ax.set_ylim(0, 100)
ax.legend(frameon=False, loc="lower left", fontsize=10)
ax.annotate(f"among the famous: r = {r_sel:.2f}", xy=(0.97, 0.93), xycoords="axes fraction",
            ha="right", va="top", color=style.MUTED, fontsize=11)
style.save(fig, str(FIG / "fig_select.png")); plt.close(fig)
print("wrote toy.html, fig_select.png")
