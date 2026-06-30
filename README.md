# Data Curiosities

*Counterintuitive statistics, one chart at a time — bite-sized data-science tidbits,
each "wait, what?" grounded in real published work. Built while working through the
Claude Skilljar course; lives at [williamcatt.dev/curiosities](https://williamcatt.dev/curiosities/).*

Each piece takes a counter-intuitive statistical idea, grounds it in real published
work, and explains it with hand-made charts plus a small drag-to-reveal interactive.
Aimed at being fun for data and non-data people alike.

## Pieces

| # | Topic | What it shows |
|---|-------|---------------|
| 01 | [Simpson's Paradox](explorations/01-simpsons-paradox/) | A trend true in every age group reverses once you pool the groups. Age-reveal slider + the real kidney-stone case. |
| 02 | [Confounding](explorations/02-confounding/) | Ice-cream sales "cause" drownings until you hold temperature fixed. Storks-and-babies as the real case. |
| 03 | [Ecological fallacy](explorations/03-ecological-fallacy/) | Group-level and individual-level correlations disagree in sign (Robinson 1950, literacy vs % foreign-born). |
| 04 | [Berkson's paradox](explorations/04-berksons-collider/) | Selecting on a collider invents a negative link between independent traits. |
| 05 | [Suppression effect](explorations/05-suppression/) | A real effect stays hidden until you account for a variable working against it. |
| 06 | [Lord's paradox](explorations/06-lords-paradox/) | Change-score vs baseline-adjusted (ANCOVA) give two analysts opposite conclusions on the same data. |
| 07 | [M-bias](explorations/07-m-bias/) | Adjusting for a pre-treatment collider (SAT) invents a link between prep and GPA. |
| 08 | [Noncollapsibility](explorations/08-noncollapsibility/) | A constant conditional odds ratio of 2.0 reads as ~1.5 when pooled — with no confounding. |

All eight live at [williamcatt.dev/curiosities](https://williamcatt.dev/curiosities/). Further ideas
(Datasaurus, survivorship bias, base-rate fallacy) in [`BACKLOG.md`](BACKLOG.md).

## Layout

```
.
├── lib/
│   ├── style.py                    # shared palette + matplotlib rcParams (one source of truth)
│   ├── pieces.py                   # shared builders: fits, the split figure, toy writers
│   ├── reveal_scatter.template.html  # pooled-vs-bands interactive (Simpson's/confounding/suppression)
│   ├── ecological.template.html      # individuals-vs-group-means interactive
│   └── selection.template.html       # draggable selection cutoff (Berkson)
├── explorations/
│   └── NN-<name>/
│       ├── build.py                # data + static figure + toy.html for that piece
│       ├── figures/                # generated PNGs
│       └── toy.html                # self-contained interactive (opens in any browser)
├── requirements.txt                # numpy, matplotlib
└── BACKLOG.md
```

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# build a piece (regenerates its figure(s) and toy.html)
.venv/bin/python explorations/01-simpsons-paradox/build.py

# then open the interactive
open explorations/01-simpsons-paradox/toy.html
```

## House style

Charts reuse the `williamcatt.dev` palette via `lib/style.py` (warm ivory
background, amber accent), so any figure can later slot straight into the portfolio.
No seaborn/plotly — hand-styled matplotlib. British spelling, plain language,
real citations.
