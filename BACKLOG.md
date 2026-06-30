# Backlog

Future tidbits, each built by cloning `explorations/01-simpsons-paradox/`: a
`build.py` (synthetic or real data → palette-matched figures via `lib/style.py`), a
cited `notes.md`, and a small `toy.html` where it earns one.

Pattern per piece: **a surprising claim → a chart that sells it → the mechanism → a
real documented case → "how not to get fooled".**

---

## 02 — Datasaurus / Anscombe's Quartet
**Hook:** thirteen wildly different scatterplots (one is a *dinosaur*) that share the
same mean, variance, and correlation to two decimal places. "Always plot your data."
- **Build:** Anscombe's four sets are tiny and can be hard-coded; the Datasaurus
  Dozen ships as a public dataset. Animate or small-multiple them.
- **Interactive angle:** cycle the shapes while the summary stats stay frozen on screen.
- **Sources:** F. J. Anscombe (1973), *Graphs in Statistical Analysis*, The American
  Statistician, 27(1): 17–21. · J. Matejka & G. Fitzmaurice (2017), *Same Stats,
  Different Graphs* (the Datasaurus Dozen), CHI 2017.

## 03 — Survivorship Bias
**Hook:** WWII analysts wanted to armour the bombers where returning planes had the
most bullet holes. Abraham Wald said: armour everywhere there *aren't* holes — those
are the planes that didn't come back.
- **Build:** a bomber silhouette with a hit-density heatmap; toggle "what we see"
  (survivors) vs "what we should infer" (the missing planes).
- **Interactive angle:** click to "shoot down" planes and watch the survivor
  distribution diverge from the true one.
- **Sources:** Statistical Research Group memoranda, A. Wald (1943). · M. Mangel & F.
  J. Samaniego (1984), *Abraham Wald's Work on Aircraft Survivability*, JASA, 79(386).

## 04 — Base-Rate Fallacy
**Hook:** a test that's "99% accurate" comes back positive — yet you probably *don't*
have the disease. Why a great test plus a rare condition equals a coin-flip result.
- **Build:** a 1,000-person icon array (true/false positives/negatives) that makes
  the positive-predictive-value collapse visible at a glance.
- **Interactive angle:** sliders for prevalence, sensitivity, specificity → watch PPV
  swing. The "natural frequencies" framing makes it click.
- **Sources:** Bayes' theorem. · G. Gigerenzer & U. Hoffrage (1995), *How to Improve
  Bayesian Reasoning Without Instruction: Frequency Formats*, Psychological Review,
  102(4): 684–704.

## 05 — Berkson's Paradox / The Friendship Paradox
**Hook (pick one):**
- *Berkson:* among people you'd date, "nice" and "attractive" look negatively
  correlated — not because they are in the world, but because you filtered out the
  people who were neither. Collider bias from selecting on the outcome.
- *Friendship:* almost everyone's friends have, on average, more friends than they
  do. A sampling quirk, not low self-esteem.
- **Build:** Berkson — scatter with a selection threshold you can drag, watching the
  in-sample correlation go negative. Friendship — a small social graph with the
  per-person vs per-friend degree averages side by side.
- **Sources:** J. Berkson (1946), *Limitations of the Application of Fourfold Table
  Analysis to Hospital Data*, Biometrics Bulletin, 2(3): 47–53. · S. L. Feld (1991),
  *Why Your Friends Have More Friends Than You Do*, American Journal of Sociology,
  96(6): 1464–1477.
