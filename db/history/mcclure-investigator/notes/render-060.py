#!/usr/bin/env python3
"""Render mcclure-investigator-060 (the 1853 new-coastline map) as a PNG:
the three sledge tracks that charted the new coastline (McClintock,
Mecham, Hamilton) over a plain lat/lon graticule, no coastline basemap
available offline. Run with .ocr-venv/bin/python (has matplotlib)."""
import json
import sqlite3
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

ROOT = Path("/data/dev/arctic-history")
DB = ROOT / "db/history/history.sqlite"
OUT = ROOT / "db/history/mcclure-investigator/files/mcclure-investigator-060-new-coastline-1853.png"

TRACKS = [
    ("mcclure-investigator-009", "McClintock", "#1f5fa8", "o"),
    ("mcclure-investigator-010", "Mecham", "#b8412f", "s"),
    ("mcclure-investigator-011", "Hamilton", "#3f8f3f", "^"),
]

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

routes = []
all_lat, all_lon = [], []
for tid, label, color, marker in TRACKS:
    r = conn.execute("SELECT waypoints FROM artifacts WHERE id=?", (tid,)).fetchone()
    wp = json.loads(r["waypoints"])
    lats = [p["lat"] for p in wp]
    lons = [p["lon"] for p in wp]
    all_lat += lats
    all_lon += lons
    routes.append((label, color, marker, lats, lons))

lat0, lat1 = min(all_lat) - 0.4, max(all_lat) + 0.4
lon0, lon1 = min(all_lon) - 0.6, max(all_lon) + 0.6

fig, ax = plt.subplots(figsize=(9.5, 8.0), dpi=200)
fig.patch.set_facecolor("#f4f1ea")
ax.set_facecolor("#eef3f7")

# graticule: 1-degree lines, labelled
lat_ticks = list(range(int(lat0 // 1) * 1, int(lat1) + 2, 1))
lon_ticks = list(range(int(lon0 // 1) * 1, int(lon1) + 2, 1))
for la in lat_ticks:
    if lat0 <= la <= lat1:
        ax.axhline(la, color="#9fb0bd", linewidth=0.5, zorder=1)
for lo in lon_ticks:
    if lon0 <= lo <= lon1:
        ax.axvline(lo, color="#9fb0bd", linewidth=0.5, zorder=1)

ax.set_xlim(lon0, lon1)
ax.set_ylim(lat0, lat1)
ax.set_xticks([lo for lo in lon_ticks if lon0 <= lo <= lon1])
ax.set_yticks([la for la in lat_ticks if lat0 <= la <= lat1])
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, pos: f"{abs(v):.0f}°W"))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, pos: f"{v:.0f}°N"))
ax.tick_params(labelsize=8, colors="#40525e")
for spine in ax.spines.values():
    spine.set_color("#5c6b74")

ax.set_aspect(1 / max(0.15, __import__("math").cos(__import__("math").radians((lat0 + lat1) / 2))))

label_offsets = {
    "McClintock": (8, 14),
    "Mecham": (8, -2),
    "Hamilton": (8, -18),
}
for label, color, marker, lats, lons in routes:
    ax.plot(lons, lats, color=color, linewidth=1.8, zorder=3, solid_capstyle="round", label=label)
    ax.scatter(lons, lats, color=color, marker=marker, s=16, zorder=4,
               edgecolors="white", linewidths=0.4)
    # mark the shared start point (Dealy Island) once; label each track's own end, staggered
    ax.annotate(label, (lons[-1], lats[-1]), textcoords="offset points",
                xytext=label_offsets[label], fontsize=8.5, color=color, fontweight="bold")

# Dealy Island start marker (all three depart from/return to it)
ax.scatter([-108.733], [74.95], color="black", marker="*", s=90, zorder=5)
ax.annotate("Dealy Island\n(Resolute & Intrepid)", (-108.733, 74.95), textcoords="offset points",
            xytext=(8, -34), fontsize=7.5, color="#222", ha="left")

fig.suptitle("New coastline charted by Kellett's division, 1853", fontsize=13.5,
             fontweight="bold", color="#20303a", y=0.975)
ax.set_title(
    "Sledge routes of M'Clintock, Mecham and Hamilton from Dealy Island, Melville Island — "
    "graticule only, no charted coastline available offline",
    fontsize=8.5, color="#4a5a63", pad=10)

legend = ax.legend(loc="lower left", fontsize=8.5, framealpha=0.9, title="Sledge party")
legend.get_title().set_fontsize(8.5)

credit = ("Routes reconstructed from M'Dougall 1857, appendix p. 496 and the officers' printed "
          "journals (Further Papers relative to the Recent Arctic Expeditions, 1855); "
          "Internet Archive. Positions to c. 10 km; several inferred between named landmarks.")
fig.text(0.02, 0.012, credit, fontsize=6.7, color="#5a5a5a", wrap=True)

fig.tight_layout(rect=(0, 0.035, 1, 0.955))
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, facecolor=fig.get_facecolor())
print("wrote", OUT, OUT.stat().st_size, "bytes")
