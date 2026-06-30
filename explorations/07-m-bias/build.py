"""07 — M-bias.

Prep courses and college GPA are unrelated. But SAT score is a collider: family
wealth drives both prep and SAT; innate ability drives both SAT and GPA. 'Control
for SAT' — usually the safe move for a pre-treatment variable — INVENTS a link.
Here, unlike the earlier pieces, splitting is the mistake.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "lib"))
import pieces  # noqa: E402

FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)

RNG = np.random.default_rng(23)
N = 240
wealth = RNG.normal(0, 1, N)     # U1: drives prep AND SAT
ability = RNG.normal(0, 1, N)    # U2: drives SAT AND GPA

prep = (6 + 2.4 * wealth + RNG.normal(0, 1.0, N)).clip(0, None)  # X: hours of test prep
gpa = (3.0 + 0.42 * ability + RNG.normal(0, 0.16, N)).clip(0, 4.0)  # Y (no prep effect)
sat = 1000 + 130 * wealth + 130 * ability + RNG.normal(0, 40, N)    # Z: the collider

# bands = SAT tertiles (what 'adjusting for SAT' amounts to)
edges = np.quantile(sat, [1/3, 2/3])
band = np.where(sat < edges[0], 0, np.where(sat < edges[1], 1, 2))
LABELS = ["Lower SAT", "Mid SAT", "Higher SAT"]
rows = [(float(p), float(g), int(b)) for p, g, b in zip(prep, gpa, band)]

payload = pieces.reveal_payload(
    rows, LABELS,
    x_label="Hours of test prep", y_label="College GPA",
    title="Does test prep raise your GPA?",
    lede="Drag from <strong>Ignore SAT</strong> to <strong>Adjust for SAT</strong>. Overall there's "
         "no link — the truth. Splitting by SAT manufactures one. Here, adjusting is the mistake.",
    left="Ignore SAT", right="Adjust for SAT",
    callout_pooled="→ no link (the truth)", callout_split="↘ a fake link, created by adjusting",
    state_pooled="unadjusted (correct)", state_split="adjusted for SAT (biased)",
    hint="Synthetic. Prep depends on wealth, GPA on ability; SAT is caused by both (a collider).",
    footer="Data Curiosities · 07 — M-bias · williamcatt.dev",
    x_pad=0.5, y_pad=0.15)

print("M-bias: pooled %.3f | bands %s | corr(prep,gpa)=%.2f" % (
    payload["_pooled"][0], [round(m, 3) for m, _ in payload["_bandFits"]],
    pieces.pearson(prep, gpa)))

pieces.reveal_figure(FIG / "fig_split.png", payload,
                     title="Adjusting for a collider invents a link",
                     annotation="Within an SAT band, prep and GPA\nappear linked — but it's an artefact.",
                     legend_loc="lower left")
pieces.write_reveal_toy(HERE / "toy.html", payload)
print("wrote toy.html, fig_split.png")
