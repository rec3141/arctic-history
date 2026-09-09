# Routing the voyage tracks through water: a prototype

A track artifact's `geometry` is its waypoints joined by straight lines, and
those lines cut across Baffin Island, Somerset, Greenland and the rest. This
folder is the routing tool, and the numbers and pictures from running it on
grid on 2026-09-09 against every track in the live database: 147 tracks, 91
routed, 56 skipped as sledge, overland, drift or retreat journeys.

    route_tracks.py     the tool (GDAL command-line tools + numpy, scipy, scikit-image, Pillow)
    routes.json         its output for the 91 routed tracks: waypoints, the straight line, the routed line, land fractions
    geojson/            one GeoJSON LineString per routed track, for history-db.py --geometry-file
    summary.md          land along the line for each track, straight and routed
    overview.png        every routed track (yellow) over its straight line (red) on the 1 km mask
    archipelago.png     the same, the Northwest Passage region
    three-voyages.png   Franklin 1845, the Gjoa and Parry's Fury and Hecla alone (an earlier 2 km run), so the routing can be read

Run on grid as

    export MAMBA_ROOT_PREFIX=~/micromamba; eval "$(~/bin/micromamba shell hook -s bash)"; micromamba activate routing
    python routing-scratch/route_tracks.py --db db/history/history.sqlite \
        --land /data/gis/shoreline/osm_box.gpkg --bbox=-180,35,15,86 --res 1000 \
        --coarse-land /data/gis/shoreline/gshhg_global_i.gpkg --coarse-bbox=-180,-60,180,86 --coarse-res 4000 \
        --out /data/gis/routing/runN --geojson-dir /data/gis/routing/runN/geojson

Two masks: a fine one at 1 km from the OpenStreetMap land polygons over the
North Atlantic and Arctic (-180..15 E, 35..86 N, 21707 by 15808 cells), and
a coarse one at 4 km from GSHHG intermediate over the globe to 60 S, for the
ocean legs outside it (the voyages by the Pacific). A segment goes on the
fine mask when both ends are in it, else the coarse one, else a great circle.
The run took 102 minutes; the long Atlantic legs dominate.

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
| of the line on land, mean over 91 tracks | 36 % | 3 % |
| points per track, mean | 20 | 48 |

What is left on land, in order of size (see summary.md), is almost all
journeys on foot, by sledge or by air that the word rule does not catch: the
Oxford Ellesmere sledge journeys of 1934-35, the RCMP patrols, the SHORAN
survey flights, the Netsilik journey to Akkoolee. Routed through water they
come out as staircases across the land, which is worse than the straight
line. Each track needs an explicit flag set by the research crew, not a
guess from its title; that is the one thing the tool cannot decide.

## What the full version needs

1. A per-track flag: routed through water, or drawn as given.
2. (Done.) The masks above: 1 km from the OSM polygons, with Bellot Strait
   and Fury and Hecla Strait open, and a 4 km global mask for the Pacific
   approaches.
4. The routed line written to `geometry`, `waypoints` untouched as the truth.
   The front end already draws `geometry` as the line and `waypoints` as the
   markers and table, so it needs no change.
5. The crew's review. The router picks the cheapest water path, not the
   historic one, and knows nothing about ice; where a voyage's channel is
   known, a waypoint forces it, which is how the data already works.
