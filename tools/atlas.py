"""The atlas plate: a figure for the history layer drawn to one house style.

    import sys; sys.path.insert(0, "tools")
    import atlas
    fig, ax = atlas.plate("Greely's winter at Fort Conger, 1881-1883",
                          "Daily minimum air temperature as read at the station, against the Alert normals of 1991-2020")
    ax.plot(dates, temps)
    atlas.finish(fig, ax, "Greely 1888, vol. 1 appendix; ECCC climate normals",
                 "the-weather-and-the-climate/files/the-weather-and-the-climate-fig-conger-winter.png",
                 ylabel="air temperature (F)", ylabel_right="C", convert=lambda f: (f - 32) * 5 / 9)

The look is an atlas plate, not a lab figure: warm paper, a serif face, a
title set left like a caption, a one-line source at the foot, no box round
the plot, no chart junk. Every researcher's figures use it so the layer
reads as one book. Colours: ink blue first, then ochre, moss, gold, plum,
teal, madder.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
plt.style.use(str(ROOT / "tools" / "atlas.mplstyle"))

INK, OCHRE, MOSS, GOLD, PLUM, TEAL, MADDER = (
    "#1f3a5f", "#a4552b", "#5b7553", "#8b6f2e", "#6d5a7a", "#2e6f7e", "#b23a3a")
PAPER, RULE, MUTED = "#f7f3ea", "#d9d2c3", "#7a7264"


def plate(title: str, subtitle: str = "", size=(16, 9)):
    """A figure with the title and subtitle set like a caption, top left."""
    fig, ax = plt.subplots(figsize=size)
    fig.subplots_adjust(left=0.07, right=0.95, top=0.84, bottom=0.14)
    fig.text(0.07, 0.94, title, fontsize=20, ha="left", va="top")
    if subtitle:
        fig.text(0.07, 0.895, subtitle, fontsize=12.5, color=MUTED, ha="left", va="top")
    return fig, ax


def finish(fig, ax, sources: str, path: str | Path, ylabel: str = "", xlabel: str = "",
           ylabel_right: str = "", convert=None, note: str = "") -> Path:
    """Label the axes, add a converted scale on the right when the original
    unit is not the reader's, set the source line at the foot, save."""
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    if convert is not None and ylabel_right:
        lo, hi = ax.get_ylim()
        twin = ax.twinx()
        twin.set_ylim(convert(lo), convert(hi))
        twin.set_ylabel(ylabel_right)
        twin.grid(False)
        twin.spines["top"].set_visible(False)
    if note:
        fig.text(0.07, 0.065, note, fontsize=10.5, color=MUTED, ha="left", va="top")
    fig.text(0.07, 0.03, f"Sources: {sources}", fontsize=10, color=MUTED, ha="left", va="bottom")
    fig.text(0.95, 0.03, "CCGS Amundsen history layer", fontsize=9, color=MUTED, ha="right", va="bottom")
    out = ROOT / "db" / "history" / path if not str(path).startswith("/") else Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out)
    plt.close(fig)
    return out


def polar_map(ax, lat_min=70, lat_max=85, lon_min=-125, lon_max=-55):
    """A plain graticule for a small map when no basemap is at hand: the
    caller plots lon/lat straight on. Coastlines: shapely + the GSHHG
    shoreline under /data/gis if the figure wants them."""
    ax.set_xlim(lon_min, lon_max)
    ax.set_ylim(lat_min, lat_max)
    ax.set_aspect(1 / 0.35)
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")
