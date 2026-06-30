"""Shared builders for the reveal-scatter family of curiosities.

Most pieces here are the same shape: a pooled trend over all the points that
changes character once you split by a third variable (reverses, vanishes, or
appears). This module centralises the maths, the static "split" figure, and the
interactive toy so each piece's build.py is just data + labels.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import style

LIB = Path(__file__).resolve().parent


def fit(x, y):
    """(slope, intercept) of a simple linear fit."""
    m, b = np.polyfit(x, y, 1)
    return float(m), float(b)


def pearson(x, y):
    return float(np.corrcoef(x, y)[0, 1])


def reveal_payload(rows, bands, *, x_label, y_label, title, lede,
                   left, right, callout_pooled, callout_split,
                   state_pooled, state_split, hint, footer,
                   x_pad=0.5, y_pad=5.0):
    """Build the JSON payload shared by the static figure and the toy.

    rows: list of (x, y, band_index). bands: list of band labels.
    """
    x = np.array([r[0] for r in rows], float)
    y = np.array([r[1] for r in rows], float)
    b = np.array([r[2] for r in rows], int)
    pooled = fit(x, y)
    band_fits = [fit(x[b == i], y[b == i]) for i in range(len(bands))]
    return {
        "points": [{"x": round(xx, 3), "y": round(yy, 3), "band": int(bb)}
                   for xx, yy, bb in rows],
        "bands": list(bands),
        "bandColors": style.BAND_COLORS[: len(bands)],
        "pooled": {"m": pooled[0], "b": pooled[1]},
        "bandFits": [{"m": m, "b": b_} for m, b_ in band_fits],
        "xLabel": x_label, "yLabel": y_label,
        "title": title, "lede": lede, "left": left, "right": right,
        "calloutPooled": callout_pooled, "calloutSplit": callout_split,
        "statePooled": state_pooled, "stateSplit": state_split,
        "hint": hint, "footer": footer,
        "domain": {"x": [float(x.min()) - x_pad, float(x.max()) + x_pad],
                   "y": [float(y.min()) - y_pad, float(y.max()) + y_pad]},
        "_pooled": pooled, "_bandFits": band_fits,  # for the python figure
    }


def reveal_figure(path, payload, *, title, annotation, legend_loc="upper left"):
    """The static 'split by group' chart: coloured points, a fit per band, the
    dashed pooled line behind them. Mirrors Simpson's fig2."""
    style.apply_rcParams()
    pts = payload["points"]
    x = np.array([p["x"] for p in pts]); y = np.array([p["y"] for p in pts])
    b = np.array([p["band"] for p in pts])
    pm, pb = payload["_pooled"]
    xline = np.array([x.min(), x.max()])

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(xline, pm * xline + pb, color=style.GREY, lw=2.5, ls="--", zorder=1,
            label="pooled trend")
    for i, label in enumerate(payload["bands"]):
        c = style.BAND_COLORS[i]
        mask = b == i
        m, bb = payload["_bandFits"][i]
        ax.scatter(x[mask], y[mask], s=26, color=c, edgecolor="none", alpha=0.85,
                   label=label)
        xb = np.array([x[mask].min(), x[mask].max()])
        ax.plot(xb, m * xb + bb, color=c, lw=3, zorder=3)
    style.despine(ax)
    style.title_left(ax, title)
    ax.set_xlabel(payload["xLabel"]); ax.set_ylabel(payload["yLabel"])
    ax.legend(frameon=False, loc=legend_loc, fontsize=10)
    ax.annotate(annotation, xy=(0.97, 0.06), xycoords="axes fraction",
                ha="right", va="bottom", color=style.MUTED, fontsize=11)
    style.save(fig, str(path))
    plt.close(fig)


def _strip_private(payload):
    return {k: v for k, v in payload.items() if not k.startswith("_")}


def write_reveal_toy(out_path, payload):
    tpl = (LIB / "reveal_scatter.template.html").read_text()
    p = _strip_private(payload)
    html = (tpl.replace("__DATA__", json.dumps(p))
               .replace("__TITLE__", payload["title"])
               .replace("__LEDE__", payload["lede"])
               .replace("__LEFT__", payload["left"])
               .replace("__RIGHT__", payload["right"])
               .replace("__HINT__", payload["hint"])
               .replace("__FOOTER__", payload["footer"]))
    Path(out_path).write_text(html)


def write_selection_toy(out_path, payload):
    tpl = (LIB / "selection.template.html").read_text()
    html = (tpl.replace("__DATA__", json.dumps(payload))
               .replace("__TITLE__", payload["title"])
               .replace("__LEDE__", payload["lede"])
               .replace("__LEFT__", payload["left"])
               .replace("__RIGHT__", payload["right"])
               .replace("__HINT__", payload["hint"])
               .replace("__FOOTER__", payload["footer"]))
    Path(out_path).write_text(html)


def ecological_payload(rows, groups, *, x_label, y_label, title, lede, left, right,
                       callout_pooled, callout_split, state_pooled, state_split,
                       hint, footer, x_pad=1.0, y_pad=1.0):
    """Individual-level fit vs group-means fit (the two can disagree in sign)."""
    x = np.array([r[0] for r in rows], float)
    y = np.array([r[1] for r in rows], float)
    g = np.array([r[2] for r in rows], int)
    ind = fit(x, y)
    means = [(float(x[g == i].mean()), float(y[g == i].mean())) for i in range(len(groups))]
    mx = np.array([m[0] for m in means]); my = np.array([m[1] for m in means])
    meanfit = fit(mx, my)
    return {
        "points": [{"x": round(xx, 3), "y": round(yy, 3), "group": int(gg)}
                   for xx, yy, gg in rows],
        "groups": list(groups),
        "groupColors": style.BAND_COLORS[: len(groups)],
        "indFit": {"m": ind[0], "b": ind[1]},
        "groupMeans": [{"x": round(a, 3), "y": round(b, 3)} for a, b in means],
        "meanFit": {"m": meanfit[0], "b": meanfit[1]},
        "xLabel": x_label, "yLabel": y_label,
        "title": title, "lede": lede, "left": left, "right": right,
        "calloutPooled": callout_pooled, "calloutSplit": callout_split,
        "statePooled": state_pooled, "stateSplit": state_split,
        "hint": hint, "footer": footer,
        "domain": {"x": [float(x.min()) - x_pad, float(x.max()) + x_pad],
                   "y": [float(y.min()) - y_pad, float(y.max()) + y_pad]},
        "_ind": ind, "_meanfit": meanfit, "_means": means,
    }


def ecological_figure(path, payload, *, title, annotation):
    style.apply_rcParams()
    pts = payload["points"]
    x = np.array([p["x"] for p in pts]); y = np.array([p["y"] for p in pts])
    g = np.array([p["group"] for p in pts])
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    for i, label in enumerate(payload["groups"]):
        mask = g == i
        ax.scatter(x[mask], y[mask], s=20, color=style.BAND_COLORS[i], edgecolor="none",
                   alpha=0.45)
    im, ib = payload["_ind"]
    xl = np.array([x.min(), x.max()])
    ax.plot(xl, im * xl + ib, color=style.AMBER, lw=3, label="individual people")
    mm, mb = payload["_meanfit"]
    mx = np.array([m[0] for m in payload["_means"]])
    my = np.array([m[1] for m in payload["_means"]])
    ax.plot(np.sort(mx), mm * np.sort(mx) + mb, color=style.TEAL, lw=3, ls="-",
            label="group averages")
    ax.scatter(mx, my, s=90, color=style.BAND_COLORS[: len(mx)], edgecolor="white",
               linewidth=1.5, zorder=5)
    style.despine(ax); style.title_left(ax, title)
    ax.set_xlabel(payload["xLabel"]); ax.set_ylabel(payload["yLabel"])
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    ax.annotate(annotation, xy=(0.97, 0.06), xycoords="axes fraction", ha="right",
                va="bottom", color=style.MUTED, fontsize=11)
    style.save(fig, str(path)); plt.close(fig)


def write_ecological_toy(out_path, payload):
    tpl = (LIB / "ecological.template.html").read_text()
    p = _strip_private(payload)
    html = (tpl.replace("__DATA__", json.dumps(p))
               .replace("__TITLE__", payload["title"])
               .replace("__LEDE__", payload["lede"])
               .replace("__LEFT__", payload["left"])
               .replace("__RIGHT__", payload["right"])
               .replace("__HINT__", payload["hint"])
               .replace("__FOOTER__", payload["footer"]))
    Path(out_path).write_text(html)


def write_noncollapse_toy(out_path, payload):
    tpl = (LIB / "noncollapse.template.html").read_text()
    html = (tpl.replace("__DATA__", json.dumps(payload))
               .replace("__TITLE__", payload["title"])
               .replace("__LEDE__", payload["lede"])
               .replace("__LEFT__", payload["left"])
               .replace("__RIGHT__", payload["right"])
               .replace("__HINT__", payload["hint"])
               .replace("__FOOTER__", payload["footer"]))
    Path(out_path).write_text(html)


def write_lord_toy(out_path, payload):
    tpl = (LIB / "lord.template.html").read_text()
    html = (tpl.replace("__DATA__", json.dumps(payload))
               .replace("__TITLE__", payload["title"])
               .replace("__LEDE__", payload["lede"])
               .replace("__LEFT__", payload["left"])
               .replace("__RIGHT__", payload["right"])
               .replace("__HINT__", payload["hint"])
               .replace("__FOOTER__", payload["footer"]))
    Path(out_path).write_text(html)
