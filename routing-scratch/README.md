# Routing the voyage tracks through water: a prototype

A track artifact's `geometry` is its waypoints joined by straight lines, and
those lines cut across Baffin Island, Somerset, Greenland and the rest. This
folder is a prototype that routes each pair of consecutive waypoints along
the least-cost water path over a land mask, with the numbers and pictures
from running it on every track in the database on 2026-09-08.

    route_tracks.py     the prototype (GDAL command-line tools + numpy, scipy, scikit-image, Pillow)
    routes.json         its output for the 59 routed tracks: waypoints, the straight line, the routed line, land fractions
    summary.md          land along the line for each track, straight and routed
    overview.png        every routed track (yellow) over its straight line (red) on the 2 km mask
    archipelago.png     the same, the Northwest Passage region
    three-voyages.png   Franklin 1845, the Gjoa and Parry's Fury and Hecla alone, so the routing can be read

Run as

    python3 routing-scratch/route_tracks.py --db db/history/history.sqlite \
        --land ne_10m_land.shp --land ne_10m_minor_islands.shp [--gebco gebco.tif] --out routing-out

with the Natural Earth 10 m land and minor-islands shapefiles (naciscdn.org,
8 MB); GEBCO is optional. The mask is Web Mercator at 2 km over the North
Atlantic and Arctic (-150..15 E, 35..86 N), 9184 by 7904 cells. Every track
takes a few seconds; all 59 take about six minutes.

## How it routes

- A water cell costs 1, plus a penalty that fades over about 15 km from any
  coast so a line stays offshore, plus 0.5 in water shallower than 50 m when
  GEBCO is given. A land cell costs 500, so a route crosses land only to
  reach a waypoint that sits on it.
- A waypoint in a land cell (a harbour, a camp on the shore) starts from the
  nearest water cell within 20 km.
- The least-cost path is scikit-image's `route_through_array` in a window
  around each segment.
- On open water a grid's least-cost path is a staircase of 45 and 90 degree
  moves that ties with the straight line, so each segment is then pulled
  straight wherever a straight line touches no land cell, and simplified to
  1 km. This runs within a segment, never across a waypoint: every waypoint
  stays on the line, and an out-and-back voyage keeps its far end.
- Tracks whose title or tags say sledge, overland, drift, retreat, ice
  journey, walk or march are skipped: those went over ice or land and must
  not be routed. 41 of the 100 tracks are skipped by that rule.

## What came out

| | straight lines | routed |
|---|---|---|
| of the line on land, mean over 59 tracks | 30 % | 3 % |
| points per track, mean | 20 | 46 |

What is left on land, in order of size (see summary.md):

- Voyages that went by the Pacific — Collinson's Enterprise, McClure's
  Investigator, the Karluk, the Polar Sea — have waypoints west of 150 W and
  south of 35 N, outside the mask, and those segments are left straight
  across the continent. The mask must cover the whole route, or those legs
  need a great-circle fallback and the mask a Pacific extension.
- Journeys on foot or by sledge that the word rule does not catch (the
  Netsilik journey to Akkoolee, Iligliuk's coast). Each track needs an
  explicit flag set by the research crew, not a guess from its title.
- Waypoints themselves in land cells and the short stub to them.

## What the full version needs

1. A per-track flag: routed through water, or drawn as given.
2. A finer mask, 500 m or 1 km, from a better shoreline. Bellot Strait and
   Fury and Hecla Strait are about 2 km wide and close at 2 km. The Natural
   Earth polygons keep them open when rasterized at 100 m, but Natural Earth
   "10 m" is 1:10 million scale, generalized to about a kilometre; GSHHG full
   resolution (about 150 MB) or the OSM land polygons (about 1 GB, clip on
   grid) would serve both the routing and the map's coastline, which is
   drawn from the same Natural Earth file today.
3. A mask that covers every route, including the Pacific approaches.
4. The routed line written to `geometry`, `waypoints` untouched as the truth.
   The front end already draws `geometry` as the line and `waypoints` as the
   markers and table, so it needs no change.
5. The crew's review. The router picks the cheapest water path, not the
   historic one, and knows nothing about ice; where a voyage's channel is
   known, a waypoint forces it, which is how the data already works.
