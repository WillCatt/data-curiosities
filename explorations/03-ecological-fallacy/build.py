"""03 — Ecological fallacy.

Robinson (1950): across US states, areas with more foreign-born residents had
HIGHER literacy — yet individual immigrants were LESS literate than the
native-born. A correlation measured on groups need not hold for the people in them.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "lib"))
import pieces  # noqa: E402

FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)

RNG = np.random.default_rng(5)
REGIONS = ["Region A", "Region B", "Region C", "Region D", "Region E"]
x_mean = [18, 24, 30, 36, 44]      # % foreign-born, by region (rising)
y_base = [79, 82, 84, 87, 90]      # region literacy %, rising with industrialisation
WITHIN_SLOPE = -1.25               # an immigrant individual: lower literacy
rows = []
for i, (xm, yb) in enumerate(zip(x_mean, y_base)):
    dx = RNG.normal(0, 9, 70)
    x = (xm + dx).clip(1, None)
    y = (yb + WITHIN_SLOPE * dx + RNG.normal(0, 3.0, dx.size)).clip(48, 99)
    rows += [(float(a), float(b), i) for a, b in zip(x, y)]

payload = pieces.ecological_payload(
    rows, REGIONS,
    x_label="% foreign-born", y_label="Literacy (%)",
    title="Do immigrants lower literacy?",
    lede="Drag from <strong>Each person</strong> to <strong>Region averages</strong>. "
         "Person by person the trend slopes down; region by region it slopes up.",
    left="Each person", right="Region averages",
    callout_pooled="↘ people: more foreign-born, lower literacy",
    callout_split="↗ regions: more foreign-born, higher literacy",
    state_pooled="individual view", state_split="aggregate view",
    hint="Synthetic data echoing Robinson's 1950 structure (individual r negative, area r positive).",
    footer="Data Curiosities · 03 — Ecological fallacy · williamcatt.dev",
    x_pad=3, y_pad=3)

print("Ecological: individual slope %.3f (r=%.2f) | region-mean slope %.3f" % (
    payload["_ind"][0], pieces.pearson(
        np.array([p["x"] for p in payload["points"]]),
        np.array([p["y"] for p in payload["points"]])),
    payload["_meanfit"][0]))

pieces.ecological_figure(FIG / "fig_split.png", payload,
                         title="Same data, opposite trends at two scales",
                         annotation="People (amber) slope down;\nregion averages (teal) slope up.")
pieces.write_ecological_toy(HERE / "toy.html", payload)
print("wrote toy.html, fig_split.png")
