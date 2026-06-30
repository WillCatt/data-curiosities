"""Build the Simpson's Paradox explainer assets.

Generates a small synthetic-but-honest dataset where the relationship between
weekly exercise and blood sugar *reverses* once you account for age, then writes:

  figures/fig1_pooled.png    the upward "more exercise looks worse" hook
  figures/fig2_split.png     the reveal: every age band slopes down
  figures/fig3_kidney.png    a real documented case (Charig et al. 1986)
  data/data.json             the points + fitted lines (also used by the toy)
  toy.html                   self-contained interactive (data inlined)

Run:  python explorations/01-simpsons-paradox/build.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]              # project root
sys.path.insert(0, str(ROOT / "lib"))

import style  # noqa: E402  (path set above)
import matplotlib.pyplot as plt  # noqa: E402

FIG = HERE / "figures"
DATA = HERE / "data"
FIG.mkdir(exist_ok=True)
DATA.mkdir(exist_ok=True)

# --------------------------------------------------------------------------
# 1. Synthetic data with a built-in confounder
# --------------------------------------------------------------------------
# Three age bands. The mechanism that creates the paradox:
#   * older people exercise MORE here (exercise centre rises with age), and
#   * older people run HIGHER baseline blood sugar (base rises with age).
# So pooling the data, exercise tracks age tracks high sugar -> a spurious
# UPWARD trend. But WITHIN any band, more exercise lowers sugar (the real,
# negative effect). That gap is Simpson's paradox.

RNG = np.random.default_rng(7)
N_PER_BAND = 80
WITHIN_SLOPE = -1.6   # mg/dL per extra hour of exercise (the true effect)

BANDS = [
    # label,        exercise_centre,  baseline_glucose
    ("Age 20–35", 2.0,  88.0),
    ("Age 36–50", 4.2,  96.0),
    ("Age 51–65", 6.4, 104.0),
]

rows = []  # (exercise, glucose, band_index)
for i, (_label, ex_centre, base) in enumerate(BANDS):
    ex = RNG.normal(ex_centre, 1.0, N_PER_BAND).clip(0.2, None)
    glucose = base + WITHIN_SLOPE * (ex - ex_centre) + RNG.normal(0, 3.0, N_PER_BAND)
    for x, y in zip(ex, glucose):
        rows.append((float(x), float(y), i))

ex_all = np.array([r[0] for r in rows])
gl_all = np.array([r[1] for r in rows])
band_all = np.array([r[2] for r in rows])


def fit(x, y):
    """Return (slope, intercept) of a simple linear fit."""
    m, b = np.polyfit(x, y, 1)
    return float(m), float(b)


pooled_m, pooled_b = fit(ex_all, gl_all)
band_fits = [fit(ex_all[band_all == i], gl_all[band_all == i]) for i in range(len(BANDS))]

print(f"pooled slope  = {pooled_m:+.2f} mg/dL per hour  (looks like exercise = worse)")
for (label, *_), (m, _b) in zip(BANDS, band_fits):
    print(f"  {label}: {m:+.2f} mg/dL per hour  (more exercise = better)")

# --------------------------------------------------------------------------
# 2. Figures
# --------------------------------------------------------------------------
style.apply_rcParams()

xline = np.array([ex_all.min(), ex_all.max()])

# fig1 — the pooled hook
fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.scatter(ex_all, gl_all, s=26, color=style.GREY, edgecolor="none", alpha=0.9)
ax.plot(xline, pooled_m * xline + pooled_b, color=style.AMBER, lw=3,
        label=f"pooled trend ({pooled_m:+.1f} mg/dL per hr)")
style.despine(ax)
style.title_left(ax, "More exercise, higher blood sugar?")
ax.set_xlabel("Exercise (hours per week)")
ax.set_ylabel("Fasting blood sugar (mg/dL)")
ax.legend(frameon=False, loc="upper left")
ax.annotate("The line slopes up.\nLooks like exercise is bad for you.",
            xy=(0.97, 0.06), xycoords="axes fraction", ha="right", va="bottom",
            color=style.MUTED, fontsize=11)
style.save(fig, str(FIG / "fig1_pooled.png"))
plt.close(fig)

# fig2 — the reveal
fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.plot(xline, pooled_m * xline + pooled_b, color=style.GREY, lw=2.5, ls="--",
        zorder=1, label="pooled trend (misleading)")
for i, (label, *_), in enumerate(BANDS):
    c = style.BAND_COLORS[i]
    m, b = band_fits[i]
    mask = band_all == i
    ax.scatter(ex_all[mask], gl_all[mask], s=26, color=c, edgecolor="none",
               alpha=0.85, label=label)
    xb = np.array([ex_all[mask].min(), ex_all[mask].max()])
    ax.plot(xb, m * xb + b, color=c, lw=3, zorder=3)
style.despine(ax)
style.title_left(ax, "Split by age, every group slopes down")
ax.set_xlabel("Exercise (hours per week)")
ax.set_ylabel("Fasting blood sugar (mg/dL)")
ax.legend(frameon=False, loc="upper left", fontsize=10)
ax.annotate("Within each age band,\nmore exercise = lower blood sugar.",
            xy=(0.97, 0.06), xycoords="axes fraction", ha="right", va="bottom",
            color=style.MUTED, fontsize=11)
style.save(fig, str(FIG / "fig2_split.png"))
plt.close(fig)

# fig3 — real documented case: kidney stone treatment (Charig et al. 1986, BMJ)
# Open surgery beats PCNL for BOTH small and large stones, yet loses overall,
# because the easier (small-stone) cases were steered toward PCNL.
groups = ["Small stones", "Large stones", "Overall"]
open_surgery = [93, 73, 78]      # success %
pcnl = [83, 69, 83]
open_n = ["81/87", "192/263", "273/350"]
pcnl_n = ["234/270", "55/80", "289/350"]

x = np.arange(len(groups))
w = 0.38
fig, ax = plt.subplots(figsize=(7.4, 4.6))
b1 = ax.bar(x - w / 2, open_surgery, w, color=style.AMBER, label="Open surgery")
b2 = ax.bar(x + w / 2, pcnl, w, color=style.TEAL, label="Keyhole (PCNL)")
for bars, ns in ((b1, open_n), (b2, pcnl_n)):
    for rect, n in zip(bars, ns):
        ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height() + 1,
                f"{int(rect.get_height())}%\n{n}", ha="center", va="bottom",
                fontsize=9, color=style.INK)
style.despine(ax)
ax.set_xticks(x, groups)
ax.set_ylim(0, 105)
ax.set_ylabel("Success rate")
style.title_left(ax, "Real case: open surgery wins both subgroups, loses overall")
ax.legend(frameon=False, loc="lower left")
ax.annotate("Charig et al. 1986, BMJ", xy=(0.5, 0.88), xycoords="axes fraction",
            ha="center", va="center", color=style.MUTED, fontsize=9)
style.save(fig, str(FIG / "fig3_kidney.png"))
plt.close(fig)

# --------------------------------------------------------------------------
# 3. data.json + toy.html (data inlined so the toy opens from file://)
# --------------------------------------------------------------------------
payload = {
    "points": [{"x": round(x, 3), "y": round(y, 2), "band": int(b)} for x, y, b in rows],
    "bands": [label for label, *_ in BANDS],
    "bandColors": style.BAND_COLORS[: len(BANDS)],
    "pooled": {"m": pooled_m, "b": pooled_b},
    "bandFits": [{"m": m, "b": b} for m, b in band_fits],
    "xLabel": "Exercise (hours per week)",
    "yLabel": "Fasting blood sugar (mg/dL)",
    "domain": {
        "x": [float(ex_all.min()) - 0.5, float(ex_all.max()) + 0.5],
        "y": [float(gl_all.min()) - 5, float(gl_all.max()) + 5],
    },
}
(DATA / "data.json").write_text(json.dumps(payload, indent=2))

template = (HERE / "toy.template.html").read_text()
(HERE / "toy.html").write_text(template.replace("__DATA__", json.dumps(payload)))

print("\nwrote figures/, data/data.json, toy.html")
