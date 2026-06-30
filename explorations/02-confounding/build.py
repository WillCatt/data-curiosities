"""02 — Confounding.

Ice-cream sales track drownings — but only because hot weather drives both.
Hold temperature roughly fixed (split into bands) and the link disappears.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "lib"))
import pieces  # noqa: E402

FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)

RNG = np.random.default_rng(11)
# temperature is the confounder: it pushes up both ice-cream sales and drownings.
BANDS = ["Cool days", "Mild days", "Hot days"]
centres = [14.0, 21.0, 28.0]   # °C
rows = []
for i, c in enumerate(centres):
    temp = RNG.normal(c, 1.6, 70)
    ice = 30 + 6.0 * temp + RNG.normal(0, 14, temp.size)        # cones sold (index)
    drown = 1.0 + 0.20 * temp + RNG.normal(0, 1.1, temp.size)   # incidents
    rows += [(float(a), float(b), i) for a, b in zip(ice, drown)]

payload = pieces.reveal_payload(
    rows, BANDS,
    x_label="Ice-cream sales (index)", y_label="Drowning incidents",
    title="Ice cream is linked to drownings?",
    lede="Drag from <strong>Ignore weather</strong> to <strong>Group by temperature</strong>. "
         "The strong upward link flattens out once each group shares the same weather.",
    left="Ignore weather", right="Group by temperature",
    callout_pooled="↗ more ice cream, more drownings", callout_split="→ within a temperature, no link",
    state_pooled="pooled view", state_split="held at one temperature",
    hint="Illustrative synthetic data. Temperature is the lurking cause of both.",
    footer="Data Curiosities · 02 — Confounding · williamcatt.dev",
    y_pad=0.8)

print("Confounding: pooled %.3f | bands %s" %
      (payload["_pooled"][0], [round(m, 3) for m, _ in payload["_bandFits"]]))

pieces.reveal_figure(FIG / "fig_split.png", payload,
                     title="Hold the weather fixed and the link vanishes",
                     annotation="Within one temperature band,\nice cream and drownings barely move together.")
pieces.write_reveal_toy(HERE / "toy.html", payload)
print("wrote toy.html, fig_split.png")
