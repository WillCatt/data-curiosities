# Backlog

Built so far: 01 Simpson's, 02 Confounding, 03 Ecological fallacy, 04 Berkson's /
collider, 05 Suppression. Each new piece clones the pattern: a `build.py` (synthetic
data → palette-matched figure via `lib/style.py` + an interactive via the shared
templates) and a portfolio piece page at `Portfolio/curiosities/pieces/<name>.html`.

Pattern per piece: **a plain-English line → an interactive you can drag → the
mechanism → a real documented case → "how not to get fooled".**

---

## Queued next — the subtle trio

### 06 — Lord's Paradox
**Hook:** two statisticians analyse the same before/after weight data and reach
opposite conclusions about whether a diet had an effect — one compares change scores,
the other adjusts for baseline (ANCOVA).
- **Interactive idea:** toggle between "difference in gains" and "baseline-adjusted"
  views on the same scatter; watch the conclusion flip.
- **Care needed:** the resolution is causal (which estimand answers the actual
  question), not statistical. Get the framing right.
- **Sources:** F. M. Lord (1967), *A paradox in the interpretation of group
  comparisons*, Psychological Bulletin, 68(5): 304–305. · J. Pearl (2016),
  *Lord's paradox revisited*, Journal of Causal Inference.

### 07 — M-Bias
**Hook:** controlling for a pre-treatment covariate — usually the "safe" thing to do —
can *open* a path and introduce bias, when that covariate is a collider on an M-shaped
DAG.
- **Interactive idea:** an M-shaped DAG where toggling "adjust for Z" switches the
  X→Y estimate from unbiased to biased.
- **Care needed:** distinguish from ordinary confounding; the whole point is that
  "adjust for everything pre-treatment" is wrong here.
- **Sources:** S. Greenland (2003), *Quantifying biases in causal models: classical
  confounding vs collider-stratification bias*, Epidemiology, 14(3): 300–306. ·
  Ding & Miratrix (2015), *To adjust or not to adjust?*, Journal of Causal Inference.

### 08 — Noncollapsibility
**Hook:** the odds ratio for a treatment can change when you adjust for a covariate
that is **not** a confounder — the effect measure shifts with no bias involved.
- **Interactive idea:** show the marginal vs conditional odds ratio side by side as you
  add a purely prognostic (non-confounding) covariate; the OR moves, the risk
  difference doesn't.
- **Care needed:** the cleanest illustration contrasts collapsible measures (risk
  difference, risk ratio) with the non-collapsible odds ratio / hazard ratio.
- **Sources:** S. Greenland, J. Robins & J. Pearl (1999), *Confounding and
  collapsibility in causal inference*, Statistical Science, 14(1): 29–46. ·
  Daniel, Zhang & Farewell (2021), *Making apples from oranges: noncollapsibility*.

---

## Other fun ideas (not paradoxes, lighter)

- **Datasaurus / Anscombe** — identical summary stats, wildly different shapes
  (Anscombe 1973; Matejka & Fitzmaurice 2017). "Always plot your data."
- **Survivorship bias** — Wald's WWII bomber armour (SRG memos; Mangel & Samaniego 1984).
- **Base-rate fallacy** — a 99%-accurate test at low prevalence gives a low PPV
  (Gigerenzer & Hoffrage 1995, natural frequencies).
