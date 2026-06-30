"""05 — Suppression effect.

Practice looks unrelated to test scores — because people who practise more take
on harder tasks, and harder tasks score lower. The two effects cancel. Control
for difficulty and practice's real, positive effect appears.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "lib"))
import pieces  # noqa: E402

FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)

RNG = np.random.default_rng(19)
# more practice -> harder tasks chosen (centre rises); harder tasks score lower (base falls)
BANDS = ["Easy tasks", "Medium tasks", "Hard tasks"]
practice_c = [4.0, 6.5, 9.0]
score_base = [86.0, 75.0, 64.0]
WITHIN_SLOPE = 2.1     # the true, hidden benefit of practice
rows = []
for i, (pc, sb) in enumerate(zip(practice_c, score_base)):
    p = RNG.normal(pc, 1.5, 70).clip(0.5, None)
    s = sb + WITHIN_SLOPE * (p - pc) + RNG.normal(0, 3.5, p.size)
    rows += [(float(a), float(b), i) for a, b in zip(p, s)]

payload = pieces.reveal_payload(
    rows, BANDS,
    x_label="Practice (hours per week)", y_label="Test score",
    title="Does practice even help?",
    lede="Drag from <strong>Ignore difficulty</strong> to <strong>Group by difficulty</strong>. "
         "Overall, more practice looks like <em>lower</em> scores; inside each difficulty, practice clearly pays off.",
    left="Ignore difficulty", right="Group by difficulty",
    callout_pooled="↘ more practice, lower scores?!",
    callout_split="↗ within a difficulty, practice helps",
    state_pooled="pooled view", state_split="held at one difficulty",
    hint="Illustrative synthetic data. Difficulty hides practice's real benefit.",
    footer="Data Curiosities · 05 — Suppression effect · williamcatt.dev",
    y_pad=3)

print("Suppression: pooled %.3f | bands %s" %
      (payload["_pooled"][0], [round(m, 3) for m, _ in payload["_bandFits"]]))

pieces.reveal_figure(FIG / "fig_split.png", payload,
                     title="Account for difficulty and practice's payoff appears",
                     annotation="Within one difficulty band,\nmore practice = higher scores.",
                     legend_loc="lower left")
pieces.write_reveal_toy(HERE / "toy.html", payload)
print("wrote toy.html, fig_split.png")
