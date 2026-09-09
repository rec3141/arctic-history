#!/usr/bin/env python3
"""Route the History tab's voyage tracks through water instead of across the islands.

A track artifact's line is its waypoints joined straight, and the waypoints are
150 to 400 km apart, so almost every voyage cuts over Baffin Island, Somerset or
Greenland.  This routes each consecutive pair of waypoints along the least-cost
water path over a land mask, straightens and smooths the result, and writes it
out for review.  ``waypoints`` are never touched: they stay the truth, the
markers and the table, and every waypoint stays exactly on the routed line.

    tools/route-tracks.py --all                 route every track, write nothing to the database
    tools/route-tracks.py --track ross-parry-003 --track frobisher-001
    tools/route-tracks.py --all --jobs 12       workers (default: cores - 4)
    tools/route-tracks.py --straits             only check the two narrow straits
    tools/route-tracks.py --all --rebuild-masks throw the cached masks and cost surfaces away first
    tools/route-tracks.py --all --no-figures    skip the pictures
    tools/route-tracks.py --all --theirs DIR    compare against another run's per-track GeoJSON
                                                for the tracks it has not written to the db yet
    tools/route-tracks.py --all --gc-step-km 20 how finely an as-given track's great-circle legs
                                                are drawn (the default; --as-given-straight is the
                                                old bare-waypoint line)
    tools/route-tracks.py --all --write         ALSO write geometry and routing into the database

Run it from the repository root with the routing venv:

    .route-venv/bin/python tools/route-tracks.py --all

made with `uv venv .route-venv --python 3.11 && uv pip install --python
.route-venv/bin/python numpy scipy scikit-image pillow shapely pyproj rasterio`.
rasterio's wheel carries its own GDAL, so no GDAL command-line tool is needed.
Only the mask build needs rasterio; once the masks are cached, numpy, scipy,
scikit-image and Pillow are enough.

## What it writes

Everything lands in db/history/_ledger/routing/ (gitignored):

    routes.geojson      one Feature per track: the routed line as the geometry,
                        and id / title / routing / the straight line and the
                        numbers in the properties
    summary.md          per-track flag decision, land fractions, point counts,
                        seconds, fallbacks; the mask header and the strait
                        check; and a COMPARISON section against whatever the
                        live database holds
    figures/*.png       three-voyages, archipelago, overview, six zooms on the
                        places that decide a route, and a contact sheet

**The database is not touched unless --write is given.**  --write is OFF by
default and exists so that, once the crew is happy with the lines, the same
tool can put them in: it calls ``H.add_artifact`` with every field of the row
as it stands plus ``routing=`` and ``geometry=``, so no other column moves and
``waypoints`` is passed through unchanged.  Every track gets both a flag and a
geometry, whichever way it is drawn.

## The flag

Each track carries a ``routing`` flag, which the crew owns:

    water       the line is routed through water (voyages)
    as-given    the line follows the waypoints as they are given, and the
                router never moves it aside for land (sledge, overland, drift,
                retreat, ice journeys, walks, marches, patrols, flights)
    ''          nobody has decided yet

**--as-given-great-circle is the default and there is no flag to ask for it.**
An as-given track is not left as a bare list of waypoints: its legs are drawn
as great-circle arcs, densified to a point every 20 km (--gc-step-km) along
the geodesic and safe across the antimeridian.  Two waypoints 400 km apart at
80 N are 60 km from the geodesic at the middle of a Mercator straight line, so
Peary's sledge route, a B-29 over the Pole and Bartlett's walk to Siberia all
drew as bows through the wrong ice until this.  ``--as-given-straight`` puts
the old bare-waypoint line back.

An unset flag is decided by the title-and-tags rule below and the decision is
reported in summary.md as the value a --write run would set.  A flag already
set is obeyed: 'as-given' is never routed, 'water' always is.

The rule is the prototype's word list, mended.  Title words are matched whole,
so "Prince of Wales Island" is not a walk.  Tags are matched as whole tokens,
not as substrings, so the ship tracks tagged `eastern-arctic-patrol` are not
swept up with the sledge patrols tagged `patrol`.  Month names are stripped
from the title first, so "March-April 1853" is not read as a march.  Patrol,
migration, flight and "and back" are added to the words, which catches the
RCMP sledge patrols, Qitdlarssuaq's migration and the aerial surveys that the
prototype routed through water.  And a short table of decisions by
hand (OVERRIDES) carries what the words cannot settle -- Cook's two companions,
Peary over the sea ice, the Krüger search parties, the coast Iligliuk drew, and
the C.G.S. Arctic's sovereignty voyage, a ship tagged `patrol` along with the
sledge patrols.  Every override is listed in summary.md with its reason, and so
is every decision the rule made on its own.

## The masks

Two land masks are built once from GSHHG (Wessel and Smith's shoreline; the zip
is fetched to db/history/_ledger/masks/) and cached there, level 1 only -- a
lake is not sea:

    fine    1 km cells, Web Mercator, -150..15 E, 35..86 N, from the full
            resolution shoreline, 18368 x 17233 cells.  A Web Mercator cell
            shrinks as the cosine of the latitude, so those cells are 800 m on
            the ground off Newfoundland and 300 m in Lancaster Sound: finer,
            where it matters, than the 500 m the issue asked for.  Bellot
            Strait, whose tightest place is 900 m wide, and Fury and Hecla
            Strait at 1.6 km stay open on it; --straits proves it.
    coarse  0.045 degree cells (about 5 km), equirectangular, 130 W..130 E the
            long way through the Pacific, 60 S..84 N, from the intermediate
            shoreline, for the approaches by Bering Strait and the Pacific.

A segment is routed on the fine mask when both its ends lie in it, else on the
coarse one, else it is left as a great circle.  When a fine route has to cross
real land -- the Polar Sea's last leg runs from Prudhoe Bay to Seattle, and the
water between them goes through Bering Strait, which the fine mask does not
reach -- the coarse mask is asked instead.

The cost surface is built once per mask and cached as a memory-mapped float32
.npy, so a run never recomputes it and every worker process shares one copy.
The cost of stepping into a cell is

    water   (its ground length in km) x (1 + 4 exp(-d/25 km) + 8 exp(-d/4 km))
    land    5000

with d the distance to the coast, in ground kilometres.  Costing a step by its
ground length rather than by the cell makes the cheapest path the shortest on
the ground and not the shortest on the page, which matters when a cell at 80 N
is a third of a cell at 45 N.  The long penalty term gives a channel a cost
minimum along its centreline, so a route sits in the middle of Lancaster Sound
rather than against one shore; the short term gives an open coast a standoff of
several kilometres.  Land at 5000 is dear enough that no detour is worth a
shortcut across a spit.

## The routing

Every consecutive pair of waypoints is routed on its own, in a window that is
the pair's bounding box plus a margin proportional to the distance, in two
levels: first over the cost surface downsampled 4x (a cell is land only when
all sixteen of its cells are, so a two-kilometre strait is still open there),
then again at full resolution inside a corridor of 20 km around that path,
everything outside the corridor set to infinity so scikit-image's MCP_Geometric
never looks at it.  Because MCP costs one pass over whatever array it is handed,
the full-resolution pass is run only along the stretches of the coarse path that
come within about 70 km of a coast -- mid-ocean the coarse path is already a
straight line and the straightening below would collapse it anyway -- and each
stretch is cut so its window stays under four million cells.  If the corridor
route still crosses land the corridor is widened and, failing that, the whole
window is searched at full resolution.  A waypoint in a land cell (a harbour, a
camp on the shore) starts from the nearest water within 20 km.

A grid's least-cost path is a staircase of 45 and 90 degree moves, so each
segment is then

  - simplified to 0.5 km,
  - pulled straight: from each kept point, the farthest later point whose
    straight line touches no land, found by doubling and then bisecting,
  - simplified to 1 km,
  - and rounded by three guarded Chaikin passes -- a corner is cut only when
    the cut itself touches no land, so a smoothed line can never cross a
    shore that the straightened one respected,
  - and thinned of collinear points, again only where the shortcut is clear.

All of that happens within one segment, never across a waypoint, so every
waypoint stays exactly on the line and an out-and-back voyage keeps its far
end.

## Rerunning

Everything is cached and nothing is incremental: a rerun rebuilds every track
from the waypoints in the database, in a few seconds for the lot, and
overwrites routes.geojson, summary.md and the figures.  Only the masks and
cost surfaces survive between runs; --rebuild-masks throws them away.
"""
import argparse, json, math, os, re, struct, sys, time, zipfile
import multiprocessing as mp
from pathlib import Path

import numpy as np
from scipy import ndimage
from skimage.graph import route_through_array

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

LEDGER = ROOT / "db" / "history" / "_ledger"
MASKS = LEDGER / "masks"
OUT = LEDGER / "routing"
FIGS = OUT / "figures"
GSHHG_URL = "https://www.soest.hawaii.edu/pwessel/gshhg/gshhg-shp-2.3.7.zip"

# ------------------------------------------------------------------ the rule
# a whole tag token, or one of these words in the title, means the journey went
# over ice or land and its line is drawn as its waypoints are given
TITLE_WORDS = (r"sledg(?:e|es|ed|ing)", r"sledge-journey", r"man-haul(?:ed|ing)?", r"overland",
               r"on foot", r"ice[- ]journey", r"ice[- ]floe", r"ice[- ]island", r"drift(?:s|ed|ing)?",
               r"retreat(?:s|ed|ing)?", r"walk(?:s|ed|ing)?", r"skis?", r"ride to", r"across",
               r"crossing of", r"migration", r"sleeping places", r"and back", r"patrols?",
               r"march(?:es|ed|ing)?")
# whole words only: "Prince of Wales Island" is not a walk, and "Walker" is not one either
TITLE_RE = re.compile(r"\b(?:" + "|".join(TITLE_WORDS) + r")\b", re.I)
TAG_WORDS = {"sledge", "sledging", "sledge-journey", "sledge-journeys", "man-hauling",
             "overland", "drift", "floe-drift", "retreat", "walk", "march", "ski",
             "ice-island", "ice-cap", "iceshelf", "ice-shelf", "migration", "patrol",
             "flying", "aircraft", "sledging-journey"}
MONTHS = ("january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december")

# the tracks the word rule cannot settle: journeys whose title and tags say
# nothing about how they travelled, and one ship voyage tagged with the sledge
# patrols.  Read off the titles; each is a judgement, and the crew's flag
# replaces it.
OVERRIDES = {
    "cook-1908-axel-heiberg-002": ("as-given", "Cook's return by sledge and canvas boat over the sea ice of Eureka and Jones Sounds"),
    "greenland-inughuit-043": ("as-given", "Ahwelah and Etukishook's account of the same sledge journey with Cook"),
    "haig-thomas-1937-002": ("as-given", "a sledge survey of south-east Ellesmere"),
    "inuit-oral-history-029": ("as-given", "a coastline Iligliuk drew on a chart, not a track through water"),
    "kruger-1930-001": ("as-given", "Krüger's sledge party from Bache Peninsula, lost"),
    "kruger-1930-002": ("as-given", "Stallworthy's sledge search"),
    "kruger-1930-003": ("as-given", "Stallworthy's sledge search around Axel Heiberg"),
    "oxford-ellesmere-1934-002": ("as-given", "a sledge journey to Grant Land"),
    "oxford-ellesmere-1934-003": ("as-given", "a sledge journey through Grinnell and Ellesmere Land"),
    "oxford-ellesmere-1934-004": ("as-given", "a sledge journey to Scoresby Bay"),
    "pole-seekers-from-ellesmere-006": ("as-given", "Peary's 1909 route over the sea ice to the Pole"),
    "pole-seekers-from-ellesmere-007": ("as-given", "Peary's 1906 route over the sea ice"),
    "qei-from-the-air-1947-023": ("as-given", "a B-29 flight over the Pole"),
    "qei-from-the-air-1947-024": ("as-given", "where an aerial survey flew, season by season"),
    "sverdrup-bernier-peary-002": ("water", "the C.G.S. Arctic's sovereignty voyage: a ship, tagged "
                                            "`patrol` along with the sledge patrols"),
}
# the ones the rule decides but a reader might argue with; listed for the crew
DEBATABLE = {
    "thule-dorset-001": "a schematic migration by umiak along the coast and by sledge over the ice",
    "greenland-inughuit-016": "Qitdlarssuaq's migration went by sledge over the sea ice and the coasts",
    "greenland-inughuit-017": "the same migration turning back",
    "mcclure-investigator-014": "the Resolute's drift, and then her voyage to New London under salvage",
    "franklin-1845-002": "the drift of the ships after 1848, as the Inuit testimony describes it",
    "norse-helluland-012": "the Nordrsetur hunting grounds: a sea route drawn between the hunting places",
    "franklin-search-023": "HMS Resolute: a voyage, then a besetment and a drift, in one line",
}

FINE = dict(name="fine", proj="merc", bbox=(-150.0, 35.0, 15.0, 86.0), res=1000.0,
            member="GSHHS_shp/f/GSHHS_f_L1.shp",
            label="1 km, Web Mercator, full-resolution GSHHG")
COARSE = dict(name="coarse", proj="plate", bbox=(-230.0, -60.0, 130.0, 84.0), res=0.045,
              member="GSHHS_shp/i/GSHHS_i_L1.shp",
              label="0.045 deg (~5 km), equirectangular, intermediate GSHHG")

# the two narrow straits the fine mask must keep open: a point at each end and
# the window (south, west, north, east) to look for a water path in
STRAITS = {
    "Bellot Strait": ((71.99, -93.60), (71.92, -95.90), (71.4, -96.6, 72.5, -93.0)),
    "Fury and Hecla Strait": ((69.60, -81.40), (69.95, -86.90), (69.0, -87.6, 70.6, -80.6)),
}

COST_LAND = 5000.0
COAST_FAR, COAST_FAR_KM = 4.0, 25.0     # centres a channel, stands a route off a coast
COAST_NEAR, COAST_NEAR_KM = 8.0, 4.0    # a few kilometres of clearance from the shore itself
SNAP_KM = 20.0
CORRIDOR_KM = 20.0
WINDOW_MIN_KM = 250.0
WINDOW_MAX_CELLS = 1400
LEVEL1_MAX_CELLS = 500_000
REFINE_BUDGET = 4_000_000
NEAR_PENALTY = 0.25         # refine at full resolution within ~70 km of a coast
CROSS_TOL_KM = 2.0          # a route this far over land is a crossing worth saying
BIG_CROSS_KM = 25.0         # and this far means the fine mask does not hold the way round
HUG_KM = 5.0                # closer than this to a shore is hugging it
GC_STEP_KM = 20.0           # a point every this far along an as-given great-circle leg
DOWN = 4                                # the first level's downsampling
SIMPLIFY_KM = 1.0
CHAIKIN_PASSES = 3
R_EARTH = 6371.0088
M_MERC = 20037508.342789244
R_MERC = 6378137.0

ZOOMS = [
    ("bellot-strait", "Bellot Strait", (71.20, -97.60, 72.60, -91.60)),
    ("fury-and-hecla", "Fury and Hecla Strait", (68.60, -88.60, 70.60, -79.40)),
    ("lancaster-barrow", "Lancaster Sound and Barrow Strait", (72.60, -102.00, 76.20, -74.00)),
    ("melville-bay-north-water", "Melville Bay and the North Water", (73.40, -80.00, 78.60, -54.00)),
    ("hudson-strait", "Hudson Strait", (59.60, -79.00, 65.00, -62.00)),
    ("smith-sound-kane", "Smith Sound and Kane Basin", (77.20, -82.00, 81.20, -58.00)),
]


# ------------------------------------------------------------------ geodesy
def gc_km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R_EARTH * math.asin(min(1.0, math.sqrt(h)))


def great_circle(a, b, step_km=50.0):
    """Points along the great circle from a to b, (lat, lon), every step_km."""
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    d = gc_km(a, b) / R_EARTH
    if d < 1e-9:
        return [a, b]
    n = max(1, int(d * R_EARTH / step_km))
    out = []
    for i in range(n + 1):
        f = i / n
        A, B = math.sin((1 - f) * d) / math.sin(d), math.sin(f * d) / math.sin(d)
        x = A * math.cos(la1) * math.cos(lo1) + B * math.cos(la2) * math.cos(lo2)
        y = A * math.cos(la1) * math.sin(lo1) + B * math.cos(la2) * math.sin(lo2)
        z = A * math.sin(la1) + B * math.sin(la2)
        out.append((math.degrees(math.atan2(z, math.hypot(x, y))), math.degrees(math.atan2(y, x))))
    out[0], out[-1] = a, b
    return out


def unwrap(lon0, lon):
    """lon moved by a whole turn so that it is within 180 degrees of lon0."""
    return lon + 360.0 * round((lon0 - lon) / 360.0)


def densify(pts, step_km):
    """A polyline sampled every step_km on the ground, dateline-safe."""
    out = []
    for a, b in zip(pts, pts[1:]):
        n = max(1, min(20000, int(gc_km(a, b) / step_km)))
        lb = unwrap(a[1], b[1])
        for i in range(n):
            f = i / n
            out.append((a[0] + f * (b[0] - a[0]), a[1] + f * (lb - a[1])))
    out.append(pts[-1])
    return out


def simplify(pts, tol_km):
    """Douglas-Peucker on (lat, lon), tolerance in km (flat and local, which is
    all a 1 km tolerance needs)."""
    if len(pts) < 3:
        return list(pts)
    lat0 = pts[0][0]
    ky, kx = 111.0, 111.0 * max(0.05, math.cos(math.radians(lat0)))
    xy = np.array([[unwrap(pts[0][1], p[1]) * kx, p[0] * ky] for p in pts])
    keep, stack = {0, len(pts) - 1}, [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j - i < 2:
            continue
        a, b = xy[i], xy[j]
        d = b - a
        seg = xy[i + 1:j] - a
        L2 = float(d @ d)
        if L2 == 0.0:
            dist = np.hypot(seg[:, 0], seg[:, 1])
        else:
            t = np.clip((seg @ d) / L2, 0.0, 1.0)
            dist = np.hypot(seg[:, 0] - t * d[0], seg[:, 1] - t * d[1])
        k = int(np.argmax(dist))
        if dist[k] > tol_km:
            keep.add(i + 1 + k)
            stack += [(i, i + 1 + k), (i + 1 + k, j)]
    return [pts[k] for k in sorted(keep)]


# ------------------------------------------------------- the shoreline file
def gshhg_zip(path: Path) -> Path:
    if not path.exists():
        import urllib.request
        path.parent.mkdir(parents=True, exist_ok=True)
        print(f"fetching {GSHHG_URL} (149 MB)", file=sys.stderr)
        urllib.request.urlretrieve(GSHHG_URL, path)
    return path


def read_polygons(zpath: Path, member: str):
    """Every polygon ring in a GSHHG shapefile, as (n, 2) lon/lat arrays with the
    record's bounding box.  GSHHG's L1 records are single-part polygons in
    geographic coordinates; the .shp is read straight, so no OGR is needed."""
    buf = zipfile.ZipFile(zpath).read(member)
    if struct.unpack_from(">i", buf, 0)[0] != 9994 or struct.unpack_from("<i", buf, 32)[0] != 5:
        raise SystemExit(f"{member} is not a polygon shapefile")
    pos = 100
    while pos < len(buf):
        clen = struct.unpack_from(">i", buf, pos + 4)[0]
        box = struct.unpack_from("<4d", buf, pos + 12)
        nparts, npoints = struct.unpack_from("<ii", buf, pos + 44)
        parts = np.frombuffer(buf, np.int32, nparts, pos + 52)
        xy = np.frombuffer(buf, np.float64, npoints * 2, pos + 52 + 4 * nparts).reshape(-1, 2)
        for k, start in enumerate(parts):
            end = parts[k + 1] if k + 1 < nparts else npoints
            if end - start >= 4:
                yield box, xy[start:end]
        pos += 8 + clen * 2


# --------------------------------------------------------------- the masks
class Grid:
    """A land mask on a regular grid, its cached cost surface, the conversions
    between (lat, lon) and (row, col), and the least-cost water route.

    ``proj`` is 'merc' (Web Mercator metres, EPSG:3857) or 'plate'
    (equirectangular degrees, so a grid can hold the whole Pacific).  A cell's
    size on the ground varies with latitude in both, so ``gkm`` holds it per row
    and every distance the router uses -- the coast penalty, the snap radius,
    the corridor, the window, the cost of a step -- is in ground kilometres."""

    def __init__(self, spec, zpath: Path, rebuild=False):
        self.name, self.proj, self.res, self.label = spec["name"], spec["proj"], spec["res"], spec["label"]
        w, s, e, n = self.bbox = spec["bbox"]
        if self.proj == "merc":
            x0, y0 = merc_fwd(s, w)
            x1, y1 = merc_fwd(n, e)
        else:
            x0, x1, y0, y1 = w, e, s, n
            self.lon0 = w
        self.ncols = int(round((x1 - x0) / self.res))
        self.nrows = int(round((y1 - y0) / self.res))
        self.x0, self.y1 = x0, y0 + self.nrows * self.res
        meta = {"proj": self.proj, "res": self.res, "bbox": list(self.bbox),
                "member": spec["member"], "shape": [self.nrows, self.ncols]}
        mpath, jpath = MASKS / f"{self.name}.mask.npy", MASKS / f"{self.name}.meta.json"
        MASKS.mkdir(parents=True, exist_ok=True)
        if not rebuild and mpath.exists() and jpath.exists() and json.loads(jpath.read_text()) == meta:
            self.land = np.unpackbits(np.load(mpath), count=self.nrows * self.ncols).reshape(self.nrows, self.ncols).astype(bool)
        else:
            self.land = self._build(zpath, spec["member"])
            np.save(mpath, np.packbits(self.land))
            jpath.write_text(json.dumps(meta))
        self._costs(rebuild, meta)
        self.gkm = self._row_km(self.nrows)[0]      # ground km per cell, per row
        self.gkm4 = self._row_km(-(-self.nrows // DOWN), DOWN)[0]
        print(f"{self.name}: {self.ncols} x {self.nrows} cells, {self.label}, "
              f"land {self.land.mean():.1%}, cell {self.gkm.min():.2f}-{self.gkm.max():.2f} km "
              f"on the ground", file=sys.stderr)

    def cells(self, km, r):
        """How many cells a ground distance spans at row r."""
        return max(1, int(round(km / self.gkm[min(max(int(r), 0), self.nrows - 1)])))

    def km_at(self, r):
        return float(self.gkm[min(max(int(r), 0), self.nrows - 1)])

    # -- building
    def _build(self, zpath, member):
        import rasterio.features
        from rasterio.transform import from_origin
        t0 = time.time()
        w, s, e, n = self.bbox
        rings, npts = [], 0
        for box, xy in read_polygons(zpath, member):
            for shift in ((0.0,) if self.proj == "merc" else (0.0, -360.0, 360.0)):
                if box[2] + shift < w or box[0] + shift > e or box[3] < s or box[1] > n:
                    continue
                a = xy.copy()
                a[:, 0] += shift
                if self.proj == "merc":
                    lat = np.clip(a[:, 1], -89.5, 89.5)
                    a = np.column_stack([a[:, 0] / 180.0 * M_MERC,
                                         R_MERC * np.log(np.tan(np.pi / 4 + np.radians(lat) / 2))])
                rings.append(a)
                npts += len(a)
        shapes = [({"type": "Polygon", "coordinates": [a.tolist()]}, 1) for a in rings]
        land = rasterio.features.rasterize(
            shapes, out_shape=(self.nrows, self.ncols), fill=0, dtype="uint8",
            transform=from_origin(self.x0, self.y1, self.res, self.res), all_touched=False)
        print(f"{self.name}: {len(rings)} polygons, {npts} vertices rasterized in "
              f"{time.time() - t0:.0f} s", file=sys.stderr)
        if not land.any():
            raise SystemExit(f"{self.name}: the mask came out empty")
        return land.astype(bool)

    def _row_km(self, nrows, down=1):
        """The ground size of a cell, in km, for every row of a grid: a Web
        Mercator cell shrinks as cos(latitude), so the "1 km" fine mask is about
        300 m on the ground in Lancaster Sound and 900 m off Newfoundland.
        Everything the router measures -- the coast penalty, the snap radius,
        the corridor, the window -- is in ground kilometres because of this, and
        so is the cost of a step, so that the cheapest path is the shortest on
        the ground and not the shortest on the page."""
        res = self.res * down
        r = np.arange(nrows) + 0.5
        if self.proj == "merc":
            lat = np.degrees(2 * np.arctan(np.exp((self.y1 - r * res) / R_MERC)) - np.pi / 2)
            return res / 1000.0 * np.cos(np.radians(lat)), np.cos(np.radians(lat))
        lat = self.y1 - r * res
        cos = np.clip(np.cos(np.radians(lat)), 0.05, 1.0)
        return res * 111.32 * np.sqrt(cos), cos

    def _cost_from_land(self, land, out, gkm, cos, down=1):
        """The cost of stepping into a cell: its ground length in km in open
        water, multiplied by 1 + a coast penalty, and COST_LAND on land.
        Written band by band so the distance transform never holds the whole
        grid; the halo carries a coast just outside a band into it, far enough
        out that the penalty there is below a part in a hundred."""
        n, w = land.shape
        step = max(256, min(4096, 2 ** 26 // max(1, w)))
        for a in range(0, n, step):
            b = min(n, a + step)
            halo = int(min(900, max(8, 5.0 * COAST_FAR_KM / gkm[a:b].min())))
            A, B = max(0, a - halo), min(n, b + halo)
            blk = land[A:B]
            g = gkm[A:B, None].astype(np.float32)
            if blk.all():
                out[a:b] = COST_LAND
                continue
            if not blk.any():
                out[a:b] = g[a - A:b - A]
                continue
            if self.proj == "merc":
                d = ndimage.distance_transform_edt(~blk) * g
            else:
                samp = (1.0, float(cos[(A + B) // 2]))
                d = ndimage.distance_transform_edt(~blk, sampling=samp) * (self.res * down * 111.32)
            c = (g * (1.0 + COAST_FAR * np.exp(-d / COAST_FAR_KM)
                      + COAST_NEAR * np.exp(-d / COAST_NEAR_KM))).astype(np.float32)
            c[blk] = COST_LAND
            out[a:b] = c[a - A:b - A]
        return out

    def _costs(self, rebuild, meta):
        """The cost surface and its 4x downsample, memory-mapped so every worker
        shares one copy and a rerun never recomputes them."""
        cmeta = dict(meta, cost=[COST_LAND, COAST_FAR, COAST_FAR_KM, COAST_NEAR, COAST_NEAR_KM, DOWN, "ground-km"])
        cpath = MASKS / f"{self.name}.cost.npy"
        c4path = MASKS / f"{self.name}.cost4.npy"
        jpath = MASKS / f"{self.name}.costmeta.json"
        if not rebuild and cpath.exists() and c4path.exists() and jpath.exists() \
                and json.loads(jpath.read_text()) == cmeta:
            self.cost = np.load(cpath, mmap_mode="r")
            self.cost4 = np.load(c4path, mmap_mode="r")
            return
        t0 = time.time()
        for p in (cpath, c4path, jpath):
            p.unlink(missing_ok=True)
        cost = np.lib.format.open_memmap(cpath, mode="w+", dtype=np.float32,
                                         shape=(self.nrows, self.ncols))
        gkm, cos = self._row_km(self.nrows)
        self._cost_from_land(self.land, cost, gkm, cos)
        cost.flush()
        # the first level: a cell is land only when all DOWN x DOWN of its cells
        # are, so a two-kilometre strait is still open on it
        nr, nc = -(-self.nrows // DOWN), -(-self.ncols // DOWN)
        pad = np.ones((nr * DOWN, nc * DOWN), bool)
        pad[:self.nrows, :self.ncols] = self.land
        land4 = pad.reshape(nr, DOWN, nc, DOWN).all(axis=(1, 3))
        cost4 = np.lib.format.open_memmap(c4path, mode="w+", dtype=np.float32, shape=(nr, nc))
        gkm4, cos4 = self._row_km(nr, DOWN)
        self._cost_from_land(land4, cost4, gkm4, cos4, DOWN)
        cost4.flush()
        del cost, cost4
        jpath.write_text(json.dumps(cmeta))
        self.cost = np.load(cpath, mmap_mode="r")
        self.cost4 = np.load(c4path, mmap_mode="r")
        print(f"{self.name}: cost surface built in {time.time() - t0:.0f} s "
              f"({cpath.stat().st_size / 1e6:.0f} MB, memory-mapped)", file=sys.stderr)

    # -- coordinates
    def fwd(self, lat, lon):
        if self.proj == "merc":
            return merc_fwd(lat, lon)
        return self.lon0 + (lon - self.lon0) % 360.0, lat

    def inv(self, x, y):
        if self.proj == "merc":
            return merc_inv(x, y)
        return y, (x + 180.0) % 360.0 - 180.0

    def rc(self, lat, lon):
        x, y = self.fwd(lat, lon)
        return int(math.floor((self.y1 - y) / self.res)), int(math.floor((x - self.x0) / self.res))

    def rcf(self, lat, lon):
        x, y = self.fwd(lat, lon)
        return (self.y1 - y) / self.res - 0.5, (x - self.x0) / self.res - 0.5

    def ll(self, r, c):
        return self.inv(self.x0 + (c + 0.5) * self.res, self.y1 - (r + 0.5) * self.res)

    def inside(self, r, c):
        return 0 <= r < self.nrows and 0 <= c < self.ncols

    def holds(self, p):
        return self.inside(*self.rc(*p))

    # -- water
    def snap(self, r, c):
        """The nearest water cell within SNAP_KM, for a waypoint on land."""
        if not self.inside(r, c):
            return r, c
        r, c = min(max(r, 0), self.nrows - 1), min(max(c, 0), self.ncols - 1)
        if not self.land[r, c]:
            return r, c
        rad = self.cells(SNAP_KM, r)
        ra, rb = max(0, r - rad), min(self.nrows, r + rad + 1)
        ca, cb = max(0, c - rad), min(self.ncols, c + rad + 1)
        water = np.argwhere(~self.land[ra:rb, ca:cb])
        if not len(water):
            return r, c
        d = (water[:, 0] + ra - r) ** 2 + (water[:, 1] + ca - c) ** 2
        i = int(np.argmin(d))
        if math.sqrt(d[i]) * self.km_at(r) > SNAP_KM:
            return r, c
        return int(water[i, 0] + ra), int(water[i, 1] + ca)

    def clear(self, a, b):
        """True when the straight line between two (lat, lon) points touches no
        land cell.  Sampled every cell in the grid plane, which is where the
        route was found."""
        r0, c0 = self.rcf(*a)
        r1, c1 = self.rcf(*b)
        n = int(max(abs(r1 - r0), abs(c1 - c0))) + 1
        if n > 200000:
            n = 200000
        f = np.linspace(0.0, 1.0, n + 1)
        rr = np.rint(r0 + f * (r1 - r0)).astype(np.int64)
        cc = np.rint(c0 + f * (c1 - c0)).astype(np.int64)
        np.clip(rr, 0, self.nrows - 1, out=rr)
        np.clip(cc, 0, self.ncols - 1, out=cc)
        return not bool(self.land[rr, cc].any())

    # -- the route
    def _mcp(self, cost, start, end):
        idx, _ = route_through_array(cost, start, end, fully_connected=True, geometric=True)
        return idx

    def _window(self, r0, c0, r1, c1):
        """The segment's bounding box plus a margin proportional to its length,
        so a route can go round an island but never wanders the whole mask."""
        mid = (r0 + r1) // 2
        seg = self.km_at(mid) * math.hypot(r1 - r0, c1 - c0)
        m = min(WINDOW_MAX_CELLS, self.cells(max(WINDOW_MIN_KM, 0.6 * seg), mid))
        ra = max(0, (min(r0, r1) - m) // DOWN * DOWN)
        ca = max(0, (min(c0, c1) - m) // DOWN * DOWN)
        rb = min(self.nrows, -(-(max(r0, r1) + m + 1) // DOWN) * DOWN)
        cb = min(self.ncols, -(-(max(c0, c1) + m + 1) // DOWN) * DOWN)
        return ra, rb, ca, cb

    def route(self, p, q):
        """The water path from p to q, (lat, lon), p and q included exactly."""
        if self.clear(p, q):
            return [p, q], 0.0
        r0, c0 = self.snap(*self.rc(*p))
        r1, c1 = self.snap(*self.rc(*q))
        if (r0, c0) == (r1, c1):
            return [p, q], 0.0
        ra, rb, ca, cb = self._window(r0, c0, r1, c1)
        idx, crossed = None, math.inf

        def keep(cand):
            """Take the candidate that runs least over land."""
            nonlocal idx, crossed
            if cand is None:
                return crossed
            cr = self._crosses(cand, ra, ca)
            if cr < crossed:
                idx, crossed = cand, cr
            return cr

        if max(rb - ra, cb - ca) > 6 * DOWN:
            for widen in (1.0, 3.0):
                try:
                    cand = self._corridor(ra, rb, ca, cb, r0, c0, r1, c1, widen)
                except Exception:
                    cand = None
                if keep(cand) <= CROSS_TOL_KM:
                    break
        if crossed > CROSS_TOL_KM and (rb - ra) * (cb - ca) <= REFINE_BUDGET:
            try:
                keep(self._mcp(np.asarray(self.cost[ra:rb, ca:cb]),
                               (r0 - ra, c0 - ca), (r1 - ra, c1 - ca)))
            except Exception:
                pass
        if idx is None:
            return [p, q], gc_km(p, q)
        pts = [p] + [self.ll(r + ra, c + ca) for r, c in idx] + [q]
        return self.polish(pts), crossed

    def _crosses(self, idx, ra, ca):
        """How far a grid path runs over land away from its ends, in ground km.
        A land run at either end is the stub to a waypoint that sits in a land
        cell -- a harbour up a fjord the mask does not resolve -- and is not a
        crossing."""
        a = np.array(idx)
        rows = a[:, 0] + ra
        on = self.land[rows, a[:, 1] + ca]
        i, j = 0, len(on)
        while i < j and on[i]:
            i += 1
        while j > i and on[j - 1]:
            j -= 1
        if not on[i:j].any():
            return 0.0
        return float(self.gkm[np.clip(rows[i:j][on[i:j]], 0, self.nrows - 1)].sum())

    def _corridor(self, ra, rb, ca, cb, r0, c0, r1, c1, widen=1.0):
        """The two-level search.  First a least-cost path over the 4x surface,
        which is small; then the same path again at full resolution, but only
        where the full resolution can change it -- inside a corridor around the
        coarse path, and only along the stretches of it that run within about
        70 km of a coast.  Mid-ocean the coarse path is already a straight line
        and the straightening that follows would collapse it anyway, and MCP
        costs one pass over whatever array it is handed, so a Dartmouth to
        Greenland crossing is not worth twenty million cells."""
        w4 = np.asarray(self.cost4[ra // DOWN:rb // DOWN, ca // DOWN:cb // DOWN])
        h4, w4n = w4.shape
        s0 = ((r0 - ra) // DOWN, (c0 - ca) // DOWN)
        s1 = ((r1 - ra) // DOWN, (c1 - ca) // DOWN)
        # a long segment at a high latitude makes even the 4x window large: pool
        # it further, by the cheapest cell of each block so a channel is never
        # closed by the pooling
        lvl, f = w4, 1
        while lvl.size > LEVEL1_MAX_CELLS:
            h, w = lvl.shape[0] // 2 * 2, lvl.shape[1] // 2 * 2
            lvl = lvl[:h, :w].reshape(h // 2, 2, w // 2, 2).min(axis=(1, 3))
            f *= 2

        def at(s):
            return (min(s[0] // f, lvl.shape[0] - 1), min(s[1] // f, lvl.shape[1] - 1))
        a4 = np.array(self._mcp(lvl, at(s0), at(s1))) * f + f // 2
        a4[:, 0] = np.clip(a4[:, 0], 0, h4 - 1)
        a4[:, 1] = np.clip(a4[:, 1], 0, w4n - 1)
        k = max(2, f, int(widen * self.cells(CORRIDOR_KM, (r0 + r1) // 2)) // DOWN)

        # the same path in fine cells, with the true ends put back
        P = np.stack([a4[:, 0] * DOWN + DOWN // 2, a4[:, 1] * DOWN + DOWN // 2], 1)
        P[:, 0] = np.clip(P[:, 0], 0, rb - ra - 1)
        P[:, 1] = np.clip(P[:, 1], 0, cb - ca - 1)
        P[0], P[-1] = (r0 - ra, c0 - ca), (r1 - ra, c1 - ca)
        # where is refining worth it?  the coast penalty says so, at both levels
        pen4 = w4[a4[:, 0], a4[:, 1]] / np.maximum(self.gkm4[ra // DOWN + a4[:, 0]], 1e-6) - 1.0
        penf = (np.asarray(self.cost[P[:, 0] + ra, P[:, 1] + ca])
                / np.maximum(self.gkm[np.clip(P[:, 0] + ra, 0, self.nrows - 1)], 1e-6) - 1.0)
        near = (pen4 > NEAR_PENALTY) | (penf > NEAR_PENALTY)
        near = ndimage.binary_dilation(near, np.ones(2 * max(2, k) + 1, bool))

        out, u = [], 0
        while u < len(P) - 1:
            v = u + 1
            while v < len(P) - 1:
                h = int(P[u:v + 2, 0].max() - P[u:v + 2, 0].min()) + 2 * k * DOWN + 8
                w = int(P[u:v + 2, 1].max() - P[u:v + 2, 1].min()) + 2 * k * DOWN + 8
                if h * w > REFINE_BUDGET:
                    break
                v += 1
            if near[u:v + 1].any():
                out += self._refine(P, a4, u, v, k, ra, ca, rb, cb, h4, w4n)
            else:
                out += [(int(x), int(y)) for x, y in P[u:v]]
            u = v
        out.append((int(P[-1, 0]), int(P[-1, 1])))
        return out

    def _refine(self, P, a4, u, v, k, ra, ca, rb, cb, h4, w4n):
        """One stretch of the coarse path, routed again at full resolution
        inside a corridor around it.  The corridor is dilated on the 4x grid,
        sixteen times smaller, and then blown up.  Returns cells in window
        coordinates, P[u] included and P[v] not, so the stretches join."""
        ends4 = np.array([[int(P[u, 0]) // DOWN, int(P[u, 1]) // DOWN],
                          [int(P[v, 0]) // DOWN, int(P[v, 1]) // DOWN]])
        run = np.vstack([a4[u:v + 1], ends4])
        ka = max(0, int(run[:, 0].min()) - k)
        kb = min(h4, int(run[:, 0].max()) + k + 1)
        kc = max(0, int(run[:, 1].min()) - k)
        kd = min(w4n, int(run[:, 1].max()) + k + 1)
        seed = np.zeros((kb - ka, kd - kc), bool)
        seed[np.clip(run[:, 0], ka, kb - 1) - ka, np.clip(run[:, 1], kc, kd - 1) - kc] = True
        cor4 = ndimage.maximum_filter(seed, size=2 * k + 1, mode="constant")
        sa, sb = ka * DOWN, min(rb - ra, kb * DOWN)
        sc, sd = kc * DOWN, min(cb - ca, kd * DOWN)
        cor = np.repeat(np.repeat(cor4, DOWN, 0), DOWN, 1)[:sb - sa, :sd - sc]
        cost = np.asarray(self.cost[sa + ra:sb + ra, sc + ca:sd + ca]).copy()
        cost[~cor] = np.inf
        a = (min(max(int(P[u, 0]) - sa, 0), sb - sa - 1), min(max(int(P[u, 1]) - sc, 0), sd - sc - 1))
        b = (min(max(int(P[v, 0]) - sa, 0), sb - sa - 1), min(max(int(P[v, 1]) - sc, 0), sd - sc - 1))
        cost[a] = min(cost[a], COST_LAND)
        cost[b] = min(cost[b], COST_LAND)
        idx = self._mcp(cost, a, b)
        return [(r + sa, c + sc) for r, c in idx[:-1]]

    # -- from a staircase to a line
    def polish(self, pts):
        pts = simplify(pts, 0.5 * SIMPLIFY_KM)
        pts = self.straighten(pts)
        pts = simplify(pts, SIMPLIFY_KM)
        for _ in range(CHAIKIN_PASSES):
            pts = self.chaikin(pts)
        return self.thin(pts)

    def straighten(self, pts):
        """From each kept point, the farthest later point whose straight line
        touches no land: found by doubling the step while it is clear and then
        bisecting, so a hundred-point staircase costs a few dozen tests, not
        thousands."""
        out, i, n = [pts[0]], 0, len(pts)
        while i < n - 1:
            step = 1
            while i + 2 * step < n and self.clear(pts[i], pts[i + 2 * step]):
                step *= 2
            lo, hi = step, min(2 * step, n - 1 - i)      # lo is clear, hi may not be
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if self.clear(pts[i], pts[i + mid]):
                    lo = mid
                else:
                    hi = mid - 1
            i += max(1, lo)
            out.append(pts[i])
        return out

    def chaikin(self, pts):
        """One corner-cutting pass, guarded: a corner is rounded only when the
        cut itself touches no land.  Every other new edge lies inside an edge
        that was already clear, so the smoothed line never crosses a shore."""
        if len(pts) < 3:
            return list(pts)
        out = [pts[0]]
        for i in range(1, len(pts) - 1):
            a, b, c = pts[i - 1], pts[i], pts[i + 1]
            lo_a, lo_c = unwrap(b[1], a[1]), unwrap(b[1], c[1])
            u = (b[0] + 0.25 * (a[0] - b[0]), b[1] + 0.25 * (lo_a - b[1]))
            v = (b[0] + 0.25 * (c[0] - b[0]), b[1] + 0.25 * (lo_c - b[1]))
            if self.clear(u, v):
                out += [u, v]
            else:
                out.append(b)
        out.append(pts[-1])
        return [(la, (lo + 180.0) % 360.0 - 180.0) for la, lo in out]

    def thin(self, pts, tol_km=0.25):
        """Drop a point whose removal moves the line by less than tol_km and
        whose shortcut touches no land."""
        if len(pts) < 3:
            return list(pts)
        out = [pts[0]]
        i = 1
        while i < len(pts) - 1:
            a, b, c = out[-1], pts[i], pts[i + 1]
            ky, kx = 111.0, 111.0 * max(0.05, math.cos(math.radians(b[0])))
            ax, ay = (unwrap(b[1], a[1]) - b[1]) * kx, (a[0] - b[0]) * ky
            cx, cy = (unwrap(b[1], c[1]) - b[1]) * kx, (c[0] - b[0]) * ky
            dx, dy = cx - ax, cy - ay
            L2 = dx * dx + dy * dy
            t = 0.0 if L2 == 0 else max(0.0, min(1.0, -(ax * dx + ay * dy) / L2))
            if math.hypot(ax + t * dx, ay + t * dy) < tol_km and self.clear(a, c):
                i += 1
                continue
            out.append(b)
            i += 1
        out.append(pts[-1])
        return out


def merc_fwd(lat, lon):
    lat = max(-89.5, min(89.5, lat))
    return lon / 180.0 * M_MERC, R_MERC * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def merc_inv(x, y):
    return math.degrees(2 * math.atan(math.exp(y / R_MERC)) - math.pi / 2), x / M_MERC * 180.0


# ------------------------------------------------------------- measurements
def land_fraction(grids, pts, step_km=2.0):
    """The share of a polyline that lies on land, sampled every step_km on the
    ground on the finest mask that holds the sample.  Samples outside every mask
    are counted apart."""
    if len(pts) < 2:
        return 0.0, 0
    hits = seen = missed = 0
    for p in densify(pts, step_km):
        for g in grids:
            r, c = g.rc(*p)
            if g.inside(r, c):
                seen += 1
                hits += int(g.land[r, c])
                break
        else:
            missed += 1
    return hits / max(1, seen), missed


def line_km(pts):
    return sum(gc_km(a, b) for a, b in zip(pts, pts[1:]))


def nearest_place(places, p, within_km=250.0):
    """The name of the nearest place in the database, so a difference between
    two lines can be said in words rather than in degrees."""
    best, bd = None, within_km
    for name, lat, lon in places:
        d = gc_km(p, (lat, lon))
        if d < bd:
            best, bd = name, d
    return best


def _one_way(a_pts, b_pts, step_km):
    """Distance from every point every step_km along a_pts to the nearest point
    of the polyline b_pts, on a local flat approximation."""
    samples = densify(a_pts, step_km)
    lat0 = sum(p[0] for p in samples) / len(samples)
    ky, kx = 111.0, 111.0 * max(0.05, math.cos(math.radians(lat0)))
    lon0 = samples[0][1]
    P = np.array([[unwrap(lon0, p[1]) * kx, p[0] * ky] for p in samples])
    Q = np.array([[unwrap(lon0, p[1]) * kx, p[0] * ky] for p in b_pts])
    A, B = Q[:-1], Q[1:]
    D = B - A
    L2 = np.maximum((D * D).sum(1), 1e-12)
    best = np.empty(len(P))
    for i in range(0, len(P), 512):
        p = P[i:i + 512][:, None, :]
        t = np.clip(((p - A[None]) * D[None]).sum(2) / L2[None], 0.0, 1.0)
        proj = A[None] + t[..., None] * D[None]
        best[i:i + 512] = np.hypot(*(p - proj).transpose(2, 0, 1)).min(1)
    return best, samples


def line_distance_km(mine, theirs, step_km=5.0):
    """How far apart two lines run: the mean over points along this run's line,
    the largest separation either way (a symmetric Hausdorff distance, so a line
    that misses a whole leg cannot hide), and where that largest gap is."""
    if len(mine) < 2 or len(theirs) < 2:
        return 0.0, 0.0, None
    da, sa = _one_way(mine, theirs, step_km)
    db, sb = _one_way(theirs, mine, step_km)
    ia, ib = int(np.argmax(da)), int(np.argmax(db))
    where = sa[ia] if da[ia] >= db[ib] else sb[ib]
    return float(da.mean()), float(max(da[ia], db[ib])), where


def line_shore(grids, pts, step_km=3.0):
    """(on land, hugging the shore, median distance offshore) for a polyline.
    The distance to the coast comes straight out of the cached cost surface: the
    coast penalty is a known function of it, so inverting the penalty is a table
    lookup and needs no second distance transform."""
    if len(pts) < 2:
        return 0.0, 0.0, 0.0
    dd = np.linspace(0.0, 400.0, 4001)
    pen = COAST_FAR * np.exp(-dd / COAST_FAR_KM) + COAST_NEAR * np.exp(-dd / COAST_NEAR_KM)
    on, off = 0, []
    n = 0
    for p in densify(pts, step_km):
        for g in grids:
            r, c = g.rc(*p)
            if not g.inside(r, c):
                continue
            n += 1
            if g.land[r, c]:
                on += 1
            else:
                v = float(g.cost[r, c]) / max(1e-6, g.km_at(r)) - 1.0
                off.append(float(np.interp(-v, -pen, dd)))
            break
    if not n:
        return 0.0, 0.0, 0.0
    hug = sum(1 for d in off if d < HUG_KM) / max(1, len(off))
    return on / n, hug, float(np.median(off)) if off else 0.0


# ---------------------------------------------------------------- the flag
def tag_tokens(tags):
    try:
        v = json.loads(tags or "[]")
    except json.JSONDecodeError:
        v = [tags or ""]
    if isinstance(v, str):
        v = [v]
    out = set()
    for item in v:
        for tok in str(item).replace(";", ",").split(","):
            tok = tok.strip().lower()
            if tok:
                out.add(tok)
    return out


def decide(row):
    """(flag, why) for a track whose routing flag is unset."""
    tid = row["id"]
    if tid in OVERRIDES:
        flag, why = OVERRIDES[tid]
        return flag, f"by hand: {why}"
    title = (row["title"] or "").lower()
    for m in MONTHS:
        title = title.replace(m, " ")       # "March-April 1853" is a date, not a march
    hits = sorted(set(TITLE_RE.findall(title)))
    tags = sorted(tag_tokens(row["tags"]) & TAG_WORDS)
    if hits or tags:
        why = []
        if hits:
            why.append("the title says " + ", ".join(hits))
        if tags:
            why.append("tagged " + ", ".join(tags))
        return "as-given", "; ".join(why)
    return "water", "no word for a journey over land or ice in the title or tags"


# --------------------------------------------------------------- the worker
GRIDS = None


def route_track(job):
    """One track, in a worker.  The masks and cost surfaces are inherited by
    fork: the mask is one shared read-only page set and the cost surfaces are
    memory-mapped, so nothing is copied."""
    fine, coarse = GRIDS
    grids = (fine, coarse)
    tid, title, flag, pts = job["id"], job["title"], job["flag"], job["pts"]
    t0 = time.time()
    rec = dict(id=tid, title=title, routing=flag, waypoints=len(pts), north_of=0.0,
               great_circle=0, coarse=0, crossed=0, crossed_km=0.0, outside=0)
    if len(pts) < 2:
        rec.update(straight_land=0.0, routed_land=0.0, points=len(pts), wp_on_land=0.0,
                   straight_km=0.0, routed_km=0.0, seconds=0.0, line=list(pts))
        return rec
    on = have = 0
    for p in pts:
        for g in grids:
            r, c = g.rc(*p)
            if g.inside(r, c):
                have += 1
                on += int(g.land[r, c])
                break
    rec["wp_on_land"] = on / max(1, have)
    s_frac, s_missed = land_fraction(grids, pts)
    rec["straight_land"] = s_frac
    rec["straight_km"] = line_km(pts)
    rec["outside"] = int(bool(s_missed))
    if flag != "water":
        # a track drawn as-given still gets a line, and that line is the
        # waypoints joined by great-circle arcs, densified: a sledge journey or
        # a flight over the Pole followed the geodesic, not a Mercator straight
        # line, and on the map the two are far apart at these latitudes
        step = job.get("gc_step", GC_STEP_KM)
        line = [pts[0]]
        for p, q in zip(pts, pts[1:]):
            line += great_circle(p, q, step)[1:] if step > 0 else [q]
        r_frac, r_missed = land_fraction(grids, line)
        rec["outside"] = int(bool(s_missed or r_missed))
        rec.update(points=len(line), routed_land=r_frac, routed_km=line_km(line),
                   seconds=round(time.time() - t0, 2), line=line)
        return rec
    line = [pts[0]]
    for p, q in zip(pts, pts[1:]):
        g = next((g for g in grids if g.holds(p) and g.holds(q)), None)
        if g is None:
            seg = great_circle(p, q)
            rec["great_circle"] += 1
        else:
            seg, crossed = g.route(p, q)
            # the Polar Sea's last leg runs from Prudhoe Bay to Seattle: both
            # ends are on the fine mask but the water between them goes through
            # Bering Strait, which is not, so the fine mask has to cross Alaska.
            # When a route crosses real land, ask the mask that holds more sea.
            if (crossed > BIG_CROSS_KM and g is fine
                    and coarse.holds(p) and coarse.holds(q)):
                seg2, crossed2 = coarse.route(p, q)
                if crossed2 < crossed:
                    seg, crossed, g = seg2, crossed2, coarse
            rec["coarse"] += int(g is coarse)
            rec["crossed"] += int(crossed > CROSS_TOL_KM)
            rec["crossed_km"] += crossed
        line += seg[1:]
    r_frac, r_missed = land_fraction(grids, line)
    rec["outside"] = int(bool(s_missed or r_missed))
    # the mask knows nothing about ice: an ocean crossing can be routed over the
    # pole or through the Northeast Passage because that is the shortest water.
    # Say how much further north the line goes than any waypoint asked for.
    rec["north_of"] = max(p[0] for p in line) - max(p[0] for p in pts)
    rec.update(points=len(line), routed_land=r_frac, routed_km=line_km(line),
               seconds=round(time.time() - t0, 2), line=line)
    return rec


def _init(grids):
    global GRIDS
    GRIDS = grids


# ----------------------------------------------------------------- straits
def check_straits(fine):
    """Both ends of a strait must be in one connected patch of water inside a
    window around it: that is what 'the strait is open' means to the router.
    The narrowest crossing is measured too, on the 4x surface as well, since
    that is the surface the first level of the search sees."""
    out = []
    for name, (east, west, box) in STRAITS.items():
        s, w, n, e = box
        r0, c0 = fine.rc(n, w)
        r1, c1 = fine.rc(s, e)
        ra, rb = max(0, r0), min(fine.nrows, r1 + 1)
        ca, cb = max(0, c0), min(fine.ncols, c1 + 1)
        water = ~fine.land[ra:rb, ca:cb]
        row = {"strait": name, "ends": []}
        cells = []
        for p in (east, west):
            r, c = fine.snap(*fine.rc(*p))
            cells.append((r - ra, c - ca))
            row["ends"].append(f"{p[0]:.2f} {p[1]:.2f} -> {'water' if not fine.land[r, c] else 'LAND'}")
        for conn, st in (("open at 1 km", ndimage.generate_binary_structure(2, 1)),
                         ("open diagonally", ndimage.generate_binary_structure(2, 2))):
            lab, _ = ndimage.label(water, structure=st)
            a, b = lab[cells[0]], lab[cells[1]]
            row[conn] = bool(a and a == b)
        # and on the first level's surface, where a cell is land only if all 16 are
        w4 = np.asarray(fine.cost4[ra // DOWN:-(-rb // DOWN), ca // DOWN:-(-cb // DOWN)]) < COST_LAND
        lab, _ = ndimage.label(w4, structure=ndimage.generate_binary_structure(2, 2))
        a = lab[min(cells[0][0] // DOWN, w4.shape[0] - 1), min(cells[0][1] // DOWN, w4.shape[1] - 1)]
        b = lab[min(cells[1][0] // DOWN, w4.shape[0] - 1), min(cells[1][1] // DOWN, w4.shape[1] - 1)]
        row["open on the 4 km first level"] = bool(a and a == b)
        # the width at the tightest place a route through the strait must pass,
        # in ground km (a Web Mercator cell is about 300 m on the ground here)
        dist = ndimage.distance_transform_edt(water)
        lab, _ = ndimage.label(water, structure=ndimage.generate_binary_structure(2, 2))
        comp = lab == lab[cells[0]]
        row["width km"] = round(float(2 * _throat(dist, comp, cells[0], cells[1])
                                      * fine.km_at(ra + cells[0][0])), 1)
        row["cell km"] = round(fine.km_at(ra + cells[0][0]), 2)
        out.append(row)
    return out


def _throat(dist, comp, a, b):
    """The smallest distance-to-shore along the widest water path between two
    cells: the half-width of the tightest place a route must pass."""
    d = np.where(comp, dist, 0.0)
    lo, hi = 0.0, float(d.max())
    for _ in range(24):
        mid = (lo + hi) / 2
        lab, _ = ndimage.label(d >= mid, structure=ndimage.generate_binary_structure(2, 2))
        if lab[a] and lab[a] == lab[b]:
            lo = mid
        else:
            hi = mid
    return lo


# ------------------------------------------------------------- the database
TRACK_COLS = ("creator", "description", "source_url", "download_url", "local_file",
              "licence", "credit", "bibkey", "pages", "language", "view_file",
              "people", "tags", "waypoints")


def waypoints_of(row):
    try:
        w = json.loads(row["waypoints"] or "[]")
    except json.JSONDecodeError:
        return []
    return [(float(p["lat"]), float(p["lon"])) for p in w
            if isinstance(p, dict) and p.get("lat") is not None and p.get("lon") is not None]


def geometry_of(row):
    try:
        g = json.loads(row["geometry"] or "null")
    except json.JSONDecodeError:
        return []
    if not isinstance(g, dict) or g.get("type") != "LineString":
        return []
    return [(float(y), float(x)) for x, y in g.get("coordinates", [])]


def write_row(c, row, routing, geometry):
    """Put the flag and the routed line back, with every other field of the row
    as it stands, so nothing is blanked.  waypoints pass through unchanged: they
    are the truth, not the drawing.  Only ever called under --write."""
    import arctic_history as H
    kw = {k: row[k] for k in TRACK_COLS if row[k] is not None}
    kw.update(date=row["date_text"], date_end=row["date_end"], lat=row["lat"], lon=row["lon"],
              routing=routing)
    if geometry is not None:
        kw["geometry"] = json.dumps(geometry, ensure_ascii=False)
    elif row["geometry"]:
        kw["geometry"] = row["geometry"]
    H.add_artifact(c, row["id"], row["topic"], row["type"], row["title"], **kw)


def as_geojson(line):
    return {"type": "LineString",
            "coordinates": [[round(lo, 5), round(la, 5)] for la, lo in line]}


# ----------------------------------------------------------------- pictures
def _font(size):
    from PIL import ImageFont
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()


WATER_RGB, LAND_RGB, COAST_RGB = (18, 28, 42), (74, 76, 70), (128, 136, 130)
C_STRAIGHT, C_THEIRS, C_MINE, C_WP = (168, 66, 66), (86, 186, 246), (255, 205, 66), (255, 255, 255)
C_ASGIVEN = (150, 146, 128)


def _panel(fine, box, width, ss=2, aspect=None):
    """A land/water panel for a lat/lon box (s, w, n, e): the image, and a
    function from (lat, lon) to pixels.  With `aspect` (width over height) the
    window is grown, not cropped, to that shape, so a sheet of panels lines up."""
    from PIL import Image
    s, w, n, e = box
    r0, c0 = fine.rcf(n, w)
    r1, c1 = fine.rcf(s, e)
    ra, ca = max(0, int(r0)), max(0, int(c0))
    rb, cb = min(fine.nrows, int(r1) + 2), min(fine.ncols, int(c1) + 2)
    if aspect:
        h, wd = rb - ra, cb - ca
        if wd / h < aspect:
            want = min(fine.ncols, int(round(h * aspect)))
            ca = max(0, min(fine.ncols - want, ca - (want - wd) // 2))
            cb = ca + want
            want_h = max(1, int(round(want / aspect)))
            ra = max(0, min(fine.nrows - want_h, ra - (want_h - h) // 2))
            rb = ra + want_h
        else:
            want = min(fine.nrows, int(round(wd / aspect)))
            ra = max(0, min(fine.nrows - want, ra - (want - h) // 2))
            rb = ra + want
    W = width * ss
    sc = W / (cb - ca)
    H = max(1, int(round((rb - ra) * sc)))
    a = Image.fromarray((fine.land[ra:rb, ca:cb] * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    a = np.asarray(a, dtype=np.float32) / 255.0
    t = np.clip((a - 0.35) / 0.30, 0.0, 1.0)[..., None]
    img = (np.array(WATER_RGB, np.float32) * (1 - t) + np.array(LAND_RGB, np.float32) * t)
    edge = np.clip(1.0 - np.abs(a - 0.5) / 0.22, 0.0, 1.0)[..., None]
    img = img * (1 - edge) + np.array(COAST_RGB, np.float32) * edge
    img = Image.fromarray(img.astype(np.uint8), "RGB")

    def xy(p):
        r, c = fine.rcf(*p)
        return ((c - ca) * sc, (r - ra) * sc)
    return img, xy, sc, (ra, rb, ca, cb)


def _draw_line(d, xy, pts, colour, width, maxjump=None):
    if len(pts) < 2:
        return
    seq = [xy(p) for p in pts]
    run = [seq[0]]
    for a, b in zip(seq, seq[1:]):
        if maxjump and math.hypot(b[0] - a[0], b[1] - a[1]) > maxjump:
            if len(run) > 1:
                d.line(run, fill=colour, width=width, joint="curve")
            run = [b]
        else:
            run.append(b)
    if len(run) > 1:
        d.line(run, fill=colour, width=width, joint="curve")


def _scalebar(d, img, sc, fine, lat, ss):
    """A scale bar: Mercator metres per pixel shrunk by cos(lat) is the ground."""
    km_per_px = fine.res / sc * math.cos(math.radians(lat)) / 1000.0
    target = img.width * 0.18 * km_per_px
    step = 10 ** math.floor(math.log10(max(1.0, target)))
    for m in (1, 2, 5, 10):
        if m * step >= target:
            step *= m
            break
    px = step / km_per_px
    x0, y0 = 34 * ss, img.height - 40 * ss
    d.rectangle([x0 - 14 * ss, y0 - 42 * ss, x0 + px + 20 * ss, y0 + 14 * ss], fill=(10, 16, 26))
    d.line([(x0, y0), (x0 + px, y0)], fill=(235, 235, 235), width=4 * ss)
    for x in (x0, x0 + px):
        d.line([(x, y0 - 7 * ss), (x, y0 + 7 * ss)], fill=(235, 235, 235), width=4 * ss)
    d.text((x0, y0 - 34 * ss), f"{step:g} km", fill=(235, 235, 235), font=_font(20 * ss))


def _legend(d, img, items, ss, title=None):
    f = _font(22 * ss)
    x, y = 34 * ss, 30 * ss
    w = max(d.textlength(l, font=f) for _, l in items) + 100 * ss
    h = 34 * ss * len(items) + (44 * ss if title else 0) + 24 * ss
    d.rectangle([x - 16 * ss, y - 14 * ss, x + w, y + h], fill=(10, 16, 26))
    if title:
        d.text((x, y), title, fill=(244, 244, 244), font=_font(30 * ss))
        y += 46 * ss
    for colour, label in items:
        d.line([(x, y + 12 * ss), (x + 44 * ss, y + 12 * ss)], fill=colour, width=5 * ss)
        d.text((x + 58 * ss, y), label, fill=(226, 226, 230), font=f)
        y += 34 * ss


def figure(fine, box, width, path, tracks, title, ss=2, waypoints=True, legend=True, theirs_label="the other run"):
    """One panel with, per track, the straight line faint, the other run's line,
    and this one's.  A track drawn as-given is not a routed line and is shown
    apart, in grey, so it cannot be read as one."""
    from PIL import Image, ImageDraw
    img, xy, sc, _ = _panel(fine, box, width, ss)
    d = ImageDraw.Draw(img)
    jump = img.width * 0.5
    routed = [t for t in tracks if t["routing"] == "water"]
    given = [t for t in tracks if t["routing"] != "water"]
    wide = 2 * ss if len(routed) > 20 else 3 * ss
    for t in routed:
        _draw_line(d, xy, t["straight"], C_STRAIGHT, max(1, ss), jump)
    for t in given:
        _draw_line(d, xy, t["line"], C_ASGIVEN, max(1, ss), jump)
    for t in tracks:
        if t.get("theirs"):
            _draw_line(d, xy, t["theirs"], C_THEIRS, wide, jump)
    for t in routed:
        _draw_line(d, xy, t["line"], C_MINE, wide, jump)
    if waypoints:
        for t in tracks:
            for p in t["straight"]:
                x, y = xy(p)
                r = 2.5 * ss
                d.ellipse([x - r, y - r, x + r, y + r], fill=C_WP)
    if legend:
        n_theirs = sum(1 for t in tracks if t.get("theirs"))
        items = [(C_MINE, f"routed here ({len(routed)} tracks)"),
                 (C_THEIRS, f"{theirs_label} ({n_theirs} of them here)"),
                 (C_ASGIVEN, f"drawn as-given, not routed ({len(given)})"),
                 (C_STRAIGHT, "the waypoints joined straight")]
        if waypoints:
            items.append((C_WP, "waypoints"))
        _legend(d, img, items, ss, title)
        _scalebar(d, img, sc, fine, (box[0] + box[2]) / 2, ss)
    img = img.resize((img.width // ss, img.height // ss), Image.LANCZOS)
    img.save(path)
    return img.size


def contact_sheet(fine, path, tracks, cols=2, panel_w=1200, ss=2, aspect=4 / 3):
    """The longest voyages, one panel each, every panel the same shape."""
    from PIL import Image, ImageDraw
    tiles = []
    for t in tracks:
        pts = t["line"] + t["straight"]
        lat = [p[0] for p in pts]
        lon = [unwrap(pts[0][1], p[1]) for p in pts]
        pad_lat = max(0.4, (max(lat) - min(lat)) * 0.10)
        pad_lon = max(1.0, (max(lon) - min(lon)) * 0.10)
        box = (max(35.5, min(lat) - pad_lat), min(lon) - pad_lon,
               min(85.5, max(lat) + pad_lat), max(lon) + pad_lon)
        box = (box[0], max(-149.5, box[1]), box[2], min(14.5, box[3]))
        img, xy, sc, _ = _panel(fine, box, panel_w, ss, aspect)
        d = ImageDraw.Draw(img)
        jump = img.width * 0.5
        _draw_line(d, xy, t["straight"], C_STRAIGHT, 2 * ss, jump)
        if t.get("theirs"):
            _draw_line(d, xy, t["theirs"], C_THEIRS, 3 * ss, jump)
        _draw_line(d, xy, t["line"], C_MINE, 3 * ss, jump)
        d.rectangle([0, 0, img.width, 64 * ss], fill=(10, 16, 26))
        d.text((18 * ss, 8 * ss), t["id"], fill=(250, 250, 250), font=_font(26 * ss))
        d.text((18 * ss, 38 * ss), t["title"][:70], fill=(198, 204, 210), font=_font(20 * ss))
        _scalebar(d, img, sc, fine, (box[0] + box[2]) / 2, ss)
        tiles.append(img.resize((img.width // ss, img.height // ss), Image.LANCZOS))
    h = max(t.height for t in tiles)
    rows = -(-len(tiles) // cols)
    bar = 34
    sheet = Image.new("RGB", (cols * panel_w, rows * h + bar), (10, 16, 26))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * panel_w, bar + (i // cols) * h))
    ImageDraw.Draw(sheet).text(
        (18, 8), "the ten longest routed voyages — yellow this run, blue the other run, "
                 "faint red the waypoints joined straight", fill=(190, 196, 204), font=_font(17))
    sheet.save(path)
    return sheet.size


# ----------------------------------------------------------------- summary
def verdict(rec, cmp):
    """One line on where the two lines differ and which reads better as a ship's
    route: how far apart they run and where, whether either crosses land, and
    whether either hugs a shore that the other stands off."""
    mx, where = cmp["max_km"], cmp["at"]
    at = f" off {cmp['at_place']}" if cmp.get("at_place") else (
        f" near {where[0]:.1f} N {abs(where[1]):.1f} {'W' if where[1] < 0 else 'E'}" if where else "")
    if rec["routing"] != "water":
        return (f"**the flag, not the line**: this run draws it as-given ({rec['why']}) and their run "
                f"routed it through water, so the two lines are up to {mx:.0f} km apart{at} — "
                f"decide the flag first")
    bits = []
    if mx < 5:
        bits.append("the same line to within a few kilometres")
    elif mx < 25:
        bits.append(f"the same channels throughout, up to {mx:.0f} km apart{at}")
    elif mx < 150:
        bits.append(f"the same broad route, but a different lead{at}, up to {mx:.0f} km apart")
    else:
        bits.append(f"a different way round{at}: up to {mx:.0f} km apart, {cmp['mean_km']:.0f} km on average")
    dl = rec["routed_land"] - cmp["their_land"]
    if dl < -0.02:
        bits.append(f"theirs runs {cmp['their_land']:.0%} of its length over land against mine "
                    f"{rec['routed_land']:.0%}")
    elif dl > 0.02:
        bits.append(f"mine runs {rec['routed_land']:.0%} over land against theirs {cmp['their_land']:.0%}")
    dh = cmp["their_hug"] - cmp["mine_hug"]
    if abs(dh) > 0.10:
        who = "theirs" if dh > 0 else "mine"
        other = "mine" if dh > 0 else "theirs"
        bits.append(f"{who} hugs the shore for {max(cmp['their_hug'], cmp['mine_hug']):.0%} of its "
                    f"length where {other} stands off (median offshore "
                    f"{cmp['mine_off']:.0f} km mine, {cmp['their_off']:.0f} km theirs)")
    if cmp["their_points"] and rec["points"] > 1.6 * cmp["their_points"]:
        bits.append(f"mine is the smoother line ({rec['points']} points against {cmp['their_points']})")
    elif cmp["their_points"] > 1.6 * max(1, rec["points"]):
        bits.append(f"theirs carries more points ({cmp['their_points']} against {rec['points']})")
    score = (dl < -0.02) + (dh > 0.10) - (dl > 0.02) - (dh < -0.10)
    if mx >= 25:
        if score:
            bits.append(("mine" if score > 0 else "theirs") + " reads better as a ship's route")
        else:
            d = (cmp["mine_km"] - cmp["their_km"]) / max(1.0, cmp["their_km"])
            longer = (f"; mine sails {abs(d):.0%} {'further' if d > 0 else 'less far'}"
                      if abs(d) > 0.03 else "")
            bits.append("both keep to the water, so the difference is which channel is right, "
                        "not which line is cleaner" + longer)
    return "; ".join(bits)


def render_summary(recs, comps, fine, coarse, straits, meta, path):
    routed = [r for r in recs if r["routing"] == "water"]
    L = ["# Routing the tracks through water", "",
         f"{meta['run']} — {len(recs)} tracks: {len(routed)} flagged **water** and routed, "
         f"{len(recs) - len(routed)} drawn **as-given**. "
         f"{meta['seconds']:.0f} s in all on {meta['jobs']} workers, "
         f"{np.mean([r['seconds'] for r in routed]):.1f} s per routed track on average, "
         f"{max(r['seconds'] for r in recs):.1f} s at worst.", "",
         f"Command: `{meta['cmd']}`", "",
         ("**Written to the database.** This run was given `--write`, so every track's `routing` flag "
          "and `geometry` below are now in `db/history/history.sqlite`, put there through "
          "`H.add_artifact` with the row's own fields, `waypoints` untouched. The same lines are in "
          "`routes.geojson` beside this file."
          if meta.get("wrote") else
          "**The database was not written to.** This run only reads waypoints from it; the lines are "
          "in `routes.geojson` beside this file. `--write` would put them in `geometry` and set "
          "`routing`, and it is off by default."), "",
         "## The masks", "",
         f"- **fine** — {fine.label}, {fine.ncols} x {fine.nrows} cells, land {fine.land.mean():.1%}. "
         f"A Web Mercator cell shrinks as the cosine of the latitude, so a cell is "
         f"{fine.km_at(fine.rc(45, -60)[0]):.2f} km on the ground at 45 N and "
         f"{fine.km_at(fine.rc(74, -95)[0]):.2f} km in Barrow Strait — finer, where it matters, than "
         f"the 500 m the issue asked for.",
         f"- **coarse** — {coarse.label}, {coarse.ncols} x {coarse.nrows} cells, "
         f"land {coarse.land.mean():.1%}, for the Pacific approaches.",
         f"- **the cost of a step**, cached beside each mask as a memory-mapped float32 array: in "
         f"water, the cell's ground length in km times "
         f"(1 + {COAST_FAR:g}·exp(−d/{COAST_FAR_KM:g} km) + {COAST_NEAR:g}·exp(−d/{COAST_NEAR_KM:g} km)) "
         f"with d the distance to the coast; on land, {COST_LAND:g}. Costing a step by its ground "
         f"length makes the cheapest path the shortest on the ground, not the shortest on the page; "
         f"the long penalty term centres a route in a channel and the short one holds it a few "
         f"kilometres off an open shore.", "",
         "### The two straits that decide the mask's resolution", ""]
    for s in straits:
        L.append(f"- **{s['strait']}** — {'; '.join(s['ends'])}. Open at 1 km: "
                 f"**{'yes' if s['open at 1 km'] else 'NO'}** (diagonally "
                 f"{'yes' if s['open diagonally'] else 'no'}); open on the 4 km first level of the "
                 f"search: {'yes' if s['open on the 4 km first level'] else 'no'}. Narrowest place a "
                 f"route must pass: about {s['width km']:.1f} km wide, on cells "
                 f"{s['cell km']:.2f} km across on the ground.")
    L += ["", "Both straits are open on the fine mask, which is the point of the full-resolution "
              "GSHHG shoreline: at 2 km cells from Natural Earth they close and every route through "
              "them goes the long way round.", ""]

    if routed:
        L += ["## What came out", "",
              "| | straight | routed |", "|---|---|---|",
              f"| of the line on land, mean over the {len(routed)} tracks routed through water | "
              f"{np.mean([r['straight_land'] for r in routed]):.0%} | "
              f"{np.mean([r['routed_land'] for r in routed]):.0%} |",
              f"| points per track, mean | {np.mean([r['waypoints'] for r in routed]):.0f} | "
              f"{np.mean([r['points'] for r in routed]):.0f} |",
              f"| length of the line, total km | {sum(r['straight_km'] for r in routed):,.0f} | "
              f"{sum(r['routed_km'] for r in routed):,.0f} |", ""]

    L += ["## Every track", "",
          "Land along the line is sampled every 2 km on the ground, on the finest mask that holds the "
          "sample. **on land, straight** is the waypoints joined by straight lines, which is what the "
          "map drew before. **on land, drawn** is the line this run gives it: the routed water path "
          f"for a water track, and the waypoints joined by great-circle arcs every {GC_STEP_KM:g} km "
          "for an as-given one, which is not routed round anything and so still runs over land wherever "
          "the journey did.", "",
          "| track | flag | waypoints | points | on land, straight | on land, drawn | notes | s |",
          "|---|---|---|---|---|---|---|---|"]
    for r in sorted(recs, key=lambda r: (-(r["routed_land"] if r["routing"] == "water" else -1),
                                         -r["straight_land"], r["id"])):
        note = []
        if r["great_circle"]:
            note.append(f"{r['great_circle']} segment(s) great circle, outside both masks")
        if r["coarse"]:
            note.append(f"{r['coarse']} on the coarse mask")
        if r["crossed"]:
            note.append(f"{r['crossed']} segment(s) with no water way through, "
                        f"{r['crossed_km']:.0f} km of land crossed")
        if r["routing"] == "water" and r["routed_land"] > 0.02:
            note.append(f"{r['routed_land']:.0%} still on land")
        if r["outside"]:
            note.append("part of the line is outside both masks")
        if r["routing"] != "water" or r["why"].startswith(("by hand", "the flag")):
            note.append(r["why"])       # a water track the rule decided needs no note
        if not note:
            note.append("—")
        L.append(f"| {r['id']} | {r['routing']} | {r['waypoints']} | {r['points']} | "
                 f"{r['straight_land']:.0%} | {r['routed_land']:.0%} | {'; '.join(note)} | "
                 f"{r['seconds']:.1f} |")

    left = [r for r in routed if r["routed_land"] > 0.02]
    L += ["", "## What is left on land", ""]
    if left:
        for r in sorted(left, key=lambda r: -r["routed_land"]):
            why = ("waypoints outside both masks, so those legs are great circles across the continent"
                   if r["great_circle"] else
                   f"no water way through on either mask, so {r['crossed_km']:.0f} km of land was "
                   "crossed" if r["crossed_km"] > BIG_CROSS_KM else
                   f"{r['wp_on_land']:.0%} of its waypoints sit in a land cell, and the stub to each "
                   "of them is drawn straight")
            L.append(f"- **{r['id']}** — {r['title']}  \n  {r['routed_land']:.0%} of the line "
                     f"({r['straight_land']:.0%} straight): {why}")
    else:
        L.append("- nothing over 2 %")

    L += ["", "## The flag, and what to look at", "",
          "The flag is the crew's. This run wrote none of them; these are the values a `--write` run "
          "would set, and each one's reason. A track already flagged in the database is obeyed as it "
          "stands.", "",
          f"Decided by hand ({len(OVERRIDES)} tracks the word rule cannot settle):", ""]
    for tid, (flag, why) in sorted(OVERRIDES.items()):
        L.append(f"- `{tid}` → **{flag}** — {why}")
    L += ["", "Decided by the rule but arguable:", ""]
    for tid, why in sorted(DEBATABLE.items()):
        rec = next((r for r in recs if r["id"] == tid), None)
        if rec:
            L.append(f"- `{tid}` → **{rec['routing']}** — {why}")

    ice = sorted([r for r in routed if r["north_of"] > 3.0], key=lambda r: -r["north_of"])
    L += ["", "### Routes the ice would not have allowed", "",
          "The mask is a shoreline and knows nothing about ice, so the cheapest water between two "
          "far-apart waypoints can be a passage no ship of the day could take. These are the routed "
          "lines that reach well north of every waypoint on their own track; the fix is a waypoint in "
          "the channel the voyage actually used, which is how the data already works.", ""]
    if ice:
        for r in ice:
            L.append(f"- **{r['id']}** — {r['title']}  \n  the line reaches {r['north_of']:.0f}° "
                     f"further north than any of its waypoints, and runs {r['routed_km']:,.0f} km "
                     f"against {r['straight_km']:,.0f} km straight")
    else:
        L.append("- none")

    gc = [r for r in routed if r["great_circle"] or r["outside"]]
    L += ["", "### Legs outside the masks", ""]
    if gc:
        for r in sorted(gc, key=lambda r: -r["great_circle"]):
            L.append(f"- **{r['id']}** — {r['title']}: {r['great_circle']} leg(s) fell back to a "
                     f"great circle" + (", and part of the line is outside both masks" if r["outside"] else ""))
    else:
        L.append("- none")
    L.append("")

    # ------------------------------------------------------------- comparison
    L += ["## Comparison with the other routing run", ""]
    if comps is None:
        L.append("The live database was not readable at the end of this run.")
    elif not comps:
        L += [f"Read at {meta['cmp_time']}: **no track's `geometry` yet differs from its waypoints "
              f"joined straight**, so their run had rewritten none of the {meta['cmp_tracks']} tracks "
              "by the time this one finished. Rerun this tool later, or give `--theirs DIR` a "
              "directory of their per-track GeoJSON, and the comparison will fill in.", ""]
    else:
        both = [c for c in comps if c["routing"] == "water"] or comps
        L += [f"Read at {meta['cmp_time']}: **{meta['db_rewritten']} of {meta['cmp_tracks']} tracks** "
              "had a `geometry` in the live database differing from the waypoints joined straight, so "
              "that is how many their run had rewritten by then."
              + (f" **{meta['from_dir']}** further lines were read from `{meta['theirs']}`, where "
                 "their run leaves each track as it finishes; the source is given per track below."
                 if meta["from_dir"] else "")
              + " Both lines are measured on **this** run's fine mask, which is not the mask their "
              "run used, so a land fraction of a per cent or so on either line may be no more than "
              "the two shorelines disagreeing; a land fraction of five or ten per cent is a real "
              "crossing. The measures are the "
              "share on land, the share running within "
              f"{HUG_KM:g} km of a shore, and the median distance offshore, all sampled every 3 km. "
              "The separation is symmetric -- points every 5 km along each line to the nearest point "
              "of the other, so a leg one of them leaves straight cannot hide -- and 'where the gap "
              "is' names the place nearest the widest gap.", "",
              f"Over the {len(both)} tracks both runs routed through water: on land "
              f"{np.mean([c['their_land'] for c in both]):.1%} theirs, "
              f"{np.mean([c['mine_land'] for c in both]):.1%} mine; hugging a shore "
              f"{np.mean([c['their_hug'] for c in both]):.0%} theirs, "
              f"{np.mean([c['mine_hug'] for c in both]):.0%} mine; median offshore "
              f"{np.mean([c['their_off'] for c in both]):.0f} km theirs, "
              f"{np.mean([c['mine_off'] for c in both]):.0f} km mine; points per track "
              f"{np.mean([c['their_points'] for c in both]):.0f} theirs, "
              f"{np.mean([c['mine_points'] for c in both]):.0f} mine; length "
              f"{sum(c['their_km'] for c in both):,.0f} km theirs, "
              f"{sum(c['mine_km'] for c in both):,.0f} km mine; the two lines are "
              f"{np.mean([c['mean_km'] for c in both]):.1f} km apart on average.",
              "",
              f"{len(comps) - len(both)} of the {len(comps)} are tracks this run draws as-given and "
              "theirs routed, where the disagreement is over the flag and not over the water."
              if len(both) < len(comps) else "", "",
              "| track | flag here | theirs from | on land T/M | hugging shore T/M | points T/M | "
              "mean apart | max apart | where the gap is |",
              "|---|---|---|---|---|---|---|---|---|"]
        for c in sorted(comps, key=lambda c: -c["max_km"]):
            at = c.get("at_place") or (f"{c['at'][0]:.1f} N {abs(c['at'][1]):.1f} "
                                       f"{'W' if c['at'][1] < 0 else 'E'}" if c["at"] else "-")
            src = "db" if c["source"] == "the live database" else "geojson"
            L.append(f"| {c['id']} | {c['routing']} | {src} | "
                     f"{c['their_land']:.0%} / {c['mine_land']:.0%} | "
                     f"{c['their_hug']:.0%} / {c['mine_hug']:.0%} | "
                     f"{c['their_points']} / {c['mine_points']} | {c['mean_km']:.1f} km | "
                     f"{c['max_km']:.0f} km | {at} |")
        L += ["", "### Where they differ most, and which line reads better", ""]
        for c in sorted(comps, key=lambda c: -c["max_km"]):
            L.append(f"- **{c['id']}** — {c['title']}  \n  {c['verdict'].rstrip('.')}.")
    L.append("")

    L += ["## Figures", "",
          "In `figures/`, all drawn at twice the size and reduced, so the lines are smooth. "
          "This run's line is yellow, the live database's is blue, the waypoints joined straight are "
          "faint red, waypoints are white dots.", "",
          "- `three-voyages.png` — Franklin 1845, the Gjoa, Parry's Fury and Hecla",
          "- `archipelago.png` — every track over the Northwest Passage",
          "- `overview.png` — every track over the whole fine mask",
          "- `contact-sheet.png` — the ten longest voyages, one panel each"]
    for slug, name, _ in ZOOMS:
        L.append(f"- `zoom-{slug}.png` — {name}")
    L.append("")
    path.write_text("\n".join(L), encoding="utf-8")


# -------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--db", default=None)
    ap.add_argument("--track", action="append", default=[], help="one track id; repeatable")
    ap.add_argument("--all", action="store_true", help="every track in the database")
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 4) - 4))
    ap.add_argument("--rebuild-masks", action="store_true", help="rebuild the masks and cost surfaces")
    ap.add_argument("--straits", action="store_true", help="only check the two narrow straits")
    ap.add_argument("--no-figures", action="store_true")
    ap.add_argument("--write", action="store_true",
                    help="ALSO write geometry and routing into the database (OFF by default; "
                         "this tool is meant to be read from its ledger, not to touch the db)")
    ap.add_argument("--theirs", default=None, metavar="DIR",
                    help="a directory of <track-id>.geojson LineStrings to compare against for any "
                         "track the live database has not had rewritten yet, for when the other run "
                         "writes the database only at the end")
    ap.add_argument("--gc-step-km", type=float, default=GC_STEP_KM,
                    help="how far apart the points are along an as-given track's great-circle legs "
                         f"(default {GC_STEP_KM:g} km)")
    ap.add_argument("--as-given-straight", action="store_true",
                    help="draw an as-given track as its bare waypoints instead of great-circle arcs "
                         "(the old behaviour; --as-given-great-circle is the default)")
    ap.add_argument("--gshhg", default=str(MASKS / "gshhg-shp-2.3.7.zip"))
    a = ap.parse_args()
    if not (a.all or a.track or a.straits):
        ap.error("give --all, --track ID or --straits")
    t_start = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    FIGS.mkdir(parents=True, exist_ok=True)
    zpath = gshhg_zip(Path(a.gshhg))
    fine = Grid(FINE, zpath, a.rebuild_masks)
    coarse = Grid(COARSE, zpath, a.rebuild_masks)

    straits = check_straits(fine)
    ok = True
    for s in straits:
        print(f"{s['strait']}: {'; '.join(s['ends'])}; open at 1 km: {s['open at 1 km']}, "
              f"diagonally: {s['open diagonally']}, on the 4 km level: "
              f"{s['open on the 4 km first level']}, narrowest {s['width km']:.1f} km",
              file=sys.stderr)
        ok &= bool(s["open at 1 km"] or s["open diagonally"])
    if a.straits:
        return 0 if ok else 1
    if not ok:
        print("WARNING: a strait the mask must keep open is closed", file=sys.stderr)

    # read-only, always: another run may be writing this database right now, and
    # this tool is not allowed to disturb it. --write opens its own connection.
    import sqlite3
    dbpath = Path(a.db) if a.db else ROOT / "db" / "history" / "history.sqlite"
    ro = sqlite3.connect(f"file:{dbpath}?mode=ro", uri=True, timeout=60)
    ro.row_factory = sqlite3.Row
    rows = {r["id"]: r for r in ro.execute("SELECT * FROM artifacts WHERE type='track' ORDER BY id")}
    want = list(a.track) if a.track else list(rows)
    missing = [i for i in want if i not in rows]
    if missing:
        raise SystemExit(f"no track {', '.join(missing)}")

    jobs, why = [], {}
    for tid in want:
        row = rows[tid]
        flag = (row["routing"] or "").strip()
        if flag:
            why[tid] = f"the flag in the database is already {flag}"
        else:
            flag, why[tid] = decide(row)
        jobs.append(dict(id=tid, title=row["title"], flag=flag, pts=waypoints_of(row),
                         gc_step=0.0 if a.as_given_straight else a.gc_step_km))

    n = min(max(1, a.jobs), len(jobs))
    print(f"routing {len(jobs)} tracks on {n} workers", file=sys.stderr)
    if n > 1:
        ctx = mp.get_context("fork")
        with ctx.Pool(n, initializer=_init, initargs=((fine, coarse),)) as pool:
            recs = []
            for rec in pool.imap_unordered(route_track, jobs, chunksize=1):
                recs.append(rec)
                print(f"  {rec['id']}: {rec['routing']}, {rec['waypoints']} waypoints -> "
                      f"{rec['points']} points, land {rec['straight_land']:.0%} -> "
                      f"{rec['routed_land']:.0%}, {rec['seconds']:.1f} s", file=sys.stderr)
    else:
        _init((fine, coarse))
        recs = [route_track(j) for j in jobs]
    by_job = {j["id"]: j for j in jobs}
    for r in recs:
        r["why"] = why[r["id"]]
        r["straight"] = [(p[0], p[1]) for p in by_job[r["id"]]["pts"]]
    recs.sort(key=lambda r: r["id"])
    seconds = time.time() - t_start
    print(f"\n{len(recs)} tracks in {seconds:.0f} s", file=sys.stderr)

    # ------------------------------------------------ their run, at the end
    cmp_time = time.strftime("%Y-%m-%d %H:%M")
    comps, theirs, from_dir = [], {}, 0
    live_ro = sqlite3.connect(f"file:{dbpath}?mode=ro", uri=True, timeout=60)
    live_ro.row_factory = sqlite3.Row
    live = {r["id"]: r for r in live_ro.execute("SELECT * FROM artifacts WHERE type='track'")}
    places = [(r["name"], float(r["lat"]), float(r["lon"])) for r in
              live_ro.execute("SELECT name, lat, lon FROM places WHERE lat IS NOT NULL")]
    for r in recs:
        row = live.get(r["id"])
        if row is None:
            continue
        their = geometry_of(row)
        straight = r["straight"]
        # their geometry is stored rounded, so "the waypoints joined straight"
        # means the same points to within the rounding
        same = (len(their) == len(straight)
                and all(abs(x[0] - y[0]) < 1e-4 and abs(x[1] - y[1]) < 1e-4
                        for x, y in zip(their, straight)))
        source = "the live database"
        if a.theirs:
            # the other run may not write the database at all; its line on disk
            # is the better source, and stays the right one after this tool has
            # written its own lines into the database
            f = Path(a.theirs) / f"{r['id']}.geojson"
            if f.exists():
                try:
                    g = json.loads(f.read_text())
                    their = [(float(y), float(x)) for x, y in
                             (g.get("coordinates") or g.get("geometry", {}).get("coordinates", []))]
                    source, from_dir = f"{a.theirs}", from_dir + 1
                    same = False
                except (json.JSONDecodeError, OSError, TypeError, ValueError):
                    pass
        if len(their) < 2 or same:
            continue
        theirs[r["id"]] = their
        tl, t_hug, t_off = line_shore((fine, coarse), their)
        ml, m_hug, m_off = line_shore((fine, coarse), r["line"])
        mean_km, max_km, where = line_distance_km(r["line"], their)
        cc = dict(id=r["id"], title=r["title"], routing=r["routing"], why=r["why"],
                  their_land=tl, mine_land=ml, their_hug=t_hug, mine_hug=m_hug,
                  their_off=t_off, mine_off=m_off,
                  their_points=len(their), mine_points=r["points"],
                  their_km=line_km(their), mine_km=r["routed_km"],
                  mean_km=mean_km, max_km=max_km, at=where, source=source,
                  at_place=nearest_place(places, where) if where else None)
        cc["verdict"] = verdict(r, cc)
        comps.append(cc)
    for r in recs:
        r["theirs"] = theirs.get(r["id"], [])
        r["verdict"] = next((c["verdict"] for c in comps if c["id"] == r["id"]), "")

    # ----------------------------------------------------------- the output
    fc = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "id": r["id"], "geometry": as_geojson(r["line"]),
         "properties": {"id": r["id"], "title": r["title"], "routing": r["routing"],
                        "routing_reason": r["why"],
                        "straight": [[round(lo, 5), round(la, 5)] for la, lo in r["straight"]],
                        "waypoints": r["waypoints"], "points": r["points"],
                        "straight_land_frac": round(r["straight_land"], 4),
                        "routed_land_frac": round(r["routed_land"], 4),
                        "straight_km": round(r["straight_km"], 1), "routed_km": round(r["routed_km"], 1),
                        "segments_coarse": r["coarse"], "segments_great_circle": r["great_circle"],
                        "segments_crossing_land": r["crossed"], "seconds": r["seconds"],
                        "verdict_vs_live_db": r["verdict"]}}
        for r in recs]}
    (OUT / "routes.geojson").write_text(json.dumps(fc, ensure_ascii=False), encoding="utf-8")

    meta = dict(run=time.strftime("%Y-%m-%d"), seconds=seconds, jobs=n,
                cmd=" ".join(["python tools/route-tracks.py"] + sys.argv[1:]),
                cmp_time=cmp_time, cmp_tracks=len(live), from_dir=from_dir, theirs=a.theirs,
                wrote=a.write,
                db_rewritten=sum(1 for c in comps if c["source"] == "the live database"))
    render_summary(recs, comps, fine, coarse, straits, meta, OUT / "summary.md")

    if not a.no_figures:
        t0 = time.time()
        by_id = {r["id"]: r for r in recs}
        lbl = ("the live database" if not from_dir else
               "their run, from " + os.path.basename(str(a.theirs).rstrip("/")))
        three = [by_id[i] for i in ("franklin-1845-001", "amundsen-gjoa-001", "ross-parry-003") if i in by_id]
        figure(fine, (60.0, -125.0, 80.0, -60.0), 2400, FIGS / "three-voyages.png", three,
               "Franklin 1845, the Gjoa, Parry's Fury and Hecla", theirs_label=lbl)
        drawn = [r for r in recs if len(r["line"]) > 1]
        figure(fine, (58.0, -130.0, 80.5, -58.0), 2400, FIGS / "archipelago.png", drawn,
               "Every track, the Northwest Passage", waypoints=False, theirs_label=lbl)
        figure(fine, (36.0, -149.0, 85.0, 14.0), 2400, FIGS / "overview.png", drawn,
               "Every track, the whole fine mask", waypoints=False, theirs_label=lbl)
        for slug, name, box in ZOOMS:
            here = [r for r in drawn if _touches(r, box)]
            figure(fine, box, 2400, FIGS / f"zoom-{slug}.png", here, name, theirs_label=lbl)
        longest = sorted([r for r in recs if r["routing"] == "water"],
                         key=lambda r: -r["routed_km"])[:10]
        contact_sheet(fine, FIGS / "contact-sheet.png", longest)
        print(f"figures in {time.time() - t0:.0f} s -> {FIGS.relative_to(ROOT)}", file=sys.stderr)

    if a.write:
        print("--write: putting geometry and routing into the database", file=sys.stderr)
        import arctic_history as H
        c = H.connect(dbpath, create=False)
        n_w = n_water = n_given = 0
        refused = []
        for r in recs:
            row = live[r["id"]]
            # both flags get a line: the routed one for water, the waypoints
            # joined by great-circle arcs for as-given
            geom = as_geojson(r["line"]) if len(r["line"]) > 1 else None
            try:
                write_row(c, row, r["routing"], geom)
            except Exception as e:                          # a row the writer will not take
                refused.append(f"{r['id']}: {e}")
                continue
            n_w += 1
            n_water += r["routing"] == "water"
            n_given += r["routing"] != "water"
        c.commit()
        for line in refused:
            print("REFUSED " + line, file=sys.stderr)
        print(f"--write: {n_water} water, {n_given} as-given, {len(refused)} refused",
              file=sys.stderr)
        print(f"--write: {n_w} rows written", file=sys.stderr)
    else:
        print("the database was not written to (--write is off)", file=sys.stderr)
    print(f"{(OUT / 'summary.md').relative_to(ROOT)} and routes.geojson written", file=sys.stderr)
    return 0


def _touches(rec, box):
    s, w, n, e = box
    for p in rec["line"]:
        if s <= p[0] <= n and w <= p[1] <= e:
            return True
    return False


if __name__ == "__main__":
    sys.exit(main())
