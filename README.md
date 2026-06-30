# Data Curiosities

*Counterintuitive statistics, one chart at a time — bite-sized data-science tidbits,
each "wait, what?" grounded in real published work. Built while working through the
Claude Skilljar course; lives at [williamcatt.dev/projects/data-curiosities](https://williamcatt.dev/projects/data-curiosities.html).*

Each piece takes a counter-intuitive statistical idea, grounds it in real published
work, and explains it with hand-made charts (and, where it helps, a small
interactive). Aimed at being fun for data and non-data people alike.

## Pieces

| # | Topic | What it shows |
|---|-------|---------------|
| 01 | [Simpson's Paradox](explorations/01-simpsons-paradox/notes.md) | A trend true in every age group reverses once you pool the groups. Interactive age-reveal slider + the real kidney-stone case. |

See [`BACKLOG.md`](BACKLOG.md) for what's next.

## Layout

```
Skilljar Data Exploration/
├── lib/style.py                      # shared palette + matplotlib rcParams (one source of truth)
├── explorations/
│   └── 01-simpsons-paradox/
│       ├── build.py                  # generates the data, figures, and toy.html
│       ├── notes.md                  # the explainer + cited sources
│       ├── toy.html                  # self-contained interactive (opens in any browser)
│       ├── toy.template.html         # template build.py inlines the data into
│       ├── figures/                  # generated PNGs (gitignored)
│       └── data/                     # generated data.json (gitignored)
├── requirements.txt                  # numpy, matplotlib
└── BACKLOG.md
```

## Run

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# build a piece (regenerates its figures, data.json, and toy.html)
.venv/bin/python explorations/01-simpsons-paradox/build.py

# then open the interactive
open explorations/01-simpsons-paradox/toy.html
```

## House style

Charts reuse the `williamcatt.dev` palette via `lib/style.py` (warm ivory
background, amber accent), so any figure can later slot straight into the portfolio.
No seaborn/plotly — hand-styled matplotlib. British spelling, plain language,
real citations.
