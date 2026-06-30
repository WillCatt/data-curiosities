"""01 — Simpson's Paradox.

A trend that holds inside every age band reverses once you pool the bands.
Generates the interactive toy, a static 'split' figure, and the real
kidney-stone case (Charig et al. 1986).
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

# --- synthetic data: older people exercise more AND run higher blood sugar ---
RNG = np.random.default_rng(7)
N = 80
WITHIN_SLOPE = -1.6
BANDS = [("Age 20–35", 2.0, 88.0), ("Age 36–50", 4.2, 96.0), ("Age 51–65", 6.4, 104.0)]
rows = []
for i, (_lbl, ex_c, base) in enumerate(BANDS):
    ex = RNG.normal(ex_c, 1.0, N).clip(0.2, None)
    gl = base + WITHIN_SLOPE * (ex - ex_c) + RNG.normal(0, 3.0, N)
    rows += [(float(x), float(y), i) for x, y in zip(ex, gl)]

payload = pieces.reveal_payload(
    rows, [b[0] for b in BANDS],
    x_label="Exercise (hours per week)", y_label="Fasting blood sugar (mg/dL)",
    title="More exercise, higher blood sugar?",
    lede="Drag from <strong>Ignore age</strong> to <strong>Reveal age</strong>. The single "
         "upward trend splits into three age bands — and every one slopes <em>down</em>.",
    left="Ignore age", right="Reveal age",
    callout_pooled="↗ pooled trend slopes up", callout_split="↘ every age band slopes down",
    state_pooled="pooled view", state_split="split by age",
    hint="Illustrative synthetic data — the real documented cases are in the write-up.",
    footer="Data Curiosities · 01 — Simpson's Paradox · williamcatt.dev")

print("Simpson's: pooled %.2f | bands %s" %
      (payload["_pooled"][0], [round(m, 2) for m, _ in payload["_bandFits"]]))

pieces.reveal_figure(FIG / "fig_split.png", payload,
                     title="Split by age, every group slopes down",
                     annotation="Within each age band,\nmore exercise = lower blood sugar.")
pieces.write_reveal_toy(HERE / "toy.html", payload)

# --- real case: kidney stones (Charig et al. 1986, BMJ) ---
style.apply_rcParams()
groups = ["Small stones", "Large stones", "Overall"]
open_s, pcnl = [93, 73, 78], [83, 69, 83]
open_n, pcnl_n = ["81/87", "192/263", "273/350"], ["234/270", "55/80", "289/350"]
x = np.arange(len(groups)); w = 0.38
fig, ax = plt.subplots(figsize=(7.4, 4.6))
b1 = ax.bar(x - w/2, open_s, w, color=style.AMBER, label="Open surgery")
b2 = ax.bar(x + w/2, pcnl, w, color=style.TEAL, label="Keyhole (PCNL)")
for bars, ns in ((b1, open_n), (b2, pcnl_n)):
    for r, n in zip(bars, ns):
        ax.text(r.get_x()+r.get_width()/2, r.get_height()+1, f"{int(r.get_height())}%\n{n}",
                ha="center", va="bottom", fontsize=9, color=style.INK)
style.despine(ax); ax.set_xticks(x, groups); ax.set_ylim(0, 105); ax.set_ylabel("Success rate")
style.title_left(ax, "Real case: open surgery wins both subgroups, loses overall")
ax.legend(frameon=False, loc="lower left")
ax.annotate("Charig et al. 1986, BMJ", xy=(0.5, 0.88), xycoords="axes fraction",
            ha="center", va="center", color=style.MUTED, fontsize=9)
style.save(fig, str(FIG / "fig_kidney.png")); plt.close(fig)
print("wrote toy.html, fig_split.png, fig_kidney.png")
