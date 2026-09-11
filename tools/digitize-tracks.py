#!/usr/bin/env python3
"""Digitize the printed route maps and route the overland tracks through the terrain.

The sea router (tools/route-tracks.py) draws a voyage through water.  This is
its overland sibling.  A sledge journey's waypoints are 50 to 150 km apart, and
the great-circle legs the map draws between them run over ridges and ice caps
that the party went round: they used the valleys, the passes and the fiord ice.
The collection also holds the expeditions' own printed route maps, which show
where the line went at a scale that hides the valley.  This tool does three
things, each usable alone:

  1. georeference a printed map from control points,
  2. extract the drawn route from the scan and turn it into lon/lat, and
  3. route each leg between consecutive waypoints over a cost surface built
     from a digital elevation model, the shoreline and the season, pulled
     toward the printed route where one has been digitized.

``waypoints`` are never touched.  Every waypoint stays exactly on the routed
line, as with the sea router, and nothing is written to the database unless
--write is given.

    tools/digitize-tracks.py dem                      build the DEM mosaic cache (once; 4 min)
    tools/digitize-tracks.py crops --map haig-thomas-1937-059
                                                      gridded crops of a map to read control points off
    tools/digitize-tracks.py georef --map haig-thomas-1937-059
                                                      fit the projection from <id>.cp.json, draw the check
    tools/digitize-tracks.py digitize --map haig-thomas-1937-059 --track haig-thomas-1937-001
                                                      pull the drawn route out of the scan
    tools/digitize-tracks.py route --track haig-thomas-1937-001
                                                      route the legs through the terrain
    tools/digitize-tracks.py route --all               every track flagged as-given or terrain
    tools/digitize-tracks.py route --track ID --write  ALSO write geometry and routing=terrain to the db
    tools/digitize-tracks.py gallery                   rebuild the gallery page from what is on disk

Run it from the repository root with the routing venv:

    .route-venv/bin/python tools/digitize-tracks.py route --track haig-thomas-1937-001

The venv is the sea router's (numpy, scipy, scikit-image, pillow, shapely,
pyproj, rasterio); nothing was added to it.

## What it writes

Everything lands in db/history/_ledger/routing/terrain/ (gitignored), beside
the sea router's output:

    georef/<map-id>.cp.json         the control points, read by hand off the crops
    georef/<map-id>.georef.json     the fitted model: family, parameters, affine,
                                    residuals; reused by every later run
    georef/<map-id>.crops.png       the gridded crops the points were read from
    digitized/<track-id>.geojson    the drawn route in lon/lat, one part per leg,
                                    each part saying whether it came from ink
    routes.geojson                  one Feature per routed track: the routed line,
                                    the digitized line and the numbers
    summary.md                      per-track verdicts, per-map residuals
    figures/<map-id>-georef.png     the GSHHG shoreline projected through the model
                                    over the scan: the fit's own check
    figures/<track-id>-map.png      the scan with the digitized chain, the routed
                                    line and the waypoints
    figures/<track-id>-terrain.png  a hillshade with the old line, the digitized
                                    line and the routed one
    gallery.html                    all of it on one page, served like the sea
                                    router's: python3 -m http.server 8766 in
                                    db/history/_ledger/routing, then
                                    http://127.0.0.1:8766/terrain/gallery.html

## The DEM

Copernicus GLO-90 (the 90 m global DSM from the ESA Copernicus programme), read
from the public AWS bucket copernicus-dem-90m, one tile per degree square, no
login.  Its licence is the Copernicus DEM licence: free use, reproduction and
distribution, with the source acknowledged ("produced using Copernicus WorldDEM-90
(c) DLR e.V. 2010-2014 and (c) Airbus Defence and Space GmbH 2014-2018 provided
under COPERNICUS by the European Union and ESA; all rights reserved").  It was
chosen over Natural Resources Canada's CDEM because it covers Greenland and the
Canadian islands alike from one source, at one resolution, and because a tile is
a single curl.  The tiles live in /data/gis/dem/glo90/ (2,172 tiles, 60 to 84 N,
30 to 170 W, 3.3 GB; 74 to 84 N and 30 to 130 W until 2026-09-10); the fetch script beside them is
/data/gis/dem/fetch.sh.  The cost surface never needs 90 m: the routes were drawn
at 1:2,000,000, so the tiles are mosaicked once into a polar stereographic grid
at 250 m,

    +proj=stere +lat_0=90 +lat_ts=78 +lon_0=-85 +datum=WGS84 +units=m

covering 60 to 84 N, 30 to 170 W, and cached in /data/gis/dem/mosaic/ as
memory-mapped float32 arrays: the elevation, the slope in degrees, and two byte
masks -- land from the full-resolution GSHHG shoreline (the sea router's zip,
level 1: a lake is not sea), ice from Natural Earth's 10 m glaciated areas
(public domain, /data/gis/dem/ne/).  A cell of the grid is 250 m on the ground
to within 3 per cent across the extent (the stereographic scale runs from 0.97
at 84 N to 1.03 at 74 N) and the cost of a step is its true ground length, so
the cheapest path is the shortest on the ground, as in the sea router.

## Georeferencing

A printed map's projection is unknown but from a short list: the expeditions'
maps are polar stereographic or a conic with a central meridian somewhere near
80 to 90 W, the Admiralty's are Mercator, the American charts polyconic.  The
model fitted here is a projection from that list plus a full affine (six
parameters: scale, rotation, shear, offset), fitted to control points:
graticule intersections read off the scan, and named capes, harbours and
islands whose coordinates the ``places`` table holds.  For each family the
projection's free parameters (the standard parallels of a conic, the central
meridian of a polyconic) are found by least squares with the affine solved
linearly inside, and the family with the smallest residual wins; a rotation
about the pole is a rigid rotation of the page, so the central meridian of a
conic or an azimuthal map is fixed at the middle of the control points rather
than fitted.

That is the whole model for a surveyed chart.  An expedition's sketch map is
another thing: Haig-Thomas's graticule is hand-drawn and 20 px from where any
projection puts it, and his Axel Heiberg is 40 px from the real one, yet the
route was drawn against *his* coasts, so what has to be recovered is the map
from the sketched coast to the real one.  The fit is therefore refined against
the shoreline itself: an iterative closest-point match between the GSHHG
shoreline projected through the model and the map's ink, the affine refitted
at a wide radius and then, at shrinking radii, a smooth warp in pixel space
(Gaussian radial functions on a grid of knots 250 px apart, fitted by least
squares to the matched pairs with the control points weighted fifty times each
and a weak zero-shift anchor at every knot, so it fades to nothing where no
coast holds it).  Lettering and the route's own dots are outvoted by the coast.

Residuals are reported per point in pixels and in ground kilometres, before
and after the refinement, with the coast match (the median distance of the
projected shoreline from the nearest ink, inside the control points' box, and
the share within 3 and 6 px).  **A fit is accepted when the control-point RMS
is under four pixels with no point over ten, or, after the coast refinement,
when the coast match's median is under eight pixels and eight kilometres with
at least 40 per cent of the shoreline within six pixels**; four pixels is the
width of a drawn line on these scans and eight is what a sketch map's coast
can be held to, and a fit worse than that is refused as a coincidence.  The
kilometre ceiling is what refuses the Crocker Land plate, a pictorial globe at
2 km/px whose coast the warp can hold to seven pixels and sixteen kilometres.  The check figure draws the
shoreline through the model over the scan, which is the test a number cannot
replace.  The model is saved beside the figures and read back by every later
run, so a map is fitted once.

Control points are read by hand: ``crops`` writes a sheet of gridded crops with
pixel rulers, one reads the intersections and the capes off it, and writes
them to ``georef/<map-id>.cp.json`` as

    {"rotate": 0,
     "points": [{"px": 701, "py": 557, "lon": -100, "lat": 80},
                {"px": 1409, "py": 902, "place": "Etah"}]}

``rotate`` is the quarter turns anticlockwise that put the scan north-up; every
pixel coordinate is in the north-up image.  A ``place`` is looked up in the
``places`` table and its coordinates used; a point with ``lon`` and ``lat``
is a graticule intersection.  A residual named in the check figure is a point
to re-read.

## Extraction

The route on a printed map is a dotted, dashed or solid line, sometimes
coloured, drawn over coastlines and lettering.  The ink is separated by colour
where the line is coloured (``"ink": "colour:red"`` in the map table below) and
by morphology otherwise: connected components of ink whose size is a dot's or
a dash's, the coastline and the lettering being far larger; for a solid black
route the ink is skeletonized and the GSHHG shoreline, projected through the
georeference, is erased from it first.  What remains is a cloud of fragments.
They are chained in order by the track's own waypoints: for each leg the
fragments within a corridor of the leg are the nodes of a graph, edges join
neighbours with a cost that grows faster than the distance so that many short
hops beat one long jump, and the cheapest path from one waypoint's pixel to the
next is the drawn route between them.  A leg with no ink within reach is left
as its great circle and said so.  The chain is converted to lon/lat through the
model's inverse and simplified to a kilometre.

## Routing through the terrain

Each leg between consecutive waypoints is routed on its own, as in the sea
router, by scikit-image's geometric minimum-cost path over a window of the 250 m
grid.  The cost of stepping into a cell is its ground length in km times a
multiplier:

    land        1.3 x (1 + 6 (tan slope / 0.12)^2, capped at 60)
                    x (1 + elevation above 100 m / 500 m)
    ice cap     the land cost x 4; or, when the narrative says the ice cap
                was crossed (a note on either waypoint of the leg naming an
                ice cap or glacier or a crossing, or, when no note does, the
                track's description or tags naming an ice cap), 1.3 x 1.2 x
                the slope term alone, an ice cap being smooth going
    sea ice     1.0 in the sledging season (November to June by the leg's date)
    open water  4 in July to October when both ends of the leg are on land
                (they walked, and a crossing between islands is dear but not
                a wall); 1.5 whatever the month when both ends are in the sea
                or the track's title, description or tags name a boat (a boat
                leg); 3 when one end is
    corridor    x (1 + 3 min(1, (d / 12 km)^2)), d the distance to the
                digitized line, when a digitized line exists for the track
    straight    x (1 + 0.08 min(1, d / 25 km)), d the distance to the leg's
                great circle, on a leg with no digitized line instead

so a valley floor is cheap, a valley wall dear, a plateau dearer the higher it
is, a pass the cheapest way over a divide, and fiord ice the cheapest way of
all.  The slope term is quadratic in the gradient so that a 7 degree slope costs
double and a 20 degree one twenty times; the elevation term is what makes a
route go round a plateau through the valleys rather than over it.  The corridor
term pulls the path toward the printed route without pinning it: a valley five
kilometres off the drawn line costs a fifth more, a pass twenty kilometres off
four times as much, so the result follows what the map shows but through the
valley the map's scale hides.

The straightness term is the same idea for a leg no ink holds.  Over sea ice
the surface is flat: every path of the same ground length costs the same, so
which detour the search returns is arbitrary, and it is not even quite flat,
because the stereographic scale makes a cell one per cent cheaper at one end of
the grid than the other, which is enough to bow a 500 km leg by forty
kilometres into the middle of a sound.  The term is linear in the distance from
the great circle, not quadratic, so that it bites at once and beats that
artefact within a kilometre or two of the line, and it is capped at eight per
cent, a quarter of what the cheapest land costs over sea ice and a fiftieth of
an ice cap, so it settles a tie and never outvotes the terrain: a party that
went round an island still goes round it, and one that crossed featureless ice
goes straight.  It is off wherever a digitized line exists, the ink being
better evidence than the straight line.

The ice mask is clipped to the land: Natural Earth's glaciated areas are drawn
at 10 m and spill over the fiords the glaciers head, and ice cannot be where
the full-resolution shoreline says sea.  And a waypoint plotted to a tenth of a
degree often falls a few kilometres inland of the water its own note names -- a
sound, a fiord, the pack -- which would make the leg climb the shore and come
back down.  Such a waypoint has the nearest sea within twelve kilometres cut
open to it, a channel at the sea-ice cost, and counts as a sea end for the
season's sake.  The waypoint itself is not moved: the line still passes through
it exactly, by the shortest way to the water.

A leg's date is the waypoint's own where it has
one and otherwise interpolated between the dated waypoints either side (the
track's own dates at the ends).

A window is the leg's bounding box plus a margin; when it exceeds six million
cells the search runs first on the surface pooled 4x by its cheapest cell, so a
valley is never closed by the pooling, and then again at 250 m inside a 10 km
corridor round that path.  The staircase that comes out is simplified to 300 m,
rounded by two Chaikin passes and simplified again to half a kilometre, within
one leg, never across a waypoint.  A waypoint outside the DEM's extent hands
its legs to the sea router (tools/route-tracks.py): the water path on its fine
mask when both ends lie in it, else its coarse one, else a great circle -- so
the voyage legs of a mixed track (Rae's passage home, the Isabella carrying
Ross's boats to Hull) follow the sea instead of chording across Greenland.
Those legs are flagged ``fallback`` all the same, and the grade says so.

## Waypoints that are wrong, and moving them

Many waypoints were guesses: the note says "inferred" or "approximate", or the
point sits on land at 600 m though the note names a sound.  The run reports
every waypoint's ground (sea, land, ice cap), elevation and distance from the
digitized ink, and for one that is inferred or contradicted by its ground and
more than 5 km from the ink it proposes a move to the nearest point of the
ink, written to ``digitized/<track>.moves.proposed.json``.  Nothing moves on
its own: renaming that file to ``<track>.moves.json`` (or writing one by hand,
a list of {"index", "lat", "lon", "why"}) applies the moves on the next run,
the digitizing and the routing both start from the moved points, and
``--write`` then writes the moved waypoint with its note extended by the reason
and the position it had before, and the description extended by a sentence
listing the moves.  Waypoints are the dated truth of the narrative and a move
is only ever made on the evidence of the map and the terrain together.

## The flag, the grades and the gallery

A track routed here is flagged ``terrain`` (added to ROUTING in
arctic_history/__init__.py and to the brief with this tool); ``--write`` sets
it and puts the line in ``geometry``, through ``H.add_artifact`` with every
other field of the row as it stands.  ``route --all`` takes every track flagged
``as-given`` or ``terrain``; a ``water`` track is the sea router's.

Each track gets a grade in summary.md and the gallery: **recommend** (every leg
routed inside the DEM and, where a map was digitized, at least half the legs
from its ink), **review** (some legs outside the DEM, left as great circles,
which is right over the sea ice), **same** (the routed line is the database's
to within 3 km, so nothing to write back: a journey over uniform sea ice routes
straight), **outside** (every leg outside the DEM: not this tool's track) and
**written** (already in the database with this line).  The gallery shows, per
track, the verdict, a table of the waypoints with their ground and flags, the
hillshade figure and the map figure.

A grade is not a judgement, and one thing in particular the numbers cannot
settle: a long leg held by no ink.  Over uniform sea ice every path of the same
ground length costs the same, so which detour the search returns is arbitrary,
and a party's single long homeward leg can come back as a bow into the middle of
a sound or a circuit round the wrong side of an island.  The verdict therefore
names every leg with no ink that the terrain lengthens by more than a quarter
and by more than twenty kilometres; those are the legs to look at in the figure
before the track is written back.
"""
import argparse, importlib.util, json, math, os, sys, time, zipfile
from pathlib import Path

import numpy as np
from scipy import ndimage
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra
from skimage.graph import route_through_array

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

LEDGER = ROOT / "db" / "history" / "_ledger"
OUT = LEDGER / "routing" / "terrain"
GEOREF = OUT / "georef"
DIGIT = OUT / "digitized"
FIGS = OUT / "figures"
FILES = ROOT / "db" / "history"
GIS = Path("/data/gis/dem")
TILES = GIS / "glo90"
MOSAIC = GIS / "mosaic"
NE_ZIP = GIS / "ne" / "ne_10m_glaciated_areas.zip"
NE_URL = "https://naciscdn.org/naturalearth/10m/physical/ne_10m_glaciated_areas.zip"
GSHHG_ZIP = LEDGER / "masks" / "gshhg-shp-2.3.7.zip"

# the grid: polar stereographic, 250 m, 60..84 N, 30..170 W (74..84 N, 30..130 W until 2026-09-10)
PROJ = "+proj=stere +lat_0=90 +lat_ts=78 +lon_0=-85 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
RES = 250.0
EXTENT = dict(lat=(60.0, 84.0), lon=(-170.0, -30.0))
R_EARTH = 6371.0088

# the cost surface
LAND_BASE = 1.3
SLOPE_W, SLOPE_S, SLOPE_CAP = 6.0, 0.12, 60.0
ELEV_FLOOR, ELEV_S = 100.0, 500.0
ICE_DEAR, ICE_CROSSED = 4.0, 1.2
SEA_ICE, SEA_SUMMER, SEA_BOAT, SEA_MIXED = 1.0, 4.0, 1.5, 3.0
BOAT_WORDS = ("boat", "umiak", "canoe", "kayak", "whaleboat", "raft")
CORR_W, CORR_KM = 3.0, 12.0
# the straightness prior on a leg held by no ink: over featureless sea ice the
# cost surface is flat and every path of the same ground length ties, so the
# search returns an arbitrary bow -- and it is not quite flat, because the
# stereographic scale makes a cell one per cent cheaper at one end of the grid
# than the other, which is enough to bend a long leg by forty kilometres.  A
# weak pull toward the leg's great circle breaks the tie.  It is linear in the
# distance, not quadratic, so that it bites at once (a kilometre off the line
# already costs more than the scale artefact), and it is capped at eight per
# cent, far below the cheapest land's thirty over sea ice and the ice cap's
# four hundred, so real terrain still bends the route where terrain is what is
# in the way and only a tie is settled by the straight line
STRAIGHT_W, STRAIGHT_KM = 0.08, 25.0
# a waypoint whose note names water but which the shoreline puts on land: the
# nearest sea within this far is cut open to it at the sea-ice cost, so the leg
# reaches the fiord instead of climbing the shore, and the end counts as sea
SHORE_KM = 12.0
WINDOW_MARGIN_KM, WINDOW_MARGIN_FRAC = 40.0, 0.5
WINDOW_BUDGET = 6_000_000
DOWN = 4
REFINE_KM = 10.0
SLEDGE_MONTHS = {11, 12, 1, 2, 3, 4, 5, 6}
ICE_WORDS = ("ice cap", "ice-cap", "icecap", "glacier", "ice sheet", "inland ice")
CROSS_WORDS = ("crossing", "crossed", "across", "overland", "portage", "over the pass", "up the valley")

# the georeference
FIT_RMS_PX, FIT_MAX_PX = 4.0, 10.0
COAST_MEDIAN_PX, COAST_WITHIN_6 = 8.0, 0.4    # after the coastline refinement
COAST_MEDIAN_KM = 8.0                          # and on the ground: a pictorial globe at 2 km/px is no map
FAMILIES = ("stere", "lcc", "eqdc", "aea", "bonne", "poly", "merc", "eqc", "laea", "aeqd")

# the extraction
DOT_AREA, DOT_SIZE = (2, 60), 10          # a dot: area in px, longest side
DASH_AREA, DASH_SIZE = (2, 400), 40       # a dash
CORRIDOR_KM = 60.0                        # fragments this far from a leg's straight line are its candidates
HOP_POWER = 1.6                           # edge cost = d^HOP_POWER, so short hops beat long jumps
DOUBT_FACTOR, DOUBT_KM = 1.5, 5.0        # a chain longer than this times the leg is doubted

# a leg with no ink that the terrain lengthens by more than this is named in the
# verdict: over uniform sea ice the cheapest path is degenerate and the detour it
# picks is arbitrary, so a long unpinned leg is the first thing to look at
DETOUR_FACTOR, DETOUR_KM = 1.25, 20.0

# maps in the collection and the tracks drawn on them.  ``rotate`` is quarter
# turns anticlockwise to north-up; ``ink`` how the route is drawn
MAPS = {
    "haig-thomas-1937-059": dict(rotate=0, ink="dots", tracks={"haig-thomas-1937-001": None}),
    "oxford-ellesmere-1934-005": dict(rotate=0, ink="dashes",
                                      tracks={"oxford-ellesmere-1934-002": "dashes",      # Moore and Stallworthy, dashed
                                              "oxford-ellesmere-1934-003": "solid",       # Humphreys and Haig-Thomas
                                              "oxford-ellesmere-1934-004": "dots"}),      # Shackleton and Bentham
    "oxford-ellesmere-1934-073": dict(rotate=0, ink="dashes",
                                      tracks={t: None for t in (
                                          "rcmp-high-arctic-patrols-001", "rcmp-high-arctic-patrols-002",
                                          "rcmp-high-arctic-patrols-003", "rcmp-high-arctic-patrols-004",
                                          "rcmp-high-arctic-patrols-005", "rcmp-high-arctic-patrols-006",
                                          "rcmp-high-arctic-patrols-007", "rcmp-high-arctic-patrols-008",
                                          "rcmp-high-arctic-patrols-009", "rcmp-high-arctic-patrols-010",
                                          "posts-rcmp-missions-023")}),
    "kruger-1930-006": dict(rotate=0, ink="dashes", tracks={}),      # georeferenced, but no route drawn on it
    "kruger-1930-027": dict(rotate=0, ink="dashes", tracks={}),
    "kruger-1930-061": dict(rotate=0, ink="dashes", tracks={}),
    "nares-greely-154": dict(rotate=0, ink="dashes", tracks={}),   # georeferenced, but nothing extractable
    "nares-greely-171": dict(rotate=0, ink="dots",
                             tracks={"nares-greely-022": None, "nares-greely-038": None, "nares-greely-039": None}),
    "nares-greely-204": dict(rotate=0, ink="dashes", tracks={}),
    "crocker-land-1913-022": dict(rotate=0, ink="dashes",
                                  tracks={"crocker-land-1913-002": None, "crocker-land-1913-003": None,
                                          "crocker-land-1913-004": None}),
    "cook-1908-axel-heiberg-041": dict(rotate=0, ink="dashes", erase_coast=True,      # a stippled coast
                                       tracks={"cook-1908-axel-heiberg-001": None, "cook-1908-axel-heiberg-002": None}),
    "sverdrup-bernier-peary-064": dict(rotate=0, ink="dashes", erase_coast=True,     # hachured relief
                                       grade_cap="review",
                                       note="a first-reconnaissance sketch with hachured relief: the dash-dot "
                                            "route is hard to tell from the shading and the chain wanders, so "
                                            "the corridor is weak evidence here",
                                       tracks={"sverdrup-bernier-peary-300": None, "sverdrup-bernier-peary-301": None}),
    "kane-hall-polaris-193": dict(rotate=0, ink="dots", erase_coast=True,          # hachured coasts
                                  tracks={"kane-hall-polaris-263": None},
                                  grade_cap="review",   # Hayes's Ellesmere coast is a degree out
                                  note="Hayes's own chart puts the Ellesmere coast a degree too far north, so "
                                       "a route digitized against it is only as good as his coast"),
    "sverdrup-bernier-peary-154": dict(rotate=0, ink="dashes", tracks={}),
}


# maps in the candidate list that have no track to digitize onto, and why
MAP_NOTES = {
    "kruger-1930-006": "Barr's locator map of the search area: georeferenced (3 px), but it draws no route at "
                       "all, only coasts, names and the two posts, so there is nothing on it to digitize.",
    "kruger-1930-027": "Krüger's own sketch of the route he intended, not the one he took: nothing to route.",
    "kruger-1930-061": "the 1957 Geological Survey sledge journey to Meighen Island has no track artifact yet.",
    "nares-greely-154": "Lockwood's chart of the north Greenland coast: georeferenced against its own coast to "
                        "1.7 px (0.1 km), but its route is a hairline strung between small numbered camp circles "
                        "and the whole sheet is dense hachured relief.  The hachure strokes are a dash's size and "
                        "a dot's, so the morphology returns 7,000 of them and none of the route; skeletonizing the "
                        "sheet instead gives 61,000 fragments and the chain runs up Mascart Inlet through the "
                        "shading.  The sheet also covers only the last of the five legs (Cape Britannia to "
                        "Lockwood Island), so even a clean extraction would leave the track short of the half "
                        "the grade asks for.  nares-greely-023 is routed from its waypoints alone.",
    "nares-greely-204": "Lockwood's chart of his March to April 1883 journey north from Fort Conger; the only 1883 "
                        "track in the database is the August retreat (nares-greely-025), which this map does not show.",
    "sverdrup-bernier-peary-154": "the Falcon's 1893 voyage to Bowdoin Bay is a ship's track, the sea router's.",
}


# ------------------------------------------------------------------ helpers
def _load_route_tracks():
    spec = importlib.util.spec_from_file_location("route_tracks", ROOT / "tools" / "route-tracks.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_SEA = None


def _sea_grids():
    """The sea router's fine and coarse masks, loaded once from their caches,
    for the legs that leave the DEM."""
    global _SEA
    if _SEA is None:
        rt = _load_route_tracks()
        zpath = rt.gshhg_zip(GSHHG_ZIP)
        _SEA = (rt, rt.Grid(rt.FINE, zpath), rt.Grid(rt.COARSE, zpath))
    return _SEA


def gc_km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R_EARTH * math.asin(min(1.0, math.sqrt(h)))


def line_km(pts):
    return sum(gc_km(a, b) for a, b in zip(pts, pts[1:]))


def great_circle(a, b, step_km=20.0):
    return _load_route_tracks().great_circle(a, b, step_km)


def simplify_xy(xy, tol):
    """Douglas-Peucker on an (n, 2) array in a flat plane."""
    if len(xy) < 3:
        return list(range(len(xy)))
    keep, stack = {0, len(xy) - 1}, [(0, len(xy) - 1)]
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
        if dist[k] > tol:
            keep.add(i + 1 + k)
            stack += [(i, i + 1 + k), (i + 1 + k, j)]
    return sorted(keep)


def chaikin(xy, passes=2):
    for _ in range(passes):
        if len(xy) < 3:
            return xy
        out = [xy[0]]
        for a, b in zip(xy[:-1], xy[1:]):
            out.append(0.75 * a + 0.25 * b)
            out.append(0.25 * a + 0.75 * b)
        out.append(xy[-1])
        xy = np.array(out)
    return xy


def read_shapefile_polygons(zpath, member):
    """Every polygon ring in a shapefile inside a zip, as (n, 2) arrays with the
    record's bounding box (the sea router's reader, which needs no OGR)."""
    return _load_route_tracks().read_polygons(zpath, member)


# ---------------------------------------------------------------- the DEM
class Terrain:
    """The 250 m polar grid: elevation, slope, land and ice, memory-mapped, and
    the conversions between (lat, lon) and (row, col)."""

    def __init__(self, build=False):
        from pyproj import Transformer
        self.fwd_t = Transformer.from_crs("EPSG:4326", PROJ, always_xy=True)
        self.inv_t = Transformer.from_crs(PROJ, "EPSG:4326", always_xy=True)
        MOSAIC.mkdir(parents=True, exist_ok=True)
        meta_p = MOSAIC / "meta.json"
        lat0, lat1 = EXTENT["lat"]
        lon0, lon1 = EXTENT["lon"]
        lons = np.linspace(lon0, lon1, 721)
        lats = np.linspace(lat0, lat1, 101)
        LO, LA = np.meshgrid(lons, lats)
        X, Y = self.fwd_t.transform(LO, LA)
        x0, x1 = math.floor(X.min() / RES) * RES, math.ceil(X.max() / RES) * RES
        y0, y1 = math.floor(Y.min() / RES) * RES, math.ceil(Y.max() / RES) * RES
        self.x0, self.y1 = x0, y1
        self.ncols, self.nrows = int((x1 - x0) / RES), int((y1 - y0) / RES)
        meta = json.loads(json.dumps(dict(proj=PROJ, res=RES, extent=EXTENT, x0=x0, y1=y1,
                                          shape=[self.nrows, self.ncols])))
        names = ("dem", "slope", "land", "ice")
        ok = meta_p.exists() and json.loads(meta_p.read_text()) == meta and \
            all((MOSAIC / f"{n}.npy").exists() for n in names)
        if not ok or build:
            self._build(meta, meta_p)
        self.dem = np.load(MOSAIC / "dem.npy", mmap_mode="r")
        self.slope = np.load(MOSAIC / "slope.npy", mmap_mode="r")
        self.land = np.load(MOSAIC / "land.npy", mmap_mode="r")
        if not (MOSAIC / "ice.clipped").exists():
            # a cache built before the ice was clipped to the land
            ice = np.load(MOSAIC / "ice.npy") & np.load(MOSAIC / "land.npy", mmap_mode="r")
            np.save(MOSAIC / "ice.npy", ice)
            (MOSAIC / "ice.clipped").write_text("ice &= land\n")
            del ice
        self.ice = np.load(MOSAIC / "ice.npy", mmap_mode="r")

    # -- coordinates
    def rcf(self, lat, lon):
        x, y = self.fwd_t.transform(lon, lat)
        return (self.y1 - y) / RES - 0.5, (x - self.x0) / RES - 0.5

    def rc(self, lat, lon):
        r, c = self.rcf(lat, lon)
        return int(round(r)), int(round(c))

    def ll(self, r, c):
        lon, lat = self.inv_t.transform(self.x0 + (c + 0.5) * RES, self.y1 - (r + 0.5) * RES)
        return float(lat), float(lon)

    def ll_array(self, rr, cc):
        lon, lat = self.inv_t.transform(self.x0 + (np.asarray(cc) + 0.5) * RES,
                                        self.y1 - (np.asarray(rr) + 0.5) * RES)
        return np.asarray(lat), np.asarray(lon)

    def inside(self, r, c):
        return 0 <= r < self.nrows and 0 <= c < self.ncols

    def holds(self, p):
        return self.inside(*self.rc(*p))

    def ground_km(self, ra, rb, ca, cb, step=16):
        """The ground length of a cell in km over a window: the stereographic
        scale is (1 + sin lat_ts) / (1 + sin lat), sampled every `step` cells and
        blown up."""
        rr = np.arange(ra, rb, step)
        cc = np.arange(ca, cb, step)
        C, Rw = np.meshgrid(cc, rr)
        lat, _ = self.ll_array(Rw, C)
        k = (1 + math.sin(math.radians(78.0))) / (1 + np.sin(np.radians(lat)))
        g = (RES / 1000.0) / k
        g = np.repeat(np.repeat(g, step, 0), step, 1)[:rb - ra, :cb - ca]
        return g.astype(np.float32)

    # -- building
    def _build(self, meta, meta_p):
        import rasterio
        from rasterio.warp import reproject, Resampling, transform_bounds
        from rasterio.transform import from_origin
        from rasterio.crs import CRS
        t0 = time.time()
        dst_t = from_origin(self.x0, self.y1, RES, RES)
        dst_crs = CRS.from_proj4(PROJ)
        dem = np.lib.format.open_memmap(MOSAIC / "dem.npy", mode="w+", dtype=np.float32,
                                        shape=(self.nrows, self.ncols))
        dem[:] = 0.0
        tiles = sorted(TILES.glob("*.tif"))
        if not tiles:
            raise SystemExit(f"no GLO-90 tiles in {TILES}; run /data/gis/dem/fetch.sh")
        print(f"mosaicking {len(tiles)} tiles into {self.ncols} x {self.nrows} cells at {RES:g} m",
              file=sys.stderr)
        for i, tp in enumerate(tiles):
            with rasterio.open(tp) as src:
                a = src.read(1)
                try:
                    bx = transform_bounds(src.crs, dst_crs, *src.bounds, densify_pts=21)
                except Exception:
                    continue
                ca = max(0, int((bx[0] - self.x0) / RES) - 2)
                cb = min(self.ncols, int((bx[2] - self.x0) / RES) + 3)
                ra = max(0, int((self.y1 - bx[3]) / RES) - 2)
                rb = min(self.nrows, int((self.y1 - bx[1]) / RES) + 3)
                if cb <= ca or rb <= ra:
                    continue
                sub = np.full((rb - ra, cb - ca), -9999.0, np.float32)
                reproject(a, sub, src_transform=src.transform, src_crs=src.crs,
                          dst_transform=from_origin(self.x0 + ca * RES, self.y1 - ra * RES, RES, RES),
                          dst_crs=dst_crs, dst_nodata=-9999.0, resampling=Resampling.average)
                good = sub > -9000
                blk = dem[ra:rb, ca:cb]
                blk[good] = np.maximum(blk[good], sub[good])
                dem[ra:rb, ca:cb] = blk
            if i % 100 == 0:
                print(f"  {i}/{len(tiles)} tiles, {time.time() - t0:.0f} s", file=sys.stderr)
        dem[dem < 0] = 0.0
        dem.flush()
        # slope, in degrees, from the gradient over 250 m
        slope = np.lib.format.open_memmap(MOSAIC / "slope.npy", mode="w+", dtype=np.float32,
                                          shape=(self.nrows, self.ncols))
        step = 2048
        for r in range(0, self.nrows, step):
            a, b = max(0, r - 1), min(self.nrows, r + step + 1)
            blk = np.asarray(dem[a:b]).astype(np.float32)
            gy, gx = np.gradient(blk, RES)
            s = np.degrees(np.arctan(np.hypot(gx, gy)))
            slope[r:min(self.nrows, r + step)] = s[r - a:r - a + min(step, self.nrows - r)]
        slope.flush()
        print(f"slope done, {time.time() - t0:.0f} s", file=sys.stderr)
        # land from GSHHG full resolution, ice from Natural Earth
        import rasterio.features
        for name, zpath, member, url in (
                ("land", GSHHG_ZIP, "GSHHS_shp/f/GSHHS_f_L1.shp", None),
                ("ice", NE_ZIP, "ne_10m_glaciated_areas.shp", NE_URL)):
            if not zpath.exists():
                if url is None:
                    raise SystemExit(f"{zpath} missing: run the sea router once to fetch GSHHG")
                import urllib.request
                zpath.parent.mkdir(parents=True, exist_ok=True)
                urllib.request.urlretrieve(url, zpath)
            shapes = []
            lo0, lo1 = EXTENT["lon"]
            la0, la1 = EXTENT["lat"]
            for box, xy in read_shapefile_polygons(zpath, member):
                if box[2] < lo0 or box[0] > lo1 or box[3] < la0 or box[1] > la1:
                    continue
                keep = xy[(xy[:, 1] > la0 - 2) & (xy[:, 1] < 89.9)] if name == "ice" else xy
                if len(keep) < 4:
                    continue
                x, y = self.fwd_t.transform(xy[:, 0], np.clip(xy[:, 1], -89.9, 89.9))
                shapes.append(({"type": "Polygon", "coordinates": [np.column_stack([x, y]).tolist()]}, 1))
            mask = rasterio.features.rasterize(shapes, out_shape=(self.nrows, self.ncols), fill=0,
                                               dtype="uint8", transform=dst_t, all_touched=False)
            if name == "ice":
                # Natural Earth's glaciated areas are drawn at 10 m and spill
                # over the fiords and sounds they head; ice cannot be where the
                # full-resolution shoreline says sea, so the ice is clipped to
                # the land
                mask &= np.load(MOSAIC / "land.npy", mmap_mode="r")
            np.save(MOSAIC / f"{name}.npy", mask.astype(np.uint8))
            print(f"{name}: {len(shapes)} polygons, {mask.mean():.1%} of the grid, "
                  f"{time.time() - t0:.0f} s", file=sys.stderr)
        del dem, slope
        meta_p.write_text(json.dumps(meta))
        print(f"mosaic built in {time.time() - t0:.0f} s -> {MOSAIC}", file=sys.stderr)

    # -- pictures
    def hillshade(self, ra, rb, ca, cb, az=315.0, alt=45.0):
        z = np.asarray(self.dem[ra:rb, ca:cb]).astype(np.float32)
        gy, gx = np.gradient(z, RES)
        slope = np.arctan(np.hypot(gx, gy) * 1.5)
        aspect = np.arctan2(-gx, gy)
        azr, altr = math.radians(360.0 - az + 90.0), math.radians(alt)
        hs = np.sin(altr) * np.cos(slope) + np.cos(altr) * np.sin(slope) * np.cos(azr - aspect)
        return np.clip(hs, 0, 1)


# --------------------------------------------------------------- georef
def _design2(x, y, quad):
    cols = [np.ones_like(x), x, y]
    if quad:
        cols += [x * y, x * x, y * y]
    return np.column_stack(cols)


class Warp:
    """A smooth correction in pixel space: Gaussian radial functions on a grid
    of knots, fitted by least squares to (pixel, shift) pairs with a weak
    zero-shift observation at every knot, so the warp fades to nothing where
    no coast holds it.  p_out = p + w(p).  Linear in its weights, so it takes
    ten thousand pairs cheaply; the knots are a few hundred pixels apart, so
    lettering and the stray dot cannot bend it locally."""

    def __init__(self, knots, weights=None, scale=250.0):
        self.knots = np.asarray(knots, float)
        self.scale = float(scale)
        self.W = None if weights is None else np.asarray(weights, float)

    @classmethod
    def grid(cls, W, H, spacing):
        xs = np.arange(-spacing, W + 2 * spacing, spacing)
        ys = np.arange(-spacing, H + 2 * spacing, spacing)
        X, Y = np.meshgrid(xs, ys)
        return cls(np.column_stack([X.ravel(), Y.ravel()]), scale=0.9 * spacing)

    def basis(self, p):
        p = np.clip(np.atleast_2d(p), -1e6, 1e6) / self.scale
        k = self.knots / self.scale
        out = np.empty((len(p), len(k)))
        for i in range(0, len(p), 4096):
            r2 = ((p[i:i + 4096, None, :] - k[None, :, :]) ** 2).sum(2)
            out[i:i + 4096] = np.exp(-0.5 * r2)
        return out

    def fit(self, p, shift, w=None, anchor=3.0):
        w = np.ones(len(p)) if w is None else np.asarray(w, float)
        P = np.vstack([p, self.knots])
        S = np.vstack([shift, np.zeros((len(self.knots), 2))])
        ww = np.concatenate([w, np.full(len(self.knots), anchor)])
        B = self.basis(P) * np.sqrt(ww)[:, None]
        self.W, *_ = np.linalg.lstsq(B, S * np.sqrt(ww)[:, None], rcond=None)
        return self

    def __call__(self, p):
        if self.W is None:
            return np.zeros_like(np.atleast_2d(p), dtype=float)
        return self.basis(p) @ self.W

    def to_dict(self):
        return dict(knots=self.knots.tolist(), scale=self.scale, weights=None if self.W is None else self.W.tolist())

    @classmethod
    def from_dict(cls, d):
        return cls(d["knots"], d["weights"], d["scale"])


class Georef:
    """pixel = Q(P(lon, lat)) + w(Q(P)), P a projection from FAMILIES with its
    free parameters fitted, Q an affine (three coefficients per axis) or a full
    quadratic (six per axis) in the projected coordinates scaled by ``scale``,
    and w an optional Warp fitted to the coastline.  Pixel coordinates are in
    the north-up image."""

    def __init__(self, family, params, affine, lon0, scale=1.0, warp=None):
        from pyproj import Proj
        self.family, self.params, self.lon0, self.scale = family, dict(params), lon0, float(scale)
        A = np.array(affine, float)
        self.A = A.reshape(2, -1)
        self.quad = self.A.shape[1] == 6
        self.warp = warp
        self.proj = Proj(self.proj4(family, params, lon0))

    @staticmethod
    def proj4(family, params, lon0):
        p = dict(params)
        if family in ("lcc", "eqdc", "aea"):
            return (f"+proj={family} +lat_1={p['lat1']} +lat_2={p['lat2']} +lat_0={(p['lat1'] + p['lat2']) / 2} "
                    f"+lon_0={lon0} +datum=WGS84 +units=m +no_defs")
        if family == "bonne":
            return f"+proj=bonne +lat_1={p['lat1']} +lon_0={lon0} +datum=WGS84 +units=m +no_defs"
        if family == "poly":
            return f"+proj=poly +lon_0={p['lon0']} +datum=WGS84 +units=m +no_defs"
        if family in ("stere", "laea", "aeqd"):
            return f"+proj={family} +lat_0=90 +lon_0={lon0} +datum=WGS84 +units=m +no_defs"
        if family == "merc":
            return f"+proj=merc +lon_0={lon0} +datum=WGS84 +units=m +no_defs"
        if family == "eqc":
            return f"+proj=eqc +lon_0={lon0} +datum=WGS84 +units=m +no_defs"
        raise ValueError(family)

    def xy(self, lon, lat):
        x, y = self.proj(np.asarray(lon, float), np.asarray(lat, float))
        return np.atleast_1d(x) / self.scale, np.atleast_1d(y) / self.scale

    def xy_to_px(self, x, y, warped=True):
        X = _design2(np.asarray(x, float), np.asarray(y, float), self.quad)
        px, py = X @ self.A[0], X @ self.A[1]
        if warped and self.warp is not None:
            P = np.column_stack([px, py])
            P = P + self.warp(P)
            return P[:, 0], P[:, 1]
        return px, py

    def to_px(self, lon, lat):
        return self.xy_to_px(*self.xy(lon, lat))

    def unwarp(self, px, py):
        """The pixel before the warp: fixed-point iteration, the warp being
        smooth and small next to the page."""
        if self.warp is None:
            return px, py
        P0 = np.column_stack([px, py])
        P = P0.copy()
        for _ in range(20):
            Pn = P0 - self.warp(P)
            if np.abs(Pn - P).max() < 1e-4:
                P = Pn
                break
            P = Pn
        return P[:, 0], P[:, 1]

    def to_ll(self, px, py):
        px, py = np.atleast_1d(px).astype(float), np.atleast_1d(py).astype(float)
        px, py = self.unwarp(px, py)
        M = self.A[:, 1:3]
        Minv = np.linalg.inv(M)
        d = np.column_stack([px - self.A[0, 0], py - self.A[1, 0]])
        xy = d @ Minv.T
        if self.quad:
            # Newton on the quadratic, from the affine's answer; the quadratic
            # terms are small so a few steps are plenty
            for _ in range(12):
                fx, fy = self.xy_to_px(xy[:, 0], xy[:, 1], warped=False)
                r = np.column_stack([fx - px, fy - py])
                x, y = xy[:, 0], xy[:, 1]
                a, b = self.A[0], self.A[1]
                J = np.empty((len(x), 2, 2))
                J[:, 0, 0] = a[1] + a[3] * y + 2 * a[4] * x
                J[:, 0, 1] = a[2] + a[3] * x + 2 * a[5] * y
                J[:, 1, 0] = b[1] + b[3] * y + 2 * b[4] * x
                J[:, 1, 1] = b[2] + b[3] * x + 2 * b[5] * y
                step = np.linalg.solve(J, r[..., None])[..., 0]
                xy = xy - step
                if np.abs(step).max() < 1e-9:
                    break
        lon, lat = self.proj(xy[:, 0] * self.scale, xy[:, 1] * self.scale, inverse=True)
        return np.asarray(lon), np.asarray(lat)

    def km_per_px(self, px, py):
        lon, lat = self.to_ll([px, px + 1], [py, py])
        return gc_km((lat[0], lon[0]), (lat[1], lon[1]))

    def to_dict(self):
        return dict(family=self.family, params=self.params, lon0=self.lon0, scale=self.scale,
                    affine=self.A.ravel().tolist(), warp=self.warp.to_dict() if self.warp else None)

    @classmethod
    def from_dict(cls, d):
        return cls(d["family"], d["params"], d["affine"], d["lon0"], d.get("scale", 1.0),
                   Warp.from_dict(d["warp"]) if d.get("warp") else None)


def _affine_fit(xy, px, py, quad=False, w=None):
    X = _design2(xy[:, 0], xy[:, 1], quad)
    sw = np.sqrt(w) if w is not None else np.ones(len(px))
    a, *_ = np.linalg.lstsq(X * sw[:, None], px * sw, rcond=None)
    b, *_ = np.linalg.lstsq(X * sw[:, None], py * sw, rcond=None)
    res = np.hypot(X @ a - px, X @ b - py)
    return np.concatenate([a, b]), res


XY_SCALE = 1e5      # projected metres are scaled by this before the polynomial, for conditioning


def refine_by_coast(g, img, cps, rounds=(40.0, 30.0, 24.0, 18.0, 14.0, 10.0, 8.0, 6.0, 5.0, 4.0),
                    warp_spacing=250.0):
    """Iterative closest point between the GSHHG shoreline projected through the
    model and the map's ink: every round projects the coast, pairs each sample
    with the nearest ink pixel within a shrinking radius, and refits the
    polynomial (affine, then quadratic once the pairs are close) to the pairs
    and the control points together, the control points weighted as fifty
    coast samples each.  Returns the refined model and a report: the median
    distance of the coast samples from the ink and the share within three
    pixels, which is the map's precision along its coasts."""
    W, H = img.size
    grey = np.asarray(img.convert("L"))
    ink = grey < 120
    dist, (ir, ic) = ndimage.distance_transform_edt(~ink, return_indices=True)
    lon, lat = g.to_ll(np.array([0, W, 0, W, W / 2]), np.array([0, 0, H, H, H / 2]))
    box = (float(np.nanmin(lat)) - 1, float(np.nanmin(lon)) - 3, min(89.5, float(np.nanmax(lat)) + 1),
           float(np.nanmax(lon)) + 3)
    km = g.km_per_px(W / 2, H / 2)
    step_km = max(1.0, 1.5 * km)
    samples = []
    for ring in coast_rings(box):
        if len(ring) < 20:
            continue
        # resample the ring every step_km on the ground
        dlat = np.diff(ring[:, 1]) * 111.0
        dlon = np.diff(ring[:, 0]) * 111.0 * np.cos(np.radians(ring[:-1, 1]))
        s = np.concatenate([[0.0], np.cumsum(np.hypot(dlat, dlon))])
        if s[-1] < 3 * step_km:
            continue
        t = np.arange(0.0, s[-1], step_km)
        samples.append(np.column_stack([np.interp(t, s, ring[:, 0]), np.interp(t, s, ring[:, 1])]))
    S = np.vstack(samples)
    if len(S) > 60000:
        S = S[np.random.RandomState(0).choice(len(S), 60000, replace=False)]
    sx, sy = g.xy(S[:, 0], S[:, 1])
    cx, cy = g.xy(np.array([c["lon"] for c in cps]), np.array([c["lat"] for c in cps]))
    cpx, cpy = np.array([c["px"] for c in cps], float), np.array([c["py"] for c in cps], float)
    A = g.A.ravel()
    warp = None
    cp_w = 50.0

    def matched(gk, R):
        px, py = gk.xy_to_px(sx, sy)
        inside = (px >= 0) & (px < W - 1) & (py >= 0) & (py < H - 1)
        pi, pj = np.clip(py, 0, H - 1).astype(int), np.clip(px, 0, W - 1).astype(int)
        d = np.where(inside, dist[pi, pj], np.inf)
        ok = d < R
        return ok, ic[pi[ok], pj[ok]].astype(float), ir[pi[ok], pj[ok]].astype(float), px, py

    for k, R in enumerate(rounds):
        gk = Georef(g.family, g.params, A, g.lon0, g.scale, warp)
        ok, tx, ty, px, py = matched(gk, R)
        if ok.sum() < 50:
            break
        if k < 2 or warp_spacing is None:
            # the affine again, on the pairs and the control points together
            w = np.concatenate([np.ones(ok.sum()), np.full(len(cps), cp_w)])
            X = np.column_stack([np.concatenate([sx[ok], cx]), np.concatenate([sy[ok], cy])])
            A, res = _affine_fit(X, np.concatenate([tx, cpx]), np.concatenate([ty, cpy]), False, w)
            w2 = w / np.maximum(1.0, res / 3.0)      # a sample matched to lettering counts less
            A, res = _affine_fit(X, np.concatenate([tx, cpx]), np.concatenate([ty, cpy]), False, w2)
            warp = None
        else:
            # the warp: from the affine's pixel to the matched ink, on the knots
            base = Georef(g.family, g.params, A, g.lon0, g.scale, None)
            bx, by = base.xy_to_px(sx[ok], sy[ok])
            bcx, bcy = base.xy_to_px(cx, cy)
            P = np.column_stack([np.concatenate([bx, bcx]), np.concatenate([by, bcy])])
            shift = np.column_stack([np.concatenate([tx, cpx]), np.concatenate([ty, cpy])]) - P
            w = np.concatenate([np.ones(ok.sum()), np.full(len(cps), cp_w)])
            warp = Warp.grid(W, H, warp_spacing).fit(P, shift, w)
            r = np.hypot(*(warp(P) - shift).T)
            w2 = w / np.maximum(1.0, r / 3.0)
            warp = Warp.grid(W, H, warp_spacing).fit(P, shift, w2)
    def measure(gk):
        # measured within the control points' box, which spans the map's frame:
        # the shoreline outside the frame has nothing to match
        px, py = gk.xy_to_px(sx, sy)
        x0, x1 = cpx.min(), cpx.max()
        y0, y1 = cpy.min(), cpy.max()
        mx, my = 0.1 * (x1 - x0), 0.1 * (y1 - y0)
        inside = ((px >= max(0, x0 - mx)) & (px < min(W - 1, x1 + mx))
                  & (py >= max(0, y0 - my)) & (py < min(H - 1, y1 + my)))
        pi, pj = np.clip(py, 0, H - 1).astype(int), np.clip(px, 0, W - 1).astype(int)
        d = dist[pi, pj][inside]
        if not len(d):
            return dict(coast_samples=0, coast_median_px=math.inf, coast_within_3px=0.0, coast_within_6px=0.0)
        return dict(coast_samples=int(inside.sum()), coast_median_px=float(np.median(d)),
                    coast_within_3px=float((d <= 3).mean()), coast_within_6px=float((d <= 6).mean()))

    gk = Georef(g.family, g.params, A, g.lon0, g.scale, warp)
    before, after = measure(g), measure(gk)
    # the refinement is kept only when it matches the coast better: a surveyed
    # chart fitted to a pixel or two by its graticule needs no warp
    if after["coast_median_px"] <= before["coast_median_px"]:
        rep = dict(after, coast_median_px_before=before["coast_median_px"],
                   warp_spacing_px=warp_spacing if warp is not None else None, refined=True)
        return gk, rep
    rep = dict(before, coast_median_px_before=before["coast_median_px"], warp_spacing_px=None, refined=False)
    return g, rep


def fit_georef(cps, families=FAMILIES):
    """Fit every family to the control points; return them all, best first, as
    (rms_px, max_px, Georef, residuals)."""
    from pyproj import Proj
    from scipy.optimize import least_squares
    lon = np.array([c["lon"] for c in cps], float)
    lat = np.array([c["lat"] for c in cps], float)
    px = np.array([c["px"] for c in cps], float)
    py = np.array([c["py"] for c in cps], float)
    lon0 = float(np.round(np.median(lon)))
    out = []
    for fam in families:
        def solve(params):
            try:
                p = Proj(Georef.proj4(fam, params, lon0))
                x, y = p(lon, lat)
            except Exception:
                return None, None
            if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
                return None, None
            aff, res = _affine_fit(np.column_stack([x, y]) / XY_SCALE, px, py)
            return aff, res

        if fam in ("lcc", "eqdc", "aea"):
            free = ["lat1", "lat2"]
            x0 = [max(45.0, lat.min() - 2), min(89.0, lat.max() + 2)]
            lo, hi = [30.0, 30.0], [89.5, 89.9]
        elif fam == "bonne":
            free, x0, lo, hi = ["lat1"], [float(np.mean(lat))], [30.0], [89.9]
        elif fam == "poly":
            free, x0, lo, hi = ["lon0"], [lon0], [lon0 - 60], [lon0 + 60]
        else:
            free, x0, lo, hi = [], [], [], []
        if free:
            def f(v):
                aff, res = solve(dict(zip(free, v)))
                return res if res is not None else np.full(len(px), 1e6)
            best = None
            starts = [x0]
            if len(free) == 2:
                starts += [[60.0, 80.0], [70.0, 85.0], [75.0, 82.0], [50.0, 85.0]]
            for s in starts:
                try:
                    r = least_squares(f, s, bounds=(lo, hi), diff_step=1e-3)
                except Exception:
                    continue
                if best is None or r.cost < best.cost:
                    best = r
            if best is None:
                continue
            params = dict(zip(free, [float(v) for v in best.x]))
            if len(free) == 2 and params["lat1"] > params["lat2"]:
                params["lat1"], params["lat2"] = params["lat2"], params["lat1"]
        else:
            params = {}
        aff, res = solve(params)
        if res is None:
            continue
        g = Georef(fam, params, aff, lon0, XY_SCALE)
        out.append((float(np.sqrt((res ** 2).mean())), float(res.max()), g, res))
    out.sort(key=lambda t: t[0])
    return out


def load_image(map_id, rotate=None):
    """The map's raster, north-up, as an RGB PIL image, and the row it came from."""
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    row = read_row(map_id)
    if row is None:
        raise SystemExit(f"no artifact {map_id}")
    f = row["view_file"] or row["local_file"]
    if not f:
        raise SystemExit(f"{map_id} has no raster file")
    img = Image.open(FILES / f).convert("RGB")
    k = MAPS.get(map_id, {}).get("rotate", 0) if rotate is None else rotate
    cp = GEOREF / f"{map_id}.cp.json"
    if rotate is None and cp.exists():
        k = json.loads(cp.read_text()).get("rotate", k)
    if k % 4:
        img = img.rotate(90 * (k % 4), expand=True)
    return img, row


def crops_sheet(map_id, step=100, tile=600, scale=1.5, rotate=None):
    """A sheet of the whole map cut into tiles, each enlarged with a pixel ruler
    every `step` pixels, so that graticule intersections and named places can be
    read off with their pixel coordinates."""
    from PIL import Image, ImageDraw
    img, _ = load_image(map_id, rotate)
    W, H = img.size
    font = _font(14)
    tiles = []
    for y0 in range(0, H, tile):
        for x0 in range(0, W, tile):
            x1, y1 = min(W, x0 + tile), min(H, y0 + tile)
            t = img.crop((x0, y0, x1, y1)).resize((int((x1 - x0) * scale), int((y1 - y0) * scale)), Image.LANCZOS)
            d = ImageDraw.Draw(t)
            for gx in range((x0 + step - 1) // step * step, x1, step):
                X = (gx - x0) * scale
                d.line([(X, 0), (X, t.height)], fill=(0, 170, 0), width=1)
                d.text((X + 2, 2), str(gx), fill=(0, 120, 0), font=font)
            for gy in range((y0 + step - 1) // step * step, y1, step):
                Y = (gy - y0) * scale
                d.line([(0, Y), (t.width, Y)], fill=(0, 170, 0), width=1)
                d.text((2, Y + 1), str(gy), fill=(0, 120, 0), font=font)
            tiles.append((x0, y0, t))
    GEOREF.mkdir(parents=True, exist_ok=True)
    paths = []
    for x0, y0, t in tiles:
        p = GEOREF / f"{map_id}.crop-{x0}-{y0}.png"
        t.save(p)
        paths.append(p)
    return paths, (W, H)


def read_cps(map_id, places):
    p = GEOREF / f"{map_id}.cp.json"
    if not p.exists():
        raise SystemExit(f"no control points at {p}; run crops and read them off")
    d = json.loads(p.read_text())
    out = []
    for c in d["points"]:
        c = dict(c)
        if "place" in c and ("lon" not in c or "lat" not in c):
            hit = places.get(c["place"].lower())
            if hit is None:
                print(f"  control point {c['place']!r}: not in the places table, skipped", file=sys.stderr)
                continue
            c["lat"], c["lon"] = hit
        c["kind"] = "place" if "place" in c else "graticule"
        out.append(c)
    return out, d.get("rotate", MAPS.get(map_id, {}).get("rotate", 0))


def georef_map(map_id, family=None, no_coast=False):
    """Fit the map, save the model and draw the check figure.  Returns the model
    or None when the fit is refused."""
    places = read_places()
    cps, rotate = read_cps(map_id, places)
    if len(cps) < 4:
        raise SystemExit(f"{map_id}: {len(cps)} control points; four is the least a fit needs")
    fits = fit_georef(cps, (family,) if family else FAMILIES)
    if not fits:
        raise SystemExit(f"{map_id}: no family fitted")
    rms0, mx0, g0, res0 = fits[0]
    img, _ = load_image(map_id, rotate)
    km = g0.km_per_px(*np.mean([[c["px"], c["py"]] for c in cps], axis=0))
    print(f"{map_id}: {g0.family} {g0.params}, {len(cps)} points, rms {rms0:.2f} px ({rms0 * km:.1f} km), "
          f"worst {mx0:.2f} px, {km:.2f} km/px, before the coast refinement", file=sys.stderr)
    coast = {}
    g = g0
    if not no_coast:
        g, coast = refine_by_coast(g0, img, cps)
    px, py = g.to_px([c["lon"] for c in cps], [c["lat"] for c in cps])
    res = np.hypot(px - np.array([c["px"] for c in cps]), py - np.array([c["py"] for c in cps]))
    rms, mx = float(np.sqrt((res ** 2).mean())), float(res.max())
    by_points = rms <= FIT_RMS_PX and mx <= FIT_MAX_PX
    by_coast = (bool(coast) and coast["coast_median_px"] <= COAST_MEDIAN_PX
                and coast["coast_within_6px"] >= COAST_WITHIN_6 and coast["coast_median_px"] * km <= COAST_MEDIAN_KM)
    report = dict(map=map_id, rotate=rotate, n=len(cps), family=g.family, params=g.params, lon0=g.lon0,
                  scale=g.scale, affine=g.A.ravel().tolist(), quadratic=g.quad,
                  warp=g.warp.to_dict() if g.warp is not None else None,
                  rms_px=rms, max_px=mx, km_per_px=km, rms_km=rms * km, max_km=mx * km,
                  rms_px_before_coast=rms0, max_px_before_coast=mx0,
                  accepted=bool(by_points or by_coast),
                  accepted_by="control points" if by_points else ("the coastline" if by_coast else ""),
                  families=[dict(family=f[2].family, rms_px=f[0], max_px=f[1], params=f[2].params) for f in fits],
                  points=[dict(c, res_px=float(r), res_km=float(r) * km) for c, r in zip(cps, res)], **coast)
    GEOREF.mkdir(parents=True, exist_ok=True)
    (GEOREF / f"{map_id}.georef.json").write_text(json.dumps(report, indent=1))
    print(f"{map_id}: after: control points rms {rms:.2f} px ({rms * km:.1f} km), worst {mx:.2f} px"
          + (f"; coast median {coast['coast_median_px']:.1f} px ({coast['coast_median_px'] * km:.1f} km), "
             f"{coast['coast_within_3px']:.0%} within 3 px, {coast['coast_within_6px']:.0%} within 6 px, "
             f"{coast['coast_samples']} samples" if coast else "")
          + f" -> {'accepted by ' + report['accepted_by'] if report['accepted'] else 'REFUSED'}", file=sys.stderr)
    for c, r in sorted(zip(cps, res), key=lambda t: -t[1])[:3]:
        print(f"    {c.get('place') or c.get('name') or (str(c['lon']) + ' ' + str(c['lat']))}: {r:.1f} px",
              file=sys.stderr)
    georef_figure(map_id, g, cps, res, report)
    return g if report["accepted"] else None


def load_georef(map_id):
    p = GEOREF / f"{map_id}.georef.json"
    if not p.exists():
        return None, None
    d = json.loads(p.read_text())
    return (Georef.from_dict(d) if d.get("accepted") else None), d


def coast_rings(box):
    """GSHHG full-resolution rings within a (s, w, n, e) box."""
    s, w, n, e = box
    rings = []
    for bx, xy in read_shapefile_polygons(GSHHG_ZIP, "GSHHS_shp/f/GSHHS_f_L1.shp"):
        if bx[2] < w or bx[0] > e or bx[3] < s or bx[1] > n:
            continue
        rings.append(xy)
    return rings


def georef_figure(map_id, g, cps, res, report):
    """The shoreline projected through the model over the scan, with the control
    points and their residuals: the fit's own check."""
    from PIL import Image, ImageDraw
    img, _ = load_image(map_id, report["rotate"])
    W, H = img.size
    lon, lat = g.to_ll(np.array([0, W, 0, W, W / 2]), np.array([0, 0, H, H, H / 2]))
    box = (float(np.nanmin(lat)) - 1, float(np.nanmin(lon)) - 3, min(89.5, float(np.nanmax(lat)) + 1),
           float(np.nanmax(lon)) + 3)
    img = Image.blend(img, Image.new("RGB", img.size, (255, 255, 255)), 0.35)
    d = ImageDraw.Draw(img)
    for ring in coast_rings(box):
        step = max(1, len(ring) // 4000)
        r = ring[::step]
        px, py = g.to_px(r[:, 0], r[:, 1])
        pts = [(float(x), float(y)) for x, y in zip(px, py) if np.isfinite(x) and np.isfinite(y)]
        if len(pts) > 1:
            d.line(pts, fill=(30, 110, 220), width=2)
    for lo in range(-180, 180, 10):
        la = np.linspace(60, 89.5, 120)
        px, py = g.to_px(np.full_like(la, lo), la)
        d.line(list(zip(px, py)), fill=(200, 120, 0), width=1)
    for la in range(60, 90, 2):
        lo = np.linspace(-180, 180, 721)
        px, py = g.to_px(lo, np.full_like(lo, la))
        d.line(list(zip(px, py)), fill=(200, 120, 0), width=1)
    f = _font(18)
    for c, r in zip(cps, res):
        x, y = c["px"], c["py"]
        px, py = g.to_px(c["lon"], c["lat"])
        d.ellipse([x - 6, y - 6, x + 6, y + 6], outline=(220, 0, 0), width=2)
        d.line([(x, y), (float(px[0]), float(py[0]))], fill=(220, 0, 0), width=2)
        d.text((x + 8, y - 8), f"{c.get('place') or ''} {r:.1f}px", fill=(160, 0, 0), font=f)
    d.rectangle([0, 0, W, 34], fill=(255, 255, 255))
    coast = (f", coast median {report['coast_median_px']:.1f} px with {report['coast_within_6px']:.0%} within 6"
             if "coast_median_px" in report else "")
    d.text((8, 6), f"{map_id}: {g.family} {g.params}, {report['n']} points, rms {report['rms_px']:.1f} px = "
                   f"{report['rms_km']:.1f} km, worst {report['max_px']:.1f} px{coast}; blue GSHHG shoreline through "
                   f"the model, orange graticule every 10 deg / 2 deg, red control points -> "
                   f"{'ACCEPTED by ' + report['accepted_by'] if report['accepted'] else 'REFUSED'}",
           fill=(0, 0, 0), font=f)
    FIGS.mkdir(parents=True, exist_ok=True)
    if W > 2600:
        img = img.resize((2600, int(H * 2600 / W)), Image.LANCZOS)
    img.save(FIGS / f"{map_id}-georef.png")


# ------------------------------------------------------------ extraction
def ink_mask(img, ink):
    """Boolean array of the route's ink.  ``ink`` is dots, dashes, solid or
    colour:<name>."""
    a = np.asarray(img).astype(np.int16)
    if ink.startswith("colour:"):
        name = ink.split(":", 1)[1]
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        if name == "red":
            return (r > 120) & (r - g > 50) & (r - b > 50)
        if name == "blue":
            return (b > 110) & (b - r > 40) & (b - g > 20)
        if name == "green":
            return (g > 90) & (g - r > 30) & (g - b > 20)
        raise SystemExit(f"unknown colour {name}")
    # black ink only: a coloured map's blue coast and green land are not the
    # route, and on a greyscale scan the test is the same as a threshold
    grey = a.mean(axis=2)
    spread = a.max(axis=2) - a.min(axis=2)
    return (grey < 120) & (spread < 60)


def fragments(mask, ink):
    """Centroids of the ink fragments that are a dot's or a dash's size, and for
    a solid line the skeleton pixels every third one."""
    if ink == "solid" or ink.startswith("colour:"):
        from skimage.morphology import skeletonize
        sk = skeletonize(mask)
        rr, cc = np.nonzero(sk)
        return np.column_stack([cc, rr]).astype(float)[::2]
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    if n == 0:
        return np.zeros((0, 2))
    idx = np.arange(1, n + 1)
    area = ndimage.sum_labels(np.ones_like(mask, np.uint8), lab, idx)
    objs = ndimage.find_objects(lab)
    lo, hi = DOT_AREA if ink == "dots" else DASH_AREA
    size = DOT_SIZE if ink == "dots" else DASH_SIZE
    keep = []
    for i, sl in enumerate(objs):
        if sl is None:
            continue
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        if lo <= area[i] <= hi and max(h, w) <= size:
            keep.append(i + 1)
    if not keep:
        return np.zeros((0, 2))
    cen = ndimage.center_of_mass(mask, lab, keep)
    return np.array([(c, r) for r, c in cen], float)


def chain_leg(nodes, a, b, spacing):
    """The cheapest path through the fragment cloud from pixel a to pixel b:
    a graph whose edges join fragments within a few spacings, weighted d^1.6,
    so a run of dots is cheaper than a jump across a gap.  Returns the ordered
    pixels, a and b included, or None."""
    from scipy.spatial import cKDTree
    P = np.vstack([nodes, [a], [b]]) if len(nodes) else np.array([a, b], float)
    n = len(P)
    ia, ib = n - 2, n - 1
    tree = cKDTree(P)
    for R in (4 * spacing, 8 * spacing, 16 * spacing, 40 * spacing):
        pairs = tree.query_pairs(R, output_type="ndarray")
        if len(pairs) == 0:
            continue
        d = np.hypot(*(P[pairs[:, 0]] - P[pairs[:, 1]]).T)
        w = np.maximum(d, 0.5) ** HOP_POWER
        G = coo_matrix((np.concatenate([w, w]), (np.concatenate([pairs[:, 0], pairs[:, 1]]),
                                                 np.concatenate([pairs[:, 1], pairs[:, 0]]))), shape=(n, n)).tocsr()
        dist, pred = dijkstra(G, indices=ia, return_predecessors=True)
        if np.isfinite(dist[ib]):
            path, k = [], ib
            while k != ia and k >= 0:
                path.append(k)
                k = pred[k]
            path.append(ia)
            path.reverse()
            return P[path], R
    return None, None


def digitize_track(map_id, track_id, terrain=None, ink=None):
    """Extract the track's drawn route from the map; write the digitized
    GeoJSON and return (legs, report)."""
    g, rep = load_georef(map_id)
    if g is None:
        raise SystemExit(f"{map_id}: no accepted georeference; run georef first")
    row = read_row(track_id)
    if row is None:
        raise SystemExit(f"no track {track_id}")
    moves = load_moves(track_id)
    wps = [(float(w["lat"]), float(w["lon"])) for w in apply_moves(waypoints_raw(row), moves)]
    img, _ = load_image(map_id, rep["rotate"])
    spec = MAPS.get(map_id, {})
    ink = ink or spec.get("tracks", {}).get(track_id) or spec.get("ink", "dashes")
    mask = ink_mask(img, ink)
    if ink == "solid" or ink.startswith("colour:") or spec.get("erase_coast"):
        # erase the shoreline through the model, so the coast is not the route
        # (a solid route would be chained along it; a stippled coast is dots)
        from PIL import Image, ImageDraw
        W, H = img.size
        lon, lat = g.to_ll(np.array([0, W, 0, W]), np.array([0, 0, H, H]))
        box = (float(np.nanmin(lat)) - 1, float(np.nanmin(lon)) - 3, min(89.5, float(np.nanmax(lat)) + 1),
               float(np.nanmax(lon)) + 3)
        cm = Image.new("L", img.size, 0)
        d = ImageDraw.Draw(cm)
        for ring in coast_rings(box):
            px, py = g.to_px(ring[:, 0], ring[:, 1])
            pts = [(float(x), float(y)) for x, y in zip(px, py) if np.isfinite(x)]
            if len(pts) > 1:
                d.line(pts, fill=255, width=int(2 * max(3.0, rep["rms_px"])) + 3)
        mask &= np.asarray(cm) == 0
    frags = fragments(mask, ink)
    km = rep["km_per_px"]
    wpx = np.column_stack(g.to_px([p[1] for p in wps], [p[0] for p in wps]))
    corr = CORRIDOR_KM / km
    if len(frags):
        from scipy.spatial import cKDTree
        dd, _ = cKDTree(frags).query(frags, k=2)
        spacing = float(np.median(dd[:, 1]))
    else:
        spacing = 5.0
    spacing = max(spacing, 3.0)
    legs, report = [], []
    for i in range(len(wps) - 1):
        a, b = wpx[i], wpx[i + 1]
        ab = b - a
        L2 = float(ab @ ab)
        if L2 < 1:
            legs.append(dict(source="zero", ll=[wps[i], wps[i + 1]], px=[a.tolist(), b.tolist()]))
            report.append((i, "zero", 0))
            continue
        if len(frags):
            t = ((frags - a) @ ab) / L2
            proj = a + np.outer(t, ab)
            perp = np.hypot(*(frags - proj).T)
            near = frags[(t > -0.2) & (t < 1.2) & (perp < corr)]
        else:
            near = frags
        path, R = chain_leg(near, a, b, spacing) if len(near) else (None, None)
        if path is None or len(path) < 3:
            legs.append(dict(source="straight", ll=great_circle(wps[i], wps[i + 1]), px=[a.tolist(), b.tolist()]))
            report.append((i, "straight", 0))
            continue
        # drop the jump from the waypoint onto the ink when it is long: the
        # waypoint is approximate and the ink is the line
        keep = simplify_xy(path, 1.0 / km)
        p2 = path[keep]
        lon, lat = g.to_ll(p2[:, 0], p2[:, 1])
        ll = [wps[i]] + [(float(la), float(lo)) for la, lo in zip(lat[1:-1], lon[1:-1])] + [wps[i + 1]]
        # a chain much longer than the leg is hachures or lettering, not the
        # route: kept for the picture, doubted for the routing
        straight = gc_km(wps[i], wps[i + 1])
        source = "ink" if line_km(ll) <= DOUBT_FACTOR * straight + DOUBT_KM else "ink-doubtful"
        legs.append(dict(source=source, ll=ll, px=p2.tolist()))
        report.append((i, source, len(p2)))
    DIGIT.mkdir(parents=True, exist_ok=True)
    fc = {"type": "FeatureCollection", "map": map_id, "track": track_id, "ink": ink,
          "km_per_px": km, "fragments": int(len(frags)), "spacing_px": spacing,
          "features": [{"type": "Feature", "properties": {"leg": i, "source": lg["source"], "px": lg["px"]},
                        "geometry": {"type": "LineString",
                                     "coordinates": [[round(lo, 5), round(la, 5)] for la, lo in lg["ll"]]}}
                       for i, lg in enumerate(legs)]}
    (DIGIT / f"{track_id}.geojson").write_text(json.dumps(fc))
    n_ink = sum(1 for lg in legs if lg["source"] == "ink")
    n_doubt = sum(1 for lg in legs if lg["source"] == "ink-doubtful")
    print(f"{track_id} on {map_id}: {len(frags)} fragments ({ink}, spacing {spacing:.1f} px), "
          f"{n_ink} of {len(legs)} legs from ink, {n_doubt} doubted", file=sys.stderr)
    return legs, fc


def load_digitized(track_id):
    p = DIGIT / f"{track_id}.geojson"
    if not p.exists():
        return None
    fc = json.loads(p.read_text())
    legs = []
    for f in fc["features"]:
        legs.append(dict(source=f["properties"]["source"], px=f["properties"].get("px"),
                         ll=[(float(la), float(lo)) for lo, la in f["geometry"]["coordinates"]]))
    fc["legs"] = legs
    return fc


# --------------------------------------------------------------- routing
def leg_dates(row, wps_raw):
    """A date (year, month) for every leg: the waypoint's own where it has one,
    else interpolated between the dated neighbours, the track's dates at the ends."""
    n = len(wps_raw)
    ords = [None] * n
    import datetime as dt

    def parse(s):
        s = (s or "").strip()[:10]
        for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
            try:
                return dt.datetime.strptime(s, fmt).toordinal()
            except ValueError:
                continue
        return None
    for i, w in enumerate(wps_raw):
        ords[i] = parse(w.get("date"))
    if ords[0] is None:
        ords[0] = parse(row["date_start"])
    if ords[-1] is None:
        ords[-1] = parse(row["date_end"]) or ords[0]
    known = [i for i, o in enumerate(ords) if o is not None]
    if not known:
        return [(None, 4)] * max(1, n - 1)
    out = []
    for i in range(n):
        if ords[i] is None:
            lo = max([k for k in known if k < i], default=None)
            hi = min([k for k in known if k > i], default=None)
            if lo is None:
                ords[i] = ords[hi]
            elif hi is None:
                ords[i] = ords[lo]
            else:
                ords[i] = ords[lo] + (ords[hi] - ords[lo]) * (i - lo) / (hi - lo)
    for i in range(n - 1):
        m = dt.date.fromordinal(int((ords[i] + ords[i + 1]) / 2))
        out.append((m.year, m.month))
    return out


def ice_allowed(row, wps_raw, i):
    """The ice cap is cheap on a leg whose waypoint notes name it; when no note
    does but the description or the tags do, on every leg."""
    notes = " ".join([(wps_raw[i].get("note") or ""), (wps_raw[i + 1].get("note") or "")]).lower()
    if any(w in notes for w in ICE_WORDS + CROSS_WORDS):
        return True
    if any(any(w in (wp.get("note") or "").lower() for w in ICE_WORDS) for wp in wps_raw):
        return False
    text = " ".join([row["description"] or "", row["tags"] or ""]).lower()
    return any(w in text for w in ICE_WORDS + ("ice-cap",))


class Router:
    def __init__(self, terrain):
        self.T = terrain

    def cost_window(self, ra, rb, ca, cb, month, ends_in_sea, ice_ok, corridor_px=None, down=1,
                    straight_px=None):
        T = self.T
        dem = np.asarray(T.dem[ra:rb, ca:cb]).astype(np.float32)
        slope = np.asarray(T.slope[ra:rb, ca:cb]).astype(np.float32)
        land = np.asarray(T.land[ra:rb, ca:cb]).astype(bool)
        ice = np.asarray(T.ice[ra:rb, ca:cb]).astype(bool)
        g = T.ground_km(ra, rb, ca, cb)
        tan = np.tan(np.radians(slope))
        m = LAND_BASE * np.minimum(SLOPE_CAP, 1.0 + SLOPE_W * (tan / SLOPE_S) ** 2) \
            * (1.0 + np.maximum(0.0, dem - ELEV_FLOOR) / ELEV_S)
        if ice_ok:
            # an ice cap the narrative says was crossed: smooth going, so the
            # slope alone, no elevation term
            m_ice = LAND_BASE * ICE_CROSSED * np.minimum(SLOPE_CAP, 1.0 + SLOPE_W * (tan / SLOPE_S) ** 2)
            m = np.where(ice & land, m_ice, m)
        else:
            m = np.where(ice & land, m * ICE_DEAR, m)
        sea = self.sea_multiplier(month, ends_in_sea)
        m = np.where(land, m, sea).astype(np.float32)
        if corridor_px is not None:
            dkm = corridor_px * (RES / 1000.0)
            m *= (1.0 + CORR_W * np.minimum(1.0, (dkm / CORR_KM) ** 2)).astype(np.float32)
        elif straight_px is not None:
            # no ink holds this leg: break the flat-ice tie toward the great circle
            dkm = straight_px * (RES / 1000.0)
            m *= (1.0 + STRAIGHT_W * np.minimum(1.0, dkm / STRAIGHT_KM)).astype(np.float32)
        return (m * g).astype(np.float32)

    def sea_multiplier(self, month, ends_in_sea):
        if month in SLEDGE_MONTHS or month is None:
            return SEA_ICE
        if ends_in_sea == 2:
            return SEA_BOAT
        return SEA_MIXED if ends_in_sea == 1 else SEA_SUMMER

    def corridor_distance(self, ra, rb, ca, cb, line_ll):
        """Distance in cells from every cell of the window to the digitized line."""
        seed = np.zeros((rb - ra, cb - ca), bool)
        pts = np.array([self.T.rcf(*p) for p in line_ll])
        # densify in the grid plane
        for (r0, c0), (r1, c1) in zip(pts, pts[1:]):
            n = int(max(abs(r1 - r0), abs(c1 - c0))) + 1
            rr = np.rint(np.linspace(r0, r1, n + 1)).astype(int) - ra
            cc = np.rint(np.linspace(c0, c1, n + 1)).astype(int) - ca
            ok = (rr >= 0) & (rr < seed.shape[0]) & (cc >= 0) & (cc < seed.shape[1])
            seed[rr[ok], cc[ok]] = True
        if not seed.any():
            return None
        return ndimage.distance_transform_edt(~seed).astype(np.float32)

    def shore_cell(self, p):
        """The nearest sea cell to a waypoint within SHORE_KM, or None.  A
        waypoint plotted to a tenth of a degree whose note names a sound or a
        fiord often lands a few kilometres inland of the shoreline; this is
        where the water it names actually is."""
        T = self.T
        r, c = T.rc(*p)
        if not T.inside(r, c) or not T.land[r, c]:
            return None
        k = int(SHORE_KM * 1000.0 / RES)
        ra, rb = max(0, r - k), min(T.nrows, r + k + 1)
        ca, cb = max(0, c - k), min(T.ncols, c + k + 1)
        sea = ~np.asarray(T.land[ra:rb, ca:cb]).astype(bool)
        if not sea.any():
            return None
        rr, cc = np.nonzero(sea)
        d = np.hypot(rr - (r - ra), cc - (c - ca))
        i = int(np.argmin(d))
        if d[i] > k:
            return None
        return int(rr[i] + ra), int(cc[i] + ca)

    def sea_leg(self, p, q):
        """A leg with an end outside the DEM: the sea router's water path, on its
        fine mask when both ends lie in it, else its coarse one, else a great
        circle.  Flagged as a fallback either way: it is not a terrain route."""
        try:
            rt, fine, coarse = _sea_grids()
        except Exception as e:
            print(f"sea router unavailable ({e}); great circle", file=sys.stderr)
            return great_circle(p, q), dict(fallback="outside the DEM")
        for g in (fine, coarse):
            if g.holds(p) and g.holds(q):
                pts, crossed = g.route(p, q)
                if g is fine and crossed > rt.CROSS_TOL_KM and coarse.holds(p) and coarse.holds(q):
                    pts2, crossed2 = coarse.route(p, q)
                    if crossed2 < crossed:
                        pts, crossed, g = pts2, crossed2, coarse
                return [tuple(x) for x in pts], dict(fallback="outside the DEM", sea_router=g.name,
                                                     crossed_km=round(float(crossed), 1))
        return great_circle(p, q), dict(fallback="outside the DEM")

    def route_leg(self, p, q, month, ice_ok, corridor_ll=None, boat=False, shore=(None, None)):
        T = self.T
        r0, c0 = T.rc(*p)
        r1, c1 = T.rc(*q)
        if not (T.inside(r0, c0) and T.inside(r1, c1)):
            return self.sea_leg(p, q)
        if (r0, c0) == (r1, c1):
            return [p, q], dict(fallback="same cell")
        L = math.hypot(r1 - r0, c1 - c0) * RES / 1000.0
        m = int(max(WINDOW_MARGIN_KM, WINDOW_MARGIN_FRAC * L) * 1000.0 / RES)
        ra, rb = max(0, min(r0, r1) - m), min(T.nrows, max(r0, r1) + m + 1)
        ca, cb = max(0, min(c0, c1) - m), min(T.ncols, max(c0, c1) + m + 1)
        ends_in_sea = int(not T.land[r0, c0] or shore[0] is not None) + \
            int(not T.land[r1, c1] or shore[1] is not None)
        if boat:
            ends_in_sea = 2          # the narrative names a boat: water is cheap whatever the month
        cd = self.corridor_distance(ra, rb, ca, cb, corridor_ll) if corridor_ll else None
        sd = None if cd is not None else self.corridor_distance(ra, rb, ca, cb,
                                                                great_circle(p, q, step_km=10.0))
        cost = self.cost_window(ra, rb, ca, cb, month, ends_in_sea, ice_ok, cd, straight_px=sd)
        # cut the shore open: a channel at the sea-ice cost from a waypoint the
        # mask puts on land to the water its note names
        shore_km = 0.0
        for end, cell in zip(((r0, c0), (r1, c1)), shore):
            if cell is None:
                continue
            n = int(max(abs(cell[0] - end[0]), abs(cell[1] - end[1]))) + 1
            rr = np.rint(np.linspace(end[0], cell[0], n + 1)).astype(int) - ra
            cc = np.rint(np.linspace(end[1], cell[1], n + 1)).astype(int) - ca
            ok = (rr >= 0) & (rr < cost.shape[0]) & (cc >= 0) & (cc < cost.shape[1])
            gg = T.ground_km(ra, rb, ca, cb)
            cost[rr[ok], cc[ok]] = (self.sea_multiplier(month, ends_in_sea) * gg[rr[ok], cc[ok]]).astype(np.float32)
            shore_km = max(shore_km, math.hypot(cell[0] - end[0], cell[1] - end[1]) * RES / 1000.0)
        info = dict(window=[rb - ra, cb - ca], ends_in_sea=ends_in_sea, month=month, ice_ok=ice_ok,
                    corridor=cd is not None)
        if shore_km:
            info["shore_km"] = round(shore_km, 1)
        s, e = (r0 - ra, c0 - ca), (r1 - ra, c1 - ca)
        if cost.size > WINDOW_BUDGET:
            # pooled first, by the cheapest cell so no valley closes; then refined
            # inside a corridor round that path
            h, w = cost.shape[0] // DOWN * DOWN, cost.shape[1] // DOWN * DOWN
            pooled = cost[:h, :w].reshape(h // DOWN, DOWN, w // DOWN, DOWN).min(axis=(1, 3)) * DOWN
            s4 = (min(s[0] // DOWN, pooled.shape[0] - 1), min(s[1] // DOWN, pooled.shape[1] - 1))
            e4 = (min(e[0] // DOWN, pooled.shape[0] - 1), min(e[1] // DOWN, pooled.shape[1] - 1))
            idx4, _ = route_through_array(pooled, s4, e4, fully_connected=True, geometric=True)
            seed = np.zeros(cost.shape, bool)
            a4 = np.array(idx4) * DOWN + DOWN // 2
            seed[np.clip(a4[:, 0], 0, cost.shape[0] - 1), np.clip(a4[:, 1], 0, cost.shape[1] - 1)] = True
            seed[s] = seed[e] = True
            k = int(REFINE_KM * 1000 / RES)
            cor = ndimage.binary_dilation(seed, iterations=k) if k < 60 else \
                ndimage.distance_transform_edt(~seed) <= k
            c2 = np.where(cor, cost, np.inf).astype(np.float32)
            idx, total = route_through_array(c2, s, e, fully_connected=True, geometric=True)
            info["pooled"] = True
        else:
            idx, total = route_through_array(cost, s, e, fully_connected=True, geometric=True)
        idx = np.array(idx)
        rr, cc = idx[:, 0] + ra, idx[:, 1] + ca
        # what the line runs over
        onland = np.asarray(T.land[rr, cc]).astype(bool)
        onice = np.asarray(T.ice[rr, cc]).astype(bool) & onland
        g = T.ground_km(ra, rb, ca, cb)[idx[:, 0], idx[:, 1]]
        steps = np.hypot(np.diff(rr), np.diff(cc)) * g[1:]
        info.update(km=float(steps.sum()), land_km=float(steps[onland[1:]].sum()),
                    ice_km=float(steps[onice[1:]].sum()),
                    max_elev=float(np.asarray(T.dem[rr, cc]).max()),
                    max_slope=float(np.asarray(T.slope[rr, cc]).max()), cost=float(total))
        if cd is not None:
            info["mean_off_map_km"] = float((cd[idx[:, 0], idx[:, 1]] * RES / 1000.0).mean())
        # from a staircase to a line, in the grid plane
        xy = np.column_stack([cc.astype(float), rr.astype(float)])
        xy = xy[simplify_xy(xy, 300.0 / RES)]
        xy = chaikin(xy, 2)
        xy = xy[simplify_xy(xy, 500.0 / RES)]
        lat, lon = T.ll_array(xy[:, 1], xy[:, 0])
        pts = [p] + [(float(a), float(b)) for a, b in zip(lat[1:-1], lon[1:-1])] + [q]
        return pts, info

    def route_track(self, row, digitized=None, moves=()):
        wps_raw = apply_moves(waypoints_raw(row), moves)
        wps = [(float(w["lat"]), float(w["lon"])) for w in wps_raw]
        dates = leg_dates(row, wps_raw)
        text = " ".join([row["title"] or "", row["description"] or "", row["tags"] or ""]).lower()
        boat = any(w in text for w in BOAT_WORDS)
        # the waypoints the shoreline puts on land though their notes name water
        shore = [self.shore_cell(p) if note_names_water(w.get("note")) else None
                 for p, w in zip(wps, wps_raw)]
        line, legs = [wps[0]], []
        t0 = time.time()
        for i in range(len(wps) - 1):
            corr = None
            if digitized and i < len(digitized["legs"]) and digitized["legs"][i]["source"] == "ink":
                corr = digitized["legs"][i]["ll"]
            seg, info = self.route_leg(wps[i], wps[i + 1], dates[i][1], ice_allowed(row, wps_raw, i), corr, boat,
                                       (shore[i], shore[i + 1]))
            info["leg"] = i
            info["straight_km"] = gc_km(wps[i], wps[i + 1])
            legs.append(info)
            line += seg[1:]
        return line, legs, time.time() - t0, wps_raw


# ------------------------------------------------------------- database
def db_ro():
    import sqlite3
    c = sqlite3.connect(f"file:{ROOT / 'db' / 'history' / 'history.sqlite'}?mode=ro", uri=True, timeout=60)
    c.row_factory = sqlite3.Row
    return c


def read_row(aid):
    return db_ro().execute("SELECT * FROM artifacts WHERE id=?", (aid,)).fetchone()


def read_places():
    out = {}
    for r in db_ro().execute("SELECT name, historic, lat, lon FROM places WHERE lat IS NOT NULL"):
        out[r["name"].lower()] = (float(r["lat"]), float(r["lon"]))
        if r["historic"]:
            out.setdefault(r["historic"].lower(), (float(r["lat"]), float(r["lon"])))
    return out


def waypoints_raw(row):
    try:
        w = json.loads(row["waypoints"] or "[]")
    except json.JSONDecodeError:
        return []
    return [p for p in w if isinstance(p, dict) and p.get("lat") is not None and p.get("lon") is not None]


def waypoints_of(row):
    return [(float(p["lat"]), float(p["lon"])) for p in waypoints_raw(row)]


INFERRED_WORDS = ("inferred", "approximate", "approx.", "unmapped", "position uncertain", "placed by")
WATER_WORDS = ("sound", "fiord", "fjord", "bay ", "bay,", "bay;", "channel", "strait", "sea ice", "the ice",
               "pack", "floe", "off ", "inlet", "basin", "harbour",
               # Sverdrup's names, which half this collection keeps in Norwegian:
               # a sund is a sound and a fjorden a fiord ("sund" alone would take
               # Sunday with it)
               "sundet", "sund ", "sund,", "sund;", "fjorden")
# a note that names the shore itself, or a thing standing on it, is not a note
# that puts the party on the water
LAND_WORDS = ("hut", "post", "camp", "cairn", "depot", "point", "cape", "shore", "coast", "island", "land")


def note_names_water(note):
    """True when a waypoint's own note says the party was on the water (or its
    ice) and says nothing of the shore."""
    note = (note or "").lower()
    return any(k in note for k in WATER_WORDS) and not any(k in note for k in LAND_WORDS)


def load_moves(track_id):
    """Waypoint moves for a track: digitized/<id>.moves.json, a list of
    {"index", "lat", "lon", "why"}; the owner's own or the tool's proposals
    once accepted (renamed from .moves.proposed.json)."""
    p = DIGIT / f"{track_id}.moves.json"
    if not p.exists():
        return []
    return json.loads(p.read_text()).get("moves", [])


def apply_moves(wps_raw, moves):
    """The waypoints with the moves applied; the original position is kept in
    the entry as 'was'."""
    out = [dict(w) for w in wps_raw]
    for m in moves:
        i = int(m["index"])
        if 0 <= i < len(out):
            w = out[i]
            if "was" not in w:
                w["was"] = [float(w["lat"]), float(w["lon"])]
            w["lat"], w["lon"] = float(m["lat"]), float(m["lon"])
            w["moved_why"] = m.get("why", "")
    return out


def nearest_on_line(p, line):
    """The nearest point of a (lat, lon) polyline to p, and its distance in km."""
    if len(line) < 2:
        return None, math.inf
    lat0 = p[0]
    ky, kx = 111.0, 111.0 * max(0.05, math.cos(math.radians(lat0)))
    P = np.array([p[1] * kx, p[0] * ky])
    Q = np.array([[q[1] * kx, q[0] * ky] for q in line])
    A, B = Q[:-1], Q[1:]
    D = B - A
    L2 = np.maximum((D * D).sum(1), 1e-12)
    t = np.clip(((P - A) * D).sum(1) / L2, 0.0, 1.0)
    proj = A + t[:, None] * D
    d = np.hypot(*(P - proj).T)
    i = int(np.argmin(d))
    return (float(proj[i, 1] / ky), float(proj[i, 0] / kx)), float(d[i])


def waypoint_diagnostics(T, wps_raw, digitized):
    """Per waypoint: the ground it sits on, its elevation, its distance from
    the digitized ink, whether its note calls it inferred, and whether its
    ground contradicts its note.  A waypoint that is inferred or contradicted
    and more than 5 km from the ink gets a proposed move to the nearest point
    of the ink, when that is within 25 km."""
    # the ink alone: a leg's chain starts and ends at the waypoint itself, and
    # that stub is not the drawn line
    ink = []
    if digitized:
        for lg in digitized["legs"]:
            if lg["source"] == "ink" and len(lg["ll"]) > 3:
                ink.append(lg["ll"][1:-1])
    out = []
    for i, w in enumerate(wps_raw):
        p = (float(w["lat"]), float(w["lon"]))
        note = (w.get("note") or "").lower()
        d = dict(index=i, lat=p[0], lon=p[1], note=w.get("note", "")[:80])
        if T.holds(p):
            r, c = T.rc(*p)
            land = bool(T.land[r, c])
            ice = bool(T.ice[r, c]) and land
            d.update(ground="ice cap" if ice else ("land" if land else "sea"),
                     elevation=float(T.dem[r, c]))
        else:
            d.update(ground="outside the DEM", elevation=None)
        d["inferred"] = any(k in note for k in INFERRED_WORDS)
        d["contradicted"] = d["ground"] in ("land", "ice cap") and note_names_water(note)
        if ink:
            q, dk = None, math.inf
            for part in ink:
                q2, d2 = nearest_on_line(p, part)
                if d2 < dk:
                    q, dk = q2, d2
            d["km_from_ink"] = dk
            if (d["inferred"] or d["contradicted"]) and 5.0 < dk < 25.0 and 0 < i < len(wps_raw) - 1 \
                    and "was" not in w:
                d["proposed"] = dict(index=i, lat=round(q[0], 4), lon=round(q[1], 4),
                                     why=f"{'inferred' if d['inferred'] else 'on land though the note names water'}; "
                                         f"moved {dk:.0f} km onto the printed route")
        out.append(d)
    return out


def geometry_of(row):
    try:
        g = json.loads(row["geometry"] or "null")
    except json.JSONDecodeError:
        return []
    if not isinstance(g, dict) or g.get("type") != "LineString":
        return []
    return [(float(y), float(x)) for x, y in g.get("coordinates", [])]


TRACK_COLS = ("creator", "description", "source_url", "download_url", "local_file",
              "licence", "credit", "bibkey", "pages", "language", "view_file",
              "people", "tags", "waypoints", "rights_note")


def write_row(c, row, routing, geometry, moved=()):
    """The sea router's writer: every field of the row as it stands, plus the
    flag and the line.  waypoints pass through unchanged unless a move was
    applied, in which case the moved waypoint carries its new position, its
    note says so with the old position, and the description gains a sentence
    listing the moves and their evidence."""
    import arctic_history as H
    kw = {k: row[k] for k in TRACK_COLS if k in row.keys() and row[k] is not None}
    kw.update(date=row["date_text"], date_end=row["date_end"], lat=row["lat"], lon=row["lon"], routing=routing)
    kw["geometry"] = json.dumps(geometry, ensure_ascii=False)
    if moved:
        wps = json.loads(row["waypoints"])
        said = []
        for m in moved:
            w = wps[m["index"]]
            w["lat"], w["lon"] = round(float(m["lat"]), 4), round(float(m["lon"]), 4)
            w["note"] = (w.get("note", "").rstrip() +
                         f" (position moved to the printed route and the terrain, {m['why']}; "
                         f"was {m['was'][0]:.3f}, {m['was'][1]:.3f})")
            said.append(f"waypoint {m['index'] + 1} ({m['why']}; before {m['was'][0]:.3f} N "
                        f"{abs(m['was'][1]):.3f} W)")
        kw["waypoints"] = json.dumps(wps, ensure_ascii=False)
        kw["description"] = ((row["description"] or "").rstrip() +
                             " The line is routed through the terrain from the expedition's printed route map "
                             "and the elevation model, and these waypoints, whose positions were inferred, were "
                             "moved to where the map and the terrain put them: " + "; ".join(said) + ".")
    H.add_artifact(c, row["id"], row["topic"], row["type"], row["title"], **kw)


def as_geojson(line):
    return {"type": "LineString", "coordinates": [[round(lo, 5), round(la, 5)] for la, lo in line]}


# --------------------------------------------------------------- figures
def _font(size):
    from PIL import ImageFont
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            pass
    return ImageFont.load_default()


C_OLD, C_DIG, C_NEW, C_WP, C_STRAIGHT = (86, 186, 246), (60, 200, 90), (255, 205, 66), (255, 255, 255), (168, 66, 66)


def terrain_figure(T, track_id, title, wps, old, new, digitized, legs, path, width=1800):
    """A hillshade of the track's ground with the old line, the digitized line
    and the routed one."""
    from PIL import Image, ImageDraw
    pts = [p for p in wps + old + new if T.holds(p)]
    if len(pts) < 2:
        return None
    rc = np.array([T.rcf(*p) for p in pts])
    m = max(80, int(0.08 * max(np.ptp(rc[:, 0]), np.ptp(rc[:, 1]))))
    ra, rb = max(0, int(rc[:, 0].min()) - m), min(T.nrows, int(rc[:, 0].max()) + m)
    ca, cb = max(0, int(rc[:, 1].min()) - m), min(T.ncols, int(rc[:, 1].max()) + m)
    ss = max(1, int(math.ceil((cb - ca) / width)))
    hs = T.hillshade(ra, rb, ca, cb)
    land = np.asarray(T.land[ra:rb, ca:cb]).astype(bool)
    ice = np.asarray(T.ice[ra:rb, ca:cb]).astype(bool) & land
    dem = np.asarray(T.dem[ra:rb, ca:cb])
    base = np.empty(hs.shape + (3,), np.float32)
    t = np.clip(dem / 1500.0, 0, 1)[..., None]
    base[:] = np.array([120, 140, 90], np.float32) * (1 - t) + np.array([170, 150, 120], np.float32) * t
    base[ice] = (225, 232, 240)
    base[~land] = (30, 45, 70)
    img = base * (0.45 + 0.75 * hs[..., None])
    img[~land] = base[~land]
    img = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    if ss > 1:
        img = img.resize((img.width // ss, img.height // ss), Image.LANCZOS)
    d = ImageDraw.Draw(img)

    def xy(p):
        r, c = T.rcf(*p)
        return ((c - ca) / ss, (r - ra) / ss)
    for line, col, w in ((old, C_OLD, 2), (digitized, C_DIG, 2), (new, C_NEW, 3)):
        if line and len(line) > 1:
            d.line([xy(p) for p in line], fill=col, width=w, joint="curve")
    for p in wps:
        x, y = xy(p)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=C_WP, outline=(0, 0, 0))
    f = _font(16)
    d.rectangle([0, 0, img.width, 46], fill=(10, 16, 26))
    d.text((8, 4), f"{track_id}: {title[:90]}", fill=(245, 245, 245), font=f)
    d.text((8, 24), "yellow: routed through the terrain   green: digitized from the printed map   "
                    "blue: the line in the database   white: waypoints   pale: ice cap", fill=(200, 205, 210), font=f)
    kmpx = RES * ss / 1000.0
    L = 50.0 / kmpx
    d.line([(20, img.height - 20), (20 + L, img.height - 20)], fill=(255, 255, 255), width=3)
    d.text((20, img.height - 40), "50 km", fill=(255, 255, 255), font=f)
    img.save(path)
    return img.size


def map_figure(map_id, g, rep, track_id, title, wps, old, new, digitized, path):
    """The scan with the digitized chain, the routed line and the waypoints."""
    from PIL import Image, ImageDraw
    img, _ = load_image(map_id, rep["rotate"])
    img = Image.blend(img, Image.new("RGB", img.size, (255, 255, 255)), 0.4)
    d = ImageDraw.Draw(img)

    def xy(line):
        px, py = g.to_px([p[1] for p in line], [p[0] for p in line])
        return [(float(x), float(y)) for x, y in zip(px, py)]
    for line, col, w in ((old, (60, 140, 230), 2), (digitized, (40, 170, 70), 3), (new, (230, 160, 20), 3)):
        if line and len(line) > 1:
            d.line(xy(line), fill=col, width=w, joint="curve")
    f = _font(14)
    for i, (x, y) in enumerate(xy(wps)):
        d.ellipse([x - 5, y - 5, x + 5, y + 5], outline=(200, 0, 0), width=2)
        d.text((x + 6, y - 7), str(i), fill=(160, 0, 0), font=f)
    # crop to the lines with a margin, then the caption
    allp = xy(wps + old + new)
    xs, ys = [p[0] for p in allp], [p[1] for p in allp]
    m = 0.15 * max(max(xs) - min(xs), max(ys) - min(ys)) + 60
    box = (max(0, int(min(xs) - m)), max(0, int(min(ys) - m)), min(img.width, int(max(xs) + m)),
           min(img.height, int(max(ys) + m)))
    img = img.crop(box)
    if img.width > 2400:
        img = img.resize((2400, int(img.height * 2400 / img.width)), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width, 30], fill=(255, 255, 255))
    d.text((8, 6), f"{track_id} on {map_id}: orange routed, green digitized from the ink, blue the line in the "
                   f"database, red circles the waypoints", fill=(0, 0, 0), font=_font(16))
    img.save(path)


# ------------------------------------------------------------- the verdict
def verdict(rec):
    bits = []
    legs = rec["legs"]
    fb = [l for l in legs if l.get("fallback") and l["fallback"] != "same cell"]
    sea = [l for l in fb if l.get("sea_router")]
    if fb:
        bits.append(f"{len(fb)} of {len(legs)} legs lie outside the DEM" +
                    (f", {len(sea)} of them routed through water by the sea router" if sea else "") +
                    (f", {len(fb) - len(sea)} left as great circles" if len(sea) < len(fb) else ""))
    if rec.get("digitized"):
        n_ink = rec["digitized_ink_legs"]
        bits.append(f"{n_ink} of {len(legs)} legs follow ink digitized from {rec['map']} "
                    f"(georef rms {rec['georef_rms_km']:.1f} km)"
                    + (f", {rec['digitized_doubtful_legs']} chained through hachures or lettering and doubted"
                       if rec.get("digitized_doubtful_legs") else ""))
        offs = [l["mean_off_map_km"] for l in legs if "mean_off_map_km" in l]
        if offs:
            bits.append(f"the routed line runs {np.mean(offs):.1f} km from the printed one on average")
    land = sum(l.get("land_km", 0) for l in legs)
    ice = sum(l.get("ice_km", 0) for l in legs)
    km = sum(l.get("km", l.get("straight_km", 0)) for l in legs)
    bits.append(f"{km:,.0f} km routed against {rec['straight_km']:,.0f} km straight, "
                f"{land:,.0f} km over land, {ice:,.0f} km over ice cap, "
                f"highest {max((l.get('max_elev', 0) for l in legs), default=0):.0f} m")
    if rec["old_km"]:
        bits.append(f"the line in the database is {rec['old_km']:,.0f} km and {rec['old_points']} points; "
                    f"this one {rec['points']} points")
    det = [l for l in legs
           if not l.get("corridor") and not l.get("fallback")
           and l.get("km", 0.0) > DETOUR_FACTOR * l.get("straight_km", 0.0)
           and l.get("km", 0.0) - l.get("straight_km", 0.0) > DETOUR_KM]
    if det:
        bits.append("legs held by no ink that the terrain lengthens by more than a quarter, to look at: " + "; ".join(
            f"{l['leg']} ({l['straight_km']:,.0f} km straight, {l['km']:,.0f} routed)" for l in det))
    diag = rec.get("diagnostics") or []
    odd = [d for d in diag if d.get("contradicted")]
    if odd:
        bits.append("waypoints on land whose note names water: " + ", ".join(str(d["index"]) for d in odd))
    if rec.get("waypoints_moved"):
        bits.append("waypoints moved: " + "; ".join(
            f"{m['index']} ({m['why']})" for m in rec["waypoints_moved"]))
    if rec.get("proposed_moves"):
        bits.append("proposed moves, not applied: " + "; ".join(
            f"{m['index']} ({m['why']})" for m in rec["proposed_moves"]))
    if rec.get("old_max_km") is not None:
        bits.append(f"it runs {rec['old_mean_km']:.1f} km from the line in the database on average and "
                    f"{rec['old_max_km']:.0f} km at most")
    if fb and len(fb) == len(legs):
        rec["grade"] = "outside"
        bits.append("every leg is outside the DEM, so this is not the terrain router's track: leave it as-given")
    elif rec.get("old_max_km") is not None and rec["old_max_km"] < 3.0:
        if rec.get("routing_before") == "terrain":
            rec["grade"] = "written"
            bits.append("this line is already in the database, flagged terrain")
        else:
            rec["grade"] = "same"
            bits.append("the same line as the database holds to within 3 km (a journey over the sea ice routes "
                        "straight), so there is nothing to write back")
    elif fb:
        rec["grade"] = "review"
        bits.append("the legs outside the DEM are the sea router's water paths or great circles, which is right "
                    "over the sea ice; review the rest")
    elif rec.get("digitized") and (rec["digitized_ink_legs"] < 0.5 * len(legs)
                                   or rec.get("digitized_doubtful_legs", 0) > 0.2 * len(legs)):
        rec["grade"] = "review"
    else:
        rec["grade"] = "recommend"
    spec = MAPS.get(rec.get("map") or "", {})
    if spec.get("grade_cap") and rec["grade"] == "recommend":
        rec["grade"] = spec["grade_cap"]
        bits.append(spec.get("note", "the map is not to be trusted for this"))
    return "; ".join(bits)


def render_summary(recs, georefs, meta, path):
    L = ["# Routing the overland tracks through the terrain", "",
         f"{meta['run']} — {meta.get('this_run', len(recs))} tracks routed in {meta['seconds']:.0f} s, "
         f"{len(recs)} on file from this and earlier runs. Command: `{meta['cmd']}`", "",
         "**Written to the database.**" if meta.get("wrote") else "**The database was not written to** "
         "(`--write` is off).", "",
         "## The DEM", "",
         f"Copernicus GLO-90, mosaicked at {RES:g} m in `{PROJ}` ({meta['shape'][1]} x {meta['shape'][0]} cells), "
         "with land from GSHHG full resolution and ice from Natural Earth 10 m glaciated areas.  See the "
         "tool's docstring for the cost surface.", "",
         "## The maps", "",
         "| map | family | parameters | points | rms px | rms km | worst px | km/px | fit |", "|---|---|---|---|---|---|---|---|---|"]
    for m in georefs:
        L.append(f"| {m['map']} | {m['family']} | {m['params']} | {m['n']} | {m['rms_px']:.1f} | {m['rms_km']:.1f} | "
                 f"{m['max_px']:.1f} | {m['km_per_px']:.2f} | {'accepted' if m['accepted'] else 'REFUSED'} |")
    grades = {}
    for r in recs:
        grades.setdefault(r["grade"], []).append(r)
    fitted = {m["map"] for m in georefs}
    L += ["", "Maps in the candidate list with no track digitized from them: " + "; ".join(
        f"**{mid}**: {MAP_NOTES.get(mid, 'no control points read yet')}"
        for mid in MAPS if mid not in fitted or mid in MAP_NOTES), ""]
    L += ["", "## The grades", "",
          "- **recommend** — every leg routed inside the DEM, and where a printed map was digitized at least "
          "half the legs follow its ink: a line to write back once the owner has looked at it.",
          "- **review** — some legs fall outside the DEM (great circles there, which is right over the sea "
          "ice) or fewer than half follow the ink.",
          "- **same** — the routed line is the database's line to within 3 km: nothing to write back.",
          "- **outside** — every leg outside the DEM: not this tool's track.",
          "- **written** — already in the database with this line, flagged terrain.", "",
          " · ".join(f"{g}: {len(v)}" for g, v in sorted(grades.items())), "",
          "## Every track", "",
          "| track | grade | legs | from ink | routed km | straight km | land km | ice km | highest m | "
          "from db line, max km | moved | s |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    order = {"written": 0, "recommend": 1, "review": 2, "same": 3, "outside": 4}
    for r in sorted(recs, key=lambda r: (order.get(r["grade"], 9), r["id"])):
        legs = r["legs"]
        old = f"{r['old_max_km']:.0f}" if r.get("old_max_km") is not None else "-"
        L.append(f"| {r['id']} | {r['grade']} | {len(legs)} | {r.get('digitized_ink_legs', 0)} | "
                 f"{sum(l.get('km', 0) for l in legs):,.0f} | {r['straight_km']:,.0f} | "
                 f"{sum(l.get('land_km', 0) for l in legs):,.0f} | {sum(l.get('ice_km', 0) for l in legs):,.0f} | "
                 f"{max((l.get('max_elev', 0) for l in legs), default=0):.0f} | {old} | "
                 f"{len(r.get('waypoints_moved') or [])} | {r['seconds']:.1f} |")
    L += ["", "## Verdicts", ""]
    for r in sorted(recs, key=lambda r: (order.get(r["grade"], 9), r["id"])):
        L.append(f"- **{r['id']}** ({r['grade']}) — {r['title']}  \n  {r['verdict']}")
    L += ["", "## Waypoints that look misplaced", "",
          "A waypoint on land whose note names water, or one whose note calls it inferred and that lies more "
          "than 5 km from the digitized ink.  A proposed move is written to "
          "`digitized/<track>.moves.proposed.json`; renaming it to `<track>.moves.json` applies it on the next "
          "run, and `--write` then moves the waypoint with its note and the description saying so.", ""]
    for r in recs:
        odd = [d for d in (r.get("diagnostics") or []) if d.get("contradicted") or "proposed" in d]
        for d in odd:
            L.append(f"- {r['id']} waypoint {d['index']}: {d['ground']}"
                     + (f" at {d['elevation']:.0f} m" if d.get("elevation") else "")
                     + (f", {d['km_from_ink']:.0f} km from the ink" if "km_from_ink" in d else "")
                     + (f"; proposed {d['proposed']['lat']:.3f} {d['proposed']['lon']:.3f} ({d['proposed']['why']})"
                        if "proposed" in d else "")
                     + f" — {d['note']}")
    L.append("")
    path.write_text("\n".join(L), encoding="utf-8")


def render_gallery(path):
    """gallery.html from everything on disk: the maps' check figures and the
    tracks' figures with their verdicts."""
    import html
    fc = json.loads((OUT / "routes.geojson").read_text()) if (OUT / "routes.geojson").exists() else {"features": []}
    recs = [f["properties"] for f in fc["features"]]
    maps = []
    for p in sorted(GEOREF.glob("*.georef.json")):
        maps.append(json.loads(p.read_text()))
    H = ["<!doctype html><html><head><meta charset='utf-8'><title>Terrain routing</title>",
         "<style>body{margin:0;background:#111;color:#ddd;font:15px sans-serif} nav{position:sticky;top:0;"
         "background:#111e;padding:8px 16px;border-bottom:1px solid #333} a{color:#ffd54a} h2{margin:28px 16px 6px;"
         "font-weight:normal} p{margin:4px 16px 10px;max-width:1400px} img{display:block;width:100%;height:auto}"
         ".grade{padding:2px 8px;border-radius:4px;font-size:13px} .recommend{background:#1d5c2e} "
         ".review{background:#6b5410} .outside{background:#444} .same{background:#2a3f5c} .written{background:#5c1d5c} "
         "table{margin:4px 16px;border-collapse:collapse;font-size:13px}"
         " td,th{padding:2px 8px;border-bottom:1px solid #333;text-align:left} details{margin:4px 16px}"
         " summary{cursor:pointer;color:#aaa}</style></head><body>",
         "<nav><b>Terrain routing</b> — yellow/orange: routed through the terrain · green: digitized from the "
         "printed map · blue: the line in the database · white/red: waypoints. "
         "<a href='#index'>index</a> · <a href='#maps'>maps</a> · <a href='summary.md'>summary.md</a></nav>"]
    order = {"written": 0, "recommend": 1, "review": 2, "same": 3, "outside": 4}
    recs.sort(key=lambda r: (order.get(r["grade"], 9), r["id"]))
    H.append("<h2 id='index'>Every track, by grade</h2><table><tr><th>track</th><th>grade</th><th>title</th>"
             "<th>routed km</th><th>land km</th><th>ice km</th><th>from db line, max km</th><th>moved</th></tr>")
    for r in recs:
        legs = r["legs"]
        H.append(f"<tr><td><a href='#{html.escape(r['id'])}'>{html.escape(r['id'])}</a></td>"
                 f"<td><span class='grade {r['grade']}'>{r['grade']}</span></td><td>{html.escape(r['title'][:70])}</td>"
                 f"<td>{sum(l.get('km', 0) for l in legs):,.0f}</td><td>{sum(l.get('land_km', 0) for l in legs):,.0f}</td>"
                 f"<td>{sum(l.get('ice_km', 0) for l in legs):,.0f}</td>"
                 + (f"<td>{r['old_max_km']:.0f}</td>" if r.get("old_max_km") is not None else "<td>-</td>")
                 + f"<td>{len(r.get('waypoints_moved') or [])}</td></tr>")
    H.append("</table>")
    for r in recs:
        H.append(f"<h2 id='{html.escape(r['id'])}'>{html.escape(r['id'])} <span class='grade {r['grade']}'>"
                 f"{r['grade']}</span> — {html.escape(r['title'])}</h2>")
        H.append(f"<p>{html.escape(r['verdict'])}</p>")
        diag = r.get("diagnostics") or []
        if diag:
            H.append("<details><summary>waypoints: ground, elevation, distance from the ink, proposals</summary>"
                     "<table><tr><th>#</th><th>lat</th><th>lon</th><th>ground</th><th>m</th><th>km from ink</th>"
                     "<th>flags</th><th>note</th></tr>")
            for d in diag:
                flags = ", ".join(k for k in ("inferred", "contradicted") if d.get(k))
                if "proposed" in d:
                    flags += f"; proposed {d['proposed']['lat']:.3f} {d['proposed']['lon']:.3f}"
                H.append(f"<tr><td>{d['index']}</td><td>{d['lat']:.3f}</td><td>{d['lon']:.3f}</td><td>{d['ground']}</td>"
                         + (f"<td>{d['elevation']:.0f}</td>" if d.get("elevation") is not None else "<td>-</td>")
                         + (f"<td>{d['km_from_ink']:.0f}</td>" if "km_from_ink" in d else "<td>-</td>")
                         + f"<td>{html.escape(flags)}</td><td>{html.escape(d['note'])}</td></tr>")
            H.append("</table></details>")
        fig_t = FIGS / f"{r['id']}-terrain.png"
        fig_m = FIGS / f"{r['id']}-map.png"
        if fig_t.exists():
            H.append(f"<img src='figures/{fig_t.name}' loading='lazy'>")
        if fig_m.exists():
            H.append(f"<img src='figures/{fig_m.name}' loading='lazy'>")
    H.append("<h2 id='maps'>The maps and their georeferences</h2>")
    fitted = {m["map"] for m in maps}
    H.append("<p>" + " ".join(
        f"<b>{html.escape(mid)}</b>: {html.escape(MAP_NOTES.get(mid, 'no control points read yet.'))}"
        for mid in MAPS if mid not in fitted or mid in MAP_NOTES) + "</p>")
    H.append("<table><tr><th>map</th><th>family</th><th>parameters</th><th>points</th><th>rms px</th><th>rms km</th>"
             "<th>worst px</th><th>km/px</th><th>fit</th></tr>")
    for m in maps:
        H.append(f"<tr><td><a href='#{m['map']}-georef'>{m['map']}</a></td><td>{m['family']}</td><td>"
                 f"{html.escape(json.dumps(m['params']))}</td><td>{m['n']}</td><td>{m['rms_px']:.1f}</td>"
                 f"<td>{m['rms_km']:.1f}</td><td>{m['max_px']:.1f}</td><td>{m['km_per_px']:.2f}</td>"
                 f"<td>{'accepted' if m['accepted'] else 'REFUSED'}</td></tr>")
    H.append("</table>")
    for m in maps:
        fig = FIGS / f"{m['map']}-georef.png"
        H.append(f"<h2 id='{m['map']}-georef'>{m['map']} — {m['family']} {html.escape(json.dumps(m['params']))}, "
                 f"rms {m['rms_px']:.1f} px = {m['rms_km']:.1f} km, {'accepted' if m['accepted'] else 'REFUSED'}</h2>")
        worst = sorted(m["points"], key=lambda c: -c["res_px"])[:3]
        H.append("<p>worst points: " + "; ".join(
            f"{html.escape(str(c.get('place') or (str(c['lon']) + ' ' + str(c['lat']))))} {c['res_px']:.1f} px"
            for c in worst) + "</p>")
        if fig.exists():
            H.append(f"<img src='figures/{fig.name}' loading='lazy'>")
    H.append("</body></html>")
    path.write_text("\n".join(H), encoding="utf-8")


# -------------------------------------------------------------------- main
def cmd_route(a):
    T = Terrain()
    R = Router(T)
    ro = db_ro()
    rows = {r["id"]: r for r in ro.execute("SELECT * FROM artifacts WHERE type='track' ORDER BY id")}
    if a.all:
        # every as-given or terrain track, and an unflagged one the sea
        # router's rule would call as-given
        decide = _load_route_tracks().decide
        want = [i for i, r in rows.items() if (r["routing"] or "") in ("as-given", "terrain")
                or (not (r["routing"] or "") and decide(r)[0] == "as-given")]
    else:
        want = list(a.track)
    missing = [i for i in want if i not in rows]
    if missing:
        raise SystemExit(f"no track {', '.join(missing)}")
    prev = {}
    if (OUT / "routes.geojson").exists() and not a.all:
        for f in json.loads((OUT / "routes.geojson").read_text())["features"]:
            prev[f["id"]] = f
    track_map = {t: m for m, spec in MAPS.items() for t in spec["tracks"]}
    t_start = time.time()
    feats = []
    for tid in want:
        row = rows[tid]
        wps = waypoints_of(row)
        if len(wps) < 2:
            print(f"{tid}: fewer than two waypoints, skipped", file=sys.stderr)
            continue
        dig = None if a.no_digitized else load_digitized(tid)
        moves = load_moves(tid)
        line, legs, secs, wps_raw = R.route_track(row, dig, moves)
        wps = [(float(w["lat"]), float(w["lon"])) for w in wps_raw]
        old = geometry_of(row)
        diag = waypoint_diagnostics(T, wps_raw, dig)
        proposed = [d["proposed"] for d in diag if "proposed" in d]
        if proposed:
            DIGIT.mkdir(parents=True, exist_ok=True)
            (DIGIT / f"{tid}.moves.proposed.json").write_text(json.dumps({"moves": proposed}, indent=1))
        rec = dict(id=tid, title=row["title"], topic=row["topic"], routing_before=row["routing"] or "",
                   waypoints=len(wps), points=len(line), legs=legs, seconds=round(secs, 1),
                   straight_km=line_km(wps), routed_km=line_km(line), old_km=line_km(old) if old else 0.0,
                   old_points=len(old), diagnostics=diag, moves=moves, proposed_moves=proposed,
                   waypoints_moved=[dict(index=i, lat=w["lat"], lon=w["lon"], was=w["was"], why=w.get("moved_why", ""))
                                    for i, w in enumerate(wps_raw) if "was" in w])
        if dig:
            rec.update(digitized=True, map=dig["map"], digitized_ink_legs=sum(1 for l in dig["legs"] if l["source"] == "ink"),
                       digitized_doubtful_legs=sum(1 for l in dig["legs"] if l["source"] == "ink-doubtful"))
            _, grep = load_georef(dig["map"])
            rec["georef_rms_km"] = grep["rms_km"] if grep else float("nan")
        if len(old) > 1 and len(line) > 1:
            mean_km, max_km, _ = _load_route_tracks().line_distance_km(line, old)
            rec.update(old_mean_km=mean_km, old_max_km=max_km)
        rec["verdict"] = verdict(rec)
        print(f"  {tid}: {len(wps)} waypoints -> {len(line)} points, {rec['routed_km']:,.0f} km, "
              f"{secs:.1f} s, {rec['grade']}", file=sys.stderr)
        if not a.no_figures:
            FIGS.mkdir(parents=True, exist_ok=True)
            digline = [p for lg in dig["legs"] for p in lg["ll"]] if dig else []
            terrain_figure(T, tid, row["title"], wps, old, line, digline, legs, FIGS / f"{tid}-terrain.png")
            mid = track_map.get(tid) or (dig["map"] if dig else None)
            if mid:
                g, grep = load_georef(mid)
                if g is not None:
                    map_figure(mid, g, grep, tid, row["title"], wps, old, line, digline, FIGS / f"{tid}-map.png")
        feats.append({"type": "Feature", "id": tid, "geometry": as_geojson(line),
                      "properties": {k: v for k, v in rec.items()}})
    for tid, f in prev.items():
        if tid not in {x["id"] for x in feats}:
            feats.append(f)
    feats.sort(key=lambda f: f["id"])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "routes.geojson").write_text(json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False))
    georefs = [json.loads(p.read_text()) for p in sorted(GEOREF.glob("*.georef.json"))]
    meta = dict(run=time.strftime("%Y-%m-%d %H:%M"), seconds=time.time() - t_start,
                cmd=" ".join(["python tools/digitize-tracks.py"] + sys.argv[1:]), wrote=a.write,
                shape=[T.nrows, T.ncols], this_run=len(want))
    render_summary([f["properties"] for f in feats], georefs, meta, OUT / "summary.md")
    render_gallery(OUT / "gallery.html")
    if a.write:
        import arctic_history as H
        c = H.connect(ROOT / "db" / "history" / "history.sqlite", create=False)
        n = 0
        for f in feats:
            if f["id"] not in want:
                continue
            row = rows[f["id"]]
            moved = f["properties"].get("waypoints_moved") or []
            write_row(c, row, "terrain", f["geometry"], moved)
            n += 1
        c.commit()
        print(f"--write: {n} rows written with routing=terrain", file=sys.stderr)
    else:
        print("the database was not written to (--write is off)", file=sys.stderr)
    print(f"{OUT.relative_to(ROOT)}/summary.md, routes.geojson and gallery.html written", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("dem", help="build the DEM mosaic cache")
    p.add_argument("--rebuild", action="store_true")
    p = sub.add_parser("crops", help="gridded crops of a map to read control points off")
    p.add_argument("--map", required=True)
    p.add_argument("--rotate", type=int, default=None, help="quarter turns anticlockwise to north-up")
    p.add_argument("--step", type=int, default=100)
    p.add_argument("--tile", type=int, default=600)
    p = sub.add_parser("georef", help="fit a map's projection from its control points")
    p.add_argument("--map", required=True)
    p.add_argument("--family", default=None, choices=FAMILIES)
    p.add_argument("--no-coast", action="store_true", help="skip the coastline refinement")
    p = sub.add_parser("digitize", help="extract the drawn route of a track from its map")
    p.add_argument("--map", required=True)
    p.add_argument("--track", action="append", default=[])
    p.add_argument("--ink", default=None, help="dots, dashes, solid or colour:red")
    p = sub.add_parser("route", help="route tracks through the terrain")
    p.add_argument("--track", action="append", default=[])
    p.add_argument("--all", action="store_true")
    p.add_argument("--no-figures", action="store_true")
    p.add_argument("--no-digitized", action="store_true", help="ignore a digitized line")
    p.add_argument("--write", action="store_true", help="ALSO write geometry and routing=terrain to the database")
    sub.add_parser("gallery", help="rebuild gallery.html from what is on disk")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.cmd == "dem":
        T = Terrain(build=a.rebuild)
        print(f"{T.ncols} x {T.nrows} cells at {RES:g} m; land {np.asarray(T.land).mean():.1%}, "
              f"ice {np.asarray(T.ice).mean():.1%}, highest {float(np.asarray(T.dem).max()):.0f} m", file=sys.stderr)
    elif a.cmd == "crops":
        paths, size = crops_sheet(a.map, a.step, a.tile, rotate=a.rotate)
        print(f"{a.map}: {size[0]} x {size[1]} px north-up, {len(paths)} crops in {GEOREF.relative_to(ROOT)}")
    elif a.cmd == "georef":
        georef_map(a.map, family=a.family, no_coast=a.no_coast)
        render_gallery(OUT / "gallery.html")
    elif a.cmd == "digitize":
        tracks = a.track or list(MAPS.get(a.map, {}).get("tracks", {}))
        for t in tracks:
            digitize_track(a.map, t, ink=a.ink)
    elif a.cmd == "route":
        if not (a.all or a.track):
            ap.error("give --all or --track ID")
        cmd_route(a)
    elif a.cmd == "gallery":
        render_gallery(OUT / "gallery.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
