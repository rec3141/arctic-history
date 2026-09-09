#!/usr/bin/env python3
"""Prototype: route the History tab's voyage tracks through water.

A track artifact's geometry is its waypoints joined by straight lines, and
those lines cut across islands. This routes each pair of consecutive waypoints
along the least-cost water path over a land mask, and writes the result next
to the straight line so the two can be compared.

    route_tracks.py --db db/history/history.sqlite --land ne_10m_land.shp [--land ne_10m_minor_islands.shp]
                    [--gebco gebco.tif] [--res 2000] [--ids id,id,...] [--out routing-out]

Needs the GDAL command-line tools (ogr2ogr, gdal_rasterize, gdal_translate,
gdalwarp) and numpy, scipy, scikit-image and Pillow. The land polygons are
Natural Earth 10 m land (and minor islands); GEBCO is optional and only adds a
small cost to water shallower than 50 m.

The cost of a water cell is 1, plus a penalty that fades over ~15 km from any
coast so a line stays offshore, plus 0.5 in shallow water; a land cell costs
500, so a route crosses land only to reach a waypoint that sits on it. Each
waypoint is first snapped to the nearest water cell within 20 km (harbours and
coastal camps fall in a land cell at 2 km). The routed line is simplified to
1 km. Tracks whose tags or title say sledge, overland, drift, retreat or ice
journey are skipped: those went over ice or land and must not be routed.

Outputs, in --out: routes.json ({id: {title, waypoints, straight, routed,
straight_land_frac, routed_land_frac, seconds}}), overview.png (the whole
mask with every routed track), archipelago.png (the Northwest Passage
region), and summary.md (a table of the per-track land fractions).
"""
import argparse, json, math, os, sqlite3, subprocess, sys, time
import numpy as np
from scipy import ndimage
from skimage.graph import route_through_array
from PIL import Image, ImageDraw

M = 20037508.342789244; R = 6378137.0
SKIP_WORDS = ("sledge", "sledging", "overland", "drift", "ice-island", "ice journey", "retreat", "ski", "ride to", "across", "walk", "march")


def merc(lat, lon):
    return lon / 180 * M, R * math.log(math.tan(math.pi / 4 + math.radians(max(-85, min(85, lat))) / 2))


def unmerc(x, y):
    return math.degrees(2 * math.atan(math.exp(y / R)) - math.pi / 2), x / M * 180


def build_grids(out, lands, gebco, bbox, res):
    """Rasterize the land polygons (and warp GEBCO) onto one Mercator grid; ENVI
    raw files so numpy reads them without the GDAL Python bindings."""
    x0, y0 = merc(bbox[1], bbox[0]); x1, y1 = merc(bbox[3], bbox[2])
    te = ["-te", f"{x0:.1f}", f"{y0:.1f}", f"{x1:.1f}", f"{y1:.1f}", "-tr", str(res), str(res)]
    gpkg = os.path.join(out, "land3857.gpkg")
    if not os.path.exists(gpkg):
        for i, shp in enumerate(lands):
            subprocess.run(["ogr2ogr", "-q", "-t_srs", "EPSG:3857"] + (["-update"] if i else []) + [gpkg, shp, "-nln", f"land{i}"], check=True)
    tif = os.path.join(out, "land.tif")
    if not os.path.exists(tif):
        for i in range(len(lands)):
            subprocess.run(["gdal_rasterize", "-q", "-burn", "1", "-l", f"land{i}"] + ([] if i else te + ["-ot", "Byte", "-a_srs", "EPSG:3857"]) + [gpkg, tif], check=True)
    subprocess.run(["gdal_translate", "-q", "-of", "ENVI", tif, os.path.join(out, "land.bin")], check=True)
    ncols = int(round((x1 - x0) / res)); nrows = int(round((y1 - y0) / res))
    land = np.fromfile(os.path.join(out, "land.bin"), dtype=np.uint8).reshape(nrows, ncols).astype(bool)
    elev = None
    if gebco:
        ebin = os.path.join(out, "elev.bin")
        if not os.path.exists(ebin):
            subprocess.run(["gdalwarp", "-q", "-t_srs", "EPSG:3857"] + te + ["-r", "bilinear", "-ot", "Int16", "-of", "ENVI", "-multi", gebco, ebin], check=True)
        elev = np.fromfile(ebin, dtype=np.int16).reshape(nrows, ncols)
    gt = (x0, res, 0, y1, 0, -res)
    return land, elev, gt


def simplify(pts, tol_km):
    """Douglas-Peucker on (lat, lon) points, tolerance in km (flat, local)."""
    if len(pts) < 3:
        return pts
    def dist(p, a, b):
        ky = 111.0; kx = 111.0 * math.cos(math.radians(p[0]))
        ax, ay = (a[1] - p[1]) * kx, (a[0] - p[0]) * ky; bx, by = (b[1] - p[1]) * kx, (b[0] - p[0]) * ky
        dx, dy = bx - ax, by - ay
        if dx == dy == 0:
            return math.hypot(ax, ay)
        t = max(0.0, min(1.0, -(ax * dx + ay * dy) / (dx * dx + dy * dy)))
        return math.hypot(ax + t * dx, ay + t * dy)
    keep = [0, len(pts) - 1]; stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j - i < 2:
            continue
        k, d = max(((k, dist(pts[k], pts[i], pts[j])) for k in range(i + 1, j)), key=lambda t: t[1])
        if d > tol_km:
            keep.append(k); stack += [(i, k), (k, j)]
    return [pts[k] for k in sorted(keep)]


def line_of_sight(pts, land, rc, km):
    """Pull the route straight wherever it can be: from each kept point, jump to
    the farthest later point whose straight line touches no land cell. On open
    water a grid's least-cost path is a staircase of 45 and 90 degree moves
    that ties with the straight line; this takes the straight one."""
    def clear(a, b):
        (r0, c0), (r1, c1) = rc(*a), rc(*b)
        n = int(max(abs(r1 - r0), abs(c1 - c0))) + 1
        for f in np.linspace(0, 1, n + 1):
            r, c = int(round(r0 + f * (r1 - r0))), int(round(c0 + f * (c1 - c0)))
            if 0 <= r < land.shape[0] and 0 <= c < land.shape[1] and land[r, c]:
                return False
        return True
    out = [pts[0]]; i = 0
    while i < len(pts) - 1:
        j = len(pts) - 1
        while j > i + 1 and not clear(pts[i], pts[j]):
            j -= 1
        out.append(pts[j]); i = j
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True); ap.add_argument("--land", action="append", required=True)
    ap.add_argument("--gebco"); ap.add_argument("--res", type=float, default=2000.0)
    ap.add_argument("--bbox", default="-150,35,15,86", help="lon,lat,lon,lat of the mask")
    ap.add_argument("--ids"); ap.add_argument("--out", default="routing-out")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    bbox = [float(v) for v in a.bbox.split(",")]
    land, elev, gt = build_grids(a.out, a.land, a.gebco, bbox, a.res)
    print(f"grid {land.shape[1]}x{land.shape[0]} at {a.res:.0f} m, land fraction {land.mean():.2f}", file=sys.stderr)
    km = a.res / 1000.0
    dist = ndimage.distance_transform_edt(~land) * km
    cost = (1.0 + 3.0 * np.exp(-dist / 15.0)).astype(np.float32)
    if elev is not None:
        cost += np.where(elev > -50, 0.5, 0.0).astype(np.float32)
    cost[land] = 500.0
    _, nearest_water = ndimage.distance_transform_edt(land, return_indices=True)

    def rc(lat, lon):
        x, y = merc(lat, lon)
        return int((gt[3] - y) / a.res), int((x - gt[0]) / a.res)
    def ll(r, c):
        return unmerc(gt[0] + (c + 0.5) * a.res, gt[3] - (r + 0.5) * a.res)
    inside = lambda r, c: 0 <= r < land.shape[0] and 0 <= c < land.shape[1]

    db = sqlite3.connect(a.db); db.row_factory = sqlite3.Row
    rows = db.execute("select id, title, tags, waypoints from artifacts where type='track' order by id").fetchall()
    if a.ids:
        want = set(a.ids.split(",")); rows = [r for r in rows if r["id"] in want]
    results = {}
    for r in rows:
        words = (r["title"] + " " + (r["tags"] or "")).lower()
        if any(w in words for w in SKIP_WORDS):
            print(f"skip {r['id']}: {r['title'][:60]}", file=sys.stderr); continue
        wps = json.loads(r["waypoints"] or "[]")
        pts = [(float(w["lat"]), float(w["lon"])) for w in wps if w.get("lat") is not None and w.get("lon") is not None]
        if len(pts) < 2:
            continue
        t0 = time.time(); routed = []; s_land = s_n = 0
        for p, q in zip(pts, pts[1:]):
            for f in np.linspace(0, 1, 50):
                cell = rc(p[0] + f * (q[0] - p[0]), p[1] + f * (q[1] - p[1]))
                if inside(*cell): s_n += 1; s_land += int(land[cell])
            (r0, c0), (r1, c1) = rc(*p), rc(*q)
            if not (inside(r0, c0) and inside(r1, c1)):
                routed += [p, q]; continue                       # outside the mask: left straight (a great circle would be better)
            # a waypoint in a land cell starts from the nearest water within 20 km
            def snap(rr, cc):
                nr, nc = int(nearest_water[0][rr, cc]), int(nearest_water[1][rr, cc])
                return (nr, nc) if math.hypot(nr - rr, nc - cc) * km <= 20 else (rr, cc)
            (sr0, sc0), (sr1, sc1) = snap(r0, c0), snap(r1, c1)
            seg_km = km * math.hypot(r1 - r0, c1 - c0)
            m = int(max(400, 0.6 * seg_km) / km)
            ra, rb = max(0, min(sr0, sr1) - m), min(land.shape[0], max(sr0, sr1) + m + 1)
            ca, cb = max(0, min(sc0, sc1) - m), min(land.shape[1], max(sc0, sc1) + m + 1)
            idx, _ = route_through_array(cost[ra:rb, ca:cb], (sr0 - ra, sc0 - ca), (sr1 - ra, sc1 - ca), fully_connected=True, geometric=True)
            # straightened within the segment only: every waypoint stays on the line
            routed += line_of_sight([p] + [ll(rr + ra, cc + ca) for rr, cc in idx] + [q], land, rc, km)
        routed = simplify(routed, 1.0)
        r_land = r_n = 0                                        # land along the routed line, sampled every cell
        for p, q in zip(routed, routed[1:]):
            (r0, c0), (r1, c1) = rc(*p), rc(*q)
            for f in np.linspace(0, 1, int(max(abs(r1 - r0), abs(c1 - c0))) + 2):
                cell = (int(round(r0 + f * (r1 - r0))), int(round(c0 + f * (c1 - c0))))
                if inside(*cell): r_n += 1; r_land += int(land[cell])
        results[r["id"]] = {"title": r["title"], "waypoints": wps, "straight": pts, "routed": routed,
                            "straight_land_frac": round(s_land / max(1, s_n), 3), "routed_land_frac": round(r_land / max(1, r_n), 3),
                            "points": len(routed), "seconds": round(time.time() - t0, 1)}
        print(f"{r['id']}: {len(pts)} waypoints -> {len(routed)} points, land {s_land/max(1,s_n):.0%} -> {r_land/max(1,r_n):.0%}, {time.time()-t0:.1f}s", file=sys.stderr)
    json.dump(results, open(os.path.join(a.out, "routes.json"), "w"))

    # figures: the mask with every routed track (yellow) over its straight line (red)
    def draw(k, crop, name):
        img = Image.fromarray(np.where(land[::k, ::k], 70, 20).astype(np.uint8)).convert("RGB"); d = ImageDraw.Draw(img)
        for v in results.values():
            d.line([(c / k, rr / k) for rr, c in (rc(*p) for p in v["straight"])], fill=(220, 60, 60), width=1)
        for v in results.values():
            d.line([(c / k, rr / k) for rr, c in (rc(*p) for p in v["routed"])], fill=(255, 220, 60), width=2)
        if crop:
            (r0, c0), (r1, c1) = rc(crop[3], crop[0]), rc(crop[1], crop[2])
            img = img.crop((c0 // k, r0 // k, c1 // k, r1 // k))
        img.save(os.path.join(a.out, name))
    draw(8, None, "overview.png")
    draw(4, (-130, 60, -60, 78), "archipelago.png")
    with open(os.path.join(a.out, "summary.md"), "w") as fh:
        fh.write("| track | waypoints | routed points | on land, straight | on land, routed | s |\n|---|---|---|---|---|---|\n")
        for k, v in results.items():
            fh.write(f"| {k} | {len(v['straight'])} | {v['points']} | {v['straight_land_frac']:.0%} | {v['routed_land_frac']:.0%} | {v['seconds']} |\n")


if __name__ == "__main__":
    main()
